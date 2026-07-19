"""Extract the hard-locked Round 4 fresh held-out frames losslessly."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROUND3_PREPARE = HERE / "prepare_data.py"
SOURCE_INDICES = (216, 244, 272, 300)
OUTPUT = HERE / "data" / "heldout2-sealed"
STAGING = HERE / "data" / "round4-staging"
MANIFEST = HERE / "data" / "round4_manifest.json"


def _load_round3_prepare():
    spec = importlib.util.spec_from_file_location("round3_prepare", ROUND3_PREPARE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def frame_name(source_index: int) -> str:
    return f"round4_src_{source_index:04d}.png"


def require_fresh_outputs() -> None:
    occupied = [path for path in (OUTPUT, STAGING, MANIFEST) if path.exists()]
    if occupied:
        raise RuntimeError(
            "Refusing to overwrite Round 4 outputs: "
            + ", ".join(str(path) for path in occupied)
        )


def extract(video: Path) -> list[Path]:
    STAGING.mkdir(parents=True)
    selector = "+".join(f"eq(n\\,{index})" for index in SOURCE_INDICES)
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
            "-map", "0:v:0", "-vf", f"select={selector}",
            "-fps_mode", "passthrough", "-frames:v", str(len(SOURCE_INDICES)),
            "-pix_fmt", "rgb24", "-compression_level", "3", "-start_number", "0",
            str(STAGING / "frame_%02d.png"),
        ],
        check=True,
    )
    frames = sorted(STAGING.glob("frame_*.png"))
    if len(frames) != len(SOURCE_INDICES):
        raise RuntimeError(f"Expected 4 fresh frames, got {len(frames)}")
    return frames


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    args = parser.parse_args()
    video = args.video.resolve()
    if not video.is_file():
        raise FileNotFoundError(video)
    require_fresh_outputs()

    round3 = _load_round3_prepare()
    video_hash = round3.sha256(video)
    if video_hash != round3.EXPECTED_VIDEO_SHA256:
        raise RuntimeError("Round 4 source video hash differs from the pinned original")
    metadata = round3.probe(video)
    round3.validate_probe(metadata)

    frames = extract(video)
    OUTPUT.mkdir()
    entries = []
    for staged, source_index in zip(frames, SOURCE_INDICES):
        target = OUTPUT / frame_name(source_index)
        staged.rename(target)
        entries.append({
            "source_frame_index": source_index,
            "timestamp_seconds": source_index / round3.EXPECTED_FPS,
            "relative_path": target.relative_to(HERE).as_posix(),
            "sha256": round3.sha256(target),
            "bytes": target.stat().st_size,
        })
    manifest = {
        "schema_version": 1,
        "round": 4,
        "status": "sealed",
        "source_video": {
            "basename": video.name,
            "sha256": video_hash,
            "bytes": video.stat().st_size,
            "probe": metadata,
        },
        "source_indices": list(SOURCE_INDICES),
        "lossless_rgb_png": True,
        "ffmpeg_version": subprocess.check_output(
            ["ffmpeg", "-version"], text=True
        ).splitlines()[0],
        "frames": entries,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"sealed {len(entries)} Round 4 frames -> {OUTPUT}")


if __name__ == "__main__":
    main()
