"""Metrics-only shard trajectories and paired aggregation-loss diagnostics.

Read existing datasets/partitions; never create an experiment cache or checkpoint.
The executed Cora script remains immutable in AAGU-104/evidence/run_curve.py.
"""
from __future__ import annotations
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
import argparse
import copy
import csv
import json
import logging
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace, MethodType
import yaml

ROOT = None
STUDY = {}
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import numpy as np
import torch
from torch.nn import functional as F
from torch_geometric.utils import subgraph
from experiments.modular_model import create_model, runtime_defaults
runtime_defaults()
from experiments.dataset_inputs import resolve_input
from experiments.node_deletion import retained_graph
from experiments.modular_shards import ShardEnsemble, train_shard, aggregate_weights
from experiments.modular_graphrevoker import graphrevoker_weights
from attack.cache_identity import seeded_execution
from utils.target_checkpoint import capture_state, state_hash, data_identity
from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator as Eraser
from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.optimal_aggregator import OptimalAggregator as Revoker
for cls in (Eraser, Revoker):
    sys.modules[cls.__module__].tqdm = lambda xs, **kw: xs

def clock():
    if STUDY['device'].startswith('cuda'):
        torch.cuda.synchronize(torch.device(STUDY['device']))
    return time.perf_counter()

def load_data(cfg):
    data = resolve_input(cfg['dataset_input'], Path(STUDY['data_root']))
    assert data_identity(data) == cfg['data_identity']
    return data.to(torch.device(STUDY['device']))

def utc():
    return datetime.now(timezone.utc).isoformat()

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def event(out, **value):
    value = {'at': utc(), **value}
    with (out / 'events.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False) + '\n')
        f.flush()
    write_json(out / 'progress.json', value)
    print(json.dumps(value, ensure_ascii=False), flush=True)

def shard_graph(data, assignment, i):
    # The exact retained-supervision/filtering operations of train_shard.
    d = data.clone()
    d.train_mask = data.train_mask & (assignment == i)
    assert d.train_mask.any(), 'Empty shard is parameter-infeasible, not zero accuracy.'
    allowed = (assignment == i) | (assignment < 0)
    keep = allowed[data.edge_index[0]] & allowed[data.edge_index[1]]
    d.edge_index = data.edge_index[:, keep]
    return d

def trajectory(cfg, data, assignment, shard, epochs, evaluation_epochs, observe, loss_writer=None):
    d = shard_graph(data, assignment, shard)
    elapsed = 0.0
    with seeded_execution(cfg['training']['seed']):
        model = create_model(cfg['model'], 'shard', data, data.x.device)
        opt = torch.optim.Adam(model.parameters(), lr=cfg['training']['lr'],
                               weight_decay=cfg['training']['weight_decay'])
        scheduler = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=[], gamma=1.0)
        for epoch in range(1, epochs + 1):
            started = clock()
            model.train()
            opt.zero_grad(set_to_none=True)
            logits = model(d.x, d.edge_index)
            loss = F.cross_entropy(logits[d.train_mask], d.y[d.train_mask], reduction='mean')
            loss.backward()
            opt.step()
            scheduler.step()
            loss_value = float(loss.item())
            if not np.isfinite(loss_value):
                raise RuntimeError('nonfinite shard training objective')
            elapsed += clock() - started
            if loss_writer is not None:
                loss_writer.writerow([shard, epoch, loss_value, elapsed, int(d.train_mask.sum())])
            if epoch in evaluation_epochs:
                # Dropout is disabled during evaluation; protect RNG anyway.
                with torch.random.fork_rng(), torch.no_grad():
                    model.eval()
                    observe(epoch, model, elapsed)
        return model.eval(), elapsed

def metrics(z, data, mask):
    return {'accuracy_pct': float((z[mask].argmax(-1) == data.y[mask]).double().mean()) * 100,
            'nll': float(F.cross_entropy(z[mask], data.y[mask])), 'nodes': int(mask.sum())}

def sample(data, cfg):
    with seeded_execution(cfg['training']['seed']):
        nodes = data.train_mask.nonzero().flatten()
        count = cfg['parameters']['num_opt_samples']
        assert count == 1000
        if not len(nodes):
            raise ValueError('aggregation requires retained training nodes')
        count = min(count, len(nodes))
        return nodes[torch.as_tensor(np.random.choice(len(nodes), count, replace=False), device=nodes.device)].sort().values

def corrected_loss(self, posteriors, labels, weights):
    z = torch.zeros_like(posteriors[0])
    for i in range(self.num_shards):
        z += weights[i] * posteriors[i]
    return F.cross_entropy(z, labels) + torch.linalg.vector_norm(weights)

