"""Checks for the detection-efficiency (loss) forward model (issue #42).

Pins, in order of independence:
  * eta = 1 delegates exactly to the pure model;
  * the closed-form lossy pdf equals a brute-force numerical convolution of
    the pure pdf with the loss Gaussian (same formula, different route);
  * it equals the homodyne marginal of the LOSS-CHANNEL density matrix built
    in the Fock basis (fully independent route: Kraus algebra vs Gaussian
    integrals);
  * the lossy pdf stays normalized (loss is trace preserving);
  * the analytic lossy NLL gradient matches central differences;
  * fitting samples drawn from a known lossy state recovers eta.
"""
import numpy as np
import pytest

from wigner_splat.bbdagS import (
    SqueezedKetState, _pack, _unpack, fit_bbdagS_lossy, lossy_pdf, nll,
    nll_and_grad, nll_and_grad_lossy, nll_lossy,
)
from wigner_splat.fock import _coherent_coeffs, marginal_from_rho


def _random_problem(K, M, squeeze=0.3, groups=2, samples=25, seed=20260714):
    rng = np.random.default_rng(seed)
    state = SqueezedKetState(
        z=rng.normal(size=K) + 1j * rng.normal(size=K),
        alpha=rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M)),
        xi=squeeze * (rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M))),
    )
    data = [
        (rng.uniform(0.0, np.pi, M), rng.normal(scale=1.5, size=(samples, M)))
        for _ in range(groups)
    ]
    return state, data


def _cat_state(a=1.5, parity=+1):
    return SqueezedKetState(
        z=np.array([1.0, parity], complex),
        alpha=np.array([[a], [-a]], complex),
        xi=np.zeros((2, 1), complex),
    )


def _lossy_cat_fock_rho(a, parity, eta, n_max=35):
    """Single-mode lossy cat, rank 2 on the |+-sqrt(eta) a> span.

    E(|a><b|) = <b|a>^{1-eta} |sqrt(eta)a><sqrt(eta)b| gives cross damping
    e^{-2 a^2 (1-eta)} and norm 2(1 + parity e^{-2 a^2}) -- the single-mode
    analog of fock.lossy_cat3_fock.
    """
    cp = _coherent_coeffs(np.sqrt(eta) * a, n_max)
    cm = cp * (-1.0) ** np.arange(n_max)
    cross = parity * np.exp(-2.0 * a ** 2 * (1.0 - eta))
    norm = 2.0 * (1.0 + parity * np.exp(-2.0 * a ** 2))
    return (
        np.outer(cp, cp) + np.outer(cm, cm)
        + cross * (np.outer(cp, cm) + np.outer(cm, cp))
    ) / norm


def test_eta_one_delegates_to_pure():
    state, data = _random_problem(K=2, M=2)
    assert nll_lossy(state, data, eta=1.0) == pytest.approx(
        nll(state, data), rel=1e-12
    )
    v0, g0 = nll_and_grad(state, data)
    v1, g1 = nll_and_grad_lossy(state, data, eta=1.0)
    assert v1 == pytest.approx(v0, rel=1e-12)
    assert np.allclose(g1, g0, rtol=1e-12)


def test_near_unit_eta_approaches_pure():
    state, data = _random_problem(K=2, M=1)
    assert nll_lossy(state, data, eta=1.0 - 1e-6) == pytest.approx(
        nll(state, data), abs=1e-3
    )


@pytest.mark.parametrize("eta,extra_var", [(0.7, 0.0), (0.9, 0.0), (1.0, 0.05)])
def test_lossy_pdf_matches_numerical_convolution(eta, extra_var):
    state, _ = _random_problem(K=2, M=1, squeeze=0.4)
    theta = np.array([0.7])
    ys = np.linspace(-16, 16, 12001)
    p_pure = np.abs(state.psi_at(ys[:, None], theta)) ** 2 / state.norm_sq()
    sigma2 = (1.0 - eta) / 2.0 + extra_var
    xs = np.linspace(-4, 4, 41)
    kern = np.exp(-(xs[:, None] - np.sqrt(eta) * ys[None, :]) ** 2 / (2 * sigma2))
    kern /= np.sqrt(2 * np.pi * sigma2)
    p_num = np.trapezoid(kern * p_pure[None, :], ys, axis=1)
    p_cf = lossy_pdf(state, xs[:, None], theta, eta, extra_var)
    assert np.allclose(p_cf, p_num, rtol=1e-7, atol=1e-12)


