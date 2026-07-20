"""High-fidelity GPU renderer for the signed-splat expression demo.

The loader stays dependency-light so PLY handling is testable on CPU-only CI.
PyTorch and gsplat are imported only when :class:`GpuDemoRenderer` is created.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from signed_renderer import apply_signed_field, signed_gaussian_field


@dataclass(frozen=True)
class GaussianScene:
    means: np.ndarray
    quaternions: np.ndarray
    scales: np.ndarray
    opacities: np.ndarray
    sh_coefficients: np.ndarray
    source: Path


def _sigmoid(values: np.ndarray) -> np.ndarray:
    positive = values >= 0
    result = np.empty_like(values, dtype=np.float32)
    result[positive] = 1.0 / (1.0 + np.exp(-values[positive]))
    exponential = np.exp(values[~positive])
    result[~positive] = exponential / (1.0 + exponential)
    return result


def load_gaussian_ply(path: str | Path) -> GaussianScene:
    """Load a binary little-endian INRIA/Postshot Gaussian PLY.

    The expected payload contains position, SH degree-3 coefficients, opacity
    logits, log scales, and WXYZ quaternions.  This is the full trained model,
    not a sparse initialization point cloud.
    """
    source = Path(path)
    with source.open("rb") as stream:
        header = bytearray()
        while not header.endswith(b"end_header\n"):
            byte = stream.read(1)
            if not byte:
                raise ValueError(f"{source} has an incomplete PLY header")
            header.extend(byte)
            if len(header) > 64 * 1024:
                raise ValueError(f"{source} has an unexpectedly large PLY header")
        data_offset = stream.tell()

    lines = header.decode("ascii").splitlines()
    if "format binary_little_endian 1.0" not in lines:
        raise ValueError(f"{source} is not a binary little-endian PLY")
    vertex_lines = [line for line in lines if line.startswith("element vertex ")]
    if len(vertex_lines) != 1:
        raise ValueError(f"{source} must define exactly one vertex element")
    count = int(vertex_lines[0].split()[2])
    properties = [line.split()[2] for line in lines if line.startswith("property float ")]
    required = {
        "x",
        "y",
        "z",
        "opacity",
        *(f"f_dc_{index}" for index in range(3)),
        *(f"f_rest_{index}" for index in range(45)),
        *(f"scale_{index}" for index in range(3)),
        *(f"rot_{index}" for index in range(4)),
    }
    missing = sorted(required.difference(properties))
    if missing:
        raise ValueError(f"{source} is missing Gaussian properties: {', '.join(missing)}")

    dtype = np.dtype([(name, "<f4") for name in properties])
    expected_bytes = data_offset + count * dtype.itemsize
    if source.stat().st_size < expected_bytes:
        raise ValueError(f"{source} ends before its declared vertex payload")
    vertices = np.memmap(source, dtype=dtype, mode="r", offset=data_offset, shape=(count,))

    def columns(names: list[str]) -> np.ndarray:
        return np.stack([vertices[name] for name in names], axis=-1).astype(np.float32, copy=False)

    means = columns(["x", "y", "z"])
    quaternions = columns([f"rot_{index}" for index in range(4)])
    scales = np.exp(columns([f"scale_{index}" for index in range(3)]))
    opacities = _sigmoid(np.asarray(vertices["opacity"], dtype=np.float32))
    dc = columns([f"f_dc_{index}" for index in range(3)])[:, None, :]
    rest = columns([f"f_rest_{index}" for index in range(45)]).reshape(count, 3, 15)
    sh_coefficients = np.concatenate([dc, rest.transpose(0, 2, 1)], axis=1)

    finite = np.isfinite(means).all(axis=1)
    finite &= np.isfinite(quaternions).all(axis=1) & np.isfinite(scales).all(axis=1)
    finite &= np.isfinite(opacities) & np.isfinite(sh_coefficients).all(axis=(1, 2))
    if not finite.any():
        raise ValueError(f"{source} contains no finite Gaussian splats")
    if not finite.all():
        means, quaternions, scales = means[finite], quaternions[finite], scales[finite]
        opacities, sh_coefficients = opacities[finite], sh_coefficients[finite]

    return GaussianScene(
        means=np.ascontiguousarray(means),
        quaternions=np.ascontiguousarray(quaternions),
        scales=np.ascontiguousarray(scales),
        opacities=np.ascontiguousarray(opacities),
        sh_coefficients=np.ascontiguousarray(sh_coefficients),
        source=source,
    )


def robust_bounds(means: np.ndarray, opacities: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    visible = opacities > 0.05
    if not visible.any():
        visible = np.ones(len(means), dtype=bool)
    low, high = np.quantile(means[visible], [0.01, 0.99], axis=0)
    if not np.isfinite(low).all() or not np.isfinite(high).all() or np.any(high <= low):
        raise ValueError("scene has invalid robust bounds")
    return low.astype(np.float32), high.astype(np.float32)


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Build an OpenCV world-to-camera matrix for gsplat."""
    forward = np.asarray(target - eye, dtype=np.float32)
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, up)
    right /= np.linalg.norm(right)
    down = np.cross(forward, right)
    rotation = np.stack([right, down, forward], axis=0)
    view = np.eye(4, dtype=np.float32)
    view[:3, :3] = rotation
    view[:3, 3] = -rotation @ eye
    return view


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    x = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


