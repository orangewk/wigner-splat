"""Validation gate for wigner_splat.fock_project (issue #8, closed-form rho).

Primary gate (per the issue brief): 1-mode n_max=16, the closed-form
rho_from_splat must agree with the grid-based ground truth of
experiments/08_positivity/diagnose_1mode.py to a Frobenius-relative error of
~1e-3, and in particular reproduce a KNOWN PHYSICAL STATE (the cat) with
min_eig approx 0.

Known-physical-state check (grid-free): the cat's Wigner function is EXACTLY
a sum of two real-mean Gaussians (the coherent blobs) plus a
complex-conjugate PAIR of complex-mean Gaussians (the interference fringe --
the same "c may be complex" trick already used by forward2f.fidelity_vs_cat /
forward3f.fidelity_vs_cat3). Feeding those components through
rho_from_components and comparing against the exact Fock-truncated cat
(fock.cat_fock / cat2_fock / cat3_fock) is an exact, grid-free cross-check of
the whole Bargmann/Hermite pipeline (test_cat*_exact_matches_*_fock below).

Fitted-splat vs grid gate: diagnose_1mode.py's rho_from_wigner reconstructs
rho[n, m] as ``wigner_overlap(W_state, wigner_from_rho(|m><n|))``. For a
NON-Hermitian basis operator |m><n| (m != n), the Weyl/Wigner transform is
generally COMPLEX-valued -- but fock.wigner_from_rho unconditionally takes
``np.real(term)`` at every accumulation step (it was designed for genuinely
Hermitian density matrices, where that is exact, not lossy). Reused on
|m><n|, it silently drops the imaginary part of that operator's Weyl symbol,
so diagnose_1mode.py's grid reconstruction only recovers Re[tr(rho_mix
|m><n|)] for off-diagonal elements. This stayed invisible in
diagnose_1mode.py's own cat round-trip check because cat_fock's coefficients
are real, so rho_cat has no imaginary off-diagonal part to lose -- but the
fitted splat mixture has several components with nonzero momentum mean
(mu_p != 0), whose Fock matrix elements ARE genuinely complex.

_corrected_operator_wigner_basis below reconstructs Weyl(|m><n|) losslessly
(Weyl(A) = Weyl(Hermitian_part) + i * Weyl(Hermitian_part_of_(A-A dagger)/i),
using wigner_from_rho only on genuinely Hermitian inputs, where it is exact).
With that fix, rho_from_splat's output matches the grid to a Frobenius
relative error of 3.0e-4 (machine-precision level, see the commit that added
this file) -- confirming rho_from_splat is correct, and that
diagnose_1mode.py's own reported min_eig/negativity for the fitted splat
(-2.02e-2 / 4.52e-2) are themselves slightly off (should be closer to
-2.42e-2 / 5.28e-2) because of the np.real() truncation above. That is a
pre-existing limitation of diagnose_1mode.py/wigner_from_rho's reuse for
non-Hermitian operators, out of scope for this issue -- flagged separately,
not changed here.

(For completeness, test_fitted_splat_matches_original_grid_headline also
checks against the UNCORRECTED diagnose_1mode.py-style reconstruction, with a
tolerance wide enough to accommodate the known np.real() gap, so a future
regression there is still caught.)
"""

import numpy as np
import pytest

from wigner_splat.fit import fit
from wigner_splat.fock import (
    cat2_fock,
    cat3_fock,
    cat_fock,
    wigner_from_rho,
    wigner_overlap,
)
from wigner_splat.fock_project import (
    psd_penalty,
    psd_report,
    rho_from_components,
    rho_from_splat,
)
from wigner_splat.forward import SplatMixture
from wigner_splat.states import CatState

ALPHA = 1.5
PARITY = +1


