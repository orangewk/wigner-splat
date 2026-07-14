"""Experiment 14 -- rank-R x squeezed x loss on the GKP data (issue #40).

Exp13 (exploratory reanalysis, PR #37) left a descriptive residual on the
Furusawa GKP dataset: lossy rank-1 K=4 sits +0.002..+0.004 nats above the
test-selected MLE frontier best on both split reshuffles. Its physical
cause was explicitly NOT identified -- optimization, finite-K/pure-state
capacity, and misspecification of a single Gaussian loss channel all remain
open. Issue #40 tests ONE of those hypotheses: give the ansatz genuine rank
freedom (rho = B B^dagger with R independent squeezed-ket columns, then the
same fitted loss channel; PSD by construction, closed form throughout --
bbdagS.MixedSqueezedKetState).

EXPLORATORY REANALYSIS PROTOCOL (declared before this run, but the dataset,
the exp12/13 results, and one 100-iteration R=2 smoke fit had already been
inspected; split seeds 0 and 1 are the same reshuffles exp13 used, so
nothing here is preregistered or an independent holdout):

  * PRIMARY config PRE-FIXED: lossy mixed R=2, K=4. Secondary (primary
    split only, never test-selected): R=3, K=4 -- the rank-saturation probe.
  * BASELINE rerun in-script under IDENTICAL conditions (same split, seeds,
    iters, lr): lossy rank-1 K=4, so the rank axis is the only difference.
  * init seeds {0, 1, 2} per config, selection by TRAIN NLL only,
    convergence flagged by the train-NLL drop over the final 100 iters.
  * MLE n_max dof frontier as in exp13; the reported opponent is the
    EMPIRICAL test-selected best (descriptive oracle favoring the MLE).
  * CONDITIONAL paired bootstraps (B = 2000) describe test-sample variation
    for the already-fitted models: (mixed - rank1) and (mixed - best MLE).
    They do not account for model or n_max selection.
  * ALTERNATE-SPLIT SENSITIVITY CHECK: seed 1 reshuffle, rank-1 + R=2 +
    frontier only.

Exploratory decision checks (descriptive, not confirmatory):
  1. Does rank do anything on real data? CI(mixed R=2 - rank1) below 0 on
     the primary split = descriptive support for the rank hypothesis;
     an interval containing 0 = rank freedom bought nothing here, which
     would point the residual at the OTHER hypotheses (optimization /
     ket capacity / non-Gaussian noise).
  2. Does it reach the frontier? CI(mixed - best MLE) including or below 0
     = the descriptive gap of exp13 is closed for these fits.
  3. Rank saturation: R=3 vs R=2 train NLL (primary split) -- does more
     rank keep helping, at matched budget?
  4. eta-vs-rank identifiability is EXPECTED (rank absorbs mixedness and
     pushes fitted eta up, as the smoke fit showed 0.64 -> 0.72); fitted
     eta is reported as a model parameter, not a calibrated efficiency.

dof accounting (real parameters): mixed = 6RK - R (per-column global
phases) - 1 (global scale) + 1 (eta): R=2,K=4 -> 46; R=3,K=4 -> 69;
rank-1 K=4 -> 23. MLE n_max -> n_max^2 - 1.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS_lossy, fit_bbdagS_lossy_mixed, lossy_pdf, lossy_pdf_mixed,
    nll_lossy, nll_lossy_mixed,
)
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "12_gkp_data" / "data"
OUT_FIG = pathlib.Path(__file__).resolve().parent / "gkp_rank_marginals.png"
OUT_FRONTIER = pathlib.Path(__file__).resolve().parent / "gkp_rank_frontier.png"
DEGS = (0, 30, 60, -30, -60, -90)
TRAIN_FRACTION = 0.8
PRIMARY_SPLIT_SEED = 0
ALT_SPLIT_SEED = 1
N_MAX_GRID = (4, 6, 8, 10, 12, 16, 20, 25)
BINS = 80
K = 4
PRIMARY_R = 2
SECONDARY_R = 3
INIT_SEEDS = (0, 1, 2)
ITERS = 500
LEARNING_RATE = 0.05
ETA0 = 0.8
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 123


def load_gkp_data():
    data = []
    for deg in DEGS:
        arr = np.load(DATA_DIR / f"quad_{deg}deg.npy")
        data.append((np.deg2rad(deg), np.asarray(arr, float)))
    return data


def split(data, seed):
    rng = np.random.default_rng(seed)
    train, test = [], []
    for th, x in data:
        idx = rng.permutation(len(x))
        n_tr = int(TRAIN_FRACTION * len(x))
        train.append((th, x[idx[:n_tr]]))
        test.append((th, x[idx[n_tr:]]))
    return train, test


def as_bbdag(data):
    return [(np.array([th]), x[:, None]) for th, x in data]


def dof(R):
    return 6 * R * K - R - 1 + 1


def per_sample_nll_mle(rho, data):
    out = []
    for th, x in data:
        p = np.maximum(marginal_from_rho(rho, x, th), 1e-300)
        out.append(-np.log(p))
    return np.concatenate(out)


def per_sample_nll_bb(st, eta, data, mixed):
    pdf = lossy_pdf_mixed if mixed else lossy_pdf
    out = []
    for th, x in as_bbdag(data):
        out.append(-np.log(np.maximum(pdf(st, x, th, eta), 1e-300)))
    return np.concatenate(out)


def fit_config(train, R, label):
    """R = 1 uses the rank-1 fitter; selection by TRAIN NLL over INIT_SEEDS."""
    best = None
    for seed in INIT_SEEDS:
        trace = []
        cb = lambda t, v, *rest: trace.append(v)  # noqa: E731
        t0 = time.perf_counter()
        if R == 1:
            st, eta = fit_bbdagS_lossy(train, K=K, M=1, eta0=ETA0,
                                       iters=ITERS, lr=LEARNING_RATE,
                                       seed=seed, callback=cb)
            tr = nll_lossy(st, train, eta)
        else:
            st, eta = fit_bbdagS_lossy_mixed(train, R=R, K=K, M=1, eta0=ETA0,
                                             iters=ITERS, lr=LEARNING_RATE,
                                             seed=seed, callback=cb)
            tr = nll_lossy_mixed(st, train, eta)
        wall = time.perf_counter() - t0
        conv = trace[-5] - trace[-1] if len(trace) >= 5 else float("nan")
        flag = "  [NOT CONVERGED]" if conv > 1e-3 else ""
        print(f"    {label} seed={seed}: train NLL={tr:.5f}  "
              f"final-100-iter drop={conv:+.5f}{flag}  eta={eta:.4f}  "
              f"wall={wall:.0f}s", flush=True)
        if best is None or tr < best[0]:
            best = (tr, seed, st, eta)
    tr, seed, st, eta = best
    print(f"    -> {label}: best-by-TRAIN seed={seed}  train NLL={tr:.5f}")
    return st, eta, tr


def mle_frontier(train, test):
    centers, targets = histogram_targets(train, bins=BINS)
    rows = []
    for n_max in N_MAX_GRID:
        rho, iters = mle_reconstruct(centers, targets, n_max=n_max,
                                     max_iters=2000)
        te = float(np.mean(per_sample_nll_mle(rho, test)))
        rows.append((n_max, n_max ** 2 - 1, te, rho))
        print(f"    mle n_max={n_max:2d} (dof {n_max ** 2 - 1:3d}, "
              f"{iters} iters): test NLL={te:.5f}", flush=True)
    best = min(rows, key=lambda r: r[2])
    print(f"    -> empirical test-selected frontier best (descriptive): "
          f"n_max={best[0]} test NLL={best[2]:.5f}")
    return rows, best


def paired_bootstrap_ci(diff, B, seed):
    rng = np.random.default_rng(seed)
    n = len(diff)
    means = np.array([np.mean(diff[rng.integers(0, n, n)]) for _ in range(B)])
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def run_split(name, split_seed, rs):
    data = load_gkp_data()
    train_raw, test_raw = split(data, split_seed)
    train = as_bbdag(train_raw)
    print(f"\n--- split '{name}' (seed {split_seed}) ---")
    fits = {}
    for R in rs:
        label = f"lossy R={R} K={K}"
        st, eta, tr = fit_config(train, R, label)
        te = float(np.mean(per_sample_nll_bb(st, eta, test_raw, mixed=R > 1)))
        print(f"    {label}: test NLL={te:.5f}  (dof {dof(R)})", flush=True)
        fits[R] = (st, eta, tr, te)
    print("  MLE dof frontier:")
    rows, best_mle = mle_frontier(train_raw, test_raw)
    return data, test_raw, fits, rows, best_mle


def cis(fits, test_raw, best_mle):
    d1 = per_sample_nll_bb(fits[1][0], fits[1][1], test_raw, mixed=False)
    d2 = per_sample_nll_bb(fits[PRIMARY_R][0], fits[PRIMARY_R][1], test_raw,
                           mixed=True)
    dm = per_sample_nll_mle(best_mle[3], test_raw)
    ci_rank = paired_bootstrap_ci(d2 - d1, BOOTSTRAP_B, BOOTSTRAP_SEED)
    ci_mle = paired_bootstrap_ci(d2 - dm, BOOTSTRAP_B, BOOTSTRAP_SEED)
    return ci_rank, ci_mle, float(np.mean(d2 - d1)), float(np.mean(d2 - dm))


def main():
    print("=== exp14: rank-R x squeezed x loss on real GKP data ===")
    print("(post-review exploratory reanalysis protocol; see docstring)")

    data, test_raw, fits, rows, best_mle = run_split(
        "primary (exp12/13 split, reused for comparability)",
        PRIMARY_SPLIT_SEED, rs=(1, PRIMARY_R, SECONDARY_R),
    )
    ci_rank, ci_mle, pt_rank, pt_mle = cis(fits, test_raw, best_mle)
    print(f"\n  conditional paired bootstrap 95% CIs (primary split):")
    print(f"    mixed R={PRIMARY_R} - rank1:    [{ci_rank[0]:+.5f}, "
          f"{ci_rank[1]:+.5f}]  (point {pt_rank:+.5f})")
    print(f"    mixed R={PRIMARY_R} - best MLE: [{ci_mle[0]:+.5f}, "
          f"{ci_mle[1]:+.5f}]  (point {pt_mle:+.5f})")
    print(f"  rank saturation (train NLL, matched budget): "
          f"R=1 {fits[1][2]:.5f}, R=2 {fits[PRIMARY_R][2]:.5f}, "
          f"R=3 {fits[SECONDARY_R][2]:.5f}")
    print(f"  fitted eta by R (identifiability, not calibration): "
          f"R=1 {fits[1][1]:.4f}, R=2 {fits[PRIMARY_R][1]:.4f}, "
          f"R=3 {fits[SECONDARY_R][1]:.4f}")

    _, test_alt, fits_alt, rows_alt, best_mle_alt = run_split(
        "alternate reshuffle (sensitivity check)",
        ALT_SPLIT_SEED, rs=(1, PRIMARY_R),
    )
    ci_rank_a, ci_mle_a, pt_rank_a, pt_mle_a = cis(fits_alt, test_alt,
                                                   best_mle_alt)
    print(f"\n  conditional CIs (alternate reshuffle):")
    print(f"    mixed R={PRIMARY_R} - rank1:    [{ci_rank_a[0]:+.5f}, "
          f"{ci_rank_a[1]:+.5f}]  (point {pt_rank_a:+.5f})")
    print(f"    mixed R={PRIMARY_R} - best MLE: [{ci_mle_a[0]:+.5f}, "
          f"{ci_mle_a[1]:+.5f}]  (point {pt_mle_a:+.5f})")

    # figures
    st, eta = fits[PRIMARY_R][0], fits[PRIMARY_R][1]
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    for ax, (th, x) in zip(axes.ravel(), data):
        xs = np.linspace(-5, 5, 400)
        ax.hist(x, bins=100, density=True, alpha=0.5, label="data (all)")
        ax.plot(xs, lossy_pdf_mixed(st, xs[:, None], np.array([th]), eta),
                "r-", lw=1.5, label=f"BB† R={PRIMARY_R} K={K} (η={eta:.2f})")
        ax.plot(xs, marginal_from_rho(best_mle[3], xs, th), "k--", lw=1.2,
                label=f"MLE n={best_mle[0]}")
        ax.set_title(f"{np.rad2deg(th):+.0f} deg")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=100)

    fig2, ax = plt.subplots(figsize=(7, 5))
    ax.plot([r[1] for r in rows], [r[2] for r in rows], "ko-",
            label="MLE (n_max grid)")
    marks = {1: "b^", PRIMARY_R: "r*", SECONDARY_R: "m*"}
    for R, (_, _, _, te) in fits.items():
        ax.plot(dof(R), te, marks[R], ms=12, label=f"BB† lossy R={R} K={K}")
    ax.set_xlabel("real degrees of freedom")
    ax.set_ylabel("held-out per-sample NLL")
    ax.set_xscale("log")
    ax.legend(fontsize=8)
    ax.set_title("NLL-dof frontier with rank (primary split)")
    plt.tight_layout()
    plt.savefig(OUT_FRONTIER, dpi=100)
    print(f"  figures: {OUT_FIG}, {OUT_FRONTIER}")

    print("\n=== exploratory decision checks (see docstring) ===")
    if ci_rank[1] < 0 and ci_rank_a[1] < 0:
        v1 = ("rank freedom DESCRIPTIVELY HELPS on both reshuffles "
              "(CIs below 0)")
    elif ci_rank[0] > 0 and ci_rank_a[0] > 0:
        v1 = "rank freedom descriptively HURTS held-out NLL (CIs above 0)"
    else:
        v1 = ("no descriptive rank effect resolvable at CI width -- points "
              "the exp13 residual at the other hypotheses (optimization / "
              "ket capacity / non-Gaussian noise)")
    print(f"1. rank effect: {v1}")
    if ci_mle[1] < 0 and ci_mle_a[1] < 0:
        v2 = "frontier gap CLOSED descriptively (both CIs below 0)"
    elif ci_mle[0] > 0 and ci_mle_a[0] > 0:
        v2 = ("frontier gap REMAINS for these fits (both CIs above 0) -- "
              "recorded as another descriptive loss")
    else:
        v2 = "at CI resolution the fits TIE the test-selected MLE frontier"
    print(f"2. vs MLE frontier: {v2}")
    print(f"3. rank saturation and 4. fitted-eta drift: see lines above.")


if __name__ == "__main__":
    main()
