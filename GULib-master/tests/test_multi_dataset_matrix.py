"""AAGU-035 practical evidence: real CPU entry, immutable caches and Core collection."""
import copy
import hashlib
import json
import pickle
from pathlib import Path

import pytest
import torch
import yaml
from torch_geometric.data import Data
from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, commit, cli, declaration, FixtureRegistration
from test_syncmate_gu_outputs import collect
from experiments.modular_config import load_experiment, experiment_batches, configuration_fingerprint
from experiments.modular_artifacts import read_summary_outputs
from experiments.modular_run import execute
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context, devices, queue
from utils.target_checkpoint import data_identity, sha256_file


def dataset(root, stem, *, alternate=False):
    torch.manual_seed(35)
    n = 24
    nodes = torch.arange(n)
    edges = torch.stack([nodes, (nodes + 1) % n])
    train = nodes < 12
    val = (nodes >= 12) & (nodes < 18)
    if alternate:
        train[[0, 12]] = ~train[[0, 12]]
        val[[0, 12]] = ~val[[0, 12]]
    data = Data(x=torch.randn(n, 3), y=nodes % 2,
        edge_index=torch.cat([edges, edges.flip(0)], dim=1),
        train_mask=train, val_mask=val, test_mask=nodes >= 18)
    graph = root / 'data/processed' / (stem + '.pkl'); graph.write_bytes(pickle.dumps(data))
    instance = {'kind': 'dataset_split', 'schema_version': 1,
        'dataset': {'name': 'cpu_second'}, 'preprocessing': {'adapter': 'OpenGU_persisted_processed_pair'},
        'split': {'profile': 'alternate' if alternate else 'second', 'train_ratio': .5,
                  'val_ratio': .25, 'test_ratio': .25, 'seed': 36 if alternate else 35}}
    manifest = {k: instance[k] for k in ('dataset', 'preprocessing', 'split')}
    manifest.update(schema='opengu.persisted_dataset_split', version=1, data_path=graph.name,
                    data_sha256=sha256_file(graph), data_identity=data_identity(data))
    path = root / 'data/processed' / (stem + '.json'); path.write_text(json.dumps(manifest))
    instance['artifacts'] = {'manifest': path.relative_to(root).as_posix(), 'manifest_sha256': sha256_file(path),
        'split_hash': data_identity(data)['split_hash'], 'node_id_space': 'pyg-global-node-index-v1'}
    write_yaml(root / (stem + '.yaml'), instance)
    return data


def run(root, path, run_id):
    result = cli(root, path, run_id)
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


def identities(summary, name):
    return {
        'score': [r['score']['artifact_id'] for r in summary['selectors'] if r['matrix_values']['dataset_name'] == name],
        'selection': [r['selection']['artifact']['artifact_id'] for r in summary['selectors'] if r['matrix_values']['dataset_name'] == name],
        'output': [r['output'] for r in summary['unlearning'] if r['matrix_values']['dataset_name'] == name],
    }


def assert_hot(summary, name):
    for r in summary['selectors']:
        if r['matrix_values']['dataset_name'] == name:
            assert r['score']['hit'] and not r['score']['producer_called']
            assert r['selection']['cache']['hit'] and not r['selection']['cache']['producer_called']
    for r in summary['unlearning']:
        if r['matrix_values']['dataset_name'] == name:
            assert r['hit'] and not r['producer_called']


