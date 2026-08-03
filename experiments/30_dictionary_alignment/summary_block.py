"""Single authoring location plumbing for experiment 30's README results.

`run.py` calls `write_into_readme` after writing
`dictionary_alignment.json`; `tests/test_claim_surface_policy.py`
re-renders the block from the committed JSON and asserts the README
carries exactly that text.

Epistemic status is NOT authored here: derivation.md's §9 claim table is
its sole authoring location, and `load_claim_registry()` parses that
table so the block can quote each claim's status and basis verbatim.
"""

from __future__ import annotations

from pathlib import Path

BEGIN = "<!-- generated-block: do not edit (written by run.py from dictionary_alignment.json) -->"
END = "<!-- generated-block: end -->"

DERIVATION_PATH = Path(__file__).resolve().parent / "derivation.md"
CLAIM_IDS = (
    "A0", "A1", "A2", "A3", "A4", "A5", "N1", "N2", "N3", "N4",
)


def load_claim_registry(derivation_path=DERIVATION_PATH):
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


def _fmt_dn(x, digits=6):
    """Safe display of a LOWER bound / threshold: Decimal.from_float +
    ROUND_FLOOR (the exp29 Sol re-audit pattern; naive scaling is unsafe
    at binary-decimal boundaries)."""
    from decimal import ROUND_FLOOR, Decimal

    if x is None:
        return "-"
    q = Decimal(1).scaleb(-digits)
    d = Decimal.from_float(float(x)).quantize(q, rounding=ROUND_FLOOR)
    return f"{d:.{digits}f}"


def _fmt_up(x, digits=6):
    """Safe display of an UPPER bound: ROUND_CEILING on the exact binary
    value."""
    from decimal import ROUND_CEILING, Decimal

    if x is None:
        return "-"
    q = Decimal(1).scaleb(-digits)
    d = Decimal.from_float(float(x)).quantize(q, rounding=ROUND_CEILING)
    return f"{d:.{digits}f}"


def render(results: dict) -> str:
    verdicts = results.get("verdicts", {})
    registry = load_claim_registry()
    lines = [BEGIN]

    if "E1" in results:
        e1 = results["E1"]
        lines.append(
            f"- E1 normal-form referee ({e1['n_seeds']} seeded Gaussian-unitary "
            "chains vs the A1 recipe): polynomial part stayed degree 0 on all; "
            f"max ||A|| = {_fmt_up(e1['max_A_norm'], 6)} < 1; max phase-aligned "
            f"Fock mismatch (upper display) {_fmt_up(e1['max_state_mismatch'], 12)}; "
            f"max b-map residual {_fmt_up(e1['max_b_residual'], 12)}; sandwich "
            f"violations {e1['sandwich_violations']}."
        )

    if "E2" in results:
        e2 = results["E2"]
        lines.append(
            f"- E2 norm closed form vs bracketed partial sums "
            f"({e2['n_pairs']} sigma pairs, cutoff {e2['cutoff']}): bracket "
            f"failures {e2['bracket_failures']}; max relative bracket width "
            f"(upper display) {_fmt_up(e2['max_rel_bracket_width'], 8)}."
        )

    if "E3" in results:
        e3 = results["E3"]
        lines.append(
            f"- E3 committed exp25 cells ({e3['n_cells_checked']} rebuilt from "
            "`best_params`): max fidelity re-derivation gap (upper display) "
            f"{_fmt_up(e3['max_fidelity_gap'], 8)}; max atom ||A|| "
            f"{_fmt_up(e3['max_atom_A_norm'], 4)} <= committed box "
            f"{e3['quad_norm_max']}: {_cell(e3['membership_ok'])}; descended-"
            f"bound violations {e3['bound_violations']} (verdict from raw "
            "values). Diagnostic only (no bound claimed, A3 contrast): "
            f"`t11/gaussian/K=2` measured F = "
            f"{_fmt_up(e3['t11_gaussian_k2_measured'], 6)}."
        )

    if "E4" in results:
        e4 = results["E4"]
        lines.append(
            f"- E4 exact conversions: identity failures {e4['identity_failures']} "
            f"on the declared grid; committed-bound outwardness re-verified: "
            f"{_cell(e4['committed_bounds_outward'])}. Note-convention "
            "thresholds (rounded DOWN; 'for all eps below'): trefoil/K<=2 "
            f"eps < {_fmt_dn(e4['eps_note_trefoil'], 6)} (from exp29's radius, "
            f"fidelity bound {_fmt_up(e4['fidelity_bound_trefoil'], 6)} rounded "
            "up); |11>/coherent and common-quadratic K<=2 eps < "
            f"{_fmt_dn(e4['eps_note_t11'], 6)} (from exp28's radius, fidelity "
            f"bound {_fmt_up(e4['fidelity_bound_t11'], 6)} rounded up)."
        )

    lines.append("")
    lines.append("Pre-declared verdicts (computed in run.py from the data):")
    lines.append("")
    label_map = (
        ("e1_normal_form_ok", "E1 normal-form referee passes (F1 gate)"),
        ("e2_norm_bracket_ok", "E2 norm bracket holds (F2 gate)"),
        ("e3_cells_ok", "E3 membership + re-derivation + descended bounds (F3 gate)"),
        ("e4_conversions_ok", "E4 exact conversions verified (F4 gate)"),
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
        "Epistemic status — quoted verbatim from derivation.md §9, its sole "
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
