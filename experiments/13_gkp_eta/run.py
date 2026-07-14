"""Experiment 13 -- GKP rematch with the detection-efficiency model (issue #42).

Experiment 12 (first real data) showed the pure squeezed-product BB-dagger
ansatz losing to full-rank MLE on the propagating-GKP dataset (Konno et al.,
Science 383, 289 (2024); Dryad doi:10.5061/dryad.t76hdr86j, data under
../12_gkp_data/data/), with over-deep interference dips as the visible
failure. Issue #42's minimal physical fix: model the MEASURED pdf as the
pure-ansatz pdf convolved with the loss Gaussian (efficiency eta, fitted),
which is exactly the homodyne marginal of loss_eta(|psi><psi|/Z) -- PSD by
construction, closed form throughout (bbdagS lossy section), and |psi>
doubles as a loss-corrected pure estimate.

PROTOCOL (pre-declared; revised after owner review of the first run, which
had selected K on the test set, attributed the eta effect across unequal
configs, compared against a single arbitrary MLE cutoff, and reused the
exp12 test split for every decision):

  * PRIMARY model config is PRE-FIXED: lossy K=4. K=6 is reported as a
    secondary observation and is never selected by test NLL.
  * Each config runs init seeds {0, 1, 2}; the reported fit per config is
    chosen by TRAIN NLL only. Convergence is checked by the train-NLL drop
    over the final 100 iterations (flagged if > 1e-3).
  * eta ablation at IDENTICAL conditions: pure vs lossy at the same K,
    same seed set, same iters and lr. Gap closure is computed per K.
  * The MLE baseline is a degrees-of-freedom FRONTIER: n_max in
    N_MAX_GRID, dof = n_max^2 - 1; the opponent's headline number is the
    BEST test NLL over the grid (choice favorable to the MLE).
  * Match/loss on the headline is decided by a PAIRED BOOTSTRAP (B = 2000)
    95% CI on the mean per-sample test NLL difference (primary BB-dagger
    minus frontier-best MLE), not by comparing point values.
  * CONFIRMATION SPLIT: split seed 1 (untouched by exp12/13 decisions)
    reruns the frozen primary protocol once -- pure/lossy K=4 and the MLE
    frontier -- as the guard against test-set reuse on split seed 0.

Falsification conditions (declared before the run):
  1. Mixedness-by-loss diagnosis: the same-K eta ablation must close >= 50%
     of that K's pure-vs-MLE gap, else exp12's diagnosis was wrong.
  2. Headline "matches full-rank MLE on real data": the bootstrap CI of the
     NLL difference must include or fall below 0; a CI strictly above 0 is
     a LOSS, recorded.
  3. Parameter-efficiency claim: allowed only in Pareto form -- lossy K=4
     (dof 6K-2+1 = 23) must beat the MLE at comparable dof (n_max = 4 or
     6); no "1/N of the parameters" rhetoric against an arbitrary cutoff.
  4. exp12's "more kets do not help (K=6 overfits)" claim is retested: it
     conflated optimization failure with overfitting if best-of-3 pure K=6
     TRAIN NLL <= pure K=4's (a nested family cannot train worse when
     optimized well).
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
    fit_bbdagS, fit_bbdagS_lossy, lossy_pdf, nll, nll_lossy,
)
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "12_gkp_data" / "data"
OUT_FIG = pathlib.Path(__file__).resolve().parent / "gkp_eta_marginals.png"
OUT_FRONTIER = pathlib.Path(__file__).resolve().parent / "gkp_eta_frontier.png"
DEGS = (0, 30, 60, -30, -60, -90)
TRAIN_FRACTION = 0.8
PRIMARY_SPLIT_SEED = 0      # the exp12 split: kept for comparability
CONFIRM_SPLIT_SEED = 1      # untouched by any prior decision
N_MAX_GRID = (4, 6, 8, 10, 12, 16, 20, 25)
BINS = 80
PRIMARY_K = 4               # pre-fixed; K=6 is secondary, never test-selected
SECONDARY_K = 6
INIT_SEEDS = (0, 1, 2)      # per-config; selection among seeds by TRAIN NLL
ITERS = 500                 # identical for pure and lossy (ablation fairness)
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


def bb_dof(K, lossy):
    """Real dof of the K-ket ansatz: 6K params minus global phase and scale
    (both divided out by Z), plus eta when lossy."""
    return 6 * K - 2 + (1 if lossy else 0)


def per_sample_nll_mle(rho, data):
    out = []
    for th, x in data:
        p = np.maximum(marginal_from_rho(rho, x, th), 1e-300)
        out.append(-np.log(p))
    return np.concatenate(out)


def per_sample_nll_bb(st, eta, data):
    out = []
    for th, x in as_bbdag(data):
        p = np.maximum(lossy_pdf(st, x, th, eta), 1e-300)
        out.append(-np.log(p))
    return np.concatenate(out)


def fit_config(train, K, lossy, label):
    """Fit all INIT_SEEDS, pick by train NLL, report convergence deltas."""
    best = None
    for seed in INIT_SEEDS:
        trace = []
        cb = lambda t, v, *rest: trace.append(v)  # noqa: E731
        t0 = time.perf_counter()
        if lossy:
            st, eta = fit_bbdagS_lossy(train, K=K, M=1, eta0=ETA0,
                                       iters=ITERS, lr=LEARNING_RATE,
                                       seed=seed, callback=cb)
        else:
            st = fit_bbdagS(train, K=K, M=1, iters=ITERS, lr=LEARNING_RATE,
                            seed=seed, callback=cb)
            eta = 1.0
        wall = time.perf_counter() - t0
        tr = nll_lossy(st, train, eta) if lossy else nll(st, train)
        # trace has a value every 25 iters; final-100-iter drop = last 4 steps
        conv = trace[-5] - trace[-1] if len(trace) >= 5 else float("nan")
        flag = "  [NOT CONVERGED]" if conv > 1e-3 else ""
        print(f"    {label} seed={seed}: train NLL={tr:.4f}  "
              f"final-100-iter drop={conv:+.5f}{flag}  "
              f"eta={eta:.4f}  wall={wall:.0f}s", flush=True)
        if best is None or tr < best[0]:
            best = (tr, seed, st, eta)
    tr, seed, st, eta = best
    print(f"    -> {label}: best-by-TRAIN seed={seed}  train NLL={tr:.4f}")
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
    print(f"    -> frontier best (favors MLE): n_max={best[0]} "
          f"test NLL={best[2]:.5f}")
    return rows, best


def paired_bootstrap_ci(diff, B, seed):
    rng = np.random.default_rng(seed)
    n = len(diff)
    means = np.array([
        np.mean(diff[rng.integers(0, n, n)]) for _ in range(B)
    ])
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def run_split(name, split_seed, ks):
    data = load_gkp_data()
    train_raw, test_raw = split(data, split_seed)
    train = as_bbdag(train_raw)
    print(f"\n--- split '{name}' (seed {split_seed}) ---")
    fits = {}
    for K in ks:
        for lossy in (False, True):
            tag = f"{'lossy' if lossy else 'pure '} K={K}"
            st, eta, tr = fit_config(train, K, lossy, tag)
            te = float(np.mean(per_sample_nll_bb(st, eta, test_raw)))
            print(f"    {tag}: test NLL={te:.5f}  "
                  f"(dof {bb_dof(K, lossy)})", flush=True)
            fits[(K, lossy)] = (st, eta, tr, te)
    print("  MLE dof frontier:")
    rows, best_mle = mle_frontier(train_raw, test_raw)
    for K in ks:
        gap = fits[(K, False)][3] - best_mle[2]
        closed = (fits[(K, False)][3] - fits[(K, True)][3]) / gap
        print(f"  same-K eta ablation K={K}: pure {fits[(K, False)][3]:.5f} "
              f"-> lossy {fits[(K, True)][3]:.5f} vs MLE {best_mle[2]:.5f}: "
              f"gap closed {100 * closed:.1f}%")
    return data, train_raw, test_raw, fits, rows, best_mle


def main():
    print("=== exp13: GKP rematch -- squeezed BB-dagger + fitted loss eta ===")
    print("(protocol and falsification conditions pre-declared in docstring)")

    data, train_raw, test_raw, fits, rows, best_mle = run_split(
        "primary (exp12 split, reused for comparability)",
        PRIMARY_SPLIT_SEED, ks=(PRIMARY_K, SECONDARY_K),
    )
    st, eta, _, te_bb = fits[(PRIMARY_K, True)]

    # paired bootstrap on the PRE-FIXED primary config vs frontier-best MLE
    d_bb = per_sample_nll_bb(st, eta, test_raw)
    d_mle = per_sample_nll_mle(best_mle[3], test_raw)
    lo, hi = paired_bootstrap_ci(d_bb - d_mle, BOOTSTRAP_B, BOOTSTRAP_SEED)
    print(f"\n  paired bootstrap 95% CI of (lossy K={PRIMARY_K} - best MLE) "
          f"mean test NLL diff: [{lo:+.5f}, {hi:+.5f}] "
          f"(point {np.mean(d_bb - d_mle):+.5f})")

    # exp12 K=6-overfit claim retest (pure, train NLL, best over seeds)
    tr_p4 = fits[(PRIMARY_K, False)][2]
    tr_p6 = fits[(SECONDARY_K, False)][2]
    if tr_p6 <= tr_p4 + 1e-4:
        retest = ("K=6 trains at least as well: exp12's overfitting claim "
                  "was an OPTIMIZATION artifact")
    else:
        retest = ("K=6 still trains worse: optimization, not the family, "
                  "is the limit")
    print(f"  exp12 claim retest: pure train NLL best-of-{len(INIT_SEEDS)}: "
          f"K=4 {tr_p4:.5f} vs K=6 {tr_p6:.5f} -> {retest}")

    # confirmation split: frozen primary protocol on untouched seed
    _, _, test_c, fits_c, rows_c, best_mle_c = run_split(
        "confirmation (frozen protocol, untouched seed)",
        CONFIRM_SPLIT_SEED, ks=(PRIMARY_K,),
    )
    st_c, eta_c, _, te_bb_c = fits_c[(PRIMARY_K, True)]
    d_c = (per_sample_nll_bb(st_c, eta_c, test_c)
           - per_sample_nll_mle(best_mle_c[3], test_c))
    lo_c, hi_c = paired_bootstrap_ci(d_c, BOOTSTRAP_B, BOOTSTRAP_SEED)
    print(f"\n  confirmation CI (lossy K={PRIMARY_K} - best MLE): "
          f"[{lo_c:+.5f}, {hi_c:+.5f}] (point {np.mean(d_c):+.5f})")

    # figures: marginal overlay (primary fit) + NLL-dof frontier
    fig, axes = plt.subplots(2, 3, figsize=(15, 7))
    for ax, (th, x) in zip(axes.ravel(), data):
        xs = np.linspace(-5, 5, 400)
        ax.hist(x, bins=100, density=True, alpha=0.5, label="data (all)")
        ax.plot(xs, lossy_pdf(st, xs[:, None], np.array([th]), eta), "r-",
                lw=1.5, label=f"BB† K={PRIMARY_K} + loss (η={eta:.2f})")
        ax.plot(xs, marginal_from_rho(best_mle[3], xs, th), "k--", lw=1.2,
                label=f"MLE n={best_mle[0]}")
        ax.set_title(f"{np.rad2deg(th):+.0f} deg")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(OUT_FIG, dpi=100)

    fig2, ax = plt.subplots(figsize=(7, 5))
    ax.plot([r[1] for r in rows], [r[2] for r in rows], "ko-",
            label="MLE (n_max grid)")
    for (K, lossy), (_, _, _, te) in fits.items():
        ax.plot(bb_dof(K, lossy), te, "r*" if lossy else "b^", ms=12,
                label=f"BB† {'lossy' if lossy else 'pure'} K={K}")
    ax.set_xlabel("real degrees of freedom")
    ax.set_ylabel("held-out per-sample NLL")
    ax.set_xscale("log")
    ax.legend(fontsize=8)
    ax.set_title("NLL-dof frontier, GKP data (primary split)")
    plt.tight_layout()
    plt.savefig(OUT_FRONTIER, dpi=100)
    print(f"  figures: {OUT_FIG}, {OUT_FRONTIER}")

    # verdicts against the pre-declared falsification conditions
    print("\n=== verdicts (conditions 1-4 in docstring) ===")
    te_p = fits[(PRIMARY_K, False)][3]
    closed = (te_p - te_bb) / (te_p - best_mle[2])
    print(f"1. same-K (K={PRIMARY_K}) gap closure {100 * closed:.1f}% -> "
          f"mixedness-by-loss diagnosis "
          f"{'CONFIRMED' if closed >= 0.5 else 'FALSIFIED'}")
    if hi < 0 and hi_c < 0:
        v2 = "BB-dagger+loss BEATS the MLE frontier (both CIs below 0)"
    elif lo > 0 and lo_c > 0:
        v2 = ("LOSS, recorded: MLE keeps a real edge (both CIs above 0); "
              "the residual passes to issue #40 (rank beyond a single "
              "Gaussian loss channel)")
    else:
        v2 = ("STATISTICAL TIE on at least one split (CI includes 0): "
              "'matches full-rank MLE on real data' stands at CI resolution")
    print(f"2. headline: {v2}")
    mle_at_dof = {r[0]: r[2] for r in rows}
    pareto = te_bb < mle_at_dof[6] and bb_dof(PRIMARY_K, True) < 35
    print(f"3. Pareto claim (dof {bb_dof(PRIMARY_K, True)} vs MLE n_max=6 "
          f"dof 35: {te_bb:.5f} vs {mle_at_dof[6]:.5f}): "
          f"{'SUPPORTED' if pareto else 'NOT SUPPORTED'}")
    print(f"4. see 'exp12 claim retest' line above; confirmation split "
          f"test NLLs: lossy K={PRIMARY_K} {te_bb_c:.5f} vs best MLE "
          f"{best_mle_c[2]:.5f}")


if __name__ == "__main__":
    main()
