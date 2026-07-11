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
Fresh runs save raw samples, optimizer trace, fitted parameters, metadata, and
the source commit under the ignored ``out/`` directory.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from bbdag_bundle import (  # noqa: E402
    git_source_state, timestamped_bundle_path, write_bbdag_bundle,
)
from wigner_splat.bbdagM import (  # noqa: E402
    CoherentKetState, fit_bbdagM, fidelity_vs_cat3, nll,
)
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
MODES = 3
SHOTS = 2000
SEED = 42
K_VALUES = (4, 8)
ITERS = 200
LEARNING_RATE = 0.05
INIT_SEED = 0
GRAD_EPS = 1e-5
OUT_ROOT = pathlib.Path(__file__).resolve().parent / "out"
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
    source = git_source_state()
    print(f"\nsampling {len(GRID)} triples x {SHOTS} shots, seed={SEED} ...",
          flush=True)
    data = cat.sample_homodyne(GRID, SHOTS, rng=SEED)

    print("\n=== BB-dagger 3-mode target-aligned existence probe ===")
    print("historical reports: signed-splat overlap=0.756 (non-PSD), "
          "PSD-projected fidelity=0.48")
    for K in K_VALUES:
        trace = []

        def record_trace(iteration, loss):
            trace.append((int(iteration), float(loss)))
            print(f"    K={K} it{iteration}: NLL={loss:.4f}", flush=True)

        t0 = time.perf_counter()
        state = fit_bbdagM(
            data, K=K, M=MODES, iters=ITERS, lr=LEARNING_RATE,
            seed=INIT_SEED, callback=record_trace, grad_eps=GRAD_EPS,
        )
        wall = time.perf_counter() - t0
        F = fidelity_vs_cat3(state, ALPHA, PARITY)
        final_nll = nll(state, data)
        final_trace = (ITERS, float(final_nll))
        if trace and trace[-1][0] == ITERS:
            trace[-1] = final_trace
        else:
            trace.append(final_trace)
        observation = (
            "HIGH-F TARGET-ALIGNED FIT"
            if F >= 0.70
            else "BELOW HISTORICAL PROBE THRESHOLD"
        )
        print(f"  K={K}: F={F:.4f}  wall={wall:.1f}s  physical=YES(by construction)  "
              f"[{observation}]")
        bundle = write_bbdag_bundle(
            timestamped_bundle_path(OUT_ROOT, f"bbdag-3mode-seed{SEED}-k{K}"),
            data=data,
            state=state,
            trace=trace,
            metadata={
                "entrypoint": "experiments/08_positivity/bbdag_3mode.py",
                "target": {
                    "family": "three_mode_cat", "modes": MODES,
                    "alpha": ALPHA, "parity": PARITY,
                },
                "data": {
                    "seed": SEED, "shots_per_grid_point": SHOTS,
                    "grid_points": len(GRID), "grid_interval": "[0, pi)",
                    "grid_endpoint": False,
                },
                "optimizer": {
                    "K": K, "iters": ITERS, "init_seed": INIT_SEED,
                    "learning_rate": LEARNING_RATE, "grad_eps": GRAD_EPS,
                    "loss": "per_sample_nll", "gradient": "finite_difference",
                },
                "result": {
                    "exact_state_fidelity": float(F),
                    "final_training_per_sample_nll": float(final_nll),
                    "fit_wall_s": float(wall),
                    "physical_by_construction": True,
                },
                "source": source,
            },
        )
        print(f"  evidence bundle: {bundle}")


if __name__ == "__main__":
    main()
