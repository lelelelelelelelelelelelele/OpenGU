"""Persistent ordinary-executor observations, separate from scientific identity."""
from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter

from scripts.evaluation.reporting.events import (
    cache_observation, make_cell_id, new_run_id, record_event, refresh_status_views,
)


class ExecutionAudit:
    def __init__(self, context, fingerprint, experiment_id):
        self.context = context
        self.experiment_id = experiment_id
        self.fingerprint = fingerprint
        self.journal = context.runtime_root.parent / '_journal'
        self.path = self.journal / 'auto_report.events.jsonl'
        self.seconds = 0.0
        self.last_refresh = 0.0
        self.timings = {}
        self.completed_stages = set()
        self.stack = []

    @contextmanager
    def phase(self, name):
        started = perf_counter()
        frame = [name, 0.0]
        self.stack.append(frame)
        try:
            yield
        finally:
            elapsed = perf_counter() - started
            self.stack.pop()
            self.timings[name] = self.timings.get(name, 0.0) + elapsed - frame[1]
            if self.stack:
                self.stack[-1][1] += elapsed

    def refresh(self, force=False):
        # Every event is fsynced. Projection rebuilding is bounded to once per
        # second and forced at a terminal boundary; there is no epoch journal.
        if force or perf_counter() - self.last_refresh >= 1.0:
            started = perf_counter()
            refresh_status_views(event_path=self.path)
            self.seconds += perf_counter() - started
            self.last_refresh = perf_counter()

    def emit(self, common, state, **values):
        started = perf_counter()
        record_event(state=state, event_path=self.path, refresh=False, **common, **values)
        self.seconds += perf_counter() - started
        first_completion = state == 'completed' and common['stage'] not in self.completed_stages
        if first_completion:
            self.completed_stages.add(common['stage'])
        self.refresh(force=first_completion)

    @contextmanager
    def entry(self, stage, conditions):
        identity = dict(conditions)
        identity.update(experiment_id=self.experiment_id, execution_stage=stage)
        identity['dataset'] = identity.get('dataset_name', identity.get('dataset'))
        identity['model'] = identity.get('model') or 'selector'
        identity['method'] = identity.get('method') or 'selector'
        identity['strategy'] = identity.get('selector', identity.get('strategy'))
        identity['ratio'] = identity.get('ratio') or identity.get('budget_ratio') or identity.get('budget', {}).get('value', 'k')
        cell_id = make_cell_id(identity)
        common = dict(identity=identity, stage=stage, producer='experiments.modular_run',
            config_fingerprint=self.fingerprint, git_sha=self.context.source_git_sha,
            cell_id=cell_id, run_id=new_run_id(cell_id))
        metadata = dict(execution_run_id=self.context.run_id, level=self.context.level)
        self.emit(common, 'started', metadata=metadata)
        started = perf_counter()
        before = dict(self.timings)
        result = {}
        try:
            yield result
        except BaseException as exc:
            self.emit(common, 'failed', error=dict(type=type(exc).__name__, message=str(exc) or type(exc).__name__),
                metadata={**metadata, 'wall_seconds': perf_counter() - started,
                          'phase_seconds_exclusive': {k:v-before.get(k, 0.0) for k,v in self.timings.items()}})
            raise
        else:
            result['timing'] = dict(wall_seconds=perf_counter() - started,
                phase_seconds_exclusive={k:v-before.get(k, 0.0) for k,v in self.timings.items()})
            self.emit(common, 'completed', cache=result.get('cache', []), metrics=result.get('metrics', {}),
                artifacts=result.get('artifacts', []), metadata={**metadata,
                    'wall_seconds': perf_counter() - started,
                    'phase_seconds_exclusive': {k:v-before.get(k, 0.0) for k,v in self.timings.items()},
                    'producer_compute_seconds': result.get('metadata_compute_seconds'),
                    'timing_semantics': 'current access; exclusive phases; unmeasured remainder is not zero'})


def cache_fact(kind, reference, hit, *, disabled=False):
    return cache_observation(cache_type=kind, outcome='bypass' if disabled else 'hit' if hit else 'miss',
        recipe_hash=reference.get('recipe_hash'), artifact=reference,
        hit_source='cache_v2:' + reference.get('artifact_id', 'run') if hit else None,
        lookup_policy='cache_v2_exact_recipe', authoritative=True,
        write_outcome='not_written' if disabled else 'reused' if hit else 'saved')
