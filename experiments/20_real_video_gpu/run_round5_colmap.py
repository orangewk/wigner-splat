"""Run the Round 5 train-only COLMAP reconstruction for one public scene."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

import pycolmap

HERE = Path(__file__).resolve().parent
BASE_RUNNER = HERE / "run_colmap.py"
ROUND5_DATA = HERE / "data" / "round5"
ROUND5_OUT = HERE / "out" / "round5"


def _load_base():
    spec = importlib.util.spec_from_file_location("round3_colmap", BASE_RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_train_boundary(scene: str) -> tuple[Path, list[str]]:
    scene_root = ROUND5_DATA / scene.lower()
    manifest = json.loads((scene_root / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("scene") != scene:
        raise RuntimeError(f"Scene manifest mismatch for {scene}")
    expected_rows = [row for row in manifest["frames"] if row["split"] == "train"]
    train_images = scene_root / "train"
    actual = sorted(path.name for path in train_images.iterdir() if path.is_file())
    expected = sorted(Path(row["relative_path"]).name for row in expected_rows)
    if len(expected) != 20 or actual != expected:
        raise RuntimeError(
            f"{scene} train boundary mismatch: expected={expected}, actual={actual}"
        )
    for row in expected_rows:
        path = train_images / Path(row["relative_path"]).name
        if sha256(path) != row["sha256"]:
            raise RuntimeError(f"{scene} train frame hash mismatch: {path.name}")
    if any("heldout" in name.lower() for name in actual):
        raise RuntimeError("Held-out filename reached the train image directory")
    return train_images, actual


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=("Truck", "Train"), required=True)
    parser.add_argument("--colmap", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    colmap = args.colmap.resolve()
    output = (
        args.output.resolve()
        if args.output is not None
        else (ROUND5_OUT / args.scene.lower() / "colmap" / "exhaustive_v1").resolve()
    )
    if not colmap.is_file():
        raise FileNotFoundError(colmap)
    if output.exists():
        raise RuntimeError(f"Refusing to overwrite existing output: {output}")
    train_images, image_names = validate_train_boundary(args.scene)
    version = subprocess.check_output([str(colmap), "-h"], text=True).splitlines()[0]
    if "with CUDA" not in version:
        raise RuntimeError(f"COLMAP is not a CUDA build: {version}")

    output.mkdir(parents=True)
    database = output / "database.db"
    sparse = output / "sparse"
    common = ("--log_target", "stderr")
    base = _load_base()
    base.run(
        colmap, "feature_extractor", *common,
        "--database_path", database,
        "--image_path", train_images,
        "--ImageReader.single_camera", 1,
        "--ImageReader.camera_model", "SIMPLE_RADIAL",
        "--FeatureExtraction.use_gpu", 1,
        "--FeatureExtraction.gpu_index", 0,
    )
    base.run(
        colmap, "exhaustive_matcher", *common,
        "--database_path", database,
        "--FeatureMatching.use_gpu", 1,
        "--FeatureMatching.gpu_index", 0,
    )
    sparse.mkdir()
    base.run(
        colmap, "mapper", *common,
        "--database_path", database,
        "--image_path", train_images,
        "--output_path", sparse,
    )
    models = sorted(path for path in sparse.iterdir() if path.is_dir())
    if len(models) != 1:
        raise RuntimeError(f"Expected one reconstruction, got {models}")
    base.run(colmap, "model_analyzer", *common, "--path", models[0])
    registered_count = pycolmap.Reconstruction(str(models[0])).num_reg_images()
    complete = registered_count == len(image_names)
    record = {
        "phase": "round5_train_colmap",
        "status": "complete" if complete else "did_not_finish",
        "scene": args.scene,
        "train_images": image_names,
        "train_count": len(image_names),
        "registered_train_count": registered_count,
        "heldout_access": False,
        "feature_and_mapper_recipe_inherited_from": (
            "experiments/20_real_video_gpu/run_colmap.py"
        ),
        "matcher": "exhaustive",
        "matcher_correction_issue_comment": 5014845453,
        "preserved_failed_sequential_output": "colmap/train",
        "colmap_version": version,
        "sparse_model": str(models[0]),
    }
    (output / "result.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, indent=2))
    if not complete:
        raise RuntimeError(
            f"{args.scene} COLMAP registered {registered_count}/20 train images; DNF"
        )


if __name__ == "__main__":
    main()
