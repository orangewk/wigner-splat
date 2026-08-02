"""Experiment 29 runner: certified trefoil margins (derivation.md E1-E5).

Executes the pre-declared blocks and writes every evaluated number to
trefoil_certified.json (the only artifact; verdict booleans are computed
from the data; no hand-written conclusions). README's generated block is
rendered from the JSON by summary_block.py.

Halt discipline (derivation.md §7): F1 (enclosure failure) and F2
(eps29_cert infeasible) halt before the referee blocks; F3 (certified
above grid), F4 (census structure mismatch), F5 (exp25 measurement above
the certified bound) are blocking halts. A halt still writes the JSON
and README block with the halt recorded.
"""

from __future__ import annotations

import importlib.util
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

HERE = Path(__file__).resolve().parent

from wigner_splat.stellar2 import TraceError, census, fock_stellar  # noqa: E402

sys.path.insert(0, str(HERE))
import certified  # noqa: E402
import summary_block  # noqa: E402


def _load_exp28_stability():
    path = HERE.parent / "28_isotopy_stability" / "stability.py"
    spec = importlib.util.spec_from_file_location("exp28_stability", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


stability = _load_exp28_stability()

# --- declared constants (recorded in the JSON) ------------------------------

GRID = {"n_eta": 90, "n_xi": 96}  # the exp24/25 standard census grid
RHO_LIST = [round(0.02 * k, 2) for k in range(1, 11)]
H_GRID = np.linspace(0.05, 2.5, 600)
E3_TOL = 1e-9
E3_CLOUD_SLACK = 1e-8
CLOUD_KEEP_TOL = 1e-10
E4_THETA_TOL = 0.01
EXP25_JSON = HERE.parent / "25_topological_kcurves" / "topological_kcurves.json"
EXP25_CELLS = ("trefoil/gaussian/K=1", "trefoil/gaussian/K=2")


def log(msg):
    print(f"[exp29 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def trefoil_coeffs():
    c = np.zeros((3, 4), dtype=complex)
    c[2, 0] = 0.8
    c[0, 3] = 0.6
    return c


def main():
    t0 = time.time()
    results = {
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "census_grid": GRID,
        "declared": {
            "rho_list": RHO_LIST,
            "h_grid": [float(H_GRID[0]), float(H_GRID[-1]), len(H_GRID)],
            "slop": certified.SLOP,
            "band_B": [certified.THETA_LO_B, certified.THETA_HI_B],
            "e3_tol": E3_TOL,
            "e3_cloud_slack": E3_CLOUD_SLACK,
            "cloud_polish_keep_tol": CLOUD_KEEP_TOL,
            "cloud_dedup": 5e-3,
            "e4_theta_tol": E4_THETA_TOL,
            "exp25_cells": list(EXP25_CELLS),
        },
        "verdicts": {},
    }
    verdicts = results["verdicts"]

    log("E1: exact enclosures")
    try:
        enc = certified.enclosures()
        band_ok = certified.band_check(enc)
    except AssertionError as err:
        results["E1"] = {"failed": str(err)}
        verdicts["e1_enclosures_established"] = False
        verdicts["halted_at"] = "F1"
        finish(results, t0)
        return
    results["E1"] = {
        "a": list(enc["a"]),
        "b": list(enc["b"]),
        "s_star": list(enc["s_star"]),
        "s_star_exact": list(enc["s_star_exact"]),
        "a_exact": list(enc["a_exact"]),
        "b_exact": list(enc["b_exact"]),
        "theta_star": list(enc["theta_star"]),
        "band_contains_theta_star": band_ok,
        "rho_cap_core_disjoint": certified.rho_cap(enc),
    }
    verdicts["e1_enclosures_established"] = bool(band_ok)
    if not band_ok:
        verdicts["halted_at"] = "F1"
        finish(results, t0)
        return

    log("E2: certified evaluation")
    w2 = certified.w2_constants(enc)
    best, rows = certified.eps29_cert(RHO_LIST, H_GRID, enc, w2)
    eps_cert, rho_star, h_star, m_star, s_star_val = best
    results["E2"] = {
        "w2_constants": w2,
        "rows": rows,
        "eps29_cert": eps_cert,
        "rho_star": rho_star,
        "h_star": h_star,
        "m_cert_at_star": m_star,
        "sigma_cert_at_star": s_star_val,
        "fidelity_bound": certified.fidelity_bound(eps_cert),
    }
    verdicts["e2_eps29_cert_positive"] = bool(eps_cert > 0.0)
    if not verdicts["e2_eps29_cert_positive"]:
        verdicts["halted_at"] = "F2"
        finish(results, t0)
        return

    log("E3: sound margin referees + diagnostic")
    coeffs = trefoil_coeffs()
    cloud = stability.zero_cloud(coeffs, keep_tol=CLOUD_KEEP_TOL)
    p = stability.poly_scaled(coeffs)
    d1p, d2p = stability.poly_partials(p)
    th_lo_enc, th_hi_enc = enc["theta_star"]
    g_lower = w2["G_lower"]
    # §3 corollary: certified residual-to-distance bound for cloud points;
    # the cloud-inside membership family is valid only under this check
    cloud_err = certified.cloud_error_bound(CLOUD_KEEP_TOL, w2)
    cloud_membership_valid = bool(cloud_err <= E3_CLOUD_SLACK)

    # shared sphere sample sweep
    sample_rows, sample_thetas, sample_f, sample_sig = [], [], [], []
    for th in np.linspace(0.02, math.pi / 2 - 0.02, 60):
        for aa in np.arange(8) * (2 * math.pi / 8):
            for bb in np.arange(8) * (2 * math.pi / 8):
                w1, w2c = stability.sphere_point(th, aa, bb)
                sample_rows.append([w1.real, w1.imag, w2c.real, w2c.imag])
                sample_thetas.append(th)
                sample_f.append(abs(complex(stability.poly_eval(p, w1, w2c))))
                sample_sig.append(
                    stability.sigma2_on_sphere(
                        complex(stability.poly_eval(d1p, w1, w2c)),
                        complex(stability.poly_eval(d2p, w1, w2c)),
                        w1,
                        w2c,
                    )
                )
    sample_thetas = np.array(sample_thetas)
    sample_f = np.array(sample_f)
    sample_sig = np.array(sample_sig)
    cloud_dists = stability.geodesic_dists(np.array(sample_rows), cloud)

    e3_rows = []
    violations = 0
    for row in rows:
        rho = row["rho"]
        entry = {"rho": rho}
        if not row.get("admissible") or row["m_cert"] <= 0.0 or row[
            "sigma_cert"
        ] <= 0.0:
            entry["checked"] = False
            e3_rows.append(entry)
            continue
        # (a) sound clearance referee on the theta-certain complement
        outside = sample_f[
            (sample_thetas <= th_lo_enc - rho) | (sample_thetas >= th_hi_enc + rho)
        ]
        m_ok = bool(
            outside.size > 0 and float(np.min(outside)) >= row["m_cert"] - E3_TOL
        )
        # (b-i) sound transversality referee inside via cloud membership,
        # valid only under the cloud-error certificate established above
        inside = sample_sig[cloud_dists <= rho - E3_CLOUD_SLACK]
        s_ok_cloud = bool(
            cloud_membership_valid
            and inside.size > 0
            and float(np.min(inside)) >= row["sigma_cert"] - E3_TOL
        )
        # (b-ii) targeted phase-normal probes on the theta* torus
        th_mid = 0.5 * (th_lo_enc + th_hi_enc)
        dth = th_hi_enc - th_lo_enc
        probe_sigs = []
        for frac in (0.2, 0.5, 0.9):
            psi_mag = max(0.0, (rho - dth) * g_lower * frac)
            for sign in (1.0, -1.0):
                for bb in np.arange(12) * (2 * math.pi / 12):
                    alpha = (math.pi + sign * psi_mag + 3.0 * bb) / 2.0
                    w1, w2c = (
                        math.cos(th_mid) * complex(math.cos(alpha), math.sin(alpha)),
                        math.sin(th_mid) * complex(math.cos(bb), math.sin(bb)),
                    )
                    probe_sigs.append(
                        stability.sigma2_on_sphere(
                            complex(stability.poly_eval(d1p, w1, w2c)),
                            complex(stability.poly_eval(d2p, w1, w2c)),
                            w1,
                            w2c,
                        )
                    )
        s_ok_probe = bool(
            probe_sigs and min(probe_sigs) >= row["sigma_cert"] - E3_TOL
        )
        entry.update(
            {
                "checked": True,
                "m_cert": row["m_cert"],
                "sigma_cert": row["sigma_cert"],
                "m_ok_theta_complement": m_ok,
                "sigma_ok_cloud_inside": s_ok_cloud,
                "sigma_ok_phase_normal": s_ok_probe,
                "min_sigma_phase_normal": min(probe_sigs) if probe_sigs else None,
            }
        )
        if not (m_ok and s_ok_cloud and s_ok_probe):
            violations += 1
        e3_rows.append(entry)
    # (c) diagnostic only: heuristic cloud-complement grid margins
    grid_m = stability.grid_margins(coeffs, cloud, RHO_LIST)
    diag = [
        {"rho": r, "m_grid": (grid_m[r][0] if grid_m[r] else None),
         "sigma_grid": (grid_m[r][1] if grid_m[r] else None)}
        for r in RHO_LIST
    ]
    results["E3"] = {
        "zero_cloud_points": int(cloud.shape[0]),
        "cloud_error_certified": cloud_err,
        "cloud_membership_valid": cloud_membership_valid,
        "rows": e3_rows,
        "violations": violations,
        "diagnostic_grid_margins_heuristic": diag,
    }
    verdicts["e3_sound_referees_pass"] = bool(violations == 0)
    if not verdicts["e3_sound_referees_pass"]:
        verdicts["halted_at"] = "F3"
        finish(results, t0)
        return

    log("E4: census structure referee")
    try:
        res = census(fock_stellar(trefoil_coeffs()), **GRID)
        windings = [c["windings"] for c in res["components"]]
        lk = np.array(res["linking_matrix"], dtype=int)
        n = lk.shape[0] if lk.size else 0
        offdiag = [int(lk[i, j]) for i in range(n) for j in range(i + 1, n)]
        abs_winds = sorted(
            abs(int(w)) for ws in windings for w in ws if w is not None
        )
        census_summary = {
            "n_components": len(windings),
            "windings": [[str(w) for w in ws] for ws in windings],
            "abs_windings_sorted": abs_winds,
            "linking_offdiag": offdiag,
        }
    except TraceError as err:
        census_summary = {"census_failed": str(err)}
    # polished zero-cloud points are the declared stand-in for traced loop
    # points (derivation.md E4): both the theta-enclosure check and the
    # declared min(theta, pi/2 - theta) cores-disjointness check run on them
    th_lo, th_hi = enc["theta_star"]
    if cloud.shape[0]:
        thetas = np.arcsin(
            np.clip(np.hypot(cloud[:, 2], cloud[:, 3]), 0.0, 1.0)
        )
        theta_dev = float(
            np.max(np.maximum(th_lo - thetas, thetas - th_hi).clip(min=0.0))
        )
        core_dist_min = float(
            np.min(np.minimum(thetas, math.pi / 2.0 - thetas))
        )
    else:
        theta_dev = math.inf
        core_dist_min = 0.0
    core_dist_floor = min(th_lo, math.pi / 2.0 - th_hi)
    cores_ok = bool(core_dist_min >= core_dist_floor - E4_THETA_TOL)
    structure_ok = (
        "census_failed" not in census_summary
        and census_summary["n_components"] == 1
        and census_summary["abs_windings_sorted"] == [2, 3]
        and census_summary["linking_offdiag"] == []
        and theta_dev <= E4_THETA_TOL
        and cores_ok
    )
    results["E4"] = {
        "census": census_summary,
        "cloud_theta_max_deviation_from_enclosure": theta_dev,
        "cloud_min_core_distance": core_dist_min,
        "core_distance_floor": core_dist_floor,
        "cores_disjoint_ok": cores_ok,
    }
    verdicts["e4_census_matches_w1"] = bool(structure_ok)
    if not structure_ok:
        verdicts["halted_at"] = "F4"
        finish(results, t0)
        return

    log("E5: exp25 consistency")
    exp25 = json.loads(EXP25_JSON.read_text(encoding="utf-8"))
    bound = results["E2"]["fidelity_bound"]
    cells = []
    all_ok = True
    for key in EXP25_CELLS:
        measured = exp25["cells"][key]["best_fidelity"]
        ok = bool(measured <= bound)
        all_ok = all_ok and ok
        cells.append({"cell": key, "measured": measured, "within_bound": ok})
    results["E5"] = {"certified_bound": bound, "cells": cells}
    verdicts["e5_exp25_within_certified_bound"] = bool(all_ok)
    if not all_ok:
        verdicts["halted_at"] = "F5"

    finish(results, t0)


def finish(results, t0):
    results["wall_seconds"] = time.time() - t0
    payload = json_safe(results)
    (HERE / "trefoil_certified.json").write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    summary_block.write_into_readme(HERE / "README.md", payload)
    log(
        f"done in {results['wall_seconds']:.1f}s; halted_at="
        f"{results['verdicts'].get('halted_at')}"
    )


def json_safe(obj):
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return [json_safe(v) for v in obj.tolist()]
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    return obj


if __name__ == "__main__":
    main()
