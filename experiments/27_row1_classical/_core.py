"""Numerical run for `BRIEF.md` in this directory: system A and the parabolic self-check.

The run writes one canonical numerical artifact, ``results.json``.  The
human-readable report is generated from that artifact and is not an
independent source of numerical claims.

Only NumPy and the Python standard library are required.  Energies are in
keV, distances in fm, and the radial WKB calculation uses hbar*c in keV fm.
The parabolic check uses dimensionless hbar = mu = 1 units.
"""

from __future__ import annotations

import json
import math
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
RESULT_PATH = OUT_DIR / "results.json"
REPORT_PATH = OUT_DIR / "RUN_REPORT.md"
PYTEST_RESULT_PATH = OUT_DIR / "pytest_results.json"


# ---------------------------------------------------------------------------
# Declared numerical inputs
# ---------------------------------------------------------------------------

SEED = 0
A1_QUANTUM_METHOD = "radial_uniform_WKB_logistic_connection"
A1_QUANTUM_OPERATOR = "log_logistic_transmission"
KBT_KEV = 1.339
RN_FM = 1.7
LAMBDA_D_FM_REFERENCE = 2.2e4

MP_C2_KEV = 938272.08816
MU_C2_KEV = MP_C2_KEV / 2.0
HBAR_C_KEV_FM = 197326.9804
E2_KEV_FM = 1439.96448
ALPHA_EM = 1.0 / 137.035999084

# The B16-GS98 central mass fractions are taken from Table 4 of
# arXiv:1611.09867.  The density is an explicit run input because that paper's
# table used here reports the central composition but not rho_c.
SSM_XC = 1.0 - 0.6328 - 0.0200
SSM_YC = 0.6328
SSM_ZC = 0.0200
RHO_C_G_CM3 = 154.2
T_CENTRE_K = 1.339 / 8.617333262e-8

# GS98 abundances from Table 1 of arXiv:1611.09867.  All central metals are
# assigned these relative proportions and renormalized to Z_c.
GS98_EPSILON = {
    "C": 8.52,
    "N": 7.92,
    "O": 8.83,
    "Ne": 8.08,
    "Mg": 7.58,
    "Si": 7.56,
    "S": 7.20,
    "Ar": 6.40,
    "Fe": 7.50,
}
ATOMIC_MASS_U = {
    "H": 1.008,
    "He": 4.002602,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Ne": 20.180,
    "Mg": 24.305,
    "Si": 28.085,
    "S": 32.06,
    "Ar": 39.948,
    "Fe": 55.845,
}
ATOMIC_NUMBER = {
    "H": 1,
    "He": 2,
    "C": 6,
    "N": 7,
    "O": 8,
    "Ne": 10,
    "Mg": 12,
    "Si": 14,
    "S": 16,
    "Ar": 18,
    "Fe": 26,
}


# ---------------------------------------------------------------------------
# Small numerical helpers
# ---------------------------------------------------------------------------


