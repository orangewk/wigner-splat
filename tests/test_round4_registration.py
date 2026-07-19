"""CPU checks for the Round 4 registration hard stop and trajectory record."""

import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "register_round4_poses.py"
_spec = importlib.util.spec_from_file_location("register_round4_poses", MODULE_PATH)
registration = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(registration)


def identity_pose(tx):
    return ("1", "0", "0", "0", str(tx), "0", "0", "1", "image.png")


def test_trajectory_record_is_descriptive_and_scale_relative():
    poses = {
        "train0.png": identity_pose(0),
        "train1.png": identity_pose(1),
        "fresh0.png": identity_pose(2),
        "fresh1.png": identity_pose(4),
    }
    result = registration.trajectory_record(
        poses, ["train0.png", "train1.png"], ["fresh0.png", "fresh1.png"]
    )
    assert result["descriptive_only"] is True
    assert result["train_consecutive_step_median"] == pytest.approx(1.0)
    assert result["fresh_steps_over_train_median"] == pytest.approx([1.0, 2.0])


def test_write_dnf_records_missing_views_without_scores(tmp_path):
    result = registration.write_dnf(
        tmp_path, ["train.png"], ["fresh0.png", "fresh1.png"], {"fresh0.png"}
    )
    assert result["status"] == "dnf"
    assert result["scores_computed"] is False
    assert result["missing_fresh_names"] == ["fresh1.png"]
