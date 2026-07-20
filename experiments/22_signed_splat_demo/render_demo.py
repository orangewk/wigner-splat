"""Render Issue #89's three signed-splat expression demos on the CPU."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image

from signed_renderer import (
    apply_signed_field,
    composite,
    load_scene,
    normalize_positions,
    project_orthographic,
    project_perspective,
    rasterize_scene,
    rotate_positions,
    signed_gaussian_field,
)


EFFECTS = ("eraser", "dark-flashlight", "annihilation")
GARDEN_CAMERA = {
    "position": np.array([-3.0089893469, -0.1108648970, -3.7527640949], dtype=np.float32),
    "rotation": np.array(
        [
            [0.8761342012, 0.0692596203, 0.4770659980],
            [-0.0474742184, 0.9972110940, -0.0575867393],
            [-0.4797239415, 0.0278053765, 0.8769787916],
        ],
        dtype=np.float32,
    ),
    "fx": 1159.5880733038,
    "fy": 1164.6601287485,
    "width": 1959,
    "height": 1090,
}


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    x = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


class DemoRenderer:
    def __init__(
        self,
        scene_path: Path,
        width: int,
        height: int,
        yaw: float,
        pitch: float,
        max_splats: int | None,
        camera_preset: str,
    ) -> None:
        self.scene = load_scene(scene_path, max_splats=max_splats)
        if camera_preset == "garden":
            self.xy, self.depth, camera_points = project_perspective(
                self.scene.positions,
                width,
                height,
                camera_position=GARDEN_CAMERA["position"],
                camera_rotation=GARDEN_CAMERA["rotation"],
                fx=GARDEN_CAMERA["fx"],
                fy=GARDEN_CAMERA["fy"],
                source_width=GARDEN_CAMERA["width"],
                source_height=GARDEN_CAMERA["height"],
            )
            visible = (
                (self.depth > 0.2)
                & (self.xy[:, 0] >= 0)
                & (self.xy[:, 0] < width)
                & (self.xy[:, 1] >= 0)
                & (self.xy[:, 1] < height)
            )
            low, high = np.quantile(camera_points[visible], [0.02, 0.98], axis=0)
            self.center = (low + high) / 2.0
            self.scene_radius = float(max(high[0] - low[0], high[1] - low[1]) / 2.0)
            self.points = ((camera_points - self.center) / self.scene_radius).astype(np.float32)
        else:
            normalized, self.center, self.scene_radius = normalize_positions(self.scene.positions)
            self.points = rotate_positions(normalized, yaw, pitch)
            self.xy, self.depth = project_orthographic(self.points, width, height)
        self.width, self.height = width, height
        self.point_radius = max(1, round(height / 420))
        yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None, None]
        top = np.array([0.055, 0.070, 0.095], dtype=np.float32).reshape(1, 1, 3)
        bottom = np.array([0.16, 0.18, 0.20], dtype=np.float32).reshape(1, 1, 3)
        self.background = np.broadcast_to(top * (1.0 - yy) + bottom * yy, (height, width, 3)).copy()
        self.base_rgb, self.base_alpha = rasterize_scene(
            self.xy,
            self.depth,
            self.scene.colors,
            self.scene.opacities,
            width,
            height,
            point_radius=self.point_radius,
        )
        self.base = composite(self.base_rgb, self.base_alpha, self.background)

    def render(self, effect: str, progress: float) -> np.ndarray:
        progress = float(np.clip(progress, 0.0, 1.0))
        if effect == "eraser":
            return self._eraser(progress)
        if effect == "dark-flashlight":
            return self._dark_flashlight(progress)
        if effect == "annihilation":
            return self._annihilation(progress)
        raise ValueError(f"unknown effect {effect!r}")

    def _eraser(self, progress: float) -> np.ndarray:
        # A genuine 3D sphere: matched negative copies cancel positive source
        # splats inside it.  Its center sits in the near half of the scan, so
        # farther measured splats remain available behind the erased surface.
        center = np.array([-1.35 + 2.70 * progress, 0.05, -0.28], dtype=np.float32)
        distance = np.linalg.norm(self.points - center, axis=1)
        cancellation = 1.0 - smoothstep(0.28, 0.40, distance)
        keep = cancellation < 0.985
        rgb, alpha = rasterize_scene(
            self.xy,
            self.depth,
            self.scene.colors,
            self.scene.opacities * (1.0 - cancellation),
            self.width,
            self.height,
            point_radius=self.point_radius,
            keep=keep,
        )
        return composite(rgb, alpha, self.background)

    def _dark_flashlight(self, progress: float) -> np.ndarray:
        # Fill a swept beam with low-amplitude negative Gaussian particles.
        phase = 2.0 * np.pi * progress
        origin = np.array([0.23 * self.width, 0.74 * self.height], dtype=np.float32)
        angle = -0.80 + 0.34 * np.sin(phase)
        direction = np.array([np.cos(angle), np.sin(angle)], dtype=np.float32)
        normal = np.array([-direction[1], direction[0]], dtype=np.float32)
        axial = np.linspace(0.05, 0.92, 44, dtype=np.float32)
        centers, sigmas = [], []
        for i, along in enumerate(axial):
            spread = (0.010 + 0.095 * along) * self.height
            offset = spread * 0.42 * np.sin(i * 2.399963)
            centers.append(origin + direction * along * self.width * 0.92 + normal * offset)
            sigmas.append(max(2.0, spread * 0.38))
        field = signed_gaussian_field(
            self.width,
            self.height,
            np.asarray(centers),
            np.asarray(sigmas),
            np.full(len(centers), -0.12, dtype=np.float32),
        )
        image = apply_signed_field(self.base, np.clip(field, -0.82, 0.0), np.array([0.95, 0.90, 1.0]))
        yy, xx = np.ogrid[: self.height, : self.width]
        orb = (xx - origin[0]) ** 2 + (yy - origin[1]) ** 2 <= (0.055 * self.height) ** 2
        image[orb] *= 0.05
        return image

    def _annihilation(self, progress: float) -> np.ndarray:
        # A compact central object receives an identical negative copy.  The
        # copy approaches from the right and exactly cancels at contact.
        object_mask = (self.points[:, 0] / 0.58) ** 2 + (self.points[:, 1] / 0.72) ** 2 < 1.0
        strength = smoothstep(0.55, 0.98, np.asarray(progress)).item()
        positive_opacity = self.scene.opacities.copy()
        positive_opacity[object_mask] *= 1.0 - strength
        positive_rgb, positive_alpha = rasterize_scene(
            self.xy,
            self.depth,
            self.scene.colors,
            positive_opacity,
            self.width,
            self.height,
            point_radius=self.point_radius,
        )
        image = composite(positive_rgb, positive_alpha, self.background)

        if progress < 0.99:
            shifted = self.xy[object_mask].copy()
            shifted[:, 0] += (1.35 * (1.0 - progress)) * 0.46 * min(self.width, self.height)
            ghost_rgb, ghost_alpha = rasterize_scene(
                shifted,
                self.depth[object_mask] - 0.01,
                self.scene.colors[object_mask],
                self.scene.opacities[object_mask] * (0.42 + 0.58 * progress),
                self.width,
                self.height,
                point_radius=self.point_radius,
            )
            signed = -0.70 * ghost_alpha
            image = apply_signed_field(image, signed, np.clip(ghost_rgb * 0.55 + 0.45, 0.0, 1.0))
        return image


def frame_progress(index: int, frame_count: int) -> float:
    if frame_count <= 1:
        return 0.5
    return index / (frame_count - 1)


def write_video(path: Path, renderer: DemoRenderer, effect: str, fps: int, seconds: float) -> dict:
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
            frame = renderer.render(effect, frame_progress(index, frame_count))
            process.stdin.write(np.asarray(frame * 255.0, dtype=np.uint8).tobytes())
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code:
        raise RuntimeError(f"ffmpeg exited with code {return_code}")
    return {"frames": frame_count, "seconds": seconds, "fps": fps, "wall_seconds": time.perf_counter() - started}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--effect", choices=EFFECTS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--width", type=int, default=1296)
    parser.add_argument("--height", type=int, default=840)
    parser.add_argument("--fps", type=int, default=15)
    parser.add_argument("--seconds", type=float, default=8.0)
    parser.add_argument("--yaw", type=float, default=0.0)
    parser.add_argument("--pitch", type=float, default=0.0)
    parser.add_argument("--max-splats", type=int, default=None)
    parser.add_argument("--camera-preset", choices=("auto", "garden"), default="auto")
    parser.add_argument("--preview-progress", type=float, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing to overwrite {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    renderer = DemoRenderer(
        args.scene,
        args.width,
        args.height,
        args.yaw,
        args.pitch,
        args.max_splats,
        args.camera_preset,
    )
    metadata = {
        "scene": str(args.scene.resolve()),
        "source_bytes": args.scene.stat().st_size,
        "loaded_splats": len(renderer.scene.positions),
        "effect": args.effect,
        "width": args.width,
        "height": args.height,
        "yaw": args.yaw,
        "pitch": args.pitch,
        "camera_preset": args.camera_preset,
        "renderer": "signed CPU post-process; nearest-surface screen footprint",
    }
    if args.preview_progress is not None:
        frame = renderer.render(args.effect, args.preview_progress)
        Image.fromarray(np.asarray(frame * 255.0, dtype=np.uint8), mode="RGB").save(args.output)
        metadata["preview_progress"] = args.preview_progress
    else:
        metadata.update(write_video(args.output, renderer, args.effect, args.fps, args.seconds))
    metadata_path = args.output.with_suffix(args.output.suffix + ".json")
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
