"""Issue #8 -- BB^dagger 3-mode robustness across the exp06 data seeds.

Confirms the seed-42 result is not seed-specific: fit the physical coherent-ket
reconstructor on each of exp06's three data seeds and report fidelity. Measured:
    seed 42: F=0.9501   seed 1: F=0.9434   seed 2: F=0.9332   (K=4, iters=120)
vs the signed splat's 0.756 / 0.741 / 0.624 on the same seeds.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.bbdagM import fit_bbdagM, fidelity_vs_cat3  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
SHOTS = 2000
GRID = [t for t in itertools.product(
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
    np.linspace(0, np.pi, 3, endpoint=False),
)]
SPLAT_F = {42: 0.756, 1: 0.741, 2: 0.624}  # exp06 signed-splat baseline (unphysical)


def main():
    cat = ThreeModeCat(ALPHA, parity=PARITY)
    print("seed | BB† F (physical) | splat F (unphysical)")
    for seed in [42, 1, 2]:
        data = cat.sample_homodyne(GRID, SHOTS, rng=seed)
        t0 = time.time()
        st = fit_bbdagM(data, K=4, M=3, iters=120, lr=0.05, seed=0)
        F = fidelity_vs_cat3(st, ALPHA, PARITY)
        print(f"{seed:>4} | {F:.4f}          | {SPLAT_F[seed]:.3f}   "
              f"(wall {time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
