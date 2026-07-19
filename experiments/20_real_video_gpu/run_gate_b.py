"""Run the preregistered full-resolution held-out Gate B/B2 maps.

Each invocation handles one fixed fit seed.  The three covariance scores share
the same Rademacher signs and central-difference renderer.  Progress is saved
every 16 probes and after every held-out view.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Callable

import imageio.v2 as imageio
import numpy as np
import torch
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
BUILDER_PATH = HERE / "build_production_fisher.py"
REGISTRATION = HERE / "out" / "heldout_registration_v2"
PROBE_COUNT = 256
SMOKE_PROBE_COUNT = 2
CHECKPOINT_EVERY = 16
ESTIMATOR_SEED = 314159
VIEW_SEED_STRIDE = 1_000_003
DAMPING_FRACTION = 1e-6
MAX_PARAMETER_DISPLACEMENT = 1e-3
GATE_RHO = 0.3
HELDOUT_NAMES = (
    "frame_04_src_0060.png",
    "frame_10_src_0105.png",
    "frame_16_src_0150.png",
    "frame_22_src_0195.png",
)


def _load_builder():
    spec = importlib.util.spec_from_file_location("production_fisher", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def score_seed(view_index: int) -> int:
    return ESTIMATOR_SEED + VIEW_SEED_STRIDE * (view_index + 1)


def block_damping(blocks: torch.Tensor) -> float:
    mean_diagonal = torch.diagonal(blocks, dim1=1, dim2=2).mean()
    return float(mean_diagonal) * DAMPING_FRACTION


def psd_inverse_sqrt(
    blocks: torch.Tensor, damping: float, chunk_size: int = 50_000
) -> tuple[torch.Tensor, torch.Tensor, dict[str, float | int]]:
    eigenvectors = []
    inverse_sqrt = []
    negative_count = 0
    minimum = 0.0
    correction_sq = 0.0
    norm_sq = 0.0
    for chunk in blocks.split(chunk_size):
        values_cpu, vectors_cpu = torch.linalg.eigh(chunk.double().cpu())
        negative = values_cpu < 0
        negative_count += int(negative.sum())
        minimum = min(minimum, float(values_cpu.min()))
        correction_sq += float(values_cpu.clamp_max(0).square().sum())
        norm_sq += float(values_cpu.square().sum())
        clamped = values_cpu.clamp_min(0).add(damping).rsqrt().float()
        eigenvectors.append(vectors_cpu.float().to(blocks.device))
        inverse_sqrt.append(clamped.to(blocks.device))
    metrics = {
        "negative_eigenvalue_count": negative_count,
        "minimum_eigenvalue": minimum,
        "relative_frobenius_psd_correction": (correction_sq / norm_sq) ** 0.5,
    }
    return torch.cat(eigenvectors), torch.cat(inverse_sqrt), metrics


def apply_inverse_sqrt(
    eigenvectors: torch.Tensor, inverse_sqrt: torch.Tensor, signs: torch.Tensor
) -> torch.Tensor:
    rotated = torch.bmm(
        eigenvectors.transpose(1, 2), signs.unsqueeze(-1)
    ).squeeze(-1)
    rotated.mul_(inverse_sqrt)
    return torch.bmm(eigenvectors, rotated.unsqueeze(-1)).squeeze(-1)


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


def spearman_from_ranks(actual: np.ndarray, expected_rank: np.ndarray) -> float:
    actual_rank = rankdata(actual.reshape(-1), method="average")
    actual_rank -= actual_rank.mean()
    denominator = np.linalg.norm(actual_rank) * np.linalg.norm(expected_rank)
    if denominator == 0:
        raise RuntimeError("Spearman input has zero rank variance")
    return float(np.dot(actual_rank, expected_rank) / denominator)


def load_heldout_views(examples: Path) -> list[dict[str, torch.Tensor | str]]:
    sys.path.insert(0, str(examples))
    import cv2
    import pycolmap
    from datasets.colmap import Parser, _image_w2c
    from datasets.normalize import transform_cameras

    train_dataset = HERE / "out" / "seed0_fixed_4000" / "train_dataset"
    train_parser = Parser(
        data_dir=str(train_dataset), factor=1, normalize=True,
        test_every=8, load_exposure=False,
    )
    for camera_id, mapx in train_parser.mapx_dict.items():
        height, width = mapx.shape
        train_parser.roi_undist_dict[camera_id] = (0, 0, width, height)
        train_parser.imsize_dict[camera_id] = (width, height)

    registration = json.loads((REGISTRATION / "result.json").read_text())
    if registration.get("status") != "complete":
        raise RuntimeError("Held-out registration is incomplete")
    frozen = (
        registration.get("train_poses_frozen") is True
        and registration.get("train_point_xyz_frozen") is True
        and registration.get("camera_intrinsics_frozen") is True
    )
    if not frozen or tuple(registration.get("heldout_names", ())) != HELDOUT_NAMES:
        raise RuntimeError("Held-out registration invariants do not match")

    reconstruction = pycolmap.Reconstruction(str(REGISTRATION / "registered_model"))
    images_by_name = {
        image.name: image for image in reconstruction.images.values()
        if image.has_pose
    }
    views = []
    for name in HELDOUT_NAMES:
        image = images_by_name[name]
        raw_camtoworld = np.linalg.inv(_image_w2c(image))[None]
        camtoworld = transform_cameras(train_parser.transform, raw_camtoworld)[0]
        camera_id = int(image.camera_id)
        target = imageio.imread(REGISTRATION / "images" / name)[..., :3]
        if camera_id in train_parser.mapx_dict:
            target = cv2.remap(
                target,
                train_parser.mapx_dict[camera_id],
                train_parser.mapy_dict[camera_id],
                cv2.INTER_LINEAR,
            )
        if target.shape != (1080, 1920, 3):
            raise RuntimeError(f"Unexpected held-out shape for {name}: {target.shape}")
        views.append(
            {
                "name": name,
                "K": torch.from_numpy(train_parser.Ks_dict[camera_id]).float(),
                "camtoworld": torch.from_numpy(camtoworld).float(),
                "height": torch.tensor(1080),
                "width": torch.tensor(1920),
                "target": torch.from_numpy(target.copy()).float() / 255.0,
            }
        )
    return views


def load_blocks(builder, fit_seed: int, device: torch.device) -> torch.Tensor:
    path = HERE / "out" / f"production_fisher_seed{fit_seed}" / "fisher_blocks.pt"
    record = json.loads((HERE / "phase5_production_fisher_result.json").read_text())
    expected = next(row for row in record["seeds"] if row["fit_seed"] == fit_seed)
    if builder.sha256(path) != expected["fisher_blocks_sha256"]:
        raise RuntimeError("Production Fisher artifact hash mismatch")
    state = torch.load(path, map_location="cpu", weights_only=True)
    if state["fit_seed"] != fit_seed or state["probe_count"] != 512:
        raise RuntimeError("Production Fisher metadata mismatch")
    return state["blocks"].to(device)


def save_state(
    path: Path,
    fit_seed: int,
    view_index: int,
    next_probe: int,
    generator: torch.Generator,
    accumulators: dict[str, torch.Tensor],
    probe_count: int,
) -> None:
    torch.save(
        {
            "fit_seed": fit_seed,
            "view_index": view_index,
            "next_probe": next_probe,
            "probe_count": probe_count,
            "generator_state": generator.get_state(),
            "accumulators": {
                name: value.detach().cpu() for name, value in accumulators.items()
            },
        },
        path,
    )


def load_state(
    path: Path,
    fit_seed: int,
    probe_count: int,
    device: torch.device,
) -> tuple[int, int, torch.Generator | None, dict[str, torch.Tensor] | None]:
    if not path.is_file():
        return 0, 0, None, None
    state = torch.load(path, map_location="cpu", weights_only=True)
    if state["fit_seed"] != fit_seed or state["probe_count"] != probe_count:
        raise RuntimeError("Gate checkpoint protocol mismatch")
    generator = torch.Generator(device="cpu")
    generator.set_state(state["generator_state"])
    accumulators = {
        name: value.to(device) for name, value in state["accumulators"].items()
    }
    return state["view_index"], state["next_probe"], generator, accumulators


def run(fit_seed: int, source: Path, smoke: bool = False) -> dict[str, object]:
    builder = _load_builder()
    examples = builder.verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Gate B/B2 requires CUDA")
    device = torch.device("cuda")
    probe_count = SMOKE_PROBE_COUNT if smoke else PROBE_COUNT
    view_count = 1 if smoke else len(HELDOUT_NAMES)
    run_dir = HERE / "out" / (
        f"gate_b_smoke_seed{fit_seed}" if smoke else f"gate_b_seed{fit_seed}"
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    state_path = run_dir / "state.pt"

    views = load_heldout_views(examples)
    splats = builder.load_checkpoint(fit_seed, device)
    blocks = load_blocks(builder, fit_seed, device)
    theta_template = torch.cat([splats["means"], splats["scales"]], dim=1)
    if blocks.shape != (theta_template.shape[0], 6, 6):
        raise RuntimeError("Fisher/checkpoint shape mismatch")
    damping = block_damping(blocks)
    eigenvectors, inverse_sqrt, psd_metrics = psd_inverse_sqrt(blocks, damping)
    diagonal_scale = torch.diagonal(blocks, dim1=1, dim2=2).add(damping).rsqrt()

    start_view, start_probe, saved_generator, saved_accumulators = load_state(
        state_path, fit_seed, probe_count, device
    )
    if start_view > view_count:
        raise RuntimeError("Gate checkpoint is beyond requested views")
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    for view_index in range(start_view, view_count):
        view = views[view_index]
        theta, raw_render = builder.make_renderer(splats, view)

        def render(value: torch.Tensor) -> torch.Tensor:
            return raw_render(value).clamp(0.0, 1.0)

        with torch.no_grad():
            baseline = render(theta)
        target = view["target"].to(device).unsqueeze(0)
        residual = torch.linalg.vector_norm(baseline - target, dim=-1).squeeze(0)
        amplitude = torch.linalg.vector_norm(baseline, dim=-1).squeeze(0)

        if view_index == start_view and saved_accumulators is not None:
            generator = saved_generator
            assert generator is not None
            accumulators = saved_accumulators
            probe_start = start_probe
        else:
            generator = torch.Generator(device="cpu").manual_seed(score_seed(view_index))
            accumulators = {
                name: torch.zeros_like(baseline)
                for name in ("block", "diag", "identity")
            }
            probe_start = 0

        for probe_index in range(probe_start, probe_count):
            signs = torch.randint(
                0, 2, tuple(theta.shape), generator=generator, dtype=torch.int8
            ).to(device=device, dtype=torch.float32).mul_(2).sub_(1)
            directions = {
                "block": apply_inverse_sqrt(eigenvectors, inverse_sqrt, signs),
                "diag": signs * diagonal_scale,
                "identity": signs,
            }
            for name, direction in directions.items():
                jvp = finite_difference_jvp(render, theta, direction)
                accumulators[name].add_(jvp.square())
            completed = probe_index + 1
            if completed % CHECKPOINT_EVERY == 0 or completed == probe_count:
                save_state(
                    state_path, fit_seed, view_index, completed, generator,
                    accumulators, probe_count,
                )
                print(
                    f"seed {fit_seed} view {view_index + 1}/{view_count} "
                    f"probe {completed}/{probe_count}", flush=True,
                )

        maps = {
            name: (value / probe_count).sum(dim=-1).clamp_min(0).sqrt().squeeze(0).cpu()
            for name, value in accumulators.items()
        }
        torch.save(
            {
                "fit_seed": fit_seed,
                "view_index": view_index,
                "view_name": view["name"],
                "probe_count": probe_count,
                "residual": residual.cpu(),
                "amplitude": amplitude.cpu(),
                **maps,
                "mse_rgb": float((baseline - target).square().mean()),
            },
            run_dir / f"view_{view_index}.pt",
        )
        next_view = view_index + 1
        next_generator = torch.Generator(device="cpu").manual_seed(
            score_seed(next_view) if next_view < view_count else ESTIMATOR_SEED
        )
        save_state(
            state_path, fit_seed, next_view, 0, next_generator,
            {name: torch.empty(0) for name in ("block", "diag", "identity")},
            probe_count,
        )
        start_probe = 0
        saved_accumulators = None

    rows = [
        torch.load(run_dir / f"view_{index}.pt", map_location="cpu", weights_only=True)
        for index in range(view_count)
    ]
    residual_values = np.concatenate([row["residual"].numpy().reshape(-1) for row in rows])
    residual_rank = rankdata(residual_values, method="average")
    residual_rank -= residual_rank.mean()
    correlations = {
        "block_fisher": spearman_from_ranks(
            np.concatenate([row["block"].numpy().reshape(-1) for row in rows]), residual_rank
        ),
        "amplitude": spearman_from_ranks(
            np.concatenate([row["amplitude"].numpy().reshape(-1) for row in rows]), residual_rank
        ),
        "j_norm_h_identity": spearman_from_ranks(
            np.concatenate([row["identity"].numpy().reshape(-1) for row in rows]), residual_rank
        ),
        "diagonal_fisher": spearman_from_ranks(
            np.concatenate([row["diag"].numpy().reshape(-1) for row in rows]), residual_rank
        ),
    }
    controls = {name: value for name, value in correlations.items() if name != "block_fisher"}
    result = {
        "phase": "gate_b_b2_smoke" if smoke else "gate_b_b2",
        "status": "smoke_complete" if smoke else "complete",
        "fit_seed": fit_seed,
        "heldout_views": view_count,
        "probe_count_per_view": probe_count,
        "estimator_seed": ESTIMATOR_SEED,
        "view_seed_rule": "314159 + 1000003 * (zero_based_heldout_view + 1)",
        "same_rademacher_signs_across_scores": True,
        "max_parameter_displacement": MAX_PARAMETER_DISPLACEMENT,
        "damping": damping,
        "damping_fraction": DAMPING_FRACTION,
        "psd_projection": psd_metrics,
        "render_rgb_clamped_0_1": True,
        "pixel_scalar": "RGB L2",
        "correlations": correlations,
        "gate_b_pass": correlations["block_fisher"] >= GATE_RHO,
        "gate_b2_pass": correlations["block_fisher"] > max(controls.values()),
        "pooled_heldout_mse_rgb": float(np.mean([row["mse_rgb"] for row in rows])),
        "elapsed_this_invocation_seconds": time.perf_counter() - started,
        "peak_vram_gib": torch.cuda.max_memory_allocated() / 1024**3,
    }
    (run_dir / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fit-seed", type=int, choices=(0, 1, 2), required=True)
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    run(args.fit_seed, args.gsplat_source, smoke=args.smoke)


if __name__ == "__main__":
    main()
