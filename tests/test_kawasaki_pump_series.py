"""Execution-contract tests for experiment 32; public values are not read."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "32_kawasaki_data"


def _load_module():
    sys.path.insert(0, str(EXP))
    spec = importlib.util.spec_from_file_location(
        "kawasaki_pump_series", EXP / "run_pump_series.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


pump = _load_module()


def test_plan_pins_four_arms_and_fixed_models():
    plan = pump.load_plan()
    assert [row["id"] for row in plan["arms"]["scale"]] == ["stored", "sqrt2"]
    assert [row["id"] for row in plan["arms"]["phase"]] == ["H1", "H2"]
    assert list(pump.arm_pairs(plan)) == [
        (plan["arms"]["scale"][0], plan["arms"]["phase"][0]),
        (plan["arms"]["scale"][0], plan["arms"]["phase"][1]),
        (plan["arms"]["scale"][1], plan["arms"]["phase"][0]),
        (plan["arms"]["scale"][1], plan["arms"]["phase"][1]),
    ]
    models = pump.model_map(plan)
    assert (models["bbdag_r4k4"]["R"], models["bbdag_r4k4"]["K"]) == (4, 4)
    assert models["mle16"]["n_max"] == 16
    assert models["mle10"]["n_max"] == 10


def test_split_is_shared_before_arm_transform_and_h2_flips_only_180_plus():
    plan = pump.load_plan()
    data = (
        (np.deg2rad(150), np.arange(10.0)),
        (np.deg2rad(180), np.arange(10.0) + 20),
        (np.deg2rad(210), np.arange(10.0) + 40),
    )
    train, test = pump.split_within_phase(data, seed=0, train_fraction=0.8)
    stored = plan["arms"]["scale"][0]
    sqrt2 = plan["arms"]["scale"][1]
    h1, h2 = plan["arms"]["phase"]
    primary = pump.apply_arm(train, stored, h1)
    phase_flip = pump.apply_arm(train, stored, h2)
    scale = pump.apply_arm(train, sqrt2, h1)
    np.testing.assert_array_equal(primary[0][1], phase_flip[0][1])
    np.testing.assert_array_equal(primary[1][1], -phase_flip[1][1])
    np.testing.assert_array_equal(primary[2][1], -phase_flip[2][1])
    np.testing.assert_allclose(scale[0][1], primary[0][1] * np.sqrt(2.0))
    assert [len(samples) for _theta, samples in train] == [8, 8, 8]
    assert [len(samples) for _theta, samples in test] == [2, 2, 2]


@pytest.mark.parametrize(
    "values, expected",
    [
        ({("stored", "H1"): "win", ("stored", "H2"): "win",
          ("sqrt2", "H1"): "win", ("sqrt2", "H2"): "win"},
         "convention-stable"),
        ({("stored", "H1"): "win", ("stored", "H2"): "win",
          ("sqrt2", "H1"): "loss", ("sqrt2", "H2"): "loss"},
         "unit-convention-dependent"),
        ({("stored", "H1"): "win", ("stored", "H2"): "loss",
          ("sqrt2", "H1"): "win", ("sqrt2", "H2"): "loss"},
         "phase-convention-dependent"),
        ({("stored", "H1"): "win", ("stored", "H2"): "loss",
          ("sqrt2", "H1"): "loss", ("sqrt2", "H2"): "win"},
         "unit-and-phase-convention-dependent"),
    ],
)
def test_convention_status_is_computed_from_all_four_classifications(
    values, expected
):
    assert pump.convention_status(values, pump.load_plan()) == expected


@pytest.mark.parametrize(
    "interval, expected",
    [((-0.2, -0.1), "win"), ((0.1, 0.2), "loss"), ((-0.1, 0.2), "unresolved")],
)
def test_classification_is_computed_from_ci(interval, expected):
    assert pump.classify(*interval, pump.load_plan()) == expected


def test_development_source_selection_cannot_load_validation_values(monkeypatch):
    manifest = {
        "files": [
            {
                "name": f"pump_{value}.mat",
                "role": "quadrature",
                "series": "pump_power",
                "condition": {"pump_mw": value},
            }
            for value in (1, 3, 10, 25)
        ]
    }
    loaded_names = []

    def fake_load(path, _manifest):
        loaded_names.append(path.name)
        return path.name

    monkeypatch.setattr(pump, "load_manifest", lambda: manifest)
    monkeypatch.setattr(pump, "load_condition", fake_load)
    _manifest, loaded = pump.load_pump_conditions(Path("outside"), [1])
    assert loaded == ["pump_1.mat"]
    assert loaded_names == ["pump_1.mat"]


def test_result_surface_keeps_model_rows_and_arm_comparison_separate():
    plan = pump.load_plan()
    rows = []
    for scale in ("stored", "sqrt2"):
        for phase in ("H1", "H2"):
            rows.append({
                "source_file": "source.mat",
                "reshuffle_seed": 0,
                "scale_arm": scale,
                "phase_arm": phase,
                "model": "bbdag_r4k4",
                "mode_count": 1,
                "fitted_eta": 0.8,
                "train_nll": 1.0 if scale == "stored" else 1.1,
                "test_nll": 1.2,
                "delta_nll_vs_mle16": -0.1,
                "ci_low": -0.2,
                "ci_high": -0.01,
                "classification": "win",
                "convention_status": "convention-stable",
            })
    comparisons = pump.build_comparison_rows(rows, plan)
    by_quantity = {row["quantity"]: row for row in comparisons}
    assert by_quantity["mode_count"]["comparison_status"] == "same-across-arms"
    assert by_quantity["train_nll"]["comparison_status"] == (
        "arm-specific-difference"
    )
    assert by_quantity["classification"]["convention_status"] == (
        "convention-stable"
    )
    assert by_quantity["train_nll"]["differences_vs_stored_H1"][
        "sqrt2/H2"
    ] == pytest.approx(0.1)


def test_validation_requires_matching_fixed_sha_review_record(tmp_path):
    development = tmp_path / "development.json"
    development.write_text(
        json.dumps({"development_gate": {"passed": True}}), encoding="utf-8"
    )
    plan_hash = "a" * 64
    runner_hash = "b" * 64
    git = {"head_sha": "c" * 40, "dirty": False}
    review = {
        "schema_version": 1,
        "review_status": "pass",
        "review_url": "https://example/review",
        "reviewed_git_sha": git["head_sha"],
        "plan_sha256": plan_hash,
        "runner_sha256": runner_hash,
        "development_artifact_sha256": pump.sha256_path(development),
    }
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(review), encoding="utf-8")
    assert pump.validate_review_record(
        review_path, development, plan_hash, runner_hash, git
    ) == review
    review["review_status"] = "pending"
    review_path.write_text(json.dumps(review), encoding="utf-8")
    with pytest.raises(pump.PumpSeriesError, match="passing review"):
        pump.validate_review_record(
            review_path, development, plan_hash, runner_hash, git
        )


def test_development_checkpoint_is_bound_to_runner_plan_and_git(tmp_path):
    expected = {
        "schema_version": 1,
        "plan_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "git_head_sha": "c" * 40,
        "source_file": "source.mat",
        "reshuffle_seed": 0,
        "scale_arm": "stored",
        "phase_arm": "H1",
        "init_seed": 0,
    }
    checkpoint = tmp_path / "checkpoint.json"
    attempt = {"init_seed": 0, "train_nll": 1.25}
    checkpoint.write_text(
        json.dumps({**expected, "attempt": attempt}), encoding="utf-8"
    )
    assert pump._load_development_checkpoint(checkpoint, expected) == attempt
    with pytest.raises(pump.PumpSeriesError, match="runner_sha256"):
        pump._load_development_checkpoint(
            checkpoint, {**expected, "runner_sha256": "d" * 64}
        )
