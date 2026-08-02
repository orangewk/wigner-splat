"""Experiment 28 runner: certified link-stability radii (derivation.md E1-E5).

Executes the pre-declared numerical blocks and writes every measured number
to isotopy_stability.json (the only artifact; this module authors no
epistemic status and prints no hand-written conclusions — verdict booleans
are computed from the data below). README's generated block is rendered from
the JSON by summary_block.py.

Halt discipline (derivation.md §6): F1 (E1 one-sided referee violation) and
F2 (eps0_cert infeasible) halt before the probe blocks; F3 (census change
below eps0_cert) and F4 (exp25 measured fidelity above the certified bound)
halt interpretation. A halt still writes the JSON and README block with the
halt recorded.
"""

from __future__ import annotations

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
import stability  # noqa: E402
import summary_block  # noqa: E402

# --- declared constants (recorded in the JSON) ------------------------------

GRID = {"n_eta": 90, "n_xi": 96}  # the exp24/25 standard census grid
RHO_GRID = np.linspace(0.002, math.pi / 4.0 - 0.002, 600)
H_GRID = np.linspace(0.05, 2.5, 600)
E1_THETAS = np.linspace(0.005, math.pi / 2.0 - 0.005, 481)
E1_PHASES = np.arange(4) * (math.pi / 2.0)
E1_TOL = 1e-9
LATTICE_STEP = 0.02
LATTICE_MAX_K = 70
BISECT_TOL = 1e-3
E5_RHO_LIST = [round(0.05 * k, 2) for k in range(1, 11)]
EXP25_JSON = HERE.parent / "25_topological_kcurves" / "topological_kcurves.json"


