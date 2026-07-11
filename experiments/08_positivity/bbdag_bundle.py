"""Write self-contained evidence bundles for fresh three-mode BB-dagger runs."""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


SCHEMA_VERSION = 1
REPO_ROOT = Path(__file__).resolve().parents[2]


def git_source_state(repo_root=REPO_ROOT):
    """Return the exact Git commit and whether tracked/untracked source is dirty."""
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return {
            "commit": None,
            "dirty": None,
            "unavailable_reason": f"{type(exc).__name__}: {exc}",
        }
    return {"commit": commit, "dirty": bool(status)}


def timestamped_bundle_path(root, stem):
    """Return a UTC-stamped path; the writer will reject a collision."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    return Path(root) / f"{timestamp}-{stem}"


def _sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_bbdag_bundle(path, *, data, state, trace, metadata):
    """Persist raw data, optimizer trace, fitted state, and run metadata.

    ``data`` is the homodyne ``[(theta, samples), ...]`` sequence used by the
    fitter. The destination must not exist, preventing accidental replacement
    of an earlier observation.
    """
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dictionary")
    if not data:
        raise ValueError("data must contain at least one angle group")

    theta = np.stack([np.asarray(group_theta, float) for group_theta, _ in data])
    samples = np.stack([np.asarray(group_samples, float) for _, group_samples in data])
    if theta.ndim != 2 or samples.ndim != 3:
        raise ValueError("data must have theta (G,M) and samples (G,S,M)")
    if theta.shape[0] != samples.shape[0] or theta.shape[1] != samples.shape[2]:
        raise ValueError("theta and sample group/mode dimensions must agree")

    z = np.asarray(state.z, complex)
    alpha = np.asarray(state.alpha, complex)
    if z.ndim != 1 or alpha.ndim != 2 or len(z) != alpha.shape[0]:
        raise ValueError("state must provide z (K,) and alpha (K,M)")

    trace_array = np.asarray(trace, float)
    if trace_array.size == 0:
        trace_array = np.empty((0, 2), float)
    if trace_array.ndim != 2 or trace_array.shape[1] != 2:
        raise ValueError("trace must contain (iteration, NLL) pairs")

    bundle = Path(path)
    bundle.mkdir(parents=True, exist_ok=False)
    arrays_path = bundle / "arrays.npz"
    np.savez_compressed(
        arrays_path,
        theta=theta,
        samples=samples,
        trace=trace_array,
        z=z,
        alpha=alpha,
    )

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": "three_mode_bbdag_run",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata,
        "arrays": {
            "path": arrays_path.name,
            "sha256": _sha256(arrays_path),
            "theta_shape": list(theta.shape),
            "samples_shape": list(samples.shape),
            "trace_shape": list(trace_array.shape),
            "z_shape": list(z.shape),
            "alpha_shape": list(alpha.shape),
        },
    }
    (bundle / "metadata.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return bundle