def test_lossy_pdf_matches_fock_loss_channel():
    a, parity, eta = 1.5, +1, 0.75
    state = _cat_state(a, parity)
    rho = _lossy_cat_fock_rho(a, parity, eta)
    xs = np.linspace(-4.5, 4.5, 61)
    for th in (0.0, 0.5, 1.3):
        p_cf = lossy_pdf(state, xs[:, None], np.array([th]), eta)
        p_fock = marginal_from_rho(rho, xs, th)
        assert np.allclose(p_cf, p_fock, rtol=1e-8, atol=1e-10)


def test_lossy_pdf_normalizes():
    state, _ = _random_problem(K=3, M=1, squeeze=0.4)
    xs = np.linspace(-18, 18, 12001)
    for th in (0.0, 1.1):
        p = lossy_pdf(state, xs[:, None], np.array([th]), eta=0.7)
        assert np.trapezoid(p, xs) == pytest.approx(1.0, abs=1e-8)


@pytest.mark.parametrize("K,M,squeeze", [(1, 1, 0.4), (2, 2, 0.3), (2, 2, 0.0)])
def test_lossy_grad_matches_central_difference(K, M, squeeze):
    state, data = _random_problem(K, M, squeeze=squeeze)
    eta = 0.75
    value, g = nll_and_grad_lossy(state, data, eta)
    assert value == pytest.approx(nll_lossy(state, data, eta), rel=1e-12)
    v0 = _pack(state)
    g_fd = np.zeros_like(v0)
    eps = 1e-5
    for i in range(len(v0)):
        vp = v0.copy(); vp[i] += eps
        vm = v0.copy(); vm[i] -= eps
        g_fd[i] = (
            nll_lossy(_unpack(vp, K, M), data, eta)
            - nll_lossy(_unpack(vm, K, M), data, eta)
        ) / (2 * eps)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 2e-7


def test_loss_params_are_validated():
    state, data = _random_problem(K=1, M=1)
    xs = np.linspace(-1, 1, 5)[:, None]
    th = np.array([0.0])
    for bad_eta in (1.2, -0.1):
        with pytest.raises(ValueError):
            lossy_pdf(state, xs, th, eta=bad_eta)
        with pytest.raises(ValueError):
            nll_and_grad_lossy(state, data, eta=bad_eta)
    with pytest.raises(ValueError):
        lossy_pdf(state, xs, th, eta=0.8, extra_noise_var=-0.1)
    for bad_eta0 in (0.0, 1.0, 1.3):
        with pytest.raises(ValueError):
            fit_bbdagS_lossy(data, K=1, M=1, eta0=bad_eta0, iters=1)


@pytest.mark.slow
def test_fit_recovers_eta_on_lossy_cat_samples():
    """Samples drawn from the Fock-route lossy-cat pdf; fit must find eta."""
    a, parity, eta_true = 1.5, +1, 0.8
    rho = _lossy_cat_fock_rho(a, parity, eta_true)
    rng = np.random.default_rng(11)
    xs = np.linspace(-6, 6, 2001)
    data = []
    for th in (0.0, np.pi / 3, 2 * np.pi / 3):
        p = np.maximum(marginal_from_rho(rho, xs, th), 0.0)
        cdf = np.cumsum(p)
        cdf /= cdf[-1]
        u = rng.uniform(size=3000)
        samples = np.interp(u, cdf, xs)
        data.append((np.array([th]), samples[:, None]))
    st, eta_fit = fit_bbdagS_lossy(data, K=2, M=1, eta0=0.6, iters=600,
                                   lr=0.08, seed=0)
    assert abs(eta_fit - eta_true) < 0.06
    # and the fit must reach the true model's own NLL on these samples
    nll_true = -np.mean([
        np.log(np.maximum(marginal_from_rho(rho, x[:, 0], th[0]), 1e-300))
        for th, x in data
    ])
    assert nll_lossy(st, data, eta_fit) < nll_true + 0.01
