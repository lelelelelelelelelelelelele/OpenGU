"""Reproducible disposable CPU example for Selection -> GU/Retrain -> Metrics."""
from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import torch
import yaml
from torch_geometric.data import Data
from experiments.modular_execution import ExecutionContext
from experiments.modular_run import execute
from utils.target_checkpoint import data_identity, sha256_file


def write_yaml(path, value):
    if value.get('kind') == 'experiment':
        value = dict(value)
        value['dataset_ref'] = str((path.parent / value['dataset_ref']).resolve())
        for field in ('selector_refs', 'unlearning_refs', 'evaluation_refs'):
            if field in value:
                value[field] = [str((path.parent / ref).resolve()) for ref in value[field]]
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding='utf-8')


def run_example(directory):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    torch.set_num_threads(1)
    torch.manual_seed(17)
    n = 24
    edges = torch.stack((torch.arange(n - 1), torch.arange(1, n)))
    data = Data(x=torch.randn(n, 3), y=torch.arange(n) % 2,
        edge_index=torch.cat((edges, edges.flip(0)), dim=1),
        train_mask=torch.arange(n) < 12,
        val_mask=(torch.arange(n) >= 12) & (torch.arange(n) < 17),
        test_mask=torch.arange(n) >= 17)
    (directory / 'graph.pkl').write_bytes(pickle.dumps(data))
    dataset = {'kind': 'dataset_split', 'schema_version': 1,
        'dataset': {'name': 'cpu_example'}, 'preprocessing': {'adapter': 'OpenGU_persisted_processed_pair'},
        'split': {'profile': 'disposable24', 'train_ratio': .5, 'val_ratio': 5/24,
                  'test_ratio': 7/24, 'seed': 17}}
    manifest = {key: dataset[key] for key in ('dataset', 'preprocessing', 'split')}
    manifest.update(schema='opengu.persisted_dataset_split', version=1, data_path='graph.pkl',
                    data_sha256=sha256_file(directory / 'graph.pkl'), data_identity=data_identity(data))
    (directory / 'dataset.json').write_text(json.dumps(manifest), encoding='utf-8')
    dataset['artifacts'] = {'manifest': 'dataset.json',
        'manifest_sha256': sha256_file(directory / 'dataset.json'),
        'split_hash': data_identity(data)['split_hash'], 'node_id_space': 'pyg-global-node-index-v1'}
    write_yaml(directory / 'dataset.yaml', dataset)
    write_yaml(directory / 'degree.yaml', {'kind': 'selector', 'schema_version': 1, 'method': 'degree',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 2}})
    for method, parameters in (('Retrain', {}), ('GNNDelete', {'unlearning_epochs': 3}), ('GIF', {'iteration': 3})):
        write_yaml(directory / (method + '.yaml'), {'kind': 'unlearning', 'schema_version': 1,
            'method': method, 'model': {'hidden_channels': 4}, 'training': {'epochs': 4},
            'parameters': parameters})
    write_yaml(directory / 'gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
                                      'case': 'post_unlearning_utility_and_retrain_gap'})
    base = {'kind': 'experiment', 'schema_version': 1, 'dataset_ref': 'dataset.yaml',
            'matrix': 'cartesian_product'}
    def run(name, **fields):
        path = directory / (name + '.yaml')
        write_yaml(path, {**base, 'experiment_id': name, **fields})
        context = ExecutionContext(name, 'verification', 'cpu', directory / 'store',
            directory / 'checkpoints', directory / 'runtime' / name, directory / (name + '.json'),
            'aagu028-disposable-example')
        return execute(path, context=context)
    selected = run('01-selection', stage='selector', selector_refs=['degree.yaml'])
    common = {'stage': 'unlearning', 'selector_refs': ['degree.yaml']}
    gu = run('02-gu', **common, unlearning_refs=['GNNDelete.yaml', 'GIF.yaml'])['unlearning']
    cold = run('03-retrain', **common, unlearning_refs=['Retrain.yaml'])['unlearning'][0]
    pairs = [{'unlearning': row['output'], 'retrain': cold['output']} for row in gu]
    def forbidden(*args, **kwargs):
        raise AssertionError('training invoked during Metrics or hot Retrain read')
    write_yaml(directory / 'single.yaml', {'kind': 'evaluation', 'schema_version': 1, 'case': 'post_method_metrics'})
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbidden)
    try:
        with patch.object(torch.optim.Adam, 'step', forbidden), patch.object(torch.optim.SGD, 'step', forbidden):
            warm = run('04-retrain-hot', **common, unlearning_refs=['Retrain.yaml'])['unlearning'][0]
            single = run('05-single-metrics', stage='metrics', output_inputs=[row['output'] for row in [*gu, cold]], evaluation_refs=['single.yaml'])
            metrics = run('06-metrics', stage='metrics', output_inputs=pairs, evaluation_refs=['gap.yaml'])
            repeat = run('07-metrics-repeat', stage='metrics', output_inputs=pairs, evaluation_refs=['gap.yaml'])
    finally:
        hook.remove()
    assert cold['output'] == warm['output'] and warm['hit']
    assert metrics['evaluations'] == repeat['evaluations']
    cli_pairs = [{'strategy': method, **pair} for method, pair in zip(('GNNDelete', 'GIF'), pairs)]
    (directory / 'output-references.json').write_text(json.dumps(cli_pairs, indent=2), encoding='utf-8')
    receipt = {'retrain_output': cold['output'], 'GU_outputs': [row['output'] for row in gu],
               'hot_retrain_producer_called': warm['producer_called'],
               'metrics': metrics['evaluations'], 'metrics_repeat_equal': True,
               'single_method_metrics': single['evaluations'], 'method_order': ['GNNDelete', 'GIF', 'Retrain'],
               'forward_forbidden_during_reads': True,
               'training_steps_forbidden_during_reads': True, 'software_evidence_only': True}
    (directory / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True, help='New disposable directory')
    args = parser.parse_args()
    receipt = run_example(args.directory)
    print(json.dumps(receipt, indent=2))
