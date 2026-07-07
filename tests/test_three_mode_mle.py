"""Three-mode product-Fock MLE (mle3.py): correctness, cost, and recovery.

This is the "opponent" side of the decisive scaling point (issue #7): the
n_max**3 Fock reconstructor whose COST -- seconds/iteration and the honest
extrapolation to convergence -- is the headline datum for experiment 06, not a
pass/fail fidelity bar. The tests here therefore MEASURE and print cost, and
assert only sanity around it.

* test_kron_ordering_matches_coefficient_tensor: validates the flat triple-kron
  row layout against states3's index convention (m*n_max + n)*n_max + q, by
  reproducing the coefficient-TENSOR pdf (the einsum construction proven in
  test_three_mode_state.py) at n_max=8. Numerically identical constructions, so
  the match is to machine precision -- a pure ordering check.
* test_per_iteration_cost_official_budget: builds the full official problem
  (3x3x3 triples, 2000 shots/triple, rng=42, bins=24, n_max=8), runs EXACTLY 3
  iterations, and prints seconds/iteration. Asserts only sanity (finite,
  positive loglik, monotone ascent). Kept under ~60 s (not marked slow).
* test_mle3_recovery_within_budget (slow): the same problem under a 15-minute
  soft wall budget; prints fidelity reached, iterations, converged flag, and the
  fidelity trajectory. The scientific deliverable is the measured trajectory;
  the asserts are floors the run genuinely clears.
"""

import time

import numpy as np
import pytest

from wigner_splat.data3 import histogram_targets3
from wigner_splat.fock import (
    _coherent_coeffs,
    cat3_fock,
    cat3_truncation_fidelity,
    fidelity_pure,
    quadrature_vectors,
)
from wigner_splat.mle3 import mle3_reconstruct
from wigner_splat.states3 import ThreeModeCat


def _official_problem(n_max=8):
    """The shared official-budget problem: 3x3x3 triples, 2000 shots, bins=24.

    Both cost and recovery tests build the SAME histograms (the same-data rule),
    so this factory keeps them identical.
    """
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    grid = np.linspace(0, np.pi, 3, endpoint=False)
    triples = [(a, b, c) for a in grid for b in grid for c in grid]
    data = cat.sample_homodyne(triples, 2000, rng=42)
    centers, targets = histogram_targets3(data, bins=24)
    return centers, targets


