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
    ROOT / "docs" / "2026-08-18-general-c-block-frame-program--wip.md",
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
    expected_root_far_row = (
        "| `root-far`: root 2+1 far/unheld | binary | weighted / S4-step-w | "
        "`(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),"
        "27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)+(INTERNAL-EXACT,"
        "docs/2026-08-10-three-atom-block-frame-preparation--wip.md,§10.5.3 補題 RF,"
        "c271919d330c718a8e6f7d76af7fc1f052aa9d71,PASS)` | D-ROOT-FAR | "
        "`(graded-root(C_RF,pair-difference-derivative),5,0)` | weighted-no-A / accepted | "
        "interval domain witness(全 7 key)+ `step_cost_witness` |"
    )
    root_far_lines = [
        line
        for line in route_spec.splitlines()
        if line.startswith("| `root-far`:")
    ]
    assert root_far_lines == [expected_root_far_row], (
        f"{FR_SPEC_DOC}: resolved root-far row missing or drifted"
    )


def test_root_far_rf_acceptance_surfaces_agree():
    """After R-RF acceptance the RF contract, proof status, and resolved row
    must agree; no surface may drift back to the unresolved vocabulary."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    rf_spec = current.split(
        "#### 10.5.2 RF graded interface (accepted specification)", 1
    )[1].split("### 10.6 Coefficient-free constants", 1)[0]

    required_contract = (
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

    # the resolved row must consume the Sec 10.5.2 intended discriminant
    # verbatim, so the two surfaces cannot drift independently
    intended = (
        "route ID=`root-far`、arity=binary、mode=weighted / S4-step-w、\n"
        "source rule=`(QR5 accepted ref + RF INTERNAL proof ref)`、domain=`D-ROOT-FAR`、\n"
        "`(graded-root(C_RF,pair-difference-derivative),γ=5,κ̄=0)`、A-ledger=`weighted-no-A`"
    )
    assert intended in rf_spec, f"{FR_SPEC_DOC}: intended discriminant drifted"

    # promoted state must not retain candidate/unresolved vocabulary anywhere
    # in the current region (version history is excluded by the split above)
    stale_tokens = (
        "candidate (specification only)",
        "M-ROOT-FAR-KERNEL のまま",
        "RF候補だけが将来",
        "M-ROOT-FAR-KERNEL unresolved",
        "は引き続きunresolved",
        "RF proof待ちのunresolved",
        "RF candidate",
        "RF-CandidateSpec",
        "graded-root候補",
        "候補定数",
    )
    for token in stale_tokens:
        assert token not in current, f"{FR_SPEC_DOC}: stale promoted-state token: {token}"

    # after final acceptance no pending marker survives in the active region,
    # and the promote surgery carries its own acceptance record
    assert current.count("pending") == 0
    assert "**PASS (R-RF-PROMOTE R3、fixed SHA `9cca48d`)**" in current

    # provenance: every external source_ref SHA in the active RouteSpec (and
    # the C-prime source rule) must be named PASS/accepted by its canonical
    # ledger; full SHAs are compared against the ledger's short prefix
    assert "PASS (R-RF R2、fixed SHA `9f19389`; minors v0.9.4 `c271919`)" in current

    def ledger_names_sha(doc_name: str, full_sha: str, marker: str) -> None:
        """`marker` is a literal string; the ledger SHA must follow it."""
        text = (ROOT / "docs" / doc_name).read_text(encoding="utf-8")
        found = re.search(
            re.escape(marker) + r"[^`]*`([0-9a-f]{7,40})`", text
        )
        assert found, f"{doc_name}: acceptance record marker missing: {marker}"
        short = found.group(1)
        assert full_sha.startswith(short), (
            f"{doc_name}: ledger SHA {short} does not prefix source_ref {full_sha}"
        )

    external_refs = {
        "2026-08-08-quadratic-phase-turan-K2.md": (
            "eb1804acf103d05e3261073405deb1381b44c256",
            "R-K2-FRESH R3 PASS、fixed SHA ",
        ),
        "2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md": (
            "96671e61ac62fdcf2160f63a03bf4f173f15f14a",
            "R-K2Q-ACCEPT PASS、reviewed SHA ",
        ),
        "2026-08-09-pair-block-kernel-K2p1--wip.md": (
            "27a1817150ab7a857cdd00320ed3809c73e3c1bd",
            "**PASS**(R-P3、fixed SHA ",
        ),
    }
    for doc_name, (full_sha, marker) in external_refs.items():
        # the FR spec must actually cite this full SHA in its active region...
        assert full_sha in current, f"{FR_SPEC_DOC}: missing source_ref SHA {full_sha}"
        # ...and the canonical ledger must name a prefix of it as accepted
        ledger_names_sha(doc_name, full_sha, marker)

    # positional binding (luna R-RF-PROMOTE R3): each source rule must carry
    # its own kernel/file/anchor/SHA tuple, so reverting one row cannot hide
    # behind the same SHA appearing at another position
    route_spec_full = current.split("次表を active `RouteSpec`", 1)[1].split(
        "`REFIX` は RouteSpec", 1
    )[0]
    s4_0_sha = "56498bb6e6e53ec7a07bd4c131dae5ec0575be5c"
    row_source_expectations = {
        "| `K2-u`:": (
            "(K2,docs/2026-08-08-quadratic-phase-turan-K2.md,§2 主結果,"
            "eb1804acf103d05e3261073405deb1381b44c256,PASS)",
        ),
        "| `K2Q-aff-u`:": (
            "(K2Q-aff,docs/2026-08-09-quadratic-phase-turan-K2Q-weight21--wip.md,"
            "§6.1 K2Q-aff,96671e61ac62fdcf2160f63a03bf4f173f15f14a,PASS)",
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            "--wip.md,§10.5.4 補題 PΣ-2,"
            "4d0f636c6b4c2e05bd09912164f97ff06e35ba41,PASS)",
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            "--wip.md,§10.5.4 補題 PΣ-3,"
            "65bb02ef9f410460f127ad2339e49d8c903fe377,PASS)",
        ),
        "| `generalized-singleton-u`:": (
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            f"--wip.md,§10.5 generalized-singleton-u,{s4_0_sha},PASS)",
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            "--wip.md,§10.5.4 補題 PΣ-2,"
            "4d0f636c6b4c2e05bd09912164f97ff06e35ba41,PASS)",
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            "--wip.md,§10.5.4 補題 PΣ-3,"
            "65bb02ef9f410460f127ad2339e49d8c903fe377,PASS)",
        ),
        "| `QR5-w`:": (
            "(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),"
            "27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)",
        ),
        "| `root-far`:": (
            "(QR5,docs/2026-08-09-pair-block-kernel-K2p1--wip.md,§3.8.6 QR5(U_T),"
            "27a1817150ab7a857cdd00320ed3809c73e3c1bd,PASS)",
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            "--wip.md,§10.5.3 補題 RF,"
            "c271919d330c718a8e6f7d76af7fc1f052aa9d71,PASS)",
        ),
        "| `trivial-u`:": (
            "(INTERNAL-EXACT,docs/2026-08-10-three-atom-block-frame-preparation"
            f"--wip.md,§10.5 trivial-u,{s4_0_sha},PASS)",
        ),
    }
    for prefix, fragments in row_source_expectations.items():
        rows = [
            line
            for line in route_spec_full.splitlines()
            if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"{FR_SPEC_DOC}: row {prefix} count {len(rows)} != 1"
        for fragment in fragments:
            assert fragment in rows[0], (
                f"{FR_SPEC_DOC}: row {prefix} lost source tuple {fragment[:40]}..."
            )

    cprime_block = current.split("CprimeSourceRule := (C-prime,", 1)[1].split(
        "Cprime_ref", 1
    )[0]
    assert "docs/2026-08-08-quadratic-phase-turan-K2.md" in cprime_block
    assert "§3 補題 C′" in cprime_block
    assert "eb1804acf103d05e3261073405deb1381b44c256" in cprime_block
    assert "PASS)" in cprime_block

    # coverage: every category row appears exactly once in the active RouteSpec
    for prefix in (
        "| `K2-u`:",
        "| `K2Q-aff-u`:",
        "| `generalized-singleton-u`:",
        "| `QR5-w`:",
        "| `root-far`:",
        "| `trivial-u`:",
    ):
        count = sum(
            1 for line in route_spec_full.splitlines() if line.startswith(prefix)
        )
        assert count == 1, f"{FR_SPEC_DOC}: category row {prefix} count {count} != 1"

    # promoted state: no RF obligation row may remain, and all three proof
    # rows carry the same acceptance record
    assert rf_spec.count("| proof obligation |") == 0
    rf_acceptance = "**accepted**(R-RF R2 PASS `9f19389`、minors `c271919`)"
    assert rf_spec.count(rf_acceptance) == 3
    assert "は引き続きunresolved" not in current
    assert "M-ROOT-FAR-KERNEL unresolved" not in current

    assert "| S4-0.RF |" in current
    accepted_status = (
        "**PASS (R-RFSPEC R3、fixed SHA "
        "`25afe6ebb54f93845d48b8993ff7523f0f2643d8`)**"
    )
    assert current.count(accepted_status) == 1
    assert "R-RFSPEC pending" not in current
    proof_status = (
        "**PASS (R-RF R2、fixed SHA `9f19389`; minors v0.9.4 `c271919`)**"
    )
    assert current.count(proof_status) == 1
    assert "| S4-0.RF-PROOF |" in current


def test_polynomial_sigma_a_promotion_surfaces_agree():
    """PS-4 surgery: promoted polynomial-envelope rows bind their accepted
    intrinsic PS-2/PS-3 proofs; no proof-required vocabulary survives."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    route_spec_full = current.split("次表を active `RouteSpec`", 1)[1].split(
        "`REFIX` は RouteSpec", 1
    )[0]

    # stale obligation vocabulary must not survive in the active RouteSpec
    for token in ("proof-required", "ΣA proof別途", "ΣA proofが別途必要"):
        assert token not in route_spec_full, (
            f"{FR_SPEC_DOC}: stale ΣA token in RouteSpec: {token}"
        )

    # canonical acceptance records (short SHA + minors SHA) in §10.5.4/§10.7
    for marker in (
        "R-PS1 PASS、fixed SHA `f875d76`; minors `050156b`",
        "R-PS2 PASS、fixed SHA `540d0c1`; minors `4d0f636`",
        "R-PS3 R2 PASS、fixed SHA `65bb02e`",
    ):
        assert marker in current, (
            f"{FR_SPEC_DOC}: missing PS acceptance record: {marker}"
        )

    # row-level intrinsic refs carry full SHAs prefixed by the ledger records
    for short, full in (
        ("4d0f636", "4d0f636c6b4c2e05bd09912164f97ff06e35ba41"),
        ("65bb02e", "65bb02ef9f410460f127ad2339e49d8c903fe377"),
    ):
        assert full.startswith(short)
        assert full in route_spec_full, (
            f"{FR_SPEC_DOC}: RouteSpec missing intrinsic PS SHA {full}"
        )

    # both promoted rows demand the accepted ledger, the frequency witness,
    # and their own intrinsic SHA tuples (positional, independent of the RF
    # test's row_source_expectations)
    ps2_full = "4d0f636c6b4c2e05bd09912164f97ff06e35ba41"
    ps3_full = "65bb02ef9f410460f127ad2339e49d8c903fe377"
    for prefix in ("| `K2Q-aff-u`:", "| `generalized-singleton-u`:"):
        rows = [
            line
            for line in route_spec_full.splitlines()
            if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"{FR_SPEC_DOC}: row {prefix} count != 1"
        assert "polynomial-envelope / accepted(assembly_proof_ref)" in rows[0]
        assert "`leaf_phase_max` witness 必須" in rows[0]
        assert f"§10.5.4 補題 PΣ-2,{ps2_full},PASS" in rows[0], (
            f"{FR_SPEC_DOC}: row {prefix} lost PS-2 intrinsic ref"
        )
        assert f"§10.5.4 補題 PΣ-3,{ps3_full},PASS" in rows[0], (
            f"{FR_SPEC_DOC}: row {prefix} lost PS-3 intrinsic ref"
        )

    # active-region stale prose (luna R-PS4 M1): consumer sentences must not
    # keep describing the ΣA proof as an open blocker or PΣ-3 as unclaimed
    for token in (
        "PΣ-3/PΣ-4 は非主張",
        "polynomial ΣA proof、",
        "の polynomial ΣA proofが",
        "PΣ-4 で行う",
        "PΣ-4で行う",
    ):
        assert token not in current, (
            f"{FR_SPEC_DOC}: stale ΣA consumer prose: {token}"
        )

    # §10.5.4 state table, bound row-by-row
    ps_table_rows = {
        "| PΣ-1 局所補題 |": "R-PS1 PASS、fixed SHA `f875d76`; minors `050156b`",
        "| PΣ-2 max-envelope lift |": (
            "R-PS2 PASS、fixed SHA `540d0c1`; minors `4d0f636`"
        ),
        "| PΣ-3 ray-wide ledger |": "R-PS3 R2 PASS、fixed SHA `65bb02e`",
        "| PΣ-4 route 昇格 |": "R-PS4 R3 PASS、fixed SHA `58b9c9f`",
    }
    ps_section = current.split("#### 10.5.4", 1)[1]
    for prefix, fragment in ps_table_rows.items():
        rows = [
            line for line in ps_section.splitlines() if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"{FR_SPEC_DOC}: PS table row {prefix} count != 1"
        assert fragment in rows[0], (
            f"{FR_SPEC_DOC}: PS table row {prefix} lost record {fragment}"
        )

    # §10.4 record vocabulary forbids NONE for accepted polynomial-envelope
    assert "`NONE` を許さない" in current

    # §10.7 ledger rows, bound row-by-row: acceptance names all five SHAs,
    # surgery row stays 査読待ち until the audit passes
    ledger_section = current.split("### 10.7 S4-0 acceptance ledger", 1)[1]
    ps_rows = [
        line for line in ledger_section.splitlines()
        if line.startswith("| S4-0.PS |")
    ]
    assert len(ps_rows) == 1, f"{FR_SPEC_DOC}: S4-0.PS row count != 1"
    for sha in ("`f875d76`", "`050156b`", "`540d0c1`", "`4d0f636`", "`65bb02e`"):
        assert sha in ps_rows[0], f"{FR_SPEC_DOC}: S4-0.PS row lost SHA {sha}"
    promote_rows = [
        line for line in ledger_section.splitlines()
        if line.startswith("| S4-0.PS-PROMOTE |")
    ]
    assert len(promote_rows) == 1, (
        f"{FR_SPEC_DOC}: S4-0.PS-PROMOTE row count != 1"
    )
    assert "**PASS (R-PS4 R3、fixed SHA `58b9c9f`)**" in promote_rows[0], (
        f"{FR_SPEC_DOC}: S4-0.PS-PROMOTE row lost acceptance record"
    )
    # the audit-wait marker must not survive anywhere in the active region
    assert "R-PS4 査読待ち" not in current, (
        f"{FR_SPEC_DOC}: stale R-PS4 audit-wait marker after acceptance"
    )


def test_s4b_cov0_selection_schema_spec_surfaces():
    """COV0 surgery: selector spec present, lemma S4b-COV stays unclaimed."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]

    # §10.4 RouteRecord carries the selection_witness field
    assert "| `selection_witness` |" in current
    assert "route ID が selector 値と一致しなければ無効" in current

    # §10.5.5 selector spec: closed world, equal-sign convention, fail-close,
    # K_T index contract, terminal record, guard/certificate coupling
    for fragment in (
        "CanonicalNodeFormEnum := {root-2+1, binary-pure-atom, binary-poly-deg12,",
        "`uncertified` として S4b-α/β を fail-close",
        "等号 `M_k=1/8` は held(`QR5-w`)",
        "`uncertified` として fail-close",
        "K_T := {1,…,N−1}",
        "`TerminalRecord`** へ送り",
        "RayCoverageManifest_{θ,T}",
        "coverage 用の有限再分割は行わない",
        "far 条件は schema でなく selector witness が",
        "`A_{H,N}`/`C_step,N` は**定義しない**",
        "`k∈K_T` 上で主張する",
    ):
        assert fragment in current, (
            f"{FR_SPEC_DOC}: COV0 spec fragment missing: {fragment}"
        )

    # the selection_witness FIELD ROW itself must carry the 4-tuple and the
    # guard coupling (luna R-COV0 R2: section-wide token search is not enough)
    sw_rows = [
        line for line in current.splitlines()
        if line.startswith("| `selection_witness` |")
    ]
    assert len(sw_rows) == 1, f"{FR_SPEC_DOC}: selection_witness row count != 1"
    assert (
        "(canonical_node_form,degree_class,root_held_guard,threshold_certificate)"
        in sw_rows[0]
    ), f"{FR_SPEC_DOC}: selection_witness row lost the 4-tuple"
    assert "`QR5-w`⇒held、`root-far`⇒far を必須" in sw_rows[0], (
        f"{FR_SPEC_DOC}: selection_witness row lost guard coupling"
    )

    # accepted proof bodies stay untouched: PS-3 keeps its accepted k=1..N sum
    # (the K_T restriction lives ONLY in the §10.5.5 consumer-side contract,
    # per the source_ref content-SHA rule — luna R-COV0 R2 PROV-01)
    assert "Σ_{k=1}^{N} [A_{H,k} + κ_H Λ_{H,k} ε_chain]" in current, (
        f"{FR_SPEC_DOC}: accepted PS-3 ledger sum drifted"
    )
    assert "v0.12.2 index 注" not in current, (
        f"{FR_SPEC_DOC}: in-body index note reintroduced into accepted proof"
    )

    # the coverage lemma must remain unclaimed until R-COV1 passes, and no
    # premature acceptance may appear anywhere in the active region
    cov_section = current.split("#### 10.5.5", 1)[1].split("### 10.6", 1)[0]
    # acceptance markers in §10.5.5: COV0 row, COV1 row, and the proof-body
    # label — exactly three, no more (fail-closed against silent additions)
    assert cov_section.count("**accepted**") == 2, (
        f"{FR_SPEC_DOC}: unexpected acceptance count inside §10.5.5"
    )
    cov1_ledger = [
        line
        for line in current.split("### 10.7 S4-0 acceptance ledger", 1)[1].splitlines()
        if line.startswith("| S4-0.COV1 |")
    ]
    assert len(cov1_ledger) == 1, f"{FR_SPEC_DOC}: S4-0.COV1 row count != 1"
    assert "**PASS (R-COV1 R4、fixed SHA `c36d818`)**" in cov1_ledger[0], (
        f"{FR_SPEC_DOC}: S4-0.COV1 row lost acceptance record"
    )
    lemma_block = cov_section.split("**補題 S4b-COV", 1)[1].split(
        "| ID | scope | state |", 1
    )[0]
    assert "(COV-0) canonical form closure" in lemma_block, (
        f"{FR_SPEC_DOC}: COV-0 obligation missing from the lemma block itself"
    )
    assert "(COV-1)" in lemma_block and "(COV-2)" in lemma_block, (
        f"{FR_SPEC_DOC}: COV-1/COV-2 missing from the lemma block"
    )
    cov0_rows = [
        line for line in cov_section.splitlines()
        if line.startswith("| COV0 selection schema 手術 |")
    ]
    assert len(cov0_rows) == 1, f"{FR_SPEC_DOC}: COV0 row count != 1"
    assert "R-COV0 R3 PASS、fixed SHA `256ab38`" in cov0_rows[0], (
        f"{FR_SPEC_DOC}: COV0 row lost acceptance record"
    )
    assert "R-COV0 査読待ち" not in current, (
        f"{FR_SPEC_DOC}: stale R-COV0 audit-wait marker after acceptance"
    )
    ledger_section = current.split("### 10.7 S4-0 acceptance ledger", 1)[1]
    cov0_ledger = [
        line for line in ledger_section.splitlines()
        if line.startswith("| S4-0.COV0 |")
    ]
    assert len(cov0_ledger) == 1, f"{FR_SPEC_DOC}: S4-0.COV0 row count != 1"
    assert "**PASS (R-COV0 R3、fixed SHA `256ab38`)**" in cov0_ledger[0], (
        f"{FR_SPEC_DOC}: S4-0.COV0 row lost acceptance record"
    )
    rows = [
        line for line in cov_section.splitlines()
        if line.startswith("| COV1 canonical coverage lemma |")
    ]
    assert len(rows) == 1, f"{FR_SPEC_DOC}: COV1 row count != 1"
    assert "**accepted**(R-COV1 R4 PASS、fixed SHA `c36d818`)" in rows[0], (
        f"{FR_SPEC_DOC}: COV1 row lost acceptance record"
    )
    assert "(COV-0)(COV-1)(COV-2)" in rows[0], (
        f"{FR_SPEC_DOC}: COV1 row lost an obligation id"
    )


def test_s4a_program_states_fail_closed():
    """§10.8 S4a program: W1 stays draft, W2..EW stay unclaimed until review."""

    current = FR_SPEC_DOC.read_text(encoding="utf-8").split("## 11. 版履歴", 1)[0]
    s4a = current.split("### 10.8 S4a envelope assembly program", 1)[1]

    w1_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| W1 Child-reserve interface |")
    ]
    assert len(w1_rows) == 1, f"{FR_SPEC_DOC}: W1 row count != 1"
    assert "**accepted**(R-W1 R2 PASS、fixed SHA `a59768e`)" in w1_rows[0], (
        f"{FR_SPEC_DOC}: W1 row lost acceptance record"
    )
    w2_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| W2 Pair norming |")
    ]
    assert len(w2_rows) == 1, f"{FR_SPEC_DOC}: W2 row count != 1"
    assert "**accepted**(R-W2 PASS、fixed SHA `a0fcd10`)" in w2_rows[0], (
        f"{FR_SPEC_DOC}: W2 row lost acceptance record"
    )
    c0_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| C0 Terminal two-anchor |")
    ]
    assert len(c0_rows) == 1, f"{FR_SPEC_DOC}: C0 row count != 1"
    assert "**accepted**(R-C0 R2 PASS、fixed SHA `f31cca0`)" in c0_rows[0], (
        f"{FR_SPEC_DOC}: C0 row lost acceptance record"
    )
    m1_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| M1 mode audit |")
    ]
    assert len(m1_rows) == 1, f"{FR_SPEC_DOC}: M1 row count != 1"
    assert "**accepted**(R-M1 R2 PASS、fixed SHA `fd18e9d`)" in m1_rows[0], (
        f"{FR_SPEC_DOC}: M1 row lost acceptance record"
    )
    w3_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| W3 Weighted chain |")
    ]
    assert len(w3_rows) == 1, f"{FR_SPEC_DOC}: W3 row count != 1"
    assert "**accepted**(R-W3 R2 PASS、fixed SHA `4086ef9`)" in w3_rows[0], (
        f"{FR_SPEC_DOC}: W3 row lost acceptance record"
    )
    w4_rows = [
        line for line in s4a.splitlines()
        if line.startswith("| W4 Terminal-cancelled exit |")
    ]
    assert len(w4_rows) == 1, f"{FR_SPEC_DOC}: W4 row count != 1"
    assert "**accepted**(R-W4 R2 PASS、fixed SHA `cb87eee`)" in w4_rows[0], (
        f"{FR_SPEC_DOC}: W4 row lost acceptance record"
    )
    for prefix in (
        "| EW-B original-collision bridge |",
        "| EW final |",
    ):
        rows = [line for line in s4a.splitlines() if line.startswith(prefix)]
        assert len(rows) == 1, f"{FR_SPEC_DOC}: S4a row {prefix} count != 1"
        assert "**accepted**(R-EW R2 PASS、fixed SHA `b39216f`)" in rows[0], (
            f"{FR_SPEC_DOC}: S4a row {prefix} lost acceptance record"
        )
    # S4c acceptance is recorded with the reviewed SHA
    assert current.count("R-S4C R3 PASS、fixed SHA `b6bbe01`") >= 3, (
        f"{FR_SPEC_DOC}: S4c acceptance records missing"
    )
    # FR7 no-return: forbidden inputs stay out of the final surfaces (S4a
    # program text and RouteSpec rows); prohibition-context mentions live in
    # §10.4/§10.5.5 only
    route_spec_full = current.split("次表を active `RouteSpec`", 1)[1].split(
        "`REFIX` は RouteSpec", 1
    )[0]
    kernel_bodies = current.split("#### 10.5.2", 1)[1].split("### 10.6", 1)[0]
    for token in ("U_F", "1/t_m", "DC discount"):
        assert token not in s4a.split("### 10.9", 1)[0], (
            f"{FR_SPEC_DOC}: forbidden FR7 token {token} in §10.8"
        )
        assert token not in route_spec_full, (
            f"{FR_SPEC_DOC}: forbidden FR7 token {token} in RouteSpec"
        )
    # §10.5.2-10.5.5 accepted bodies: DC discount / 1/t_m absent entirely;
    # U_F appears exactly once, and only inside COV-0's non-producer exclusion
    for token in ("1/t_m", "DC discount"):
        assert token not in kernel_bodies, (
            f"{FR_SPEC_DOC}: forbidden FR7 token {token} in §10.5.2-10.5.5"
        )
    uf_count = kernel_bodies.count("U_F")
    assert uf_count == 1, (
        f"{FR_SPEC_DOC}: U_F count in §10.5.2-10.5.5 is {uf_count}, expected 1"
    )
    uf_idx = kernel_bodies.find("U_F")
    uf_ctx = kernel_bodies[max(0, uf_idx - 200):uf_idx + 100]
    assert "RouteRecord` producer ではない" in uf_ctx or "producer ではない" in uf_ctx, (
        f"{FR_SPEC_DOC}: the single U_F mention left its exclusion context"
    )
    # S4c rows stay proof draft until R-S4C passes
    s4c_section = current.split("### 10.9 S4c closure", 1)[1]
    for prefix in (
        "| S4c-i N3′/N4 ledger |",
        "| S4c-ii FR7 audit |",
        "| S4c-iii FR acceptance |",
    ):
        rows = [
            line for line in s4c_section.splitlines()
            if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"{FR_SPEC_DOC}: S4c row {prefix} count != 1"
        assert "**accepted**(R-S4C R3 PASS、fixed SHA `b6bbe01`)" in rows[0], (
            f"{FR_SPEC_DOC}: S4c row {prefix} lost acceptance record"
        )
    # the closure-doc c=3 sync block must exist and stay conservative
    closure_doc = (
        ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md"
    ).read_text(encoding="utf-8")
    assert "(N3′/N4 の c=3 具体化 — v1.8.13、FR 文書 v0.14.1 と同期)" in closure_doc
    assert "補題 N 本体の量化完備化・一般 c の" in closure_doc
    assert "証明(G1′)を主張しない" in closure_doc
    # (S4-Ew) closure must be recorded with the reviewed SHA, and S4c stays open
    assert "**S4a program 完結・(S4-Ew) 閉鎖**" in current, (
        f"{FR_SPEC_DOC}: S4a closure record missing from header"
    )
    s4c_rows = [
        line for line in current.splitlines()
        if line.startswith("| S4c proofs |")
    ]
    assert len(s4c_rows) == 1 and "R-S4C R3 PASS" in s4c_rows[0], (
        f"{FR_SPEC_DOC}: S4c ledger row lost acceptance record"
    )
    # U1 retirement is a recorded design decision, not a silent deletion
    assert "U1 の退役(design 決定)" in s4a
    assert "capability として保持する(削除しない)" in s4a


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


GC_PROGRAM_DOC = ROOT / "docs" / "2026-08-18-general-c-block-frame-program--wip.md"

F3PRIME_SPEC_ONLY_FRAGMENTS = (
    "z\u2075/\u221a5!",
    "A_j = \u2212B_j\u00b2",
    "profile (0,1,5)",
    "h_\u03b2/\u2016h_\u03b2\u2016",
)


def test_f3prime_gc_program_doc_uses_pointer_not_restatement():
    """The GC program doc must point at the FR spec \u00a77 canonical F3-prime
    witness and must not restate its defining formulas/profile
    (luna R-GC4B0 R6 [04])."""

    text = GC_PROGRAM_DOC.read_text(encoding="utf-8")
    pointer = "\u6b63\u672c: FR \u6587\u66f8 \u00a77"
    assert pointer in text
    for fragment in F3PRIME_SPEC_ONLY_FRAGMENTS:
        assert fragment not in text, (
            f"F3-prime restatement returned: {fragment!r}"
        )

    # luna R-GC4B0 R7 [02]: a document-wide pointer check cannot detect the
    # removal of the (2c) pointer while pointers elsewhere (e.g. section 3)
    # survive, so the (2c) slice must carry its own pointer.
    start = text.index("*(2c) counting")
    end = text.index("**(AD-3)", start)
    section_2c = text[start:end]
    assert pointer in section_2c, "(2c) lost its FR spec pointer"


def test_qrg_witness_schema_is_declared():
    """GC-4A.5a0 (QRG) must declare the versioned v4 schema and the typed
    qr_global_witness fields (luna R-GC4A5A0 R1 [03][05])."""

    text = GC_PROGRAM_DOC.read_text(encoding="utf-8")
    for fragment in (
        "GCRouteRecord-v4",
        "qr_global_witness",
        "同一オブジェクト参照",
        "closed-world fail-closed",
    ):
        assert fragment in text, f"QRG schema fragment missing: {fragment!r}"

    # luna R-GC4A5A0 R2 [01]: the accepted WE9 section must carry the v4
    # reference (via its annotation) so the consumption contract types align.
    start = text.index("### 8.13 GC-4A.4")
    end = text.index("### 8.14")
    section_we9 = text[start:end]
    assert "GCRouteRecord-v4" in section_we9, (
        "WE9 section lost its v4 alignment"
    )
    # luna R-GC4A5A0 R3 [01]: the consumer type itself must reference v4 --
    # no bare v3 reference may remain in the WE9 section (the annotation may
    # mention v3 only inside "v3 から置換" / "v3 不変" style audit phrases).
    import re as _re
    bare_v3 = [
        m for m in _re.finditer(r"GCRouteRecord-v3", section_we9)
        if "から置換" not in section_we9[m.start():m.start() + 40]
        and "不変" not in section_we9[m.start():m.start() + 60]
    ]
    assert not bare_v3, "WE9 section still has a bare v3 consumer reference"


def test_ptn_spec_interface_declared():
    """GC-4A.5a1 (PTN-SPEC) must declare the typed BORD-22/PTN-22 interface
    (consult #15, luna R-GC4A5A1 R1-R3). Checks are structural: the section
    is split into its (PS-n) blocks and each obligation is verified inside
    the block that owns it, including the constructor-level exclusivity of
    the valid|nogo union (R3-01)."""

    import re

    text = GC_PROGRAM_DOC.read_text(encoding="utf-8")
    start = text.index("### 8.16 GC-4A.5a1")
    # the section ends at the next packet section (S8.17) if present,
    # else at the experiment ledger
    try:
        end = text.index("### 8.17", start)
    except ValueError:
        end = text.index("## 9. 早期検証実験台帳")
    section = text[start:end]

    # split into PS blocks: ps[n] = text of (PS-n)
    parts = re.split(r"\*\*\(PS-(\d)\)", section)
    ps = {
        int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)
    }
    assert set(ps) == set(range(1, 10)), f"PS blocks missing: {sorted(ps)}"

    # PS-1 (R1-01): two-layer raw/reduced typing and gauge invariance
    for frag in ("未約分", "g(𝐁) = g(𝐁̃)", "common gauge"):
        assert frag in ps[1], f"PS-1 missing: {frag!r}"

    # PS-2 (R1-01): d0 is the unreduced divisor order, same object;
    # reduced near-common zeros are a separate field
    for frag in ("divisor_record", "同一オブジェクト", "D の零点とは別物"):
        assert frag in ps[2], f"PS-2 missing: {frag!r}"

    # PS-3 (R1-03/R2-01): identity refs into GC-3 D-PBK-22 required keys;
    # active_children_nonzero must be coupled to its consumption condition
    for frag in (
        "D-PBK-22 record 参照",
        "certificate_ref",
        "η_dw witness",
        "collision-scale witness",
    ):
        assert frag in ps[3], f"PS-3 missing: {frag!r}"
    acn = ps[3].index("active_children_nonzero")
    ban = ps[3].index("t3_witness 生成禁止")
    assert 0 < ban - acn < 200, (
        "PS-3: active_children_nonzero not coupled to its generation ban"
    )

    # PS-4 (R1-02): zf-scope split and same-object window refs
    for frag in (
        "zf_scope",
        "W_zf 被覆 witness",
        "A.3a は供給しない",
        "we9_witness-v1 参照",
        "d10_witness-v1 参照",
        "disjoint-forbidden",
        "zf/stratum 条件は省略不能",
    ):
        assert frag in ps[4], f"PS-4 missing: {frag!r}"
    # R1-06: probe results are authored only in section 9
    assert "BORD22-PROBE" in ps[4]
    for restated in ("0.25/ε", "slope", "plateau", "2.8×10"):
        assert restated not in section, (
            f"PTN-SPEC section restates probe result: {restated!r}"
        )

    # PS-5: two-chart covering with completeness as the stated obligation
    for frag in ("outer chart", "inner chart", "被覆完備性"):
        assert frag in ps[5], f"PS-5 missing: {frag!r}"

    # PS-6/PS-7: QR exit and the registered (not claimed) statement
    assert "qr_global_witness" in ps[6]
    assert "‖g‖_W ≤ C₂₂ · (L_C/s)⁹ · ‖g‖_S" in ps[7]
    assert "本 packet はこの不等式を主張しない" in ps[7]

    # PS-8: the seven-item BORD-22 coverage checklist
    for mark in "①②③④⑤⑥⑦":
        assert mark in ps[8], f"PS-8 checklist missing item {mark}"

    # PS-9 (R1-04/05, R2-02, R3-01): constructor-level exclusivity.
    # Split the union into its valid/nogo sub-blocks and check each side.
    assert "ptn22_witness-v1 := valid | nogo" in ps[9]
    v_at = ps[9].index("`valid := (")
    n_at = ps[9].index("`nogo := (")
    rule_at = ps[9].index("**消費規則**")
    assert v_at < n_at < rule_at, "PS-9: valid/nogo/rule order broken"
    valid_sub = ps[9][v_at:n_at]
    nogo_sub = ps[9][n_at:rule_at]
    rule_sub = ps[9][rule_at:]
    # valid carries checked_clear only, and the mandatory v != 0 gate
    assert "checked_clear" in valid_sub
    assert "detected" not in valid_sub, (
        "PS-9: valid sub-block must not admit a detected scan"
    )
    assert "v ≢ 0 必須" in valid_sub
    assert "valid の生成を**禁止**" in valid_sub
    assert "qr_global_witness" in valid_sub
    # nogo carries detected only
    assert "detected" in nogo_sub
    assert "checked_clear" not in nogo_sub, (
        "PS-9: nogo sub-block must not admit a checked_clear scan"
    )
    # consumption rule couples valid-only consumption with the nogo bar
    assert "valid" in rule_sub and "のみ" in rule_sub
    assert "nogo の証明経路での消費は禁止" in rule_sub

    # ledger rows: deps recorded, obligations stay open (never resolved by
    # forwarding), COND9 stays withdrawn
    rows = {
        prefix: [l for l in text.splitlines() if l.startswith(prefix)]
        for prefix in (
            "| GC-4A.5a1 PBK22-PTN-SPEC ",
            # consult #16 split GC-5-T2 into three packets; all four stay
            # open A.5a blocking obligations until accepted
            "| GC-5-T2a BORD22-ATLAS ",
            "| GC-5-T2b BORD22-FRAME ",
            "| GC-5-T2c BORD22-FLOOR ",
            "| GC-5-T3 PTN-22 ",
            "| GC-4A.5a PBK22-COND9 ",
        )
    }
    for prefix, found in rows.items():
        assert len(found) == 1, f"ledger row {prefix!r} count != 1"
    a5a1 = rows["| GC-4A.5a1 PBK22-PTN-SPEC "][0]
    assert "GC-3" in a5a1 and "GC-4C.0" in a5a1, "A.5a1 deps lost GC-3/GC-4C.0"
    # accepted at R-GC4A5A1 R4; the acceptance record must survive
    assert "accepted" in a5a1 and "5d7400a" in a5a1, (
        "A.5a1 lost its acceptance record (R-GC4A5A1 R4, fixed SHA 5d7400a)"
    )
    for prefix in (
        "| GC-5-T2a BORD22-ATLAS ",
        "| GC-5-T2b BORD22-FRAME ",
        "| GC-5-T2c BORD22-FLOOR ",
        "| GC-5-T3 PTN-22 ",
    ):
        row = rows[prefix][0]
        # states may progress (open -> drafted -> accepted), but the A.5a
        # blocking-obligation marking must never be dropped ("forwarding"
        # a packet to GC-5 must not resolve A.5a -- consult #15)
        assert "blocking obligation" in row, (
            f"{prefix!r} lost its A.5a blocking-obligation marking"
        )
    # T3 consumes the completed BORD-22 chain, not the atlas alone
    assert "GC-5-T2c" in rows["| GC-5-T3 PTN-22 "][0]
    assert "withdrawn" in rows["| GC-4A.5a PBK22-COND9 "][0]

    # the probe ledger row stays the sole authoring location and stays a
    # diagnostic (never a proof substitute)
    probe_rows = [
        l for l in text.splitlines() if l.startswith("| BORD22-PROBE ")
    ]
    assert len(probe_rows) == 1
    assert "診断であり証明の代替ではない" in probe_rows[0]


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


def test_kawasaki_readme_generated_block_matches_artifact():
    """Register issue #180 in the repository-wide claim-surface policy."""
    import importlib.util

    exp_dir = EXPERIMENTS / "32_kawasaki_data"
    spec = importlib.util.spec_from_file_location(
        "kawasaki_pump_result_summary", exp_dir / "pump_result_summary.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = module.load_json(exp_dir / "pump_results.json")
    readme = (exp_dir / "README.md").read_text(encoding="utf-8")
    start = readme.find(module.BEGIN)
    stop = readme.find(module.END)
    assert start >= 0 and stop >= 0, "experiment 32 lost its generated markers"
    block = readme[start : stop + len(module.END)]
    assert block == module.render(results), (
        "experiment 32 README diverges from pump_results.json; "
        "run pump_result_summary.py --write instead of editing the block"
    )


def test_exp27_closure_table_is_the_complete_status_surface():
    """Issue #126 closes by one table, while historical run output stays evidence.

    The test checks the status-surface shape without copying its scientific
    dispositions into a second authoring location.  Exact dispositions are a
    fixed-SHA review responsibility.
    """
    readme = (EXPERIMENTS / "27_row1_classical" / "README.md").read_text(
        encoding="utf-8"
    )
    rows = {
        match.group(1): line
        for line in readme.splitlines()
        if (match := re.match(r"\| (E27-[A-Z]\d) \|", line))
    }
    assert set(rows) == {
        "E27-D0",
        "E27-P1",
        "E27-E1",
        "E27-V1",
        "E27-R1",
        "E27-K1",
        "E27-N1",
    }
    assert all(line.count("|") == 6 for line in rows.values())
    assert "sole authoring location" in readme
    assert "RUN_REPORT.md" in readme and "not acceptance surfaces" in readme

    log = (ROOT / "docs" / "research-log.md").read_text(encoding="utf-8")
    pointer = log[log.index("## 2026-09-03 — experiment 27 / issue #126 closure pointer"):]
    assert "experiments/27_row1_classical/README.md" in pointer
    for claim_shaped_term in ("R_obs", "K > 1", "Wigner", "negative result"):
        assert claim_shaped_term not in pointer, (
            "the research-log pointer must not become a second exp27 "
            f"status surface: {claim_shaped_term}"
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


def test_lemma_n_c3_program_states_fail_closed():
    """§4.3.6 Lemma N (c<=3) packet ledger must keep its acceptance records.

    Each packet row carries a fixed-SHA review record; losing one silently
    would let the quantified c<=3 claim float free of its evidence. The
    non-claim boundary (general c / G1' stays open, no human review) must
    also survive edits.
    """
    closure = (
        ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md"
    ).read_text(encoding="utf-8")
    section = closure.split("### 4.3.6 補題 N(c≤3)の量化 program", 1)[1]
    section = section.split("### 4.4 ", 1)[0]
    expected = {
        "| N-P0 ": "R-NP0 R3 PASS、fixed SHA `2619b10`",
        "| N-P1 ": "R-NP1 R2 PASS、fixed SHA `c893f04`",
        "| N-P2 ": "R-NP2 R2 PASS、fixed SHA `8f64cd0`",
        "| N-P3 ": "R-NP3 R1 PASS、fixed SHA `f86acae`",
        "| N-P4 ": "R-NP4 R1 PASS、fixed SHA `1058eda`",
        "| N-P5 ": "R-NP5 R1 PASS、fixed SHA `ef9d463`",
    }
    for prefix, record in expected.items():
        rows = [
            line for line in section.splitlines() if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"closure doc: packet row {prefix} count != 1"
        assert record in rows[0], (
            f"closure doc: packet row {prefix} lost acceptance record {record}"
        )
    # non-claim boundary stays conservative
    assert "一般 c の補題 N(G1′ 本体)" in section
    assert "人間査読未実施" in section or "人間による査読は未実施" in section
    # vocabulary split: coarse 2|1 is not the FR-internal nested 2+1
    assert "内部 rate tree" in section
    # coordinate binding note survives
    assert "U_m^{-1}v^{FR}_{ℓ,m}" in section


def test_nc_program_states_fail_closed():
    """§4.4.1 NC-program ledger must keep acceptance records and stay conservative.

    The k<=3 vertical chain (T_{k<=3}/C1_{k<=3}) is conditional on G6/G8; the
    audit's conservative verdict and the packet SHAs must survive edits.
    """
    closure = (
        ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md"
    ).read_text(encoding="utf-8")
    section = closure.split("#### 4.4.1 c≤3 接続監査と NC program", 1)[1]
    section = section.split("## 5. 補題 L2b", 1)[0]
    expected = {
        "| NC-1 ": "R-NC1 R3 PASS、fixed SHA `b003341`",
        "| NC-2 ": "R-NC2 R3 PASS、fixed SHA `36108d1`",
        "| NC-3 ": "R-NC3 R2 PASS、fixed SHA `30658b1`",
        "| NC-4 ": "R-NC4 R2 PASS、fixed SHA `7529bce`",
    }
    for prefix, record in expected.items():
        rows = [
            line for line in section.splitlines() if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"closure doc: NC row {prefix} count != 1"
        assert record in rows[0], (
            f"closure doc: NC row {prefix} lost acceptance record {record}"
        )
    # audit stays conservative: G6/G8 remain open conditions, no unconditional claim
    assert "G6/G8 が閉じるまで proof-body の完全性は主張しない" in section
    assert "`T_{k≤3}` の無条件宣言もしない" in section
    # G8 scope extension is recorded in the gap ledger
    assert "affine metaplectic 表現の強連続性" in closure


def test_g6_g8_closure_records_fail_closed():
    """G6/G8 ledger rows must keep acceptance records; draft status must survive.

    G6 (phase alignment, S7) accepted at R-G6 R1 `5d64f36`; G8 (covariance
    write-up, S9.1, extended scope) accepted at R-G8 R2 `dc76258`. Their
    closure makes the k<=3 vertical chain condition-free as a *draft* -- the
    no-human-review caveat must never be dropped from the claim hierarchy.
    """
    closure = (
        ROOT / "docs" / "2026-08-02-gaussian-border-rank-closure--wip.md"
    ).read_text(encoding="utf-8")
    for prefix, record in {
        "| G6 ": "R-G6 R1 ACCEPTED、fixed SHA `5d64f36`",
        "| G8 ": "R-G8 R2 ACCEPTED、fixed SHA `dc76258`",
    }.items():
        rows = [
            line for line in closure.splitlines() if line.startswith(prefix)
        ]
        assert len(rows) == 1, f"closure doc: gap row {prefix} count != 1"
        assert record in rows[0], (
            f"closure doc: gap row {prefix} lost acceptance record {record}"
        )
        assert "closed" in rows[0], f"closure doc: gap row {prefix} not closed"
    # claim hierarchy: condition-free k<=3 chain stays a draft, never a theorem
    assert "G 条件なしの証明ドラフト完全体" in closure
    hierarchy = closure.split("**主張の階層(G6/G8 受理後更新)**", 1)[1]
    hierarchy = hierarchy.split("\n\n", 1)[0]
    assert "人間による査読は未実施" in hierarchy
    assert "外部査読体制は現存しない" in hierarchy
