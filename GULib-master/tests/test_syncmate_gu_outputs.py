"""CPU producer -> actual SyncMate collection -> OpenGU acceptance, with no formal data."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import torch
from test_modular_consumers import tables
from test_retrain_outputs import configs, method, forbidden, snapshot
from scripts.syncmate import syncmate  # install the project extension for the actual Core
from opengu_adapter import OpenGUProjectExtension
from opengu_recipes import recipe_definitions
from experiments.target_direct_v1 import syncmate_stage as stage
from experiments.target_direct_v1.run_outputs import save_method_result
from experiments.modular_config import load_instance
from syncmate_core import collection, context, devices, index

ROOT = Path(__file__).resolve().parents[1]
RECIPES = [(name, definition) for name, definition in recipe_definitions().items()
           if 'gu_gate' in definition or 'gu_stage' in definition]


@pytest.mark.parametrize('seed', [42, 212, 2024])
def test_registered_method_conditions_match_matrix_consumer(tmp_path, seed):
    from experiments.target_direct_v1.build_manifest import SCHEMA, VERSION
    from experiments.target_direct_v1.build_gu_config import build_gu_config
    from experiments.target_direct_v1.run_outputs import cell_instance
    definition = recipe_definitions()[f'opengu-target-direct-gu-cora-seed{seed}-r001-v2']
    scope = definition['gu_stage']
    manifest = {'schema': SCHEMA, 'version': VERSION, 'parameter_scope': 'last_layer',
        'dataset': 'Cora', 'ratio': .01, 'candidate_count': 1895, 'expected_k': 18,
        'strategies': ['degree'], 'seeds': [seed], 'store_root': str(tmp_path / 'store'),
        'processed_profile': scope['split_contract']['processed_profile'], 'split_contract': scope['split_contract'],
        'budget': {'ratio': .01, 'denominator': 'train_candidate_count',
                   'rounding': 'floor_with_minimum_one', 'denominator_count': 1895, 'expected_k': 18}}
    path = tmp_path / 'manifest.json'
    path.write_text(json.dumps(manifest))
    cfg = build_gu_config(manifest_path=path, processed_root=tmp_path / 'processed',
                          runtime_root=tmp_path / 'runtime', run_root=tmp_path / 'runs')
    cfg['_source_path'] = str(tmp_path / 'gu.yaml')
    for name in scope['gu_methods']:
        assert scope['method_instances'][name] == cell_instance(cfg, name, seed)


@pytest.mark.parametrize('name,definition', RECIPES)
def test_registered_gu_contract_matches_actual_executor(name, definition):
    scope = definition.get('gu_gate') or definition['gu_stage']
    expected = stage.gu_artifacts(scope['stage'], ratio=scope['ratio'], gate_only='gu_gate' in definition)
    assert tuple(definition['expected_artifact_paths']) == expected
    assert len(expected) == (8 if 'gu_gate' in definition else 136)
    assert set(scope['gu_methods']) == {'GNNDelete', 'Retrain'}
    assert {p.rsplit('/', 1)[0] for p in expected} == set(definition['collector_result_roots'])
    assert set(definition['collector_artifact_names']) == set(stage.ARTIFACT_NAMES)


@pytest.mark.parametrize('name,definition', RECIPES)
def test_adapter_calls_real_preflight_with_reviewed_arguments(name, definition, monkeypatch):
    visited = []
    def formal(config, received_stage, *, require_gpu):
        visited.append((received_stage, require_gpu, config['repository_root']))
        return {'git': {'head': 'a' * 40}, 'errors': ['disposable preflight boundary']}
    monkeypatch.setattr(stage, '_formal_preflight', formal)
    monkeypatch.setattr(stage, '_validate_selection_pair', forbidden)
    result = OpenGUProjectExtension().preflight(definition['preflight_profile'], definition,
                                                ROOT / definition['config_path'])
    scope = definition.get('gu_gate') or definition['gu_stage']
    assert visited and visited[0][:2] == (scope['stage'], True)
    assert result['ratio'] == scope['ratio']
    assert result['gate_only'] is ('gu_gate' in definition)
    assert result['ready'] is False  # real runtime gate remains enforced
    assert 'disposable preflight boundary' in result['errors']


@pytest.fixture
def exported(tables):
    root = tables[0]
    reference = configs(tables)
    gnn = method(tables, 'collected-gnn', reference, 'gu.yaml')
    rt = method(tables, 'collected-rt', reference, 'retrain.yaml')
    runner, collector = root / 'runner', root / 'collector'
    runner.mkdir()
    collector.mkdir()
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(runner)], check=True)
    subprocess.run(['git', '-C', str(runner), '-c', 'user.name=CPU fixture', '-c',
                    'user.email=fixture@example.invalid', 'commit', '-q', '--allow-empty', '-m', 'CPU fixture'], check=True)
    sha = subprocess.check_output(['git', '-C', str(runner), 'rev-parse', 'HEAD'], text=True).strip()
    definition = copy.deepcopy(recipe_definitions()['opengu-target-direct-gu-gate-r001-v2'])
    # Disposable graph has 10 candidates / k=1; formal recipe/YAML stays untouched.
    definition['gu_gate'].update(k=1, candidate_count=10)
    definition['gu_gate']['method_instances'] = {name: load_instance(root / filename, 'unlearning')
        for name, filename in [('GNNDelete', 'gu.yaml'), ('Retrain', 'retrain.yaml')]}
    selection = {**reference, 'strategy': 'degree', 'ratio': .01, 'k': 1,
                 'authoritative': True, 'target_checkpoint': gnn['checkpoint']}
    for name, row in [('GNNDelete', gnn), ('Retrain', rt)]:
        leaf = next(p for p in definition['collector_result_roots'] if '/' + name + '_degree/' in p)
        save_method_result(row, store_root=root / 'v2', output_dir=runner / leaf, strategy='degree',
            meta={'git_sha': sha, 'method': name, 'strategy': 'degree', 'seed': 42,
                'config_fingerprint': hashlib.sha256(name.encode()).hexdigest(),
                'fingerprint_version': 'v5-single-method-output', 'comparison_stage': 'deferred',
                'selection_artifact': selection})
    return root, runner, collector, sha, definition


def collect(exported):
    root, runner, collector, sha, definition = exported
    peer = devices.build_peer_config('runner', None, str(runner), transport='local')
    args = ('cpu-runner', devices.transport_ssh_value(peer), str(runner),
            list(definition['collector_result_roots']), 'results/runs/cpu-runner')
    options = {'artifact_names': tuple(definition['collector_artifact_names']),
               'expected_paths': list(definition['expected_artifact_paths']), 'expected_git_sha': sha, 'save': True}
    applied = collection.apply_collect(*args, **options)
    assert not applied.get('errors'), applied
    verified = collection.verify_collect(*args, **options)
    assert verified['summary']['status'] == 'verified', verified
    observed = index.load_artifact_index()
    return {'project_root': collector, 'node_id': 'cpu-runner', 'expected_git_sha': sha,
            'artifact_index': observed}, args, options


@pytest.mark.parametrize('gate', [True, False])
def test_real_outputs_survive_collect_accept_results_and_repeat(exported, monkeypatch, record_property, gate):
    root, runner, collector, sha, definition = exported
    if not gate:
        scope = definition.pop('gu_gate')
        scope['selectors'] = [scope.pop('selector')]
        definition['gu_stage'] = scope
        definition['collector_profile'] = 'target-direct-gu-stage-v2'
    extension = OpenGUProjectExtension()
    before = snapshot(root / 'v2')
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbidden)
    try:
        with context.use(collector, extension=extension):
            collected, args, options = collect(exported)
            accepted = extension.accept(definition['collector_profile'], definition, collected)
            assert accepted['passed'], accepted['errors']
            assert accepted['accepted_cells'] == 2
            assert {c['method'] for c in accepted['cells']} == {'GNNDelete', 'Retrain'}
            rows = extension.results(collected['artifact_index'], {'project_root': collector})
            assert len(rows['rows']) == 2 and not rows['parse_errors'], rows
            assert all(r['status'] == 'ok' and r['comparison_stage'] == 'deferred' for r in rows['rows'])
            repeated = collection.apply_collect(*args, **options)
            assert repeated['summary']['fetched'] == 0
            record_property('aagu005_collection', json.dumps({'gate': gate,
                'accepted': accepted, 'rows': rows['rows'], 'repeat_fetched': 0}, default=str))
    finally:
        hook.remove()
    assert snapshot(root / 'v2') == before
    assert not (collector / 'results/cache_v2').exists()


@pytest.mark.parametrize('fault', ['missing_retrain', 'duplicate_index', 'unverified_index', 'git',
    'checksum', 'output_reference', 'metrics', 'checkpoint', 'selection', 'missing_prediction', 'invalid_prediction',
    'method_configuration'])
def test_collected_faults_never_pass(exported, fault):
    _, _, collector, _, definition = exported
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        collected, _, _ = collect(exported)
        peer = collected['artifact_index']['peers']['cpu-runner']
        items = peer['items']
        meta_item = next(i for i in items if '/Retrain_' in i['remote_path'] and i['remote_path'].endswith('/_meta.json'))
        if fault == 'missing_retrain':
            peer['items'] = [i for i in items if '/Retrain_' not in i['remote_path']]
        elif fault == 'duplicate_index':
            peer['items'].append(copy.deepcopy(items[0]))
        elif fault == 'unverified_index':
            peer['summary']['status'] = 'incomplete'
        elif fault == 'method_configuration':
            definition['gu_gate']['method_instances']['GNNDelete']['parameters']['unlearn_lr'] *= 2
        elif fault in ('checksum', 'missing_prediction', 'invalid_prediction'):
            item = next(i for i in items if i['remote_path'].endswith('/predictions.npz'))
            path = collector / item['local_path']
            if fault == 'missing_prediction':
                path.unlink()
            else:
                path.write_bytes(b'not an output')
                if fault == 'invalid_prediction':
                    item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            item = meta_item
            if fault == 'metrics':
                item = next(i for i in items if '/Retrain_' in i['remote_path'] and i['remote_path'].endswith('/attack.json'))
            path = collector / item['local_path']
            doc = json.loads(path.read_text())
            if fault == 'git': doc['git_sha'] = 'f' * 40
            elif fault == 'output_reference': doc['output_reference']['content_hash'] = 'f' * 64
            elif fault == 'metrics': doc['results']['degree']['evaluation']['metrics']['f1'] = -1
            elif fault == 'checkpoint': doc['selection_artifact']['target_checkpoint']['state_hash'] = 'f' * 64
            elif fault == 'selection': doc['selection_artifact']['content_hash'] = 'f' * 64
            path.write_text(json.dumps(doc))
            item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        result = extension.accept(definition['collector_profile'], definition, collected)
        assert not result['passed'], (fault, result)
        assert result['errors']
