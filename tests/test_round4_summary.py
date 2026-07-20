"""Verdict aggregation pins for Round 4."""

import importlib.util
import pathlib

import pytest

pytest.importorskip("torch")  # the summarize_* module imports torch at load time

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "summarize_round4.py"
_spec = importlib.util.spec_from_file_location("summarize_round4", MODULE_PATH)
summary = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(summary)


def row(seed, block, ensemble):
    return {
        "fit_seed": seed, "status": "complete", "heldout_views": 4,
        "probe_count_per_view": 256, "view_seed_indices": [4, 5, 6, 7],
        "gate_b_pass": block >= 0.3, "gate_b2_pass": block > ensemble,
        "correlations": {
            "block_fisher": block, "ensemble_sigma": ensemble,
            "block_fisher_damping_1e-4": block - 0.05,
            "block_fisher_damping_1e-8": block + 0.05,
        },
    }


def test_round4_gate_b_passes_while_ensemble_forces_b2_failure():
    result = summary.aggregate([
        row(0, 0.369, 0.575),
        row(1, 0.337, 0.567),
        row(2, 0.376, 0.543),
    ])
    assert result["gate_b"]["passed"] is True
    assert result["gate_b2"]["passed"] is False
    assert result["gate_b2"]["ensemble_ge_block_by_seed"] == [True, True, True]
