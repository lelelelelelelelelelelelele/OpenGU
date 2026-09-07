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
from experiments.modular_artifacts import read_run, output_paths
from experiments.unlearning_outputs import load_output, restore_model
from experiments.dataset_inputs import resolve_input
from utils.target_checkpoint import data_identity, sha256_file
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context, devices


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
    warm = command(root, config_path, 'warm', poison=True)
    assert inventory(root / 'data/processed') == inputs_before
    assert all(r['producer_called'] and not r['hit'] for r in cold['unlearning'])
    assert all(r['hit'] and not r['producer_called'] for r in warm['unlearning'])
    assert [r['output'] for r in cold['unlearning']] == [r['output'] for r in warm['unlearning']]
    warm_trace = json.loads((root / 'warm.trace.json').read_text())
    assert warm_trace == {'training_seeds': [], 'score_calls': []}
    summary = Path(cold['execution_receipt']['output'])
    returned, documents = read_run(summary, sha256_file(summary))
    for row, document in zip(cold['unlearning'], documents):
        assert document['metrics.json']['rows'][0]['values'] == row['evaluation']['metrics']
        assert document['selection.json']['requested_k'] == int((n//2)*row['matrix_values']['budget_ratio'])
    files = inventory(summary.parent)
    assert len(files) == 9
    assert {Path(p).name for p in files} == {'run.json', 'metrics.json', 'selection.json'}
    assert not any(key in summary.read_text() for key in ('effective_selectors', 'configuration_sources', 'dataset_input'))
    collector = root / 'collector'; collector.mkdir()
    for p in root.glob('*.yaml'):
        (collector/p.name).write_bytes(p.read_bytes())
    definition = declaration(root, config_path, 'unlearning')
    definition['run_identity']['run_id'] = 'cold'
    relative = summary.relative_to(root).as_posix()
    from experiments.modular_config import load_experiment
    definition['expected_artifact_paths'] = [relative] + list(output_paths(relative, load_experiment(config_path)))
    definition['collector_result_roots'] = [Path(relative).parent.as_posix()]
    definition['expected_datasets'] = [{'num_nodes':n,'candidate_count':n//2}]
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        collected, _, _ = collect((root, collector, sha, definition))
        acceptance = extension.accept('modular-output-v1',definition,collected)
        assert acceptance['passed'], acceptance
    assert not (collector/'results/cache_v2').exists()
    assert not (collector/'data').exists()
    evidence = {'shape':shape,'cells':4,'runs':2,
        'cold_export_files':files, 'cold_bytes':sum(files.values()),
        'warm_export_files':inventory(Path(warm['execution_receipt']['output']).parent),
        'collected_files':inventory(collector/'results'), 'warm_trace':warm_trace,
        'checks':{'metrics_equal':True,'no_inputs_or_payload_collected':True}}
    record_property('storage_evidence',json.dumps(evidence))
    if os.environ.get('AAGU036_EVIDENCE'):
        destination = Path(os.environ['AAGU036_EVIDENCE']); destination.mkdir(parents=True,exist_ok=True)
        (destination/('storage-'+str(n)+'.json')).write_text(json.dumps(evidence,indent=2))
