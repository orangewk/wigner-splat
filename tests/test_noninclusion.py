"""Accuracy pins for the exp20 non-inclusion scan (issue #63).

The scan's conclusions rest on reconstructing the UNIQUE loss-channel
pre-image rho'(eta') of the exp19 thermal-noise target from its
closed-form characteristic function. These tests pin that
reconstruction against independent references on every regime of the
derivation (experiments/20_noninclusion/derivation.md):

  * chi normalization and the scalar displacement_matrix reference
  * eta' = eta      -> rho' must equal N_{sigma/eta}(cat)      (Lemma 1)
  * regime I        -> rho' must equal the remapped thermal lossy cat
  * regime III      -> applying truncated-Kraus loss to rho' must
                       recover the target (the inversion is an operator
                       identity whether or not rho' is PSD)
  * 3-mode assembly -> must match thermal_lossy_cat3_fock remapped
"""
import importlib.util
import pathlib
import sys
from math import comb

import numpy as np
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from wigner_splat.fock import (  # noqa: E402
    displacement_matrix, gaussian_noise_channel_1mode,
    thermal_lossy_cat3_fock,
)

_spec = importlib.util.spec_from_file_location(
    "run20", pathlib.Path(__file__).resolve().parents[1]
    / "experiments" / "20_noninclusion" / "run.py")
run20 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run20)

ALPHA, PARITY, ETA, SIGMA = run20.ALPHA, run20.PARITY, run20.ETA, run20.SIGMA


def cat1_fock(alpha, parity, n_max):
    """1-mode cat |alpha> + parity |-alpha>, normalized Fock vector."""
    n = np.arange(n_max)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    c = np.exp(-alpha ** 2 / 2.0 + n * np.log(alpha) - log_fact / 2.0)
    c = c * (1.0 + parity * (-1.0) ** n)
    return c / np.linalg.norm(c)


def kraus_loss_1mode(rho, eta, n_max):
    """Truncated per-mode loss Kraus (exact downward)."""
    out = np.zeros_like(rho)
    for k in range(n_max):
        A = np.zeros((n_max, n_max))
        idx = np.arange(k, n_max)
        A[idx - k, idx] = [np.sqrt(comb(m, k) * eta ** (m - k)
                                   * (1 - eta) ** k) for m in idx]
        out += A @ rho @ A.T
    return out


def test_chi_cat_normalized_at_zero():
    tot = sum(coef * run20.coh_pair_chi(b, g, 0.0 + 0.0j)
              for b, g, coef in run20.cat_terms_1mode(ALPHA, PARITY))
    assert abs(tot - 1.0) < 1e-14


def test_displacement_batch_matches_scalar_reference():
    betas = np.array([0.3 + 0.1j, -1.2 + 0.7j, 2.0 - 1.5j])
    Db = run20.displacement_batch(betas, 12)
    for g, b in enumerate(betas):
        assert np.max(np.abs(Db[g] - displacement_matrix(b, 12))) < 1e-12


def test_preimage_at_eta_equals_noise_on_cat():
    """Lemma 1: at eta' = eta the pre-image is N_{sigma/eta}(cat)."""
    n_show, n_wide = 16, 30
    c = cat1_fock(ALPHA, PARITY, n_wide)
    ref = gaussian_noise_channel_1mode(np.outer(c, c.conj()), SIGMA / ETA)
    got = run20.preimage_1mode(ETA, n_show)
    assert np.max(np.abs(got - ref[:n_show, :n_show])) < 1e-9


def test_preimage_regime1_equals_remapped_thermal_lossy_cat():
    """Regime I (eta' > eta): rho' = N_{sigma/eta'}(E_{eta/eta'}(cat))."""
    eta_p, n_show, n_wide = 0.9, 14, 30
    c = cat1_fock(ALPHA, PARITY, n_wide)
    lossy = kraus_loss_1mode(np.outer(c, c.conj()), ETA / eta_p, n_wide)
    ref = gaussian_noise_channel_1mode(lossy, SIGMA / eta_p)
    got = run20.preimage_1mode(eta_p, n_show)
    assert np.max(np.abs(got - ref[:n_show, :n_show])) < 1e-9


