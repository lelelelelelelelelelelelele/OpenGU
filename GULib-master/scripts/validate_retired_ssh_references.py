#!/usr/bin/env python3
"""Reject tracked references to retired AutoDL OpenGU sibling roots."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Iterable, Sequence


DEPLOYMENT_ROOT = "/autodl-fs/data"
RETIRED_SIBLING_NAMES = (
    "OpenGU-cache-v2-rollout",
    "OpenGU-shared",
    "OpenGU-small-selection-gu",
    "OpenGU-worktrees",
    "cache-v2-canary",
    "cache-v2-materializer",
    "opengu-experiment-evidence",
    "opengu-experiment-ops",
    "opengu-experiments",
)


def retired_prefixes() -> tuple[str, ...]:
    """Return the forbidden top-level prefixes without storing them verbatim."""

    return tuple(
        "{0}/{1}".format(DEPLOYMENT_ROOT, name)
        for name in RETIRED_SIBLING_NAMES
    )


def inspect_text(path: str, text: str) -> list[dict]:
    """Return every retired-prefix occurrence in one UTF-8 text."""

    matches = []
    prefixes = retired_prefixes()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for prefix in prefixes:
            count = line.count(prefix)
            if count:
                matches.append(
                    {
                        "path": path,
                        "line": line_number,
                        "prefix": prefix,
                        "count": count,
                    }
                )
    return matches


def tracked_paths(repository_root: Path) -> list[Path]:
    """Return tracked files below *repository_root*."""

    root = Path(repository_root).resolve()
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    names = result.stdout.decode("utf-8").split("\0")
    return [root / name for name in names if name]


def inspect_paths(repository_root: Path, paths: Iterable[Path]) -> dict:
    """Inspect UTF-8 tracked text while safely ignoring binary files."""

    root = Path(repository_root).resolve()
    matches = []
    scanned = 0
    for path in paths:
        path = Path(path)
        if not path.is_file():
            continue
        payload = path.read_bytes()
        if b"\0" in payload:
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        relative = path.resolve().relative_to(root).as_posix()
        matches.extend(inspect_text(relative, text))
    return {
        "schema": "opengu.retired_ssh_references.v1",
        "repository_root": str(root),
        "scanned_text_files": scanned,
        "matches": matches,
        "match_count": sum(item["count"] for item in matches),
        "passed": not matches,
    }


def inspect_repository(repository_root: Path) -> dict:
    """Inspect every tracked UTF-8 text in one Git repository."""

    root = Path(repository_root).resolve()
    return inspect_paths(root, tracked_paths(root))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = inspect_repository(args.repository_root)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
