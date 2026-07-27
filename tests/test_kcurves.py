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


def test_committed_family_curve_extracts_all_cutoffs_and_rank_primitives():
    curve = kcurve_io.extract_empirical_upper_bound(ROOT / "experiments/20_noninclusion/results_routeB.json")
    assert curve["label"] == "family-constrained approximation curve"
    assert len(curve["points"]) == 9
    assert {(p["n_score"], p["K"]) for p in curve["points"]} == {(n, k) for n in (8, 10, 12) for k in (2, 4, 8)}
    assert curve["rank_primitive"]["pre_loss_operator_rank_R"] == 2
    assert curve["family_fit_residual_points"]["points"][-1]["epsilon"] == pytest.approx(0.0021749434414252145)
    assert curve["cutoff_status"] == "still increasing with cutoff; infinite-cutoff limit unresolved"


def test_stale_route_b_params_fail_loudly(tmp_path):
    raw = json.loads((ROOT / "experiments/20_noninclusion/results_routeB.json").read_text())
    raw["params"]["eta"] = 0.7
    path = tmp_path / "route_b.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(AssertionError):
        kcurve_io.extract_empirical_upper_bound(path)


def test_route_b_missing_cell_or_duplicate_seed_fails_loudly(tmp_path):
    raw = json.loads((ROOT / "experiments/20_noninclusion/results_routeB.json").read_text())
    raw["squeezed"][1]["seed"] = 0
    path = tmp_path / "route_b.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(AssertionError):
        kcurve_io.extract_empirical_upper_bound(path)


def test_data_proxy_has_ranks_one_through_five_and_ci_checks():
    curve = kcurve_io.extract_data_proxy(ROOT / "experiments/18_gkp_saturation/results.json", ROOT / "experiments/14_gkp_rank/out_run.log")
    assert curve["label"] == "data proxy"
    assert [p["R"] for p in curve["points"]] == [1, 2, 3, 4, 5]
    assert curve["points"][3]["held_out_per_sample_nll"] == pytest.approx(1.6299296036916187)
    assert curve["ci_vs_test_selected_mle"]["R4_primary_95"] == pytest.approx([-0.000018046357874321374, 0.00019604652582752948])
    assert curve["rank_primitive"]["ket_components_per_rank_column_K"] == 4
