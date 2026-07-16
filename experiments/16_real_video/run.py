"""Experiment 16 -- issue #48 Phase 1: the certificate on real video.

Real hand-held walking video (carousel; provenance in data/README.md),
24 frames over 6 s. The declared protocol (posted to issue #48 before
implementation) in short:

  * held-out frames 4, 10, 16, 22 (pre-fixed); the other 20 train. All
    pipeline tuning used TRAIN frames only.
  * joint pose+splat fit (jointfit.py); held-out poses are optimized with
    the splats FROZEN against the held-out frame (standard NVS practice,
    declared).
  * PRECONDITION -- a HARD STOP in code (PR #59 review item 1): every
    seed's PRIMARY (blur-on) fit must reach mean train PSNR >= 18 dB
    (PSNR of the POOLED per-frame MSE, the aggregation fixed in
    tune.py), or main() returns before the held-out frames are even
    loaded. tune.py reproduces the round-1 tuning trajectory from
    committed code and never loads held-out frames either.
  * GATE B (primary): Spearman(sigma_pred, |residual|) pooled over the
    held-out frames' pixels, >= 0.3 on all 3 seeds. sigma_pred is the
    exp15 round-2 delta-method score with H built from TRAIN frames only
    (splat parameters + background; poses and global knobs fixed,
    eps = 1e-9 tr(H)/P).
  * GATE B2 (the candidate promoted from the exp15 review): sigma_pred
    must show a CONSISTENT uplift over the three DECLARED controls --
    |rendered| (amplitude, exactly as worded on the issue), row-norm of
    J (the H = I score), diagonal-H -- on every seed. The centered
    variant |render - b| is reported as an auxiliary (PR #59 review
    item 4) but does not enter the verdict. B passing with B2 failing
    reads "the certificate still does not separate from amplitude
    tracking on real video" and is recorded as such.
  * BLUR ABLATION: held-out MSE with the closed-form blur knob <= without,
    paired per seed; fitted sigma_blur reported.
  * Gates B/B2 are evaluated on the blur-ON fit (the declared Phase 1
    model includes the knob); the ablation is the with/without pair.

Falsification (declared): Gate B failing on real video reads "the
certificate does not survive occlusion + model mismatch" and sends the
work back to the renderer, not to the score.
"""
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "15_video_conf"))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from gauss3d import spearman  # noqa: E402
from jointfit import _cam, fit_pose, fit_video, psnr  # noqa: E402
from splatvid import frame_jacobian, render  # noqa: E402

HELD_OUT = (4, 10, 16, 22)          # pre-fixed in the declaration
K = 250
F0 = 78.0                            # iPhone wide prior; logf fitted
SEEDS = (0, 1, 2)
SHAPE = (54, 96)
FINAL_SCHEDULE = ((600, 0.02), (400, 0.006))
ITERS_A, ITERS_POSE, ITERS_WIN, WINDOW = 300, 60, 60, 5
ITERS_HO_POSE = 150
PSNR_FLOOR = 18.0
GATE_RHO = 0.3
EPS_FRAC = 1e-9


def load_train():
    """Train frames ONLY. tune.py and the pre-gate phase of run.py use
    this loader; the held-out frames live behind load_holdout(), which
    is called only after the precondition gate passes."""
    d = np.load(HERE / "data" / "carousel_frames.npz")
    return [d["fit"][i].ravel().astype(float) for i in range(24)
            if i not in HELD_OUT]


def load_holdout():
    d = np.load(HERE / "data" / "carousel_frames.npz")
    return [d["fit"][i].ravel().astype(float) for i in HELD_OUT]


def pixel_grid(shape):
    H, W = shape
    vs, us = np.meshgrid(np.arange(H, dtype=float),
                         np.arange(W, dtype=float), indexing="ij")
    return us.ravel(), vs.ravel()


