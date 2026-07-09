"""Experiment 08 (positivity) -- penalty THEN projection, single mode.

The lambda_psd sweep (penalty_sweep_1mode.py) found that the soft PSD penalty
alone asymptotes at min_eig ~ -1e-3 and never reaches the -1e-9 PSD bar -- which
is expected: a SOFT penalty pushes toward the cone but cannot land exactly on it.
And naive projection ALONE costs dF=-0.044 (diagnose_1mode.py part C), breaking
(a).

This tests the combination the sweep's "negative result" verdict skipped:
  1. penalty (fit_psd) to cheaply shrink negativity from ~0.07 to ~0.004,
  2. THEN a hard post-hoc PSD projection from that already-near-physical rho.

If projecting from negativity ~0.004 (instead of ~0.045 raw) costs little
fidelity, the pipeline can satisfy BOTH (a) dF>-0.03 (on the FINAL projected
fidelity vs baseline) and (b) min_eig>=-1e-9 (projection makes this exact).
"""
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit import fit, fit_psd  # noqa: E402
from wigner_splat.fock import cat_fock  # noqa: E402
from wigner_splat.fock_project import psd_report, rho_from_splat  # noqa: E402
from wigner_splat.states import CatState  # noqa: E402

ALPHA, PARITY, N_ANGLES, SHOTS, DATA_SEED = 1.5, +1, 12, 4000, 42
FIT_KWARGS = dict(K=4, iters=800, seed=0, densify_every=100, K_max=12)
N_MAX_PSD = 28
DF_THRESHOLD, MIN_EIG_THRESHOLD = -0.03, -1e-9
LAMBDAS = [0.0, 5.0, 20.0, 50.0, 100.0]
POLISH_ITERS, POLISH_LR = 200, 0.008


def project_psd(rho):
    """Nearest PSD (clip negative eigenvalues), renormalize trace to 1."""
    rho_h = (rho + rho.conj().T) / 2
    ev, U = np.linalg.eigh(rho_h)
    rho_p = (U * np.clip(ev, 0.0, None)) @ U.conj().T
    return rho_p / np.real(np.trace(rho_p))


def fidelity(rho, psi):
    return float(np.real(psi.conj() @ rho @ psi))


def main():
    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, N_ANGLES, endpoint=False)
    data = cat.sample_homodyne(angles, SHOTS, rng=DATA_SEED)
    psi = cat_fock(ALPHA, PARITY, N_MAX_PSD)

    mix0 = fit(data, **FIT_KWARGS)
    f0 = fidelity(rho_from_splat(mix0, N_MAX_PSD), psi)
    print(f"baseline F={f0:.4f}  (falsification: (a) dF>{DF_THRESHOLD}, "
          f"(b) projected min_eig>={MIN_EIG_THRESHOLD:.0e})\n")

    header = (f"{'lambda':>7} {'F_pen':>8} {'min_eig_pen':>12} {'neg_pen':>9} "
              f"{'F_proj':>8} {'dF_proj':>9} {'min_eig_proj':>13} "
              f"{'(a)':>4} {'(b)':>4} {'both':>5}")
    print(header)
    print("-" * len(header))
    any_both = False
    for lam in LAMBDAS:
        mix = mix0 if lam == 0.0 else fit_psd(
            data, lambda_psd=lam, n_max_psd=N_MAX_PSD,
            psd_polish_iters=POLISH_ITERS, psd_polish_lr=POLISH_LR, **FIT_KWARGS)
        rho = rho_from_splat(mix, N_MAX_PSD)
        r_pen = psd_report(rho)
        rho_p = project_psd(rho)
        r_proj = psd_report(rho_p)
        f_proj = fidelity(rho_p, psi)
        dF = f_proj - f0
        ok_a = dF > DF_THRESHOLD
        ok_b = r_proj["min_eig"] >= MIN_EIG_THRESHOLD
        any_both = any_both or (ok_a and ok_b)
        print(f"{lam:>7.1f} {fidelity(rho, psi):>8.4f} {r_pen['min_eig']:>12.4e} "
              f"{r_pen['negativity']:>9.4f} {f_proj:>8.4f} {dF:>+9.4f} "
              f"{r_proj['min_eig']:>13.4e} {'yes' if ok_a else 'no':>4} "
              f"{'yes' if ok_b else 'no':>4} "
              f"{'YES' if (ok_a and ok_b) else 'no':>5}")

    print()
    if any_both:
        print("VERDICT: penalty+projection satisfies (a) AND (b). Issue #8 is "
              "resolvable -- soft penalty to shrink negativity cheaply, then a "
              "small projection to land exactly on the PSD cone.")
    else:
        print("VERDICT (negative result): even penalty+projection cannot meet "
              "(a) and (b) jointly for this state.")


if __name__ == "__main__":
    main()
