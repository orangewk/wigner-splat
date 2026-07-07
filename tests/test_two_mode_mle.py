"""Two-mode product-Fock MLE (mle2.py) and the cat coefficients (fock.cat2_*).

Mirrors the single-mode falsification comparison: reconstruct the entangled
two-mode cat from shared binned homodyne histograms and recover it above a
fidelity floor. cat2_fock is cross-validated against the closed-form joint
pdf (the identity already proven in test_two_mode_state.py), and the
hardened R rho R stop condition is exercised.
"""

import time

import numpy as np
import pytest

from wigner_splat.data2 import histogram_targets2
from wigner_splat.fock import (
    cat2_fock,
    cat2_truncation_fidelity,
    fidelity_pure,
    quadrature_vectors,
)
from wigner_splat.mle2 import mle2_reconstruct
from wigner_splat.states2 import TwoModeCat


def test_cat2_fock_matches_homodyne_pdf():
    """cat2_fock reproduces states2.TwoModeCat.homodyne_pdf via kron'd
    quadrature vectors: |sum_{mn} c_{mn} <m|x1><n|x2>|^2 == P(x1, x2)."""
    n_max = 30
    for parity in (+1, -1):
        cat = TwoModeCat(alpha=1.5, parity=parity)
        c = cat2_fock(1.5, parity=parity, n_max=n_max)
        C = c.reshape(n_max, n_max)
        xs = np.linspace(-6, 6, 41)
        X1, X2 = np.meshgrid(xs, xs, indexing="ij")
        for th1, th2 in [(0.0, 0.0), (0.3, 1.1), (0.7, np.pi / 2)]:
            v1 = quadrature_vectors(xs, th1, n_max)  # (G, n_max), <m|x1_theta>
            v2 = quadrature_vectors(xs, th2, n_max)
            pdf_fock = np.abs(v1 @ C @ v2.T) ** 2
            np.testing.assert_allclose(
                pdf_fock, cat.homodyne_pdf(X1, X2, th1, th2), atol=1e-9
            )


def test_cat2_fock_normalized():
    for parity in (+1, -1):
        c = cat2_fock(1.5, parity=parity, n_max=12)
        assert np.linalg.norm(c) == pytest.approx(1.0, abs=1e-12)


def test_truncation_ceiling_high_at_n_max_12():
    """The MLE ceiling: truncating alpha=1.5 at n_max=12 keeps > 0.999."""
    ceiling = cat2_truncation_fidelity(1.5, parity=+1, n_max=12)
    assert ceiling > 0.999
    # a coarse truncation must lose noticeably more, sanity check the metric
    assert cat2_truncation_fidelity(1.5, parity=+1, n_max=6) < ceiling


def test_mle2_recovers_two_mode_cat():
    """Recovery test: MLE on a 4x4 angle-pair grid, 3000 shots/pair, recovers
    the entangled cat well above the falsification floor."""
    alpha, n_max = 1.5, 12
    cat = TwoModeCat(alpha=alpha, parity=+1)
    grid = np.linspace(0, np.pi, 4, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]

    data = cat.sample_homodyne(pairs, 3000, rng=42)
    centers, targets = histogram_targets2(data, bins=40)

    t0 = time.perf_counter()
    rho, iters = mle2_reconstruct(centers, targets, n_max=n_max)
    wall = time.perf_counter() - t0

    psi = cat2_fock(alpha, parity=+1, n_max=n_max)
    fid = fidelity_pure(psi, rho)
    ceiling = cat2_truncation_fidelity(alpha, parity=+1, n_max=n_max)

    print(
        f"\nmle2 recovery: fidelity={fid:.4f}  ceiling={ceiling:.6f}  "
        f"iters={iters}  wall={wall:.1f}s"
    )
    assert iters < 2000  # converged, did not hit the iteration cap
    # falsification floor is 0.9; observed ~0.924 (finite 3000 shots x 16
    # pairs, ceiling 0.999). Tightened just below the observed value.
    assert fid > 0.91


def test_mle2_converges_monotonically_without_hitting_cap():
    """Positive half of the hardened stop condition: on clean data the run
    ascends the likelihood monotonically and converges strictly before the
    iteration cap. (Per the orientation warning in mle.py, a transposed R
    'silently stalls' rather than decreasing, so it would NOT trip the guard;
    the reliable, meaningful check is monotone ascent + genuine convergence,
    with the decrease guard exercised directly below.)"""
    alpha, n_max = 1.5, 8
    cat = TwoModeCat(alpha=alpha, parity=+1)
    grid = np.linspace(0, np.pi, 3, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 1500, rng=1)
    centers, targets = histogram_targets2(data, bins=30)

    lls = []
    rho, iters = mle2_reconstruct(
        centers, targets, n_max=n_max, callback=lambda it, ll: lls.append(ll)
    )
    assert iters < 2000  # converged, did not hit the cap
    # sampled every 50 iters; ascent must be monotone non-decreasing
    for a, b in zip(lls, lls[1:]):
        assert b >= a - 1e-9


def test_mle2_decrease_guard_is_live():
    """Negative half: the RuntimeError guard is not vacuous. Inject a one-shot
    likelihood-decreasing perturbation (halve p at a single late iteration,
    once the guard is active at it > 10) and confirm the monotonic-ascent
    violation is caught -- the same failure mode as broken measurement
    operators or an under-truncated basis."""
    alpha, n_max = 1.5, 8
    cat = TwoModeCat(alpha=alpha, parity=+1)
    grid = np.linspace(0, np.pi, 3, endpoint=False)
    pairs = [(t1, t2) for t1 in grid for t2 in grid]
    data = cat.sample_homodyne(pairs, 1500, rng=1)
    centers, targets = histogram_targets2(data, bins=30)

    orig_einsum = np.einsum
    state = {"calls": 0}

    def bad_einsum(subscripts, *operands, **kwargs):
        out = orig_einsum(subscripts, *operands, **kwargs)
        if subscripts == "mj,mj->m":  # the per-iteration p = <v|rho|v>
            state["calls"] += 1
            if state["calls"] == 15:  # guard already active (it > 10)
                out = out * 0.5  # force ll to drop by ~log(2)
        return out

    try:
        np.einsum = bad_einsum
        with pytest.raises(RuntimeError, match="likelihood decreased"):
            mle2_reconstruct(centers, targets, n_max=n_max)
    finally:
        np.einsum = orig_einsum
