"""Experiment 30 runner: E1-E4 of derivation.md §7 with blocking gates
F1-F4 (§8). Every verdict is COMPUTED from the data; artifacts are
written before any halt. Evaluated numbers live only in
`dictionary_alignment.json` and the README block generated from it.
"""

from __future__ import annotations

import json
import math
import platform
import sys
import time
from fractions import Fraction
from itertools import product
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

import alignment  # noqa: E402
import summary_block  # noqa: E402
from wigner_splat import gaussact  # noqa: E402

EXP25_JSON = ROOT / "experiments" / "25_topological_kcurves" / "topological_kcurves.json"
EXP28_JSON = ROOT / "experiments" / "28_isotopy_stability" / "isotopy_stability.json"
EXP29_JSON = ROOT / "experiments" / "29_trefoil_certified" / "trefoil_certified.json"

# declared constants (derivation.md §7)
SEEDS = range(64)
R_MAX = 0.8
ALPHA_MAX = 1.0
CUTOFF_E1 = 30
TOL_E1 = 1e-9
SIGMAS_E2 = (0.1, 0.3, 0.5, 0.7, 0.9, 0.95)
CUTOFF_E2 = 80
E2_REL_SLACK = 1e-12  # declared float slack (derivation.md §7 E2 note)
TOL_E3_F = 1e-6
EPS_GRID_E4 = [Fraction(k, 50) for k in range(1, 50)]


def log(msg):
    print(f"[exp30 {time.strftime('%H:%M:%S')}] {msg}", flush=True)


def finish(results, t0):
    results["environment"] = {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
    }
    results["wall_seconds"] = time.time() - t0
    (HERE / "dictionary_alignment.json").write_text(
        json.dumps(results, indent=1, sort_keys=True), encoding="utf-8"
    )
    summary_block.write_into_readme(HERE / "README.md", results)
    log(f"done in {results['wall_seconds']:.1f}s; "
        f"halted_at={results['verdicts'].get('halted_at')}")


def _norm_or_zero(v):
    n = float(np.linalg.norm(v))
    return v / n if n > 0 else v


