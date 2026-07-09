"""Experiment 08 (positivity) -- penalty THEN projection, three modes.

The decisive test. 1-mode showed penalty+projection satisfies (a) dF>-0.03 and
(b) min_eig>=-1e-9 jointly (penalty_then_project_1mode.py). But 1-mode is the
regime MLE already wins; the HEADLINE claim is at 3 modes, where the baseline
splat is far more unphysical (min_eig=-0.14, negativity=0.27 -- observe_3mode.py).

Question: can the weight-only convex PSD penalty (fit3f_psd) shrink 3-mode
negativity cheaply enough that a final projection costs < 0.03 fidelity? If yes,
issue #8 is resolvable at the regime that matters. If the negative fringe mass is
"load-bearing" for the 3-mode fidelity, penalty+projection fails here even though
it worked at 1 mode -- itself a sharp, publishable result about where the splat
representation's physicality breaks.

Same official condition as penalty_sweep_3mode.py / observe_3mode.py.
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

ALPHA, PARITY, BINS, SHOTS, DATA_SEED = 1.5, +1, 24, 2000, 42
GRID = list(itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
))  # 27 triples, exp06 official
N_MAX_PSD = 8
DF_THRESHOLD, MIN_EIG_THRESHOLD = -0.03, -1e-9
LAMBDAS = [0.0, 10.0, 50.0, 200.0]
POLISH_ITERS, POLISH_LR = 40, 0.02


def project_psd(rho):
    rho_h = (rho + rho.conj().T) / 2
    ev, U = np.linalg.eigh(rho_h)
    rho_p = (U * np.clip(ev, 0.0, None)) @ U.conj().T
    return rho_p / np.real(np.trace(rho_p))


def fidelity(rho, psi):
    return float(np.real(psi.conj() @ rho @ psi))


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    psi = cat3_fock(ALPHA, PARITY, N_MAX_PSD)
    print(f"3-mode cat alpha={ALPHA}, {len(GRID)} triples, {SHOTS} shots, "
          f"n_max_psd={N_MAX_PSD}. (a) dF>{DF_THRESHOLD}, (b) proj min_eig>="
          f"{MIN_EIG_THRESHOLD:.0e}\n")
    t0 = time.time()
    data = cat.sample_homodyne(GRID, SHOTS, rng=DATA_SEED)
    mix0 = fit3f(data, bins=BINS)
    f0 = fidelity(rho_from_splat(mix0, N_MAX_PSD), psi)
    print(f"baseline F={f0:.4f}  K={len(mix0.w)}  "
          f"(fit3f+rho wall={time.time()-t0:.1f}s)\n")

    header = (f"{'lambda':>7} {'F_pen':>8} {'min_eig_pen':>12} {'neg_pen':>9} "
              f"{'F_proj':>8} {'dF_proj':>9} {'min_eig_proj':>13} "
              f"{'(a)':>4} {'(b)':>4} {'both':>5} {'wall_s':>7}")
    print(header)
    print("-" * len(header))
    any_both = False
    for lam in LAMBDAS:
        t0 = time.time()
        mix = mix0 if lam == 0.0 else fit3f_psd(
            data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
            psd_polish_iters=POLISH_ITERS, psd_polish_lr=POLISH_LR, bins=BINS)
        rho = rho_from_splat(mix, N_MAX_PSD)
        r_pen = psd_report(rho)
        rho_p = project_psd(rho)
        r_proj = psd_report(rho_p)
        f_proj = fidelity(rho_p, psi)
        dF = f_proj - f0
        ok_a, ok_b = dF > DF_THRESHOLD, r_proj["min_eig"] >= MIN_EIG_THRESHOLD
        any_both = any_both or (ok_a and ok_b)
        print(f"{lam:>7.1f} {fidelity(rho, psi):>8.4f} {r_pen['min_eig']:>12.4e} "
              f"{r_pen['negativity']:>9.4f} {f_proj:>8.4f} {dF:>+9.4f} "
              f"{r_proj['min_eig']:>13.4e} {'yes' if ok_a else 'no':>4} "
              f"{'yes' if ok_b else 'no':>4} "
              f"{'YES' if (ok_a and ok_b) else 'no':>5} {time.time()-t0:>6.1f}s")

    print()
    if any_both:
        print("VERDICT: penalty+projection satisfies (a) AND (b) at 3 modes. "
              "Issue #8 is resolvable at the headline regime.")
    else:
        print("VERDICT (negative result): penalty+projection cannot meet (a) "
              "and (b) jointly at 3 modes -- the negative-eigenvalue mass is "
              "load-bearing for the 3-mode fidelity. Physicality and the "
              "3-mode fidelity advantage are in tension for signed splats.")


if __name__ == "__main__":
    main()
