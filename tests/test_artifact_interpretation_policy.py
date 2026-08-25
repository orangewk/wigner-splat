"""Regression policy for issue #71 numerical artifacts."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {"claim", "description", "interpretation"}


def _keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _keys(nested)


def test_issue_71_artifacts_have_no_conclusion_prose_fields():
    artifacts = [
        ROOT / "experiments/22_kcurves/empirical_upper_bound.json",
        ROOT / "experiments/22_kcurves/data_proxy.json",
        ROOT / "experiments/23_gkp_robust_zeros/robust_zero_results.json",
    ]
    for artifact in artifacts:
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        assert FORBIDDEN.isdisjoint(_keys(payload)), artifact


def test_issue_71_generator_sources_have_no_conclusion_strings():
    generators = [
        ROOT / "experiments/22_kcurves/run.py",
        ROOT / "experiments/22_kcurves/kcurve_io.py",
        ROOT / "experiments/23_gkp_robust_zeros/run.py",
    ]
    forbidden = ("R_epsilon", "claim")
    for generator in generators:
        source = generator.read_text(encoding="utf-8").lower()
        assert all(token.lower() not in source for token in forbidden), generator


def test_kawasaki_result_artifact_has_no_conclusion_prose_fields():
    artifact = ROOT / "experiments/32_kawasaki_data/pump_results.json"
    forbidden = {
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
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert forbidden.isdisjoint(_keys(payload)), artifact
