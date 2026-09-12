"""Run a bounded, real local Cora comparison for GIF and IDEA.

This is an isolated diagnostic, not a formal table producer.  It trains one
real two-layer OpenGU GCN on a downloaded Planetoid Cora graph, keeps one
checkpoint and one deletion request fixed, and runs the existing modular GIF
and IDEA adapters with several numerical settings.  Outputs belong below
results/diagnostics/AAGU-052 only.
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
from pathlib import Path
import sys
import time

import numpy as np
import torch
from torch_geometric.datasets import Planetoid

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def flatten(values):
    return torch.cat([value.detach().reshape(-1).cpu() for value in values])


def state_copy(model):
    return {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}


def parameter_vector(model):
    return flatten([parameter for parameter in model.parameters() if parameter.requires_grad])


def f1_and_logits(model, data):
    model.eval()
    with torch.no_grad():
        logits = model(data.x, data.edge_index).detach().cpu()
    mask = data.test_mask.cpu()
    f1 = float((logits[mask].argmax(dim=1) == data.y.cpu()[mask]).double().mean())
    return f1, logits


def split_real_cora(data, seed):
    generator = torch.Generator().manual_seed(seed)
    permutation = torch.randperm(data.num_nodes, generator=generator)
    train_count = int(data.num_nodes * 0.7)
    val_count = int(data.num_nodes * 0.1)
    train = permutation[:train_count]
    val = permutation[train_count:train_count + val_count]
    test = permutation[train_count + val_count:]
    for name, indices in [('train', train), ('val', val), ('test', test)]:
        mask = torch.zeros(data.num_nodes, dtype=torch.bool)
        mask[indices] = True
        setattr(data, name + '_mask', mask)
        setattr(data, name + '_indices', indices.numpy())
    return data


def common_args(runtime_defaults, *, method, parameters, model_config, training, k):
    args = runtime_defaults()
    args.update(
        instance={'method': method, 'model': model_config, 'training': training,
                  'parameters': parameters},
        dataset_name='Cora', base_model='GCN', downstream_task='node',
        unlearn_task='node', unlearning_methods=method, GIF_method='GIF',
        num_epochs=training['epochs'], num_runs=1, random_seed=42,
        num_unlearned_nodes=k, formal_expected_k=k, formal_fail_closed=True,
        test_freq=1, device='cpu', gcn_num_layers=model_config['layers'],
        gcn_hidden=model_config['hidden_channels'], run_update_detection_auc=False,
        gaussian_mean=0.0, gaussian_std=0.0,
    )
    args.update(parameters)
    return args


def metrics(model, data, before_state, before_logits, rhs=None, delta=None):
    f1, logits = f1_and_logits(model, data)
    vector = parameter_vector(model)
    baseline = flatten([value for name, value in before_state.items()
                        if name in dict(model.named_parameters())])
    result = {
        'f1': f1,
        'f1_change_pp': (f1 - float((before_logits[data.test_mask].argmax(dim=1)
                                     == data.y.cpu()[data.test_mask]).double().mean())) * 100,
        'logit_max_abs': float((logits - before_logits).abs().max()),
        'logit_rmse': float((logits - before_logits).square().mean().sqrt()),
        'test_class_flips': int((logits[data.test_mask].argmax(dim=1)
                                 != before_logits[data.test_mask].argmax(dim=1)).sum()),
        'parameter_delta_l2': float((vector - baseline).norm()),
        'parameter_delta_relative_l2': float((vector - baseline).norm() / baseline.norm()),
    }
    if rhs is not None and delta is not None:
        result['rhs_l2'] = float(rhs.norm())
        result['delta_l2'] = float(delta.norm())
    return result


def run_gif(args, base_model, data, nodes, before_state, before_logits, root, label):
    from experiments.modular_gu import gif_node

    model = copy.deepcopy(base_model)
    model.load_state_dict(before_state)
    working = data.clone()
    runtime_root = root / ('gif-' + label)
    runtime_root.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    try:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(42)
            output, _ = gif_node(args, model, working, nodes, runtime_root)
        result = metrics(output, data, before_state, before_logits)
        solver_path = runtime_root / 'gif-solver.json'
        solver = json.loads(solver_path.read_text(encoding='utf-8')) if solver_path.exists() else None
        result.update(status='returned', seconds=time.perf_counter() - started,
                      solver=solver)
    except Exception as error:
        solver_path = runtime_root / 'gif-solver.json'
        result = {
            'status': 'failed', 'seconds': time.perf_counter() - started,
            'error_type': type(error).__name__, 'error': str(error),
            'solver': json.loads(solver_path.read_text(encoding='utf-8'))
            if solver_path.exists() else None,
        }
    return result


def run_idea(args, base_model, data, nodes, before_state, before_logits, root, label):
    """Observe the production IDEA adapter; never replace its update function."""
    from experiments.modular_idea import idea_node

    model = copy.deepcopy(base_model)
    model.load_state_dict(before_state)
    runtime_root = root / ('idea-' + label)
    runtime_root.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    try:
        with torch.random.fork_rng(devices=[]):
            torch.manual_seed(42)
            output, _ = idea_node(args, model, data.clone(), nodes, runtime_root)
        result = metrics(output, data, before_state, before_logits)
        result.update(status='returned', seconds=time.perf_counter() - started,
                      solver=json.loads((runtime_root / 'idea-solver.json').read_text()))
    except Exception as error:
        result = {'status': 'failed', 'seconds': time.perf_counter() - started,
                  'error_type': type(error).__name__, 'error': str(error)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--current-iterations', type=int, default=200)
    args_cli = parser.parse_args()
    root = PROJECT_ROOT
    output = args_cli.output.resolve()
    allowed = (root / 'results' / 'diagnostics' / 'AAGU-052').resolve()
    try:
        output.relative_to(allowed)
    except ValueError:
        raise ValueError('output must be a new directory under results/diagnostics/AAGU-052')
    output.mkdir(parents=True, exist_ok=False)
    # OpenGU's config.py parses argv at import time. Keep this diagnostic's
    # arguments out of that parser before importing any project module.
    sys.argv = ['aagu052_local_if_debug']
    logging.basicConfig(level=logging.WARNING)
    torch.set_num_threads(2)

    from attack.cache_identity import seeded_execution
    from experiments.modular_model import create_model, runtime_defaults, train_supervised
    from unlearning.unlearning_methods.Retrain.retrain import run_retrain

    data = Planetoid(str(output / 'planetoid'), 'Cora')[0]
    data = split_real_cora(data, 2024)
    data.num_classes = int(data.y.max()) + 1
    model_config = {'architecture': 'OpenGU.GCNNet', 'layers': 2, 'hidden_channels': 8}
    training = {'epochs': 30, 'optimizer': 'Adam', 'lr': 0.005, 'weight_decay': 0.000001,
                'seed': 42}
    with seeded_execution(42):
        base_model = create_model(model_config, 'Cora', data, torch.device('cpu'))
    with seeded_execution(42):
        train_supervised(base_model, data, training, ())
    before_state = state_copy(base_model)
    baseline_f1, before_logits = f1_and_logits(base_model, data)
    train_nodes = np.asarray(data.train_indices, dtype=np.int64)
    nodes = train_nodes[:max(1, int(len(train_nodes) * 0.01))].tolist()

    cases = [
        ('old_scale_1e9', {'iteration': 100, 'scale': 1000000000, 'damp': 0.0}),
        ('reference_scale_500', {'iteration': 100, 'scale': 500, 'damp': 0.0}),
        ('reference_scale_5000', {'iteration': 100, 'scale': 5000, 'damp': 0.0}),
        ('same_scale_no_damp', {'iteration': args_cli.current_iterations, 'scale': 65536,
                                'damp': 0.0}),
        ('current_shifted', {'iteration': args_cli.current_iterations, 'scale': 65536,
                             'damp': 0.00390625}),
    ]
    instance = {'method': 'Retrain', 'model': model_config, 'training': training}
    with seeded_execution(42):
        retrained, retrain_seconds = run_retrain(instance, data, nodes, 'Cora')
    retrain_metrics = metrics(retrained, data, before_state, before_logits)
    result = {
        'schema': 'aagu052.local_real_if_debug.v1',
        'dataset': 'Cora Planetoid graph', 'split': 'random 70/10/20, seed 2024',
        'model': model_config, 'training': training, 'device': 'cpu',
        'deletion': {'count': len(nodes), 'fraction_of_train': len(nodes) / len(train_nodes),
                     'nodes': nodes},
        'baseline': {'f1': baseline_f1, 'parameter_count': int(parameter_vector(base_model).numel())},
        'retrain': {**retrain_metrics, 'seconds': retrain_seconds},
        'cases': [],
    }
    for label, parameters in cases:
        for method_name, runner in [('GIF', run_gif), ('IDEA', run_idea)]:
            method_args = common_args(runtime_defaults, method=method_name,
                                       parameters=parameters, model_config=model_config,
                                       training=training, k=len(nodes))
            result['cases'].append({
                'method': method_name, 'label': label, 'parameters': parameters,
                'result': runner(method_args, base_model, data, nodes, before_state,
                                 before_logits, output, method_name.lower() + '-' + label),
            })
    result['finished'] = True
    (output / 'result.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
