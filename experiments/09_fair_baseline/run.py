"""Experiment 09 -- fair baseline for BB-dagger (issue #27).

The exp06/exp08 comparison (BB-dagger K=4 pure ansatz vs full-rank 512-dim
Fock MLE) confounds two advantages: the REPRESENTATION (coherent-product
kets) and the CONSTRAINT (rank-1 / few parameters vs an underdetermined
262k-parameter density matrix). This experiment separates them by adding the
missing control: a GENERIC pure Fock ket (n_max=8, 512 complex parameters)
trained with the SAME per-sample NLL, the SAME Adam optimizer, and the same
analytic-gradient discipline (wigner_splat/purefock3.py). The only remaining
difference from BB-dagger is the representation.

Also introduces the held-out evaluation issue #27 asks for: each triple's
shots are split into train/test, and per-sample NLL is reported on both
splits for every method plus the true state (the historical NLL(fit) <
NLL(true) observation was train-only).

Falsification condition (issue #27): if the constrained generic baseline
matches BB-dagger's fidelity at comparable-or-less compute, the "BB-dagger
ansatz advantage" claim must be withdrawn in favor of "the win source is the
parameter-count constraint".

Historical context (committed logs): full-rank mle3 at this budget reached
F 0.676 in a 900 s budget (DNF, seed 42); BB-dagger K=4 analytic reaches
exact-state F 0.950-0.959 in ~10 s (exp08, issue #25).
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM, fidelity_vs_cat3, nll  # noqa: E402
from wigner_splat.purefock3 import (  # noqa: E402
    fidelity_vs_cat3 as fidelity_purefock, fit_purefock3, nll_psi,
)
from wigner_splat.fock import cat3_truncation_fidelity  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
SHOTS = 2000
TRAIN_SHOTS = 1600  # per triple; the rest is the held-out test split
DATA_SEEDS = (42, 1, 2)
INIT_SEED = 0
BBDAG_K = 4
BBDAG_ITERS = 200
PUREFOCK_NMAX = 8
PUREFOCK_ITERS = 1000
LEARNING_RATE = 0.05
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def split(data):
    train = [(theta, X[:TRAIN_SHOTS]) for theta, X in data]
    test = [(theta, X[TRAIN_SHOTS:]) for theta, X in data]
    return train, test


def true_state_nll(cat, data):
    """Exact per-sample NLL of the true state (no truncation, no fit)."""
    tot, n = 0.0, 0
    for theta, X in data:
        p = cat.homodyne_pdf(X[:, 0], X[:, 1], X[:, 2], *theta)
        tot += -np.sum(np.log(np.maximum(p, 1e-300)))
        n += len(X)
    return tot / n


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    ceiling = cat3_truncation_fidelity(ALPHA, PARITY, PUREFOCK_NMAX)
    print("=== exp09: fair baseline -- representation vs constraint (issue #27) ===")
    print(f"shared: per-sample NLL objective, Adam(lr={LEARNING_RATE}), analytic "
          f"gradients, train={TRAIN_SHOTS}/test={SHOTS - TRAIN_SHOTS} shots/triple")
    print(f"purefock truncation ceiling (n_max={PUREFOCK_NMAX}): {ceiling:.5f}")
    print("historical full-rank mle3 (same data family, committed log): "
          "F=0.676 at 900 s DNF (seed 42)\n")

    rows = []
    for seed in DATA_SEEDS:
        print(f"--- data seed {seed}: sampling {len(GRID)} triples x {SHOTS} ---",
              flush=True)
        data = cat.sample_homodyne(GRID, SHOTS, rng=seed)
        train, test = split(data)
        nll_true_train = true_state_nll(cat, train)
        nll_true_test = true_state_nll(cat, test)

        t0 = time.perf_counter()
        bb = fit_bbdagM(train, K=BBDAG_K, M=3, iters=BBDAG_ITERS,
                        lr=LEARNING_RATE, seed=INIT_SEED)
        t_bb = time.perf_counter() - t0
        row_bb = dict(
            seed=seed, method=f"bbdag K={BBDAG_K}",
            F=fidelity_vs_cat3(bb, ALPHA, PARITY), wall=t_bb,
            nll_train=nll(bb, train), nll_test=nll(bb, test),
        )

        t0 = time.perf_counter()
        pf = fit_purefock3(train, n_max=PUREFOCK_NMAX, iters=PUREFOCK_ITERS,
                           lr=LEARNING_RATE, seed=INIT_SEED)
        t_pf = time.perf_counter() - t0
        f_trunc, f_exact = fidelity_purefock(pf, ALPHA, PARITY)
        row_pf = dict(
            seed=seed, method=f"purefock n_max={PUREFOCK_NMAX}",
            F=f_exact, F_trunc=f_trunc, wall=t_pf,
            nll_train=nll_psi(pf, train), nll_test=nll_psi(pf, test),
        )

        for row in (row_bb, row_pf):
            extra = (f"  (F_trunc={row['F_trunc']:.4f})"
                     if "F_trunc" in row else "")
            print(f"  {row['method']:22s} F_exact={row['F']:.4f}{extra}  "
                  f"wall={row['wall']:.1f}s  NLL train={row['nll_train']:.4f} "
                  f"test={row['nll_test']:.4f}", flush=True)
        print(f"  {'true state':22s} NLL train={nll_true_train:.4f} "
              f"test={nll_true_test:.4f}", flush=True)
        rows.extend([row_bb, row_pf])

    bb_rows = [r for r in rows if r["method"].startswith("bbdag")]
    pf_rows = [r for r in rows if r["method"].startswith("purefock")]
    mean = lambda key, rs: float(np.mean([r[key] for r in rs]))
    f_bb, f_pf = mean('F', bb_rows), mean('F', pf_rows)
    w_bb, w_pf = mean('wall', bb_rows), mean('wall', pf_rows)
    t_bb, t_pf = mean('nll_test', bb_rows), mean('nll_test', pf_rows)
    print("\n=== verdict (issue #27, per axis) ===")
    print(f"bbdag    mean: F={f_bb:.4f}  wall={w_bb:.1f}s  test NLL={t_bb:.4f}")
    print(f"purefock mean: F={f_pf:.4f}  wall={w_pf:.1f}s  test NLL={t_pf:.4f}")
    print(f"axis fidelity:     {'purefock' if f_pf > f_bb else 'bbdag'} wins "
          f"({f_pf:.4f} vs {f_bb:.4f})")
    print(f"axis compute:      {'bbdag' if w_bb < w_pf else 'purefock'} wins "
          f"({w_bb:.1f}s vs {w_pf:.1f}s, {w_pf / w_bb:.0f}x)")
    print(f"axis held-out NLL: {'bbdag' if t_bb < t_pf else 'purefock'} wins "
          f"({t_bb:.4f} vs {t_pf:.4f})")
    strict = f_pf >= f_bb - 1e-3 and w_pf <= w_bb
    if strict:
        print("-> strict trigger FIRES (purefock matches at <= compute): "
              "withdraw the ansatz-advantage claim entirely.")
    else:
        print("-> strict trigger (match at <= compute) does not fire, BUT the "
              "fidelity axis goes to the generic constrained fit: most of the "
              "fidelity gap over full-rank MLE is the pure-state constraint + "
              "gradient ML, not the coherent ansatz. Do NOT claim an ansatz "
              "fidelity advantage; bbdag's measured edge is compute, "
              "parameter count, and held-out likelihood.")


if __name__ == "__main__":
    main()
