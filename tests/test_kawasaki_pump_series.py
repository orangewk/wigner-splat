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


def _synthetic_attempt(seed=0, *, model=None):
    model = pump.model_map(pump.load_plan())["bbdag_r4k4"] if model is None else model
    trace = [
        {
            "iteration": iteration,
            "train_nll": 1.5 - iteration * 1e-6,
            "fitted_eta": 0.8,
        }
        for iteration in range(25, model["iters"] + 1, 25)
    ]
    return {
        "init_seed": seed,
        "train_nll": trace[-1]["train_nll"],
        "fitted_eta": trace[-1]["fitted_eta"],
        "final_100_iteration_train_nll_drop": pump.convergence_drop(
            trace, model["iters"]
        ),
        "trace": trace,
        "wall_seconds": 1.0,
    }


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


def test_tracked_text_hash_ignores_checkout_line_endings_only():
    assert pump.sha256_text_bytes(b"one\r\ntwo\r\n") == pump.sha256_text_bytes(
        b"one\ntwo\n"
    )
    assert pump.normalize_text_snapshot(b"one\r\ntwo\r\n") == b"one\ntwo\n"


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

    monkeypatch.setattr(pump, "load_condition", fake_load)
    loaded = pump.load_pump_conditions(Path("outside"), [1], manifest)
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


def test_validation_requires_matching_fixed_sha_review_record(
    tmp_path, monkeypatch
):
    development = {"development_gate": {"passed": True}}
    development_snapshot = b"development"
    plan_hash = "a" * 64
    runner_hash = "b" * 64
    manifest_hash = "d" * 64
    artifact_hash = "e" * 64
    execution_sha = "f" * 40
    git = {"head_sha": "c" * 40, "dirty": False}
    review = {
        "schema_version": 1,
        "review_status": "pass",
        "review_url": "https://example/review",
        "reviewed_git_sha": git["head_sha"],
        "plan_sha256": plan_hash,
        "runner_sha256": runner_hash,
        "source_manifest_sha256": manifest_hash,
        "development_artifact_sha256": artifact_hash,
        "development_artifact_path": pump.DEVELOPMENT_ARTIFACT_RELATIVE.as_posix(),
        "development_execution_sha": execution_sha,
    }
    monkeypatch.setattr(
        pump,
        "validate_development_artifact",
        lambda *_args, **_kwargs: execution_sha,
    )
    assert pump.validate_review_record(
        review,
        development,
        development_snapshot,
        tmp_path / "development.json",
        pump.load_plan(),
        pump.load_manifest(),
        plan_hash,
        runner_hash,
        manifest_hash,
        artifact_hash,
        git,
    ) == review
    review["review_status"] = "pending"
    with pytest.raises(pump.PumpSeriesError, match="passing review"):
        pump.validate_review_record(
            review,
            development,
            development_snapshot,
            tmp_path / "development.json",
            pump.load_plan(),
            pump.load_manifest(),
            plan_hash,
            runner_hash,
            manifest_hash,
            artifact_hash,
            git,
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
    model = pump.model_map(pump.load_plan())["bbdag_r4k4"]
    attempt = _synthetic_attempt(0, model=model)
    checkpoint.write_text(
        json.dumps({**expected, "attempt": attempt}), encoding="utf-8"
    )
    assert pump._load_development_checkpoint(
        checkpoint, expected, model
    ) == attempt
    with pytest.raises(pump.PumpSeriesError, match="runner_sha256"):
        pump._load_development_checkpoint(
            checkpoint,
            {**expected, "runner_sha256": "d" * 64},
            model,
        )


def test_checkpoint_rejects_internal_seed_or_trace_drift(tmp_path):
    plan = pump.load_plan()
    model = pump.model_map(plan)["bbdag_r4k4"]
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
    for name, mutate, message in (
        ("seed", lambda attempt: attempt.update(init_seed=99), "init_seed"),
        ("trace", lambda attempt: attempt["trace"].pop(), "trace iterations"),
        ("drop", lambda attempt: attempt.update(
            final_100_iteration_train_nll_drop=0.5
        ), "convergence drop"),
    ):
        attempt = _synthetic_attempt(0, model=model)
        mutate(attempt)
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps({**expected, "attempt": attempt}), encoding="utf-8"
        )
        with pytest.raises(pump.PumpSeriesError, match=message):
            pump._load_development_checkpoint(path, expected, model)