def evaluate(st, poses, train_frames, ho_frames, ho_prev_pos, U, V):
    """Held-out pose fits, residuals, sigma_pred and controls."""
    H, W = SHAPE
    f = float(np.exp(st["logf"]))
    # H from TRAIN frames only
    P = 5 * len(st["w"]) + 1
    Hgn = np.zeros((P, P))
    for pos in range(len(train_frames)):
        J = frame_jacobian(st["mu"], st["s"], st["w"], st["b"],
                           _cam(poses[pos], f, SHAPE, U, V),
                           s_blur=st["s_blur"])
        Hgn += J.T @ J
    eps = EPS_FRAC * np.trace(Hgn) / P
    Hreg = Hgn + eps * np.eye(P)

    out = []
    for frame, prev_pos in zip(ho_frames, ho_prev_pos):
        ho_poses = list(poses) + [(poses[prev_pos][0].copy(),
                                   poses[prev_pos][1].copy())]
        fit_pose(st, ho_poses, len(ho_poses) - 1, frame, SHAPE, U, V,
                 ITERS_HO_POSE)
        cam = _cam(ho_poses[-1], f, SHAPE, U, V)
        img = render(st["mu"], st["s"], st["w"], st["b"], cam,
                     s_blur=st["s_blur"])
        res = np.abs(img - frame)
        J = frame_jacobian(st["mu"], st["s"], st["w"], st["b"], cam,
                           s_blur=st["s_blur"])
        X = np.linalg.solve(Hreg, J.T)
        sig = np.sqrt(np.maximum(np.sum(J.T * X, axis=0), 0.0))
        # amplitude controls: 'amp' = |rendered| is the DECLARED primary
        # control (issue #48 wording); 'ampc' = |render - b| (centered,
        # foreground amplitude) is reported as an auxiliary variant.
        ctrl_amp = np.abs(img)
        ctrl_ampc = np.abs(img - st["b"])
        ctrl_jn = np.linalg.norm(J, axis=1)
        ctrl_dg = np.sqrt(np.sum(J ** 2 / (np.diag(Hgn) + eps)[None, :],
                                 axis=1))
        out.append({"img": img, "res": res, "sig": sig, "amp": ctrl_amp,
                    "ampc": ctrl_ampc, "jn": ctrl_jn, "dg": ctrl_dg,
                    "mse": float(np.mean((img - frame) ** 2))})
    return out


def precondition_met(tr_psnrs, floor=PSNR_FLOOR):
    """The declared hard gate: gate evaluation is meaningless (DNF) unless
    the PRIMARY (blur-on) fit reaches the floor on every seed. Pure
    function so tests can pin the stop."""
    return len(tr_psnrs) > 0 and min(tr_psnrs) >= floor


