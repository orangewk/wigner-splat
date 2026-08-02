"""Single authoring location plumbing for experiment 29's README results.

`run.py` calls `write_into_readme` after writing `trefoil_certified.json`;
`tests/test_claim_surface_policy.py` re-renders the block from the
committed JSON and asserts the README carries exactly that text.

Epistemic status is NOT authored here: derivation.md's §8 claim table is
its sole authoring location, and `load_claim_registry()` parses that
table so the block can quote each claim's status and basis verbatim.
"""

from __future__ import annotations

from pathlib import Path

BEGIN = "<!-- generated-block: do not edit (written by run.py from trefoil_certified.json) -->"
END = "<!-- generated-block: end -->"

DERIVATION_PATH = Path(__file__).resolve().parent / "derivation.md"
CLAIM_IDS = (
    "W0", "W1", "W2", "W3", "W4", "W5", "N1", "N2", "N3", "N4", "N5",
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


def _fmt(x, digits=6):
    if x is None:
        return "-"
    return f"{float(x):.{digits}f}"


def render(results: dict) -> str:
    verdicts = results.get("verdicts", {})
    registry = load_claim_registry()
    lines = [BEGIN]

    if "E1" in results and "failed" not in results["E1"]:
        e1 = results["E1"]
        lines.append(
            f"- E1 exact enclosures (fractions; slop "
            f"{results['declared']['slop']:g} on transcendental steps): "
            f"`s*` in [{e1['s_star_exact'][0]}, {e1['s_star_exact'][1]}], "
            f"`theta*` in [{_fmt(e1['theta_star'][0])}, "
            f"{_fmt(e1['theta_star'][1])}]; band contains `theta*`: "
            f"{_cell(e1['band_contains_theta_star'])}; core-disjoint rho cap "
            f"{_fmt(e1['rho_cap_core_disjoint'], 4)}."
        )

    if "E2" in results:
        e2 = results["E2"]
        lines.append(
            f"- E2 certified radius: `eps29_cert` = {_fmt(e2['eps29_cert'])} "
            f"at (rho, h) = ({_fmt(e2['rho_star'], 2)}, "
            f"{_fmt(e2['h_star'], 4)}) with margins (m, sigma) = "
            f"({_fmt(e2['m_cert_at_star'])}, "
            f"{_fmt(e2['sigma_cert_at_star'])}); certified fidelity bound "
            f"(W5) = {_fmt(e2['fidelity_bound'])}."
        )
        lines.append("")
        lines.append("  | rho | m_cert | sigma_cert |")
        lines.append("  | --- | --- | --- |")
        for row in e2["rows"]:
            if not row.get("admissible"):
                lines.append(f"  | {row['rho']:.2f} | not admissible | - |")
                continue
            lines.append(
                f"  | {row['rho']:.2f} | {_fmt(row['m_cert'])} | "
                f"{_fmt(max(0.0, row['sigma_cert']))} |"
            )
        lines.append("")

    if "E3" in results:
        e3 = results["E3"]
        lines.append(
            f"- E3 sound margin referees ({e3['zero_cloud_points']} polished "
            "zero points; clearance on the theta-certain complement, "
            "transversality on cloud-inside and phase-normal probe "
            f"families): violations {e3['violations']}. Cloud-complement "
            "grid margins are recorded as a heuristic diagnostic only."
        )

    if "E4" in results:
        e4 = results["E4"]
        c = e4["census"]
        if "census_failed" in c:
            lines.append(f"- E4 census: FAILED ({c['census_failed']}).")
        else:
            lines.append(
                f"- E4 census structure: {c['n_components']} component(s), "
                f"|windings| sorted {c['abs_windings_sorted']}, linking "
                f"offdiag {c['linking_offdiag']}; cloud (declared loop-point "
                "stand-in) theta deviation from the enclosure "
                f"{_fmt(e4['cloud_theta_max_deviation_from_enclosure'], 5)}, "
                f"min core distance {_fmt(e4['cloud_min_core_distance'], 4)} "
                f"vs floor {_fmt(e4['core_distance_floor'], 4)}."
            )

    if "E5" in results:
        e5 = results["E5"]
        for cell in e5["cells"]:
            lines.append(
                f"- E5 `{cell['cell']}`: measured best-found F = "
                f"{_fmt(cell['measured'])} vs certified bound "
                f"{_fmt(e5['certified_bound'])} — within: "
                f"{_cell(cell['within_bound'])}."
            )

    lines.append("")
    lines.append("Pre-declared verdicts (computed in run.py from the data):")
    lines.append("")
    label_map = (
        ("e1_enclosures_established", "E1 exact enclosures established (F1 gate)"),
        ("e2_eps29_cert_positive", "E2 certified radius positive (F2 gate)"),
        ("e3_sound_referees_pass", "E3 sound margin referees pass (F3 gate)"),
        ("e4_census_matches_w1", "E4 census matches the W1 structure (F4 gate)"),
        (
            "e5_exp25_within_certified_bound",
            "E5 exp25 trefoil cells within the certified bound (F5 gate)",
        ),
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
        "Epistemic status — quoted verbatim from derivation.md §8, its sole "
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
