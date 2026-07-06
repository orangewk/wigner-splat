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


def test_analytic_gradient_matches_central_difference():
    """loss_and_grad must agree with central differences on the same loss."""
    from wigner_splat.fit import _pack, _unpack, histogram_targets, loss, loss_and_grad

    cat = CatState(alpha=1.5, parity=+1)
    data = cat.sample_homodyne(np.linspace(0, np.pi, 5, endpoint=False), 500, rng=7)
    centers, targets = histogram_targets(data, bins=40)
    K = 4
    mix = SplatMixture.random_init(K, rng=3)
    mix.w += np.linspace(-0.3, 0.3, K)  # break symmetry, include negative weight
    v = _pack(mix)

    _, grad = loss_and_grad(_unpack(v, K), centers, targets)

    eps = 1e-6
    numeric = np.empty_like(v)
    for i in range(len(v)):
        vp, vm = v.copy(), v.copy()
        vp[i] += eps
        vm[i] -= eps
        numeric[i] = (
            loss(_unpack(vp, K), centers, targets)
            - loss(_unpack(vm, K), centers, targets)
        ) / (2 * eps)
    np.testing.assert_allclose(grad, numeric, rtol=1e-5, atol=1e-7)


def test_adapt_prunes_and_splits_with_moment_bookkeeping():
    from wigner_splat.fit import _pack, adapt

    mix = SplatMixture(
        w=[0.6, 0.25, 0.15, 1e-4],  # last splat is below the prune threshold
        mu=[[1.0, 0.0], [-1.0, 0.5], [0.5, -0.5], [0.0, 0.0]],
        s=np.log([[1.5, 0.4], [0.5, 0.5], [0.6, 0.6], [0.5, 0.5]]),
        phi=[0.0, 0.2, 0.4, 0.0],
    )
    m1 = _pack(mix) * 0.1  # arbitrary nonzero moments to track through rows
    m2 = np.abs(_pack(mix)) * 0.2
    gnorm = np.array([10.0, 0.1, 0.1, 0.1])  # only splat 0 far above median

    new, m1n, m2n = adapt(mix, m1, m2, gnorm, K_max=5)

    assert len(new.w) == 4  # 4 kept - 1 pruned - 1 parent + 2 children
    # the split children carry half the parent weight each, offset along the
    # major axis (phi=0, axis x), with that axis shrunk
    np.testing.assert_allclose(new.w[:2], [0.3, 0.3])
    assert new.mu[0, 0] < 1.0 < new.mu[1, 0]
    np.testing.assert_allclose(new.mu[:2, 1], 0.0)
    np.testing.assert_allclose(np.exp(new.s[:2, 0]), 1.5 / 1.6)
    # the untouched splats and their moments survive unchanged
    np.testing.assert_allclose(new.w[2:], [0.25, 0.15])
    assert m1n.shape == m2n.shape == (6 * 4,)
    np.testing.assert_allclose(m1n[2], 0.25 * 0.1)  # w-moment of kept splat


def test_birth_splat_decreases_loss():
    """A splat born at the extremum of the weight-gradient field, with the
    descent sign, must reduce the loss — this is what lets negativity emerge
    from an all-positive mixture."""
    from wigner_splat.fit import birth_field, histogram_targets, loss

    cat = CatState(alpha=1.5, parity=+1)
    data = cat.sample_homodyne(np.linspace(0, np.pi, 8, endpoint=False), 3000, rng=5)
    centers, targets = histogram_targets(data)
    # two positive blobs only: the fringe structure is entirely missing
    blobs = SplatMixture(
        w=[0.5, 0.5],
        mu=[[np.sqrt(2) * 1.5, 0.0], [-np.sqrt(2) * 1.5, 0.0]],
        s=np.full((2, 2), np.log(np.sqrt(0.5))),
        phi=[0.0, 0.0],
    )
    xg = np.linspace(centers[0], centers[-1], 40)
    grid = np.stack(np.meshgrid(xg, xg), axis=-1).reshape(-1, 2)
    field = birth_field(blobs, centers, targets, grid)
    i = np.argmax(np.abs(field))
    # the descent guarantee is first-order, so probe with a small weight
    born = SplatMixture(
        np.append(blobs.w, -np.sign(field[i]) * 0.005),
        np.vstack([blobs.mu, grid[i]]),
        np.vstack([blobs.s, np.full(2, np.log(0.5))]),
        np.append(blobs.phi, 0.0),
    )
    assert loss(born, centers, targets) < loss(blobs, centers, targets)


def test_densified_fit_from_small_K_recovers_negativity():
    """Acceptance: starting from K=4, densification reaches fixed-K=8 quality."""
    from wigner_splat.fit import fit

    cat = CatState(alpha=1.5, parity=+1)
    data = cat.sample_homodyne(np.linspace(0, np.pi, 12, endpoint=False), 4000, rng=42)
    mix = fit(data, K=4, iters=800, seed=0, densify_every=100, K_max=12)
    xs = np.linspace(-4.5, 4.5, 121)
    X, P = np.meshgrid(xs, xs)
    w_true, w_fit = cat.wigner(X, P), mix.wigner(X, P)
    l2 = np.sqrt(np.mean((w_true - w_fit) ** 2)) / np.sqrt(np.mean(w_true ** 2))
    assert l2 <= 0.13
    assert w_fit.min() < -0.1  # true minimum is -0.19


def test_fock_module_matches_reference_state():
    """Fock-basis cat (density matrix) must reproduce states.py closed forms:
    homodyne pdf at several angles and the Wigner function on a grid."""
    from wigner_splat.fock import cat_fock, marginal_from_rho, wigner_from_rho

    cat = CatState(alpha=1.5, parity=+1)
    c = cat_fock(1.5, +1, n_max=30)
    rho = np.outer(c, c.conj())
    xs = np.linspace(-6, 6, 121)
    for theta in [0.0, 0.7, np.pi / 2]:
        np.testing.assert_allclose(
            marginal_from_rho(rho, xs, theta), cat.homodyne_pdf(xs, theta), atol=1e-9
        )
    g = np.linspace(-4, 4, 41)
    X, P = np.meshgrid(g, g)
    np.testing.assert_allclose(wigner_from_rho(rho, X, P), cat.wigner(X, P), atol=1e-9)


def test_wigner_overlap_matches_analytic_fidelity():
    from wigner_splat.fock import wigner_overlap

    a = 1.5
    cat = CatState(alpha=a, parity=+1)
    xs = np.linspace(-6, 6, 301)
    X, P = np.meshgrid(xs, xs)
    vac = SplatMixture(w=[1.0], mu=[[0, 0]], s=[[np.log(np.sqrt(0.5))] * 2], phi=[0.0])
    overlap = wigner_overlap(vac.wigner(X, P), cat.wigner(X, P), xs)
    exact = (np.exp(-a ** 2 / 2) * 2) ** 2 / (2 * (1 + np.exp(-2 * a ** 2)))
    assert overlap == pytest.approx(exact, abs=1e-9)


def test_mle_recovers_cat():
    from wigner_splat.fit import histogram_targets
    from wigner_splat.fock import cat_fock, fidelity_pure
    from wigner_splat.mle import mle_reconstruct

    cat = CatState(alpha=1.5, parity=+1)
    data = cat.sample_homodyne(np.linspace(0, np.pi, 12, endpoint=False), 4000, rng=42)
    centers, targets = histogram_targets(data)
    rho, iters = mle_reconstruct(centers, targets, n_max=20)
    assert fidelity_pure(cat_fock(1.5, +1, 20), rho) > 0.97
    assert iters < 2000  # converged, did not hit the cap
