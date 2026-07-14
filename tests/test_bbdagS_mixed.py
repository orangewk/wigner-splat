"""Checks for the rank-R x squeezed x loss model (issue #40).

Pins: exact reduction to the rank-1 lossy machinery at R = 1 (value and
gradient), the closed-form lossy pdf against a numerical convolution of the
pure mixed pdf, the mixed pdf against the Fock-basis loss channel through an
exact rank-2 B B^dagger factorization of the lossy cat, normalization, the
analytic gradient against central differences, and parameter validation.
"""
import numpy as np
import pytest

from wigner_splat.bbdagS import (
    MixedSqueezedKetState, SqueezedKetState, _pack_mixed, _unpack_mixed,
    fit_bbdagS_lossy_mixed, lossy_pdf_mixed, nll_and_grad_lossy,
    nll_and_grad_lossy_mixed, nll_lossy, nll_lossy_mixed, nll_mixed,
)
from wigner_splat.fock import _coherent_coeffs, marginal_from_rho

from tests.test_bbdagS_lossy import _lossy_cat_fock_rho


def _random_problem(R, K, M, squeeze=0.3, groups=2, samples=25,
                    seed=20260714):
    rng = np.random.default_rng(seed)
    state = MixedSqueezedKetState(
        z=rng.normal(size=(R, K)) + 1j * rng.normal(size=(R, K)),
        alpha=rng.normal(size=(R, K, M)) + 1j * rng.normal(size=(R, K, M)),
        xi=squeeze * (rng.normal(size=(R, K, M))
                      + 1j * rng.normal(size=(R, K, M))),
    )
    data = [
        (rng.uniform(0.0, np.pi, M), rng.normal(scale=1.5, size=(samples, M)))
        for _ in range(groups)
    ]
    return state, data


def test_rank1_reduces_to_lossy_rank1_exactly():
    st, data = _random_problem(R=1, K=3, M=2)
    flat = SqueezedKetState(st.z[0], st.alpha[0], st.xi[0])
    eta = 0.75
    assert nll_lossy_mixed(st, data, eta) == pytest.approx(
        nll_lossy(flat, data, eta), rel=1e-12
    )
    v0, g0 = nll_and_grad_lossy(flat, data, eta)
    v1, g1 = nll_and_grad_lossy_mixed(st, data, eta)
    assert v1 == pytest.approx(v0, rel=1e-12)
    assert np.allclose(g1, g0, rtol=1e-10)


@pytest.mark.parametrize("eta,extra_var", [(0.7, 0.0), (1.0, 0.05)])
def test_mixed_lossy_pdf_matches_numerical_convolution(eta, extra_var):
    st, _ = _random_problem(R=2, K=2, M=1, squeeze=0.4)
    theta = np.array([0.9])
    ys = np.linspace(-16, 16, 12001)
    Z = st.norm_sq()
    p_pure = sum(
        np.abs(c.psi_at(ys[:, None], theta)) ** 2 for c in st.columns()
    ) / Z
    sigma2 = (1.0 - eta) / 2.0 + extra_var
    xs = np.linspace(-4, 4, 41)
    kern = np.exp(-(xs[:, None] - np.sqrt(eta) * ys[None, :]) ** 2
                  / (2 * sigma2))
    kern /= np.sqrt(2 * np.pi * sigma2)
    p_num = np.trapezoid(kern * p_pure[None, :], ys, axis=1)
    p_cf = lossy_pdf_mixed(st, xs[:, None], theta, eta, extra_var)
    assert np.allclose(p_cf, p_num, rtol=1e-7, atol=1e-12)


