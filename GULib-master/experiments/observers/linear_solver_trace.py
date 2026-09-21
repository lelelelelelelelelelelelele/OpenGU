"""Observe solver residuals and update norms at iteration events."""
import json

import torch

from experiments.effective_config import ConfigurationError, fields


def norm(value):
    return float(torch.linalg.vector_norm(value.detach().double()))


class LinearSolverTrace:
    version = 'linear-solver-trace-v1'
    requires = {'solver_step': {'update', 'rhs', 'matvec', 'curvature', 'scale', 'damp', 'iterations'}}
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


