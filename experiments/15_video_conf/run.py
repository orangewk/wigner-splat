"""Experiment 15 -- issue #48 Phase 0: confidence certificate vs true error.

A fully known synthetic 3D scene (signed isotropic Gaussians) is imaged by
a short low-parallax camera trajectory ("6 seconds": 24 frames, total
baseline 0.8 world units at ~6 units depth), reconstructed by gradient
descent, and the question is whether a CLOSED-FORM confidence score --
computed WITHOUT ever seeing the ground truth or even the pixel data --
predicts where the reconstruction is actually wrong.

Confidence score (candidate 1 of the issue: Fisher-information closed
form): at each 3D grid point, lambda_min of the 5x5 Gauss-Newton
information matrix of a hypothetical unit probe splat (position
nondimensionalized by the probe scale). Low parallax leaves the monocular
size-distance degeneracy (sigma_img = f sigma / z) unbroken, so the
worst-constrained direction collapses exactly where a certificate should
say "do not trust depth here". The score is pure camera geometry.

DECLARED PROTOCOL (posted to issue #48 before this run):
  * GATE A (primary): Spearman rank correlation between (-confidence) and
    the true absolute density error, over grid points COVERED by >= 1
    camera, must be rho >= 0.3 on ALL of 3 seeds (seed varies the true
    scene, the fit init, and the pixel noise; the camera path is fixed).
  * Auxiliary (descriptive, not the gate): the same correlation over all
    grid points (uncovered points have zero score and would trivially
    help), and over covered points restricted to model support
    (|rho_fit| > 0.05 max) -- "of the things the model draws, which
    should you trust".
  * Pixel noise sigma = 0.02 on the rendered frames (without noise the
    degenerate directions would only carry init error).
  * INVERSE CRIME accepted deliberately at Phase 0: frames are rendered
    by the same forward model that fits them. The question tested is
    information-vs-error, not model mismatch; real video (Phase 1) breaks
    the crime.

Falsification (issue #48): if the correlation does not clear the gate,
record that the certificate philosophy does not export to this regime and
return to score design -- itself a result for the #46 applications map.
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
    density3d, fit, make_camera, probe_information, render, spearman,
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
    print("=== exp15 / issue #48 Phase 0: geometry-only confidence vs "
          "true error ===")
    print(f"trajectory: {N_FRAMES} frames, baseline {BASELINE} at depth "
          f"{LOOK_AT[2]:.0f} (parallax ~{BASELINE / LOOK_AT[2]:.3f} rad); "
          f"noise sigma {NOISE}; declared gate: covered-region Spearman "
          f">= {GATE_RHO} on all seeds {SEEDS}")
    cams = make_cameras()
    pts = eval_grid()
    cov = coverage_mask(pts, cams)
    print(f"eval grid: {len(pts)} points, covered {int(cov.sum())}")

    t0 = time.perf_counter()
    conf = np.array([np.linalg.eigvalsh(
        probe_information(x, SIGMA_PROBE, cams))[0] for x in pts])
    print(f"confidence field (camera geometry ONLY -- no data, no truth): "
          f"{time.perf_counter() - t0:.0f}s, lambda_min range "
          f"[{conf.min():.3e}, {conf.max():.3e}]")

    rows = []
    err0 = None
    for seed in SEEDS:
        mu_t, s_t, w_t = make_scene(seed)
        rng = np.random.default_rng(2000 + seed)
        frames = [render(mu_t, s_t, w_t, cam)
                  + rng.normal(0.0, NOISE, IMG * IMG) for cam in cams]
        t0 = time.perf_counter()
        params, losses = fit(frames, cams, K_FIT, iters=ITERS, lr=LR,
                             seed=seed)
        err = np.abs(density3d(pts, params["mu"], params["s"], params["w"])
                     - density3d(pts, mu_t, s_t, w_t))
        rho_fit = density3d(pts, params["mu"], params["s"], params["w"])
        support = cov & (np.abs(rho_fit) > SUPPORT_FRAC * np.max(np.abs(rho_fit)))
        r_cov = spearman(-conf[cov], err[cov])
        r_all = spearman(-conf, err)
        r_sup = spearman(-conf[support], err[support])
        rows.append((seed, r_cov, r_all, r_sup))
        if seed == SEEDS[0]:
            err0 = err
        print(f"  seed={seed}: fit loss {losses[0]:.3e} -> {losses[-1]:.3e} "
              f"({time.perf_counter() - t0:.0f}s, {K_FIT} splats, "
              f"{int(np.sum(params['w'] < 0))} negative); "
              f"Spearman covered={r_cov:+.3f} all={r_all:+.3f} "
              f"support={r_sup:+.3f}", flush=True)

    # figure: confidence vs error slices (seed 0) + scatter
    nz = len(GRID_Z)
    conf_g = conf.reshape(12, 12, nz)
    err_g = err0.reshape(12, 12, nz)
    zi = [2, nz // 2, nz - 3]
    fig, axes = plt.subplots(2, 4, figsize=(14, 6.4))
    for col, k in enumerate(zi):
        for row, (F, name, cmap) in enumerate(
                [(np.log10(conf_g + 1e-12), "log10 confidence", "viridis"),
                 (err_g, "|error|", "magma")]):
            im = axes[row, col].imshow(F[:, :, k].T, origin="lower",
                                       cmap=cmap,
                                       extent=[GRID_XY[0], GRID_XY[-1]] * 2)
            axes[row, col].set_title(f"{name}  z={GRID_Z[k]:.1f}", fontsize=9)
            fig.colorbar(im, ax=axes[row, col], shrink=0.8)
    axes[0, 3].scatter(np.log10(conf[cov] + 1e-12), np.log10(err0[cov] + 1e-9),
                       s=4, alpha=0.4)
    axes[0, 3].set_xlabel("log10 confidence (geometry only)")
    axes[0, 3].set_ylabel("log10 |error| (seed 0)")
    axes[0, 3].set_title(f"covered points, Spearman {rows[0][1]:+.3f}",
                         fontsize=9)
    axes[1, 3].axis("off")
    axes[1, 3].text(0.0, 0.6, "score sees camera geometry only\n"
                    "(never pixels, never truth);\n"
                    "error needs the ground truth", fontsize=9)
    fig.tight_layout()
    fig.savefig(HERE / "conf_vs_error.png", dpi=110)
    print(f"figure: {HERE / 'conf_vs_error.png'}")

    print("\n=== verdict vs declared Gate A ===")
    r_covs = [r[1] for r in rows]
    print(f"primary (covered-region Spearman, gate >= {GATE_RHO} on all "
          f"seeds): {[f'{r:+.3f}' for r in r_covs]}")
    if min(r_covs) >= GATE_RHO:
        print("   -> GATE A PASSED: the geometry-only certificate ranks "
              "true error above the declared bar on every seed.")
    else:
        print("   -> GATE A NOT PASSED on at least one seed -- recorded; "
              "per the declared falsification, return to score design "
              "before any Phase 1 work.")
    print("auxiliary (descriptive, not the gate): "
          f"all-points {[f'{r[2]:+.3f}' for r in rows]}, "
          f"model-support {[f'{r[3]:+.3f}' for r in rows]}")


if __name__ == "__main__":
    main()
