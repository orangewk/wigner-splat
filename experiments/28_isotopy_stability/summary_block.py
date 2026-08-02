"""Single authoring location plumbing for experiment 28's README results.

`run.py` calls `write_into_readme` after writing `isotopy_stability.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the committed
JSON and asserts the README carries exactly that text.

Epistemic status is NOT authored here: derivation.md's §7 claim table is its
sole authoring location, and `load_claim_registry()` parses that table so the
block can quote each claim's status and basis verbatim (the exp25/26
mechanism, applied from the start here).
"""

from __future__ import annotations

from pathlib import Path

BEGIN = "<!-- generated-block: do not edit (written by run.py from isotopy_stability.json) -->"
END = "<!-- generated-block: end -->"

DERIVATION_PATH = Path(__file__).resolve().parent / "derivation.md"
CLAIM_IDS = ("S1", "S2", "S3", "S4", "S5", "N1", "N2", "N3", "N4", "N5")


def load_claim_registry(derivation_path=DERIVATION_PATH):
    """Parse derivation.md's §7 claim table (ID | Claim | Status | Basis)
    into verbatim cell strings; raises if a declared ID is missing."""
    registry = {}
    for line in Path(derivation_path).read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] not in CLAIM_IDS:
            continue
        registry[cells[0]] = {
            "claim": "|".join(cells[1:-2]),
            "status": cells[-2],
            "basis": cells[-1],
        }
    missing = [cid for cid in CLAIM_IDS if cid not in registry]
    if missing:
        raise RuntimeError(f"derivation.md claim table is missing rows: {missing}")
    return registry


def _cell(v):
    if v is None:
        return "INDETERMINATE"
    return str(bool(v))


def _fmt(x, digits=6):
    """Nearest rounding — only for non-claim identifiers and diagnostics."""
    if x is None:
        return "-"
    return f"{float(x):.{digits}f}"


def _fmt_dn(x, digits=6):
    """Safe display of a LOWER bound: round down (direction-aware display,
    applied across experiments after the exp29 Sol audit)."""
    import math as _math

    if x is None:
        return "-"
    return f"{_math.floor(float(x) * 10**digits) / 10**digits:.{digits}f}"


def _fmt_up(x, digits=6):
    """Safe display of an UPPER bound: round up."""
    import math as _math

    if x is None:
        return "-"
    return f"{_math.ceil(float(x) * 10**digits) / 10**digits:.{digits}f}"


def _family_of(label):
    if label.startswith("kernel"):
        return "kernel"
    if label.startswith("random"):
        return "random"
    return "exp25_endpoint"


