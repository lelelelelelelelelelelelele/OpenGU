"""Independent evaluation-case registry for modular experiment plans.

The plan selects an evaluation case.  Each execution lane declares whether it
can supply that case's required inputs; an unavailable case fails before any
Store or runtime write.
"""
from __future__ import annotations

from cache_v2 import canonical_sha256
from experiments.effective_config import ConfigurationError, fields
from experiments.node_deletion import retrain_pairing_matches


CASES = {
    'post_unlearning_flip_hop': {
        'metrics': ('fraction_flipped', 'node_count', 'flipped_count') + tuple(
            label + '_hop_' + suffix for label in ('1', '2', '3', 'gt3')
            for suffix in ('count', 'flipped_count', 'flip_rate')),
        'required_inputs': ('method_output', 'exact_retrain_same_selection', 'bound_original_graph'),
        'consumers': ('modular_v1',),
        'producer_version': 'persisted-output-flip-hop-v1',
    },
    'post_method_metrics': {
        'metrics': ('f1', 'accuracy', 'cross_entropy', 'classification_auc',
                    'classification_auc_status', 'update_detection_auc', 'update_detection_auc_status'),
        'required_inputs': ('method_output',),
        'consumers': ('modular_v1',),
        'producer_version': 'single-method-output-metrics-v1',
    },
    'post_unlearning_utility': {
        'metrics': ('f1_before', 'f1_after', 'f1_drop', 'f1_drop_pct'),
        'required_inputs': ('unlearning_result',),
        'consumers': ('modular_v1',),
        'producer_version': 'persisted-output-utility-v2',
    },
    'post_unlearning_utility_and_retrain_gap': {
        'metrics': ('perf_before', 'perf_unlearn', 'perf_retrain', 'drop_retrain',
                    'gap', 'gap_pct'),
        'required_inputs': ('model_before', 'model_unlearned',
                            'exact_retrain_same_selection'),
        'consumers': ('modular_v1',),
        'producer_version': 'persisted-output-retrain-gap-v2',
    },
}


def is_paired_evaluation(instance):
    return 'exact_retrain_same_selection' in instance['required_inputs']


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


def _formula_functions(case):
    from experiments.measurement_formulas import utility_metrics, retrain_gap, flip_metrics
    from experiments.output_metrics import method_metrics, update_detection
    from experiments.unlearning_outputs import utility
    if case == 'post_method_metrics':
        return [method_metrics, update_detection]
    if case == 'post_unlearning_utility':
        return [utility_metrics, utility]
    if case == 'post_unlearning_utility_and_retrain_gap':
        return [retrain_gap, utility, retrain_pairing_matches]
    from experiments.flip_hop_metrics import exact_retrain, flip_hop, hop_groups
    return [flip_metrics, exact_retrain, flip_hop, hop_groups, retrain_pairing_matches]


def _measure(instance, reference, output, pair=None):
    from experiments.measurement_formulas import utility_metrics, retrain_gap, flip_metrics, method_values
    from experiments.implementation_identity import implementation_fingerprint
    identity = dict(case=instance['case'], metrics=sorted(instance['metrics']),
        producer_version=instance['producer_version'],
        implementation=implementation_fingerprint(*_formula_functions(instance['case'])),
        unlearning_output=reference)
    case = instance['case']
    if case == 'post_method_metrics':
        values, protocol = method_values(reference, output)
        identity['method_evaluation'] = protocol
    elif case == 'post_unlearning_utility':
        values, _ = utility_metrics(output)
    elif case == 'post_unlearning_utility_and_retrain_gap':
        values, _ = retrain_gap(output, pair[1])
        identity['retrain_output'] = pair[0]
    else:
        values, protocol = flip_metrics(output, pair[1])
        identity.update(retrain_output=pair[0], protocol=protocol)
    metrics = {key:values[key] for key in instance['metrics']}
    return dict(evaluation_receipt_id='evalr_' + canonical_sha256(identity)[:32], identity=identity, metrics=metrics)


def _pair(instance, identity, candidates):
    matches = [(ref, value) for ref,value in candidates if retrain_pairing_matches(identity, value.identity if hasattr(value,'identity') else value)]
    if instance['case'] == 'post_unlearning_utility_and_retrain_gap':
        matches = list({ref['content_hash']:(ref,value) for ref,value in matches}.values())
    if len(matches) != 1:
        raise ConfigurationError('paired evaluation needs exactly one verified Retrain with the same request, Dataset/Split, training and evaluation graph')
    return matches[0]


