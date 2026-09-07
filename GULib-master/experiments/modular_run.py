"""Execute independent instances through existing selector and GU consumers."""
from __future__ import annotations

import json
from pathlib import Path
import torch
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import fields, ConfigurationError
from experiments.modular_config import load_experiment, resolve_budget, experiment_batches, configuration_fingerprint, selector_entries, unlearning_entries
from experiments.modular_evaluation import evaluate_modular, require_consumer
from experiments.modular_execution import ExecutionContext
from experiments.modular_model import prepare_model, runtime_defaults
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1.method_cache import resolve_methods
from utils.target_checkpoint import data_identity
from experiments.dataset_inputs import read_dataset


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
        'schema': 'opengu.modular_run', 'version': 3,
        'experiment_id': config['experiment_id'], 'case_id': config.get('case_id'),
        'stage': config['stage'], 'effective_selectors': config['selectors'],
        'effective_unlearning': config['unlearnings'],
        'effective_evaluations': config['evaluations'],
        'effective_datasets': config['datasets'],
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
        len(unlearning_entries(batch)) if batch['stage'] == 'unlearning' else len(selector_entries(batch))
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
    dataset_root = context.store_root.parent.parent
    datasets = []
    loaded_data = []
    for index, instance in enumerate(config['datasets']):
        dataset_config = {'dataset': instance, 'dataset_directory': config['dataset_directories'][index]}
        if context.level == 'verification':
            from experiments.modular_execution import verify_temporary_dataset
            verify_temporary_dataset(dataset_config, context)
        data, inputs = read_dataset(instance, dataset_config['dataset_directory'])
        loaded_data.append((data, inputs))
        from experiments.dataset_inputs import bind_input
        reference = bind_input(instance, dataset_config['dataset_directory'], dataset_root)
        if context.level == 'formal' and any(not reference[key].startswith('data/processed/') for key in ('manifest', 'graph')):
            raise ConfigurationError('formal inputs must stay in data/processed')
        datasets.append({'input_reference': reference, 'dataset': instance, 'data_identity': data_identity(data),
                         'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count})
    for batch in batches:
        _, inputs = loaded_data[batch['matrix_values']['dataset_index']]
        batch['selectors'] = [{**item, 'budget': resolve_budget(item['budget'], inputs.candidate_count)}
                              for item in batch['selectors']]
    summary = {**plan, 'effective_selectors': [item for batch in batches for item in batch['selectors']],
        'effective_unlearning': [item for batch in batches for item in batch['unlearnings']],
        'execution_receipt': context.receipt(), 'datasets': datasets,
        'selectors': [], 'unlearning': [], 'evaluations': []}
    if config['stage'] == 'metrics':
        from experiments.modular_artifacts import read_summary_outputs
        from cache_v2 import canonical_sha256
        # Validate every imported dataset before distributing outputs by identity.
        portable = {canonical_sha256(d['dataset']): [] for d in datasets}
        rows = []
        for value in config['output_inputs']:
            if 'summary' not in value:
                rows.append(value)
                continue
            if not value['summary'] or not value.get('sha256'):
                raise ConfigurationError('bind real output summaries and SHA-256 before metrics')
            previous, outputs = read_summary_outputs(directory / value['summary'], value['sha256'], dataset_root=dataset_root)
            for prior in previous['datasets']:
                if prior not in datasets:
                    raise ConfigurationError('metrics input Dataset/Split mismatch')
            for row, result in zip(previous['unlearning'], outputs):
                fingerprint = row['matrix_values']['dataset_fingerprint']
                portable[fingerprint].append((result['output'], result['payload'], None))
        if rows and len(datasets) != 1:
            raise ConfigurationError('multi-dataset metrics requires bound portable summaries')
        from experiments.modular_config import dataset_binding
        for index, (data, _) in enumerate(loaded_data):
            binding = dataset_binding(config, index)
            for item in config['evaluations']:
                result = evaluate_modular(item, rows, store_root=store_root, data=data,
                    dataset_root=dataset_root, verified_outputs=portable[binding['dataset_fingerprint']])
                summary['evaluations'].append({**result, 'dataset_binding': binding})
        summary['selector_producer_called'] = False
        _write_summary(output, summary)
        return summary
    device = torch.device(context.request_device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    for batch in batches:
        data, inputs = loaded_data[batch['matrix_values']['dataset_index']]
        data = data.to(device)
        loaded_selections = {}
        for item, selector_ref in selector_entries(batch):
            model, checkpoints, observation = None, [], None
            if 'model' in item:
                model, checkpoints, observation = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                    checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
            resolved = resolve_methods(store_root=store_root, data=data, dataset_name=inputs.dataset_name,
                model=model, checkpoints=checkpoints, selectors=[item], model_config=item.get('model'), training=item.get('training'))[item['method']]
            reference = {key: resolved['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
            loaded_selections[selector_ref] = verified_selection(reference, store_root=store_root, data=data, inputs=inputs)
            summary['selectors'].append({**resolved, 'checkpoint': observation, 'matrix_values': batch['matrix_values'],
                'selector_ref': selector_ref})
        if config['stage'] == 'unlearning':
            from experiments.modular_gu import run_unlearning
            for item, gu_ref, _, selector_ref in unlearning_entries(batch):
                model, checkpoint = None, None
                if item['method'] != 'Retrain':
                    model, _, checkpoint = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                        checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
                result = run_unlearning(item, selection=loaded_selections[selector_ref], model=model, data=data,
                    dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root, dataset_root=dataset_root,
                    dataset_input=datasets[batch['matrix_values']['dataset_index']]['input_reference'])
                summary['unlearning'].append({**result, 'checkpoint': checkpoint,
                    'matrix_values': batch['matrix_values'], 'selector_ref': selector_ref,
                    'unlearning_ref': gu_ref})
    if config['stage'] == 'unlearning':
        from experiments.modular_config import dataset_binding
        for index, (data, _) in enumerate(loaded_data):
            rows = [row for row in summary['unlearning'] if row['matrix_values']['dataset_index'] == index]
            for item in config['evaluations']:
                result = evaluate_modular(item, rows, store_root=store_root, data=data, dataset_root=dataset_root)
                summary['evaluations'].append({**result, 'dataset_binding': dataset_binding(config, index)})
    summary['selector_producer_called'] = any(item['score']['producer_called'] or item['selection']['cache']['producer_called'] for item in summary['selectors'])
    from experiments.modular_artifacts import export_outputs
    export_outputs(summary, output=output, store_root=store_root, dataset_root=dataset_root)
    _write_summary(output, summary)
    return summary


def _write_summary(output, summary):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')
    return summary
