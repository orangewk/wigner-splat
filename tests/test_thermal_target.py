"""Physical-consistency checks for the thermal-noise lossy cat (issue #38).

The held-out full-rank target for the blind-generalization gate. Pins, in
order of independence:
  * sigma_add = 0 reduces exactly to LossyThreeModeCat (pdf and sampler);
  * the closed-form pdf equals a brute-force per-mode numerical convolution
    of the lossy pdf;
  * the pdf is normalized and nonnegative;
  * the Fock-route construction (displacement-quadrature noise channel on
    lossy_cat3_fock) agrees with the closed-form pdf at a truncation-safe
    amplitude -- Kraus/displacement algebra vs Gaussian integrals;
  * the noise channel preserves the trace, is the identity at sigma = 0,
    and its 1-mode version matches the 1D pdf convolution;
  * the splat overlap score vs the thermal target reduces to the lossy one
    at sigma_add = 0 and agrees with the Fock-projection route.
"""
import numpy as np
import pytest

from wigner_splat.fock import (
    displacement_matrix, gaussian_noise_channel_1mode,
    gaussian_noise_channel_3mode, lossy_cat3_fock, marginal_from_rho,
    thermal_lossy_cat3_fock, _coherent_coeffs,
)
from wigner_splat.forward3f import (
    SplatMixture3F, overlap_vs_lossy_cat3, overlap_vs_thermal_lossy_cat3,
)
from wigner_splat.states3x import LossyThreeModeCat, ThermalLossyThreeModeCat

ALPHA, PARITY, ETA, SIG = 1.5, +1, 0.8, 0.1


def test_sigma_zero_reduces_to_lossy_cat():
    th = ThermalLossyThreeModeCat(ALPHA, PARITY, ETA, sigma_add=0.0)
    lo = LossyThreeModeCat(ALPHA, PARITY, ETA)
    rng = np.random.default_rng(0)
    x = rng.normal(scale=1.5, size=(40, 3))
    angles = (0.3, 1.1, 2.4)
    assert np.allclose(
        th.homodyne_pdf(x[:, 0], x[:, 1], x[:, 2], *angles),
        lo.homodyne_pdf(x[:, 0], x[:, 1], x[:, 2], *angles), rtol=1e-12)


def test_pdf_matches_numerical_convolution():
    """Closed form vs brute-force per-mode convolution of the lossy pdf."""
    th = ThermalLossyThreeModeCat(ALPHA, PARITY, ETA, SIG)
    lo = LossyThreeModeCat(ALPHA, PARITY, ETA)
    angles = (0.6, 1.4, 2.9)
    ys = np.linspace(-9, 9, 481)
    x2, x3 = 0.7, -1.3
    # convolve mode 1 only requires convolving ALL modes; do the full 3D
    # convolution on a separable grid for a 1D slice in x1
    Y1, Y2, Y3 = np.meshgrid(ys, ys, ys, indexing="ij", sparse=True)
    p_pure = lo.homodyne_pdf(Y1, Y2, Y3, *angles)
    xs1 = np.linspace(-3, 3, 7)
    k2 = np.exp(-(x2 - ys) ** 2 / (2 * SIG)) / np.sqrt(2 * np.pi * SIG)
    k3 = np.exp(-(x3 - ys) ** 2 / (2 * SIG)) / np.sqrt(2 * np.pi * SIG)
    h = ys[1] - ys[0]
    p23 = np.einsum("ijl,j,l->i", p_pure, k2, k3) * h * h
    for x1 in xs1:
        k1 = np.exp(-(x1 - ys) ** 2 / (2 * SIG)) / np.sqrt(2 * np.pi * SIG)
        p_num = float(np.sum(k1 * p23) * h)
        p_cf = float(th.homodyne_pdf(np.array([x1]), np.array([x2]),
                                     np.array([x3]), *angles)[0])
        assert p_cf == pytest.approx(p_num, rel=1e-6, abs=1e-12)


