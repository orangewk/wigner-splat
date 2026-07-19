"""Download pinned Round 5 Tanks and Temples archives with resume support."""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREPARE = HERE / "prepare_round5_data.py"


def _load_prepare():
    spec = importlib.util.spec_from_file_location("round5_prepare", PREPARE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def download(scene: str, destination: Path) -> Path:
    prepare = _load_prepare()
    spec = prepare.SCENES[scene]
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / f"{scene}.zip"
    partial = destination / f"{scene}.zip.partial"
    if target.exists():
        if (
            target.stat().st_size == spec.archive_bytes
            and prepare.sha256(target) == spec.archive_sha256
        ):
            print(f"verified existing {target}")
            return target
        raise RuntimeError(f"Refusing mismatched existing archive: {target}")

    offset = partial.stat().st_size if partial.exists() else 0
    if offset > spec.archive_bytes:
        raise RuntimeError(f"Partial archive is too large: {partial}")
    request = urllib.request.Request(spec.source_url)
    if offset:
        request.add_header("Range", f"bytes={offset}-")
    mode = "ab" if offset else "xb"
    with urllib.request.urlopen(request) as response, partial.open(mode) as stream:
        if offset and response.status != 206:
            raise RuntimeError("Server did not honor the resume Range request")
        shutil.copyfileobj(response, stream, length=1024 * 1024)

    if partial.stat().st_size != spec.archive_bytes:
        raise RuntimeError(
            f"Incomplete {scene} archive retained at {partial}: "
            f"{partial.stat().st_size}/{spec.archive_bytes} bytes"
        )
    if prepare.sha256(partial) != spec.archive_sha256:
        raise RuntimeError(f"SHA-256 mismatch; retained for diagnosis: {partial}")
    partial.rename(target)
    print(f"downloaded and verified {target}")
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=("Truck", "Train"), required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    download(args.scene, args.destination)


if __name__ == "__main__":
    main()