def run():
    t0 = time.time()
    results = {"declared": {
        "seeds": [int(s) for s in SEEDS],
        "r_max": R_MAX,
        "alpha_max": ALPHA_MAX,
        "cutoff_e1": CUTOFF_E1,
        "tol_e1": TOL_E1,
        "sigmas_e2": list(SIGMAS_E2),
        "cutoff_e2": CUTOFF_E2,
        "e2_rel_slack": E2_REL_SLACK,
        "tol_e3_f": TOL_E3_F,
        "eps_grid_e4": "k/50, k=1..49",
    }}
    verdicts = {}
    results["verdicts"] = verdicts

    log("E1: normal-form referee (gaussact chain vs A1 recipe)")
    vac = gaussact.pq_state(np.array([[1.0 + 0j]]))
    max_mis, max_bres, max_anorm = 0.0, 0.0, 0.0
    sandwich_viol, defects = 0, 0
    for seed in SEEDS:
        params = gaussact.random_gauss_params(seed, r_max=R_MAX, alpha_max=ALPHA_MAX)
        chain = gaussact.gauss_unitary(vac, params)
        if chain.P.shape != (1, 1) or abs(chain.P[0, 0]) == 0.0:
            defects += 1
            continue
        a_norm = float(np.linalg.norm(chain.A, 2))
        max_anorm = max(max_anorm, a_norm)
        if not a_norm < 1.0:
            defects += 1
            continue
        recipe = alignment.recipe_state(chain.A, chain.b)
        c1 = _norm_or_zero(gaussact.fock_coeffs(chain, CUTOFF_E1).ravel())
        c2 = _norm_or_zero(gaussact.fock_coeffs(recipe, CUTOFF_E1).ravel())
        ip = complex(np.vdot(c2, c1))
        phase = ip / abs(ip) if abs(ip) > 0 else 1.0
        mis = float(np.linalg.norm(c1 - phase * c2))
        max_mis = max(max_mis, mis)
        alpha = alignment.alpha_from_b(chain.A, chain.b)
        bres = float(np.linalg.norm(
            alignment.b_from_alpha(chain.A, alpha) - chain.b
        ))
        max_bres = max(max_bres, bres)
        bmag, amag = float(np.linalg.norm(chain.b)), float(np.linalg.norm(alpha))
        if not ((1.0 - a_norm) * amag - TOL_E1 <= bmag
                <= (1.0 + a_norm) * amag + TOL_E1):
            sandwich_viol += 1
    e1_ok = bool(
        defects == 0 and sandwich_viol == 0
        and max_mis <= TOL_E1 and max_bres <= TOL_E1
    )
    results["E1"] = {
        "n_seeds": len(list(SEEDS)),
        "degree_or_norm_defects": defects,
        "max_A_norm": max_anorm,
        "max_state_mismatch": max_mis,
        "max_b_residual": max_bres,
        "sandwich_violations": sandwich_viol,
    }
    verdicts["e1_normal_form_ok"] = e1_ok
    if not e1_ok:
        verdicts["halted_at"] = "F1"
        finish(results, t0)
        return

    log("E2: norm closed form vs bracketed partials")
    bracket_failures, max_relw = 0, 0.0
    for s1, s2 in product(SIGMAS_E2, SIGMAS_E2):
        st = gaussact.pq_state(
            np.array([[1.0 + 0j]]), np.diag([s1, s2]).astype(complex)
        )
        c = gaussact.fock_coeffs(st, CUTOFF_E2)
        t1 = np.abs(c[0::2, 0]) ** 2
        t2 = np.abs(c[0, 0::2]) ** 2
        p1, p2 = float(np.sum(t1)), float(np.sum(t2))
        u1 = p1 + alignment.mode_tail_bound(float(t1[-1]), s1)
        u2 = p2 + alignment.mode_tail_bound(float(t2[-1]), s2)
        closed = alignment.norm_sq_closed(s1, s2)
        if not (
            p1 * p2 <= closed * (1.0 + E2_REL_SLACK)
            and closed <= u1 * u2 * (1.0 + E2_REL_SLACK)
        ):
            bracket_failures += 1
        max_relw = max(max_relw, (u1 * u2 - p1 * p2) / closed)
    e2_ok = bool(bracket_failures == 0)
    results["E2"] = {
        "n_pairs": len(SIGMAS_E2) ** 2,
        "cutoff": CUTOFF_E2,
        "bracket_failures": bracket_failures,
        "max_rel_bracket_width": max_relw,
    }
    verdicts["e2_norm_bracket_ok"] = e2_ok
    if not e2_ok:
        verdicts["halted_at"] = "F2"
        finish(results, t0)
        return

    log("E3: committed exp25 cells (membership, re-derivation, bounds)")
    exp25 = json.loads(EXP25_JSON.read_text(encoding="utf-8"))
    exp28 = json.loads(EXP28_JSON.read_text(encoding="utf-8"))
    exp29 = json.loads(EXP29_JSON.read_text(encoding="utf-8"))
    cutoff25 = int(exp25["cutoff"])
    box = float(exp25["bounded_dictionary"]["quad_norm_max"])
    bound_tref = float(exp29["E2"]["fidelity_bound"])
    bound_t11 = float(exp28["E2"]["fidelity_bound"])

    def target_vec(name):
        t = np.zeros((cutoff25, cutoff25), dtype=complex)
        if name == "t11":
            t[1, 1] = 1.0
        else:
            t[2, 0] = 0.8
            t[0, 3] = 0.6
        return t.ravel()

    max_gap, max_anorm3 = 0.0, 0.0
    membership_ok = True
    cells_checked = 0
    cell_rows = []
    for key, cell in exp25["cells"].items():
        tname, dtype, kpart = key.split("/")
        if dtype != "gaussian":
            continue
        cells_checked += 1
        x = np.asarray(cell["best_params"], dtype=float).reshape(-1, 10)
        vecs = []
        for row in x:
            l1, l2 = row[0] + 1j * row[1], row[2] + 1j * row[3]
            q11, q12, q22 = (
                row[4] + 1j * row[5], row[6] + 1j * row[7], row[8] + 1j * row[9],
            )
            A = np.array([[2 * q11, q12], [q12, 2 * q22]])
            max_anorm3 = max(max_anorm3, float(np.linalg.norm(A, 2)))
            if float(np.linalg.norm(A, 2)) > box:
                membership_ok = False
            st = gaussact.pq_state(np.array([[1.0 + 0j]]), A, np.array([l1, l2]))
            v = gaussact.fock_coeffs(st, cutoff25).ravel()
            vecs.append(v / float(np.linalg.norm(v)))
        # exp25's own estimator, end to end from best_params (run.py
        # `best_fidelity`): Gram + pinv projection of the target
        vecs = np.array(vecs)
        tvec = target_vec(tname)
        gram = np.conj(vecs) @ vecs.T
        h = np.conj(vecs) @ tvec
        zsol = np.linalg.pinv(gram, rcond=1e-12, hermitian=True) @ h
        fre = min(max(float(np.real(np.conj(h) @ zsol)), 0.0), 1.0)
        gap = abs(fre - float(cell["best_fidelity"]))
        max_gap = max(max_gap, gap)
        cell_rows.append({"cell": key, "refit_gap": gap})
    # descended-bound checks on committed measured values (A2)
    bound_rows, bound_violations = [], 0
    for key, bound, label in (
        ("trefoil/gaussian/K=1", bound_tref, "exp29"),
        ("trefoil/gaussian/K=2", bound_tref, "exp29"),
        ("trefoil/coherent/K=1", bound_tref, "exp29"),
        ("trefoil/coherent/K=2", bound_tref, "exp29"),
        ("t11/coherent/K=1", bound_t11, "exp28"),
        ("t11/coherent/K=2", bound_t11, "exp28"),
    ):
        measured = float(exp25["cells"][key]["best_fidelity"])
        ok = bool(measured <= bound)
        if not ok:
            bound_violations += 1
        bound_rows.append(
            {"cell": key, "measured": measured, "bound": bound,
             "bound_source": label, "within": ok}
        )
    e3_ok = bool(
        membership_ok and bound_violations == 0 and max_gap <= TOL_E3_F
    )
    results["E3"] = {
        "n_cells_checked": cells_checked,
        "cutoff": cutoff25,
        "quad_norm_max": box,
        "max_atom_A_norm": max_anorm3,
        "membership_ok": membership_ok,
        "max_fidelity_gap": max_gap,
        "cells": cell_rows,
        "bound_checks": bound_rows,
        "bound_violations": bound_violations,
        "t11_gaussian_k2_measured": float(
            exp25["cells"]["t11/gaussian/K=2"]["best_fidelity"]
        ),
    }
    verdicts["e3_cells_ok"] = e3_ok
    if not e3_ok:
        verdicts["halted_at"] = "F3"
        finish(results, t0)
        return

    log("E4: exact conversions and note-convention thresholds")
    identity_failures = 0
    for g in EPS_GRID_E4:
        # delta^2-grid leg: d2 -> F -> d2 (exact both ways)
        F = alignment.fidelity_of_delta_sq(g)
        if alignment.delta_sq_of_fidelity(F) != Fraction(g):
            identity_failures += 1
        # F-grid leg on the exact rational squares (k/50)^2
        Fsq = Fraction(g) ** 2
        d2 = alignment.delta_sq_of_fidelity(Fsq)
        if alignment.fidelity_of_delta_sq(d2) != Fsq:
            identity_failures += 1
    eps28 = float(exp28["E2"]["eps0_cert"])
    eps29 = float(exp29["E2"]["eps29_cert"])
    outward = bool(
        Fraction(bound_t11) >= (1 - Fraction(eps28) ** 2 / 2) ** 2
        and Fraction(bound_tref) >= (1 - Fraction(eps29) ** 2 / 2) ** 2
    )
    e4_ok = bool(identity_failures == 0 and outward)
    results["E4"] = {
        "identity_failures": identity_failures,
        "committed_bounds_outward": outward,
        "eps_note_trefoil": alignment.float_down(alignment.eps_note_exact(eps29)),
        "fidelity_bound_trefoil": bound_tref,
        "eps_note_t11": alignment.float_down(alignment.eps_note_exact(eps28)),
        "fidelity_bound_t11": bound_t11,
    }
    verdicts["e4_conversions_ok"] = e4_ok
    if not e4_ok:
        verdicts["halted_at"] = "F4"
    finish(results, t0)


if __name__ == "__main__":
    run()