def log(msg):
    print(f"[exp28 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def target_coeffs():
    c = np.zeros((2, 2), dtype=complex)
    c[1, 1] = 1.0
    return c


def trefoil_coeffs():
    c = np.zeros((3, 4), dtype=complex)
    c[2, 0] = 0.8
    c[0, 3] = 0.6
    return c


# --- E1: one-sided closed-form referee --------------------------------------

def run_e1(rho_star):
    p = stability.poly_scaled(target_coeffs())
    d1p, d2p = stability.poly_partials(p)
    m_bound = stability.hopf_m(rho_star)
    viol_m = viol_s = 0
    worst_m_gap = worst_s_gap = math.inf
    min_excess_m = math.inf
    for th in E1_THETAS:
        sig_bound = abs(math.cos(2.0 * th))
        for a in E1_PHASES:
            for b in E1_PHASES:
                w1, w2 = stability.sphere_point(th, a, b)
                fval = abs(complex(stability.poly_eval(p, w1, w2)))
                sig = stability.sigma2_on_sphere(
                    complex(stability.poly_eval(d1p, w1, w2)),
                    complex(stability.poly_eval(d2p, w1, w2)),
                    w1,
                    w2,
                )
                if rho_star <= th <= math.pi / 2.0 - rho_star:
                    gap = fval - m_bound
                    min_excess_m = min(min_excess_m, gap)
                    if gap < -E1_TOL:
                        viol_m += 1
                        worst_m_gap = min(worst_m_gap, gap)
                sgap = sig - sig_bound
                if sgap < -E1_TOL:
                    viol_s += 1
                    worst_s_gap = min(worst_s_gap, sgap)
    return {
        "n_thetas": len(E1_THETAS),
        "n_phases": len(E1_PHASES),
        "tol": E1_TOL,
        "rho_star": rho_star,
        "clearance_violations": viol_m,
        "sigma_violations": viol_s,
        "worst_clearance_gap": None if viol_m == 0 else worst_m_gap,
        "worst_sigma_gap": None if viol_s == 0 else worst_s_gap,
        "min_clearance_excess_over_bound": min_excess_m,
    }


# --- E3 probe machinery -----------------------------------------------------

def census_signature(summary):
    """Isotopy-invariant census content only (derivation.md S3 conclusion):
    component count and |linking| multiset. Frame-fixed windings are NOT
    part of the signature — for the |1,1> target they sit on the cores
    ("x" in the census) and change representation under any perturbation
    without any change of link type; they stay recorded as diagnostics."""
    if "census_failed" in summary:
        return None
    return (
        summary["n_components"],
        tuple(sorted(abs(v) for v in summary["linking_offdiag"])),
    )


def census_of_coeffs(coeffs):
    try:
        res = census(fock_stellar(coeffs), **GRID)
    except TraceError as err:
        return {"census_failed": str(err)}
    windings = [c["windings"] for c in res["components"]]
    lk = np.array(res["linking_matrix"], dtype=int)
    n = lk.shape[0] if lk.size else 0
    offdiag = [int(lk[i, j]) for i in range(n) for j in range(i + 1, n)]
    return {
        "n_components": len(windings),
        "winding_multiset": sorted(
            ["x" if w is None else str(w) for w in ws] for ws in windings
        ),
        "linking_offdiag": sorted(offdiag),
    }


def scan_direction(label, v, target_c, ref_sig, eps0_cert):
    """Ascending-lattice first-change scan + bracketing bisection (E3)."""
    entry = {
        "direction": label,
        "lattice_step": LATTICE_STEP,
        "lattice_max": LATTICE_STEP * LATTICE_MAX_K,
        "failures": [],
        "delta_break": None,
        "census_at_break": None,
        "bracketing_k": None,
    }
    prev_delta = 0.0
    for k in range(1, LATTICE_MAX_K + 1):
        delta = LATTICE_STEP * k
        s = stability.s_of_delta(delta)
        summ = census_of_coeffs(stability.perturbed_coeffs(target_c, v, s))
        sig = census_signature(summ)
        if sig is None:
            entry["failures"].append(delta)
            continue
        if sig != ref_sig:
            lo, hi = prev_delta, delta
            while hi - lo > BISECT_TOL:
                mid = (lo + hi) / 2.0
                msum = census_of_coeffs(
                    stability.perturbed_coeffs(
                        target_c, v, stability.s_of_delta(mid)
                    )
                )
                msig = census_signature(msum)
                if msig is None or msig == ref_sig:
                    lo = mid
                else:
                    hi = mid
                    summ = msum
            entry["delta_break"] = hi
            entry["census_at_break"] = summ
            entry["bracketing_k"] = k
            break
        prev_delta = delta
    if entry["delta_break"] is not None:
        entry["ratio_to_eps0_cert"] = entry["delta_break"] / eps0_cert
        entry["breaks_below_eps0_cert"] = bool(entry["delta_break"] < eps0_cert)
    else:
        entry["ratio_to_eps0_cert"] = None
        entry["breaks_below_eps0_cert"] = False
    return entry


# --- main -------------------------------------------------------------------

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
            "rho_grid": [float(RHO_GRID[0]), float(RHO_GRID[-1]), len(RHO_GRID)],
            "h_grid": [float(H_GRID[0]), float(H_GRID[-1]), len(H_GRID)],
            "e1_thetas": [float(E1_THETAS[0]), float(E1_THETAS[-1]), len(E1_THETAS)],
            "e1_phases": len(E1_PHASES),
            "e1_tol": E1_TOL,
            "lattice_step": LATTICE_STEP,
            "lattice_max_k": LATTICE_MAX_K,
            "bisect_tol": BISECT_TOL,
            "random_seed": stability.RANDOM_SEED,
            "random_directions": stability.RANDOM_DIRECTIONS,
            "random_cutoff": stability.RANDOM_CUTOFF,
            "kernel_cutoff": stability.KERNEL_CUTOFF,
            "e5_rho_list": E5_RHO_LIST,
        },
        "verdicts": {},
    }
    verdicts = results["verdicts"]
    target_c = target_coeffs()

    # E2 first: rho_star feeds E1's clearance region.
    log("E2: eps0_cert grid search")
    eps0_cert, rho_star, h_star = stability.eps0_cert_hopf(RHO_GRID, H_GRID)
    results["E2"] = {
        "eps0_cert": eps0_cert,
        "rho_star": rho_star,
        "h_star": h_star,
        "fidelity_bound": stability.fidelity_bound(eps0_cert),
    }
    verdicts["e2_eps0_cert_positive"] = bool(eps0_cert > 0.0)
    if not verdicts["e2_eps0_cert_positive"]:
        verdicts["halted_at"] = "F2"
        finish(results, t0)
        return

    log("E1: one-sided closed-form referee")
    results["E1"] = run_e1(rho_star)
    verdicts["e1_no_sample_below_proved_bounds"] = bool(
        results["E1"]["clearance_violations"] == 0
        and results["E1"]["sigma_violations"] == 0
    )
    if not verdicts["e1_no_sample_below_proved_bounds"]:
        verdicts["halted_at"] = "F1"
        finish(results, t0)
        return

    log("E3: reference census of the target")
    ref = census_of_coeffs(target_c)
    results["E3"] = {"reference_census": ref, "directions": []}
    ref_sig = census_signature(ref)
    if ref_sig is None or ref["n_components"] != 2:
        verdicts["halted_at"] = "F3"
        verdicts["e3_reference_census_is_hopf"] = False
        finish(results, t0)
        return
    verdicts["e3_reference_census_is_hopf"] = True

    directions = (
        stability.kernel_direction_list(target_c)
        + stability.random_direction_list(target_c)
    )
    exp25 = json.loads(EXP25_JSON.read_text(encoding="utf-8"))
    directions.append(
        stability.exp25_endpoint_direction(
            exp25["cells"], target_c, exp25["cutoff"]
        )
    )
    for i, (label, v) in enumerate(directions):
        log(f"E3 [{i + 1}/{len(directions)}]: {label}")
        entry = scan_direction(label, v, target_c, ref_sig, eps0_cert)
        results["E3"]["directions"].append(entry)
    breaks = [
        d["delta_break"]
        for d in results["E3"]["directions"]
        if d["delta_break"] is not None
    ]
    results["E3"]["min_delta_break"] = min(breaks) if breaks else None
    verdicts["e3_no_census_change_below_eps0_cert"] = bool(
        not any(d["breaks_below_eps0_cert"] for d in results["E3"]["directions"])
    )
    if not verdicts["e3_no_census_change_below_eps0_cert"]:
        verdicts["halted_at"] = "F3"
        finish(results, t0)
        return

    log("E4: exp25 consistency")
    measured = exp25["cells"]["t11/coherent/K=2"]["best_fidelity"]
    results["E4"] = {
        "exp25_cell": "t11/coherent/K=2",
        "measured_best_fidelity": measured,
        "certified_bound": results["E2"]["fidelity_bound"],
    }
    verdicts["e4_measured_within_certified_bound"] = bool(
        measured <= results["E2"]["fidelity_bound"]
    )
    if not verdicts["e4_measured_within_certified_bound"]:
        verdicts["halted_at"] = "F4"
        finish(results, t0)
        return

    log("E5: trefoil grid margins (numerically supported only)")
    cloud = stability.zero_cloud(trefoil_coeffs())
    margins = stability.grid_margins(trefoil_coeffs(), cloud, E5_RHO_LIST)
    best = (0.0, None, None)
    rows = []
    for rho in E5_RHO_LIST:
        pair = margins[rho]
        if pair is None:
            rows.append({"rho": rho, "m_grid": None, "sigma_grid": None})
            continue
        m_g, s_g = pair
        rows.append({"rho": rho, "m_grid": m_g, "sigma_grid": s_g})
        for h in H_GRID:
            val = stability.cert_value(m_g, s_g, float(h))
            if val > best[0]:
                best = (val, rho, float(h))
    results["E5"] = {
        "zero_cloud_points": int(cloud.shape[0]),
        "rows": rows,
        "eps0_grid_estimate_not_certified": best[0],
        "rho_at_best": best[1],
        "h_at_best": best[2],
    }
    verdicts["e5_margins_recorded"] = bool(any(r["m_grid"] for r in rows))

    finish(results, t0)


def finish(results, t0):
    results["wall_seconds"] = time.time() - t0
    payload = json_safe(results)
    (HERE / "isotopy_stability.json").write_text(
        json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8"
    )
    summary_block.write_into_readme(HERE / "README.md", payload)
    log(f"done in {results['wall_seconds']:.1f}s; halted_at="
        f"{results['verdicts'].get('halted_at')}")


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
