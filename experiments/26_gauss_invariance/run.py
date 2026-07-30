"""Experiment 26 — Gaussian-group action on stellar zero links (issue #137,
Gate T′ slice 1).

Deterministically generates `gauss_invariance.json` (the authoritative
artifact), `out_run.log`, and `gauss_links.png`. The propositions, E-series
grids/seeds/thresholds (§5), and falsification gates F1–F5 (§6) are
pre-declared in `derivation.md`; every verdict below is COMPUTED by comparing
measured data against the encoded expectation — no verdict string is
hard-coded.

Sections:
  E1  transformer machinery gate: G1 constant + truncated-Fock brute force
      (F1 gate for everything downstream)
  E2  fixed-radius threshold scan of squeeze2(|1,1>) at radius 1 (G2/F2)
  E3  radius restoration at lam = 0.5 (G2/F2)
  E4  top-form partition of seeded Gaussian orbits (G3/F3)
  E5  large-radius censuses of orbit images vs the G4 sketch (F4: no halt)
  E6  adversarial multi-start probe of Gaussian |2,0> <-> |1,1> (G5/F5)
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

from wigner_splat.gaussact import (  # noqa: E402
    GaussActError,
    fock_coeffs,
    gauss_unitary,
    norm,
    passive,
    pq_state,
    random_gauss_params,
    squeeze2,
    stellar_callable,
    top_partition,
)
from wigner_splat.stellar2 import TraceError, census, rotated  # noqa: E402

OUT = Path(__file__).resolve().parent
FIT_SEED = 20260731
BRUTE_CUTOFF = 36
BRUTE_SEED = 100
BRUTE_TOL = 1e-6
PASSIVE_TOL = 1e-10
PASSIVE_POINT_SEED = 11  # sample points only; any fixed seed, recorded here
G1_TOL = 1e-12
E2_LAMS = (0.30, 0.35, 0.40, 0.43, 0.46, 0.50, 0.60)
E4_FAMILIES = (
    ("t11", range(100, 108), (1, 1)),
    ("t20", range(200, 208), (2,)),
    ("trefoil", range(300, 308), (3,)),
)
E4_TOL = 1e-3   # np.roots scatters an exact triple root by ~6e-6 (measured
E4_MARGIN = 1e-2  # in tests/test_gaussact.py); margin < 10x tol = indeterminate
E5_GRID = {"n_eta": 120, "n_xi": 128}
E5_RADII = (2.5, 3.0)
E6_ALARM = 1e-6
LOG_LINES: list[str] = []


def log(msg: str) -> None:
    print(msg)
    LOG_LINES.append(msg)


# ---------------------------------------------------------------------------
# input states (monomial-basis P arrays; asserted against fock_coeffs in E1)
# ---------------------------------------------------------------------------

def state_11():
    p = np.zeros((2, 2), dtype=complex)
    p[1, 1] = 1.0
    return pq_state(p)


def state_20():
    p = np.zeros((3, 1), dtype=complex)
    p[2, 0] = 1.0 / math.sqrt(2.0)
    return pq_state(p)


def state_trefoil():
    p = np.zeros((3, 4), dtype=complex)
    p[2, 0] = 0.8 / math.sqrt(2.0)
    p[0, 3] = 0.6 / math.sqrt(6.0)
    return pq_state(p)


STATE_MAKERS = {"t11": state_11, "t20": state_20, "trefoil": state_trefoil}
EXPECTED_FOCK = {
    "t11": {(1, 1): 1.0},
    "t20": {(2, 0): 1.0},
    "trefoil": {(2, 0): 0.8, (0, 3): 0.6},
}


# ---------------------------------------------------------------------------
# census readouts (exp24 helpers)
# ---------------------------------------------------------------------------

def offdiag_multiset(res):
    lk = np.array(res["linking_matrix"], dtype=int)
    n = lk.shape[0] if lk.size else 0
    return sorted(int(lk[i, j]) for i in range(n) for j in range(i + 1, n))


def winding_multiset(res):
    """Canonical winding multiset; entries stringified ('x' = undefined,
    the component runs along that core) so mixed lists sort deterministically."""
    return sorted(
        ["x" if w is None else str(w) for w in comp["windings"]]
        for comp in res["components"]
    )


def strip_loops(res):
    return {k: v for k, v in res.items() if k != "loops_r3"}


def make_panel(label, res):
    """Figure panel dict. The title carries only measured census numbers
    (counts/linking read from the census dict), never a conclusion word."""
    n = len(res["components"])
    off = offdiag_multiset(res)
    title = f"{label}\nr = {res['radius']:.3f}: {n} components, lk offdiag {off}"
    loops = res.get("loops_r3") or []
    text = None if loops else f"{n} zero components\non this sphere"
    return {"title": title, "loops": loops, "text": text}


def predicted_link(c_lam, radius):
    """G2 geometry, computed per cell: the conic w1 w2 = c meets S3_radius iff
    |c| <= radius^2/2 (AM-GM); below the threshold the link is the two-circle
    +1 pattern (24/P4b), above it is empty."""
    if c_lam > radius * radius / 2.0:
        return 0, []
    return 2, [1]


def aggregate(flags):
    """False if any cell mismatches; None if none mismatch but some are
    indeterminate; True only when every cell matched."""
    if any(f is False for f in flags):
        return False
    if any(f is None for f in flags):
        return None
    return True


def cell_word(v):
    if v is None:
        return "INDETERMINATE"
    return "match" if v else "MISMATCH"


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


# ---------------------------------------------------------------------------
# E1: transformer machinery gate (F1)
# ---------------------------------------------------------------------------

def _brute_apply(x, vecs):
    """exp(x) @ vecs for anti-Hermitian x, via eigh of the Hermitian i x
    (symmetrized to kill truncation asymmetry); never forms the expm matrix."""
    h = 1j * x
    h = (h + h.conj().T) / 2.0
    w, v = np.linalg.eigh(h)
    return v @ (np.exp(-1j * w)[:, None] * (v.conj().T @ vecs))


def run_e1(results):
    e1 = {}

    # (a) G1 constant: -(P'[0,0]/P'[1,1]) must equal sinh(r) cosh(r)
    g1_cells = []
    for lam in (0.3, 0.5):
        r = math.atanh(lam)
        out = squeeze2(state_11(), r)
        sc = math.sinh(r) * math.cosh(r)
        rel = abs(-(out.P[0, 0] / out.P[1, 1]) - sc) / sc
        g1_cells.append({"lam": lam, "rel_err_vs_sinh_cosh": float(rel)})
        log(f"E1a lam={lam}: G1 constant rel err = {rel:.3e}")
    e1["g1_constant_cells"] = g1_cells
    e1["g1_tol"] = G1_TOL
    e1["g1_ok"] = bool(
        all(c["rel_err_vs_sinh_cosh"] <= G1_TOL for c in g1_cells)
    )

    # E0-style input sanity: the monomial P arrays must be the claimed kets
    fock_errs = {}
    for name, maker in STATE_MAKERS.items():
        expect = np.zeros((6, 6), dtype=complex)
        for (m, n), v in EXPECTED_FOCK[name].items():
            expect[m, n] = v
        got = fock_coeffs(maker(), 6)
        fock_errs[name] = float(np.max(np.abs(got - expect)))
    e1["input_fock_max_abs_err"] = fock_errs
    e1["input_fock_ok"] = bool(all(v <= 1e-12 for v in fock_errs.values()))

    # (b) truncated-Fock brute force, cutoff 36, seeded Gaussian. The passive
    # factors are validated separately below (against stellar2.rotated, which
    # is exact), so the brute-force chain runs the params with U_pre/U_post
    # replaced by identity — same simplification as tests/test_gaussact.py T3,
    # which validates factors, not full products.
    params = random_gauss_params(BRUTE_SEED)
    params_np = dict(params)
    params_np["U_pre"] = None
    params_np["U_post"] = None
    n = BRUTE_CUTOFF
    am = np.diag(np.sqrt(np.arange(1.0, n)), 1)  # a|n> = sqrt(n)|n-1>
    ad = am.T
    eye = np.eye(n)

    def sq(z):
        return 0.5 * (z * ad @ ad - np.conj(z) * am @ am)

    def dsp(a):
        return a * ad - np.conj(a) * am

    # factor order matches gauss_unitary's docstring (state sees squeeze1
    # mode 0 first, then mode 1, squeeze2, displace); mode 1 is the first
    # kron factor so index layout m*n + n matches reshape
    chain = [
        np.kron(sq(params["zeta1"]), eye),
        np.kron(eye, sq(params["zeta2"])),
        params["zeta12"] * np.kron(ad, ad)
        - np.conj(params["zeta12"]) * np.kron(am, am),
        np.kron(dsp(params["alpha"][0]), eye)
        + np.kron(eye, dsp(params["alpha"][1])),
    ]
    brute_states = [("t11", state_11()), ("trefoil", state_trefoil())]
    vecs = np.stack(
        [fock_coeffs(st, n).reshape(-1) for _, st in brute_states], axis=1
    )
    for x in chain:
        vecs = _brute_apply(x, vecs)
    brute_rels = {}
    for col, (name, st) in enumerate(brute_states):
        got = vecs[:, col].reshape(n, n)[:9, :9]
        want = fock_coeffs(gauss_unitary(st, params_np), 9)
        brute_rels[name] = float(
            np.max(np.abs(got - want)) / np.max(np.abs(want))
        )
        log(f"E1b brute force ({name}): max rel diff = {brute_rels[name]:.3e}")
    e1["bruteforce_cutoff"] = n
    e1["bruteforce_seed"] = BRUTE_SEED
    e1["bruteforce_tol"] = BRUTE_TOL
    e1["bruteforce_max_rel_diff"] = brute_rels
    e1["bruteforce_ok"] = bool(all(v <= BRUTE_TOL for v in brute_rels.values()))

    # passive-only value comparison against stellar2.rotated (exact reference)
    rng = np.random.default_rng(PASSIVE_POINT_SEED)
    w1 = 0.9 * (rng.normal(size=8) + 1j * rng.normal(size=8))
    w2 = 0.9 * (rng.normal(size=8) + 1j * rng.normal(size=8))
    passive_rels = {}
    for name, st in brute_states:
        row = {}
        for uname in ("U_pre", "U_post"):
            u = params[uname]
            got = stellar_callable(passive(st, u))(w1, w2)
            want = rotated(stellar_callable(st), u)(w1, w2)
            row[uname] = float(np.max(np.abs(got - want)) / np.max(np.abs(want)))
        passive_rels[name] = row
    e1["passive_point_seed"] = PASSIVE_POINT_SEED
    e1["passive_tol"] = PASSIVE_TOL
    e1["passive_max_rel_diff"] = passive_rels
    e1["passive_ok"] = bool(
        all(v <= PASSIVE_TOL for row in passive_rels.values() for v in row.values())
    )

    ok = bool(
        e1["g1_ok"] and e1["input_fock_ok"] and e1["bruteforce_ok"] and e1["passive_ok"]
    )
    results["E1"] = e1
    results["verdicts"]["e1_transformer_validated"] = ok
    log(
        "E1 verdict: "
        + ("MATCH — transformer validated" if ok else "MISMATCH — F1 fires, halt")
    )
    return ok


# ---------------------------------------------------------------------------
# E2/E3: fixed-radius threshold and restoration (G2, F2)
# ---------------------------------------------------------------------------

def _census_cell(state, radius, grid, c_lam, want_loops, fail_tag,
                 figures, figure_label, census_failures):
    pn, poff = predicted_link(c_lam, radius)
    cell = {
        "c_lam": c_lam,
        "radius": radius,
        "predicted_n_components": pn,
        "predicted_linking_offdiag": poff,
    }
    try:
        res = census(
            stellar_callable(state), radius=radius, **grid,
            return_loops=want_loops,
        )
    except TraceError as err:
        cell["census_failed"] = str(err)
        cell["matches_prediction"] = None
        census_failures.append(fail_tag)
        return cell
    if want_loops:
        figures.append(make_panel(figure_label, res))
        res = strip_loops(res)
    mn = len(res["components"])
    moff = offdiag_multiset(res)
    cell["census"] = res
    cell["measured_n_components"] = mn
    cell["measured_linking_offdiag"] = moff
    cell["matches_prediction"] = bool((mn, moff) == (pn, poff))
    return cell


def run_e2(results, figures, census_failures):
    cells = []
    for lam in E2_LAMS:
        st = squeeze2(state_11(), math.atanh(lam))
        c = lam / (1.0 - lam * lam)
        cell = _census_cell(
            st, 1.0, {}, c, lam in (0.30, 0.50), f"E2/lam={lam:.2f}",
            figures, f"E2: squeeze2(|1,1>), lam = {lam:.2f}", census_failures,
        )
        cell = {"lam": lam, **cell}
        cells.append(cell)
        meas = (
            "census failed"
            if "census_failed" in cell
            else f"{cell['measured_n_components']} comps, lk {cell['measured_linking_offdiag']}"
        )
        log(
            f"E2 lam={lam:.2f}: c = {c:.4f}, predicted "
            f"{cell['predicted_n_components']} comps, measured {meas} "
            f"-> {cell_word(cell['matches_prediction'])}"
        )
    results["E2"] = {"radius": 1.0, "cells": cells}
    flags = [c["matches_prediction"] for c in cells]
    results["verdicts"]["e2_fixed_radius_matches_g2"] = aggregate(flags)
    return not any(f is False for f in flags)


def run_e3(results, figures, census_failures):
    lam = 0.5
    c = lam / (1.0 - lam * lam)
    rad_star = math.sqrt(2.0 * c)
    st = squeeze2(state_11(), math.atanh(lam))
    cells = []
    for factor in (0.9, 1.2):
        radius = factor * rad_star
        cell = _census_cell(
            st, radius, {}, c, factor == 1.2, f"E3/radius={factor:.1f}*rad_star",
            figures, f"E3: squeeze2(|1,1>), lam = {lam:.2f}", census_failures,
        )
        cell = {"radius_factor": factor, **cell}
        cells.append(cell)
        meas = (
            "census failed"
            if "census_failed" in cell
            else f"{cell['measured_n_components']} comps, lk {cell['measured_linking_offdiag']}"
        )
        log(
            f"E3 radius {radius:.4f} ({factor:.1f} x rad*): predicted "
            f"{cell['predicted_n_components']} comps, measured {meas} "
            f"-> {cell_word(cell['matches_prediction'])}"
        )
    results["E3"] = {"lam": lam, "rad_star": rad_star, "cells": cells}
    flags = [c["matches_prediction"] for c in cells]
    results["verdicts"]["e3_restoration_matches_g2"] = aggregate(flags)
    return not any(f is False for f in flags)


# ---------------------------------------------------------------------------
# E4: top-form partition of seeded Gaussian orbits (G3, F3)
# ---------------------------------------------------------------------------

def run_e4(results):
    families = []
    all_flags = []
    for name, seeds, expected in E4_FAMILIES:
        maker = STATE_MAKERS[name]
        cells = []
        for seed in seeds:
            img = gauss_unitary(maker(), random_gauss_params(seed))
            part, margin = top_partition(img, tol=E4_TOL)
            if margin < E4_MARGIN:
                # ambiguous clustering (margin within a decade of the
                # tolerance): indeterminate, not a pass and not a mismatch
                v = None
            else:
                v = bool(tuple(part) == expected)
            cells.append(
                {
                    "seed": seed,
                    "partition": list(part),
                    "margin": float(margin),
                    "cell_pass": v,
                }
            )
        fam_flags = [c["cell_pass"] for c in cells]
        families.append(
            {
                "family": name,
                "expected_partition": list(expected),
                "cells": cells,
                "all_cells_pass": aggregate(fam_flags),
            }
        )
        all_flags.extend(fam_flags)
        parts = sorted({tuple(c["partition"]) for c in cells})
        log(
            f"E4 {name}: partitions {parts}, min margin "
            f"{min(c['margin'] for c in cells):.3e} "
            f"-> {cell_word(aggregate(fam_flags))}"
        )
    results["E4"] = {
        "tol": E4_TOL,
        "margin_floor": E4_MARGIN,
        "families": families,
    }
    results["verdicts"]["e4_top_partition_invariant"] = aggregate(all_flags)
    return not any(f is False for f in all_flags)


# ---------------------------------------------------------------------------
# E5: large-radius censuses vs the G4 sketch (F4: record, never halt)
# ---------------------------------------------------------------------------

def classify_t20(state):
    """Data-computed classifier of a transformed |2,0> polynomial P'.

    G3 makes the quadratic part rank-1 (recorded, not assumed: sigma2/sigma1
    is measured). Writing P' = gamma u^2 + beta_u u + beta_v v + delta in an
    orthonormal chart whose first coordinate is the doubled direction, the
    curve is a parallel-line pair iff beta_v vanishes (predict 2 components,
    lk 0, guarded by the quadratic-root separation) and a parabola otherwise
    (predict 1 component). Returns (record, predicted (n, offdiag) or None).
    """
    P = state.P

    def coef(i, j):
        if i < P.shape[0] and j < P.shape[1]:
            return complex(P[i, j])
        return 0.0j

    ap = np.array(
        [[coef(2, 0), coef(1, 1) / 2.0], [coef(1, 1) / 2.0, coef(0, 2)]]
    )
    u_svd, s, _ = np.linalg.svd(ap)
    sigma_ratio = float(s[1] / s[0])
    u = u_svd[:, 0]  # principal left singular vector spans the doubled direction
    gamma = np.conj(u) @ ap @ np.conj(u)
    v = np.array([-np.conj(u[1]), np.conj(u[0])])
    lvec = np.array([coef(1, 0), coef(0, 1)])
    beta_u = lvec @ np.conj(u)
    beta_v = lvec @ np.conj(v)
    delta = coef(0, 0)
    pmax = float(np.max(np.abs(P)))
    record = {
        "sigma_ratio": sigma_ratio,
        "gamma": gamma,
        "beta_u": beta_u,
        "beta_v": beta_v,
        "delta": delta,
        "beta_v_rel": float(abs(beta_v) / pmax),
        "root_separation": None,
    }
    if sigma_ratio >= 1e-8:
        record["curve_type"] = "quad_not_rank1"
        return record, None
    if abs(beta_v) < 1e-9 * pmax:
        disc = beta_u * beta_u - 4.0 * gamma * delta
        sep = float(abs(np.sqrt(disc)) / abs(gamma))
        record["curve_type"] = "parallel_lines"
        record["root_separation"] = sep
        if sep >= 1e-3:
            return record, (2, [0])
        return record, None  # interpretability guard: lines too close
    record["curve_type"] = "parabola"
    return record, (1, [])


def run_e5(results, figures, census_failures):
    cells = []
    for name, seeds, _ in E4_FAMILIES:
        maker = STATE_MAKERS[name]
        for seed in list(seeds)[:2]:
            img = gauss_unitary(maker(), random_gauss_params(seed))
            cell = {"family": name, "seed": seed, "classifier": None}
            if name == "t11":
                pred = (2, [1])
            elif name == "t20":
                record, pred = classify_t20(img)
                cell["classifier"] = record
            else:  # trefoil: one component; windings recorded descriptively
                pred = (1, [])
            cell["predicted_n_components"] = None if pred is None else pred[0]
            cell["predicted_linking_offdiag"] = None if pred is None else pred[1]
            sigs = []
            radii_entries = []
            for radius in E5_RADII:
                want_loops = name == "t11" and seed == 100 and radius == E5_RADII[0]
                entry = {"radius": radius}
                try:
                    res = census(
                        stellar_callable(img), radius=radius, **E5_GRID,
                        return_loops=want_loops,
                    )
                except TraceError as err:
                    entry["census_failed"] = str(err)
                    census_failures.append(
                        f"E5/{name}/seed={seed}/radius={radius}"
                    )
                    sigs.append(None)
                else:
                    if want_loops:
                        figures.append(
                            make_panel(f"E5: G(seed {seed}) |1,1>", res)
                        )
                        res = strip_loops(res)
                    entry["census"] = res
                    entry["n_components"] = len(res["components"])
                    entry["linking_offdiag"] = offdiag_multiset(res)
                    entry["winding_multiset"] = winding_multiset(res)
                    sigs.append(
                        (entry["n_components"], tuple(entry["linking_offdiag"]))
                    )
                radii_entries.append(entry)
            cell["radii"] = radii_entries
            agree = None if None in sigs else bool(sigs[0] == sigs[1])
            cell["radii_agree"] = agree
            if agree and pred is not None:
                cell["sketch_consistent"] = bool(
                    sigs[0] == (pred[0], tuple(pred[1]))
                )
            else:
                cell["sketch_consistent"] = None
            cells.append(cell)
            ctype = cell["classifier"]["curve_type"] if cell["classifier"] else "-"
            log(
                f"E5 {name}/seed={seed}: type {ctype}, radii agree "
                f"{cell['radii_agree']}, sketch "
                f"{cell_word(cell['sketch_consistent'])}"
            )
    results["E5"] = {"radii": list(E5_RADII), "grid": dict(E5_GRID), "cells": cells}
    flags = [c["sketch_consistent"] for c in cells]
    results["verdicts"]["e5_sketch_cells"] = {
        "consistent": sum(1 for f in flags if f is True),
        "inconsistent": sum(1 for f in flags if f is False),
        "indeterminate": sum(1 for f in flags if f is None),
    }
    det = [f for f in flags if f is not None]
    results["verdicts"]["e5_determinate_cells_all_consistent"] = (
        None if not det else bool(all(det))
    )


# ---------------------------------------------------------------------------
# E6: adversarial multi-start probe of Gaussian |2,0> <-> |1,1> (G5, F5)
# ---------------------------------------------------------------------------

NM_ITERS, NM_STEP, NM_TOL = 800, 0.3, 1e-12
E6_CUTOFF = 12       # single coefficients from the forward recursion are exact
E6_NORM_CUTOFF = 48
E6_MAG_CAP = 1.2     # squeezing magnitudes / displacement radii = 1.2 tanh(raw)


def nelder_mead(fun, x0, iters=800, step=0.3, tol=1e-12):
    """Same minimal numpy-only Nelder-Mead as experiments/25_topological_kcurves."""
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


def u2_chart(ph0, ph1, t):
    """3-parameter U(2)/U(1) chart: diag phases times a real mixing rotation.

    The missing right-diagonal phases act on |1,1> / |2,0> as global phases
    (both are number-diagonal), and on the squeezer side they are absorbed by
    the free squeezing phases — so with free zeta phases this chart loses no
    generality for the E6 family, while global phases never move |overlap|.
    """
    rot = np.array(
        [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]], dtype=complex
    )
    return np.diag([np.exp(1j * ph0), np.exp(1j * ph1)]) @ rot


def params_from_x(x):
    """14 real coords -> gauss_unitary params: U_pre 3, zeta1 2, zeta2 2,
    U_post 3, alpha 4. zeta12 is fixed at 0: Lemma A (derivation §A) makes the
    two-mode squeezer redundant between two free passives, so the 14-parameter
    family already covers the full group modulo global phase."""
    return {
        "U_pre": u2_chart(x[0], x[1], x[2]),
        "zeta1": E6_MAG_CAP * math.tanh(x[3]) * np.exp(1j * x[4]),
        "zeta2": E6_MAG_CAP * math.tanh(x[5]) * np.exp(1j * x[6]),
        "zeta12": 0.0,
        "U_post": u2_chart(x[7], x[8], x[9]),
        "alpha": np.array(
            [
                E6_MAG_CAP * math.tanh(x[10]) * np.exp(1j * x[11]),
                E6_MAG_CAP * math.tanh(x[12]) * np.exp(1j * x[13]),
            ]
        ),
    }


def e6_objective(x, source, target_idx):
    try:
        img = gauss_unitary(source, params_from_x(x))
    except GaussActError:
        return 1.0  # off-domain penalty plateau; never a candidate optimum
    c = fock_coeffs(img, E6_CUTOFF)
    return -float(abs(c[target_idx]) ** 2)


def e6_starts(rng):
    """8 structured starts (identity neighborhood + pure-squeeze directions)
    then 24 random starts, as declared in derivation.md §5 E6."""
    starts = []
    squeeze_pats = (
        (0.0, 0.0), (0.5, 0.0), (-0.5, 0.0), (0.0, 0.5),
        (0.0, -0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5),
    )
    for m1, m2 in squeeze_pats:
        x = rng.normal(scale=0.05, size=14)
        x[3] += m1  # zeta1 raw magnitude
        x[5] += m2  # zeta2 raw magnitude
        starts.append(x)
    for _ in range(24):
        starts.append(rng.normal(scale=0.7, size=14))
    return starts


def run_e6(results):
    rng = np.random.default_rng(FIT_SEED)
    directions = []
    best_found = {}
    for dname, source_name, target_idx in (
        ("from_20_to_11", "t20", (1, 1)),
        ("from_11_to_20", "t11", (2, 0)),
    ):
        source = STATE_MAKERS[source_name]()
        starts = e6_starts(rng)
        best_x, best_v = None, 0.0
        for x0 in starts:
            x, v = nelder_mead(
                lambda y, s=source, t=target_idx: e6_objective(y, s, t),
                x0, iters=NM_ITERS, step=NM_STEP, tol=NM_TOL,
            )
            if v < best_v:
                best_x, best_v = x, v
        if best_x is None:
            raise RuntimeError(f"E6 {dname}: no start produced a positive overlap")
        # unitarity check once per optimization, at the best point (the
        # transformer's norm preservation is separately tested per factor)
        img = gauss_unitary(source, params_from_x(best_x))
        nval, shell = norm(img, cutoff=E6_NORM_CUTOFF)
        entry = {
            "direction": dname,
            "n_starts": len(starts),
            "best_found": -best_v,
            "best_x": [float(v) for v in best_x],
            "norm_at_best": float(nval),
            "last_shell_mass_at_best": float(shell),
            "norm_ok": bool(abs(nval - 1.0) < 1e-8 and shell < 1e-10),
        }
        directions.append(entry)
        best_found[dname] = -best_v
        log(
            f"E6 {dname}: best-found F = {-best_v:.8f} over {len(starts)} "
            f"starts (norm at best = {nval:.10f}, tail {shell:.1e})"
        )
    results["E6"] = {
        "fit_seed": FIT_SEED,
        "n_params": 14,
        "mag_cap": E6_MAG_CAP,
        "overlap_cutoff": E6_CUTOFF,
        "norm_cutoff": E6_NORM_CUTOFF,
        "nm": {"iters": NM_ITERS, "step": NM_STEP, "tol": NM_TOL},
        "directions": directions,
    }
    alarm = bool(any(v >= 1.0 - E6_ALARM for v in best_found.values()))
    results["verdicts"]["e6_best_found"] = best_found
    results["verdicts"]["e6_alarm"] = alarm
    log(f"E6 alarm (best-found >= 1 - {E6_ALARM:g}): {alarm}")
    return alarm


# ---------------------------------------------------------------------------
# artifacts
# ---------------------------------------------------------------------------

def finish(results, figures):
    if figures:
        fig = plt.figure(figsize=(11, 9))
        for idx, panel in enumerate(figures[:4]):
            ax = fig.add_subplot(2, 2, idx + 1, projection="3d")
            for loop in panel["loops"]:
                closed = np.vstack([loop, loop[:1]])
                ax.plot(closed[:, 0], closed[:, 1], closed[:, 2], lw=1.2)
            if panel["text"]:
                ax.text2D(
                    0.5, 0.5, panel["text"], transform=ax.transAxes,
                    ha="center", va="center", fontsize=9,
                )
            ax.set_title(panel["title"], fontsize=9)
            ax.set_axis_off()
        fig.suptitle(
            "Gaussian-transformed stellar zero links (stereographic), experiment 26",
            fontsize=11,
        )
        fig.tight_layout()
        fig.savefig(OUT / "gauss_links.png", dpi=160)
        plt.close(fig)

    log("artifacts: gauss_invariance.json, out_run.log, gauss_links.png, "
        "README generated block")
    (OUT / "gauss_invariance.json").write_text(
        json.dumps(json_safe(results), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUT / "out_run.log").write_text("\n".join(LOG_LINES) + "\n", encoding="utf-8")
    write_into_readme(OUT / "README.md", json_safe(results))


def main():
    results = {
        "fit_seed": FIT_SEED,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": sys.platform,
            "machine": platform.machine(),
        },
        "census_parameters": {
            "e2_e3_grid": {"n_eta": 90, "n_xi": 96},
            "e5_grid": dict(E5_GRID),
            "e5_radii": list(E5_RADII),
            "eta_margin": 0.05,
            "frame_seed": 0,
        },
        "verdicts": {},
    }
    figures = []
    census_failures = []

    def close(halt_msg=None):
        results["verdicts"]["census_failures"] = sorted(census_failures)
        finish(results, figures)
        if halt_msg is not None:
            raise SystemExit(halt_msg)

    log("== E1: transformer machinery gate (F1) ==")
    if not run_e1(results):
        close("F1: transformer failed E1; downstream cells are uninterpretable")

    log("== E2: fixed-radius threshold scan (G2/F2) ==")
    if not run_e2(results, figures, census_failures):
        close("F2: an E2 census disagrees with the G2 prediction; "
              "tool/proof alarm, halting interpretation")

    log("== E3: radius restoration (G2/F2) ==")
    if not run_e3(results, figures, census_failures):
        close("F2: an E3 census disagrees with the G2 prediction; "
              "tool/proof alarm, halting interpretation")

    log("== E4: orbit top-form partitions (G3/F3) ==")
    if not run_e4(results):
        close("F3: an E4 partition changed with unambiguous clustering; "
              "diagnose the Lemma A/B/C chain before interpreting anything else")

    log("== E5: large-radius censuses vs the G4 sketch (F4: no halt) ==")
    run_e5(results, figures, census_failures)

    log("== E6: adversarial Gaussian-connectivity probe (G5/F5) ==")
    alarm = run_e6(results)
    close(
        "F5: E6 best-found crossed 1 - 1e-6; numerically contradicts the G3 chain"
        if alarm
        else None
    )


if __name__ == "__main__":
    main()
