"""Small CPU renderer for signed Gaussian-splat expression demos.

This is deliberately a post-processing renderer, not a trainer.  Positive
scene splats and procedural negative fields are kept separate until the final
signed composition so the cancellation mechanism stays inspectable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


SPLAT_RECORD_BYTES = 32


@dataclass(frozen=True)
class Scene:
    positions: np.ndarray
    colors: np.ndarray
    opacities: np.ndarray
    scales: np.ndarray
    source: Path


def load_scene(path: str | Path, *, max_splats: int | None = None) -> Scene:
    """Load the common 32-byte .splat layout or gsplat's test .npz layout."""
    source = Path(path)
    if source.suffix.lower() == ".npz":
        with np.load(source) as data:
            positions = np.asarray(data["means3d"], dtype=np.float32)
            colors = np.asarray(data["colors"], dtype=np.float32) / 255.0
            scales = np.asarray(
                data["scales"] if "scales" in data else np.full_like(positions, 0.01),
                dtype=np.float32,
            )
            opacities = np.asarray(
                data["opacities"] if "opacities" in data else np.full(len(positions), 0.92),
                dtype=np.float32,
            ).reshape(-1)
    elif source.suffix.lower() == ".splat":
        size = source.stat().st_size
        if size % SPLAT_RECORD_BYTES:
            raise ValueError(f"{source} is not a 32-byte-record .splat file")
        dtype = np.dtype(
            [
                ("position", "<f4", (3,)),
                ("scale", "<f4", (3,)),
                ("rgba", "u1", (4,)),
                ("rotation", "u1", (4,)),
            ]
        )
        records = np.memmap(source, mode="r", dtype=dtype)
        positions = np.asarray(records["position"], dtype=np.float32)
        scales = np.asarray(records["scale"], dtype=np.float32)
        rgba = np.asarray(records["rgba"], dtype=np.float32) / 255.0
        colors = rgba[:, :3]
        opacities = rgba[:, 3]
    else:
        raise ValueError(f"unsupported scene format: {source.suffix}")

    finite = np.isfinite(positions).all(axis=1) & np.isfinite(scales).all(axis=1)
    finite &= np.isfinite(colors).all(axis=1) & np.isfinite(opacities)
    positions, scales = positions[finite], scales[finite]
    colors, opacities = colors[finite], opacities[finite]
    if not len(positions):
        raise ValueError(f"{source} contains no finite splats")

    if max_splats is not None and len(positions) > max_splats:
        # Stable spatially uniform thinning.  Avoid a random sample so the same
        # command produces the same frames on every machine.
        keep = np.linspace(0, len(positions) - 1, max_splats, dtype=np.int64)
        positions, scales = positions[keep], scales[keep]
        colors, opacities = colors[keep], opacities[keep]

    return Scene(
        positions=np.ascontiguousarray(positions),
        colors=np.clip(np.ascontiguousarray(colors), 0.0, 1.0),
        opacities=np.clip(np.ascontiguousarray(opacities), 0.0, 1.0),
        scales=np.abs(np.ascontiguousarray(scales)),
        source=source,
    )