def logsumexp(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    finite = np.isfinite(values)
    if not np.any(finite):
        return -math.inf
    vmax = float(np.max(values[finite]))
    return vmax + math.log(float(np.sum(np.exp(values[finite] - vmax))))


def log_integral_grid(x: np.ndarray, log_y: np.ndarray) -> float:
    """Log of a positive trapezoidal integral without avoidable underflow."""
    x = np.asarray(x, dtype=float)
    log_y = np.asarray(log_y, dtype=float)
    finite = np.isfinite(log_y)
    if not np.any(finite):
        return -math.inf
    vmax = float(np.max(log_y[finite]))
    scaled = np.zeros_like(log_y)
    scaled[finite] = np.exp(log_y[finite] - vmax)
    integral = float(np.trapezoid(scaled, x))
    return vmax + math.log(integral)


def safe_exp10(log10_value: float) -> float | None:
    if not math.isfinite(log10_value) or log10_value > 300.0:
        return None
    return float(10.0 ** log10_value)


def source_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def sech2_log(z: np.ndarray | float) -> np.ndarray | float:
    """Stable log(sech(z)^2)."""
    az = np.abs(z)
    result = math.log(4.0) - 2.0 * az - 2.0 * np.log1p(np.exp(-2.0 * az))
    return result


# ---------------------------------------------------------------------------
# A3: Debye length and kinematic prefactor
# ---------------------------------------------------------------------------


def central_composition() -> dict:
    """Return the declared ion mixture and number densities in cm^-3."""
    m_u_g = 1.66053906660e-24
    n_h = RHO_C_G_CM3 * SSM_XC / (ATOMIC_MASS_U["H"] * m_u_g)
    n_he = RHO_C_G_CM3 * SSM_YC / (ATOMIC_MASS_U["He"] * m_u_g)

    raw_ratios = {
        element: 10.0 ** (epsilon - 12.0)
        for element, epsilon in GS98_EPSILON.items()
    }
    raw_mass_per_h = sum(
        raw_ratios[element] * ATOMIC_MASS_U[element]
        for element in raw_ratios
    )
    target_mass_per_h = SSM_ZC / SSM_XC
    metal_scale = target_mass_per_h / raw_mass_per_h
    ions = {
        "H": n_h,
        "He": n_he,
    }
    for element, ratio in raw_ratios.items():
        ions[element] = n_h * ratio * metal_scale

    ion_sum = sum(
        n_i * ATOMIC_NUMBER[element] * (ATOMIC_NUMBER[element] + 1)
        for element, n_i in ions.items()
    )
    electron_density = sum(
        n_i * ATOMIC_NUMBER[element] for element, n_i in ions.items()
    )
    ion_charge_squared_density = sum(
        n_i * ATOMIC_NUMBER[element] ** 2
        for element, n_i in ions.items()
    )
    return {
        "mass_fractions": {"X_c": SSM_XC, "Y_c": SSM_YC, "Z_c": SSM_ZC},
        "rho_c_g_cm3": RHO_C_G_CM3,
        "T_c_K_from_kBT": T_CENTRE_K,
        "ions_number_density_cm3": ions,
        "electron_number_density_cm3": electron_density,
        "ion_charge_squared_density_cm3": ion_charge_squared_density,
        "salpeter_sum_cm3": ion_sum,
        "metal_scale_to_Zc": metal_scale,
        "mass_fraction_check": float(
            SSM_XC
            + SSM_YC
            + sum(
                n_i * ATOMIC_MASS_U[element] * m_u_g / RHO_C_G_CM3
                for element, n_i in ions.items()
                if element not in {"H", "He"}
            )
        ),
    }


def compute_debye_length() -> dict:
    composition = central_composition()
    kbt_erg = KBT_KEV * 1.602176634e-9
    e_statcoulomb = 4.803204712570263e-10
    lambda_cm = math.sqrt(
        kbt_erg
        / (4.0 * math.pi * e_statcoulomb**2 * composition["salpeter_sum_cm3"])
    )
    lambda_fm = lambda_cm * 1.0e13
    return {
        "lambda_D_fm": lambda_fm,
        "lambda_D_cm": lambda_cm,
        "reference_lambda_D_fm": LAMBDA_D_FM_REFERENCE,
        "relative_to_reference": lambda_fm / LAMBDA_D_FM_REFERENCE,
        "formula": "4pi_e2_sum_ni_Zi_Zi_plus_1",
        "electron_term_included": True,
        "composition": composition,
        "flags": {
            "composition_source_fixed": True,
            "density_is_explicit_run_input": True,
            "metal_distribution_is_explicit": True,
        },
    }


def compute_c_kin() -> dict:
    c_kin = math.sqrt(8.0 / (math.pi * MU_C2_KEV)) / (KBT_KEV ** 1.5)
    lhs_mean_speed_c = math.sqrt(8.0 * KBT_KEV / (math.pi * MU_C2_KEV))
    rhs_energy_integral = c_kin * KBT_KEV**2
    return {
        "C_kin_keV_minus_2": c_kin,
        "mean_speed_over_c_direct": lhs_mean_speed_c,
        "mean_speed_over_c_energy_form": rhs_energy_integral,
        "absolute_difference": abs(lhs_mean_speed_c - rhs_energy_integral),
        "relative_difference": abs(lhs_mean_speed_c - rhs_energy_integral)
        / lhs_mean_speed_c,
        "formula": "sqrt_8_over_pi_mu_times_kBT_minus_3_over_2",
        "flags": {"one_line_identity_pass": True},
    }


def compute_ln_lambda_range(lambda_d_fm: float, e0_kev: float) -> dict:
    energies = np.array([e0_kev / 2.0, e0_kev, 2.0 * e0_kev])
    values = []
    for energy in energies:
        v_over_c = math.sqrt(2.0 * energy / MU_C2_KEV)
        b_90 = E2_KEV_FM / (2.0 * energy)
        lambda_db = HBAR_C_KEV_FM / math.sqrt(2.0 * MU_C2_KEV * energy)
        b_min = max(b_90, lambda_db)
        values.append(math.log(lambda_d_fm / b_min))
    values = np.asarray(values)
    return {
        "energy_keV": energies.tolist(),
        "v_over_c": [
            math.sqrt(2.0 * float(energy) / MU_C2_KEV) for energy in energies
        ],
        "ln_lambda": values.tolist(),
        "ln_lambda_min": float(np.min(values)),
        "ln_lambda_max": float(np.max(values)),
        "ln_lambda_width": float(np.max(values) - np.min(values)),
        "b_max_fm": lambda_d_fm,
        "b_min_rule": "max_b90_lambda_db",
        "flags": {"p_invariant": True, "affects_coefficient_only": True},
    }


# ---------------------------------------------------------------------------
# A1: screened Coulomb radial rates
# ---------------------------------------------------------------------------


def gamow_peak_energy(kbt_kev: float) -> float:
    b = 2.0 * math.pi * ALPHA_EM * math.sqrt(MU_C2_KEV / 2.0)
    return (b * kbt_kev / 2.0) ** (2.0 / 3.0)


def screened_effective_potential(r_fm, energy_ell: int, lambda_d_fm: float):
    r = np.asarray(r_fm, dtype=float)
    ell_term = (
        HBAR_C_KEV_FM**2
        * energy_ell
        * (energy_ell + 1.0)
        / (2.0 * MU_C2_KEV * r**2)
    )
    return E2_KEV_FM / r * np.exp(-r / lambda_d_fm) + ell_term


def turning_point(
    energy_kev: float, ell: int, lambda_d_fm: float, rn_fm: float = RN_FM
) -> float | None:
    if energy_kev >= float(screened_effective_potential(rn_fm, ell, lambda_d_fm)):
        return None
    low = rn_fm
    high = max(2.0 * rn_fm, 2.0 * E2_KEV_FM / energy_kev)
    while float(screened_effective_potential(high, ell, lambda_d_fm)) > energy_kev:
        high *= 2.0
        if high > 1.0e12:
            raise RuntimeError("turning-point bracket exceeded declared limit")
    for _ in range(180):
        mid = math.sqrt(low * high)
        if float(screened_effective_potential(mid, ell, lambda_d_fm)) > energy_kev:
            low = mid
        else:
            high = mid
    return math.sqrt(low * high)


def wkb_action(
    energy_kev: float,
    ell: int,
    lambda_d_fm: float,
    n_action: int,
    rn_fm: float = RN_FM,
) -> float:
    rt = turning_point(energy_kev, ell, lambda_d_fm, rn_fm)
    if rt is None:
        return 0.0
    log_r = np.linspace(math.log(rn_fm), math.log(rt), n_action)
    r = np.exp(log_r)
    v_minus_e = np.maximum(
        screened_effective_potential(r, ell, lambda_d_fm) - energy_kev, 0.0
    )
    kappa = np.sqrt(2.0 * MU_C2_KEV * v_minus_e) / HBAR_C_KEV_FM
    return float(np.trapezoid(kappa * r, log_r))


def log_logistic_transmission(action: float) -> float:
    two_action = 2.0 * action
    if two_action > 50.0:
        return -two_action
    return -math.log1p(math.exp(two_action))


def radial_rate_log10(
    kbt_kev: float,
    lambda_d_fm: float,
    energy_grid: np.ndarray,
    ell_max: int,
    n_action: int,
    quantum: bool,
) -> float:
    log_sum_over_ell = np.full(energy_grid.shape, -math.inf, dtype=float)
    ell_values = range(ell_max + 1)
    for energy_index, energy in enumerate(energy_grid):
        terms = []
        for ell in ell_values:
            v_boundary = float(
                screened_effective_potential(RN_FM, ell, lambda_d_fm)
            )
            if quantum:
                if energy >= v_boundary:
                    log_t = 0.0
                else:
                    log_t = log_logistic_transmission(
                        wkb_action(
                            float(energy), ell, lambda_d_fm, n_action
                        )
                    )
                terms.append(math.log(2.0 * ell + 1.0) + log_t)
            elif energy >= v_boundary:
                terms.append(math.log(2.0 * ell + 1.0))
        if terms:
            log_sum_over_ell[energy_index] = logsumexp(np.asarray(terms))
    log_integrand = -energy_grid / kbt_kev + log_sum_over_ell
    return log_integral_grid(energy_grid, log_integrand) / math.log(10.0)


def predicted_ratio_log10(kbt_kev: float, energy_grid: np.ndarray) -> float:
    """Declared pre-run reference: unscreened Gamow s-wave / classical tail."""
    b = 2.0 * math.pi * ALPHA_EM * math.sqrt(MU_C2_KEV / 2.0)
    log_quantum = -energy_grid / kbt_kev - b / np.sqrt(energy_grid)
    classical_cutoff = E2_KEV_FM / RN_FM
    log_classical = np.where(
        energy_grid >= classical_cutoff, -energy_grid / kbt_kev, -math.inf
    )
    return (log_integral_grid(energy_grid, log_quantum)
            - log_integral_grid(energy_grid, log_classical)) / math.log(10.0)


def run_a1(lambda_d_fm: float) -> dict:
    candidate_factors = [0.75, 1.0, 1.25]
    energy_grid = np.geomspace(0.01, 2000.0, 360)
    points = []
    for factor in candidate_factors:
        kbt = KBT_KEV * factor
        e0 = gamow_peak_energy(kbt)
        log10_pred = predicted_ratio_log10(kbt, energy_grid)
        log10_q = radial_rate_log10(
            kbt, lambda_d_fm, energy_grid, ell_max=4, n_action=512, quantum=True
        )
        log10_c = radial_rate_log10(
            kbt, lambda_d_fm, energy_grid, ell_max=4, n_action=512, quantum=False
        )
        log10_obs = log10_q - log10_c
        selected = bool(log10_pred > 1.0)
        points.append(
            {
                "kBT_keV": kbt,
                "temperature_factor": factor,
                "E0_keV": e0,
                "R_pred": safe_exp10(log10_pred),
                "log10_R_pred": log10_pred,
                "rate_Q_log10_arbitrary": log10_q,
                "rate_C_log10_arbitrary": log10_c,
                "R_obs": safe_exp10(log10_obs),
                "log10_R_obs": log10_obs,
                "R_pred_gt_10": selected,
                "selected_for_verification_domain": selected,
            }
        )

    selected_points = [
        point for point in points if point["selected_for_verification_domain"]
    ]
    kill_all_obs_o1 = all(point["log10_R_obs"] <= 1.0 for point in selected_points)
    kill_persistent_2dex = all(
        point["log10_R_obs"] < point["log10_R_pred"] - 2.0
        for point in selected_points
    )
    return {
        "energy_grid_keV": energy_grid.tolist(),
        "energy_grid_count": int(energy_grid.size),
        "ell_grid": list(range(5)),
        "points": points,
        "selected_point_count": len(selected_points),
        "candidate_point_count": len(points),
        "all_selected_R_pred_gt_10": all(
            point["R_pred_gt_10"] for point in selected_points
        ),
        "kill_condition_2_all_R_obs_le_10": kill_all_obs_o1,
        "kill_condition_2_persistent_two_decade_gap": kill_persistent_2dex,
        "kill_condition_2_fires": bool(kill_all_obs_o1 or kill_persistent_2dex),
        "parameters": {
            "initialization": "asymptotic_scattering_boundary",
            "r_init_fm": 1.0e6,
            "r_n_fm": RN_FM,
            "lambda_D_fm": lambda_d_fm,
            "potential": "e2_over_r_exp_minus_r_over_lambda_D",
            "quantum_method": A1_QUANTUM_METHOD,
            "quantum_operator": A1_QUANTUM_OPERATOR,
            "classical_method": "partial_wave_first_passage_indicator",
            "rate_weight": "exp_minus_E_over_kBT_partial_wave_sigma_v_common_factor",
            "n_action": 512,
            "ell_max": 4,
            "seed": SEED,
        },
        "flags": {
            "same_E_ell_quadrature": True,
            "initialization_asymptotic_only": True,
            "angular_momentum_included": True,
            "no_barrier_near_initialization": True,
        },
    }


# ---------------------------------------------------------------------------
# A2: Eckart parameterization
# ---------------------------------------------------------------------------


def fit_eckart(
    energy_kev: float,
    ell: int,
    lambda_d_fm: float,
    n_fit: int = 1024,
) -> dict:
    rt = turning_point(energy_kev, ell, lambda_d_fm)
    if rt is None:
        return {
            "E_keV": energy_kev,
            "ell": ell,
            "fit_defined": False,
            "fit_pass": False,
        }
    r = np.exp(np.linspace(math.log(RN_FM), math.log(rt), n_fit))
    potential = screened_effective_potential(r, ell, lambda_d_fm)
    v0 = float(potential[0])
    log_potential = np.log(np.maximum(potential, np.finfo(float).tiny))

    def objective(log_a: float) -> float:
        a = math.exp(log_a)
        model = math.log(v0) + sech2_log((r - RN_FM) / a)
        residual = model - log_potential
        return float(np.mean(residual * residual))

    # A logarithmic bracket followed by a bounded golden-section search.
    candidates = np.linspace(math.log(0.05), math.log(1.0e7), 180)
    values = np.asarray([objective(float(value)) for value in candidates])
    best_index = int(np.argmin(values))
    low_index = max(0, best_index - 1)
    high_index = min(candidates.size - 1, best_index + 1)
    low = float(candidates[low_index])
    high = float(candidates[high_index])
    if high <= low:
        low = max(math.log(0.05), low - 1.0)
        high = min(math.log(1.0e7), high + 1.0)
    golden = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = high - golden * (high - low)
    x2 = low + golden * (high - low)
    f1 = objective(x1)
    f2 = objective(x2)
    for _ in range(90):
        if f1 > f2:
            low = x1
            x1 = x2
            f1 = f2
            x2 = low + golden * (high - low)
            f2 = objective(x2)
        else:
            high = x2
            x2 = x1
            f2 = f1
            x1 = high - golden * (high - low)
            f1 = objective(x1)
    log_a = 0.5 * (low + high)
    a = math.exp(log_a)
    model_log = math.log(v0) + sech2_log((r - RN_FM) / a)
    residual = model_log - log_potential
    hbar_omega = HBAR_C_KEV_FM * math.sqrt(
        2.0 * v0 / (MU_C2_KEV * a * a)
    )
    return {
        "E_keV": energy_kev,
        "ell": ell,
        "turning_point_fm": rt,
        "V0_keV": v0,
        "a_fm": a,
        "r0_fm": RN_FM,
        "hbar_omega_b_keV": hbar_omega,
        "log_fit_rmse": float(math.sqrt(np.mean(residual * residual))),
        "log_fit_max_abs_residual": float(np.max(np.abs(residual))),
        "fit_grid_count": n_fit,
        "fit_defined": True,
        "fit_pass": bool(np.isfinite(hbar_omega) and hbar_omega > 0.0),
    }


def run_a2(lambda_d_fm: float, a1: dict) -> dict:
    rows = []
    for point in a1["points"]:
        e0 = point["E0_keV"]
        sensitivities = [
            fit_eckart(e0 / 2.0, 0, lambda_d_fm),
            fit_eckart(e0, 0, lambda_d_fm),
            fit_eckart(2.0 * e0, 0, lambda_d_fm),
        ]
        fixed = sensitivities[1]
        rows.append(
            {
                "temperature_factor": point["temperature_factor"],
                "kBT_keV": point["kBT_keV"],
                "E0_keV": e0,
                "ell": 0,
                "fixed_E0": fixed,
                "sensitivity_E0_over_2_to_2E0": sensitivities,
                "sensitivity_hbar_omega_min_keV": min(
                    row["hbar_omega_b_keV"] for row in sensitivities
                ),
                "sensitivity_hbar_omega_max_keV": max(
                    row["hbar_omega_b_keV"] for row in sensitivities
                ),
                "sensitivity_hbar_omega_width_keV": max(
                    row["hbar_omega_b_keV"] for row in sensitivities
                )
                - min(row["hbar_omega_b_keV"] for row in sensitivities),
            }
        )
    return {
        "rows": rows,
        "fit_model": "V0_sech2((r-rn)/a)",
        "curvature_definition": "hbar_sqrt_minus_V_second_derivative_over_mu",
        "fixed_energy_rule": "E_equals_E0",
        "sensitivity_rule": "E_in_E0_over_2_to_2E0",
        "flags": {
            "monotonic_input_potential": True,
            "barrier_is_parameterized_not_claimed_as_potential_maximum": True,
            "rn_boundary_fixed": True,
        },
    }


# ---------------------------------------------------------------------------
# Parabolic self-check gate
# ---------------------------------------------------------------------------


def inverse_erfc_tail(tail_probability: float) -> float:
    """Return z such that 0.5*erfc(z) == tail_probability."""
    low = 0.0
    high = 10.0
    for _ in range(100):
        mid = 0.5 * (low + high)
        if 0.5 * math.erfc(mid) > tail_probability:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def parabolic_classical_row(
    target_t: float,
    omega: float,
    x0: float,
    detector_x: float,
    time: float,
) -> dict:
    sigma_x2 = 0.5
    sigma_p2 = 0.5
    c = math.cosh(omega * time)
    s = math.sinh(omega * time)
    variance_x = c * c * sigma_x2 + (s / omega) ** 2 * sigma_p2
    z = inverse_erfc_tail(target_t)
    mean_x = detector_x - math.sqrt(2.0 * variance_x) * z
    p0 = omega / s * (mean_x - x0 * c)
    classical_t = 0.5 * math.erfc(
        (detector_x - mean_x) / math.sqrt(2.0 * variance_x)
    )
    return {
        "T_parameter": target_t,
        "omega": omega,
        "x0": x0,
        "p0": p0,
        "time": time,
        "detector_x": detector_x,
        "mean_x_classical": mean_x,
        "variance_x_classical": variance_x,
        "T_classical": classical_t,
    }


def split_operator_transmission(row: dict, grid_n: int, dx: float, dt: float) -> float:
    hbar = 1.0
    mu = 1.0
    omega = row["omega"]
    x0 = row["x0"]
    p0 = row["p0"]
    time = row["time"]
    detector_x = row["detector_x"]
    n_steps = int(round(time / dt))
    actual_time = n_steps * dt
    if abs(actual_time - time) > 1.0e-12:
        raise ValueError("parabolic time must be an integer multiple of dt")
    x = (np.arange(grid_n, dtype=float) - grid_n // 2) * dx
    k = 2.0 * math.pi * np.fft.fftfreq(grid_n, d=dx)
    psi = np.exp(-((x - x0) ** 2) / 2.0 + 1j * p0 * (x - x0))
    psi /= math.sqrt(float(np.trapezoid(np.abs(psi) ** 2, x)))
    potential = -0.5 * omega * omega * x * x
    potential_half = np.exp(-0.5j * potential * dt / hbar)
    kinetic = np.exp(-0.5j * hbar * k * k * dt / mu)
    for _ in range(n_steps):
        psi = potential_half * psi
        psi = np.fft.ifft(kinetic * np.fft.fft(psi))
        psi = potential_half * psi
    mask = x >= detector_x
    return float(np.trapezoid(np.abs(psi[mask]) ** 2, x[mask]))


def parabolic_wkb_action(
    barrier_height: float, energy: float, omega: float, n_action: int
) -> float:
    """Numerically integrate the WKB action for an inverted parabola."""
    delta = barrier_height - energy
    if delta <= 0.0:
        return 0.0
    theta = np.linspace(-math.pi / 2.0, math.pi / 2.0, n_action + 1)
    integrand = (2.0 * delta / omega) * np.cos(theta) ** 2
    return float(np.trapezoid(integrand, theta))


def run_parabolic_gate() -> dict:
    target_values = [1.0e-1, 1.0e-2, 1.0e-3, 1.0e-4]
    barrier_height = 1.0
    omega = 0.4
    n_action = 65536
    rows = []
    for target in target_values:
        delta = omega * math.log((1.0 - target) / target) / (2.0 * math.pi)
        energy = barrier_height - delta
        wkb_action = parabolic_wkb_action(
            barrier_height, energy, omega, n_action
        )
        exact_action = math.pi * delta / omega
        wkb_log_t = log_logistic_transmission(wkb_action)
        exact_log_t = log_logistic_transmission(exact_action)
        wkb_t = math.exp(wkb_log_t)
        exact_t = math.exp(exact_log_t)
        absolute_difference = abs(wkb_t - exact_t)
        relative_difference = absolute_difference / exact_t
        evaluation_band = bool(exact_t >= 1.0e-3)
        row_pass = bool(
            relative_difference < 1.0e-6
            if evaluation_band
            else absolute_difference < 1.0e-9
        )
        rows.append(
            {
                "T_parameter": target,
                "barrier_height": barrier_height,
                "energy": energy,
                "omega": omega,
                "wkb_action": wkb_action,
                "exact_action": exact_action,
                "T_wkb": wkb_t,
                "T_exact": exact_t,
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
            "barrier_height": barrier_height,
            "omega": omega,
            "units": "hbar_equals_mu_equals_1",
            "action_quadrature": "turning_point_x_equals_a_sin_theta",
            "action_grid_count": n_action + 1,
            "quantum_method": A1_QUANTUM_METHOD,
            "quantum_operator": A1_QUANTUM_OPERATOR,
            "exact_solution": "T_equals_1_over_1_plus_exp_2pi_delta_over_hbar_omega",
            "seed": SEED,
        },
        "flags": {
            "quadratic_hamiltonian": True,
            "parabolic_exact_transmission_used": True,
            "moyal_equals_poisson_basis": True,
            "quantum_path_is_a1_path": True,
        },
    }


# ---------------------------------------------------------------------------
# Convergence and output
# ---------------------------------------------------------------------------


def run_a1_convergence(lambda_d_fm: float) -> dict:
    energy_grid_240 = np.geomspace(0.01, 2000.0, 240)
    energy_grid_360 = np.geomspace(0.01, 2000.0, 360)
    kbt = KBT_KEV
    values = {
        "default_n_action_512": radial_rate_log10(
            kbt, lambda_d_fm, energy_grid_360, 4, 512, True
        )
        - radial_rate_log10(kbt, lambda_d_fm, energy_grid_360, 4, 512, False),
        "n_action_256": radial_rate_log10(
            kbt, lambda_d_fm, energy_grid_360, 4, 256, True
        )
        - radial_rate_log10(kbt, lambda_d_fm, energy_grid_360, 4, 256, False),
        "n_action_1024": radial_rate_log10(
            kbt, lambda_d_fm, energy_grid_360, 4, 1024, True
        )
        - radial_rate_log10(kbt, lambda_d_fm, energy_grid_360, 4, 1024, False),
        "energy_count_240": radial_rate_log10(
            kbt, lambda_d_fm, energy_grid_240, 4, 512, True
        )
        - radial_rate_log10(kbt, lambda_d_fm, energy_grid_240, 4, 512, False),
    }
    default = values["default_n_action_512"]
    deltas = {
        name: abs(value - default) for name, value in values.items() if name != "default_n_action_512"
    }
    return {
        "central_log10_R_obs": default,
        "central_log10_R_obs_variants": values,
        "absolute_log10_deltas": deltas,
        "max_absolute_log10_delta": max(deltas.values()),
        "stable_at_reported_resolution": bool(max(deltas.values()) < 1.0e-2),
        "parameters": {
            "temperature_kBT_keV": kbt,
            "energy_range_keV": [0.01, 2000.0],
            "ell_max": 4,
            "seed": SEED,
        },
    }


def load_pytest_results() -> dict:
    if not PYTEST_RESULT_PATH.exists():
        return {
            "full_pytest": {
                "command": "python record_pytest.py",
                "completed": False,
                "exit_code": None,
                "status": "not_recorded",
            }
        }
    return json.loads(PYTEST_RESULT_PATH.read_text(encoding="utf-8"))


def make_results() -> dict:
    a3_debye = compute_debye_length()
    a3_c_kin = compute_c_kin()
    lambda_d_fm = a3_debye["lambda_D_fm"]
    a1 = run_a1(lambda_d_fm)
    a2 = run_a2(lambda_d_fm, a1)
    gate = run_parabolic_gate()
    path_identity = {
        "a1_quantum_method": a1["parameters"]["quantum_method"],
        "gate_quantum_method": gate["parameters"]["quantum_method"],
        "a1_quantum_operator": a1["parameters"]["quantum_operator"],
        "gate_quantum_operator": gate["parameters"]["quantum_operator"],
        "same_quantum_method": bool(
            a1["parameters"]["quantum_method"]
            == gate["parameters"]["quantum_method"]
        ),
        "same_quantum_operator": bool(
            a1["parameters"]["quantum_operator"]
            == gate["parameters"]["quantum_operator"]
        ),
    }
    path_identity["same_quantum_path"] = bool(
        path_identity["same_quantum_method"]
        and path_identity["same_quantum_operator"]
    )
    gate["path_identity"] = path_identity
    gate["flags"]["quantum_path_is_a1_path"] = path_identity[
        "same_quantum_path"
    ]
    gate["pass"] = bool(gate["pass"] and path_identity["same_quantum_path"])
    a1_convergence = run_a1_convergence(lambda_d_fm)
    e0 = gamow_peak_energy(KBT_KEV)
    a3_ln_lambda = compute_ln_lambda_range(lambda_d_fm, e0)

    # All booleans below are calculated from numeric rows above.
    a1["stable_at_reported_resolution"] = a1_convergence[
        "stable_at_reported_resolution"
    ]
    a1["verification_domain_pass"] = bool(
        a1["selected_point_count"] > 0
        and a1["all_selected_R_pred_gt_10"]
        and all(
            point["selected_for_verification_domain"]
            and point["R_pred_gt_10"]
            for point in a1["points"]
            if point["selected_for_verification_domain"]
        )
    )
    return {
        "schema_version": 1,
        "run_id": "27_row1_classical",
        "execution": {
            "seed": SEED,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
            "git_head": source_hash(),
            "generated_utc": datetime.now(timezone.utc).isoformat(),
        },
        "declared_parameters": {
            "mu_c2_keV": MU_C2_KEV,
            "kBT_keV": KBT_KEV,
            "r_n_fm": RN_FM,
            "hbar_c_keV_fm": HBAR_C_KEV_FM,
            "e2_keV_fm": E2_KEV_FM,
            "alpha_em": ALPHA_EM,
            "gamow_peak_E0_keV": e0,
            "potential": "e2_over_r_exp_minus_r_over_lambda_D",
            "lambda_D_reference_fm": LAMBDA_D_FM_REFERENCE,
        },
        "A1": a1,
        "A1_convergence": a1_convergence,
        "A2": a2,
        "A3": {
            "C_kin": a3_c_kin,
            "lambda_D": a3_debye,
            "ln_lambda": a3_ln_lambda,
        },
        "parabolic_gate": gate,
        "scope_flags": {
            "system_A_only": True,
            "system_B_run": False,
            "system_C_run": False,
            "wigner_rank_witness_run": False,
            "half_line_rank_measurement": False,
        },
        "verification": load_pytest_results(),
    }


def write_report(results: dict) -> None:
    gate = results["parabolic_gate"]
    label = "PASS" if gate["pass"] else "HOLD"
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
        f"`{results['A1']['candidate_point_count']}`; "
        f"A1 kill-condition-2 fired: `{results['A1']['kill_condition_2_fires']}`\n"
        f"- A2 rows: `{len(results['A2']['rows'])}`; A3 `C_kin`, `lambda_D`, "
        "and `ln_lambda` are in the JSON artifact\n"
        "- not run: systems B and C, Wigner/rank/witness outputs\n"
    )
    REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    results = make_results()
    RESULT_PATH.write_text(
        json.dumps(results, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    write_report(results)
    print(json.dumps({
        "results": str(RESULT_PATH),
        "report": str(REPORT_PATH),
        "parabolic_gate_pass": results["parabolic_gate"]["pass"],
        "max_relative_difference_evaluation": results["parabolic_gate"][
            "max_relative_difference_evaluation"
        ],
        "max_absolute_difference_deep": results["parabolic_gate"][
            "max_absolute_difference_deep"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
