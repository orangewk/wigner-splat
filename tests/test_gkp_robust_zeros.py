"""Synthetic and structural checks for Gate E robust-zero numerics."""

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "23_gkp_robust_zeros"
spec = importlib.util.spec_from_file_location("gkp_robust_zeros", EXP / "gkp_robust_zeros.py")
assert spec is not None and spec.loader is not None
gkp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gkp
spec.loader.exec_module(gkp)


def test_coherent_state_has_no_finite_bargmann_zeros():
    alpha = 1.1
    coeff = np.array([np.exp(-alpha**2 / 2) * alpha**n / math.sqrt(math.factorial(n)) for n in range(32)])
    roots = gkp.find_zeros(coeff, radius=4.0)
    assert len(roots) == 0


def test_even_cat_zeros_are_imaginary_and_equally_spaced():
    alpha = 1.2
    n = np.arange(48)
    coeff = np.zeros_like(n, dtype=np.complex128)
    coeff[::2] = alpha ** n[::2] / np.sqrt(np.array([math.factorial(int(k)) for k in n[::2]], dtype=float))
    coeff /= np.linalg.norm(coeff)
    roots = gkp.find_zeros(coeff, radius=5.0)
    roots = roots[np.argsort(roots.imag)]
    assert np.max(np.abs(roots.real)) < 1e-6
    expected_spacing = np.pi / alpha
    assert np.allclose(np.diff(roots.imag), expected_spacing, atol=2e-5)


def test_cat_robust_zero_count_scales_linearly_in_window():
    alpha = 1.0
    n = np.arange(56)
    coeff = np.zeros_like(n, dtype=np.complex128)
    coeff[::2] = alpha ** n[::2] / np.sqrt(np.array([math.factorial(int(k)) for k in n[::2]], dtype=float))
    coeff /= np.linalg.norm(coeff)
    small = gkp.find_zeros(coeff, radius=3.0)
    large = gkp.find_zeros(coeff, radius=6.0)
    small_epsilon = 1e-4 * np.exp(-3.0**2)
    large_epsilon = 1e-4 * np.exp(-6.0**2)
    small_rows = gkp.robust_zero_rows(coeff, small, 0.2, (small_epsilon,))
    small_count = sum(row["certified_robust"] for row in small_rows)
    large_rows = gkp.robust_zero_rows(coeff, large, 0.2, (large_epsilon,))
    large_count = sum(row["certified_robust"] for row in large_rows)
    assert all(row["certified_robust"] <= row["sampled_robust"] for row in small_rows + large_rows)
    assert large_count >= 2 * small_count - 1


def test_circle_minimum_lower_bound_has_known_linear_margin():
    coefficients = np.array([0.0, 1.0], dtype=np.complex128)
    sampled, derivative_bound, lower = gkp.circle_minimum_lower_bound(coefficients, 0.0j, 0.4, 1440)
    assert sampled == pytest.approx(0.4)
    assert derivative_bound == pytest.approx(1.0)
    assert lower == pytest.approx(0.4 - 2.0 * math.pi * 0.4 / 1440)

@pytest.mark.slow
def test_finite_energy_gkp_tail_bound_is_small_and_explicit():
    state = gkp.build_gkp_state(0.3, 160)
    assert state.fock_tail_upper_bound < 1e-3
    assert state.lattice_envelope_amplitude_bound < 1e-15


@pytest.mark.slow
def test_robust_zero_map_bytes_are_deterministic(tmp_path):
    sys.path.insert(0, str(EXP))
    run_spec = importlib.util.spec_from_file_location("gkp_robust_zeros_run", EXP / "run.py")
    assert run_spec is not None and run_spec.loader is not None
    run = importlib.util.module_from_spec(run_spec)
    run_spec.loader.exec_module(run)
    result = run.compute()
    output = tmp_path / "robust_zero_map.png"
    run.make_figure(result, output)
    first = output.read_bytes()
    run.make_figure(result, output)
    assert output.read_bytes() == first

def test_lifted_counts_and_generated_certification_are_data_derived():
    payload = json.loads((EXP / "robust_zero_results.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(EXP))
    run_spec = importlib.util.spec_from_file_location("gkp_robust_zeros_run_certification", EXP / "run.py")
    assert run_spec is not None and run_spec.loader is not None
    run = importlib.util.module_from_spec(run_spec)
    run_spec.loader.exec_module(run)
    for configuration in payload["configurations"]:
        max_radius = max(row["R"] for row in configuration["rows"])
        rows = [row for row in configuration["rows"] if row["R"] == max_radius and row["delta"] == 0.18]
        assert all(row["N_robust_certified"] <= row["N_robust_sampled"] for row in rows)
        assert all(row["N_robust_lifted_certified"] <= row["N_robust_lifted_sampled"] for row in rows)
        assert configuration["certification"]["ideal_comb"]["delta"] == 0.18
        assert configuration["certification"] == run.certification_from_rows(configuration["rows"], max_radius, 0.18)
