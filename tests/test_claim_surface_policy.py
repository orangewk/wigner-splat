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


# --- PR #158 F3-prime correction surfaces ----------------------------------

FR_SPEC_DOC = ROOT / "docs" / "2026-08-10-three-atom-block-frame-preparation--wip.md"

PR158_CLAIM_DOCS = (
    ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md",
    ROOT / "docs" / "2026-08-08-quadratic-phase-turan-K2.md",
    ROOT / "docs" / "2026-08-09-three-atom-one-transition--wip.md",
    ROOT / "docs" / "2026-08-10-three-atom-block-frame-preparation--wip.md",
    ROOT / "docs" / "2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md",
    ROOT / "docs" / "2026-08-11-three-atom-wronskian-valuation-W--wip.md",
)

K2_STATUS_POINTER_DOCS = (
    ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md",
    ROOT / "docs" / "2026-08-09-three-atom-one-transition--wip.md",
    FR_SPEC_DOC,
)

K2Q_STATUS_POINTER_DOCS = (
    ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md",
    ROOT / "docs" / "2026-08-09-three-atom-one-transition--wip.md",
    FR_SPEC_DOC,
)


def test_k2_review_status_is_not_reauthored_on_pointer_surfaces():
    """The canonical R-K2 block lives only in the standalone K2 draft."""

    status_restatement = re.compile(
        r"R-K2[\s\S]{0,160}?R2\s*(?:PASS|待ち)", re.IGNORECASE
    )
    for surface in K2_STATUS_POINTER_DOCS:
        text = surface.read_text(encoding="utf-8")
        found = status_restatement.search(text)
        assert found is None, (
            f"{surface}: noncanonical K2 status returned: {found.group(0)!r}"
        )


def test_k2q_review_status_is_not_reauthored_on_pointer_surfaces():
    """The canonical R-K2Q block lives only in the standalone K2Q draft."""

    status_restatement = re.compile(
        r"R-K2Q[\s\S]{0,160}?(?:R\d+\s*)?(?:PASS|待ち)", re.IGNORECASE
    )
    for surface in K2Q_STATUS_POINTER_DOCS:
        text = surface.read_text(encoding="utf-8")
        found = status_restatement.search(text)
        assert found is None, (
            f"{surface}: noncanonical K2Q status returned: {found.group(0)!r}"
        )


def test_retired_split_route_ids_are_absent_from_current_fr_spec():
    """Retired root routes and chart-only certificate IDs stay out of S4b."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    retired_tokens = (
        "K2Q-wt-w",
        "D-K2Q-WT",
        "M-SPLIT-I-WITNESS",
        "split_i_witness_ref",
        "SplitCellData",
        "C_split",
        "constant_provenance_ref",
        "split-ii",
        "split-iii",
        "M-SPLIT-II-KERNEL",
        "M-SPLIT-III-KERNEL",
    )
    for token in retired_tokens:
        assert token not in current, f"{FR_SPEC_DOC}: retired route token returned: {token}"
    assert re.search(r"K2Q-wt[^\n]{0,120}S4-step-w", current) is None, (
        f"{FR_SPEC_DOC}: retired K2Q-wt root step returned"
    )

    def enum_items(enum_name: str) -> list[str]:
        match = re.search(
            rf"{re.escape(enum_name)}\s*:=\s*\{{(?P<body>[^}}]*)\}}",
            current,
            re.DOTALL,
        )
        assert match is not None, f"{FR_SPEC_DOC}: missing {enum_name}"
        return [item.strip() for item in match.group("body").split(",")]

    category_items = enum_items("CategoryEnum")
    cost_items = enum_items("CostSpecEnum")
    domain_items = enum_items("DomainSchemaEnum")
    missing_items = enum_items("MissingObligationEnum")
    assert category_items.count("root-far") == 1
    assert cost_items == ["uniform", "graded-root"]
    assert domain_items.count("D-ROOT-FAR") == 1
    assert missing_items.count("M-ROOT-FAR-KERNEL") == 1

    route_spec = current.split("次表を active `RouteSpec`", 1)[1].split(
        "`REFIX` は RouteSpec", 1
    )[0]
    root_far_row = re.compile(
        r"^\| `root-far`: root 2\+1 far/unheld \| binary \| — \| — \| — \| — \| — "
        r"\| M-ROOT-FAR-KERNEL unresolved; RF candidate §10\.5\.2 \|$",
        re.MULTILINE,
    )
    assert len(root_far_row.findall(route_spec)) == 1


def test_root_far_graded_candidate_stays_fail_closed():
    """The RF interface may be specified without resolving the active route."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    rf_spec = current.split(
        "#### 10.5.2 RF graded-interface candidate (specification only)", 1
    )[1].split("### 10.6 Coefficient-free constants", 1)[0]

    required_contract = (
        "review statusの唯一のauthoring locationは\n§10.7 `S4-0.RF` row",
        "`root-far` は引き続きunresolved",
        "RECENTER(C,t_c)",
        "D-ROOT-FAR",
        "graded-root(C_RF,pair-difference-derivative)",
        "N_cell,k≤4+8Λ_{η,k}",
        "Σ_kΛ_{η,k}",
        "RF-1 exact recenter",
        "RF-2 cell chain",
        "RF-3 graded ledger",
        "RF-4 fail-closed schema",
    )
    for token in required_contract:
        assert token in rf_spec, f"{FR_SPEC_DOC}: missing RF contract token: {token}"

    assert rf_spec.count("| proof obligation |") == 3
    assert "| status pointer: §10.7 `S4-0.RF` |" in rf_spec
    route_spec = current.split("次表を active `RouteSpec`", 1)[1].split(
        "`REFIX` は RouteSpec", 1
    )[0]
    assert re.search(
        r"^\| `root-far`:[^\n]*\| weighted / S4-step-w \|",
        route_spec,
        re.MULTILINE,
    ) is None, f"{FR_SPEC_DOC}: unresolved root-far was promoted in active RouteSpec"
    assert "| S4-0.RF |" in current
    accepted_status = (
        "**PASS (R-RFSPEC R3、fixed SHA "
        "`25afe6ebb54f93845d48b8993ff7523f0f2643d8`)**"
    )
    assert current.count(accepted_status) == 1
    assert "R-RFSPEC pending" not in current


