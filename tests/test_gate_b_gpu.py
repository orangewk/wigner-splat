"""CPU protocol checks for the restartable GPU Gate B/B2 runner."""

import importlib.util
import pathlib

import numpy as np
import pytest
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "run_gate_b.py"
_spec = importlib.util.spec_from_file_location("run_gate_b", MODULE_PATH)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)


def test_score_view_seeds_are_pinned_and_independent():
    assert [gate.score_seed(index) for index in range(4)] == [
        1314162, 2314165, 3314168, 4314171
    ]


def test_block_damping_is_mean_diagonal_times_declared_fraction():
    blocks = torch.diag_embed(torch.tensor([[1.0, 2, 3, 4, 5, 6]]))
    assert gate.block_damping(blocks) == pytest.approx(3.5e-6)


def test_central_difference_pins_max_parameter_displacement():
    theta = torch.tensor([[2.0, -1.0]])
    direction = torch.tensor([[4.0, -2.0]])
    render = lambda value: value.square()
    actual = gate.finite_difference_jvp(render, theta, direction)
    assert torch.allclose(actual, 2 * theta * direction, atol=1e-3)


def test_spearman_uses_average_tie_ranks():
    expected = np.array([0.0, 1.0, 1.0, 3.0])
    ranks = gate.rankdata(expected, method="average")
    ranks -= ranks.mean()
    assert gate.spearman_from_ranks(expected, ranks) == pytest.approx(1.0)

def test_psd_inverse_sqrt_clamps_only_negative_eigenvalues():
    blocks = torch.tensor([
        [[1.0, 0.0], [0.0, -1e-4]],
        [[4.0, 0.0], [0.0, 9.0]],
    ])
    vectors, inverse_sqrt, metrics = gate.psd_inverse_sqrt(
        blocks, damping=0.01, chunk_size=1
    )
    direction = gate.apply_inverse_sqrt(vectors, inverse_sqrt, torch.ones((2, 2)))
    assert metrics["negative_eigenvalue_count"] == 1
    assert metrics["minimum_eigenvalue"] < 0
    assert torch.allclose(
        direction[1],
        torch.tensor([1 / 4.01**0.5, 1 / 9.01**0.5]),
        atol=1e-6,
    )