def test_kron_ordering_matches_coefficient_tensor():
    """Flat triple-kron rows reproduce the coefficient-tensor pdf at n_max=8.

    The tensor construction (test_three_mode_state.py test 2) evaluates
    |sum_{mnq} c_{mnq} <x1|m>e^{-im th}<x2|n>e^{-in th}<x3|q>e^{-iq th}|^2 via
    einsum. mle3's measurement rows instead flatten the triple kron with index
    (m*n_max + n)*n_max + q and dot against cat3_fock's flat coefficient vector.
    Same numbers, different bookkeeping: agreement to machine precision confirms
    the kron ordering matches states3's / cat3_fock's flat layout. (~0.05 s)
    """
    n_max = 8
    xs = np.linspace(-5, 5, 9)  # one tiny grid
    th1, th2, th3 = 0.3, 1.1, 0.7
    v1 = quadrature_vectors(xs, th1, n_max)
    v2 = quadrature_vectors(xs, th2, n_max)
    v3 = quadrature_vectors(xs, th3, n_max)

    # coefficient-TENSOR pdf (the already-validated einsum construction)
    cp = _coherent_coeffs(1.5, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = (
        cp[:, None, None] * cp[None, :, None] * cp[None, None, :]
        + cm[:, None, None] * cm[None, :, None] * cm[None, None, :]
    )
    C = C / np.linalg.norm(C)
    pdf_tensor = np.abs(np.einsum("im,jn,kq,mnq->ijk", v1, v2, v3, C)) ** 2

    # flat triple-kron rows (mle3's V-row layout) dotted with the flat cat3_fock
    c = cat3_fock(1.5, +1, n_max)
    assert np.array_equal(c, C.reshape(-1))  # cat3_fock IS this flat layout
    rows = (
        v1[:, None, None, :, None, None]
        * v2[None, :, None, None, :, None]
        * v3[None, None, :, None, None, :]
    ).reshape(len(xs), len(xs), len(xs), n_max ** 3)
    pdf_flat = np.abs(rows @ c) ** 2

    np.testing.assert_allclose(pdf_flat, pdf_tensor, atol=1e-12)


def test_per_iteration_cost_official_budget():
    """PER-ITERATION COST at the official budget, n_max=8 -- the headline datum.

    Runs EXACTLY 3 iterations and prints seconds/iteration (measured from the
    callback's elapsed deltas, which exclude the one-off V build). Asserts only
    sanity: finite positive loglik, monotone ascent over the 3 iterations. On
    the dev box ~0.7 s/iter, so the whole test is a few seconds (not slow).
    """
    n_max = 8
    centers, targets = _official_problem(n_max)

    lls, elapsed = [], []
    t0 = time.perf_counter()
    rho, iters, converged = mle3_reconstruct(
        centers, targets, n_max=n_max, max_iters=3,
        callback=lambda it, ll, el, rho: (lls.append(ll), elapsed.append(el)),
    )
    total = time.perf_counter() - t0

    assert iters == 3 and not converged  # hit the 3-iteration cap, did not converge
    per_iter = np.diff([0.0] + elapsed)
    print(
        f"\nmle3 per-iteration cost (n_max={n_max}, N={n_max**3}): "
        f"{np.mean(per_iter[1:]) if len(per_iter) > 1 else per_iter[0]:.3f} s/iter "
        f"(iters {per_iter.round(3).tolist()} s, build+3it total {total:.1f} s)"
    )
    assert all(np.isfinite(ll) for ll in lls)
    # ll = f @ log(p) with p the per-cell probability MASS (density x dx^3 < 1),
    # so ll is negative here; the meaningful sanity check is monotone ascent.
    for a, b in zip(lls, lls[1:]):
        assert b >= a - 1e-9  # monotone R rho R ascent


@pytest.mark.slow
def test_mle3_recovery_within_budget():
    """Recovery under a 15-minute soft wall budget (SLOW). Prints the fidelity
    trajectory, iterations, converged flag, and time -- the scientific output.

    Measured on the dev box (~0.9 s/iter): the run does NOT converge inside the
    budget -- it returns at ~935 iterations with converged=False and F ~ 0.70
    against the 0.99321 ceiling. The loglik plateaus within ~40 iterations while
    the fidelity keeps creeping (0.49 at it=20, 0.70 at it=920): with only
    M ~ 17.7k measurement rows against 512**2 density-matrix parameters the
    problem is badly underdetermined and the R rho R fixed point drifts slowly
    along near-flat likelihood directions. That DNF trajectory is the
    deliverable; the asserts are floors the run genuinely clears (fidelity
    above 0.5, monotone loglik), not a tight fidelity bar. (~15 min)
    """
    alpha, n_max = 1.5, 8
    centers, targets = _official_problem(n_max)
    psi = cat3_fock(alpha, +1, n_max)
    ceiling = cat3_truncation_fidelity(alpha, +1, n_max)

    lls, traj = [], []

    def cb(it, ll, elapsed, rho):
        lls.append(ll)
        if it == 1 or it % 20 == 0:
            traj.append((it, elapsed, fidelity_pure(psi, rho)))

    rho, iters, converged = mle3_reconstruct(
        centers, targets, n_max=n_max, tol=1e-10, callback=cb,
        time_budget_s=900,
    )
    fid = fidelity_pure(psi, rho)

    print(
        f"\nmle3 recovery (n_max={n_max}): fidelity={fid:.5f} "
        f"ceiling={ceiling:.5f} iters={iters} converged={converged}"
    )
    print("  trajectory (it, elapsed_s, fidelity) every ~20 iters:")
    for it, el, f in traj:
        print(f"    it={it:4d}  t={el:7.1f}s  F={f:.5f}")

    # floors the run genuinely achieves; cost trajectory above is the deliverable
    assert fid > 0.5
    for a, b in zip(lls, lls[1:]):
        assert b >= a - 1e-9  # monotone ascent throughout
