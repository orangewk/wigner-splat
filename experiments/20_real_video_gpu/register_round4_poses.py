"""Register the four hard-locked Round 4 frames into a frozen train model copy."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROUND3_REGISTRATION = HERE / "register_heldout_poses.py"
ROUND4_MANIFEST = HERE / "data" / "round4_manifest.json"
FRESH_IMAGES = HERE / "data" / "heldout2-sealed"
DEFAULT_OUTPUT = HERE / "out" / "round4_registration"


def _load_round3_registration():
    spec = importlib.util.spec_from_file_location(
        "round3_registration", ROUND3_REGISTRATION
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def fresh_names_after_authorization(base) -> list[str]:
    phase3, fisher = base.load_authorization_records()
    base.authorize_heldout_access(phase3, fisher)
    manifest = json.loads(ROUND4_MANIFEST.read_text(encoding="utf-8"))
    expected_indices = [216, 244, 272, 300]
    if (
        manifest.get("round") != 4
        or manifest.get("status") != "sealed"
        or manifest.get("source_indices") != expected_indices
        or manifest.get("lossless_rgb_png") is not True
    ):
        raise RuntimeError("Round 4 sealed manifest does not match the hard lock")
    names = []
    for row in manifest.get("frames", []):
        path = HERE / row["relative_path"]
        if not path.is_file() or base.sha256(path) != row["sha256"].upper():
            raise RuntimeError(f"Round 4 sealed frame hash mismatch: {path}")
        names.append(path.name)
    expected_names = [f"round4_src_{index:04d}.png" for index in expected_indices]
    if names != expected_names:
        raise RuntimeError("Round 4 frame names/order do not match the hard lock")
    if {path.name for path in FRESH_IMAGES.glob("*.png")} != set(names):
        raise RuntimeError("Round 4 sealed directory contains unexpected files")
    return names


def quaternion_rotation(q: tuple[str, ...]) -> np.ndarray:
    w, x, y, z = (float(value) for value in q[:4])
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
        [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
    ])


def camera_center(pose: tuple[str, ...]) -> np.ndarray:
    rotation = quaternion_rotation(pose)
    translation = np.array([float(value) for value in pose[4:7]])
    return -rotation.T @ translation


def trajectory_record(
    poses: dict[str, tuple[str, ...]], train_names: list[str], fresh_names: list[str]
) -> dict[str, object]:
    ordered_train = sorted(train_names)
    train_centers = [camera_center(poses[name]) for name in ordered_train]
    train_steps = [
        float(np.linalg.norm(right - left))
        for left, right in zip(train_centers, train_centers[1:])
    ]
    fresh_centers = [camera_center(poses[name]) for name in fresh_names]
    fresh_steps = [
        float(np.linalg.norm(right - left))
        for left, right in zip(fresh_centers, fresh_centers[1:])
    ]
    bridge = float(np.linalg.norm(fresh_centers[0] - train_centers[-1]))
    median_train = float(np.median(train_steps))
    return {
        "descriptive_only": True,
        "coordinate_system": "raw COLMAP reconstruction",
        "train_consecutive_step_median": median_train,
        "last_train_to_first_fresh_step": bridge,
        "fresh_consecutive_steps": fresh_steps,
        "fresh_steps_over_train_median": [
            value / median_train for value in [bridge, *fresh_steps]
        ],
    }


def write_dnf(output: Path, train_names: list[str], fresh_names: list[str],
              registered_names: set[str]) -> dict[str, object]:
    missing = sorted(set(fresh_names) - registered_names)
    result = {
        "phase": "round4_fresh_pose_registration",
        "status": "dnf",
        "reason": "not_all_fresh_views_registered",
        "hard_stop": True,
        "scores_computed": False,
        "train_expected": len(train_names),
        "fresh_expected": len(fresh_names),
        "fresh_registered": len(set(fresh_names) & registered_names),
        "missing_fresh_names": missing,
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return result


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

    base = _load_round3_registration()
    train_names, old_heldout = base.split_names_after_authorization()
    fresh_names = fresh_names_after_authorization(base)
    if set(old_heldout) & set(fresh_names):
        raise RuntimeError("Fresh and previously opened held-out names overlap")

    output.mkdir(parents=True)
    images = output / "images"
    images.mkdir()
    for name in train_names:
        shutil.copy2(base.TRAIN_IMAGES / name, images / name)
    for name in fresh_names:
        shutil.copy2(FRESH_IMAGES / name, images / name)
    database = output / "database.db"
    shutil.copy2(base.TRAIN_COLMAP / "database.db", database)
    input_model = base.TRAIN_COLMAP / "sparse" / "0"
    frozen_model = output / "frozen_train_model"
    shutil.copytree(input_model, frozen_model)
    registered_model = output / "registered_model"
    registered_model.mkdir()
    fresh_list = output / "fresh_images.txt"
    fresh_list.write_text("\n".join(fresh_names) + "\n", encoding="utf-8")

    camera_id = base.single_camera_id(database)
    common = ("--log_target", "stderr")
    base.run(
        colmap, "feature_extractor", *common,
        "--database_path", database, "--image_path", images,
        "--image_list_path", fresh_list,
        "--ImageReader.existing_camera_id", camera_id,
        "--FeatureExtraction.use_gpu", 1, "--FeatureExtraction.gpu_index", 0,
    )
    base.run(
        colmap, "exhaustive_matcher", *common,
        "--database_path", database,
        "--FeatureMatching.use_gpu", 1, "--FeatureMatching.gpu_index", 0,
    )
    base.run(
        colmap, "image_registrator", *common,
        "--database_path", database, "--input_path", frozen_model,
        "--output_path", registered_model,
        "--Mapper.structure_less_registration_fallback", 0,
        "--Mapper.fix_existing_frames", 1,
    )

    frozen_txt = output / "frozen_train_txt"
    registered_txt = output / "registered_txt"
    frozen_txt.mkdir()
    registered_txt.mkdir()
    base.run(colmap, "model_converter", "--input_path", frozen_model,
             "--output_path", frozen_txt, "--output_type", "TXT")
    base.run(colmap, "model_converter", "--input_path", registered_model,
             "--output_path", registered_txt, "--output_type", "TXT")
    before = base.parse_registered_images(frozen_txt / "images.txt")
    after = base.parse_registered_images(registered_txt / "images.txt")
    if set(before) != set(train_names):
        raise RuntimeError("Frozen model does not contain exactly the train images")
    if not set(fresh_names).issubset(after):
        write_dnf(output, train_names, fresh_names, set(after))
        raise SystemExit(2)
    if set(after) != set(train_names + fresh_names):
        raise RuntimeError("Registered model contains unexpected images")
    if any(after[name] != before[name] for name in train_names):
        raise RuntimeError("An existing train pose or camera assignment changed")
    camera_hash = base.sha256(frozen_model / "cameras.bin")
    if camera_hash != base.sha256(registered_model / "cameras.bin"):
        raise RuntimeError("Frozen camera intrinsics changed")
    before_xyz = base.parse_point_xyz(frozen_txt / "points3D.txt")
    after_xyz = base.parse_point_xyz(registered_txt / "points3D.txt")
    if before_xyz != after_xyz:
        raise RuntimeError("A frozen train point ID or XYZ coordinate changed")

    result = {
        "phase": "round4_fresh_pose_registration",
        "status": "complete",
        "hard_stop_passed": True,
        "scores_computed": False,
        "train_poses_frozen": True,
        "train_point_xyz_frozen": True,
        "camera_intrinsics_frozen": True,
        "bundle_adjustment_run": False,
        "triangulation_run": False,
        "fresh_registered": len(fresh_names),
        "fresh_names": fresh_names,
        "trajectory": trajectory_record(after, train_names, fresh_names),
        "frozen_camera_sha256": camera_hash,
        "input_points3d_sha256": base.sha256(frozen_model / "points3D.bin"),
        "registered_points3d_sha256": base.sha256(registered_model / "points3D.bin"),
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