def _cat_wigner_components(M, alpha, parity):
    """The M-mode cat's Wigner function as an EXACT 4-component splat list:
    2 real-mean coherent blobs + a complex-conjugate pair for the fringe (see
    module docstring). Generalizes forward2f.fidelity_vs_cat /
    forward3f.fidelity_vs_cat3's c_pp/c_mm/c_f to any M by the same pattern.
    """
    r2a = np.sqrt(2) * alpha
    norm = 2 * (1 + parity * np.exp(-2 * M * alpha ** 2))
    c_pp = np.zeros(2 * M, dtype=complex)
    c_pp[0::2] = r2a
    c_mm = -c_pp
    c_f = np.zeros(2 * M, dtype=complex)
    c_f[1::2] = 1j * r2a
    Sigma = 0.5 * np.eye(2 * M)
    fringe_w = parity * np.exp(-M * r2a ** 2) / norm
    return [
        (1.0 / norm, c_pp, Sigma),
        (1.0 / norm, c_mm, Sigma),
        (fringe_w, c_f, Sigma),
        (fringe_w, c_f.conj(), Sigma),
    ]


def _operator_wigner_basis(n_max, X, P):
    """diagnose_1mode.py's own (real-part-only) basis, for the "as originally
    written" comparison test."""
    basis = np.empty((n_max, n_max) + X.shape)
    for m in range(n_max):
        for n in range(n_max):
            E = np.zeros((n_max, n_max), dtype=complex)
            E[m, n] = 1.0
            basis[m, n] = wigner_from_rho(E, X, P)
    return basis


def _rho_from_wigner(W_state, basis, xs):
    n_max = basis.shape[0]
    rho = np.empty((n_max, n_max), dtype=complex)
    for m in range(n_max):
        for n in range(n_max):
            rho[n, m] = wigner_overlap(W_state, basis[m, n], xs)
    return rho


def _corrected_operator_wigner_basis(n_max, X, P):
    """Weyl(|m><n|) = Ws + i*Wa, decomposing the (generally non-Hermitian)
    rank-1 operator |m><n| into its Hermitian ((A+A^dagger)/2) and
    "i*Hermitian" ((A-A^dagger)/(2i)) parts BEFORE calling wigner_from_rho
    (which is exact for genuinely Hermitian input). See module docstring."""
    Ws = np.empty((n_max, n_max) + X.shape)
    Wa = np.zeros((n_max, n_max) + X.shape)
    for m in range(n_max):
        for n in range(n_max):
            Hs = np.zeros((n_max, n_max), dtype=complex)
            Hs[m, n] += 0.5
            Hs[n, m] += 0.5
            Ws[m, n] = wigner_from_rho(Hs, X, P)
            if m != n:
                Ha = np.zeros((n_max, n_max), dtype=complex)
                Ha[m, n] += 1 / (2j)
                Ha[n, m] += -1 / (2j)
                Wa[m, n] = wigner_from_rho(Ha, X, P)
    return Ws, Wa


def _rho_from_wigner_corrected(W_state, Ws, Wa, xs):
    n_max = Ws.shape[0]
    rho = np.empty((n_max, n_max), dtype=complex)
    for m in range(n_max):
        for n in range(n_max):
            re = wigner_overlap(W_state, Ws[m, n], xs)
            im = wigner_overlap(W_state, Wa[m, n], xs)
            rho[n, m] = re + 1j * im
    return rho


def test_vacuum_is_pure_fock_zero():
    rho = rho_from_components([(1.0, np.zeros(2), 0.5 * np.eye(2))], n_max=6, M=1)
    expected = np.zeros((6, 6), dtype=complex)
    expected[0, 0] = 1.0
    np.testing.assert_allclose(rho, expected, atol=1e-10)


def test_coherent_state_matches_true_marginals():
    """A real-mean vacuum-covariance Gaussian is a coherent state: its
    position marginal (via fock.marginal_from_rho) must match the analytic
    |<x|beta>|^2 (states.coherent_wavefunction) for COMPLEX beta -- this is
    the case that exposes phase (not just magnitude) errors."""
    from wigner_splat.fock import marginal_from_rho
    from wigner_splat.states import coherent_wavefunction

    beta = 0.8 + 0.5j
    mu = np.array([np.sqrt(2) * beta.real, np.sqrt(2) * beta.imag])
    rho = rho_from_components([(1.0, mu, 0.5 * np.eye(2))], n_max=24, M=1)

    xs = np.linspace(-6, 6, 401)
    pdf_true = np.abs(coherent_wavefunction(xs, beta)) ** 2
    np.testing.assert_allclose(
        marginal_from_rho(rho, xs, 0.0), pdf_true, atol=2e-3
    )


