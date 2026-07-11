"""Issue #8 -- BB^dagger 3-mode robustness across the exp06 data seeds.

Fit the target-aligned physical coherent-ket reconstructor on each of exp06's
three data seeds. The historical branch report lists:
    seed 42: F=0.9501   seed 1: F=0.9434   seed 2: F=0.9332   (K=4, iters=120)
versus signed-splat target Wigner-overlap scores 0.756 / 0.741 / 0.624.

The BB^dagger stdout logs and fit parameters for those historical numbers were
not retained. A fresh invocation produces new measurements; it does not recover
the missing historical evidence. BB^dagger also uses a different representation
and per-sample NLL rather than the splat's histogram-L2 objective, so this is an
existence/robustness probe rather than a physicalization of the signed splat.
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
from wigner_splat.bbdagM import fit_bbdagM, fidelity_vs_cat3, nll  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
MODES = 3
SHOTS = 2000
SEEDS = (42, 1, 2)
K = 4
ITERS = 120
LEARNING_RATE = 0.05
INIT_SEED = 0
GRAD_EPS = 1e-5
OUT_ROOT = pathlib.Path(__file__).resolve().parent / "out"
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]
SPLAT_F = {42: 0.756, 1: 0.741, 2: 0.624}  # exp06 non-PSD overlap-score baseline


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    print("seed | BB† exact F (physical) | splat overlap score (non-PSD)")
    source = git_source_state()
    for seed in SEEDS:
        data = cat.sample_homodyne(GRID, SHOTS, rng=seed)
        trace = []

        def record_trace(iteration, loss):
            trace.append((int(iteration), float(loss)))

        t0 = time.perf_counter()
        st = fit_bbdagM(
            data, K=K, M=MODES, iters=ITERS, lr=LEARNING_RATE,
            seed=INIT_SEED, callback=record_trace, grad_eps=GRAD_EPS,
        )
        wall = time.perf_counter() - t0
        final_nll = nll(st, data)
        final_trace = (ITERS, float(final_nll))
        if trace and trace[-1][0] == ITERS:
            trace[-1] = final_trace
        else:
            trace.append(final_trace)
        F = fidelity_vs_cat3(st, ALPHA, PARITY)
        print(f"{seed:>4} | {F:.4f}          | {SPLAT_F[seed]:.3f}   "
              f"(wall {wall:.0f}s)")
        bundle = write_bbdag_bundle(
            timestamped_bundle_path(OUT_ROOT, f"bbdag-robust-seed{seed}-k{K}"),
            data=data,
            state=st,
            trace=trace,
            metadata={
                "entrypoint": (
                    "experiments/08_positivity/bbdag_3mode_robustness.py"
                ),
                "target": {
                    "family": "three_mode_cat", "modes": MODES,
                    "alpha": ALPHA, "parity": PARITY,
                },
                "data": {
                    "seed": seed, "shots_per_grid_point": SHOTS,
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
        print(f"     evidence bundle: {bundle}")


if __name__ == "__main__":
    main()
