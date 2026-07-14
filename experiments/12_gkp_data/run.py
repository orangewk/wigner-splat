"""Experiment 12 -- FIRST REAL DATA: propagating-light GKP states (issue #41).

Dataset: Konno, Asavanant, Hanamura, ..., Furusawa, "Logical states for
fault-tolerant quantum computation with propagating light", Science 383, 289
(2024). Raw homodyne quadrature values from Dryad, doi:10.5061/dryad.t76hdr86j
(CC0; redistributed under data/ with the original Dryad README). Six LO
phases (0, +-30, +-60, -90 deg), ~20k shots each -- the first non-synthetic
data this program has ever seen.

Conventions observed from the data (recorded, not assumed):
  * 0-deg peak spacing ~1.69 ~ sqrt(pi) => the data are consistent with the
    repo's hbar=1 / vacuum-variance-1/2 convention; no rescaling applied.
  * A phase-INDEPENDENT mean offset ~ -0.26 across all six phases: a coherent
    displacement would rotate as cos(theta - phi) over the 150-deg span, so
    this is an instrumental/calibration offset (or a genuinely displaced
    state; the paper's own MLE would absorb it either way). First pass fits
    the data AS-IS -- no offset subtraction.

Contenders (single mode):
  * BB-dagger squeezed-product ansatz (bbdagS, M=1) -- per-sample NLL,
    analytic gradients, PURE (rank-1) by construction. GKP is natively a
    superposition of squeezed kets, so the representation matches; the
    RANK does not (a real lossy GKP state is mixed).
  * mle (R rho R, n_max=25) on binned histograms -- the paper's own method
    class, full rank.
Metric: per-sample NLL on a held-out 20% split (no ground truth exists for
real data, so likelihood generalization is the honest scalar; marginal
overlays are the qualitative check).

Falsification-style expectation (declared before the run): if the pure
ansatz shows systematically over-deep interference dips vs the data, the
deficit is MIXEDNESS, and the fix is the rank-R x squeezed extension
(issue #40) plus the efficiency/noise model (issue #42) -- not more kets.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.bbdagS import SqueezedKetState, fit_bbdagS, nll  # noqa: E402
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402

DATA_DIR = pathlib.Path(__file__).resolve().parent / "data"
OUT_FIG = pathlib.Path(__file__).resolve().parent / "gkp_marginals.png"
DEGS = (0, 30, 60, -30, -60, -90)
SPLIT_SEED = 0
TRAIN_FRACTION = 0.8
N_MAX_MLE = 25
BINS = 80
K_VALUES = (4, 6)
ITERS = 300
LEARNING_RATE = 0.05
INIT_SEED = 0


def load_gkp_data():
    """[(theta_rad, samples (S,))] from the Dryad npy files, phases from names."""
    data = []
    for deg in DEGS:
        arr = np.load(DATA_DIR / f"quad_{deg}deg.npy")
        data.append((np.deg2rad(deg), np.asarray(arr, float)))
    return data


def split(data, rng):
    train, test = [], []
    for th, x in data:
        idx = rng.permutation(len(x))
        n_tr = int(TRAIN_FRACTION * len(x))
        train.append((th, x[idx[:n_tr]]))
        test.append((th, x[idx[n_tr:]]))
    return train, test


def as_bbdag(data):
    return [(np.array([th]), x[:, None]) for th, x in data]


def mle_per_sample_nll(rho, data):
    tot, n = 0.0, 0
    for th, x in data:
        p = marginal_from_rho(rho, x, th)
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(x)
    return tot / n


def main():
    data = load_gkp_data()
    print("=== exp12: first real data -- Furusawa-group GKP (Science 2024) ===")
    for th, x in data:
        print(f"  {np.rad2deg(th):+4.0f} deg: n={len(x)}  mean={x.mean():+.4f}  "
              f"var={x.var():.4f}")
    train, test = split(data, np.random.default_rng(SPLIT_SEED))

    results = {}
    for K in K_VALUES:
        t0 = time.perf_counter()
        st = fit_bbdagS(as_bbdag(train), K=K, M=1, iters=ITERS,
                        lr=LEARNING_RATE, seed=INIT_SEED)
        wall = time.perf_counter() - t0
        tr = nll(st, as_bbdag(train))
        te = nll(st, as_bbdag(test))
        print(f"  bbdagS K={K} (pure): train NLL={tr:.4f}  test NLL={te:.4f}  "
              f"wall={wall:.0f}s  squeezes r={np.round(np.abs(st.xi.ravel()), 2)}",
              flush=True)
        results[f"bbdagS K={K}"] = (st, te)

    centers, targets = histogram_targets(train, bins=BINS)
    t0 = time.perf_counter()
    rho, iters = mle_reconstruct(centers, targets, n_max=N_MAX_MLE,
                                 max_iters=2000)
    wall = time.perf_counter() - t0
    tr = mle_per_sample_nll(rho, train)
    te = mle_per_sample_nll(rho, test)
    print(f"  mle n_max={N_MAX_MLE} (full rank, {iters} iters): "
          f"train NLL={tr:.4f}  test NLL={te:.4f}  wall={wall:.0f}s", flush=True)

    st6 = results["bbdagS K=6"][0]
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    Z = st6.norm_sq()
    for ax, (th, x) in zip(axes.ravel(), data):
        xs = np.linspace(-5, 5, 400)
        ax.hist(x, bins=100, density=True, alpha=0.5, label="data (all)")
        p_bb = np.abs(st6.psi_at(xs[:, None], np.array([th]))) ** 2 / Z
        ax.plot(xs, p_bb, "r-", lw=1.5, label="BB† K=6 (pure)")
        ax.plot(xs, marginal_from_rho(rho, xs, th), "k--", lw=1.2,
                label=f"MLE n={N_MAX_MLE}")
        ax.set_title(f"{np.rad2deg(th):+.0f} deg")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=100)
    print(f"  figure: {OUT_FIG}")

    best_bb = min(te for _, te in results.values())
    print("\n=== first-contact verdict (declared expectation in docstring) ===")
    print(f"held-out per-sample NLL: best pure BB-dagger {best_bb:.4f} vs "
          f"full-rank MLE {te:.4f}")
    if te < best_bb:
        print("-> MLE WINS on real data: the pure (rank-1) ansatz cannot wash "
              "out interference contrast the way the real (lossy, mixed) "
              "state does -- visible as over-deep dips in the overlay. "
              "Actionable: rank-R x squeezed ansatz (issue #40) + "
              "efficiency/noise model (issue #42), benchmarked on THIS data.")
    else:
        print("-> pure BB-dagger matches or beats full-rank MLE on held-out "
              "likelihood.")


if __name__ == "__main__":
    main()