def _execute_checkpoint_identity(model_id, *, init_seed):
    return {
        "schema_version": 1,
        "checkpoint_kind": "pump-execute-fit",
        "plan_sha256": "a" * 64,
        "runner_sha256": "b" * 64,
        "source_manifest_sha256": "c" * 64,
        "reviewed_git_sha": "d" * 40,
        "development_artifact_sha256": "e" * 64,
        "review_record_sha256": "f" * 64,
        "source_file": "source.mat",
        "source_series": "pump_power",
        "source_condition": {"pump_mw": 3},
        "reshuffle_seed": 0,
        "scale_arm": "stored",
        "phase_arm": "H1",
        "model": model_id,
        "init_seed": init_seed,
    }


def test_execute_bb_checkpoint_roundtrips_state_and_recomputes_train_nll(
    tmp_path,
):
    model = pump.model_map(pump.load_plan())["bbdag_r4k4"]
    state = pump.MixedSqueezedKetState.random_init(
        model["R"], model["K"], model["mode_count"], rng=12
    )
    train = [(0.0, np.array([-0.4, 0.2, 0.7]))]
    eta = 0.8
    train_nll = float(
        pump.nll_lossy_mixed(state, pump.as_bbdag(train), eta)
    )
    attempt = _synthetic_attempt(0, model=model)
    for row in attempt["trace"]:
        row["train_nll"] += train_nll - attempt["train_nll"]
    attempt["trace"][-1]["train_nll"] = train_nll
    attempt["train_nll"] = train_nll
    attempt["fitted_eta"] = eta
    attempt["trace"][-1]["fitted_eta"] = eta
    attempt["final_100_iteration_train_nll_drop"] = pump.convergence_drop(
        attempt["trace"], model["iters"]
    )
    expected = _execute_checkpoint_identity(
        "bbdag_r4k4", init_seed=0
    )
    checkpoint = tmp_path / "bb.json"
    checkpoint.write_text(
        json.dumps({
            **expected,
            "attempt": attempt,
            "state": pump.encode_bb_state(state),
        }),
        encoding="utf-8",
    )

    loaded = pump._load_execute_bb_checkpoint(
        checkpoint, expected, model, train
    )
    np.testing.assert_allclose(loaded["state"].z, state.z)
    assert loaded["attempt"] == attempt

    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload["state"]["alpha"]["real"][0] += 3.0
    checkpoint.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(pump.PumpSeriesError, match="reproduce train NLL"):
        pump._load_execute_bb_checkpoint(checkpoint, expected, model, train)


def test_execute_mle_checkpoint_is_identity_bound_and_physical(tmp_path):
    model = pump.model_map(pump.load_plan())["mle10"]
    expected = _execute_checkpoint_identity("mle10", init_seed=None)
    rho = np.eye(model["n_max"], dtype=complex) / model["n_max"]
    train = [(0.0, np.array([-0.4, 0.2, 0.7]))]
    train_nll = float(np.mean(pump.per_sample_nll_mle(rho, train)))
    checkpoint = tmp_path / "mle.json"
    checkpoint.write_text(
        json.dumps({
            **expected,
            "iterations": 42,
            "train_nll": train_nll,
            "rho": pump.encode_complex_array(rho),
        }),
        encoding="utf-8",
    )

    loaded = pump._load_execute_mle_checkpoint(
        checkpoint, expected, model, train
    )
    np.testing.assert_allclose(loaded["rho"], rho)
    assert loaded["iterations"] == 42
    assert loaded["train_nll"] == pytest.approx(train_nll)

    with pytest.raises(pump.PumpSeriesError, match="review_record_sha256"):
        pump._load_execute_mle_checkpoint(
            checkpoint,
            {**expected, "review_record_sha256": "0" * 64},
            model,
            train,
        )

    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    payload["rho"]["real"][0] = -0.1
    payload["rho"]["real"][1] = 0.2
    checkpoint.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(pump.PumpSeriesError, match="Hermitian"):
        pump._load_execute_mle_checkpoint(checkpoint, expected, model, train)

    payload = json.loads(checkpoint.read_text(encoding="utf-8"))
    vacuum = np.zeros_like(rho)
    vacuum[0, 0] = 1.0
    payload["rho"] = pump.encode_complex_array(vacuum)
    checkpoint.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(pump.PumpSeriesError, match="reproduce train NLL"):
        pump._load_execute_mle_checkpoint(checkpoint, expected, model, train)


