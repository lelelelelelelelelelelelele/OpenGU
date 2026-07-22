"""Shared CLI/provenance helpers for IM benchmark runners."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[2]
EXECUTION_TOKEN = "IM-SELECTOR-A"


def parse_int_list(value: str) -> List[int]:
    parsed = [int(item.strip()) for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("integer list must be non-empty")
    return parsed


def parse_float_list(value: str) -> List[float]:
    parsed = [
        float(item.strip()) for item in str(value).split(",") if item.strip()
    ]
    if not parsed:
        raise ValueError("float list must be non-empty")
    return parsed


def parse_name_list(value: str) -> List[str]:
    parsed = [item.strip() for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("name list must be non-empty")
    return parsed


def git_provenance() -> Dict[str, Any]:
    def run(*args: str) -> str:
        completed = subprocess.run(
            ["git"] + list(args),
            cwd=str(REPO_ROOT),
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    status = run("status", "--porcelain")
    branch = run("branch", "--show-current")
    return {
        "sha": run("rev-parse", "HEAD"),
        "branch": branch,
        "dirty": bool(status),
        "status_porcelain": status.splitlines(),
    }


def assert_execution_authorized(
    *,
    execute: bool,
    approval_token: str,
    formal: bool,
) -> Dict[str, Any]:
    provenance = git_provenance()
    if not execute:
        return provenance
    if str(approval_token) != EXECUTION_TOKEN:
        raise RuntimeError(
            "execution requires --approval-token {0}".format(EXECUTION_TOKEN)
        )
    if formal:
        if provenance["branch"] != "main":
            raise RuntimeError("formal run requires branch main")
        if provenance["dirty"]:
            raise RuntimeError("formal run requires a clean worktree")
    return provenance


def write_json_atomic(path: Path, value: Any, *, overwrite: bool) -> None:
    target = Path(path).expanduser().resolve(strict=False)
    if target.exists() and not overwrite:
        raise FileExistsError(
            "output already exists; pass --overwrite explicitly: {0}".format(
                target
            )
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    descriptor, temp_name = tempfile.mkstemp(
        prefix=target.name + ".",
        suffix=".tmp",
        dir=str(target.parent),
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, str(target))
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def budgets_from_ratios(candidate_count: int, ratios: Iterable[float]) -> List[int]:
    values = []
    for ratio in ratios:
        ratio = float(ratio)
        if not 0.0 < ratio <= 1.0:
            raise ValueError("budget ratios must be in (0, 1]")
        values.append(max(1, int(candidate_count * ratio)))
    return sorted(set(values))