class GpuDemoRenderer:
    """Render full anisotropic Gaussian splats and three signed effects."""

    def __init__(self, scene_path: Path, width: int, height: int) -> None:
        import torch
        from gsplat.rendering import rasterization

        if not torch.cuda.is_available():
            raise RuntimeError("the high-fidelity renderer requires a CUDA GPU")
        self.torch = torch
        self.rasterization = rasterization
        self.scene = load_gaussian_ply(scene_path)
        self.width, self.height = width, height
        self.low, self.high = robust_bounds(self.scene.means, self.scene.opacities)
        self.center = (self.low + self.high) * 0.5
        self.extent = self.high - self.low

        target = self.center.copy()
        target[1] -= 0.10 * self.extent[1]
        radius = float(np.linalg.norm(self.extent) * 0.5)
        eye = target + np.array([0.0, 0.0, -2.20 * radius], dtype=np.float32)
        view = look_at(eye, target, np.array([0.0, -1.0, 0.0], dtype=np.float32))
        focal = min(width, height) / (2.0 * np.tan(np.deg2rad(42.0) * 0.5))
        intrinsic = np.array(
            [[focal, 0.0, width / 2.0], [0.0, focal, height / 2.0], [0.0, 0.0, 1.0]],
            dtype=np.float32,
        )

        device = torch.device("cuda")
        self.means = torch.from_numpy(self.scene.means).to(device)
        self.quaternions = torch.from_numpy(self.scene.quaternions).to(device)
        self.scales = torch.from_numpy(self.scene.scales).to(device)
        self.opacities = torch.from_numpy(self.scene.opacities).to(device)
        self.colors = torch.from_numpy(self.scene.sh_coefficients).to(device)
        self.view = torch.from_numpy(view)[None].to(device)
        self.intrinsic = torch.from_numpy(intrinsic)[None].to(device)

        yy = np.linspace(0.0, 1.0, height, dtype=np.float32)[:, None, None]
        top = np.array([0.004, 0.006, 0.010], dtype=np.float32).reshape(1, 1, 3)
        bottom = np.array([0.035, 0.025, 0.020], dtype=np.float32).reshape(1, 1, 3)
        self.background = np.broadcast_to(top * (1.0 - yy) + bottom * yy, (height, width, 3)).copy()
        self._base: np.ndarray | None = None

    def _rasterize(self, *, means=None, opacities=None, colors=None) -> tuple[np.ndarray, np.ndarray]:
        torch = self.torch
        rendered, alpha, _ = self.rasterization(
            means=self.means if means is None else means,
            quats=self.quaternions,
            scales=self.scales,
            opacities=self.opacities if opacities is None else opacities,
            colors=self.colors if colors is None else colors,
            viewmats=self.view,
            Ks=self.intrinsic,
            width=self.width,
            height=self.height,
            near_plane=0.01,
            far_plane=1e4,
            sh_degree=3,
            packed=True,
            backgrounds=torch.zeros((1, 3), device=self.means.device),
            rasterize_mode="antialiased",
        )
        rgb = rendered[0].clamp(0.0, 1.0).detach().cpu().numpy()
        opacity = alpha[0, ..., 0].clamp(0.0, 1.0).detach().cpu().numpy()
        return rgb + self.background * (1.0 - opacity[..., None]), opacity

    @property
    def base(self) -> np.ndarray:
        if self._base is None:
            self._base, _ = self._rasterize()
        return self._base

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
        torch = self.torch
        center = torch.tensor(
            [
                self.low[0] - 0.10 * self.extent[0] + progress * 1.20 * self.extent[0],
                self.center[1] - 0.20 * self.extent[1],
                self.low[2] + 0.18 * self.extent[2],
            ],
            dtype=torch.float32,
            device=self.means.device,
        )
        radius = float(0.28 * min(self.extent[0], self.extent[2]))
        distance = torch.linalg.vector_norm(self.means - center, dim=1)
        x = ((distance - 0.72 * radius) / (0.28 * radius)).clamp(0.0, 1.0)
        keep = x * x * (3.0 - 2.0 * x)
        image, _ = self._rasterize(opacities=self.opacities * keep)
        return image

    def _dark_flashlight(self, progress: float) -> np.ndarray:
        phase = 2.0 * np.pi * progress
        origin = np.array([0.18 * self.width, 0.82 * self.height], dtype=np.float32)
        angle = -0.90 + 0.46 * np.sin(phase)
        direction = np.array([np.cos(angle), np.sin(angle)], dtype=np.float32)
        normal = np.array([-direction[1], direction[0]], dtype=np.float32)
        axial = np.linspace(0.04, 1.0, 52, dtype=np.float32)
        centers, sigmas = [], []
        for index, along in enumerate(axial):
            spread = (0.010 + 0.105 * along) * self.height
            offset = spread * 0.40 * np.sin(index * 2.399963)
            centers.append(origin + direction * along * self.width * 1.05 + normal * offset)
            sigmas.append(max(2.0, spread * 0.36))
        field = signed_gaussian_field(
            self.width,
            self.height,
            np.asarray(centers),
            np.asarray(sigmas),
            np.full(len(centers), -0.115, dtype=np.float32),
        )
        image = apply_signed_field(
            self.base,
            np.clip(field, -0.88, 0.0),
            np.array([0.92, 0.88, 1.0], dtype=np.float32),
        )
        yy, xx = np.ogrid[: self.height, : self.width]
        orb = (xx - origin[0]) ** 2 + (yy - origin[1]) ** 2 <= (0.045 * self.height) ** 2
        image[orb] *= 0.04
        return image

    def _annihilation(self, progress: float) -> np.ndarray:
        torch = self.torch
        object_mask = self.means[:, 1] < float(self.center[1] - 0.02 * self.extent[1])
        object_mask &= torch.abs(self.means[:, 0] - float(self.center[0])) < float(0.60 * self.extent[0])
        strength = float(smoothstep(0.58, 0.98, np.asarray(progress)))
        positive_opacity = self.opacities.clone()
        positive_opacity[object_mask] *= 1.0 - strength
        image, _ = self._rasterize(opacities=positive_opacity)

        if progress < 0.99:
            shift = float(1.05 * self.extent[0] * (1.0 - progress))
            ghost_means = self.means[object_mask].clone()
            ghost_means[:, 0] += shift
            ghost_rgb, ghost_alpha = self._rasterize_subset(ghost_means, object_mask)
            image = np.clip(image - 0.72 * ghost_rgb, 0.0, 1.0)
            image += ghost_alpha[..., None] * np.array([0.025, 0.040, 0.060], dtype=np.float32)
        return np.clip(image, 0.0, 1.0)

    def _rasterize_subset(self, means, mask) -> tuple[np.ndarray, np.ndarray]:
        torch = self.torch
        rendered, alpha, _ = self.rasterization(
            means=means,
            quats=self.quaternions[mask],
            scales=self.scales[mask],
            opacities=self.opacities[mask],
            colors=self.colors[mask],
            viewmats=self.view,
            Ks=self.intrinsic,
            width=self.width,
            height=self.height,
            near_plane=0.01,
            far_plane=1e4,
            sh_degree=3,
            packed=True,
            backgrounds=torch.zeros((1, 3), device=self.means.device),
            rasterize_mode="antialiased",
        )
        rgb = rendered[0].detach().cpu().numpy()
        opacity = alpha[0, ..., 0].clamp(0.0, 1.0).detach().cpu().numpy()
        return rgb, opacity
