"""Method-scoped Score identities, independent of GU and experiment ownership."""
from __future__ import annotations

from functools import partial

from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion, build_artifact_id
from experiments.implementation_identity import implementation_fingerprint, model_functions
from experiments.c_target_v1.core import ids_hash, parameter_schema_hash, stable_ranking
from experiments.target_direct_v1.methods import (
    SCORE_NAMES, METHODS, uses_model, uses_target, selected_checkpoint_indices, implementation_functions,
)
from utils.target_checkpoint import data_identity, state_hash
from experiments.modular_model import numerical_environment
from experiments.target_direct_v1.class_matching import METHOD as CLASS_MATCHED, MATCHING_VERSION, source_parameters

ALGORITHM_VERSION = 'target-direct-method-score-v1'
SCORE_FAMILY = 'target_direct_method_score'
APPROVED_BUDGET_RATIOS = (0.01, 0.05)
SCORE_BUDGET_SEMANTICS = 'prefix_stable_budget_independent'
GRAPH_SOURCE_SCOPE = 'affected_intersection_train_mask'


def build_recipe(*, name, computations, parameters, model_config=None, training=None, dataset_identity=None,
                 source_score=None):
    c = computations
    functions = implementation_functions(name) + [stable_ranking]
    if uses_model(name):
        functions.extend(model_functions(c.model))
    producer = ProducerVersion(ALGORITHM_VERSION, implementation_fingerprint(*functions))
    method = METHODS[name]
    fields = {
        'artifact_kind': 'score_bundle', 'score_family': SCORE_FAMILY, 'score_names': [name],
        'algorithm_version': ALGORITHM_VERSION, 'producer': producer.to_dict(),
        'data_identity': data_identity(c.data) if dataset_identity is None else dataset_identity,
        'candidate_set': {'ordered_ids_hash': ids_hash(c.candidates),
                          'node_id_space': 'pyg-global-node-index-v1',
                          'ranking_reusable_across_budgets': True},
        'parameters': parameters,
        'method_binding': dict(method.keywords) if isinstance(method, partial) else {},
        'aggregation': {'ranking': 'score_desc_node_id_asc'},
        'budget_semantics': SCORE_BUDGET_SEMANTICS,
    }
    if uses_model(name):
        fields['selector_model'] = dict(model_config or {})
        fields['training'] = dict(training or {})
        fields['parameter_schema_hash'] = parameter_schema_hash(c.model, parameters['parameter_scope'])
        fields['numerics'] = numerical_environment(c.data)
        if name.startswith('tracin_cp_'):
            indices = selected_checkpoint_indices(c.checkpoints, parameters)
            fields['trajectory'] = [
                {'global_step': c.checkpoints[i]['global_step'],
                 'state_hash': state_hash(c.checkpoints[i]['state']),
                 'weight': float(c.checkpoints[i]['update_lr'])} for i in indices]
        else:
            fields['final_state_hash'] = state_hash(c.final_state)
    if uses_target(name):
        fields['target_ids_hash'] = ids_hash(c.targets)
    if name == CLASS_MATCHED:
        expected, _ = build_recipe(name='r_point', computations=c, parameters=source_parameters(parameters),
            model_config=model_config, training=training, dataset_identity=dataset_identity)
        if (source_score is None or source_score.get('recipe_hash') != expected.recipe_hash
                or source_score.get('recipe') != expected.to_dict()
                or source_score.get('artifact_id') != build_artifact_id(
                    ArtifactType.SCORE, expected.recipe_hash, source_score['content_hash'])):
            raise ValueError('class matching requires the exact verified R-point Score for this source')
        fields['source_r_point'] = {key: source_score[key] for key in
                                   ('artifact_id', 'recipe_hash', 'content_hash')}
        fields['matching'] = {'algorithm': MATCHING_VERSION, 'labels': 'candidate_train_labels_only',
            'candidate_labels_hash': ids_hash(c.data.y[c.candidates].detach().cpu().tolist()),
            'rng': 'per_class_sha256_domain_torch_cpu_randperm',
            'score_values': 'ordinal_order_encoding_not_influence_magnitude'}
    return ArtifactRecipe(fields), producer
