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


def test_run_logs_are_excluded_from_the_scan():
    """The exclusion is deliberate; assert it stays deliberate.

    If a future edit makes the scan cover .log files, the withdrawn-claim check
    would demand rewriting committed evidence. This test fails first, so the
    reason gets read before that happens.
    """
    logs = _issue_71_paths(".log")
    assert logs, "expected committed run logs under the issue #71 experiments"
    assert not any(log in _issue_71_paths(".py") for log in logs)
