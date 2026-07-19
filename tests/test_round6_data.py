"""Hard-lock pins for Round 6 public-scene preparation."""

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "experiments" / "20_real_video_gpu"


def _load(name):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


sys.path.insert(0, str(EXPERIMENT))
round5 = _load("prepare_round5_data")
round6 = _load("prepare_round6_data")


def test_round6_contiguous_central_block_is_hard_locked():
    assert round6.selected_indices(251) == tuple(range(113, 137))
    assert round6.selected_indices(301) == tuple(range(138, 162))
    assert round6.HELDOUT_POSITIONS == {4, 10, 16, 22}
    assert round6.FRAME_COUNT == 24


def test_round6_reuses_round5_archive_pins():
    assert round6.SCENES is round5.SCENES
    assert round6.SCENES["Truck"].scene_index == 1
    assert round6.SCENES["Truck"].archive_bytes == 380_210_369
    assert round6.SCENES["Truck"].archive_sha256 == (
        "9ae9ebe88c23f10e02e1abdb2a85f6bd7d4d59fad6b549685f7cbcc872439cc2"
    )
    assert round6.SCENES["Train"].scene_index == 2
    assert round6.SCENES["Train"].archive_bytes == 201_581_296
    assert round6.SCENES["Train"].archive_sha256 == (
        "542bb34aa5e83eba8e7f8095b11909f619f5f09349eaea716933a14cd8894367"
    )


def test_round6_output_root_does_not_touch_round5_record():
    assert round6.DATA_ROOT == EXPERIMENT / "data" / "round6"
    assert round6.STAGING_ROOT == EXPERIMENT / "data" / "round6-staging"
    assert round5.DATA_ROOT == EXPERIMENT / "data" / "round5"
