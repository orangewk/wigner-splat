"""Experiment 08 (positivity) -- rho=BB^dagger, THREE modes (issue #8 decider).

The falsification test declared in the handoff. On exp06 seed42's data (the
point where the SIGNED splat wins fidelity 0.756 but its rho is UNphysical,
physicalized F_proj=0.48), ask whether a CONSTRUCTIVELY-PHYSICAL reconstructor
can match it:

    PASS (tension RESOLVED): BB^dagger reaches F >= 0.70 AND is physical
        (automatic for |psi><psi|)  -> the negativity was NOT load-bearing.
    FAIL (negative result): BB^dagger stalls below F ~ 0.55 within budget
        -> physicality genuinely costs fidelity here, OR the ansatz/optimizer
        is too weak.

Same data as exp06: alpha=1.5, parity=+1, 3x3x3=27 angle triples over [0,pi)^3,
2000 shots/triple, seed 42. Fairness note: BB^dagger uses per-sample NLL, not
the shared histogram; both consume the SAME homodyne samples. Fidelity is the
exact pure-state overlap |<psi_fit|cat3>|^2 (closed form), comparable to the
splat's Wigner-overlap fidelity but not identical -- reported as such.
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

    print(f"\n=== BB-dagger 3-mode fit (compare: signed splat F=0.756 unphysical, "
          f"F_proj=0.48) ===")
    for K in [4, 8]:
        t0 = time.time()
        state = fit_bbdagM(data, K=K, M=3, iters=200, lr=0.05, seed=0,
                           callback=lambda t, l: print(f"    K={K} it{t}: NLL={l:.4f}",
                                                        flush=True))
        wall = time.time() - t0
        F = fidelity_vs_cat3(state, ALPHA, PARITY)
        verdict = "PASS" if F >= 0.70 else ("FAIL" if F < 0.55 else "GRAY")
        print(f"  K={K}: F={F:.4f}  wall={wall:.1f}s  physical=YES(by construction)  "
              f"[{verdict}]")


if __name__ == "__main__":
    main()
