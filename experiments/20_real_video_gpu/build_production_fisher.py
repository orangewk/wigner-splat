"""Build the declared production block Fisher from train views only.

The fixed Phase 3 checkpoint supplies the Gaussian parameters.  This adapter
opens only that run's hard-linked ``train_dataset`` and accumulates 512
Rademacher VJP probes per view into per-Gaussian 6x6 blocks over
``[mean(3), raw log-scale(3)]``.  A restart checkpoint is written after every
completed view; no held-out path is constructed or enumerated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np
import torch

UPSTREAM_COMMIT = "77ab983ffe43420b2131669cb35776b883ca4c3c"
ESTIMATOR_SEED = 314159
PROBE_COUNT = 512
EXPERIMENT_DIR = Path(__file__).resolve().parent
CHECKPOINT_SHA256 = {
    0: "CB602D0971CA996347C7812EB36A8DCA6D3B0523AC15A73D74D9B7690FCBFFC2",
    1: "8AA722643FFCD62259C54EE0992FD58C6E1F53FC206055F2F65751CC563AEDA5",
    2: "04CF7C63608E92C57F5C92943970C675BDC5D3573AE910D3950ECC4B40BC5F49",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def verify_upstream(source: Path) -> Path:
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
    examples = source / "examples"
    if not (examples / "datasets" / "colmap.py").is_file():
        raise FileNotFoundError("Pinned gsplat COLMAP dataset module is missing")
    return examples


def checkpoint_path(fit_seed: int) -> Path:
    return (
        EXPERIMENT_DIR
        / "out"
        / f"seed{fit_seed}_fixed_4000"
        / "results"
        / "ckpts"
        / "ckpt_3999_rank0.pt"
    )


def load_checkpoint(fit_seed: int, device: torch.device) -> dict[str, torch.Tensor]:
    path = checkpoint_path(fit_seed)
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_sha = sha256(path)
    if actual_sha != CHECKPOINT_SHA256[fit_seed]:
        raise RuntimeError(
            f"checkpoint hash mismatch for seed {fit_seed}: {actual_sha}"
        )
    checkpoint = torch.load(path, map_location="cpu", weights_only=True)
    if checkpoint["step"] != 3999 or checkpoint["scene_id"] != "scene":
        raise RuntimeError("Unexpected checkpoint identity")
    required = {"means", "scales", "quats", "opacities", "sh0", "shN"}
    if set(checkpoint["splats"]) != required:
        raise RuntimeError("Unexpected checkpoint splat keys")
    return {name: value.to(device) for name, value in checkpoint["splats"].items()}


def load_train_views(examples: Path, fit_seed: int) -> list[dict[str, torch.Tensor]]:
    sys.path.insert(0, str(examples))
    from datasets.colmap import Dataset, Parser

    dataset_dir = (
        EXPERIMENT_DIR / "out" / f"seed{fit_seed}_fixed_4000" / "train_dataset"
    )
    parser = Parser(
        data_dir=str(dataset_dir),
        factor=1,
        normalize=True,
        test_every=8,
        load_exposure=False,
    )
    if len(parser.image_names) != 20:
        raise RuntimeError(f"Expected exactly 20 train images, got {len(parser.image_names)}")
    for camera_id, mapx in parser.mapx_dict.items():
        height, width = mapx.shape
        parser.roi_undist_dict[camera_id] = (0, 0, width, height)
        parser.imsize_dict[camera_id] = (width, height)
    dataset = Dataset(parser, split="train")
    dataset.indices = np.arange(len(parser.image_names))
    views = []
    for index in range(len(dataset)):
        item = dataset[index]
        height, width = item["image"].shape[:2]
        views.append(
            {
                "K": item["K"],
                "camtoworld": item["camtoworld"],
                "height": torch.tensor(height),
                "width": torch.tensor(width),
            }
        )
    if {(int(view["width"]), int(view["height"])) for view in views} != {
        (1920, 1080)
    }:
        raise RuntimeError("Production Fisher requires the fixed full resolution")
    return views


def make_renderer(
    splats: dict[str, torch.Tensor], view: dict[str, torch.Tensor]
) -> tuple[torch.Tensor, Callable[[torch.Tensor], torch.Tensor]]:
    from gsplat.rendering import rasterization

    theta = torch.cat([splats["means"], splats["scales"]], dim=1)
    fixed_quats = splats["quats"]
    fixed_opacities = torch.sigmoid(splats["opacities"])
    fixed_colors = torch.cat([splats["sh0"], splats["shN"]], dim=1)
    device = theta.device
    camtoworld = view["camtoworld"].to(device).unsqueeze(0)
    K = view["K"].to(device).unsqueeze(0)
    width, height = int(view["width"]), int(view["height"])

    def render(value: torch.Tensor) -> torch.Tensor:
        image, _, _ = rasterization(
            means=value[:, :3],
            quats=fixed_quats,
            scales=value[:, 3:].exp(),
            opacities=fixed_opacities,
            colors=fixed_colors,
            viewmats=torch.linalg.inv(camtoworld),
            Ks=K,
            width=width,
            height=height,
            packed=True,
            sh_degree=3,
            render_mode="RGB",
            near_plane=0.01,
            far_plane=1e10,
            rasterize_mode="classic",
            camera_model="pinhole",
        )
        return image

    return theta, render


def view_generator(view_index: int) -> torch.Generator:
    # Independent, reproducible streams derived from the declared root seed.
    return torch.Generator(device="cpu").manual_seed(
        ESTIMATOR_SEED + 1_000_003 * view_index
    )


def rademacher_like(output: torch.Tensor, generator: torch.Generator) -> torch.Tensor:
    signs = torch.randint(
        0, 2, tuple(output.shape), generator=generator, dtype=torch.int8
    )
    return signs.to(device=output.device, dtype=output.dtype).mul_(2).sub_(1)


def load_partial(
    path: Path,
    fit_seed: int,
    n_splats: int,
    device: torch.device,
) -> tuple[int, torch.Tensor, list[dict[str, float]]]:
    if not path.is_file():
        blocks = torch.zeros((n_splats, 6, 6), device=device, dtype=torch.float32)
        return 0, blocks, []
    state = torch.load(path, map_location="cpu", weights_only=True)
    expected = {
        "fit_seed": fit_seed,
        "estimator_seed": ESTIMATOR_SEED,
        "probe_count": PROBE_COUNT,
        "checkpoint_sha256": CHECKPOINT_SHA256[fit_seed],
        "n_splats": n_splats,
    }
    for key, value in expected.items():
        if state[key] != value:
            raise RuntimeError(f"Partial Fisher state mismatch for {key}")
    return state["next_view"], state["blocks"].to(device), state["view_stats"]


def save_partial(
    path: Path,
    fit_seed: int,
    next_view: int,
    blocks: torch.Tensor,
    view_stats: list[dict[str, float]],
) -> None:
    torch.save(
        {
            "fit_seed": fit_seed,
            "estimator_seed": ESTIMATOR_SEED,
            "probe_count": PROBE_COUNT,
            "checkpoint_sha256": CHECKPOINT_SHA256[fit_seed],
            "n_splats": blocks.shape[0],
            "next_view": next_view,
            "blocks": blocks.detach().cpu(),
            "view_stats": view_stats,
            "heldout_accessed": False,
        },
        path,
    )


def run(
    fit_seed: int,
    source: Path,
    smoke: bool = False,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    examples = verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Production Fisher requires CUDA")
    device = torch.device("cuda")
    views = load_train_views(examples, fit_seed)
    splats = load_checkpoint(fit_seed, device)
    n_splats = splats["means"].shape[0]
    probe_count = 2 if smoke else PROBE_COUNT
    view_count = 1 if smoke else len(views)
    if output_dir is not None and not smoke:
        raise ValueError("output_dir override is restricted to smoke runs")
    run_dir = output_dir or EXPERIMENT_DIR / "out" / (
        f"production_fisher_smoke_seed{fit_seed}"
        if smoke
        else f"production_fisher_seed{fit_seed}"
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    state_path = run_dir / "fisher_state.pt"
    if smoke:
        start_view = 0
        blocks = torch.zeros((n_splats, 6, 6), device=device)
        view_stats: list[dict[str, float]] = []
    else:
        start_view, blocks, view_stats = load_partial(
            state_path, fit_seed, n_splats, device
        )
    if start_view > view_count:
        raise RuntimeError("Partial Fisher state is beyond the requested views")

    torch.cuda.reset_peak_memory_stats()
    total_started = time.perf_counter()
    for view_index in range(start_view, view_count):
        view_started = time.perf_counter()
        theta, render = make_renderer(splats, views[view_index])
        theta_var = theta.detach().clone().requires_grad_(True)
        output = render(theta_var)
        if output.shape != (1, 1080, 1920, 3) or not torch.isfinite(output).all():
            raise RuntimeError("Unexpected or non-finite production render")
        generator = view_generator(view_index)
        for probe_index in range(probe_count):
            signs = rademacher_like(output, generator)
            gradient = torch.autograd.grad(
                output,
                theta_var,
                grad_outputs=signs,
                retain_graph=probe_index + 1 < probe_count,
            )[0]
            blocks += torch.einsum("ni,nj->nij", gradient, gradient) / probe_count
        torch.cuda.synchronize()
        view_stats.append(
            {
                "view_index": view_index,
                "seconds": time.perf_counter() - view_started,
                "block_trace_sum": float(
                    torch.diagonal(blocks, dim1=1, dim2=2).sum()
                ),
            }
        )
        if not smoke:
            save_partial(state_path, fit_seed, view_index + 1, blocks, view_stats)
        print(
            f"view {view_index + 1}/{view_count}: "
            f"{view_stats[-1]['seconds']:.1f}s",
            flush=True,
        )

    elapsed = time.perf_counter() - total_started
    diagonal = torch.diagonal(blocks, dim1=1, dim2=2)
    result = {
        "phase": "production_train_block_fisher_smoke" if smoke else "production_train_block_fisher",
        "status": "smoke_pass" if smoke else "complete",
        "fit_seed": fit_seed,
        "checkpoint_sha256": CHECKPOINT_SHA256[fit_seed],
        "gsplat_commit": UPSTREAM_COMMIT,
        "heldout_accessed": False,
        "train_views": view_count,
        "probe_count_per_view": probe_count,
        "estimator_seed": ESTIMATOR_SEED,
        "view_seed_rule": "estimator_seed + 1000003 * zero_based_view_index",
        "n_splats": n_splats,
        "block_parameterization": [
            "mean_x", "mean_y", "mean_z", "log_scale_x", "log_scale_y", "log_scale_z"
        ],
        "elapsed_this_invocation_seconds": elapsed,
        "peak_vram_gib": torch.cuda.max_memory_allocated() / 1024**3,
        "block_trace_sum": float(diagonal.sum()),
        "finite": bool(torch.isfinite(blocks).all()),
        "view_stats": view_stats,
    }
    if not result["finite"]:
        raise RuntimeError("Production Fisher contains non-finite values")
    if not smoke:
        torch.save(
            {
                "blocks": blocks.detach().cpu(),
                "fit_seed": fit_seed,
                "probe_count": PROBE_COUNT,
                "estimator_seed": ESTIMATOR_SEED,
                "checkpoint_sha256": CHECKPOINT_SHA256[fit_seed],
            },
            run_dir / "fisher_blocks.pt",
        )
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
