"""Experiment 16 -- issue #48 Phase 1: the certificate on real video.

Real hand-held walking video (carousel; provenance in data/README.md),
24 frames over 6 s. The declared protocol (posted to issue #48 before
implementation; round-2 amendment -- renderer only -- posted before the
gate run) in short:

  * held-out frames 4, 10, 16, 22 (pre-fixed); the other 20 train. All
    pipeline tuning used TRAIN frames only.
  * ROUND-2 MODEL (the declared falsification path of round 1's DNF):
    sorted alpha compositing (composite.py) over the same isotropic
    Gaussians, background, blur knob, and jointly-fitted poses. Round 1's
    additive renderer asymptoted at 17.85 dB train PSNR (DNF, recorded in
    out_tuning_round1.log); the compositing recipe cleared the floor on
    the train-only tuning (18.09 dB, seed 0).
  * RECIPE (fixed from train-only tuning; identical budgets for the
    blur ablation pair, which branches from a SHARED checkpoint):
      base   fit_video(composite, K=250, opacity_init=-2, stages A/B,
             final (600, 0.02), (400, 0.006))
      polish fit_pose per frame (80 it, lr rot 0.004 / trans 0.01)
      branch blur-off: continuation (600, 0.006), (400, 0.002)
             blur-on : same schedule with use_blur (s_blur Adam lr 0.01)
             [joint pose lrs 0.005 / 0.01, logf lr 0.002]
  * PRECONDITION -- a HARD STOP in code: every seed's PRIMARY (blur-on)
    fit must reach train PSNR >= 18 dB (PSNR of the POOLED per-frame
    MSE), or gating returns before the held-out frames are even loaded.
  * GATE B (primary): Spearman(sigma_pred, |residual|) pooled over the
    held-out frames' pixels, >= 0.3 on all 3 seeds. sigma_pred is the
    exp15 round-2 delta-method score with H built from TRAIN frames only
    (splat parameters incl. opacity + background; poses and global knobs
    fixed, eps = 1e-9 tr(H)/P).
  * GATE B2: sigma_pred must show a CONSISTENT uplift over the three
    DECLARED controls -- |rendered| (amplitude, as worded on the issue),
    row-norm of J (the H = I score), diagonal-H -- on every seed. The
    centered |render - b| is reported as an auxiliary only.
  * BLUR ABLATION: held-out MSE with the blur knob <= without, paired
    per seed (identical budgets by construction); fitted sigma_blur
    reported. Gates B/B2 are evaluated on the blur-ON fit.

Operationally the ~3 h/seed fits run as separate invocations writing
checkpoints (restart-safe on this 4-core box):

    python run.py fit --seed 0     # base + polish + both branches
    python run.py gate             # precondition hard stop, then gates

python run.py (no args) does everything sequentially (used by the
hard-stop regression test with a faked fit_video).

Falsification (declared): Gate B failing on real video reads "the
certificate does not survive occlusion + model mismatch" and sends the
work back to the renderer, not to the score.
"""
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "15_video_conf"))
sys.path.insert(0, str(HERE))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import composite  # noqa: E402
from gauss3d import spearman  # noqa: E402
from jointfit import _cam, fit_pose, fit_video, psnr  # noqa: E402

HELD_OUT = (4, 10, 16, 22)          # pre-fixed in the declaration
K = 250
F0 = 78.0                            # iPhone wide prior; logf fitted
SEEDS = (0, 1, 2)
SHAPE = (54, 96)
OPACITY_INIT = -2.0
BASE_SCHEDULE = ((600, 0.02), (400, 0.006))
CONT_SCHEDULE = ((600, 0.006), (400, 0.002))
POLISH = (80, 0.004, 0.01)           # iters, lr rot, lr trans
CONT_LRS = dict(lr_pose_r=0.005, lr_pose_c=0.01, lr_glob=0.002,
                lr_blur=0.01)
ITERS_A, ITERS_POSE, ITERS_WIN, WINDOW = 300, 60, 60, 5
ITERS_HO_POSE = 150
PSNR_FLOOR = 18.0
GATE_RHO = 0.3
EPS_FRAC = 1e-9
CKPT = HERE / "checkpoints"


