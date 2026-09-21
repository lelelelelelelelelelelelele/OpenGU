"""065 observations at production events; numerical decisions belong to the consumer."""
import json
import math

import torch
import torch.nn.functional as F

from experiments.effective_config import fields, ConfigurationError


def flat(parameters):
    return torch.cat([p.detach().reshape(-1) for p in parameters])


def magnitude(value):
    return float(value.detach().double().norm())


def scalar(value):
    return value if math.isfinite(value) else None


def relative_difference(actual, expected):
    denominator = magnitude(expected)
    return scalar(magnitude(actual - expected) / denominator) if denominator else None


def curvature_samples(matvec, rhs, seeds, steps):
    """Full reorthogonalization; private RNG, actual production dtype/operator."""
    rows = []
    for seed in seeds:
        generator = torch.Generator(device=rhs.device).manual_seed(seed)
        q = torch.randn(rhs.shape, dtype=rhs.dtype, device=rhs.device, generator=generator)
        q = q / q.norm()
        basis, diagonal, off = [], [], []
        previous, beta = torch.zeros_like(q), 0.
        row = dict(seed=seed, status='finite', dtype=str(rhs.dtype))
        for k in range(min(steps, rhs.numel())):
            basis.append(q)
            z = matvec(q).detach() - beta * previous
            if not torch.isfinite(z).all():
                row.update(status='nonfinite_hvp', step=k)
                break
            alpha = q @ z
            z = z - alpha * q
            for _ in range(2):
                for v in basis:
                    z = z - (v @ z) * v
            diagonal.append(float(alpha))
            beta = magnitude(z)
            if k == min(steps, rhs.numel()) - 1 or beta < torch.finfo(rhs.dtype).eps:
                break
            off.append(beta)
            previous, q = q, z / beta
        if row['status'] == 'finite':
            t = torch.diag(torch.tensor(diagonal, dtype=torch.float64))
            o = torch.tensor(off, dtype=torch.float64)
            t += torch.diag(o, 1) + torch.diag(o, -1)
            values, vectors = torch.linalg.eigh(t)
            row['steps'] = len(diagonal)
            for label, j in [('minimum', 0), ('maximum', -1)]:
                v = sum(float(c) * b for c, b in zip(vectors[:, j], basis))
                eigenvalue = float(values[j])
                row[label] = dict(value=eigenvalue,
                                  ritz_residual=scalar(magnitude(matvec(v).detach() - eigenvalue * v)))
        rows.append(row)
    return rows


class HessianCalibration:
    version = 'hessian-calibration-v1'
    requires = {
        'loss_ready': {'loss', 'loss_reduction', 'model', 'data', 'parameters'},
        'solver_system_ready': {'matvec', 'rhs', 'parameters', 'scale', 'damp', 'iterations'},
        'update_applied': {'parameters', 'expected_parameters', 'update'},
    }
    files = ('calibration.json',)

    def __init__(self, parameters):
        fields(parameters, {'probe_seed', 'lanczos_seeds', 'lanczos_steps'}, (), 'hessian_calibration')
        self.parameters = dict(probe_seed=173, lanczos_seeds=[173, 941], lanczos_steps=80)
        self.parameters.update(parameters)
        p = self.parameters
        if (type(p['probe_seed']) is not int or not isinstance(p['lanczos_seeds'], list)
                or not p['lanczos_seeds'] or any(type(s) is not int for s in p['lanczos_seeds'])
                or type(p['lanczos_steps']) is not int or p['lanczos_steps'] < 1):
            raise ConfigurationError('invalid Hessian observation parameters')
        self.measurements, self.coverage = {}, []

    def __call__(self, event):
        phase, v = event['phase'], event['values']
        if phase not in self.requires:
            return
        self.coverage.append(phase)
        if phase == 'loss_ready':
            model, data, params = v['model'], v['data'], v['parameters']
            self.baseline = flat(params).clone()
            # Independent reconstruction of the 065 declared node-loss semantics.
            with torch.enable_grad():
                output = model.reason_once(data) if event['method'] == 'GIF' else model.forward_once(data, None)
                loss = F.cross_entropy(output[data.train_mask], data.y[data.train_mask], reduction='sum')
                gradient = torch.autograd.grad(loss, params, create_graph=True, retain_graph=True)
            sizes = [p.numel() for p in params]
            def expected(vector):
                pieces = [part.reshape_as(p) for part, p in zip(vector.detach().split(sizes), params)]
                with torch.enable_grad():
                    result = torch.autograd.grad(gradient, params, grad_outputs=pieces, retain_graph=True)
                return flat(result)
            self.expected = expected
            self.measurements['loss'] = dict(reduction=v['loss_reduction'],
                production=scalar(float(v['loss'].detach())), independently_reconstructed=scalar(float(loss.detach())),
                definition='sum cross entropy on train_mask; reason_once for GIF, forward_once for IDEA',
                parameter_shapes=[list(p.shape) for p in params], parameter_count=sum(sizes))
        elif phase == 'solver_system_ready':
            rhs, matvec = v['rhs'], v['matvec']
            generator = torch.Generator(device=rhs.device).manual_seed(self.parameters['probe_seed'])
            probe = torch.randn(rhs.shape, device=rhs.device, dtype=rhs.dtype, generator=generator)
            probe = probe / probe.norm()
            with torch.enable_grad():
                actual = matvec(probe).detach()
                repeated = matvec(probe).detach()
                expected = self.expected(probe)
                actual_rhs, expected_rhs = matvec(rhs).detach(), self.expected(rhs)
                self.measurements['hvp'] = dict(
                    probe_seed=self.parameters['probe_seed'], dtype=str(rhs.dtype),
                    probe_relative_error=relative_difference(actual, expected),
                    rhs_relative_error=relative_difference(actual_rhs, expected_rhs),
                    repeat_relative_error=relative_difference(repeated, actual),
                    finite=all(bool(torch.isfinite(x).all()) for x in (actual, expected, actual_rhs, expected_rhs, repeated)),
                    rhs_l2=scalar(magnitude(rhs)))
                self.measurements['curvature'] = curvature_samples(matvec, rhs,
                    self.parameters['lanczos_seeds'], self.parameters['lanczos_steps'])
            self.measurements['system'] = {key: v[key] for key in ('scale', 'damp', 'iterations')}
            # Release the independent autograd graph before the production solve.
            self.expected = None
        else:
            actual, expected = flat(v['parameters']), flat(v['expected_parameters'])
            self.measurements['writeback'] = dict(
                actual_vs_expected_max_abs=scalar(float((actual - expected).abs().max())),
                actual_delta_l2=scalar(magnitude(actual - self.baseline)),
                solver_delta_l2=scalar(magnitude(v['update'])),
                actual_vs_solver_delta_l2=scalar(magnitude(actual - self.baseline - v['update'])),
                finite=bool(torch.isfinite(actual).all()))

    def save(self, folder, metadata):
        (folder/'calibration.json').write_text(json.dumps({**metadata,
            'coverage': self.coverage, 'measurements': self.measurements,
            'limitation': 'Production-dtype finite Ritz observations do not certify the full spectrum. No acceptance thresholds.'},
            indent=2, allow_nan=False), encoding='utf-8')

    @staticmethod
    def read(payload):
        """Consumer-facing interpretation stays with this Observer, never the runtime."""
        return json.loads(payload)
