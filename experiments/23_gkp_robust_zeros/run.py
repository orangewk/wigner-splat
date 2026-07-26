"""Deterministically generate Gate E finite-energy GKP robust-zero artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from gkp_robust_zeros import build_gkp_state, find_zeros, robust_zero_rows, validate_zero_count


OUT = Path(__file__).resolve().parent
DELTAS = (0.2, 0.3, 0.4)
N_MAX = 160
N_MAX_ELEVATED = 200
DISK_RADII = (0.18, 0.30)
EPSILONS = (1e-2, 1e-3, 1e-4)
LIFTED_EXPECTED_MAX_WINDOW = {
    0.2: {1e-2: 0, 1e-3: 0, 1e-4: 0},
    0.3: {1e-2: 0, 1e-3: 0, 1e-4: 4},
    0.4: {1e-2: 0, 1e-3: 4, 1e-4: 4},
}

def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _radii(energy: float) -> tuple[float, ...]:
    base = np.sqrt(max(energy, 1.0))
    return tuple(float(np.round(x * base, 3)) for x in (0.75, 1.0, 1.25))


def _format_epsilon(epsilon: float) -> str:
    return format(epsilon, ".0e").replace("e-0", "e-")


def certification_from_rows(rows: list[dict], max_radius: float, delta: float) -> dict:
    """Derive configuration-level scope and prose solely from lifted row counts."""
    lifted = {
        row["epsilon"]: row["N_robust_lifted"]
        for row in rows
        if row["R"] == max_radius and row["delta"] == delta
    }
    nonzero_epsilons = sorted(epsilon for epsilon, count in lifted.items() if count > 0)
    certification = {
        "ideal_comb": {
            "epsilons_with_nonzero_lifted": nonzero_epsilons,
            "max_N_robust_lifted": max(lifted.values()),
        },
        "psi_trunc_only": not nonzero_epsilons,
    }
    if nonzero_epsilons:
        certification["description"] = (
            "The ideal finite-energy comb is certified for epsilon <= "
            f"{_format_epsilon(max(nonzero_epsilons))}, with maximum "
            f"N_robust_lifted={certification['ideal_comb']['max_N_robust_lifted']}."
        )
    else:
        certification["description"] = (
            "Only psi_trunc is certified at this cutoff: all scanned "
            f"lifted counts are {certification['ideal_comb']['max_N_robust_lifted']}."
        )
    return certification

def compute() -> dict:
    configurations = []
    map_data = []
    for envelope_delta in DELTAS:
        state = build_gkp_state(envelope_delta, N_MAX)
        elevated = build_gkp_state(envelope_delta, N_MAX_ELEVATED)
        radii = _radii(state.mean_photon_reference)
        max_radius = max(radii) + max(DISK_RADII)
        roots = find_zeros(state.coefficients, max_radius)
        elevated_roots = find_zeros(elevated.coefficients, max_radius)
        rows = []
        tail_norm = float(np.sqrt(state.fock_tail_upper_bound))
        for radius in radii:
            inside = roots[np.abs(roots) <= radius]
            validate_zero_count(state.coefficients, radius, inside)
            # A finite-window density check: area/pi plus a perimeter allowance.
            assert len(inside) <= int(np.ceil(radius**2 + 4.0 * radius + 8.0))
            for disk_radius in DISK_RADII:
                robust_rows = robust_zero_rows(state.coefficients, inside, disk_radius, EPSILONS, tail_norm=tail_norm)
                elevated_inside = elevated_roots[np.abs(elevated_roots) <= radius]
                elevated_rows = robust_zero_rows(elevated.coefficients, elevated_inside, disk_radius, EPSILONS)
                for epsilon in EPSILONS:
                    count = sum(row["robust"] for row in robust_rows if row["epsilon"] == epsilon)
                    lifted_count = sum(row["lifted_robust"] for row in robust_rows if row["epsilon"] == epsilon)
                    elevated_count = sum(row["robust"] for row in elevated_rows if row["epsilon"] == epsilon)
                    assert count == elevated_count, (envelope_delta, radius, disk_radius, epsilon, count, elevated_count)
                    rows.append({
                        "R": radius,
                        "delta": disk_radius,
                        "epsilon": epsilon,
                        "N_zeros": len(inside),
                        "N_robust": count,
                        "N_robust_lifted": lifted_count,
                        "K_lower_bound_symbolic": f"{count}/C - B*({radius + disk_radius:.3f})",
                    })
                if radius == radii[-1] and disk_radius == DISK_RADII[0]:
                    map_data.append((envelope_delta, inside, robust_rows))
        lifted_max_window = {
            row["epsilon"]: row["N_robust_lifted"]
            for row in rows
            if row["R"] == radii[-1] and row["delta"] == DISK_RADII[0]
        }
        assert lifted_max_window == LIFTED_EXPECTED_MAX_WINDOW[envelope_delta], (envelope_delta, lifted_max_window)
        configurations.append({
            "envelope_width_Delta": envelope_delta,
            "state": {
                "n_max": N_MAX,
                "elevated_n_max": N_MAX_ELEVATED,
                "reference_cutoff": state.reference_cutoff,
                "mean_photon_reference": state.mean_photon_reference,
                "fock_tail_upper_bound": state.fock_tail_upper_bound,
                "lattice_half_width_s_max": state.s_max,
                "lattice_envelope_amplitude_bound": state.lattice_envelope_amplitude_bound,
            },
            "rows": rows,
            "certification": certification_from_rows(rows, radii[-1], DISK_RADII[0]),
        })
    return {"configurations": configurations, "map_data": map_data}


def make_figure(result: dict, output: Path) -> None:
    fig, axes = plt.subplots(1, len(result["map_data"]), figsize=(12, 3.8), sharex=False, sharey=False)
    for ax, (envelope_delta, roots, rows) in zip(axes, result["map_data"]):
        robust = {(round(row["zero"][0], 12), round(row["zero"][1], 12)) for row in rows if row["epsilon"] == 1e-3 and row["robust"]}
        colors = ["#1b7f3a" if (round(root.real, 12), round(root.imag, 12)) in robust else "#b5503c" for root in roots]
        ax.scatter(roots.real, roots.imag, c=colors, s=22)
        ax.axhline(0, color="#999999", lw=0.6)
        ax.axvline(0, color="#999999", lw=0.6)
        ax.set_aspect("equal")
        ax.set_title(f"Delta={envelope_delta}, eps=1e-3")
        ax.set_xlabel("Re z")
    axes[0].set_ylabel("Im z")
    fig.suptitle("Finite-energy GKP Bargmann zeros: green robust, red non-robust")
    fig.tight_layout()
    fig.savefig(output, dpi=180, metadata={"Software": "matplotlib"})
    plt.close(fig)


def main() -> None:
    computed = compute()
    payload = {
        "schema_version": 2,
        "epistemic_status": "Certification scope is derived separately for every configuration.",
        "lifting_rule": (
            "For a truncated-state zero disk, ||psi_trunc - phi|| <= sqrt(fock_tail_upper_bound) + d(epsilon). "
            "Therefore the disk lifts to the untruncated finite-energy comb when circle_minimum exceeds "
            "exp((|z_j|+delta)^2/2) times that sum; the tail bound includes the renormalization contribution."
        ),        "rank_primitive": {
            "quantity": "restricted equal-squeezing Gaussian ket-component count",
            "dictionary": "G_eq(a,B): common complex squeezing a and |b_k| <= B",
        },
        "fidelity_convention": "pure-state fidelity F(psi,phi) >= 1-epsilon; d(epsilon)=sqrt(2-2sqrt(1-epsilon))",
        "theorem_scope": "The symbolic bound is K >= N_robust/C - B(R+delta); C is intentionally not assigned a numerical value.",
        "zero_method": "Fock-truncated Bargmann polynomial roots, residual-checked and tiled argument-principle cross-checked",
        "robustness_method": "1440-point circle minimum and Rouché threshold; disk disjointness asserted",
        "truncation_protocol": "componentwise resolved Fock tail plus exact second-factorial-moment Markov remainder; N_robust asserted invariant when n_max rises from 160 to 200",
        "configurations": computed["configurations"],
    }
    _write_json(OUT / "robust_zero_results.json", payload)
    make_figure(computed, OUT / "robust_zero_map.png")
    print("generated robust_zero_results.json, robust_zero_map.png")


if __name__ == "__main__":
    main()