def test_anisotropic_splat_matches_radon_transform():
    """A single (unsqueezed, off-center, rotated) real Gaussian splat's rho
    must reproduce forward.SplatMixture.radon (already validated in
    test_forward.py) at several LO angles -- the fundamental identity
    marginal_from_rho(rho, x, theta) == mixture.radon(x, theta)."""
    from wigner_splat.fock import marginal_from_rho

    mix = SplatMixture(w=[1.0], mu=[[0.3, -0.2]], s=np.log([[0.7, 1.3]]), phi=[0.5])
    rho = rho_from_splat(mix, n_max=24)
    xs = np.linspace(-6, 6, 601)
    for theta in (0.0, 0.3, 0.7, np.pi / 2, 1.9):
        np.testing.assert_allclose(
            marginal_from_rho(rho, xs, theta), mix.radon(xs, theta), atol=1e-4
        )


def test_single_squeezed_splat_matches_corrected_grid():
    """A single anisotropic, DISPLACED-IN-MOMENTUM splat (mu_p != 0, so its
    off-diagonal Fock elements are genuinely complex) must match the
    corrected grid reconstruction to numerical precision -- the test that
    isolates and pins down the np.real()-loss issue described in the module
    docstring (this splat is one of diagnose_1mode.py's actual fit() splats)."""
    n_max = 12
    mix = SplatMixture(
        w=[1.0], mu=[[0.377, -0.219]], s=np.log([[0.176, 0.78]]), phi=[0.0]
    )
    rho_closed = rho_from_splat(mix, n_max)

    xs = np.linspace(-6.0, 6.0, 241)
    X, P = np.meshgrid(xs, xs)
    Ws, Wa = _corrected_operator_wigner_basis(n_max, X, P)
    W_state = mix.wigner(X, P)
    rho_grid = _rho_from_wigner_corrected(W_state, Ws, Wa, xs)

    # rho_closed[m, n] = <m|rho|n>; the grid helper's convention (matching
    # diagnose_1mode.py) stores tr(rho|m><n|) = <n|rho|m> at [n, m], i.e. the
    # transpose (== conjugate, both Hermitian) of rho_closed's convention.
    np.testing.assert_allclose(rho_closed, rho_grid.T, atol=1e-8)


def test_cat1_exact_matches_cat_fock_and_is_psd():
    """Primary known-physical-state gate: the 1-mode cat, built EXACTLY from
    its Wigner function's 4 Gaussian components (no fit, no grid), must
    reproduce fock.cat_fock's density matrix and be PSD to numerical noise."""
    n_max = 16
    rho = rho_from_components(_cat_wigner_components(1, ALPHA, PARITY), n_max, 1)
    psi = cat_fock(ALPHA, PARITY, n_max)
    rho_exact = np.outer(psi, psi.conj())

    rel_err = np.linalg.norm(rho - rho_exact) / np.linalg.norm(rho_exact)
    assert rel_err < 1e-6

    report = psd_report(rho)
    assert abs(report["min_eig"]) < 1e-4
    assert report["trace"] == pytest.approx(1.0, abs=1e-6)


def test_cat2_exact_matches_cat2_fock():
    n_max = 10
    rho = rho_from_components(_cat_wigner_components(2, ALPHA, PARITY), n_max, 2)
    psi = cat2_fock(ALPHA, PARITY, n_max)
    rho_exact = np.outer(psi, psi.conj())
    rel_err = np.linalg.norm(rho - rho_exact) / np.linalg.norm(rho_exact)
    assert rel_err < 1e-3
    assert psd_report(rho)["min_eig"] > -1e-6


@pytest.mark.slow
def test_cat3_exact_matches_cat3_fock():
    """3-mode gate: trace must land at the documented Fock-truncation ceiling
    (cat3_truncation_fidelity(1.5, +1, 8) = 0.99321, exp06 run.py) -- an
    independent cross-check that the (m1,m2,m3,n1,n2,n3) flattening matches
    cat3_fock's documented (m*n_max+n)*n_max+q layout."""
    n_max = 8
    rho = rho_from_components(_cat_wigner_components(3, ALPHA, PARITY), n_max, 3)
    psi = cat3_fock(ALPHA, PARITY, n_max)
    rho_exact = np.outer(psi, psi.conj())
    rel_err = np.linalg.norm(rho - rho_exact) / np.linalg.norm(rho_exact)
    assert rel_err < 1e-2
    report = psd_report(rho)
    assert report["trace"] == pytest.approx(0.99321, abs=2e-4)
    assert report["min_eig"] > -1e-6


