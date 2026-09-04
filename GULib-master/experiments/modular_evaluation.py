"""Independent evaluation-case registry for modular experiment plans.

The plan selects an evaluation case.  Each execution lane declares whether it
can supply that case's required inputs; an unavailable case fails before any
Store or runtime write.
"""
from __future__ import annotations

from cache_v2 import canonical_sha256
from experiments.effective_config import ConfigurationError, fields


CASES = {
    'post_unlearning_utility': {
        'metrics': ('f1_before', 'f1_after', 'f1_drop', 'f1_drop_pct'),
        'required_inputs': ('unlearning_result',),
        'consumers': ('modular_cpu_v1', 'target_direct_syncmate_v2'),
        'producer_version': 'post-unlearning-utility-v1',
    },
    'post_unlearning_utility_and_retrain_gap': {
        'metrics': ('perf_before', 'perf_unlearn', 'perf_retrain', 'drop_retrain',
                    'gap', 'gap_pct'),
        'required_inputs': ('model_before', 'model_unlearned',
                            'exact_retrain_same_selection'),
        'consumers': ('target_direct_syncmate_v2',),
        'producer_version': 'retrain-gap-v1',
    },
}


def resolve_evaluation(value):
    fields(value, {'kind', 'schema_version', 'case', 'metrics', 'acceptance'},
           {'kind', 'schema_version', 'case'}, 'evaluation')
    case = value['case']
    if case not in CASES:
        raise ConfigurationError('unknown evaluation case: ' + str(case))
    definition = CASES[case]
    requested = value.get('metrics', list(definition['metrics']))
    if (not isinstance(requested, list) or not requested
            or any(not isinstance(item, str) for item in requested)
            or len(set(requested)) != len(requested)):
        raise ConfigurationError('evaluation.metrics must be a unique nonempty list')
    unknown = set(requested) - set(definition['metrics'])
    if unknown:
        raise ConfigurationError('unsupported metrics for {0}: {1}'.format(case, sorted(unknown)))
    acceptance = value.get('acceptance', {})
    if not isinstance(acceptance, dict):
        raise ConfigurationError('evaluation.acceptance must be a mapping')
    return {
        'kind': 'evaluation', 'schema_version': 1, 'case': case,
        'metrics': requested, 'acceptance': dict(acceptance),
        'required_inputs': list(definition['required_inputs']),
        'available_consumers': list(definition['consumers']),
        'producer_version': definition['producer_version'],
    }


def require_consumer(instance, consumer):
    if consumer not in instance['available_consumers']:
        raise ConfigurationError(
            "evaluation case '{0}' is not implemented by {1}; required inputs: {2}".format(
                instance['case'], consumer, ', '.join(instance['required_inputs'])))


def evaluate_modular(instance, unlearning_rows):
    require_consumer(instance, 'modular_cpu_v1')
    rows = []
    for row in unlearning_rows:
        result = row['result']
        available = {
            'f1_before': result['f1_before'],
            'f1_after': result['f1_after'],
            'f1_drop': result['f1_drop'],
            'f1_drop_pct': result['f1_drop_ratio'],
        }
        metrics = {name: available[name] for name in instance['metrics']}
        identity = {
            'case': instance['case'], 'metrics': instance['metrics'],
            'producer_version': instance['producer_version'],
            'unlearning_artifact_id': row['artifact_id'],
        }
        rows.append({
            'evaluation_receipt_id': 'evalr_' + canonical_sha256(identity)[:32],
            'identity': identity, 'metrics': metrics,
        })
    return {'effective_config': instance, 'rows': rows}
