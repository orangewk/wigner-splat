"""Fit-free validation tests for the Issue #8 result registry.

Targeted command: python -m pytest tests/test_issue8_results.py
"""

import copy
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RESULT_DIR = ROOT / "experiments" / "08_positivity"
RESULTS_PATH = RESULT_DIR / "issue8_results.json"


def _load_result_io():
    module_path = RESULT_DIR / "result_io.py"
    spec = importlib.util.spec_from_file_location(
        "issue8_result_io",
        module_path,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


result_io = _load_result_io()


def _record(registry, record_id):
    return next(
        record
        for record in registry["records"]
        if record["id"] == record_id
    )


def _series(registry, series_id):
    return next(
        entry
        for entry in registry["figure"]["series"]
        if entry["id"] == series_id
    )


def test_committed_issue8_registry_validates():
    registry = result_io.load_results(RESULTS_PATH)

    assert result_io.validate_results(registry) is registry
    assert registry["schema_version"] == result_io.SCHEMA_VERSION
    assert len(registry["records"]) == 11

    raw_records = [
        record
        for record in registry["records"]
        if record["evidence_level"] == "committed_raw_log"
    ]
    assert {record["data_seed"] for record in raw_records} == {42, 1, 2}
    assert {
        record["provenance"]["source_commit"] for record in raw_records
    } == {"4259cab45f89b84bfc86bece38eeeb56378cd3cc"}

    historical_records = [
        record
        for record in registry["records"]
        if record["evidence_level"] == "historical_report_only"
    ]
    assert historical_records
    assert all(
        record["provenance"]["raw_log_retained"] is False
        and record["provenance"]["fit_parameters_retained"] is False
        for record in historical_records
    )


def test_figure_series_uses_primary_records_and_evidence_marks():
    registry = result_io.load_results(RESULTS_PATH)
    series = result_io.get_figure_series(registry)

    assert [entry["id"] for entry in series] == registry["figure"][
        "figure_order"
    ]
    assert [entry["evidence_mark"] for entry in series] == [
        "",
        "*",
        "*",
        "*",
    ]

    k4 = next(entry for entry in series if entry["id"] == "bbdag_k4")
    assert k4["primary_record_id"] == (
        "bbdag.main.k4.seed42.exact_state_fidelity"
    )
    assert k4["record"]["iters"] == 200
    assert k4["wall_s"] == 527

    robustness = _record(
        registry,
        "bbdag.robustness.k4.seed42.exact_state_fidelity",
    )
    assert robustness["iters"] == 120
    assert robustness["id"] != k4["primary_record_id"]


@pytest.mark.parametrize(
    ("case", "message"),
    [
        ("unknown_schema", "unsupported schema_version"),
        ("missing_required", "missing required field"),
        ("nonfinite", "non-finite"),
        ("missing_null_reason", "missing reason for null field"),
        ("evidence_contradiction", "contradicts provenance.kind"),
        ("duplicate_id", "duplicate record id"),
        ("figure_primary_mismatch", "does not match selector"),
    ],
)
def test_invalid_registries_are_rejected(case, message):
    registry = copy.deepcopy(result_io.load_results(RESULTS_PATH))

    if case == "unknown_schema":
        registry["schema_version"] = 999
    elif case == "missing_required":
        del registry["records"][0]["metric"]
    elif case == "nonfinite":
        registry["records"][0]["value"] = float("nan")
    elif case == "missing_null_reason":
        del registry["records"][0]["reason"]["optimizer_init_seed"]
    elif case == "evidence_contradiction":
        registry["records"][0][
            "evidence_level"
        ] = "historical_report_only"
    elif case == "duplicate_id":
        registry["records"].append(copy.deepcopy(registry["records"][0]))
    elif case == "figure_primary_mismatch":
        _series(registry, "bbdag_k4")["primary_record_id"] = (
            "bbdag.robustness.k4.seed42.exact_state_fidelity"
        )
    else:
        raise AssertionError(f"unhandled test case: {case}")

    with pytest.raises(result_io.ResultRegistryError, match=message):
        result_io.validate_results(registry)
