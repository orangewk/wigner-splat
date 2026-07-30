"""Single authoring location for experiment 25's README numbers.

`run.py` calls `write_into_readme` after writing `topological_kcurves.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the committed
JSON and asserts the README carries exactly that text.
"""

from __future__ import annotations

BEGIN = "<!-- generated-block: do not edit (written by run.py from topological_kcurves.json) -->"
END = "<!-- generated-block: end -->"

LADDER_MARKS = {"t11": "linked pair", "trefoil": "(3,2) winding"}
MARK_KEYS = {"t11": "has_linked_pair", "trefoil": "has_trefoil_windings"}


def _verdict(v):
    if v is None:
        return "INDETERMINATE (census failures)"
    return str(bool(v))


def render(results: dict) -> str:
    cells = results["cells"]
    verdicts = results.get("verdicts", {})
    ladders = results.get("ladders", {})
    lines = [BEGIN]
    for target, title in (("t11", "|1,1>"), ("trefoil", "0.8|20>+0.6|03> (trefoil)")):
        mark = LADDER_MARKS[target]
        lines.append(f"**{title}** — per-K best-found `1 - F` ({mark} flagged):")
        lines.append("")
        lines.append(f"  | dictionary | K | 1 - F | {mark} |")
        lines.append("  | --- | --- | --- | --- |")
        for dict_type in ("coherent", "gaussian"):
            ks = sorted(
                int(name.split("K=")[1])
                for name in cells
                if name.startswith(f"{target}/{dict_type}/")
            )
            for k in ks:
                cell = cells[f"{target}/{dict_type}/K={k}"]
                if "census_failed" in cell:
                    flag = "census failed"
                else:
                    flag = "yes" if cell.get(MARK_KEYS[target]) else "no"
                lines.append(
                    f"  | {dict_type} | {k} | {cell['one_minus_F']:.3e} | {flag} |"
                )
        lines.append("")
        for dict_type in ("coherent", "gaussian"):
            lad = ladders.get(f"{target}/{dict_type}")
            if not lad:
                continue
            fk = lad["first_transition"]
            first = fk["K"] if fk["K"] is not None else "none found"
            caveat = (
                f" (indeterminate below K={min(fk['indeterminate_below'])})"
                if fk["indeterminate_below"]
                else ""
            )
            agree = (
                "coincides"
                if fk["K"] is not None
                and fk["K"] == lad["largest_relative_step_at_K"]
                else "does NOT coincide"
            )
            lines.append(
                f"  - {dict_type}: first {mark} at K = {first}{caveat}; the "
                f"ladder's largest relative step lands at "
                f"K = {lad['largest_relative_step_at_K']} "
                f"(x{lad['largest_relative_step_factor']:.1f}), which "
                f"{agree} with the transition. Descriptive only — no cliff "
                "criterion was pre-declared."
            )
        lines.append("")
    scored = [
        (name, lad)
        for name, lad in sorted(ladders.items())
        if lad["first_transition"]["K"] is not None
    ]
    agree = [
        name
        for name, lad in scored
        if lad["first_transition"]["K"] == lad["largest_relative_step_at_K"]
    ]
    differ = [
        name
        for name, lad in scored
        if lad["first_transition"]["K"] != lad["largest_relative_step_at_K"]
    ]
    lines.append(
        f"Tally (descriptive, no pre-declared criterion): transition and "
        f"largest relative step coincide in {len(agree)} of {len(scored)} "
        f"scored ladders"
        + (f"; differing: {', '.join(differ)}." if differ else ".")
    )
    lines.append("")
    lines.append("Pre-declared verdicts (computed; None = blocked by census failure):")
    lines.append("")
    lines.append(
        f"- PA `|11>`/Gaussian/K=2 reaches the target with the Hopf link: "
        f"**{_verdict(verdicts.get('pa_11_gauss_k2_reaches_target_with_hopf_link'))}** "
        "(theorem-backed expectation, 24/P4 proved)"
    )
    lines.append(
        f"- PB no coherent K<=2 linked pair: "
        f"**{_verdict(verdicts.get('pb_all_coherent_k_le_2_unlinked'))}** "
        "(theorem-backed expectation, 24/P3 proved)"
    )
    lines.append(
        f"- PC Gaussian K=2 max |winding| <= 2: "
        f"**{_verdict(verdicts.get('pc_all_gaussian_k2_max_winding_le_2'))}** "
        "(empirical consistency with the 24/P6 SKETCH — not theorem-backed; "
        "a violation would have been evidence against the sketch, per plan.md)"
    )
    pe = verdicts.get("pe_trefoil_gauss_k6_fidelity")
    if pe is not None:
        lines.append(f"- PE trefoil/Gaussian/K=6 best-found fidelity: **{pe:.4f}**")
    cc = verdicts.get("crosscheck_exp24_e4_max_abs_diff")
    if cc is not None:
        lines.append(
            f"- Cross-check vs exp24's closed-form machinery: max |dF| = {cc:.1e} "
            f"(consistent: {verdicts.get('crosscheck_exp24_e4_consistent')})"
        )
    fails = verdicts.get("census_failures", [])
    lines.append(f"- Census failures: {fails if fails else 'none'}")
    lines.append(END)
    return "\n".join(lines)


def write_into_readme(readme_path, results) -> None:
    text = readme_path.read_text(encoding="utf-8")
    start = text.find(BEGIN)
    stop = text.find(END)
    if start < 0 or stop < 0:
        raise RuntimeError(f"{readme_path} is missing the generated-block markers")
    new = text[:start] + render(results) + text[stop + len(END):]
    readme_path.write_text(new, encoding="utf-8")
