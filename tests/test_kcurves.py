"""Torch-free tests for issue #100 K-curve extraction."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / "experiments" / "22_kcurves"
spec = importlib.util.spec_from_file_location("kcurve_io", EXP / "kcurve_io.py")
assert spec is not None and spec.loader is not None
kcurve_io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kcurve_io)


def test_committed_empirical_upper_bound_extracts_largest_cutoff():
    curve = kcurve_io.extract_empirical_upper_bound(ROOT / "experiments/20_noninclusion/results_routeB.json")
    assert curve["label"] == "empirical upper bound"
    assert [p["K"] for p in curve["points"]] == [2, 4, 8]
    assert [p["n_score"] for p in curve["points"]] == [12, 12, 12]
    assert curve["points"][-1]["epsilon_upper"] == pytest.approx(0.0021749434414252145)


def test_stale_route_b_params_fail_loudly(tmp_path):
    raw = json.loads((ROOT / "experiments/20_noninclusion/results_routeB.json").read_text())
    raw["params"]["eta"] = 0.7
    path = tmp_path / "route_b.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(AssertionError):
        kcurve_io.extract_empirical_upper_bound(path)


def test_data_proxy_has_ranks_one_through_five_and_ci_checks():
    curve = kcurve_io.extract_data_proxy(ROOT / "experiments/18_gkp_saturation/results.json", ROOT / "experiments/14_gkp_rank/out_run.log")
    assert curve["label"] == "data proxy"
    assert [p["K"] for p in curve["points"]] == [1, 2, 3, 4, 5]
    assert curve["points"][3]["held_out_per_sample_nll"] == pytest.approx(1.6299296036916187)
    assert curve["ci_vs_test_selected_mle"]["R4_primary_95"] == pytest.approx([-0.000018046357874321374, 0.00019604652582752948])
