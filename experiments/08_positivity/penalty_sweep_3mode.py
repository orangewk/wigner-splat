"""Experiment 08 (positivity) -- lambda_psd sweep, three modes (stretch goal).

The three-mode counterpart of penalty_sweep_1mode.py, using fit3f_psd's
WEIGHT-ONLY polish (see wigner_splat.fit3f.fit3f_psd's docstring for why:
n_max=8, M=3 makes a single rho_component call cost ~1 s, so a full
finite-difference polish over fit3f's ~28 shape params/splat -- fit_psd's
1-mode approach -- is computationally infeasible here; holding shapes fixed
makes rho LINEAR in the weights, and psd_penalty(rho(w)) -- a sum of squared
negative eigenvalues of an AFFINE map of w -- is then a CONVEX function of w,
a friendlier landscape than 1-mode's full nonconvex parameter search).

Uses exp06/observe_3mode.py's official condition: alpha=1.5 cat, 3x3x3 angle
triples over [0, pi)^3, 2000 shots/triple, data rng=42, fit3f(bins=24)
(K=16, matching observe_3mode.py's own baseline: min_eig=-0.141,
negativity=0.273). n_max_psd=8, the exp06/observe_3mode.py Fock cutoff.

Same falsification conditions as the 1-mode sweep: (a) dF > -0.03,
(b) min_eig >= -1e-9. Budget note: EACH rho_component rebuild at this scale
is ~1 s and a psd polish iteration needs 2*K of them (K=16 -> ~32 s... no --
weight-only precomputes components ONCE and each iteration is then a cheap
weighted sum + eigvalsh, measured ~15 s/iteration, still expensive) -- kept
to a SMALL iteration budget (a "does the same qualitative pattern hold"
check, not an exhaustively tuned optimum, consistent with the issue brief's
"fit3f ~15s + rho materialize ~20s -> a few trials only" budget note).
"""

import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit3f import fit3f, fit3f_psd  # noqa: E402
from wigner_splat.fock import cat3_fock  # noqa: E402
from wigner_splat.fock_project import psd_report, rho_from_splat  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
BINS = 24
SHOTS = 2000  # per angle triple
DATA_SEED = 42
GRID = [
    t for t in itertools.product(
        np.linspace(0, np.pi, 3, endpoint=False),
        np.linspace(0, np.pi, 3, endpoint=False),
        np.linspace(0, np.pi, 3, endpoint=False),
    )
]  # 3x3x3 = 27 triples, exp06's official budget

N_MAX_PSD = 8  # exp06 / observe_3mode.py's Fock cutoff (8**3 = 512 dims)

DF_THRESHOLD = -0.03
MIN_EIG_THRESHOLD = -1e-9

LAMBDAS = [0.0, 1.0, 10.0, 50.0]
POLISH_ITERS = 25
POLISH_LR = 0.02


def fidelity_and_report(mixture, n_max):
    rho = rho_from_splat(mixture, n_max)
    psi_cat3 = cat3_fock(ALPHA, PARITY, n_max)
    f = float(np.real(psi_cat3.conj() @ rho @ psi_cat3))
    return f, psd_report(rho)


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    print(f"3-mode cat alpha={ALPHA}, {len(GRID)} angle triples, "
          f"{SHOTS} shots/triple, data rng={DATA_SEED}, fit3f(bins={BINS}), "
          f"n_max_psd={N_MAX_PSD}")
    print(f"falsification: (a) dF > {DF_THRESHOLD}  (b) min_eig >= "
          f"{MIN_EIG_THRESHOLD:.0e}\n")

    t0 = time.time()
    data = cat.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    mix0 = fit3f(data, bins=BINS)
    f0, r0 = fidelity_and_report(mix0, N_MAX_PSD)
    print(f"baseline (lambda_psd=0, no polish): K={len(mix0.w)}  F={f0:.4f}  "
          f"min_eig={r0['min_eig']:+.4e}  negativity={r0['negativity']:.4f}  "
          f"(fit3f+baseline-rho wall={time.time() - t0:.1f}s)\n")

    rows = []
    header = (f"{'lambda_psd':>10} {'F':>8} {'dF':>9} {'min_eig':>12} "
              f"{'negativity':>11} {'(a)':>5} {'(b)':>5} {'both':>5} "
              f"{'wall_s':>7}")
    print(header)
    print("-" * len(header))

    for lam in LAMBDAS:
        t0 = time.time()
        if lam == 0.0:
            mix = mix0
        else:
            mix = fit3f_psd(data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
                            psd_polish_iters=POLISH_ITERS,
                            psd_polish_lr=POLISH_LR, bins=BINS)
        wall = time.time() - t0
        f, r = fidelity_and_report(mix, N_MAX_PSD)
        dF = f - f0
        ok_a = dF > DF_THRESHOLD
        ok_b = r["min_eig"] >= MIN_EIG_THRESHOLD
        rows.append(dict(lambda_psd=lam, F=f, dF=dF, min_eig=r["min_eig"],
                         ok_a=ok_a, ok_b=ok_b))
        print(f"{lam:>10.1f} {f:>8.4f} {dF:>+9.4f} {r['min_eig']:>12.4e} "
              f"{r['negativity']:>11.4f} {'yes' if ok_a else 'no':>5} "
              f"{'yes' if ok_b else 'no':>5} "
              f"{'YES' if (ok_a and ok_b) else 'no':>5} {wall:>6.1f}s")

    both = [row for row in rows if row["ok_a"] and row["ok_b"]]
    print()
    if both:
        print(f"VERDICT: (a) and (b) jointly satisfiable at lambda_psd in "
              f"{[row['lambda_psd'] for row in both]}.")
    else:
        print("VERDICT (negative result): no swept lambda_psd satisfies (a) "
              "and (b) simultaneously for the 3-mode weight-only polish "
              "either.")


if __name__ == "__main__":
    main()
