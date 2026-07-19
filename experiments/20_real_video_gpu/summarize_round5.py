"""Summarize the preregistered Round 5 DNF without opening held-out images."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pycolmap

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "round5"
OUT = HERE / "out" / "round5"

ATTEMPTS = {
    "Truck": {
        "sequential": ("colmap/train/sparse/0", 17.7),
        "exhaustive": ("colmap/exhaustive_v1/sparse/0", 10.9),
    },
    "Train": {
        "sequential": ("colmap/train/sparse/0", 19.2),
        "exhaustive": ("colmap/exhaustive_v1/sparse/0", 6.5),
    },
}


def registered_images(model: Path) -> int:
    if not model.is_dir():
        raise FileNotFoundError(model)
    return pycolmap.Reconstruction(str(model)).num_reg_images()


def aggregate() -> dict:
    scenes = {}
    for scene, attempts in ATTEMPTS.items():
        manifest = json.loads(
            (DATA / scene.lower() / "manifest.json").read_text(encoding="utf-8")
        )
        rows = []
        for matcher, (relative_model, elapsed) in attempts.items():
            model = OUT / scene.lower() / relative_model
            rows.append({
                "matcher": matcher,
                "registered_train_images": registered_images(model),
                "required_train_images": 20,
                "wall_seconds": elapsed,
                "wall_seconds_source": "execution harness observation",
                "cuda_feature_extraction_and_matching": True,
                "peak_vram_gib": None,
                "peak_vram_note": (
                    "The COLMAP process was too brief for a synchronized peak sample; "
                    "GPU use is established by the CUDA extractor/matcher logs."
                ),
                "model": model.relative_to(HERE).as_posix(),
            })
        scenes[scene] = {
            "status": "did_not_finish",
            "source_archive_sha256": manifest["source"]["archive_sha256"],
            "total_official_frames": manifest["selection"]["total_frame_count"],
            "selection_stride": manifest["selection"]["stride"],
            "train_images": 20,
            "heldout_sealed_images": 4,
            "heldout_access": False,
            "attempts": rows,
            "best_registered_train_images": max(
                row["registered_train_images"] for row in rows
            ),
            "dnf_reason": "No COLMAP attempt registered all 20 train images.",
            "fit_started": False,
            "fit_hard_stop_evaluated": False,
            "fisher_started": False,
            "gate_started": False,
        }
    return {
        "phase": "round5_independent_public_scene_replication",
        "status": "did_not_finish",
        "hard_lock_issue_comment": 5014598454,
        "operational_correction_issue_comment": 5014845453,
        "prework": {
            "shared_ensemble_reuse_guard": "implemented_and_cpu_verified",
            "validated_fields": [
                "heldout_names", "fit_seeds", "ddof", "map_sha256",
            ],
        },
        "scenes": scenes,
        "conclusion": (
            "Both preregistered public scenes failed before fitting because the "
            "hard-locked 20-image training sets did not yield complete COLMAP "
            "reconstructions. Truck registered at most 15/20 and Train at most "
            "3/20 across the preserved attempts. No gsplat, Fisher, held-out "
            "registration, Gate B/B2, or decomposition result exists. This DNF "
            "does not support either replication or rejection of Gate B."
        ),
    }


def render_figure(result: dict, output: Path) -> None:
    scenes = list(result["scenes"])
    matchers = ["sequential", "exhaustive"]
    values = {
        scene: {
            row["matcher"]: row["registered_train_images"]
            for row in result["scenes"][scene]["attempts"]
        }
        for scene in scenes
    }
    fig, ax = plt.subplots(figsize=(7.5, 4.8), constrained_layout=True)
    positions = range(len(scenes))
    width = 0.34
    for offset, matcher in zip((-width / 2, width / 2), matchers):
        bars = ax.bar(
            [position + offset for position in positions],
            [values[scene][matcher] for scene in scenes],
            width,
            label=matcher,
        )
        ax.bar_label(bars)
    ax.axhline(20, color="black", linestyle="--", label="required 20/20")
    ax.set_xticks(list(positions), scenes)
    ax.set_ylim(0, 21)
    ax.set_ylabel("registered train images")
    ax.set_title("Issue #48 Round 5: COLMAP prerequisite DNF")
    ax.legend()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=HERE / "phase7_round5_result.json"
    )
    parser.add_argument(
        "--figure", type=Path, default=HERE / "round5_dnf_certificate.png"
    )
    args = parser.parse_args()
    result = aggregate()
    render_figure(result, args.figure)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