def load_train():
    """Train frames ONLY. The held-out frames live behind load_holdout(),
    called only after the precondition gate passes."""
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


def _render_state(st, cam):
    return composite.render(st["mu"], st["s"], st["w"], st["b"], cam,
                            s_blur=st["s_blur"], o=st["o"])


def train_psnr(st, poses, frames, U, V):
    f = float(np.exp(st["logf"]))
    mses = [np.mean((_render_state(st, _cam(poses[i], f, SHAPE, U, V))
                     - fr) ** 2) for i, fr in enumerate(frames)]
    return psnr(float(np.mean(mses)))


def _save_ckpt(path, st, poses):
    path.parent.mkdir(exist_ok=True)
    np.savez_compressed(path, mu=st["mu"], s=st["s"], w=st["w"],
                        o=st["o"], b=st["b"], logf=st["logf"],
                        s_blur=(np.nan if st["s_blur"] is None
                                else st["s_blur"]),
                        Rs=np.stack([p[0] for p in poses]),
                        cs=np.stack([p[1] for p in poses]))


def _load_ckpt(path):
    S = np.load(path)
    sb = float(S["s_blur"])
    st = {"mu": S["mu"].copy(), "s": S["s"].copy(), "w": S["w"].copy(),
          "o": S["o"].copy(), "b": float(S["b"]),
          "logf": float(S["logf"]),
          "s_blur": None if np.isnan(sb) else sb}
    poses = [(S["Rs"][i].copy(), S["cs"][i].copy())
             for i in range(len(S["cs"]))]
    return st, poses


def fit_seed(seed, train_frames, U, V):
    """The fixed recipe: shared base + polish, then the paired branches.
    Returns {True: (st, poses), False: (st, poses)} keyed by use_blur."""
    t0 = time.perf_counter()
    st, poses, _ = fit_video(train_frames, SHAPE, F0, K=K, seed=seed,
                             renderer=composite,
                             opacity_init=OPACITY_INIT, iters_a=ITERS_A,
                             iters_pose=ITERS_POSE, iters_win=ITERS_WIN,
                             window=WINDOW, final_schedule=BASE_SCHEDULE)
    n_it, lr_r, lr_c = POLISH
    for i in range(1, len(train_frames)):
        fit_pose(st, poses, i, train_frames[i], SHAPE, U, V, n_it, lr_r,
                 lr_c, renderer=composite)
    print(f"  seed={seed} base+polish done "
          f"({time.perf_counter() - t0:.0f}s)", flush=True)
    out = {}
    for use_blur in (False, True):
        t1 = time.perf_counter()
        st2, poses2, _ = fit_video(
            train_frames, SHAPE, F0, K=K, seed=seed, renderer=composite,
            use_blur=use_blur,
            resume=({k: (v.copy() if hasattr(v, "copy") else v)
                     for k, v in st.items()},
                    [(R.copy(), c.copy()) for R, c in poses]),
            final_schedule=CONT_SCHEDULE, **CONT_LRS)
        tp = train_psnr(st2, poses2, train_frames, U, V)
        sb = (f", sigma_blur={np.exp(st2['s_blur']):.2f}px"
              if st2["s_blur"] is not None else "")
        print(f"  seed={seed} blur={'on ' if use_blur else 'off'}: "
              f"train PSNR {tp:.2f} dB, f={np.exp(st2['logf']):.1f}{sb}"
              f"  ({time.perf_counter() - t1:.0f}s)", flush=True)
        out[use_blur] = (st2, poses2)
    return out


def precondition_met(tr_psnrs, floor=PSNR_FLOOR):
    """The declared hard gate: gate evaluation is meaningless (DNF)
    unless the PRIMARY (blur-on) fit reaches the floor on every seed."""
    return len(tr_psnrs) > 0 and min(tr_psnrs) >= floor


