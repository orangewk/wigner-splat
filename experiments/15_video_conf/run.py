"""Experiment 15 -- issue #48 Phase 0: confidence certificate vs true error.

A fully known synthetic 3D scene (signed isotropic Gaussians) is imaged by
a short low-parallax camera trajectory ("6 seconds": 24 frames, total
baseline 0.8 world units at ~6 units depth), reconstructed by gradient
descent, and the question is whether a CLOSED-FORM confidence score --
computed WITHOUT ever seeing the ground truth or even the pixel data --
predicts where the reconstruction is actually wrong.

ROUND 1 (recorded, out_round1.log): the pure-geometry score -- lambda_min
of a unit probe splat's Gauss-Newton information at each grid point --
FAILED the declared gate (covered Spearman -0.101 / +0.096 / -0.200).
Lesson: reconstruction error concentrates on structure in the well-covered
center (fit imperfection), while information-starved EMPTY regions are
cheap to get right; a score that never couples to model amplitude measures
"where you could be wrong", not "where you are wrong".

ROUND 2 score (declared on issue #48 before running): delta-method
predicted uncertainty of the fitted density,

    sigma_pred(x)^2 = J_rho(x)^T (H + eps I)^{-1} J_rho(x),

H = Gauss-Newton matrix of the FITTED splats over all frames,
eps = 1e-9 tr(H)/P fixed in advance. Sees the video (through the fit) and
the model -- never the ground truth. Degenerate directions (the monocular
size-distance trade-off sigma_img = f sigma / z that low parallax fails
to break) blow sigma_pred up through H's null space; coupling to model
amplitude enters through J_rho.

DECLARED PROTOCOL (identical numbers to round 1):
  * GATE A (primary): Spearman rank correlation between sigma_pred and
    the true absolute density error, over grid points COVERED by >= 1
    camera, must be rho >= 0.3 on ALL of 3 seeds (seed varies the true
    scene, the fit init, and the pixel noise; the camera path is fixed).
  * Auxiliary (descriptive, not the gate): the same correlation over all
    grid points, over covered points restricted to model support
    (|rho_fit| > 0.05 max), and the round-1 lambda_min score kept for
    comparison.
  * Pixel noise sigma = 0.02 on the rendered frames (without noise the
    degenerate directions would only carry init error).
  * INVERSE CRIME accepted deliberately at Phase 0: frames are rendered
    by the same forward model that fits them. The question tested is
    information-vs-error, not model mismatch; real video (Phase 1) breaks
    the crime.

Falsification (issue #48): if round 2 also misses the gate, record that
the delta-method certificate does not reach either and pause Phase 0 for
a scope decision -- itself a result for the #46 applications map.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from gauss3d import (  # noqa: E402
    density3d, fit, make_camera, predicted_sigma, probe_information,
    render, spearman,
)

HERE = pathlib.Path(__file__).resolve().parent

IMG = 64
FOCAL = 64.0
N_FRAMES = 24            # "6 seconds" at 4 fps
BASELINE = 0.8           # total lateral travel, world units
LOOK_AT = np.array([0.0, 0.0, 6.0])
NOISE = 0.02             # declared pixel noise sigma
K_TRUE = 10
K_FIT = 24
ITERS = 2000
LR = 0.03
SEEDS = (0, 1, 2)
SIGMA_PROBE = 0.4        # probe scale for the confidence score (fixed)
GATE_RHO = 0.3           # declared primary threshold, every seed
SUPPORT_FRAC = 0.05      # auxiliary model-support cut: |rho_fit| > frac*max

GRID_XY = np.linspace(-2.6, 2.6, 12)
GRID_Z = np.linspace(2.6, 9.4, 14)


def make_cameras():
    ts = np.linspace(-0.5, 0.5, N_FRAMES)
    return [make_camera((BASELINE * t, 0.05 * np.sin(2 * np.pi * i / N_FRAMES),
                         0.0), LOOK_AT, FOCAL, (IMG, IMG))
            for i, t in enumerate(ts)]


def make_scene(seed):
    rng = np.random.default_rng(1000 + seed)
    z = rng.uniform(3.0, 9.0, K_TRUE)
    xy = rng.uniform(-0.3, 0.3, (K_TRUE, 2)) * z[:, None]
    mu = np.column_stack([xy, z])
    s = np.log(rng.uniform(0.25, 0.55, K_TRUE))
    signs = rng.choice([-1.0, 1.0], K_TRUE)
    w = signs * rng.uniform(0.4, 1.0, K_TRUE)
    return mu, s, w


def eval_grid():
    Xg, Yg, Zg = np.meshgrid(GRID_XY, GRID_XY, GRID_Z, indexing="ij")
    return np.column_stack([Xg.ravel(), Yg.ravel(), Zg.ravel()])


def coverage_mask(pts, cams):
    cov = np.zeros(len(pts), dtype=bool)
    for cam in cams:
        p = (pts - cam["c"]) @ cam["R"].T
        z = p[:, 2]
        ok = z > 0.5
        u0 = cam["f"] * p[:, 0] / np.where(ok, z, 1.0) + cam["cx"]
        v0 = cam["f"] * p[:, 1] / np.where(ok, z, 1.0) + cam["cy"]
        H, W = cam["shape"]
        cov |= ok & (u0 >= 0) & (u0 <= W - 1) & (v0 >= 0) & (v0 <= H - 1)
    return cov


def main():
    print("=== exp15 / issue #48 Phase 0 round 2: predicted uncertainty "
          "vs true error ===")
    print(f"trajectory: {N_FRAMES} frames, baseline {BASELINE} at depth "
          f"{LOOK_AT[2]:.0f} (parallax ~{BASELINE / LOOK_AT[2]:.3f} rad); "
          f"noise sigma {NOISE}; declared gate: covered-region Spearman "
          f"(sigma_pred vs |error|) >= {GATE_RHO} on all seeds {SEEDS}")
    cams = make_cameras()
    pts = eval_grid()
    cov = coverage_mask(pts, cams)
    print(f"eval grid: {len(pts)} points, covered {int(cov.sum())}")

    t0 = time.perf_counter()
    conf1 = np.array([np.linalg.eigvalsh(
        probe_information(x, SIGMA_PROBE, cams))[0] for x in pts])
    print(f"round-1 score kept as auxiliary (geometry-only lambda_min, "
          f"{time.perf_counter() - t0:.0f}s)")

    rows = []
    err0 = sp0 = None
    for seed in SEEDS:
        mu_t, s_t, w_t = make_scene(seed)
        rng = np.random.default_rng(2000 + seed)
        frames = [render(mu_t, s_t, w_t, cam)
                  + rng.normal(0.0, NOISE, IMG * IMG) for cam in cams]
        t0 = time.perf_counter()
        params, losses = fit(frames, cams, K_FIT, iters=ITERS, lr=LR,
                             seed=seed)
        rho_fit = density3d(pts, params["mu"], params["s"], params["w"])
        err = np.abs(rho_fit - density3d(pts, mu_t, s_t, w_t))
        sig_pred = predicted_sigma(pts, params, cams)
        support = cov & (np.abs(rho_fit)
                         > SUPPORT_FRAC * np.max(np.abs(rho_fit)))
        r_cov = spearman(sig_pred[cov], err[cov])
        r_all = spearman(sig_pred, err)
        r_sup = spearman(sig_pred[support], err[support])
        r_v1 = spearman(-conf1[cov], err[cov])
        rows.append((seed, r_cov, r_all, r_sup, r_v1))
        if seed == SEEDS[0]:
            err0, sp0 = err, sig_pred
        print(f"  seed={seed}: fit loss {losses[0]:.3e} -> {losses[-1]:.3e} "
              f"({time.perf_counter() - t0:.0f}s, {K_FIT} splats, "
              f"{int(np.sum(params['w'] < 0))} negative); "
              f"Spearman v2 covered={r_cov:+.3f} all={r_all:+.3f} "
              f"support={r_sup:+.3f} | v1 covered={r_v1:+.3f}", flush=True)

    # figure: predicted sigma vs error slices (seed 0) + scatter
    nz = len(GRID_Z)
    sp_g = sp0.reshape(12, 12, nz)
    err_g = err0.reshape(12, 12, nz)
    zi = [2, nz // 2, nz - 3]
    fig, axes = plt.subplots(2, 4, figsize=(14, 6.4))
    for col, k in enumerate(zi):
        for row, (F, name, cmap) in enumerate(
                [(np.log10(sp_g + 1e-12), "log10 sigma_pred", "viridis"),
                 (err_g, "|error|", "magma")]):
            im = axes[row, col].imshow(F[:, :, k].T, origin="lower",
                                       cmap=cmap,
                                       extent=[GRID_XY[0], GRID_XY[-1]] * 2)
            axes[row, col].set_title(f"{name}  z={GRID_Z[k]:.1f}", fontsize=9)
            fig.colorbar(im, ax=axes[row, col], shrink=0.8)
    axes[0, 3].scatter(np.log10(sp0[cov] + 1e-12), np.log10(err0[cov] + 1e-9),
                       s=4, alpha=0.4)
    axes[0, 3].set_xlabel("log10 sigma_pred (no truth)")
    axes[0, 3].set_ylabel("log10 |error| (seed 0)")
    axes[0, 3].set_title(f"covered points, Spearman {rows[0][1]:+.3f}",
                         fontsize=9)
    axes[1, 3].axis("off")
    axes[1, 3].text(0.0, 0.6, "sigma_pred sees the video and the\n"
                    "fitted model -- never the truth;\n"
                    "|error| needs the ground truth", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "conf_vs_error.png", dpi=110)
    print(f"figure: {HERE / 'conf_vs_error.png'}")

    print("\n=== verdict vs declared Gate A (round 2) ===")
    r_covs = [r[1] for r in rows]
    print(f"primary (covered-region Spearman, gate >= {GATE_RHO} on all "
          f"seeds): {[f'{r:+.3f}' for r in r_covs]}")
    if min(r_covs) >= GATE_RHO:
        print("   -> GATE A PASSED: the delta-method certificate ranks "
              "true error above the declared bar on every seed.")
    else:
        print("   -> GATE A NOT PASSED on at least one seed -- recorded; "
              "per the declared falsification, pause Phase 0 for a scope "
              "decision.")
    print("auxiliary (descriptive, not the gate): "
          f"all-points {[f'{r[2]:+.3f}' for r in rows]}, "
          f"model-support {[f'{r[3]:+.3f}' for r in rows]}, "
          f"round-1 score {[f'{r[4]:+.3f}' for r in rows]}")


if __name__ == "__main__":
    main()
