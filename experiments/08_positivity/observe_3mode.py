"""Experiment 08 (positivity) -- observation step, three modes.

Issue #8 asked whether a signed splat mixture's Hermitian operator is PSD.
experiments/08_positivity/diagnose_1mode.py answered that in 1 mode via a
phase-space GRID (161^2 points) -- infeasible in 6D. wigner_splat.fock_project
answers it in closed form instead (no grid, see its module docstring for the
Bargmann/Hermite derivation), validated against the grid in 1 mode and against
exact Fock-truncated cat states in 1/2/3 modes (tests/test_fock_project.py).

This script reuses exp06's winning fit3f splat (seed 42, official 3x3x3 angle
grid over [0,pi)^3, 2000 shots/triple, bins=24 -- see
experiments/06_three_mode/run.py) and reports the 3-mode operator's min
eigenvalue / negativity: the observation a future fit-loop PSD penalty would
need to justify itself against, now that materializing rho at this scale is
tractable.
"""
import itertools
import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit3f import fit3f  # noqa: E402
from wigner_splat.fock_project import psd_report, rho_from_splat  # noqa: E402
from wigner_splat.states3 import ThreeModeCat  # noqa: E402

ALPHA = 1.5
PARITY = +1
BINS = 24
N_MAX = 8  # per-mode Fock cutoff, matching exp06's MLE cutoff (8**3 = 512 dims)
SHOTS = 2000  # per angle triple
SEED = 42
GRID = [
    t
    for t in itertools.product(
        np.linspace(0, np.pi, 3, endpoint=False),
        np.linspace(0, np.pi, 3, endpoint=False),
        np.linspace(0, np.pi, 3, endpoint=False),
    )
]  # 3x3x3 = 27 triples over [0, pi)^3, the exp06 official budget


def main():
    cat = ThreeModeCat(ALPHA, PARITY)
    print(f"three-mode cat alpha={ALPHA} parity={PARITY:+d}  "
          f"n_max={N_MAX} ({N_MAX ** 3} Fock dims)")
    print(f"sampling {len(GRID)} triples x {SHOTS} shots (seed={SEED}) ...",
          flush=True)
    data = cat.sample_homodyne(GRID, SHOTS, rng=SEED)

    print(f"fitting fit3f (bins={BINS}) ...", flush=True)
    t0 = time.perf_counter()
    mix = fit3f(data, bins=BINS)
    t_fit = time.perf_counter() - t0
    K = len(mix.w)
    print(f"fit3f done: K={K} splats, wall={t_fit:.1f}s  "
          f"weight sum={mix.w.sum():.4f}", flush=True)

    print(f"materializing rho_from_splat (n_max={N_MAX}, {K} splats) ...",
          flush=True)
    t0 = time.perf_counter()
    rho = rho_from_splat(mix, N_MAX)
    t_rho = time.perf_counter() - t0
    print(f"rho materialized: shape={rho.shape}  wall={t_rho:.1f}s", flush=True)

    report = psd_report(rho)
    print("\n" + "=" * 72)
    print("3-MODE PSD OBSERVATION (closed-form, no grid)")
    print("=" * 72)
    print(f"trace      = {report['trace']:+.4f}")
    print(f"min_eig    = {report['min_eig']:+.4e}")
    print(f"max_eig    = {report['max_eig']:+.4f}")
    print(f"negativity = {report['negativity']:.4e}  "
          f"(|sum of negative eigenvalues|)")
    print(f"\nPSD? {'NO -- min_eig < 0' if report['min_eig'] < 0 else 'yes'}")
    print(f"\n(fit3f wall={t_fit:.1f}s, rho_from_splat wall={t_rho:.1f}s, "
          f"K={K} splats)")


if __name__ == "__main__":
    main()
