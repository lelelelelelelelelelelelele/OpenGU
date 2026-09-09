"""Result documents, separate from remote computation artifacts."""
from __future__ import annotations

from experiments.im_methods import IM_METHODS

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

import numpy as np

ARTIFACT_NAMES = ('metrics.json', 'selection.json', 'scores.npz')


def existing_scores(resolved, candidate_ids):
    """Project only arrays already produced; IM never becomes a full ranking."""
    if resolved['selection']['strategy'] in IM_METHODS:
        gains = resolved.get('selected_gains')
        if gains is None:
            raise ValueError('IM has no recorded selected gains to return')
        return {'selected_gains': np.asarray(gains)}, 'recorded_selection_step_gains'
    if 'scores' not in resolved or 'ranking' not in resolved:
        raise ValueError('selector has no existing scores/ranking to return')
    return {'candidate_ids': np.asarray(candidate_ids, dtype=np.int64),
            'scores': np.asarray(resolved['scores']),
            'ranking': np.asarray(resolved['ranking'], dtype=np.int64)}, 'candidate_scores_and_node_ranking'


def _slug(value):
    return re.sub(r'[^A-Za-z0-9_.-]+', '-', str(value)).strip('.-')[:60] or 'none'


def planned_cells(config):
    """Shared matrix expansion for execution, declaration and validation."""
    from experiments.modular_config import experiment_batches, selector_entries, unlearning_entries
    cells = []
    if config['stage'] == 'metrics':
        for source in config['output_inputs']:
            run, _ = read_run(Path(config['source_directory']) / source['run'], source['sha256'])
            for cell in run['cells']:
                if cell.get('output') and (cell['conditions']['method'] != 'Retrain' or any(
                        e['case'] != 'post_unlearning_utility_and_retrain_gap' for e in config['evaluations'])):
                    cells.append({key: cell[key] for key in ('cell_id', 'path', 'conditions')})
    else:
        for batch in experiment_batches(config):
            entries = (unlearning_entries(batch) if config['stage'] == 'unlearning' else
                       [(None, None, selector, ref) for selector, ref in selector_entries(batch)])
            for gu, gu_ref, selector, selector_ref in entries:
                model = (gu or selector).get('model', {}).get('architecture')
                seed = (gu or selector).get('training', {}).get('seed', selector.get('parameters', {}).get('seed', 0))
                conditions = {**batch['matrix_values'], 'model': model, 'method': gu['method'] if gu else None,
                    'selector': selector['method'], 'selector_ref': selector_ref, 'unlearning_ref': gu_ref,
                    'seed': seed, 'budget': {k: v for k, v in selector['budget'].items() if k != 'k'}}
                identity = json.dumps(conditions, sort_keys=True, separators=(',', ':'))
                cell_id = hashlib.sha256(identity.encode()).hexdigest()[:20]
                budget = selector['budget']
                coordinate = '{}_{}_{}{}'.format(_slug(conditions['dataset_name']),
                    _slug(model.replace('OpenGU.', '').replace('Net', '') if model else 'selector'),
                    'r' if budget['mode'] == 'ratio' else 'k', budget['value'])
                method = (gu['method'] + '_' if gu else '') + selector['method']
                cells.append({'cell_id': cell_id, 'path': f'cells/{coordinate}/{_slug(method)}_{cell_id}/seed{seed}',
                              'conditions': conditions})
    if len({c['cell_id'] for c in cells}) != len(cells):
        raise ValueError('duplicate result cell identity')
    return cells


def output_paths(run_path, config):
    names = ['selection.json'] if config['stage'] == 'selector' else ['metrics.json', 'selection.json']
    if config.get('return_scores'):
        names.append('scores.npz')
    return tuple((Path(run_path).parent / cell['path'] / name).as_posix()
                 for cell in planned_cells(config) for name in names)


