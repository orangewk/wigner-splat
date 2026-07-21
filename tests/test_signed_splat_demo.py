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
gpu_renderer = _load("gpu_renderer")


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


def test_gaussian_ply_loader_preserves_trained_attributes(tmp_path):
    properties = (
        ["x", "y", "z"]
        + [f"f_dc_{index}" for index in range(3)]
        + [f"f_rest_{index}" for index in range(45)]
        + ["opacity"]
        + [f"scale_{index}" for index in range(3)]
        + [f"rot_{index}" for index in range(4)]
    )
    dtype = np.dtype([(name, "<f4") for name in properties])
    records = np.zeros(2, dtype=dtype)
    records["x"], records["y"], records["z"] = [1, 4], [2, 5], [3, 6]
    records["opacity"] = [0.0, np.log(3.0)]
    records["scale_0"] = np.log(2.0)
    records["scale_1"] = np.log(3.0)
    records["scale_2"] = np.log(4.0)
    records["rot_0"] = 1.0
    records["f_dc_0"] = [0.25, 0.5]
    records["f_rest_44"] = [0.75, 1.0]
    header = "\n".join(
        ["ply", "format binary_little_endian 1.0", "element vertex 2"]
        + [f"property float {name}" for name in properties]
        + ["end_header", ""]
    ).encode("ascii")
    path = tmp_path / "trained.ply"
    path.write_bytes(header + records.tobytes())

    scene = gpu_renderer.load_gaussian_ply(path)

    np.testing.assert_allclose(scene.means, [[1, 2, 3], [4, 5, 6]])
    np.testing.assert_allclose(scene.scales, [[2, 3, 4], [2, 3, 4]], rtol=1e-6)
    np.testing.assert_allclose(scene.opacities, [0.5, 0.75], rtol=1e-6)
    assert scene.sh_coefficients.shape == (2, 16, 3)
    np.testing.assert_allclose(scene.sh_coefficients[:, 0, 0], [0.25, 0.5])
    np.testing.assert_allclose(scene.sh_coefficients[:, 15, 2], [0.75, 1.0])


def test_look_at_maps_target_to_positive_camera_depth():
    eye = np.array([0.0, 0.0, -4.0], dtype=np.float32)
    target = np.zeros(3, dtype=np.float32)
    view = gpu_renderer.look_at(eye, target, np.array([0.0, -1.0, 0.0], dtype=np.float32))
    camera_target = view @ np.array([*target, 1.0], dtype=np.float32)
    np.testing.assert_allclose(camera_target[:2], 0.0, atol=1e-7)
    assert camera_target[2] == 4.0


def test_animated_camera_changes_elevation_while_crossing_target():
    target = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    radius = 5.0
    start = gpu_renderer.animated_camera_eye("eraser", 0.0, target, radius)
    overhead = gpu_renderer.animated_camera_eye("eraser", 0.42, target, radius)
    finish = gpu_renderer.animated_camera_eye("eraser", 1.0, target, radius)

    np.testing.assert_allclose(np.linalg.norm(start - target), radius, rtol=1e-6)
    assert overhead[1] < target[1]
    assert finish[1] > target[1]
    assert start[0] < target[0] < finish[0]


def test_flashlight_camera_uses_restrained_vertical_arc():
    target = np.zeros(3, dtype=np.float32)
    eraser = gpu_renderer.animated_camera_eye("eraser", 0.42, target, 5.0)
    flashlight = gpu_renderer.animated_camera_eye("dark-flashlight", 0.42, target, 5.0)

    assert abs(flashlight[1]) < abs(eraser[1])
