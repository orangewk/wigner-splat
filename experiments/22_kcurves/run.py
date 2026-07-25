"""Generate issue #100 K-curves from committed results only (no fitting)."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from kcurve_io import extract_data_proxy, extract_empirical_upper_bound

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def make_figure(upper: dict, proxy: dict, output: Path) -> None:
    fig, (ax_upper, ax_proxy, ax_lower) = plt.subplots(3, 1, figsize=(7.2, 7.0))
    upper_points = upper["points"]
    ax_upper.plot([p["K"] for p in upper_points], [p["epsilon_upper"] for p in upper_points], marker="o", color="#20456b")
    ax_upper.set_ylabel("best-found $1-F$")
    ax_upper.set_title("empirical upper bound (synthetic Route B)", loc="left", fontsize=10)
    ax_upper.text(0.02, 0.05, "fit attains $K_\\epsilon \\leq K$; not a certified lower bound", transform=ax_upper.transAxes, fontsize=8, va="bottom")
    ax_upper.grid(axis="y", alpha=0.25)

    proxy_points = proxy["points"]
    ax_proxy.plot([p["K"] for p in proxy_points], [p["held_out_per_sample_nll"] for p in proxy_points], marker="o", color="#b0653a")
    ax_proxy.set_ylabel("held-out per-sample NLL")
    ax_proxy.set_title("data proxy (real GKP data)", loc="left", fontsize=10)
    ax_proxy.text(0.02, 0.05, "true-state fidelity unavailable; this is not $K_\\epsilon$", transform=ax_proxy.transAxes, fontsize=8, va="bottom")
    ax_proxy.grid(axis="y", alpha=0.25)

    ax_lower.set_axis_off()
    ax_lower.text(0.02, 0.67, "certified lower bound", fontsize=10, fontweight="bold", transform=ax_lower.transAxes)
    ax_lower.text(0.02, 0.32, "Reserved for Gate T; not computed or inferred in this figure.", fontsize=9, transform=ax_lower.transAxes)
    for spine in ax_lower.spines.values(): spine.set_visible(True)
    for axis in (ax_upper, ax_proxy):
        axis.set_xlabel("K (mixture rank / number of Gaussian components)")
        axis.set_xticks([1, 2, 3, 4, 5, 8])
    fig.tight_layout()
    fig.savefig(output, dpi=180, metadata={"Software": "matplotlib"})
    plt.close(fig)


def main() -> None:
    upper = extract_empirical_upper_bound(ROOT / "experiments/20_noninclusion/results_routeB.json")
    proxy = extract_data_proxy(ROOT / "experiments/18_gkp_saturation/results.json", ROOT / "experiments/14_gkp_rank/out_run.log")
    _write_json(OUT / "empirical_upper_bound.json", upper)
    _write_json(OUT / "data_proxy.json", proxy)
    make_figure(upper, proxy, OUT / "kcurves.png")
    print("generated empirical_upper_bound.json, data_proxy.json, kcurves.png")


if __name__ == "__main__":
    main()
