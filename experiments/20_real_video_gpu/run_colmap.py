"""Reproduce the train-only COLMAP reconstruction with a hard data boundary."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_MANIFEST = HERE / "data" / "manifest.json"
TRAIN_IMAGES = HERE / "data" / "train"
DEFAULT_OUTPUT = HERE / "colmap" / "train"


def run(*args: object) -> None:
    subprocess.run([str(arg) for arg in args], check=True)


def validate_train_boundary() -> None:
    manifest = json.loads(DATA_MANIFEST.read_text(encoding="utf-8"))
    expected = {
        Path(frame["relative_path"]).name
        for frame in manifest["frames"]
        if frame["split"] == "train"
    }
    actual = {path.name for path in TRAIN_IMAGES.glob("*.png")}
    if len(expected) != 20 or actual != expected:
        raise RuntimeError(
            f"Train boundary mismatch: expected={sorted(expected)}, actual={sorted(actual)}"
        )
    if any("heldout" in name.lower() for name in actual):
        raise RuntimeError("Held-out filename reached the train image directory")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--colmap", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    colmap = args.colmap.resolve()
    output = args.output.resolve()
    if not colmap.is_file():
        raise FileNotFoundError(colmap)
    if output.exists():
        raise RuntimeError(f"Refusing to overwrite existing output: {output}")
    validate_train_boundary()
    version = subprocess.check_output([str(colmap), "-h"], text=True).splitlines()[0]
    if "with CUDA" not in version:
        raise RuntimeError(f"COLMAP is not a CUDA build: {version}")

    output.mkdir(parents=True)
    database = output / "database.db"
    sparse = output / "sparse"
    common = ("--log_target", "stderr")
    run(colmap, "feature_extractor", *common, "--database_path", database,
        "--image_path", TRAIN_IMAGES, "--ImageReader.single_camera", 1,
        "--ImageReader.camera_model", "SIMPLE_RADIAL",
        "--FeatureExtraction.use_gpu", 1, "--FeatureExtraction.gpu_index", 0)
    run(colmap, "sequential_matcher", *common, "--database_path", database,
        "--FeatureMatching.use_gpu", 1, "--FeatureMatching.gpu_index", 0,
        "--SequentialMatching.overlap", 10,
        "--SequentialMatching.quadratic_overlap", 1,
        "--SequentialMatching.loop_detection", 0)
    sparse.mkdir()
    run(colmap, "mapper", *common, "--database_path", database,
        "--image_path", TRAIN_IMAGES, "--output_path", sparse)
    models = sorted(path for path in sparse.iterdir() if path.is_dir())
    if len(models) != 1:
        raise RuntimeError(f"Expected one reconstruction, got {models}")
    run(colmap, "model_analyzer", *common, "--path", models[0])


if __name__ == "__main__":
    main()
