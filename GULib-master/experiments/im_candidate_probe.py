"""Disposable CPU candidate comparison; no formal datasets, SSH or research gate.

Run with python -m experiments.im_candidate_probe --output <new-json-path>.
Three fixed graphs, K=5 of 40 candidates, three independent selector seeds.
Independent evaluation uses a fixed 16384 RR samples, never selection samples.
"""
import argparse
from contextlib import redirect_stdout
import itertools
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace

import numpy as np
import torch

from experiments.modular_rr import select_rr
from experiments.selection_producer import load_im_strategy
from experiments.im_score_benchmark.rr_core import DirectedGraph
from experiments.im_score_benchmark.evaluate_spread import evaluate_selections


def probe():
    strategy_class, has_numba, _ = load_im_strategy()
    started = time.perf_counter()
    with redirect_stdout(sys.stderr):
        strategy_class({'propagation_prob': .1, 'mc_rounds': 100, 'im_batch_size': 1,
            'parallel_mc': False, 'im_selector_seed': 0, 'enable_score_cache': False}).compute_im_celf(
                torch.tensor([[0, 1], [1, 0]]), 2, 1, [0, 1])
    warmup = time.perf_counter() - started
    graphs = []
    for topology in ('ring', 'communities', 'hubs'):
        rng = np.random.default_rng(730)
        pairs = {(i, (i+1) % 80) for i in range(80)}
        if topology == 'communities':
            pairs.update((i, j) for i in range(80) for j in range(i+1, 80)
                         if i//20 == j//20 and rng.random() < .2)
        if topology == 'hubs':
            pairs.update((hub, node) for hub in (0, 20, 40, 60) for node in range(hub, hub+20)
                         if hub != node)
        edges = sorted(pairs | {(v, u) for u, v in pairs})
        edge_index = torch.tensor(edges).t().contiguous()
        candidates = list(range(0, 80, 2))
        inputs = SimpleNamespace(edge_index=edge_index, num_nodes=80, candidate_nodes=candidates)
        selections, durations, rows = {}, {}, []
        degrees = np.bincount(edge_index[0].numpy(), minlength=80)
        selections['degree'] = sorted(candidates, key=lambda n: (-degrees[n], n))[:5]
        for seed in (11, 22, 33):
            selections[f'random/{seed}'] = np.random.default_rng(seed).choice(candidates, 5, replace=False).tolist()
            for method in ('im_celf', 'im_rr_greedy'):
                start = time.perf_counter()
                with redirect_stdout(sys.stderr):
                    if method == 'im_celf':
                        strategy = strategy_class({'propagation_prob': .1, 'mc_rounds': 100,
                            'im_batch_size': 1, 'parallel_mc': False, 'im_selector_seed': seed,
                            'candidate_fraction': 1., 'enable_score_cache': False})
                        nodes, _ = strategy.compute_im_celf(edge_index, 80, 5, candidates)
                        nodes = [int(n) for n in nodes]
                    else:
                        nodes = select_rr(inputs, 5, {'propagation_prob': .1,
                            'rr_count': 4096, 'im_selector_seed': seed})
                key = f'{method}/{seed}'
                durations[key] = time.perf_counter() - start
                selections[key] = nodes
        evaluation = evaluate_selections(DirectedGraph.from_edge_index(edge_index, 80),
            selections=selections, degree_key='degree', propagation_probability=.1,
            evaluator_seed=88001, min_rr_sets=16384, max_rr_sets=16384, batch_rr_sets=16384)
        for method in ('im_celf', 'im_rr_greedy', 'random'):
            keys = [f'{method}/{seed}' for seed in (11, 22, 33)]
            overlaps = [len(set(selections[a]) & set(selections[b])) / len(set(selections[a]) | set(selections[b]))
                        for a, b in itertools.combinations(keys, 2)]
            rows.append({'method': method,
                'mean_spread': float(np.mean([evaluation['methods'][k]['spread_estimate'] for k in keys])),
                'mean_pairwise_jaccard': float(np.mean(overlaps)),
                'mean_selection_seconds': float(np.mean([durations[k] for k in keys])) if method != 'random' else None})
        graphs.append({'topology': topology, 'num_nodes': 80, 'edges': edges, 'candidates': candidates,
            'k': 5, 'selections': selections, 'durations': durations, 'summary': rows,
            'evaluation': evaluation})
    return {'level': 'synthetic CPU exploratory comparison, not GU attack evidence',
        'numba_available': has_numba, 'mc_parallel': False, 'warmup_seconds': warmup,
        'mc_rounds': 100, 'rr_count': 4096, 'propagation_prob': .1,
        'selector_seeds': [11, 22, 33], 'graphs': graphs}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(probe(), stream, indent=2)
