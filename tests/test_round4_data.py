"""Protocol pins for the fresh Round 4 held-out split."""

import importlib.util
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "experiments" / "20_real_video_gpu" / "prepare_round4_data.py"
_spec = importlib.util.spec_from_file_location("prepare_round4_data", MODULE_PATH)
round4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(round4)


def test_round4_indices_and_names_are_hard_locked():
    assert round4.SOURCE_INDICES == (216, 244, 272, 300)
    assert [round4.frame_name(index) for index in round4.SOURCE_INDICES] == [
        "round4_src_0216.png",
        "round4_src_0244.png",
        "round4_src_0272.png",
        "round4_src_0300.png",
    ]


def test_round4_refuses_any_existing_output(monkeypatch, tmp_path):
    output = tmp_path / "heldout2-sealed"
    output.mkdir()
    monkeypatch.setattr(round4, "OUTPUT", output)
    monkeypatch.setattr(round4, "STAGING", tmp_path / "staging")
    monkeypatch.setattr(round4, "MANIFEST", tmp_path / "manifest.json")
    with pytest.raises(RuntimeError, match="Refusing to overwrite"):
        round4.require_fresh_outputs()
