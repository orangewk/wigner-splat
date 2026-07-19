"""Pre-declared randomized matrix-free Fisher gate for issue #48.

This module never accesses experiment data.  It reuses Phase 4's synthetic
fused-gsplat scene and exact Jacobian, then tests the production estimators:
Rademacher VJPs for per-splat Fisher blocks and finite-difference JVPs for the
diagonal of the block-GN predictive covariance.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Callable

import torch

EXPERIMENT_DIR = Path(__file__).resolve().parent
PHASE4_PATH = EXPERIMENT_DIR / "phase4_fisher_spike.py"
FISHER_COUNTS = (32, 128, 512)
SCORE_COUNTS = (16, 64, 256)
ESTIMATOR_SEEDS = (314159, 271828, 161803)
DAMPING_FRACTION = 1e-6
MAX_PARAMETER_DISPLACEMENT = 1e-3


def _load_phase4():
    spec = importlib.util.spec_from_file_location("phase4_fisher_spike", PHASE4_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rademacher(
    shape: tuple[int, ...], generator: torch.Generator, device: torch.device
) -> torch.Tensor:
    signs = torch.randint(0, 2, shape, generator=generator, dtype=torch.int8)
    return signs.to(device=device, dtype=torch.float32).mul_(2).sub_(1)


def randomized_fisher_blocks(
    render: Callable[[torch.Tensor], torch.Tensor],
    theta: torch.Tensor,
    counts: tuple[int, ...],
    seed: int,
) -> dict[int, torch.Tensor]:
    """Estimate each diagonal 6x6 block of J^T J with nested VJP probes."""
    if tuple(sorted(counts)) != counts or counts[0] < 1:
        raise ValueError("counts must be positive and increasing")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    theta_var = theta.detach().clone().requires_grad_(True)
    outputs = render(theta_var)
    accumulated = torch.zeros(
        (theta.shape[0], 6, 6), device=theta.device, dtype=theta.dtype
    )
    snapshots: dict[int, torch.Tensor] = {}
    for probe_index in range(1, counts[-1] + 1):
        signs = rademacher((outputs.numel(),), generator, theta.device)
        gradient = torch.autograd.grad(
            outputs,
            theta_var,
            grad_outputs=signs,
            retain_graph=probe_index < counts[-1],
        )[0]
        accumulated += torch.einsum("ni,nj->nij", gradient, gradient)
        if probe_index in counts:
            snapshots[probe_index] = accumulated.detach().clone() / probe_index
    return snapshots


def block_damping(blocks: torch.Tensor) -> float:
    return float(torch.diagonal(blocks, dim1=1, dim2=2).sum() / blocks.numel() * 6) * DAMPING_FRACTION


def predictive_score_from_jacobian(
    jacobian: torch.Tensor,
    blocks: torch.Tensor,
    damping: float,
    image_shape: tuple[int, int, int, int],
) -> torch.Tensor:
    """Exact RGB-L2 predictive sigma under a block-diagonal precision."""
    output_count, parameter_count = jacobian.shape
    n_splats = blocks.shape[0]
    assert parameter_count == n_splats * 6
    jac_blocks = jacobian.reshape(output_count, n_splats, 6)
    eye = torch.eye(6, device=blocks.device, dtype=blocks.dtype)
    solved = torch.linalg.solve(
        blocks + damping * eye,
        jac_blocks.permute(1, 2, 0),
    )
    variance = torch.einsum("oni,nio->o", jac_blocks, solved).clamp_min(0)
    return variance.reshape(image_shape).sum(dim=-1).sqrt()


def finite_difference_jvp(
    render: Callable[[torch.Tensor], torch.Tensor],
    theta: torch.Tensor,
    direction: torch.Tensor,
) -> torch.Tensor:
    max_abs = float(direction.abs().max())
    if not max_abs > 0:
        raise ValueError("direction must be nonzero")
    step = MAX_PARAMETER_DISPLACEMENT / max_abs
    with torch.no_grad():
        plus = render(theta + step * direction)
        minus = render(theta - step * direction)
    return (plus - minus) / (2.0 * step)


def randomized_predictive_scores(
    render: Callable[[torch.Tensor], torch.Tensor],
    theta: torch.Tensor,
    blocks: torch.Tensor,
    counts: tuple[int, ...],
    seed: int,
    image_shape: tuple[int, int, int, int],
    exact_jacobian: torch.Tensor,
) -> tuple[dict[int, torch.Tensor], list[float]]:
    """Estimate diag(J B^-1 J^T) using parameter-space Rademacher probes."""
    if tuple(sorted(counts)) != counts or counts[0] < 1:
        raise ValueError("counts must be positive and increasing")
    generator = torch.Generator(device="cpu").manual_seed(seed + 1_000_003)
    damping = block_damping(blocks)
    eye = torch.eye(6, device=blocks.device, dtype=blocks.dtype)
    cholesky = torch.linalg.cholesky(blocks + damping * eye)
    accumulated = torch.zeros(exact_jacobian.shape[0], device=theta.device)
    snapshots: dict[int, torch.Tensor] = {}
    jvp_errors: list[float] = []
    for probe_index in range(1, counts[-1] + 1):
        signs = rademacher(tuple(theta.shape), generator, theta.device)
        direction = torch.linalg.solve_triangular(
            cholesky.transpose(1, 2), signs.unsqueeze(-1), upper=True
        ).squeeze(-1)
        fd_jvp = finite_difference_jvp(render, theta, direction)
        if probe_index <= 8:
            exact_jvp = exact_jacobian @ direction.reshape(-1)
            denominator = torch.linalg.vector_norm(exact_jvp).clamp_min(
                torch.finfo(exact_jvp.dtype).eps
            )
            jvp_errors.append(
                float(torch.linalg.vector_norm(fd_jvp - exact_jvp) / denominator)
            )
        accumulated += fd_jvp.square()
        if probe_index in counts:
            variance = (accumulated / probe_index).reshape(image_shape).sum(dim=-1)
            snapshots[probe_index] = variance.clamp_min(0).sqrt()
    return snapshots, jvp_errors


def relative_frobenius(actual: torch.Tensor, expected: torch.Tensor) -> float:
    return float(
        torch.linalg.vector_norm(actual - expected)
        / torch.linalg.vector_norm(expected).clamp_min(torch.finfo(expected.dtype).eps)
    )


def normalized_rmse(actual: torch.Tensor, expected: torch.Tensor) -> float:
    numerator = torch.mean((actual - expected).square()).sqrt()
    denominator = torch.mean(expected.square()).sqrt().clamp_min(
        torch.finfo(expected.dtype).eps
    )
    return float(numerator / denominator)


def spearman(actual: torch.Tensor, expected: torch.Tensor) -> float:
    actual_rank = torch.argsort(torch.argsort(actual.reshape(-1))).float()
    expected_rank = torch.argsort(torch.argsort(expected.reshape(-1))).float()
    actual_rank -= actual_rank.mean()
    expected_rank -= expected_rank.mean()
    denominator = torch.linalg.vector_norm(actual_rank) * torch.linalg.vector_norm(
        expected_rank
    )
    return float(torch.dot(actual_rank, expected_rank) / denominator)


def run(source: Path) -> dict[str, object]:
    phase4 = _load_phase4()
    phase4.verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Phase 4b requires CUDA gsplat")
    device = torch.device("cuda")
    scene = phase4.make_scene(device)
    theta = scene["theta_log"]
    assert isinstance(theta, torch.Tensor)
    render = phase4.renderer(scene, "log_scale")
    jacobian = phase4.exact_jacobian(render, theta)
    exact_blocks = phase4.diagonal_blocks(jacobian.T @ jacobian, theta.shape[0])
    image_shape = (2, int(scene["height"]), int(scene["width"]), 3)
    exact_score = predictive_score_from_jacobian(
        jacobian, exact_blocks, block_damping(exact_blocks), image_shape
    )

    rows: list[dict[str, object]] = []
    for seed in ESTIMATOR_SEEDS:
        fisher_snapshots = randomized_fisher_blocks(
            render, theta, FISHER_COUNTS, seed
        )
        fisher_errors = {
            str(count): relative_frobenius(blocks, exact_blocks)
            for count, blocks in fisher_snapshots.items()
        }
        final_blocks = fisher_snapshots[FISHER_COUNTS[-1]]
        score_snapshots, jvp_errors = randomized_predictive_scores(
            render,
            theta,
            final_blocks,
            SCORE_COUNTS,
            seed,
            image_shape,
            jacobian,
        )
        score_metrics = {
            str(count): {
                "spearman": spearman(score, exact_score),
                "normalized_rmse": normalized_rmse(score, exact_score),
            }
            for count, score in score_snapshots.items()
        }
        rows.append(
            {
                "seed": seed,
                "fisher_relative_frobenius": fisher_errors,
                "score": score_metrics,
                "max_first_8_jvp_normalized_l2": max(jvp_errors),
            }
        )

    final_fisher_ok = all(
        row["fisher_relative_frobenius"][str(FISHER_COUNTS[-1])] <= 0.10
        for row in rows
    )
    final_score_ok = all(
        row["score"][str(SCORE_COUNTS[-1])]["spearman"] >= 0.95
        and row["score"][str(SCORE_COUNTS[-1])]["normalized_rmse"] <= 0.20
        for row in rows
    )
    jvp_ok = all(row["max_first_8_jvp_normalized_l2"] <= 0.01 for row in rows)
    initial_nrmse = sorted(
        row["score"][str(SCORE_COUNTS[0])]["normalized_rmse"] for row in rows
    )[1]
    final_nrmse = sorted(
        row["score"][str(SCORE_COUNTS[-1])]["normalized_rmse"] for row in rows
    )[1]
    convergence_ratio = final_nrmse / initial_nrmse
    convergence_ok = convergence_ratio <= 0.60
    passed = final_fisher_ok and final_score_ok and jvp_ok and convergence_ok
    return {
        "phase": "4b_randomized_matrix_free_fisher",
        "status": "pass" if passed else "stop",
        "heldout_accessed": False,
        "declaration": {
            "issue_comment": 5011474178,
            "metric_clarification_comment": 5011480536,
            "fisher_probe_counts": list(FISHER_COUNTS),
            "score_probe_counts": list(SCORE_COUNTS),
            "estimator_seeds": list(ESTIMATOR_SEEDS),
            "production_estimator_seed": ESTIMATOR_SEEDS[0],
            "max_parameter_displacement": MAX_PARAMETER_DISPLACEMENT,
            "damping_fraction": DAMPING_FRACTION,
        },
        "rows": rows,
        "convergence": {
            "median_initial_score_nrmse": initial_nrmse,
            "median_final_score_nrmse": final_nrmse,
            "final_over_initial": convergence_ratio,
        },
        "acceptance": {
            "all_512_probe_fisher_errors_le_0.10": final_fisher_ok,
            "all_256_probe_score_spearman_ge_0.95_and_nrmse_le_0.20": final_score_ok,
            "all_first_8_jvp_max_errors_le_0.01": jvp_ok,
            "median_score_nrmse_final_over_initial_le_0.60": convergence_ok,
        },
        "claim_scope": (
            "Tiny fused-gsplat validation only. Passing authorizes the declared "
            "512-VJP Fisher and 256 finite-difference-JVP score estimators; it does "
            "not establish Gate B/B2 on held-out real video."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EXPERIMENT_DIR / "phase4b_randomized_fisher_result.json",
    )
    args = parser.parse_args()
    result = run(args.gsplat_source)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "pass":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
