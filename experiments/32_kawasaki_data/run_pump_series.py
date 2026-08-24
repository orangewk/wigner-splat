"""Execute the predeclared Kawasaki pump-power comparison in gated stages.

``smoke`` reads only the 01 mW development condition with a tiny, explicitly
non-interpretable budget. ``development`` reads only 01 mW and evaluates the
train-only convergence gate. ``execute`` reads all four pump conditions only
after a passing fixed-SHA review record is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PLAN_PATH = HERE / "pump_series_plan.json"
MANIFEST_PATH = HERE / "source_manifest.json"
RUNNER_PATH = Path(__file__).resolve()

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from kawasaki_data import (  # noqa: E402
    LoadedCondition,
    file_entries,
    load_condition,
    load_manifest,
)
from wigner_splat.bbdagS import (  # noqa: E402
    fit_bbdagS_lossy_mixed,
    lossy_pdf_mixed,
    nll_lossy_mixed,
)
from wigner_splat.fit import histogram_targets  # noqa: E402
from wigner_splat.fock import marginal_from_rho  # noqa: E402
from wigner_splat.mle import mle_reconstruct  # noqa: E402


class PumpSeriesError(ValueError):
    """The execution plan, review gate, or result surface is invalid."""


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_plan(path: Path = PLAN_PATH) -> dict[str, Any]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "series",
        "development_pump_mw",
        "validation_pump_mw",
        "split",
        "arms",
        "models",
        "primary_comparison",
        "development_gate",
        "smoke_budget",
        "vocabulary",
    }
    missing = required.difference(plan)
    if missing:
        raise PumpSeriesError(f"Plan missing keys: {sorted(missing)}")
    if plan["schema_version"] != 1 or plan["series"] != "pump_power":
        raise PumpSeriesError("Unsupported pump-series plan identity")
    if plan["split"].get("unit") != "within_phase":
        raise PumpSeriesError("Split unit must be within_phase")
    train_fraction = plan["split"].get("train_fraction")
    if not isinstance(train_fraction, (int, float)) or not 0 < train_fraction < 1:
        raise PumpSeriesError("train_fraction must be in (0, 1)")
    if plan["split"].get("reshuffle_seeds") != [0, 1]:
        raise PumpSeriesError("Official reshuffle seeds must be [0, 1]")

    scale = plan["arms"].get("scale", [])
    phase = plan["arms"].get("phase", [])
    if [row.get("id") for row in scale] != ["stored", "sqrt2"]:
        raise PumpSeriesError("Scale arms must be stored and sqrt2")
    if [row.get("id") for row in phase] != ["H1", "H2"]:
        raise PumpSeriesError("Phase arms must be H1 and H2")
    if scale[0].get("multiplier") != 1.0 or not np.isclose(
        scale[1].get("multiplier"), np.sqrt(2.0), rtol=0.0, atol=1e-15
    ):
        raise PumpSeriesError("Scale multipliers do not match the fixed arms")
    if phase[0].get("sign_flip_min_stored_phase_deg") is not None:
        raise PumpSeriesError("H1 must not flip stored samples")
    if phase[1].get("sign_flip_min_stored_phase_deg") != 180:
        raise PumpSeriesError("H2 must flip stored phases at or above 180 deg")

    models = {row.get("id"): row for row in plan["models"]}
    if set(models) != {"bbdag_r4k4", "mle16", "mle10"}:
        raise PumpSeriesError("Model ids do not match the fixed comparison")
    bb = models["bbdag_r4k4"]
    if (
        bb.get("kind") != "bbdag_mixed_lossy"
        or (bb.get("R"), bb.get("K"), bb.get("mode_count")) != (4, 4, 1)
        or bb.get("init_seeds") != [0, 1, 2]
        or bb.get("selection") != "minimum_train_nll"
    ):
        raise PumpSeriesError("BB-dagger model does not match the fixed plan")
    for model_id, n_max in (("mle16", 16), ("mle10", 10)):
        model = models[model_id]
        if (
            model.get("kind") != "fixed_mle"
            or model.get("n_max") != n_max
            or model.get("bins") != 80
            or model.get("mode_count") != 1
        ):
            raise PumpSeriesError(f"{model_id} does not match the fixed plan")
    comparison = plan["primary_comparison"]
    if (
        comparison.get("left_model") != "bbdag_r4k4"
        or comparison.get("right_model") != "mle16"
        or comparison.get("metric") != "held_out_per_sample_nll"
    ):
        raise PumpSeriesError("Primary comparison identity is invalid")

    vocabulary = plan["vocabulary"]
    expected_vocabulary = {
        "classification": {"win", "loss", "unresolved"},
        "convention_status": {
            "convention-stable",
            "unit-convention-dependent",
            "phase-convention-dependent",
            "unit-and-phase-convention-dependent",
        },
        "comparison_status": {
            "same-across-arms",
            "arm-specific-difference",
        },
        "epistemic_status": {
            "descriptive-conditional-ci",
            "source-assignment-inferred",
            "convention-conditional",
            "unresolved",
        },
    }
    for field, expected in expected_vocabulary.items():
        if set(vocabulary.get(field, [])) != expected:
            raise PumpSeriesError(f"Uncontrolled {field} vocabulary")
    return plan


def git_identity(*, require_clean: bool) -> dict[str, Any]:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if require_clean and status:
        raise PumpSeriesError(
            "Official execution requires a clean fixed-SHA worktree; "
            f"dirty entries: {status}"
        )
    return {"head_sha": head, "dirty": bool(status)}


def model_map(plan: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in plan["models"]}


def arm_pairs(plan: dict[str, Any]):
    for scale in plan["arms"]["scale"]:
        for phase in plan["arms"]["phase"]:
            yield scale, phase


def split_within_phase(
    data: tuple[tuple[float, np.ndarray], ...],
    seed: int,
    train_fraction: float,
) -> tuple[list[tuple[float, np.ndarray]], list[tuple[float, np.ndarray]]]:
    rng = np.random.default_rng(seed)
    train, test = [], []
    for theta, samples in data:
        indices = rng.permutation(len(samples))
        n_train = int(train_fraction * len(samples))
        train.append((theta, samples[indices[:n_train]].copy()))
        test.append((theta, samples[indices[n_train:]].copy()))
    return train, test


def apply_arm(
    data: list[tuple[float, np.ndarray]],
    scale_arm: dict[str, Any],
    phase_arm: dict[str, Any],
) -> list[tuple[float, np.ndarray]]:
    multiplier = float(scale_arm["multiplier"])
    flip_min = phase_arm["sign_flip_min_stored_phase_deg"]
    transformed = []
    for theta, samples in data:
        sign = -1.0 if (
            flip_min is not None
            and np.rad2deg(theta) >= float(flip_min) - 1e-12
        ) else 1.0
        transformed.append((theta, np.asarray(samples, float) * multiplier * sign))
    return transformed


def as_bbdag(data: list[tuple[float, np.ndarray]]):
    return [(np.array([theta]), samples[:, None]) for theta, samples in data]


def per_sample_nll_bb(state, eta, data):
    return np.concatenate([
        -np.log(np.maximum(lossy_pdf_mixed(
            state, samples[:, None], np.array([theta]), eta
        ), 1e-300))
        for theta, samples in data
    ])


def per_sample_nll_mle(rho, data):
    return np.concatenate([
        -np.log(np.maximum(marginal_from_rho(rho, samples, theta), 1e-300))
        for theta, samples in data
    ])


def convergence_drop(trace: list[dict[str, float]], iters: int) -> float | None:
    if not trace or iters < 100:
        return None
    final = trace[-1]
    eligible = [row for row in trace if row["iteration"] <= final["iteration"] - 100]
    if not eligible:
        return None
    return float(eligible[-1]["train_nll"] - final["train_nll"])


def fit_bbdag(
    train,
    model,
    *,
    init_seeds: list[int] | None = None,
    iters: int | None = None,
):
    seeds = model["init_seeds"] if init_seeds is None else init_seeds
    iterations = model["iters"] if iters is None else iters
    bb_train = as_bbdag(train)
    attempts = []
    fitted = []
    for seed in seeds:
        trace: list[dict[str, float]] = []

        def callback(iteration, value, eta):
            trace.append({
                "iteration": int(iteration),
                "train_nll": float(value),
                "fitted_eta": float(eta),
            })

        started = time.perf_counter()
        state, eta = fit_bbdagS_lossy_mixed(
            bb_train,
            R=model["R"],
            K=model["K"],
            M=model["mode_count"],
            eta0=model["eta0"],
            fit_eta=model["fit_eta"],
            iters=iterations,
            lr=model["learning_rate"],
            seed=seed,
            callback=callback,
        )
        train_nll = float(nll_lossy_mixed(state, bb_train, eta))
        attempt = {
            "init_seed": seed,
            "train_nll": train_nll,
            "fitted_eta": float(eta),
            "final_100_iteration_train_nll_drop": convergence_drop(
                trace, iterations
            ),
            "trace": trace,
            "wall_seconds": float(time.perf_counter() - started),
        }
        attempts.append(attempt)
        fitted.append((train_nll, seed, state, float(eta), attempt))
    selected = min(fitted, key=lambda row: (row[0], row[1]))
    return {
        "state": selected[2],
        "fitted_eta": selected[3],
        "train_nll": selected[0],
        "selected_init_seed": selected[1],
        "selected_convergence_drop": selected[4][
            "final_100_iteration_train_nll_drop"
        ],
        "attempts": attempts,
    }


def fit_mle(train, test, model, *, max_iters: int | None = None):
    centers, targets = histogram_targets(train, bins=model["bins"])
    rho, iterations = mle_reconstruct(
        centers,
        targets,
        n_max=model["n_max"],
        max_iters=model["max_iters"] if max_iters is None else max_iters,
    )
    train_vector = per_sample_nll_mle(rho, train)
    test_vector = per_sample_nll_mle(rho, test)
    return {
        "rho": rho,
        "iterations": iterations,
        "train_nll": float(np.mean(train_vector)),
        "test_nll": float(np.mean(test_vector)),
        "test_vector": test_vector,
    }


def paired_bootstrap_ci(
    difference: np.ndarray,
    *,
    replicates: int,
    seed: int,
    quantiles: list[float],
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    n = len(difference)
    means = np.empty(replicates, float)
    for index in range(replicates):
        means[index] = np.mean(difference[rng.integers(0, n, n)])
    return tuple(float(value) for value in np.quantile(means, quantiles))


def classify(ci_low: float, ci_high: float, plan: dict[str, Any]) -> str:
    rules = plan["primary_comparison"]["classification"]
    if ci_high < 0:
        result = rules["ci_high_lt_zero"]
    elif ci_low > 0:
        result = rules["ci_low_gt_zero"]
    else:
        result = rules["otherwise"]
    if result not in plan["vocabulary"]["classification"]:
        raise PumpSeriesError(f"Uncontrolled classification: {result}")
    return result


def convention_status(classifications, plan):
    scale_dep = (
        classifications[("stored", "H1")] != classifications[("sqrt2", "H1")]
        or classifications[("stored", "H2")] != classifications[("sqrt2", "H2")]
    )
    phase_dep = (
        classifications[("stored", "H1")] != classifications[("stored", "H2")]
        or classifications[("sqrt2", "H1")] != classifications[("sqrt2", "H2")]
    )
    if scale_dep and phase_dep:
        status = "unit-and-phase-convention-dependent"
    elif scale_dep:
        status = "unit-convention-dependent"
    elif phase_dep:
        status = "phase-convention-dependent"
    else:
        status = "convention-stable"
    if status not in plan["vocabulary"]["convention_status"]:
        raise PumpSeriesError(f"Uncontrolled convention status: {status}")
    return status


def source_assignment(manifest, source_file):
    return file_entries(manifest)[source_file]["series_assignment"]


def result_row(
    loaded,
    split_seed,
    scale_id,
    phase_id,
    model,
    fit,
    comparison,
    status,
    manifest,
    plan,
):
    is_primary = model["id"] == plan["primary_comparison"]["left_model"]
    epistemic = ["convention-conditional"]
    if source_assignment(manifest, loaded.source_file) == "inferred":
        epistemic.append("source-assignment-inferred")
    if is_primary:
        epistemic.insert(0, "descriptive-conditional-ci")
        if comparison["classification"] == "unresolved":
            epistemic.append("unresolved")
    allowed = set(plan["vocabulary"]["epistemic_status"])
    if not set(epistemic).issubset(allowed):
        raise PumpSeriesError(f"Uncontrolled epistemic status: {epistemic}")
    return {
        "source_file": loaded.source_file,
        "series": loaded.series,
        "condition": loaded.condition,
        "reshuffle_seed": split_seed,
        "scale_arm": scale_id,
        "phase_arm": phase_id,
        "model": model["id"],
        "mode_count": model["mode_count"],
        "fitted_eta": fit.get("fitted_eta"),
        "train_nll": fit["train_nll"],
        "test_nll": fit["test_nll"],
        "delta_nll_vs_mle16": comparison["delta"] if is_primary else None,
        "ci_low": comparison["ci_low"] if is_primary else None,
        "ci_high": comparison["ci_high"] if is_primary else None,
        "classification": comparison["classification"] if is_primary else None,
        "convention_status": status if is_primary else None,
        "epistemic_status": epistemic,
    }


def arm_value_key(scale_id: str, phase_id: str) -> str:
    return f"{scale_id}/{phase_id}"


def build_comparison_rows(rows, plan):
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for row in rows:
        key = (
            row["source_file"],
            row["reshuffle_seed"],
            row["model"],
        )
        groups.setdefault(key, []).append(row)
    quantities = (
        "mode_count",
        "fitted_eta",
        "train_nll",
        "test_nll",
        "delta_nll_vs_mle16",
        "ci_low",
        "ci_high",
        "classification",
    )
    output = []
    for (source_file, split_seed, model_id), group in groups.items():
        by_arm = {
            arm_value_key(row["scale_arm"], row["phase_arm"]): row
            for row in group
        }
        if len(by_arm) != 4:
            raise PumpSeriesError("Comparison table requires all four arms")
        for quantity in quantities:
            values = {key: row[quantity] for key, row in by_arm.items()}
            if all(value is None for value in values.values()):
                continue
            primary = values["stored/H1"]
            differences = {
                key: (None if value is None or primary is None
                      or isinstance(value, str) else float(value - primary))
                for key, value in values.items()
            }
            if quantity == "classification":
                conv_status = group[0]["convention_status"]
                comp_status = None
            else:
                same = all(value == primary for value in values.values())
                comp_status = (
                    "same-across-arms" if same else "arm-specific-difference"
                )
                if comp_status not in plan["vocabulary"]["comparison_status"]:
                    raise PumpSeriesError(
                        f"Uncontrolled comparison status: {comp_status}"
                    )
                conv_status = None
            output.append({
                "source_file": source_file,
                "reshuffle_seed": split_seed,
                "model": model_id,
                "quantity": quantity,
                "arm_values": values,
                "differences_vs_stored_H1": differences,
                "comparison_status": comp_status,
                "convention_status": conv_status,
            })
    return output


def load_pump_conditions(data_dir: Path, pumps: list[int]):
    manifest = load_manifest()
    selected = []
    for entry in manifest["files"]:
        if (
            entry.get("role") == "quadrature"
            and entry.get("series") == "pump_power"
            and entry.get("condition", {}).get("pump_mw") in pumps
        ):
            selected.append(entry)
    if sorted(row["condition"]["pump_mw"] for row in selected) != sorted(pumps):
        raise PumpSeriesError(f"Pump source selection is incomplete: {pumps}")
    return manifest, [load_condition(data_dir / row["name"], manifest) for row in selected]


def _checkpoint_name(split_seed: int, scale_id: str, phase_id: str, init_seed: int):
    return (
        f"split{split_seed}_{scale_id}_{phase_id}_init{init_seed}.json"
    )


def _load_development_checkpoint(path: Path, expected: dict[str, Any]):
    payload = json.loads(path.read_text(encoding="utf-8"))
    for field, value in expected.items():
        if payload.get(field) != value:
            raise PumpSeriesError(
                f"Checkpoint {path.name} field {field} "
                f"{payload.get(field)!r} != {value!r}"
            )
    attempt = payload.get("attempt")
    train_nll = attempt.get("train_nll") if isinstance(attempt, dict) else None
    if (
        not isinstance(train_nll, (int, float))
        or not np.isfinite(train_nll)
    ):
        raise PumpSeriesError(f"Checkpoint {path.name} has no finite attempt")
    return attempt


def run_development(
    data_dir: Path,
    plan: dict[str, Any],
    *,
    smoke: bool,
    checkpoint_dir: Path | None = None,
    checkpoint_identity: dict[str, Any] | None = None,
):
    manifest, loaded_conditions = load_pump_conditions(
        data_dir, plan["development_pump_mw"]
    )
    if len(loaded_conditions) != 1:
        raise PumpSeriesError("Development must load exactly one condition")
    loaded = loaded_conditions[0]
    data = loaded.data
    budget = plan["smoke_budget"] if smoke else None
    if smoke:
        data = tuple(
            (theta, samples[:budget["samples_per_phase"]].copy())
            for theta, samples in data
        )
    seeds = budget["reshuffle_seeds"] if smoke else plan["split"]["reshuffle_seeds"]
    models = model_map(plan)
    records = []
    if not smoke:
        if checkpoint_dir is None or checkpoint_identity is None:
            raise PumpSeriesError(
                "Development requires a checkpoint directory and identity"
            )
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
    for split_seed in seeds:
        canonical_train, canonical_test = split_within_phase(
            data, split_seed, plan["split"]["train_fraction"]
        )
        for scale, phase in arm_pairs(plan):
            train = apply_arm(canonical_train, scale, phase)
            test = apply_arm(canonical_test, scale, phase)
            if smoke:
                bb = fit_bbdag(
                    train,
                    models["bbdag_r4k4"],
                    init_seeds=budget["bbdag_init_seeds"],
                    iters=budget["bbdag_iters"],
                )
            else:
                attempts = []
                for init_seed in models["bbdag_r4k4"]["init_seeds"]:
                    checkpoint_path = checkpoint_dir / _checkpoint_name(
                        split_seed, scale["id"], phase["id"], init_seed
                    )
                    expected = {
                        **checkpoint_identity,
                        "source_file": loaded.source_file,
                        "reshuffle_seed": split_seed,
                        "scale_arm": scale["id"],
                        "phase_arm": phase["id"],
                        "init_seed": init_seed,
                    }
                    if checkpoint_path.is_file():
                        attempt = _load_development_checkpoint(
                            checkpoint_path, expected
                        )
                        print(
                            f"checkpoint reuse: {checkpoint_path.name}",
                            flush=True,
                        )
                    else:
                        fitted = fit_bbdag(
                            train,
                            models["bbdag_r4k4"],
                            init_seeds=[init_seed],
                        )
                        attempt = fitted["attempts"][0]
                        write_payload(
                            checkpoint_path,
                            {**expected, "attempt": attempt},
                        )
                        print(
                            f"checkpoint wrote: {checkpoint_path.name} "
                            f"train_nll={attempt['train_nll']:.6f}",
                            flush=True,
                        )
                    attempts.append(attempt)
                selected = min(
                    attempts,
                    key=lambda row: (row["train_nll"], row["init_seed"]),
                )
                bb = {
                    "selected_init_seed": selected["init_seed"],
                    "train_nll": selected["train_nll"],
                    "fitted_eta": selected["fitted_eta"],
                    "selected_convergence_drop": selected[
                        "final_100_iteration_train_nll_drop"
                    ],
                    "attempts": attempts,
                }
            record = {
                "source_file": loaded.source_file,
                "series": loaded.series,
                "condition": loaded.condition,
                "reshuffle_seed": split_seed,
                "scale_arm": scale["id"],
                "phase_arm": phase["id"],
                "model": "bbdag_r4k4",
                "selected_init_seed": bb["selected_init_seed"],
                "selected_train_nll": bb["train_nll"],
                "selected_fitted_eta": bb["fitted_eta"],
                "selected_final_100_iteration_train_nll_drop": (
                    bb["selected_convergence_drop"]
                ),
                "attempts": bb["attempts"],
            }
            if smoke:
                record["smoke_test_nll"] = float(np.mean(
                    per_sample_nll_bb(bb["state"], bb["fitted_eta"], test)
                ))
                record["mle_smoke"] = {}
                for model_id in ("mle16", "mle10"):
                    fit = fit_mle(
                        train,
                        test,
                        models[model_id],
                        max_iters=budget["mle_max_iters"],
                    )
                    record["mle_smoke"][model_id] = {
                        "train_nll": fit["train_nll"],
                        "test_nll": fit["test_nll"],
                        "iterations": fit["iterations"],
                    }
            records.append(record)
    if smoke:
        gate = {
            "evaluated": False,
            "passed": None,
            "reason": "smoke budget is non-interpretable",
        }
    else:
        maximum = plan["development_gate"]["maximum_drop"]
        values = [
            row["selected_final_100_iteration_train_nll_drop"] for row in records
        ]
        passed = all(
            value is not None and np.isfinite(value) and value <= maximum
            for value in values
        )
        gate = {
            "evaluated": True,
            "passed": bool(passed),
            "metric": plan["development_gate"]["metric"],
            "maximum_drop": maximum,
            "pass_rule": plan["development_gate"]["pass_rule"],
        }
    return manifest, {
        "publication_status": (
            "non-interpretable-smoke" if smoke else "train-only-development"
        ),
        "development_gate": gate,
        "records": records,
    }


def validate_review_record(
    review_path: Path,
    development_path: Path,
    plan_sha256: str,
    runner_sha256: str,
    git: dict[str, Any],
):
    review = json.loads(review_path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "review_status",
        "review_url",
        "reviewed_git_sha",
        "plan_sha256",
        "runner_sha256",
        "development_artifact_sha256",
    }
    if required.difference(review):
        raise PumpSeriesError("Review record is incomplete")
    if review["schema_version"] != 1 or review["review_status"] != "pass":
        raise PumpSeriesError("Validation requires a passing review record")
    expected = {
        "reviewed_git_sha": git["head_sha"],
        "plan_sha256": plan_sha256,
        "runner_sha256": runner_sha256,
        "development_artifact_sha256": sha256_path(development_path),
    }
    for field, value in expected.items():
        if review[field] != value:
            raise PumpSeriesError(
                f"Review record {field} {review[field]!r} != {value!r}"
            )
    development = json.loads(development_path.read_text(encoding="utf-8"))
    if development.get("development_gate", {}).get("passed") is not True:
        raise PumpSeriesError("Development convergence gate did not pass")
    return review


def run_execute(data_dir: Path, plan: dict[str, Any]):
    pumps = plan["development_pump_mw"] + plan["validation_pump_mw"]
    manifest, loaded_conditions = load_pump_conditions(data_dir, pumps)
    models = model_map(plan)
    raw_results = []
    fit_attempts = []
    for loaded in loaded_conditions:
        for split_seed in plan["split"]["reshuffle_seeds"]:
            canonical_train, canonical_test = split_within_phase(
                loaded.data, split_seed, plan["split"]["train_fraction"]
            )
            for scale, phase in arm_pairs(plan):
                train = apply_arm(canonical_train, scale, phase)
                test = apply_arm(canonical_test, scale, phase)
                bb = fit_bbdag(train, models["bbdag_r4k4"])
                bb_vector = per_sample_nll_bb(
                    bb["state"], bb["fitted_eta"], test
                )
                fits = {
                    "bbdag_r4k4": {
                        "fitted_eta": bb["fitted_eta"],
                        "train_nll": bb["train_nll"],
                        "test_nll": float(np.mean(bb_vector)),
                        "test_vector": bb_vector,
                    }
                }
                fit_attempts.append({
                    "source_file": loaded.source_file,
                    "reshuffle_seed": split_seed,
                    "scale_arm": scale["id"],
                    "phase_arm": phase["id"],
                    "model": "bbdag_r4k4",
                    "selected_init_seed": bb["selected_init_seed"],
                    "attempts": bb["attempts"],
                })
                for model_id in ("mle16", "mle10"):
                    fits[model_id] = fit_mle(train, test, models[model_id])
                difference = bb_vector - fits["mle16"]["test_vector"]
                bootstrap = plan["primary_comparison"]["bootstrap"]
                ci_low, ci_high = paired_bootstrap_ci(
                    difference,
                    replicates=bootstrap["replicates"],
                    seed=bootstrap["seed"],
                    quantiles=bootstrap["quantiles"],
                )
                comparison = {
                    "delta": float(np.mean(difference)),
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                    "classification": classify(ci_low, ci_high, plan),
                }
                raw_results.append({
                    "loaded": loaded,
                    "split_seed": split_seed,
                    "scale_id": scale["id"],
                    "phase_id": phase["id"],
                    "fits": fits,
                    "comparison": comparison,
                })

    statuses = {}
    for loaded in loaded_conditions:
        for split_seed in plan["split"]["reshuffle_seeds"]:
            subset = [
                row for row in raw_results
                if row["loaded"].source_file == loaded.source_file
                and row["split_seed"] == split_seed
            ]
            classifications = {
                (row["scale_id"], row["phase_id"]): row["comparison"][
                    "classification"
                ]
                for row in subset
            }
            statuses[(loaded.source_file, split_seed)] = convention_status(
                classifications, plan
            )

    rows = []
    for raw in raw_results:
        status = statuses[(raw["loaded"].source_file, raw["split_seed"])]
        for model_id in ("bbdag_r4k4", "mle16", "mle10"):
            rows.append(result_row(
                raw["loaded"],
                raw["split_seed"],
                raw["scale_id"],
                raw["phase_id"],
                models[model_id],
                raw["fits"][model_id],
                raw["comparison"],
                status,
                manifest,
                plan,
            ))
    return manifest, {
        "publication_status": "descriptive-conditional",
        "result_rows": rows,
        "comparison_rows": build_comparison_rows(rows, plan),
        "fit_attempts": fit_attempts,
    }


def write_payload(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise PumpSeriesError(f"Refusing to overwrite existing artifact: {path}")
    partial = path.with_suffix(path.suffix + ".partial")
    partial.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    partial.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("smoke", "development"):
        stage = sub.add_parser(command)
        stage.add_argument("--data-dir", type=Path, required=True)
        stage.add_argument("--output", type=Path, required=True)
        if command == "development":
            stage.add_argument("--checkpoint-dir", type=Path, required=True)
    execute = sub.add_parser("execute")
    execute.add_argument("--data-dir", type=Path, required=True)
    execute.add_argument("--output", type=Path, required=True)
    execute.add_argument("--development-artifact", type=Path, required=True)
    execute.add_argument("--review-record", type=Path, required=True)
    args = parser.parse_args()

    plan = load_plan()
    plan_sha256 = sha256_path(PLAN_PATH)
    runner_sha256 = sha256_path(RUNNER_PATH)
    official = args.command != "smoke"
    git = git_identity(require_clean=official)
    metadata = {
        "schema_version": 1,
        "run_kind": args.command,
        "plan_sha256": plan_sha256,
        "source_manifest_sha256": sha256_path(MANIFEST_PATH),
        "runner_sha256": runner_sha256,
        "git": git,
    }
    if args.command in {"smoke", "development"}:
        checkpoint_identity = {
            "schema_version": 1,
            "plan_sha256": plan_sha256,
            "runner_sha256": runner_sha256,
            "git_head_sha": git["head_sha"],
        }
        _manifest, result = run_development(
            args.data_dir.resolve(),
            plan,
            smoke=args.command == "smoke",
            checkpoint_dir=(
                args.checkpoint_dir.resolve()
                if args.command == "development" else None
            ),
            checkpoint_identity=checkpoint_identity,
        )
    else:
        review = validate_review_record(
            args.review_record.resolve(),
            args.development_artifact.resolve(),
            plan_sha256,
            runner_sha256,
            git,
        )
        metadata["review_record"] = review
        _manifest, result = run_execute(args.data_dir.resolve(), plan)
    payload = {**metadata, **result}
    write_payload(args.output.resolve(), payload)
    print(json.dumps({
        "output": str(args.output.resolve()),
        "run_kind": args.command,
        "publication_status": payload["publication_status"],
        "development_gate": payload.get("development_gate"),
        "result_row_count": len(payload.get("result_rows", [])),
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