def test_execute_cli_requires_checkpoint_directory():
    source = pump.RUNNER_PATH.read_text(encoding="utf-8")
    assert 'execute.add_argument("--checkpoint-dir"' in source
    assert "checkpoint_identity=checkpoint_identity" in source


def test_execute_reuses_every_completed_fit_checkpoint(tmp_path, monkeypatch):
    plan = pump.load_plan()
    plan["development_pump_mw"] = [1]
    plan["validation_pump_mw"] = []
    plan["split"]["reshuffle_seeds"] = [0]
    plan["primary_comparison"]["bootstrap"]["replicates"] = 5
    loaded = pump.LoadedCondition(
        source_file="source.mat",
        series="pump_power",
        condition={"pump_mw": 1},
        data=((0.0, np.arange(5.0)),),
    )
    manifest = {
        "files": [{
            "name": "source.mat",
            "series_assignment": "source-supported",
        }]
    }
    monkeypatch.setattr(
        pump, "load_pump_conditions", lambda *_args: [loaded]
    )
    counts = {"bb": 0, "mle": 0}

    def fake_fit_bbdag(_train, model, *, init_seeds, **_kwargs):
        counts["bb"] += 1
        seed = init_seeds[0]
        state = pump.MixedSqueezedKetState.random_init(
            model["R"], model["K"], model["mode_count"], rng=seed
        )
        attempt = _synthetic_attempt(seed, model=model)
        offset = 1.0 - attempt["train_nll"]
        for row in attempt["trace"]:
            row["train_nll"] += offset
        attempt["trace"][-1]["train_nll"] = 1.0
        attempt["train_nll"] = 1.0
        attempt["final_100_iteration_train_nll_drop"] = pump.convergence_drop(
            attempt["trace"], model["iters"]
        )
        return {
            "state": state,
            "fitted_eta": attempt["fitted_eta"],
            "train_nll": attempt["train_nll"],
            "selected_init_seed": seed,
            "attempts": [attempt],
        }

    def fake_reconstruct_mle(_train, model, **_kwargs):
        counts["mle"] += 1
        return np.eye(model["n_max"], dtype=complex) / model["n_max"], 12

    monkeypatch.setattr(pump, "fit_bbdag", fake_fit_bbdag)
    monkeypatch.setattr(pump, "reconstruct_mle", fake_reconstruct_mle)
    monkeypatch.setattr(pump, "nll_lossy_mixed", lambda *_args: 1.0)
    monkeypatch.setattr(
        pump,
        "per_sample_nll_bb",
        lambda _state, _eta, data: np.full(
            sum(len(samples) for _theta, samples in data), 0.9
        ),
    )
    monkeypatch.setattr(
        pump,
        "per_sample_nll_mle",
        lambda _rho, data: np.full(
            sum(len(samples) for _theta, samples in data), 1.0
        ),
    )
    identity = {
        key: value
        for key, value in _execute_checkpoint_identity(
            "unused", init_seed=None
        ).items()
        if key not in {
            "source_file",
            "source_series",
            "source_condition",
            "reshuffle_seed",
            "scale_arm",
            "phase_arm",
            "model",
            "init_seed",
        }
    }

    _manifest, first = pump.run_execute(
        tmp_path,
        plan,
        manifest,
        checkpoint_dir=tmp_path / "checkpoints",
        checkpoint_identity=identity,
    )
    assert counts == {"bb": 12, "mle": 8}
    assert len(list((tmp_path / "checkpoints").glob("*.json"))) == 20

    _manifest, second = pump.run_execute(
        tmp_path,
        plan,
        manifest,
        checkpoint_dir=tmp_path / "checkpoints",
        checkpoint_identity=identity,
    )
    assert counts == {"bb": 12, "mle": 8}
    assert second == first


