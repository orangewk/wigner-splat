"""Prepare the hard-locked Round 5 Tanks and Temples scene split."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from PIL import Image
from io import BytesIO

HERE = Path(__file__).resolve().parent
DATA_ROOT = HERE / "data" / "round5"
STAGING_ROOT = HERE / "data" / "round5-staging"
HELDOUT_POSITIONS = frozenset((4, 10, 16, 22))
FRAME_COUNT = 24
EXPECTED_WIDTH = 1920
EXPECTED_HEIGHT = 1080
LICENSE_URL = "https://www.tanksandtemples.org/license/"
DOWNLOAD_PAGE = "https://www.tanksandtemples.org/download/"


@dataclass(frozen=True)
class SceneSpec:
    scene: str
    scene_index: int
    archive_bytes: int
    archive_sha256: str
    drive_id: str
    resource_key: str
    expected_frames: int

    @property
    def source_url(self) -> str:
        return (
            "https://drive.usercontent.google.com/download?"
            f"id={self.drive_id}&export=download&confirm=t&"
            f"resourcekey={self.resource_key}"
        )


SCENES = {
    "Truck": SceneSpec(
        scene="Truck",
        scene_index=1,
        archive_bytes=380_210_369,
        archive_sha256="9ae9ebe88c23f10e02e1abdb2a85f6bd7d4d59fad6b549685f7cbcc872439cc2",
        drive_id="0B-ePgl6HF260NEw3OGN4ckF0dnM",
        resource_key="0-uYzL1Ga_EW1Ck0o-msT7Sg",
        expected_frames=251,
    ),
    "Train": SceneSpec(
        scene="Train",
        scene_index=2,
        archive_bytes=201_581_296,
        archive_sha256="542bb34aa5e83eba8e7f8095b11909f619f5f09349eaea716933a14cd8894367",
        drive_id="0B-ePgl6HF260UFNWeXk3MHhCT00",
        resource_key="0-EbTpTf5_Nyvf0E68VPIJxw",
        expected_frames=301,
    ),
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def selected_indices(total_frame_count: int) -> tuple[int, ...]:
    if total_frame_count < FRAME_COUNT:
        raise RuntimeError(f"Need at least {FRAME_COUNT} source frames")
    stride = total_frame_count // FRAME_COUNT
    return tuple(position * stride for position in range(FRAME_COUNT))


def image_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = []
    for member in archive.infolist():
        path = PurePosixPath(member.filename)
        if member.is_dir() or path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        if path.is_absolute() or ".." in path.parts:
            raise RuntimeError(f"Unsafe archive member: {member.filename}")
        members.append(member)
    members.sort(key=lambda member: member.filename)
    return members


def require_fresh_scene(scene: str) -> tuple[Path, Path]:
    output = DATA_ROOT / scene.lower()
    staging = STAGING_ROOT / scene.lower()
    occupied = [path for path in (output, staging) if path.exists()]
    if occupied:
        raise RuntimeError(f"Refusing to overwrite existing Round 5 data: {occupied}")
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
        "round": 5,
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
            "rule": "source_index = position * floor(total_frame_count / 24)",
            "stride": len(members) // FRAME_COUNT,
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
        "stride": len(members) // FRAME_COUNT,
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
