"""CPU protocol pins for the Round 4 GPU Gate."""

import importlib.util
import json
import pathlib

import pytest
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "run_round4_gate.py"
_spec = importlib.util.spec_from_file_location("run_round4_gate", MODULE_PATH)
round4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(round4)
round3 = round4._load_round3_gate()


def test_fresh_view_seeds_continue_round3_sequence():
    assert [round4.score_seed(round3, index) for index in range(4)] == [
        5314174, 6314177, 7314180, 8314183,
    ]


def test_damping_grid_and_primary_are_hard_locked():
    blocks = torch.diag_embed(torch.tensor([[1.0, 2, 3, 4, 5, 6]]))
    values = round4.damping_values(round3, blocks)
    assert values == pytest.approx({
        "1e-04": 3.5e-4, "1e-06": 3.5e-6, "1e-08": 3.5e-8,
    })
    assert round4.PRIMARY_DAMPING_FRACTION == 1e-6


def test_shared_ensemble_guard_accepts_exact_artifact(tmp_path):
    names = ["view-a.png", "view-b.png"]
    hashes = {}
    for index, name in enumerate(names):
        path = tmp_path / f"view_{index}.pt"
        torch.save({
            "view_index": index,
            "view_name": name,
            "fit_seeds": [0, 1, 2],
            "ddof": 1,
            "sigma_ensemble": torch.tensor([index], dtype=torch.float32),
        }, path)
        hashes[name] = round4.sha256(path)
    (tmp_path / "result.json").write_text(json.dumps({
        "status": "complete",
        "heldout_names": names,
        "fit_seeds": [0, 1, 2],
        "ddof": 1,
        "shared_single_map_across_fit_seed_comparisons": True,
        "map_sha256": hashes,
    }), encoding="utf-8")

    record = round4.validate_shared_ensemble(tmp_path, names)

    assert record["map_sha256"] == hashes


def test_shared_ensemble_guard_rejects_wrong_view_or_bytes(tmp_path):
    name = "view-a.png"
    path = tmp_path / "view_0.pt"
    torch.save({
        "view_index": 0, "view_name": name, "fit_seeds": [0, 1, 2],
        "ddof": 1, "sigma_ensemble": torch.ones(1),
    }, path)
    (tmp_path / "result.json").write_text(json.dumps({
        "status": "complete", "heldout_names": [name],
        "fit_seeds": [0, 1, 2], "ddof": 1,
        "shared_single_map_across_fit_seed_comparisons": True,
        "map_sha256": {name: round4.sha256(path)},
    }), encoding="utf-8")
    with pytest.raises(RuntimeError, match="heldout_names"):
        round4.validate_shared_ensemble(tmp_path, ["other.png"])

    with path.open("ab") as stream:
        stream.write(b"tampered")
    with pytest.raises(RuntimeError, match="hash mismatch"):
        round4.validate_shared_ensemble(tmp_path, [name])
