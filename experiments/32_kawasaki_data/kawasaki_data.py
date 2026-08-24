"""Implementation of issue #180's loader contract (`protocol.md` section 1)."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.io import loadmat, whosmat


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST_PATH = HERE / "source_manifest.json"


class DataContractError(ValueError):
    """A source file or manifest does not satisfy the pinned contract."""


@dataclass(frozen=True)
class LoadedCondition:
    """One source condition plus the common single-mode data contract."""

    source_file: str
    series: str
    condition: dict[str, int]
    data: tuple[tuple[float, np.ndarray], ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        raise DataContractError("Manifest is not an object")
    required = {
        "schema_version",
        "source",
        "expected_mat_schema",
        "convention_status_vocabulary",
        "convention_record",
        "series_assignment_status_vocabulary",
        "series_record_status_vocabulary",
        "series_record",
        "files",
    }
    missing = required.difference(manifest)
    if missing:
        raise DataContractError(f"Manifest missing keys: {sorted(missing)}")
    if manifest["schema_version"] != 1:
        raise DataContractError(
            f"Unsupported manifest schema: {manifest['schema_version']}"
        )
    vocabulary = manifest["convention_status_vocabulary"]
    if (
        not isinstance(vocabulary, list)
        or not vocabulary
        or not all(isinstance(status, str) and status for status in vocabulary)
        or len(vocabulary) != len(set(vocabulary))
    ):
        raise DataContractError("Convention status vocabulary is invalid")
    records = manifest["convention_record"]
    if not isinstance(records, dict):
        raise DataContractError("Convention records are not an object")
    allowed_statuses = set(vocabulary)
    for name, record in records.items():
        if not isinstance(record, dict):
            raise DataContractError(f"Convention record {name!r} is not an object")
        if record.get("status") not in allowed_statuses:
            raise DataContractError(
                f"Convention record {name!r} has uncontrolled status "
                f"{record.get('status')!r}"
            )
    assignment_statuses = manifest["series_assignment_status_vocabulary"]
    record_statuses = manifest["series_record_status_vocabulary"]
    for label, statuses in (
        ("Series assignment", assignment_statuses),
        ("Series record", record_statuses),
    ):
        if (
            not isinstance(statuses, list)
            or not statuses
            or not all(isinstance(status, str) and status for status in statuses)
            or len(statuses) != len(set(statuses))
        ):
            raise DataContractError(f"{label} status vocabulary is invalid")
    series_records = manifest["series_record"]
    if not isinstance(series_records, dict):
        raise DataContractError("Series records are not an object")
    allowed_record_statuses = set(record_statuses)
    allowed_assignment_statuses = set(assignment_statuses)
    for name, record in series_records.items():
        if not isinstance(record, dict):
            raise DataContractError(f"Series record {name!r} is not an object")
        if record.get("status") not in allowed_record_statuses:
            raise DataContractError(
                f"Series record {name!r} has uncontrolled status "
                f"{record.get('status')!r}"
            )
        if not isinstance(record.get("rationale"), str) or not record["rationale"]:
            raise DataContractError(f"Series record {name!r} lacks rationale")
    for entry in manifest["files"]:
        if entry.get("role") != "quadrature":
            continue
        if entry.get("series") not in series_records:
            raise DataContractError(
                f"File {entry.get('name')!r} has unregistered series "
                f"{entry.get('series')!r}"
            )
        if entry.get("series_assignment") not in allowed_assignment_statuses:
            raise DataContractError(
                f"File {entry.get('name')!r} has uncontrolled series assignment "
                f"{entry.get('series_assignment')!r}"
            )
    names = [entry["name"] for entry in manifest["files"]]
    if len(names) != len(set(names)):
        raise DataContractError("Manifest file names are not unique")
    return manifest


def load_manifest(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    return _validate_manifest(manifest)


def file_entries(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {entry["name"]: entry for entry in manifest["files"]}


def expected_variable_names(schema: dict[str, Any]) -> list[str]:
    template = schema["variable_name_template"]
    return [template.format(phase_deg=degree) for degree in schema["phases_deg"]]


def public_download_url(manifest: dict[str, Any], entry: dict[str, Any]) -> str:
    template = manifest["download_contract"]["public_download_url_template"]
    return template.format(file_id=entry["file_id"])


def _verify_bytes(path: Path, entry: dict[str, Any]) -> None:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        pass
    else:
        raise DataContractError(
            f"Source files must be outside the repository: {resolved}"
        )
    if not path.is_file():
        raise FileNotFoundError(path)
    size = path.stat().st_size
    if size != entry["size_bytes"]:
        raise DataContractError(
            f"{path.name}: byte size {size} != {entry['size_bytes']}"
        )
    digest = sha256_file(path)
    if digest != entry["sha256"]:
        raise DataContractError(
            f"{path.name}: SHA-256 {digest} != {entry['sha256']}"
        )


def inspect_source_file(
    path: Path,
    manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Verify bytes and MAT directory information without loading values."""
    manifest = load_manifest() if manifest is None else _validate_manifest(manifest)
    try:
        entry = file_entries(manifest)[path.name]
    except KeyError as exc:
        raise DataContractError(f"Unregistered source file: {path.name}") from exc
    _verify_bytes(path, entry)
    result = {
        "name": path.name,
        "role": entry["role"],
        "size_bytes": entry["size_bytes"],
        "sha256": entry["sha256"],
    }
    if entry["role"] != "quadrature":
        return result

    schema = manifest["expected_mat_schema"]
    expected_names = expected_variable_names(schema)
    directory = whosmat(path)
    actual_names = [name for name, _shape, _kind in directory]
    if (
        len(actual_names) != len(set(actual_names))
        or set(actual_names) != set(expected_names)
    ):
        raise DataContractError(
            f"{path.name}: MAT variables {actual_names} != {expected_names}"
        )
    directory_by_name = {name: (shape, kind) for name, shape, kind in directory}
    expected_shape = tuple(schema["stored_shape"])
    expected_kind = schema["matlab_class"]
    for name in expected_names:
        shape, kind = directory_by_name[name]
        if tuple(shape) != expected_shape or kind != expected_kind:
            raise DataContractError(
                f"{path.name}:{name} has shape/class {shape}/{kind}; "
                f"expected {expected_shape}/{expected_kind}"
            )
    result["variables"] = [
        {
            "name": name,
            "shape": list(directory_by_name[name][0]),
            "matlab_class": directory_by_name[name][1],
        }
        for name in expected_names
    ]
    result["series"] = entry["series"]
    result["condition"] = entry["condition"]
    return result


