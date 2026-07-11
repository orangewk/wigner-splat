"""Experiment 08 -- target-aligned physical rho=BB^dagger, three modes.

On exp06 seed-42 homodyne samples, measure whether a constructively physical
coherent-product ansatz can attain high exact state fidelity. This is an
existence probe: the ansatz contains the target cat family.

Same data as exp06: alpha=1.5, parity=+1, 3x3x3=27 angle triples over [0,pi)^3,
2000 shots/triple, seed 42. Fairness note: BB^dagger uses per-sample NLL, not
the splat's histogram-L2 objective. BB^dagger reports the exact pure-state
fidelity |<psi_fit|cat3>|^2; the historical non-PSD splat number is a Wigner
overlap score. This run does not determine whether negative-eigenvalue
components of the existing splat fit are necessary for that fit's score.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import (  # noqa: E402
    CoherentKetState, fit_bbdagM, fidelity_vs_cat3,
)
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
SHOTS = 2000
SEED = 42
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]


def sanity():
    print("=== sanity: exact cat3 as CoherentKetState -> F should be 1 ===")
    a = ALPHA
    exact = CoherentKetState(
        z=np.array([1.0, PARITY], complex),
        alpha=np.array([[a, a, a], [-a, -a, -a]], complex),
    )
    F = fidelity_vs_cat3(exact, ALPHA, PARITY)
    print(f"  F(exact cat3) = {F:.6f}  (expect 1.0)")
    # closed-form Z vs brute 1D grid on mode-factorized norm (single mode check)
    one = CoherentKetState(z=np.array([1.0, 1.0], complex),
                           alpha=np.array([[0.8], [-1.1]], complex))
    xs = np.linspace(-12, 12, 4000)
    from wigner_splat.states import coherent_wavefunction
    psi = coherent_wavefunction(xs, 0.8) + coherent_wavefunction(xs, -1.1)
    Zgrid = np.trapezoid(np.abs(psi) ** 2, xs)
    print(f"  Z closed-form={one.norm_sq():.6f}  Z grid={Zgrid:.6f}  "
          f"diff={abs(one.norm_sq() - Zgrid):.2e}")


def main():
    sanity()
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    print(f"\nsampling {len(GRID)} triples x {SHOTS} shots, seed={SEED} ...",
          flush=True)
    data = cat.sample_homodyne(GRID, SHOTS, rng=SEED)

    print("\n=== BB-dagger 3-mode target-aligned existence probe ===")
    print("historical reports: signed-splat overlap=0.756 (non-PSD), "
          "PSD-projected fidelity=0.48")
    for K in [4, 8]:
        t0 = time.time()
        state = fit_bbdagM(data, K=K, M=3, iters=200, lr=0.05, seed=0,
                           callback=lambda t, l: print(f"    K={K} it{t}: NLL={l:.4f}",
                                                        flush=True))
        wall = time.time() - t0
        F = fidelity_vs_cat3(state, ALPHA, PARITY)
        observation = (
            "HIGH-F TARGET-ALIGNED FIT"
            if F >= 0.70
            else "BELOW HISTORICAL PROBE THRESHOLD"
        )
        print(f"  K={K}: F={F:.4f}  wall={wall:.1f}s  physical=YES(by construction)  "
              f"[{observation}]")


if __name__ == "__main__":
    main()
