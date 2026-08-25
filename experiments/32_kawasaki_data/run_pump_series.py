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
DEVELOPMENT_ARTIFACT_RELATIVE = Path(
    "experiments/32_kawasaki_data/pump_development.json"
)

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from kawasaki_data import (  # noqa: E402
    LoadedCondition,
    file_entries,
    load_condition,
    load_manifest,
)
from wigner_splat.bbdagS import (  # noqa: E402
    MixedSqueezedKetState,
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
    return sha256_text_bytes(path.read_bytes())


def sha256_bytes(snapshot: bytes) -> str:
    return hashlib.sha256(snapshot).hexdigest()


def normalize_text_snapshot(snapshot: bytes) -> bytes:
    return snapshot.replace(b"\r\n", b"\n")


def sha256_text_bytes(snapshot: bytes) -> str:
    return sha256_bytes(normalize_text_snapshot(snapshot))


def read_json_snapshot(path: Path) -> tuple[bytes, dict[str, Any], str]:
    snapshot = path.read_bytes()
    try:
        payload = json.loads(snapshot.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PumpSeriesError(f"Invalid JSON snapshot: {path}") from exc
    if not isinstance(payload, dict):
        raise PumpSeriesError(f"JSON snapshot is not an object: {path}")
    return snapshot, payload, sha256_text_bytes(snapshot)


def load_plan(
    path: Path = PLAN_PATH,
    *,
    raw: bytes | None = None,
) -> dict[str, Any]:
    snapshot = path.read_bytes() if raw is None else raw
    plan = json.loads(snapshot.decode("utf-8"))
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


def git_blob_bytes(revision: str, relative_path: Path) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{relative_path.as_posix()}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise PumpSeriesError(
            f"Missing git blob {revision}:{relative_path.as_posix()}"
        )
    return result.stdout


def require_git_ancestor(ancestor: str, descendant: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise PumpSeriesError(
            f"Development execution SHA {ancestor} is not an ancestor of "
            f"reviewed SHA {descendant}"
        )


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


def validate_fit_attempt(
    attempt: Any,
    *,
    expected_seed: int,
    model: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(attempt, dict):
        raise PumpSeriesError("Fit attempt is not an object")
    if attempt.get("init_seed") != expected_seed:
        raise PumpSeriesError(
            f"Fit attempt init_seed {attempt.get('init_seed')!r} != "
            f"slice seed {expected_seed}"
        )
    for field in ("train_nll", "fitted_eta", "wall_seconds"):
        value = attempt.get(field)
        if not isinstance(value, (int, float)) or not np.isfinite(value):
            raise PumpSeriesError(f"Fit attempt {field} is not finite")
    if not 0.0 < attempt["fitted_eta"] < 1.0:
        raise PumpSeriesError("Fit attempt fitted_eta is outside (0, 1)")
    trace = attempt.get("trace")
    expected_iterations = list(range(25, model["iters"] + 1, 25))
    if (
        not isinstance(trace, list)
        or [row.get("iteration") for row in trace
            if isinstance(row, dict)] != expected_iterations
        or len(trace) != len(expected_iterations)
    ):
        raise PumpSeriesError("Fit attempt trace iterations are incomplete")
    for row in trace:
        for field in ("train_nll", "fitted_eta"):
            value = row.get(field)
            if not isinstance(value, (int, float)) or not np.isfinite(value):
                raise PumpSeriesError(f"Fit trace {field} is not finite")
    if (
        attempt["train_nll"] != trace[-1]["train_nll"]
        or attempt["fitted_eta"] != trace[-1]["fitted_eta"]
    ):
        raise PumpSeriesError("Fit attempt final values do not match its trace")
    recomputed_drop = convergence_drop(trace, model["iters"])
    recorded_drop = attempt.get("final_100_iteration_train_nll_drop")
    if (
        recomputed_drop is None
        or not isinstance(recorded_drop, (int, float))
        or not np.isfinite(recorded_drop)
        or not np.isclose(recorded_drop, recomputed_drop, rtol=0.0, atol=1e-15)
    ):
        raise PumpSeriesError("Fit attempt convergence drop is inconsistent")
    return attempt


def encode_complex_array(array: np.ndarray) -> dict[str, Any]:
    values = np.asarray(array, complex)
    if not np.all(np.isfinite(values)):
        raise PumpSeriesError("Cannot checkpoint a non-finite complex array")
    return {
        "shape": list(values.shape),
        "real": np.real(values).ravel().tolist(),
        "imag": np.imag(values).ravel().tolist(),
    }


def decode_complex_array(
    payload: Any,
    *,
    expected_shape: tuple[int, ...],
    label: str,
) -> np.ndarray:
    if not isinstance(payload, dict) or payload.get("shape") != list(
        expected_shape
    ):
        raise PumpSeriesError(f"Checkpoint {label} shape is invalid")
    size = int(np.prod(expected_shape))
    real = payload.get("real")
    imag = payload.get("imag")
    if (
        not isinstance(real, list)
        or not isinstance(imag, list)
        or len(real) != size
        or len(imag) != size
    ):
        raise PumpSeriesError(f"Checkpoint {label} values are incomplete")
    try:
        values = np.asarray(real, float) + 1j * np.asarray(imag, float)
    except (TypeError, ValueError) as exc:
        raise PumpSeriesError(f"Checkpoint {label} values are invalid") from exc
    if not np.all(np.isfinite(values)):
        raise PumpSeriesError(f"Checkpoint {label} contains non-finite values")
    return values.reshape(expected_shape)


def encode_bb_state(state: MixedSqueezedKetState) -> dict[str, Any]:
    return {
        "z": encode_complex_array(state.z),
        "alpha": encode_complex_array(state.alpha),
        "xi": encode_complex_array(state.xi),
    }


def decode_bb_state(payload: Any, model: dict[str, Any]) -> MixedSqueezedKetState:
    if not isinstance(payload, dict):
        raise PumpSeriesError("BB checkpoint state is not an object")
    R, K, M = model["R"], model["K"], model["mode_count"]
    state = MixedSqueezedKetState(
        z=decode_complex_array(
            payload.get("z"), expected_shape=(R, K), label="BB z"
        ),
        alpha=decode_complex_array(
            payload.get("alpha"),
            expected_shape=(R, K, M),
            label="BB alpha",
        ),
        xi=decode_complex_array(
            payload.get("xi"),
            expected_shape=(R, K, M),
            label="BB xi",
        ),
    )
    norm = state.norm_sq()
    if not np.isfinite(norm) or norm <= 0.0:
        raise PumpSeriesError("BB checkpoint state has invalid norm")
    return state


def decode_mle_rho(payload: Any, model: dict[str, Any]) -> np.ndarray:
    n_max = model["n_max"]
    rho = decode_complex_array(
        payload,
        expected_shape=(n_max, n_max),
        label=f"{model['id']} rho",
    )
    if not np.allclose(rho, rho.conj().T, rtol=0.0, atol=1e-10):
        raise PumpSeriesError(f"{model['id']} checkpoint rho is not Hermitian")
    if not np.isclose(np.trace(rho), 1.0, rtol=0.0, atol=1e-10):
        raise PumpSeriesError(f"{model['id']} checkpoint rho trace is not one")
    if np.min(np.linalg.eigvalsh(rho)) < -1e-8:
        raise PumpSeriesError(f"{model['id']} checkpoint rho is not PSD")
    return rho


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


def reconstruct_mle(train, model, *, max_iters: int | None = None):
    centers, targets = histogram_targets(train, bins=model["bins"])
    return mle_reconstruct(
        centers,
        targets,
        n_max=model["n_max"],
        max_iters=model["max_iters"] if max_iters is None else max_iters,
    )


def evaluate_mle(rho, iterations, train, test):
    train_vector = per_sample_nll_mle(rho, train)
    test_vector = per_sample_nll_mle(rho, test)
    return {
        "rho": rho,
        "iterations": iterations,
        "train_nll": float(np.mean(train_vector)),
        "test_nll": float(np.mean(test_vector)),
        "test_vector": test_vector,
    }


def fit_mle(train, test, model, *, max_iters: int | None = None):
    rho, iterations = reconstruct_mle(train, model, max_iters=max_iters)
    return evaluate_mle(rho, iterations, train, test)


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


def load_pump_conditions(
    data_dir: Path,
    pumps: list[int],
    manifest: dict[str, Any],
):
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
    return [load_condition(data_dir / row["name"], manifest) for row in selected]


def _checkpoint_name(split_seed: int, scale_id: str, phase_id: str, init_seed: int):
    return (
        f"split{split_seed}_{scale_id}_{phase_id}_init{init_seed}.json"
    )


def _validate_checkpoint_identity(
    path: Path,
    payload: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    for field, value in expected.items():
        if payload.get(field) != value:
            raise PumpSeriesError(
                f"Checkpoint {path.name} field {field} "
                f"{payload.get(field)!r} != {value!r}"
            )


def _load_development_checkpoint(
    path: Path,
    expected: dict[str, Any],
    model: dict[str, Any],
):
    _snapshot, payload, _digest = read_json_snapshot(path)
    _validate_checkpoint_identity(path, payload, expected)
    return validate_fit_attempt(
        payload.get("attempt"),
        expected_seed=expected["init_seed"],
        model=model,
    )


def _execute_checkpoint_name(
    source_file: str,
    split_seed: int,
    scale_id: str,
    phase_id: str,
    model_id: str,
    init_seed: int | None = None,
) -> str:
    source_key = sha256_bytes(source_file.encode("utf-8"))[:10]
    init_key = "" if init_seed is None else f"_init{init_seed}"
    return (
        f"{Path(source_file).stem}_{source_key}_split{split_seed}_"
        f"{scale_id}_{phase_id}_{model_id}{init_key}.json"
    )


def _load_execute_bb_checkpoint(
    path: Path,
    expected: dict[str, Any],
    model: dict[str, Any],
    train,
) -> dict[str, Any]:
    _snapshot, payload, _digest = read_json_snapshot(path)
    _validate_checkpoint_identity(path, payload, expected)
    attempt = validate_fit_attempt(
        payload.get("attempt"),
        expected_seed=expected["init_seed"],
        model=model,
    )
    state = decode_bb_state(payload.get("state"), model)
    recomputed_nll = float(
        nll_lossy_mixed(state, as_bbdag(train), attempt["fitted_eta"])
    )
    if not np.isclose(
        recomputed_nll,
        attempt["train_nll"],
        rtol=1e-12,
        atol=1e-12,
    ):
        raise PumpSeriesError(
            f"Checkpoint {path.name} BB state does not reproduce train NLL"
        )
    return {"state": state, "attempt": attempt}


def _load_execute_mle_checkpoint(
    path: Path,
    expected: dict[str, Any],
    model: dict[str, Any],
) -> dict[str, Any]:
    _snapshot, payload, _digest = read_json_snapshot(path)
    _validate_checkpoint_identity(path, payload, expected)
    iterations = payload.get("iterations")
    if (
        isinstance(iterations, bool)
        or not isinstance(iterations, int)
        or not 1 <= iterations <= model["max_iters"]
    ):
        raise PumpSeriesError(
            f"Checkpoint {path.name} MLE iterations are invalid"
        )
    return {
        "rho": decode_mle_rho(payload.get("rho"), model),
        "iterations": iterations,
    }


def run_development(
    data_dir: Path,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    *,
    smoke: bool,
    checkpoint_dir: Path | None = None,
    checkpoint_identity: dict[str, Any] | None = None,
):
    loaded_conditions = load_pump_conditions(
        data_dir, plan["development_pump_mw"], manifest
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
                            checkpoint_path,
                            expected,
                            models["bbdag_r4k4"],
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
                        validate_fit_attempt(
                            attempt,
                            expected_seed=init_seed,
                            model=models["bbdag_r4k4"],
                        )
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


def validate_development_artifact(
    development: dict[str, Any],
    development_snapshot: bytes,
    development_path: Path,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    *,
    plan_sha256: str,
    runner_sha256: str,
    manifest_sha256: str,
    reviewed_git_sha: str,
) -> str:
    try:
        snapshot_payload = json.loads(development_snapshot.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PumpSeriesError("Development artifact snapshot is invalid JSON") from exc
    if snapshot_payload != development:
        raise PumpSeriesError(
            "Development object does not come from the supplied byte snapshot"
        )
    expected_artifact_path = (ROOT / DEVELOPMENT_ARTIFACT_RELATIVE).resolve()
    if development_path.resolve() != expected_artifact_path:
        raise PumpSeriesError(
            "Development artifact must be the committed protocol path"
        )
    if (
        development.get("schema_version") != 1
        or development.get("run_kind") != "development"
        or development.get("publication_status") != "train-only-development"
    ):
        raise PumpSeriesError("Development artifact identity is invalid")
    expected_hashes = {
        "plan_sha256": plan_sha256,
        "runner_sha256": runner_sha256,
        "source_manifest_sha256": manifest_sha256,
    }
    for field, value in expected_hashes.items():
        if development.get(field) != value:
            raise PumpSeriesError(
                f"Development artifact {field} does not match current input"
            )
    execution_git = development.get("git")
    if (
        not isinstance(execution_git, dict)
        or execution_git.get("dirty") is not False
        or not isinstance(execution_git.get("head_sha"), str)
    ):
        raise PumpSeriesError("Development artifact lacks a clean execution SHA")
    execution_sha = execution_git["head_sha"]
    require_git_ancestor(execution_sha, reviewed_git_sha)

    tracked_inputs = (
        (PLAN_PATH.relative_to(ROOT), plan_sha256),
        (RUNNER_PATH.relative_to(ROOT), runner_sha256),
        (MANIFEST_PATH.relative_to(ROOT), manifest_sha256),
    )
    for relative_path, expected_hash in tracked_inputs:
        for revision in (execution_sha, reviewed_git_sha):
            actual = sha256_text_bytes(git_blob_bytes(revision, relative_path))
            if actual != expected_hash:
                raise PumpSeriesError(
                    f"{relative_path.as_posix()} at {revision} does not match "
                    "the development input snapshot"
                )
    reviewed_artifact = git_blob_bytes(
        reviewed_git_sha, DEVELOPMENT_ARTIFACT_RELATIVE
    )
    if normalize_text_snapshot(reviewed_artifact) != normalize_text_snapshot(
        development_snapshot
    ):
        raise PumpSeriesError(
            "Development artifact bytes do not match the reviewed git blob"
        )

    candidates = [
        row for row in manifest["files"]
        if row.get("role") == "quadrature"
        and row.get("series") == plan["series"]
        and row.get("condition", {}).get("pump_mw")
        in plan["development_pump_mw"]
    ]
    if len(candidates) != 1:
        raise PumpSeriesError("Development source identity is not unique")
    source = candidates[0]
    records = development.get("records")
    if not isinstance(records, list):
        raise PumpSeriesError("Development records are missing")
    expected_identities = {
        (seed, scale["id"], phase["id"])
        for seed in plan["split"]["reshuffle_seeds"]
        for scale, phase in arm_pairs(plan)
    }
    actual_identities = {
        (row.get("reshuffle_seed"), row.get("scale_arm"), row.get("phase_arm"))
        for row in records if isinstance(row, dict)
    }
    if len(records) != len(expected_identities) or actual_identities != expected_identities:
        raise PumpSeriesError("Development artifact does not cover each arm once")

    bb_model = model_map(plan)["bbdag_r4k4"]
    selected_drops = []
    for row in records:
        if (
            row.get("source_file") != source["name"]
            or row.get("series") != source["series"]
            or row.get("condition") != source["condition"]
            or row.get("model") != "bbdag_r4k4"
        ):
            raise PumpSeriesError("Development record source/model identity drifted")
        attempts = row.get("attempts")
        if not isinstance(attempts, list) or len(attempts) != len(
            bb_model["init_seeds"]
        ):
            raise PumpSeriesError("Development record has incomplete init attempts")
        for expected_seed, attempt in zip(bb_model["init_seeds"], attempts):
            validate_fit_attempt(
                attempt,
                expected_seed=expected_seed,
                model=bb_model,
            )
        selected = min(
            attempts,
            key=lambda attempt: (attempt["train_nll"], attempt["init_seed"]),
        )
        selected_fields = {
            "selected_init_seed": selected["init_seed"],
            "selected_train_nll": selected["train_nll"],
            "selected_fitted_eta": selected["fitted_eta"],
            "selected_final_100_iteration_train_nll_drop": selected[
                "final_100_iteration_train_nll_drop"
            ],
        }
        for field, value in selected_fields.items():
            if row.get(field) != value:
                raise PumpSeriesError(
                    f"Development record {field} is not selected by train NLL"
                )
        selected_drops.append(
            selected["final_100_iteration_train_nll_drop"]
        )

    gate_plan = plan["development_gate"]
    recomputed_pass = all(
        np.isfinite(value) and value <= gate_plan["maximum_drop"]
        for value in selected_drops
    )
    expected_gate = {
        "evaluated": True,
        "passed": bool(recomputed_pass),
        "metric": gate_plan["metric"],
        "maximum_drop": gate_plan["maximum_drop"],
        "pass_rule": gate_plan["pass_rule"],
    }
    if development.get("development_gate") != expected_gate:
        raise PumpSeriesError("Development gate is not computed from attempts")
    if not recomputed_pass:
        raise PumpSeriesError("Development convergence gate did not pass")
    return execution_sha


def validate_review_record(
    review: dict[str, Any],
    development: dict[str, Any],
    development_snapshot: bytes,
    development_path: Path,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    plan_sha256: str,
    runner_sha256: str,
    manifest_sha256: str,
    development_sha256: str,
    git: dict[str, Any],
):
    required = {
        "schema_version",
        "review_status",
        "review_url",
        "reviewed_git_sha",
        "plan_sha256",
        "runner_sha256",
        "source_manifest_sha256",
        "development_artifact_sha256",
        "development_artifact_path",
        "development_execution_sha",
    }
    if required.difference(review):
        raise PumpSeriesError("Review record is incomplete")
    if (
        review["schema_version"] != 1
        or review["review_status"] != "pass"
        or not isinstance(review["review_url"], str)
        or not review["review_url"]
    ):
        raise PumpSeriesError("Validation requires a passing review record")
    expected = {
        "reviewed_git_sha": git["head_sha"],
        "plan_sha256": plan_sha256,
        "runner_sha256": runner_sha256,
        "source_manifest_sha256": manifest_sha256,
        "development_artifact_sha256": development_sha256,
        "development_artifact_path": DEVELOPMENT_ARTIFACT_RELATIVE.as_posix(),
    }
    for field, value in expected.items():
        if review[field] != value:
            raise PumpSeriesError(
                f"Review record {field} {review[field]!r} != {value!r}"
            )
    execution_sha = validate_development_artifact(
        development,
        development_snapshot,
        development_path,
        plan,
        manifest,
        plan_sha256=plan_sha256,
        runner_sha256=runner_sha256,
        manifest_sha256=manifest_sha256,
        reviewed_git_sha=git["head_sha"],
    )
    if review["development_execution_sha"] != execution_sha:
        raise PumpSeriesError(
            "Review record development_execution_sha does not match artifact"
        )
    return review


def run_execute(
    data_dir: Path,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    *,
    checkpoint_dir: Path,
    checkpoint_identity: dict[str, Any],
):
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    pumps = plan["development_pump_mw"] + plan["validation_pump_mw"]
    loaded_conditions = load_pump_conditions(data_dir, pumps, manifest)
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
                bb_model = models["bbdag_r4k4"]
                bb_fitted = []
                for init_seed in bb_model["init_seeds"]:
                    expected = {
                        **checkpoint_identity,
                        "source_file": loaded.source_file,
                        "source_series": loaded.series,
                        "source_condition": loaded.condition,
                        "reshuffle_seed": split_seed,
                        "scale_arm": scale["id"],
                        "phase_arm": phase["id"],
                        "model": bb_model["id"],
                        "init_seed": init_seed,
                    }
                    checkpoint_path = checkpoint_dir / _execute_checkpoint_name(
                        loaded.source_file,
                        split_seed,
                        scale["id"],
                        phase["id"],
                        bb_model["id"],
                        init_seed,
                    )
                    if not checkpoint_path.is_file():
                        fitted = fit_bbdag(
                            train,
                            bb_model,
                            init_seeds=[init_seed],
                        )
                        write_payload(
                            checkpoint_path,
                            {
                                **expected,
                                "attempt": fitted["attempts"][0],
                                "state": encode_bb_state(fitted["state"]),
                            },
                        )
                        print(
                            f"checkpoint wrote: {checkpoint_path.name} "
                            f"train_nll={fitted['train_nll']:.6f}",
                            flush=True,
                        )
                    else:
                        print(
                            f"checkpoint reuse: {checkpoint_path.name}",
                            flush=True,
                        )
                    loaded_bb = _load_execute_bb_checkpoint(
                        checkpoint_path,
                        expected,
                        bb_model,
                        train,
                    )
                    attempt = loaded_bb["attempt"]
                    bb_fitted.append((
                        attempt["train_nll"],
                        init_seed,
                        loaded_bb["state"],
                        attempt["fitted_eta"],
                        attempt,
                    ))
                selected_bb = min(bb_fitted, key=lambda row: (row[0], row[1]))
                bb = {
                    "state": selected_bb[2],
                    "fitted_eta": selected_bb[3],
                    "train_nll": selected_bb[0],
                    "selected_init_seed": selected_bb[1],
                    "attempts": [row[4] for row in bb_fitted],
                }
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
                    model = models[model_id]
                    expected = {
                        **checkpoint_identity,
                        "source_file": loaded.source_file,
                        "source_series": loaded.series,
                        "source_condition": loaded.condition,
                        "reshuffle_seed": split_seed,
                        "scale_arm": scale["id"],
                        "phase_arm": phase["id"],
                        "model": model_id,
                        "init_seed": None,
                    }
                    checkpoint_path = checkpoint_dir / _execute_checkpoint_name(
                        loaded.source_file,
                        split_seed,
                        scale["id"],
                        phase["id"],
                        model_id,
                    )
                    if not checkpoint_path.is_file():
                        rho, iterations = reconstruct_mle(train, model)
                        write_payload(
                            checkpoint_path,
                            {
                                **expected,
                                "iterations": int(iterations),
                                "rho": encode_complex_array(rho),
                            },
                        )
                        print(
                            f"checkpoint wrote: {checkpoint_path.name} "
                            f"iterations={iterations}",
                            flush=True,
                        )
                    else:
                        print(
                            f"checkpoint reuse: {checkpoint_path.name}",
                            flush=True,
                        )
                    loaded_mle = _load_execute_mle_checkpoint(
                        checkpoint_path,
                        expected,
                        model,
                    )
                    fits[model_id] = evaluate_mle(
                        loaded_mle["rho"],
                        loaded_mle["iterations"],
                        train,
                        test,
                    )
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
    execute.add_argument("--checkpoint-dir", type=Path, required=True)
    args = parser.parse_args()

    official = args.command != "smoke"
    git = git_identity(require_clean=official)
    plan_snapshot = PLAN_PATH.read_bytes()
    plan_sha256 = sha256_text_bytes(plan_snapshot)
    plan = load_plan(raw=plan_snapshot)
    manifest_snapshot = MANIFEST_PATH.read_bytes()
    manifest_sha256 = sha256_text_bytes(manifest_snapshot)
    manifest = load_manifest(raw=manifest_snapshot)
    runner_snapshot = RUNNER_PATH.read_bytes()
    runner_sha256 = sha256_text_bytes(runner_snapshot)
    if official:
        tracked_snapshots = (
            (PLAN_PATH.relative_to(ROOT), plan_snapshot),
            (MANIFEST_PATH.relative_to(ROOT), manifest_snapshot),
            (RUNNER_PATH.relative_to(ROOT), runner_snapshot),
        )
        for relative_path, snapshot in tracked_snapshots:
            if normalize_text_snapshot(
                git_blob_bytes(git["head_sha"], relative_path)
            ) != normalize_text_snapshot(snapshot):
                raise PumpSeriesError(
                    f"Runtime snapshot differs from fixed SHA: "
                    f"{relative_path.as_posix()}"
                )
    metadata = {
        "schema_version": 1,
        "run_kind": args.command,
        "plan_sha256": plan_sha256,
        "source_manifest_sha256": manifest_sha256,
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
            manifest,
            smoke=args.command == "smoke",
            checkpoint_dir=(
                args.checkpoint_dir.resolve()
                if args.command == "development" else None
            ),
            checkpoint_identity=checkpoint_identity,
        )
    else:
        _review_snapshot, review_payload, review_sha256 = read_json_snapshot(
            args.review_record.resolve()
        )
        development_snapshot, development_payload, development_sha256 = (
            read_json_snapshot(args.development_artifact.resolve())
        )
        review = validate_review_record(
            review_payload,
            development_payload,
            development_snapshot,
            args.development_artifact.resolve(),
            plan,
            manifest,
            plan_sha256,
            runner_sha256,
            manifest_sha256,
            development_sha256,
            git,
        )
        metadata["review_record"] = review
        final_git = git_identity(require_clean=True)
        if final_git != git:
            raise PumpSeriesError(
                "Git identity changed after review validation"
            )
        checkpoint_identity = {
            "schema_version": 1,
            "checkpoint_kind": "pump-execute-fit",
            "plan_sha256": plan_sha256,
            "runner_sha256": runner_sha256,
            "source_manifest_sha256": manifest_sha256,
            "reviewed_git_sha": git["head_sha"],
            "development_artifact_sha256": development_sha256,
            "review_record_sha256": review_sha256,
        }
        _manifest, result = run_execute(
            args.data_dir.resolve(),
            plan,
            manifest,
            checkpoint_dir=args.checkpoint_dir.resolve(),
            checkpoint_identity=checkpoint_identity,
        )
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
