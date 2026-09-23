"""Observer registry, event dispatch and file lifecycle; no observation analysis."""
from __future__ import annotations

import hashlib
import time
from pathlib import Path, PurePosixPath

from experiments.effective_config import ConfigurationError, fields
from . import linear_solver_trace, same_graph_change, hessian_calibration


SOLVER_FIELDS = {'update', 'rhs', 'matvec', 'curvature', 'scale', 'damp', 'iterations'}
CAPABILITIES = {method: {
    'unlearning_start': {'model', 'graphs'}, 'unlearning_end': {'model', 'graphs'},
    'solver_step': SOLVER_FIELDS,
    'loss_ready': {'loss', 'loss_reduction', 'model', 'data', 'parameters'},
    'solver_system_ready': {'matvec', 'rhs', 'parameters', 'scale', 'damp', 'iterations'},
    'update_applied': {'parameters', 'expected_parameters', 'update'},
} for method in ('GIF', 'IDEA')}


OBSERVERS = {
    'linear_solver_trace': linear_solver_trace.LinearSolverTrace,
    'same_graph_change': same_graph_change.SameGraphChange,
    'hessian_calibration': hessian_calibration.HessianCalibration,
}


def resolve_observer(value):
    fields(value, {'name', 'parameters'}, {'name'}, 'observer')
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
            for name in declared_files(OBSERVERS[spec['name']])]


class ObserverSession:
    """Runner-owned lifecycle and timing; implementations own result documents."""
    def __init__(self, specs, folder, identity):
        self.folder, self.identity = Path(folder), identity
        self.items = [(spec, OBSERVERS[spec['name']](spec['parameters'])) for spec in specs]
        for _, observer in self.items:
            declared_files(observer)
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
                    observer({**event, 'values': {key: event['values'][key]
                                                 for key in observer.requires[event['phase']]}})
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
                implementation=implementation_fingerprint(type(observer)), parameters=spec['parameters'],
                status='failed' if error else 'completed', error=str(error)[:1000] if error else None,
                observer_seconds=self.seconds, timing='total callbacks; scalar CPU extraction synchronizes CUDA',
                events=self.events)
            try:
                observer.save(folder, metadata)
            except BaseException as exc:
                metadata.update(status='failed', error=str(exc))
                save_errors.append(exc)
            files = {f'observers/{spec["name"]}/{name}': {
                'sha256': hashlib.sha256((folder/name).read_bytes()).hexdigest()} for name in observer.files if (folder/name).is_file()}
            references.append(dict(name=spec['name'], semantic_version=observer.version,
                status=metadata['status'], error=metadata['error'], identity=self.identity,
                parameters=spec['parameters'], implementation=metadata['implementation'], files=files))
            if metadata['status'] == 'completed' and len(files) != len(observer.files):
                references[-1]['status'] = 'failed'
                save_errors.append(ValueError('Observer did not save all declared files'))
        if save_errors:
            raise RuntimeError('Observer save failed: ' + '; '.join(map(str, save_errors))) from save_errors[0]
        return references


def declared_files(observer):
    names = observer.files
    if not names or len(set(names)) != len(names):
        raise ConfigurationError('Observer files must be nonempty and unique')
    for name in names:
        if (not isinstance(name, str) or not name or '\\' in name or ':' in name
                or PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts
                or str(PurePosixPath(name)) != name):
            raise ConfigurationError('Observer file must be a normalized relative path')
    return names