def evaluate(st, poses, n_train, ho_frames, ho_prev_pos, U, V):
    """Held-out pose fits, residuals, sigma_pred and controls."""
    f = float(np.exp(st["logf"]))
    P = 6 * len(st["w"]) + 1
    Hgn = np.zeros((P, P))
    for pos in range(n_train):
        J = composite.frame_jacobian(st["mu"], st["s"], st["w"], st["b"],
                                     _cam(poses[pos], f, SHAPE, U, V),
                                     s_blur=st["s_blur"], o=st["o"])
        Hgn += J.T @ J
    eps = EPS_FRAC * np.trace(Hgn) / P
    Hreg = Hgn + eps * np.eye(P)

    out = []
    for frame, prev_pos in zip(ho_frames, ho_prev_pos):
        ho_poses = list(poses) + [(poses[prev_pos][0].copy(),
                                   poses[prev_pos][1].copy())]
        fit_pose(st, ho_poses, len(ho_poses) - 1, frame, SHAPE, U, V,
                 ITERS_HO_POSE, renderer=composite)
        cam = _cam(ho_poses[-1], f, SHAPE, U, V)
        img = _render_state(st, cam)
        res = np.abs(img - frame)
        J = composite.frame_jacobian(st["mu"], st["s"], st["w"], st["b"],
                                     cam, s_blur=st["s_blur"], o=st["o"])
        X = np.linalg.solve(Hreg, J.T)
        sig = np.sqrt(np.maximum(np.sum(J.T * X, axis=0), 0.0))
        out.append({"img": img, "res": res, "sig": sig,
                    "amp": np.abs(img),            # DECLARED control
                    "ampc": np.abs(img - st["b"]),  # auxiliary variant
                    "jn": np.linalg.norm(J, axis=1),
                    "dg": np.sqrt(np.sum(
                        J ** 2 / (np.diag(Hgn) + eps)[None, :], axis=1)),
                    "mse": float(np.mean((img - frame) ** 2))})
    return out


def gate(fits_by_seed, train_frames, U, V):
    """Precondition hard stop, then held-out gates. fits_by_seed maps
    seed -> {use_blur: (st, poses)}."""
    pre = [train_psnr(*fits_by_seed[s][True], train_frames, U, V)
           for s in SEEDS]
    print(f"\nprecondition (train PSNR >= {PSNR_FLOOR} dB on the primary "
          f"blur-on fit, all seeds): {[f'{p:.2f}' for p in pre]}")
    if not precondition_met(pre):
        print("   -> PRECONDITION NOT MET: DNF recorded. STOPPING before "
              "the held-out frames are loaded or evaluated (declared "
              "hard stop; the protocol stays intact for a later round).")
        return

    train_idx = [i for i in range(24) if i not in HELD_OUT]
    pos_of = {orig: pos for pos, orig in enumerate(train_idx)}
    ho_prev_pos = [pos_of[i - 1] for i in HELD_OUT]
    ho_frames = load_holdout()
    rows = []
    keep0 = None
    for seed in SEEDS:
        evs = {ub: evaluate(fits_by_seed[seed][ub][0],
                            fits_by_seed[seed][ub][1],
                            len(train_frames), ho_frames, ho_prev_pos,
                            U, V) for ub in (True, False)}
        st = fits_by_seed[seed][True][0]
        ev = evs[True]
        res = np.concatenate([e["res"] for e in ev])
        sig = np.concatenate([e["sig"] for e in ev])
        r_sig = spearman(sig, res)
        r_ctrl = {n: spearman(np.concatenate([e[n] for e in ev]), res)
                  for n in ("amp", "jn", "dg")}
        r_ampc = spearman(np.concatenate([e["ampc"] for e in ev]), res)
        rows.append({"seed": seed, "rho": r_sig, "ctrl": r_ctrl,
                     "ampc": r_ampc,
                     "mse_on": float(np.mean([e["mse"] for e in ev])),
                     "mse_off": float(np.mean([e["mse"]
                                               for e in evs[False]])),
                     "sblur": float(np.exp(st["s_blur"]))})
        print(f"  seed={seed}: rho(sigma_pred)={r_sig:+.3f}  declared "
              "controls: "
              + "  ".join(f"{k}={v:+.3f}" for k, v in r_ctrl.items())
              + f"  [aux centered amp={r_ampc:+.3f}]", flush=True)
        if seed == SEEDS[0]:
            keep0 = (ev, ho_frames)

    _figure(keep0)
    _verdicts(rows)


