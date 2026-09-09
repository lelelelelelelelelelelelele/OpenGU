"""Execute independent instances through existing selector and GU consumers."""
from __future__ import annotations

import json
from dataclasses import dataclass
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


@dataclass(frozen=True)
class SelectionPrefix:
    """Consumer view; the hashes continue to identify the full source Artifact."""
    artifact_id: str
    recipe_hash: str
    content_hash: str
    artifact_k: int
    requested_k: int
    selected_nodes: tuple


def selection_prefix(loaded, requested_k):
    if type(requested_k) is not int or not 0 < requested_k <= loaded.k:
        raise ConfigurationError('requested Selection prefix is outside the source artifact')
    return SelectionPrefix(loaded.artifact_id, loaded.recipe_hash, loaded.content_hash,
                           loaded.k, requested_k, loaded.selected_nodes[:requested_k])


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


def _execute(path, *, context=None, dry_run=False, run_state):
    config = load_experiment(path)
    batches = list(experiment_batches(config))
    plan = _plan_summary(config)
    plan['batches'] = [{**_plan_summary(batch), 'matrix_values': batch['matrix_values']} for batch in batches]
    plan['logical_cells'] = sum(
        len(batch.get('output_inputs', [])) if batch['stage'] == 'metrics' else
        len(unlearning_entries(batch)) if batch['stage'] == 'unlearning' else len(selector_entries(batch))
        for batch in batches)
    if config['stage'] == 'metrics' and all(v.get('run') and v.get('sha256') for v in config['output_inputs']):
        from experiments.modular_artifacts import planned_cells
        plan['logical_cells'] = len(planned_cells(config))
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
    if config['stage'] == 'metrics' and any(not v.get('run') or not v.get('sha256') for v in config['output_inputs']):
        raise ConfigurationError('metrics requires bound run.json paths and checksums')
    directory = Path(config['source_directory'])
    # Import-time OpenGU CLI belongs to the execution adapter, not its caller's argv.
    runtime_defaults()
    from attack.cache_identity import resolve_store_root
    store_root = resolve_store_root(context.store_root)
    checkpoint_root = context.checkpoint_root
    runtime_root = context.runtime_root
    output = context.output
    if output.parent.exists():
        raise FileExistsError('each invocation must use a new run output: ' + str(output))
    from experiments.modular_artifacts import start_run
    run = start_run(config, context, path)
    run_state['run'] = run
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
        from experiments.modular_artifacts import read_run
        from experiments.unlearning_outputs import load_output
        from experiments.modular_config import dataset_binding
        portable = {d['data_identity']['split_hash']: [] for d in datasets}
        summary['metric_sources'] = {}
        for value in config['output_inputs']:
            previous, documents = read_run(directory / value['run'], value['sha256'])
            for cell, document in zip(previous['cells'], documents):
                reference = cell.get('output')
                if not reference:
                    continue
                payload = load_output(reference, store_root, dataset_root=dataset_root)
                matches = [d for d in datasets if d['data_identity'] == payload.identity['pairing']['data_identity']]
                if len(matches) != 1:
                    raise ConfigurationError('metrics input Dataset/Split mismatch')
                if (payload.identity['selection']['artifact_id'] != cell['selection_id']
                        or payload.arrays['selected_nodes'].tolist() != document['selection.json']['selected_nodes']
                        or payload.identity['target']['method'] != cell['conditions']['method']
                        or payload.identity['pairing']['model']['architecture'] != cell['conditions']['model']
                        or payload.identity['pairing']['training']['seed'] != cell['conditions']['seed']):
                    raise ConfigurationError('metrics source conditions differ from remote output')
                portable[matches[0]['data_identity']['split_hash']].append((reference, payload, None))
                summary['metric_sources'][cell['cell_id']] = {'output': reference,
                    'selection_document': document['selection.json'],
                    'source': cell.get('source', {'experiment_id': previous['experiment_id'], 'run_id': previous['run_id']})}
        for index, (data, _) in enumerate(loaded_data):
            for item in config['evaluations']:
                result = evaluate_modular(item, [], store_root=store_root, data=data,
                    dataset_root=dataset_root, verified_outputs=portable[datasets[index]['data_identity']['split_hash']])
                summary['evaluations'].append({**result, 'dataset_binding': dataset_binding(config, index)})
        summary['selector_producer_called'] = False
        from experiments.modular_artifacts import export_outputs
        export_outputs(summary, config=config, context=context, run=run)
        return summary
    device = torch.device(context.request_device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    for batch in batches:
        data, inputs = loaded_data[batch['matrix_values']['dataset_index']]
        data = data.to(device)
        loaded_selections = {}
        for item, selector_ref in selector_entries(batch):
            run_state['active'] = [c for c in run['cells'] if c['conditions']['selector_ref'] == selector_ref
                and all(c['conditions'][k] == v for k, v in batch['matrix_values'].items())]
            model, checkpoints, observation = None, [], None
            if 'model' in item:
                model, checkpoints, observation = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                    checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
            resolved = resolve_methods(store_root=store_root, data=data, dataset_name=inputs.dataset_name,
                model=model, checkpoints=checkpoints, selectors=[item], model_config=item.get('model'), training=item.get('training'))[item['method']]
            reference = {key: resolved['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
            loaded = verified_selection(reference, store_root=store_root, data=data, inputs=inputs,
                expected_selector=item['method'], expected_k=resolved['selection']['artifact_k'])
            loaded_selections[selector_ref] = selection_prefix(loaded, item['budget']['k'])
            summary['selectors'].append({**resolved, 'checkpoint': observation, 'matrix_values': batch['matrix_values'],
                'selector_ref': selector_ref, 'requested_k': item['budget']['k']})
            if config.get('return_scores'):
                from experiments.modular_artifacts import existing_scores
                arrays, semantics = existing_scores(resolved, inputs.candidate_nodes)
                summary['selectors'][-1].update(result_scores=arrays, score_semantics=semantics)
            run_state['active'] = []
        if config['stage'] == 'unlearning':
            from experiments.modular_gu import run_unlearning
            for item, gu_ref, _, selector_ref in unlearning_entries(batch):
                run_state['active'] = [c for c in run['cells']
                    if c['conditions']['selector_ref'] == selector_ref and c['conditions']['unlearning_ref'] == gu_ref
                    and all(c['conditions'][k] == v for k, v in batch['matrix_values'].items())]
                model, checkpoint = None, None
                if item['method'] != 'Retrain':
                    model, _, checkpoint = prepare_model(item, data=data, dataset_name=inputs.dataset_name,
                        checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
                consumer = run_unlearning
                if item['method'] == 'MEGU':
                    from experiments.modular_megu import run_megu_unlearning
                    consumer = run_megu_unlearning
                elif item['method'] == 'GraphEraser':
                    from experiments.modular_shards import run_shard_unlearning
                    consumer = run_shard_unlearning
                result = consumer(item, selection=loaded_selections[selector_ref], model=model, data=data,
                    dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root, dataset_root=dataset_root,
                    dataset_input=datasets[batch['matrix_values']['dataset_index']]['input_reference'])
                summary['unlearning'].append({**result, 'checkpoint': checkpoint,
                    'matrix_values': batch['matrix_values'], 'selector_ref': selector_ref,
                    'unlearning_ref': gu_ref})
                run_state['active'] = []
    if config['stage'] == 'unlearning':
        from experiments.modular_config import dataset_binding
        for index, (data, _) in enumerate(loaded_data):
            rows = [row for row in summary['unlearning'] if row['matrix_values']['dataset_index'] == index]
            for item in config['evaluations']:
                result = evaluate_modular(item, rows, store_root=store_root, data=data, dataset_root=dataset_root)
                summary['evaluations'].append({**result, 'dataset_binding': dataset_binding(config, index)})
    summary['selector_producer_called'] = any(item['score']['producer_called'] or item['selection']['cache']['producer_called'] for item in summary['selectors'])
    from experiments.modular_artifacts import export_outputs
    export_outputs(summary, config=config, context=context, run=run)
    for row in summary['selectors']:
        row.pop('result_scores', None)
    return summary



def execute(path, *, context=None, dry_run=False):
    run_state = {}
    try:
        return _execute(path, context=context, dry_run=dry_run, run_state=run_state)
    except BaseException as exc:
        if 'run' in run_state:
            from experiments.modular_artifacts import update_run
            run = run_state['run']
            run.update(status='failed', error=str(exc)[:1000])
            for cell in run_state.get('active', []):
                cell.update(status='failed', error=str(exc)[:1000])
            update_run(run, context.output)
        raise

