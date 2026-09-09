"""Ordinary CELF Selection with explicitly bounded cross-budget reuse."""
from dataclasses import asdict
import math
import time

from cache_v2 import ProducerVersion
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import effective, ConfigurationError
from experiments.selection_producer import (
    ImParameters, SelectionInputs, build_selection_job, build_im_producer,
    resolve_or_produce_selection, load_im_strategy, im_algorithm_version,
    producer_source_fingerprint,
)
from experiments.selection_budget_planner import materialize_budget_selection
from utils.target_checkpoint import data_identity


def resolve_im_parameters(value):
    params = effective(value, asdict(ImParameters()), 'IM parameters')
    for key in ('mc_rounds', 'im_batch_size', 'im_selector_seed'):
        if type(params[key]) is not int or params[key] < (0 if key == 'im_selector_seed' else 1):
            raise ConfigurationError('invalid IM ' + key)
    for key in ('propagation_prob', 'candidate_fraction'):
        if type(params[key]) not in (int, float) or not math.isfinite(params[key]):
            raise ConfigurationError('invalid IM ' + key)
    if type(params['parallel_mc']) is not bool:
        raise ConfigurationError('IM parallel_mc must be boolean')
    return ImParameters(**params).to_dict()


def resolve_im(item, *, store_root, data, inputs):
    params = ImParameters(**item['parameters'])
    strategy, has_numba, source = load_im_strategy()
    if not has_numba and params.im_batch_size != 1:
        raise ConfigurationError('Batch-CELF requires numba; Python CELF requires im_batch_size=1')
    prefix_stable = params.im_batch_size == 1 and params.candidate_fraction == 1.0
    identity = {**params.to_dict(), 'split_hash': data_identity(data)['split_hash'],
                'prefix_stable': prefix_stable}
    k = item['budget']['k']
    producer = ProducerVersion('opengu-im-prefix-selection-v3',
                               producer_source_fingerprint(source, 'im'))
    if prefix_stable:
        # No K-dependent candidate pruning or batch truncation. The heap,
        # MC seed schedule and tie breaking depend only on the common prefix.
        started = time.perf_counter()
        materialized = materialize_budget_selection(store_root=store_root, dataset=inputs,
            strategy='im', selector_seed=params.im_selector_seed, budgets=[k],
            producer_version=producer, algorithm_version=im_algorithm_version(has_numba),
            parameters=identity, source_score_artifact_id=None,
            producer=lambda max_k: build_im_producer(inputs, max_k, params, strategy)())
        return {'score': {'hit': None, 'producer_called': False, 'access_seconds': None},
            'selection': {**materialized.to_manifest(store_root),
                          'effective_parameters': params.to_dict()},
            'selection_seconds': time.perf_counter() - started}
    job = build_selection_job(SelectionInputs(inputs, 'im', params.im_selector_seed, k,
        producer, im_algorithm_version(has_numba), identity),
        build_im_producer(inputs, k, params, strategy))
    started = time.perf_counter()
    materialized = resolve_or_produce_selection(job, store_root)
    loaded = load_selection_artifact(store_root, materialized.artifact_id,
        num_nodes=inputs.num_nodes, candidate_nodes=inputs.candidate_nodes,
        expected_selector='im', expected_k=k, expected_parameters=identity,
        expected_dataset_fingerprint=inputs.dataset_fingerprint,
        expected_graph_fingerprint=inputs.graph_fingerprint)
    if loaded.recipe_hash != job.recipe.recipe_hash or loaded.content_hash != materialized.content_hash:
        raise ConfigurationError('IM Selection identity differs from resolved request')
    return {'score': {'hit': None, 'producer_called': False, 'access_seconds': None},
        'selection': {'strategy': 'im', 'artifact_k': k,
            'artifact': {key: getattr(loaded, key) for key in ('artifact_id', 'recipe_hash', 'content_hash')},
            'cache': {'hit': materialized.hit, 'producer_called': materialized.producer_called,
                      'lookup_policy': 'exact_k',
                      'prefix_reuse_unavailable': 'requires im_batch_size=1 and candidate_fraction=1'},
            'views': {str(k): {'selected_nodes': list(loaded.selected_nodes)}},
            'effective_parameters': params.to_dict(), 'recipe': job.recipe.to_dict()},
        'selection_seconds': time.perf_counter() - started}
