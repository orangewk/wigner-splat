"""CPU protocol pins for the Round 4 GPU Gate."""

import importlib.util
import pathlib

import pytest

torch = pytest.importorskip("torch")  # GPU-line dependency; skip cleanly in torch-less envs

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
