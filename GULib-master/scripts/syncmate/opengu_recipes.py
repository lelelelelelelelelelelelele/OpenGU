"""Read declarative project recipes and assemble the existing Core contract."""
from __future__ import annotations

import copy
from pathlib import Path
import re

import yaml
from experiments.modular_artifacts import ARTIFACT_NAMES, output_paths
from scripts.syncmate.opengu_layout import modular_output_path
from syncmate_core.contracts import Recipe, resolve_repo_path

ROOT = Path(__file__).resolve().parents[2]
RECIPE_DIRECTORY = Path('scripts/syncmate/recipes')
OUTPUT_ROOT = 'results/runs/{experiment_id}/{run_id}'


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate declaration fields rather than silently replacing them."""


def _mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError('duplicate recipe field: ' + str(key))
        result[key] = loader.construct_object(value_node)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _fields(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise ValueError('recipe declaration has missing or unsupported fields')


def load_declaration(path):
    path = Path(path)
    if path.is_symlink():
        raise ValueError('recipe declaration must be a regular file')
    spec = yaml.load(path.read_text(encoding='utf-8'), Loader=UniqueLoader)
    return validate_declaration(spec)


def validate_declaration(spec):
    common = {'schema_version', 'id', 'runner', 'config_path', 'config_sha256', 'timeout_seconds'}
    experiment = {'configuration_fingerprint', 'run_identity', 'logical_cells', 'expected_datasets', 'stage', 'outputs'}
    runner = spec.get('runner') if isinstance(spec, dict) else None
    if runner not in ('smoke', 'opengu-preflight-v1', 'experiment', 'diagnostic'):
        raise ValueError('unknown recipe runner')
    required = common
    if runner == 'experiment':
        required = common | experiment
    elif runner == 'diagnostic':
        required = common | (experiment - {'stage', 'expected_datasets'}) | {'hidden_channels'}
    _fields(spec, required)
    if type(spec['schema_version']) is not int or spec['schema_version'] != 1:
        raise ValueError('unsupported recipe schema_version')
    if not isinstance(spec['id'], str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,80}', spec['id']):
        raise ValueError('unsafe recipe id')
    if runner in ('smoke', 'opengu-preflight-v1') and spec['id'] != runner:
        raise ValueError('built-in runner identity mismatch')
    if runner in ('experiment', 'diagnostic'):
        _fields(spec['run_identity'], {'experiment_id', 'run_id'})
        modular_output_path(**spec['run_identity'])
        if not isinstance(spec['configuration_fingerprint'], str) or not re.fullmatch('[0-9a-f]{64}', spec['configuration_fingerprint']):
            raise ValueError('invalid configuration fingerprint')
        if type(spec['logical_cells']) is not int or spec['logical_cells'] < 1:
            raise ValueError('logical_cells must be positive')
        _fields(spec['outputs'], {'root', 'layout', 'files'})
        layout = 'modular-cells-v1' if runner == 'experiment' else 'aagu059-curvature-v1'
        files = ['run.json', *ARTIFACT_NAMES] if runner == 'experiment' else ['run.json', 'inputs.json', 'h{hidden_channels}-{method}-curvature.json', 'h{hidden_channels}-{method}-{budget}.json']
        if spec['outputs'] != {'root': OUTPUT_ROOT, 'layout': layout, 'files': files}:
            raise ValueError('outputs must match the ordinary executor layout and collection rules')
        if runner == 'experiment':
            if spec['stage'] not in ('selector', 'unlearning', 'metrics') or not isinstance(spec['expected_datasets'], list) or not spec['expected_datasets']:
                raise ValueError('invalid experiment stage or dataset counts')
            for counts in spec['expected_datasets']:
                _fields(counts, {'num_nodes', 'candidate_count'})
                if any(type(v) is not int for v in counts.values()) or not 0 < counts['candidate_count'] <= counts['num_nodes']:
                    raise ValueError('invalid dataset counts')
        elif type(spec['hidden_channels']) is not int or spec['hidden_channels'] not in (16, 64):
            raise ValueError('diagnostic width must be 16 or 64')
    return spec


def assemble(spec, project_root=ROOT):
    from experiments.modular_config import load_experiment
    root = Path(project_root)
    config_path = resolve_repo_path(root, spec['config_path'])
    if not config_path.is_file():
        raise ValueError('recipe config is missing')
    spec = validate_declaration(spec)
    runner = spec['runner']
    definition = {k: copy.deepcopy(v) for k, v in spec.items()
                  if k not in ('schema_version', 'runner', 'outputs', 'hidden_channels')}
    definition.update(git_binding_policy='job-exact-main-v1', collector_acceptance=False)
    if runner in ('smoke', 'opengu-preflight-v1'):
        definition.update(argv=('{python}', 'scripts/syncmate/syncmate.py', 'smoke', '--json'),
            recipe_introduced_git_sha='3331c641ce16d0d7a3def66b0e302dd4a39a919c',
            expected_artifact_paths=(), success_predicate='json.passed == true')
        if runner == 'opengu-preflight-v1':
            definition.update(argv=('{python}', 'scripts/syncmate/syncmate.py', 'runner-preflight', '--recipe', spec['id'], '--json'),
                expected_artifact_paths=tuple('results/runs/__syncmate_preflight__/opengu_preflight/seed0/'+n
                    for n in ('attack.json', 'collateral.json', '_meta.json')),
                collector_acceptance=True,
                success_predicate='json.passed == true and generated_artifacts == expected_artifact_paths')
    else:
        summary = modular_output_path(**spec['run_identity'])
        base = summary.rsplit('/', 1)[0]
        entry = 'experiments/run.py' if runner == 'experiment' else 'experiments/aagu059_diagnostic.py'
        definition.update(argv=('{python}', entry, spec['config_path'], '--run-id', spec['run_identity']['run_id']),
            requires_job_expected_git_sha=True, collector_result_roots=(base,),
            preflight_profile='modular-project-v1', execution_validator='exact-artifacts-json-v1')
        if runner == 'experiment':
            config = load_experiment(config_path)
            if config['experiment_id'] != spec['run_identity']['experiment_id'] or config['stage'] != spec['stage']:
                raise ValueError('recipe identity or stage differs from experiment')
            if len(config['datasets']) != len(spec['expected_datasets']):
                raise ValueError('recipe dataset count differs from experiment')
            paths = (summary,) + output_paths(summary, config)
            definition.update(expected_artifact_paths=paths,
                collector_artifact_names=tuple(sorted({Path(p).name for p in paths})),
                collector_profile='modular-output-v1', collector_acceptance=True,
                success_predicate='json.passed == true and all reviewed artifacts exist')
        else:
            width = spec['hidden_channels']
            names = ['run.json', 'inputs.json']
            names += [f'h{width}-{method}-curvature.json' for method in ('gif', 'idea')]
            names += [f'h{width}-{method}-{budget}.json' for method in ('gif', 'idea') for budget in (100, 200, 400)]
            definition.update(expected_artifact_paths=tuple(sorted(base+'/'+n for n in names)),
                collector_artifact_names=tuple(names),
                success_predicate='json.passed == true and all reviewed diagnostic artifacts exist')
    Recipe(id=definition['id'], argv=definition['argv'], config_path=definition['config_path'],
           config_sha256=definition['config_sha256'], timeout_seconds=definition['timeout_seconds'],
           expected_artifact_paths=definition['expected_artifact_paths'],
           execution_validator=definition.get('execution_validator', 'json-passed-v1'))
    return definition


def recipe_ids(project_root=ROOT):
    """List reviewed recipe identifiers without loading YAML or configs."""
    root = Path(project_root).resolve()
    directory = (root / RECIPE_DIRECTORY).resolve()
    directory.relative_to(root)
    return tuple(path.stem for path in sorted(directory.glob('*.yaml')) if path.is_file())


def resolve_recipe(project_root, recipe_id):
    """Load and assemble exactly one recipe declaration by its reviewed ID."""
    from syncmate_core.contracts import JOB_ID_RE

    if not isinstance(recipe_id, str) or not JOB_ID_RE.fullmatch(recipe_id):
        raise ValueError('invalid recipe identifier')
    root = Path(project_root).resolve()
    declaration_path = root / RECIPE_DIRECTORY / (recipe_id + '.yaml')
    declaration_path.resolve().relative_to(root)
    if not declaration_path.is_file():
        raise ValueError('recipe is not allowlisted: ' + recipe_id)
    spec = load_declaration(declaration_path)
    if spec['id'] != recipe_id or declaration_path.stem != spec['id']:
        raise ValueError('recipe filename/id mismatch: ' + str(declaration_path))
    return assemble(spec, root)


def generate(config_path, *, recipe_id, run_id, timeout_seconds=21600, project_root=ROOT,
             node=None, device_file=None):
    """Explicit generation refreshes hashes; ordinary reads never refresh them."""
    from experiments.modular_run import execute
    from experiments.modular_config import load_experiment
    from syncmate_core.identity import sha256_recipe_config
    root = Path(project_root).resolve()
    path = resolve_repo_path(root, config_path)
    plan = execute(path, dry_run=True)
    from scripts.syncmate.recipe_inputs import dataset_counts
    expected_datasets = dataset_counts(load_experiment(path), root, node=node,
        device_file=device_file or root / '.syncmate/device.yaml')
    return {'schema_version': 1, 'id': recipe_id, 'runner': 'experiment',
        'config_path': path.relative_to(root).as_posix(), 'config_sha256': sha256_recipe_config(path),
        'configuration_fingerprint': plan['configuration_fingerprint'],
        'run_identity': {'experiment_id': plan['experiment_id'], 'run_id': run_id},
        'timeout_seconds': timeout_seconds, 'logical_cells': plan['logical_cells'],
        'stage': plan['stage'], 'expected_datasets': expected_datasets,
        'outputs': {'root': OUTPUT_ROOT, 'layout': 'modular-cells-v1', 'files': ['run.json', *ARTIFACT_NAMES]}}
