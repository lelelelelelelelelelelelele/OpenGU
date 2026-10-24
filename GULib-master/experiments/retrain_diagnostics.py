"""Explicit Ret-only replay of checksum-bound requests; never a Metrics producer."""
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import time

import torch

from experiments.effective_config import ConfigurationError


METRICS = {'best_accuracy', 'best_cross_entropy', 'final_accuracy', 'final_cross_entropy',
           'best_epoch', 'final_epoch', 'best_validation_accuracy', 'final_validation_accuracy',
           'optimization_sensitive'}


def validate_observer_reference(identity, cell, reference):
    from cache_v2 import ArtifactRecipe
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    source = cell.get('source', {})
    original = source.get('output', {})
    if ('output' in cell or cell['conditions']['method'] != 'Retrain'
            or reference['name'] != 'retrain_validation_trace'
            or reference['status'] != 'completed'
            or identity.get('source') != source
            or identity['output_identity']['target']['method'] != 'Retrain'
            or ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity['output_identity']}).recipe_hash != original.get('recipe_hash')):
        raise ValueError('Ret diagnostic Observer source identity mismatch')


def source_inputs(config, context, datasets, loaded_data):
    from experiments.modular_artifacts import read_run, metric_source_cells
    from experiments.unlearning_outputs import load_output_payload, resolve_output
    from experiments.modular_config import model_training, dataset_binding, resolve_budget
    from experiments.modular_run import verified_selection
    from utils.target_checkpoint import state_hash
    root = context.store_root.parent.parent
    ready = []
    seen = set()
    for source in config['output_inputs']:
        path = Path(config['source_directory']) / source['run']
        run, documents = read_run(path, source['sha256'])
        for cell, document in metric_source_cells(run, source, documents):
            if run['stage'] != 'unlearning' or cell['conditions']['method'] != 'Retrain':
                raise ConfigurationError('diagnostic source must be an original Retrain Output')
            reference = cell['output']
            if reference.get('storage') == 'run':
                raise ConfigurationError('Ret diagnostics require an immutable cached source Output')
            if reference['recipe_hash'] in seen:
                raise ConfigurationError('duplicate Ret diagnostic source Output')
            seen.add(reference['recipe_hash'])
            payload = load_output_payload(reference, context.store_root, dataset_root=root)
            identity, pair = payload.identity, payload.identity['pairing']
            matches = [i for i, item in enumerate(datasets)
                       if item['data_identity'] == pair['data_identity'] and item['input_reference'] == identity['dataset_input']]
            if len(matches) != 1:
                raise ConfigurationError('Ret diagnostic Dataset/Split mismatch')
            index = matches[0]
            data, inputs = loaded_data[index]
            output = resolve_output(payload, root, data=data)
            selected = document['selection.json']
            binding = dataset_binding(config, index)
            if (any(cell['conditions'][key] != binding[key] for key in ('dataset_name', 'dataset_fingerprint'))
                    or resolve_budget(cell['conditions']['budget'], int(data.train_mask.sum()))['k'] != len(pair['selected_nodes'])
                    or identity['target']['method'] != 'Retrain'
                    or pair['model']['architecture'] != cell['conditions']['model']
                    or pair['training']['seed'] != cell['conditions']['seed']
                    or identity['selection']['artifact_id'] != cell['selection_id']
                    or pair['selected_nodes'] != selected['selected_nodes']
                    or selected['requested_k'] != len(pair['selected_nodes'])):
                raise ConfigurationError('Ret diagnostic source conditions disagree with Output')
            model, training = model_training({'model': pair['model'], 'training': pair['training']})
            if (model != pair['model'] or training != pair['training'] or training['epochs'] != 3000
                    or model['architecture'] != 'OpenGU.GCNNet' or pair['deletion']['evaluation_graph'] != 'original'):
                raise ConfigurationError('Ret diagnostics require exact 3000-epoch GCN training and original test graph')
            selection = verified_selection(identity['selection'], store_root=context.store_root, data=data,
                inputs=inputs, expected_selector=cell['conditions']['selector'])
            nodes = tuple(pair['selected_nodes'])
            if tuple(selection.selected_nodes[:len(nodes)]) != nodes:
                raise ConfigurationError('Ret diagnostic ordered Selection prefix mismatch')
            ready.append({'cell': cell, 'selection': selected, 'output': output,
                'data_index': index, 'instance': {'model': model, 'training': training},
                'old_state_hash': state_hash({k: torch.tensor(v) for k, v in output.state.items()}),
                'source': {'experiment_id': run['experiment_id'], 'run_id': run['run_id'],
                    'cell_id': cell['cell_id'], 'commit': run['commit'], 'run_sha256': source['sha256'],
                    'output': reference}})
    return ready