def test_root_far_domain_schema_binds_all_required_keys():
    """D-ROOT-FAR must not survive after losing one of its seven witnesses."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    domain_table = current.split("各 domain schema の key set は次で固定する。", 1)[
        1
    ].split("`D-ROOT-FAR` は §10.5.2", 1)[0]
    row_pattern = r"^\| `D-ROOT-FAR` \|[^\n]*\|$"
    rows = re.findall(row_pattern, domain_table, re.MULTILINE)
    expected_row = (
        "| `D-ROOT-FAR` | `active_children_nonzero`, `c₁c₂c₃≠0`, "
        "`B₁₂≢0`, `η=q₂−q₁` nonconstant, `q₁−q₃`/`q₂−q₃` nonconstant"
        "(§2 constant-gauge quotient witness), collision-scale witness "
        "`(|ΔA|≤s_m²,|ΔB|≤s_m)`, `Λ_{η,k}=sup_{I_k}|η′|` witness |"
    )
    assert rows == [expected_row]
    assert re.findall(row_pattern, current, re.MULTILINE) == [expected_row]
    actual_row = rows[0]

    required_keys = (
        "`active_children_nonzero`",
        "`c₁c₂c₃≠0`",
        "`B₁₂≢0`",
        "`η=q₂−q₁` nonconstant",
        "`q₁−q₃`/`q₂−q₃` nonconstant(§2 constant-gauge quotient witness)",
        "collision-scale witness `(|ΔA|≤s_m²,|ΔB|≤s_m)`",
        "`Λ_{η,k}=sup_{I_k}|η′|` witness",
    )
    for key in required_keys:
        assert actual_row.count(key) == 1

    # negative path (luna R-RF R2, RF-TEST-1): a row that silently drops any
    # single witness is still a syntactically valid table row, so the guard is
    # the exact-match equality above, not the row regex. Exercise that guard.
    for key in required_keys:
        mutated = actual_row.replace(key, "`dropped`", 1)
        assert mutated != actual_row
        assert re.fullmatch(r"\| `D-ROOT-FAR` \|[^\n]*\|", mutated), (
            "mutated row must remain regex-valid so only the equality catches it"
        )
        assert mutated != expected_row


F3PRIME_WITHDRAWN_ACTIVE_SENTENCES = (
    "の形を持ち、クラスタ重み r_c(≥ 1, Σ_c r_c ≤ k)により deg P_c ≤ 2(r_c − 1)",
    "**系 C2**: κ^G_border(|2t⟩) = t+1",
    "奇 |2t+1⟩: 下界 r ≥ t+2",
    "特に非零 P_ℓΦ(ξ*) (deg P_ℓ≤2o′_ℓ) へ norm 収束",
    "prepared valuation chart 上で\nQ = e^{q*}(P_r + R_{r+1})",
)


def test_f3prime_withdrawn_degree_ledger_is_not_reintroduced():
    """F3-prime makes the old c=3 degree-4 ledger and its C2 lower
    bounds false.  Historical withdrawal records may quote formulas, but the
    former active statement sentences must not return on a current surface.
    The exact witness itself is authored only in the FR specification.
    """

    for surface in PR158_CLAIM_DOCS:
        text = surface.read_text(encoding="utf-8")
        for sentence in F3PRIME_WITHDRAWN_ACTIVE_SENTENCES:
            assert sentence not in text, (
                f"{surface}: F3-prime-withdrawn active sentence returned: "
                f"{sentence!r}"
            )

    witness_heading = "**Flex witness F3′ (旧次数4帳簿の反例・本 witness の唯一の authoring location)**"
    occurrences = {
        surface: surface.read_text(encoding="utf-8").count(witness_heading)
        for surface in PR158_CLAIM_DOCS
    }
    assert occurrences[FR_SPEC_DOC] == 1
    assert sum(occurrences.values()) == 1


# --- issue #137 (topological K-epsilon) surfaces -----------------------------

TOPO_DIRS = {
    "24_hopf_stellar": "hopf_link_results.json",
    "25_topological_kcurves": "topological_kcurves.json",
    "26_gauss_invariance": "gauss_invariance.json",
    "28_isotopy_stability": "isotopy_stability.json",
    "29_trefoil_certified": "trefoil_certified.json",
    "30_dictionary_alignment": "dictionary_alignment.json",
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


def test_exp29_status_not_restated_outside_claim_table():
    """PR #157 review rounds two and three (Sol audit): exp29's W0-W5
    statuses live only in its derivation.md §8 claim table. Scanned:
    docs/research-log.md, the exp29 README outside the generated block,
    the exp29 sources, and derivation.md itself outside table rows
    (headings and prose may not carry per-claim status tags)."""
    exp_dir = EXPERIMENTS / "29_trefoil_certified"
    module = _load_summary_module("29_trefoil_certified")
    readme = (exp_dir / "README.md").read_text(encoding="utf-8")
    start = readme.find(module.BEGIN)
    stop = readme.find(module.END)
    assert start >= 0 and stop >= 0
    derivation = (exp_dir / "derivation.md").read_text(encoding="utf-8")
    outside_table = "\n".join(
        line
        for line in derivation.splitlines()
        if not line.lstrip().startswith("|")
    )
    surfaces = {
        "docs/research-log.md": (ROOT / "docs" / "research-log.md").read_text(
            encoding="utf-8"
        ),
        "29_trefoil_certified/README.md (outside block)": (
            readme[:start] + readme[stop + len(module.END):]
        ),
        "29_trefoil_certified/derivation.md (outside table rows)": outside_table,
        "29_trefoil_certified/run.py": (exp_dir / "run.py").read_text(
            encoding="utf-8"
        ),
        "29_trefoil_certified/certified.py": (exp_dir / "certified.py").read_text(
            encoding="utf-8"
        ),
        "29_trefoil_certified/summary_block.py": (
            exp_dir / "summary_block.py"
        ).read_text(encoding="utf-8"),
    }
    for name, text in surfaces.items():
        found = re.search(
            r"\bw[0-5]\b[^\n]{0,80}(proved|sketch)\b", _normalize(text)
        )
        assert not found, (
            f"{name} restates an exp29 claim status outside the authoring "
            f"location: {found.group(0)!r}"
        )


def test_exp30_status_not_restated_outside_claim_table():
    """Same backstop as exp29's, for exp30: A0-A5 / N1-N4 statuses live
    only in its derivation.md §9 claim table. Scanned: docs/research-log.md,
    the exp30 README outside the generated block, the exp30 sources, and
    derivation.md itself outside table rows."""
    exp_dir = EXPERIMENTS / "30_dictionary_alignment"
    module = _load_summary_module("30_dictionary_alignment")
    readme = (exp_dir / "README.md").read_text(encoding="utf-8")
    start = readme.find(module.BEGIN)
    stop = readme.find(module.END)
    assert start >= 0 and stop >= 0
    derivation = (exp_dir / "derivation.md").read_text(encoding="utf-8")
    outside_table = "\n".join(
        line
        for line in derivation.splitlines()
        if not line.lstrip().startswith("|")
    )
    surfaces = {
        "docs/research-log.md": (ROOT / "docs" / "research-log.md").read_text(
            encoding="utf-8"
        ),
        "30_dictionary_alignment/README.md (outside block)": (
            readme[:start] + readme[stop + len(module.END):]
        ),
        "30_dictionary_alignment/derivation.md (outside table rows)": outside_table,
        "30_dictionary_alignment/run.py": (exp_dir / "run.py").read_text(
            encoding="utf-8"
        ),
        "30_dictionary_alignment/alignment.py": (exp_dir / "alignment.py").read_text(
            encoding="utf-8"
        ),
        "30_dictionary_alignment/summary_block.py": (
            exp_dir / "summary_block.py"
        ).read_text(encoding="utf-8"),
    }
    for name, text in surfaces.items():
        found = re.search(
            r"\b(a[0-5]|n[1-4])\b[^\n]{0,80}(proved|sketch)\b", _normalize(text)
        )
        assert not found, (
            f"{name} restates an exp30 claim status outside the authoring "
            f"location: {found.group(0)!r}"
        )
    # round-1 review of PR #162 (finding 3): status-word scans miss
    # SEMANTIC copies of claim content. These are high-signal signatures
    # of this memo's conclusions; they may appear only in derivation.md.
    content_signatures = (
        r"common[- ]quadratic[^\n]{0,120}(no linked pair|cannot link|"
        r"divides out|transfers|uniformly)",
        r"(certified|fidelity) (bound|gap)s?[^\n]{0,80}(descend|transfer)",
        r"normal form[^\n]{0,80}(iff|exactly the pure gaussian)",
    )
    for name in (
        "docs/research-log.md",
        "30_dictionary_alignment/README.md (outside block)",
    ):
        for pat in content_signatures:
            found = re.search(pat, _normalize(surfaces[name]))
            assert not found, (
                f"{name} carries a semantic copy of exp30 claim content: "
                f"{found.group(0)!r}"
            )


def test_exp31_classifications_not_restated_in_research_log():
    """exp31 (Gate S' survey): per-topic prior-art classifications live
    only in experiments/31_prior_art_survey/findings.md §4; the research
    log may not restate them."""
    text = _normalize(
        (ROOT / "docs" / "research-log.md").read_text(encoding="utf-8")
    )
    found = re.search(
        r"\bt[1-6]\b[^\n]{0,80}(class\b|classified|prior art|adjacent|"
        r"not found)",
        text,
    )
    assert not found, (
        "docs/research-log.md restates an exp31 classification outside "
        f"the authoring location: {found.group(0)!r}"
    )
    findings = EXPERIMENTS / "31_prior_art_survey" / "findings.md"
    table_rows = [
        line
        for line in findings.read_text(encoding="utf-8").splitlines()
        if re.match(r"\| T[1-6] \|", line)
    ]
    assert len(table_rows) == 6, "findings.md §4 must carry all six topic rows"


def test_exp31_classifications_not_restated_outside_findings_table():
    """Round 1 of the PR #168 review (B2): the §4 table is the sole
    authoring location *within findings.md too*. Aggregate restatements
    ("no topic is ...", "every topic ..."), per-topic classification
    prose outside the table rows, and G3-outcome prose are barred on
    every non-table line of findings.md."""
    findings = EXPERIMENTS / "31_prior_art_survey" / "findings.md"
    non_table = [
        line
        for line in findings.read_text(encoding="utf-8").splitlines()
        if not re.match(r"\| (T[1-6]|Topic|---) \|", line)
    ]
    text = _normalize("\n".join(non_table))
    patterns = (
        r"\bno topic is\b",
        r"(all|every)[^\n]{0,30}topics?[^\n]{0,60}(classif|adjacent|"
        r"neighbor)",
        r"\bt[1-6]\b[^\n]{0,80}(classif|adjacent\b|prior[- ]art|"
        r"not found)",
        r"\bg3\b[^\n]{0,50}\b(not|never)\b",
        r"(did not find|found no)[^\n]{0,30}prior[- ]art",
        r"prior[- ]art[^\n]{0,50}\bnot found\b",
        r"\bt[1-6]\b *\|",
    )
    for pattern in patterns:
        found = re.search(pattern, text)
        assert not found, (
            "findings.md restates classification content outside the §4 "
            f"table rows: {found.group(0)!r}"
        )


def test_exp31_load_bearing_sources_have_primary_read_records():
    """PR #168 B1: every source retained in the §4 basis must have a
    dated primary-tier locator and exact read scope in the §1 register.
    This makes a later table-only citation edit fail closed rather than
    silently reviving the engine-tier incident."""
    text = (EXPERIMENTS / "31_prior_art_survey" / "findings.md").read_text(
        encoding="utf-8"
    )
    register_start = text.index("### Primary-read register (2026-08-08)")
    table_start = text.index("## 4. Classification table")
    register = text[register_start:table_start]
    assert "| Retained §4 source | Stable primary locator | Text read on 2026-08-08 |" in register
    retained = (
        "2607.04007",
        "Dennis et al. 2010",
        "Leach et al. 2005",
        "Berry 2001",
        "1904.07229",
        "2605.15008",
        "2604.00766",
        "2410.23721",
        "2404.07115",
        "2111.02391",
        "2305.10277",
        "Pires et al. 2025",
        "Annala et al. 2022",
        "1611.02563",
        "2607.02427",
    )
    for source in retained:
        assert f"| {source} | https://" in register, (
            f"retained exp31 §4 source lacks a primary-tier read record: {source}"
        )
    for removed in ("Milnor 1968", "Brauner 1928", "nested-coding item"):
        assert removed not in text[table_start:], (
            f"unreadable exp31 source remains load-bearing: {removed}"
        )


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
