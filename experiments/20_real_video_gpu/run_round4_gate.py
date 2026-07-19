"""Run the hard-locked Round 4 fresh-view Gate B/B2 evaluation."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
import torch
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ensemble_artifact import sha256, validate_shared_ensemble

ROUND3_GATE = HERE / "run_gate_b.py"
REGISTRATION = HERE / "out" / "round4_registration"
ENSEMBLE_DIR = HERE / "out" / "round4_ensemble"
HELDOUT_NAMES = (
    "round4_src_0216.png",
    "round4_src_0244.png",
    "round4_src_0272.png",
    "round4_src_0300.png",
)
DAMPING_FRACTIONS = (1e-4, 1e-6, 1e-8)
PRIMARY_DAMPING_FRACTION = 1e-6
VIEW_INDEX_OFFSET = 4
PROBE_COUNT = 256
CHECKPOINT_EVERY = 16


def _load_round3_gate():
    spec = importlib.util.spec_from_file_location("round3_gate", ROUND3_GATE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_views(examples: Path) -> list[dict[str, torch.Tensor | str]]:
    sys.path.insert(0, str(examples))
    import cv2
    import pycolmap
    from datasets.colmap import Parser, _image_w2c
    from datasets.normalize import transform_cameras

    parser = Parser(
        data_dir=str(HERE / "out" / "seed0_fixed_4000" / "train_dataset"),
        factor=1, normalize=True, test_every=8, load_exposure=False,
    )
    for camera_id, mapx in parser.mapx_dict.items():
        height, width = mapx.shape
        parser.roi_undist_dict[camera_id] = (0, 0, width, height)
        parser.imsize_dict[camera_id] = (width, height)
    record = json.loads((REGISTRATION / "result.json").read_text())
    frozen = (
        record.get("status") == "complete"
        and record.get("hard_stop_passed") is True
        and record.get("train_poses_frozen") is True
        and record.get("train_point_xyz_frozen") is True
        and record.get("camera_intrinsics_frozen") is True
        and tuple(record.get("fresh_names", ())) == HELDOUT_NAMES
    )
    if not frozen:
        raise RuntimeError("Round 4 registration hard stop has not passed")
    reconstruction = pycolmap.Reconstruction(str(REGISTRATION / "registered_model"))
    by_name = {
        image.name: image for image in reconstruction.images.values() if image.has_pose
    }
    views = []
    for name in HELDOUT_NAMES:
        image = by_name[name]
        raw = np.linalg.inv(_image_w2c(image))[None]
        camtoworld = transform_cameras(parser.transform, raw)[0]
        camera_id = int(image.camera_id)
        target = imageio.imread(REGISTRATION / "images" / name)[..., :3]
        if camera_id in parser.mapx_dict:
            target = cv2.remap(
                target, parser.mapx_dict[camera_id], parser.mapy_dict[camera_id],
                cv2.INTER_LINEAR,
            )
        if target.shape != (1080, 1920, 3):
            raise RuntimeError(f"Unexpected fresh-view shape: {name} {target.shape}")
        views.append({
            "name": name,
            "K": torch.from_numpy(parser.Ks_dict[camera_id]).float(),
            "camtoworld": torch.from_numpy(camtoworld).float(),
            "height": torch.tensor(1080),
            "width": torch.tensor(1920),
            "target": torch.from_numpy(target.copy()).float() / 255.0,
        })
    return views


def build_ensemble(gate, builder, views, device: torch.device) -> dict[str, object]:
    ENSEMBLE_DIR.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    map_sha256 = {}
    for view_index, view in enumerate(views):
        renders = []
        for fit_seed in range(3):
            splats = builder.load_checkpoint(fit_seed, device)
            theta, render = builder.make_renderer(splats, view)
            with torch.no_grad():
                renders.append(render(theta).clamp(0.0, 1.0))
            del splats, theta
        stack = torch.stack(renders)
        sigma = stack.var(dim=0, correction=1).sum(dim=-1).sqrt().squeeze(0)
        output = ENSEMBLE_DIR / f"view_{view_index}.pt"
        torch.save({
            "view_index": view_index,
            "view_name": view["name"],
            "fit_seeds": [0, 1, 2],
            "ddof": 1,
            "rgb_scalar": "sqrt(sum(channel sample variance))",
            "render_clamp": [0.0, 1.0],
            "sigma_ensemble": sigma.cpu(),
        }, output)
        map_sha256[view["name"]] = sha256(output)
    result = {
        "phase": "round4_shared_ensemble",
        "status": "complete",
        "fit_seeds": [0, 1, 2],
        "heldout_names": list(HELDOUT_NAMES),
        "ddof": 1,
        "shared_single_map_across_fit_seed_comparisons": True,
        "map_sha256": map_sha256,
        "monte_carlo_budget": 0,
        "elapsed_seconds": time.perf_counter() - started,
        "peak_vram_gib": torch.cuda.max_memory_allocated() / 1024**3,
    }
    (ENSEMBLE_DIR / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return result


def score_seed(gate, fresh_view_index: int) -> int:
    return gate.score_seed(VIEW_INDEX_OFFSET + fresh_view_index)


def damping_values(gate, blocks: torch.Tensor) -> dict[str, float]:
    mean_diagonal = float(torch.diagonal(blocks, dim1=1, dim2=2).mean())
    return {f"{fraction:.0e}": mean_diagonal * fraction
            for fraction in DAMPING_FRACTIONS}


def run(fit_seed: int, source: Path, build_shared_ensemble: bool = False) -> dict:
    gate = _load_round3_gate()
    builder = gate._load_builder()
    examples = builder.verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Round 4 Gate requires CUDA")
    device = torch.device("cuda")
    views = load_views(examples)
    if build_shared_ensemble:
        build_ensemble(gate, builder, views, device)
    validate_shared_ensemble(ENSEMBLE_DIR, HELDOUT_NAMES)

    splats = builder.load_checkpoint(fit_seed, device)
    blocks = gate.load_blocks(builder, fit_seed, device)
    theta_template = torch.cat([splats["means"], splats["scales"]], dim=1)
    if blocks.shape != (theta_template.shape[0], 6, 6):
        raise RuntimeError("Fisher/checkpoint shape mismatch")
    dampings = damping_values(gate, blocks)
    decompositions = {}
    psd_metrics = {}
    for label, damping in dampings.items():
        vectors, inverse_sqrt, metrics = gate.psd_inverse_sqrt(blocks, damping)
        decompositions[label] = (vectors, inverse_sqrt)
        psd_metrics[label] = metrics
    primary_label = f"{PRIMARY_DAMPING_FRACTION:.0e}"
    diagonal_scale = torch.diagonal(blocks, dim1=1, dim2=2).add(
        dampings[primary_label]
    ).rsqrt()
    names = ["block_1e-04", "block_1e-06", "block_1e-08", "diag", "identity"]
    run_dir = HERE / "out" / f"round4_gate_seed{fit_seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    state_path = run_dir / "state.pt"
    start_view, start_probe, saved_generator, saved_accumulators = gate.load_state(
        state_path, fit_seed, PROBE_COUNT, device
    )
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    for view_index in range(start_view, len(views)):
        view = views[view_index]
        theta, raw_render = builder.make_renderer(splats, view)
        render = lambda value: raw_render(value).clamp(0.0, 1.0)
        with torch.no_grad():
            baseline = render(theta)
        target = view["target"].to(device).unsqueeze(0)
        residual = torch.linalg.vector_norm(baseline - target, dim=-1).squeeze(0)
        amplitude = torch.linalg.vector_norm(baseline, dim=-1).squeeze(0)
        ensemble = torch.load(
            ENSEMBLE_DIR / f"view_{view_index}.pt", map_location="cpu",
            weights_only=True,
        )["sigma_ensemble"]
        if view_index == start_view and saved_accumulators is not None:
            generator = saved_generator
            accumulators = saved_accumulators
            probe_start = start_probe
        else:
            generator = torch.Generator(device="cpu").manual_seed(
                score_seed(gate, view_index)
            )
            accumulators = {name: torch.zeros_like(baseline) for name in names}
            probe_start = 0
        assert generator is not None
        for probe_index in range(probe_start, PROBE_COUNT):
            signs = torch.randint(
                0, 2, tuple(theta.shape), generator=generator, dtype=torch.int8
            ).to(device=device, dtype=torch.float32).mul_(2).sub_(1)
            directions = {"identity": signs, "diag": signs * diagonal_scale}
            for label, decomposition in decompositions.items():
                directions[f"block_{label}"] = gate.apply_inverse_sqrt(
                    *decomposition, signs
                )
            for name, direction in directions.items():
                accumulators[name].add_(
                    gate.finite_difference_jvp(render, theta, direction).square()
                )
            completed = probe_index + 1
            if completed % CHECKPOINT_EVERY == 0 or completed == PROBE_COUNT:
                gate.save_state(
                    state_path, fit_seed, view_index, completed, generator,
                    accumulators, PROBE_COUNT,
                )
                print(
                    f"round4 seed {fit_seed} view {view_index + 1}/4 "
                    f"probe {completed}/{PROBE_COUNT}", flush=True,
                )
        maps = {
            name: (value / PROBE_COUNT).sum(dim=-1).clamp_min(0).sqrt()
            .squeeze(0).cpu()
            for name, value in accumulators.items()
        }
        torch.save({
            "fit_seed": fit_seed, "view_index": view_index,
            "view_name": view["name"], "probe_count": PROBE_COUNT,
            "residual": residual.cpu(), "amplitude": amplitude.cpu(),
            "ensemble": ensemble, **maps,
            "mse_rgb": float((baseline - target).square().mean()),
        }, run_dir / f"view_{view_index}.pt")
        next_view = view_index + 1
        next_generator = torch.Generator(device="cpu").manual_seed(
            score_seed(gate, next_view) if next_view < 4 else gate.ESTIMATOR_SEED
        )
        gate.save_state(
            state_path, fit_seed, next_view, 0, next_generator,
            {name: torch.empty(0) for name in names}, PROBE_COUNT,
        )
        start_probe = 0
        saved_accumulators = None

    rows = [torch.load(
        run_dir / f"view_{index}.pt", map_location="cpu", weights_only=True
    ) for index in range(4)]
    residual_values = np.concatenate(
        [row["residual"].numpy().reshape(-1) for row in rows]
    )
    residual_rank = rankdata(residual_values, method="average")
    residual_rank -= residual_rank.mean()
    key_map = {
        "block_fisher": "block_1e-06", "amplitude": "amplitude",
        "j_norm_h_identity": "identity", "diagonal_fisher": "diag",
        "ensemble_sigma": "ensemble",
        "block_fisher_damping_1e-4": "block_1e-04",
        "block_fisher_damping_1e-8": "block_1e-08",
    }
    correlations = {
        label: gate.spearman_from_ranks(
            np.concatenate([row[key].numpy().reshape(-1) for row in rows]),
            residual_rank,
        )
        for label, key in key_map.items()
    }
    controls = [
        correlations[name] for name in (
            "amplitude", "j_norm_h_identity", "diagonal_fisher", "ensemble_sigma"
        )
    ]
    result = {
        "phase": "round4_gate_b_b2", "status": "complete",
        "fit_seed": fit_seed, "heldout_views": 4,
        "heldout_names": list(HELDOUT_NAMES),
        "probe_count_per_view": PROBE_COUNT,
        "view_seed_indices": [4, 5, 6, 7],
        "view_seeds": [score_seed(gate, index) for index in range(4)],
        "damping_fractions": list(DAMPING_FRACTIONS),
        "primary_damping_fraction": PRIMARY_DAMPING_FRACTION,
        "damping_values": dampings, "psd_projection": psd_metrics,
        "correlations": correlations,
        "gate_b_pass": correlations["block_fisher"] >= gate.GATE_RHO,
        "gate_b2_pass": correlations["block_fisher"] > max(controls),
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
    parser.add_argument("--build-shared-ensemble", action="store_true")
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    args = parser.parse_args()
    run(args.fit_seed, args.gsplat_source, args.build_shared_ensemble)


if __name__ == "__main__":
    main()
