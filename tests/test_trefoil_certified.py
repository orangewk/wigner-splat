"""Referee tests for experiment 29's certified evaluator.

Independent checks of experiments/29_trefoil_certified/derivation.md's
pre-declared quantities: the E1 exact enclosures re-verified in raw
fractions arithmetic, the W2/W3 certified margins refereed one-sidedly
against direct evaluation on sphere samples, and a numerical probe of the
W4 winding bound on Gaussian K=2 censuses. No epistemic status is
authored here (derivation.md §8 is the sole authoring location).
"""

from __future__ import annotations

import importlib.util
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP29 = ROOT / "experiments" / "29_trefoil_certified"
EXP28 = ROOT / "experiments" / "28_isotopy_stability"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


certified = _load(EXP29 / "certified.py", "exp29_certified")
summary_block = _load(EXP29 / "summary_block.py", "exp29_summary")
stability = _load(EXP28 / "stability.py", "exp28_stability_for29")


def _trefoil():
    c = np.zeros((3, 4), dtype=complex)
    c[2, 0] = 0.8
    c[0, 3] = 0.6
    return c


def test_e1_enclosures_reverified_in_exact_arithmetic():
    """Re-prove the enclosures with raw Fractions, independently of the
    evaluator's own assertions."""
    assert certified.A_LO ** 2 < Fraction(8, 25) < certified.A_HI ** 2
    assert certified.B_LO ** 2 < Fraction(3, 50) < certified.B_HI ** 2
    s_lo, s_hi = certified.s_star_enclosure()
    # exact sign proofs at the bracket ends
    _, up_at_lo = certified.cubic_sign_bounds(s_lo)
    lo_at_hi, _ = certified.cubic_sign_bounds(s_hi)
    assert up_at_lo < 0 < lo_at_hi
    assert 0 < s_hi - s_lo < Fraction(1, 10**5)
    enc = certified.enclosures()
    assert enc["theta_star"][0] < enc["theta_star"][1]
    assert certified.band_check(enc)


def test_w2_clearance_one_sided_on_samples():
    """Every sphere sample in the theta-certain complement (|theta -
    theta*| >= rho implies true-link distance >= rho, since theta is
    1-Lipschitz) must have |f| >= m_cert(rho). The earlier cloud-based
    selector was withdrawn in the Sol audit round: cloud distance
    over-estimates link distance and cannot certify complement
    membership."""
    enc = certified.enclosures()
    w2 = certified.w2_constants(enc)
    rho = 0.1
    m = certified.m_cert(rho, w2)
    assert m > 0.0
    th_lo, th_hi = enc["theta_star"]
    p = stability.poly_scaled(_trefoil())
    checked = 0
    for th in np.linspace(0.02, math.pi / 2 - 0.02, 60):
        if th_lo - rho < th < th_hi + rho:
            continue
        for a in np.arange(6) * (2 * math.pi / 6):
            for b in np.arange(6) * (2 * math.pi / 6):
                w1, w2c = stability.sphere_point(th, a, b)
                fval = abs(complex(stability.poly_eval(p, w1, w2c)))
                assert fval >= m - 1e-9
                checked += 1
    assert checked > 100


def test_w3_transversality_one_sided_on_samples():
    """Every sphere sample within cloud distance rho - slack of the zero
    cloud lies in U_rho — sound only under the §3 cloud-error
    certificate, established first — and must have sigma_2 >=
    sigma_cert(rho). rho sits where the corrected formula is positive
    (the 2026-08-02 review fixed a /4 coefficient error)."""
    enc = certified.enclosures()
    w2 = certified.w2_constants(enc)
    slack = 1e-8
    keep_tol = 1e-10
    assert certified.cloud_error_bound(keep_tol, w2) <= slack
    rho = 0.08
    s_cert = certified.sigma_cert(rho, enc)
    assert s_cert > 0.0
    coeffs = _trefoil()
    cloud = stability.zero_cloud(coeffs, n_theta=24, n_phase=16, keep_tol=keep_tol)
    p = stability.poly_scaled(coeffs)
    d1p, d2p = stability.poly_partials(p)
    rows, sigs = [], []
    for th in np.linspace(0.7, 1.3, 30):
        for a in np.arange(8) * (2 * math.pi / 8):
            for b in np.arange(8) * (2 * math.pi / 8):
                w1, w2c = stability.sphere_point(th, a, b)
                rows.append([w1.real, w1.imag, w2c.real, w2c.imag])
                sigs.append(
                    stability.sigma2_on_sphere(
                        complex(stability.poly_eval(d1p, w1, w2c)),
                        complex(stability.poly_eval(d2p, w1, w2c)),
                        w1,
                        w2c,
                    )
                )
    dists = stability.geodesic_dists(np.array(rows), cloud)
    sigs = np.array(sigs)
    inside = sigs[dists <= rho - slack]
    assert inside.size > 0
    assert float(np.min(inside)) >= s_cert - 1e-9