def render(results: dict) -> str:
    verdicts = results.get("verdicts", {})
    registry = load_claim_registry()
    lines = [BEGIN]

    if "E2" in results:
        e2 = results["E2"]
        lines.append(
            f"- E2 certified radius (grid per JSON `declared`; lower bound "
            f"displayed rounded down): `eps0_cert(|11>)` = "
            f"{_fmt_dn(e2['eps0_cert'])} at "
            f"(rho, h) = ({_fmt(e2['rho_star'], 4)}, {_fmt(e2['h_star'], 4)}); "
            f"certified fidelity bound (S5 runnable form; upper bound "
            f"displayed rounded up) = {_fmt_up(e2['fidelity_bound'])}."
        )

    if "E1" in results:
        e1 = results["E1"]
        lines.append(
            f"- E1 one-sided referee ({e1['n_thetas']} thetas x "
            f"{e1['n_phases']}^2 phases, tol {e1['tol']:g}): clearance "
            f"violations {e1['clearance_violations']}, sigma violations "
            f"{e1['sigma_violations']}; min clearance excess over the closed "
            f"form {_fmt(e1['min_clearance_excess_over_bound'], 3)} "
            f"(refinement diagnostic, not an alarm)."
        )

    if "E3" in results and "directions" in results["E3"]:
        e3 = results["E3"]
        fams: dict[str, list] = {}
        for d in e3["directions"]:
            fams.setdefault(_family_of(d["direction"]), []).append(d)
        lines.append(
            "- E3 first-change probe (ascending lattice per JSON `declared`; "
            "first census change per direction, bisected in the bracketing "
            "interval; census signature = isotopy-invariant content only, "
            "components + |linking|):"
        )
        lines.append("")
        lines.append(
            "  | family | directions | broke | min delta_break | "
            "min ratio to eps0_cert | census failures |"
        )
        lines.append("  | --- | --- | --- | --- | --- | --- |")
        for fam in ("kernel", "random", "exp25_endpoint"):
            ds = fams.get(fam, [])
            if not ds:
                continue
            broke = [d for d in ds if d["delta_break"] is not None]
            min_break = min((d["delta_break"] for d in broke), default=None)
            min_ratio = min(
                (d["ratio_to_eps0_cert"] for d in broke), default=None
            )
            fails = sum(len(d["failures"]) for d in ds)
            lines.append(
                f"  | {fam} | {len(ds)} | {len(broke)} | {_fmt(min_break, 4)} "
                f"| {_fmt(min_ratio, 2)} | {fails} |"
            )
        lines.append("")
        lines.append(
            f"  Overall min delta_break: {_fmt(e3.get('min_delta_break'), 4)} "
            "(best-found upper bounds within the probed families; no "
            "minimality claim)."
        )

    if "E4" in results:
        e4 = results["E4"]
        lines.append(
            f"- E4 exp25 consistency: measured best-found F of "
            f"`{e4['exp25_cell']}` = {_fmt_up(e4['measured_best_fidelity'])} "
            f"(displayed rounded up) vs certified bound "
            f"{_fmt_up(e4['certified_bound'])} (verdict from raw values)."
        )

    if "E5" in results:
        e5 = results["E5"]
        lines.append(
            f"- E5 trefoil grid margins ({e5['zero_cloud_points']} polished "
            "zero points; grid minima over-estimate true margins, so these "
            "are numerically supported only, NOT certified):"
        )
        lines.append("")
        lines.append("  | rho | m_grid | sigma_grid |")
        lines.append("  | --- | --- | --- |")
        for row in e5["rows"]:
            lines.append(
                f"  | {row['rho']:.2f} | {_fmt(row['m_grid'], 4)} | "
                f"{_fmt(row['sigma_grid'], 4)} |"
            )
        lines.append("")
        lines.append(
            f"  Induced eps0-style grid estimate (not certified): "
            f"{_fmt(e5['eps0_grid_estimate_not_certified'])} at "
            f"(rho, h) = ({_fmt(e5['rho_at_best'], 2)}, "
            f"{_fmt(e5['h_at_best'], 4)})."
        )

    lines.append("")
    lines.append("Pre-declared verdicts (computed in run.py from the data):")
    lines.append("")
    label_map = (
        ("e2_eps0_cert_positive", "E2 certified radius positive (F2 gate)"),
        (
            "e1_no_sample_below_proved_bounds",
            "E1 no grid sample below a proved bound (F1 gate)",
        ),
        ("e3_reference_census_is_hopf", "E3 reference census is the Hopf link"),
        (
            "e3_no_census_change_below_eps0_cert",
            "E3 no census change below eps0_cert (F3 gate)",
        ),
        (
            "e3_no_census_failure_below_eps0_cert",
            "E3 no census failure below eps0_cert (F3 gate)",
        ),
        (
            "e4_measured_within_certified_bound",
            "E4 exp25 measured cell within the certified bound (F4 gate)",
        ),
        ("e5_margins_recorded", "E5 trefoil margins recorded"),
    )
    for key, label in label_map:
        if key in verdicts:
            lines.append(f"- {label}: **{_cell(verdicts[key])}**")

    if verdicts.get("halted_at"):
        lines.append("")
        lines.append(
            f"- **RUN HALTED at the {verdicts['halted_at']} gate; later "
            "sections may be absent (artifacts written before the halt).**"
        )

    lines.append("")
    lines.append(
        "Epistemic status — quoted verbatim from derivation.md §7, its sole "
        "authoring location:"
    )
    lines.append("")
    for cid in CLAIM_IDS:
        row = registry[cid]
        lines.append(
            f'- {cid} — status: "{row["status"]}"; basis: "{row["basis"]}"'
        )
    lines.append(END)
    return "\n".join(lines)


def write_into_readme(readme_path, results) -> None:
    readme_path = Path(readme_path)
    text = readme_path.read_text(encoding="utf-8")
    start = text.find(BEGIN)
    stop = text.find(END)
    if start < 0 or stop < 0:
        raise RuntimeError(f"{readme_path} is missing the generated-block markers")
    new = text[:start] + render(results) + text[stop + len(END):]
    readme_path.write_text(new, encoding="utf-8")