def test_real_multi_dataset_lifecycle(workspace, record_property):
    root, path, config = workspace
    first = pickle.loads((root / 'data/processed/graph.pkl').read_bytes())
    second = dataset(root, 'second')
    config.update(stage='unlearning', unlearning_refs=['gu.yaml', 'retrain.yaml'])
    write_yaml(path, config)
    cold = run(root, path, 'single-cold')
    config['dataset_refs'] = ['dataset.yaml', 'second.yaml']
    write_yaml(path, config)
    sha = commit(root)
    definition = declaration(root, path, 'unlearning')
    definition['expected_datasets'] = [{'num_nodes': 20, 'candidate_count': 10},
                                       {'num_nodes': 24, 'candidate_count': 12}]
    summary_path = definition['expected_artifact_paths'][0]
    definition['expected_artifact_paths'] = [summary_path] + [
        'results/runs/modular/contract/registered/summary.outputs/{}/{}'.format(i, name)
        for i in range(16) for name in ('attack.json','output-references.json','predictions.npz','_meta.json')]
    assert definition['logical_cells'] == 16
    with context.use(root, extension=FixtureRegistration(definition)):
        submitted = queue.runner_queue_submit('multi-job', definition['id'], expected_git_sha=sha)
        assert submitted['submitted'], submitted
        device, warnings = devices.load_device(root / '.syncmate/device.yaml')
        assert not warnings
        result = queue.runner_queue_run_once(device)
        assert result['status'] == 'done', result
    multi = json.loads((root / summary_path).read_text())
    assert identities(cold, 'cpu_fixture') == identities(multi, 'cpu_fixture')
    assert_hot(multi, 'cpu_fixture')
    assert any(r['score']['producer_called'] for r in multi['selectors'] if r['matrix_values']['dataset_name'] == 'cpu_second')
    assert all(r['producer_called'] for r in multi['unlearning'] if r['matrix_values']['dataset_name'] == 'cpu_second')
    _, outputs = read_summary_outputs(root / summary_path, sha256_file(root / summary_path), dataset_root=root)
    for row, output in zip(multi['unlearning'], outputs):
        arrays = output['payload'].arrays
        selected = arrays['selected_nodes']
        idx = row['matrix_values']['dataset_index']
        assert len(arrays['y']) == (20 if idx == 0 else 24)
        actual_data = first if idx == 0 else second
        for mask in ('train_mask', 'val_mask', 'test_mask'):
            assert (arrays[mask] == getattr(actual_data, mask).numpy()).all()
        assert arrays['train_mask'][selected].all()
        assert not arrays['retain_mask'][selected].any()
    collector = root / 'collector'; collector.mkdir()
    for source in root.glob('*.yaml'):
        (collector / source.name).write_bytes(source.read_bytes())
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        collected, args, options = collect((root, collector, sha, definition))
        accepted = extension.accept('modular-output-v1', definition, collected)
        assert accepted['passed'], accepted
        assert accepted['accepted_cells'] == 16
        rows = extension.results(collected['artifact_index'], {'project_root': collector})
        assert len(rows['rows']) == 16 and not rows['parse_errors']
        assert {r['dataset'] for r in rows['rows']} == {'cpu_fixture', 'cpu_second'}
        assert {r['seed'] for r in rows['rows']} == {122, 722}
        assert {r['ratio'] for r in rows['rows']} == {.1, .2}
        faults = {}
        for fault in ('missing', 'duplicate', 'wrong_owner'):
            bad = copy.deepcopy(collected)
            peer = bad['artifact_index']['peers']['cpu-runner']
            if fault == 'missing': peer['items'].pop()
            elif fault == 'duplicate': peer['items'].append(copy.deepcopy(peer['items'][0]))
            else:
                entry = next(i for i in peer['items'] if i['remote_path'].endswith('/summary.json'))
                target = collector / entry['local_path']; original = target.read_bytes()
                document = json.loads(original)
                document['unlearning'][0]['matrix_values']['dataset_index'] = 1
                target.write_text(json.dumps(document))
                entry['sha256'] = sha256_file(target)
            checked = extension.accept('modular-output-v1', definition, bad)
            if fault == 'wrong_owner': target.write_bytes(original)
            assert not checked['passed'], fault
            faults[fault] = checked['errors']
    # Reorder and rename the table and experiment while keeping computational identity.
    config['dataset_refs'].reverse(); config['experiment_id'] = 'renamed'
    renamed = root / 'renamed.yaml'; write_yaml(renamed, config)
    warm = run(root, renamed, 'warm-reordered')
    for name in ('cpu_fixture', 'cpu_second'):
        assert identities(multi, name) == identities(warm, name)
        assert_hot(warm, name)
    metrics = {'kind':'experiment','schema_version':1,'experiment_id':'multi-metrics','stage':'metrics',
        'dataset_refs':['dataset.yaml','second.yaml'], 'matrix':'cartesian_product',
        'evaluation_refs':['utility.yaml'], 'output_inputs':[{'summary':str(root/summary_path),
                                                           'sha256':sha256_file(root/summary_path)}]}
    write_yaml(root/'metrics.yaml', metrics)
    evaluated = run(root, root/'metrics.yaml', 'metrics')
    assert len(evaluated['evaluations']) == 2 and not evaluated['selector_producer_called']
    assert all(e['rows'] for e in evaluated['evaluations'])
    dataset(root, 'second-alternate', alternate=True)
    config['dataset_refs'] = ['second-alternate.yaml', 'dataset.yaml']; write_yaml(renamed, config)
    changed = run(root, renamed, 'changed-split')
    assert identities(changed, 'cpu_fixture') == identities(cold, 'cpu_fixture')
    assert_hot(changed, 'cpu_fixture')
    for key in ('score','selection','output'):
        assert identities(changed, 'cpu_second')[key] != identities(multi, 'cpu_second')[key]
    assert any(r['score']['producer_called'] for r in changed['selectors'] if r['matrix_values']['dataset_name']=='cpu_second')
    assert all(r['selection']['cache']['producer_called'] for r in changed['selectors'] if r['matrix_values']['dataset_name']=='cpu_second')
    assert all(r['producer_called'] for r in changed['unlearning'] if r['matrix_values']['dataset_name']=='cpu_second')
    evidence = {'logical_cells':16, 'artifact_count':65, 'accepted_cells':accepted['accepted_cells'],
        'faults':faults, 'single_to_multi':'HIT', 'reordered':'HIT', 'changed_split':'MISS',
        'unchanged_dataset':'HIT', 'metrics_datasets':2,
        'runs':{k:v['execution_receipt']['output'] for k,v in [('cold',cold),('multi',multi),('warm',warm),('changed',changed)]}}
    record_property('multi_dataset_evidence', json.dumps(evidence))