def _figure(keep0):
    ev, ho_fr = keep0
    Hh, Wh = SHAPE
    fig, axes = plt.subplots(4, len(HELD_OUT),
                             figsize=(3.2 * len(HELD_OUT), 7.6))
    for j, (e, fr) in enumerate(zip(ev, ho_fr)):
        panels = [(fr.reshape(Hh, Wh), "held-out frame", "gray"),
                  (e["img"].reshape(Hh, Wh), "render", "gray"),
                  (e["res"].reshape(Hh, Wh), "|residual|", "magma"),
                  (np.log10(e["sig"] + 1e-9).reshape(Hh, Wh),
                   "log10 sigma_pred", "viridis")]
        for i, (img, name, cmap) in enumerate(panels):
            axes[i, j].imshow(img, cmap=cmap, origin="upper")
            if j == 0:
                axes[i, j].set_ylabel(name, fontsize=8)
            if i == 0:
                axes[i, j].set_title(f"frame {HELD_OUT[j]}", fontsize=9)
            axes[i, j].set_xticks([]); axes[i, j].set_yticks([])
    fig.tight_layout()
    fig.savefig(HERE / "heldout_certificate.png", dpi=110)
    print(f"figure: {HERE / 'heldout_certificate.png'}")


def _verdicts(rows):
    print("\n=== verdicts vs declared gates (issue #48) ===")
    rhos = [r["rho"] for r in rows]
    print(f"Gate B (pooled held-out Spearman >= {GATE_RHO}, all seeds): "
          f"{[f'{r:+.3f}' for r in rhos]}")
    print("   -> " + ("GATE B PASSED." if min(rhos) >= GATE_RHO else
                      "GATE B NOT PASSED -- recorded; per the declared "
                      "falsification this sends the work back to the "
                      "renderer, not the score."))
    uplift = all(r["rho"] > max(r["ctrl"].values()) for r in rows)
    for r in rows:
        print(f"  seed={r['seed']}: sigma_pred {r['rho']:+.3f} vs best "
              f"declared control {max(r['ctrl'].values()):+.3f} "
              f"({max(r['ctrl'], key=r['ctrl'].get)})")
    print("   -> Gate B2 " + ("PASSED: consistent uplift over all "
                              "declared controls on every seed."
                              if uplift else
                              "NOT PASSED: the certificate does not "
                              "separate from amplitude/support tracking "
                              "on this data -- recorded."))
    print("blur ablation (held-out MSE, paired per seed, identical "
          "budgets):")
    for r in rows:
        print(f"  seed={r['seed']}: on {r['mse_on']:.4e} vs off "
              f"{r['mse_off']:.4e} (ratio {r['mse_on'] / r['mse_off']:.3f}"
              f"), sigma_blur={r['sblur']:.2f}px")
    ok = all(r["mse_on"] <= r["mse_off"] for r in rows)
    print("   -> " + ("blur knob helps or is neutral on every seed "
                      "(declared bar)." if ok else
                      "blur knob does NOT meet the declared bar on at "
                      "least one seed -- recorded."))


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    train_frames = load_train()
    U, V = pixel_grid(SHAPE)
    print("=== exp16 / issue #48 Phase 1 round 2: real video, "
          "compositing ===")

    if argv and argv[0] == "fit":
        seed = int(argv[argv.index("--seed") + 1])
        fits = fit_seed(seed, train_frames, U, V)
        for ub, (st, poses) in fits.items():
            _save_ckpt(CKPT / f"seed{seed}_{'on' if ub else 'off'}.npz",
                       st, poses)
        print(f"checkpoints written for seed {seed}")
        return
    if argv and argv[0] == "gate":
        fits_by_seed = {
            s: {ub: _load_ckpt(CKPT / f"seed{s}_{'on' if ub else 'off'}"
                               ".npz") for ub in (True, False)}
            for s in SEEDS}
        gate(fits_by_seed, train_frames, U, V)
        return

    # no args: full sequential protocol (also the test path)
    fits_by_seed = {s: fit_seed(s, train_frames, U, V) for s in SEEDS}
    gate(fits_by_seed, train_frames, U, V)


if __name__ == "__main__":
    main()
