"""Method-scoped Score identities, independent of GU and experiment ownership."""
from __future__ import annotations

from functools import partial

from cache_v2 import ArtifactRecipe, ProducerVersion
from experiments.implementation_identity import implementation_fingerprint, model_functions
from experiments.c_target_v1.core import ids_hash, parameter_schema_hash, stable_ranking
from experiments.target_direct_v1.methods import (
    SCORE_NAMES, METHODS, uses_model, uses_target, selected_checkpoint_indices, implementation_functions,
)
from utils.target_checkpoint import data_identity, state_hash
from experiments.modular_model import numerical_environment

ALGORITHM_VERSION = 'target-direct-method-score-v1'
SCORE_FAMILY = 'target_direct_method_score'
APPROVED_BUDGET_RATIOS = (0.01, 0.05)
SCORE_BUDGET_SEMANTICS = 'prefix_stable_budget_independent'
GRAPH_SOURCE_SCOPE = 'affected_intersection_train_mask'


def build_recipe(*, name, computations, parameters, model_config=None, training=None):
    c = computations
    functions = implementation_functions(name) + [stable_ranking]
    if uses_model(name):
        functions.extend(model_functions(c.model))
    producer = ProducerVersion(ALGORITHM_VERSION, implementation_fingerprint(*functions))
    method = METHODS[name]
    fields = {
        'artifact_kind': 'score_bundle', 'score_family': SCORE_FAMILY, 'score_names': [name],
        'algorithm_version': ALGORITHM_VERSION, 'producer': producer.to_dict(),
        'data_identity': data_identity(c.data),
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
            fields['final_state_hash'] = state_hash(c.checkpoints[-1]['state'])
    if uses_target(name):
        fields['target_ids_hash'] = ids_hash(c.targets)
    return ArtifactRecipe(fields), producer
