"""Generate a recipe declaration or inspect a submission without dispatching it."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT, Path(__file__).resolve().parent):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import yaml
from scripts.syncmate.opengu_recipes import RECIPE_DIRECTORY, assemble, generate, load_declaration


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'Git inspection failed')
    return result.stdout.strip()


def preview(recipe_id, node_id, device_file, project_root=ROOT, source_ref='refs/heads/main'):
    """Inspect exactly one committed source through the installed consumer."""
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
        '--project-root', str(Path(project_root).resolve()), '--config', str(device_file),
        '--source-ref', source_ref, 'preview', recipe_id, '--node', node_id],
        capture_output=True, text=True, encoding='utf-8')
    view = json.loads(result.stdout)
    if result.returncode:
        raise ValueError('; '.join(view.get('errors') or ['committed preview failed']))
    return view


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    gen = sub.add_parser('generate', help='write a new Recipe YAML using bound dataset evidence')
    gen.add_argument('config')
    gen.add_argument('--id', required=True)
    gen.add_argument('--run-id', required=True)
    gen.add_argument('--node', help='read bound dataset evidence from this configured runner')
    gen.add_argument('--device-config', type=Path, default=ROOT / '.syncmate/device.yaml')
    gen.add_argument('--output', type=Path, required=True, help='new Recipe YAML file; never overwritten')
    gen.add_argument('--timeout-seconds', type=int, default=21600)
    view = sub.add_parser('preview')
    view.add_argument('recipe')
    view.add_argument('--source-ref', default='refs/heads/main')
    view.add_argument('--node', required=True)
    view.add_argument('--device-config', type=Path, default=ROOT / '.syncmate/device.yaml')
    args = parser.parse_args(argv)
    try:
        if args.action == 'generate':
            if args.output.name != args.id + '.yaml' or args.output.exists():
                raise ValueError('output must be a new file named <Recipe ID>.yaml')
            spec = generate(args.config, recipe_id=args.id, run_id=args.run_id,
                timeout_seconds=args.timeout_seconds, node=args.node, device_file=args.device_config)
            from scripts.syncmate.opengu_recipes import validate_declaration
            validate_declaration(spec)
            assemble(spec)
            if args.output.name != args.id + '.yaml':
                raise ValueError('output filename must match Recipe ID')
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(yaml.safe_dump(spec, sort_keys=False))
            print(json.dumps({'recipe': spec['id'], 'path': str(args.output.resolve()),
                              'expected_datasets': spec['expected_datasets']}))
        else:
            print(json.dumps(preview(args.recipe, args.node, args.device_config, source_ref=args.source_ref), indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, yaml.YAMLError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
