"""Physics consistency tests for the two-mode entangled cat (states2.py).

Mirrors the single-mode checks in test_forward.py: the joint homodyne pdf
normalizes, equals the 2D Radon transform of the 4D Wigner function, and
agrees with an independent product-Fock construction built on the already
validated fock.py. The Wigner function is checked to be pure (purity 1) and
to carry the negativity that makes the state nonclassical.
"""

import numpy as np
import pytest

from wigner_splat.fock import quadrature_vectors
from wigner_splat.states2 import TwoModeCat


def _fock_cat_matrix(alpha, parity, n_max):
    """c_{mn} of |a,a> + parity |-a,-a| in the product Fock basis.

    Single-mode coherent coeffs coh(a)_m = e^{-a^2/2} a^m / sqrt(m!), and
    coh(-a)_m = (-1)^m coh(a)_m, so the cross term is a checkerboard sign.
    """
    m = np.arange(n_max)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    coh = np.exp(-(alpha ** 2) / 2 + m * np.log(np.abs(alpha)) - log_fact / 2)
    coh *= np.sign(alpha) ** m
    sign = (-1.0) ** m
    C = np.outer(coh, coh) + parity * np.outer(coh * sign, coh * sign)
    return C / np.linalg.norm(C)


def test_homodyne_pdf_normalized():
    cat = TwoModeCat(alpha=1.5, parity=+1)
    xs = np.linspace(-9, 9, 401)
    X1, X2 = np.meshgrid(xs, xs, indexing="ij")
    for th1, th2 in [(0.0, 0.0), (0.3, 1.1), (np.pi / 2, 0.7), (1.3, 2.5)]:
        P = cat.homodyne_pdf(X1, X2, th1, th2)
        integral = np.trapezoid(np.trapezoid(P, xs, axis=1), xs)
        assert integral == pytest.approx(1.0, abs=1e-6)


def test_homodyne_pdf_is_2d_radon_of_wigner():
    """THE KEY IDENTITY: the joint pdf is the 2D Radon transform of the 4D
    Wigner function. For each mode integrate over the direction orthogonal to
    the measured quadrature u_j = (cos th_j, sin th_j). This is the identity
    the whole two-mode reconstruction program rests on."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    qs = np.linspace(-3, 3, 5)  # coarse position grid (expensive integral)
    ss = np.linspace(-8, 8, 161)  # integration over the orthogonal directions
    Q1, Q2 = np.meshgrid(qs, qs, indexing="ij")
    for th1, th2 in [(0.0, 0.0), (0.3, 1.1), (0.7, np.pi / 2)]:
        c1, s1 = np.cos(th1), np.sin(th1)
        c2, s2 = np.cos(th2), np.sin(th2)
        q1 = qs[:, None, None, None]
        b1 = ss[None, :, None, None]
        q2 = qs[None, None, :, None]
        b2 = ss[None, None, None, :]
        x1, p1 = q1 * c1 - b1 * s1, q1 * s1 + b1 * c1
        x2, p2 = q2 * c2 - b2 * s2, q2 * s2 + b2 * c2
        W = cat.wigner(x1, p1, x2, p2)
        marginal = np.trapezoid(np.trapezoid(W, ss, axis=3), ss, axis=1)
        np.testing.assert_allclose(
            marginal, cat.homodyne_pdf(Q1, Q2, th1, th2), atol=1e-6
        )


def test_homodyne_pdf_matches_product_fock():
    """Cross-validation against the (1e-12-validated) fock.py: build the cat in
    the product Fock basis and evaluate the joint pdf as |(v1 kron v2).c|^2 with
    fock.quadrature_vectors. Must match the closed-form pdf to ~1e-9."""
    n_max = 30
    for parity in (+1, -1):
        cat = TwoModeCat(alpha=1.5, parity=parity)
        C = _fock_cat_matrix(1.5, parity, n_max)
        xs = np.linspace(-6, 6, 41)
        X1, X2 = np.meshgrid(xs, xs, indexing="ij")
        for th1, th2 in [(0.0, 0.0), (0.3, 1.1), (0.7, np.pi / 2)]:
            v1 = quadrature_vectors(xs, th1, n_max)  # (G, n_max), <n|x_theta>
            v2 = quadrature_vectors(xs, th2, n_max)
            pdf_fock = np.abs(v1 @ C @ v2.T) ** 2  # |sum c_{mn} v1_m v2_n|^2
            np.testing.assert_allclose(
                pdf_fock, cat.homodyne_pdf(X1, X2, th1, th2), atol=1e-9
            )


def test_wigner_is_pure_state():
    """(2 pi)^2 * integral W^2 d^4z = tr(rho^2) = 1 for the pure two-mode cat.
    Coarse 4D grid (41^4); documented tolerance abs 1e-3 covers the trapezoid
    truncation of the fringe on this resolution."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    g = np.linspace(-4.5, 4.5, 41)
    x1, p1, x2, p2 = np.meshgrid(g, g, g, g, indexing="ij")
    W = cat.wigner(x1, p1, x2, p2)
    dv = (g[1] - g[0]) ** 4
    purity = (2 * np.pi) ** 2 * np.sum(W ** 2) * dv
    assert purity == pytest.approx(1.0, abs=1e-3)


def test_wigner_has_negative_regions():
    """Nonclassicality: the fringe drives W clearly negative. Scan the (p1, p2)
    plane at x1 = x2 = 0, where the cos(2 sqrt2 a (p1+p2)) fringe lives."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    p = np.linspace(-3, 3, 201)
    P1, P2 = np.meshgrid(p, p)
    zero = np.zeros_like(P1)
    W = cat.wigner(zero, P1, zero, P2)
    assert W.min() < -1e-3


def test_sample_homodyne_deterministic_and_shaped():
    """Sampler is reproducible given rng and returns the promised data format."""
    cat = TwoModeCat(alpha=1.5, parity=+1)
    pairs = [(0.0, 0.0), (0.3, 1.1)]
    a = cat.sample_homodyne(pairs, 500, rng=7)
    b = cat.sample_homodyne(pairs, 500, rng=7)
    assert len(a) == 2
    for (ang, s), (angb, sb) in zip(a, b):
        assert s.shape == (500, 2)
        np.testing.assert_array_equal(s, sb)  # deterministic given rng
    # marginal means track the two displaced blobs at x = +/- sqrt(2) a along
    # theta = 0, so the joint sample cloud should have near-zero mean but
    # substantial spread on both axes.
    (_, s0) = a[0]
    assert abs(s0.mean()) < 0.3
    assert s0.std() > 1.0
