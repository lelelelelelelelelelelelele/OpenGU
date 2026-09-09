"""Confirm the preselected GIF configuration through the real adapter.

Two existing Cora Random Selection/checkpoint pairs (seeds 212 and 2024).
No new training or selection computation. Retains failed attempts.
"""
import argparse
import json
from pathlib import Path
import sys

from diagnose_gif_solver import sha, write, load_module


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--bundle',required=True,type=Path)
    parser.add_argument('--destination',required=True,type=Path)
    parser.add_argument('--parameters',required=True,type=Path)
    options=parser.parse_args()
    root=options.repo.resolve();bundle=options.bundle.resolve();destination=options.destination.resolve()
    assert destination.is_relative_to(root/'results/diagnostics/AAGU-052')
    manifest=json.loads((bundle/'manifest.json').read_text())
    for name,expected in manifest['files'].items():assert sha(bundle/name)==expected
    parameters=json.loads(options.parameters.read_text())
    assert parameters['seeds']==[212,2024] and parameters['selector']=='random'
    destination.mkdir(parents=True,exist_ok=False)
    sys.path.insert(0,str(root))
    import numpy as np
    import torch
    from experiments.modular_model import runtime_defaults,create_model,train_supervised,numerical_environment
    runtime_defaults();torch.set_num_threads(2)
    assert torch.cuda.is_available()
    from experiments.unlearning_outputs import load_output
    from experiments.dataset_inputs import resolve_input
    from experiments.node_deletion import retained_graph
    from experiments.implementation_identity import implementation_fingerprint,model_functions
    from utils.target_checkpoint import data_identity,load_target_checkpoint,state_hash
    from cache_v2 import canonical_sha256
    from attack.cache_identity import seeded_execution
    runpath=root/'results/runs/aagu011-table01-gu/aagu011-table01-v2/run.json'
    retrainpath=root/'results/runs/aagu011-table01-retrain/aagu011-references-v1/run.json'
    run=json.loads(runpath.read_text());retrain_run=json.loads(retrainpath.read_text())
    records=[]
    # Validate all historical producers before loading the isolated new producer.
    for seed in parameters['seeds']:
        match=lambda c: c['conditions']['dataset_name']=='Cora' and c['conditions']['training_seed']==seed and c['conditions']['selector']=='random'
        cell=next(c for c in run['cells'] if match(c) and c['conditions']['method']=='GIF')
        rcell=next(c for c in retrain_run['cells'] if match(c) and c['conditions']['method']=='Retrain')
        output=load_output(cell['output'],root/'results/cache_v2',dataset_root=root)
        retrain=load_output(rcell['output'],root/'results/cache_v2',dataset_root=root)
        assert output.identity['pairing']==retrain.identity['pairing']
        records.append((seed,cell,rcell,output,retrain))
    solver=load_module('unlearning.unlearning_methods.GIF.solver',bundle/'solver.py')
    cls=load_module('unlearning.unlearning_methods.GIF.gif',bundle/'gif.py').gif
    adapter=load_module('experiments.modular_gu',bundle/'modular_gu.py')
    result=dict(source_manifest=manifest,parameters=parameters,
                run=dict(path=str(runpath),sha256=sha(runpath)),
                retrain_run=dict(path=str(retrainpath),sha256=sha(retrainpath)),cells=[])
    for seed,cell,rcell,output,retrain in records:
        pair=output.identity['pairing']
        data=resolve_input(output.identity['dataset_input'],root)
        assert (root/output.identity['dataset_input']['graph']).resolve().is_relative_to(root/'data/processed')
        original=create_model(pair['model'],'Cora',data,'cpu')
        metadata=dict(data_identity=data_identity(data),model=pair['model'],training=pair['training'],
                      numerics=numerical_environment(data),implementation=implementation_fingerprint(*model_functions(original),train_supervised))
        checkpoint=root/'results/runtime/modular/checkpoints'/(canonical_sha256(metadata)+'.pt')
        ck=load_target_checkpoint(checkpoint,expected_state_hash=output.identity['target']['checkpoint_state_hash'],expected_metadata=metadata)
        original.load_state_dict(ck['state_dict']);original=original.cuda().eval();data=data.cuda()
        for name in ('train','val','test'):
            setattr(data,name+'_indices',getattr(data,name+'_mask').nonzero().flatten().cpu().numpy())
        data.num_classes=int(data.y.max())+1
        nodes=pair['selected_nodes']
        assert len(nodes)==189
        model=create_model(pair['model'],'Cora',data,'cuda');model.load_state_dict(ck['state_dict']);model.eval()
        reference=create_model(pair['model'],'Cora',data,'cuda')
        reference.load_state_dict({name:torch.as_tensor(value) for name,value in retrain.state.items()});reference.eval()
        with torch.no_grad():before=original(data.x,data.edge_index);ref=reference(data.x,data.edge_index)
        np.testing.assert_allclose(ref.cpu().numpy(),retrain.arrays['logits'],rtol=1e-5,atol=2e-5)
        args=runtime_defaults();args.update(output.identity['target']['parameters']);args.update(parameters['solver'])
        args.update(dataset_name='Cora',base_model='GCN',downstream_task='node',unlearn_task='node',
                    num_runs=1,num_unlearned_nodes=len(nodes),formal_expected_k=len(nodes),
                    run_update_detection_auc=False,random_seed=seed,formal_fail_closed=True)
        row=dict(seed=seed,k=len(nodes),status='started',original_output=cell['output'],retrain_output=rcell['output'],
                 selection=output.identity['selection'],data_identity=pair['data_identity'],
                 checkpoint=dict(path=str(checkpoint),file_sha256=ck['file_sha256'],state_hash=ck['state_hash']),
                 producer=adapter.gu_producer('GIF',pair['model']).to_dict())
        result['cells'].append(row);write(destination/'result.json',result)
        def trace(frame,event,value):
            if frame.f_code is cls.approxi.__code__ and event=='return':
                obj=frame.f_locals['self']
                row['solver']=obj.solver_diagnostics
                row['graph_matches_declared_deletion']=torch.equal(obj.data.edge_index_unlearn,retained_graph(data,nodes).edge_index)
                assert row['graph_matches_declared_deletion']
            return trace
        try:
            with seeded_execution(seed):
                sys.settrace(trace)
                model,elapsed=adapter.gif_node(args,model,data.clone(),nodes,destination)
            row.update(status='converged',seconds=elapsed)
        except solver.GIFConvergenceError as error:
            row.update(status='rejected',solver=error.diagnostics)
            assert state_hash(model.state_dict())==ck['state_hash']
        finally:sys.settrace(None)
        model.eval()
        with torch.no_grad():after=model(data.x,data.edge_index)
        mask=data.test_mask;y=data.y[mask]
        def gap(left,right):
            return dict(flips=int((left[mask].argmax(1)!=right[mask].argmax(1)).sum()),
                        probability_rmse=float((left[mask].softmax(1)-right[mask].softmax(1)).square().mean().sqrt()),
                        probability_max_abs=float((left[mask].softmax(1)-right[mask].softmax(1)).abs().max()))
        row.update(before_f1=float((before[mask].argmax(1)==y).double().mean()),
                   after_f1=float((after[mask].argmax(1)==y).double().mean()),
                   retrain_f1=float((ref[mask].argmax(1)==y).double().mean()),
                   update_gap=gap(after,before),baseline_retrain_gap=gap(before,ref),retrain_gap=gap(after,ref),
                   evaluation_graph='original',test_count=int(mask.sum()),state_hash=state_hash(model.state_dict()))
        path=destination/f'seed{seed}.pt'
        torch.save(dict(state_dict={name:v.detach().cpu() for name,v in model.state_dict().items()},logits=after.cpu(),selected_nodes=nodes),path)
        row['file']=dict(path=str(path),sha256=sha(path));write(destination/'result.json',result)
        print(json.dumps(row),flush=True)
    result['finished']=True;write(destination/'result.json',result)


if __name__=='__main__':main()
