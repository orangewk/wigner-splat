"""Experiment 25 — topological K–ε curves (issue #137, Gate M).

Deterministically generates `topological_kcurves.json` (authoritative
artifact), `out_run.log`, and `topological_kcurves.png`. Predictions and
alarms are pre-declared in `plan.md` (PA/PB/PC/PD/PE); every verdict is
computed from measured data.

Per cell (target, dictionary, K): best-found fidelity via Fock-recursion
overlaps (exact in the truncated space) with multi-start Nelder-Mead over the
nonlinear term parameters, then a zero-link census of the best state with the
exp24 toolkit.
"""

from __future__ import annotations

import json
import math
import platform
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Pin the console stream: code-page consoles (e.g. CP932) must not abort the
# run on log typography; artifacts are UTF-8 regardless (PR #136 review).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from summary_block import write_into_readme  # noqa: E402

from wigner_splat.stellar2 import (  # noqa: E402
    TraceError,
    census,
    gaussian_sum_stellar,
    gaussian_term_fock_coeffs,
)

OUT = Path(__file__).resolve().parent
EXP24_JSON = OUT.parent / "24_hopf_stellar" / "hopf_link_results.json"
CUTOFF = 36
GRID = {"n_eta": 90, "n_xi": 96}
FIT_SEED = 20260731
QUAD_NORM_MAX = 0.98
TAIL_MAX = 1e-8
LOG_LINES: list[str] = []

K_RANGE = {"t11": (1, 2, 3, 4), "trefoil": (1, 2, 3, 4, 5, 6)}
PARAMS_PER_TERM = {"coherent": 4, "gaussian": 10}


def log(msg: str) -> None:
    print(msg)
    LOG_LINES.append(msg)


def target_vec(name):
    c = np.zeros((CUTOFF, CUTOFF), dtype=complex)
    if name == "t11":
        c[1, 1] = 1.0
    elif name == "trefoil":
        c[2, 0] = 0.8
        c[0, 3] = 0.6
    else:
        raise ValueError(name)
    return c.ravel()


def terms_from_params(x, dict_type):
    """Unit-z stellar terms from the real parameter vector (z is solved
    exactly through the Gram matrix, so it is not a search parameter)."""
    per = PARAMS_PER_TERM[dict_type]
    x = np.asarray(x, dtype=float).reshape(-1, per)
    terms = []
    for row in x:
        l1 = row[0] + 1j * row[1]
        l2 = row[2] + 1j * row[3]
        if dict_type == "coherent":
            q11 = q12 = q22 = 0.0
        else:
            q11 = row[4] + 1j * row[5]
            q12 = row[6] + 1j * row[7]
            q22 = row[8] + 1j * row[9]
        terms.append((1.0, l1, l2, q11, q12, q22))
    return terms


def term_invalid(term):
    """Penalty > 0 if the term leaves the bounded dictionary, else 0."""
    _, _, _, q11, q12, q22 = term
    a = np.array([[2 * q11, q12], [q12, 2 * q22]])
    smax = float(np.linalg.norm(a, 2))
    if smax >= QUAD_NORM_MAX:
        return 1.0 + smax
    return 0.0


def term_vectors(terms):
    """Normalized truncated Fock vectors; None + penalty if tail too heavy."""
    vecs = []
    for term in terms:
        pen = term_invalid(term)
        if pen:
            return None, pen
        c = gaussian_term_fock_coeffs(term, CUTOFF)
        total = float(np.sum(np.abs(c) ** 2))
        if not math.isfinite(total) or total == 0.0:
            return None, 2.5
        tail = float(np.sum(np.abs(c[-4:, :]) ** 2) + np.sum(np.abs(c[:, -4:]) ** 2))
        if tail / total > TAIL_MAX:
            return None, 1.0 + min(tail / total, 1.0)
        vecs.append(c.ravel() / math.sqrt(total))
    return np.array(vecs), 0.0


