"""Verdict aggregation pins for Round 3(a)."""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "summarize_gate_b.py"
_spec = importlib.util.spec_from_file_location("summarize_gate_b", MODULE_PATH)
summary = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(summary)


def row(seed, block, identity, diagonal, amplitude=-0.01):
    controls = {
        "block_fisher": block,
        "j_norm_h_identity": identity,
        "diagonal_fisher": diagonal,
        "amplitude": amplitude,
    }
    return {
        "fit_seed": seed,
        "status": "complete",
        "heldout_views": 4,
        "probe_count_per_view": 256,
        "gate_b_pass": block >= 0.3,
        "gate_b2_pass": block > max(identity, diagonal, amplitude),
        "correlations": controls,
    }


def test_gate_b_and_b2_are_independent_all_seed_verdicts():
    result = summary.aggregate([
        row(0, 0.334, 0.402, 0.378),
        row(1, 0.332, 0.398, 0.366),
        row(2, 0.335, 0.401, 0.378),
    ])
    assert result["gate_b"]["passed"] is True
    assert result["gate_b2"]["passed"] is False
