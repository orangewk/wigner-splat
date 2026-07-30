"""Single authoring location plumbing for experiment 26's README results.

`run.py` calls `write_into_readme` after writing `gauss_invariance.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the committed
JSON and asserts the README carries exactly that text.

Epistemic status is NOT authored here: `derivation.md`'s §4 claim table is
its sole authoring location, and `load_claim_registry()` parses that table so
the block can quote each claim's basis and on-violation cell verbatim (the
mechanism introduced for exp25 in PR #136 round 3, applied from the start
here).
"""

from __future__ import annotations

import math
from pathlib import Path

BEGIN = "<!-- generated-block: do not edit (written by run.py from gauss_invariance.json) -->"
END = "<!-- generated-block: end -->"

DERIVATION_PATH = Path(__file__).resolve().parent / "derivation.md"
CLAIM_IDS = ("G1", "G2", "G3", "G4", "G5")


def load_claim_registry(derivation_path=DERIVATION_PATH):
    """Parse derivation.md's §4 claim table (ID | Statement | Basis |
    On violation) into a dict of verbatim cell strings. Raises if any
    declared ID is missing, so a drifted table fails loudly."""
    registry = {}
    for line in Path(derivation_path).read_text(encoding="utf-8").splitlines():
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
        raise RuntimeError(
            f"derivation.md claim table is missing rows: {missing}"
        )
    return registry


def _cell(v):
    if v is None:
        return "INDETERMINATE"
    return str(bool(v))


def _mark(ok):
    return "MATCH" if ok else "MISMATCH"


def _fmt_margin(m):
    m = float(m)
    return "inf" if math.isinf(m) else f"{m:.3e}"


def _fmt_partition(p):
    return "(" + ",".join(str(int(v)) for v in p) + ")"


def _link_str(n, off):
    return f"{n} comps, lk {list(off)}"


def _measured_str(cell):
    if "census_failed" in cell:
        return "census failed"
    return _link_str(cell["measured_n_components"], cell["measured_linking_offdiag"])


def _radius_cols(entry):
    if "census_failed" in entry:
        return "fail", "fail"
    return str(entry["n_components"]), str(entry["linking_offdiag"])


