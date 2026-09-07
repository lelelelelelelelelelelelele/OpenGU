"""AAGU-036: measured files, real cold/warm entry and Core dependency collection."""
import copy
import hashlib
import json
import os
import pickle
from pathlib import Path

import numpy as np
import pytest
import torch
import yaml
from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, commit, declaration
from test_syncmate_gu_outputs import collect
from test_unified_execution import command
from experiments.modular_artifacts import read_summary_outputs, output_paths
from experiments.unlearning_outputs import load_output, restore_model
from experiments.dataset_inputs import resolve_input
from utils.target_checkpoint import data_identity, sha256_file
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context, devices
from scripts.syncmate.opengu_inputs import collect_inputs


def inventory(root):
    return {p.relative_to(root).as_posix(): p.stat().st_size
            for p in sorted(root.rglob('*')) if p.is_file()}


@pytest.mark.parametrize('shape', [(20, 3), (1200, 256)])
def test_shared_inputs_real_growth_collection_and_faults(workspace, shape, monkeypatch, record_property):
    root, config_path, config = workspace
    n, width = shape
    torch.manual_seed(36)
    from torch_geometric.data import Data
    nodes = torch.arange(n)
    data = Data(x=torch.randn(n, width), y=nodes % 2,
        edge_index=torch.stack([nodes, (nodes + 1) % n]),
        train_mask=nodes < n//2, val_mask=(nodes >= n//2) & (nodes < n*3//4),
        test_mask=nodes >= n*3//4)
    graph = root / 'data/processed/graph.pkl'
    graph.write_bytes(pickle.dumps(data))
    manifest_path = root / 'data/processed/dataset.json'
    manifest = json.loads(manifest_path.read_text())
    manifest.update(data_sha256=sha256_file(graph), data_identity=data_identity(data))
    manifest_path.write_text(json.dumps(manifest))
    dataset = yaml.safe_load((root / 'dataset.yaml').read_text())
    dataset['artifacts'].update(manifest_sha256=sha256_file(manifest_path),
                                split_hash=data_identity(data)['split_hash'])
    write_yaml(root / 'dataset.yaml', dataset)
    selector = yaml.safe_load((root/'degree.yaml').read_text())
    selector['budget'] = {'mode':'ratio','value':.1}
    write_yaml(root/'degree.yaml',selector)
    config.update(stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['retrain.yaml'], seeds=[122, 722], budget_ratios=[.1, .2])
    write_yaml(config_path, config)
    sha = commit(root)
    monkeypatch.setenv('OMP_NUM_THREADS', '1')
    monkeypatch.setenv('MKL_NUM_THREADS', '1')
    inputs_before = inventory(root / 'data/processed')
    cold = command(root, config_path, 'cold')
    cache_before_warm = inventory(root / 'results/cache_v2')
    warm = command(root, config_path, 'warm', poison=True)
    assert inventory(root / 'data/processed') == inputs_before
    assert inventory(root / 'results/cache_v2') == cache_before_warm
    assert all(r['producer_called'] and not r['hit'] for r in cold['unlearning'])
    assert all(r['hit'] and not r['producer_called'] for r in warm['unlearning'])
    assert [r['output'] for r in cold['unlearning']] == [r['output'] for r in warm['unlearning']]
    warm_trace = json.loads((root / 'warm.trace.json').read_text())
    assert warm_trace == {'training_seeds': [], 'score_calls': []}
    summary = Path(cold['execution_receipt']['output'])
    _, outputs = read_summary_outputs(summary, sha256_file(summary), dataset_root=root)
    forbidden = {'x','y','edge_index','train_mask','val_mask','test_mask',
                 'retain_mask','training_edge_index','evaluation_edge_index'}
    fixed_bytes = sum(getattr(data, k).numpy().nbytes for k in
                      ('x','y','edge_index','train_mask','val_mask','test_mask'))
    sizes = []
    for row, result in zip(cold['unlearning'], outputs):
        payload = result['payload']
        assert not forbidden.intersection(payload.payload.arrays)
        cache = load_output(row['output'], root/'results/cache_v2', dataset_root=root)
        assert cache.canonical_bytes == payload.canonical_bytes
        for k in ('x','y','edge_index','train_mask','val_mask','test_mask'):
            np.testing.assert_array_equal(payload.arrays[k], getattr(data,k).numpy())
        with torch.no_grad():
            logits = restore_model(payload)(torch.tensor(payload.arrays['x']),
                                           torch.tensor(payload.arrays['evaluation_edge_index']))
        np.testing.assert_array_equal(logits.numpy(), payload.arrays['logits'])
        # Actual uncompressed archive with the old fixed-array layout, only a size control.
        from cache_v2.formal_artifacts import _archive_bytes, _npy_bytes
        old = _archive_bytes([(k+'.npy', _npy_bytes(v)) for k,v in payload.arrays.items()])
        new = _archive_bytes([(k+'.npy', _npy_bytes(v)) for k,v in payload.payload.arrays.items()])
        controls = root/'.syncmate/size-controls'; controls.mkdir(exist_ok=True)
        (controls/(str(len(sizes))+'-old.npz')).write_bytes(old)
        (controls/(str(len(sizes))+'-new.npz')).write_bytes(new)
        sizes.append({'old_array_archive_bytes':len(old), 'new_array_archive_bytes':len(new),
                      'result_payload_bytes':len(payload.canonical_bytes)})
    collector = root / 'collector'; collector.mkdir()
    for p in root.glob('*.yaml'):
        (collector/p.name).write_bytes(p.read_bytes())
    with pytest.raises(FileNotFoundError):
        read_summary_outputs(summary, sha256_file(summary), dataset_root=collector)
    def no_producer(*args, **kwargs):
        raise AssertionError('offline input handling started training')
    monkeypatch.setattr(torch.optim.Adam, 'step', no_producer)
    definition = declaration(root, config_path, 'unlearning')
    definition['run_identity']['run_id'] = 'cold'
    relative = summary.relative_to(root).as_posix()
    definition['expected_artifact_paths'] = [relative] + list(output_paths(relative,4))
    definition['collector_result_roots'] = [str(Path(relative).parent).replace('\\','/')]
    definition['expected_datasets'] = [{'num_nodes':n,'candidate_count':n//2}]
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        peer = devices.build_peer_config('runner',None,str(root),transport='local')
        opts = dict(node_id='cpu-runner', ssh=devices.transport_ssh_value(peer),
                    repo_path=str(root), project_root=collector, expected_git_sha=sha)
        transfer = collect_inputs(collector/'experiment.yaml', **opts)
        repeat = collect_inputs(collector/'experiment.yaml', **opts)
        assert sum(p['fetched'] for p in transfer['phases']) == 2
        assert sum(p['fetched'] for p in repeat['phases']) == 0
        collected, _, _ = collect((root, collector, sha, definition))
        acceptance = extension.accept('modular-output-v1',definition,collected)
        assert acceptance['passed'], acceptance
    assert not (collector/'results/cache_v2').exists()
    assert inventory(collector/'data/processed') == inputs_before
    reference = outputs[0]['payload'].identity['dataset_input']
    restored_graph = collector/'data/processed/graph.pkl'
    original = restored_graph.read_bytes()
    restored_graph.write_bytes(original + b'corrupt')
    with context.use(collector, extension=extension):
        with pytest.raises(ValueError, match='conflicts'):
            collect_inputs(collector/'experiment.yaml', **opts)
    with pytest.raises(ValueError, match='digest'):
        resolve_input(reference, collector)
    restored_graph.unlink()
    with pytest.raises(FileNotFoundError):
        resolve_input(reference, collector)
    restored_graph.write_bytes(original)
    wrong = copy.deepcopy(reference)
    wrong['instance']['split']['seed'] += 1
    with pytest.raises(ValueError, match='split mismatch'):
        resolve_input(wrong, collector)
    wrong = copy.deepcopy(reference); wrong['manifest'] = '../dataset.json'
    with pytest.raises(ValueError, match='unsafe'):
        resolve_input(wrong, collector)
    evidence = {'shape':shape,'cells':4,'runs':2, 'fixed_input_array_bytes':fixed_bytes,
        'shared_files':inputs_before,'array_archive_controls':sizes,
        'cache_files':cache_before_warm,'cold_export_files':inventory(summary.parent),
        'warm_export_files':inventory(Path(warm['execution_receipt']['output']).parent),
        'collected_files':inventory(collector/'results'),
        'first_dependency_collection':transfer,'repeat_dependency_collection':repeat,
        'cold_trace':json.loads((root/'cold.trace.json').read_text()),'warm_trace':warm_trace,
        'checks':{'restored_logits_exact':True,'metrics_verified_after_collection':True,
                  'missing_corrupt_wrong_split_rejected':True}}
    record_property('storage_evidence',json.dumps(evidence))
    if os.environ.get('AAGU036_EVIDENCE'):
        destination = Path(os.environ['AAGU036_EVIDENCE']); destination.mkdir(parents=True,exist_ok=True)
        (destination/('storage-'+str(n)+'.json')).write_text(json.dumps(evidence,indent=2))