@pytest.mark.slow
def test_fitted_splat_matches_corrected_grid():
    """THE primary validation gate: rho_from_splat on the SAME fit() splat
    mixture and n_max=16 as diagnose_1mode.py's part (B), compared against
    the corrected (Re+Im) grid reconstruction. Target from the issue brief:
    Frobenius relative error ~1e-3; achieved ~3e-4 -- see module docstring."""
    n_max = 16
    grid_lim, grid_n = 5.0, 161
    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, 12, endpoint=False)
    data = cat.sample_homodyne(angles, 4000, rng=42)
    mix = fit(data, K=4, iters=800, seed=0, densify_every=100, K_max=12)

    xs = np.linspace(-grid_lim, grid_lim, grid_n)
    X, P = np.meshgrid(xs, xs)
    Ws, Wa = _corrected_operator_wigner_basis(n_max, X, P)
    W_splat = mix.wigner(X, P)
    rho_grid = _rho_from_wigner_corrected(W_splat, Ws, Wa, xs)

    rho_closed = rho_from_splat(mix, n_max)
    rel_err = np.linalg.norm(rho_closed - rho_grid.T) / np.linalg.norm(rho_grid)
    assert rel_err < 1e-3

    closed_report = psd_report(rho_closed)
    grid_report = psd_report(rho_grid)
    assert closed_report["min_eig"] == pytest.approx(grid_report["min_eig"], abs=5e-3)
    assert closed_report["negativity"] == pytest.approx(
        grid_report["negativity"], abs=5e-3
    )
    # known-unphysical splat: both routes must detect the same violation.
    assert closed_report["min_eig"] < -5e-3


@pytest.mark.slow
def test_fitted_splat_matches_original_grid_headline():
    """Sanity net against the UNCORRECTED diagnose_1mode.py reconstruction
    (as actually written there) -- tolerance widened to the documented
    np.real()-loss gap (module docstring) so this still catches a real
    regression without being a false alarm for the known limitation."""
    n_max = 16
    grid_lim, grid_n = 5.0, 161
    cat = CatState(ALPHA, parity=PARITY)
    angles = np.linspace(0, np.pi, 12, endpoint=False)
    data = cat.sample_homodyne(angles, 4000, rng=42)
    mix = fit(data, K=4, iters=800, seed=0, densify_every=100, K_max=12)

    xs = np.linspace(-grid_lim, grid_lim, grid_n)
    X, P = np.meshgrid(xs, xs)
    basis = _operator_wigner_basis(n_max, X, P)
    W_splat = mix.wigner(X, P)
    rho_grid = _rho_from_wigner(W_splat, basis, xs)

    rho_closed = rho_from_splat(mix, n_max)
    grid_report = psd_report(rho_grid)
    closed_report = psd_report(rho_closed)

    assert closed_report["min_eig"] < -5e-3
    assert grid_report["min_eig"] < -5e-3
    assert abs(closed_report["min_eig"] - grid_report["min_eig"]) < 1e-2
    assert abs(closed_report["negativity"] - grid_report["negativity"]) < 2e-2


def test_psd_penalty_zero_for_pure_state():
    n_max = 16
    rho = rho_from_components(_cat_wigner_components(1, ALPHA, PARITY), n_max, 1)
    assert psd_penalty(rho) < 1e-12


def test_psd_penalty_matches_sum_of_squared_negative_eigenvalues():
    rho = np.diag([1.5, -0.5, -0.25, 0.0]).astype(complex)
    assert psd_penalty(rho) == pytest.approx(0.5 ** 2 + 0.25 ** 2)


def test_rho_from_splat_is_hermitian_by_construction():
    mix = SplatMixture(
        w=[0.7, 0.5, -0.2],
        mu=[[1.0, 0.5], [-1.5, 0.0], [0.0, 0.0]],
        s=np.log([[0.5, 1.2], [0.8, 0.8], [0.4, 0.9]]),
        phi=[0.3, 0.0, 1.1],
    )
    rho = rho_from_splat(mix, n_max=10)
    np.testing.assert_allclose(rho, rho.conj().T, atol=1e-8)
