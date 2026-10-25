#!/usr/bin/env python
"""Launch the installed OpenGU control, outside the execution checkout."""
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
                           '--project-root', str(PROJECT_ROOT), *argv],
                          **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {})).returncode


if __name__ == '__main__':
    raise SystemExit(main())
