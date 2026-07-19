"""Load and validate the Issue #8 result registry.

Schema intent:

* Each record is one method/metric/seed observation; runtime and fit settings
  remain contextual fields rather than additional bundled observations.
* Nullable context fields remain present and require a field-specific reason,
  so absence cannot be mistaken for zero or silently omitted metadata.
* Evidence is a tagged union: ``evidence_level`` must agree with the provenance
  kind, and historical reports explicitly state that raw logs and fitted
  parameters are absent.
* Figure order and primary-record selection live in the registry. Evidence
  marks are derived from evidence level rather than independently editable.
"""

import json
import math
import re
from collections.abc import Mapping
from pathlib import Path


SCHEMA_VERSION = 1
DEFAULT_RESULTS_PATH = Path(__file__).with_name("issue8_results.json")
EVIDENCE_MARKS = {
    "committed_raw_log": "",
    "historical_report_only": "*",
}

_RECORD_FIELDS = {
    "id",
    "method",
    "metric",
    "value",
    "data_seed",
    "optimizer_init_seed",
    "K",
    "iters",
    "shots",
    "grid",
    "wall_s",
    "reason",
    "evidence_level",
    "provenance",
}
_NULLABLE_RECORD_FIELDS = {
    "optimizer_init_seed",
    "K",
    "iters",
    "wall_s",
}
_FIGURE_SELECTOR_FIELDS = {
    "method",
    "metric",
    "data_seed",
    "optimizer_init_seed",
    "K",
    "iters",
    "shots",
    "grid",
    "evidence_level",
}
_COMMIT_RE = re.compile(r"[0-9a-f]{40}")


class ResultRegistryError(ValueError):
    """Raised when an Issue #8 result registry violates its schema."""


def _require_mapping(value, where):
    if not isinstance(value, Mapping):
        raise ResultRegistryError(f"{where} must be an object")
    return value


def _require_keys(value, keys, where):
    missing = sorted(keys - set(value))
    if missing:
        joined = ", ".join(missing)
        raise ResultRegistryError(
            f"{where} missing required field(s): {joined}"
        )


def _nonempty_string(value, where):
    if not isinstance(value, str) or not value.strip():
        raise ResultRegistryError(f"{where} must be a non-empty string")


def _finite_number(value, where):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
    ):
        raise ResultRegistryError(f"{where} must be a finite number")


def _positive_int(value, where):
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ResultRegistryError(f"{where} must be a positive integer")


def _nonnegative_int(value, where):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ResultRegistryError(f"{where} must be a non-negative integer")


