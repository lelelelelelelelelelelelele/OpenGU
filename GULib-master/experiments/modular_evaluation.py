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
        'producer_version': 'persisted-output-utility-v2',
    },
    'post_unlearning_utility_and_retrain_gap': {
        'metrics': ('perf_before', 'perf_unlearn', 'perf_retrain', 'drop_retrain',
                    'gap', 'gap_pct'),
        'required_inputs': ('model_before', 'model_unlearned',
                            'exact_retrain_same_selection'),
        'consumers': ('modular_cpu_v1', 'target_direct_syncmate_v2'),
        'producer_version': 'persisted-output-retrain-gap-v2',
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


def evaluate_modular(instance, unlearning_rows, *, store_root, data=None, retrain_input=None):
    from experiments.unlearning_outputs import load_output, utility
    from experiments.implementation_identity import implementation_fingerprint
    require_consumer(instance, 'modular_cpu_v1')
    outputs = []
    for row in unlearning_rows:
        reference = row.get('unlearning', row.get('output', row))
        outputs.append((reference, load_output(reference, store_root, data=data), row.get('retrain')))
    retrains = [(ref, payload) for ref, payload, _ in outputs if payload.identity['target']['method'] == 'Retrain']
    if retrain_input:
        retrains.append((retrain_input, load_output(retrain_input, store_root, data=data)))
    rows = []
    for reference, output, paired_reference in outputs:
        if output.identity['target']['method'] == 'Retrain':
            continue
        values = utility(output)
        available = {**values, 'f1_drop_pct': values['f1_drop_ratio']}
        identity = {'case': instance['case'], 'metrics': sorted(instance['metrics']),
            'producer_version': instance['producer_version'],
            'implementation': implementation_fingerprint(evaluate_modular, utility),
            'unlearning_output': reference}
        if instance['case'] == 'post_unlearning_utility_and_retrain_gap':
            candidates = ([(paired_reference, load_output(paired_reference, store_root, data=data))]
                          if paired_reference else retrains)
            matches = {ref['artifact_id']: (ref, payload) for ref, payload in candidates
                       if payload.identity['target']['method'] == 'Retrain'
                       and payload.identity['pairing'] == output.identity['pairing']}
            if len(matches) != 1:
                raise ConfigurationError('retrain-gap needs exactly one verified Retrain with the same request, training and deletion semantics')
            ref, retrain = next(iter(matches.values()))
            for name in ('y', 'test_mask', 'evaluation_edge_index'):
                import numpy as np
                if not np.array_equal(output.arrays[name], retrain.arrays[name]):
                    raise ConfigurationError('paired output evaluation inputs differ')
            perf = utility(retrain)['f1_after']
            gap = perf - values['f1_after']
            available.update(perf_before=values['f1_before'], perf_unlearn=values['f1_after'],
                perf_retrain=perf, drop_retrain=values['f1_before'] - perf,
                gap=gap, gap_pct=gap / perf * 100 if perf > 0 else 0.0)
            identity['retrain_output'] = ref
        metrics = {name: available[name] for name in instance['metrics']}
        rows.append({'evaluation_receipt_id': 'evalr_' + canonical_sha256(identity)[:32],
                     'identity': identity, 'metrics': metrics})
    if not rows:
        raise ConfigurationError('evaluation requires at least one GU output with baseline predictions')
    return {'effective_config': instance, 'rows': rows}
