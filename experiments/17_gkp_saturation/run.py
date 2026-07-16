"""Experiment 17 -- issue #40 follow-up: rank saturation on the GKP data.

Exp14 (PR #44) left three open threads: train NLL was still improving at
R=3 under the fixed schedule (so the rank curve had not visibly plateaued),
warm starts were untested (so under-optimization of the cold-started deeper
ranks could not be ruled out), and the rank-vs-K interplay had only the
46/47-dof control point. The frontier deficit after exp14 was half a
millinat: CI(R=2 - best MLE) = [+0.00055, +0.00149] primary /
[+0.00002, +0.00093] alternate.

EXPLORATORY REANALYSIS PROTOCOL (declared before this run; same standing
caveats as exp13/14 -- the dataset and all prior results have been
inspected, split seeds 0/1 are the same reshuffles, the MLE opponent is the
empirical test-selected frontier best, and the paired bootstrap intervals
are conditional on the fitted models; nothing here is preregistered):

  * Deeper ranks, PRE-FIXED: R=4 K=4 on BOTH reshuffles (primary probe);
    R=5 K=4 on the primary split only. Cold starts, init seeds {0,1,2},
    selection by TRAIN NLL, same schedule as exp14 (iters=500, lr=0.05,
    eta0=0.8 jointly fitted).
  * Rank curve context on each split: R=3 K=4 refitted here (same protocol;
    exp14 ran it on the primary split only, and no fitted state was
    persisted, so both splits refit it for the paired comparisons and the
    warm-start parent). Exp14's committed R=1/R=2 test NLLs are quoted as
    context constants, not refitted.
  * WARM STARTS (optimization hypothesis, primary split): grow the
    best-by-train R=3 fit to R=4 (append one fresh random column at small
    weight 0.05, eta0 = the parent's fitted eta), fit the same 500-iter
    schedule; then grow the better of {cold-best R=4, warm R=4} to R=5.
  * K INTERPLAY at the ~70-dof frontier point (primary split): R=2 K=6
    (dof 70) vs R=3 K=4 (dof 69), cold, 3 init seeds each -- does a dof
    spent on rank beat a dof spent on ket count where the MLE frontier has
    flattened?
  * MLE dof frontier rerun per split (deterministic; needed for per-sample
    paired vectors).

Pre-declared decision checks (descriptive, not confirmatory):
  1. SATURATION: successive best-by-train drops delta(R) = train(R-1) -
     train(R). Exp14 saw delta(3) = +0.00073. If delta(4) (and delta(5))
     fall below 0.0002 nats (about the paired-CI resolution), the rank
     curve is FLATTENING under this schedule; if held-out NLL stops
     improving while train NLL still falls, the extra rank is fitting
     noise, not structure.
  2. FRONTIER: CI(R=4 - best MLE) on both reshuffles. Both CIs below 0 =
     first descriptive WIN against the test-selected MLE; both above 0 =
     fourth descriptive loss; straddling = tie at CI resolution.
  3. OPTIMIZATION: warm R=4 train NLL vs cold-best R=4 train NLL. Warm
     better by more than 0.0001 nats = cold starts under-optimize at this
     depth (part of the residual is optimization, not model class); within
     0.0001 = the schedule is adequate and the optimization hypothesis is
     descriptively disfavored at R=4.
  4. K INTERPLAY: paired CI(R=3 K=4 - R=2 K=6) held-out on the primary
     split. Below 0 = rank beats ket count at matched dof (consistent with
     the exp14 46-dof control); above 0 = the opposite; straddling = no
     resolvable difference.
  5. eta drift by R is recorded (identifiability trade, pre-declared in
     exp14; fitted eta is a model parameter, not a calibrated efficiency).

dof accounting (real parameters): 6RK - R - 1 + 1: R4K4 -> 92, R5K4 -> 115,
R2K6 -> 70, R3K4 -> 69. MLE n_max -> n_max^2 - 1.

Context constants from the exp14 committed log (NOT refit here):
  primary:   R1K4 test 1.63304 (23 dof), R2K4 test 1.63084 (46 dof),
             R3K4 test 1.63009 (69 dof), best MLE n16 1.62984;
             train best-by-seed: R1 1.62938, R2 1.62761, R3 1.62688.
  alternate: R1K4 test 1.62975, R2K4 test 1.62770, best MLE n16 1.62722.
"""
import json
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from wigner_splat.bbdagS import (  # noqa: E402
    MixedSqueezedKetState, fit_bbdagS_lossy_mixed, lossy_pdf_mixed,
    nll_lossy_mixed,
)
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "12_gkp_data" / "data"
OUT_DIR = pathlib.Path(__file__).resolve().parent
DEGS = (0, 30, 60, -30, -60, -90)
TRAIN_FRACTION = 0.8
PRIMARY_SPLIT_SEED = 0
ALT_SPLIT_SEED = 1
N_MAX_GRID = (4, 6, 8, 10, 12, 16, 20, 25)
BINS = 80
INIT_SEEDS = (0, 1, 2)
ITERS = 500
LEARNING_RATE = 0.05
ETA0 = 0.8
WARM_COLUMN_WEIGHT = 0.05
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 123
EPS_FLAT = 0.0002
EPS_WARM = 0.0001
EXP14 = {  # committed exp14 context constants (test NLL, train best)
    "primary": {"R1_test": 1.63304, "R2_test": 1.63084, "R3_test": 1.63009,
                "mle_test": 1.62984,
                "R1_train": 1.62938, "R2_train": 1.62761,
                "R3_train": 1.62688},
    "alternate": {"R1_test": 1.62975, "R2_test": 1.62770,
                  "mle_test": 1.62722},
}