def test_w3_holds_on_torus_normal_probes():
    """Reviewer-style probe family (second review round): points moved
    off the zero curve along the in-torus normal by distances up to rho
    must respect the corrected sigma_cert(rho)."""
    enc = certified.enclosures()
    rho = 0.08
    s_cert = certified.sigma_cert(rho, enc)
    assert s_cert > 0.0
    th = 0.5 * (enc["theta_star"][0] + enc["theta_star"][1])
    cs, sn = math.cos(th), math.sin(th)
    n_a = 1.0
    n_b = -(cs * cs * 3.0 * n_a) / (sn * sn * 2.0)
    norm = math.sqrt(cs * cs * n_a * n_a + sn * sn * n_b * n_b)
    n_a, n_b = n_a / norm, n_b / norm
    p = stability.poly_scaled(_trefoil())
    d1p, d2p = stability.poly_partials(p)
    for dist_frac in (0.3, 0.6, 0.95):
        dist = rho * dist_frac
        for u in np.linspace(0.0, 2.0 * math.pi, 24, endpoint=False):
            b0 = u
            a0 = (math.pi + 3.0 * b0) / 2.0
            aa, bb = a0 + dist * n_a, b0 + dist * n_b
            w1 = cs * complex(math.cos(aa), math.sin(aa))
            w2c = sn * complex(math.cos(bb), math.sin(bb))
            sig = stability.sigma2_on_sphere(
                complex(stability.poly_eval(d1p, w1, w2c)),
                complex(stability.poly_eval(d2p, w1, w2c)),
                w1,
                w2c,
            )
            assert sig >= s_cert - 1e-9


def test_g_lower_bounds_the_exact_gradient_norm():
    enc = certified.enclosures()
    w2 = certified.w2_constants(enc)
    th_mid = 0.5 * (enc["theta_star"][0] + enc["theta_star"][1])
    g_exact = math.sqrt(
        4.0 / math.cos(th_mid) ** 2 + 9.0 / math.sin(th_mid) ** 2
    )
    assert w2["G_lower"] <= g_exact + 1e-6


def test_zero_curve_parametrization_annihilates_f():
    """W1 referee: the declared (3,2) parametrization at a float root of
    the cubic lies on the zero set to solver precision."""
    enc = certified.enclosures()
    s_mid = 0.5 * (enc["s_star"][0] + enc["s_star"][1])
    th = math.asin(s_mid)
    p = stability.poly_scaled(_trefoil())
    for u in np.linspace(0.0, 2 * math.pi, 17):
        alpha = (math.pi + 0.0) / 2.0 + 3.0 * u / 2.0  # 2 alpha - 3 beta = pi at beta = u...
        beta = u
        alpha = (math.pi + 3.0 * beta) / 2.0
        w1 = math.cos(th) * complex(math.cos(alpha), math.sin(alpha))
        w2c = math.sin(th) * complex(math.cos(beta), math.sin(beta))
        val = abs(complex(stability.poly_eval(p, w1, w2c)))
        assert val < 5e-6


def test_directional_formatters_are_decimal_safe():
    """Sol re-audit boundary cases: naive floor/ceil-of-scaled-float
    formatters fail exactly here."""
    from decimal import Decimal

    assert summary_block._fmt_dn(0.3, 1) == "0.2"  # binary 0.3 < decimal 0.3
    assert summary_block._fmt_up(0.1, 1) == "0.2"  # binary 0.1 > decimal 0.1
    for x in (0.008482623318894482, 0.9999280463960066, 1.0243409567380726):
        for digits in (4, 6, 7):
            dn = Decimal(summary_block._fmt_dn(x, digits))
            up = Decimal(summary_block._fmt_up(x, digits))
            assert dn <= Decimal.from_float(x) <= up


def test_fidelity_bound_is_outward():
    """The serialized upper bound must never sit below the exact value
    (Sol re-audit: the naive double chain lost an ULP)."""
    for eps in (0.008482623318894482, 0.10996407377738154, 0.3, 1.0):
        fb = certified.fidelity_bound(eps)
        assert Fraction(fb) >= (1 - Fraction(eps) ** 2 / 2) ** 2


def test_cloud_residual_upper_bounds_the_committed_cloud():
    """The recorded certificate must upper-bound float-evaluated
    residuals at the normalized cloud points and stay within the slack
    chain of the §3 corollary."""
    enc = certified.enclosures()
    w2 = certified.w2_constants(enc)
    cloud = stability.zero_cloud(_trefoil(), n_theta=16, n_phase=8)
    assert cloud.shape[0] > 5
    upper = certified.cloud_residual_upper(cloud)
    p = stability.poly_scaled(_trefoil())
    for row in cloud:
        w1 = complex(row[0], row[1])
        w2c = complex(row[2], row[3])
        n = math.sqrt(abs(w1) ** 2 + abs(w2c) ** 2)
        resid = abs(complex(stability.poly_eval(p, w1 / n, w2c / n)))
        assert resid <= upper + 1e-13
    assert certified.cloud_error_bound(upper, w2) <= 1e-8


def test_claim_registry_parses_all_declared_ids():
    registry = summary_block.load_claim_registry()
    assert set(registry) == set(summary_block.CLAIM_IDS)
    for row in registry.values():
        assert row["status"] and row["basis"]


@pytest.mark.slow
def test_w4_probe_gaussian_k2_censuses_have_windings_at_most_2():
    """Numerical probe of W4: censuses of K=2 pure-Gaussian states show
    no |winding| above 2. (A probe, not the proof; TraceError skips.)"""
    from wigner_splat.stellar2 import TraceError, census, gaussian_sum_stellar, tmsv_term

    states = [
        [tmsv_term(0.3, 1.0), tmsv_term(-0.3, -1.0)],  # odd TMSV cat (24/P4)
        [
            (1.0, 0.2, 0.1, 0.15, 0.3, -0.1),
            (-1.0, -0.1, 0.25, -0.2, 0.1, 0.2),
        ],
    ]
    checked = 0
    for terms in states:
        try:
            res = census(gaussian_sum_stellar(terms), n_eta=90, n_xi=96)
        except TraceError:
            continue
        for comp in res["components"]:
            for w in comp["windings"]:
                if w is not None:
                    assert abs(int(w)) <= 2
        checked += 1
    assert checked >= 1
