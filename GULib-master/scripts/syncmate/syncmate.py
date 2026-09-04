#!/usr/bin/env python
"""OpenGU CLI entry; project semantics stay in its adapter."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for directory in (PROJECT_ROOT, Path(__file__).resolve().parent):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from syncmate_core.cli import main as core_main
from opengu_adapter import OpenGUProjectExtension


def main(argv=None):
    return core_main(argv, project_root=PROJECT_ROOT, extension=OpenGUProjectExtension(), require_origin_main=True)


if __name__ == '__main__':
    raise SystemExit(main())
