"""Compact loader and validator for the Issue #8 result registry."""

import json
import math
import re
from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_RESULTS_PATH = Path(__file__).with_name("issue8_results.json")
EVIDENCE_MARKS = {"committed_raw_log": "", "historical_report_only": "*"}
RECORD_FIELDS = {
    "id", "method", "metric", "value", "data_seed", "optimizer_init_seed",
    "K", "iters", "shots", "grid", "wall_s", "reason",
    "evidence_level", "provenance",
}
NULLABLE_FIELDS = {"optimizer_init_seed", "K", "iters", "wall_s"}
COMMIT_RE = re.compile(r"[0-9a-f]{40}")


class ResultRegistryError(ValueError):
    """Raised when the Issue #8 registry violates its schema."""


def _require(obj, fields, where):
    if not isinstance(obj, dict):
        raise ResultRegistryError(f"{where} must be an object")
    missing = sorted(fields - set(obj))
    if missing:
        raise ResultRegistryError(
            f"{where} missing required field(s): {', '.join(missing)}"
        )


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def _validate_provenance(record, where):
    provenance = record["provenance"]
    _require(
        provenance,
        {"kind", "raw_log_retained", "fit_parameters_retained", "absence_note"},
        f"{where}.provenance",
    )
    evidence = record["evidence_level"]
    if provenance["kind"] != evidence:
        raise ResultRegistryError(
            f"{where}.evidence_level contradicts provenance.kind"
        )
    if (
        type(provenance["raw_log_retained"]) is not bool
        or type(provenance["fit_parameters_retained"]) is not bool
    ):
        raise ResultRegistryError(f"{where} retained flags must be booleans")
    if not _text(provenance["absence_note"]):
        raise ResultRegistryError(f"{where}.absence_note must be non-empty")
    if evidence == "committed_raw_log":
        _require(
            provenance, {"source_commit", "artifact_path", "locator"},
            f"{where}.provenance",
        )
        if provenance["raw_log_retained"] is not True:
            raise ResultRegistryError(
                f"{where} committed log requires raw_log_retained=true"
            )
        commit = provenance["source_commit"]
        if not isinstance(commit, str) or not COMMIT_RE.fullmatch(commit):
            raise ResultRegistryError(f"{where}.source_commit must be a full SHA")
        if not _text(provenance["artifact_path"]) or not _text(
            provenance["locator"]
        ):
            raise ResultRegistryError(f"{where} log path/locator must be non-empty")
    elif evidence == "historical_report_only":
        _require(provenance, {"reported_in"}, f"{where}.provenance")
        if (
            provenance["raw_log_retained"] is not False
            or provenance["fit_parameters_retained"] is not False
        ):
            raise ResultRegistryError(
                f"{where} historical retained flags must be false"
            )
        sources = provenance["reported_in"]
        if (
            not isinstance(sources, list) or not sources
            or any(not _text(source) for source in sources)
        ):
            raise ResultRegistryError(f"{where}.reported_in must be non-empty")
    else:
        raise ResultRegistryError(f"{where}.evidence_level is unsupported")


def validate_results(registry):
    """Validate and return an Issue #8 registry."""
    _require(
        registry, {"schema_version", "target", "data", "figure", "records"},
        "registry",
    )
    if (
        type(registry["schema_version"]) is not int
        or registry["schema_version"] != SCHEMA_VERSION
    ):
        raise ResultRegistryError(
            f"unsupported schema_version: {registry['schema_version']!r}"
        )
    records = registry["records"]
    if not isinstance(records, list) or not records:
        raise ResultRegistryError("records must be a non-empty list")
    records_by_id = {}
    for index, record in enumerate(records):
        where = f"records[{index}]"
        _require(record, RECORD_FIELDS, where)
        if not all(_text(record[field]) for field in ("id", "method", "metric")):
            raise ResultRegistryError(f"{where} identity fields must be non-empty")
        if record["id"] in records_by_id:
            raise ResultRegistryError(f"duplicate record id: {record['id']}")
        if not _finite(record["value"]):
            raise ResultRegistryError(f"{where}.value must be finite")
        if record["wall_s"] is not None and not _finite(record["wall_s"]):
            raise ResultRegistryError(f"{where}.wall_s must be finite or null")
        reasons = record["reason"]
        if not isinstance(reasons, dict):
            raise ResultRegistryError(f"{where}.reason must be an object")
        for field in NULLABLE_FIELDS:
            if record[field] is None and not _text(reasons.get(field)):
                raise ResultRegistryError(
                    f"{where} missing reason for null field: {field}"
                )
        if record["evidence_level"] not in EVIDENCE_MARKS:
            raise ResultRegistryError(f"{where}.evidence_level is unsupported")
        _validate_provenance(record, where)
        records_by_id[record["id"]] = record

    figure = registry["figure"]
    _require(
        figure, {"figure_order", "figure_order_reason", "series"}, "figure"
    )
    order = figure["figure_order"]
    if (
        not isinstance(order, list) or not order
        or any(not _text(series_id) for series_id in order)
        or len(order) != len(set(order))
    ):
        raise ResultRegistryError("figure_order must contain unique series ids")
    if not _text(figure["figure_order_reason"]):
        raise ResultRegistryError("figure_order_reason must be non-empty")
    series_by_id = {}
    if not isinstance(figure["series"], list) or not figure["series"]:
        raise ResultRegistryError("figure.series must be a non-empty list")
    for index, series in enumerate(figure["series"]):
        where = f"figure.series[{index}]"
        _require(
            series,
            {
                "id", "label", "wall_label", "physical", "selector",
                "primary_record_id",
                "primary_selection_reason",
            },
            where,
        )
        if not _text(series["id"]) or series["id"] in series_by_id:
            raise ResultRegistryError(f"{where}.id must be unique and non-empty")
        if (
            not _text(series["label"])
            or not _text(series["wall_label"])
            or not _text(series["primary_selection_reason"])
        ):
            raise ResultRegistryError(f"{where} text fields must be non-empty")
        if type(series["physical"]) is not bool:
            raise ResultRegistryError(f"{where}.physical must be a boolean")
        primary = records_by_id.get(series["primary_record_id"])
        if primary is None:
            raise ResultRegistryError(
                f"{where}.primary_record_id does not reference a record"
            )
        selector = series["selector"]
        if not isinstance(selector, dict) or not selector:
            raise ResultRegistryError(f"{where}.selector must be non-empty")
        if any(primary.get(field) != expected for field, expected in selector.items()):
            raise ResultRegistryError(
                f"{where}.primary_record_id does not match selector"
            )
        series_by_id[series["id"]] = series
    if set(order) != set(series_by_id):
        raise ResultRegistryError(
            "figure_order must contain every figure series id exactly once"
        )
    return registry


def load_results(path=None):
    """Load and validate the committed registry or a supplied JSON path."""
    result_path = DEFAULT_RESULTS_PATH if path is None else Path(path)
    with result_path.open("r", encoding="utf-8") as handle:
        return validate_results(json.load(handle))


def get_figure_series(registry):
    """Return ordered figure entries enriched with primary observations."""
    registry = validate_results(registry)
    records = {record["id"]: record for record in registry["records"]}
    series = {item["id"]: item for item in registry["figure"]["series"]}
    ordered = []
    for series_id in registry["figure"]["figure_order"]:
        item = dict(series[series_id])
        record = records[item["primary_record_id"]]
        item.update(
            value=record["value"], wall_s=record["wall_s"],
            evidence_level=record["evidence_level"],
            evidence_mark=EVIDENCE_MARKS[record["evidence_level"]],
            record=dict(record),
        )
        ordered.append(item)
    return ordered