def render(results: dict) -> str:
    verdicts = results.get("verdicts", {})
    registry = load_claim_registry()
    lines = [BEGIN]

    if "E1" in results:
        e1 = results["E1"]
        rel = e1["bruteforce_max_rel_diff"]
        lines.append(
            f"- E1 transformer gate (F1): "
            f"**{_mark(verdicts.get('e1_transformer_validated'))}** "
            f"(truncated-Fock brute force at cutoff {e1['bruteforce_cutoff']}, "
            f"max rel diff on the low block — `|1,1>`: {rel['t11']:.2e}, "
            f"trefoil: {rel['trefoil']:.2e})."
        )

    if "E2" in results:
        lines.append(
            f"- E2 fixed-radius scan (squeeze2 of `|1,1>`, radius "
            f"{results['E2']['radius']}; prediction computed per cell from "
            "c(lam) vs rad^2/2):"
        )
        lines.append("")
        lines.append("  | lam | c(lam) | predicted | measured comps | linking | cell |")
        lines.append("  | --- | --- | --- | --- | --- | --- |")
        for cell in results["E2"]["cells"]:
            pred = _link_str(
                cell["predicted_n_components"], cell["predicted_linking_offdiag"]
            )
            if "census_failed" in cell:
                comps, link = "census failed", "-"
            else:
                comps = str(cell["measured_n_components"])
                link = str(cell["measured_linking_offdiag"])
            lines.append(
                f"  | {cell['lam']:.2f} | {cell['c_lam']:.4f} | {pred} | "
                f"{comps} | {link} | {_cell(cell['matches_prediction'])} |"
            )
        lines.append("")

    if "E3" in results:
        for cell in results["E3"]["cells"]:
            pred = _link_str(
                cell["predicted_n_components"], cell["predicted_linking_offdiag"]
            )
            lines.append(
                f"- E3 radius {cell['radius']:.4f} "
                f"({cell['radius_factor']:.1f} x rad*): predicted {pred}; "
                f"measured {_measured_str(cell)} — "
                f"{_cell(cell['matches_prediction'])}."
            )

    if "E4" in results:
        lines.append(
            f"- E4 top-form partitions of seeded Gaussian orbits "
            f"(clustering tol {results['E4']['tol']:g}, indeterminate below "
            f"margin {results['E4']['margin_floor']:g}):"
        )
        lines.append("")
        lines.append("  | state | partitions (8 seeds) | min margin | cells |")
        lines.append("  | --- | --- | --- | --- |")
        for fam in results["E4"]["families"]:
            counts: dict[str, int] = {}
            for c in fam["cells"]:
                key = _fmt_partition(c["partition"])
                counts[key] = counts.get(key, 0) + 1
            parts = ", ".join(f"{k} x{n}" for k, n in counts.items())
            min_margin = min(float(c["margin"]) for c in fam["cells"])
            lines.append(
                f"  | {fam['family']} | {parts} | {_fmt_margin(min_margin)} | "
                f"{_cell(fam['all_cells_pass'])} |"
            )
        lines.append("")

    if "E5" in results:
        r1, r2 = results["E5"]["radii"]
        lines.append(
            f"- E5 large-radius censuses (radii {r1} / {r2}; a cell is "
            "indeterminate unless both radii agree on components and linking):"
        )
        lines.append("")
        lines.append(
            "  | state/seed | type | radii agree | comps "
            f"{r1}/{r2} | lk {r1}/{r2} | sketch-consistent |"
        )
        lines.append("  | --- | --- | --- | --- | --- | --- |")
        for cell in results["E5"]["cells"]:
            cls = cell.get("classifier")
            ctype = cls["curve_type"] if cls else "-"
            c1, l1 = _radius_cols(cell["radii"][0])
            c2, l2 = _radius_cols(cell["radii"][1])
            lines.append(
                f"  | {cell['family']}/{cell['seed']} | {ctype} | "
                f"{_cell(cell['radii_agree'])} | {c1} / {c2} | {l1} / {l2} | "
                f"{_cell(cell['sketch_consistent'])} |"
            )
        lines.append("")

    if "E6" in results:
        dirs = {d["direction"]: d for d in results["E6"]["directions"]}
        f1 = dirs["from_20_to_11"]["best_found"]
        f2 = dirs["from_11_to_20"]["best_found"]
        n_starts = dirs["from_20_to_11"]["n_starts"]
        lines.append(
            f"- E6 adversarial probe ({n_starts} NM starts per direction, "
            f"best-found only, never a supremum): max F(G`|2,0>`, `|1,1>`) = "
            f"{f1:.6f}; max F(G`|1,1>`, `|2,0>`) = {f2:.6f}; alarm "
            f"(best-found >= 1 - 1e-6): **{bool(verdicts.get('e6_alarm'))}**."
        )

    lines.append("")
    lines.append(
        "Pre-declared verdicts (computed; INDETERMINATE = census failure or "
        "ambiguous clustering, never a pass):"
    )
    lines.append("")
    label_map = (
        ("e1_transformer_validated", "E1 transformer validated (F1 gate)"),
        ("e2_fixed_radius_matches_g2", "E2 fixed-radius cells match the G2 prediction"),
        ("e3_restoration_matches_g2", "E3 restoration cells match the G2 prediction"),
        (
            "e4_top_partition_invariant",
            "E4 top-form partition unchanged across all orbit cells (G3)",
        ),
        (
            "e5_determinate_cells_all_consistent",
            "E5 determinate cells all consistent with the G4 sketch (F4: no halt either way)",
        ),
    )
    for key, label in label_map:
        if key in verdicts:
            lines.append(f"- {label}: **{_cell(verdicts[key])}**")
    if "e5_sketch_cells" in verdicts:
        sc = verdicts["e5_sketch_cells"]
        lines.append(
            f"- E5 cell tally: consistent {sc['consistent']}, inconsistent "
            f"{sc['inconsistent']}, indeterminate {sc['indeterminate']}"
        )
    if "e6_best_found" in verdicts:
        bf = verdicts["e6_best_found"]
        lines.append(
            f"- E6 best-found F (descriptive; G5/F5 alarm threshold 1 - 1e-6): "
            f"G`|2,0>` -> `|1,1>`: {bf['from_20_to_11']:.6f}; "
            f"G`|1,1>` -> `|2,0>`: {bf['from_11_to_20']:.6f}"
        )
    if "e6_alarm" in verdicts:
        lines.append(f"- E6 alarm fired: **{bool(verdicts['e6_alarm'])}**")
    fails = verdicts.get("census_failures", [])
    lines.append(f"- Census failures: {fails if fails else 'none'}")

    halted = None
    if verdicts.get("e1_transformer_validated") is False:
        halted = "F1"
    elif verdicts.get("e2_fixed_radius_matches_g2") is False:
        halted = "F2"
    elif verdicts.get("e3_restoration_matches_g2") is False:
        halted = "F2"
    elif verdicts.get("e4_top_partition_invariant") is False:
        halted = "F3"
    elif verdicts.get("e6_alarm") is True:
        halted = "F5"
    if halted:
        lines.append("")
        lines.append(
            f"- **RUN HALTED at the {halted} gate; later sections may be "
            "absent (artifacts written before the halt).**"
        )

    lines.append("")
    lines.append(
        "Epistemic status — quoted verbatim from derivation.md §4, its sole "
        "authoring location:"
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