def fit_from_posts(name, cfg, data, posts, arm='original'):
    cls = Eraser if name == 'GraphEraser' else Revoker
    with seeded_execution(cfg['training']['seed']):
        nodes = sample(data, cfg)
        opt = cls(0, SimpleNamespace(model=None), data, cfg['parameters'], logging.getLogger('EXP-082'))
        opt.device = torch.device('cpu')
        # Preserve the original small CPU optimizer; graph forwards use CUDA.
        opt.true_labels = data.y[nodes].cpu()
        opt.posteriors = {i: p.cpu() for i, p in enumerate(posts)}
        if arm == 'corrected':
            opt._loss_fn = MethodType(corrected_loss, opt)
        else:
            assert arm == 'original'
        weights = opt.optimization().detach().to(data.x.device)
        assert torch.isfinite(weights).all() and (weights >= 0).all() and weights.sum() > 0
        return weights

def verify(out):
    checks = []
    # Compare the instrumented optimization against the actual shared producer,
    # including dropout, initialization, loss, scheduler and sampled evaluation.
    for name, cfg in STUDY['methods'].items():
        data = load_data(cfg)
        assignment = torch.tensor(cfg['assignment'], dtype=torch.long, device=data.x.device)
        small = copy.deepcopy(cfg)
        small['training']['epochs'] = 30
        observed = []
        m, training_seconds = trajectory(small, data, assignment, 0, 30, [10, 20, 30],
                         lambda epoch, model, sec: observed.append(float(model(data.x, data.edge_index).sum())))
        reference = train_shard(small, data, assignment, 0)
        a, b = capture_state(m), capture_state(reference)
        for k in a:
            torch.testing.assert_close(a[k], b[k], rtol=1e-4, atol=1e-5)
        models = [m] * cfg['parameters']['num_shards']
        ensemble = ShardEnsemble(models, assignment, torch.ones(len(models), device=data.x.device) / len(models)).eval()
        nodes = sample(data, cfg)
        edges, _ = subgraph(nodes, data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)
        with torch.no_grad():
            posts = [F.log_softmax(model(data.x[nodes], edges), dim=-1) for model in models]
        weights = fit_from_posts(name, cfg, data, posts)
        adapter = aggregate_weights if name == 'GraphEraser' else graphrevoker_weights
        with seeded_execution(cfg['training']['seed']):
            expected = adapter(ensemble, data, cfg['parameters'])
        torch.testing.assert_close(weights.cpu(), expected.cpu(), rtol=1e-4, atol=1e-5)
        for label, r in STUDY['requests'].items():
            nodes_deleted = r['selected_nodes']
            assert len(nodes_deleted) == len(set(nodes_deleted)) and data.train_mask[nodes_deleted].all()
            retained = retained_graph(data, nodes_deleted)
            assert int(retained.train_mask.sum()) == int(data.train_mask.sum()) - len(nodes_deleted)
            for i in range(cfg['parameters']['num_shards']):
                assert shard_graph(retained, assignment, i).train_mask.any()
        checks.append({'method': name, 'instrumented_training_state_exact': all(torch.equal(a[k], b[k]) for k in a),
                       'training_state_close': True, '30_epochs_training_seconds': training_seconds,
                       'state_hash': state_hash(a), 'production_aggregator_weights_exact': torch.equal(weights.cpu(), expected.cpu()),
                       'production_aggregator_weights_close': True,
                       'evaluation_did_not_change_training_rng': True,
                       'data_identity': data_identity(data)})
    write_json(out / 'validation.json', {'complete': True, 'at': utc(), 'checks': checks,
               'source_sha': STUDY['source_sha'],
               'scope': '30-step numerical equivalence; not a scientific result'})

