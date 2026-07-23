#!/usr/bin/env python3
"""Validate that the AutoDL deployment root has no OpenGU peer directories."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


DEFAULT_ALLOWED = (".gitignore", ".sys", "OpenGU")


def inspect_layout(base: Path, allowed: Sequence[str]) -> dict:
    """Return a machine-readable, non-mutating deployment layout verdict."""

    root = Path(base).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("deployment root is not a directory: {0}".format(root))
    allowed_names = set(allowed)
    entries = sorted(item.name for item in root.iterdir())
    unexpected = sorted(set(entries) - allowed_names)
    missing = sorted(allowed_names - set(entries))
    active = root / "OpenGU"
    return {
        "schema": "opengu.ssh_deployment_layout.v1",
        "base": str(root),
        "allowed": sorted(allowed_names),
        "entries": entries,
        "unexpected": unexpected,
        "missing": missing,
        "active_checkout_exists": active.is_dir(),
        "passed": not unexpected and active.is_dir(),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=Path("/autodl-fs/data"))
    parser.add_argument(
        "--allow",
        action="append",
        dest="allowed",
        help="Allowed top-level name; repeat to override the defaults.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = inspect_layout(args.base, args.allowed or DEFAULT_ALLOWED)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