def test_exact_rank2_factorization_matches_fock_loss_channel():
    """The lossy cat is exactly rank 2: B = [A' + cB', sqrt(1-c^2) B'] gives
    rho = B B^dagger / norm with the fock-route density. The mixed model
    evaluated at eta = 1 (columns already post-loss) must match."""
    a, parity, eta = 1.5, +1, 0.75
    a_out = np.sqrt(eta) * a
    c = parity * np.exp(-2.0 * a ** 2 * (1.0 - eta))
    norm = 2.0 * (1.0 + parity * np.exp(-2.0 * a ** 2))
    st = MixedSqueezedKetState(
        z=np.array([[1.0, c], [0.0, np.sqrt(1.0 - c ** 2)]],
                   complex) / np.sqrt(norm),
        alpha=np.array([[[a_out], [-a_out]]] * 2, complex),
        xi=np.zeros((2, 2, 1), complex),
    )
    rho = _lossy_cat_fock_rho(a, parity, eta)
    xs = np.linspace(-4.5, 4.5, 61)
    for th in (0.0, 0.6, 1.4):
        p_cf = lossy_pdf_mixed(st, xs[:, None], np.array([th]), eta=1.0)
        p_fock = marginal_from_rho(rho, xs, th)
        assert np.allclose(p_cf, p_fock, rtol=1e-8, atol=1e-10)
    # trace check: the truncated-basis trace of rho is ~1, and our Z-based
    # normalization must integrate to 1 as well
    p = lossy_pdf_mixed(st, np.linspace(-18, 18, 12001)[:, None],
                        np.array([0.3]), eta=1.0)
    assert np.trapezoid(p, np.linspace(-18, 18, 12001)) == pytest.approx(
        1.0, abs=1e-8)


def test_mixed_lossy_pdf_normalizes():
    st, _ = _random_problem(R=3, K=2, M=1, squeeze=0.4)
    xs = np.linspace(-18, 18, 12001)
    p = lossy_pdf_mixed(st, xs[:, None], np.array([0.7]), eta=0.7)
    assert np.trapezoid(p, xs) == pytest.approx(1.0, abs=1e-8)


@pytest.mark.parametrize("R,K,M,squeeze", [(2, 1, 1, 0.4), (2, 2, 2, 0.3),
                                           (3, 2, 1, 0.0)])
def test_mixed_lossy_grad_matches_central_difference(R, K, M, squeeze):
    st, data = _random_problem(R, K, M, squeeze=squeeze)
    eta = 0.75
    value, g = nll_and_grad_lossy_mixed(st, data, eta)
    assert value == pytest.approx(nll_lossy_mixed(st, data, eta), rel=1e-12)
    v0 = _pack_mixed(st)
    g_fd = np.zeros_like(v0)
    eps = 1e-5
    for i in range(len(v0)):
        vp = v0.copy(); vp[i] += eps
        vm = v0.copy(); vm[i] -= eps
        g_fd[i] = (
            nll_lossy_mixed(_unpack_mixed(vp, R, K, M), data, eta)
            - nll_lossy_mixed(_unpack_mixed(vm, R, K, M), data, eta)
        ) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 2e-7


def test_mixed_validation_and_pure_grad_refusal():
    st, data = _random_problem(R=2, K=1, M=1)
    with pytest.raises(ValueError):
        nll_lossy_mixed(st, data, eta=1.2)
    with pytest.raises(NotImplementedError):
        nll_and_grad_lossy_mixed(st, data, eta=1.0)
    with pytest.raises(ValueError):
        fit_bbdagS_lossy_mixed(data, R=2, K=1, M=1, eta0=1.0, iters=1)


def test_fit_smoke_runs_and_improves():
    rng = np.random.default_rng(5)
    data = [(np.array([th]), rng.normal(loc=mu, scale=0.9, size=(400, 1)))
            for th, mu in ((0.0, 1.0), (1.2, -0.5))]
    st0 = MixedSqueezedKetState.random_init(2, 2, 1, rng=0)
    before = nll_lossy_mixed(st0, data, 0.8)
    st, eta = fit_bbdagS_lossy_mixed(data, R=2, K=2, M=1, eta0=0.8,
                                     iters=60, lr=0.08, seed=0)
    assert 0.0 < eta < 1.0
    assert nll_lossy_mixed(st, data, eta) < before
    # pure-detection evaluation path also runs on the fitted state
    assert np.isfinite(nll_mixed(st, data))
