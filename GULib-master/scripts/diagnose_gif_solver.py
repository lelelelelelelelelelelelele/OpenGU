"""AAGU-052: fixed-input curvature inspection and bounded isolated GIF updates.

Run from the canonical SSH checkout with an explicitly hashed source bundle.
Inputs/cache stay read-only; each output directory must be new.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time
import inspect


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--phase', choices=['curvature', 'updates', 'compare'], required=True)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--updates-result', type=Path)
    options = parser.parse_args()
    root = options.repo.resolve()
    destination = options.destination.resolve()
    assert destination.is_relative_to(root/'results/diagnostics/AAGU-052')
    bundle = options.bundle.resolve()
    manifest = json.loads((bundle/'manifest.json').read_text())
    for path, expected in manifest['files'].items():
        assert sha(bundle/path) == expected, path
    destination.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(root))
    import numpy as np
    import torch
    from experiments.modular_model import runtime_defaults, create_model
    runtime_defaults()
    torch.set_num_threads(2)
    from experiments.unlearning_outputs import load_output
    from experiments.dataset_inputs import resolve_input
    from experiments.node_deletion import retained_graph
    from utils.target_checkpoint import data_identity, state_hash
    from unlearning.unlearning_methods.GIF.gif import gif as old_gif
    from task.GIFTrainer import GIFTrainer
    from types import SimpleNamespace
    import logging
    assert torch.cuda.is_available()
    previous = json.loads((bundle/'stress50-v1.json').read_text())
    runpath = root/'results/runs/aagu011-table01-gu/aagu011-table01-v2/run.json'
    assert sha(runpath) == previous['run_sha256']
    run = json.loads(runpath.read_text())
    cell = next(c for c in run['cells'] if c['conditions']['method']=='GIF' and
                c['conditions']['dataset_name']=='Cora' and c['conditions']['training_seed']==42 and
                c['conditions']['selector']=='random')
    assert cell['output'] == previous['original_output']
    output = load_output(cell['output'], root/'results/cache_v2', dataset_root=root)
    pair = output.identity['pairing']
    data = resolve_input(previous['dataset_input'], root)
    assert (root/previous['dataset_input']['graph']).resolve().is_relative_to(root/'data/processed')
    assert data_identity(data) == previous['data_identity']
    checkpoint = Path(previous['checkpoint']['path'])
    assert sha(checkpoint) == previous['checkpoint']['file_sha256']
    saved = torch.load(checkpoint, map_location='cpu', weights_only=False)
    state = saved['state_dict']
    assert state_hash(state) == previous['checkpoint']['state_hash']
    for entry in previous['files']:
        assert sha(entry['path']) == entry['sha256']
    data = data.cuda()
    for part in ('train','val','test'):
        setattr(data, part+'_indices', getattr(data, part+'_mask').nonzero().flatten().cpu().numpy())
    data.num_classes = int(data.y.max())+1
    order = previous['selection']['order']
    assert order[:189] == pair['selected_nodes'] and len(set(order))==len(data.train_indices)
    args = runtime_defaults()
    args.update(output.identity['target']['parameters'])
    args.update(dataset_name='Cora', base_model='GCN', downstream_task='node', unlearn_task='node',
                unlearning_methods='GIF', num_runs=1, num_epochs=pair['training']['epochs'],
                run_update_detection_auc=False, random_seed=42, formal_fail_closed=True)
    def model():
        result = create_model(pair['model'], 'Cora', data, 'cuda')
        result.load_state_dict(state)
        return result.eval()
    def method(k, cls=old_gif, parameters=None):
        current = model()
        settings = dict(args, num_unlearned_nodes=k, formal_expected_k=k)
        settings.update(parameters or {})
        obj = cls(settings, logging.getLogger('aagu052'), SimpleNamespace(data=data.clone(), model=current))
        obj.device = data.x.device
        obj.target_model = GIFTrainer(settings, obj.logger, current, obj.data)
        obj.target_model.device = obj.device
        obj.target_model_name = 'GCN'
        obj.unlearning_request(order[:k])
        obj.influence_nodes = np.intersect1d(obj.influence_nodes, data.train_indices)
        return obj
    flatten = lambda parts: torch.cat([p.reshape(-1) for p in parts])
    result = dict(phase=options.phase, source_manifest=manifest,
                  ssh_sha=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),
                  device=torch.cuda.get_device_name(), checkpoint=previous['checkpoint'],
                  dataset_input=previous['dataset_input'], data_identity=previous['data_identity'],
                  evaluation_graph='original', test_count=int(data.test_mask.sum()),
                  previous_evidence_sha256=sha(bundle/'stress50-v1.json'), cells=[])
    if options.phase == 'curvature':
        for k in (10,189,947):
            obj = method(k)
            expected = retained_graph(data, order[:k]).edge_index
            actual = obj.data.edge_index_unlearn.to(expected.device)
            encode = lambda edges: torch.sort(edges[0]*data.num_nodes+edges[1]).values
            same = torch.equal(encode(expected), encode(actual))
            gradients = obj.get_if_grad(0)
            params = [p for p in obj.target_model.model.parameters() if p.requires_grad]
            shapes = [p.numel() for p in params]
            def hvp(vector):
                pieces = [v.reshape_as(p) for v,p in zip(vector.split(shapes),params)]
                return flatten(torch.autograd.grad(sum((g*v).sum() for g,v in zip(gradients[0],pieces)),params,retain_graph=True)).detach()
            torch.manual_seed(52)
            q = torch.randn(sum(shapes), device='cuda')
            q /= q.norm()
            basis=[]; alphas=[]; betas=[]
            for index in range(40):
                basis.append(q)
                z = hvp(q)
                alpha = torch.dot(q,z)
                alphas.append(float(alpha))
                z = z-alpha*q
                if index:
                    z = z-betas[-1]*basis[-2]
                for _ in range(2):
                    for b in basis:
                        z -= torch.dot(b,z)*b
                beta = float(z.norm())
                if beta < 1e-8: break
                betas.append(beta)
                q = z/beta
            t = torch.diag(torch.tensor(alphas,dtype=torch.double))
            for i in range(len(alphas)-1): t[i,i+1]=t[i+1,i]=betas[i]
            eigenvalues,eigenvectors = torch.linalg.eigh(t)
            ritz = {}
            for label,i in [('minimum',0),('maximum',-1)]:
                vector = sum(float(w)*b for w,b in zip(eigenvectors[:,i],basis))
                av=hvp(vector)
                rayleigh=float(torch.dot(vector,av)/torch.dot(vector,vector))
                ritz[label]=dict(eigenvalue=float(eigenvalues[i]), rayleigh=rayleigh,
                                eigen_residual=float((av-rayleigh*vector).norm()))
            row=dict(k=k, parameter_count=sum(shapes), loss_reduction='sum',
                     gradient_all_l2=float(flatten(gradients[0]).double().norm()),
                     rhs_l2=float(flatten([a-b for a,b in zip(gradients[1],gradients[2])]).double().norm()),
                     graph_matches_declared_deletion=same, expected_edges=expected.shape[1], actual_edges=actual.shape[1],
                     actual_incident_edges=int(torch.isin(actual,torch.tensor(order[:k],device=actual.device)).any(0).sum()),
                     ritz=ritz, lanczos_steps=len(alphas))
            result['cells'].append(row)
            write(destination/'result.json',result)
            print(json.dumps(row), flush=True)
            del obj,gradients,params,basis
        return
    assert options.plan is not None
    plan = json.loads(options.plan.read_text())
    assert len(plan['arms'])*3 <= 24
    result['plan'] = plan
    result['plan_sha256'] = sha(options.plan)
    solver = load_module('unlearning.unlearning_methods.GIF.solver',bundle/'solver.py')
    new_gif = load_module('unlearning.unlearning_methods.GIF.gif',bundle/'gif.py').gif
    class SolverOnly(new_gif):
        update_edge_index_unlearn = old_gif.update_edge_index_unlearn
    class GraphOnly(old_gif):
        update_edge_index_unlearn = new_gif.update_edge_index_unlearn
    classes = dict(old=old_gif, solver_only=SolverOnly, graph_only=GraphOnly, full=new_gif)
    baseline = model()
    with torch.no_grad(): before=baseline(data.x,data.edge_index)
    zero = torch.load(root/'results/diagnostics/AAGU-049/stress50-v1/gif-k0.pt',map_location='cpu',weights_only=False)
    assert state_hash(zero['state_dict']) == previous['checkpoint']['state_hash']
    assert torch.equal(before.argmax(1).cpu(),zero['logits'].argmax(1))
    def metrics(logits, reference):
        mask=data.test_mask
        labels=data.y[mask]
        predicted=logits[mask].argmax(1)
        other=reference[mask].argmax(1)
        return dict(micro_f1=float((predicted==labels).double().mean()),
                    flips=int((predicted!=other).sum()),
                    probability_max_abs=float((logits[mask].softmax(1)-reference[mask].softmax(1)).abs().max()),
                    probability_rmse=float((logits[mask].softmax(1)-reference[mask].softmax(1)).square().mean().sqrt()))
    result['zero_update'] = dict(reused_file=str(root/'results/diagnostics/AAGU-049/stress50-v1/gif-k0.pt'),
                                 original_test=metrics(before,before))
    if options.phase == 'compare':
        assert options.updates_result is not None
        old_result=json.loads(options.updates_result.read_text())
        assert old_result['plan_sha256']==result['plan_sha256']
        assert old_result['checkpoint']==result['checkpoint']
        assert len(old_result['cells'])==3*len(plan['arms'])
        for row in old_result['cells']:
            assert row['status'] in ('returned','rejected')
            assert sha(row['saved_file']['path'])==row['saved_file']['sha256']
        old_result['comparison_source_manifest']=manifest
        old_result['updates_result_sha256']=sha(options.updates_result)
        result=old_result
    for arm in (plan['arms'] if options.phase == 'updates' else []):
        for k in (10,189,947):
            started=time.perf_counter()
            row=dict(arm=arm['name'],implementation=arm['implementation'],k=k,parameters=arm['parameters'],status='started')
            result['cells'].append(row)
            write(destination/'result.json',result)  # failed attempts remain counted
            obj=method(k,classes[arm['implementation']],arm['parameters'])
            actual=obj.data.edge_index_unlearn.to(data.x.device)
            expected=retained_graph(data,order[:k]).edge_index
            row['graph_matches_declared_deletion']=torch.equal(actual,expected)
            gradients=obj.get_if_grad(0)
            params=[p for p in obj.target_model.model.parameters() if p.requires_grad]
            rhs=flatten([a-b for a,b in zip(gradients[1],gradients[2])]).detach()
            row['rhs_l2']=float(rhs.double().norm())
            lines,start=inspect.getsourcelines(obj.approxi)
            capture_line=next(start+i for i,line in enumerate(lines) if 'test_F1 = self.target_model.eval_unlearn' in line)
            def trace(frame,event,value):
                if frame.f_code is obj.approxi.__func__.__code__ and event=='line' and frame.f_lineno==capture_line:
                    delta=frame.f_locals['params_change']
                    hd=flatten(torch.autograd.grad(sum((g*d.detach()).sum() for g,d in zip(gradients[0],delta)),params,retain_graph=True)).detach()
                    vector=flatten(delta).detach()
                    shift=arm['parameters']['scale']*arm['parameters']['damp']
                    row['undamped_residual']=float((hd-rhs).double().norm()/rhs.double().norm())
                    row['matched_residual']=float((hd+shift*vector-rhs).double().norm()/rhs.double().norm())
                    row['intended_delta_l2']=float(vector.double().norm())
                return trace
            try:
                sys.settrace(trace)
                obj.approxi(gradients)
                row['status']='returned'
            except solver.GIFConvergenceError as error:
                row['status']='rejected'
                row['solver']=error.diagnostics
                assert state_hash(obj.target_model.model.state_dict())==previous['checkpoint']['state_hash']
            finally:
                sys.settrace(None)
            row['seconds']=time.perf_counter()-started
            if hasattr(obj,'solver_diagnostics'):row['solver']=obj.solver_diagnostics
            obj.target_model.model.eval()
            with torch.no_grad(): after=obj.target_model.model(data.x,data.edge_index)
            row['original_test']=metrics(after,before)
            change=flatten([value.detach()-state[name].to(value.device) for name,value in obj.target_model.model.state_dict().items()])
            row['relative_parameter_l2']=float(change.double().norm()/flatten(list(state.values())).double().norm())
            row['state_hash']=state_hash(obj.target_model.model.state_dict())
            file=destination/(arm['name']+f'-k{k}.pt')
            torch.save(dict(state_dict={name:v.detach().cpu() for name,v in obj.target_model.model.state_dict().items()},
                            logits=after.cpu(),selected_nodes=order[:k],diagnostics=row),file)
            row['saved_file']=dict(path=str(file),sha256=sha(file))
            write(destination/'result.json',result)
            print(json.dumps({key:row.get(key) for key in ['arm','k','status','matched_residual','original_test','seconds']}),flush=True)
            del obj,gradients,params,rhs
    # Matched retraining is inspected only after every pre-registered solve.
    from unlearning.unlearning_methods.Retrain.retrain import run_retrain
    prior_retrain={row['k']:row for row in result.get('retrain',[])}
    result['retrain']=[]
    retrain_runpath=root/'results/runs/aagu011-table01-retrain/aagu011-references-v1/run.json'
    retrain_run=json.loads(retrain_runpath.read_text())
    result['retrain_run']=dict(path=str(retrain_runpath),sha256=sha(retrain_runpath))
    for k in (10,189,947):
        if k==947:
            reference_model=model()
            reference_path=root/'results/diagnostics/AAGU-049/stress50-v1/retrain-k50percent.pt'
            reference_model.load_state_dict(torch.load(reference_path,map_location='cuda',weights_only=False))
            reference_model.eval()
            with torch.no_grad(): reference=reference_model(data.x,data.edge_index)
            provenance=dict(path=str(reference_path),sha256=sha(reference_path),reused=True)
        elif k==189:
            ref_cell=next(c for c in retrain_run['cells'] if c['conditions']['method']=='Retrain' and
                         c['conditions']['dataset_name']=='Cora' and c['conditions']['training_seed']==42 and
                         c['conditions']['selector']=='random')
            ref=load_output(ref_cell['output'],root/'results/cache_v2',dataset_root=root)
            assert ref.identity['pairing']==pair
            reference_model=model()
            reference_model.load_state_dict({name:torch.as_tensor(value) for name,value in ref.state.items()})
            reference_model.eval()
            with torch.no_grad():reference=reference_model(data.x,data.edge_index)
            provenance=dict(output=ref_cell['output'],reused=True)
        else:
            if options.phase == 'compare':
                provenance=prior_retrain[k]['provenance']
                assert sha(provenance['path'])==provenance['sha256']
                reference_model=model()
                reference_model.load_state_dict(torch.load(provenance['path'],map_location='cuda',weights_only=False))
            else:
                assert plan['new_retrain_budget'] >= 1
                reference_model,elapsed=run_retrain(pair,data,order[:k],'Cora')
            reference_model.eval()
            with torch.no_grad():reference=reference_model(data.x,data.edge_index)
            if options.phase == 'updates':
                reference_path=destination/'retrain-k10.pt'
                torch.save(reference_model.state_dict(),reference_path)
                provenance=dict(path=str(reference_path),sha256=sha(reference_path),reused=False,seconds=elapsed)
        entry=dict(k=k,original_test=metrics(reference,before),provenance=provenance,
                   baseline_gap=metrics(before,reference),comparisons=[])
        for row in result['cells']:
            if row['k']==k:
                saved=torch.load(row['saved_file']['path'],map_location='cuda',weights_only=False)
                entry['comparisons'].append(dict(arm=row['arm'],status=row['status'],gap=metrics(saved['logits'],reference)))
        result['retrain'].append(entry)
        write(destination/'result.json',result)
    result['finished']=True
    write(destination/'result.json',result)


if __name__=='__main__':
    main()
