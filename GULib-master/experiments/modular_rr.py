"""Adapt the existing fixed-RR maximum-coverage implementation to Selection V2."""
import math
import time

from cache_v2 import ProducerVersion
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import effective, ConfigurationError
from experiments.implementation_identity import implementation_fingerprint
from experiments.selection_producer import (
    SelectionInputs, build_selection_job, resolve_or_produce_selection,
)
from utils.target_checkpoint import data_identity


def resolve_rr_parameters(value):
    params = effective(value, {'propagation_prob': 0.1, 'rr_count': 4096,
                              'im_selector_seed': 2024}, 'RR IM parameters')
    for key in ('rr_count', 'im_selector_seed'):
        if type(params[key]) is not int or params[key] < (0 if key == 'im_selector_seed' else 1):
            raise ConfigurationError('invalid RR IM ' + key)
    p = params['propagation_prob']
    if type(p) not in (int, float) or not math.isfinite(p) or not 0 <= p <= 1:
        raise ConfigurationError('RR propagation_prob must be in [0, 1]')
    params['propagation_prob'] = float(p)
    return params


def select_rr(inputs, k, params):
    from experiments.im_score_benchmark.rr_core import DirectedGraph, sample_rr_bundle
    from experiments.im_score_benchmark.selectors import maximum_coverage_greedy
    graph = DirectedGraph.from_edge_index(inputs.edge_index, inputs.num_nodes)
    bundle = sample_rr_bundle(graph, candidate_nodes=inputs.candidate_nodes,
        rr_count=params['rr_count'], propagation_probability=params['propagation_prob'],
        rr_seed=params['im_selector_seed'])
    return maximum_coverage_greedy(bundle, k).selected_nodes.tolist()


def resolve_rr(item, *, store_root, data, inputs):
    from experiments.im_score_benchmark.rr_core import DirectedGraph, sample_rr_bundle
    from experiments.im_score_benchmark.selectors import maximum_coverage_greedy
    params = item['parameters']
    k = item['budget']['k']
    identity = {**params, 'split_hash': data_identity(data)['split_hash'],
                'prefix_stable': False, 'root_domain': 'all_nodes',
                'diffusion': 'directed_static_ic'}
    producer = ProducerVersion('opengu-fixed-rr-selection-v1', implementation_fingerprint(
        select_rr, DirectedGraph, sample_rr_bundle, maximum_coverage_greedy))
    job = build_selection_job(SelectionInputs(inputs, 'im_rr_greedy', params['im_selector_seed'],
        k, producer, 'fixed-rr-maximum-coverage-greedy-v1', identity),
        lambda: select_rr(inputs, k, params))
    started = time.perf_counter()
    materialized = resolve_or_produce_selection(job, store_root)
    loaded = load_selection_artifact(store_root, materialized.artifact_id,
        num_nodes=inputs.num_nodes, candidate_nodes=inputs.candidate_nodes,
        expected_selector='im_rr_greedy', expected_k=k, expected_parameters=identity,
        expected_dataset_fingerprint=inputs.dataset_fingerprint,
        expected_graph_fingerprint=inputs.graph_fingerprint)
    if loaded.recipe_hash != job.recipe.recipe_hash or loaded.content_hash != materialized.content_hash:
        raise ConfigurationError('RR IM Selection identity differs from resolved request')
    return {'score': {'hit': None, 'producer_called': False, 'access_seconds': None},
        'selection': {'strategy': 'im_rr_greedy', 'artifact_k': k,
            'artifact': {key: getattr(loaded, key) for key in ('artifact_id', 'recipe_hash', 'content_hash')},
            'cache': {'hit': materialized.hit, 'producer_called': materialized.producer_called,
                      'lookup_policy': 'exact_k'},
            'views': {str(k): {'selected_nodes': list(loaded.selected_nodes)}},
            'effective_parameters': dict(params), 'recipe': job.recipe.to_dict()},
        'selection_seconds': time.perf_counter() - started}
