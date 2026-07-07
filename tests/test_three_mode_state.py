"""Physics consistency tests for the three-mode entangled cat (states3.py).

The three-mode analog of test_two_mode_state.py: the joint homodyne pdf
normalizes, equals the reduced Radon transform of the 6D Wigner function, and
agrees with an independent product-Fock coefficient construction built on the
already validated fock.py. The Wigner function is checked pure (purity 1) and
to carry the negativity that makes the state nonclassical, and the sampler is
reproducible and correctly shaped.

Runtimes on the dev box (documented per test in comments): the whole file is
about 25 s, dominated by the coarse 6D purity integral (~13 s).
"""

import numpy as np
import pytest

from wigner_splat.fock import (
    _coherent_coeffs,
    cat3_fock,
    cat3_truncation_fidelity,
    quadrature_vectors,
)
from wigner_splat.states3 import ThreeModeCat


def _fock_cat_tensor(alpha, parity, n_max):
    """c_{mnq} of |a,a,a> + parity |-a,-a,-a| in the product Fock basis.

    Single-mode coherent coeffs coh(a)_m, and coh(-a)_m = (-1)^m coh(a)_m, so
    the cross term is a checkerboard sign. Same convention as cat3_fock but
    kept as a rank-3 tensor for the einsum contraction below.
    """
    cp = _coherent_coeffs(alpha, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    C = (
        cp[:, None, None] * cp[None, :, None] * cp[None, None, :]
        + parity * cm[:, None, None] * cm[None, :, None] * cm[None, None, :]
    )
    return C / np.linalg.norm(C)


def test_homodyne_pdf_normalized():
    """3D trapezoid normalization at several triples, including asymmetric.
    (~0.2 s)"""
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    xs = np.linspace(-9, 9, 121)
    x1 = xs[:, None, None]
    x2 = xs[None, :, None]
    x3 = xs[None, None, :]
    for th in [(0.0, 0.0, 0.0), (0.3, 1.1, 0.7), (np.pi / 2, 0.7, 2.4),
               (1.3, 2.5, 0.2)]:
        P = cat.homodyne_pdf(x1, x2, x3, *th)
        integral = np.trapezoid(
            np.trapezoid(np.trapezoid(P, xs, axis=2), xs, axis=1), xs
        )
        assert integral == pytest.approx(1.0, abs=1e-6)


def test_homodyne_pdf_matches_product_fock():
    """THE KEY CROSS-VALIDATION against the (1e-12-validated) fock.py: build the
    cat as a product-Fock coefficient tensor c_{mnq} and evaluate the joint pdf
    directly as |sum_{mnq} c_{mnq} <x1|m>e^{-im th1} <x2|n>e^{-in th2}
    <x3|q>e^{-iq th3}|^2 via einsum with quadrature_vectors -- no 13824x13824
    density matrix needed. Must match the closed-form pdf to ~1e-9. This
    doubles as the validation of cat3_fock's coefficient convention. (~1.5 s)"""
    n_max = 24
    xs = np.linspace(-6, 6, 21)
    X1, X2, X3 = np.meshgrid(xs, xs, xs, indexing="ij")
    for parity in (+1, -1):
        cat = ThreeModeCat(alpha=1.5, parity=parity)
        C = _fock_cat_tensor(1.5, parity, n_max)
        for th1, th2, th3 in [(0.0, 0.0, 0.0), (0.3, 1.1, 0.7),
                              (0.7, np.pi / 2, 2.0)]:
            v1 = quadrature_vectors(xs, th1, n_max)  # (G, n_max), <n|x_theta>
            v2 = quadrature_vectors(xs, th2, n_max)
            v3 = quadrature_vectors(xs, th3, n_max)
            amp = np.einsum("im,jn,kq,mnq->ijk", v1, v2, v3, C)
            pdf_fock = np.abs(amp) ** 2
            np.testing.assert_allclose(
                pdf_fock, cat.homodyne_pdf(X1, X2, X3, th1, th2, th3),
                atol=3e-9,
            )


def test_homodyne_pdf_is_reduced_radon_of_wigner():
    """THE KEY IDENTITY: integrating the 6D Wigner over the three conjugate
    directions (orthogonal to each measured quadrature u_j = (cos th_j,
    sin th_j)) returns the joint pdf. Done at ONE asymmetric triple on a coarse
    3^3 position grid; the direction integrals run on a wide 91-point grid,
    looping over positions to keep only a 3D array live. Tolerance atol 1e-6
    (the integral is effectively exact here -- observed ~1e-14). (~1.1 s)"""
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    th1, th2, th3 = 0.3, 1.1, 0.7
    qs = np.linspace(-2, 2, 3)
    ss = np.linspace(-7, 7, 91)  # integration over the orthogonal directions
    c1, s1 = np.cos(th1), np.sin(th1)
    c2, s2 = np.cos(th2), np.sin(th2)
    c3, s3 = np.cos(th3), np.sin(th3)
    b1 = ss[:, None, None]
    b2 = ss[None, :, None]
    b3 = ss[None, None, :]
    marginal = np.zeros((3, 3, 3))
    for i, q1 in enumerate(qs):
        for j, q2 in enumerate(qs):
            for k, q3 in enumerate(qs):
                x1, p1 = q1 * c1 - b1 * s1, q1 * s1 + b1 * c1
                x2, p2 = q2 * c2 - b2 * s2, q2 * s2 + b2 * c2
                x3, p3 = q3 * c3 - b3 * s3, q3 * s3 + b3 * c3
                W = cat.wigner(x1, p1, x2, p2, x3, p3)
                marginal[i, j, k] = np.trapezoid(
                    np.trapezoid(np.trapezoid(W, ss, axis=2), ss, axis=1), ss
                )
    Q1, Q2, Q3 = np.meshgrid(qs, qs, qs, indexing="ij")
    np.testing.assert_allclose(
        marginal, cat.homodyne_pdf(Q1, Q2, Q3, th1, th2, th3), atol=1e-6
    )


def test_wigner_is_pure_state():
    """(2 pi)^3 * integral W^2 d^6z = tr(rho^2) = 1 for the pure three-mode cat.
    A full-resolution 6D grid is infeasible; this uses a coarse anisotropic grid
    (17 points on each x-axis over [-5, 5], 33 on each p-axis over [-4.5, 4.5],
    the p-axes finer because the fringe lives there) with a Riemann sum, looping
    over (x1, x2) to bound memory. Documented tolerance abs 5e-3 covers the
    fringe undersampling (observed deviation ~2e-6 here). (~13 s)"""
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    xg = np.linspace(-5.0, 5.0, 17)
    pg = np.linspace(-4.5, 4.5, 33)
    dx, dp = xg[1] - xg[0], pg[1] - pg[0]
    P1 = pg[:, None, None, None]
    X3 = xg[None, :, None, None]
    P2 = pg[None, None, :, None]
    P3 = pg[None, None, None, :]
    tot = 0.0
    for x1 in xg:
        for x2 in xg:
            W = cat.wigner(x1, P1, x2, P2, X3, P3)
            tot += np.sum(W ** 2)
    purity = (2 * np.pi) ** 3 * tot * (dx * dp) ** 3
    assert purity == pytest.approx(1.0, abs=5e-3)


def test_wigner_has_negative_regions():
    """Nonclassicality: the fringe drives W clearly negative. Scan the (p1, p2)
    plane at x1 = x2 = x3 = 0, p3 = 0, where the cos(2 sqrt2 a (p1+p2+p3))
    fringe lives. (~0.05 s)"""
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    p = np.linspace(-3, 3, 201)
    P1, P2 = np.meshgrid(p, p)
    zero = np.zeros_like(P1)
    W = cat.wigner(zero, P1, zero, P2, zero, zero)
    assert W.min() < -1e-3


def test_cat3_fock_normalized_and_truncation_ceiling():
    """cat3_fock is a unit vector of the promised length and flat layout, and
    the truncation ceiling rises monotonically toward 1 as n_max grows -- the
    hard upper bound on any n_max**3 Fock MLE fidelity. (~0.01 s)"""
    v = cat3_fock(1.5, +1, 8)
    assert v.shape == (8 ** 3,)
    assert np.linalg.norm(v) == pytest.approx(1.0, abs=1e-12)
    ceilings = [cat3_truncation_fidelity(1.5, +1, nm) for nm in (8, 10, 12)]
    # printed for the exp06 scaling story (alpha = 1.5, parity +1)
    print("cat3 truncation ceilings n_max=8/10/12:", ceilings)
    assert all(0.0 < c <= 1.0 for c in ceilings)
    assert ceilings[0] < ceilings[1] < ceilings[2]
    assert ceilings[0] == pytest.approx(0.99321, abs=1e-4)
    assert ceilings[2] == pytest.approx(0.99999, abs=1e-4)


def test_sample_homodyne_deterministic_and_shaped():
    """Sampler is reproducible given rng and returns the promised data format.
    (~0.7 s)"""
    cat = ThreeModeCat(alpha=1.5, parity=+1)
    triples = [(0.0, 0.0, 0.0), (0.3, 1.1, 0.7)]
    a = cat.sample_homodyne(triples, 500, rng=7)
    b = cat.sample_homodyne(triples, 500, rng=7)
    assert len(a) == 2
    for (ang, s), (angb, sb) in zip(a, b):
        assert s.shape == (500, 3)
        assert ang == angb
        np.testing.assert_array_equal(s, sb)  # deterministic given rng
    # along theta = 0 each mode's marginal is symmetric over the two displaced
    # blobs at x = +/- sqrt(2) a, so the joint cloud has near-zero mean and
    # substantial spread on every axis.
    (_, s0) = a[0]
    assert abs(s0.mean()) < 0.3
    assert s0.std() > 1.0
