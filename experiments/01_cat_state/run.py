"""Experiment 01: reconstruct an even cat state from simulated homodyne data.

Generates shot-noise-limited homodyne samples at several LO phases, fits a
signed splat mixture with the v0 reconstructor, and writes a comparison
figure (true Wigner / reconstruction / marginals) to out/.
"""

import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit import fit, histogram_targets, loss  # noqa: E402
from wigner_splat.states import CatState  # noqa: E402

ALPHA = 1.5
ANGLES = np.linspace(0, np.pi, 12, endpoint=False)
SHOTS = 4000
K = 8

out = pathlib.Path(__file__).parent / "out"
out.mkdir(exist_ok=True)

cat = CatState(alpha=ALPHA, parity=+1)
data = cat.sample_homodyne(ANGLES, SHOTS, rng=42)
print(f"generated {len(ANGLES)} angles x {SHOTS} shots")

mix = fit(data, K=K, iters=600, seed=0,
          callback=lambda t, l: print(f"  iter {t:4d}  loss {l:.3e}"))

# --- report ---
xs = np.linspace(-4.5, 4.5, 201)
X, P = np.meshgrid(xs, xs)
w_true, w_fit = cat.wigner(X, P), mix.wigner(X, P)
l2 = np.sqrt(np.mean((w_true - w_fit) ** 2)) / np.sqrt(np.mean(w_true ** 2))
print(f"relative L2 error on Wigner grid: {l2:.3f}")
print(f"min of reconstruction: {w_fit.min():.4f} (true: {w_true.min():.4f}) "
      f"-> negativity {'recovered' if w_fit.min() < -0.01 else 'NOT recovered'}")

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    lim = max(abs(w_true).max(), abs(w_fit).max())
    for ax, w, title in [(axes[0], w_true, "true Wigner"), (axes[1], w_fit, f"signed splats (K={K})")]:
        im = ax.pcolormesh(X, P, w, cmap="RdBu_r", vmin=-lim, vmax=lim)
        ax.set_title(title)
        ax.set_aspect("equal")
        fig.colorbar(im, ax=ax)
    centers, targets = histogram_targets(data)
    theta0, hist0 = targets[0]
    axes[2].plot(centers, hist0, "k.", ms=3, label="homodyne histogram")
    axes[2].plot(centers, mix.radon(centers, theta0), "-", label="model marginal")
    axes[2].plot(centers, cat.homodyne_pdf(centers, theta0), "--", label="true pdf")
    axes[2].set_title(f"marginal at theta={theta0:.2f}")
    axes[2].legend()
    fig.tight_layout()
    fig.savefig(out / "cat_reconstruction.png", dpi=150)
    print(f"wrote {out / 'cat_reconstruction.png'}")
except ImportError:
    print("matplotlib not available; skipped figure")