def test_pdf_normalized_and_nonnegative():
    th = ThermalLossyThreeModeCat(ALPHA, PARITY, ETA, SIG)
    ys = np.linspace(-8, 8, 201)
    Y1, Y2, Y3 = np.meshgrid(ys, ys, ys, indexing="ij", sparse=True)
    p = th.homodyne_pdf(Y1, Y2, Y3, 0.4, 1.2, 2.7)
    assert np.all(p >= 0.0)
    h = ys[1] - ys[0]
    assert float(p.sum() * h ** 3) == pytest.approx(1.0, abs=1e-6)


def test_noise_channel_identity_and_trace():
    rho = lossy_cat3_fock(0.9, +1, 0.85, 5)
    assert np.allclose(gaussian_noise_channel_3mode(rho, 0.0, 5), rho)
    out = gaussian_noise_channel_3mode(rho, 0.12, 5)
    # trace can only LEAK upward out of the truncation, never grow
    assert np.trace(out).real <= np.trace(rho).real + 1e-12
    assert np.trace(out).real > 0.9 * np.trace(rho).real
    # Hermitian and PSD (numerically)
    assert np.allclose(out, out.conj().T, atol=1e-12)
    assert np.linalg.eigvalsh(out).min() > -1e-10


def test_noise_channel_1mode_matches_pdf_convolution():
    """Fock-route channel vs 1D Gaussian convolution of the marginal."""
    n_max, sig = 30, 0.15
    c = _coherent_coeffs(1.1, n_max)
    cm = c * (-1.0) ** np.arange(n_max)
    psi = (c + cm) / np.linalg.norm(c + cm)      # even cat, well truncated
    rho = np.outer(psi, psi)
    rho_th = gaussian_noise_channel_1mode(rho, sig)
    ys = np.linspace(-10, 10, 2001)
    xs = np.linspace(-3.5, 3.5, 29)
    for theta in (0.0, 0.9):
        p_pure = marginal_from_rho(rho, ys, theta)
        kern = np.exp(-(xs[:, None] - ys[None, :]) ** 2 / (2 * sig))
        kern /= np.sqrt(2 * np.pi * sig)
        p_num = np.trapezoid(kern * p_pure[None, :], ys, axis=1)
        p_fock = marginal_from_rho(rho_th, xs, theta)
        assert np.allclose(p_fock, p_num, rtol=1e-7, atol=1e-10)


def test_displacement_matrix_is_unitary_and_displaces_vacuum():
    # unitarity holds only away from the truncation edge: at |beta|~0.8
    # a row n leaks ~|<n+k|D|n>|^2 tails past n_max, so check a 16x16
    # block against a much larger cutoff
    n_max, beta = 40, 0.7 - 0.4j
    D = displacement_matrix(beta, n_max)
    I = D @ D.conj().T
    assert np.allclose(I[:16, :16], np.eye(16), atol=1e-8)
    vac = np.zeros(n_max); vac[0] = 1.0
    coh = D @ vac
    ref = _coherent_coeffs(abs(beta), n_max).astype(complex)
    ref *= (beta / abs(beta)) ** np.arange(n_max)
    assert np.allclose(coh, ref, atol=1e-10)


def test_fock_target_matches_closed_form_pdf():
    """3-mode Fock-route thermal target vs the closed-form pdf, at a small
    amplitude where the truncation deficit is negligible."""
    a, eta, sig, n_max = 0.7, 0.8, 0.08, 10
    rho_th = thermal_lossy_cat3_fock(a, +1, eta, sig, n_max, n_r=8)
    target = ThermalLossyThreeModeCat(a, +1, eta, sig)
    rng = np.random.default_rng(1)
    X = rng.normal(scale=1.0, size=(12, 3))
    theta = np.array([0.5, 1.3, 2.2])
    from wigner_splat.purefock3 import _mode_vectors
    # NOTE -theta: same conjugate-convention pairing pinned in
    # tests/test_loss_deployment.py (invisible for real states, but kept
    # explicit here for consistency)
    v1, v2, v3 = _mode_vectors(X, -theta, n_max)
    V = np.einsum("sm,sn,sq->smnq", v1, v2, v3).reshape(len(X), -1)
    p_fock = np.real(np.einsum("sa,ab,sb->s", np.conj(V), rho_th, V))
    p_cf = target.homodyne_pdf(X[:, 0], X[:, 1], X[:, 2], *theta)
    # relative agreement in the bulk; the far tail is truncation dominated
    # (the sigma=0 lossy baseline shows the SAME order of deviation there,
    # so it measures lossy_cat3_fock's truncation, not the noise channel)
    bulk = p_cf > 1e-4
    assert bulk.sum() >= 8
    assert np.allclose(p_fock[bulk], p_cf[bulk], rtol=1e-4)


