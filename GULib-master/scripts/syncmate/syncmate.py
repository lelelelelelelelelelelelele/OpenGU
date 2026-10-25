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
from syncmate_core import context, devices
from opengu_adapter import OpenGUProjectExtension
from deployment_policy import deployment_policy, installation_receipt, execution_readiness


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    import argparse
    root_parser = argparse.ArgumentParser(add_help=False)
    root_parser.add_argument('--project-root', type=Path)
    root_parser.add_argument('--node-id')
    root_args, _ = root_parser.parse_known_args(argv)
    root = (root_args.project_root or PROJECT_ROOT).resolve()
    policy = deployment_policy(root)
    if not callable(getattr(context, 'runner_node_id', None)):
        import json
        print(json.dumps({'status': 'blocked', 'errors': ['OpenGU requires the node-queue Core interface (SM-027); old Core is unsupported']}))
        return 1
    with context.use(root, node_id=root_args.node_id):
        args = build_parser().parse_args(argv)
    if args.command == 'runner-agent' and args.runner_agent_command == 'dispatch':
        import json
        import subprocess
        target = subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()
        try:
            if root_args.node_id is not None and root_args.node_id != args.node_id:
                raise ValueError('global node differs from selected dispatch peer')
            with context.use(root, node_id=args.node_id):
                device, warnings = devices.load_device(args.config)
            if warnings:
                raise ValueError('; '.join(warnings))
            peer = device.get('peers', {}).get(args.node_id)
            installation_receipt(root, args.node_id, target, policy, peer=peer)
        except (ValueError, OSError) as exc:
            print(json.dumps({'status': 'blocked', 'errors': [str(exc)]}))
            return 1
    if args.command == 'console':
        from dataclasses import replace
        from syncmate_core import console
        with context.use(root, extension=OpenGUProjectExtension(),
                         require_origin_main=policy['require_origin_main'], node_id=root_args.node_id) as project:
            if args.stop:
                return console.cmd_console(args)
            project = replace(project, execution_readiness=execution_readiness)
            console.serve_console({root.name: project}, args.port, args.desktop)
        return 0
    return core_main(argv, project_root=root, extension=OpenGUProjectExtension(),
                     require_origin_main=policy['require_origin_main'])


if __name__ == '__main__':
    raise SystemExit(main())