def _synthetic_development_artifact():
    plan = pump.load_plan()
    manifest = pump.load_manifest()
    source = next(
        row for row in manifest["files"]
        if row.get("series") == "pump_power"
        and row.get("condition", {}).get("pump_mw") == 1
    )
    model = pump.model_map(plan)["bbdag_r4k4"]
    records = []
    for split_seed in plan["split"]["reshuffle_seeds"]:
        for scale, phase in pump.arm_pairs(plan):
            attempts = []
            for init_seed in model["init_seeds"]:
                attempt = _synthetic_attempt(init_seed, model=model)
                offset = init_seed * 1e-4
                for trace_row in attempt["trace"]:
                    trace_row["train_nll"] += offset
                attempt["train_nll"] = attempt["trace"][-1]["train_nll"]
                attempts.append(attempt)
            selected = min(
                attempts,
                key=lambda row: (row["train_nll"], row["init_seed"]),
            )
            records.append({
                "source_file": source["name"],
                "series": source["series"],
                "condition": source["condition"],
                "reshuffle_seed": split_seed,
                "scale_arm": scale["id"],
                "phase_arm": phase["id"],
                "model": "bbdag_r4k4",
                "selected_init_seed": selected["init_seed"],
                "selected_train_nll": selected["train_nll"],
                "selected_fitted_eta": selected["fitted_eta"],
                "selected_final_100_iteration_train_nll_drop": selected[
                    "final_100_iteration_train_nll_drop"
                ],
                "attempts": attempts,
            })
    execution_sha = "1" * 40
    payload = {
        "schema_version": 1,
        "run_kind": "development",
        "publication_status": "train-only-development",
        "plan_sha256": pump.sha256_path(pump.PLAN_PATH),
        "runner_sha256": pump.sha256_path(pump.RUNNER_PATH),
        "source_manifest_sha256": pump.sha256_path(pump.MANIFEST_PATH),
        "git": {"head_sha": execution_sha, "dirty": False},
        "development_gate": {
            "evaluated": True,
            "passed": True,
            "metric": plan["development_gate"]["metric"],
            "maximum_drop": plan["development_gate"]["maximum_drop"],
            "pass_rule": plan["development_gate"]["pass_rule"],
        },
        "records": records,
    }
    return payload, plan, manifest, execution_sha


def test_development_artifact_is_bound_to_execution_and_reviewed_blobs(
    monkeypatch
):
    payload, plan, manifest, execution_sha = _synthetic_development_artifact()
    snapshot = (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode()
    reviewed_sha = "2" * 40
    tracked = {
        pump.PLAN_PATH.relative_to(pump.ROOT): pump.PLAN_PATH.read_bytes(),
        pump.RUNNER_PATH.relative_to(pump.ROOT): pump.RUNNER_PATH.read_bytes(),
        pump.MANIFEST_PATH.relative_to(pump.ROOT): pump.MANIFEST_PATH.read_bytes(),
        pump.DEVELOPMENT_ARTIFACT_RELATIVE: snapshot,
    }
    monkeypatch.setattr(pump, "require_git_ancestor", lambda *_args: None)
    monkeypatch.setattr(
        pump,
        "git_blob_bytes",
        lambda _revision, relative_path: tracked[relative_path],
    )
    assert pump.validate_development_artifact(
        payload,
        snapshot,
        EXP / "pump_development.json",
        plan,
        manifest,
        plan_sha256=pump.sha256_path(pump.PLAN_PATH),
        runner_sha256=pump.sha256_path(pump.RUNNER_PATH),
        manifest_sha256=pump.sha256_path(pump.MANIFEST_PATH),
        reviewed_git_sha=reviewed_sha,
    ) == execution_sha

    payload["records"][0]["attempts"][0]["init_seed"] = 99
    mutated_snapshot = (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode()
    tracked[pump.DEVELOPMENT_ARTIFACT_RELATIVE] = mutated_snapshot
    with pytest.raises(pump.PumpSeriesError, match="init_seed"):
        pump.validate_development_artifact(
            payload,
            mutated_snapshot,
            EXP / "pump_development.json",
            plan,
            manifest,
            plan_sha256=pump.sha256_path(pump.PLAN_PATH),
            runner_sha256=pump.sha256_path(pump.RUNNER_PATH),
            manifest_sha256=pump.sha256_path(pump.MANIFEST_PATH),
            reviewed_git_sha=reviewed_sha,
        )


def test_committed_development_gate_is_recomputed_from_attempts():
    artifact_path = EXP / "pump_development.json"
    snapshot, artifact, _digest = pump.read_json_snapshot(artifact_path)
    plan = pump.load_plan()
    manifest = pump.load_manifest()
    git = pump.git_identity(require_clean=False)
    assert pump.validate_development_artifact(
        artifact,
        snapshot,
        artifact_path,
        plan,
        manifest,
        plan_sha256=pump.sha256_path(pump.PLAN_PATH),
        runner_sha256=pump.sha256_path(pump.RUNNER_PATH),
        manifest_sha256=pump.sha256_path(pump.MANIFEST_PATH),
        reviewed_git_sha=git["head_sha"],
    ) == artifact["git"]["head_sha"]
