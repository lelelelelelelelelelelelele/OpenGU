"""AAGU-065 Cora GIF/IDEA calibration on fixed pure checkpoints.

This entry is deliberately separate from the historical AAGU-059 diagnostic.
It resolves the declared Random request itself, requires an explicit pure
state-dict checkpoint, and records the production recurrence at T/2T/4T for
each declared scale/damp pair.  It does not choose parameters from F1.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import json
from collections import defaultdict
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

NEAR_ZERO_UPDATE_TO_RHS = 1e-6
NEAR_ZERO_LOGITS_MAX_ABS = 1e-8
RESIDUAL_REFERENCE_THRESHOLD = 1e-3


def write(path: Path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def norm(value):
    return float(value.double().norm())


def flat(parts):
    import torch
    return torch.cat([part.reshape(-1) for part in parts])


def method_logits(model, data, method):
    if method == 'GIF':
        return model.reason_once(data)
    return model.forward_once(data, None)


def measured_series(matvec, rhs, iterations, scale, damp):
    """Measure the exact production recurrence without early stopping."""
    import torch

    rhs = rhs.detach()
    denominator = norm(rhs)
    shift = scale * damp
    trace = []
    estimate = rhs.clone()
    last = None
    started = time.perf_counter()
    for step in range(iterations + 1):
        delta = estimate / scale
        if not torch.isfinite(delta).all():
            return None, trace, step, 'nonfinite_estimate', time.perf_counter() - started
        curvature = matvec(delta).detach()
        shifted = curvature + shift * delta - rhs
        original = curvature - rhs
        if not torch.isfinite(curvature).all() or not torch.isfinite(shifted).all():
            return None, trace, step, 'nonfinite_hvp_or_residual', time.perf_counter() - started
        shifted_relative = norm(shifted) / max(denominator, 1e-30)
        original_relative = norm(original) / max(denominator, 1e-30)
        trace.append({
            'iteration': step,
            'relative_residual': shifted_relative,
            'shifted_relative_residual': shifted_relative,
            'original_relative_residual': original_relative,
            'delta_l2': norm(delta),
            'finite': True,
        })
        last = delta.detach()
        if step == iterations:
            break
        curvature_estimate = matvec(estimate).detach()
        if not torch.isfinite(curvature_estimate).all():
            return None, trace, step + 1, 'nonfinite_iteration_hvp', time.perf_counter() - started
        with torch.no_grad():
            estimate = rhs + (1 - damp) * estimate - curvature_estimate / scale
    return last, trace, iterations, 'finite_truncation', time.perf_counter() - started


def _safe_number(value):
    return f'{float(value):g}'.replace('-', 'm').replace('.', 'p')


def comparison_path(output, method, width, scale, damp):
    return output / (
        f'h{width}-{method.lower()}-s{_safe_number(scale)}-'
        f'd{_safe_number(damp)}-budgets.json'
    )


def build_loss(model, data, method):
    import torch.nn.functional as F

    output = method_logits(model, data, method)
    loss = F.cross_entropy(output[data.train_mask], data.y[data.train_mask], reduction='sum')
    definition = (
        'sum_cross_entropy(reason_once(train_mask))'
        if method == 'GIF' else
        'sum_cross_entropy(forward_once_log_softmax(train_mask))'
    )
    return loss, definition


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    sys.argv[:] = sys.argv[:1]

    import torch

    from experiments.modular_config import (
        configuration_fingerprint,
        experiment_batches,
        load_experiment,
        resolve_budget,
    )
    from experiments.modular_artifacts import planned_cells
    from experiments.modular_execution import device_context
    from experiments.modular_model import prepare_model
    from experiments.dataset_inputs import bind_input, resolve_input
    from experiments.modular_run import verified_selection
    from experiments.selection_inputs import make_dataset_selection_inputs
    from experiments.target_direct_v1.method_cache import resolve_methods
    from utils.target_checkpoint import data_identity, sha256_file, state_hash
    from unlearning.unlearning_methods.GIF.solver import GIFNumericalError, solve_gif_system
    from experiments.aagu059_diagnostic import CapturedSystem, capture_system, lanczos

    torch.set_num_threads(2)
    config = load_experiment(args.config)
    if not config['experiment_id'].startswith('aagu065-calibration-h'):
        raise ValueError('unregistered AAGU-065 experiment identity')
    widths = {item['model']['hidden_channels'] for item in config['unlearnings']}
    if len(widths) != 1 or not widths <= {16, 64}:
        raise ValueError('AAGU-065 calibration must bind one hidden width')
    width = next(iter(widths))
    if args.run_id != f"{config['experiment_id']}-v1":
        raise ValueError('run id must match the registered AAGU-065 config')

    context = device_context(
        config['experiment_id'], run_id=args.run_id,
        device_file=ROOT / '.syncmate/device.yaml'
    )
    if subprocess.check_output(
        ['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, text=True
    ).strip():
        raise ValueError('tracked source is dirty')

    output = context.output.parent
    output.mkdir(parents=True, exist_ok=False)
    batches = list(experiment_batches(config))
    if len(batches) != 1 or len(batches[0]['selectors']) != 1:
        raise ValueError('AAGU-065 requires one independent Random request')
    batch = batches[0]
    data_ref = bind_input(batch['dataset'], batch['dataset_directory'], ROOT)
    data = resolve_input(data_ref, ROOT)
    if not (ROOT / data_ref['graph']).resolve().is_relative_to(ROOT / 'data/processed'):
        raise ValueError('formal graph outside canonical processed root')

    selector = batch['selectors'][0]
    selector['budget'] = resolve_budget(selector['budget'], int(data.train_mask.sum()))
    if selector['method'] != 'random':
        raise ValueError('AAGU-065 requires a Random selector')
    random_seed = selector['parameters'].get('seed')
    if not isinstance(random_seed, int):
        raise ValueError('AAGU-065 requires an integer Random selector seed')
    if selector['budget']['k'] != int(0.1 * int(data.train_mask.sum())):
        raise ValueError('AAGU-065 fixes exactly 10% of train_mask')

    store_root = context.store_root
    resolved_selection = resolve_methods(
        store_root=store_root, data=data, dataset_name='cora', model=None,
        checkpoints=[], selectors=[selector]
    )['random']
    selection_reference = {
        key: resolved_selection['selection']['artifact'][key]
        for key in ('artifact_id', 'recipe_hash', 'content_hash')
    }
    inputs = make_dataset_selection_inputs(data, dataset_name='cora')
    selection = verified_selection(
        selection_reference, store_root=store_root, data=data, inputs=inputs,
        expected_selector='random', expected_k=selector['budget']['k']
    )
    nodes = list(selection.selected_nodes)
    if len(nodes) != selector['budget']['k']:
        raise ValueError('verified Random request has an unexpected deletion count')

    cells = planned_cells(config)
    run = {
        'schema': 'aagu065.calibration.v1',
        'experiment_id': config['experiment_id'],
        'run_id': args.run_id,
        'commit': context.source_git_sha,
        'config_path': args.config.as_posix(),
        'configuration_fingerprint': configuration_fingerprint(args.config),
        'status': 'running',
        'contract': {
            'dataset': 'Cora',
            'split': 'persisted OpenGU public fixed split',
            'model': 'OpenGU.GCNNet, two layers',
            'training': {'seed': 42, 'epochs': 3000},
            'selector': {'method': 'random', 'seed': random_seed, 'budget_ratio': 0.1,
                         'requested_k': len(nodes)},
            'residual_reference_threshold': RESIDUAL_REFERENCE_THRESHOLD,
            'near_zero_policy': {
                'update_to_rhs_l2': f'<= {NEAR_ZERO_UPDATE_TO_RHS}',
                'same_graph_logits_max_abs': f'<= {NEAR_ZERO_LOGITS_MAX_ABS}',
            },
            'parameter_rule': 'no F1-based tuning; finite stability and residual evidence only',
        },
        'context': context.receipt(),
        'dataset_input': data_ref,
        'data_identity': data_identity(data),
        'selection': {
            **selection_reference,
            'selected_nodes_sha256': __import__('hashlib').sha256(
                json.dumps(nodes, separators=(',', ':')).encode('utf-8')
            ).hexdigest(),
        },
        'cells': [dict(cell, status='not_executed') for cell in cells],
        'budget_comparisons': [],
    }
    write(context.output, run)

    row_records = []
    started = time.perf_counter()
    for cell, instance in zip(run['cells'], batch['unlearnings']):
        method = instance['method']
        parameters = instance['parameters']
        iteration = parameters['iteration']
        scale = float(parameters['scale'])
        damp = float(parameters['damp'])
        row = {
            'method': method,
            'hidden_channels': width,
            'iteration': iteration,
            'scale': scale,
            'damp': damp,
            'shift': scale * damp,
            'status': 'not_executed',
            'failure_reason': None,
            'parameter_source': 'AAGU-065 YAML candidate; author values retained as comparison',
        }
        cell_start = time.perf_counter()
        filename = (
            f'h{width}-{method.lower()}-s{_safe_number(scale)}-'
            f'd{_safe_number(damp)}-t{iteration}.json'
        )
        try:
            if parameters.get('gaussian_std', 0.0) != 0.0 or parameters.get('gaussian_mean', 0.0) != 0.0:
                raise ValueError('AAGU-065 requires zero IDEA noise')
            model_data = data.clone().to(context.request_device)
            working = data.clone().to(context.request_device)
            working.num_classes = int(data.y.max()) + 1
            for split in ('train', 'val', 'test'):
                setattr(
                    working, split + '_indices',
                    getattr(working, split + '_mask').nonzero().flatten().cpu().numpy()
                )
            model, _, checkpoint = prepare_model(
                copy.deepcopy(instance), data=model_data, dataset_name='Cora',
                checkpoint_root=context.checkpoint_root, device=context.request_device,
                reference_directory=args.config.parent
            )
            if checkpoint.get('source') != 'external_state_dict':
                raise ValueError('AAGU-065 requires explicit PT and forbids training-cache fallback')
            row['checkpoint'] = checkpoint
            model.eval()
            saved_state_hash = state_hash(model.state_dict())
            saved_file_hash = sha256_file(checkpoint['path'])
            before_logits = method_logits(model, working, method).detach().clone()
            if not torch.isfinite(before_logits).all():
                raise ValueError('nonfinite original logits')

            captured = capture_system(instance, model, working, nodes, output)
            matvec, rhs = captured['matvec'], captured['rhs']
            model_params = [p for p in model.parameters() if p.requires_grad]
            sizes = [p.numel() for p in model_params]
            loss, loss_definition = build_loss(model, working, method)
            gradient = torch.autograd.grad(
                loss, model_params, create_graph=True, retain_graph=True
            )

            def expected(vector):
                outputs = [part.reshape_as(param) for part, param in zip(
                    vector.detach().split(sizes), model_params
                )]
                values = torch.autograd.grad(
                    gradient, model_params, grad_outputs=outputs,
                    retain_graph=True, allow_unused=False
                )
                return flat(values).detach()

            torch.manual_seed(173)
            probe = torch.randn_like(rhs)
            probe /= probe.norm()
            expected_probe = expected(probe)
            actual_probe = matvec(probe).detach()
            actual_probe_repeat = matvec(probe).detach()
            expected_rhs = expected(rhs)
            actual_rhs = matvec(rhs).detach()
            hvp_check = {
                'loss_definition': loss_definition,
                'parameter_count': sum(sizes),
                'random_probe_relative_error': norm(actual_probe - expected_probe) / max(norm(expected_probe), 1e-30),
                'rhs_relative_error': norm(actual_rhs - expected_rhs) / max(norm(expected_rhs), 1e-30),
                'repeat_relative_error': norm(actual_probe - actual_probe_repeat) / max(norm(expected_probe), 1e-30),
            }
            row['hvp_check'] = hvp_check
            if max(v for key, v in hvp_check.items() if key.endswith('error')) > 1e-5:
                raise ValueError('actual production HVP differs from declared sum-loss Hessian')

            curvature_name = f'h{width}-{method.lower()}-curvature.json'
            curvature_path = output / curvature_name
            if not curvature_path.exists():
                double_model = copy.deepcopy(model).double().eval()
                double_data = working.clone()
                double_data.x = double_data.x.double()
                double_system = capture_system(instance, double_model, double_data, nodes, output)
                curvature = lanczos(
                    double_system['matvec'], rhs.numel(), rhs.device, steps=80
                )
                curvature.update(
                    method=method, hidden_channels=width,
                    checkpoint_state_hash=checkpoint['state_hash'],
                    loss_definition=loss_definition,
                    production_scale=scale,
                    production_damp=damp,
                )
                write(curvature_path, curvature)
                del double_system, double_model, double_data
            row['curvature'] = curvature_name

            delta, trace, actual_iterations, status, solver_seconds = measured_series(
                matvec, rhs, iteration, scale, damp
            )
            row.update({
                'status': status,
                'actual_iterations': actual_iterations,
                'finite': delta is not None,
                'trace': trace,
                'solver_seconds': solver_seconds,
                'rhs_l2': norm(rhs),
                'parameters': parameters,
                'effective_parameters': captured['effective_parameters'],
            })
            try:
                production_delta, diagnostics = solve_gif_system(
                    matvec, rhs, iterations=iteration, scale=scale, damp=damp
                )
                if delta is None:
                    raise ValueError('diagnostic recurrence was nonfinite but production solver returned finite')
                recurrence_error = norm(production_delta - delta) / max(norm(delta), 1e-30)
                if recurrence_error > 1e-5:
                    raise ValueError('instrumented recurrence differs from production solver')
                row['production_solver'] = {
                    'check': 'delta_agrees_within_float32_tolerance',
                    'relative_error': recurrence_error,
                    'diagnostics': diagnostics,
                }
            except GIFNumericalError as error:
                if delta is not None:
                    raise ValueError('production solver failed while measured recurrence was finite')
                row['production_solver'] = {
                    'check': 'both_nonfinite', 'diagnostics': error.diagnostics
                }

            if delta is not None:
                before_state = [p.detach().clone() for p in model_params]
                state_l2 = norm(flat(before_state))
                candidate = copy.deepcopy(model).eval()
                candidate_params = [p for p in candidate.parameters() if p.requires_grad]
                pieces = list(delta.split(sizes))
                with torch.no_grad():
                    for param, piece in zip(candidate_params, pieces):
                        param.add_(piece.reshape_as(param))
                writeback_error = max(
                    norm((param.detach() - old) - piece.reshape_as(param))
                    / max(norm(piece), 1e-30)
                    for param, old, piece in zip(candidate_params, before_state, pieces)
                )
                after_logits = method_logits(candidate, working, method).detach()
                logits_difference = after_logits - before_logits
                update_l2 = norm(delta)
                logits_l2 = norm(logits_difference)
                row.update({
                    'delta_l2': update_l2,
                    'state_l2': state_l2,
                    'relative_update_l2': update_l2 / max(state_l2, 1e-30),
                    'writeback_relative_error': writeback_error,
                    'same_graph_logits_l2': logits_l2,
                    'same_graph_logits_max_abs': float(logits_difference.abs().max()),
                    'same_graph_logits_relative_l2': logits_l2 / max(norm(before_logits), 1e-30),
                    'finite_after_writeback': bool(torch.isfinite(after_logits).all()),
                    'near_zero_update': update_l2 / max(norm(rhs), 1e-30) <= NEAR_ZERO_UPDATE_TO_RHS,
                    'near_zero_same_graph_logits': float(logits_difference.abs().max()) <= NEAR_ZERO_LOGITS_MAX_ABS,
                })
                del candidate
            if state_hash(model.state_dict()) != saved_state_hash:
                raise ValueError('original model weights changed during calibration')
            if sha256_file(checkpoint['path']) != saved_file_hash:
                raise ValueError('checkpoint file changed during calibration')
            row['original_weights_unchanged'] = True
        except Exception as exc:
            import traceback
            row.update(
                status='diagnostic_error',
                failure_reason=f'{type(exc).__name__}: {exc}',
                error_traceback=traceback.format_exc(),
            )
        row['total_seconds'] = time.perf_counter() - cell_start
        write(output / filename, row)
        cell.update(status=row['status'], diagnostic=filename, sha256=sha256_file(output / filename))
        row_records.append((row, filename))
        write(context.output, run)
        print(
            f'h{width} {method} scale={scale:g} damp={damp:g} T={iteration}: {row["status"]}',
            file=sys.stderr, flush=True
        )

    grouped = defaultdict(list)
    for row, filename in row_records:
        if row['status'] != 'diagnostic_error':
            grouped[(row['method'], row['hidden_channels'], row['scale'], row['damp'])].append((row, filename))
    for (method, group_width, scale, damp), members in grouped.items():
        members.sort(key=lambda pair: pair[0]['iteration'])
        reference = members[0][0]
        reference_delta = reference.get('delta_l2')
        points = {}
        for row, _ in members:
            final_trace = row.get('trace', [])[-1] if row.get('trace') else {}
            delta = row.get('delta_l2')
            points[str(row['iteration'])] = {
                'shifted_relative_residual': final_trace.get('shifted_relative_residual'),
                'original_relative_residual': final_trace.get('original_relative_residual'),
                'delta_l2': delta,
                'delta_relative_to_reference': (
                    norm(torch.tensor([delta - reference_delta], dtype=torch.float64))
                    / max(abs(reference_delta), 1e-30)
                    if delta is not None and reference_delta is not None else None
                ),
                'finite': row.get('finite'),
                'near_zero_update': row.get('near_zero_update'),
            }
        comparison = {
            'method': method,
            'hidden_channels': group_width,
            'scale': scale,
            'damp': damp,
            'shift': scale * damp,
            'reference_iteration': reference['iteration'],
            'points': points,
            'budget_consistency_definition': 'delta relative to the smallest declared T in this parameter group',
        }
        path = comparison_path(output, method, group_width, scale, damp)
        write(path, comparison)
        run['budget_comparisons'].append({
            'method': method, 'hidden_channels': group_width,
            'scale': scale, 'damp': damp,
            'path': path.name, 'sha256': sha256_file(path),
        })
        for row, filename in members:
            row['budget_comparison'] = comparison
            write(output / filename, row)
            for cell in run['cells']:
                if cell.get('diagnostic') == filename:
                    cell['sha256'] = sha256_file(output / filename)

    if subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() != context.source_git_sha:
        raise ValueError('source changed during execution')
    run.update(
        status=(
            'diagnostic_complete'
            if all(cell['status'] != 'diagnostic_error' and cell['status'] != 'not_executed' for cell in run['cells'])
            else 'failed'
        ),
        total_seconds=time.perf_counter() - started,
        calibration_scope='fixed Cora PT; author and declared shifted candidates; no F1 selection',
    )
    write(context.output, run)
    paths = [str(path.relative_to(ROOT)).replace('\\', '/') for path in output.glob('*.json')]
    return {'passed': run['status'] == 'diagnostic_complete', 'generated_artifacts': sorted(paths)}


if __name__ == '__main__':
    with contextlib.redirect_stdout(sys.stderr):
        result = main()
    print(json.dumps(result))
