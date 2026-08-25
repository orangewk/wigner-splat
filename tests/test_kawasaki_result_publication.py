"""Publication-policy tests for experiment 32's fixed result artifact."""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "32_kawasaki_data"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "kawasaki_pump_result_publication", EXP / "pump_result_summary.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


publication = _load_module()


def test_fixed_artifact_is_complete_and_data_derived():
    payload = publication.load_json(publication.ARTIFACT_PATH)
    stats = publication.validate(payload)
    plan = publication.load_json(publication.PLAN_PATH)
    manifest = publication.load_json(publication.MANIFEST_PATH)
    pump_sources = [
        row
        for row in manifest["files"]
        if row.get("series") == "pump_power"
        and row.get("condition", {}).get("pump_mw")
        in plan["development_pump_mw"] + plan["validation_pump_mw"]
    ]
    expected_primary = (
        len(pump_sources)
        * len(plan["split"]["reshuffle_seeds"])
        * len(plan["arms"]["scale"])
        * len(plan["arms"]["phase"])
    )
    assert sum(stats["classifications"].values()) == expected_primary
    assert stats["result_rows"] == expected_primary * len(plan["models"])


def test_validator_rejects_missing_or_mutated_claim_rows():
    payload = publication.load_json(publication.ARTIFACT_PATH)

    missing = copy.deepcopy(payload)
    missing["result_rows"].pop()
    with pytest.raises(publication.PublicationError):
        publication.validate(missing)

    reclassified = copy.deepcopy(payload)
    primary = next(
        row for row in reclassified["result_rows"] if row["classification"] is not None
    )
    primary["classification"] = (
        "loss" if primary["classification"] != "loss" else "win"
    )
    with pytest.raises(publication.PublicationError):
        publication.validate(reclassified)

    comparison = copy.deepcopy(payload)
    comparison["comparison_rows"][0]["arm_values"]["stored/H1"] = None
    with pytest.raises(publication.PublicationError):
        publication.validate(comparison)
