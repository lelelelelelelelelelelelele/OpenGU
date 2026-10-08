"""Query complete Cache V2 measurements before preparing prediction arrays."""
from contextlib import nullcontext
from pathlib import Path
from time import perf_counter

from cache_v2 import ArtifactRecipe, ArtifactType, CacheIndex, ArtifactResolver, ProducerVersion
from cache_v2.output_evaluation import OutputEvaluationPayload, OUTPUT_EVALUATION_CONTRACT
from cache_v2.runtime import _decode_exact_mapping
from experiments.artifact_producer import FormalArtifactRequest, resolve_formal_artifact, store_formal_artifact
from experiments.effective_config import ConfigurationError
from experiments.implementation_identity import implementation_fingerprint


def phase(audit, name):
    return audit.phase(name) if audit else nullcontext()


def describe_output(reference, store_root, *, dataset_input=None):
    """Resolve registered identity without opening unused input payloads."""
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.unlearning_outputs import _allowed_output_source
    from experiments.modular_gu import gu_producer
    if set(reference) != {'artifact_id', 'recipe_hash', 'content_hash'}:
        raise ConfigurationError('an exact Cache V2 Output reference is required')
    index = CacheIndex(Path(store_root) / 'index.sqlite')
    record = index.get_artifact(reference['artifact_id'])
    wrapper = _decode_exact_mapping(record['recipe'], 'Output Recipe')
    recipe = ArtifactRecipe(wrapper['fields'], recipe_version=wrapper['recipe_version'])
    fields = recipe.fields
    if (record['artifact_type'] != ArtifactType.PREDICTION.value or fields.get('artifact_contract') != OUTPUT_CONTRACT
            or any(record[k] != v for k, v in reference.items()) or recipe.recipe_hash != reference['recipe_hash']):
        raise ConfigurationError('Output reference identity mismatch')
    current = gu_producer(fields['target']['method'], fields['pairing']['model'])
    if not _allowed_output_source(recipe, current):
        raise ConfigurationError('method output producer changed; explicit new execution required')
    explanation = ArtifactResolver(index).explain_compatible(ArtifactType.PREDICTION, recipe)
    if not explanation.hit:
        raise ConfigurationError('Output dependency is not valid and verified: ' + ','.join(explanation.miss_reasons))
    if dataset_input is not None and dataset_input != fields['dataset_input']:
        raise ConfigurationError('Output bound Dataset/Split reference mismatch')
    return {key:value for key,value in fields.items() if key != 'artifact_contract'}


def metric_environment(case):
    import numpy as np
    result = {'numpy': np.__version__}
    if case in ('method_and_utility', 'post_method_metrics'):
        import sklearn, torch
        result.update(sklearn=sklearn.__version__, torch=torch.__version__)
    return result


def evaluation_request(case, metrics, outputs, functions, version):
    implementation = implementation_fingerprint(*functions)
    identity = dict(case=case, metrics=sorted(metrics), outputs=outputs,
        protocol_version=version, implementation=implementation, metric_libraries=metric_environment(case))
    producer = ProducerVersion(OUTPUT_EVALUATION_CONTRACT, implementation)
    request = FormalArtifactRequest(ArtifactType.EVALUATION, ArtifactRecipe(dict(
        artifact_contract=OUTPUT_EVALUATION_CONTRACT, evaluation_identity=identity,
        producer_version=producer.to_dict())), producer)
    return request


def cached_measurements(request, store_root, produce, *, audit=None):
    started = perf_counter()
    with phase(audit, 'evaluation_query_validation'):
        stored = resolve_formal_artifact(Path(store_root), request)
    hit = stored is not None
    if not hit:
        producer_started = perf_counter()
        values = produce()
        producer_seconds = perf_counter() - producer_started
        with phase(audit, 'evaluation_write_validation'):
            stored = store_formal_artifact(store_root, request,
                OutputEvaluationPayload(request.recipe.fields['evaluation_identity'], values),
                compute_seconds=producer_seconds)
    return stored.payload.values, dict(hit=hit, producer_called=not hit,
        artifact_id=stored.artifact_id, recipe_hash=stored.recipe_hash,
        content_hash=stored.content_hash, access_seconds=perf_counter()-started)


def single_request(reference, identity):
    from experiments.output_metrics import method_metrics, update_detection
    from experiments.unlearning_outputs import utility
    return evaluation_request('method_and_utility', ['method', 'utility'],
        [dict(reference=reference, identity=identity)], [method_metrics, update_detection, utility],
        'single-label-test-micro-f1-ovr-macro-auc-and-utility-v1')


def single_values(reference, output):
    from experiments.output_metrics import evaluate_method
    from experiments.unlearning_outputs import utility
    return dict(result=utility(output), evaluation=evaluate_method(reference, output))


def evaluate_single(reference, identity, *, store_root, data, dataset_root, audit=None):
    from experiments.unlearning_outputs import load_output
    started = perf_counter()
    request = single_request(reference, identity)
    def produce():
        with phase(audit, 'evaluation_inputs'):
            output = load_output(reference, store_root, data=data, dataset_root=dataset_root)
        with phase(audit, 'metric_formula'):
            return single_values(reference, output)
    values, cache = cached_measurements(request, store_root, produce, audit=audit)
    cache['access_seconds'] = perf_counter() - started
    return values, cache


def persist_single(row, *, store_root, dataset_input, audit=None):
    """Cold GU already measured these values; register them without recomputation."""
    if row['output'].get('storage') == 'run':
        return None  # Explicit gu_cache=disabled produces a run-owned, uncached Output.
    identity = describe_output(row['output'], store_root, dataset_input=dataset_input)
    _, cache = cached_measurements(single_request(row['output'], identity), store_root,
        lambda: dict(result=row['result'], evaluation=row['evaluation']), audit=audit)
    return cache
