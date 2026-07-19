"""Integrity guard for shared fit-seed ensemble artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Sequence

import torch


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_shared_ensemble(
    directory: Path,
    heldout_names: Sequence[str],
    fit_seeds: Sequence[int] = (0, 1, 2),
    ddof: int = 1,
) -> dict:
    """Validate identity and bytes of every map before an ensemble is reused."""
    result_path = directory / "result.json"
    if not result_path.is_file():
        raise RuntimeError(f"Shared ensemble record is missing: {result_path}")
    record = json.loads(result_path.read_text(encoding="utf-8"))
    expected_names = list(heldout_names)
    expected_seeds = list(fit_seeds)
    checks = (
        (record.get("status") == "complete", "status"),
        (record.get("heldout_names") == expected_names, "heldout_names"),
        (record.get("fit_seeds") == expected_seeds, "fit_seeds"),
        (record.get("ddof") == ddof, "ddof"),
        (
            record.get("shared_single_map_across_fit_seed_comparisons") is True,
            "shared_single_map_across_fit_seed_comparisons",
        ),
    )
    for passed, field in checks:
        if not passed:
            raise RuntimeError(f"Shared ensemble {field} mismatch")

    hashes = record.get("map_sha256")
    if not isinstance(hashes, dict) or set(hashes) != set(expected_names):
        raise RuntimeError("Shared ensemble map_sha256 keys mismatch")
    for view_index, view_name in enumerate(expected_names):
        path = directory / f"view_{view_index}.pt"
        if not path.is_file() or sha256(path) != hashes[view_name]:
            raise RuntimeError(f"Shared ensemble map hash mismatch: {view_name}")
        payload = torch.load(path, map_location="cpu", weights_only=True)
        if (
            payload.get("view_index") != view_index
            or payload.get("view_name") != view_name
            or payload.get("fit_seeds") != expected_seeds
            or payload.get("ddof") != ddof
            or "sigma_ensemble" not in payload
        ):
            raise RuntimeError(f"Shared ensemble map metadata mismatch: {view_name}")
    return record
