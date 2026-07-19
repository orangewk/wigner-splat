"""Exact-vs-block Fisher feasibility spike on fused gsplat.

The held-out split is deliberately outside this module.  The scene is fully
synthetic and tiny: two fixed cameras, two Gaussians, and only the PUP-common
parameter block ``[mean(3), scale(3)]``.  Colors, rotations, and opacities are
fixed so the comparison tests one approximation at a time.
"""
from __future__ import annotations

import argparse
import json

import subprocess

from pathlib import Path
from typing import Callable

import torch

UPSTREAM_COMMIT = "77ab983ffe43420b2131669cb35776b883ca4c3c"
EXPERIMENT_DIR = Path(__file__).resolve().parent


def verify_upstream(source: Path) -> None:
    actual = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if actual != UPSTREAM_COMMIT:
        raise RuntimeError(
            f"gsplat commit mismatch: expected {UPSTREAM_COMMIT}, got {actual}"
        )



def make_scene(device: torch.device) -> dict[str, torch.Tensor | int]:
    dtype = torch.float32
    width, height = 8, 6
    means = torch.tensor(
        [[-0.22, -0.08, 3.0], [0.28, 0.12, 3.35]], device=device, dtype=dtype
    )
    log_scales = torch.log(
        torch.tensor(
            [[0.34, 0.26, 0.30], [0.29, 0.38, 0.32]],
            device=device,
            dtype=dtype,
        )
    )
    quats = torch.tensor(
        [[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]],
        device=device,
        dtype=dtype,
    )
    opacities = torch.tensor([0.82, 0.73], device=device, dtype=dtype)
    colors = torch.tensor(
        [[0.85, 0.20, 0.12], [0.08, 0.42, 0.92]], device=device, dtype=dtype
    )
    viewmats = torch.eye(4, device=device, dtype=dtype).repeat(2, 1, 1)
    # World-to-camera translations for camera centres x=-0.35 and x=+0.35.
    viewmats[:, 0, 3] = torch.tensor([0.35, -0.35], device=device, dtype=dtype)
    Ks = torch.tensor(
        [[[9.0, 0.0, 3.5], [0.0, 9.0, 2.5], [0.0, 0.0, 1.0]]],
        device=device,
        dtype=dtype,
    ).repeat(2, 1, 1)
    theta_log = torch.cat([means, log_scales], dim=1)
    return {
        "theta_log": theta_log,
        "quats": quats,
        "opacities": opacities,
        "colors": colors,
        "viewmats": viewmats,
        "Ks": Ks,
        "width": width,
        "height": height,
    }


def renderer(
    scene: dict[str, torch.Tensor | int], parameterization: str
) -> Callable[[torch.Tensor], torch.Tensor]:
    from gsplat.rendering import rasterization

    def render(theta: torch.Tensor) -> torch.Tensor:
        means = theta[:, :3]
        raw_scales = theta[:, 3:]
        scales = raw_scales.exp() if parameterization == "log_scale" else raw_scales
        image, _, _ = rasterization(
            means=means,
            quats=scene["quats"],
            scales=scales,
            opacities=scene["opacities"],
            colors=scene["colors"],
            viewmats=scene["viewmats"],
            Ks=scene["Ks"],
            width=scene["width"],
            height=scene["height"],
            packed=True,
            render_mode="RGB",
        )
        return image.reshape(-1)

    return render


def exact_jacobian(
    render: Callable[[torch.Tensor], torch.Tensor], theta: torch.Tensor
) -> torch.Tensor:
    """Materialize dRGB/dtheta using PyTorch's exact reverse-mode Jacobian."""
    jac = torch.autograd.functional.jacobian(
        render, theta, create_graph=False, vectorize=False
    )
    return jac.reshape(jac.shape[0], -1)


def diagonal_blocks(full_fisher: torch.Tensor, n_splats: int) -> torch.Tensor:
    return torch.stack(
        [full_fisher[6 * i : 6 * (i + 1), 6 * i : 6 * (i + 1)] for i in range(n_splats)]
    )


