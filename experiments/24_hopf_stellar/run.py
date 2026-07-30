"""Experiment 24 — stellar zero links on the phase-space 3-sphere.

Deterministically generates `hopf_link_results.json` (the authoritative
artifact: every number and verdict cited elsewhere is authored here),
`out_run.log`, and two figures. The predictions being tested are pre-declared
in `derivation.md` (P1-P6, R1, Q1); every verdict below is COMPUTED by
comparing measured census data against the encoded expectation — no verdict
string is hard-coded.

Sections:
  E1  tracker validation on states with proved zero links (P1/P2)
  E2  knot ladder: three-chain and trefoil windings (P6/R1 targets)
  E3  dictionary probes: TMSV odd cats (P4), a smooth conic pair (P4b),
      cat (x) cat with geometrically predicted satellite linking (P3 logic)
  E4  coherent-dictionary fit ladder K=1..4 against |11> (P5 numeric, Q1)
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from wigner_splat.stellar2 import (  # noqa: E402
    census,
    coherent_term,
    fock_stellar,
    gaussian_sum_stellar,
    tmsv_term,
)

OUT = Path(__file__).resolve().parent
GRID = {"n_eta": 90, "n_xi": 96}
FIT_SEED = 20260730
LOG_LINES: list[str] = []


def log(msg: str) -> None:
    print(msg)
    LOG_LINES.append(msg)


def fock(entries, shape):
    c = np.zeros(shape, dtype=complex)
    for (m, n), v in entries.items():
        c[m, n] = v
    return fock_stellar(c)


def winding_multiset(res):
    """Canonical winding multiset; entries stringified ('x' = undefined,
    the component runs along that core) so mixed lists sort deterministically."""
    return sorted(
        ["x" if w is None else str(w) for w in comp["windings"]]
        for comp in res["components"]
    )


def offdiag_multiset(res):
    lk = np.array(res["linking_matrix"], dtype=int)
    n = lk.shape[0] if lk.size else 0
    return sorted(int(lk[i, j]) for i in range(n) for j in range(i + 1, n))


def summarize(res):
    return {
        "n_components": len(res["components"]),
        "windings": winding_multiset(res),
        "linking_offdiag": offdiag_multiset(res),
    }


def strip_loops(res):
    return {k: v for k, v in res.items() if k != "loops_r3"}


def has_linked_pair(res):
    return any(v != 0 for v in offdiag_multiset(res))


# ---------------------------------------------------------------------------
# E4 machinery: best coherent-K fidelity to |11> (closed-form overlaps)
# ---------------------------------------------------------------------------

def coherent_overlap_matrix(g):
    """Gram matrix of two-mode coherent states, rows/cols = kets."""
    g1, g2 = g[:, 0], g[:, 1]
    n2 = np.abs(g1) ** 2 + np.abs(g2) ** 2
    return np.exp(
        np.conj(g1)[:, None] * g1[None, :]
        + np.conj(g2)[:, None] * g2[None, :]
        - (n2[:, None] + n2[None, :]) / 2.0
    )


def overlap_with_11(g):
    """<g1,g2|1,1> = conj(g1) conj(g2) exp(-(|g1|^2+|g2|^2)/2)."""
    g1, g2 = g[:, 0], g[:, 1]
    return np.conj(g1) * np.conj(g2) * np.exp(-(np.abs(g1) ** 2 + np.abs(g2) ** 2) / 2.0)


def best_fidelity(g):
    """max_z |<11|sum z_k g_k>|^2 / ||sum z_k g_k||^2 = h^dag G^+ h."""
    gram = coherent_overlap_matrix(g)
    h = overlap_with_11(g)
    z = np.linalg.pinv(gram, rcond=1e-12, hermitian=True) @ h
    fid = float(np.real(np.conj(h) @ z))
    return min(max(fid, 0.0), 1.0), z


def params_to_kets(x):
    x = np.asarray(x, dtype=float).reshape(-1, 4)
    return x[:, 0] + 1j * x[:, 1], x[:, 2] + 1j * x[:, 3]


def objective(x):
    g1, g2 = params_to_kets(x)
    fid, _ = best_fidelity(np.stack([g1, g2], axis=1))
    return -fid


def nelder_mead(fun, x0, iters=800, step=0.3, tol=1e-12):
    """Minimal numpy-only Nelder-Mead (no scipy in this repo's baseline)."""
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


def structured_starts(k, rng):
    """Analytic seeds (cat-derivative patterns) plus random starts."""
    starts = []
    t = 0.7
    patterns = {
        1: [[(t, t)]],
        2: [[(t, t), (-t, -t)], [(t, t), (t, -t)]],
        3: [[(t, t), (-t, -t), (t, -t)], [(t, t), (t * 1j, -t * 1j), (-t, -t)]],
        4: [[(t, t), (t, -t), (-t, t), (-t, -t)]],
    }
    for pat in patterns.get(k, []):
        x = []
        for a, b in pat:
            x += [np.real(a), np.imag(a), np.real(b), np.imag(b)]
        starts.append(np.array(x))
    for _ in range(10):
        starts.append(rng.normal(scale=0.8, size=4 * k))
    return starts


def fit_coherent_k(k, rng):
    best_x, best_f = None, 1.0
    for x0 in structured_starts(k, rng):
        x, fval = nelder_mead(objective, x0)
        if fval < best_f:
            best_x, best_f = x, fval
    g1, g2 = params_to_kets(best_x)
    fid, z = best_fidelity(np.stack([g1, g2], axis=1))
    return fid, g1, g2, z


# ---------------------------------------------------------------------------
# expectation checks (proved rows of derivation.md, encoded as data)
# ---------------------------------------------------------------------------

HOPF_EXPECT = {
    "n_components": 2,
    "windings": sorted([["1", "x"], ["x", "1"]]),
    "linking_offdiag": [1],
}


def check(measured, expected):
    return {
        "expected": expected,
        "measured": measured,
        "match": bool(measured == expected),
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
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    return obj


def main():
    results = {"grid": GRID, "fit_seed": FIT_SEED}
    figures = {}

    # ---------------- E1: validation on proved links ----------------
    log("== E1: tracker validation (P1/P2) ==")
    f11 = fock({(1, 1): 1.0}, (2, 2))
    e1 = {}
    r = census(f11, **GRID, frame_seed=0, return_loops=True)
    figures["|1,1>"] = r["loops_r3"]
    e1["state_11_frameA"] = strip_loops(r)
    e1["check_11_frameA"] = check(summarize(r), HOPF_EXPECT)
    r2 = census(f11, **GRID, frame_seed=100)
    e1["state_11_frameB"] = r2
    e1["check_11_frameB"] = check(summarize(r2), HOPF_EXPECT)

    r = census(fock({(1, 0): 1.0, (0, 1): 1.0}, (2, 2)), **GRID)
    e1["state_10_plus_01"] = r
    e1["check_10_plus_01"] = check(
        summarize(r),
        {"n_components": 1, "windings": [["1", "1"]], "linking_offdiag": []},
    )

    r = census(fock({(2, 0): 1.0, (0, 2): 1.0}, (3, 3)), **GRID, return_loops=True)
    figures["|2,0>+|0,2>"] = r["loops_r3"]
    e1["state_20_plus_02"] = strip_loops(r)
    e1["check_20_plus_02"] = check(
        summarize(r),
        {
            "n_components": 2,
            "windings": [["1", "1"], ["1", "1"]],
            "linking_offdiag": [1],
        },
    )
    results["E1"] = e1
    e1_ok = all(v["match"] for k, v in e1.items() if k.startswith("check"))
    log(f"E1 verdict: {'MATCH — tracker validated' if e1_ok else 'MISMATCH — F1 fires, halt'}")
    results["verdicts"] = {"e1_tracker_validated": e1_ok}
    if not e1_ok:
        finish(results, figures)
        raise SystemExit("F1: tracker falsified on validation states")

    # ---------------- E2: knot ladder ----------------
    log("== E2: knot ladder ==")
    e2 = {}
    r = census(fock({(3, 0): 1.0, (0, 3): 1.0}, (4, 4)), **GRID, return_loops=True)
    figures["|3,0>+|0,3>"] = r["loops_r3"]
    e2["state_30_plus_03"] = strip_loops(r)
    e2["check_three_chain"] = check(
        summarize(r),
        {
            "n_components": 3,
            "windings": [["1", "1"], ["1", "1"], ["1", "1"]],
            "linking_offdiag": [1, 1, 1],
        },
    )
    r = census(fock({(2, 0): 0.8, (0, 3): 0.6}, (3, 4)), **GRID, return_loops=True)
    figures["0.8|2,0>+0.6|0,3> (trefoil)"] = r["loops_r3"]
    e2["state_trefoil"] = strip_loops(r)
    e2["check_trefoil"] = check(
        {
            "n_components": len(r["components"]),
            "winding_magnitudes": sorted(
                sorted(abs(w) for w in c["windings"]) for c in r["components"]
            ),
        },
        {"n_components": 1, "winding_magnitudes": [[2, 3]]},
    )
    results["E2"] = e2
    e2_ok = all(v["match"] for k, v in e2.items() if k.startswith("check"))
    log(f"E2 verdict: {'MATCH vs P6/R1 predictions' if e2_ok else 'MISMATCH vs P6/R1'}")
    results["verdicts"]["e2_knot_ladder_matches"] = e2_ok

    # ---------------- E3: dictionary probes ----------------
    log("== E3: dictionary probes ==")
    e3 = {"tmsv_odd_cat": {}}
    for lam in (0.3, 0.6, 0.9):
        f = gaussian_sum_stellar([tmsv_term(lam), tmsv_term(-lam, z=-1.0)])
        r = census(f, **GRID)
        # closed-form fidelity (P4) and an independent Fock-truncation check
        fid_closed = 1.0 - lam**4
        n = np.arange(1, 200, 2)
        fid_series = float(lam ** (2 * n[0]) / np.sum(lam ** (2 * n)) * 1.0)
        entry = {
            "census": r,
            "check_link": check(summarize(r), HOPF_EXPECT),
            "fidelity_to_11_closed_form": fid_closed,
            "fidelity_to_11_fock_series": fid_series,
            "fidelity_formulas_agree": bool(
                math.isclose(fid_closed, fid_series, rel_tol=1e-10)
            ),
        }
        e3["tmsv_odd_cat"][str(lam)] = entry
        log(
            f"TMSV odd cat lam={lam}: link "
            f"{'= Hopf' if entry['check_link']['match'] else 'MISMATCH'}, "
            f"F(|11>) = {fid_closed:.4f}"
        )

    lam, phi = 0.85, 0.35
    f = gaussian_sum_stellar([tmsv_term(lam), tmsv_term(-lam, z=-np.exp(1j * phi))])
    r = census(f, **GRID, return_loops=True)
    figures[f"T({lam}) - e^(i {phi}) T(-{lam})"] = r["loops_r3"]
    e3["generic_tmsv_cat"] = {
        "lam": lam,
        "phi": phi,
        "census": strip_loops(r),
        "check_p4b": check(
            summarize(r),
            {
                "n_components": 2,
                "windings": sorted([["-1", "1"], ["1", "-1"]]),
                "linking_offdiag": [1],
            },
        ),
    }
    log(
        "generic TMSV cat conic pair: "
        f"{'windings (±1,∓1), lk +1 as P4b proves' if e3['generic_tmsv_cat']['check_p4b']['match'] else 'MISMATCH vs P4b'}"
    )

    # cat (x) cat with satellites: geometric prediction computed from levels
    t = 3.5
    f = gaussian_sum_stellar(
        [
            coherent_term(t, t),
            coherent_term(t, -t, z=-1.0),
            coherent_term(-t, t, z=-1.0),
            coherent_term(-t, -t),
        ]
    )
    r = census(f, **GRID, return_loops=True)
    figures[f"cat(x)cat t={t}"] = r["loops_r3"]
    sat = math.pi / (2 * t) * 2.0  # satellite line offset |c| = pi/t
    # class of each component from its windings; predicted lk per class pair
    # from where the corresponding complex lines intersect (P1/P3 geometry):
    # core1 {w1=0} vs core2 {w2=0}: meet at origin (inside) -> 1
    # core_i vs same-mode satellite: parallel lines -> 0
    # core1 vs {w2=c}: meet at (0, c), |c| < 1 -> 1 (and symmetrically)
    # {w1=c} vs {w2=c'}: meet at (c, c'), norm^2 = 2 sat^2 vs 1
    cls = {(None, 1): "core1", (1, None): "core2", (0, 1): "sat1", (1, 0): "sat2"}
    pred = {
        frozenset(["core1", "core2"]): 1,
        frozenset(["core1", "sat1"]): 0,
        frozenset(["core2", "sat2"]): 0,
        frozenset(["core1", "sat2"]): 1 if sat < 1.0 else 0,
        frozenset(["core2", "sat1"]): 1 if sat < 1.0 else 0,
        frozenset(["sat1", "sat1"]): 0,
        frozenset(["sat2", "sat2"]): 0,
        frozenset(["sat1", "sat2"]): 1 if 2 * sat**2 < 1.0 else 0,
    }
    labels = [cls.get(tuple(c["windings"])) for c in r["components"]]
    lk = np.array(r["linking_matrix"], dtype=int)
    catcat_ok = None not in labels
    mismatches = []
    if catcat_ok:
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                want = pred[frozenset([labels[i], labels[j]])]
                if int(lk[i, j]) != want:
                    mismatches.append([labels[i], labels[j], int(lk[i, j]), want])
        catcat_ok = not mismatches
    e3["cat_x_cat"] = {
        "t": t,
        "satellite_offset": sat,
        "census": strip_loops(r),
        "component_classes": labels,
        "prediction_mismatches": mismatches,
        "check_geometry": {"match": bool(catcat_ok)},
    }
    log(
        f"cat(x)cat t={t}: {len(labels)} components "
        f"({'geometry pattern MATCH' if catcat_ok else 'geometry MISMATCH'})"
    )
    results["E3"] = e3
    e3_ok = (
        all(v["check_link"]["match"] for v in e3["tmsv_odd_cat"].values())
        and all(v["fidelity_formulas_agree"] for v in e3["tmsv_odd_cat"].values())
        and e3["generic_tmsv_cat"]["check_p4b"]["match"]
        and bool(catcat_ok)
    )
    results["verdicts"]["e3_dictionary_probes_match"] = e3_ok
    log(f"E3 verdict: {'MATCH vs P3/P4/P4b' if e3_ok else 'MISMATCH'}")

    # ---------------- E4: coherent fit ladder ----------------
    log("== E4: coherent-dictionary fit ladder vs |11> ==")
    rng = np.random.default_rng(FIT_SEED)
    e4 = {}
    for k in (1, 2, 3, 4):
        fid, g1, g2, z = fit_coherent_k(k, rng)
        terms = [coherent_term(a, b, z=zz) for a, b, zz in zip(g1, g2, z)]
        f = gaussian_sum_stellar(terms)
        r = census(f, **GRID)
        linked = has_linked_pair(r)
        e4[f"K={k}"] = {
            "best_fidelity": fid,
            "kets_g1": [json_safe(complex(a)) for a in g1],
            "kets_g2": [json_safe(complex(b)) for b in g2],
            "coeffs_z": [json_safe(complex(zz)) for zz in z],
            "census": r,
            "linked_pair_found": linked,
        }
        log(
            f"K={k}: best fidelity {fid:.6f}, 1-F = {1-fid:.3e}, "
            f"{len(r['components'])} zero components, "
            f"linked pair: {linked}"
        )
    k2_linked = e4["K=2"]["linked_pair_found"]
    k3_linked = e4["K=3"]["linked_pair_found"]
    results["E4"] = e4
    results["verdicts"]["e4_k2_no_linked_pair_as_P3_proves"] = not k2_linked
    results["verdicts"]["e4_k3_linked_pair_found_Q1"] = bool(k3_linked)
    if k2_linked:
        log("F2 ALARM: K=2 coherent census shows a linked pair; P3 is proved, so this is a tool/proof defect.")
    gap_line = (
        f"E4 summary: 1-F at K=1..4 = "
        + ", ".join(f"{1 - e4[f'K={k}']['best_fidelity']:.3e}" for k in (1, 2, 3, 4))
        + f"; Q1 (K=3 linked pair): {k3_linked}"
    )
    log(gap_line)

    finish(results, figures)


def finish(results, figures):
    # figure 1: stereographic zero links
    keys = list(figures)
    if keys:
        fig = plt.figure(figsize=(13, 8))
        for idx, key in enumerate(keys[:6]):
            ax = fig.add_subplot(2, 3, idx + 1, projection="3d")
            for loop in figures[key]:
                closed = np.vstack([loop, loop[:1]])
                ax.plot(closed[:, 0], closed[:, 1], closed[:, 2], lw=1.2)
            ax.set_title(key, fontsize=9)
            ax.set_axis_off()
        fig.suptitle(
            "Stellar zero links on S^3 (stereographic projections), experiment 24",
            fontsize=11,
        )
        fig.tight_layout()
        fig.savefig(OUT / "stellar_links_s3.png", dpi=160)
        plt.close(fig)

    # figure 2: coherent fit ladder (only if E4 ran)
    if "E4" in results:
        ks = [1, 2, 3, 4]
        gaps = [1 - results["E4"][f"K={k}"]["best_fidelity"] for k in ks]
        linked = [results["E4"][f"K={k}"]["linked_pair_found"] for k in ks]
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        ax.semilogy(ks, gaps, "o-")
        for k, gap, ln in zip(ks, gaps, linked):
            ax.annotate(
                "linked pair" if ln else "no linked pair",
                (k, gap),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=8,
            )
        ax.set_xticks(ks)
        ax.set_xlabel("coherent terms K")
        ax.set_ylabel("1 - best fidelity to |1,1>")
        ax.set_title("Coherent-dictionary fit ladder (E4), best of multi-start")
        fig.tight_layout()
        fig.savefig(OUT / "coherent_fit_ladder.png", dpi=160)
        plt.close(fig)

    log("artifacts: hopf_link_results.json, out_run.log, "
        "stellar_links_s3.png, coherent_fit_ladder.png")
    (OUT / "hopf_link_results.json").write_text(
        json.dumps(json_safe(results), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "out_run.log").write_text("\n".join(LOG_LINES) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