def test_preimage_forward_recovers_target_in_regime3():
    """Regime III (eta' < eta - sigma): loss_eta'(rho') = target as an
    operator identity, PSD or not -- the pre-image formula's real pin."""
    eta_p, n_show, n_wide = 0.5, 14, 30
    rho_p = run20.preimage_1mode(eta_p, n_wide)
    fwd = kraus_loss_1mode(rho_p, eta_p, n_wide)
    c = cat1_fock(ALPHA, PARITY, n_wide)
    target = gaussian_noise_channel_1mode(
        kraus_loss_1mode(np.outer(c, c.conj()), ETA, n_wide), SIGMA)
    assert np.max(np.abs(fwd[:n_show, :n_show]
                         - target[:n_show, :n_show])) < 1e-8


def test_preimage_trace_and_hermiticity_regime3():
    rho = run20.preimage_1mode(0.55, 30)
    assert abs(np.trace(rho).real - 1.0) < 1e-9
    assert np.max(np.abs(rho - rho.conj().T)) < 1e-10


def test_preimage_3mode_matches_remapped_builder():
    """3-mode assembly vs thermal_lossy_cat3_fock at remapped params
    (regime I: eta -> eta/eta', sigma -> sigma/eta')."""
    eta_p, n = 0.9, 8
    ref = thermal_lossy_cat3_fock(ALPHA, PARITY, eta=ETA / eta_p,
                                  sigma_add=SIGMA / eta_p, n_max=n,
                                  n_build=20)
    got = run20.preimage_3mode(eta_p, n)
    assert np.max(np.abs(got - ref)) < 1e-8


@pytest.mark.slow
def test_regime3_scan_point_is_robust_to_quadrature_and_cutoff():
    """The scan's headline (PSD violation below the boundary) must not
    be a quadrature or truncation artifact: min eigenvalue at a
    representative regime-III point is stable under doubling nodes and
    raising the cutoff."""
    eta_p = 0.6
    base = np.linalg.eigvalsh(run20.preimage_1mode(eta_p, 30).real)[0]
    more_nodes = np.linalg.eigvalsh(
        run20.preimage_1mode(eta_p, 30, n_nodes=160).real)[0]
    wider = np.linalg.eigvalsh(run20.preimage_1mode(eta_p, 40).real)[0]
    assert abs(base - more_nodes) < 1e-9
    assert abs(base - wider) < 1e-7


def coherent_fock(beta, n_max):
    n = np.arange(n_max)
    log_fact = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, n_max)))])
    with np.errstate(divide="ignore", invalid="ignore"):
        logb = np.where(n > 0, n * np.log(np.abs(beta) + (beta == 0)), 0.0)
    c = np.exp(-np.abs(beta) ** 2 / 2.0 + logb - log_fact / 2.0)
    ph = np.ones(n_max, complex) if beta == 0 else (beta / np.abs(beta)) ** n
    return c * ph


def test_theorem1_qcat_bargmann_zero():
    """Theorem 1's witness: the even cat's Husimi function vanishes at
    beta with conj(beta) = i pi / (2 alpha) (cosh zero, closed form)."""
    beta0 = np.conj(1j * np.pi / (2.0 * ALPHA))
    cat = cat1_fock(ALPHA, PARITY, 60)
    ov = np.vdot(coherent_fock(beta0, 60), cat)
    assert abs(ov) ** 2 < 1e-28


def test_theorem1_husimi_negative_in_regime3():
    """Theorem 1 operating: in regime III the pre-image's Husimi
    function (well-defined as a quadratic form whether or not rho' is
    a state) takes NEGATIVE values -- checked at the fringe axis where
    the cat's Bargmann zeros sit."""
    rho = run20.preimage_1mode(0.6, 30)
    ys = np.linspace(0.0, 2.5, 61)
    vals = []
    for y in ys:
        v = coherent_fock(np.conj(1j * y), 30)
        vals.append(np.real(np.vdot(v, rho @ v)))
    assert min(vals) < -1e-4
