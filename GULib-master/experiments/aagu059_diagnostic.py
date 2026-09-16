"""AAGU-059 diagnostics. Reuse hidden64; prepare one hidden16 model if absent."""
from __future__ import annotations

import argparse
import contextlib
import copy
import json
import importlib
from pathlib import Path
import subprocess
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def norm(x):
    return float(x.double().norm())


def flat(parts):
    import torch
    return torch.cat([p.reshape(-1) for p in parts])


def measured_series(matvec, rhs, iterations, scale, damp):
    """Author recurrence, with per-step observations and no residual stopping."""
    import torch
    h = rhs.detach().clone()
    denominator = norm(rhs)
    trace = []
    last = None
    started = time.perf_counter()
    for step in range(iterations + 1):
        delta = h / scale
        if not torch.isfinite(delta).all():
            return None, trace, step, 'nonfinite_estimate', time.perf_counter()-started
        hd = matvec(delta.detach()).detach()
        residual = hd - rhs
        if not torch.isfinite(hd).all() or not torch.isfinite(residual).all():
            return None, trace, step, 'nonfinite_hvp_or_residual', time.perf_counter()-started
        trace.append(dict(iteration=step, relative_residual=norm(residual)/denominator,
                          delta_l2=norm(delta), finite=True))
        last = delta.detach()
        if step == iterations:
            break
        curvature = matvec(h.detach()).detach()
        if not torch.isfinite(curvature).all():
            return None, trace, step+1, 'nonfinite_iteration_hvp', time.perf_counter()-started
        with torch.no_grad():
            h = rhs + (1-damp)*h - curvature/scale
    return last, trace, iterations, 'finite_truncation', time.perf_counter()-started


def lanczos(mv, size, device, steps=80):
    import torch
    rows = []
    started = time.perf_counter()
    for seed in (173, 941):
        torch.manual_seed(seed)
        q = torch.randn(size, device=device, dtype=torch.float64)
        q /= q.norm()
        basis, diagonal, off = [], [], []
        previous, beta = torch.zeros_like(q), 0.
        for k in range(steps):
            basis.append(q)
            z = mv(q) - beta*previous
            alpha = q @ z
            z -= alpha*q
            for _ in range(2):
                for v in basis:
                    z -= (v @ z)*v
            diagonal.append(float(alpha))
            beta = norm(z)
            if k == steps-1 or beta < 1e-12:
                break
            off.append(beta)
            previous, q = q, z/beta
        t = torch.diag(torch.tensor(diagonal, dtype=torch.float64))
        o = torch.tensor(off, dtype=torch.float64)
        t += torch.diag(o, 1) + torch.diag(o, -1)
        values, vectors = torch.linalg.eigh(t)
        row = dict(seed=seed, steps=len(diagonal))
        for label, j in [('minimum', 0), ('maximum', -1)]:
            v = sum(float(c)*b for c, b in zip(vectors[:, j], basis))
            value = float(values[j])
            row[label] = dict(value=value, ritz_residual=norm(mv(v)-value*v))
        rows.append(row)
    return dict(dtype='float64', starts=rows, seconds=time.perf_counter()-started,
                limitation='Finite Lanczos cannot certify the full spectrum; saved float32 weights promoted without retraining.')


class CapturedSystem(Exception):
    pass


