"""Fit-free round-trip tests for fresh BB-dagger evidence bundles."""

import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "08_positivity" / "bbdag_bundle.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("issue8_bbdag_bundle", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bundle_io = _load_module()


def _inputs():
    data = [
        (np.array([0.0, 0.2]), np.arange(6, dtype=float).reshape(3, 2)),
        (np.array([0.4, 0.6]), np.arange(6, 12, dtype=float).reshape(3, 2)),
    ]
    state = SimpleNamespace(
        z=np.array([1.0 + 0.2j, -0.3j]),
        alpha=np.array([[0.5, -0.2j], [-0.5, 0.2j]]),
    )
    trace = [(25, 3.2), (40, 3.05)]
    metadata = {
        "entrypoint": "experiments/08_positivity/bbdag_3mode.py",
        "data_seed": 42,
        "optimizer_init_seed": 0,
        "K": 2,
        "iters": 40,
        "result": {"exact_state_fidelity": 0.9, "final_nll": 3.05},
        "source": {"commit": "a" * 40, "dirty": False},
    }
    return data, state, trace, metadata


def test_bundle_round_trip(tmp_path):
    data, state, trace, metadata = _inputs()
    target = tmp_path / "run"
    written = bundle_io.write_bbdag_bundle(
        target, data=data, state=state, trace=trace, metadata=metadata
    )

    manifest = json.loads((written / "metadata.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == bundle_io.SCHEMA_VERSION
    assert manifest["metadata"] == metadata
    arrays_path = written / manifest["arrays"]["path"]
    assert hashlib.sha256(arrays_path.read_bytes()).hexdigest() == (
        manifest["arrays"]["sha256"]
    )

    with np.load(arrays_path, allow_pickle=False) as arrays:
        np.testing.assert_allclose(arrays["theta"], np.stack([item[0] for item in data]))
        np.testing.assert_allclose(arrays["samples"], np.stack([item[1] for item in data]))
        np.testing.assert_allclose(arrays["trace"], trace)
        np.testing.assert_allclose(arrays["z"], state.z)
        np.testing.assert_allclose(arrays["alpha"], state.alpha)


def test_bundle_refuses_to_overwrite(tmp_path):
    data, state, trace, metadata = _inputs()
    target = tmp_path / "run"
    bundle_io.write_bbdag_bundle(
        target, data=data, state=state, trace=trace, metadata=metadata
    )

    with pytest.raises(FileExistsError):
        bundle_io.write_bbdag_bundle(
            target, data=data, state=state, trace=trace, metadata=metadata
        )
