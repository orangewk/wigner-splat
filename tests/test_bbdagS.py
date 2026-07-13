"""Fit-free checks for the multimode squeezed-product BB-dagger (issue #28).

Pins: reduction to the coherent ansatz at xi = 0, agreement with the tested
1-mode displaced-squeezed wavefunction, the closed-form Gram (norm) against
numeric quadrature, the analytic NLL gradient against central differences
(including through the xi = 0 singularity-free parameterization), and the
exact representation of the squeezed cat (F = 1).
"""
import numpy as np
import pytest

from wigner_splat.bbdag import sq_coherent_wavefunction
from wigner_splat.bbdagM import CoherentKetState, nll as nll_coh
from wigner_splat.bbdagS import (
    SqueezedKetState, _nll_grad_fd, _pack, fidelity_vs_squeezed_cat3,
    nll, nll_and_grad, sq_wavefunction,
)
from wigner_splat.states3x import SqueezedThreeModeCat


def _random_problem(K, M, squeeze=0.4, groups=2, samples=30, seed=20260715):
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


def test_wavefunction_matches_bbdag_closed_form():
    x = np.linspace(-6, 6, 301)
    for beta, zeta in [(1.2 - 0.7j, 0.5 + 0.3j), (-0.4 + 0.9j, 0.0j),
                       (0.3 + 0.1j, -0.6j)]:
        assert np.max(np.abs(
            sq_wavefunction(x, beta, zeta) - sq_coherent_wavefunction(x, beta, zeta)
        )) < 1e-12


def test_reduces_to_coherent_state_at_zero_squeeze():
    rng = np.random.default_rng(3)
    K, M = 3, 2
    z = rng.normal(size=K) + 1j * rng.normal(size=K)
    alpha = rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M))
    sq = SqueezedKetState(z, alpha, np.zeros((K, M), complex))
    coh = CoherentKetState(z, alpha)
    assert sq.norm_sq() == pytest.approx(coh.norm_sq(), rel=1e-12)
    X = rng.normal(size=(40, M))
    theta = rng.uniform(0, np.pi, M)
    assert np.allclose(sq.psi_at(X, theta), coh.psi_at(X, theta), rtol=1e-12)
    data = [(theta, X)]
    assert nll(sq, data) == pytest.approx(nll_coh(coh, data), rel=1e-12)


def test_closed_form_norm_matches_quadrature():
    state, _ = _random_problem(K=2, M=1, squeeze=0.5)
    xs = np.linspace(-14, 14, 8001)
    psi = np.zeros_like(xs, complex)
    for c in range(state.K):
        psi += state.z[c] * sq_wavefunction(xs, state.alpha[c, 0], state.xi[c, 0])
    Zgrid = np.trapezoid(np.abs(psi) ** 2, xs)
    assert state.norm_sq() == pytest.approx(float(Zgrid), rel=1e-9)


@pytest.mark.parametrize("K,M,squeeze", [(1, 1, 0.5), (2, 2, 0.4), (3, 3, 0.3),
                                         (2, 2, 0.0)])
def test_nll_analytic_grad_matches_central_difference(K, M, squeeze):
    state, data = _random_problem(K, M, squeeze=squeeze)
    value, g = nll_and_grad(state, data)
    assert value == pytest.approx(nll(state, data), rel=1e-12)
    g_fd = _nll_grad_fd(_pack(state), K, M, data, eps=1e-5)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 2e-7


def test_exact_squeezed_cat_has_unit_fidelity():
    a, r = 1.5, 0.4
    for parity in (+1, -1):
        exact = SqueezedKetState(
            z=np.array([1.0, parity], complex),
            alpha=np.array([[a] * 3, [-a] * 3], complex),
            xi=np.full((2, 3), complex(r)),
        )
        F = fidelity_vs_squeezed_cat3(exact, a, parity, r=r)
        assert F == pytest.approx(1.0, abs=1e-10)


def test_fidelity_agrees_with_reference_pdf_path():
    """The ansatz pdf equals SqueezedThreeModeCat.homodyne_pdf for the exact ket."""
    a, r, parity = 1.5, 0.4, +1
    exact = SqueezedKetState(
        z=np.array([1.0, parity], complex),
        alpha=np.array([[a] * 3, [-a] * 3], complex),
        xi=np.full((2, 3), complex(r)),
    )
    target = SqueezedThreeModeCat(a, parity, r=r)
    rng = np.random.default_rng(8)
    X = rng.normal(scale=1.3, size=(48, 3))
    theta = np.array([0.3, 1.4, 2.2])
    p_model = np.abs(exact.psi_at(X, theta)) ** 2 / exact.norm_sq()
    p_ref = target.homodyne_pdf(X[:, 0], X[:, 1], X[:, 2], *theta)
    assert np.allclose(p_model, p_ref, rtol=1e-8, atol=1e-12)
    # and the closed-form target norm agrees with the quadrature-based one
    assert exact.norm_sq() == pytest.approx(target.norm, rel=1e-8)


def test_zero_squeeze_fidelity_matches_coherent_convention():
    from wigner_splat.bbdagM import fidelity_vs_cat3 as fid_coh
    rng = np.random.default_rng(4)
    K, M = 3, 3
    z = rng.normal(size=K) + 1j * rng.normal(size=K)
    alpha = rng.normal(size=(K, M)) + 1j * rng.normal(size=(K, M))
    sq = SqueezedKetState(z, alpha, np.zeros((K, M), complex))
    coh = CoherentKetState(z, alpha)
    assert fidelity_vs_squeezed_cat3(sq, 1.5, +1, r=0.0) == pytest.approx(
        fid_coh(coh, 1.5, +1), rel=1e-10
    )
