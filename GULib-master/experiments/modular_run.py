"""Execute independent instances through existing selector and GU consumers."""
from __future__ import annotations

from experiments.im_methods import IM_METHODS

import json
from dataclasses import dataclass
from pathlib import Path
import torch
from cache_v2.runtime import load_selection_artifact
from experiments.effective_config import fields, ConfigurationError
from experiments.modular_config import load_experiment, resolve_budget, experiment_batches, configuration_fingerprint, selector_entries, unlearning_entries
from experiments.modular_evaluation import evaluate_modular, require_consumer, is_paired_evaluation
from experiments.modular_execution import ExecutionContext
from experiments.modular_progress import execution_batches, request_entries, request_position, notify_event
from experiments.modular_model import prepare_model, runtime_defaults
from experiments.selection_inputs import make_dataset_selection_inputs
from experiments.target_direct_v1.method_cache import resolve_methods
from utils.target_checkpoint import data_identity, tensor_hash
from experiments.dataset_inputs import read_dataset


def verified_selection(reference, *, store_root, data, inputs, expected_selector=None, expected_k=None, expected_parameters=None):
    fields(reference, {'artifact_id', 'recipe_hash', 'content_hash'},
           {'artifact_id', 'recipe_hash', 'content_hash'}, 'Selection reference')
    if any(not value for value in reference.values()):
        raise ConfigurationError('an exact existing Selection reference is required')
    loaded = load_selection_artifact(store_root, reference['artifact_id'], num_nodes=inputs.num_nodes,
        candidate_nodes=inputs.candidate_nodes, expected_selector=expected_selector, expected_k=expected_k,
        expected_dataset_fingerprint=inputs.dataset_fingerprint,
        expected_graph_fingerprint=inputs.graph_fingerprint,
        expected_parameters={'split_hash': tensor_hash(torch.stack([
            getattr(data,name+'_mask').detach().cpu().to(torch.uint8) for name in ('train','val','test')])),
            **(expected_parameters or {})})
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
        'effective_observers': config.get('observers', []),
        'execution': config.get('execution', {}),
        'effective_datasets': config['datasets'],
        'configuration_sources': config['configuration_sources'],
        'effective_parameter_profile': config.get('effective_parameter_profile'),
        'experiment_annotations': {
            key: config[key]
            for key in ('round',) if key in config
        },
    }


