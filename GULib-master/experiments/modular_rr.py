"""Adapt the existing fixed-RR maximum-coverage implementation to Selection V2."""
import math
import time

from cache_v2 import ProducerVersion
from experiments.effective_config import effective, ConfigurationError
from experiments.implementation_identity import implementation_fingerprint
from experiments.selection_budget_planner import materialize_budget_selection
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
    # Sampling has no K input; greedy ties use ascending node ID. K only
    # stops the fixed-bundle greedy sequence, including zero marginal gains.
    identity = {**params, 'split_hash': data_identity(data)['split_hash'],
                'prefix_stable': True, 'root_domain': 'all_nodes',
                'diffusion': 'directed_static_ic'}
    producer = ProducerVersion('opengu-fixed-rr-prefix-selection-v2', implementation_fingerprint(
        select_rr, DirectedGraph, sample_rr_bundle, maximum_coverage_greedy))
    started = time.perf_counter()
    materialized = materialize_budget_selection(store_root=store_root, dataset=inputs,
        strategy='im_rr_greedy', selector_seed=params['im_selector_seed'], budgets=[k],
        producer_version=producer, algorithm_version='fixed-rr-maximum-coverage-greedy-v1',
        parameters=identity, source_score_artifact_id=None,
        producer=lambda max_k: select_rr(inputs, max_k, params))
    return {'score': {'hit': None, 'producer_called': False, 'access_seconds': None},
        'selection': {**materialized.to_manifest(store_root), 'effective_parameters': dict(params)},
        'selection_seconds': time.perf_counter() - started}
