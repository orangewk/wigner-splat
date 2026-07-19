"""Regression tests for the pre-declared Phase 4b randomized Fisher gate."""
import importlib.util
import pathlib

import pytest

torch = pytest.importorskip("torch")  # GPU-line dependency; skip cleanly in torch-less envs

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "20_real_video_gpu"
    / "phase4b_randomized_fisher.py"
)
_spec = importlib.util.spec_from_file_location("phase4b_randomized_fisher", MODULE_PATH)
phase4b = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase4b)


def test_rademacher_is_seeded_and_binary():
    generator_a = torch.Generator().manual_seed(314159)
    generator_b = torch.Generator().manual_seed(314159)
    first = phase4b.rademacher((128,), generator_a, torch.device("cpu"))
    second = phase4b.rademacher((128,), generator_b, torch.device("cpu"))
    assert torch.equal(first, second)
    assert set(first.tolist()) == {-1.0, 1.0}


def test_predictive_score_matches_dense_block_inverse():
    torch.manual_seed(3)
    jacobian = torch.randn(12, 12, dtype=torch.float64)
    factors = torch.randn(2, 6, 6, dtype=torch.float64)
    blocks = factors.transpose(1, 2) @ factors + 0.5 * torch.eye(
        6, dtype=torch.float64
    )
    damping = 1e-4
    actual = phase4b.predictive_score_from_jacobian(
        jacobian, blocks, damping, (1, 2, 2, 3)
    )
    precision = torch.block_diag(*(block + damping * torch.eye(6) for block in blocks))
    covariance = jacobian @ torch.linalg.inv(precision) @ jacobian.T
    expected = torch.diagonal(covariance).reshape(1, 2, 2, 3).sum(dim=-1).sqrt()
    assert torch.allclose(actual, expected, rtol=1e-11, atol=1e-11)


def test_finite_difference_jvp_matches_polynomial_direction():
    theta = torch.tensor([[0.4, -0.2, 0.7]], dtype=torch.float64)
    direction = torch.tensor([[0.3, -0.5, 0.2]], dtype=torch.float64)

    def render(value):
        return torch.cat([value.square().reshape(-1), value.prod().reshape(1)])

    actual = phase4b.finite_difference_jvp(render, theta, direction)
    exact = torch.autograd.functional.jvp(render, theta, direction)[1]
    assert torch.allclose(actual, exact, rtol=1e-5, atol=1e-7)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA gsplat required")
def test_declared_randomized_tiny_gate_passes():
    source = pathlib.Path(r"C:\tmp\gsplat-77ab983-windows")
    if not source.is_dir():
        pytest.skip("Pinned gsplat source is not installed")
    result = phase4b.run(source)
    assert result["status"] == "pass"
    assert result["heldout_accessed"] is False
    assert all(result["acceptance"].values())
