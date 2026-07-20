"""Prepare the hard-locked Round 6 Tanks and Temples scene split.

Round 6 (Issue #48 comment 5017827938) changes only the data precondition
relative to Round 5: instead of a global stride, it selects a centrally fixed
contiguous block of 24 frames so that adjacent-frame overlap is structurally
guaranteed for SfM. The archives, scene specs, heldout positions, and all
integrity checks are reused unchanged from the Round 5 preparation module.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath

from PIL import Image

from prepare_round5_data import (
    DOWNLOAD_PAGE,
    EXPECTED_HEIGHT,
    EXPECTED_WIDTH,
    FRAME_COUNT,
    HELDOUT_POSITIONS,
    HERE,
    LICENSE_URL,
    SCENES,
    SceneSpec,
    image_members,
    sha256,
    sha256_bytes,
)

DATA_ROOT = HERE / "data" / "round6"
STAGING_ROOT = HERE / "data" / "round6-staging"


def selected_indices(total_frame_count: int) -> tuple[int, ...]:
    """Centrally fixed contiguous block: start = floor((total - 24) / 2)."""
    if total_frame_count < FRAME_COUNT:
        raise RuntimeError(f"Need at least {FRAME_COUNT} source frames")
    start = (total_frame_count - FRAME_COUNT) // 2
    return tuple(start + position for position in range(FRAME_COUNT))


def require_fresh_scene(scene: str) -> tuple[Path, Path]:
    output = DATA_ROOT / scene.lower()
    staging = STAGING_ROOT / scene.lower()
    occupied = [path for path in (output, staging) if path.exists()]
    if occupied:
        raise RuntimeError(f"Refusing to overwrite existing Round 6 data: {occupied}")
    return output, staging


def prepare_scene(spec: SceneSpec, archive_path: Path) -> dict:
    archive_path = archive_path.resolve()
    if not archive_path.is_file():
        raise FileNotFoundError(archive_path)
    if archive_path.stat().st_size != spec.archive_bytes:
        raise RuntimeError(f"{spec.scene} archive byte-size mismatch")
    archive_hash = sha256(archive_path)
    if archive_hash != spec.archive_sha256:
        raise RuntimeError(f"{spec.scene} archive SHA-256 mismatch")

    output, staging = require_fresh_scene(spec.scene)
    with zipfile.ZipFile(archive_path) as archive:
        members = image_members(archive)
        if len(members) != spec.expected_frames:
            raise RuntimeError(
                f"{spec.scene} frame count {len(members)} != {spec.expected_frames}"
            )
        source_indices = selected_indices(len(members))
        staged_payloads = []
        for position, source_index in enumerate(source_indices):
            member = members[source_index]
            payload = archive.read(member)
            with Image.open(BytesIO(payload)) as image:
                geometry = (image.width, image.height)
                mode = image.mode
            if geometry != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
                raise RuntimeError(
                    f"Unexpected native geometry for {member.filename}: {geometry}"
                )
            staged_payloads.append((position, source_index, member, payload, mode))

    train = staging / "train"
    heldout = staging / "heldout-sealed"
    train.mkdir(parents=True)
    heldout.mkdir()
    frames = []
    for position, source_index, member, payload, mode in staged_payloads:
        split = "heldout-sealed" if position in HELDOUT_POSITIONS else "train"
        target_dir = heldout if split == "heldout-sealed" else train
        suffix = PurePosixPath(member.filename).suffix.lower()
        target = target_dir / f"frame_{position:02d}_src_{source_index:04d}{suffix}"
        with target.open("xb") as stream:
            stream.write(payload)
        frames.append({
            "position": position,
            "source_frame_index": source_index,
            "source_member": member.filename,
            "split": split,
            "relative_path": target.relative_to(staging).as_posix(),
            "sha256": sha256_bytes(payload),
            "bytes": len(payload),
            "width": EXPECTED_WIDTH,
            "height": EXPECTED_HEIGHT,
            "mode": mode,
        })

    manifest = {
        "schema_version": 1,
        "round": 6,
        "scene": spec.scene,
        "scene_index": spec.scene_index,
        "source": {
            "dataset": "Tanks and Temples",
            "download_page": DOWNLOAD_PAGE,
            "archive_url": spec.source_url,
            "archive_basename": archive_path.name,
            "archive_bytes": spec.archive_bytes,
            "archive_sha256": archive_hash,
            "license_cc_by_notice": (
                "CC BY 4.0, stated in the Copyright section of the official "
                "license page"
            ),
            "license_additional_restrictions": (
                "The License Grant section of the same official license page "
                "limits use to non-commercial research and education and "
                "forbids providing copies to third parties; the page is "
                "internally inconsistent and this record does not resolve it"
            ),
            "license_url": LICENSE_URL,
            "citation": (
                "Knapitsch, Park, Zhou, and Koltun. Tanks and Temples: "
                "Benchmarking Large-Scale Scene Reconstruction. ACM TOG, 2017."
            ),
        },
        "selection": {
            "total_frame_count": len(members),
            "selected_frame_count": FRAME_COUNT,
            "rule": (
                "contiguous central block: source_index = "
                "floor((total_frame_count - 24) / 2) + position"
            ),
            "start": (len(members) - FRAME_COUNT) // 2,
            "source_indices": list(source_indices),
            "heldout_positions": sorted(HELDOUT_POSITIONS),
            "native_resolution": [EXPECTED_WIDTH, EXPECTED_HEIGHT],
            "transcoding": False,
        },
        "sealing": {
            "meaning_for_public_data": (
                "Training and COLMAP code may enumerate only train/. "
                "heldout-sealed/ is not read before the train-PSNR hard stop."
            ),
            "train_count": 20,
            "heldout_count": 4,
        },
        "frames": frames,
    }
    (staging / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    staging.rename(output)
    print(json.dumps({
        "scene": spec.scene,
        "output": str(output),
        "archive_sha256": archive_hash,
        "total_frame_count": len(members),
        "start": (len(members) - FRAME_COUNT) // 2,
        "train": 20,
        "heldout_sealed": 4,
    }, indent=2))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=tuple(SCENES), required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    prepare_scene(SCENES[args.scene], args.archive)


if __name__ == "__main__":
    main()
