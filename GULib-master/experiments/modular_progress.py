"""Optional batch progress: scalar positions, independent of transport and Cache."""
from __future__ import annotations

import sys

from experiments.modular_config import experiment_batches, selector_entries, unlearning_entries


def execution_batches(config, *, batches=None):
    """Use the same stable, larger-budget-first order in execution and progress."""
    return sorted(experiment_batches(config) if batches is None else batches,
                  key=lambda batch: -(batch['matrix_values']['budget_ratio'] or 0))


def batch_position(stage, index, batch):
    return {'stage': stage, 'batch_index': index,
            'dataset_index': batch['matrix_values']['dataset_index']}


def request_entries(batch, selector_ref):
    """One declared request, with existing Retrain dependencies first."""
    return sorted((entry for entry in unlearning_entries(batch) if entry[3] == selector_ref),
                  key=lambda entry: entry[0]['method'] != 'Retrain')


def request_position(stage, index, batch, selector_ref, gu_ref=None):
    position = {**batch_position(stage, index, batch), 'selector_ref': selector_ref}
    if gu_ref is not None:
        position['unlearning_ref'] = gu_ref
    return position


def progress_steps(config):
    """Declare actual invocation boundaries, never epochs or per-cell tree nodes."""
    steps = []
    for index, dataset in enumerate(config['datasets']):
        name = dataset['dataset']['name']
        steps.append({'position': {'stage': 'data', 'dataset_index': index},
                      'label': 'Data: ' + name, 'total': 1})
    if config['stage'] == 'metrics':
        steps.append({'position': {'stage': 'metric_inputs'},
                      'label': 'Read metric inputs', 'total': len(config['output_inputs'])})
    else:
        for index, batch in enumerate(execution_batches(config)):
            values = batch['matrix_values']
            label = '{} / batch {}'.format(values['dataset_name'], index + 1)
            if values['training_seed'] is not None:
                label += ' / seed ' + str(values['training_seed'])
            if values['budget_ratio'] is not None:
                label += ' / ratio ' + str(values['budget_ratio'])
            for field in ('random_selector_seed', 'im_selector_seed'):
                if field in values:
                    label += ' / ' + field + ' ' + str(values[field])
            for selector, selector_ref in selector_entries(batch):
                request_label = label + ' / ' + selector_ref
                steps.append({'position': request_position('selector', index, batch, selector_ref),
                              'label': request_label + ' / Selection', 'total': 1})
                if config['stage'] == 'unlearning':
                    for item, gu_ref, _, _ in request_entries(batch, selector_ref):
                        method_label = request_label + ' / ' + gu_ref
                        steps.append({'position': request_position('unlearning', index, batch, selector_ref, gu_ref),
                                      'label': method_label + ' / Output + own metrics', 'total': 1})
                        if config['evaluations']:
                            steps.append({'position': request_position('evaluation', index, batch, selector_ref, gu_ref),
                                          'label': method_label + ' / Evaluation (Retrain pairs: N/A)' if item['method'] == 'Retrain'
                                                   else method_label + ' / Evaluation',
                                          'total': len(config['evaluations'])})
                    steps.append({'position': request_position('request_complete', index, batch, selector_ref),
                                  'label': request_label + ' / Complete result', 'total': 1})
    if config['stage'] == 'metrics' and config['evaluations']:
        for index, dataset in enumerate(config['datasets']):
            steps.append({'position': {'stage': 'evaluation', 'dataset_index': index},
                          'label': 'Evaluation: ' + dataset['dataset']['name'],
                          'total': len(config['evaluations'])})
    steps.append({'position': {'stage': 'export'}, 'label': 'Export results', 'total': 1})
    return steps


def notify_event(notify, kind, *, position, current=None, total=None):
    """A broken optional observer cannot replace a scientific result or error."""
    if notify is None:
        return
    values = {'position': dict(position)}
    if kind == 'progress':
        values.update(current=current, total=total)
    try:
        notify(kind, **values)
    except Exception as exc:
        print('Warning: optional progress notification failed: {}: {}'.format(
            type(exc).__name__, exc), file=sys.stderr)
