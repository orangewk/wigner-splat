"""Summarize the preregistered Round 6 PSNR-hard-stop DNF."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "round6"
OUT = HERE / "out" / "round6"
PSNR_FLOOR_DB = 25.0
OBSERVED_WALL_SECONDS = {
    "Truck": {"colmap": 16.4, "fit_seed0": 177.3},
    "Train": {"colmap": 12.3, "fit_seed0": 180.5},
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_metrics(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def aggregate() -> dict:
    scenes = {}
    for scene in ("Truck", "Train"):
        key = scene.lower()
        manifest = _read_json(DATA / key / "manifest.json")
        colmap = _read_json(OUT / key / "colmap" / "exhaustive_v1" / "result.json")
        run = OUT / key / "gsplat" / "seed0_fixed_4000"
        final = _read_json(run / "results" / "stats" / "train_pooled_step3999.json")
        adapter = _read_json(run / "adapter_config.json")
        metrics = _read_metrics(run / "metrics.jsonl")
        peak = max(metrics, key=lambda row: row["pooled_psnr_db"])
        if colmap["registered_train_count"] != 20 or colmap["heldout_access"]:
            raise RuntimeError(f"{scene} COLMAP boundary mismatch")
        if final["step"] != 3999 or final["train_images"] != 20:
            raise RuntimeError(f"{scene} final fit metric mismatch")
        if adapter["seed"] != 0 or adapter["steps"] != 4000:
            raise RuntimeError(f"{scene} adapter recipe mismatch")
        if adapter["heldout_access"]:
            raise RuntimeError(f"{scene} fit accessed heldout data")
        if final["pooled_psnr_db"] >= PSNR_FLOOR_DB:
            raise RuntimeError(f"{scene} unexpectedly passed the PSNR hard stop")

        scenes[scene] = {
            "status": "did_not_finish",
            "source_archive_sha256": manifest["source"]["archive_sha256"],
            "selection_start": manifest["selection"]["start"],
            "source_indices": manifest["selection"]["source_indices"],
            "train_images": 20,
            "heldout_sealed_images": 4,
            "heldout_access": False,
            "colmap": {
                "matcher": "exhaustive",
                "cuda_feature_extraction_and_matching": True,
                "registered_train_images": colmap["registered_train_count"],
                "required_train_images": 20,
                "wall_seconds": OBSERVED_WALL_SECONDS[scene]["colmap"],
                "wall_seconds_source": "execution harness observation",
                "result": (
                    Path("out") / "round6" / key / "colmap" / "exhaustive_v1" / "result.json"
                ).as_posix(),
            },
            "fit_hard_stop": {
                "required_fit_seeds": [0, 1, 2],
                "executed_fit_seeds": [0],
                "not_run_after_decisive_failure": [1, 2],
                "seed0": {
                    "steps": 4000,
                    "final_step": final["step"],
                    "final_pooled_mse": final["pooled_mse"],
                    "final_pooled_psnr_db": final["pooled_psnr_db"],
                    "required_pooled_psnr_db": PSNR_FLOOR_DB,
                    "passed": False,
                    "descriptive_peak_pooled_psnr_db": peak["pooled_psnr_db"],
                    "descriptive_peak_step": peak["step"],
                    "num_gaussians_final": final["num_GS"],
                    "peak_vram_gib": final["peak_vram_gib"],
                    "wall_seconds": OBSERVED_WALL_SECONDS[scene]["fit_seed0"],
                    "wall_seconds_source": "execution harness observation",
                    "checkpoint_step3999_exists": (
                        run / "results" / "ckpts" / "ckpt_3999_rank0.pt"
                    ).is_file(),
                },
            },
            "dnf_reason": (
                "Fit seed 0 completed the fixed 4000-step recipe below the "
                "pooled train PSNR floor; one failed seed is sufficient for DNF."
            ),
            "fisher_started": False,
            "heldout_registration_started": False,
            "gate_started": False,
            "ensemble_decomposition_started": False,
        }

    return {
        "phase": "round6_independent_public_scene_replication",
        "status": "did_not_finish",
        "hard_lock_issue_comment": 5017827938,
        "execution_handoff_issue_comment": 5018136279,
        "scenes": scenes,
        "conclusion": (
            "The locked contiguous central windows repaired the Round 5 SfM "
            "failure: both scenes registered 20/20 train images. Both scenes "
            "then failed the next preregistered prerequisite on fit seed 0 "
            "(Truck 24.305 dB; Train 22.180 dB versus the 25 dB floor). Seeds "
            "1/2, Fisher, held-out registration, Gate B/B2, and ensemble "
            "decomposition were not run. This DNF neither replicates nor "
            "rejects Gate B on the public scenes."
        ),
    }


def render_figure(result: dict, output: Path) -> None:
    scenes = list(result["scenes"])
    registered = [result["scenes"][scene]["colmap"]["registered_train_images"] for scene in scenes]
    psnr = [
        result["scenes"][scene]["fit_hard_stop"]["seed0"]["final_pooled_psnr_db"]
        for scene in scenes
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 4.8), constrained_layout=True)
    bars = axes[0].bar(scenes, registered, color="#4c78a8")
    axes[0].bar_label(bars)
    axes[0].axhline(20, color="black", linestyle="--", label="required 20/20")
    axes[0].set_ylim(0, 21)
    axes[0].set_ylabel("registered train images")
    axes[0].set_title("SfM prerequisite: pass")
    axes[0].legend()

    bars = axes[1].bar(scenes, psnr, color="#e45756")
    axes[1].bar_label(bars, fmt="%.3f")
    axes[1].axhline(PSNR_FLOOR_DB, color="black", linestyle="--", label="required 25 dB")
    axes[1].set_ylim(0, 27)
    axes[1].set_ylabel("seed 0 final pooled train PSNR (dB)")
    axes[1].set_title("Fit prerequisite: DNF")
    axes[1].legend()
    fig.suptitle("Issue #48 Round 6 hard-stop result")
    fig.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    result = aggregate()
    output = HERE / "phase8_round6_result.json"
    figure = HERE / "round6_dnf_certificate.png"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    render_figure(result, figure)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
