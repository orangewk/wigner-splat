"""Experiment 13 -- GKP rematch with the detection-efficiency model (issue #42).

Experiment 12 (first real data) diagnosed the pure squeezed-product BB-dagger
ansatz's loss against full-rank MLE as MIXEDNESS: the real propagating GKP
state (Konno et al., Science 383, 289 (2024); Dryad doi:10.5061/dryad.t76hdr86j,
data under ../12_gkp_data/data/) is mixed, dominantly by optical loss, and a
rank-1 model digs interference dips too deep. Issue #42 adds the minimal
physical fix: model the MEASURED pdf as the pure-ansatz pdf convolved with the
loss Gaussian (efficiency eta, fitted), which is exactly the homodyne marginal
of loss_eta(|psi><psi|/Z) -- PSD by construction, closed form throughout
(bbdagS lossy section), and |psi> doubles as a loss-corrected pure estimate.

Same protocol as exp12: 80/20 split (SPLIT_SEED=0), per-sample NLL on the
held-out 20%. Baselines: exp12's committed numbers -- pure bbdagS K=4 test
NLL 1.7670, full-rank MLE (n_max=25) test NLL 1.6299 -- with the MLE
recomputed in-run for self-containedness.

Falsification condition (declared before the run): the single-knob loss model
must close MOST of the pure-vs-MLE gap (0.137 nats) or the mixedness story of
exp12 is wrong. The headline claim "physical few-parameter model matches
full-rank MLE on real data" additionally requires test NLL <= MLE's; if the
model lands short of MLE, the residual is the non-Gaussian part of the noise
(rank beyond loss), and the claim passes to issue #40 (rank-R x squeezed) --
recorded as a loss here either way.

Parameter count, K=4: 4 z + 4 alpha + 4 xi complex = 24 real + eta = 25,
vs 625 for the MLE density matrix.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.bbdagS import fit_bbdagS_lossy, lossy_pdf, nll_lossy  # noqa: E402
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "12_gkp_data" / "data"
OUT_FIG = pathlib.Path(__file__).resolve().parent / "gkp_eta_marginals.png"
DEGS = (0, 30, 60, -30, -60, -90)
SPLIT_SEED = 0
TRAIN_FRACTION = 0.8
N_MAX_MLE = 25
BINS = 80
K_VALUES = (4, 6)
ITERS = 500
LEARNING_RATE = 0.05
INIT_SEED = 0
ETA0 = 0.8
EXP12_PURE_K4 = 1.7670  # committed exp12 out_run.log
EXP12_MLE = 1.6299      # committed exp12 out_run.log


def load_gkp_data():
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
    train, test = split(data, np.random.default_rng(SPLIT_SEED))
    print("=== exp13: GKP rematch -- pure squeezed BB-dagger + fitted loss eta ===")
    print(f"benchmark from exp12 (committed): pure K=4 test NLL {EXP12_PURE_K4}, "
          f"full-rank MLE test NLL {EXP12_MLE}")

    results = {}
    for K in K_VALUES:
        t0 = time.perf_counter()
        st, eta = fit_bbdagS_lossy(
            as_bbdag(train), K=K, M=1, eta0=ETA0, iters=ITERS,
            lr=LEARNING_RATE, seed=INIT_SEED,
            callback=lambda t, v, e: print(
                f"    iter {t:4d}  train NLL={v:.4f}  eta={e:.4f}", flush=True)
            if t % 100 == 0 else None,
        )
        wall = time.perf_counter() - t0
        tr = nll_lossy(st, as_bbdag(train), eta)
        te = nll_lossy(st, as_bbdag(test), eta)
        print(f"  bbdagS+loss K={K}: train NLL={tr:.4f}  test NLL={te:.4f}  "
              f"eta={eta:.4f}  wall={wall:.0f}s  "
              f"squeezes r={np.round(np.abs(st.xi.ravel()), 2)}", flush=True)
        results[K] = (st, eta, te)

    centers, targets = histogram_targets(train, bins=BINS)
    t0 = time.perf_counter()
    rho, iters = mle_reconstruct(centers, targets, n_max=N_MAX_MLE,
                                 max_iters=2000)
    wall = time.perf_counter() - t0
    te_mle = mle_per_sample_nll(rho, test)
    print(f"  mle n_max={N_MAX_MLE} (full rank, {iters} iters): "
          f"train NLL={mle_per_sample_nll(rho, train):.4f}  "
          f"test NLL={te_mle:.4f}  wall={wall:.0f}s", flush=True)

    K_best = min(results, key=lambda K: results[K][2])
    st, eta, te_bb = results[K_best]
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    for ax, (th, x) in zip(axes.ravel(), data):
        xs = np.linspace(-5, 5, 400)
        ax.hist(x, bins=100, density=True, alpha=0.5, label="data (all)")
        p_bb = lossy_pdf(st, xs[:, None], np.array([th]), eta)
        ax.plot(xs, p_bb, "r-", lw=1.5,
                label=f"BB† K={K_best} + loss (η={eta:.2f})")
        ax.plot(xs, marginal_from_rho(rho, xs, th), "k--", lw=1.2,
                label=f"MLE n={N_MAX_MLE}")
        ax.set_title(f"{np.rad2deg(th):+.0f} deg")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=100)
    print(f"  figure: {OUT_FIG}")

    gap_closed = (EXP12_PURE_K4 - te_bb) / (EXP12_PURE_K4 - te_mle)
    print("\n=== rematch verdict (falsification condition in docstring) ===")
    print(f"held-out per-sample NLL: BB-dagger+loss (K={K_best}, "
          f"{6 * K_best + 1} real params) {te_bb:.4f} vs full-rank MLE "
          f"({N_MAX_MLE ** 2} real params) {te_mle:.4f}")
    print(f"pure->MLE gap closed by the single eta knob: {100 * gap_closed:.0f}%")
    if te_bb <= te_mle:
        print("-> BB-dagger+loss MATCHES OR BEATS full-rank MLE on real data: "
              "the exp12 mixedness diagnosis was right, and one physical loss "
              "parameter was the missing piece. The fitted |psi> is a "
              "loss-corrected pure GKP estimate (eta printed above).")
    elif gap_closed >= 0.5:
        print("-> mixedness diagnosis CONFIRMED (most of the gap was loss) "
              "but MLE keeps a residual edge: the leftover is structure a "
              "single Gaussian loss channel cannot express -> issue #40 "
              "(rank-R x squeezed) takes the remaining deficit. Recorded as "
              "a loss on the headline claim.")
    else:
        print("-> loss model FAILED to close most of the gap: the exp12 "
              "mixedness-by-loss story is wrong or incomplete. Recorded as "
              "a loss; rediagnose before touching issue #40.")


if __name__ == "__main__":
    main()