def normalize_positions(positions: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Robustly center a scene and fit its central 99% into a unit cube."""
    low, high = np.quantile(positions, [0.005, 0.995], axis=0)
    center = (low + high) / 2.0
    radius = float(np.max(high - low) / 2.0)
    if not np.isfinite(radius) or radius <= 0:
        raise ValueError("scene has zero or invalid spatial extent")
    return ((positions - center) / radius).astype(np.float32), center, radius


def rotate_positions(points: np.ndarray, yaw_degrees: float, pitch_degrees: float) -> np.ndarray:
    yaw, pitch = np.deg2rad([yaw_degrees, pitch_degrees])
    cy, sy = np.cos(yaw), np.sin(yaw)
    cx, sx = np.cos(pitch), np.sin(pitch)
    yaw_matrix = np.array([[cy, 0.0, sy], [0.0, 1.0, 0.0], [-sy, 0.0, cy]])
    pitch_matrix = np.array([[1.0, 0.0, 0.0], [0.0, cx, -sx], [0.0, sx, cx]])
    return (points @ (pitch_matrix @ yaw_matrix).T).astype(np.float32)


def project_orthographic(points: np.ndarray, width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    """Project normalized points, returning float pixel xy and sortable depth."""
    scale = 0.46 * min(width, height)
    xy = np.empty((len(points), 2), dtype=np.float32)
    xy[:, 0] = width / 2.0 + points[:, 0] * scale
    xy[:, 1] = height / 2.0 - points[:, 1] * scale
    return xy, (points[:, 2] + 2.0).astype(np.float32)


def project_perspective(
    points: np.ndarray,
    width: int,
    height: int,
    *,
    camera_position: np.ndarray,
    camera_rotation: np.ndarray,
    fx: float,
    fy: float,
    source_width: int,
    source_height: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Project world points with the camera convention used by cakewalk/splat."""
    camera_points = (points - camera_position) @ camera_rotation
    depth = camera_points[:, 2]
    safe_depth = np.where(np.abs(depth) > 1e-8, depth, np.nan)
    xy = np.empty((len(points), 2), dtype=np.float32)
    xy[:, 0] = width / 2.0 + (fx * width / source_width) * camera_points[:, 0] / safe_depth
    xy[:, 1] = height / 2.0 + (fy * height / source_height) * camera_points[:, 1] / safe_depth
    return xy, depth.astype(np.float32), camera_points.astype(np.float32)


def rasterize_scene(
    xy: np.ndarray,
    depth: np.ndarray,
    colors: np.ndarray,
    opacities: np.ndarray,
    width: int,
    height: int,
    *,
    point_radius: int,
    keep: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic nearest-surface CPU splat rasterization.

    Each projected point covers a small circular footprint.  This is a compact
    viewer-grade approximation: scale and quaternion are loaded for provenance,
    while rendering uses a screen-space footprint to keep CPU demo runs bounded.
    """
    if keep is None:
        keep = np.ones(len(xy), dtype=bool)
    keep = keep & np.isfinite(xy).all(axis=1) & np.isfinite(depth) & (depth > 0.2)
    order = np.flatnonzero(keep & (opacities > 0.01))
    order = order[np.argsort(depth[order], kind="stable")][::-1]  # far -> near
    px = np.rint(xy[order, 0]).astype(np.int32)
    py = np.rint(xy[order, 1]).astype(np.int32)
    z = depth[order]
    color = colors[order]
    alpha = opacities[order]

    depth_buffer = np.full(width * height, np.inf, dtype=np.float32)
    color_buffer = np.zeros((width * height, 3), dtype=np.float32)
    alpha_buffer = np.zeros(width * height, dtype=np.float32)
    offsets = [
        (dx, dy)
        for dy in range(-point_radius, point_radius + 1)
        for dx in range(-point_radius, point_radius + 1)
        if dx * dx + dy * dy <= point_radius * point_radius
    ]
    for dx, dy in offsets:
        x, y = px + dx, py + dy
        valid = (x >= 0) & (x < width) & (y >= 0) & (y < height)
        flat = y[valid] * width + x[valid]
        zv = z[valid]
        nearer = zv < depth_buffer[flat]
        flat = flat[nearer]
        source_index = np.flatnonzero(valid)[nearer]
        # order is far -> near; repeated pixel indices therefore end with the
        # nearest candidate under NumPy's deterministic indexed assignment.
        depth_buffer[flat] = zv[nearer]
        color_buffer[flat] = color[source_index]
        alpha_buffer[flat] = alpha[source_index]

    return color_buffer.reshape(height, width, 3), alpha_buffer.reshape(height, width)


def composite(rgb: np.ndarray, alpha: np.ndarray, background: np.ndarray) -> np.ndarray:
    return rgb * alpha[..., None] + background * (1.0 - alpha[..., None])


def signed_gaussian_field(
    width: int,
    height: int,
    centers: np.ndarray,
    sigmas: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    """Rasterize signed 2D Gaussian contributions into a scalar field."""
    field = np.zeros((height, width), dtype=np.float32)
    for (cx, cy), sigma, weight in zip(centers, sigmas, weights, strict=True):
        radius = max(1, int(np.ceil(3.0 * sigma)))
        x0, x1 = max(0, int(cx) - radius), min(width, int(cx) + radius + 1)
        y0, y1 = max(0, int(cy) - radius), min(height, int(cy) + radius + 1)
        if x0 >= x1 or y0 >= y1:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1]
        gaussian = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2.0 * sigma**2))
        field[y0:y1, x0:x1] += float(weight) * gaussian.astype(np.float32)
    return field


def apply_signed_field(image: np.ndarray, field: np.ndarray, tint: np.ndarray) -> np.ndarray:
    """Apply a signed field; negative values remove radiance from the image."""
    tint = np.asarray(tint, dtype=np.float32)
    if tint.shape == (3,):
        tint = tint.reshape(1, 1, 3)
    elif tint.shape != image.shape:
        raise ValueError("tint must be RGB or match the image shape")
    return np.clip(image + field[..., None] * tint, 0.0, 1.0)
