"""Fit-free extraction and loud validation for issue #100 K-curves."""

from __future__ import annotations

import json
from pathlib import Path


EXPECTED_ETA = 0.8
EXPECTED_SIGMA = 0.1
EXPECTED_N_MAX = 12


def extract_empirical_upper_bound(route_b_path: Path) -> dict:
    """Extract the Route-B rank-2 family curve at every scored cutoff."""
    source = json.loads(route_b_path.read_text(encoding="utf-8"))
    params = source["params"]
    assert params["eta"] == EXPECTED_ETA, params
    assert params["sigma"] == EXPECTED_SIGMA, params
    assert source["ruling"]["alarm"] is False, source["ruling"]

    rows = source["squeezed"]
    n_scores = sorted({row["n_score"] for row in rows})
    assert n_scores == [8, 10, EXPECTED_N_MAX], n_scores
    ks = sorted({row["K"] for row in rows})
    assert ks == [2, 4, 8], ks
    expected_seeds = {0, 1, 2}
    points = []
    for n_score in n_scores:
        for k in ks:
            candidates = [row for row in rows if row["K"] == k and row["n_score"] == n_score]
            assert len(candidates) == len(expected_seeds), (n_score, k, candidates)
            seeds = [row["seed"] for row in candidates]
            assert set(seeds) == expected_seeds and len(set(seeds)) == len(seeds), (n_score, k, seeds)
            best = max(candidates, key=lambda row: row["F"])
            assert 0.0 < best["F"] < 1.0, best
            points.append({"K": k, "epsilon": 1.0 - best["F"], "fidelity": best["F"], "eta_prime": best["eta_p"], "seed": best["seed"], "n_score": n_score})

    n12_points = [point for point in points if point["n_score"] == EXPECTED_N_MAX]
    assert [point["K"] for point in n12_points] == [2, 4, 8]
    assert abs(n12_points[0]["epsilon"] - 0.003438409405929571) < 1e-15
    assert abs(n12_points[1]["epsilon"] - 0.0023747199770521996) < 1e-15
    assert abs(n12_points[2]["epsilon"] - 0.0021749434414252145) < 1e-15
    return {
        "schema_version": 2,
        "label": "family-constrained approximation curve",
        "quantity": "best-found generalized-fidelity residual 1 - F within the fixed rank-2 BB† + loss family",
        "rank_primitive": {"pre_loss_operator_rank_R": 2, "curve_x_axis": "K = ket components per rank-2 column"},
        "fidelity_convention": "generalized Uhlmann fidelity for cropped/subnormalized matrices",
        "cutoff_status": "still increasing with cutoff; infinite-cutoff limit unresolved",
        "epistemic_status": "empirical best-found family-constrained approximation; not a proven lower bound and not an upper bound on K_epsilon^{G,F}",
        "family_fit_residual_points": {"points": n12_points},
        "lower_bound_reservation": {"status": "reserved_not_computed", "scope": "Gate T lower bounds"},
        "source": "experiments/20_noninclusion/results_routeB.json",
        "params": {"eta": params["eta"], "sigma": params["sigma"], "n_scores": n_scores},
        "points": points,
    }


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
    mle_best = primary["mle_best"]
    assert mle_best["n_max"] == 16, mle_best
    assert mle_best["dof"] == 255, mle_best
    assert mle_best["test"] == 1.629838692906455, mle_best
    assert primary["cis"]["r4_mle"][:2] == [-1.8046357874321374e-05, 0.00019604652582752948]
    assert source["alternate"]["cis"]["r4_mle"][:2] == [-0.00016675900530110381, 2.7269914027297554e-05]

    points = [{"R": rank, "held_out_per_sample_nll": nll, "source": "exp14 committed log"} for rank, nll in _exp14_primary_rank_points(exp14_log_path).items()]
    for rank in (3, 4, 5):
        fit = fits[f"R{rank}K4"]
        assert fit["dof"] == 23 * rank, fit
        points.append({"R": rank, "held_out_per_sample_nll": fit["test"], "dof": fit["dof"], "source": "exp18 results JSON"})
    assert [point["R"] for point in points] == [1, 2, 3, 4, 5]
    assert abs(points[3]["held_out_per_sample_nll"] - 1.6299296036916187) < 1e-15
    return {
        "schema_version": 2,
        "label": "data proxy",
        "quantity": "held-out per-sample NLL vs operator mixture rank R (K=4 ket components fixed)",
        "rank_primitive": {"curve_x_axis": "R = operator mixture rank", "ket_components_per_rank_column_K": 4},
        "fidelity_convention": "not available: real-data true-state fidelity is inaccessible",
        "cutoff_status": "not applicable: this is a fixed reconstruction schedule, not a fidelity cutoff sweep",
        "epistemic_status": "data proxy only; not K_epsilon^{G,F} and not a proven lower bound",
        "lower_bound_reservation": {"status": "reserved_not_computed", "scope": "Gate T lower bounds"},
        "source": ["experiments/18_gkp_saturation/results.json", "experiments/14_gkp_rank/out_run.log"],
        "primary_split": "seed 0",
        "ci_vs_test_selected_mle": {"R4_primary_95": primary["cis"]["r4_mle"][:2], "R4_alternate_95": source["alternate"]["cis"]["r4_mle"][:2]},
        "points": points,
    }
