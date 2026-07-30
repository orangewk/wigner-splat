"""Single authoring location plumbing for experiment 25's README results.

`run.py` calls `write_into_readme` after writing `topological_kcurves.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the committed
JSON and asserts the README carries exactly that text.

Epistemic status is NOT authored here: `plan.md`'s claim table is its sole
authoring location, and `load_claim_registry()` parses that table so the
block can quote each check's basis and violation clause verbatim
(PR #136 round 3 — a hand-restated status classification drifted in round 2).
"""

from __future__ import annotations

from pathlib import Path

BEGIN = "<!-- generated-block: do not edit (written by run.py from topological_kcurves.json) -->"
END = "<!-- generated-block: end -->"

PLAN_PATH = Path(__file__).resolve().parent / "plan.md"
CLAIM_IDS = ("PA", "PB", "PC", "PD", "PE")

LADDER_MARKS = {"t11": "linked pair", "trefoil": "(3,2) winding"}
MARK_KEYS = {"t11": "has_linked_pair", "trefoil": "has_trefoil_windings"}


def load_claim_registry(plan_path=PLAN_PATH):
    """Parse plan.md's pre-declared claim table (ID | Statement | Basis |
    On violation) into a dict of verbatim cell strings. Raises if any
    declared ID is missing, so a drifted plan fails loudly."""
    registry = {}
    for line in plan_path.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0] not in CLAIM_IDS:
            continue
        # statement cells may contain pipes inside backticks (e.g. `|11>`);
        # the ID and the last two columns are pipe-free, so rejoin the middle
        registry[cells[0]] = {
            "statement": "|".join(cells[1:-2]),
            "basis": cells[-2],
            "on_violation": cells[-1],
        }
    missing = [cid for cid in CLAIM_IDS if cid not in registry]
    if missing:
        raise RuntimeError(f"plan.md claim table is missing rows: {missing}")
    return registry


def _verdict(v):
    if v is None:
        return "INDETERMINATE (census failures)"
    return str(bool(v))


def coincidence_partition(ladders):
    """Split ladders into (scored, indeterminate) for the tally.

    A ladder is scored only when its first transition is found AND no
    smaller-K cell had a census failure (`indeterminate_below` empty) —
    otherwise the true first transition is unknown and the ladder must not
    enter the coincidence count (PR #136 round 3).
    """
    scored, indeterminate = [], []
    for name, lad in sorted(ladders.items()):
        fk = lad["first_transition"]
        if fk["indeterminate_below"]:
            indeterminate.append(name)
        elif fk["K"] is not None:
            scored.append((name, lad))
    return scored, indeterminate


def render(results: dict) -> str:
    cells = results["cells"]
    verdicts = results.get("verdicts", {})
    ladders = results.get("ladders", {})
    registry = load_claim_registry()
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
            step = (
                f"the ladder's largest relative step lands at "
                f"K = {lad['largest_relative_step_at_K']} "
                f"(x{lad['largest_relative_step_factor']:.1f})"
            )
            if fk["indeterminate_below"]:
                # only the first OBSERVED transition is known, so no
                # coincidence judgment may be emitted for this ladder
                first = fk["K"] if fk["K"] is not None else "none observed"
                lines.append(
                    f"  - {dict_type}: first observed {mark} at K = {first} "
                    f"(INDETERMINATE below K={min(fk['indeterminate_below'])} "
                    f"— census failures; excluded from the tally); {step}; "
                    "coincidence with the true first transition: "
                    "INDETERMINATE. Descriptive only — no cliff criterion "
                    "was pre-declared."
                )
            elif fk["K"] is None:
                lines.append(
                    f"  - {dict_type}: no {mark} found in the scanned K "
                    f"range; {step}; no transition to compare (not in the "
                    "tally). Descriptive only — no cliff criterion was "
                    "pre-declared."
                )
            else:
                agree = (
                    "coincides"
                    if fk["K"] == lad["largest_relative_step_at_K"]
                    else "does NOT coincide"
                )
                lines.append(
                    f"  - {dict_type}: first {mark} at K = {fk['K']}; {step}, "
                    f"which {agree} with the transition. Descriptive only — "
                    "no cliff criterion was pre-declared."
                )
        lines.append("")
    scored, indeterminate = coincidence_partition(ladders)
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
    tally = (
        f"Tally (descriptive, no pre-declared criterion): transition and "
        f"largest relative step coincide in {len(agree)} of {len(scored)} "
        f"scored ladders"
    )
    if differ:
        tally += f"; differing: {', '.join(differ)}"
    if indeterminate:
        tally += (
            f"; excluded as indeterminate (census failures below the "
            f"transition): {', '.join(indeterminate)}"
        )
    lines.append(tally + ".")
    lines.append("")
    lines.append("Pre-declared verdicts (computed; None = blocked by census failure):")
    lines.append("")
    lines.append(
        f"- PA `|11>`/Gaussian/K=2 reaches the target with the Hopf link: "
        f"**{_verdict(verdicts.get('pa_11_gauss_k2_reaches_target_with_hopf_link'))}**"
    )
    lines.append(
        f"- PB no coherent K<=2 linked pair: "
        f"**{_verdict(verdicts.get('pb_all_coherent_k_le_2_unlinked'))}**"
    )
    lines.append(
        f"- PC Gaussian K=2 max |winding| <= 2: "
        f"**{_verdict(verdicts.get('pc_all_gaussian_k2_max_winding_le_2'))}**"
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
    lines.append("")
    lines.append(
        "Epistemic status — quoted verbatim from plan.md's claim table, "
        "its sole authoring location:"
    )
    lines.append("")
    for cid in CLAIM_IDS:
        row = registry[cid]
        lines.append(
            f'- {cid} — basis: "{row["basis"]}"; on violation: '
            f'"{row["on_violation"]}"'
        )
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
