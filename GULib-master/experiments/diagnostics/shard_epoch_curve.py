"""Successor of the EXP-082 CPU diagnostic, with safe unaffected-shard reuse.

The executed Cora script remains immutable in AAGU-104/evidence/run_curve.py.
This runner is still CPU-only; GPU protocol preparation is separate.
Provide study.yaml and isolated inputs beside a copied runner before use.
"""
from __future__ import annotations
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
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
from types import SimpleNamespace
import yaml

ROOT = Path(__file__).resolve().parent
STUDY = yaml.safe_load((ROOT / 'study.yaml').read_text(encoding='utf-8'))
SOURCE = Path(STUDY['source'])
sys.path.insert(0, str(SOURCE))
os.chdir(SOURCE)
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
torch.set_num_threads(STUDY['threads'])

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
        model = create_model(cfg['model'], 'shard', data, torch.device('cpu'))
        opt = torch.optim.Adam(model.parameters(), lr=cfg['training']['lr'],
                               weight_decay=cfg['training']['weight_decay'])
        scheduler = torch.optim.lr_scheduler.MultiStepLR(opt, milestones=[], gamma=1.0)
        for epoch in range(1, epochs + 1):
            started = time.perf_counter()
            model.train()
            opt.zero_grad(set_to_none=True)
            logits = model(d.x, d.edge_index)
            loss = F.cross_entropy(logits[d.train_mask], d.y[d.train_mask], reduction='mean')
            loss.backward()
            opt.step()
            scheduler.step()
            loss_value = float(loss.item())
            elapsed += time.perf_counter() - started
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
        return nodes[torch.as_tensor(np.random.choice(len(nodes), count, replace=False))].sort().values

def fit_from_posts(name, cfg, data, posts):
    cls = Eraser if name == 'GraphEraser' else Revoker
    with seeded_execution(cfg['training']['seed']):
        nodes = sample(data, cfg)
        opt = cls(0, SimpleNamespace(model=None), data, cfg['parameters'], logging.getLogger('EXP-082'))
        opt.device = torch.device('cpu')
        opt.true_labels = data.y[nodes]
        opt.posteriors = {i: p for i, p in enumerate(posts)}
        return opt.optimization().detach()

def verify(out):
    checks = []
    # Compare the instrumented optimization against the actual shared producer,
    # including dropout, initialization, loss, scheduler and sampled evaluation.
    for name, cfg in STUDY['methods'].items():
        data = resolve_input(cfg['dataset_input'], ROOT / 'inputs').cpu()
        assert data_identity(data) == cfg['data_identity']
        assignment = torch.tensor(cfg['assignment'], dtype=torch.long)
        small = copy.deepcopy(cfg)
        small['training']['epochs'] = 30
        observed = []
        m, _ = trajectory(small, data, assignment, 0, 30, [10, 20, 30],
                         lambda epoch, model, sec: observed.append(float(model(data.x, data.edge_index).sum())))
        reference = train_shard(small, data, assignment, 0)
        a, b = capture_state(m), capture_state(reference)
        assert all(torch.equal(a[k], b[k]) for k in a)
        models = [m] * cfg['parameters']['num_shards']
        ensemble = ShardEnsemble(models, assignment, torch.ones(len(models)) / len(models)).eval()
        nodes = sample(data, cfg)
        edges, _ = subgraph(nodes, data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)
        with torch.no_grad():
            posts = [F.log_softmax(model(data.x[nodes], edges), dim=-1) for model in models]
        weights = fit_from_posts(name, cfg, data, posts)
        adapter = aggregate_weights if name == 'GraphEraser' else graphrevoker_weights
        with seeded_execution(cfg['training']['seed']):
            expected = adapter(ensemble, data, cfg['parameters'])
        assert torch.equal(weights, expected)
        for label, r in STUDY['requests'].items():
            nodes_deleted = r['selected_nodes']
            assert len(nodes_deleted) == len(set(nodes_deleted)) and data.train_mask[nodes_deleted].all()
            retained = retained_graph(data, nodes_deleted)
            assert int(retained.train_mask.sum()) == int(data.train_mask.sum()) - len(nodes_deleted)
            for i in range(cfg['parameters']['num_shards']):
                assert shard_graph(retained, assignment, i).train_mask.any()
        checks.append({'method': name, 'instrumented_training_state_exact': True,
                       'state_hash': state_hash(a), 'production_aggregator_weights_exact': True,
                       'evaluation_did_not_change_training_rng': True,
                       'data_identity': data_identity(data)})
    write_json(out / 'validation.json', {'complete': True, 'at': utc(), 'checks': checks,
               'source_sha': STUDY['source_sha'],
               'scope': '30-step numerical equivalence; not a scientific result'})

