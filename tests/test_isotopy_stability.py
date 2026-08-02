"""Referee tests for experiment 28's stability toolkit.

Independent checks of the pre-declared quantities of
experiments/28_isotopy_stability/derivation.md: the S1/S2 perturbation
bounds against direct evaluation, the numeric sigma_2 evaluator against an
exact closed form, the S4 margins one-sidedly on a grid, the eps0_cert
search, and the delta/s reparameterization. No epistemic status is authored
here (derivation.md §7 is the sole authoring location).
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "28_isotopy_stability"


def _load(name):
    spec = importlib.util.spec_from_file_location(f"exp28_{name}", EXP / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stability = _load("stability")
summary_block = _load("summary_block")


def _random_state(rng, cutoff):
    c = rng.normal(size=(cutoff, cutoff)) + 1j * rng.normal(size=(cutoff, cutoff))
    return c / math.sqrt(float(np.sum(np.abs(c) ** 2)))


def _stellar_eval(c, w1, w2):
    return complex(stability.poly_eval(stability.poly_scaled(c), w1, w2))


def test_s1_kernel_bound_holds_and_is_sharp():
    """|f_psi - f_phi| <= ||psi - phi|| e^{|w|^2/2} on samples, and the
    coherent-kernel-aligned difference approaches equality."""
    rng = np.random.default_rng(20260802)
    for _ in range(4):
        a = _random_state(rng, 6)
        b = _random_state(rng, 6)
        delta = math.sqrt(float(np.sum(np.abs(a - b) ** 2)))
        for _ in range(12):
            th = rng.uniform(0.05, math.pi / 2 - 0.05)
            r = rng.uniform(0.2, 1.2)
            w1, w2 = stability.sphere_point(th, rng.uniform(0, 6.28), rng.uniform(0, 6.28))
            w1, w2 = r * w1, r * w2
            lhs = abs(_stellar_eval(a, w1, w2) - _stellar_eval(b, w1, w2))
            assert lhs <= delta * math.exp(r * r / 2.0) + 1e-12

    # sharpness: difference proportional to the conjugated kernel at w0,
    # truncated at a cutoff where the tail is negligible for |w0| = 1
    w1, w2 = stability.sphere_point(0.7, 0.3, 1.1)
    cutoff = 40
    m = np.arange(cutoff)
    fact = np.vectorize(math.factorial, otypes=[float])
    v = np.outer(np.conj(w1**m), np.conj(w2**m)) / np.sqrt(np.outer(fact(m), fact(m)))
    delta = math.sqrt(float(np.sum(np.abs(v) ** 2)))
    lhs = abs(_stellar_eval(v, w1, w2))
    rhs = delta * math.exp((abs(w1) ** 2 + abs(w2) ** 2) / 2.0)
    assert lhs / rhs > 1.0 - 1e-10


def test_s2_derivative_bound_holds():
    """|d_j (f_psi - f_phi)| <= delta e^{(1+h)^2/2}/h at |w0| <= 1."""
    rng = np.random.default_rng(28)
    for _ in range(4):
        a = _random_state(rng, 6)
        b = _random_state(rng, 6)
        diff = a - b
        delta = math.sqrt(float(np.sum(np.abs(diff) ** 2)))
        p = stability.poly_scaled(diff)
        d1p, d2p = stability.poly_partials(p)
        for h in (0.3, 0.62, 1.0, 2.0):
            bound = delta * math.exp((1.0 + h) ** 2 / 2.0) / h
            for _ in range(8):
                th = rng.uniform(0.05, math.pi / 2 - 0.05)
                w1, w2 = stability.sphere_point(th, rng.uniform(0, 6.28), rng.uniform(0, 6.28))
                for dp in (d1p, d2p):
                    val = abs(complex(stability.poly_eval(dp, w1, w2)))
                    assert val <= bound + 1e-12


def test_sigma2_evaluator_matches_exact_closed_form_for_t11():
    """For f = w1 w2 the smallest singular value of d(f|S3) is exactly
    sqrt(1 - 4|f|^2) (radial-component argument with |grad| = 1); the
    generic numeric evaluator must reproduce it."""
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    p = stability.poly_scaled(c)
    d1p, d2p = stability.poly_partials(p)
    rng = np.random.default_rng(7)
    for _ in range(40):
        th = rng.uniform(0.02, math.pi / 2 - 0.02)
        w1, w2 = stability.sphere_point(th, rng.uniform(0, 6.28), rng.uniform(0, 6.28))
        f = complex(stability.poly_eval(p, w1, w2))
        exact = math.sqrt(max(0.0, 1.0 - 4.0 * abs(f) ** 2))
        num = stability.sigma2_on_sphere(
            complex(stability.poly_eval(d1p, w1, w2)),
            complex(stability.poly_eval(d2p, w1, w2)),
            w1,
            w2,
        )
        assert abs(num - exact) < 1e-9


def test_s4_closed_forms_one_sided_on_grid():
    """Mini E1: no sphere sample sits below the proved S4 bounds."""
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    p = stability.poly_scaled(c)
    d1p, d2p = stability.poly_partials(p)
    rho = 0.18
    for th in np.linspace(0.01, math.pi / 2 - 0.01, 121):
        for a in (0.0, 1.0):
            w1, w2 = stability.sphere_point(th, a, 2.0 * a)
            fval = abs(complex(stability.poly_eval(p, w1, w2)))
            if rho <= th <= math.pi / 2 - rho:
                assert fval >= stability.hopf_m(rho) - 1e-12
            sig = stability.sigma2_on_sphere(
                complex(stability.poly_eval(d1p, w1, w2)),
                complex(stability.poly_eval(d2p, w1, w2)),
                w1,
                w2,
            )
            assert sig >= abs(math.cos(2.0 * th)) - 1e-9


def test_eps0_cert_positive_and_fidelity_form_inverts():
    val, rho, h = stability.eps0_cert_hopf(
        np.linspace(0.01, math.pi / 4 - 0.01, 80), np.linspace(0.1, 2.0, 80)
    )
    assert val > 0.0 and 0.0 < rho < math.pi / 4 and h > 0.0
    fbound = stability.fidelity_bound(val)
    assert 0.0 < fbound < 1.0
    # invert: delta at that fidelity equals val
    back = math.sqrt(2.0 * (1.0 - math.sqrt(fbound)))
    assert abs(back - val) < 1e-12


def test_delta_s_reparameterization():
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    rng = np.random.default_rng(3)
    v = rng.normal(size=(5, 5)) + 1j * rng.normal(size=(5, 5))
    v = stability.unit_orthogonal(v, c)
    assert abs(float(np.sum(np.abs(v) ** 2)) - 1.0) < 1e-12
    for delta in (0.05, 0.3, 0.9, 1.3):
        s = stability.s_of_delta(delta)
        assert abs(stability.delta_of_s(s) - delta) < 1e-12
        psi = stability.perturbed_coeffs(c, v, s)
        t = stability.pad_to(c, psi.shape)
        overlap = abs(complex(np.vdot(t, psi)))
        assert abs(overlap - 1.0 / math.sqrt(1.0 + s * s)) < 1e-12
        assert abs(math.sqrt(2.0 * (1.0 - overlap)) - delta) < 1e-9


def test_claim_registry_parses_all_declared_ids():
    registry = summary_block.load_claim_registry()
    assert set(registry) == set(summary_block.CLAIM_IDS)
    for row in registry.values():
        assert row["status"] and row["basis"]


def test_trefoil_zero_cloud_and_margins_smoke():
    """E5 machinery smoke: the trefoil zero set is found and margins come
    out positive at a small rho (grid values, not certified)."""
    c = np.zeros((3, 4), dtype=complex)
    c[2, 0] = 0.8
    c[0, 3] = 0.6
    cloud = stability.zero_cloud(c, n_theta=12, n_phase=8)
    assert cloud.shape[0] >= 8
    margins = stability.grid_margins(c, cloud, [0.15], n_theta=24, n_phase=4)
    pair = margins[0.15]
    assert pair is not None
    m_g, s_g = pair
    assert m_g > 0.0 and s_g > 0.0


run_module = _load("run")


def _summary(n_components, offdiag):
    return {
        "n_components": n_components,
        "winding_multiset": [["1", "x"], ["x", "1"]][:n_components],
        "linking_offdiag": offdiag,
    }


def test_reference_acceptance_requires_hopf_linking():
    """Final-review blocking finding 1: a two-component but unlinked (or
    linking-degenerate) reference census must NOT be accepted as Hopf."""
    sig_unlinked = run_module.census_signature(_summary(2, [0]))
    sig_hopf_pos = run_module.census_signature(_summary(2, [1]))
    sig_hopf_neg = run_module.census_signature(_summary(2, [-1]))
    sig_failed = run_module.census_signature({"census_failed": "x"})
    assert sig_unlinked != run_module.HOPF_SIGNATURE
    assert sig_hopf_pos == run_module.HOPF_SIGNATURE
    assert sig_hopf_neg == run_module.HOPF_SIGNATURE
    assert sig_failed is None and sig_failed != run_module.HOPF_SIGNATURE
    assert run_module.census_signature(_summary(1, [])) != run_module.HOPF_SIGNATURE


def test_census_failure_below_eps0_cert_reaches_the_f3_gate(monkeypatch):
    """Final-review blocking finding 2: a census failure below eps0_cert is
    a census defect where S3 guarantees constancy — it must fail the F3
    gate, not be silently skipped."""
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    rng = np.random.default_rng(1)
    v = stability.unit_orthogonal(
        rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)), c
    )
    ref_sig = run_module.HOPF_SIGNATURE
    eps0_cert = 0.11

    monkeypatch.setattr(
        run_module, "census_of_coeffs", lambda coeffs: {"census_failed": "synthetic"}
    )
    entry = run_module.scan_direction("synthetic", v, c, ref_sig, eps0_cert)
    assert entry["delta_break"] is None
    assert entry["failures"]  # every lattice point failed
    assert entry["has_failure_below_eps0_cert"]
    breaks_ok, failures_ok = run_module.e3_gate([entry])
    assert breaks_ok and not failures_ok  # F3 must fire on failures alone

    # failures only above eps0_cert do not fire the failure arm
    calls = {"n": 0}

    def fail_high(coeffs):
        calls["n"] += 1
        delta = run_module.LATTICE_STEP * calls["n"]
        if delta < eps0_cert:
            return _summary(2, [1])
        return {"census_failed": "synthetic-high"}

    monkeypatch.setattr(run_module, "census_of_coeffs", fail_high)
    entry2 = run_module.scan_direction("synthetic-high", v, c, ref_sig, eps0_cert)
    assert entry2["failures"] and not entry2["has_failure_below_eps0_cert"]
    _, failures_ok2 = run_module.e3_gate([entry2])
    assert failures_ok2


def test_scan_detects_change_and_bisects(monkeypatch):
    """First-change semantics referee on a synthetic census: change appears
    at a known delta; scan must bracket and bisect to it."""
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    rng = np.random.default_rng(2)
    v = stability.unit_orthogonal(
        rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)), c
    )
    true_break = 0.273

    def synthetic(coeffs):
        # recover delta from the overlap with the target
        t = stability.pad_to(c, coeffs.shape)
        overlap = abs(complex(np.vdot(t, coeffs)))
        delta = math.sqrt(max(0.0, 2.0 * (1.0 - overlap)))
        if delta < true_break:
            return _summary(2, [1])
        return _summary(2, [0])

    monkeypatch.setattr(run_module, "census_of_coeffs", synthetic)
    entry = run_module.scan_direction(
        "synthetic-break", v, c, run_module.HOPF_SIGNATURE, 0.11
    )
    assert entry["delta_break"] is not None
    assert abs(entry["delta_break"] - true_break) <= run_module.BISECT_TOL + 1e-9
    assert not entry["breaks_below_eps0_cert"]


@pytest.mark.slow
def test_census_reference_is_hopf():
    """The |1,1> census on the standard grid has the Hopf signature."""
    from wigner_splat.stellar2 import census, fock_stellar

    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    res = census(fock_stellar(c), n_eta=90, n_xi=96)
    lk = np.array(res["linking_matrix"], dtype=int)
    assert len(res["components"]) == 2
    assert abs(int(lk[0, 1])) == 1
