"""Experiment 08 (positivity) -- lambda_psd sweep, single mode.

Issue #8's falsification test: can fit_psd's PSD-polish stage
(wigner_splat.fit.fit_psd) find a splat mixture that is BOTH close to the
unpenalized fit's fidelity AND has a physical (PSD) rho? Falsification
conditions, stated in the issue brief:

    (a) fidelity degradation  dF > -0.03   (within 0.03 of the unpenalized F)
    (b) min_eig(rho) >= -1e-9              (PSD to numerical noise)

If some lambda_psd satisfies BOTH, issue #8 is resolved constructively (the
splat representation CAN be made physical without giving up reconstruction
quality). If no lambda_psd satisfies both -- if every lambda that fixes (b)
already breaks (a), and vice versa -- that is recorded as a NEGATIVE RESULT:
"the current splat representation cannot be simultaneously physical and
high-fidelity", per this repo's convention of reporting falsifications
honestly rather than silently dropping the attempt.

IMPORTANT (see fit.py / fock_project.py module docstrings): the penalty
targets NEGATIVE EIGENVALUES OF RHO (an unphysical operator), not Wigner
negativity (W(z) < 0, a genuinely physical feature of any cat state). A
successful lambda_psd should let the fitted Wigner function KEEP its
negative fringe while making rho itself PSD.

Same condition as the issue brief's baseline observation (diagnose_1mode.py
part B / tests/test_fock_project.py): alpha=1.5 cat, 12 angles over
[0, pi), 4000 shots/angle, data rng=42, fit(K=4, iters=800, seed=0,
densify_every=100, K_max=12). Fidelity and min_eig are both read off the
SAME object, rho_from_splat(mixture, N_MAX_PSD) -- fidelity as the exact
Fock-basis <cat|rho|cat> (not diagnose_1mode.py's grid-based Wigner overlap;
tests/test_fock_project.py's test_fitted_splat_matches_corrected_grid
confirms rho_from_splat agrees with the grid ground truth to ~3e-4 relative
error, so this is a more precise, cheaper, and equally valid fidelity read).
"""

import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit import fit, fit_psd  # noqa: E402
from wigner_splat.fock import cat_fock  # noqa: E402
from wigner_splat.fock_project import psd_report, rho_from_splat  # noqa: E402
from wigner_splat.states import CatState  # noqa: E402

ALPHA = 1.5
PARITY = +1
N_ANGLES = 12
SHOTS = 4000
DATA_SEED = 42
FIT_KWARGS = dict(K=4, iters=800, seed=0, densify_every=100, K_max=12)

N_MAX_PSD = 28  # rho eigenvalues converged by here (module docstrings)

# Falsification thresholds (issue brief).
DF_THRESHOLD = -0.03
MIN_EIG_THRESHOLD = -1e-9

LAMBDAS = [0.0, 1.0, 5.0, 20.0, 50.0, 100.0, 300.0]
POLISH_ITERS = 200
POLISH_LR = 0.008


def fidelity_and_report(mixture, n_max):
    rho = rho_from_splat(mixture, n_max)
    psi_cat = cat_fock(ALPHA, PARITY, n_max)
    f = float(np.real(psi_cat.conj() @ rho @ psi_cat))
    return f, psd_report(rho)


def main():
    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, N_ANGLES, endpoint=False)
    data = cat.sample_homodyne(angles, SHOTS, rng=DATA_SEED)

    print(f"1-mode cat alpha={ALPHA}, {N_ANGLES} angles, {SHOTS} shots/angle, "
          f"data rng={DATA_SEED}, fit {FIT_KWARGS}, n_max_psd={N_MAX_PSD}")
    print(f"falsification: (a) dF > {DF_THRESHOLD}  (b) min_eig >= "
          f"{MIN_EIG_THRESHOLD:.0e}\n")

    mix0 = fit(data, **FIT_KWARGS)
    f0, r0 = fidelity_and_report(mix0, N_MAX_PSD)
    print(f"baseline (lambda_psd=0, no polish): K={len(mix0.w)}  F={f0:.4f}  "
          f"min_eig={r0['min_eig']:+.4e}  negativity={r0['negativity']:.4f}\n")

    rows = []
    header = (f"{'lambda_psd':>10} {'K':>3} {'F':>8} {'dF':>9} "
              f"{'min_eig':>12} {'negativity':>11} {'(a)':>5} {'(b)':>5} "
              f"{'both':>5} {'wall_s':>7}")
    print(header)
    print("-" * len(header))

    for lam in LAMBDAS:
        t0 = time.time()
        if lam == 0.0:
            mix = mix0
        else:
            mix = fit_psd(data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
                          psd_polish_iters=POLISH_ITERS,
                          psd_polish_lr=POLISH_LR, **FIT_KWARGS)
        wall = time.time() - t0
        f, r = fidelity_and_report(mix, N_MAX_PSD)
        dF = f - f0
        ok_a = dF > DF_THRESHOLD
        ok_b = r["min_eig"] >= MIN_EIG_THRESHOLD
        rows.append(dict(lambda_psd=lam, K=len(mix.w), F=f, dF=dF,
                         min_eig=r["min_eig"], negativity=r["negativity"],
                         ok_a=ok_a, ok_b=ok_b))
        print(f"{lam:>10.1f} {len(mix.w):>3d} {f:>8.4f} {dF:>+9.4f} "
              f"{r['min_eig']:>12.4e} {r['negativity']:>11.4f} "
              f"{'yes' if ok_a else 'no':>5} {'yes' if ok_b else 'no':>5} "
              f"{'YES' if (ok_a and ok_b) else 'no':>5} {wall:>6.1f}s")

    both = [row for row in rows if row["ok_a"] and row["ok_b"]]
    print()
    if both:
        print(f"VERDICT: falsification conditions (a) AND (b) are jointly "
              f"satisfiable -- lambda_psd in "
              f"{[row['lambda_psd'] for row in both]} works. Issue #8 is "
              f"resolved constructively for this state/fit config.")
    else:
        print("VERDICT (negative result): no swept lambda_psd satisfies (a) "
              "and (b) simultaneously. Either fidelity collapses before "
              "min_eig reaches ~0, or min_eig stays negative while fidelity "
              "is preserved -- the current splat representation cannot be "
              "made both physical (PSD rho) and high-fidelity by this "
              "weight/mean/shape PSD-polish alone, for this state.")


if __name__ == "__main__":
    main()
