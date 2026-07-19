"""Regression tests for the issue #48 Phase 4 Fisher feasibility spike."""
import importlib.util
import pathlib

import pytest

torch = pytest.importorskip("torch")  # GPU-line dependency; skip cleanly in torch-less envs

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "phase4_fisher_spike.py"
_spec = importlib.util.spec_from_file_location("phase4_fisher_spike", MODULE_PATH)
phase4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(phase4)


def test_diagonal_blocks_extract_per_splat_fisher():
    jacobian = torch.arange(60, dtype=torch.float64).reshape(5, 12)
    fisher = jacobian.T @ jacobian
    blocks = phase4.diagonal_blocks(fisher, n_splats=2)
    assert torch.equal(blocks[0], fisher[:6, :6])
    assert torch.equal(blocks[1], fisher[6:, 6:])


def test_coordinate_aware_damping_preserves_score():
    torch.manual_seed(7)
    factors = torch.randn(2, 6, 6, dtype=torch.float64)
    blocks_log = factors.transpose(1, 2) @ factors + 0.2 * torch.eye(6)
    jr_log = torch.randn(9, 2, 6, dtype=torch.float64)
    scales = torch.tensor(
        [[0.3, 0.5, 0.8], [0.4, 0.7, 1.1]], dtype=torch.float64
    )
    transform = torch.eye(6, dtype=torch.float64).repeat(2, 1, 1)
    transform[:, 3:, 3:] = torch.diag_embed(1.0 / scales)
    blocks_scale = transform.transpose(1, 2) @ blocks_log @ transform
    jr_scale = torch.einsum("pni,nij->pnj", jr_log, transform)
    metric_scale = transform.transpose(1, 2) @ transform

    score_log = phase4.score_map(blocks_log, jr_log.reshape(9, -1), 1e-4)
    score_scale = phase4.score_map(
        blocks_scale, jr_scale.reshape(9, -1), 1e-4, metric_scale
    )
    assert torch.allclose(score_log, score_scale, rtol=1e-11, atol=1e-11)


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA gsplat required")
def test_fused_gsplat_candidate_matches_exact_blocks():
    source = pathlib.Path(r"C:\tmp\gsplat-77ab983-windows")
    if not source.is_dir():
        pytest.skip("Pinned gsplat source is not installed")
    result = phase4.run(source, chunk_sizes=[1, 7, 64])
    assert result["status"] == "pass"
    assert result["heldout_accessed"] is False
    assert result["acceptance"]["all_chunk_sizes_match_exact"] is True
    assert result["acceptance"]["coordinate_aware_parameterization_invariant"] is True
    assert result["acceptance"]["damping_1e-8_to_1e-10_converged"] is True
    assert set(result["maps"]) == {
        "density_amplitude",
        "block_fisher_score",
        "density_gradient_norm",
        "diagonal_fisher_score",
    }
