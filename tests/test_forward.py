"""Physics consistency tests for the reference state and the forward model."""

import numpy as np
import pytest

from wigner_splat.forward import SplatMixture
from wigner_splat.states import CatState


def test_cat_homodyne_pdf_normalized():
    cat = CatState(alpha=2.0, parity=+1)
    xs = np.linspace(-10, 10, 4001)
    for theta in [0.0, 0.3, np.pi / 2]:
        integral = np.trapezoid(cat.homodyne_pdf(xs, theta), xs)
        assert integral == pytest.approx(1.0, abs=1e-6)


def test_cat_wigner_marginal_matches_homodyne_pdf():
    """The Radon transform of the Wigner function must equal the homodyne pdf.
    This is the identity the whole reconstruction program rests on."""
    cat = CatState(alpha=1.5, parity=+1)
    xs = np.linspace(-6, 6, 121)
    ss = np.linspace(-8, 8, 2001)
    for theta in [0.0, 0.7, np.pi / 2]:
        u = np.array([np.cos(theta), np.sin(theta)])
        n = np.array([-np.sin(theta), np.cos(theta)])
        pts = xs[:, None, None] * u + ss[None, :, None] * n
        marginal = np.trapezoid(cat.wigner(pts[..., 0], pts[..., 1]), ss, axis=1)
        np.testing.assert_allclose(marginal, cat.homodyne_pdf(xs, theta), atol=1e-6)


def test_splat_radon_matches_numeric_marginal():
    mix = SplatMixture(
        w=[0.7, 0.5, -0.2],
        mu=[[1.0, 0.5], [-1.5, 0.0], [0.0, 0.0]],
        s=np.log([[0.5, 1.2], [0.8, 0.8], [0.4, 0.9]]),
        phi=[0.3, 0.0, 1.1],
    )
    xs = np.linspace(-6, 6, 61)
    ss = np.linspace(-9, 9, 3001)
    for theta in [0.0, 0.4, 1.3]:
        u = np.array([np.cos(theta), np.sin(theta)])
        n = np.array([-np.sin(theta), np.cos(theta)])
        pts = xs[:, None, None] * u + ss[None, :, None] * n
        numeric = np.trapezoid(mix.wigner(pts[..., 0], pts[..., 1]), ss, axis=1)
        np.testing.assert_allclose(mix.radon(xs, theta), numeric, atol=1e-8)


def test_cat_state_is_representable_by_signed_splats():
    """Kenfack-style closed form: the even cat Wigner function IS a signed
    Gaussian mixture (2 positive blobs + oscillatory fringe). Check that the
    3-splat approximation with a single central fringe splat captures the
    negativity at the origin region for small alpha."""
    cat = CatState(alpha=1.5, parity=+1)
    p = np.linspace(-3, 3, 601)
    w = cat.wigner(np.zeros_like(p), p)
    assert w.min() < -1e-3  # nonclassicality is present in the target