def _execute(path, *, context=None, dry_run=False, run_state, notify=None):
    config = load_experiment(path)
    exact = None
    if 'exact_inputs' in config:
        from experiments.exact_replay_inputs import ExactInputs
        exact = ExactInputs(config)
    batches = list(experiment_batches(config))
    plan = _plan_summary(config)
    if exact is not None:
        plan['exact_inputs'] = dict(config['exact_inputs'])
    plan['batches'] = [{**_plan_summary(batch), 'matrix_values': batch['matrix_values']} for batch in batches]
    plan['logical_cells'] = sum(
        len(batch.get('output_inputs', [])) if batch['stage'] in ('metrics', 'retrain_diagnostics') else
        len(unlearning_entries(batch)) if batch['stage'] == 'unlearning' else len(selector_entries(batch))
        for batch in batches)
    if config['stage'] in ('metrics', 'retrain_diagnostics') and all(v.get('run') and v.get('sha256') for v in config['output_inputs']):
        from experiments.modular_artifacts import planned_cells
        plan['logical_cells'] = len(planned_cells(config))
    plan['configuration_fingerprint'] = configuration_fingerprint(path)
    if config['stage'] == 'unlearning' and any(
            is_paired_evaluation(item) for item in config['evaluations']):
        if exact is None and not any(item['method'] == 'Retrain' for item in config['unlearnings']):
            raise ConfigurationError('paired evaluations require an explicit Retrain in unlearning_refs')
    if dry_run:
        return {**plan, 'dry_run': True, 'execution_context_required': True,
                'producer_called': False}
    if not isinstance(context, ExecutionContext):
        raise ConfigurationError(
            'execution context must be supplied by the experiment entry')
    from experiments.ret_reference_policy import configure_for_experiment
    configure_for_experiment(config)
    if config['stage'] == 'selector' and config['evaluations']:
        raise ConfigurationError('the current modular consumer evaluates GU results only')
    for evaluation in config['evaluations']:
        require_consumer(evaluation, 'modular_v1')
    if config['stage'] in ('metrics', 'retrain_diagnostics') and any(not v.get('run') or not v.get('sha256') for v in config['output_inputs']):
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
    from experiments.execution_audit import ExecutionAudit, cache_fact
    audit = ExecutionAudit(context, plan['configuration_fingerprint'], config['experiment_id'])
    run_state['audit'] = audit
    dataset_root = context.store_root.parent.parent
    datasets = []
    loaded_data = []
    for index, instance in enumerate(config['datasets']):
        position = {'stage': 'data', 'dataset_index': index}
        notify_event(notify, 'progress', position=position, current=0, total=1)
        dataset_config = {'dataset': instance, 'dataset_directory': config['dataset_directories'][index]}
        if context.level == 'verification':
            from experiments.modular_execution import verify_temporary_dataset
            verify_temporary_dataset(dataset_config, context)
        with audit.phase('dataset_prepare'):
            data, inputs = read_dataset(instance, dataset_config['dataset_directory'])
        loaded_data.append((data, inputs))
        from experiments.dataset_inputs import bind_input
        reference = bind_input(instance, dataset_config['dataset_directory'], dataset_root)
        if context.level == 'formal' and any(not reference[key].startswith('data/processed/') for key in ('manifest', 'graph')):
            raise ConfigurationError('formal inputs must stay in data/processed')
        datasets.append({'input_reference': reference, 'dataset': instance, 'data_identity': data_identity(data),
                         'num_nodes': inputs.num_nodes, 'candidate_count': inputs.candidate_count})
        notify_event(notify, 'progress', position=position, current=1, total=1)
    for batch in batches:
        _, inputs = loaded_data[batch['matrix_values']['dataset_index']]
        batch['selectors'] = [{**item, 'budget': resolve_budget(item['budget'], inputs.candidate_count)}
                              for item in batch['selectors']]
    summary = {**plan, 'effective_selectors': [item for batch in batches for item in batch['selectors']],
        'effective_unlearning': [item for batch in batches for item in batch['unlearnings']],
        'execution_receipt': context.receipt(), 'datasets': datasets,
        'selectors': [], 'unlearning': [], 'evaluations': []}
    if config['stage'] == 'retrain_diagnostics':
        from experiments.retrain_diagnostics import execute_retrain_diagnostics
        return execute_retrain_diagnostics(config, context, datasets, loaded_data, summary, run_state, audit, notify)
    if config['stage'] == 'metrics':
        from experiments.modular_artifacts import read_run, metric_source_cells
        from experiments.evaluation_cache import describe_output
        from experiments.modular_config import dataset_binding
        portable = {d['data_identity']['split_hash']: [] for d in datasets}
        summary['metric_sources'] = {}
        position = {'stage': 'metric_inputs'}
        total = len(config['output_inputs'])
        notify_event(notify, 'progress', position=position, current=0, total=total)
        for source_index, value in enumerate(config['output_inputs']):
            previous, documents = read_run(directory / value['run'], value['sha256'])
            for cell, document in metric_source_cells(previous, value, documents):
                reference = cell.get('output')
                if not reference:
                    continue
                with audit.entry('evaluation', {**cell['conditions'], 'evaluation_part': 'source_validation'}) as fact, audit.phase('evaluation_inputs'):
                    if reference.get('storage') == 'run':
                        from experiments.unlearning_outputs import load_output
                        payload = load_output(reference, store_root, dataset_root=dataset_root).identity
                    else:
                        payload = describe_output(reference, store_root)
                    matches = [d for d in datasets if d['data_identity'] == payload['pairing']['data_identity']]
                    if len(matches) != 1:
                        raise ConfigurationError('metrics input Dataset/Split mismatch')
                    if payload['dataset_input'] != matches[0]['input_reference']:
                        raise ConfigurationError('metrics input bound Dataset/Split mismatch')
                    if (payload['selection']['artifact_id'] != cell['selection_id']
                            or payload['pairing']['selected_nodes'] != document['selection.json']['selected_nodes']
                            or payload['target']['method'] != cell['conditions']['method']
                            or payload['pairing']['model']['architecture'] != cell['conditions']['model']
                            or payload['pairing']['training']['seed'] != cell['conditions']['seed']):
                        raise ConfigurationError('metrics source conditions differ from remote output')
                    original_checkpoint = cell.get('cache_provenance', {}).get('original_checkpoint')
                    portable[matches[0]['data_identity']['split_hash']].append((reference, payload, None, cell['conditions'], original_checkpoint, cell['cell_id']))
                    summary['metric_sources'][cell['cell_id']] = {'output': reference,
                        'selection_document': document['selection.json'], 'original_checkpoint': original_checkpoint,
                        'source': cell.get('source', {'experiment_id': previous['experiment_id'], 'run_id': previous['run_id']})}
                    fact['metrics'] = {'inputs_verified': 1}
            notify_event(notify, 'progress', position=position, current=source_index + 1, total=total)
        for index, (data, _) in enumerate(loaded_data):
            position = {'stage': 'evaluation', 'dataset_index': index}
            total = len(config['evaluations'])
            notify_event(notify, 'progress', position=position, current=0, total=total)
            for evaluation_index, item in enumerate(config['evaluations']):
                result = evaluate_modular(item, [{'output':v[0], 'conditions':v[3], 'original_checkpoint':v[4], 'cell_id':v[5]} for v in portable[datasets[index]['data_identity']['split_hash']]], store_root=store_root, data=data,
                    dataset_root=dataset_root, audit=audit, checkpoint_root=checkpoint_root, device=context.request_device, endpoint_config=config)
                summary['evaluations'].append({**result, 'dataset_binding': dataset_binding(config, index)})
                notify_event(notify, 'progress', position=position, current=evaluation_index + 1, total=total)
        summary['selector_producer_called'] = False
        from experiments.modular_artifacts import export_outputs
        notify_event(notify, 'progress', position={'stage': 'export'}, current=0, total=1)
        with audit.phase('export'):
            export_outputs(summary, config=config, context=context, run=run)
        notify_event(notify, 'progress', position={'stage': 'export'}, current=1, total=1)
        summary['execution_timing'] = {'phase_seconds_exclusive': audit.timings, 'audit_seconds': audit.seconds}
        return summary
    device = torch.device(context.request_device)
    if device.type == 'cuda' and not torch.cuda.is_available():
        raise RuntimeError('CUDA requested but unavailable')
    # Execute larger ratios first even when the ordinary table lists small
    # budgets first. Cell identities and declaration-order reporting stay intact.
    ordered_batches = execution_batches(config, batches=batches)
    from experiments.prepared_models import PreparedModels
    from experiments.output_lookup import OutputLookup
    prepared = PreparedModels(prepare_model)
    reference_only = any('reference' in item for item in config['unlearnings'])
    outputs = OutputLookup(checkpoint_root, store_root, directory)
    declaration_order = {}
    for batch_index, batch in enumerate(ordered_batches):
        for _, gu_ref, _, selector_ref in unlearning_entries(batch):
            key = (json.dumps(batch['matrix_values'], sort_keys=True), gu_ref, selector_ref)
            declaration_order[key] = len(declaration_order)
        entries = selector_entries(batch)
        group = (batch['matrix_values']['dataset_index'], batch['matrix_values']['training_seed'])
        prepared.select_group(group)
        outputs.select_group(group)
        data, inputs = loaded_data[batch['matrix_values']['dataset_index']]
        data = data.to(device)
        if config['stage'] == 'unlearning' and exact is None:
            with audit.phase('shared_output_request_prepare'):
                outputs.prepare([item for item in batch['unlearnings']
                    if config.get('execution',{}).get('gu_cache',{}).get(item['method'],'reuse')=='reuse'],data)
        for item, selector_ref in entries:
            position = request_position('selector', batch_index, batch, selector_ref)
            notify_event(notify, 'progress', position=position, current=0, total=1)
            run_state['active'] = [c for c in run['cells'] if c['conditions']['selector_ref'] == selector_ref
                and all(c['conditions'][k] == v for k, v in batch['matrix_values'].items())]
            conditions = {**run_state['active'][0]['conditions'], 'method': 'selector', 'model': item.get('model', {}).get('architecture')}
            with audit.entry('selection', conditions) as fact, audit.phase('selector_access'):
                model, checkpoints, observation = None, [], None
                if exact is not None:
                    resolved, loaded = exact.selection(run_state['active'], item,
                        store_root=store_root, data=data, inputs=inputs)
                    reference = dict(resolved['selection']['artifact'])
                else:
                    if 'model' in item:
                        with audit.phase('model_prepare'):
                            model, checkpoints, observation = prepared.get(item, data=data, dataset_name=inputs.dataset_name,
                            checkpoint_root=checkpoint_root, device=device, reference_directory=directory,
                            **({'fail_if_training':True} if reference_only or item['method'] == 'overlap_profile_r_point' else {}))
                    if item['method'] in IM_METHODS:
                        from experiments.modular_im import resolve_im
                        from experiments.modular_rr import resolve_rr
                        resolver = resolve_im if item['method'] == 'im' else resolve_rr
                        resolved = resolver(item, store_root=store_root, data=data, inputs=inputs)
                    else:
                        resolved = resolve_methods(store_root=store_root, data=data, dataset_name=inputs.dataset_name,
                            model=model, checkpoints=checkpoints, selectors=[item], include_scores=config.get('return_scores',False),
                            model_config=item.get('model'), training=item.get('training'),
                            fail_if_score_called=reference_only, fail_if_selection_called=reference_only,
                            dataset_inputs=inputs,dataset_identity=datasets[batch['matrix_values']['dataset_index']]['data_identity'])[item['method']]
                    reference = {key: resolved['selection']['artifact'][key] for key in ('artifact_id', 'recipe_hash', 'content_hash')}
                    loaded = verified_selection(reference, store_root=store_root, data=data, inputs=inputs,
                        expected_selector=item['method'], expected_k=resolved['selection']['artifact_k'],
                        expected_parameters=item['parameters'] if item['method'] in IM_METHODS else None)
                selection = selection_prefix(loaded, item['budget']['k'])
                summary['selectors'].append({**resolved, 'checkpoint': observation, 'matrix_values': batch['matrix_values'],
                    'selector_ref': selector_ref, 'requested_k': item['budget']['k'],
                    'configuration_sources': batch['configuration_sources']['selectors'][batch['selector_refs'].index(selector_ref)]})
                if config.get('return_scores'):
                    from experiments.modular_artifacts import existing_scores
                    arrays, semantics = existing_scores(resolved, inputs.candidate_nodes)
                    summary['selectors'][-1].update(result_scores=arrays, score_semantics=semantics)
                fact['cache'] = [cache_fact('selection', reference, resolved['selection']['cache']['hit'])]
                fact['metrics'] = {'selected_node_count': item['budget']['k']}
            summary['selectors'][-1]['access_timing'] = fact['timing']
            run_state['active'] = []
            notify_event(notify, 'progress', position=position, current=1, total=1)
            if config['stage'] == 'unlearning':
                from experiments.modular_gu import run_unlearning
                request_rows = []
                loaded_outputs = {}  # Bounded to this request; share exact Retrain payloads across cases/methods.
                for item, gu_ref, _, selector_ref in request_entries(batch, selector_ref):
                    position = request_position('unlearning', batch_index, batch, selector_ref, gu_ref)
                    notify_event(notify, 'progress', position=position, current=0, total=1)
                    run_state['active'] = [c for c in run['cells']
                        if c['conditions']['selector_ref'] == selector_ref and c['conditions']['unlearning_ref'] == gu_ref
                        and all(c['conditions'][k] == v for k, v in batch['matrix_values'].items())]
                    with audit.entry('attack', run_state['active'][0]['conditions']) as fact:
                        model, checkpoint = None, None
                        consumer = run_unlearning
                        if item['method'] == 'MEGU':
                            from experiments.modular_megu import run_megu_unlearning
                            consumer = run_megu_unlearning
                        elif item['method'] == 'GraphEraser':
                            from experiments.modular_shards import run_shard_unlearning
                            consumer = run_shard_unlearning
                        elif item['method'] == 'GraphRevoker':
                            from experiments.modular_graphrevoker import run_graphrevoker_unlearning
                            consumer = run_graphrevoker_unlearning
                        from experiments.observers import observer_specs, ObserverSession
                        from experiments.modular_artifacts import update_run
                        cell = run_state['active'][0]
                        folder = context.output.parent / cell['path']
                        specs = observer_specs(config, item['method'])
                        session = ObserverSession(specs, folder, dict(run_id=context.run_id,
                            experiment_id=config['experiment_id'], cell_id=cell['cell_id'],
                            conditions=cell['conditions'], commit=context.source_git_sha,
                            configuration_fingerprint=plan['configuration_fingerprint'])) if specs else None
                        policy = config.get('execution', {}).get('gu_cache', {}).get(item['method'], 'reuse')
                        options = dict(gu_cache=policy, observer=session, output_path=folder/'output.npz') if consumer is run_unlearning else {}
                        error = None
                        result = None
                        try:
                            dataset_input = datasets[batch['matrix_values']['dataset_index']]['input_reference']
                            if policy == 'reuse':
                                with audit.phase('output_access'):
                                    result, checkpoint = outputs.lookup(item, selection=selection,
                                    data=data, dataset_input=dataset_input, dataset_root=dataset_root,
                                    dataset_identity=datasets[batch['matrix_values']['dataset_index']]['data_identity'],
                                    inputs=inputs, observer=session, audit=audit)
                            if result is None:
                                if item['method'] != 'Retrain':
                                    with audit.phase('model_prepare'):
                                        if exact is not None:
                                            model, checkpoint = exact.prepare(cell, item, data=data, inputs=inputs,
                                                dataset_input=dataset_input, store_root=store_root, dataset_root=dataset_root,
                                                device=device, checkpoint_root=checkpoint_root)
                                        else:
                                            model, _, checkpoint = prepared.get(item, data=data, dataset_name=inputs.dataset_name,
                                            checkpoint_root=checkpoint_root, device=device, reference_directory=directory)
                                with audit.phase('method_execution'):
                                    result = consumer(item, selection=selection, model=model, data=data,
                                    dataset_name=inputs.dataset_name, checkpoint=checkpoint, store_root=store_root, runtime_root=runtime_root, dataset_root=dataset_root,
                                    dataset_input=dataset_input, **options)
                        except BaseException as exc:
                            error = exc
                            raise
                        finally:
                            if session is not None:
                                try:
                                    session.finish(error, cache_hit=bool(result and result["hit"]))
                                finally:
                                    cell['observers'] = session.references
                                    for reference in cell['observers']:
                                        cell['files'].update(reference['files'])
                                    update_run(run, context.output)
                        if exact is not None:
                            result['retrain'] = exact.rows[cell['cell_id']]['retrain']
                        result['observer_seconds'] = session.seconds if session else 0.0
                        if 'evaluation_cache' not in result:
                            from experiments.evaluation_cache import persist_single
                            result['evaluation_cache'] = persist_single(result, store_root=store_root,
                                dataset_input=dataset_input, audit=audit)
                        summary['unlearning'].append({**result, 'checkpoint': checkpoint, 'conditions': cell['conditions'],
                            'matrix_values': batch['matrix_values'], 'selector_ref': selector_ref,
                            'unlearning_ref': gu_ref})
                        fact['cache'] = [cache_fact('artifact', result['output'], result['hit'], disabled=policy == 'disabled')]
                        if result['evaluation_cache'] is not None:
                            fact['cache'].append(cache_fact('result', result['evaluation_cache'], result['evaluation_cache']['hit']))
                        fact['metrics'] = {**result['result'], **result['evaluation']['metrics']}
                        fact['metadata_compute_seconds'] = result.get('compute_seconds')
                    summary['unlearning'][-1]['access_timing'] = fact['timing']
                    notify_event(notify, 'progress', position=position, current=1, total=1)
                    row = summary['unlearning'][-1]
                    request_rows.append(row)
                    position = request_position('evaluation', batch_index, batch, selector_ref, gu_ref)
                    total = len(config['evaluations'])
                    if total:
                        notify_event(notify, 'progress', position=position, current=0, total=total)
                    from experiments.modular_config import dataset_binding
                    for evaluation_index, evaluation in enumerate(config['evaluations']):
                        measured = evaluate_modular(evaluation, [row],
                            retrain_rows=[r for r in request_rows if r['target']['method'] == 'Retrain'],
                            loaded_outputs=loaded_outputs, store_root=store_root, data=data,
                            dataset_root=dataset_root, audit=audit)
                        binding = dataset_binding(config, batch['matrix_values']['dataset_index'])
                        group = next((e for e in summary['evaluations']
                            if e['dataset_binding'] == binding and e['effective_config'] == evaluation), None)
                        if group is None:
                            group = {'effective_config': evaluation, 'dataset_binding': binding,
                                     'rows': [], 'not_applicable': []}
                            summary['evaluations'].append(group)
                        group['rows'].extend(measured['rows'])
                        group['not_applicable'].extend(measured['not_applicable'])
                        notify_event(notify, 'progress', position=position, current=evaluation_index + 1, total=total)
                    if item['method'] != 'Retrain':
                        from cache_v2 import canonical_sha256
                        loaded_outputs.pop(canonical_sha256(row['output']), None)
                    run_state['active'] = []
                position = request_position('request_complete', batch_index, batch, selector_ref)
                notify_event(notify, 'progress', position=position, current=0, total=1)
                notify_event(notify, 'progress', position=position, current=1, total=1)
    if config['stage'] == 'unlearning':
        # Keep the established declaration-order result surface, independent of scheduling.
        summary['unlearning'].sort(key=lambda row: declaration_order[(
            json.dumps(row['matrix_values'], sort_keys=True), row['unlearning_ref'], row['selector_ref'])])
        conditions_order = {json.dumps(row['conditions'], sort_keys=True): index
                            for index, row in enumerate(summary['unlearning'])}
        for evaluation in summary['evaluations']:
            for key in ('rows', 'not_applicable'):
                evaluation[key].sort(key=lambda row: conditions_order[json.dumps(row['execution_conditions'], sort_keys=True)])
    summary['selector_producer_called'] = any(item['score']['producer_called'] or item['selection']['cache']['producer_called'] for item in summary['selectors'])
    from experiments.modular_artifacts import export_outputs
    notify_event(notify, 'progress', position={'stage': 'export'}, current=0, total=1)
    with audit.phase('export'):
        export_outputs(summary, config=config, context=context, run=run)
        if exact is not None:
            for cell in run['cells']:
                cell['cache_provenance']['exact_inputs'] = exact.provenance(cell)
            update_run(run, context.output)
    for row in summary['selectors']:
        row.pop('result_scores', None)
    notify_event(notify, 'progress', position={'stage': 'export'}, current=1, total=1)
    summary['execution_timing'] = {'phase_seconds_exclusive': audit.timings, 'audit_seconds': audit.seconds}
    return summary



