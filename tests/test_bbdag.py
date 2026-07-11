"""Fast, fit-free checks for the rho=BB^dagger reconstructors (issue #8).

Fits take seconds-to-minutes (FD gradients), so they live in experiments/. Here
we pin the closed-form pieces the fits rely on: the displaced-squeezed
wavefunction convention, the closed-form norm, and exact-state fidelity.
"""
import numpy as np

from wigner_splat.bbdag import PureKetState, sq_coherent_wavefunction
from wigner_splat.bbdagM import CoherentKetState, coherent_overlap, fidelity_vs_cat3
from wigner_splat.states import coherent_wavefunction


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


def test_pure_ket_marginal_is_normalized_and_nonnegative():
    st = PureKetState(z=np.array([1.0, 0.7], complex),
                      alpha=np.array([1.2, -0.9], complex),
                      xi=np.array([0.3 + 0.1j, 0.0 + 0.0j], complex))
    xs = np.linspace(-14, 14, 4000)
    p = st.radon(xs, theta=0.4)
    assert np.all(p >= 0.0)                       # physical by construction
    assert abs(np.trapezoid(p, xs) - 1.0) < 1e-6  # normalized