def capture_system(instance, model, data, nodes, root):
    """Intercept the existing adapter at its solver seam, before any update."""
    from experiments.modular_model import runtime_defaults
    from experiments.modular_gu import GU_METHODS
    args = runtime_defaults()
    args.update(instance['parameters'])
    args.update(instance=instance, dataset_name='Cora', base_model='GCN',
        downstream_task='node', unlearn_task='node', unlearning_methods=instance['method'],
        num_epochs=100, num_runs=1, run_update_detection_auc=False, random_seed=42,
        gcn_num_layers=2, gcn_hidden=instance['model']['hidden_channels'], formal_expected_k=len(nodes),
        num_unlearned_nodes=len(nodes), formal_fail_closed=True, test_freq=1,
        device=str(data.x.device))
    captured = {}
    def intercept(matvec, rhs, **kwargs):
        captured.update(matvec=matvec, rhs=rhs, effective_parameters=kwargs)
        raise CapturedSystem()
    module = ('unlearning.unlearning_methods.GIF.gif' if instance['method']=='GIF'
              else 'unlearning.unlearning_methods.GIF.solver')
    with patch.object(importlib.import_module(module), 'solve_gif_system', intercept):
        try:
            GU_METHODS[instance['method']](args, model, data, nodes, root)
        except CapturedSystem:
            pass
    if not captured:
        raise ValueError('existing adapter did not reach the solver seam')
    return captured


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config', type=Path)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    # Legacy config.py parses process argv on first import during data/model loading.
    # This entry owns the YAML CLI; effective model/method args are supplied explicitly.
    sys.argv[:] = sys.argv[:1]
    import torch
    from experiments.modular_config import load_experiment, experiment_batches, resolve_budget, configuration_fingerprint
    from experiments.modular_artifacts import planned_cells
    from experiments.modular_execution import device_context
    from experiments.modular_model import prepare_model, create_model, training_metadata
    from experiments.dataset_inputs import bind_input, resolve_input
    from experiments.modular_run import verified_selection
    from experiments.selection_inputs import make_dataset_selection_inputs
    from utils.target_checkpoint import state_hash, sha256_file, data_identity, load_target_checkpoint
    from attack.cache_identity import seeded_execution
    torch.set_num_threads(2)
    config = load_experiment(args.config)
    widths = {u['model']['hidden_channels'] for u in config['unlearnings']}
    if len(widths) != 1 or not widths <= {64, 16}:
        raise ValueError('each table must bind one registered hidden width')
    width = next(iter(widths))
    version=3 if width==64 else 4
    if config['experiment_id'] != f'aagu059-table01-h{width}' or args.run_id != f'aagu059-table01-h{width}-v{version}':
        raise ValueError('unregistered run identity')
    context = device_context(config['experiment_id'], run_id=args.run_id, device_file=ROOT/'.syncmate/device.yaml')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip():
        raise ValueError('tracked source is dirty')
    output = context.output.parent
    output.mkdir(parents=True, exist_ok=False)
    batch = next(experiment_batches(config))
    cells = planned_cells(config)
    started = time.perf_counter()
    run = dict(schema='aagu059.diagnostic.v1', experiment_id=config['experiment_id'], run_id=args.run_id,
        commit=context.source_git_sha, config_path=args.config.as_posix(),
        configuration_fingerprint=configuration_fingerprint(args.config), status='running',
        context=context.receipt(), cells=[dict(c, status='not_executed') for c in cells])
    write(context.output, run)
    if sha256_file(args.config.parent/'binding.json') != '6d034bb3176505b55e68abf6f39816c13f26671e4aa3ef671b0957fff136c4ac':
        raise ValueError('reviewed request binding changed')
    binding = json.loads((args.config.parent/'binding.json').read_text())
    data_ref = bind_input(batch['dataset'],batch['dataset_directory'],ROOT)
    data = resolve_input(data_ref,ROOT)
    if not (ROOT/data_ref['graph']).resolve().is_relative_to(ROOT/'data/processed'):
        raise ValueError('formal graph outside canonical processed root')
    for selector in batch['selectors']:
        selector['budget'] = resolve_budget(selector['budget'],int(data.train_mask.sum()))
    selected_ref = {k:binding['selection'][k] for k in ('artifact_id','recipe_hash','content_hash')}
    inputs = make_dataset_selection_inputs(data,dataset_name=batch['dataset']['dataset']['name'].lower())
    selection = verified_selection(selected_ref,store_root=context.store_root,data=data,inputs=inputs,
                                   expected_selector='random',expected_k=189)
    if batch['selectors'][0]['parameters']['seed'] != binding['random_seed']:
        raise ValueError('Random seed differs from sealed request')
    materialized = binding['selection']
    nodes = list(selection.selected_nodes)
    original_data_identity = data_identity(data)
    common = dict(dataset_input=data_ref, data_identity=original_data_identity, selection=materialized,
        selected_nodes=nodes, selector_parameters=batch['selectors'][0]['parameters'], source_score_artifact_id=binding['source_score_artifact_id'], binding_sha256=sha256_file(args.config.parent/'binding.json'))
    baselines = {}
    for index, (cell, instance) in enumerate(zip(run['cells'],batch['unlearnings'])):
        name = instance['method']
        width = instance['model']['hidden_channels']
        key = (name, width)
        budget = instance['parameters']['iteration']
        cell_start = time.perf_counter()
        row = dict(method=name, hidden_channels=width, budget=budget, scale=instance['parameters']['scale'], damp=0,
                   status='not_executed', failure_reason=None, f1_after=None, update_vs_T=None)
        try:
            bound_instance = copy.deepcopy(instance)
            if width not in (64, 16):
                raise ValueError('unregistered hidden width')
            preparation_start = time.perf_counter()
            training_data=data.clone().to(context.request_device) if width==16 else data
            if width == 64:
                # Historical diagnostic binds an exact internal training artifact;
                # it does not use the public pure-weight checkpoint configuration.
                fixed = binding['checkpoints']['64']
                path = (args.config.parent / fixed['path']).resolve()
                with seeded_execution(instance['training']['seed']):
                    model = create_model(instance['model'], 'Cora', training_data, context.request_device)
                metadata = training_metadata(model, instance, training_data)
                loaded = load_target_checkpoint(path, expected_file_sha256=fixed['file_sha256'],
                    expected_state_hash=fixed['state_hash'], expected_metadata=metadata)
                model.load_state_dict(loaded['state_dict'], strict=True)
                cp = dict(path=str(path), file_sha256=loaded['file_sha256'], state_hash=loaded['state_hash'],
                          hit=True, effective_identity=metadata)
            else:
                model, _, cp = prepare_model(bound_instance,data=training_data,dataset_name='Cora',checkpoint_root=context.checkpoint_root,
                    device=context.request_device,reference_directory=args.config.parent)
            row['model_preparation_seconds'] = time.perf_counter()-preparation_start
            if width == 64 and not cp['hit']:
                raise ValueError('hidden64 checkpoint was not reused')
            working = data.clone().to(context.request_device)
            working.num_classes=int(data.y.max())+1
            for split in ('train','val','test'):
                setattr(working,split+'_indices',getattr(working,split+'_mask').nonzero().flatten().cpu().numpy())
            model.eval()
            saved_hash=state_hash(model.state_dict())
            with torch.no_grad():
                logits=model(working.x,working.edge_index)
                before=float((logits[working.test_mask].argmax(1)==working.y[working.test_mask]).double().mean())
            captured=capture_system(instance,model,working,nodes,output)
            mv,rhs=captured['matvec'],captured['rhs']
            params=list(model.parameters());sizes=[p.numel() for p in params]
            loss=torch.nn.functional.cross_entropy(model.reason_once(working)[working.train_mask],working.y[working.train_mask],reduction='sum')
            gradient=torch.autograd.grad(loss,params,create_graph=True)
            def expected(v):
                return flat(torch.autograd.grad(gradient,params,grad_outputs=[x.reshape_as(p) for x,p in zip(v.detach().split(sizes),params)],retain_graph=True)).detach()
            torch.manual_seed(173)
            probe=torch.randn_like(rhs); probe/=probe.norm()
            expected_probe=expected(probe)
            agreement=norm(mv(probe)-expected_probe)/max(norm(expected_probe),1e-30)
            rhs_agreement=norm(mv(rhs)-expected(rhs))/max(norm(expected(rhs)),1e-30)
            repeat=norm(mv(probe)-mv(probe))/max(norm(expected_probe),1e-30)
            if max(agreement,rhs_agreement,repeat)>1e-5:
                raise ValueError('actual HVP differs from fixed expected Hessian')
            curvature_path=f'h{width}-{name.lower()}-curvature.json'
            if budget==100:
                double_model=copy.deepcopy(model).double().eval()
                double_data=working.clone();double_data.x=double_data.x.double()
                ds=capture_system(instance,double_model,double_data,nodes,output)
                curvature=lanczos(ds['matvec'],rhs.numel(),rhs.device)
                write(output/curvature_path,curvature)
                del ds,double_model,double_data
            delta,trace,steps,status,seconds=measured_series(mv,rhs,budget,row['scale'],0.)
            # Independently execute the unchanged production solver as a recurrence check.
            from unlearning.unlearning_methods.GIF.solver import solve_gif_system,GIFNumericalError
            recurrence_relative_error=None
            try:
                production,diagnostics=solve_gif_system(mv,rhs,iterations=budget,scale=row['scale'],damp=0.)
                if delta is not None:
                    recurrence_relative_error=norm(production-delta)/max(norm(production),1e-30)
                if delta is None or recurrence_relative_error>1e-5:
                    raise ValueError('instrumentation changed the production recurrence')
                production_check='delta_agrees_within_float32_tolerance'
            except GIFNumericalError as exc:
                diagnostics=exc.diagnostics
                if delta is not None:
                    raise ValueError('production failed but diagnostic returned a finite update')
                production_check='both_nonfinite'
            row.update(status=status,actual_iterations=steps,finite=delta is not None,
                failure_reason=None if delta is not None else status,relative_residual=trace[-1]['relative_residual'] if delta is not None else None,
                last_finite=trace[-1] if trace else None,delta_l2=norm(delta) if delta is not None else None,
                f1_before=before,checkpoint=cp,model=instance['model'],training=instance['training'],parameters=instance['parameters'],effective_parameters=captured['effective_parameters'],
                hvp_check=dict(random_relative_error=agreement,rhs_relative_error=rhs_agreement,repeat_relative_error=repeat),
                recurrence_check=production_check,recurrence_relative_error=recurrence_relative_error,recurrence_tolerance=1e-5,production_diagnostics=diagnostics,solver_seconds=seconds,
                rhs_l2=norm(rhs),curvature=curvature_path,trace=trace)
            if delta is not None:
                if budget==100: baselines[key]=delta.clone()
                else:
                    base=baselines.get(key)
                    row['update_vs_T']=norm(delta-base)/max(norm(base),1e-30) if base is not None else None
                candidate=copy.deepcopy(model)
                with torch.no_grad():
                    for p,d in zip(candidate.parameters(),delta.split(sizes)):p.add_(d.reshape_as(p))
                    after=candidate(working.x,working.edge_index)
                if torch.isfinite(after).all():
                    row['f1_after']=float((after[working.test_mask].argmax(1)==working.y[working.test_mask]).double().mean())
                else:row['failure_reason']='finite_update_but_nonfinite_logits'
                del candidate
            if state_hash(model.state_dict())!=saved_hash or sha256_file(cp['path'])!=cp['file_sha256']:
                raise ValueError('original model/checkpoint was changed')
            row['original_unchanged']=True
        except Exception as exc:
            import traceback
            row.update(status='diagnostic_error',failure_reason=f'{type(exc).__name__}: {exc}',error_traceback=traceback.format_exc())
        row['total_seconds']=time.perf_counter()-cell_start
        filename=f'h{width}-{name.lower()}-{budget}.json'
        write(output/filename,row)
        cell.update(status=row['status'],diagnostic=filename,sha256=sha256_file(output/filename))
        write(context.output,run)
        print(f'h{width} {name} {budget}: {row["status"]}',file=sys.stderr,flush=True)
        if row['status']=='diagnostic_error':
            break
    write(output/'inputs.json',common)
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()!=context.source_git_sha:
        raise ValueError('source changed during execution')
    run.update(status='diagnostic_complete' if all(c['status'] not in ('not_executed','diagnostic_error') for c in run['cells']) else 'failed',
               total_seconds=time.perf_counter()-started,inputs_sha256=sha256_file(output/'inputs.json'))
    write(context.output,run)
    paths=[str(p.relative_to(ROOT)).replace('\\','/') for p in output.glob('*.json')]
    return dict(passed=run['status']=='diagnostic_complete',generated_artifacts=sorted(paths))


if __name__=='__main__':
    with contextlib.redirect_stdout(sys.stderr):
        result=main()
    print(json.dumps(result))