def execute(path, *, context=None, dry_run=False, notify=None):
    """Run with an optional scalar callback: progress(position,current,total), completed(position)."""
    run_state = {}
    try:
        from experiments.implementation_identity import fingerprint_session
        from experiments.unlearning_outputs import metric_input_session
        from cache_v2 import CacheIndex
        from contextlib import nullcontext
        index = CacheIndex(context.store_root/'index.sqlite') if context and not dry_run else None
        scope = index.read_session() if index and index.database_path.is_file() else nullcontext()
        with fingerprint_session(), metric_input_session(), scope, (index.write_session() if index else nullcontext()):
            result = _execute(path, context=context, dry_run=dry_run, run_state=run_state, notify=notify)
        if not dry_run:
            notify_event(notify, 'completed', position={})
        return result
    except BaseException as exc:
        if 'run' in run_state:
            from experiments.modular_artifacts import update_run
            run = run_state['run']
            run.update(status='failed', error=str(exc)[:1000])
            for cell in run_state.get('active', []):
                cell.update(status='failed', error=str(exc)[:1000])
            update_run(run, context.output)
        if run_state.get('audit'):
            audit = run_state['audit']
            exc.execution_timing = {'phase_seconds_exclusive': audit.timings,
                                    'audit_seconds': audit.seconds}
        raise

