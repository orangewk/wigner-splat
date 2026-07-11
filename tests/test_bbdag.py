"""Fast, fit-free checks for the rho=BB^dagger reconstructors (issue #8).

Fits take seconds-to-minutes (FD gradients), so they live in experiments/. Here
we pin the closed-form pieces the fits rely on: the displaced-squeezed
wavefunction convention, the closed-form norm, and exact-state fidelity.
"""
import numpy as np
import pytest

from wigner_splat.bbdag import PureKetState, loss, sq_coherent_wavefunction
from wigner_splat.bbdagM import CoherentKetState, coherent_overlap, fidelity_vs_cat3
from wigner_splat.states import coherent_wavefunction
from wigner_splat.states3 import ThreeModeCat


def test_sq_wavefunction_reduces_to_coherent_at_zero_squeeze():
    x = np.linspace(-6, 6, 200)
    for beta in [1.5 + 0j, -0.7 + 1.1j, 0.3 - 0.9j]:
        a = sq_coherent_wavefunction(x, beta, 0.0 + 0.0j)
        b = coherent_wavefunction(x, beta)
        assert np.max(np.abs(a - b)) < 1e-12


def test_closed_form_norm_matches_grid():
    # single-mode two-ket superposition: closed-form Z vs numeric x-integral
    st = CoherentKetState(z=np.array([1.0, 1.0], complex),
                          alpha=np.array([[0.8], [-1.1]], complex))
    xs = np.linspace(-12, 12, 4000)
    psi = coherent_wavefunction(xs, 0.8) + coherent_wavefunction(xs, -1.1)
    Zgrid = np.trapezoid(np.abs(psi) ** 2, xs)
    assert abs(st.norm_sq() - Zgrid) < 1e-9


def test_coherent_overlap_self_is_one():
    a = np.array([0.5 + 0.3j, -1.0 + 0.0j])
    assert np.allclose(coherent_overlap(a, a), 1.0)


def test_exact_cat3_has_unit_fidelity():
    a = 1.5
    for parity in (+1, -1):
        exact = CoherentKetState(
            z=np.array([1.0, parity], complex),
            alpha=np.array([[a, a, a], [-a, -a, -a]], complex),
        )
        assert abs(fidelity_vs_cat3(exact, a, parity) - 1.0) < 1e-10


def test_exact_coherent_ket_state_matches_three_mode_cat_pdf():
    """The BB-dagger amplitude path agrees with the reference-state PDF path."""
    rng = np.random.default_rng(20260711)
    X = rng.normal(size=(32, 3))
    theta = np.array([0.17, 0.83, 2.21])
    alpha = 1.2

    for parity in (+1, -1):
        state = CoherentKetState(
            z=np.array([1.0, parity], complex),
            alpha=np.array(
                [[alpha, alpha, alpha], [-alpha, -alpha, -alpha]], complex
            ),
        )
        actual = np.abs(state.psi_at(X, theta)) ** 2 / state.norm_sq()
        expected = ThreeModeCat(alpha, parity).homodyne_pdf(
            X[:, 0], X[:, 1], X[:, 2], *theta
        )
        assert np.allclose(actual, expected, rtol=2e-13, atol=2e-14)


def test_nonzero_squeeze_quadrature_variance_and_phase_convention():
    """Numerical moments obey the independent squeezed-quadrature formula."""
    r, phi, theta = 0.47, 0.71, 0.38
    alpha = 0.62 + 0.41j
    state = PureKetState(
        z=np.array([1.0 + 0.0j]),
        alpha=np.array([alpha]),
        xi=np.array([r * np.exp(1j * phi)]),
    )
    x = np.linspace(-12.0, 12.0, 20001)
    density = np.abs(state.psi(x, theta)) ** 2
    density /= np.trapezoid(density, x)
    mean = np.trapezoid(x * density, x)
    variance = np.trapezoid((x - mean) ** 2 * density, x)

    expected_mean = np.sqrt(2.0) * np.real(alpha * np.exp(-1j * theta))
    expected_variance = 0.5 * (
        np.cosh(2.0 * r) - np.sinh(2.0 * r) * np.cos(phi - 2.0 * theta)
    )
    assert mean == pytest.approx(expected_mean, abs=2e-10)
    assert variance == pytest.approx(expected_variance, abs=2e-10)


@pytest.mark.parametrize("bad_Z", [0.0, -1.0, np.nan, np.inf])
def test_radon_rejects_nonpositive_or_nonfinite_norm(bad_Z):
    state = PureKetState(
        z=np.array([1.0 + 0.0j]),
        alpha=np.array([0.0 + 0.0j]),
        xi=np.array([0.0 + 0.0j]),
    )
    with pytest.raises(ValueError, match="finite and strictly positive"):
        state.radon(np.array([0.0]), theta=0.0, Z=bad_Z)


def test_loss_rejects_zero_norm_even_without_targets():
    zero_state = PureKetState(
        z=np.array([0.0 + 0.0j]),
        alpha=np.array([0.0 + 0.0j]),
        xi=np.array([0.0 + 0.0j]),
    )
    with pytest.raises(ValueError, match="finite and strictly positive"):
        loss(zero_state, np.array([0.0]), targets=[])


def test_norm_sq_rejects_grid_with_unresolved_tails():
    state = PureKetState(
        z=np.array([1.0 + 0.0j]),
        alpha=np.array([1.2 + 0.0j]),
        xi=np.array([0.0 + 0.0j]),
    )
    with pytest.raises(ValueError, match="truncate wavefunction tails"):
        state.norm_sq(np.linspace(-0.2, 0.2, 101))


def test_norm_sq_rejects_malformed_grids():
    state = PureKetState(
        z=np.array([1.0 + 0.0j]),
        alpha=np.array([0.0 + 0.0j]),
        xi=np.array([0.0 + 0.0j]),
    )
    invalid_grids = [
        np.array([[-1.0, 0.0, 1.0]]),
        np.array([-1.0, np.nan, 1.0]),
        np.array([-1.0, 0.5, 0.0, 1.0]),
    ]
    for grid in invalid_grids:
        with pytest.raises(ValueError, match="norm grid"):
            state.norm_sq(grid)


def test_pure_ket_marginal_is_normalized_and_nonnegative():
    st = PureKetState(z=np.array([1.0, 0.7], complex),
                      alpha=np.array([1.2, -0.9], complex),
                      xi=np.array([0.3 + 0.1j, 0.0 + 0.0j], complex))
    xs = np.linspace(-14, 14, 4000)
    p = st.radon(xs, theta=0.4)
    assert np.all(p >= 0.0)                       # physical by construction
    assert abs(np.trapezoid(p, xs) - 1.0) < 1e-6  # normalized
