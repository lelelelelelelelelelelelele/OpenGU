"""Read one collected independent method output, without a remote cache or producers."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path, PurePosixPath


def verify_evaluation(saved, current, receipt_id):
    """Verify the producer receipt and independently recompute its measurements."""
    from cache_v2 import canonical_sha256
    identity = saved['identity']
    if set(identity) != set(current['identity']):
        raise ValueError('single-method metrics identity fields differ')
    for key, value in current['identity'].items():
        if key != 'metric_libraries' and identity[key] != value:
            raise ValueError('single-method metrics protocol or output differs')
    libraries = identity['metric_libraries']
    if (not isinstance(libraries, dict) or set(libraries) != {'sklearn', 'torch', 'numpy'}
            or any(not isinstance(value, str) or not value for value in libraries.values())):
        raise ValueError('single-method metrics library provenance is missing')
    expected_id = 'evalr_' + canonical_sha256(identity)[:32]
    if saved['evaluation_receipt_id'] != expected_id or receipt_id != expected_id:
        raise ValueError('single-method metrics receipt digest differs')
    if set(saved['metrics']) != set(current['metrics']):
        raise ValueError('single-method metrics fields differ')
    for name, expected in current['metrics'].items():
        value = saved['metrics'][name]
        if isinstance(expected, (int, float)) and not isinstance(expected, bool):
            if (not isinstance(value, (int, float)) or isinstance(value, bool)
                    or not math.isfinite(value)
                    or not math.isclose(value, expected, rel_tol=1e-7, abs_tol=1e-9)):
                raise ValueError('single-method metric differs from saved predictions: ' + name)
        elif value != expected:
            raise ValueError('single-method metric status differs: ' + name)


def read_method_output(artifacts, project_root):
    from cache_v2 import ArtifactRecipe, ArtifactType
    from cache_v2.contracts import build_artifact_id
    from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
    from experiments.modular_artifacts import ARTIFACT_NAMES
    from experiments.unlearning_outputs import validate_embedded_data, utility
    from experiments.output_metrics import evaluate_method
    from experiments.modular_gu import gu_producer

    root = Path(project_root).resolve()
    content = {}
    for name in ARTIFACT_NAMES:
        item = artifacts.get(name) or {}
        relative = PurePosixPath(str(item.get('local_path') or '').replace('\\', '/'))
        if not relative.parts or relative.is_absolute() or '..' in relative.parts:
            raise ValueError('unsafe or missing collected path: ' + name)
        path = (root / Path(*relative.parts)).resolve()
        if root not in path.parents:
            raise ValueError('collected path escapes project: ' + name)
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.get('sha256'):
            raise ValueError('collected artifact checksum mismatch: ' + name)
        content[name] = raw

    meta = json.loads(content['_meta.json'])
    exported = json.loads(content['output-references.json'])
    attack = json.loads(content['attack.json'])
    payload = UnlearningOutputPayload.from_bytes(content['predictions.npz'])
    validate_embedded_data(payload)
    identity = payload.identity
    recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity})
    reference = {'recipe_hash': recipe.recipe_hash, 'content_hash': payload.content_hash,
        'artifact_id': build_artifact_id(ArtifactType.PREDICTION, recipe.recipe_hash, payload.content_hash)}
    strategy = meta['strategy']
    if set(attack['results']) != {strategy} or exported.get('strategy') != strategy:
        raise ValueError('independent output must contain exactly its own strategy')
    result = attack['results'][strategy]
    if result.get('failed') is not False:
        raise ValueError('method result is missing or failed')
    if any(value != reference for value in
           (meta.get('output_reference'), exported.get('output'), result.get('output'))):
        raise ValueError('method output references differ from collected predictions')
    artifact = meta['selection_artifact']
    if identity['selection'] != {key: artifact[key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}:
        raise ValueError('output Selection dependency differs from provenance')
    if identity['target']['method'] != meta['method']:
        raise ValueError('method identity differs from output')
    if identity['producer_version'] != gu_producer(meta['method'], identity['pairing']['model']).to_dict():
        raise ValueError('method output producer identity changed')
    if meta['method'] == 'Retrain':
        if 'checkpoint_state_hash' in identity['target']:
            raise ValueError('Retrain must be independent of a trained checkpoint')
    if result.get('selected_nodes') != payload.arrays['selected_nodes'].tolist():
        raise ValueError('selected nodes differ from saved output')
    if any(result.get(key) != value for key, value in utility(payload).items()):
        raise ValueError('method utility differs from saved predictions')
    recomputed = evaluate_method(reference, payload)
    evaluation = result['evaluation']
    verify_evaluation(evaluation, recomputed, meta.get('evaluation_receipt_id'))
    return {'payload': payload, 'meta': meta, 'result': result,
            'output': reference, 'evaluation': evaluation}
