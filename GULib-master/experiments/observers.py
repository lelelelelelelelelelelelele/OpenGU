"""Explicit observational capabilities. Callbacks must not mutate supplied state."""
from __future__ import annotations

import hashlib
import json
import math
import time
from pathlib import Path

import torch

from experiments.effective_config import ConfigurationError, fields


SOLVER_FIELDS = {'update', 'rhs', 'matvec', 'curvature', 'scale', 'damp', 'iterations'}
CAPABILITIES = {method: {
    'unlearning_start': {'model', 'graphs'}, 'unlearning_end': {'model', 'graphs'},
    'solver_step': SOLVER_FIELDS,
} for method in ('GIF', 'IDEA')}


def norm(value):
    return float(torch.linalg.vector_norm(value.detach().double()))


class LinearSolverTrace:
    version = 'linear-solver-trace-v1'
    requires = {'solver_step': SOLVER_FIELDS}
    files = ('result.json', 'trace.jsonl')

    def __init__(self, parameters):
        defaults = dict(every_n_steps=1, include_initial=True, residuals=['original', 'shifted'],
                        record=['update_l2', 'rhs_l2', 'finite'], zero_denominator='explicit_status')
        fields(parameters, set(defaults), (), 'linear_solver_trace')
        self.parameters = {**defaults, **parameters}
        p = self.parameters
        if (type(p['every_n_steps']) is not int or p['every_n_steps'] < 1
                or type(p['include_initial']) is not bool
                or any(p[k] != defaults[k] for k in ('residuals', 'record', 'zero_denominator'))):
            raise ConfigurationError('unsupported linear_solver_trace parameters')
        self.rows = []

    def __call__(self, event):
        if event['phase'] != 'solver_step':
            return
        step, v = event['step'], event['values']
        if (step == 0 and not self.parameters['include_initial']) or (
                step != v['iterations'] and step % self.parameters['every_n_steps']):
            return
        update, rhs = v['update'].detach(), v['rhs'].detach()
        curvature = v['curvature']
        if curvature is None:
            with torch.enable_grad():
                curvature = v['matvec'](update).detach()
        original = curvature - rhs
        shifted = original + v['scale'] * v['damp'] * update
        denominator = norm(rhs)
        finite = all(bool(torch.isfinite(x).all()) for x in (update, original, shifted))
        self.rows.append(dict(step=step, update_l2=norm(update) if finite else None,
            rhs_l2=denominator, finite=finite, dtype=str(update.dtype),
            scale=v['scale'], damp=v['damp'], shift=v['scale']*v['damp'],
            original_absolute_residual=norm(original) if finite else None,
            shifted_absolute_residual=norm(shifted) if finite else None,
            original_relative_residual=norm(original)/denominator if denominator and finite else None,
            shifted_relative_residual=norm(shifted)/denominator if denominator and finite else None,
            denominator_status='nonzero' if denominator else 'zero_rhs_undefined_relative'))

    def save(self, folder, metadata):
        if metadata['status'] == 'completed' and not self.rows:
            raise ValueError('solver observer has no requested coverage')
        trace = folder / 'trace.jsonl'
        trace.write_text(''.join(json.dumps(r, allow_nan=False)+'\n' for r in self.rows), encoding='utf-8')
        result = {**metadata, 'coverage': [r['step'] for r in self.rows],
                  'step_semantics': 'initial delta=rhs/scale at 0; completed recurrence at step t',
                  'budget_norms': {str(r['step']): r['update_l2'] for r in self.rows if r['step'] in (100, 200, 400)},
                  'interpretation': 'shifted residual is numerical accuracy, not original-system or forgetting proof'}
        (folder/'result.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


class SameGraphChange:
    version = 'same-graph-change-v1'
    requires = {'unlearning_start': {'model', 'graphs'}, 'unlearning_end': {'model', 'graphs'}}
    files = ('result.json',)

    def __init__(self, parameters):
        defaults = dict(graphs=['original', 'retained'], node_scope='all', utility_mask='test_mask',
            f1_average='micro', record=['parameter_delta_l2', 'parameter_delta_relative_l2',
            'logits_delta_l2', 'logits_delta_max_abs', 'prediction_flip_rate', 'accuracy', 'f1'])
        fields(parameters, set(defaults), (), 'same_graph_change')
        self.parameters = {**defaults, **parameters}
        if self.parameters != defaults:
            raise ConfigurationError('unsupported same_graph_change parameters')
        self.before = None
        self.result = {}

    def snapshot(self, model, graphs):
        # Restore every submodule's mode, including mixed train/eval models.
        modes = [(module, module.training) for module in model.modules()]
        try:
            model.eval()
            with torch.no_grad():
                return (torch.cat([p.detach().flatten() for p in model.parameters()]).clone(),
                        {name: model(g.x, g.edge_index).detach().clone() for name, g in graphs.items()})
        finally:
            for module, mode in modes:
                module.training = mode

    def __call__(self, event):
        if event['phase'] not in self.requires:
            return
        v = event['values']
        state, logits = self.snapshot(v['model'], v['graphs'])
        if event['phase'] == 'unlearning_start':
            self.before = state, logits
            return
        if self.before is None:
            raise ValueError('same_graph_change missing start')
        baseline, before = self.before
        size = norm(baseline)
        self.result = dict(parameter_delta_l2=norm(state-baseline),
            parameter_delta_relative_l2=norm(state-baseline)/size if size else None, graphs={})
        for name, graph in v['graphs'].items():
            old, new = before[name], logits[name]
            mask = graph.test_mask
            if not bool(mask.any()):
                raise ValueError('same_graph_change requires nonempty test_mask')
            accuracy = float((new[mask].argmax(1) == graph.y[mask]).float().mean())
            baseline_accuracy = float((old[mask].argmax(1) == graph.y[mask]).float().mean())
            self.result['graphs'][name] = dict(logits_delta_l2=norm(new-old),
                logits_delta_max_abs=float((new-old).abs().max()),
                prediction_flip_rate=float((new.argmax(1) != old.argmax(1)).float().mean()),
                accuracy=accuracy, f1=accuracy, baseline_accuracy=baseline_accuracy, baseline_f1=baseline_accuracy)

    def save(self, folder, metadata):
        if metadata['status'] == 'completed' and not self.result:
            raise ValueError('same_graph_change missing end coverage')
        (folder/'result.json').write_text(json.dumps({**metadata, 'measurements': self.result,
            'coverage': ['unlearning_start', 'unlearning_end'] if self.result else ['unlearning_start'] if self.before else [],
            'comparison': 'GU(graph) versus PT(same graph); all-node logits; test-mask single-label micro F1'},
            indent=2, allow_nan=False), encoding='utf-8')


OBSERVERS = {'linear_solver_trace': LinearSolverTrace, 'same_graph_change': SameGraphChange}


def resolve_observer(value):
    fields(value, {'kind', 'schema_version', 'name', 'parameters'}, {'kind', 'schema_version', 'name'}, 'observer')
    if value['name'] not in OBSERVERS:
        raise ConfigurationError('unknown observer: ' + str(value['name']))
    instance = OBSERVERS[value['name']](value.get('parameters', {}))
    return {**value, 'parameters': instance.parameters}


def validate_capabilities(method, specs, cache_policy):
    if cache_policy not in ('disabled', 'reuse'):
        raise ConfigurationError('unknown GU cache policy')
    if cache_policy == 'disabled' and method not in ('GIF', 'IDEA', 'GNNDelete', 'Retrain'):
        raise ConfigurationError('GU cache policy unsupported for ' + method)
    for spec in specs:
        for event, required in OBSERVERS[spec['name']].requires.items():
            if not required <= CAPABILITIES.get(method, {}).get(event, set()):
                raise ConfigurationError(f'{method} does not provide {event} fields required by {spec["name"]}')
        if cache_policy != 'disabled':
            raise ConfigurationError('Observer coverage requires execution.gu_cache disabled: ' + method)


def observer_specs(config, method):
    return [entry['instance'] for entry in config.get('observers', []) if method in entry['methods']]


def observer_files(config, method):
    return [f'observers/{spec["name"]}/{name}' for spec in observer_specs(config, method)
            for name in OBSERVERS[spec['name']].files]


def verify_observer_documents(cell, documents):
    """Validate scalar semantics and actual coverage in addition to file hashes."""
    def finite(value):
        if isinstance(value, dict):
            return all(finite(v) for v in value.values())
        if isinstance(value, list):
            return all(finite(v) for v in value)
        return not isinstance(value, float) or math.isfinite(value)
    for ref in cell.get('observers', []):
        name = ref['name']
        result = documents[f'observers/{name}/result.json']
        implementation = OBSERVERS[name]
        if (result['name'] != name or result['semantic_version'] != implementation.version
                or not finite(result) or len(result['implementation']) != 64):
            raise ValueError('invalid Observer semantics')
        implementation(result['parameters'])
        if name == 'linear_solver_trace':
            trace = documents[f'observers/{name}/trace.jsonl']
            if not trace or not finite(trace) or not all(row['finite'] for row in trace):
                raise ValueError('invalid solver trace')
            steps = [row['step'] for row in trace]
            params = result['identity']['output_identity']['target']['parameters']
            count = params['iteration']
            zero = trace[0]['rhs_l2'] == 0
            expected = [i for i in range(count+1) if (i != 0 or result['parameters']['include_initial'])
                        and (i % result['parameters']['every_n_steps'] == 0 or i == count)]
            if zero:
                expected = [0] if result['parameters']['include_initial'] else []
            if steps != expected or result['coverage'] != steps:
                raise ValueError('solver trace coverage mismatch')
            for row in trace:
                if row['scale'] != params['scale'] or row['damp'] != params['damp']:
                    raise ValueError('solver trace parameters mismatch')
                if zero and any(row[k] is not None for k in ('original_relative_residual', 'shifted_relative_residual')):
                    raise ValueError('zero RHS cannot claim relative residual')
        elif result['coverage'] != ['unlearning_start', 'unlearning_end'] or set(result['measurements']['graphs']) != {'original', 'retained'}:
            raise ValueError('same graph coverage mismatch')


class ObserverSession:
    """Runner-owned lifecycle and timing; implementations own result documents."""
    def __init__(self, specs, folder, identity):
        self.folder, self.identity = Path(folder), identity
        self.items = [(spec, OBSERVERS[spec['name']](spec['parameters'])) for spec in specs]
        self.seconds = 0.0
        self.events = []
        self.references = []

    def __call__(self, event):
        started = time.perf_counter()
        self.events.append({'phase': event['phase'], 'step': event['step']})
        try:
            for spec, observer in self.items:
                if event['phase'] in observer.requires:
                    missing = observer.requires[event['phase']] - set(event['values'])
                    if missing:
                        raise ValueError(f'{spec["name"]}: missing event fields {sorted(missing)}')
                    observer(event)
        finally:
            # Scalar extraction synchronizes CUDA; count all observer compute here.
            self.seconds += time.perf_counter() - started

    def finish(self, error=None):
        from experiments.implementation_identity import implementation_fingerprint
        references = self.references
        save_errors = []
        for spec, observer in self.items:
            folder = self.folder/'observers'/spec['name']
            folder.mkdir(parents=True, exist_ok=False)
            metadata = dict(identity=self.identity, name=spec['name'], semantic_version=observer.version,
                implementation=implementation_fingerprint(type(observer), norm), parameters=spec['parameters'],
                status='failed' if error else 'completed', error=str(error)[:1000] if error else None,
                observer_seconds=self.seconds, timing='total callbacks; scalar CPU extraction synchronizes CUDA',
                events=self.events)
            try:
                observer.save(folder, metadata)
            except BaseException as exc:
                metadata.update(status='failed', error=str(exc))
                (folder/'result.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
                save_errors.append(exc)
            files = {f'observers/{spec["name"]}/{name}': {
                'sha256': hashlib.sha256((folder/name).read_bytes()).hexdigest()} for name in observer.files if (folder/name).is_file()}
            references.append(dict(name=spec['name'], semantic_version=observer.version, status=metadata['status'], files=files))
        if save_errors:
            raise RuntimeError('Observer save failed: ' + '; '.join(map(str, save_errors))) from save_errors[0]
        return references