def execute_retrain_diagnostics(config, context, datasets, loaded_data, summary, run_state, audit, notify):
    from attack.cache_identity import seeded_execution
    from experiments.modular_model import create_model, train_supervised
    from experiments.node_deletion import retained_graph
    from experiments.observers import ObserverSession, observer_specs
    from experiments.observers.retrain_validation import validate_masks
    from experiments.modular_artifacts import _write, update_run
    from experiments.modular_progress import notify_event
    from experiments.implementation_identity import implementation_fingerprint, model_functions
    from utils.target_checkpoint import data_identity
    run = run_state['run']
    root = context.store_root.parent.parent
    notify_event(notify, 'progress', position={'stage': 'retrain_inputs'}, current=0, total=1)
    with audit.phase('retrain_diagnostic_inputs'):
        ready = source_inputs(config, context, datasets, loaded_data)
    notify_event(notify, 'progress', position={'stage': 'retrain_inputs'}, current=1, total=1)
    notify_event(notify, 'progress', position={'stage': 'retrain_diagnostics'}, current=0, total=len(ready))
    cells = {cell['cell_id']: cell for cell in run['cells']}
    if set(cells) != {item['cell']['cell_id'] for item in ready}:
        raise ValueError('Ret diagnostic plan differs from execution sources')
    summary['retrain_diagnostics'] = []
    for item in ready:
        cell = cells[item['cell']['cell_id']]
        run_state['active'] = [cell]
        source_data, inputs = loaded_data[item['data_index']]
        data = source_data.clone().to(context.request_device)
        retained = retained_graph(data, item['output'].identity['pairing']['selected_nodes'])
        validate_masks(retained)
        instance = item['instance']
        folder = context.output.parent / cell['path']
        with seeded_execution(instance['training']['seed']):
            model = create_model(instance['model'], inputs.dataset_name, retained, context.request_device)
        identity = {'experiment_id': run['experiment_id'], 'run_id': run['run_id'],
            'cell_id': cell['cell_id'], 'conditions': cell['conditions'], 'commit': run['commit'],
            'source': item['source'], 'output_identity': item['output'].identity,
            'configuration_fingerprint': summary['configuration_fingerprint'],
            'training': instance['training'], 'validation_graph_identity': data_identity(retained),
            'producer': {'semantic_version': 'ret-source-validation-diagnostics-v1',
                'implementation': implementation_fingerprint(train_supervised, execute_retrain_diagnostics, *model_functions(model))}}
        session = ObserverSession(observer_specs(config, 'Retrain'), folder, identity)
        error = None
        started = time.perf_counter()
        try:
            with audit.entry('retrain_diagnostics', cell['conditions']) as fact, audit.phase('retrain_training'):
                with seeded_execution(instance['training']['seed']):
                    _, statistics = train_supervised(model, retained, instance['training'], (), epoch_end=session)
                session({'phase': 'training_complete', 'step': 3000, 'values': {
                    'model': model, 'original': data, 'old_logits': item['output'].arrays['logits'],
                    'old_state_hash': item['old_state_hash'], 'dataset_root': root,
                    'asset_root': context.runtime_root / 'retrain_diagnostics' / cell['cell_id']}})
                fact['metrics'] = {'training_epochs': 3000}
        except BaseException as exc:
            error = exc
            raise
        finally:
            session.finish(error=error)
        result = session.items[0][1].result
        elapsed = time.perf_counter() - started
        metrics = {role + '_' + key: result[role]['test'][key]
                   for role in ('best', 'final') for key in ('accuracy', 'cross_entropy')}
        metrics.update(best_epoch=result['best']['epoch'], final_epoch=3000,
            best_validation_accuracy=result['best']['validation']['accuracy'],
            final_validation_accuracy=result['final']['validation']['accuracy'],
            optimization_sensitive=int(result['windows']['optimization_sensitive']))
        cell.update(source=item['source'], selection_id=cell['selection_id'] if 'selection_id' in cell else item['selection']['selection_id'],
            observers=session.references, cache={'method': 'disabled'},
            producer_called={'selection': False, 'original': False, 'method': True},
            timing={'method_compute_seconds': elapsed, 'observer_seconds': session.seconds,
                    'training_seconds_including_epoch_observer': statistics['training_seconds']})
        documents = {'selection.json': {**item['selection'], 'cell_id': cell['cell_id']},
            'metrics.json': {'cell_id': cell['cell_id'], 'rows': [{'stage': 'retrain_validation_trace', 'values': metrics}]}}
        for name, document in documents.items():
            _write(folder / name, document)
            cell['files'][name] = {'sha256': hashlib.sha256((folder / name).read_bytes()).hexdigest()}
            cell['results'][name.split('.')[0]] = 'completed'
        for reference in session.references:
            cell['files'].update(reference['files'])
        cell['status'] = 'completed'
        update_run(run, context.output)
        summary['retrain_diagnostics'].append({'cell_id': cell['cell_id'], 'source': item['source'], 'metrics': metrics})
        notify_event(notify, 'progress', position={'stage': 'retrain_diagnostics'},
                     current=len(summary['retrain_diagnostics']), total=len(ready))
    notify_event(notify, 'progress', position={'stage': 'export'}, current=0, total=1)
    run['status'], run['generated_at'] = 'completed', datetime.now(timezone.utc).isoformat()
    update_run(run, context.output)
    notify_event(notify, 'progress', position={'stage': 'export'}, current=1, total=1)
    summary['selector_producer_called'] = False
    summary['execution_timing'] = {'phase_seconds_exclusive': audit.timings, 'audit_seconds': audit.seconds}
    return summary