def generated_paths(summary, context):
    run = json.loads(context.output.read_text(encoding='utf-8'))
    base = context.store_root.parent.parent
    return [context.output.relative_to(base).as_posix()] + [
        (context.output.parent / c['path'] / name).relative_to(base).as_posix()
        for c in run['cells'] for name in c['files']]


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


def start_run(config, context, config_path):
    config_relative = Path(config_path).resolve().relative_to(context.store_root.parent.parent).as_posix()
    run = {'experiment_id': config['experiment_id'], 'run_id': context.run_id,
        'generated_at': datetime.now(timezone.utc).isoformat(), 'commit': context.source_git_sha,
        'config_path': config_relative, 'stage': config['stage'], 'status': 'pending',
        'cells': [{**cell, 'status': 'pending', 'files': {},
                   'results': {'metrics': 'not_applicable' if config['stage'] == 'selector' else 'pending',
                               'selection': 'pending',
                               'scores': 'pending' if config.get('return_scores') else 'not_requested'}}
                  for cell in planned_cells(config)]}
    _write(context.output, run)
    return run


def update_run(run, output):
    """Only the current invocation's progress document is mutable."""
    temp = output.with_suffix('.tmp')
    temp.write_text(json.dumps(run, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    temp.replace(output)


def export_outputs(summary, *, config, context, run):
    """Serialize measured values and actual requested selections, never payload bytes."""
    rows = summary['unlearning'] if config['stage'] == 'unlearning' else summary['selectors']
    if config['stage'] == 'metrics':
        rows = [summary['metric_sources'][c['cell_id']] for c in run['cells']]
    if len(rows) != len(run['cells']):
        raise ValueError('execution rows differ from planned result cells')
    for cell, row in zip(run['cells'], rows):
        folder = context.output.parent / cell['path']
        documents = {}
        if config['stage'] == 'metrics':
            selected = row['selection_document']
            cell['source'] = row['source']
            documents['selection.json'] = {**selected, 'cell_id': cell['cell_id']}
            selection_id = selected['selection_id']
            cell['timing'] = {'method_compute_seconds': None}
            cell['cache'] = {'method': 'hit'}
            cell['producer_called'] = {'method': False}
        else:
            selected = row if config['stage'] == 'selector' else next(s for s in summary['selectors']
                if s['matrix_values'] == row['matrix_values'] and s['selector_ref'] == row['selector_ref'])
            selection = selected['selection']
            k = selected['requested_k']
            nodes = selection['views'][str(k)]['selected_nodes']
            selection_id = selection['artifact']['artifact_id']
            documents['selection.json'] = {'cell_id': cell['cell_id'], 'selection_id': selection_id,
                'requested_k': k, 'selected_nodes': nodes}
            if cell['conditions']['selector'] in IM_METHODS:
                documents['selection.json'].update(
                    im_selector_seed=cell['conditions']['im_selector_seed'],
                    training_seed=cell['conditions']['seed'] if cell['conditions']['method'] else None,
                    selection_reference={key: selection['artifact'][key]
                        for key in ('artifact_id', 'recipe_hash', 'content_hash')},
                    selector_seed_source=selected['configuration_sources']['parameters.im_selector_seed'])
            cell['timing'] = {'selection_seconds': selected.get('selection_seconds'),
                'score_access_seconds': selected['score'].get('access_seconds'),
                'method_compute_seconds': row.get('compute_seconds')}
            cell['cache'] = {'score': ('not_applicable' if selected['score']['hit'] is None else
                          'hit' if selected['score']['hit'] else 'miss'),
                'selection': 'hit' if selection['cache']['hit'] else 'miss',
                'method': ('hit' if row['hit'] else 'miss') if config['stage'] == 'unlearning' else 'not_applicable'}
            for name, checkpoint in (('selector_checkpoint', selected.get('checkpoint')),
                    ('method_checkpoint', row.get('checkpoint') if config['stage'] == 'unlearning' else None)):
                cell['cache'][name] = ('hit' if checkpoint['hit'] else 'miss') if checkpoint else 'not_applicable'
            cell['producer_called'] = {'score': selected['score']['producer_called'],
                'selection': selection['cache']['producer_called'], 'method': row.get('producer_called')}
        cell['selection_id'] = selection_id
        if config['stage'] != 'selector':
            cell['output'] = row['output']
            measurements = []
            if config['stage'] == 'unlearning':
                measurements = [{'stage': 'method', 'values': row['evaluation']['metrics']},
                                {'stage': 'utility', 'values': row['result']}]
            for evaluation in summary['evaluations']:
                for measured in evaluation['rows']:
                    if measured['identity']['unlearning_output'] == row['output']:
                        item = {'stage': evaluation['effective_config']['case'], 'values': measured['metrics']}
                        if 'retrain_output' in measured['identity']:
                            item['baseline_output'] = measured['identity']['retrain_output']
                        measurements.append(item)
            if not measurements:
                raise ValueError('metrics cell has no applicable measurements')
            documents = {'metrics.json': {'cell_id': cell['cell_id'], 'rows': measurements}, **documents}
        for name, document in documents.items():
            _write(folder / name, document)
            cell['results'][name.split('.')[0]] = 'completed'
        if config.get('return_scores'):
            arrays = selected.get('result_scores')
            if not arrays:
                raise ValueError('requested scores have no existing result arrays')
            with (folder / 'scores.npz').open('xb') as handle:
                np.savez_compressed(handle, **arrays)
            documents['scores.npz'] = None
            cell['scores'] = {'keys': list(arrays), 'selector_ref': cell['conditions']['selector_ref'],
                              'semantics': selected['score_semantics']}
            cell['results']['scores'] = 'completed'
        cell['files'] = {name: {'sha256': hashlib.sha256((folder / name).read_bytes()).hexdigest()}
                         for name in documents}
        cell['status'] = 'completed'
        update_run(run, context.output)
    run['status'] = 'completed'
    run['generated_at'] = datetime.now(timezone.utc).isoformat()
    update_run(run, context.output)


def safe_path(root, value):
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
        raise ValueError('unsafe result path')
    target = (root / value).resolve()
    target.relative_to(root.resolve())
    return target


def read_run(path, expected_sha256):
    """Read a checksum-bound result directory, without any input/cache access."""
    path = Path(path).resolve()
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected_sha256:
        raise ValueError('run checksum mismatch')
    run = json.loads(path.read_text(encoding='utf-8'))
    if set(run) != {'experiment_id', 'run_id', 'generated_at', 'commit', 'config_path', 'stage', 'status', 'cells'}:
        raise ValueError('unexpected run fields')
    if run['status'] != 'completed' or run['stage'] not in ('selector', 'unlearning', 'metrics'):
        raise ValueError('run is not completed')
    seen = set()
    documents = []
    for cell in run['cells']:
        if set(cell) - {'cell_id', 'path', 'conditions', 'status', 'files', 'results', 'output',
                        'selection_id', 'timing', 'cache', 'producer_called', 'scores', 'source'}:
            raise ValueError('unexpected cell fields')
        if cell['status'] != 'completed' or cell['cell_id'] in seen or cell['path'] in seen:
            raise ValueError('duplicate or incomplete result cell')
        seen.update((cell['cell_id'], cell['path']))
        folder = safe_path(path.parent, cell['path'])
        required = {'selection.json'}
        for name in ('metrics', 'scores'):
            if cell['results'][name] == 'completed':
                required.add(name + ('.npz' if name == 'scores' else '.json'))
        if set(cell['files']) != required or required - set(ARTIFACT_NAMES):
            raise ValueError('result file declaration mismatch')
        values = {}
        for name, item in cell['files'].items():
            target = folder / name
            if hashlib.sha256(target.read_bytes()).hexdigest() != item['sha256']:
                raise ValueError('result checksum mismatch: ' + name)
            if name == 'scores.npz':
                with np.load(target, allow_pickle=False) as arrays:
                    if set(arrays.files) != set(cell['scores']['keys']):
                        raise ValueError('score keys differ from declaration')
                    values[name] = {key: arrays[key].copy() for key in arrays.files}
            else:
                value = json.loads(target.read_text(encoding='utf-8'))
                if value['cell_id'] != cell['cell_id']:
                    raise ValueError('result cell ownership mismatch')
                values[name] = value
        selection = values['selection.json']
        nodes = selection['selected_nodes']
        if (selection['selection_id'] != cell['selection_id'] or type(selection['requested_k']) is not int
                or selection['requested_k'] != len(nodes) or not nodes or len(set(nodes)) != len(nodes)
                or any(type(n) is not int or n < 0 for n in nodes)):
            raise ValueError('invalid actual selection')
        if 'metrics.json' in values:
            if set(values['metrics.json']) != {'cell_id', 'rows'} or not values['metrics.json']['rows']:
                raise ValueError('invalid metrics document')
            for row in values['metrics.json']['rows']:
                if (set(row) - {'stage', 'values', 'baseline_output'} or not row['values']
                        or any(isinstance(v, (dict, list, bool)) or (isinstance(v, float) and not math.isfinite(v))
                               for v in row['values'].values())):
                    raise ValueError('metrics must contain scalar measurements')
                for key, value in row['values'].items():
                    if key.endswith('_status'):
                        if not isinstance(value, str):
                            raise ValueError('metric status must be text')
                    elif value is not None and type(value) not in (float, int):
                        raise ValueError('metric value must be numeric or null')
        selection_fields = {'cell_id', 'selection_id', 'requested_k', 'selected_nodes'}
        if cell['conditions']['selector'] in IM_METHODS:
            selection_fields |= {'im_selector_seed', 'training_seed', 'selection_reference',
                                 'selector_seed_source'}
            reference = selection.get('selection_reference', {})
            im_seed = selection.get('im_selector_seed')
            training_seed = cell['conditions']['seed'] if cell['conditions']['method'] else None
            if (type(im_seed) is not int or im_seed != cell['conditions']['im_selector_seed']
                    or selection.get('training_seed') != training_seed
                    or set(reference) != {'artifact_id', 'recipe_hash', 'content_hash'}
                    or reference.get('artifact_id') != cell['selection_id']
                    or any(not re.fullmatch('[0-9a-f]{64}', reference.get(key, ''))
                           for key in ('recipe_hash', 'content_hash'))
                    or not isinstance(selection.get('selector_seed_source'), str)
                    or not selection['selector_seed_source']):
                raise ValueError('IM seed or Selection reference mismatch')
        if set(selection) != selection_fields:
            raise ValueError('unexpected selection fields')
        if 'scores.npz' in values:
            arrays = values['scores.npz']
            im = cell['conditions']['selector'] in IM_METHODS
            allowed = {'selected_gains'} if im else {'candidate_ids', 'scores', 'ranking'}
            if set(arrays) != allowed or any(a.ndim != 1 or not np.isfinite(a).all() for a in arrays.values()):
                raise ValueError('invalid result score arrays')
            if im:
                if len(arrays['selected_gains']) != len(nodes):
                    raise ValueError('IM gains must describe only the requested selection steps')
            else:
                candidates, scores, ranking = (arrays[k] for k in ('candidate_ids', 'scores', 'ranking'))
                if (not np.issubdtype(candidates.dtype, np.integer) or not np.issubdtype(ranking.dtype, np.integer)
                        or len(candidates) != len(scores) or len(set(candidates)) != len(candidates)
                        or sorted(candidates.tolist()) != sorted(ranking.tolist())
                        or ranking[:len(nodes)].tolist() != nodes):
                    raise ValueError('scores/ranking/selection disagree')
        documents.append(values)
    return run, documents