def load_condition(
    path: Path,
    manifest: dict[str, Any] | None = None,
) -> LoadedCondition:
    """Load one verified MAT file as ``[(theta_rad, samples), ...]``."""
    manifest = load_manifest() if manifest is None else _validate_manifest(manifest)
    inspected = inspect_source_file(path, manifest)
    if inspected["role"] != "quadrature":
        raise DataContractError(f"Not a quadrature MAT file: {path.name}")

    schema = manifest["expected_mat_schema"]
    variable_names = expected_variable_names(schema)
    contents = loadmat(
        path,
        variable_names=variable_names,
        squeeze_me=False,
        verify_compressed_data_integrity=True,
    )
    expected_samples = int(np.prod(schema["stored_shape"]))
    data = []
    for degree, name in zip(schema["phases_deg"], variable_names):
        samples = np.asarray(contents[name], dtype=float).reshape(-1).copy()
        if samples.shape != (expected_samples,):
            raise DataContractError(
                f"{path.name}:{name} loaded shape {samples.shape}"
            )
        if not np.all(np.isfinite(samples)):
            raise DataContractError(f"{path.name}:{name} contains non-finite data")
        data.append((float(np.deg2rad(degree)), samples))

    entry = file_entries(manifest)[path.name]
    return LoadedCondition(
        source_file=path.name,
        series=entry["series"],
        condition=dict(entry["condition"]),
        data=tuple(data),
    )


def verify_data_dir(
    data_dir: Path,
    *,
    load_values: bool = False,
    manifest: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Verify all pinned files; value loading is explicit and statistic-free."""
    manifest = load_manifest() if manifest is None else _validate_manifest(manifest)
    data_dir = data_dir.resolve()
    try:
        data_dir.relative_to(ROOT)
    except ValueError:
        pass
    else:
        raise DataContractError(
            f"Raw data directory must be outside the repository: {data_dir}"
        )

    rows = []
    for entry in manifest["files"]:
        path = data_dir / entry["name"]
        row = inspect_source_file(path, manifest)
        if load_values and entry["role"] == "quadrature":
            loaded = load_condition(path, manifest)
            row["loaded_phase_count"] = len(loaded.data)
            row["loaded_shots_per_phase"] = [len(x) for _theta, x in loaded.data]
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("urls", help="print stable public download URLs from manifest")
    verify = sub.add_parser("verify", help="verify a downloaded source directory")
    verify.add_argument("--data-dir", type=Path, required=True)
    verify.add_argument(
        "--load-values",
        action="store_true",
        help="also load arrays and check finiteness; prints no value statistics",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    if args.command == "urls":
        for entry in manifest["files"]:
            print(f"{entry['name']}\t{public_download_url(manifest, entry)}")
        return
    rows = verify_data_dir(
        args.data_dir,
        load_values=args.load_values,
        manifest=manifest,
    )
    print(json.dumps({"all_valid": True, "files": rows}, indent=2))


if __name__ == "__main__":
    main()
