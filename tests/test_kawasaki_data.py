"""Contract tests for experiment 32; no public quadrature values are read."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest
from scipy.io import savemat


ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "32_kawasaki_data"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "kawasaki_data_contract", EXP / "kawasaki_data.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


kawasaki = _load_module()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(tmp_path: Path, *, names=("p60deg", "p90deg")):
    source = tmp_path / "quad_test.mat"
    arrays = {
        name: np.array([[index + 0.25, index + 1.25, index + 2.25]])
        for index, name in enumerate(names)
    }
    savemat(source, arrays)
    manifest = {
        "schema_version": 1,
        "source": {},
        "download_contract": {
            "public_download_url_template": "https://example/{file_id}"
        },
        "expected_mat_schema": {
            "variable_name_template": "p{phase_deg}deg",
            "phases_deg": [60, 90],
            "stored_shape": [1, 3],
            "matlab_class": "double",
        },
        "files": [
            {
                "file_id": 1,
                "name": source.name,
                "role": "quadrature",
                "size_bytes": source.stat().st_size,
                "sha256": _sha256(source),
                "series": "synthetic",
                "condition": {
                    "bandwidth_ghz": 1,
                    "pump_mw": 1,
                    "post_psa_loss_db": 0,
                },
            }
        ],
    }
    return source, manifest, arrays


def test_committed_manifest_is_self_consistent():
    manifest = kawasaki.load_manifest()
    entries = manifest["files"]
    quadrature = [row for row in entries if row["role"] == "quadrature"]
    readmes = [row for row in entries if row["role"] == "source_readme"]
    assert len(readmes) == 1
    assert len(quadrature) + len(readmes) == len(entries)
    assert sum(row["size_bytes"] for row in entries) == (
        manifest["source"]["storage_size_bytes"]
    )
    schema = manifest["expected_mat_schema"]
    assert schema["phases_deg"] == sorted(set(schema["phases_deg"]))
    assert {row["series"] for row in quadrature} == set(
        manifest["series_record"]
    )
    assert len({row["file_id"] for row in entries}) == len(entries)
    assert all(len(row["sha256"]) == 64 for row in entries)
    assert all("X-Amz-Signature" not in json.dumps(row) for row in entries)
    assert not list(EXP.glob("*.mat"))


def test_schema_only_does_not_load_quadrature_values(tmp_path, monkeypatch):
    source, manifest, _arrays = _fixture(tmp_path)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("loadmat must not run during schema-only inspection")

    monkeypatch.setattr(kawasaki, "loadmat", forbidden)
    result = kawasaki.inspect_source_file(source, manifest)
    assert [row["name"] for row in result["variables"]] == ["p60deg", "p90deg"]


def test_loader_preserves_stored_phase_and_values(tmp_path):
    source, manifest, arrays = _fixture(tmp_path)
    loaded = kawasaki.load_condition(source, manifest)
    assert loaded.series == "synthetic"
    np.testing.assert_allclose(
        [np.rad2deg(theta) for theta, _samples in loaded.data],
        [60.0, 90.0],
        rtol=0.0,
        atol=1e-12,
    )
    for (_theta, samples), name in zip(loaded.data, ("p60deg", "p90deg")):
        np.testing.assert_array_equal(samples, arrays[name].reshape(-1))


def test_checksum_mismatch_fails_before_mat_inspection(tmp_path, monkeypatch):
    source, manifest, _arrays = _fixture(tmp_path)
    manifest["files"][0]["sha256"] = "0" * 64

    def forbidden(*_args, **_kwargs):
        raise AssertionError("whosmat must not run after a checksum failure")

    monkeypatch.setattr(kawasaki, "whosmat", forbidden)
    with pytest.raises(kawasaki.DataContractError, match="SHA-256"):
        kawasaki.inspect_source_file(source, manifest)


def test_unexpected_phase_variable_is_rejected(tmp_path):
    source, manifest, _arrays = _fixture(tmp_path, names=("p60deg", "p120deg"))
    with pytest.raises(kawasaki.DataContractError, match="MAT variables"):
        kawasaki.inspect_source_file(source, manifest)


def test_mat_variable_storage_order_is_not_semantic(tmp_path):
    source, manifest, _arrays = _fixture(tmp_path, names=("p90deg", "p60deg"))
    result = kawasaki.inspect_source_file(source, manifest)
    assert [row["name"] for row in result["variables"]] == ["p60deg", "p90deg"]


def test_data_directory_inside_repository_is_rejected(tmp_path):
    manifest = {
        "schema_version": 1,
        "source": {},
        "expected_mat_schema": {},
        "files": [],
    }
    with pytest.raises(kawasaki.DataContractError, match="outside the repository"):
        kawasaki.verify_data_dir(ROOT / "experiments", manifest=manifest)
