"""YAML-driven fixed-PT validation; no computation cache or tensor export.

Uses the production GIF/IDEA system seam and fresh Retrain implementation.
Only scalar observations and selected node IDs are persisted per run.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SCHEMA = 'aagu066.validation.v1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def load_plan(path):
    from experiments.modular_config import load_experiment, configuration_fingerprint
    import yaml
    path = Path(path).resolve()
    config = load_experiment(path)
    policy_path = path.parent / 'validation.yaml'
    policy = yaml.safe_load(policy_path.read_text(encoding='utf-8'))
    expected_seeds = {'aagu066-cora-h16': [104246, 104247, 104248],
                      'aagu066-cora-h16-gate': [104248]}
    if (config['experiment_id'] not in expected_seeds or config['stage'] != 'unlearning'
            or config.get('budget_ratios') != [0.1]
            or config.get('random_selector_seeds') != expected_seeds[config['experiment_id']]
            or len(config['datasets']) != 1 or config['datasets'][0]['dataset']['name'] != 'Cora'
            or len(config['selectors']) != 1 or config['selectors'][0]['method'] != 'random'
            or [u['method'] for u in config['unlearnings']] != ['GIF', 'IDEA', 'Retrain']):
        raise ValueError('configuration differs from the frozen AAGU-066 matrix')
    for instance in config['unlearnings']:
        if instance['training']['seed'] != 42:
            raise ValueError('training seed must remain 42')
        if instance['model'] != {'architecture': 'OpenGU.GCNNet', 'layers': 2,
                                 'hidden_channels': 16, 'dropout': 0.5}:
            raise ValueError('AAGU-066 requires two-layer H16 GCN')
        if instance['method'] != 'Retrain':
            params = instance['parameters']
            if (not instance.get('checkpoint') or params['iteration'] != 100
                    or params['scale'] != 9000 or params['damp'] != 2048 / 9000
                    or params.get('gaussian_mean', 0) != 0 or params.get('gaussian_std', 0) != 0):
                raise ValueError('GIF/IDEA parameters differ from accepted frozen settings')
        elif instance['training'] != dict(seed=42, epochs=3000, optimizer='Adam',
                                          lr=0.05, weight_decay=0.0001, scheduler='none'):
            raise ValueError('Retrain must train from scratch with the paired 3000-epoch settings')
    if policy['diagnostic_iterations'] != [100, 200, 400]:
        raise ValueError('diagnostic budgets must be T/2T/4T')
    fingerprint = digest({'experiment': configuration_fingerprint(path), 'validation': policy})
    return config, policy, fingerprint


def artifact_names(config):
    names = ['run.json']
    for seed in config['random_selector_seeds']:
        names += [f'seed{seed}/selection.json', f'seed{seed}/reference.json']
        names += [f'seed{seed}/{method.lower()}.json' for method in ('GIF', 'IDEA', 'Retrain')]
    return tuple(names)


def select_nodes(data, seed, ratio):
    from experiments.c_target_v1.core import stable_ranking
    from experiments.target_direct_v1.scoring import deterministic_random_scores
    candidates = data.train_mask.nonzero().flatten().cpu().tolist()
    return list(stable_ranking(candidates, deterministic_random_scores(len(candidates), seed))
                [:int(len(candidates) * ratio)])


def norm(value):
    return float(value.detach().double().norm())


def flat(model):
    import torch
    return torch.cat([p.detach().reshape(-1) for p in model.parameters() if p.requires_grad])


def predict(model, graph):
    import torch
    model.eval()
    with torch.no_grad():
        result = model(graph.x, graph.edge_index).detach()
    if not torch.isfinite(result).all():
        raise ValueError('nonfinite predictions')
    return result


def metrics(logits, data, nodes):
    import torch
    from sklearn.metrics import f1_score
    masks = {name: getattr(data, name + '_mask').clone() for name in ('train', 'val', 'test')}
    masks['deleted'] = torch.zeros_like(data.train_mask)
    masks['deleted'][nodes] = True
    masks['retained_train'] = data.train_mask & ~masks['deleted']
    result = {}
    for name, mask in masks.items():
        truth, pred = data.y[mask], logits[mask].argmax(1)
        result[name] = {'count': int(mask.sum()), 'accuracy': float((truth == pred).float().mean()),
                        'macro_f1': float(f1_score(truth.cpu(), pred.cpu(), average='macro', zero_division=0))}
    return result


def compare(left, right, data):
    difference = left - right
    flipped = left.argmax(1) != right.argmax(1)
    return {'logits_l2': norm(difference), 'logits_max_abs': float(difference.abs().max()),
            'logits_relative_l2': norm(difference) / max(norm(right), 1e-30),
            'flips_all': int(flipped.sum()), 'flips_test': int(flipped[data.test_mask].sum())}


def measured_update(matvec, rhs, budgets, scale, damp):
    """One recurrence, with in-memory snapshots; diagnostic reads do not update it."""
    import torch
    estimate = rhs.detach().clone()
    snapshots, trace = {}, []
    for step in range(max(budgets) + 1):
        delta = estimate / scale
        curvature = matvec(delta.detach()).detach()
        if not torch.isfinite(delta).all() or not torch.isfinite(curvature).all():
            raise ValueError(f'nonfinite solver at iteration {step}')
        trace.append({'iteration': step, 'shifted_relative_residual':
                      norm(curvature + scale * damp * delta - rhs) / max(norm(rhs), 1e-30),
                      'original_relative_residual': norm(curvature - rhs) / max(norm(rhs), 1e-30),
                      'delta_l2': norm(delta), 'finite': True})
        if step in budgets:
            snapshots[step] = delta.detach().clone()
        if step < max(budgets):
            product = matvec(estimate.detach()).detach()
            with torch.no_grad():
                estimate = rhs + (1 - damp) * estimate - product / scale
    return snapshots, trace


def read_prior(policy, seed, method, data_identity, nodes, checkpoint, parameters, root):
    """Read exact registered diagnostic files, never a computation-cache lookup."""
    from utils.target_checkpoint import sha256_file
    binding = policy['prior_diagnostics'].get(str(seed))
    if binding is None:
        return None
    documents = {}
    for relative, expected_hash in binding['files'].items():
        path = Path(root) / relative
        if sha256_file(path) != expected_hash:
            raise ValueError('prior diagnostic checksum mismatch: ' + relative)
        documents[Path(relative).name] = json.loads(path.read_text(encoding='utf-8'))
    run = documents['run.json']
    production_paths = ['experiments/aagu059_diagnostic.py', 'experiments/modular_gu.py',
        'experiments/modular_idea.py', 'model/base_gnn/gcn.py', 'task/GIFTrainer.py',
        'task/IDEATrainer.py', 'unlearning/unlearning_methods/GIF',
        'unlearning/unlearning_methods/IDEA']
    unchanged = subprocess.run(['git', 'diff', '--quiet', run['commit'], 'HEAD', '--', *production_paths],
                               cwd=root, capture_output=True)
    if unchanged.returncode != 0:
        raise ValueError('production system changed since the bound diagnostic; evidence cannot be reused')
    selection_hash = hashlib.sha256(json.dumps(nodes, separators=(',', ':')).encode()).hexdigest()
    if (run['data_identity'] != data_identity or run['selection']['selected_nodes_sha256'] != selection_hash
            or run['contract']['selector']['seed'] != seed or run['status'] != 'diagnostic_complete'):
        raise ValueError('prior diagnostic data/request identity mismatch')
    rows = sorted([row for row in documents.values()
                   if row.get('method') == method and 'trace' in row], key=lambda row: row['iteration'])
    if [row['iteration'] for row in rows] != policy['diagnostic_iterations']:
        raise ValueError('prior diagnostic budgets incomplete')
    for row in rows:
        if (row['checkpoint']['state_hash'] != checkpoint['state_hash']
                or row['checkpoint']['file_sha256'] != checkpoint['file_sha256']
                or row['scale'] != parameters['scale'] or row['damp'] != parameters['damp']
                or row['status'] != 'finite_truncation' or not row['original_weights_unchanged']):
            raise ValueError('prior diagnostic parameter/PT/finite mismatch')
    return {'trace': rows[-1]['trace'], 'points': [row['trace'][-1] for row in rows],
            'budget_norm_relative_difference': max(abs(row['delta_l2'] - rows[0]['delta_l2'])
                / max(rows[0]['delta_l2'], 1e-30) for row in rows),
            'source': binding, 'reference_delta_l2': rows[0]['delta_l2']}


def numerical_checks(diagnostics, update, rhs, same_graph, policy):
    return {'residual': all(point['shifted_relative_residual'] <= policy['residual_tolerance']
                            for point in diagnostics['points']),
            'budget_consistency': diagnostics['budget_norm_relative_difference'] <= policy['budget_tolerance'],
            'nonzero_update': norm(update) / max(norm(rhs), 1e-30) > policy['near_zero_update_to_rhs'],
            'nonzero_logits': same_graph['logits_max_abs'] > policy['near_zero_logits_max_abs']}


def verify_run(path, config_path, expected_commit=None):
    """Validate a collected run using scalar files only; never load formal data."""
    from utils.target_checkpoint import sha256_file
    config, policy, fingerprint = load_plan(config_path)
    path = Path(path)
    run = json.loads(path.read_text(encoding='utf-8'))
    expected_names = set(artifact_names(config)) - {'run.json'}
    if (run['schema'] != SCHEMA or run['status'] != 'completed'
            or run['experiment_id'] != config['experiment_id']
            or run['configuration_fingerprint'] != fingerprint or run['policy'] != policy
            or run['data_identity'] != policy['data_identity']
            or (expected_commit is not None and run['commit'] != expected_commit)
            or set(run['files']) != expected_names
            or [r['seed'] for r in run['requests']] != config['random_selector_seeds']
            or any(r['status'] != 'completed' for r in run['requests'])):
        raise ValueError('run identity, completion, or file coverage mismatch')
    documents = {}
    for name in expected_names:
        if sha256_file(path.parent / name) != run['files'][name]:
            raise ValueError('result checksum mismatch: ' + name)
        documents[name] = json.loads((path.parent / name).read_text(encoding='utf-8'))
    passed = []
    for request in run['requests']:
        seed = request['seed']
        selection = documents[f'seed{seed}/selection.json']
        nodes = selection['selected_nodes']
        actual_hash = hashlib.sha256(json.dumps(nodes, separators=(',', ':')).encode()).hexdigest()
        if (selection['seed'] != seed or selection['requested_k'] != 189 or len(nodes) != 189
                or len(set(nodes)) != 189 or any(type(n) is not int or not 0 <= n < 2708 for n in nodes)
                or actual_hash != selection['selected_nodes_sha256']):
            raise ValueError('invalid request identity or selected nodes')
        reference = documents[f'seed{seed}/reference.json']
        if reference['checkpoint']['file_sha256'] != policy['checkpoint_sha256']:
            raise ValueError('reference PT mismatch')
        numerical = []
        for method in ('gif', 'idea', 'retrain'):
            row = documents[f'seed{seed}/{method}.json']
            if (row['selection_sha256'] != actual_hash or row['seed'] != seed
                    or row['method'].lower() != method or row['status'] != 'completed'):
                raise ValueError('unpaired method result')
            if method != 'retrain':
                if row['numerical_passed'] != all(row['checks'].values()):
                    raise ValueError('numerical verdict mismatch')
                numerical.append(row['numerical_passed'])
        if request['numerical_passed'] != all(numerical):
            raise ValueError('request verdict mismatch')
        passed.extend(numerical)
    if run['numerical_passed'] != all(passed):
        raise ValueError('table verdict mismatch')
    return run, documents


def run_request(batch, policy, data, output, root, checkpoint_root):
    import torch
    from experiments.modular_model import prepare_model
    from experiments.node_deletion import retained_graph
    from experiments.aagu059_diagnostic import capture_system
    from unlearning.unlearning_methods.GIF.solver import solve_gif_system
    from unlearning.unlearning_methods.Retrain.retrain import run_retrain
    from utils.target_checkpoint import data_identity, state_hash

    seed = batch['selectors'][0]['parameters']['seed']
    nodes = select_nodes(data, seed, batch['matrix_values']['budget_ratio'])
    selected = {'seed': seed, 'requested_k': len(nodes), 'selected_nodes': nodes,
                'selected_nodes_sha256': hashlib.sha256(json.dumps(nodes, separators=(',', ':')).encode()).hexdigest()}
    write(output / 'selection.json', selected)
    original, _, checkpoint = prepare_model(batch['unlearnings'][0], data=data, dataset_name='Cora',
        checkpoint_root=checkpoint_root, device=data.x.device, reference_directory=root)
    if checkpoint['source'] != 'external_state_dict' or checkpoint['file_sha256'] != policy['checkpoint_sha256']:
        raise ValueError('fixed PT identity mismatch')
    original.eval()
    saved_hash = state_hash(original.state_dict())
    baseline = flat(original).clone()
    graphs = {'original': data, 'retained': retained_graph(data, nodes)}
    before = {name: predict(original, graph) for name, graph in graphs.items()}
    write(output / 'reference.json', {'checkpoint': checkpoint, 'selection_sha256': selected['selected_nodes_sha256'],
        'metrics': {name: metrics(logits, data, nodes) for name, logits in before.items()},
        'graph_only_change': compare(before['retained'], before['original'], data)})

    retrain_instance = batch['unlearnings'][2]
    retrain, seconds = run_retrain(retrain_instance, data, nodes, 'Cora')
    retrain_predictions = {name: predict(retrain, graph) for name, graph in graphs.items()}
    retrain_metrics = {name: metrics(value, data, nodes) for name, value in retrain_predictions.items()}
    write(output / 'retrain.json', {'method': 'Retrain', 'seed': seed, 'status': 'completed',
        'selection_sha256': selected['selected_nodes_sha256'], 'training': retrain_instance['training'],
        'seconds': seconds, 'metrics': retrain_metrics,
        'weight_update_l2': norm(flat(retrain) - baseline),
        'relative_weight_update_l2': norm(flat(retrain) - baseline) / max(norm(baseline), 1e-30),
        'versus_original_weights': {name: compare(value, before[name], data) for name, value in retrain_predictions.items()}})
    del retrain
    all_passed = True
    for instance in batch['unlearnings'][:2]:
        started = time.perf_counter()
        method, params = instance['method'], instance['parameters']
        if Path(instance['checkpoint']).resolve() != Path(checkpoint['path']).resolve():
            raise ValueError('GIF and IDEA must share the same fixed PT')
        working = data.clone()
        working.num_classes = int(data.y.max()) + 1
        for split in ('train', 'val', 'test'):
            setattr(working, split + '_indices', getattr(working, split + '_mask').nonzero().flatten().cpu().numpy())
        system = capture_system(instance, original, working, nodes, output)
        rhs, matvec = system['rhs'], system['matvec']
        prior = read_prior(policy, seed, method, data_identity(data), nodes, checkpoint, params, root)
        if prior is not None:
            update, production = solve_gif_system(matvec, rhs, iterations=params['iteration'],
                                                  scale=params['scale'], damp=params['damp'])
            diagnostics = prior
            diagnostics['current_trace'] = production['trace']
            if abs(norm(update) - prior['reference_delta_l2']) / max(prior['reference_delta_l2'], 1e-30) > policy['budget_tolerance']:
                raise ValueError('current update differs from bound diagnostic')
            current_residual = production['relative_residual']
        else:
            snapshots, trace = measured_update(matvec, rhs, policy['diagnostic_iterations'], params['scale'], params['damp'])
            update = snapshots[params['iteration']]
            diagnostics = {'trace': trace, 'points': [trace[t] for t in policy['diagnostic_iterations']],
                'budget_norm_relative_difference': max(abs(norm(value) - norm(update)) / max(norm(update), 1e-30)
                                                       for value in snapshots.values()),
                'budget_vector_relative_difference': max(norm(value - update) / max(norm(update), 1e-30)
                                                         for value in snapshots.values())}
            production_update, production = solve_gif_system(matvec, rhs, iterations=params['iteration'],
                                                              scale=params['scale'], damp=params['damp'])
            if norm(production_update - update) / max(norm(update), 1e-30) > 1e-5:
                raise ValueError('diagnostic recurrence differs from production solver')
            current_residual = production['relative_residual']
        candidate = copy.deepcopy(original).eval()
        sizes = [p.numel() for p in candidate.parameters() if p.requires_grad]
        with torch.no_grad():
            for param, part in zip((p for p in candidate.parameters() if p.requires_grad), update.split(sizes)):
                param.add_(part.reshape_as(param))
        predictions = {name: predict(candidate, graph) for name, graph in graphs.items()}
        comparisons = {name: compare(value, before[name], data) for name, value in predictions.items()}
        checks = numerical_checks(diagnostics, update, rhs, comparisons['original'], policy)
        checks['current_residual'] = current_residual <= policy['residual_tolerance']
        checks['original_weights_unchanged'] = state_hash(original.state_dict()) == saved_hash
        observed_metrics = {name: metrics(value, data, nodes) for name, value in predictions.items()}
        row = {'method': method, 'seed': seed, 'status': 'completed', 'parameters': params,
            'selection_sha256': selected['selected_nodes_sha256'], 'diagnostics': diagnostics,
            'checks': checks, 'numerical_passed': all(checks.values()),
            'weight_update_l2': norm(flat(candidate) - baseline),
            'relative_weight_update_l2': norm(flat(candidate) - baseline) / max(norm(baseline), 1e-30),
            'writeback_relative_error': norm(flat(candidate) - baseline - update) / max(norm(update), 1e-30),
            'metrics': observed_metrics, 'versus_original_weights': comparisons,
            'versus_retrain': {name: compare(value, retrain_predictions[name], data) for name, value in predictions.items()},
            'test_metric_gap_vs_retrain': {name: {metric: observed_metrics[name]['test'][metric] - retrain_metrics[name]['test'][metric]
                for metric in ('accuracy', 'macro_f1')} for name in graphs}, 'seconds': time.perf_counter() - started}
        write(output / (method.lower() + '.json'), row)
        all_passed &= row['numerical_passed']
        del candidate, system, matvec, rhs
    return all_passed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--dry_run', action='store_true')
    args = parser.parse_args()
    sys.argv[:] = sys.argv[:1]
    config, policy, fingerprint = load_plan(args.config)
    if args.dry_run:
        return {'passed': True, 'dry_run': True, 'producer_called': False,
                'logical_cells': len(config['random_selector_seeds']) * 3,
                'configuration_fingerprint': fingerprint, 'artifacts': artifact_names(config)}
    expected_run = 'aagu066-h16-gate-v1' if config['experiment_id'].endswith('-gate') else 'aagu066-h16-v1'
    if args.run_id != expected_run:
        raise ValueError('run identity differs from the reviewed recipe')
    from experiments.modular_execution import device_context
    from experiments.modular_config import experiment_batches
    from experiments.dataset_inputs import bind_input, resolve_input
    from utils.target_checkpoint import data_identity, sha256_file
    import torch
    torch.set_num_threads(2)
    context = device_context(config['experiment_id'], run_id=args.run_id, device_file=ROOT / '.syncmate/device.yaml')
    if subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True).strip():
        raise ValueError('tracked source is dirty')
    gate_path, gate_documents = None, None
    if config['experiment_id'] == 'aagu066-cora-h16':
        gate_path = ROOT / 'results/runs/aagu066-cora-h16-gate/aagu066-h16-gate-v1/run.json'
        gate, gate_documents = verify_run(gate_path, args.config.parent / 'gate.yaml', context.source_git_sha)
        if not gate['numerical_passed']:
            raise ValueError('formal gate did not pass; full table is blocked')
    output = context.output.parent
    output.mkdir(parents=True, exist_ok=False)
    run = {'schema': SCHEMA, 'experiment_id': config['experiment_id'], 'run_id': args.run_id,
           'commit': context.source_git_sha, 'config_path': args.config.resolve().relative_to(ROOT).as_posix(),
           'configuration_fingerprint': fingerprint, 'status': 'running', 'requests': [], 'files': {},
           'context': context.receipt(), 'policy': policy, 'scientific_acceptance': 'pending'}
    write(context.output, run)
    try:
        batches = list(experiment_batches(config))
        binding = bind_input(batches[0]['dataset'], batches[0]['dataset_directory'], ROOT)
        (ROOT / binding['graph']).resolve().relative_to((ROOT / 'data/processed').resolve())
        data = resolve_input(binding, ROOT).to(context.request_device)
        run['data_identity'] = data_identity(data)
        if run['data_identity'] != policy['data_identity']:
            raise ValueError('dataset identity differs from frozen calibration inputs')
        run['requests'] = [{'seed': b['selectors'][0]['parameters']['seed'], 'status': 'pending'} for b in batches]
        write(context.output, run)
        for batch, request in zip(batches, run['requests']):
            request['status'] = 'running'
            write(context.output, run)
            if config['experiment_id'] == 'aagu066-cora-h16' and request['seed'] == 104248:
                # Reuse the same-code formal gate, not a second run of its request.
                for name, document in gate_documents.items():
                    write(output / name, document)
                request['numerical_passed'] = True
                request['source'] = {'run': gate_path.relative_to(ROOT).as_posix(), 'sha256': sha256_file(gate_path)}
            else:
                request['numerical_passed'] = run_request(batch, policy, data,
                    output / f"seed{request['seed']}", ROOT, context.checkpoint_root)
            request['status'] = 'completed'
            write(context.output, run)
        if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != context.source_git_sha:
            raise ValueError('source changed during execution')
        run['status'] = 'completed'
        run['numerical_passed'] = all(r['numerical_passed'] for r in run['requests'])
    except Exception as exc:
        run.update(status='failed', error=f'{type(exc).__name__}: {exc}')
        for request in run['requests']:
            if request['status'] == 'running':
                request.update(status='failed', error=run['error'])
        raise
    finally:
        run['files'] = {p.relative_to(output).as_posix(): sha256_file(p)
                        for p in output.rglob('*.json') if p != context.output}
        write(context.output, run)
    paths = [str((output / name).relative_to(ROOT)).replace('\\', '/') for name in artifact_names(config)]
    return {'passed': run['status'] == 'completed', 'numerical_passed': run['numerical_passed'],
            'generated_artifacts': sorted(paths)}


if __name__ == '__main__':
    with contextlib.redirect_stdout(sys.stderr):
        result = main()
    print(json.dumps(result))
