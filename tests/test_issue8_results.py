"""Fit-free tests for the compact Issue #8 registry validator."""

import copy
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "experiments" / "08_positivity"
RESULTS_PATH = RESULT_DIR / "issue8_results.json"


def _load_result_io():
    spec = importlib.util.spec_from_file_location(
        "issue8_result_io", RESULT_DIR / "result_io.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


result_io = _load_result_io()


def _record(registry, record_id):
    return next(
        record for record in registry["records"] if record["id"] == record_id
    )


def _series(registry, series_id):
    return next(
        series for series in registry["figure"]["series"]
        if series["id"] == series_id
    )


def test_committed_registry_validates():
    registry = result_io.load_results(RESULTS_PATH)
    assert result_io.validate_results(registry) is registry
    raw = [
        record for record in registry["records"]
        if record["evidence_level"] == "committed_raw_log"
    ]
    assert {record["data_seed"] for record in raw} == {42, 1, 2}
    assert {
        record["provenance"]["source_commit"] for record in raw
    } == {
        "4259cab45f89b84bfc86bece38eeeb56378cd3cc",  # exp06 signed-splat log
        "1e49e00a24cb1302de69f2577a064a701878a32e",  # bbdag analytic clean run
    }
    for record in raw:
        provenance = record["provenance"]
        artifact = ROOT / provenance["artifact_path"]
        assert artifact.is_file()
        assert provenance["locator"] in artifact.read_text(encoding="utf-8")


def test_figure_primary_and_evidence_marks():
    registry = result_io.load_results(RESULTS_PATH)
    figure = result_io.get_figure_series(registry)
    assert [item["id"] for item in figure] == registry["figure"]["figure_order"]
    assert [item["wall_label"] for item in figure] == [
        "splat", "proj", "K=4", "K=8",
    ]
    assert [item["evidence_mark"] for item in figure] == ["", "*", "", ""]

    primary = next(item for item in figure if item["id"] == "bbdag_k4")
    assert primary["primary_record_id"] == (
        "bbdag.analytic.k4.seed42.exact_state_fidelity"
    )
    assert primary["record"]["iters"] == 200
    assert primary["record"]["gradient"] == "analytic"
    assert primary["wall_s"] < 60  # issue #25: analytic gradient, not FD's 527 s

    historical = _record(registry, "bbdag.main.k4.seed42.exact_state_fidelity")
    assert historical["evidence_level"] == "historical_report_only"
    assert historical["value"] == primary["value"]  # FD fidelity reproduced

    robustness = _record(
        registry, "bbdag.robustness.k4.seed42.exact_state_fidelity"
    )
    assert robustness["iters"] == 120
    assert robustness["id"] != primary["primary_record_id"]


def test_analytic_fit_parameters_recompute_reported_fidelity():
    """The committed portable evidence (issue #25) is durable: the fitted
    parameters recompute the registry's fidelity without any bundle files."""
    import json

    import numpy as np

    from wigner_splat.bbdagM import CoherentKetState, fidelity_vs_cat3

    registry = result_io.load_results(RESULTS_PATH)
    evidence = json.loads(
        (ROOT / "experiments/08_positivity/evidence/bbdag_analytic_fits.json")
        .read_text(encoding="utf-8")
    )
    runs = {(r["data_seed"], r["K"]): r for r in evidence["runs"]}
    assert set(runs) == {(42, 4), (1, 4), (2, 4), (42, 8)}

    checked = 0
    for record in registry["records"]:
        if not record["id"].startswith("bbdag.analytic."):
            continue
        provenance = record["provenance"]
        assert provenance["fit_parameters_retained"] is True
        assert (ROOT / provenance["fit_parameters_path"]).is_file()
        run = runs[(record["data_seed"], record["K"])]
        assert run["source_commit"] == provenance["source_commit"]
        state = CoherentKetState(
            z=np.array(run["z_re"]) + 1j * np.array(run["z_im"]),
            alpha=np.array(run["alpha_re"]) + 1j * np.array(run["alpha_im"]),
        )
        F = fidelity_vs_cat3(state, 1.5, +1)
        assert abs(F - record["value"]) < 5e-5
        assert abs(F - run["exact_state_fidelity"]) < 1e-9
        checked += 1
    assert checked == 4


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("schema", "unsupported schema_version"),
        ("value", "value must be finite"),
        ("wall", "wall_s must be finite"),
        ("null_reason", "missing reason for null field"),
        ("evidence", "committed log requires"),
        ("duplicate", "duplicate record id"),
        ("selector", "does not match selector"),
    ],
)
def test_invalid_registry_is_rejected(case, message):
    registry = copy.deepcopy(result_io.load_results(RESULTS_PATH))
    if case == "schema":
        registry["schema_version"] = 2
    elif case == "value":
        registry["records"][0]["value"] = float("nan")
    elif case == "wall":
        registry["records"][0]["wall_s"] = float("inf")
    elif case == "null_reason":
        del registry["records"][0]["reason"]["optimizer_init_seed"]
    elif case == "evidence":
        registry["records"][0]["provenance"]["raw_log_retained"] = False
    elif case == "duplicate":
        registry["records"].append(copy.deepcopy(registry["records"][0]))
    elif case == "selector":
        _series(registry, "bbdag_k4")["primary_record_id"] = (
            "bbdag.robustness.k4.seed42.exact_state_fidelity"
        )
    with pytest.raises(result_io.ResultRegistryError, match=message):
        result_io.validate_results(registry)
