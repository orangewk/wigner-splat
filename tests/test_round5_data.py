"""Hard-lock pins for Round 5 public-scene preparation."""

import importlib.util
import pathlib
import sys
import zipfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "prepare_round5_data.py"
_spec = importlib.util.spec_from_file_location("prepare_round5_data", MODULE_PATH)
round5 = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = round5
_spec.loader.exec_module(round5)


def test_round5_scene_order_stride_and_split_are_hard_locked():
    assert round5.SCENES["Truck"].scene_index == 1
    assert round5.SCENES["Train"].scene_index == 2
    assert round5.selected_indices(251) == tuple(range(0, 240, 10))
    assert round5.selected_indices(301) == tuple(range(0, 288, 12))
    assert round5.HELDOUT_POSITIONS == {4, 10, 16, 22}


def test_round5_archive_identity_is_pinned():
    assert round5.SCENES["Truck"].archive_bytes == 380_210_369
    assert round5.SCENES["Truck"].archive_sha256 == (
        "9ae9ebe88c23f10e02e1abdb2a85f6bd7d4d59fad6b549685f7cbcc872439cc2"
    )
    assert round5.SCENES["Train"].archive_bytes == 201_581_296
    assert round5.SCENES["Train"].archive_sha256 == (
        "542bb34aa5e83eba8e7f8095b11909f619f5f09349eaea716933a14cd8894367"
    )


def test_round5_archive_member_order_and_zip_slip_guard(tmp_path):
    valid = tmp_path / "valid.zip"
    with zipfile.ZipFile(valid, "w") as archive:
        archive.writestr("scene/00002.jpg", b"b")
        archive.writestr("scene/readme.txt", b"ignored")
        archive.writestr("scene/00001.jpg", b"a")
    with zipfile.ZipFile(valid) as archive:
        assert [member.filename for member in round5.image_members(archive)] == [
            "scene/00001.jpg", "scene/00002.jpg",
        ]

    unsafe = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(unsafe, "w") as archive:
        archive.writestr("../bad.jpg", b"bad")
    with zipfile.ZipFile(unsafe) as archive:
        with pytest.raises(RuntimeError, match="Unsafe archive member"):
            round5.image_members(archive)