def _reject_nonfinite_numbers(value, where="$"):
    if isinstance(value, bool):
        return
    if isinstance(value, (int, float)):
        if not math.isfinite(value):
            raise ResultRegistryError(f"{where} contains a non-finite number")
        return
    if isinstance(value, Mapping):
        for key, child in value.items():
            _reject_nonfinite_numbers(child, f"{where}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _reject_nonfinite_numbers(child, f"{where}[{index}]")


def _validate_target(target):
    target = _require_mapping(target, "target")
    _require_keys(
        target,
        {"id", "family", "modes", "alpha", "parity"},
        "target",
    )
    _nonempty_string(target["id"], "target.id")
    _nonempty_string(target["family"], "target.family")
    _positive_int(target["modes"], "target.modes")
    _finite_number(target["alpha"], "target.alpha")
    if target["alpha"] <= 0:
        raise ResultRegistryError("target.alpha must be positive")
    if (
        isinstance(target["parity"], bool)
        or not isinstance(target["parity"], int)
        or target["parity"] not in (-1, 1)
    ):
        raise ResultRegistryError("target.parity must be -1 or 1")
    return target


def _validate_data(data, target):
    data = _require_mapping(data, "data")
    _require_keys(
        data,
        {"id", "generator", "grid", "shots", "seeds"},
        "data",
    )
    _nonempty_string(data["id"], "data.id")
    _nonempty_string(data["generator"], "data.generator")
    _positive_int(data["shots"], "data.shots")

    seeds = data["seeds"]
    if not isinstance(seeds, list) or not seeds:
        raise ResultRegistryError("data.seeds must be a non-empty list")
    for index, seed in enumerate(seeds):
        _nonnegative_int(seed, f"data.seeds[{index}]")
    if len(seeds) != len(set(seeds)):
        raise ResultRegistryError("data.seeds contains duplicate seeds")

    grid = _require_mapping(data["grid"], "data.grid")
    _require_keys(
        grid,
        {
            "id",
            "kind",
            "modes",
            "angles_per_mode",
            "points",
            "interval",
            "endpoint",
        },
        "data.grid",
    )
    _nonempty_string(grid["id"], "data.grid.id")
    _nonempty_string(grid["kind"], "data.grid.kind")
    _positive_int(grid["modes"], "data.grid.modes")
    _positive_int(grid["angles_per_mode"], "data.grid.angles_per_mode")
    _positive_int(grid["points"], "data.grid.points")
    _nonempty_string(grid["interval"], "data.grid.interval")
    if not isinstance(grid["endpoint"], bool):
        raise ResultRegistryError("data.grid.endpoint must be a boolean")
    if grid["modes"] != target["modes"]:
        raise ResultRegistryError(
            "data.grid.modes must match target.modes"
        )
    expected_points = grid["angles_per_mode"] ** grid["modes"]
    if grid["points"] != expected_points:
        raise ResultRegistryError(
            "data.grid.points must equal angles_per_mode ** modes"
        )
    return data


def _validate_provenance(record, where):
    provenance = _require_mapping(record["provenance"], f"{where}.provenance")
    _require_keys(
        provenance,
        {
            "kind",
            "raw_log_retained",
            "fit_parameters_retained",
            "absence_note",
        },
        f"{where}.provenance",
    )

    evidence_level = record["evidence_level"]
    _nonempty_string(provenance["kind"], f"{where}.provenance.kind")
    if provenance["kind"] != evidence_level:
        raise ResultRegistryError(
            f"{where}.evidence_level contradicts provenance.kind"
        )
    if not isinstance(provenance["raw_log_retained"], bool):
        raise ResultRegistryError(
            f"{where}.provenance.raw_log_retained must be a boolean"
        )
    if not isinstance(provenance["fit_parameters_retained"], bool):
        raise ResultRegistryError(
            f"{where}.provenance.fit_parameters_retained must be a boolean"
        )
    _nonempty_string(
        provenance["absence_note"],
        f"{where}.provenance.absence_note",
    )

    if evidence_level == "committed_raw_log":
        _require_keys(
            provenance,
            {"source_commit", "artifact_path", "locator"},
            f"{where}.provenance",
        )
        if provenance["raw_log_retained"] is not True:
            raise ResultRegistryError(
                f"{where} committed_raw_log evidence requires "
                "raw_log_retained=true"
            )
        _nonempty_string(
            provenance["source_commit"],
            f"{where}.provenance.source_commit",
        )
        if not _COMMIT_RE.fullmatch(provenance["source_commit"]):
            raise ResultRegistryError(
                f"{where}.provenance.source_commit must be a full commit hash"
            )
        _nonempty_string(
            provenance["artifact_path"],
            f"{where}.provenance.artifact_path",
        )
        _nonempty_string(
            provenance["locator"],
            f"{where}.provenance.locator",
        )
        return

    if evidence_level == "historical_report_only":
        _require_keys(
            provenance,
            {"reported_in"},
            f"{where}.provenance",
        )
        if (
            provenance["raw_log_retained"] is not False
            or provenance["fit_parameters_retained"] is not False
        ):
            raise ResultRegistryError(
                f"{where} historical_report_only evidence requires "
                "raw_log_retained=false and fit_parameters_retained=false"
            )
        reported_in = provenance["reported_in"]
        if not isinstance(reported_in, list) or not reported_in:
            raise ResultRegistryError(
                f"{where}.provenance.reported_in must be a non-empty list"
            )
        for index, source in enumerate(reported_in):
            _nonempty_string(
                source,
                f"{where}.provenance.reported_in[{index}]",
            )
        if len(reported_in) != len(set(reported_in)):
            raise ResultRegistryError(
                f"{where}.provenance.reported_in contains duplicates"
            )


def _validate_record(record, data, seen_ids, index):
    where = f"records[{index}]"
    record = _require_mapping(record, where)
    _require_keys(record, _RECORD_FIELDS, where)

    for field in ("id", "method", "metric", "grid"):
        _nonempty_string(record[field], f"{where}.{field}")
    if record["id"] in seen_ids:
        raise ResultRegistryError(f"duplicate record id: {record['id']}")
    seen_ids.add(record["id"])

    _finite_number(record["value"], f"{where}.value")
    _nonnegative_int(record["data_seed"], f"{where}.data_seed")
    if record["data_seed"] not in data["seeds"]:
        raise ResultRegistryError(
            f"{where}.data_seed is not declared in data.seeds"
        )

    if record["optimizer_init_seed"] is not None:
        _nonnegative_int(
            record["optimizer_init_seed"],
            f"{where}.optimizer_init_seed",
        )
    if record["K"] is not None:
        _positive_int(record["K"], f"{where}.K")
    if record["iters"] is not None:
        _positive_int(record["iters"], f"{where}.iters")
    _positive_int(record["shots"], f"{where}.shots")
    if record["shots"] != data["shots"]:
        raise ResultRegistryError(f"{where}.shots must match data.shots")
    if record["grid"] != data["grid"]["id"]:
        raise ResultRegistryError(f"{where}.grid must match data.grid.id")
    if record["wall_s"] is not None:
        _finite_number(record["wall_s"], f"{where}.wall_s")
        if record["wall_s"] < 0:
            raise ResultRegistryError(
                f"{where}.wall_s must be non-negative"
            )

    reasons = _require_mapping(record["reason"], f"{where}.reason")
    unknown_reason_fields = set(reasons) - _NULLABLE_RECORD_FIELDS
    if unknown_reason_fields:
        names = ", ".join(sorted(unknown_reason_fields))
        raise ResultRegistryError(
            f"{where}.reason names non-nullable or unknown field(s): {names}"
        )
    for field in _NULLABLE_RECORD_FIELDS:
        if record[field] is None:
            if field not in reasons:
                raise ResultRegistryError(
                    f"{where} missing reason for null field: {field}"
                )
            _nonempty_string(reasons[field], f"{where}.reason.{field}")
        elif field in reasons:
            raise ResultRegistryError(
                f"{where}.reason.{field} is present but {field} is non-null"
            )

    _nonempty_string(record["evidence_level"], f"{where}.evidence_level")
    if record["evidence_level"] not in EVIDENCE_MARKS:
        raise ResultRegistryError(
            f"{where}.evidence_level is unsupported: "
            f"{record['evidence_level']}"
        )
    _validate_provenance(record, where)
    return record


def _validate_figure(figure, records_by_id):
    figure = _require_mapping(figure, "figure")
    _require_keys(
        figure,
        {"figure_order", "figure_order_reason", "series"},
        "figure",
    )
    _nonempty_string(
        figure["figure_order_reason"],
        "figure.figure_order_reason",
    )

    order = figure["figure_order"]
    if not isinstance(order, list) or not order:
        raise ResultRegistryError(
            "figure.figure_order must be a non-empty list"
        )
    for index, series_id in enumerate(order):
        _nonempty_string(series_id, f"figure.figure_order[{index}]")
    if len(order) != len(set(order)):
        raise ResultRegistryError("figure.figure_order contains duplicates")

    series = figure["series"]
    if not isinstance(series, list) or not series:
        raise ResultRegistryError("figure.series must be a non-empty list")

    series_by_id = {}
    primary_record_ids = set()
    for index, entry in enumerate(series):
        where = f"figure.series[{index}]"
        entry = _require_mapping(entry, where)
        _require_keys(
            entry,
            {
                "id",
                "label",
                "physical",
                "selector",
                "primary_record_id",
                "primary_selection_reason",
            },
            where,
        )
        _nonempty_string(entry["id"], f"{where}.id")
        _nonempty_string(entry["label"], f"{where}.label")
        _nonempty_string(
            entry["primary_record_id"],
            f"{where}.primary_record_id",
        )
        _nonempty_string(
            entry["primary_selection_reason"],
            f"{where}.primary_selection_reason",
        )
        if not isinstance(entry["physical"], bool):
            raise ResultRegistryError(f"{where}.physical must be a boolean")
        if entry["id"] in series_by_id:
            raise ResultRegistryError(
                f"duplicate figure series id: {entry['id']}"
            )
        series_by_id[entry["id"]] = entry

        primary_id = entry["primary_record_id"]
        if primary_id in primary_record_ids:
            raise ResultRegistryError(
                f"duplicate figure primary_record_id: {primary_id}"
            )
        primary_record_ids.add(primary_id)
        if primary_id not in records_by_id:
            raise ResultRegistryError(
                f"{where}.primary_record_id does not reference a record"
            )

        selector = _require_mapping(entry["selector"], f"{where}.selector")
        _require_keys(
            selector,
            {"method", "metric", "data_seed"},
            f"{where}.selector",
        )
        unknown_selector_fields = set(selector) - _FIGURE_SELECTOR_FIELDS
        if unknown_selector_fields:
            names = ", ".join(sorted(unknown_selector_fields))
            raise ResultRegistryError(
                f"{where}.selector contains unsupported field(s): {names}"
            )
        primary = records_by_id[primary_id]
        for field, expected in selector.items():
            if primary[field] != expected:
                raise ResultRegistryError(
                    f"{where}.primary_record_id does not match selector "
                    f"field {field}"
                )

    if set(order) != set(series_by_id):
        raise ResultRegistryError(
            "figure.figure_order must contain every figure series id exactly once"
        )
    return figure


def validate_results(registry):
    """Validate and return an Issue #8 result registry."""

    registry = _require_mapping(registry, "registry")
    _reject_nonfinite_numbers(registry)
    _require_keys(
        registry,
        {"schema_version", "target", "data", "figure", "records"},
        "registry",
    )
    if (
        isinstance(registry["schema_version"], bool)
        or not isinstance(registry["schema_version"], int)
        or registry["schema_version"] != SCHEMA_VERSION
    ):
        raise ResultRegistryError(
            f"unsupported schema_version: {registry['schema_version']!r}"
        )

    target = _validate_target(registry["target"])
    data = _validate_data(registry["data"], target)

    records = registry["records"]
    if not isinstance(records, list) or not records:
        raise ResultRegistryError("records must be a non-empty list")
    seen_ids = set()
    records_by_id = {}
    for index, record in enumerate(records):
        validated = _validate_record(record, data, seen_ids, index)
        records_by_id[validated["id"]] = validated

    _validate_figure(registry["figure"], records_by_id)
    return registry


def load_results(path=None):
    """Load and validate the committed registry or a supplied JSON path."""

    result_path = DEFAULT_RESULTS_PATH if path is None else Path(path)
    with result_path.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)
    return validate_results(registry)


def get_figure_series(registry):
    """Return ordered figure entries enriched with primary observations."""

    registry = validate_results(registry)
    records_by_id = {
        record["id"]: record for record in registry["records"]
    }
    series_by_id = {
        entry["id"]: entry for entry in registry["figure"]["series"]
    }

    ordered = []
    for series_id in registry["figure"]["figure_order"]:
        entry = series_by_id[series_id]
        record = records_by_id[entry["primary_record_id"]]
        enriched = dict(entry)
        enriched.update(
            {
                "value": record["value"],
                "wall_s": record["wall_s"],
                "method": record["method"],
                "metric": record["metric"],
                "evidence_level": record["evidence_level"],
                "evidence_mark": EVIDENCE_MARKS[
                    record["evidence_level"]
                ],
                "record": dict(record),
            }
        )
        ordered.append(enriched)
    return ordered
