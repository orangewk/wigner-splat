"""Single authoring location for experiment 24's README numbers.

`run.py` calls `write_into_readme` after writing `hopf_link_results.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the committed
JSON and asserts the README carries exactly that text. Hand-editing the
block therefore fails the policy test.
"""

from __future__ import annotations

import math

BEGIN = "<!-- generated-block: do not edit (written by run.py from hopf_link_results.json) -->"
END = "<!-- generated-block: end -->"


def _mark(ok):
    return "MATCH" if ok else "MISMATCH"


def render(results: dict) -> str:
    lines = [BEGIN]
    verdicts = results.get("verdicts", {})
    lines.append(
        "- E1 tracker validation against the proved links: "
        f"**{_mark(verdicts.get('e1_tracker_validated'))}**."
    )
    if "e2_knot_ladder_matches" in verdicts:
        lines.append(
            "- E2 knot ladder (three-chain linking, trefoil winding pair): "
            f"**{_mark(verdicts['e2_knot_ladder_matches'])}**."
        )
    if "E3" in results:
        lams = sorted(results["E3"]["tmsv_odd_cat"], key=float)
        fids = ", ".join(
            f"lam={lam}: F = {results['E3']['tmsv_odd_cat'][lam]['fidelity_to_11_closed_form']:.4f}"
            for lam in lams
        )
        lines.append(
            "- E3 dictionary probes: "
            f"**{_mark(verdicts.get('e3_dictionary_probes_match'))}** "
            f"(TMSV odd-cat fidelities {fids}; closed form and Fock series "
            "agree per the recorded booleans)."
        )
    if "E4" in results:
        lines.append("- E4 coherent fit ladder (best-found, not certified suprema):")
        lines.append("")
        lines.append("  | K | best fidelity | 1 - F | zero components | linked pair |")
        lines.append("  | --- | --- | --- | --- | --- |")
        for k in (1, 2, 3, 4):
            cell = results["E4"][f"K={k}"]
            fid = cell["best_fidelity"]
            lines.append(
                f"  | {k} | {fid:.6f} | {1 - fid:.1e} | "
                f"{len(cell['census']['components'])} | "
                f"{'yes' if cell['linked_pair_found'] else 'no'} |"
            )
        lines.append("")
        d1 = abs(results["E4"]["K=1"]["best_fidelity"] - math.exp(-2))
        d2 = abs(results["E4"]["K=2"]["best_fidelity"] - math.exp(-1))
        lines.append(
            f"  Observation (conjecture only): the K=1 / K=2 values sit within "
            f"{d1:.1e} / {d2:.1e} of e^-2 / e^-1."
        )
    if not verdicts.get("e1_tracker_validated", True):
        lines.append("- **RUN HALTED at the F1 gate; downstream sections absent.**")
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
