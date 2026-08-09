"""Run every repository pytest file as a separately recorded shard."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "pytest_results.json"
SHARD_TIMEOUT_SECONDS = 1200


def counts(output: str) -> dict[str, int]:
    result = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "xpassed": 0}
    patterns = {
        "passed": r"(\d+) passed",
        "failed": r"(\d+) failed",
        "skipped": r"(\d+) skipped",
        "xfailed": r"(\d+) xfailed",
        "xpassed": r"(\d+) xpassed",
    }
    for key, pattern in patterns.items():
        matches = re.findall(pattern, output)
        if matches:
            result[key] = int(matches[-1])
    return result


def write(payload: dict) -> None:
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    files = sorted((ROOT / "tests").glob("test_*.py"))
    shards = []
    for index, test_file in enumerate(files, start=1):
        command = [sys.executable, "-m", "pytest", "-q", str(test_file.relative_to(ROOT))]
        started = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=SHARD_TIMEOUT_SECONDS,
                check=False,
            )
            shard = {
                "index": index,
                "test_file": str(test_file.relative_to(ROOT)),
                "command": " ".join(command),
                "exit_code": completed.returncode,
                "completed": True,
                "duration_seconds": time.monotonic() - started,
                **counts(completed.stdout + completed.stderr),
            }
        except subprocess.TimeoutExpired:
            shard = {
                "index": index,
                "test_file": str(test_file.relative_to(ROOT)),
                "command": " ".join(command),
                "exit_code": 124,
                "completed": False,
                "duration_seconds": time.monotonic() - started,
                "stop_reason": "timeout",
                **counts(""),
            }
        shards.append(shard)
        partial = {
            "schema_version": 1,
            "full_pytest": {
                "command": "python experiments/27_row1_classical/record_pytest.py",
                "completed": False,
                "exit_code": None,
                "shard_count": len(files),
                "completed_shard_count": len(shards),
                "shards": shards,
            },
        }
        write(partial)
        print(json.dumps(shard, sort_keys=True), flush=True)
        if not shard["completed"] or shard["exit_code"] != 0:
            break

    completed = len(shards) == len(files) and all(
        shard["completed"] and shard["exit_code"] == 0 for shard in shards
    )
    exit_code = 0 if completed else next(
        (shard["exit_code"] for shard in shards if shard["exit_code"] != 0),
        1,
    )
    totals = {
        key: sum(shard[key] for shard in shards)
        for key in ("passed", "failed", "skipped", "xfailed", "xpassed")
    }
    payload = {
        "schema_version": 1,
        "full_pytest": {
            "command": "python experiments/27_row1_classical/record_pytest.py",
            "completed": completed,
            "exit_code": exit_code,
            "shard_count": len(files),
            "completed_shard_count": len(shards),
            **totals,
            "shards": shards,
        },
    }
    write(payload)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
