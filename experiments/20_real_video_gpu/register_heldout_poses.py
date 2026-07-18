"""Register held-out poses against the frozen train-only COLMAP model.

The held-out directory is not enumerated until both the train-fit hard stop and
the production Fisher prerequisites have passed.  Registration runs in a copy:
the original database/model and all learned splats remain untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE3 = HERE / "phase3_fixed_result.json"
PHASE5_FISHER = HERE / "phase5_production_fisher_result.json"
MANIFEST = HERE / "data" / "manifest.json"
TRAIN_IMAGES = HERE / "data" / "train"
HELDOUT_IMAGES = HERE / "data" / "heldout-sealed"
TRAIN_COLMAP = HERE / "colmap" / "train"
DEFAULT_OUTPUT = HERE / "out" / "heldout_registration"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def authorize_heldout_access(phase3: dict, fisher: dict) -> None:
    psnrs = [run["pooled_psnr_db"] for run in phase3.get("runs", [])]
    fit_pass = (
        phase3.get("status") == "hard_stop_passed"
        and phase3.get("protocol", {}).get("heldout_accessed") is False
        and phase3.get("aggregate", {}).get("all_seeds_passed") is True
        and len(psnrs) == 3
        and min(psnrs) >= 25.0
    )
    fisher_pass = (
        fisher.get("status") == "complete"
        and fisher.get("heldout_accessed") is False
        and len(fisher.get("seeds", [])) == 3
        and fisher.get("validation", {}).get("all_finite") is True
        and fisher.get("validation", {}).get("checkpoint_metadata_matches") is True
    )
    if not fit_pass:
        raise RuntimeError("Train PSNR hard stop has not passed for all three seeds")
    if not fisher_pass:
        raise RuntimeError("Production train Fisher prerequisite is incomplete")


def load_authorization_records() -> tuple[dict, dict]:
    return (
        json.loads(PHASE3.read_text(encoding="utf-8")),
        json.loads(PHASE5_FISHER.read_text(encoding="utf-8")),
    )


def split_names_after_authorization() -> tuple[list[str], list[str]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    train = [
        Path(frame["relative_path"]).name
        for frame in manifest["frames"]
        if frame["split"] == "train"
    ]
    heldout = [
        Path(frame["relative_path"]).name
        for frame in manifest["frames"]
        if frame["split"] == "heldout-sealed"
    ]
    if len(train) != 20 or len(heldout) != 4 or set(train) & set(heldout):
        raise RuntimeError("Manifest split is not exactly disjoint train=20/heldout=4")
    actual_train = {path.name for path in TRAIN_IMAGES.glob("*.png")}
    actual_heldout = {path.name for path in HELDOUT_IMAGES.glob("*.png")}
    if actual_train != set(train) or actual_heldout != set(heldout):
        raise RuntimeError("Image files do not match the pinned manifest")
    return train, heldout


def run(*args: object) -> None:
    subprocess.run([str(arg) for arg in args], check=True)


def parse_registered_images(images_txt: Path) -> dict[str, tuple[str, ...]]:
    poses: dict[str, tuple[str, ...]] = {}
    for line in images_txt.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) >= 10 and fields[-1].lower().endswith(".png"):
            poses[fields[-1]] = tuple(fields[1:10])
    return poses


def parse_point_xyz(points_txt: Path) -> dict[int, tuple[str, str, str]]:
    points = {}
    for line in points_txt.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if fields and not fields[0].startswith("#"):
            points[int(fields[0])] = tuple(fields[1:4])
    return points


def single_camera_id(database: Path) -> int:
    with sqlite3.connect(database) as connection:
        rows = connection.execute("SELECT camera_id FROM cameras").fetchall()
    if len(rows) != 1:
        raise RuntimeError(f"Expected one pinned train camera, found {rows}")
    return int(rows[0][0])


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

    phase3, fisher = load_authorization_records()
    authorize_heldout_access(phase3, fisher)
    # This is deliberately the first function allowed to enumerate held-out.
    train_names, heldout_names = split_names_after_authorization()

    output.mkdir(parents=True)
    images = output / "images"
    images.mkdir()
    for name in train_names:
        shutil.copy2(TRAIN_IMAGES / name, images / name)
    for name in heldout_names:
        shutil.copy2(HELDOUT_IMAGES / name, images / name)

    database = output / "database.db"
    shutil.copy2(TRAIN_COLMAP / "database.db", database)
    input_model = TRAIN_COLMAP / "sparse" / "0"
    frozen_model = output / "frozen_train_model"
    shutil.copytree(input_model, frozen_model)
    registered_model = output / "registered_model"
    registered_model.mkdir()
    heldout_list = output / "heldout_images.txt"
    heldout_list.write_text("\n".join(heldout_names) + "\n", encoding="utf-8")

    camera_id = single_camera_id(database)
    common = ("--log_target", "stderr")
    run(
        colmap,
        "feature_extractor",
        *common,
        "--database_path",
        database,
        "--image_path",
        images,
        "--image_list_path",
        heldout_list,
        "--ImageReader.existing_camera_id",
        camera_id,
        "--FeatureExtraction.use_gpu",
        1,
        "--FeatureExtraction.gpu_index",
        0,
    )
    run(
        colmap,
        "exhaustive_matcher",
        *common,
        "--database_path",
        database,
        "--FeatureMatching.use_gpu",
        1,
        "--FeatureMatching.gpu_index",
        0,
    )
    run(
        colmap,
        "image_registrator",
        *common,
        "--database_path",
        database,
        "--input_path",
        frozen_model,
        "--output_path",
        registered_model,
        "--Mapper.structure_less_registration_fallback",
        0,
        "--Mapper.fix_existing_frames",
        1,
    )

    frozen_txt = output / "frozen_train_txt"
    registered_txt = output / "registered_txt"
    frozen_txt.mkdir()
    registered_txt.mkdir()
    run(colmap, "model_converter", "--input_path", frozen_model,
        "--output_path", frozen_txt, "--output_type", "TXT")
    run(colmap, "model_converter", "--input_path", registered_model,
        "--output_path", registered_txt, "--output_type", "TXT")
    before = parse_registered_images(frozen_txt / "images.txt")
    after = parse_registered_images(registered_txt / "images.txt")
    if set(before) != set(train_names):
        raise RuntimeError("Frozen input model does not contain exactly the train images")
    if set(after) != set(train_names + heldout_names):
        missing = sorted(set(train_names + heldout_names) - set(after))
        raise RuntimeError(f"Held-out registration incomplete; missing={missing}")
    if any(after[name] != before[name] for name in train_names):
        raise RuntimeError("An existing train pose or camera assignment changed")

    camera_hash = sha256(frozen_model / "cameras.bin")
    if camera_hash != sha256(registered_model / "cameras.bin"):
        raise RuntimeError("Frozen camera intrinsics changed")
    before_xyz = parse_point_xyz(frozen_txt / "points3D.txt")
    after_xyz = parse_point_xyz(registered_txt / "points3D.txt")
    if before_xyz != after_xyz:
        raise RuntimeError("A frozen train point ID or XYZ coordinate changed")

    result = {
        "phase": "heldout_pose_registration",
        "status": "complete",
        "heldout_accessed": True,
        "train_poses_frozen": True,
        "train_point_xyz_frozen": True,
        "camera_intrinsics_frozen": True,
        "bundle_adjustment_run": False,
        "triangulation_run": False,
        "structure_less_registration_fallback": False,
        "gpu_feature_extraction": True,
        "gpu_feature_matching": True,
        "camera_id": camera_id,
        "train_registered": len(train_names),
        "heldout_registered": len(heldout_names),
        "heldout_names": heldout_names,
        "frozen_camera_sha256": camera_hash,
        "input_points3d_sha256": sha256(frozen_model / "points3D.bin"),
        "registered_points3d_sha256": sha256(registered_model / "points3D.bin"),
        "points3d_binary_diff_reason": "heldout observations appended to fixed XYZ tracks",
    }
    (output / "result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