def best_fidelity(vecs, tvec):
    gram = np.conj(vecs) @ vecs.T
    h = np.conj(vecs) @ tvec
    z = np.linalg.pinv(gram, rcond=1e-12, hermitian=True) @ h
    fid = float(np.real(np.conj(h) @ z))
    return min(max(fid, 0.0), 1.0), z


def objective(x, dict_type, tvec):
    vecs, pen = term_vectors(terms_from_params(x, dict_type))
    if vecs is None:
        return pen
    try:
        fid, _ = best_fidelity(vecs, tvec)
    except np.linalg.LinAlgError:
        return 1.5
    if not math.isfinite(fid):
        return 1.5
    return -fid


def nelder_mead(fun, x0, iters=800, step=0.3, tol=1e-12):
    """Same minimal numpy-only Nelder-Mead as experiments/24_hopf_stellar."""
    n = len(x0)
    simplex = [np.array(x0, dtype=float)]
    for i in range(n):
        p = np.array(x0, dtype=float)
        p[i] += step
        simplex.append(p)
    vals = [fun(p) for p in simplex]
    for _ in range(iters):
        order = np.argsort(vals)
        simplex = [simplex[i] for i in order]
        vals = [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < tol:
            break
        centroid = np.mean(simplex[:-1], axis=0)
        xr = centroid + (centroid - simplex[-1])
        fr = fun(xr)
        if fr < vals[0]:
            xe = centroid + 2.0 * (centroid - simplex[-1])
            fe = fun(xe)
            simplex[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            simplex[-1], vals[-1] = xr, fr
        else:
            xc = centroid + 0.5 * (simplex[-1] - centroid)
            fc = fun(xc)
            if fc < vals[-1]:
                simplex[-1], vals[-1] = xc, fc
            else:
                for i in range(1, n + 1):
                    simplex[i] = simplex[0] + 0.5 * (simplex[i] - simplex[0])
                    vals[i] = fun(simplex[i])
    best = int(np.argmin(vals))
    return simplex[best], vals[best]


def pack(rows, per):
    x = np.zeros(len(rows) * per)
    for i, row in enumerate(rows):
        x[i * per : i * per + len(row)] = row
    return x


def structured_starts(target, dict_type, k):
    """Analytic seeds from the derivation-memo constructions."""
    per = PARAMS_PER_TERM[dict_type]
    starts = []
    if dict_type == "coherent":
        t = 0.7
        grids = {
            1: [[(t, t)]],
            2: [[(t, t), (-t, -t)], [(t, t), (t, -t)]],
            3: [[(t, t), (-t, -t), (t, -t)]],
            4: [[(t, t), (t, -t), (-t, t), (-t, -t)]],
            5: [[(t, t), (t, -t), (-t, t), (-t, -t), (0.0, 2 * t)]],
            6: [[(t, t), (t, -t), (-t, t), (-t, -t), (0.0, 2 * t), (0.0, -2 * t)]],
        }
        for pat in grids.get(k, []):
            rows = [[a, 0.0, b, 0.0] for a, b in pat]
            starts.append(pack(rows, per))
    else:
        # rows: l1re, l1im, l2re, l2im, q11re, q11im, q12re, q12im, q22re, q22im
        tmsv = lambda lam: [0, 0, 0, 0, 0, 0, lam, 0, 0, 0]  # noqa: E731
        sq1 = lambda a: [0, 0, 0, 0, a, 0, 0, 0, 0, 0]  # noqa: E731
        sq2l = lambda q, l: [0, 0, l, 0, 0, 0, 0, 0, q, 0]  # noqa: E731
        # squeezing seeds stay at 0.22: at cutoff 36 a 0.3 quadratic already
        # puts ~1.2e-8 of its mass in the tail band, just past TAIL_MAX
        if target == "t11":
            pats = {1: [[tmsv(0.5)]], 2: [[tmsv(0.4), tmsv(-0.4)]]}
        else:
            pats = {
                2: [[sq1(0.22), sq1(-0.22)]],
                4: [[sq1(0.22), sq1(-0.22), sq2l(0.22, 0.3), sq2l(0.22, -0.3)]],
                6: [
                    [
                        sq1(0.22),
                        sq1(-0.22),
                        sq2l(0.22, 0.3),
                        sq2l(0.22, -0.3),
                        sq2l(-0.22, 0.3),
                        sq2l(-0.22, -0.3),
                    ]
                ],
            }
        for pat in pats.get(k, []):
            starts.append(pack(pat, per))
    return starts


def fit_cell(target, dict_type, k, rng, warm_x):
    per = PARAMS_PER_TERM[dict_type]
    tvec = target_vec(target)
    def damp_quadratic(x, factor):
        # gaussian rows are (l re/im x2, q re/im x6). The tail budget at
        # cutoff 36 caps the quadratic operator norm near 0.56 (0.6^32 is
        # already ~8e-8 of mass in the tail band), so random starts must
        # begin with small squeezing to sit inside the bounded dictionary.
        if dict_type == "gaussian":
            x = x.reshape(-1, per).copy()
            x[:, 4:] *= factor
            return x.ravel()
        return x

    starts = structured_starts(target, dict_type, k)
    if warm_x is not None:
        new = damp_quadratic(rng.normal(scale=0.2, size=per), 0.25)
        starts.append(np.concatenate([warm_x, new]))
    for _ in range(6):
        starts.append(damp_quadratic(rng.normal(scale=0.4, size=k * per), 0.12))
    # only a finite, strictly valid best point (objective < 0, i.e. an actual
    # fidelity) may win: penalty plateaus from starts outside the bounded
    # dictionary must never contaminate the cell result
    best_x, best_v, n_valid = None, 0.0, 0
    for x0 in starts:
        try:
            x, v = nelder_mead(lambda x: objective(x, dict_type, tvec), x0)
        except np.linalg.LinAlgError:
            continue
        if not (isinstance(v, float) or isinstance(v, np.floating)):
            continue
        if not math.isfinite(v) or v >= 0.0:
            continue
        n_valid += 1
        if v < best_v:
            best_x, best_v = x, v
    if best_x is None:
        raise RuntimeError(
            f"no valid optimum in cell {target}/{dict_type}/K={k} "
            f"({len(starts)} starts, {n_valid} valid)"
        )
    terms = terms_from_params(best_x, dict_type)
    vecs, pen = term_vectors(terms)
    if vecs is None:
        raise RuntimeError(f"best point invalid in cell {target}/{dict_type}/K={k}")
    fid, z = best_fidelity(vecs, target_vec(target))
    norms = [
        math.sqrt(float(np.sum(np.abs(gaussian_term_fock_coeffs(t, CUTOFF)) ** 2)))
        for t in terms
    ]
    census_terms = [
        (zz / nn, *t[1:]) for zz, nn, t in zip(z, norms, terms)
    ]
    return fid, best_x, census_terms


def census_summary(terms):
    try:
        res = census(gaussian_sum_stellar(terms), **GRID)
    except TraceError as err:
        return {"census_failed": str(err)}
    windings = [c["windings"] for c in res["components"]]
    abs_w = [abs(w) for ws in windings for w in ws if w is not None]
    lk = np.array(res["linking_matrix"], dtype=int)
    n = lk.shape[0] if lk.size else 0
    offdiag = [int(lk[i, j]) for i in range(n) for j in range(i + 1, n)]
    return {
        "census": res,
        "n_components": len(windings),
        "winding_multiset": sorted(
            ["x" if w is None else str(w) for w in ws] for ws in windings
        ),
        "linking_offdiag": sorted(offdiag),
        "has_linked_pair": bool(any(v != 0 for v in offdiag)),
        "max_abs_winding": max(abs_w, default=0),
        "has_trefoil_windings": bool(
            any(sorted(abs(w) for w in ws if w is not None) == [2, 3] for ws in windings)
        ),
    }


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


def main():
    rng = np.random.default_rng(FIT_SEED)
    results = {
        "cutoff": CUTOFF,
        "grid": GRID,
        "fit_seed": FIT_SEED,
        "bounded_dictionary": {"quad_norm_max": QUAD_NORM_MAX, "tail_max": TAIL_MAX},
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": sys.platform,
            "machine": platform.machine(),
        },
        "cells": {},
    }

    for target in ("t11", "trefoil"):
        for dict_type in ("coherent", "gaussian"):
            warm = None
            for k in K_RANGE[target]:
                fid, best_x, cterms = fit_cell(target, dict_type, k, rng, warm)
                warm = best_x
                summ = census_summary(cterms)
                cell = {
                    "best_fidelity": fid,
                    "one_minus_F": 1.0 - fid,
                    "best_params": [float(v) for v in best_x],
                    "coeffs_z": [json_safe(complex(t[0])) for t in cterms],
                    **summ,
                }
                results["cells"][f"{target}/{dict_type}/K={k}"] = cell
                topo = (
                    summ.get("census_failed")
                    or f"comps={summ['n_components']} linked={summ['has_linked_pair']} "
                    f"maxw={summ['max_abs_winding']} trefoil={summ['has_trefoil_windings']}"
                )
                log(f"{target}/{dict_type}/K={k}: 1-F = {1-fid:.3e} | {topo}")

    cells = results["cells"]

    # A failed census makes every topology reading of that cell unknown, so
    # verdicts touching it must be None (indeterminate), never a clean pass
    # (PR #136 review). first-K transitions carry the failed-K list so an
    # earlier, unobserved transition is never silently ruled out.
    def topo(name, key):
        cell = cells[name]
        if "census_failed" in cell:
            return None
        return cell.get(key, False)

    def first_transition(target, dict_type, key):
        failed = []
        for k in K_RANGE[target]:
            flag = topo(f"{target}/{dict_type}/K={k}", key)
            if flag is None:
                failed.append(k)
            elif flag:
                return {"K": k, "indeterminate_below": failed}
        return {"K": None, "indeterminate_below": failed}

    mark_keys = {"t11": "has_linked_pair", "trefoil": "has_trefoil_windings"}
    ladders = {}
    for target in ("t11", "trefoil"):
        for dict_type in ("coherent", "gaussian"):
            ks = list(K_RANGE[target])
            gaps = [cells[f"{target}/{dict_type}/K={k}"]["one_minus_F"] for k in ks]
            factors = [
                gaps[i] / max(gaps[i + 1], 1e-15) for i in range(len(gaps) - 1)
            ]
            best = int(np.argmax(factors))
            ladders[f"{target}/{dict_type}"] = {
                "K": ks,
                "one_minus_F": gaps,
                "relative_step_factors_into_next_K": factors,
                "largest_relative_step_at_K": ks[best + 1],
                "largest_relative_step_factor": factors[best],
                "first_transition": first_transition(
                    target, dict_type, mark_keys[target]
                ),
            }
    results["ladders"] = ladders

    pa_link = topo("t11/gaussian/K=2", "has_linked_pair")
    pa_cell = cells["t11/gaussian/K=2"]
    pb_flags = [
        topo(f"{t}/coherent/K={k}", "has_linked_pair")
        for t in ("t11", "trefoil")
        for k in (1, 2)
    ]
    pc_windings = [
        None
        if "census_failed" in cells[f"{t}/gaussian/K=2"]
        else cells[f"{t}/gaussian/K=2"]["max_abs_winding"]
        for t in ("t11", "trefoil")
    ]
    verdicts = {
        "pa_11_gauss_k2_reaches_target_with_hopf_link": None
        if pa_link is None
        else bool(
            pa_cell["best_fidelity"] >= 0.999
            and pa_link
            and pa_cell.get("n_components") == 2
        ),
        "pb_all_coherent_k_le_2_unlinked": None
        if any(f is None for f in pb_flags)
        else not any(pb_flags),
        "pc_all_gaussian_k2_max_winding_le_2": None
        if any(w is None for w in pc_windings)
        else all(w <= 2 for w in pc_windings),
        "pd_first_linked_K": {
            f"t11/{d}": ladders[f"t11/{d}"]["first_transition"]
            for d in ("coherent", "gaussian")
        },
        "pd_first_trefoil_winding_K": {
            f"trefoil/{d}": ladders[f"trefoil/{d}"]["first_transition"]
            for d in ("coherent", "gaussian")
        },
        "pe_trefoil_gauss_k6_fidelity": cells["trefoil/gaussian/K=6"]["best_fidelity"],
        "census_failures": sorted(
            name for name, c in cells.items() if "census_failed" in c
        ),
    }
    if verdicts["census_failures"]:
        log(
            "census failures present: "
            + ", ".join(verdicts["census_failures"])
            + " — affected verdicts are indeterminate (None), not passes"
        )

    # cross-check against exp24 E4 (independent machinery: closed-form
    # overlaps there, truncated Fock recursion here)
    if EXP24_JSON.exists():
        e4 = json.loads(EXP24_JSON.read_text(encoding="utf-8"))["E4"]
        diffs = {
            f"K={k}": abs(
                e4[f"K={k}"]["best_fidelity"]
                - cells[f"t11/coherent/K={k}"]["best_fidelity"]
            )
            for k in (1, 2, 3, 4)
        }
        verdicts["crosscheck_exp24_e4_max_abs_diff"] = max(diffs.values())
        verdicts["crosscheck_exp24_e4_consistent"] = bool(
            max(diffs.values()) < 1e-3
        )
    results["verdicts"] = verdicts
    log("verdicts: " + json.dumps(json_safe(verdicts), sort_keys=True))

    # figure: two panels of 1-F vs K, topology transitions annotated
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    for ax, target, marker_key, marker_label in (
        (axes[0], "t11", "has_linked_pair", "linked pair"),
        (axes[1], "trefoil", "has_trefoil_windings", "(3,2) winding"),
    ):
        for dict_type, style, color in (
            ("coherent", "o-", "C0"),
            ("gaussian", "s--", "C1"),
        ):
            ks = list(K_RANGE[target])
            gaps = [
                max(cells[f"{target}/{dict_type}/K={k}"]["one_minus_F"], 1e-9)
                for k in ks
            ]
            ax.semilogy(ks, gaps, style, color=color, label=dict_type)
            for k, gap in zip(ks, gaps):
                if cells[f"{target}/{dict_type}/K={k}"].get(marker_key):
                    ax.plot(
                        [k], [gap], ls="", marker="*", ms=14,
                        mfc="none", mec="k", color="k",
                    )
        ax.set_xlabel("terms K")
        ax.set_ylabel("1 - best-found fidelity")
        title = "|1,1>" if target == "t11" else "0.8|20>+0.6|03> (trefoil)"
        ax.set_title(f"{title} — star = {marker_label} in census", fontsize=10)
        ax.set_xticks(list(K_RANGE[target]))
        ax.legend()
    fig.suptitle("Topological K-epsilon curves (best-found, experiment 25)", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / "topological_kcurves.png", dpi=160)
    plt.close(fig)

    log("artifacts: topological_kcurves.json, out_run.log, "
        "topological_kcurves.png, README generated block")
    (OUT / "topological_kcurves.json").write_text(
        json.dumps(json_safe(results), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "out_run.log").write_text("\n".join(LOG_LINES) + "\n", encoding="utf-8")
    write_into_readme(OUT / "README.md", json_safe(results))


if __name__ == "__main__":
    main()
