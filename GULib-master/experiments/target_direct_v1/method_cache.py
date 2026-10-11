"""Real method-level Score/Selection consumers of the unified Cache V2 Store."""
from __future__ import annotations

import time
from pathlib import Path
import torch
from cache_v2 import ArtifactResolver, ArtifactType, ProducerVersion
from cache_v2.errors import CacheResolutionError
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


def resolve_methods(*, store_root, data, dataset_name, model, checkpoints, selectors, include_scores,
                    model_config=None, training=None, fail_if_score_called=False,
                    fail_if_selection_called=False, dataset_inputs=None, dataset_identity=None):
    store_root = Path(store_root)
    c = Computations(model, data, checkpoints)
    inputs = dataset_inputs if dataset_inputs is not None else make_dataset_selection_inputs(data, dataset_name=dataset_name)
    identity = data_identity(data) if dataset_identity is None else dataset_identity
    index = CacheIndex(store_root / 'index.sqlite')
    # Score identity owns ranking computation; Selection only takes its prefix.
    # Cache lookup/storage helpers must not change this computation identity.
    selection_producer = ProducerVersion('target-direct-method-prefix-v1',
        implementation_fingerprint(project_ranking))
    results = {}
    for instance in selectors:
        name, budget = instance['method'], instance['budget']
        params = resolve_parameters(name, instance.get('parameters'))
        k = budget['k']
        recipe, producer = build_recipe(name=name, computations=c, parameters=params,
                                       model_config=model_config, training=training, dataset_identity=identity)
        store = ScoreBundleStore(store_root, producer_version=producer, index=index)

        def compute():
            started = time.perf_counter()
            scores = METHODS[name](c, params).detach().cpu().to(torch.float64)
            candidates = c.candidates.cpu().tolist()
            ranking = stable_ranking(candidates, scores)
            return ScoreBundlePayload.build(candidates, {name: scores.tolist()}, {name: ranking},
                {'method': name, 'compute_seconds': time.perf_counter() - started})

        score = None
        access_seconds = 0.0

        def load_score():
            nonlocal score, access_seconds
            if score is None:
                synchronize(data)
                started = time.perf_counter()
                score = store.get_or_compute(recipe, compute, fail_if_called=fail_if_score_called)
                if record is not None and (score.artifact_id != record['artifact_id'] or score.content_hash != record['content_hash']):
                    raise CacheResolutionError('Score resolution changed during read')
                synchronize(data)
                access_seconds += time.perf_counter() - started
            return score

        started = time.perf_counter()
        record = None
        if index.database_path.is_file():
            with index.read_session():
                explanation = ArtifactResolver(index).explain_compatible(ArtifactType.SCORE, recipe)
                if explanation.hit:
                    record = explanation.exact_candidate
                elif explanation.exact_candidate is not None or explanation.miss_reasons != ('no_exact_candidate',):
                    raise CacheResolutionError('Score lookup failed closed: ' + ','.join(explanation.miss_reasons))
        access_seconds += time.perf_counter() - started
        if record is None:
            record = index.get_artifact(load_score().artifact_id)
        score_access_before_selection = access_seconds
        started = time.perf_counter()
        materialized = materialize_budget_selection(
            store_root=store_root, dataset=inputs, strategy=name, selector_seed=0,
            budgets=(k,), producer_version=selection_producer,
            algorithm_version='target-direct-method-prefix-v1',
            parameters={'prefix_stable': True, 'budget': budget,
                        'split_hash': identity['split_hash'],
                        'selection_rule': {'direction': 'descending', 'tie_break': 'node_id_ascending'},
                        'score_budget_semantics': SCORE_BUDGET_SEMANTICS},
            source_score_artifact_id=record['artifact_id'],
            producer=lambda max_k: project_ranking(load_score().payload.rankings[name], max_k),
            fail_if_producer_called=fail_if_selection_called)
        key = instance.get('instance_id', name)
        if key in results:
            raise ValueError('duplicate selector instance in one invocation')
        selection_seconds = time.perf_counter() - started - (access_seconds - score_access_before_selection)
        if include_scores:
            load_score()
        from cache_v2.source_compatibility import stored_recipe
        generation_recipe = stored_recipe(record)
        score_hit = score is None or score.hit
        results[key] = {'score': {'artifact_id': record['artifact_id'], 'recipe_hash': generation_recipe.recipe_hash,
            'content_hash': record['content_hash'], 'hit': score_hit, 'producer_called': bool(score and score.producer_called),
            'access_seconds': access_seconds,
            'cold_total_seconds': None if score_hit else access_seconds,
            'warm_read_seconds': access_seconds if score_hit else None,
            'effective_parameters': params, 'recipe': generation_recipe.to_dict(),
            'generation_producer': generation_recipe.fields['producer'], 'consumption_producer': producer.to_dict()},
            'selection': materialized.to_manifest(store_root), 'selection_seconds': selection_seconds}
        if include_scores:
            results[key].update(scores=list(score.payload.scores[name]), ranking=list(score.payload.rankings[name]))
    return results
