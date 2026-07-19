"""Aggregate the three fixed Gate B/B2 runs and render the certificate figure."""

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
GATE_PATH = HERE / "run_gate_b.py"


def _load_gate():
    spec = importlib.util.spec_from_file_location("run_gate_b", GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def aggregate(rows: list[dict[str, object]]) -> dict[str, object]:
    if [row["fit_seed"] for row in rows] != [0, 1, 2]:
        raise RuntimeError("Expected exactly ordered fit seeds 0/1/2")
    for row in rows:
        if (
            row["status"] != "complete"
            or row["heldout_views"] != 4
            or row["probe_count_per_view"] != 256
        ):
            raise RuntimeError("A production Gate result is incomplete")
    gate_b_pass = all(row["gate_b_pass"] is True for row in rows)
    gate_b2_pass = all(row["gate_b2_pass"] is True for row in rows)
    return {
        "phase": "round3a_gate_b_b2",
        "status": "complete",
        "gate_b": {
            "threshold": 0.3,
            "requires_all_seeds": True,
            "passed": gate_b_pass,
            "rho_by_seed": [row["correlations"]["block_fisher"] for row in rows],
        },
        "gate_b2": {
            "requires_strict_uplift_over_all_controls_all_seeds": True,
            "passed": gate_b2_pass,
        },
        "rows": rows,
        "interpretation": (
            "At the >=25 dB static 3DGS operating point, block-Fisher predictive "
            "sigma correlates with held-out RGB-L2 residual above the fixed 0.3 "
            "bar on all seeds. It does not isolate a block-Fisher advantage: "
            "the H=I J-norm and diagonal-Fisher controls rank residuals better on "
            "all seeds."
        ),
    }


def render_figure(gate, source: Path, output: Path) -> None:
    builder = gate._load_builder()
    examples = builder.verify_upstream(source.resolve())
    if not torch.cuda.is_available():
        raise RuntimeError("Certificate figure render requires CUDA")
    device = torch.device("cuda")
    views = gate.load_heldout_views(examples)
    splats = builder.load_checkpoint(0, device)
    rows = []
    for index, view in enumerate(views):
        theta, raw_render = builder.make_renderer(splats, view)
        with torch.no_grad():
            rendered = raw_render(theta).clamp(0.0, 1.0).squeeze(0).cpu().numpy()
        maps = torch.load(
            HERE / "out" / "gate_b_seed0" / f"view_{index}.pt",
            map_location="cpu",
            weights_only=True,
        )
        rows.append(
            {
                "target": view["target"].numpy(),
                "render": rendered,
                "residual": maps["residual"].numpy(),
                "block": maps["block"].numpy(),
                "identity": maps["identity"].numpy(),
                "diag": maps["diag"].numpy(),
            }
        )

    fig, axes = plt.subplots(6, 4, figsize=(14, 15), constrained_layout=True)
    labels = (
        ("target", "held-out RGB", None),
        ("render", "fixed 3DGS render", None),
        ("residual", "RGB-L2 residual", "magma"),
        ("block", "log10 block-Fisher sigma", "viridis"),
        ("identity", "log10 J-norm (H=I)", "viridis"),
        ("diag", "log10 diagonal-Fisher sigma", "viridis"),
    )
    for column, values in enumerate(rows):
        for row_index, (key, label, cmap) in enumerate(labels):
            image = values[key]
            if key in {"block", "identity", "diag"}:
                image = np.log10(image + 1e-9)
            axes[row_index, column].imshow(image, cmap=cmap)
            axes[row_index, column].set_xticks([])
            axes[row_index, column].set_yticks([])
            if column == 0:
                axes[row_index, column].set_ylabel(label)
            if row_index == 0:
                axes[row_index, column].set_title(gate.HELDOUT_NAMES[column])
    fig.suptitle(
        "Round 3(a): held-out residual and preregistered predictive controls (seed 0)",
        fontsize=14,
    )
    fig.savefig(output, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gsplat-source", type=Path, default=Path(r"C:\tmp\gsplat-77ab983-windows")
    )
    parser.add_argument(
        "--output", type=Path, default=HERE / "phase5_gate_b_result.json"
    )
    parser.add_argument(
        "--figure", type=Path, default=HERE / "heldout_certificate.png"
    )
    args = parser.parse_args()
    rows = [
        json.loads((HERE / "out" / f"gate_b_seed{seed}" / "result.json").read_text())
        for seed in range(3)
    ]
    result = aggregate(rows)
    render_figure(_load_gate(), args.gsplat_source, args.figure)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
