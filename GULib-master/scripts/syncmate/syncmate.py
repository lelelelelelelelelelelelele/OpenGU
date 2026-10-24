#!/usr/bin/env python
"""OpenGU CLI entry; project semantics stay in its adapter."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for directory in (PROJECT_ROOT, Path(__file__).resolve().parent):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from syncmate_core.cli import main as core_main, build_parser
from syncmate_core import context
from opengu_adapter import OpenGUProjectExtension
from deployment_policy import deployment_policy, installation_receipt


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    import argparse
    root_parser = argparse.ArgumentParser(add_help=False)
    root_parser.add_argument('--project-root', type=Path)
    root_args, _ = root_parser.parse_known_args(argv)
    root = (root_args.project_root or PROJECT_ROOT).resolve()
    policy = deployment_policy(root)
    with context.use(root):
        args = build_parser().parse_args(argv)
    if args.command == 'runner-agent' and args.runner_agent_command == 'dispatch':
        import json
        import subprocess
        target = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        try:
            installation_receipt(root, target, policy)
        except (ValueError, OSError) as exc:
            print(json.dumps({'status': 'blocked', 'errors': [str(exc)]}))
            return 1
    return core_main(argv, project_root=root, extension=OpenGUProjectExtension(),
                     require_origin_main=policy['require_origin_main'])


if __name__ == '__main__':
    raise SystemExit(main())
