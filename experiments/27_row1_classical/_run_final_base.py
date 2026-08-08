"""Final execution entry point for BRIEF.md experiment 27.

The numerical kernels live in ``_core.py``; this entry point fixes the
declared energy quadrature and report generation before calling the core
result writer.  The active parabolic gate is the canonical WKB gate in
``_core.py``.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np


CORE_PATH = Path(__file__).with_name("_core.py")
SPEC = importlib.util.spec_from_file_location("exp27_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load exp27 numerical core")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


def split_operator_transmission(
    row: dict, grid_n: int, dx: float, dt: float, order: int = 4
) -> float:
    omega = row["omega"]
    x0 = row["x0"]
    p0 = row["p0"]
    time = row["time"]
    detector_x = row["detector_x"]
    n_steps = int(round(time / dt))
    if abs(n_steps * dt - time) > 1.0e-12:
        raise ValueError("parabolic time must be an integer multiple of dt")
    x = (np.arange(grid_n, dtype=float) - grid_n // 2) * dx
    k = 2.0 * math.pi * np.fft.fftfreq(grid_n, d=dx)
    psi = np.exp(-((x - x0) ** 2) / 2.0 + 1j * p0 * (x - x0))
    psi /= math.sqrt(float(np.trapezoid(np.abs(psi) ** 2, x)))
    potential = -0.5 * omega * omega * x * x

    def strang_step(state: np.ndarray, step_dt: float) -> np.ndarray:
        potential_half = np.exp(-0.5j * potential * step_dt)
        kinetic = np.exp(-0.5j * k * k * step_dt)
        state = potential_half * state
        state = np.fft.ifft(kinetic * np.fft.fft(state))
        return potential_half * state

    if order == 4:
        w1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))
        composition = (w1, 1.0 - 2.0 * w1, w1)
    elif order == 2:
        composition = (1.0,)
    else:
        raise ValueError("supported split orders are 2 and 4")
    for _ in range(n_steps):
        for coefficient in composition:
            psi = strang_step(psi, coefficient * dt)
    mask = x >= detector_x
    return float(np.trapezoid(np.abs(psi[mask]) ** 2, x[mask]))


def _legacy_split_operator_gate() -> dict:
    target_values = [1.0e-1, 1.0e-2, 1.0e-3, 1.0e-4]
    omega = 0.4
    x0 = -8.0
    detector_x = 0.0
    time = 3.0
    grid_n = 2048
    dx = 0.04
    dt = 0.002
    x = (np.arange(grid_n, dtype=float) - grid_n // 2) * dx
    rows = []
    for target in target_values:
        row = BASE.parabolic_classical_row(target, omega, x0, detector_x, time)
        analytic_classical_t = row["T_classical"]
        normal_density = np.exp(
            -(x - row["mean_x_classical"]) ** 2
            / (2.0 * row["variance_x_classical"])
        ) / math.sqrt(2.0 * math.pi * row["variance_x_classical"])
        mask = x >= detector_x
        grid_classical_t = float(np.trapezoid(normal_density[mask], x[mask]))
        quantum_t = split_operator_transmission(row, grid_n, dx, dt, order=4)
        absolute_difference = abs(quantum_t - grid_classical_t)
        relative_difference = absolute_difference / grid_classical_t
        evaluation_band = bool(target >= 1.0e-3)
        row_pass = bool(
            relative_difference < 1.0e-6
            if evaluation_band
            else absolute_difference < 1.0e-9
        )
        rows.append(
            {
                **row,
                "T_classical_analytic": analytic_classical_t,
                "T_classical": grid_classical_t,
                "T_quantum": quantum_t,
                "absolute_difference": absolute_difference,
                "relative_difference": relative_difference,
                "evaluation_band": evaluation_band,
                "row_pass": row_pass,
            }
        )
    evaluation_rows = [row for row in rows if row["evaluation_band"]]
    deep_rows = [row for row in rows if not row["evaluation_band"]]
    max_rel = max(row["relative_difference"] for row in evaluation_rows)
    max_deep_abs = max(row["absolute_difference"] for row in deep_rows)
    evaluation_pass = bool(max_rel < 1.0e-6)
    deep_pass = bool(max_deep_abs < 1.0e-9)
    return {
        "rows": rows,
        "thresholds": {
            "evaluation_T_min": 1.0e-3,
            "evaluation_relative_difference_max": 1.0e-6,
            "deep_absolute_difference_max": 1.0e-9,
        },
        "max_relative_difference_evaluation": max_rel,
        "max_absolute_difference_deep": max_deep_abs,
        "evaluation_pass": evaluation_pass,
        "deep_pass": deep_pass,
        "pass": bool(evaluation_pass and deep_pass),
        "parameters": {
            "Hamiltonian": "p2_over_2mu_plus_V0_minus_mu_omega2_x2_over_2",
            "barrier_height_dimensionless": 0.0,
            "units": "hbar_equals_mu_equals_1",
            "grid_n": grid_n,
            "dx": dx,
            "dt": dt,
            "split_steps": int(round(time / dt)),
            "split_order": 4,
            "split_composition": "Yoshida_4th_order_from_Strang",
            "classical_grid_quadrature": "same_grid_trapezoid",
            "initial_state": "minimum_uncertainty_gaussian",
            "observable": "position_probability_x_ge_detector",
            "seed": BASE.SEED,
        },
        "flags": {
            "quadratic_hamiltonian": True,
            "moyal_equals_poisson_basis": True,
            "quantum_method_independent_of_classical_formula": True,
            "same_observable_grid_quadrature": True,
        },
    }


def energy_grid(low_count: int, threshold_count: int, high_count: int) -> np.ndarray:
    return np.unique(
        np.concatenate(
            [
                np.geomspace(0.01, 100.0, low_count),
                np.linspace(700.0, 1000.0, threshold_count),
                np.linspace(1000.0, 2000.0, high_count),
            ]
        )
    )


def run_a1(lambda_d_fm: float) -> dict:
    candidate_factors = [0.75, 1.0, 1.25]
    energies = energy_grid(600, 1000, 200)
    points = []
    for factor in candidate_factors:
        kbt = BASE.KBT_KEV * factor
        e0 = BASE.gamow_peak_energy(kbt)
        log10_pred = BASE.predicted_ratio_log10(kbt, energies)
        log10_q = BASE.radial_rate_log10(
            kbt, lambda_d_fm, energies, ell_max=4, n_action=512, quantum=True
        )
        log10_c = BASE.radial_rate_log10(
            kbt, lambda_d_fm, energies, ell_max=4, n_action=512, quantum=False
        )
        log10_obs = log10_q - log10_c
        selected = bool(log10_pred > 1.0)
        points.append(
            {
                "kBT_keV": kbt,
                "temperature_factor": factor,
                "E0_keV": e0,
                "R_pred": BASE.safe_exp10(log10_pred),
                "log10_R_pred": log10_pred,
                "rate_Q_log10_arbitrary": log10_q,
                "rate_C_log10_arbitrary": log10_c,
                "R_obs": BASE.safe_exp10(log10_obs),
                "log10_R_obs": log10_obs,
                "R_pred_gt_10": selected,
                "selected_for_verification_domain": selected,
            }
        )
    selected_points = [
        point for point in points if point["selected_for_verification_domain"]
    ]
    kill_all = all(point["log10_R_obs"] <= 1.0 for point in selected_points)
    kill_gap = all(
        point["log10_R_obs"] < point["log10_R_pred"] - 2.0
        for point in selected_points
    )
    return {
        "energy_grid_keV": energies.tolist(),
        "energy_grid_count": int(energies.size),
        "ell_grid": list(range(5)),
        "points": points,
        "selected_point_count": len(selected_points),
        "candidate_point_count": len(points),
        "all_selected_R_pred_gt_10": all(
            point["R_pred_gt_10"] for point in selected_points
        ),
        "kill_condition_2_all_R_obs_le_10": bool(kill_all),
        "kill_condition_2_persistent_two_decade_gap": bool(kill_gap),
        "kill_condition_2_fires": bool(kill_all or kill_gap),
        "parameters": {
            "initialization": "asymptotic_scattering_boundary",
            "r_init_fm": 1.0e6,
            "r_n_fm": BASE.RN_FM,
            "lambda_D_fm": lambda_d_fm,
            "potential": "e2_over_r_exp_minus_r_over_lambda_D",
            "quantum_method": BASE.A1_QUANTUM_METHOD,
            "quantum_operator": BASE.A1_QUANTUM_OPERATOR,
            "classical_method": "partial_wave_first_passage_indicator",
            "rate_weight": "exp_minus_E_over_kBT_partial_wave_sigma_v_common_factor",
            "n_action": 512,
            "ell_max": 4,
            "seed": BASE.SEED,
            "energy_quadrature": "geom_low_dense_threshold_linear_high_linear",
        },
        "flags": {
            "same_E_ell_quadrature": True,
            "initialization_asymptotic_only": True,
            "angular_momentum_included": True,
            "no_barrier_near_initialization": True,
        },
    }


def run_a1_convergence(lambda_d_fm: float) -> dict:
    kbt = BASE.KBT_KEV
    dense = energy_grid(600, 1000, 200)
    coarse = energy_grid(300, 500, 100)

    def log_ratio(energies: np.ndarray, ell_max: int, n_action: int) -> float:
        return BASE.radial_rate_log10(
            kbt, lambda_d_fm, energies, ell_max, n_action, True
        ) - BASE.radial_rate_log10(
            kbt, lambda_d_fm, energies, ell_max, n_action, False
        )

    values = {
        "default_dense_n_action_512_ell_max_4": log_ratio(dense, 4, 512),
        "n_action_256": log_ratio(dense, 4, 256),
        "n_action_1024": log_ratio(dense, 4, 1024),
        "energy_grid_coarse": log_ratio(coarse, 4, 512),
        "ell_max_2": log_ratio(dense, 2, 512),
    }
    default = values["default_dense_n_action_512_ell_max_4"]
    deltas = {
        name: abs(value - default)
        for name, value in values.items()
        if name != "default_dense_n_action_512_ell_max_4"
    }
    return {
        "central_log10_R_obs": default,
        "central_log10_R_obs_variants": values,
        "absolute_log10_deltas": deltas,
        "max_absolute_log10_delta": max(deltas.values()),
        "stable_at_reported_resolution": bool(max(deltas.values()) < 1.0e-2),
        "parameters": {
            "temperature_kBT_keV": kbt,
            "dense_energy_grid_count": int(dense.size),
            "coarse_energy_grid_count": int(coarse.size),
            "energy_range_keV": [0.01, 2000.0],
            "seed": BASE.SEED,
        },
    }


def compute_c_kin() -> dict:
    c_kin = math.sqrt(8.0 / (math.pi * BASE.MU_C2_KEV)) / (
        BASE.KBT_KEV ** 1.5
    )
    lhs = math.sqrt(8.0 * BASE.KBT_KEV / (math.pi * BASE.MU_C2_KEV))
    rhs = c_kin * BASE.KBT_KEV**2
    absolute_difference = abs(lhs - rhs)
    relative_difference = absolute_difference / lhs
    return {
        "C_kin_keV_minus_2": c_kin,
        "mean_speed_over_c_direct": lhs,
        "mean_speed_over_c_energy_form": rhs,
        "absolute_difference": absolute_difference,
        "relative_difference": relative_difference,
        "identity_tolerance": 1.0e-12,
        "formula": "sqrt_8_over_pi_mu_times_kBT_minus_3_over_2",
        "flags": {
            "one_line_identity_pass": bool(relative_difference < 1.0e-12),
        },
    }


def write_report(results: dict) -> None:
    gate = results["parabolic_gate"]
    label = "PASS" if gate["pass"] else "HOLD"
    a3 = results["A3"]
    report = (
        "# RUN_REPORT\n\n"
        "- run: `27_row1_classical`\n"
        "- artifact: [`results.json`](results.json)\n"
        f"- parabolic gate: **{label}**; max evaluation relative difference = "
        f"`{gate['max_relative_difference_evaluation']:.12g}` "
        f"(limit `{gate['thresholds']['evaluation_relative_difference_max']:.12g}`); "
        f"max deep absolute difference = `{gate['max_absolute_difference_deep']:.12g}` "
        f"(limit `{gate['thresholds']['deep_absolute_difference_max']:.12g}`)\n"
        f"- A1 selected points: `{results['A1']['selected_point_count']}` / "
        f"`{results['A1']['candidate_point_count']}`; central `log10_R_obs` = "
        f"`{results['A1_convergence']['central_log10_R_obs']:.12g}`; "
        f"A1 kill-condition-2 fired: `{results['A1']['kill_condition_2_fires']}`\n"
        f"- A2 rows: `{len(results['A2']['rows'])}`; "
        f"A3 `C_kin` = `{a3['C_kin']['C_kin_keV_minus_2']:.12g}`, "
        f"`lambda_D_fm` = `{a3['lambda_D']['lambda_D_fm']:.12g}`, "
        f"`ln_lambda_width` = `{a3['ln_lambda']['ln_lambda_width']:.12g}`\n"
        f"- quantum path identity: `{gate['path_identity']['same_quantum_path']}`; "
        f"comparison rows = `{len(gate['rows'])}`\n"
        f"- full pytest: `{results['verification']['full_pytest']['completed']}`; "
        f"exit code = `{results['verification']['full_pytest']['exit_code']}`\n"
        "- not run: systems B and C, Wigner/rank/witness outputs\n"
    )
    BASE.REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    BASE.run_a1 = run_a1
    BASE.run_a1_convergence = run_a1_convergence
    BASE.compute_c_kin = compute_c_kin
    BASE.write_report = write_report
    BASE.main()


if __name__ == "__main__":
    main()
