"""Train-only gsplat adapter for issue #48 round 3.

The pinned upstream example trainer remains the implementation. This adapter
changes only the experiment boundary: all registered images are training data,
the seed is explicit, and evaluation reports pooled train PSNR.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
import types
from pathlib import Path
from typing import Any

import numpy as np
import torch

UPSTREAM_COMMIT = "77ab983ffe43420b2131669cb35776b883ca4c3c"
EXPERIMENT_DIR = Path(__file__).resolve().parent


def _install_torchmetrics_import_stub() -> None:
    """Stub metrics replaced by the protocol's pooled-MSE PSNR."""
    class _UnusedMetric:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def to(self, *args: Any, **kwargs: Any) -> "_UnusedMetric":
            return self

    root = types.ModuleType("torchmetrics")
    image = types.ModuleType("torchmetrics.image")
    lpip = types.ModuleType("torchmetrics.image.lpip")
    image.PeakSignalNoiseRatio = _UnusedMetric
    image.StructuralSimilarityIndexMeasure = _UnusedMetric
    lpip.LearnedPerceptualImagePatchSimilarity = _UnusedMetric
    root.image = image
    image.lpip = lpip
    sys.modules["torchmetrics"] = root
    sys.modules["torchmetrics.image"] = image
    sys.modules["torchmetrics.image.lpip"] = lpip