def pup_block_fisher(
    render: Callable[[torch.Tensor], torch.Tensor],
    theta: torch.Tensor,
    chunk_size: int,
) -> torch.Tensor:
    """PUP-style per-output VJP accumulation, without a custom CUDA kernel.

    Each scalar RGB output is kept separate.  Unlike patch-summed PUP, this
    contains no within-patch cross terms, so it should equal the diagonal
    per-Gaussian blocks of the exact Gauss-Newton matrix.
    """
    theta_var = theta.detach().clone().requires_grad_(True)
    outputs = render(theta_var)
    blocks = torch.zeros(
        (theta.shape[0], 6, 6), device=theta.device, dtype=theta.dtype
    )
    for start in range(0, outputs.numel(), chunk_size):
        stop = min(start + chunk_size, outputs.numel())
        for output_index in range(start, stop):
            grad = torch.autograd.grad(
                outputs[output_index], theta_var, retain_graph=True
            )[0]
            blocks += torch.einsum("ni,nj->nij", grad, grad)
    return blocks


def density_and_jacobian(
    points: torch.Tensor, theta_log: torch.Tensor, opacities: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Anisotropic, axis-aligned 3D density and its per-splat pushforward."""

    def density(theta: torch.Tensor) -> torch.Tensor:
        means = theta[:, :3]
        scales = theta[:, 3:].exp()
        delta = points[:, None, :] - means[None, :, :]
        exponent = -0.5 * ((delta / scales[None, :, :]) ** 2).sum(dim=2)
        return (exponent.exp() * opacities[None, :]).sum(dim=1)

    values = density(theta_log)
    jac = torch.autograd.functional.jacobian(density, theta_log)
    return values, jac.reshape(points.shape[0], -1)


def score_map(
    blocks: torch.Tensor,
    density_jacobian: torch.Tensor,
    damping: float,
    damping_metric: torch.Tensor | None = None,
) -> torch.Tensor:
    n_points = density_jacobian.shape[0]
    n_splats = blocks.shape[0]
    jr = density_jacobian.reshape(n_points, n_splats, 6)
    if damping_metric is None:
        damping_metric = torch.eye(6, device=blocks.device, dtype=blocks.dtype).repeat(
            n_splats, 1, 1
        )
    solved = torch.linalg.solve(
        blocks + damping * damping_metric, jr.permute(1, 2, 0)
    )
    variance = torch.einsum("pni,nip->pn", jr, solved).sum(dim=1)
    return variance.clamp_min(0).sqrt()


def relative_error(actual: torch.Tensor, expected: torch.Tensor) -> float:
    scale = expected.abs().max().clamp_min(torch.finfo(expected.dtype).eps)
    return float((actual - expected).abs().max() / scale)


def run(source: Path, chunk_sizes: list[int]) -> dict[str, object]:
    verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Phase 4 requires CUDA gsplat")
    device = torch.device("cuda")
    torch.manual_seed(0)
    scene = make_scene(device)
    theta_log = scene["theta_log"]
    assert isinstance(theta_log, torch.Tensor)
    render_log = renderer(scene, "log_scale")

    jac_log = exact_jacobian(render_log, theta_log)
    full_log = jac_log.T @ jac_log
    exact_blocks = diagonal_blocks(full_log, theta_log.shape[0])
    candidate_errors: dict[str, float] = {}

    for chunk_size in chunk_sizes:
        candidate = pup_block_fisher(render_log, theta_log, chunk_size)

        candidate_errors[str(chunk_size)] = relative_error(candidate, exact_blocks)

    # A fixed z-plane is the tiny-scene analogue of the later per-pixel surface map.
    ys, xs = torch.meshgrid(
        torch.linspace(-0.45, 0.45, 6, device=device),
        torch.linspace(-0.60, 0.60, 8, device=device),
        indexing="ij",
    )
    points = torch.stack([xs.reshape(-1), ys.reshape(-1), torch.full_like(xs.reshape(-1), 3.15)], dim=1)
    density, jr_log = density_and_jacobian(points, theta_log, scene["opacities"])
    damping_scale = float(torch.trace(full_log) / full_log.shape[0])
    damping_fractions = [1e-4, 1e-6, 1e-8, 1e-10]
    damping_scores = {
        str(fraction): score_map(exact_blocks, jr_log, damping_scale * fraction)
        for fraction in damping_fractions
    }
    damping = damping_scale * 1e-6
    block_score = score_map(exact_blocks, jr_log, damping)

    diag = torch.diagonal(exact_blocks, dim1=1, dim2=2)
    jr_blocked = jr_log.reshape(points.shape[0], theta_log.shape[0], 6)
    diagonal_score = (
        (jr_blocked.square() / (diag[None, :, :] + damping)).sum(dim=(1, 2))
    ).clamp_min(0).sqrt()
    gradient_norm = torch.linalg.vector_norm(jr_log, dim=1)

    # Independently differentiate in activated-scale coordinates.
    theta_scale = torch.cat([theta_log[:, :3], theta_log[:, 3:].exp()], dim=1)
    render_scale = renderer(scene, "scale")
    jac_scale = exact_jacobian(render_scale, theta_scale)
    exact_scale_blocks = diagonal_blocks(jac_scale.T @ jac_scale, theta_log.shape[0])
    transform = torch.eye(6, device=device).repeat(theta_log.shape[0], 1, 1)
    transform[:, 3:, 3:] = torch.diag_embed(1.0 / theta_scale[:, 3:])
    transformed_blocks = transform.transpose(1, 2) @ exact_blocks @ transform
    jr_scale = torch.einsum("pni,nij->pnj", jr_blocked, transform)
    damping_metric_scale = transform.transpose(1, 2) @ transform
    scale_score = score_map(
        exact_scale_blocks,
        jr_scale.reshape(points.shape[0], -1),
        damping,
        damping_metric_scale,
    )

    max_candidate_error = max(candidate_errors.values())
    parameterization_fisher_error = relative_error(exact_scale_blocks, transformed_blocks)
    parameterization_score_error = relative_error(scale_score, block_score)
    damping_convergence_error = relative_error(
        damping_scores["1e-10"], damping_scores["1e-08"]
    )
    passed = (
        max_candidate_error < 2e-5
        and parameterization_fisher_error < 2e-5
        and parameterization_score_error < 2e-5
        and damping_convergence_error < 1e-3
    )
    return {
        "phase": 4,
        "status": "pass" if passed else "stop",
        "heldout_accessed": False,
        "gsplat_commit": UPSTREAM_COMMIT,
        "device": torch.cuda.get_device_name(0),
        "scene": {
            "splats": theta_log.shape[0],
            "views": 2,
            "width": scene["width"],
            "height": scene["height"],
            "parameter_block": ["mean_x", "mean_y", "mean_z", "log_scale_x", "log_scale_y", "log_scale_z"],
            "fixed_parameters": ["quaternion", "opacity", "RGB color"],
        },
        "exact_vs_candidate_relative_error_by_chunk": candidate_errors,
        "parameterization_fisher_relative_error": parameterization_fisher_error,
        "parameterization_score_relative_error": parameterization_score_error,
        "damping": {
            "rule": "1e-6 * trace(full_GN) / parameter_count",
            "value_log_coordinates": damping,
            "scale_coordinate_metric": "A^T A, A=d(log-scale params)/d(scale params)",
            "sweep": {
                str(fraction): {
                    "min_max": [
                        float(damping_scores[str(fraction)].min()),
                        float(damping_scores[str(fraction)].max()),
                    ]
                }
                for fraction in damping_fractions
            },
            "smallest_pair_relative_change": damping_convergence_error,
        },
        "map_summary": {
            "shape": [6, 8],
            "density_min_max": [float(density.min()), float(density.max())],
            "block_score_min_max": [float(block_score.min()), float(block_score.max())],
            "gradient_norm_min_max": [float(gradient_norm.min()), float(gradient_norm.max())],
            "diagonal_score_min_max": [float(diagonal_score.min()), float(diagonal_score.max())],
        },
        "maps": {
            "density_amplitude": density.reshape(6, 8).detach().cpu().tolist(),
            "block_fisher_score": block_score.reshape(6, 8).detach().cpu().tolist(),
            "density_gradient_norm": gradient_norm.reshape(6, 8).detach().cpu().tolist(),
            "diagonal_fisher_score": diagonal_score.reshape(6, 8).detach().cpu().tolist(),
        },
        "acceptance": {
            "relative_error_tolerance": 2e-5,
            "all_chunk_sizes_match_exact": max_candidate_error < 2e-5,
            "coordinate_aware_parameterization_invariant": parameterization_score_error < 2e-5,
            "damping_1e-8_to_1e-10_converged": damping_convergence_error < 1e-3,
        },
        "claim_scope": (
            "Feasibility only: scalar-output VJP accumulation on a tiny fused-gsplat "
            "scene equals exact per-splat mean+scale GN blocks. This does not validate "
            "patch-summed PUP, a custom CUDA Fisher kernel, or held-out ranking."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument("--chunk-sizes", type=int, nargs="+", default=[1, 7, 64])
    parser.add_argument(
        "--output", type=Path, default=EXPERIMENT_DIR / "phase4_fisher_result.json"
    )
    args = parser.parse_args()
    if any(size < 1 for size in args.chunk_sizes):
        parser.error("chunk sizes must be positive")
    result = run(args.gsplat_source, args.chunk_sizes)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "pass":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
