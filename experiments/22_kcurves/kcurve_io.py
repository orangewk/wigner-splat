"""Fit-free extraction and loud validation for issue #100 K-curves."""

from __future__ import annotations

import json
from pathlib import Path


EXPECTED_ETA = 0.8
EXPECTED_SIGMA = 0.1
EXPECTED_N_MAX = 12


def extract_empirical_upper_bound(route_b_path: Path) -> dict:
    """Extract best-found Route-B points at the largest scoring cutoff."""
    source = json.loads(route_b_path.read_text(encoding="utf-8"))
    params = source["params"]
    assert params["eta"] == EXPECTED_ETA, params
    assert params["sigma"] == EXPECTED_SIGMA, params
    assert source["ruling"]["alarm"] is False, source["ruling"]

    rows = source["squeezed"]
    n_max = max(row["n_score"] for row in rows)
    assert n_max == EXPECTED_N_MAX, n_max
    ks = sorted({row["K"] for row in rows})
    assert ks == [2, 4, 8], ks
    points = []
    for k in ks:
        candidates = [row for row in rows if row["K"] == k and row["n_score"] == n_max]
        assert len(candidates) == 3, (k, candidates)
        best = max(candidates, key=lambda row: row["F"])
        assert 0.0 < best["F"] < 1.0, best
        points.append({"K": k, "epsilon_upper": 1.0 - best["F"], "fidelity": best["F"], "eta_prime": best["eta_p"], "seed": best["seed"], "n_score": n_max})

    assert abs(points[0]["epsilon_upper"] - 0.003438409405929571) < 1e-15
    assert abs(points[1]["epsilon_upper"] - 0.0023747199770521996) < 1e-15
    assert abs(points[2]["epsilon_upper"] - 0.0021749434414252145) < 1e-15
    return {"schema_version": 1, "label": "empirical upper bound", "quantity": "best-found epsilon = 1 - F at fixed K", "interpretation": "A fit attains K_epsilon <= K; this is not a certified lower bound.", "source": "experiments/20_noninclusion/results_routeB.json", "params": {"eta": params["eta"], "sigma": params["sigma"], "n_score": n_max}, "points": points}


def _exp14_primary_rank_points(exp14_log_path: Path) -> dict[int, float]:
    text = exp14_log_path.read_text(encoding="utf-8")
    expected = {1: 1.63304, 2: 1.63084}
    for rank, nll in expected.items():
        assert f"lossy R={rank} K=4: test NLL={nll:.5f}" in text
    return expected


def extract_data_proxy(exp18_path: Path, exp14_log_path: Path) -> dict:
    """Extract held-out NLL vs mixture rank; this is explicitly a data proxy."""
    source = json.loads(exp18_path.read_text(encoding="utf-8"))
    primary = source["primary"]
    fits = primary["fits"]
    assert primary["mle_best"] == {"n_max": 16, "dof": 255, "test": 1.629838692906455}
    assert primary["cis"]["r4_mle"][:2] == [-1.8046357874321374e-05, 0.00019604652582752948]
    assert source["alternate"]["cis"]["r4_mle"][:2] == [-0.00016675900530110381, 2.7269914027297554e-05]

    points = [{"K": rank, "held_out_per_sample_nll": nll, "source": "exp14 committed log"} for rank, nll in _exp14_primary_rank_points(exp14_log_path).items()]
    for rank in (3, 4, 5):
        fit = fits[f"R{rank}K4"]
        assert fit["dof"] == 23 * rank, fit
        points.append({"K": rank, "held_out_per_sample_nll": fit["test"], "dof": fit["dof"], "source": "exp18 results JSON"})
    assert [point["K"] for point in points] == [1, 2, 3, 4, 5]
    assert abs(points[3]["held_out_per_sample_nll"] - 1.6299296036916187) < 1e-15
    return {"schema_version": 1, "label": "data proxy", "quantity": "held-out per-sample NLL vs mixture rank K", "interpretation": "Real-data true-state fidelity is unavailable; this is not K_epsilon.", "source": ["experiments/18_gkp_saturation/results.json", "experiments/14_gkp_rank/out_run.log"], "primary_split": "seed 0", "ci_vs_test_selected_mle": {"R4_primary_95": primary["cis"]["r4_mle"][:2], "R4_alternate_95": source["alternate"]["cis"]["r4_mle"][:2]}, "points": points}
