"""Validate and render the committed Kawasaki pump-series result artifact.

``pump_results.json`` is the sole numerical authoring location.  This module
only checks that fixed artifact and derives the README block from its rows.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACT_PATH = HERE / "pump_results.json"
PLAN_PATH = HERE / "pump_series_plan.json"
MANIFEST_PATH = HERE / "source_manifest.json"
DEVELOPMENT_PATH = HERE / "pump_development.json"
RUNNER_PATH = HERE / "run_pump_series.py"
README_PATH = HERE / "README.md"

ARTIFACT_SHA256_NORMALIZED = (
    "4279a3dda0c08caf3b3466bb7fa2843468534a6c44680362278cb28dc25f83fe"
)
BEGIN = (
    "<!-- generated-block: do not edit "
    "(written by pump_result_summary.py from pump_results.json) -->"
)
END = "<!-- generated-block: end -->"

RESULT_KEYS = {
    "source_file",
    "series",
    "condition",
    "reshuffle_seed",
    "scale_arm",
    "phase_arm",
    "model",
    "mode_count",
    "fitted_eta",
    "train_nll",
    "test_nll",
    "delta_nll_vs_mle16",
    "ci_low",
    "ci_high",
    "classification",
    "convention_status",
    "epistemic_status",
}
TOP_LEVEL_KEYS = {
    "comparison_rows",
    "fit_attempts",
    "git",
    "plan_sha256",
    "publication_status",
    "result_rows",
    "review_record",
    "run_kind",
    "runner_sha256",
    "schema_version",
    "source_manifest_sha256",
}
GIT_KEYS = {"dirty", "head_sha"}
REVIEW_KEYS = {
    "development_artifact_path",
    "development_artifact_sha256",
    "development_execution_sha",
    "plan_sha256",
    "review_status",
    "review_url",
    "reviewed_git_sha",
    "runner_sha256",
    "schema_version",
    "source_manifest_sha256",
}
FIT_GROUP_KEYS = {
    "attempts",
    "model",
    "phase_arm",
    "reshuffle_seed",
    "scale_arm",
    "selected_init_seed",
    "source_file",
}
FIT_TRIAL_KEYS = {
    "final_100_iteration_train_nll_drop",
    "fitted_eta",
    "init_seed",
    "trace",
    "train_nll",
    "wall_seconds",
}
TRACE_KEYS = {"fitted_eta", "iteration", "train_nll"}


class PublicationError(ValueError):
    """The committed result or its generated surface is inconsistent."""


def _normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(_normalized_bytes(path)).hexdigest()


def _reject_constant(value: str):
    raise PublicationError(f"Non-finite JSON constant: {value}")


def load_json(path: Path) -> dict:
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"), parse_constant=_reject_constant
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublicationError(f"Invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise PublicationError(f"Expected a JSON object: {path}")
    return payload


def _finite(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PublicationError(f"{label} is not numeric")
    value = float(value)
    if not math.isfinite(value):
        raise PublicationError(f"{label} is not finite")
    return value


def _exact_keys(value, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise PublicationError(f"Unexpected {label} schema")


def _require_hex(value, digits: int, label: str) -> None:
    if not isinstance(value, str) or re.fullmatch(
        rf"[0-9a-f]{{{digits}}}", value
    ) is None:
        raise PublicationError(f"{label} is not a {digits}-digit lowercase hex id")


def _same_typed_json(left, right) -> bool:
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def _classification(ci_low: float, ci_high: float, plan: dict) -> str:
    rules = plan["primary_comparison"]["classification"]
    if ci_high < 0:
        return rules["ci_high_lt_zero"]
    if ci_low > 0:
        return rules["ci_low_gt_zero"]
    return rules["otherwise"]


def _convention_status(by_arm: dict[tuple[str, str], str]) -> str:
    scale_dep = (
        by_arm[("stored", "H1")] != by_arm[("sqrt2", "H1")]
        or by_arm[("stored", "H2")] != by_arm[("sqrt2", "H2")]
    )
    phase_dep = (
        by_arm[("stored", "H1")] != by_arm[("stored", "H2")]
        or by_arm[("sqrt2", "H1")] != by_arm[("sqrt2", "H2")]
    )
    if scale_dep and phase_dep:
        return "unit-and-phase-convention-dependent"
    if scale_dep:
        return "unit-convention-dependent"
    if phase_dep:
        return "phase-convention-dependent"
    return "convention-stable"


def _comparison_rows(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, int, str], list[dict]] = {}
    for row in rows:
        key = (row["source_file"], row["reshuffle_seed"], row["model"])
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
    for (source_file, seed, model), group in groups.items():
        by_arm = {
            f"{row['scale_arm']}/{row['phase_arm']}": row for row in group
        }
        if set(by_arm) != {"stored/H1", "stored/H2", "sqrt2/H1", "sqrt2/H2"}:
            raise PublicationError("Comparison group does not contain four arms")
        for quantity in quantities:
            values = {arm: row[quantity] for arm, row in by_arm.items()}
            if all(value is None for value in values.values()):
                continue
            primary = values["stored/H1"]
            differences = {
                arm: (
                    None
                    if value is None or primary is None or isinstance(value, str)
                    else float(value - primary)
                )
                for arm, value in values.items()
            }
            output.append(
                {
                    "source_file": source_file,
                    "reshuffle_seed": seed,
                    "model": model,
                    "quantity": quantity,
                    "arm_values": values,
                    "differences_vs_stored_H1": differences,
                    "comparison_status": (
                        None
                        if quantity == "classification"
                        else (
                            "same-across-arms"
                            if all(value == primary for value in values.values())
                            else "arm-specific-difference"
                        )
                    ),
                    "convention_status": (
                        group[0]["convention_status"]
                        if quantity == "classification"
                        else None
                    ),
                }
            )
    return output


def validate(payload: dict, artifact_path: Path = ARTIFACT_PATH) -> dict:
    if normalized_sha256(artifact_path) != ARTIFACT_SHA256_NORMALIZED:
        raise PublicationError("Published artifact SHA-256 does not match review")
    _exact_keys(payload, TOP_LEVEL_KEYS, "top-level artifact")
    if (
        type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != 1
        or payload.get("run_kind") != "execute"
        or payload.get("publication_status") != "descriptive-conditional"
    ):
        raise PublicationError("Unsupported result artifact identity")

    git = payload.get("git", {})
    review = payload.get("review_record", {})
    _exact_keys(git, GIT_KEYS, "git identity")
    _exact_keys(review, REVIEW_KEYS, "review record")
    if (
        type(review.get("schema_version")) is not int
        or review["schema_version"] != 1
    ):
        raise PublicationError("Unsupported review-record identity")
    _require_hex(git.get("head_sha"), 40, "git.head_sha")
    _require_hex(review.get("reviewed_git_sha"), 40, "reviewed_git_sha")
    _require_hex(
        review.get("development_execution_sha"), 40, "development_execution_sha"
    )
    for key in ("plan_sha256", "source_manifest_sha256", "runner_sha256"):
        _require_hex(payload.get(key), 64, key)
        _require_hex(review.get(key), 64, f"review.{key}")
    _require_hex(
        review.get("development_artifact_sha256"),
        64,
        "development_artifact_sha256",
    )
    if git.get("dirty") is not False or review.get("review_status") != "pass":
        raise PublicationError("Result was not produced from a clean passing review")
    if git.get("head_sha") != review.get("reviewed_git_sha"):
        raise PublicationError("Execution and reviewed git SHA differ")
    for key in ("plan_sha256", "source_manifest_sha256", "runner_sha256"):
        if payload.get(key) != review.get(key):
            raise PublicationError(f"Top-level and review {key} differ")
    if review.get("development_artifact_path") != (
        "experiments/32_kawasaki_data/pump_development.json"
    ):
        raise PublicationError("Unexpected development artifact path")
    if normalized_sha256(DEVELOPMENT_PATH) != review.get(
        "development_artifact_sha256"
    ):
        raise PublicationError("Development artifact SHA-256 differs")
    if normalized_sha256(PLAN_PATH) != payload.get("plan_sha256"):
        raise PublicationError("Committed plan differs from the result input")
    if normalized_sha256(MANIFEST_PATH) != payload.get("source_manifest_sha256"):
        raise PublicationError("Committed manifest differs from the result input")
    if normalized_sha256(RUNNER_PATH) != payload.get("runner_sha256"):
        raise PublicationError("Committed runner differs from the result input")
    review_url = review.get("review_url")
    if not isinstance(review_url, str) or not review_url.startswith(
        "https://github.com/orangewk/wigner-splat/pull/184#"
    ):
        raise PublicationError("Development review URL is not the fixed PR record")

    plan = load_json(PLAN_PATH)
    manifest = load_json(MANIFEST_PATH)
    models = {model["id"]: model for model in plan["models"]}
    sources = {
        row["name"]: row
        for row in manifest["files"]
        if row.get("series") == "pump_power"
        and row.get("condition", {}).get("pump_mw")
        in plan["development_pump_mw"] + plan["validation_pump_mw"]
    }
    seeds = plan["split"]["reshuffle_seeds"]
    scales = [row["id"] for row in plan["arms"]["scale"]]
    phases = [row["id"] for row in plan["arms"]["phase"]]
    model_ids = list(models)
    expected = set(product(sources, seeds, scales, phases, model_ids))

    rows = payload.get("result_rows")
    if not isinstance(rows, list):
        raise PublicationError("result_rows is not a list")
    if not all(isinstance(row, dict) for row in rows):
        raise PublicationError("result_rows contains a non-object")
    if any(type(row.get("reshuffle_seed")) is not int for row in rows):
        raise PublicationError("Result reshuffle_seed is not an integer")
    identities = {
        (
            row.get("source_file"),
            row.get("reshuffle_seed"),
            row.get("scale_arm"),
            row.get("phase_arm"),
            row.get("model"),
        )
        for row in rows
    }
    if len(rows) != len(identities) or identities != expected:
        raise PublicationError("Result rows do not cover the declared product once")

    primary_model = plan["primary_comparison"]["left_model"]
    for row in rows:
        identity = (
            row["source_file"],
            row["reshuffle_seed"],
            row["scale_arm"],
            row["phase_arm"],
            row["model"],
        )
        if set(row) != RESULT_KEYS:
            raise PublicationError(f"Unexpected result-row schema: {identity}")
        source = sources[row["source_file"]]
        if row["series"] != "pump_power" or not _same_typed_json(
            row["condition"], source["condition"]
        ):
            raise PublicationError(f"Source routing differs: {identity}")
        if (
            type(row["mode_count"]) is not int
            or row["mode_count"] != models[row["model"]]["mode_count"]
        ):
            raise PublicationError(f"Mode count differs from plan: {identity}")
        _finite(row["train_nll"], f"train_nll {identity}")
        _finite(row["test_nll"], f"test_nll {identity}")
        tags = ["convention-conditional"]
        if source["series_assignment"] == "inferred":
            tags.append("source-assignment-inferred")
        if row["model"] == primary_model:
            tags.insert(0, "descriptive-conditional-ci")
            eta = _finite(row["fitted_eta"], f"fitted_eta {identity}")
            if not 0.0 < eta < 1.0:
                raise PublicationError(f"fitted_eta is outside (0, 1): {identity}")
            delta = _finite(row["delta_nll_vs_mle16"], f"delta {identity}")
            low = _finite(row["ci_low"], f"ci_low {identity}")
            high = _finite(row["ci_high"], f"ci_high {identity}")
            if low > high or not math.isfinite(delta):
                raise PublicationError(f"Invalid comparison interval: {identity}")
            expected_class = _classification(low, high, plan)
            if row["classification"] != expected_class:
                raise PublicationError(
                    f"Classification is not data-derived: {identity}"
                )
            if expected_class == "unresolved":
                tags.append("unresolved")
        else:
            if row["fitted_eta"] is not None or any(
                row[key] is not None
                for key in (
                    "delta_nll_vs_mle16",
                    "ci_low",
                    "ci_high",
                    "classification",
                    "convention_status",
                )
            ):
                raise PublicationError(
                    f"Non-primary row carries verdict fields: {identity}"
                )
        if row["epistemic_status"] != tags:
            raise PublicationError(f"Epistemic tags differ from routing: {identity}")

    primary = [row for row in rows if row["model"] == primary_model]
    right_model = plan["primary_comparison"]["right_model"]
    for source_file, seed, scale, phase in product(sources, seeds, scales, phases):
        by_model = {
            row["model"]: row
            for row in rows
            if row["source_file"] == source_file
            and row["reshuffle_seed"] == seed
            and row["scale_arm"] == scale
            and row["phase_arm"] == phase
        }
        expected_delta = (
            by_model[primary_model]["test_nll"] - by_model[right_model]["test_nll"]
        )
        if not math.isclose(
            by_model[primary_model]["delta_nll_vs_mle16"],
            expected_delta,
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise PublicationError(
                f"Delta is not derived from model test NLLs: "
                f"{source_file}/{seed}/{scale}/{phase}"
            )
    for source_file, seed in product(sources, seeds):
        group = [
            row
            for row in primary
            if row["source_file"] == source_file and row["reshuffle_seed"] == seed
        ]
        by_arm = {
            (row["scale_arm"], row["phase_arm"]): row["classification"]
            for row in group
        }
        status = _convention_status(by_arm)
        if any(row["convention_status"] != status for row in group):
            raise PublicationError(
                f"Convention status is not classification-derived: {source_file}/{seed}"
            )

    comparisons = payload.get("comparison_rows")
    if comparisons != _comparison_rows(rows):
        raise PublicationError("Comparison rows are not derived from result rows")

    attempts = payload.get("fit_attempts")
    if not isinstance(attempts, list):
        raise PublicationError("fit_attempts is not a list")
    for group in attempts:
        _exact_keys(group, FIT_GROUP_KEYS, "fit-attempt group")
        if type(group["reshuffle_seed"]) is not int:
            raise PublicationError("Fit-attempt reshuffle_seed is not an integer")
        if type(group["selected_init_seed"]) is not int:
            raise PublicationError("selected_init_seed is not an integer")
    expected_attempts = set(product(sources, seeds, scales, phases))
    attempt_ids = {
        (
            row.get("source_file"),
            row.get("reshuffle_seed"),
            row.get("scale_arm"),
            row.get("phase_arm"),
        )
        for row in attempts
    }
    if len(attempts) != len(attempt_ids) or attempt_ids != expected_attempts:
        raise PublicationError("Fit-attempt groups do not cover each primary arm once")
    for group in attempts:
        if group.get("model") != primary_model:
            raise PublicationError("Fit-attempt group has the wrong model")
        trials = group.get("attempts", [])
        expected_init_seeds = models[primary_model]["init_seeds"]
        if not isinstance(trials, list):
            raise PublicationError("Fit-attempt trials is not a list")
        for trial in trials:
            _exact_keys(trial, FIT_TRIAL_KEYS, "fit trial")
            if type(trial["init_seed"]) is not int:
                raise PublicationError("Fit trial init_seed is not an integer")
        trial_seeds = [trial["init_seed"] for trial in trials]
        if (
            len(trials) != len(expected_init_seeds)
            or trial_seeds != expected_init_seeds
        ):
            raise PublicationError("Fit-attempt group has the wrong init seeds")
        selected = min(trials, key=lambda trial: trial["train_nll"])["init_seed"]
        if group.get("selected_init_seed") != selected:
            raise PublicationError("Selected init is not the minimum train NLL")
        for trial in trials:
            _finite(trial["train_nll"], "attempt train_nll")
            eta = _finite(trial["fitted_eta"], "attempt fitted_eta")
            if not 0.0 < eta < 1.0:
                raise PublicationError("Attempt fitted_eta is outside (0, 1)")
            wall_seconds = _finite(trial.get("wall_seconds"), "attempt wall_seconds")
            if wall_seconds < 0.0:
                raise PublicationError("Attempt wall_seconds is negative")
            _finite(trial["final_100_iteration_train_nll_drop"], "attempt drop")
            trace = trial.get("trace")
            if not isinstance(trace, list) or not trace:
                raise PublicationError("Fit trace is not a nonempty list")
            for point in trace:
                _exact_keys(point, TRACE_KEYS, "fit trace point")
                if type(point["iteration"]) is not int:
                    raise PublicationError("Trace iteration is not an integer")
            if [row.get("iteration") for row in trace] != list(
                range(25, 501, 25)
            ):
                raise PublicationError("Fit trace does not reach the declared budget")
            for point in trace:
                _finite(point.get("train_nll"), "trace train_nll")
                trace_eta = _finite(point.get("fitted_eta"), "trace fitted_eta")
                if not 0.0 < trace_eta < 1.0:
                    raise PublicationError("Trace fitted_eta is outside (0, 1)")
            if (
                trial["train_nll"] != trace[-1]["train_nll"]
                or trial["fitted_eta"] != trace[-1]["fitted_eta"]
                or trial["final_100_iteration_train_nll_drop"]
                != trace[-5]["train_nll"] - trace[-1]["train_nll"]
            ):
                raise PublicationError("Fit-attempt summary differs from its trace")
        selected_trial = next(
            trial for trial in trials if trial["init_seed"] == selected
        )
        result = next(
            row
            for row in primary
            if row["source_file"] == group["source_file"]
            and row["reshuffle_seed"] == group["reshuffle_seed"]
            and row["scale_arm"] == group["scale_arm"]
            and row["phase_arm"] == group["phase_arm"]
        )
        if (
            result["train_nll"] != selected_trial["train_nll"]
            or result["fitted_eta"] != selected_trial["fitted_eta"]
        ):
            raise PublicationError("Published primary fit differs from selected init")

    return {
        "result_rows": len(rows),
        "comparison_rows": len(comparisons),
        "fit_attempt_groups": len(attempts),
        "classifications": Counter(row["classification"] for row in primary),
    }


def render(payload: dict) -> str:
    stats = validate(payload)
    primary = [
        row for row in payload["result_rows"] if row["classification"] is not None
    ]
    by_source_seed = {}
    for row in primary:
        by_source_seed.setdefault(
            (row["source_file"], row["reshuffle_seed"]), []
        ).append(row)

    lines = [BEGIN]
    lines.append(
        "- Artifact identity: normalized SHA-256 "
        f"`{ARTIFACT_SHA256_NORMALIZED}`; execution code SHA "
        f"`{payload['git']['head_sha']}`."
    )
    counts = stats["classifications"]
    lines.append(
        "- Arm-indexed primary classifications: "
        f"win {counts['win']}; loss {counts['loss']}; "
        f"unresolved {counts['unresolved']} (total {sum(counts.values())})."
    )
    stable_groups = [
        group
        for group in by_source_seed.values()
        if group[0]["convention_status"] == "convention-stable"
    ]
    stable_wins = sum(
        all(row["classification"] == "win" for row in group)
        for group in stable_groups
    )
    lines.append(
        "- Convention-stable condition/seed groups: "
        f"{len(stable_groups)} of {len(by_source_seed)}; classified win among "
        f"them: {stable_wins} of {len(stable_groups)}."
    )
    lines.extend(
        [
            "",
            "| pump condition | reshuffle seed | stored/H1 | stored/H2 | "
            "sqrt2/H1 | sqrt2/H2 | convention status |",
            "| --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    ordered = sorted(
        by_source_seed.items(),
        key=lambda item: (
            item[1][0]["condition"]["pump_mw"],
            item[0][1],
        ),
    )
    for (_source, seed), group in ordered:
        arms = {
            f"{row['scale_arm']}/{row['phase_arm']}": row for row in group
        }
        exemplar = group[0]
        condition = f"{exemplar['condition']['pump_mw']} mW"
        if "source-assignment-inferred" in exemplar["epistemic_status"]:
            condition += " (source assignment inferred)"
        lines.append(
            f"| {condition} | {seed} | "
            f"{arms['stored/H1']['classification']} | "
            f"{arms['stored/H2']['classification']} | "
            f"{arms['sqrt2/H1']['classification']} | "
            f"{arms['sqrt2/H2']['classification']} | "
            f"{exemplar['convention_status']} |"
        )

    robust_wins = []
    for source in {row["source_file"] for row in primary}:
        group = [row for row in primary if row["source_file"] == source]
        if all(row["classification"] == "win" for row in group):
            robust_wins.append(group[0]["condition"]["pump_mw"])
    robust = ", ".join(f"{pump} mW" for pump in sorted(robust_wins)) or "none"
    lines.extend(
        [
            "",
            "- Conditions classified win in all four convention arms and both "
            f"reshuffle seeds: **{robust}**.",
            END,
        ]
    )
    return "\n".join(lines)


def _readme_block(readme: str) -> str:
    if readme.count(BEGIN) != 1 or readme.count(END) != 1:
        raise PublicationError("README must contain exactly one generated block")
    start = readme.find(BEGIN)
    stop = readme.find(END)
    if start < 0 or stop < start:
        raise PublicationError("README is missing the generated-block markers")
    return readme[start : stop + len(END)]


def write_into_readme(payload: dict) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    old = _readme_block(text)
    README_PATH.write_text(text.replace(old, render(payload), 1), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = load_json(ARTIFACT_PATH)
    if args.write:
        write_into_readme(payload)
    elif _readme_block(README_PATH.read_text(encoding="utf-8")) != render(payload):
        raise PublicationError("README block differs; rerun with --write")
    print(json.dumps(validate(payload), indent=2, default=dict, sort_keys=True))


if __name__ == "__main__":
    main()