def test_thermal_overlap_reduces_and_matches_fock_projection():
    rng = np.random.default_rng(3)
    mix = SplatMixture3F(
        w=rng.normal(size=2),
        mu=rng.uniform(-1.0, 1.0, size=(2, 6)),
        ld=rng.uniform(-0.4, 0.1, size=(2, 6)),
        lo=0.1 * rng.normal(size=(2, 15)),
    )
    s0 = overlap_vs_thermal_lossy_cat3(mix, ALPHA, PARITY, ETA, 0.0)
    s_ref = overlap_vs_lossy_cat3(mix, ALPHA, PARITY, ETA)
    assert s0 == pytest.approx(s_ref, rel=1e-12)

    # independent Fock route at truncation-safe amplitude
    a, eta, sig, n_max = 0.7, 0.85, 0.08, 10
    from wigner_splat.fock_project import rho_from_splat
    rho_mix = rho_from_splat(mix, n_max)
    rho_th = thermal_lossy_cat3_fock(a, +1, eta, sig, n_max, n_r=8)
    s_fock = float(np.real(np.trace(rho_mix @ rho_th)))
    s_cf = overlap_vs_thermal_lossy_cat3(mix, a, +1, eta, sig)
    assert s_cf == pytest.approx(s_fock, rel=2e-3, abs=1e-6)

def test_negative_sigma_rejected_everywhere():
    """PR-61 review P2: sigma_add < 0 must be a ValueError on every public
    path, not a silent identity or a NaN."""
    rho1 = np.eye(4) / 4.0
    rho3 = np.eye(27) / 27.0
    mix = SplatMixture3F([1.0], [np.zeros(6)], [np.zeros(6)],
                         [np.zeros(15)])
    with pytest.raises(ValueError):
        ThermalLossyThreeModeCat(ALPHA, PARITY, ETA, sigma_add=-0.1)
    with pytest.raises(ValueError):
        gaussian_noise_channel_1mode(rho1, -0.1)
    with pytest.raises(ValueError):
        gaussian_noise_channel_3mode(rho3, -0.1, 3)
    with pytest.raises(ValueError):
        thermal_lossy_cat3_fock(ALPHA, PARITY, ETA, -0.1, 4)
    with pytest.raises(ValueError):
        overlap_vs_thermal_lossy_cat3(mix, ALPHA, PARITY, ETA, -0.6)


def test_fock_target_build_cutoff_converged_at_experiment_amplitude():
    """PR-61 review P1: the displacement channel scatters population BOTH
    ways, so the target must be built wide and cropped. At the experiment
    amplitude (1.5) the cropped n_max=8 block must be converged in the
    build cutoff, and the old build-at-8 construction must differ (the
    artifact this regression pins)."""
    a, eta, sig, n8 = 1.5, 0.8, 0.1, 8
    t16 = thermal_lossy_cat3_fock(a, +1, eta, sig, n8, n_r=8, n_build=16)
    t20 = thermal_lossy_cat3_fock(a, +1, eta, sig, n8, n_r=8, n_build=20)
    assert np.max(np.abs(t16 - t20)) < 5e-6
    t8 = thermal_lossy_cat3_fock(a, +1, eta, sig, n8, n_r=8, n_build=8)
    assert np.max(np.abs(t16 - t8)) > 1e-4
