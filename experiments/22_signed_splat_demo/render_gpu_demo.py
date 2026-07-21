"""Render Issue #89's three high-fidelity signed-splat demos on CUDA."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image

from gpu_renderer import GpuDemoRenderer


EFFECTS = ("eraser", "dark-flashlight", "annihilation")


def frame_progress(index: int, frame_count: int) -> float:
    if frame_count <= 1:
        return 0.5
    return index / (frame_count - 1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_video(
    path: Path,
    renderer: GpuDemoRenderer,
    effect: str,
    fps: int,
    seconds: float,
    camera_motion: str,
) -> dict:
    frame_count = max(1, round(fps * seconds))
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "rawvideo",
        "-pixel_format",
        "rgb24",
        "-video_size",
        f"{renderer.width}x{renderer.height}",
        "-framerate",
        str(fps),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        str(path),
    ]
    started = time.perf_counter()
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for index in range(frame_count):
            frame = renderer.render(
                effect, frame_progress(index, frame_count), camera_motion=camera_motion
            )
            process.stdin.write(np.asarray(frame * 255.0, dtype=np.uint8).tobytes())
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code:
        raise RuntimeError(f"ffmpeg exited with code {return_code}")
    return {
        "frames": frame_count,
        "seconds": seconds,
        "fps": fps,
        "wall_seconds": round(time.perf_counter() - started, 3),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--effect", choices=EFFECTS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--height", type=int, default=960)
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument("--seconds", type=float, default=8.0)
    parser.add_argument("--camera-motion", choices=("fixed", "orbit"), default="fixed")
    parser.add_argument("--preview-progress", type=float, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    renderer = GpuDemoRenderer(args.scene, args.width, args.height)
    metadata = {
        "scene": str(args.scene.resolve()),
        "source_bytes": args.scene.stat().st_size,
        "source_sha256": sha256(args.scene),
        "loaded_splats": len(renderer.scene.means),
        "effect": args.effect,
        "camera_motion": args.camera_motion,
        "width": args.width,
        "height": args.height,
        "renderer": "gsplat CUDA; anisotropic covariance; SH degree 3; antialiased",
        "device": renderer.torch.cuda.get_device_name(),
    }
    if args.preview_progress is not None:
        frame = renderer.render(
            args.effect, args.preview_progress, camera_motion=args.camera_motion
        )
        Image.fromarray(np.asarray(frame * 255.0, dtype=np.uint8), mode="RGB").save(args.output)
        metadata["preview_progress"] = args.preview_progress
    else:
        metadata.update(
            write_video(
                args.output,
                renderer,
                args.effect,
                args.fps,
                args.seconds,
                args.camera_motion,
            )
        )
    metadata["output_bytes"] = args.output.stat().st_size
    metadata["output_sha256"] = sha256(args.output)
    metadata_path = args.output.with_suffix(args.output.suffix + ".json")
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
