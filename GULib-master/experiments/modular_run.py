"""Execute independent instances through existing selector and GU consumers."""
from __future__ import annotations

import json
import pickle
from pathlib import Path
import torch
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import fields, ConfigurationError
from experiments.modular_config import load_experiment, resolve_budget
from experiments.modular_evaluation import evaluate_modular, require_consumer
from experiments.modular_execution import ExecutionContext
from experiments.modular_model import prepare_model
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1.method_cache import resolve_methods
from utils.target_checkpoint import sha256_file, data_identity


def read_dataset(instance, directory):
    fields(instance['dataset'], {'name', 'family'}, {'name'}, 'dataset')
    fields(instance['artifacts'], {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'},
           {'manifest', 'manifest_sha256', 'split_hash', 'node_id_space'}, 'dataset artifacts')
    artifacts = instance['artifacts']
    if artifacts['node_id_space'] != 'pyg-global-node-index-v1':
        raise ConfigurationError('unsupported node ID space')
    if not artifacts['manifest'] or not artifacts['manifest_sha256'] or not artifacts['split_hash']:
        raise ConfigurationError('persisted Dataset/Split artifacts are required')
    manifest_path = (Path(directory) / artifacts['manifest']).resolve()
    if sha256_file(manifest_path) != artifacts['manifest_sha256']:
        raise ConfigurationError('dataset manifest digest mismatch')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    fields(manifest, {'schema', 'version', 'dataset', 'preprocessing', 'split', 'data_path', 'data_sha256', 'data_identity'},
                    {'schema', 'version', 'dataset', 'preprocessing', 'split', 'data_path', 'data_sha256', 'data_identity'}, 'dataset manifest')
    if manifest['schema'] != 'opengu.persisted_dataset_split' or manifest['version'] != 1:
        raise ConfigurationError('unknown persisted Dataset/Split manifest')
    for key in ('dataset', 'preprocessing', 'split'):
        if manifest[key] != instance[key]:
            raise ConfigurationError('dataset manifest ' + key + ' mismatch')
    data_path = (manifest_path.parent / manifest['data_path']).resolve()
    if sha256_file(data_path) != manifest['data_sha256']:
        raise ConfigurationError('persisted graph digest mismatch')
    with data_path.open('rb') as handle:
        data = pickle.load(handle)
    n = int(data.num_nodes)
    masks = [getattr(data, key + '_mask', None) for key in ('train', 'val', 'test')]
    if any(mask is None or mask.dtype != torch.bool or tuple(mask.shape) != (n,) or not mask.any() for mask in masks):
        raise ConfigurationError('three nonempty persisted boolean masks are required')
    if not torch.stack(masks).sum(0).eq(1).all():
        raise ConfigurationError('persisted split must partition the node space')
    identity = data_identity(data)
    if identity != manifest['data_identity'] or identity['split_hash'] != artifacts['split_hash']:
        raise ConfigurationError('actual Dataset/Split identity mismatch')
    if data.x.dtype != torch.float32 or not torch.isfinite(data.x).all():
        raise ConfigurationError('current consumers require finite float32 features')
    inputs = make_dataset_selection_inputs(data, dataset_name=instance['dataset']['name'].lower())
    return data, inputs


def verified_selection(reference, *, store_root, data, inputs):
    fields(reference, {'artifact_id', 'recipe_hash', 'content_hash'},
           {'artifact_id', 'recipe_hash', 'content_hash'}, 'Selection reference')
    if any(not value for value in reference.values()):
        raise ConfigurationError('an exact existing Selection reference is required')
    loaded = load_selection_artifact(store_root, reference['artifact_id'], num_nodes=inputs.num_nodes,
        candidate_nodes=inputs.candidate_nodes, expected_dataset_fingerprint=inputs.dataset_fingerprint,
        expected_graph_fingerprint=inputs.graph_fingerprint,
        expected_parameters={'split_hash': data_identity(data)['split_hash']})
    if loaded.recipe_hash != reference['recipe_hash'] or loaded.content_hash != reference['content_hash']:
        raise ConfigurationError('Selection digest mismatch')
    return loaded


def _plan_summary(config):
    return {
        'schema': 'opengu.modular_run', 'version': 2,
        'experiment_id': config['experiment_id'], 'case_id': config.get('case_id'),
        'stage': config['stage'], 'effective_selectors': config['selectors'],
        'effective_unlearning': config['unlearnings'],
        'effective_evaluations': config['evaluations'],
        'configuration_sources': config['configuration_sources'],
        'experiment_annotations': {
            key: config[key]
            for key in ('round', 'research_question', 'decision_owner') if key in config
        },
    }


def execute(path, *, context=None, dry_run=False):
    config = load_experiment(path)
    plan = _plan_summary(config)
    if dry_run:
        return {**plan, 'dry_run': True, 'execution_context_required': True,
                'producer_called': False}
    if not isinstance(context, ExecutionContext):
        raise ConfigurationError(
            'execution context must be supplied by project policy or a registered SyncMate stage')
    if config['stage'] != 'unlearning' and config['evaluations']:
        raise ConfigurationError('the current modular consumer evaluates GU results only')
    for evaluation in config['evaluations']:
        require_consumer(evaluation, 'modular_cpu_v1')
    directory = Path(config['source_directory'])
    from attack.cache_identity import resolve_store_root
    store_root = resolve_store_root(context.store_root)
    checkpoint_root = context.checkpoint_root
    runtime_root = context.runtime_root
    output = context.output
    data, inputs = read_dataset(config['dataset'], config['dataset_directory'])
    selectors = [{**item, 'budget': resolve_budget(item['budget'], inputs.candidate_count)} for item in config['selectors']]
    references = [config['selection_input']] if 'selection_input' in config else []
    loaded_selections = [verified_selection(ref, store_root=store_root, data=data, inputs=inputs) for ref in references]
    summary = {**plan, 'effective_selectors': selectors,
        'execution_receipt': context.receipt(), 'data_identity': data_identity(data),
        'selectors': [], 'unlearning': [], 'evaluations': []}
    if output.exists():
        raise FileExistsError('each invocation must use a new run output: ' + str(output))
    device = torch.device(context.request_device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    data = data.to(device)
    for item in selectors:
        model, checkpoints, observation = None, [], None
        if 'model' in item:
            model, checkpoints, observation = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
        resolved = resolve_methods(store_root=store_root, data=data, dataset_name=inputs.dataset_name,
            model=model, checkpoints=checkpoints, selectors=[item], model_config=item.get('model'), training=item.get('training'))[item['method']]
        reference = {key: resolved['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
        loaded_selections.append(verified_selection(reference, store_root=store_root, data=data, inputs=inputs))
        summary['selectors'].append({**resolved, 'checkpoint': observation})
    if config['stage'] == 'unlearning':
        from experiments.modular_gu import run_unlearning
        for item in config['unlearnings']:
            for selection in loaded_selections:
                model, _, checkpoint = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                    checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
                result = run_unlearning(item, selection=selection, model=model, data=data,
                    dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root)
                summary['unlearning'].append({**result, 'checkpoint': checkpoint})
        summary['evaluations'] = [
            evaluate_modular(item, summary['unlearning']) for item in config['evaluations']
        ]
    summary['selector_producer_called'] = any(item['score']['producer_called'] or item['selection']['cache']['producer_called'] for item in summary['selectors'])
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')
    return summary
