"""Real method-level Score/Selection consumers of the unified Cache V2 Store."""
from __future__ import annotations

import time
from pathlib import Path
import torch
from cache_v2 import ProducerVersion
from cache_v2.index import CacheIndex
from experiments.c_target_v1.core import stable_ranking
from experiments.c_target_v1.score_store import ScoreBundlePayload, ScoreBundleStore
from experiments.implementation_identity import implementation_fingerprint
from experiments.selection_budget_planner import materialize_budget_selection
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1.methods import Computations, METHODS, resolve_parameters
from experiments.target_direct_v1.recipe import build_recipe, SCORE_BUDGET_SEMANTICS
from utils.target_checkpoint import data_identity


def project_ranking(ranking, k):
    return ranking[:k]


def synchronize(data):
    if data.x.device.type == 'cuda':
        torch.cuda.synchronize(data.x.device)


def resolve_methods(*, store_root, data, dataset_name, model, checkpoints, selectors,
                    model_config=None, training=None, fail_if_score_called=False,
                    fail_if_selection_called=False):
    store_root = Path(store_root)
    c = Computations(model, data, checkpoints)
    inputs = make_dataset_selection_inputs(data, dataset_name=dataset_name)
    index = CacheIndex(store_root / 'index.sqlite')
    selection_producer = ProducerVersion('target-direct-method-prefix-v1',
        implementation_fingerprint(project_ranking, materialize_budget_selection))
    results = {}
    for instance in selectors:
        name, budget = instance['method'], instance['budget']
        params = resolve_parameters(name, instance.get('parameters'))
        k = budget['k']
        recipe, producer = build_recipe(name=name, computations=c, parameters=params,
                                       model_config=model_config, training=training)
        store = ScoreBundleStore(store_root, producer_version=producer, index=index)

        def compute():
            started = time.perf_counter()
            scores = METHODS[name](c, params).detach().cpu().to(torch.float64)
            candidates = c.candidates.cpu().tolist()
            ranking = stable_ranking(candidates, scores)
            return ScoreBundlePayload.build(candidates, {name: scores.tolist()}, {name: ranking},
                {'method': name, 'compute_seconds': time.perf_counter() - started})

        synchronize(data)
        started = time.perf_counter()
        score = store.get_or_compute(recipe, compute, fail_if_called=fail_if_score_called)
        synchronize(data)
        access_seconds = time.perf_counter() - started
        ranking = score.payload.rankings[name]
        started = time.perf_counter()
        materialized = materialize_budget_selection(
            store_root=store_root, dataset=inputs, strategy=name, selector_seed=0,
            budgets=(k,), producer_version=selection_producer,
            algorithm_version='target-direct-method-prefix-v1',
            parameters={'prefix_stable': True, 'budget': budget,
                        'split_hash': data_identity(data)['split_hash'],
                        'selection_rule': {'direction': 'descending', 'tie_break': 'node_id_ascending'},
                        'score_budget_semantics': SCORE_BUDGET_SEMANTICS},
            source_score_artifact_id=score.artifact_id,
            producer=lambda max_k: project_ranking(ranking, max_k),
            fail_if_producer_called=fail_if_selection_called)
        key = instance.get('instance_id', name)
        if key in results:
            raise ValueError('duplicate selector instance in one invocation')
        selection_seconds = time.perf_counter() - started
        results[key] = {'score': {'artifact_id': score.artifact_id, 'recipe_hash': recipe.recipe_hash,
            'content_hash': score.content_hash, 'hit': score.hit, 'producer_called': score.producer_called,
            'access_seconds': access_seconds,
            'cold_total_seconds': None if score.hit else access_seconds,
            'warm_read_seconds': access_seconds if score.hit else None,
            'effective_parameters': params, 'recipe': recipe.to_dict()},
            'selection': materialized.to_manifest(store_root), 'selection_seconds': selection_seconds,
            'scores': list(score.payload.scores[name]), 'ranking': list(ranking)}
    return results