def main():
    train_frames = load_train()
    train_idx = [i for i in range(24) if i not in HELD_OUT]
    pos_of = {orig: pos for pos, orig in enumerate(train_idx)}
    ho_prev_pos = [pos_of[i - 1] for i in HELD_OUT]
    U, V = pixel_grid(SHAPE)

    print("=== exp16 / issue #48 Phase 1: real video (carousel) ===")
    print(f"train {len(train_frames)} frames, held-out {list(HELD_OUT)} "
          f"(pre-fixed); K={K}, f0={F0}; declared gates: precondition "
          f"train PSNR >= {PSNR_FLOOR} dB, Gate B rho >= {GATE_RHO} "
          f"(all seeds), Gate B2 = consistent uplift over controls, "
          f"blur ablation paired")

    # ---- phase 1: TRAIN-ONLY fits for every seed; the held-out frames
    # are not even loaded until the precondition gate passes ----
    fits_by_seed = {}
    for seed in SEEDS:
        fits = {}
        for use_blur in (True, False):
            t0 = time.perf_counter()
            st, poses, hist = fit_video(
                train_frames, SHAPE, F0, K=K, seed=seed, use_blur=use_blur,
                iters_a=ITERS_A, iters_pose=ITERS_POSE,
                iters_win=ITERS_WIN, window=WINDOW,
                final_schedule=FINAL_SCHEDULE)
            f = float(np.exp(st["logf"]))
            mses = [np.mean((render(st["mu"], st["s"], st["w"], st["b"],
                                    _cam(poses[i], f, SHAPE, U, V),
                                    s_blur=st["s_blur"]) - fr) ** 2)
                    for i, fr in enumerate(train_frames)]
            tr_psnr = psnr(float(np.mean(mses)))
            sb = (float(np.exp(st["s_blur"]))
                  if st["s_blur"] is not None else None)
            fits[use_blur] = (st, poses, hist, tr_psnr)
            print(f"  seed={seed} blur={'on ' if use_blur else 'off'}: "
                  f"train PSNR {tr_psnr:.2f} dB, f={f:.1f}"
                  + (f", sigma_blur={sb:.2f}px" if sb else "")
                  + f"  ({time.perf_counter() - t0:.0f}s)", flush=True)
        fits_by_seed[seed] = fits

    pre = [fits_by_seed[seed][True][3] for seed in SEEDS]
    print(f"\nprecondition (train PSNR >= {PSNR_FLOOR} dB on the primary "
          f"blur-on fit, all seeds): {[f'{p:.2f}' for p in pre]}")
    if not precondition_met(pre):
        print("   -> PRECONDITION NOT MET: DNF recorded. STOPPING before "
              "the held-out frames are loaded or evaluated (declared "
              "hard stop; the protocol stays intact for a later round).")
        return

    # ---- phase 2: held-out evaluation (only reachable past the gate) ----
    ho_frames = load_holdout()
    rows = []
    keep0 = None
    for seed in SEEDS:
        fits = fits_by_seed[seed]
        evs = {}
        for use_blur in (True, False):
            st, poses, hist, tr_psnr = fits[use_blur]
            evs[use_blur] = evaluate(st, poses, train_frames, ho_frames,
                                     ho_prev_pos, U, V)
        st, poses, hist, tr_psnr = fits[True]
        ev = evs[True]
        ho_mse = float(np.mean([e["mse"] for e in ev]))
        ho_mse_off = float(np.mean([e["mse"] for e in evs[False]]))
        res = np.concatenate([e["res"] for e in ev])
        sig = np.concatenate([e["sig"] for e in ev])
        r_sig = spearman(sig, res)
        r_ctrl = {name: spearman(np.concatenate([e[name] for e in ev]), res)
                  for name in ("amp", "jn", "dg")}
        r_ampc = spearman(np.concatenate([e["ampc"] for e in ev]), res)
        rows.append({"seed": seed, "tr_psnr": tr_psnr, "rho": r_sig,
                     "ctrl": r_ctrl, "ampc": r_ampc, "mse_on": ho_mse,
                     "mse_off": ho_mse_off,
                     "sblur": float(np.exp(st["s_blur"]))})
        print(f"    seed={seed} gate scores: rho(sigma_pred)={r_sig:+.3f}"
              "  declared controls: "
              + "  ".join(f"{k}={v:+.3f}" for k, v in r_ctrl.items())
              + f"  [aux centered amp={r_ampc:+.3f}]", flush=True)
        if seed == SEEDS[0]:
            keep0 = ((st, poses, hist, ev, tr_psnr, ho_mse), ho_frames)

    # ---- figure: held-out frames, seed 0, blur-on model ----
    (st, poses, hist, ev, _, _), ho_fr = keep0
    Hh, Wh = SHAPE
    fig, axes = plt.subplots(4, len(HELD_OUT), figsize=(3.2 * len(HELD_OUT),
                                                        7.6))
    for j, (e, fr) in enumerate(zip(ev, ho_fr)):
        panels = [(fr.reshape(Hh, Wh), "held-out frame", "gray", None),
                  (e["img"].reshape(Hh, Wh), "render", "gray", None),
                  (e["res"].reshape(Hh, Wh), "|residual|", "magma", None),
                  (np.log10(e["sig"] + 1e-9).reshape(Hh, Wh),
                   "log10 sigma_pred", "viridis", None)]
        for i, (img, name, cmap, _) in enumerate(panels):
            axes[i, j].imshow(img, cmap=cmap, origin="upper")
            if j == 0:
                axes[i, j].set_ylabel(name, fontsize=8)
            if i == 0:
                axes[i, j].set_title(f"frame {HELD_OUT[j]}", fontsize=9)
            axes[i, j].set_xticks([]); axes[i, j].set_yticks([])
    fig.tight_layout()
    fig.savefig(HERE / "heldout_certificate.png", dpi=110)
    print(f"figure: {HERE / 'heldout_certificate.png'}")

    # ---- verdicts vs the declared gates (only reachable past the
    # precondition hard stop above) ----
    print("\n=== verdicts vs declared gates (issue #48) ===")
    rhos = [r["rho"] for r in rows]
    print(f"Gate B (pooled held-out Spearman >= {GATE_RHO}, all seeds): "
          f"{[f'{r:+.3f}' for r in rhos]}")
    print("   -> " + ("GATE B PASSED." if min(rhos) >= GATE_RHO else
                      "GATE B NOT PASSED -- recorded; per the declared "
                      "falsification this sends the work back to the "
                      "renderer (occlusion), not the score."))
    uplift = all(r["rho"] > max(r["ctrl"].values()) for r in rows)
    for r in rows:
        print(f"  seed={r['seed']}: sigma_pred {r['rho']:+.3f} vs best "
              f"control {max(r['ctrl'].values()):+.3f} "
              f"({max(r['ctrl'], key=r['ctrl'].get)})")
    print("   -> Gate B2 " + ("PASSED: consistent uplift over all controls "
                              "on every seed." if uplift else
                              "NOT PASSED: the certificate does not "
                              "separate from amplitude/support tracking "
                              "on this data -- recorded."))
    print("blur ablation (held-out MSE, paired per seed):")
    for r in rows:
        rel = r["mse_on"] / r["mse_off"]
        print(f"  seed={r['seed']}: on {r['mse_on']:.4e} vs off "
              f"{r['mse_off']:.4e} (ratio {rel:.3f}), "
              f"sigma_blur={r['sblur']:.2f}px")
    ok = all(r["mse_on"] <= r["mse_off"] for r in rows)
    print("   -> " + ("blur knob helps or is neutral on every seed "
                      "(declared bar)." if ok else
                      "blur knob does NOT meet the declared bar on at "
                      "least one seed -- recorded."))


if __name__ == "__main__":
    main()