def load_gkp_data():
    return [
        (np.deg2rad(deg),
         np.asarray(np.load(DATA_DIR / f"quad_{deg}deg.npy"), float))
        for deg in DEGS
    ]


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


def dof(R, K):
    return 6 * R * K - R - 1 + 1


def per_sample_nll_mle(rho, data):
    return np.concatenate([
        -np.log(np.maximum(marginal_from_rho(rho, x, th), 1e-300))
        for th, x in data
    ])


def per_sample_nll_bb(st, eta, data):
    return np.concatenate([
        -np.log(np.maximum(lossy_pdf_mixed(st, x, th, eta), 1e-300))
        for th, x in as_bbdag(data)
    ])


def one_fit(train, R, K, seed=0, init=None, eta0=ETA0, label=""):
    trace = []
    cb = lambda t, v, *rest: trace.append(v)  # noqa: E731
    t0 = time.perf_counter()
    st, eta = fit_bbdagS_lossy_mixed(train, R=R, K=K, M=1, eta0=eta0,
                                     iters=ITERS, lr=LEARNING_RATE,
                                     seed=seed, callback=cb, init=init)
    wall = time.perf_counter() - t0
    tr = nll_lossy_mixed(st, train, eta)
    conv = trace[-5] - trace[-1] if len(trace) >= 5 else float("nan")
    flag = "  [NOT CONVERGED]" if conv > 1e-3 else ""
    src = "warm" if init is not None else f"seed={seed}"
    print(f"    {label} {src}: train NLL={tr:.5f}  "
          f"final-100-iter drop={conv:+.5f}{flag}  eta={eta:.4f}  "
          f"wall={wall:.0f}s", flush=True)
    return st, eta, tr


def fit_cold(train, R, K, label):
    best = None
    for seed in INIT_SEEDS:
        st, eta, tr = one_fit(train, R, K, seed=seed, label=label)
        if best is None or tr < best[2]:
            best = (st, eta, tr, seed)
    st, eta, tr, seed = best
    print(f"    -> {label}: best-by-TRAIN seed={seed}  train NLL={tr:.5f}")
    return st, eta, tr


def grow(state, K, rng_seed):
    """Append one fresh random column at small weight (warm-start init)."""
    rng = np.random.default_rng(rng_seed)
    M = state.M
    z_new = WARM_COLUMN_WEIGHT * np.ones((1, K), complex) / np.sqrt(K)
    a_new = rng.uniform(-1.5, 1.5, (1, K, M)) \
        + 1j * rng.uniform(-1.5, 1.5, (1, K, M))
    return MixedSqueezedKetState(
        z=np.vstack([state.z, z_new]),
        alpha=np.vstack([state.alpha, a_new]),
        xi=np.vstack([state.xi, np.zeros((1, K, M), complex)]),
    )


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


def paired_bootstrap_ci(diff, B=BOOTSTRAP_B, seed=BOOTSTRAP_SEED):
    rng = np.random.default_rng(seed)
    n = len(diff)
    means = np.array([np.mean(diff[rng.integers(0, n, n)]) for _ in range(B)])
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def report_ci(name, a, b):
    d = a - b
    lo, hi = paired_bootstrap_ci(d)
    print(f"    {name}: [{lo:+.5f}, {hi:+.5f}]  (point {np.mean(d):+.5f})")
    return lo, hi, float(np.mean(d))


