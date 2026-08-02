"""Surface inventory for issue #71 claims.

`test_artifact_interpretation_policy.py` checks the *content* of a named list
of artifacts and generators. This module checks the *list*: every surface where
a claim can appear is enumerated by glob, so a new experiment directory cannot
escape the policy by simply not being on anyone's list.

That distinction is the point. Of the seven claim divergences recorded on
2026-07-27, the last one to be found (the R_epsilon annotation baked into the
exp22 figure) survived a dedicated policy test because that test scanned JSON
files and the annotation lived in a matplotlib call.

Committed run logs are excluded on purpose: they record what was claimed at the
time and are evidence, not documentation. Rewriting them would destroy that.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"

# Keys whose values are free prose that has historically carried conclusions.
CONCLUSION_KEYS = {
    "claim",
    "conclusion",
    "description",
    "finding",
    "interpretation",
    "note",
    "remark",
    "summary",
    "verdict",
}

# Claims this repository has ruled out. They must not reappear on any surface.
# Each entry is paired with the record that withdrew it.
#
# Patterns match against normalized text (see `_normalize`), because the same
# claim appears as plain prose, as LaTeX, and as a doubly-escaped Python string
# literal. The first draft of this module missed the exp22 figure annotation for
# exactly that reason: it searched for "R_\epsilon \leq 2" while the source held
# "$R_\\epsilon \\leq 2$".
WITHDRAWN_CLAIMS = {
    r"cutoff-stable": "PR #106/#107 — the scored series is increasing",
    r"r_?\\?epsilon\s*(<=|≤|\\leq)\s*2": (
        "PR #117 review — cropped generalized fidelity cannot bound R_epsilon"
    ),
}

ISSUE_71_DIRS = ("20_noninclusion", "22_kcurves", "23_gkp_robust_zeros")


def _issue_71_paths(suffix: str) -> list[Path]:
    return sorted(
        path
        for name in ISSUE_71_DIRS
        for path in (EXPERIMENTS / name).rglob(f"*{suffix}")
    )


def _keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _keys(nested)


def test_every_issue_71_json_is_scanned_and_free_of_conclusion_keys():
    artifacts = _issue_71_paths(".json")
    assert artifacts, "no artifacts found — the glob or the directory list is stale"
    for artifact in artifacts:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        offending = CONCLUSION_KEYS.intersection(_keys(payload))
        assert not offending, f"{artifact}: conclusion-prose keys {sorted(offending)}"


def _normalize(text: str) -> str:
    """Collapse escaping and spacing so one pattern matches every rendering."""
    return re.sub(r"\s+", " ", text.replace("\\\\", "\\")).lower()


def test_no_withdrawn_claim_reappears_on_a_generated_surface():
    surfaces = _issue_71_paths(".py") + _issue_71_paths("README.md")
    assert surfaces, "no generator or README surfaces found — the directory list is stale"
    for surface in surfaces:
        text = _normalize(surface.read_text(encoding="utf-8"))
        for pattern, record in WITHDRAWN_CLAIMS.items():
            found = re.search(pattern, text)
            assert not found, f"{surface}: withdrawn claim {found.group(0)!r} ({record})"


# --- issue #137 (topological K-epsilon) surfaces -----------------------------

TOPO_DIRS = {
    "24_hopf_stellar": "hopf_link_results.json",
    "25_topological_kcurves": "topological_kcurves.json",
    "26_gauss_invariance": "gauss_invariance.json",
    "28_isotopy_stability": "isotopy_stability.json",
    "29_trefoil_certified": "trefoil_certified.json",
}


def _topo_paths(suffix: str) -> list[Path]:
    return sorted(
        path
        for name in TOPO_DIRS
        for path in (EXPERIMENTS / name).rglob(f"*{suffix}")
    )


def test_every_topo_json_is_scanned_and_free_of_conclusion_keys():
    artifacts = _topo_paths(".json")
    assert artifacts, "no issue #137 artifacts found — the directory list is stale"
    for artifact in artifacts:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        offending = CONCLUSION_KEYS.intersection(_keys(payload))
        assert not offending, f"{artifact}: conclusion-prose keys {sorted(offending)}"


def test_no_withdrawn_claim_reappears_on_a_topo_surface():
    surfaces = _topo_paths(".py") + _topo_paths(".md")
    assert surfaces
    for surface in surfaces:
        text = _normalize(surface.read_text(encoding="utf-8"))
        for pattern, record in WITHDRAWN_CLAIMS.items():
            found = re.search(pattern, text)
            assert not found, f"{surface}: withdrawn claim {found.group(0)!r} ({record})"


# Result-shaped phrases that may only appear inside a generated block: the
# 2026-07-30 review found the ladder-coincidence tally hand-restated in README
# prose after the numeric tables had already been generated (same drift class,
# one layer up).
RESTATED_RESULT_PATTERNS = {
    r"(one|two|three|four|five|six|\d+) of (the )?(four|five|six|\d+)( scored)? ladders": (
        "PR #136 round 2 — tallies are generated into the block"
    ),
    r"coincide[sd]? with (it|the (transition|largest))": (
        "PR #136 round 2 — coincidence lines are generated into the block"
    ),
    r"first (linked pair|\(3,2\) winding) at k = \d": (
        "PR #136 round 2 — transition Ks are generated into the block"
    ),
}


def _load_summary_module(name):
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        f"summary_block_{name}", EXPERIMENTS / name / "summary_block.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_no_result_restatement_outside_the_generated_blocks():
    for name in TOPO_DIRS:
        module = _load_summary_module(name)
        readme = (EXPERIMENTS / name / "README.md").read_text(encoding="utf-8")
        start = readme.find(module.BEGIN)
        stop = readme.find(module.END)
        assert start >= 0 and stop >= 0
        outside = _normalize(readme[:start] + readme[stop + len(module.END):])
        for pattern, record in RESTATED_RESULT_PATTERNS.items():
            found = re.search(pattern, outside)
            assert not found, (
                f"{name}/README.md restates a generated result outside the "
                f"block: {found.group(0)!r} ({record})"
            )


# Epistemic-status phrases may not be authored outside plan.md's claim table:
# round 2 hand-restated PC's class on five surfaces and it drifted (round 3).
RESTATED_STATUS_PATTERNS = {
    r"\bp[a-e]\b[^\n]{0,80}(theorem-backed|proved-proposition|sketch-consistency)": (
        "PR #136 round 3 — status is quoted verbatim from plan.md"
    ),
    r"(theorem-backed|not theorem-backed) (expectation|verdict|check)": (
        "PR #136 round 3 — status is quoted verbatim from plan.md"
    ),
}


def test_epistemic_status_quoted_from_plan_not_restated():
    module = _load_summary_module("25_topological_kcurves")
    registry = module.load_claim_registry()
    assert set(registry) == set(module.CLAIM_IDS)

    readme = (EXPERIMENTS / "25_topological_kcurves" / "README.md").read_text(
        encoding="utf-8"
    )
    start = readme.find(module.BEGIN)
    stop = readme.find(module.END)
    assert start >= 0 and stop >= 0
    block = readme[start:stop]
    for cid, row in registry.items():
        assert row["basis"] in block, f"{cid} basis not quoted in the block"
    outside = _normalize(readme[:start] + readme[stop + len(module.END):])
    for pattern, record in RESTATED_STATUS_PATTERNS.items():
        found = re.search(pattern, outside)
        assert not found, (
            f"25_topological_kcurves/README.md restates epistemic status "
            f"outside the block: {found.group(0)!r} ({record})"
        )


def test_exp26_status_quoted_from_derivation_not_restated():
    """Same one-authoring-location gate for exp26: derivation.md's §4 claim
    table is the sole authoring location for G1-G5 epistemic status, the
    generated block quotes each basis verbatim, and no status is restated
    on the scanned surfaces. Scanned: README prose outside the generated
    block, docs/research-log.md, the exp26 generator sources, and — since
    the Sol re-audit — derivation.md itself outside its claim-table rows,
    because the §4 table is the sole authoring location at CLAIM
    granularity, so even the memo's own headings and prose may not carry
    per-claim status tags. The regex net is a backstop, not the gate:
    paraphrased or distant restatements can evade it, and the PR body is a
    GitHub surface this test cannot reach — both are handled by review."""
    module = _load_summary_module("26_gauss_invariance")
    registry = module.load_claim_registry()
    assert set(registry) == set(module.CLAIM_IDS)

    exp_dir = EXPERIMENTS / "26_gauss_invariance"
    readme = (exp_dir / "README.md").read_text(encoding="utf-8")
    start = readme.find(module.BEGIN)
    stop = readme.find(module.END)
    assert start >= 0 and stop >= 0
    block = readme[start:stop]
    for cid, row in registry.items():
        assert row["basis"] in block, f"{cid} basis not quoted in the block"

    derivation = (exp_dir / "derivation.md").read_text(encoding="utf-8")
    outside_table = "\n".join(
        line
        for line in derivation.splitlines()
        if not line.lstrip().startswith("|")
    )
    surfaces = {
        "26_gauss_invariance/README.md (outside block)": (
            readme[:start] + readme[stop + len(module.END):]
        ),
        "docs/research-log.md": (ROOT / "docs" / "research-log.md").read_text(
            encoding="utf-8"
        ),
        "26_gauss_invariance/run.py": (exp_dir / "run.py").read_text(
            encoding="utf-8"
        ),
        "26_gauss_invariance/summary_block.py": (
            exp_dir / "summary_block.py"
        ).read_text(encoding="utf-8"),
        "26_gauss_invariance/derivation.md (outside claim-table rows)": (
            outside_table
        ),
    }
    patterns = {
        **RESTATED_STATUS_PATTERNS,
        r"\bg[1-5]\b[^\n]{0,80}(proved|sketch\b|corollary)": (
            "exp26 — status is quoted verbatim from derivation.md's claim table"
        ),
    }
    for name, text in surfaces.items():
        outside = _normalize(text)
        for pattern, record in patterns.items():
            found = re.search(pattern, outside)
            assert not found, (
                f"{name} restates epistemic status outside the authoring "
                f"location: {found.group(0)!r} ({record})"
            )


def test_tally_excludes_ladders_with_failures_below_transition():
    """A ladder whose transition K sits above a census failure must not be
    counted as a coincidence (PR #136 round 3 fixture test)."""
    module = _load_summary_module("25_topological_kcurves")
    ladders = {
        "t11/coherent": {
            "K": [1, 2],
            "one_minus_F": [0.5, 0.1],
            "relative_step_factors_into_next_K": [5.0],
            "largest_relative_step_at_K": 2,
            "largest_relative_step_factor": 5.0,
            "first_transition": {"K": 2, "indeterminate_below": []},
        },
        "t11/gaussian": {
            "K": [1, 2],
            "one_minus_F": [0.5, 0.1],
            "relative_step_factors_into_next_K": [5.0],
            "largest_relative_step_at_K": 2,
            "largest_relative_step_factor": 5.0,
            "first_transition": {"K": 2, "indeterminate_below": [1]},
        },
    }
    scored, indeterminate = module.coincidence_partition(ladders)
    assert [name for name, _ in scored] == ["t11/coherent"]
    assert indeterminate == ["t11/gaussian"]

    text = module.render({"cells": {}, "verdicts": {}, "ladders": ladders})
    assert "coincide in 1 of 1 scored ladders" in text
    assert "excluded as indeterminate" in text and "t11/gaussian" in text
    assert "2 of 2" not in text

    # the indeterminate ladder's own line must carry no coincidence verdict:
    # only the first OBSERVED transition is known (PR #136 round 4)
    gaussian_lines = [
        line for line in text.splitlines() if line.strip().startswith("- gaussian:")
    ]
    assert len(gaussian_lines) == 1
    assert "which coincides" not in gaussian_lines[0]
    assert "does NOT coincide" not in gaussian_lines[0]
    assert "first observed" in gaussian_lines[0]
    assert "coincidence with the true first transition: INDETERMINATE" in gaussian_lines[0]
    coherent_lines = [
        line for line in text.splitlines() if line.strip().startswith("- coherent:")
    ]
    assert "which coincides" in coherent_lines[0]


def test_exp24_status_not_restated_in_research_log():
    """Finding 3 of the PR #145 review (deferred to this line, applied with
    the 2026-08-02 P5 promotion): exp24's P1-P6 statuses live only in its
    derivation.md §4 claim table; the research log may not restate them.
    Same backstop strength as the exp25/26 patterns."""
    text = _normalize(
        (ROOT / "docs" / "research-log.md").read_text(encoding="utf-8")
    )
    found = re.search(r"\bp[1-6]b?\b[^\n]{0,80}(proved|sketch)\b", text)
    assert not found, (
        "docs/research-log.md restates an exp24 claim status outside the "
        f"authoring location: {found.group(0)!r}"
    )


def test_topo_readme_generated_blocks_match_artifacts():
    """One-authoring-location gate for exp24/25 README numbers: the block in
    each README must be exactly what its summary_block renders from the
    committed JSON (PR #136 review: hand-restated numbers survived an
    artifact change)."""
    import importlib.util

    for name, artifact in TOPO_DIRS.items():
        exp_dir = EXPERIMENTS / name
        spec = importlib.util.spec_from_file_location(
            f"summary_block_{name}", exp_dir / "summary_block.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        results = json.loads((exp_dir / artifact).read_text(encoding="utf-8"))
        readme = (exp_dir / "README.md").read_text(encoding="utf-8")
        start = readme.find(module.BEGIN)
        stop = readme.find(module.END)
        assert start >= 0 and stop >= 0, f"{name}: README lost its generated markers"
        block = readme[start : stop + len(module.END)]
        assert block == module.render(results), (
            f"{name}: README generated block diverges from {artifact}; "
            "rerun run.py instead of editing the block"
        )


def test_run_logs_are_excluded_from_the_scan():
    """The exclusion is deliberate; assert it stays deliberate.

    If a future edit makes the scan cover .log files, the withdrawn-claim check
    would demand rewriting committed evidence. This test fails first, so the
    reason gets read before that happens.
    """
    logs = _issue_71_paths(".log")
    assert logs, "expected committed run logs under the issue #71 experiments"
    assert not any(log in _issue_71_paths(".py") for log in logs)
