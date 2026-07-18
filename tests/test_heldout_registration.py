"""Protocol pins for held-out localization against the frozen train model."""

import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT / "experiments" / "20_real_video_gpu" / "register_heldout_poses.py"
)
_spec = importlib.util.spec_from_file_location("register_heldout_poses", MODULE_PATH)
registration = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(registration)


def valid_records():
    phase3 = {
        "status": "hard_stop_passed",
        "protocol": {"heldout_accessed": False},
        "aggregate": {"all_seeds_passed": True},
        "runs": [{"pooled_psnr_db": value} for value in (26.9, 27.0, 27.1)],
    }
    fisher = {
        "status": "complete",
        "heldout_accessed": False,
        "validation": {"all_finite": True, "checkpoint_metadata_matches": True},
        "seeds": [{}, {}, {}],
    }
    return phase3, fisher


def test_authorization_requires_all_three_train_psnr_values():
    phase3, fisher = valid_records()
    phase3["runs"][1]["pooled_psnr_db"] = 24.999
    with pytest.raises(RuntimeError, match="PSNR hard stop"):
        registration.authorize_heldout_access(phase3, fisher)


def test_authorization_requires_completed_fisher():
    phase3, fisher = valid_records()
    fisher["status"] = "partial"
    with pytest.raises(RuntimeError, match="Fisher prerequisite"):
        registration.authorize_heldout_access(phase3, fisher)


def test_authorization_passes_only_after_both_prerequisites():
    phase3, fisher = valid_records()
    registration.authorize_heldout_access(phase3, fisher)


def test_colmap_image_parser_extracts_only_pose_records(tmp_path):
    path = tmp_path / "images.txt"
    path.write_text(
        "# comment\n1 1 0 0 0 0 0 0 1 train.png\n10 20 -1\n"
        "2 1 0 0 0 1 2 3 1 heldout.png\n11 21 5\n",
        encoding="utf-8",
    )
    assert registration.parse_registered_images(path) == {
        "train.png": ("1", "0", "0", "0", "0", "0", "0", "1", "train.png"),
        "heldout.png": ("1", "0", "0", "0", "1", "2", "3", "1", "heldout.png"),
    }
