"""Pins for the train-only production Fisher builder."""
import importlib.util
import pathlib

import pytest
import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "20_real_video_gpu"
    / "build_production_fisher.py"
)
_spec = importlib.util.spec_from_file_location("build_production_fisher", MODULE_PATH)
production = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(production)


def test_view_generators_are_reproducible_and_independent():
    first = torch.randint(0, 100, (32,), generator=production.view_generator(3))
    repeated = torch.randint(0, 100, (32,), generator=production.view_generator(3))
    other = torch.randint(0, 100, (32,), generator=production.view_generator(4))
    assert torch.equal(first, repeated)
    assert not torch.equal(first, other)


def test_partial_round_trip_pins_protocol(tmp_path):
    path = tmp_path / "state.pt"
    blocks = torch.arange(72, dtype=torch.float32).reshape(2, 6, 6)
    stats = [{"view_index": 0, "seconds": 1.25, "block_trace_sum": 42.0}]
    production.save_partial(path, 0, 1, blocks, stats)
    next_view, loaded, loaded_stats = production.load_partial(
        path, 0, 2, torch.device("cpu")
    )
    assert next_view == 1
    assert torch.equal(loaded, blocks)
    assert loaded_stats == stats


def test_partial_rejects_protocol_mismatch(tmp_path):
    path = tmp_path / "state.pt"
    production.save_partial(path, 0, 1, torch.zeros(2, 6, 6), [])
    state = torch.load(path, weights_only=True)
    state["probe_count"] = 128
    torch.save(state, path)
    with pytest.raises(RuntimeError, match="probe_count"):
        production.load_partial(path, 0, 2, torch.device("cpu"))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA gsplat required")
def test_full_resolution_train_only_smoke(tmp_path):
    source = pathlib.Path(r"C:\tmp\gsplat-77ab983-windows")
    checkpoint = production.checkpoint_path(0)
    if not source.is_dir() or not checkpoint.is_file():
        pytest.skip("Pinned gsplat source and Phase 3 checkpoint are required")
    result = production.run(0, source, smoke=True, output_dir=tmp_path / "smoke")
    assert result["status"] == "smoke_pass"
    assert result["heldout_accessed"] is False
    assert result["train_views"] == 1
    assert result["probe_count_per_view"] == 2
    assert result["finite"] is True