def main():
    print("=== exp17: rank saturation / warm starts / K interplay on the "
          "GKP data ===")
    print("(exploratory reanalysis protocol; see docstring)")
    results = {}

    # ------------------------------------------------------ primary split --
    data = load_gkp_data()
    train_raw, test_raw = split(data, PRIMARY_SPLIT_SEED)
    train = as_bbdag(train_raw)
    print(f"\n--- primary split (seed {PRIMARY_SPLIT_SEED}) ---")

    fits = {}
    for R, K in ((3, 4), (4, 4), (5, 4), (2, 6)):
        label = f"lossy R={R} K={K}"
        st, eta, tr = fit_cold(train, R, K, label)
        te = float(np.mean(per_sample_nll_bb(st, eta, test_raw)))
        print(f"    {label}: test NLL={te:.5f}  (dof {dof(R, K)})",
              flush=True)
        fits[(R, K)] = (st, eta, tr, te)

    print("  warm starts (from the best-by-train parent):")
    warm4 = {}
    init4 = grow(fits[(3, 4)][0], 4, rng_seed=1000)
    st, eta, tr = one_fit(train, 4, 4, init=init4, eta0=fits[(3, 4)][1],
                          label="warm R=4 K=4")
    te = float(np.mean(per_sample_nll_bb(st, eta, test_raw)))
    print(f"    warm R=4: test NLL={te:.5f}")
    warm4 = (st, eta, tr, te)

    parent5 = warm4 if warm4[2] < fits[(4, 4)][2] else fits[(4, 4)]
    init5 = grow(parent5[0], 4, rng_seed=1001)
    st, eta, tr = one_fit(train, 5, 4, init=init5, eta0=parent5[1],
                          label="warm R=5 K=4")
    te = float(np.mean(per_sample_nll_bb(st, eta, test_raw)))
    print(f"    warm R=5: test NLL={te:.5f}")
    warm5 = (st, eta, tr, te)

    print("  MLE dof frontier:")
    rows, best_mle = mle_frontier(train_raw, test_raw)

    print("\n  conditional paired bootstrap 95% CIs (primary split):")
    nb = {rk: per_sample_nll_bb(f[0], f[1], test_raw)
          for rk, f in fits.items()}
    nb["warm4"] = per_sample_nll_bb(warm4[0], warm4[1], test_raw)
    nb["warm5"] = per_sample_nll_bb(warm5[0], warm5[1], test_raw)
    nm = per_sample_nll_mle(best_mle[3], test_raw)
    ci_r4_r3 = report_ci("R4 - R3", nb[(4, 4)], nb[(3, 4)])
    ci_r5_r4 = report_ci("R5 - R4", nb[(5, 4)], nb[(4, 4)])
    ci_r4_mle = report_ci("R4 - best MLE", nb[(4, 4)], nm)
    ci_r5_mle = report_ci("R5 - best MLE", nb[(5, 4)], nm)
    ci_w4_mle = report_ci("warm R4 - best MLE", nb["warm4"], nm)
    ci_w5_mle = report_ci("warm R5 - best MLE", nb["warm5"], nm)
    ci_k = report_ci("R3K4 - R2K6 (matched ~70 dof)", nb[(3, 4)], nb[(2, 6)])

    results["primary"] = dict(
        fits={f"R{R}K{K}": dict(train=tr, test=te, eta=eta, dof=dof(R, K))
              for (R, K), (st, eta, tr, te) in fits.items()},
        warm4=dict(train=warm4[2], test=warm4[3], eta=warm4[1]),
        warm5=dict(train=warm5[2], test=warm5[3], eta=warm5[1]),
        mle_best=dict(n_max=best_mle[0], dof=best_mle[1], test=best_mle[2]),
        mle_rows=[(r[0], r[1], r[2]) for r in rows],
        cis=dict(r4_r3=ci_r4_r3, r5_r4=ci_r5_r4, r4_mle=ci_r4_mle,
                 r5_mle=ci_r5_mle, warm4_mle=ci_w4_mle, warm5_mle=ci_w5_mle,
                 k_interplay=ci_k),
    )

    # ---------------------------------------------------- alternate split --
    train_raw_a, test_raw_a = split(data, ALT_SPLIT_SEED)
    train_a = as_bbdag(train_raw_a)
    print(f"\n--- alternate reshuffle (seed {ALT_SPLIT_SEED}) ---")
    fits_a = {}
    for R, K in ((3, 4), (4, 4)):
        label = f"lossy R={R} K={K}"
        st, eta, tr = fit_cold(train_a, R, K, label)
        te = float(np.mean(per_sample_nll_bb(st, eta, test_raw_a)))
        print(f"    {label}: test NLL={te:.5f}  (dof {dof(R, K)})",
              flush=True)
        fits_a[(R, K)] = (st, eta, tr, te)
    print("  MLE dof frontier:")
    rows_a, best_mle_a = mle_frontier(train_raw_a, test_raw_a)
    print("\n  conditional CIs (alternate reshuffle):")
    nb3 = per_sample_nll_bb(fits_a[(3, 4)][0], fits_a[(3, 4)][1], test_raw_a)
    nb4 = per_sample_nll_bb(fits_a[(4, 4)][0], fits_a[(4, 4)][1], test_raw_a)
    nma = per_sample_nll_mle(best_mle_a[3], test_raw_a)
    ci_r4_r3_a = report_ci("R4 - R3", nb4, nb3)
    ci_r4_mle_a = report_ci("R4 - best MLE", nb4, nma)
    results["alternate"] = dict(
        fits={f"R{R}K{K}": dict(train=tr, test=te, eta=eta, dof=dof(R, K))
              for (R, K), (st, eta, tr, te) in fits_a.items()},
        mle_best=dict(n_max=best_mle_a[0], dof=best_mle_a[1],
                      test=best_mle_a[2]),
        cis=dict(r4_r3=ci_r4_r3_a, r4_mle=ci_r4_mle_a),
    )

    (OUT_DIR / "results.json").write_text(json.dumps(results, indent=1))

    # ------------------------------------------------------------ figure --
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.plot([r[1] for r in rows], [r[2] for r in rows], "ko-",
            label="MLE (n_max grid)")
    ctx = EXP14["primary"]
    ax.plot([23, 46], [ctx["R1_test"], ctx["R2_test"]], "b^",
            ms=9, label="BB† lossy R=1/2 K=4 (exp14 log)")
    for (R, K), mark in (((3, 4), "r*"), ((4, 4), "r*"), ((5, 4), "r*")):
        ax.plot(dof(R, K), fits[(R, K)][3], mark, ms=12)
    ax.plot([], [], "r*", ms=12, label="BB† lossy R=3/4/5 K=4 (this run)")
    ax.plot(dof(2, 6), fits[(2, 6)][3], "gs", ms=9,
            label="BB† lossy R=2 K=6 (K interplay)")
    ax.plot(dof(4, 4), warm4[3], "mv", ms=9, label="warm R=4/5")
    ax.plot(dof(5, 4), warm5[3], "mv", ms=9)
    ax.set_xlabel("real degrees of freedom")
    ax.set_ylabel("held-out per-sample NLL")
    ax.set_xscale("log")
    ax.legend(fontsize=8)
    ax.set_title("NLL-dof frontier, deeper ranks (primary split)")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "gkp_saturation_frontier.png", dpi=100)
    print(f"  figure: {OUT_DIR / 'gkp_saturation_frontier.png'}")

    # ------------------------------------------------- decision checks ----
    print("\n=== pre-declared decision checks (descriptive) ===")
    tr3, tr4, tr5 = fits[(3, 4)][2], fits[(4, 4)][2], fits[(5, 4)][2]
    d4, d5 = tr3 - tr4, tr4 - tr5
    print(f"1. saturation: delta(4)={d4:+.5f}, delta(5)={d5:+.5f} "
          f"(exp14 delta(3)=+0.00073; flat if < {EPS_FLAT})")
    print(f"   held-out by R (primary): R3 {fits[(3, 4)][3]:.5f}, "
          f"R4 {fits[(4, 4)][3]:.5f}, R5 {fits[(5, 4)][3]:.5f}")
    print("2. frontier: see CI(R4 - best MLE) on both splits above")
    dwarm = fits[(4, 4)][2] - warm4[2]
    verdict3 = ("warm start FOUND A BETTER OPTIMUM (cold under-optimizes)"
                if dwarm > EPS_WARM else
                "cold schedule adequate at R=4 (optimization descriptively "
                "disfavored)")
    print(f"3. optimization: cold-best - warm train NLL = {dwarm:+.5f} -> "
          f"{verdict3}")
    print("4. K interplay: see CI(R3K4 - R2K6) above")
    print(f"5. fitted eta by R (primary): "
          + ", ".join(f"R{R}K{K} {fits[(R, K)][1]:.4f}"
                      for (R, K) in fits)
          + f"; warm4 {warm4[1]:.4f}, warm5 {warm5[1]:.4f}")


if __name__ == "__main__":
    main()
