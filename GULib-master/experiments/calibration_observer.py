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


def compare_runs(observed_path, control_path, *, dataset_root, store_root):
    """Read completed outputs for the 065 integration check; never execute GU."""
    import hashlib
    from pathlib import Path
    import numpy as np
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_output

    def read(path):
        path = Path(path)
        return read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())

    observed, documents = read(observed_path)
    control, _ = read(control_path)
    if observed['commit'] != control['commit']:
        raise ValueError('observer comparison requires the same code commit')
    key = lambda cell: json.dumps(cell['conditions'], sort_keys=True)
    controls = {key(cell): cell for cell in control['cells']}
    if len(controls) != len(control['cells']) or set(controls) != {key(c) for c in observed['cells']}:
        raise ValueError('observer/control condition sets differ')
    pairs = []
    for cell, document in zip(observed['cells'], documents):
        if not cell.get('observers'):
            continue
        baseline = controls[key(cell)]
        if (cell['selection_id'] != baseline['selection_id']
                or cell['output']['recipe_hash'] != baseline['output']['recipe_hash']):
            raise ValueError('observer/control calculation identities differ')
        actual = load_output(cell['output'], store_root, dataset_root=dataset_root)
        expected = load_output(baseline['output'], store_root, dataset_root=dataset_root)
        same_state = (set(actual.state) == set(expected.state) and
                      all(np.array_equal(actual.state[k], expected.state[k]) for k in actual.state))
        same_logits = np.array_equal(actual.arrays['logits'], expected.arrays['logits'])
        calibration = HessianCalibration.read(document['observers/hessian_calibration/calibration.json'])
        trace = [json.loads(line) for line in document['observers/linear_solver_trace/trace.jsonl'].splitlines()]
        pairs.append(dict(conditions=cell['conditions'], state_equal=same_state, logits_equal=same_logits,
            observer_coverage=calibration['coverage'], calibration=calibration['measurements'],
            final_solver_observation=trace[-1], observed_steps=len(trace)))
    return dict(schema='aagu065.observer_integration.v1', commit=observed['commit'],
        observed_run_id=observed['run_id'], control_run_id=control['run_id'], pairs=pairs,
        production_unchanged=bool(pairs) and all(row['state_equal'] and row['logits_equal'] for row in pairs),
        scope='Observer integration and noninterference; no scientific acceptance decision')


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description='Read-only AAGU-065 Observer/control comparison')
    parser.add_argument('--observed', type=Path, required=True)
    parser.add_argument('--control', type=Path, required=True)
    parser.add_argument('--dataset-root', type=Path, required=True)
    parser.add_argument('--store-root', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(compare_runs(args.observed, args.control, dataset_root=args.dataset_root,
                                  store_root=args.store_root), indent=2, allow_nan=False))