def evaluate_modular(instance, unlearning_rows, *, store_root, data=None, verified_outputs=(), dataset_root=None, audit=None):
    from contextlib import nullcontext
    from experiments.evaluation_cache import describe_output, evaluation_request, cached_measurements, phase
    from experiments.unlearning_outputs import load_output
    from experiments.execution_audit import cache_fact
    require_consumer(instance, 'modular_v1')
    # Explicit already-verified in-memory inputs remain a computation consumer.
    # Ordinary YAML uses exact references so its HIT can precede Output loading.
    supplied = [(ref,value,pair,None) for ref,value,pair in verified_outputs]
    references = [(row.get('unlearning', row.get('output', row)), row.get('retrain'), row.get('conditions')) for row in unlearning_rows]
    descriptors = []
    for reference, paired_reference, conditions in references:
        input_conditions = conditions or dict(scope='experiment', experiment_id=audit.experiment_id if audit else 'evaluation',
            dataset='Output '+reference.get('artifact_id',reference.get('path','')), execution_stage='evaluation')
        input_conditions = {**input_conditions, 'evaluation':instance['case'], 'evaluation_part':'input_validation'}
        with (audit.entry('evaluation',input_conditions) if audit else nullcontext({})) as fact, phase(audit,'evaluation_identity'):
            if reference.get('storage') == 'run':
                with phase(audit, 'evaluation_inputs'):
                    supplied.append((reference, load_output(reference, store_root, data=data, dataset_root=dataset_root), paired_reference, conditions))
            else:
                descriptors.append((reference, describe_output(reference, store_root, data=data, dataset_root=dataset_root), paired_reference, conditions))
            fact['metrics'] = {'identity_verified':1}
    retrains = [(ref,identity) for ref,identity,_,_ in descriptors if identity['target']['method'] == 'Retrain']
    retrains.extend((ref,output) for ref,output,_,_ in supplied if output.identity['target']['method']=='Retrain')
    loaded = {}
    def read(ref):
        key = canonical_sha256(ref)
        if key not in loaded:
            with phase(audit, 'evaluation_inputs'):
                loaded[key] = load_output(ref, store_root, data=data, dataset_root=dataset_root)
        return loaded[key]
    rows = []
    for reference, value, paired_reference, own_conditions in [*descriptors, *supplied]:
        in_memory = hasattr(value, 'identity')
        identity = value.identity if in_memory else value
        if identity['target']['method']=='Retrain' and is_paired_evaluation(instance):
            continue
        conditions = {}
        if audit:
            binding = identity['pairing']
            conditions = dict(dataset=identity['dataset_input']['instance']['dataset']['name'],
                dataset_fingerprint=binding['data_identity']['split_hash'], model=binding['model']['architecture'],
                method=identity['target']['method'], seed=binding['training']['seed'],
                ratio=len(binding['selected_nodes']), output_id=reference.get('artifact_id',reference.get('path')),
                evaluation=instance['case'])
        conditions = {**conditions, **(own_conditions or {}), 'evaluation':instance['case']}
        if audit and own_conditions:
            conditions['ratio'] = own_conditions.get('budget_ratio') or own_conditions.get('budget', {}).get('value', conditions['ratio'])
        with (audit.entry('evaluation', conditions) if audit else nullcontext({})) as fact:
            pair = None
            if is_paired_evaluation(instance):
                candidates = retrains
                if paired_reference:
                    candidates = [(paired_reference, read(paired_reference) if paired_reference.get('storage') == 'run'
                        else describe_output(paired_reference, store_root, data=data, dataset_root=dataset_root))]
                pair = _pair(instance, identity, candidates)
            def produce():
                output = value if in_memory else read(reference)
                baseline = None if pair is None else (pair[0], pair[1] if hasattr(pair[1],'identity') else read(pair[0]))
                with phase(audit, 'metric_formula'):
                    return _measure(instance, reference, output, baseline)
            if in_memory or (pair and pair[0].get('storage') == 'run'):
                measured, cache = produce(), None
            else:
                dependencies = [dict(reference=reference,identity=identity)]
                if pair:
                    dependencies.append(dict(reference=pair[0],identity=pair[1].identity if hasattr(pair[1],'identity') else pair[1]))
                request = evaluation_request(instance['case'], instance['metrics'], dependencies,
                    _formula_functions(instance['case']), instance['producer_version'])
                measured, cache = cached_measurements(request, store_root, produce, audit=audit)
            rows.append({**measured, 'cache':cache})
            fact['metrics'] = measured['metrics']
            if cache:
                fact['cache'] = [cache_fact('result', cache, cache['hit'])]
    if not rows:
        raise ConfigurationError('evaluation has no applicable method outputs')
    return {'effective_config':instance, 'rows':rows}
