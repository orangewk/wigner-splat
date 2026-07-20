"""Tests for the dependency-light signed-splat demo renderer."""

import importlib.util
import pathlib
import sys

import numpy as np


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "22_signed_splat_demo"
sys.path.insert(0, str(EXPERIMENT))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


renderer = _load("signed_renderer")


def test_splat_loader_decodes_32_byte_records(tmp_path):
    dtype = np.dtype(
        [
            ("position", "<f4", (3,)),
            ("scale", "<f4", (3,)),
            ("rgba", "u1", (4,)),
            ("rotation", "u1", (4,)),
        ]
    )
    records = np.zeros(2, dtype=dtype)
    records["position"] = [[1, 2, 3], [4, 5, 6]]
    records["scale"] = 0.25
    records["rgba"] = [[255, 128, 0, 64], [0, 255, 255, 255]]
    path = tmp_path / "tiny.splat"
    path.write_bytes(records.tobytes())

    scene = renderer.load_scene(path)

    assert scene.positions.shape == (2, 3)
    np.testing.assert_allclose(scene.colors[0], [1.0, 128 / 255, 0.0])
    np.testing.assert_allclose(scene.opacities, [64 / 255, 1.0])


def test_signed_field_exactly_cancels_equal_positive_radiance():
    image = np.full((3, 4, 3), 0.6, dtype=np.float32)
    field = np.full((3, 4), -0.6, dtype=np.float32)
    cancelled = renderer.apply_signed_field(image, field, np.ones(3, dtype=np.float32))
    np.testing.assert_allclose(cancelled, 0.0, atol=1e-7)


def test_perspective_projection_places_optical_axis_at_image_center():
    xy, depth, camera_points = renderer.project_perspective(
        np.array([[0.0, 0.0, 2.0]], dtype=np.float32),
        100,
        80,
        camera_position=np.zeros(3, dtype=np.float32),
        camera_rotation=np.eye(3, dtype=np.float32),
        fx=50.0,
        fy=40.0,
        source_width=100,
        source_height=80,
    )
    np.testing.assert_allclose(xy, [[50.0, 40.0]])
    np.testing.assert_allclose(depth, [2.0])
    np.testing.assert_allclose(camera_points, [[0.0, 0.0, 2.0]])


def test_scene_rasterizer_exposes_background_when_splats_are_removed():
    xy = np.array([[2.0, 2.0]], dtype=np.float32)
    depth = np.array([1.0], dtype=np.float32)
    colors = np.array([[1.0, 0.0, 0.0]], dtype=np.float32)
    opacity = np.array([1.0], dtype=np.float32)
    rgb, alpha = renderer.rasterize_scene(xy, depth, colors, opacity, 5, 5, point_radius=1)
    background = np.full((5, 5, 3), 0.25, dtype=np.float32)
    visible = renderer.composite(rgb, alpha, background)
    _, removed_alpha = renderer.rasterize_scene(
        xy, depth, colors, np.zeros(1, dtype=np.float32), 5, 5, point_radius=1
    )
    removed = renderer.composite(rgb, removed_alpha, background)
    assert visible[2, 2, 0] == 1.0
    np.testing.assert_allclose(removed[2, 2], 0.25)
