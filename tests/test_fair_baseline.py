"""Fit-free checks for the issue #27 fair baseline (pure-state Fock ML).

Pins the pieces the exp09 comparison relies on: the model pdf agrees with the
closed-form reference state, the analytic gradient matches central
differences, and the fidelity conventions (truncated vs exact) are coherent.
"""
import numpy as np
import pytest

from wigner_splat.fock import cat3_fock, cat3_truncation_fidelity
from wigner_splat.purefock3 import (
    _nll_grad_fd, _pack, _unpack, fidelity_vs_cat3, nll_and_grad_psi, nll_psi,
)
from wigner_splat.states3 import ThreeModeCat


def _random_problem(n_max, groups=2, samples=25, seed=20260714):
    rng = np.random.default_rng(seed)
    psi = rng.normal(size=(n_max,) * 3) + 1j * rng.normal(size=(n_max,) * 3)
    data = [
        (rng.uniform(0.0, np.pi, 3), rng.normal(scale=1.4, size=(samples, 3)))
        for _ in range(groups)
    ]
    return psi, data


def test_model_pdf_matches_reference_cat_up_to_truncation():
    """p(x) of the truncated cat ket ~ ThreeModeCat.homodyne_pdf (n_max=14)."""
    alpha, parity, n_max = 1.0, +1, 14
    cat = ThreeModeCat(alpha, parity)
    psi = cat3_fock(alpha, parity, n_max).reshape(n_max, n_max, n_max)
    rng = np.random.default_rng(3)
    X = rng.normal(scale=1.2, size=(64, 3))
    theta = np.array([0.3, 1.1, 2.0])

    from wigner_splat.purefock3 import _amplitudes, _mode_vectors
    v1, v2, v3 = _mode_vectors(X, theta, n_max)
    p_model = np.abs(_amplitudes(psi, v1, v2, v3)) ** 2 / np.sum(np.abs(psi) ** 2)
    p_ref = cat.homodyne_pdf(X[:, 0], X[:, 1], X[:, 2], *theta)
    # truncated-state pdf vs exact-state pdf: agree to truncation accuracy
    assert np.allclose(p_model, p_ref, rtol=2e-4, atol=1e-7)


@pytest.mark.parametrize("n_max", [2, 3])
def test_nll_and_grad_value_and_gradient(n_max):
    psi, data = _random_problem(n_max)
    value, g = nll_and_grad_psi(psi, data)
    assert value == pytest.approx(nll_psi(psi, data), rel=1e-12)
    g_fd = _nll_grad_fd(_pack(psi), n_max, data, eps=1e-5)
    scale = np.maximum(np.abs(g_fd), 1e-3 * np.max(np.abs(g_fd)))
    assert np.max(np.abs(g - g_fd) / scale) < 1e-7


def test_pack_unpack_roundtrip():
    psi, _ = _random_problem(3)
    assert np.allclose(_unpack(_pack(psi), 3), psi)


def test_fidelity_conventions():
    alpha, parity, n_max = 1.5, +1, 8
    psi = cat3_fock(alpha, parity, n_max).reshape(n_max, n_max, n_max)
    f_trunc, f_exact = fidelity_vs_cat3(psi, alpha, parity)
    assert f_trunc == pytest.approx(1.0, abs=1e-12)
    assert f_exact == pytest.approx(
        cat3_truncation_fidelity(alpha, parity, n_max), abs=1e-12
    )
    # scaling psi must not change either fidelity
    f2_trunc, f2_exact = fidelity_vs_cat3(3.7 * psi, alpha, parity)
    assert f2_trunc == pytest.approx(f_trunc, rel=1e-12)
    assert f2_exact == pytest.approx(f_exact, rel=1e-12)
