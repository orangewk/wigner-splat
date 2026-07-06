"""Experiment 03: splat fitter vs iterative MLE — the falsification test.

The README commits to a falsification condition: if the splat approach
cannot beat iterative MLE on both fidelity and speed at equal shot counts,
it brings no computational gain. This experiment runs both reconstructors
on identical binned homodyne data across several shot budgets and prints
the comparison. Record the outcome either way.

Both methods see the same histograms (fit.histogram_targets, 80 bins).
Fidelity to the true cat state: for MLE, <psi|rho|psi> in the Fock basis;
for the splat mixture (which only exists as a Wigner function),
tr(rho sigma) = 2 pi * integral of W_fit W_true — the estimators agree for
a common state to grid accuracy (checked in tests).
"""

import pathlib
import sys
import time

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from wigner_splat.fit import fit, histogram_targets  # noqa: E402
from wigner_splat.fock import (  # noqa: E402
    cat_fock, fidelity_pure, wigner_from_rho, wigner_overlap,
)
from wigner_splat.mle import mle_reconstruct  # noqa: E402
from wigner_splat.states import CatState  # noqa: E402

ALPHA = 1.5
ANGLES = np.linspace(0, np.pi, 12, endpoint=False)
BUDGETS = [250, 1000, 4000]  # shots per angle
N_MAX = 20

cat = CatState(alpha=ALPHA, parity=+1)
psi = cat_fock(ALPHA, +1, n_max=N_MAX)
xs = np.linspace(-6, 6, 301)
X, P = np.meshgrid(xs, xs)
W_true = cat.wigner(X, P)

rows = []
for shots in BUDGETS:
    data = cat.sample_homodyne(ANGLES, shots, rng=42)
    centers, targets = histogram_targets(data)

    t0 = time.time()
    mix = fit(data, K=4, iters=800, seed=0, densify_every=100, K_max=12)
    t_splat = time.time() - t0
    W_splat = mix.wigner(X, P)
    f_splat = wigner_overlap(W_splat, W_true, xs)

    t0 = time.time()
    rho, iters = mle_reconstruct(centers, targets, n_max=N_MAX)
    t_mle = time.time() - t0
    f_mle = fidelity_pure(psi, rho)
    W_mle = wigner_from_rho(rho, X, P)

    rows.append((shots, f_splat, t_splat, W_splat.min(),
                 f_mle, t_mle, W_mle.min(), iters))

print(f"\ncat alpha={ALPHA}, {len(ANGLES)} angles, true Wigner min "
      f"{W_true.min():.3f}\n")
print(f"{'shots/angle':>11} | {'F_splat':>7} {'t_splat':>8} {'min_W':>7} | "
      f"{'F_mle':>7} {'t_mle':>8} {'min_W':>7} {'iters':>5}")
print("-" * 78)
for shots, fs, ts, ms, fm, tm, mm, it in rows:
    print(f"{shots:>11} | {fs:7.4f} {ts:7.2f}s {ms:7.3f} | "
          f"{fm:7.4f} {tm:7.2f}s {mm:7.3f} {it:>5}")

print("\nverdict per budget (falsification: splat must win BOTH):")
for shots, fs, ts, ms, fm, tm, mm, it in rows:
    fid = "splat" if fs > fm else "MLE"
    spd = "splat" if ts < tm else "MLE"
    both = "PASS" if (fid == "splat" and spd == "splat") else "FAIL"
    print(f"  {shots:>5} shots/angle: fidelity -> {fid}, speed -> {spd}  [{both}]")