@pytest.mark.parametrize('refs', [[], 'dataset.yaml', ['dataset.yaml','dataset.yaml']])
def test_invalid_dataset_axis(tables, refs):
    root, config, _ = tables
    config['dataset_refs'] = refs
    path = root/'invalid.yaml'
    path.write_text(yaml.safe_dump(config))
    with pytest.raises(ValueError): load_experiment(path)


def test_old_field_rejected(tables):
    root, config, _ = tables
    config['dataset_ref'] = config.pop('dataset_refs')[0]
    write_yaml(root/'old.yaml', config)
    with pytest.raises(ValueError): load_experiment(root/'old.yaml')


def test_extension_preserves_288_and_adds_72():
    root = Path(__file__).resolve().parents[1]/'experiments/configs'
    path = root/'aagu032_extend_v2/experiment.yaml'
    merged = load_experiment(path)
    dry = execute(path, dry_run=True)
    assert dry['logical_cells'] == 360 and not dry['producer_called']
    assert [d['dataset']['name'].lower() for d in merged['datasets']] == ['cora','citeseer','pubmed']
    for d in merged['datasets']:
        assert d['split']['seed'] == 2024
        assert [d['split'][key] for key in ('train_ratio','val_ratio','test_ratio')] == [.7,.1,.2]
    # Existing extension tables own the retained eight-selector conditions.
    for suffix in ('', '.citeseer', '.pubmed'):
        original = load_experiment(root / ('aagu032_extend/experiment'+suffix+'.yaml'))
        assert merged['selector_refs'][:8] == original['selector_refs']
        for field in ('unlearning_refs','evaluation_refs','seeds','budget_ratios'):
            assert merged[field] == original[field]
    assert merged['selector_refs'][8:] == ['gt_full_all_trainable_hops3.yaml','gt_full_sgc_all_trainable_hops3.yaml']
    assert len(merged['selectors'][:8])*3*3*4 == 288
    assert len(merged['selectors'][8:])*3*3*4 == 72
