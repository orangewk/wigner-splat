"""Extract the predeclared 24 full-resolution RGB frames without split leakage."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


SRC_INDICES = (30, 38, 45, 52, 60, 68, 75, 82, 90, 98, 105, 112,
               120, 128, 135, 142, 150, 158, 165, 172, 180, 188, 195, 202)
HELD_OUT_POSITIONS = frozenset((4, 10, 16, 22))
EXPECTED_VIDEO_SHA256 = (
    "4483e8983295e559774cdb76fc43f963cfab358307161eaa390ab5f2b31f7b9e"
)
EXPECTED_WIDTH = 1920
EXPECTED_HEIGHT = 1080
EXPECTED_FPS = 30.0

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
STAGING = DATA / "staging"
TRAIN = DATA / "train"
HELD_OUT = DATA / "heldout-sealed"
MANIFEST = DATA / "manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def probe(video: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=codec_name,width,height,pix_fmt,r_frame_rate",
        "-show_entries", "format=duration", "-of", "json", str(video),
    ]
    return json.loads(subprocess.check_output(command, text=True))


def validate_probe(metadata: dict) -> None:
    stream = metadata["streams"][0]
    numerator, denominator = map(int, stream["r_frame_rate"].split("/"))
    fps = numerator / denominator
    observed = (stream["width"], stream["height"], fps)
    expected = (EXPECTED_WIDTH, EXPECTED_HEIGHT, EXPECTED_FPS)
    if observed != expected:
        raise RuntimeError(f"Unexpected video geometry/fps: {observed} != {expected}")


def require_fresh_outputs() -> None:
    occupied = [path for path in (STAGING, TRAIN, HELD_OUT, MANIFEST)
                if path.exists()]
    if occupied:
        rendered = ", ".join(str(path) for path in occupied)
        raise RuntimeError(f"Refusing to overwrite existing outputs: {rendered}")


def extract(video: Path) -> list[Path]:
    STAGING.mkdir(parents=True)
    selector = "+".join(f"eq(n\\,{index})" for index in SRC_INDICES)
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
        "-map", "0:v:0", "-vf", f"select={selector}", "-fps_mode", "passthrough",
        "-frames:v", str(len(SRC_INDICES)), "-pix_fmt", "rgb24",
        "-compression_level", "3", "-start_number", "0",
        str(STAGING / "frame_%02d.png"),
    ]
    subprocess.run(command, check=True)
    frames = sorted(STAGING.glob("frame_*.png"))
    if len(frames) != len(SRC_INDICES):
        raise RuntimeError(f"Expected {len(SRC_INDICES)} frames, got {len(frames)}")
    return frames


def partition(frames: list[Path]) -> list[dict]:
    TRAIN.mkdir()
    HELD_OUT.mkdir()
    entries = []
    for position, (staged, source_index) in enumerate(zip(frames, SRC_INDICES)):
        split = "heldout-sealed" if position in HELD_OUT_POSITIONS else "train"
        target_dir = HELD_OUT if position in HELD_OUT_POSITIONS else TRAIN
        filename = f"frame_{position:02d}_src_{source_index:04d}.png"
        target = target_dir / filename
        staged.rename(target)
        entries.append({
            "position": position,
            "source_frame_index": source_index,
            "timestamp_seconds": source_index / EXPECTED_FPS,
            "split": split,
            "relative_path": target.relative_to(HERE).as_posix(),
            "sha256": sha256(target),
            "bytes": target.stat().st_size,
        })
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    args = parser.parse_args()
    video = args.video.resolve()
    if not video.is_file():
        raise FileNotFoundError(video)
    require_fresh_outputs()
    video_hash = sha256(video)
    if video_hash != EXPECTED_VIDEO_SHA256:
        raise RuntimeError(
            f"Unexpected video SHA-256: {video_hash} != {EXPECTED_VIDEO_SHA256}"
        )
    metadata = probe(video)
    validate_probe(metadata)
    entries = partition(extract(video))
    train_count = sum(entry["split"] == "train" for entry in entries)
    heldout_count = sum(entry["split"] == "heldout-sealed" for entry in entries)
    if (train_count, heldout_count) != (20, 4):
        raise RuntimeError((train_count, heldout_count))
    manifest = {
        "schema_version": 1,
        "source_video": {
            "basename": video.name,
            "sha256": video_hash,
            "bytes": video.stat().st_size,
            "probe": metadata,
        },
        "extraction": {
            "ffmpeg_executable": Path(shutil.which("ffmpeg") or "ffmpeg").name,
            "ffmpeg_version": subprocess.check_output(
                ["ffmpeg", "-version"], text=True
            ).splitlines()[0],
            "pixel_format": "rgb24",
            "container": "png",
            "lossless": True,
            "source_indices_inherited_from": "experiments/16_real_video/data/carousel_frames.npz",
        },
        "held_out_positions": sorted(HELD_OUT_POSITIONS),
        "frames": entries,
    }
    DATA.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST}")
    print(f"train={train_count}, heldout-sealed={heldout_count}")


if __name__ == "__main__":
    main()
