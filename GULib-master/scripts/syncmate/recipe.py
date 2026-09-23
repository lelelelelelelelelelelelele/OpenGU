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
from opengu_recipes import RECIPE_DIRECTORY, assemble, generate, load_declaration


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'Git inspection failed')
    return result.stdout.strip()


def preview(recipe_id, node_id, device_file, project_root=ROOT):
    from syncmate_core import context, devices, recipes, run_handoff
    from opengu_adapter import OpenGUProjectExtension
    from verify_core_dependency import verify_core_dependency
    root = Path(project_root).resolve()
    declaration_path = root / RECIPE_DIRECTORY / (recipe_id + '.yaml')
    # A recipe argument is an ID, never an arbitrary filesystem path.
    from syncmate_core.contracts import JOB_ID_RE
    if not JOB_ID_RE.fullmatch(recipe_id):
        raise ValueError('invalid recipe id')
    declaration_path.resolve().relative_to(root)
    spec = load_declaration(declaration_path)
    if spec['id'] != recipe_id:
        raise ValueError('recipe filename/id mismatch')
    definition = assemble(spec, root)
    with context.use(root, extension=OpenGUProjectExtension(), require_origin_main=True):
        device, warnings = devices.load_device(Path(device_file))
    peer = device.get('peers', {}).get(node_id)
    if not peer or peer.get('role') not in ('runner', 'runner+collector'):
        raise ValueError('select a configured runner peer')
    sha = git(root, 'rev-parse', 'HEAD')
    branch = git(root, 'branch', '--show-current')
    errors = list(warnings)
    if git(root, 'status', '--porcelain', '--untracked-files=all'):
        errors.append('checkout has uncommitted files; commit the declaration and configuration before dispatch')
    if branch != 'main':
        errors.append('Core dispatch requires the reviewed candidate to land on main')
    git(root, 'ls-files', '--error-unmatch', str(declaration_path.relative_to(root)))
    git(root, 'ls-files', '--error-unmatch', definition['config_path'])
    dependency = verify_core_dependency()
    errors.extend(dependency['errors'])
    with context.use(root, extension=OpenGUProjectExtension(), require_origin_main=True):
        binding = recipes.runner_recipe_binding(definition)
        errors.extend(binding['errors'])
        landing = run_handoff.landing_for(node_id)
    python = sys.executable if devices.peer_uses_local_transport(peer) else devices.peer_python_executable(peer)
    command = [python if value == '{python}' else value for value in definition['argv']]
    try:
        repository = git(root, 'remote', 'get-url', 'origin')
    except ValueError:
        repository = None
        errors.append('origin repository is not configured')
    try:
        if git(root, 'rev-parse', 'refs/remotes/origin/main') != sha:
            errors.append('local HEAD differs from origin/main')
    except ValueError:
        errors.append('origin/main is unavailable')
    return {'recipe': recipe_id, 'declaration': declaration_path.relative_to(root).as_posix(),
        'repository': repository, 'commit': sha, 'branch': branch,
        'config_path': definition['config_path'], 'config_sha256': definition['config_sha256'],
        'configuration_fingerprint': definition.get('configuration_fingerprint'),
        'node': node_id, 'transport': peer.get('transport', 'ssh'), 'ssh_alias': peer.get('ssh'),
        'remote_workdir': peer['repo_path'], 'python': python, 'argv': command,
        'run_identity': definition.get('run_identity', {}),
        'remote_result_roots': list(definition.get('collector_result_roots', [])),
        'local_receiving_root': str(root / landing),
        'collection': spec.get('outputs', {'layout': 'core-preflight'}),
        'expected_artifact_count': len(definition['expected_artifact_paths']),
        'code_sync': 'Separate reviewed Git synchronization before dispatch; Core requires local/runner clean main at the same full commit. Dispatch does not copy dirty files or update code.',
        'local_checks_passed': not errors, 'errors': errors,
        'remote_checks': 'NOT OBSERVED: preview makes no remote connection; dispatch performs peer preflight and exact version checks.',
        'submitted': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    gen = sub.add_parser('generate', help='print a new ordinary-experiment recipe YAML to stdout')
    gen.add_argument('config')
    gen.add_argument('--id', required=True)
    gen.add_argument('--run-id', required=True)
    gen.add_argument('--dataset-count', action='append', required=True, metavar='NODES:CANDIDATES',
                     help='one reviewed count pair per dataset, in config order')
    gen.add_argument('--timeout-seconds', type=int, default=21600)
    view = sub.add_parser('preview')
    view.add_argument('recipe')
    view.add_argument('--node', required=True)
    view.add_argument('--device-config', type=Path, default=ROOT / '.syncmate/device.yaml')
    args = parser.parse_args(argv)
    try:
        if args.action == 'generate':
            counts = []
            for value in args.dataset_count:
                nodes, candidates = map(int, value.split(':'))
                counts.append({'num_nodes': nodes, 'candidate_count': candidates})
            spec = generate(args.config, recipe_id=args.id, run_id=args.run_id,
                expected_datasets=counts, timeout_seconds=args.timeout_seconds)
            from opengu_recipes import validate_declaration
            validate_declaration(spec)
            assemble(spec)
            print(yaml.safe_dump(spec, sort_keys=False), end='')
        else:
            print(json.dumps(preview(args.recipe, args.node, args.device_config), indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, yaml.YAMLError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
