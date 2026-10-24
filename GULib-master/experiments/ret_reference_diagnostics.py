"""Explicit source-bound Ret references; source Selection and Original never run."""
from datetime import datetime, timezone
import hashlib
import time

from experiments.retrain_diagnostics import source_inputs
from experiments.ret_reference_training import train_reference
from experiments.observers import ObserverSession, observer_specs
from experiments.modular_artifacts import _write, update_run
from experiments.modular_progress import notify_event
from experiments.implementation_identity import implementation_fingerprint
from experiments.observers.ret_reference import RetReferenceTrace
from experiments.ret_reference_policy import configure_for_experiment, reference_cell


def execute_references(config, context, datasets, loaded_data, summary, run_state, audit, notify):
    run, spec = run_state['run'], config['ret_reference']
    root = context.store_root.parent.parent
    notify_event(notify,'progress',position={'stage':'retrain_inputs'},current=0,total=1)
    with audit.phase('retrain_diagnostic_inputs'):
        ready = source_inputs(config,context,datasets,loaded_data)
    notify_event(notify,'progress',position={'stage':'retrain_inputs'},current=1,total=1)
    entries = [(item,arm,reference_cell(item['cell'],spec,arm)) for item in ready for arm in spec['arms']]
    cells = {c['cell_id']:c for c in run['cells']}
    if set(cells) != {p['cell_id'] for _,_,p in entries}:
        raise ValueError('Ret reference plan differs from source expansion')
    notify_event(notify,'progress',position={'stage':'retrain_diagnostics'},current=0,total=len(entries))
    summary['retrain_diagnostics'] = []
    for item,arm,plan in entries:
        cell = cells[plan['cell_id']]
        run_state['active'] = [cell]
        data, inputs = loaded_data[item['data_index']]
        data = data.clone().to(context.request_device)
        instance = {**item['instance'],'reference':dict(policy=spec['policy'],arm=arm)}
        identity = dict(experiment_id=run['experiment_id'],run_id=run['run_id'],commit=run['commit'],
            cell_id=cell['cell_id'],conditions=cell['conditions'],source=item['source'],
            output_identity=item['output'].identity,configuration_fingerprint=summary['configuration_fingerprint'],
            reference_configuration=instance['reference'],
            producer=dict(semantic_version='ret-source-reference-v1',
                          implementation=implementation_fingerprint(train_reference,execute_references,
                              RetReferenceTrace,configure_for_experiment)))
        folder = context.output.parent/cell['path']
        session = ObserverSession(observer_specs(config,'Retrain'),folder,identity)
        error = None
        started = time.perf_counter()
        try:
            with audit.entry('retrain_diagnostics',cell['conditions']) as fact, audit.phase('retrain_training'):
                _,_,statistics = train_reference(instance,data,item['output'].identity['pairing']['selected_nodes'],
                    inputs.dataset_name,observer=session,
                    asset_root=context.runtime_root/'ret_reference'/cell['cell_id'],dataset_root=root,
                    prior=dict(reference=item['source']['output'],state_hash=item['old_state_hash'],
                               logits=item['output'].arrays['logits']),mode=spec['mode'])
                fact['metrics'] = {'training_epochs':3000*len(statistics)}
        except BaseException as exc:
            error = exc
            raise
        finally:
            session.finish(error=error)
        result = session.items[0][1].result
        endpoint = result['replays'][0]['endpoints']['final']['probes']['original']['test']
        metrics = dict(final_accuracy=endpoint['accuracy'],final_cross_entropy=endpoint['cross_entropy'],
                       repetitions=len(statistics))
        cell.update(source=item['source'],selection_id=item['selection']['selection_id'],
            observers=session.references,cache={'method':'disabled'},
            producer_called={'selection':False,'original':False,'method':True},
            timing={'method_compute_seconds':time.perf_counter()-started,'observer_seconds':session.seconds,
                    'training_seconds_including_epoch_observer':sum(s['training_seconds'] for s in statistics)})
        for name,document in {
            'selection.json':{**item['selection'],'cell_id':cell['cell_id']},
            'metrics.json':{'cell_id':cell['cell_id'],'rows':[{'stage':'ret_reference_trace','values':metrics}]}
        }.items():
            _write(folder/name,document)
            cell['files'][name] = {'sha256':hashlib.sha256((folder/name).read_bytes()).hexdigest()}
            cell['results'][name.split('.')[0]] = 'completed'
        for reference in session.references:
            cell['files'].update(reference['files'])
        cell['status'] = 'completed'
        update_run(run,context.output)
        summary['retrain_diagnostics'].append(dict(cell_id=cell['cell_id'],source=item['source'],metrics=metrics))
        notify_event(notify,'progress',position={'stage':'retrain_diagnostics'},
                     current=len(summary['retrain_diagnostics']),total=len(entries))
    notify_event(notify,'progress',position={'stage':'export'},current=0,total=1)
    run['status'],run['generated_at'] = 'completed',datetime.now(timezone.utc).isoformat()
    update_run(run,context.output)
    notify_event(notify,'progress',position={'stage':'export'},current=1,total=1)
    summary['selector_producer_called'] = False
    summary['execution_timing'] = {'phase_seconds_exclusive':audit.timings,'audit_seconds':audit.seconds}
    return summary