def _verify_upstream(source: Path) -> Path:
    examples = source / "examples"
    if not (examples / "simple_trainer.py").is_file():
        raise FileNotFoundError(f"Pinned gsplat trainer not found under {source}")
    actual = subprocess.run(
        ["git", "-C", str(source), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if actual != UPSTREAM_COMMIT:
        raise RuntimeError(f"gsplat commit mismatch: expected {UPSTREAM_COMMIT}, got {actual}")
    return examples


def _link_exact_file(source: Path, target: Path) -> None:
    if target.exists():
        if not target.is_file() or source.stat().st_size != target.stat().st_size:
            raise RuntimeError(f"Refusing mismatched existing dataset file: {target}")
        return
    try:
        os.link(source, target)
    except OSError:
        import shutil
        shutil.copy2(source, target)


def _prepare_train_only_dataset(run_dir: Path) -> Path:
    """Build a COLMAP layout without opening/enumerating heldout-sealed."""
    image_source = EXPERIMENT_DIR / "data" / "train"
    sparse_source = EXPERIMENT_DIR / "colmap" / "train" / "sparse" / "0"
    images = sorted(image_source.glob("*.png"))
    if len(images) != 20:
        raise RuntimeError(f"Expected exactly 20 train PNGs, found {len(images)}")
    dataset = run_dir / "train_dataset"
    image_target = dataset / "images"
    sparse_target = dataset / "sparse" / "0"
    image_target.mkdir(parents=True, exist_ok=True)
    sparse_target.mkdir(parents=True, exist_ok=True)
    for source in images:
        _link_exact_file(source, image_target / source.name)
    for name in ["cameras.bin", "images.bin", "points3D.bin", "rigs.bin", "frames.bin"]:
        source = sparse_source / name
        if not source.is_file():
            raise FileNotFoundError(source)
        _link_exact_file(source, sparse_target / name)
    if {p.name for p in image_target.glob("*.png")} != {p.name for p in images}:
        raise RuntimeError("Train dataset contains unexpected image names")
    return dataset


def _eval_steps(max_steps: int, every: int) -> list[int]:
    values = {1, max_steps}
    values.update(range(every, max_steps + 1, every))
    return sorted(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--steps", type=int, default=4000)
    parser.add_argument("--eval-every", type=int, default=250)
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument("--run-name", default=None)
    args = parser.parse_args()
    if args.steps < 1 or args.eval_every < 1:
        parser.error("--steps and --eval-every must be positive")

    examples = _verify_upstream(args.gsplat_source.resolve())
    sys.path.insert(0, str(examples))
    _install_torchmetrics_import_stub()
    import simple_trainer as upstream
    import utils as upstream_utils
    from datasets.colmap import Dataset as UpstreamDataset
    from gsplat.strategy import DefaultStrategy

    run_name = args.run_name or f"seed{args.seed}_pilot_{args.steps}"
    run_dir = EXPERIMENT_DIR / "out" / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    dataset_dir = _prepare_train_only_dataset(run_dir)

    class TrainOnlyDataset(UpstreamDataset):
        """Use every registered image and cache decoded tensors in CPU RAM."""
        def __init__(self, parser: Any, *pos: Any, **kwargs: Any) -> None:
            # Upstream crops the valid undistortion ROI (1919x1079 here).
            # Keep its calibrated remap/K but retain the declared 1920x1080
            # canvas; no resolution reduction is permitted in this round.
            for camera_id, mapx in parser.mapx_dict.items():
                height, width = mapx.shape
                parser.roi_undist_dict[camera_id] = (0, 0, width, height)
                parser.imsize_dict[camera_id] = (width, height)
                mask = parser.mask_dict[camera_id]
                if mask is not None and mask.shape != (height, width):
                    raise RuntimeError("Unexpected cropped fisheye mask")
            super().__init__(parser, *pos, **kwargs)
            self.indices = np.arange(len(parser.image_names))
            if not hasattr(parser, "_round3_cpu_cache"):
                parser._round3_cpu_cache = {}

        def __getitem__(self, item: int) -> dict[str, Any]:
            cache = self.parser._round3_cpu_cache
            index = int(self.indices[item])
            if index not in cache:
                cache[index] = super().__getitem__(item)
            return cache[index]

    upstream.Dataset = TrainOnlyDataset

    def set_experiment_seed(_ignored: int) -> None:
        upstream_utils.set_random_seed(args.seed)
        torch.cuda.manual_seed_all(args.seed)

    upstream.set_random_seed = set_experiment_seed
    real_dataloader = torch.utils.data.DataLoader

    def cpu_dataloader(*pos: Any, **kwargs: Any) -> Any:
        kwargs["num_workers"] = 0
        kwargs.pop("persistent_workers", None)
        return real_dataloader(*pos, **kwargs)

    upstream.torch.utils.data.DataLoader = cpu_dataloader

    @torch.no_grad()
    def pooled_train_eval(self: Any, step: int, stage: str = "train_pooled") -> None:
        started = time.perf_counter()
        squared_error = 0.0
        value_count = 0
        loader = real_dataloader(self.trainset, batch_size=1, shuffle=False, num_workers=0)
        for data in loader:
            camtoworlds = data["camtoworld"].to(self.device)
            intrinsics = data["K"].to(self.device)
            target = data["image"].to(self.device) / 255.0
            height, width = target.shape[1:3]
            rendered, _, _ = self.stage.render(
                self.scene.id,
                camtoworlds=camtoworlds,
                Ks=intrinsics,
                width=width,
                height=height,
                sh_degree=self.cfg.sh_degree,
                near_plane=self.cfg.near_plane,
                far_plane=self.cfg.far_plane,
                image_ids=data["image_id"].to(self.device),
            )
            delta = torch.clamp(rendered[..., :3], 0.0, 1.0) - target
            squared_error += torch.sum(delta.double().square()).item()
            value_count += delta.numel()
        mse = squared_error / value_count
        stats = {
            "step": step,
            "pooled_mse": mse,
            "pooled_psnr_db": -10.0 * math.log10(mse),
            "train_images": len(self.trainset),
            "value_count": value_count,
            "num_GS": len(self.splats["means"]),
            "peak_vram_gib": torch.cuda.max_memory_allocated() / 1024**3,
            "eval_seconds": time.perf_counter() - started,
        }
        output = Path(self.stats_dir) / f"{stage}_step{step:04d}.json"
        output.write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8")
        with (run_dir / "metrics.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(stats) + "\n")
        print(
            f"Pooled train PSNR: {stats['pooled_psnr_db']:.3f} dB | "
            f"GS: {stats['num_GS']} | peak VRAM: {stats['peak_vram_gib']:.3f} GiB"
        )

    upstream.Runner.eval = pooled_train_eval
    cfg = upstream.Config(
        disable_viewer=True,
        data_dir=str(dataset_dir),
        data_factor=1,
        result_dir=str(run_dir / "results"),
        load_exposure=False,
        max_steps=args.steps,
        eval_steps=_eval_steps(args.steps, args.eval_every),
        save_steps=_eval_steps(args.steps, args.eval_every),
        ply_steps=[],
        disable_video=True,
        packed=True,
        strategy=DefaultStrategy(verbose=True),
    )
    record = {
        "seed": args.seed,
        "steps": args.steps,
        "eval_every": args.eval_every,
        "upstream_commit": UPSTREAM_COMMIT,
        "train_images": 20,
        "full_resolution": True,
        "packed": True,
        "configured_sh_degree": cfg.sh_degree,
        "sh_degree_interval": cfg.sh_degree_interval,
        "max_sh_degree_reached": min((args.steps - 1) // cfg.sh_degree_interval, cfg.sh_degree),
        "appearance_optimization": False,
        "heldout_access": False,
    }
    (run_dir / "adapter_config.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    torch.cuda.reset_peak_memory_stats()
    upstream.main(0, 0, 1, cfg)


if __name__ == "__main__":
    main()