def run(out):
    assert not (out / 'run.json').exists(), 'Do not overwrite or silently restart an attempt.'
    assert json.loads((ROOT / 'verification/validation.json').read_text(encoding='utf-8'))['complete']
    started = clock()
    record = {'experiment_id': 'EXP-082', 'run_id': out.name, 'kind': 'isolated exploratory diagnostic',
        'source_sha': STUDY['source_sha'],
        'started_at': utc(), 'device': STUDY['device'], 'aggregation_device': 'cpu',
        'threads': torch.get_num_threads(), 'torch': torch.__version__,
        'seed': STUDY['seed'], 'epochs': STUDY['epochs'], 'evaluation_epochs': STUDY['evaluation_epochs'],
        'complete': False, 'groups': [], 'saved_checkpoints': 0,
        'test_used_for_selection': False, 'partition_retrained': False}
    write_json(out / 'run.json', record)
    curve_path = out / 'curve_metrics.csv'
    with curve_path.open('w', newline='', encoding='utf-8') as curve_handle:
        writer = csv.DictWriter(curve_handle, fieldnames=['method', 'phase', 'epoch', 'validation_accuracy_pct',
            'test_accuracy_pct', 'validation_nll', 'test_nll', 'train_accuracy_pct',
            'shard_training_seconds', 'aggregation_seconds', 'evaluation_seconds', 'aggregation_arm'])
        writer.writeheader()
        for name, cfg in STUDY['methods'].items():
            data = load_data(cfg)
            assignment = torch.tensor(cfg['assignment'], dtype=torch.long, device=data.x.device)
            base_posts = None
            base_request_posts = {}
            base_models = None
            # Unaffected shards are only trained in the before phase. Evaluate
            # their future request-specific inputs while each epoch is in memory.
            request_contexts = {}
            for label, request in STUDY['requests'].items():
                retained = retained_graph(data, request['selected_nodes'])
                request_nodes = sample(retained, cfg)
                request_edges, _ = subgraph(request_nodes, retained.edge_index,
                                           relabel_nodes=True, num_nodes=data.num_nodes)
                affected_ids = set(assignment[request['selected_nodes']].tolist())
                request_contexts[label] = (retained.x[request_nodes], request_edges, affected_ids)
                base_request_posts[label] = {e: [None] * cfg['parameters']['num_shards']
                                             for e in STUDY['evaluation_epochs']}
            for phase in ['before', 'IF', 'Random']:
                training_data = data if phase == 'before' else retained_graph(data, STUDY['requests'][phase]['selected_nodes'])
                count = cfg['parameters']['num_shards']
                points = STUDY['evaluation_epochs']
                posts = {e: [None] * count for e in points}
                sample_posts = {e: [None] * count for e in points}
                times = {e: [0.0] * count for e in points}
                nodes = sample(training_data, cfg)
                edges, _ = subgraph(nodes, training_data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)
                affected = list(range(count)) if phase == 'before' else sorted(set(assignment[STUDY['requests'][phase]['selected_nodes']].tolist()))
                final_models = []
                eval_seconds = 0.0
                hashes = []
                shard_rows = []
                event(out, event='phase_started', method=name, phase=phase, affected_shards=affected)
                loss_path = out / (name + '_' + phase + '_epoch_loss.csv')
                with loss_path.open('w', newline='', encoding='utf-8') as losses:
                    loss_writer = csv.writer(losses)
                    loss_writer.writerow(['shard', 'epoch', 'train_objective_loss', 'cumulative_training_seconds', 'supervised_nodes'])
                    for i in range(count):
                        if i not in affected:
                            for e in points:
                                posts[e][i] = base_posts[e][i]
                                sample_posts[e][i] = base_request_posts[phase][e][i]
                                assert sample_posts[e][i] is not None
                            final_models.append(base_models[i])
                            continue
                        allowed = (assignment == i) | (assignment < 0)
                        keep = allowed[data.edge_index[0]] & allowed[data.edge_index[1]]
                        inference_edges = data.edge_index[:, keep]
                        shard_training_data = shard_graph(training_data, assignment, i)
                        def observe(epoch, model, secs):
                            nonlocal eval_seconds
                            tick = clock()
                            posts[epoch][i] = F.log_softmax(model(data.x, inference_edges), dim=-1).detach()
                            sample_posts[epoch][i] = F.log_softmax(model(training_data.x[nodes], edges), dim=-1).detach()
                            if phase == 'before':
                                for label, (request_x, request_edges, affected_ids) in request_contexts.items():
                                    if i not in affected_ids:
                                        base_request_posts[label][epoch][i] = F.log_softmax(
                                            model(request_x, request_edges), dim=-1).detach()
                            times[epoch][i] = secs
                            train_z = model(shard_training_data.x, shard_training_data.edge_index)
                            shard_rows.append({'shard': i, 'epoch': epoch,
                                'train': metrics(train_z, training_data, shard_training_data.train_mask),
                                'validation': metrics(posts[epoch][i], data, data.val_mask),
                                'test': metrics(posts[epoch][i], data, data.test_mask)})
                            eval_seconds += clock() - tick
                            event(out, event='shard_point', method=name, phase=phase, shard=i, epoch=epoch,
                                  training_seconds=secs)
                            losses.flush()
                        model, secs = trajectory(cfg, training_data, assignment, i, STUDY['epochs'], points, observe, loss_writer)
                        hashes.append({'shard': i, 'state_hash': state_hash(capture_state(model)), 'seconds': secs})
                        final_models.append(model)
                group = {'method': name, 'phase': phase, 'affected_shards': affected, 'rows': [], 'final_state_hashes': hashes,
                         'evaluation_seconds': eval_seconds, 'sample_nodes': nodes.tolist(),
                         'retained_train_nodes': int(training_data.train_mask.sum()),
                         'deleted_nodes': 0 if phase == 'before' else len(STUDY['requests'][phase]['selected_nodes']),
                         'shard_metrics': shard_rows}
                if phase == 'before':
                    fixed_weights = fit_from_posts(name, cfg, training_data, sample_posts[points[-1]], 'corrected')
                for e in points:
                    for arm in ['original', 'corrected', 'equal', 'fixed_before_final']:
                        tick = clock()
                        if arm == 'equal':
                            weights = torch.ones(count, device=data.x.device) / count
                        elif arm == 'fixed_before_final':
                            weights = fixed_weights
                        else:
                            weights = fit_from_posts(name, cfg, training_data, sample_posts[e], arm)
                        agg_seconds = clock() - tick
                        tick = clock()
                        z = sum(w * p for w, p in zip(weights, posts[e]))
                        val, test = metrics(z, data, data.val_mask), metrics(z, data, data.test_mask)
                        train = metrics(z, data, training_data.train_mask)
                        evaluation_seconds = clock() - tick
                        row = {'method': name, 'phase': phase, 'epoch': e, 'aggregation_arm': arm,
                            'validation_accuracy_pct': val['accuracy_pct'], 'test_accuracy_pct': test['accuracy_pct'],
                            'validation_nll': val['nll'], 'test_nll': test['nll'], 'train_accuracy_pct': train['accuracy_pct'],
                            'shard_training_seconds': sum(times[e]), 'aggregation_seconds': agg_seconds,
                            'evaluation_seconds': evaluation_seconds}
                        writer.writerow(row)
                        curve_handle.flush()
                        group['rows'].append({**row, 'weights': weights.tolist()})
                        event(out, event='ensemble_point', **row)
                        if arm == 'original':
                            original_weights, original_z = weights, z
                # Compare all terminal models, including reused unaffected shards,
                # with a fresh production aggregation on the retained input.
                ensemble = ShardEnsemble(final_models, assignment, torch.ones(count, device=data.x.device) / count).eval()
                adapter = aggregate_weights if name == 'GraphEraser' else graphrevoker_weights
                with seeded_execution(cfg['training']['seed']):
                    actual_weights = adapter(ensemble, training_data, cfg['parameters'])
                torch.testing.assert_close(actual_weights.cpu(), original_weights.cpu(), rtol=1e-4, atol=1e-5)
                ensemble.weights.copy_(actual_weights)
                with torch.no_grad():
                    actual_z = ensemble(data.x, data.edge_index)
                torch.testing.assert_close(actual_z, original_z, rtol=1e-4, atol=1e-5)
                group['terminal_production_adapter_close'] = True
                group['terminal_production_adapter_exact'] = bool(torch.equal(actual_z, original_z))
                if phase == 'before':
                    base_posts, base_models = posts, final_models
                record['groups'].append(group)
                record['wall_seconds_so_far'] = clock() - started
                write_json(out / 'run.json', record)
                event(out, event='phase_completed', method=name, phase=phase, seconds=record['wall_seconds_so_far'])
        record['complete'] = True
        record['finished_at'] = utc()
        record['wall_seconds'] = clock() - started
        write_json(out / 'run.json', record)
        event(out, event='completed', seconds=record['wall_seconds'])

def main():
    global ROOT, STUDY
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', required=True, type=Path)
    parser.add_argument('--output-name', required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    ROOT = args.study.resolve().parent
    STUDY = yaml.safe_load(args.study.read_text(encoding='utf-8'))
    # OpenGU model property files resolve relative to the source checkout.
    os.chdir(Path(__file__).resolve().parents[2])
    torch.set_num_threads(STUDY['threads'])
    if STUDY['device'].startswith('cuda') and not torch.cuda.is_available():
        raise RuntimeError('Requested CUDA device unavailable; no CPU fallback')
    assert Path(args.output_name).name == args.output_name
    out = ROOT / args.output_name
    assert not out.exists(), 'Existing attempt directory must be preserved.'
    out.mkdir()
    try:
        verify(out) if args.verify else run(out)
    except BaseException:
        write_json(out / 'failure.json', {'at': utc(), 'traceback': traceback.format_exc()})
        raise

if __name__ == '__main__':
    main()
