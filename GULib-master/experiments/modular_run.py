"""Execute independent instances through existing selector and GU consumers."""
from __future__ import annotations

import json
import pickle
from pathlib import Path
import torch
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import fields, ConfigurationError
from experiments.modular_config import load_experiment, resolve_budget, experiment_batches, configuration_fingerprint
from experiments.modular_evaluation import evaluate_modular, require_consumer
from experiments.modular_execution import ExecutionContext
from experiments.modular_model import prepare_model, runtime_defaults
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


def verified_selection(reference, *, store_root, data, inputs, expected_selector=None, expected_k=None):
    fields(reference, {'artifact_id', 'recipe_hash', 'content_hash'},
           {'artifact_id', 'recipe_hash', 'content_hash'}, 'Selection reference')
    if any(not value for value in reference.values()):
        raise ConfigurationError('an exact existing Selection reference is required')
    loaded = load_selection_artifact(store_root, reference['artifact_id'], num_nodes=inputs.num_nodes,
        candidate_nodes=inputs.candidate_nodes, expected_selector=expected_selector, expected_k=expected_k,
        expected_dataset_fingerprint=inputs.dataset_fingerprint,
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
            for key in ('round',) if key in config
        },
    }


def execute(path, *, context=None, dry_run=False):
    config = load_experiment(path)
    batches = list(experiment_batches(config))
    plan = _plan_summary(config)
    plan['batches'] = [{**_plan_summary(batch), 'matrix_values': batch['matrix_values']} for batch in batches]
    plan['logical_cells'] = sum(
        len(batch.get('output_inputs', [])) if batch['stage'] == 'metrics' else
        (len(batch['selectors']) or batch.get('selection_count', 1)) * (len(batch['unlearnings']) or 1)
        for batch in batches)
    plan['configuration_fingerprint'] = configuration_fingerprint(path)
    if dry_run:
        return {**plan, 'dry_run': True, 'execution_context_required': True,
                'producer_called': False}
    if not isinstance(context, ExecutionContext):
        raise ConfigurationError(
            'execution context must be supplied by the experiment entry')
    if config['stage'] == 'selector' and config['evaluations']:
        raise ConfigurationError('the current modular consumer evaluates GU results only')
    for evaluation in config['evaluations']:
        require_consumer(evaluation, 'modular_v1')
    if config['stage'] == 'unlearning' and any(
            item['case'] == 'post_unlearning_utility_and_retrain_gap' for item in config['evaluations']):
        raise ConfigurationError('retrain-gap belongs to the independent metrics stage')
    directory = Path(config['source_directory'])
    # Import-time OpenGU CLI belongs to the execution adapter, not its caller's argv.
    runtime_defaults()
    from attack.cache_identity import resolve_store_root
    store_root = resolve_store_root(context.store_root)
    checkpoint_root = context.checkpoint_root
    runtime_root = context.runtime_root
    output = context.output
    if output.exists() or (output.parent / (output.stem + '.outputs')).exists():
        raise FileExistsError('each invocation must use a new run output: ' + str(output))
    if context.level == 'verification' and context.executor in ('experiment-run', 'local-cpu-verification'):
        from experiments.modular_execution import verify_temporary_dataset
        verify_temporary_dataset(config, context)
    data, inputs = read_dataset(config['dataset'], config['dataset_directory'])
    for batch in batches:
        batch['selectors'] = [{**item, 'budget': resolve_budget(item['budget'], inputs.candidate_count)}
                              for item in batch['selectors']]
    references = [config['selection_input']] if 'selection_input' in config and 'selection_source' not in config else []
    existing_selections = [verified_selection(ref, store_root=store_root, data=data, inputs=inputs) for ref in references]
    source_rows = None
    if 'selection_source' in config:
        bound = config['selection_input']
        if not bound['summary'] or not bound['sha256']:
            raise ConfigurationError('bind a real selector summary and its SHA-256 before execution')
        source_path = (directory / bound['summary']).resolve()
        if sha256_file(source_path) != bound['sha256']:
            raise ConfigurationError('selector summary checksum mismatch')
        source_summary = json.loads(source_path.read_text(encoding='utf-8'))
        expected = configuration_fingerprint(directory / bound['experiment_ref'])
        if (source_summary['configuration_fingerprint'] != expected
                or source_summary['stage'] != 'selector'
                or source_summary['data_identity'] != data_identity(data)):
            raise ConfigurationError('selector summary configuration or Dataset/Split mismatch')
        source_rows = source_summary['selectors']
        if len(source_rows) != sum(batch['selection_count'] for batch in batches):
            raise ConfigurationError('selector summary row count mismatch')
    summary = {**plan, 'effective_selectors': [item for batch in batches for item in batch['selectors']],
        'effective_unlearning': [item for batch in batches for item in batch['unlearnings']],
        'execution_receipt': context.receipt(), 'data_identity': data_identity(data), 'dataset': config['dataset'],
        'selectors': [], 'unlearning': [], 'evaluations': []}
    if output.exists():
        raise FileExistsError('each invocation must use a new run output: ' + str(output))
    if config['stage'] == 'metrics':
        rows = []
        portable = []
        from experiments.modular_artifacts import read_summary_outputs
        for value in config['output_inputs']:
            if 'summary' in value:
                if not value['summary'] or not value.get('sha256'):
                    raise ConfigurationError('bind real output summaries and SHA-256 before metrics')
                previous, outputs = read_summary_outputs(directory / value['summary'], value['sha256'])
                if previous['dataset'] != config['dataset'] or previous['data_identity'] != data_identity(data):
                    raise ConfigurationError('metrics input Dataset/Split mismatch')
                portable.extend((result['output'], result['payload'], None) for result in outputs)
            else:
                rows.append(value)
        summary['evaluations'] = [evaluate_modular(item, rows, store_root=store_root, data=data, verified_outputs=portable)
                                  for item in config['evaluations']]
        summary['selector_producer_called'] = False
        _write_summary(output, summary)
        return summary
    device = torch.device(context.request_device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    data = data.to(device)
    for batch in batches:
        loaded_selections = [(selection, None) for selection in existing_selections]
        if source_rows is not None:
            matching = [row for row in source_rows if row['matrix_values'] == batch['matrix_values']]
            if len(matching) != batch['selection_count']:
                raise ConfigurationError('selector summary seed/budget binding mismatch')
            source_batch = next(item for item in experiment_batches(config['selection_source'])
                                if item['matrix_values'] == batch['matrix_values'])
            if [row['selector_ref'] for row in matching] != config['selection_source']['selector_refs']:
                raise ConfigurationError('selector summary reference order mismatch')
            for row, instance in zip(matching, source_batch['selectors']):
                ref = {key: row['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
                loaded_selections.append((verified_selection(ref, store_root=store_root, data=data, inputs=inputs,
                    expected_selector=instance['method'],
                    expected_k=resolve_budget(instance['budget'], inputs.candidate_count)['k']), row['selector_ref']))
        for selector_index, item in enumerate(batch['selectors']):
            model, checkpoints, observation = None, [], None
            if 'model' in item:
                model, checkpoints, observation = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                    checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
            resolved = resolve_methods(store_root=store_root, data=data, dataset_name=inputs.dataset_name,
                model=model, checkpoints=checkpoints, selectors=[item], model_config=item.get('model'), training=item.get('training'))[item['method']]
            reference = {key: resolved['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
            loaded_selections.append((verified_selection(reference, store_root=store_root, data=data, inputs=inputs),
                                      config['selector_refs'][selector_index]))
            summary['selectors'].append({**resolved, 'checkpoint': observation, 'matrix_values': batch['matrix_values'],
                'selector_ref': config['selector_refs'][selector_index]})
        if config['stage'] == 'unlearning':
            from experiments.modular_gu import run_unlearning
            for gu_index, item in enumerate(batch['unlearnings']):
                for selection, selector_ref in loaded_selections:
                    model, checkpoint = None, None
                    if item['method'] != 'Retrain':
                        model, _, checkpoint = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                            checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
                    result = run_unlearning(item, selection=selection, model=model, data=data,
                        dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root)
                    summary['unlearning'].append({**result, 'checkpoint': checkpoint,
                        'matrix_values': batch['matrix_values'], 'selector_ref': selector_ref,
                        'unlearning_ref': config['unlearning_refs'][gu_index]})
    if config['stage'] == 'unlearning':
        summary['evaluations'] = [
            evaluate_modular(item, summary['unlearning'], store_root=store_root, data=data) for item in config['evaluations']
        ]
    summary['selector_producer_called'] = any(item['score']['producer_called'] or item['selection']['cache']['producer_called'] for item in summary['selectors'])
    from experiments.modular_artifacts import export_outputs
    export_outputs(summary, output=output, store_root=store_root)
    _write_summary(output, summary)
    return summary


def _write_summary(output, summary):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')
    return summary