def run(out):
    assert not (out / 'run.json').exists(), 'Do not overwrite or silently restart an attempt.'
    assert json.loads((ROOT / 'verification/validation.json').read_text(encoding='utf-8'))['complete']
    started = time.perf_counter()
    record = {'experiment_id': 'EXP-082', 'run_id': out.name, 'kind': 'isolated exploratory CPU diagnostic',
        'source_sha': STUDY['source_sha'],
        'started_at': utc(), 'device': 'cpu', 'threads': torch.get_num_threads(), 'torch': torch.__version__,
        'seed': STUDY['seed'], 'epochs': STUDY['epochs'], 'evaluation_epochs': STUDY['evaluation_epochs'],
        'complete': False, 'groups': [], 'saved_checkpoints': 0,
        'test_used_for_selection': False, 'partition_retrained': False}
    write_json(out / 'run.json', record)
    curve_path = out / 'curve_metrics.csv'
    with curve_path.open('w', newline='', encoding='utf-8') as curve_handle:
        writer = csv.DictWriter(curve_handle, fieldnames=['method', 'phase', 'epoch', 'validation_accuracy_pct',
            'test_accuracy_pct', 'validation_nll', 'test_nll', 'train_accuracy_pct',
            'shard_training_seconds', 'aggregation_seconds', 'evaluation_seconds'])
        writer.writeheader()
        for name, cfg in STUDY['methods'].items():
            data = resolve_input(cfg['dataset_input'], ROOT / 'inputs').cpu()
            assert data_identity(data) == cfg['data_identity']
            assignment = torch.tensor(cfg['assignment'], dtype=torch.long)
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
                        def observe(epoch, model, secs):
                            nonlocal eval_seconds
                            tick = time.perf_counter()
                            posts[epoch][i] = F.log_softmax(model(data.x, inference_edges), dim=-1).detach()
                            sample_posts[epoch][i] = F.log_softmax(model(training_data.x[nodes], edges), dim=-1).detach()
                            if phase == 'before':
                                for label, (request_x, request_edges, affected_ids) in request_contexts.items():
                                    if i not in affected_ids:
                                        base_request_posts[label][epoch][i] = F.log_softmax(
                                            model(request_x, request_edges), dim=-1).detach()
                            times[epoch][i] = secs
                            eval_seconds += time.perf_counter() - tick
                            event(out, event='shard_point', method=name, phase=phase, shard=i, epoch=epoch,
                                  training_seconds=secs)
                            losses.flush()
                        model, secs = trajectory(cfg, training_data, assignment, i, STUDY['epochs'], points, observe, loss_writer)
                        hashes.append({'shard': i, 'state_hash': state_hash(capture_state(model)), 'seconds': secs})
                        final_models.append(model)
                group = {'method': name, 'phase': phase, 'affected_shards': affected, 'rows': [], 'final_state_hashes': hashes,
                         'evaluation_seconds': eval_seconds}
                for e in points:
                    tick = time.perf_counter()
                    weights = fit_from_posts(name, cfg, training_data, sample_posts[e])
                    agg_seconds = time.perf_counter() - tick
                    tick = time.perf_counter()
                    z = sum(w * p for w, p in zip(weights, posts[e]))
                    val, test = metrics(z, data, data.val_mask), metrics(z, data, data.test_mask)
                    train = metrics(z, data, training_data.train_mask)
                    evaluation_seconds = time.perf_counter() - tick
                    row = {'method': name, 'phase': phase, 'epoch': e,
                        'validation_accuracy_pct': val['accuracy_pct'], 'test_accuracy_pct': test['accuracy_pct'],
                        'validation_nll': val['nll'], 'test_nll': test['nll'], 'train_accuracy_pct': train['accuracy_pct'],
                        'shard_training_seconds': sum(times[e]), 'aggregation_seconds': agg_seconds,
                        'evaluation_seconds': evaluation_seconds}
                    writer.writerow(row)
                    curve_handle.flush()
                    group['rows'].append({**row, 'weights': weights.tolist()})
                    event(out, event='ensemble_point', **row)
                # Compare all terminal models, including reused unaffected shards,
                # with a fresh production aggregation on the retained input.
                ensemble = ShardEnsemble(final_models, assignment, torch.ones(count) / count).eval()
                adapter = aggregate_weights if name == 'GraphEraser' else graphrevoker_weights
                with seeded_execution(cfg['training']['seed']):
                    actual_weights = adapter(ensemble, training_data, cfg['parameters'])
                torch.testing.assert_close(actual_weights, weights, rtol=0, atol=0)
                ensemble.weights.copy_(actual_weights)
                with torch.no_grad():
                    actual_z = ensemble(data.x, data.edge_index)
                torch.testing.assert_close(actual_z, z, rtol=0, atol=0)
                group['terminal_production_adapter_exact'] = True
                if phase == 'before':
                    base_posts, base_models = posts, final_models
                record['groups'].append(group)
                record['wall_seconds_so_far'] = time.perf_counter() - started
                write_json(out / 'run.json', record)
                event(out, event='phase_completed', method=name, phase=phase, seconds=record['wall_seconds_so_far'])
        record['complete'] = True
        record['finished_at'] = utc()
        record['wall_seconds'] = time.perf_counter() - started
        write_json(out / 'run.json', record)
        event(out, event='completed', seconds=record['wall_seconds'])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    out = ROOT / ('verification' if args.verify else 'cpu1')
    assert not out.exists(), 'Existing attempt directory must be preserved.'
    out.mkdir()
    try:
        verify(out) if args.verify else run(out)
    except BaseException:
        write_json(out / 'failure.json', {'at': utc(), 'traceback': traceback.format_exc()})
        raise

if __name__ == '__main__':
    main()
