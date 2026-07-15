"""Experiment 14 control -- matched-dof rank-vs-capacity separation (issue #40).

The owner review of PR #44 identified a blocking confound in exp14's main
run: comparing lossy R=1,K=4 (23 dof) against R=2,K=4 (46 dof) changes the
squeezed-ket primitive count (4 -> 8), the dof, and the compute per
iteration TOGETHER, so the observed improvement cannot be attributed to
physical rank as opposed to plain ket/parameter capacity.

This control is the nearly-matched-dof comparison the review asked for:

    R=1, K=8  (pure column, 8 kets):  dof 6*8 - 2 + 1 = 47
    R=2, K=4  (two columns, 4 kets each): dof 6*2*4 - 2 - 1 + 1 = 46

Same exploratory framing as exp14 (same reshuffles seeds 0/1, nothing here
is preregistered): both configs refit fresh under the IDENTICAL schedule
(init seeds {0,1,2}, selection by TRAIN NLL, 500 iterations, lr 0.05,
eta0 0.8), on both reshuffles, with conditional paired bootstrap CIs of
(R2K4 - R1K8) per-sample test NLL.

Optimization caveat, declared upfront (exp13's K=6 lesson: larger K can
train WORSE at a fixed budget, an optimization artifact): the R1K8 family
nests R1K4, so if R1K8's best-of-3 train NLL comes out above R1K4's exp14
values (1.62938 primary / 1.63019 alternate), the K=8 side is
under-optimized and this control CANNOT settle the attribution -- flagged
in the output rather than silently interpreted.

Descriptive readings (pre-declared):
  * CI(R2K4 - R1K8) below 0 on both reshuffles AND no under-optimization
    flag: capacity-matched descriptive support for the rank hypothesis.
  * CI including 0: the exp14 gain is attributable to capacity as readily
    as to rank -- the rank attribution stays UNRESOLVED.
  * CI above 0: at matched dof, pure-ket capacity beats the rank
    parameterization on this data.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS_lossy, fit_bbdagS_lossy_mixed, lossy_pdf, lossy_pdf_mixed,
    nll_lossy, nll_lossy_mixed,
)

DATA_DIR = pathlib.Path(__file__).resolve().parents[1] / "12_gkp_data" / "data"
DEGS = (0, 30, 60, -30, -60, -90)
TRAIN_FRACTION = 0.8
SPLIT_SEEDS = (0, 1)
INIT_SEEDS = (0, 1, 2)
ITERS = 500
LEARNING_RATE = 0.05
ETA0 = 0.8
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 123
# exp14 main-run best-of-3 train NLLs for the nested under-optimization check
R1K4_TRAIN = {0: 1.62938, 1: 1.63019}


def load_split(seed):
    rng = np.random.default_rng(seed)
    train, test = [], []
    for deg in DEGS:
        x = np.asarray(np.load(DATA_DIR / f"quad_{deg}deg.npy"), float)
        idx = rng.permutation(len(x))
        n_tr = int(TRAIN_FRACTION * len(x))
        th = np.array([np.deg2rad(deg)])
        train.append((th, x[idx[:n_tr]][:, None]))
        test.append((th, x[idx[n_tr:]][:, None]))
    return train, test


def per_sample_nll(st, eta, data, mixed):
    pdf = lossy_pdf_mixed if mixed else lossy_pdf
    return np.concatenate([
        -np.log(np.maximum(pdf(st, x, th, eta), 1e-300)) for th, x in data
    ])


def fit_config(train, R, K, label):
    best = None
    for seed in INIT_SEEDS:
        t0 = time.perf_counter()
        if R == 1:
            st, eta = fit_bbdagS_lossy(train, K=K, M=1, eta0=ETA0,
                                       iters=ITERS, lr=LEARNING_RATE,
                                       seed=seed)
            tr = nll_lossy(st, train, eta)
        else:
            st, eta = fit_bbdagS_lossy_mixed(train, R=R, K=K, M=1, eta0=ETA0,
                                             iters=ITERS, lr=LEARNING_RATE,
                                             seed=seed)
            tr = nll_lossy_mixed(st, train, eta)
        print(f"    {label} seed={seed}: train NLL={tr:.5f}  eta={eta:.4f}  "
              f"wall={time.perf_counter() - t0:.0f}s", flush=True)
        if best is None or tr < best[0]:
            best = (tr, seed, st, eta)
    tr, seed, st, eta = best
    print(f"    -> {label}: best-by-TRAIN seed={seed}  train NLL={tr:.5f}")
    return st, eta, tr


def paired_bootstrap_ci(diff):
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    n = len(diff)
    means = np.array([np.mean(diff[rng.integers(0, n, n)])
                      for _ in range(BOOTSTRAP_B)])
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def main():
    print("=== exp14 control: matched-dof R=1,K=8 (47 dof) vs R=2,K=4 (46 dof) ===")
    print("(exploratory; caveats and pre-declared readings in docstring)")
    verdict_parts = []
    for split_seed in SPLIT_SEEDS:
        train, test = load_split(split_seed)
        print(f"\n--- reshuffle seed {split_seed} ---")
        st8, eta8, tr8 = fit_config(train, 1, 8, "lossy R=1 K=8")
        underopt = tr8 > R1K4_TRAIN[split_seed] + 1e-4
        if underopt:
            print(f"    [UNDER-OPTIMIZED] R1K8 best train {tr8:.5f} > nested "
                  f"R1K4 {R1K4_TRAIN[split_seed]:.5f} -- K=8 optimization "
                  f"did not reach its own family's floor; attribution "
                  f"cannot be settled on this side.")
        st2, eta2, tr2 = fit_config(train, 2, 4, "lossy R=2 K=4")
        d8 = per_sample_nll(st8, eta8, test, mixed=False)
        d2 = per_sample_nll(st2, eta2, test, mixed=True)
        te8, te2 = float(np.mean(d8)), float(np.mean(d2))
        lo, hi = paired_bootstrap_ci(d2 - d8)
        print(f"    test NLL: R1K8 {te8:.5f} (dof 47)  vs  R2K4 {te2:.5f} "
              f"(dof 46)")
        print(f"    conditional paired CI (R2K4 - R1K8): [{lo:+.5f}, "
              f"{hi:+.5f}]  (point {te2 - te8:+.5f})")
        verdict_parts.append((split_seed, lo, hi, underopt))

    print("\n=== matched-dof reading (pre-declared in docstring) ===")
    any_under = any(u for _, _, _, u in verdict_parts)
    if all(hi < 0 for _, _, hi, _ in verdict_parts) and not any_under:
        print("-> capacity-matched descriptive support for the rank "
              "hypothesis (both CIs below 0, no under-optimization flag).")
    elif all(lo > 0 for _, lo, _, _ in verdict_parts) and not any_under:
        print("-> at matched dof, pure-ket capacity beats the rank "
              "parameterization on this data.")
    else:
        print("-> attribution UNRESOLVED: the exp14 R2K4 gain cannot be "
              "assigned to physical rank over ket/parameter capacity"
              + (" (K=8 under-optimization flag raised)" if any_under else
                 " (CI spans 0 on at least one reshuffle)") + ".")


if __name__ == "__main__":
    main()
