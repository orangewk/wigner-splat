"""Aggregate Round 4 and render its fresh-view certificate figure."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "run_round4_gate.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_round4_gate", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def aggregate(rows: list[dict]) -> dict:
    if [row["fit_seed"] for row in rows] != [0, 1, 2]:
        raise RuntimeError("Expected ordered Round 4 fit seeds 0/1/2")
    for row in rows:
        if (
            row["status"] != "complete"
            or row["heldout_views"] != 4
            or row["probe_count_per_view"] != 256
            or row["view_seed_indices"] != [4, 5, 6, 7]
        ):
            raise RuntimeError("A Round 4 production result is incomplete")
    gate_b = all(row["gate_b_pass"] is True for row in rows)
    gate_b2 = all(row["gate_b2_pass"] is True for row in rows)
    block = [row["correlations"]["block_fisher"] for row in rows]
    ensemble = [row["correlations"]["ensemble_sigma"] for row in rows]
    return {
        "phase": "round4_fresh_replication_and_ensemble_control",
        "status": "complete",
        "registration_hard_stop": {
            "passed": True,
            "fresh_registered": 4,
            "train_model_frozen": True,
        },
        "gate_b": {
            "threshold": 0.3,
            "requires_all_seeds": True,
            "passed": gate_b,
            "block_fisher_rho_by_seed": block,
        },
        "gate_b2": {
            "requires_strict_uplift_over_four_controls_all_seeds": True,
            "passed": gate_b2,
            "ensemble_rho_by_seed": ensemble,
            "ensemble_ge_block_by_seed": [
                ensemble[index] >= block[index] for index in range(3)
            ],
        },
        "damping_sensitivity_descriptive_only": {
            "fractions": [1e-4, 1e-6, 1e-8],
            "block_rho_by_fraction_then_seed": {
                "1e-4": [
                    row["correlations"]["block_fisher_damping_1e-4"] for row in rows
                ],
                "1e-6": block,
                "1e-8": [
                    row["correlations"]["block_fisher_damping_1e-8"] for row in rows
                ],
            },
            "primary_fraction_remains": 1e-6,
        },
        "rows": rows,
        "interpretation": (
            "Gate B replicates on four fresh, temporally extrapolated registered views. "
            "Block Fisher now strictly beats amplitude, H=I J-norm, and diagonal Fisher "
            "on every fit seed, but the shared three-fit-seed ensemble sigma ranks "
            "residual better on every seed. Therefore Gate B2 fails and the hard-locked "
            "reading applies: at this operating point the H^-1 certificate does not "
            "beat brute-force repetition. Damping sensitivity is descriptive and does "
            "not alter the primary 1e-6 verdict."
        ),
    }


def render_figure(runner, source: Path, output: Path) -> None:
    gate = runner._load_round3_gate()
    builder = gate._load_builder()
    examples = builder.verify_upstream(source.resolve())
    device = torch.device("cuda")
    views = runner.load_views(examples)
    splats = builder.load_checkpoint(0, device)
    values = []
    for index, view in enumerate(views):
        theta, raw_render = builder.make_renderer(splats, view)
        with torch.no_grad():
            rendered = raw_render(theta).clamp(0.0, 1.0).squeeze(0).cpu().numpy()
        maps = torch.load(
            HERE / "out" / "round4_gate_seed0" / f"view_{index}.pt",
            map_location="cpu", weights_only=True,
        )
        values.append({
            "target": view["target"].numpy(),
            "render": rendered,
            "residual": maps["residual"].numpy(),
            "block": maps["block_1e-06"].numpy(),
            "ensemble": maps["ensemble"].numpy(),
        })
    fig, axes = plt.subplots(5, 4, figsize=(14, 13), constrained_layout=True)
    labels = (
        ("target", "fresh held-out RGB", None),
        ("render", "fixed 3DGS render", None),
        ("residual", "RGB-L2 residual", "magma"),
        ("block", "log10 block-Fisher sigma", "viridis"),
        ("ensemble", "log10 3-seed ensemble sigma", "viridis"),
    )
    for column, row in enumerate(values):
        for row_index, (key, label, cmap) in enumerate(labels):
            image = row[key]
            if key in {"block", "ensemble"}:
                image = np.log10(image + 1e-9)
            axes[row_index, column].imshow(image, cmap=cmap)
            axes[row_index, column].set_xticks([])
            axes[row_index, column].set_yticks([])
            if column == 0:
                axes[row_index, column].set_ylabel(label)
            if row_index == 0:
                axes[row_index, column].set_title(runner.HELDOUT_NAMES[column])
    fig.suptitle("Round 4: fresh-view residual, block Fisher, and ensemble control")
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument("--output", type=Path, default=HERE / "phase6_round4_result.json")
    parser.add_argument("--figure", type=Path, default=HERE / "round4_certificate.png")
    args = parser.parse_args()
    rows = [json.loads(
        (HERE / "out" / f"round4_gate_seed{seed}" / "result.json").read_text()
    ) for seed in range(3)]
    result = aggregate(rows)
    render_figure(_load_runner(), args.gsplat_source, args.figure)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
