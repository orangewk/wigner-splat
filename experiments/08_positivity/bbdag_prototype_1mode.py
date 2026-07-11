"""Experiment 08 (positivity) -- rho=BB^dagger prototype, single mode.

Prototype GATE for the constructively-physical reparameterization (issue #8,
dream #1). Falsification declared before running:

  1mode cat, K displaced-squeezed kets fit to homodyne data:
    PASS  if state fidelity F >= 0.95 (and physical -- automatic for |psi><psi|)
    FAIL  if F < 0.95 -> the fitting machinery is broken

A cat state IS a superposition of two coherent kets, so a correct pure-ket
fitter should recover it easily. This validates the forward model, loss,
optimizer, and fidelity path before the harder 3-mode test.

Also cross-checks sq_coherent_wavefunction(xi=0) == states.coherent_wavefunction.
"""
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdag import (  # noqa: E402
    PureKetState, fit_bbdag, fidelity_vs_pure, sq_coherent_wavefunction,
)
from wigner_splat.states import CatState, coherent_wavefunction  # noqa: E402

ALPHA = 1.5
PARITY = +1


def check_wavefunction_convention():
    x = np.linspace(-6, 6, 200)
    for beta in [1.5 + 0.0j, -0.7 + 1.1j, 0.3 - 0.9j]:
        a = sq_coherent_wavefunction(x, beta, 0.0 + 0.0j)
        b = coherent_wavefunction(x, beta)
        err = np.max(np.abs(a - b))
        print(f"  xi=0 vs coherent_wavefunction, beta={beta}: max|diff|={err:.2e}")
        assert err < 1e-12, "squeezed wavefunction does not reduce to coherent at xi=0"


def main():
    print("=== sq_coherent_wavefunction convention check ===")
    check_wavefunction_convention()

    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, 12, endpoint=False)
    data = cat.sample_homodyne(angles, 4000, rng=42)

    def psi_cat(x):
        beta = ALPHA
        return coherent_wavefunction(x, beta) + PARITY * coherent_wavefunction(x, -beta)

    print(f"\n=== BB-dagger fit: 1mode cat alpha={ALPHA}, parity={PARITY:+d} ===")
    for K in [2, 3, 4]:
        t0 = time.time()
        state = fit_bbdag(data, K=K, iters=400, lr=0.05, seed=0)
        wall = time.time() - t0
        F = fidelity_vs_pure(state, psi_cat)
        # physicality is automatic (rank-1 |psi><psi|), min_eig == 0 by construction
        print(f"  K={K}: F={F:.4f}  wall={wall:.1f}s  "
              f"(PASS if F>=0.95: {'PASS' if F >= 0.95 else 'FAIL'})")


if __name__ == "__main__":
    main()
