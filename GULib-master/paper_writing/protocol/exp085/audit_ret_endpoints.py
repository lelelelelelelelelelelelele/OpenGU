"""Read-only exact Ret endpoint asset audit; run on the idle installed checkout.

No training, scoring, model forward, cache repair, or file output. Emit one JSON
to stdout. Consumes immutable old Output via existing readers and the native
Ret run reader; independent file/state hashes and endpoint comparison checks.
"""
from pathlib import Path
import argparse
import contextlib
import io
import json
import hashlib
import subprocess
import sys

sys.dont_write_bytecode = True
from analyze_ret import read, sha, require, close, check_frozen, quantify, exact_final, OBS


def contained(root, relative):
    path=(root/relative).resolve()
    require(root==path or root in path.parents,'path escapes checkout')
    return path


def compare_arrays(old_logits, final_logits, mask, old_state_hash, final_state_hash):
    import numpy as np
    require(old_logits.shape==final_logits.shape and old_logits.dtype==final_logits.dtype,'old/final logits shape/dtype differs')
    require(np.isfinite(old_logits).all() and np.isfinite(final_logits).all(),'nonfinite predictions')
    changed=old_logits.argmax(1)!=final_logits.argmax(1)
    return dict(state_hash_equal=old_state_hash==final_state_hash,
        all_node_prediction_changes=int(changed.sum()),test_prediction_changes=int(changed[mask].sum()),
        maximum_absolute_logit_error=float(np.abs(final_logits-old_logits).max()))


def load_endpoint(root, endpoint, old_state):
    import numpy as np
    from utils.target_checkpoint import load_weights
    files={key:contained(root,value['path']) for key,value in endpoint.items() if key in ('weights','predictions')}
    for key,path in files.items(): require(sha(path)==endpoint[key]['sha256'],'endpoint file checksum differs: '+key)
    loaded=load_weights(files['weights'])
    require(loaded['state_hash']==endpoint['state_hash'],'endpoint state hash differs')
    require(set(loaded['state_dict'])==set(old_state),'endpoint state keys differ from old Ret')
    for name,tensor in loaded['state_dict'].items():
        array=tensor.numpy();old=old_state[name]
        require(array.dtype==old.dtype and array.shape==old.shape,'endpoint tensor dtype/shape differs')
        require(np.isfinite(array).all(),'nonfinite endpoint state')
    with np.load(io.BytesIO(files['predictions'].read_bytes()),allow_pickle=False) as bundle:
        require(set(bundle.files)=={'logits'},'unexpected prediction arrays')
        logits=bundle['logits'].copy()
    require(logits.ndim==2 and np.isfinite(logits).all(),'invalid endpoint logits')
    return loaded,logits,files


def pair_counts(gu_logits, ret_logits, labels):
    import numpy as np
    from experiments.response_diagnostics import cross_entropy
    g,r,y=np.asarray(gu_logits),np.asarray(ret_logits),np.asarray(labels)
    require(g.ndim==r.ndim==2 and g.shape==r.shape and len(g)==len(y),'paired prediction shape differs')
    require(np.isfinite(g).all() and np.isfinite(r).all(),'paired predictions nonfinite')
    gp,rp=g.argmax(1),r.argmax(1);gc,rc=gp==y,rp==y;different=gp!=rp
    cells={}
    for left in (0,1):
        for right in (0,1):
            mask=(gc==left)&(rc==right)
            cells[str(left)+str(right)]=dict(count=int(mask.sum()),disagreement_count=int((different&mask).sum()))
    return dict(node_count=len(y),correctness_order=['GU','Ret'],cells=cells,
        disagreement_count=int(different.sum()),disagreement=float(different.mean()) if len(y) else None,
        gu_accuracy=float(gc.mean()) if len(y) else None,retrain_accuracy=float(rc.mean()) if len(y) else None,
        gu_cross_entropy=cross_entropy(g,y),retrain_cross_entropy=cross_entropy(r,y))


def audit(args):
    root=args.repo_root.resolve()
    frozen,source=check_frozen(args.frozen_manifest,args.frozen_sha256)
    require(sha(Path(__file__))==frozen['endpoint_audit_script_sha256'],'audit source differs from freeze')
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    require(head==args.expected_commit,'installed checkout SHA differs')
    sys.path.insert(0,str(root));sys.argv=[sys.argv[0]]
    import numpy as np
    import torch
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_output_payload,load_metric_output
    from utils.target_checkpoint import state_hash
    from cache_v2 import ArtifactRecipe
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.flip_hop_metrics import exact_retrain

    store=root/'results/cache_v2';index=store/'index.sqlite';index_before=sha(index)
    path=contained(root,args.run)
    run,documents=read_run(path,args.run_sha256)
    require(run['commit']==head and run['stage']=='retrain_diagnostics' and run['status']=='completed','run identity/state differs')
    batches=[b for b in frozen['batches'] if b['run_id']==run['run_id']]
    require(len(batches)==1,'run is not one frozen batch');batch=batches[0]
    require(run['experiment_id']==batch['experiment_id'] and run['config_path']==batch['config_path'],'run experiment/config differs')
    require(path==root/'results/runs'/run['experiment_id']/run['run_id']/'run.json','run layout differs')
    require(len(run['cells'])==len(batch['cell_ids']) and {c['cell_id'] for c in run['cells']}==set(batch['cell_ids']),'run matrix differs')
    refs={v['cell_id']:v for v in source['cells']};files={path:args.run_sha256};rows=[]
    source_path=root/'results/runs'/source['experiment_id']/source['run_id']/'run.json'
    old_run,old_documents=read_run(source_path,source['run_sha256'])
    require(old_run['commit']==source['commit'],'old run execution differs')
    old_cells={c['cell_id']:(c,d) for c,d in zip(old_run['cells'],old_documents)}
    files[source_path]=source['run_sha256']
    gu_refs=source['gu_cells'];require(len(gu_refs)==18,'fixed GU matrix incomplete')
    for cell,document in zip(run['cells'],documents):
        ref=refs[cell['cell_id']]
        require(cell['conditions']==ref['conditions'] and cell['source']['output']==ref['output'],'source conditions/Output differs')
        result_path=path.parent/cell['path']/('observers/'+OBS+'/result.json')
        result=read(result_path);diagnostic=result['diagnostics']
        files[result_path]=cell['files']['observers/'+OBS+'/result.json']['sha256']
        identity=result['identity']
        require(identity['source']==cell['source'] and identity['commit']==head,'Observer source differs')
        trace_path=path.parent/cell['path']/('observers/'+OBS+'/trace.jsonl')
        files[trace_path]=cell['files']['observers/'+OBS+'/trace.jsonl']['sha256']
        quantify(read(trace_path),diagnostic)
        old=load_output_payload(ref['output'],store,dataset_root=root)
        require(old.identity==identity['output_identity'],'old Output payload identity differs')
        require(ArtifactRecipe({'artifact_contract':OUTPUT_CONTRACT,**old.identity}).recipe_hash==ref['output']['recipe_hash'],'old Output Recipe differs')
        resolved=load_metric_output(ref['output'],store,dataset_root=root)
        labels=torch.tensor(resolved.arrays['y']);mask=np.asarray(resolved.arrays['test_mask'])
        require(mask.dtype==np.bool_ and mask.sum()==666 and len(mask)==3327,'original test mask differs')
        require(old.identity['pairing']['deletion']['evaluation_graph']=='original','test graph differs')
        old_hash=state_hash({key:torch.tensor(value) for key,value in old.state.items()})
        endpoints={};logits_by={};states={}
        for role in ('best','final'):
            endpoint=diagnostic[role]
            for key,suffix in (('weights','.pt'),('predictions','.npz')):
                expected=f'results/runtime/modular/{run["run_id"]}/retrain_diagnostics/{cell["cell_id"]}/{role}{suffix}'
                require(endpoint[key]['path']==expected,'runtime path does not bind run/cell/role')
            loaded,logits,paths=load_endpoint(root,endpoint,old.state)
            require(logits.shape==old.arrays['logits'].shape and logits.dtype==old.arrays['logits'].dtype,'endpoint prediction shape/dtype differs')
            states[role]=loaded['state_hash'];logits_by[role]=logits
            for key,asset in paths.items(): files[asset]=endpoint[key]['sha256']
            selected=torch.tensor(logits[mask]);truth=labels[torch.tensor(mask)]
            measured=dict(accuracy=float((selected.argmax(1)==truth).double().mean()),
                cross_entropy=float(torch.nn.functional.cross_entropy(selected,truth)))
            for key,value in measured.items():
                close(value,endpoint['test'][key],role+' test '+key,atol=2e-6 if key=='cross_entropy' else 1e-12,rtol=2e-6 if key=='cross_entropy' else 0)
            endpoints[role]=dict(state_hash=loaded['state_hash'],weights=endpoint['weights'],predictions=endpoint['predictions'],independent_test=measured)
        comparison=compare_arrays(old.arrays['logits'],logits_by['final'],mask,old_hash,states['final'])
        for key,value in comparison.items(): require(value==diagnostic['old_final_comparison'][key],'old/final comparison differs: '+key)
        old_values=torch.tensor(old.arrays['logits'][mask]);truth=labels[torch.tensor(mask)]
        old_test=dict(accuracy=float((old_values.argmax(1)==truth).double().mean()),
            cross_entropy=float(torch.nn.functional.cross_entropy(old_values,truth)))
        for key,value in old_test.items():
            close(value,diagnostic['old_final_comparison']['old_test'][key],'old test '+key,atol=2e-6 if key=='cross_entropy' else 1e-12,rtol=2e-6 if key=='cross_entropy' else 0)
        comparisons=[]
        matched=[g for g in gu_refs if g['retrain_cell_id']==cell['cell_id']]
        require(len(matched)==2 and {g['conditions']['method'] for g in matched}=={'GIF','MEGU'},'missing fixed GU pair')
        for gu_ref in matched:
            gu_cell,gu_docs=old_cells[gu_ref['cell_id']]
            require(gu_cell['output']==gu_ref['output'] and gu_cell['conditions']==gu_ref['conditions']
                and gu_cell['selection_id']==ref['selection_id'] and gu_docs['selection.json']['selected_nodes']==ref['selected_nodes'],'GU source binding differs')
            gu=load_metric_output(gu_ref['output'],store,dataset_root=root)
            exact_retrain(gu,[(None,resolved)])
            require(np.array_equal(gu.arrays['test_mask'],mask) and np.array_equal(gu.arrays['y'],resolved.arrays['y']),'paired test/labels differ')
            for role,predictions in [('old_final',old.arrays['logits'])]+list(logits_by.items()):
                truth=resolved.arrays['y'][mask];gu_logits=gu.arrays['logits'][mask];ret_logits=predictions[mask]
                comparisons.append(dict(gu_cell_id=gu_ref['cell_id'],gu_output=gu_ref['output'],method=gu_ref['conditions']['method'],
                    checkpoint_role=role,gu_prediction='updated_C&S' if gu_ref['conditions']['method']=='MEGU' else 'persisted_updated_logits',
                    metrics=pair_counts(gu_logits,ret_logits,truth),
                    by_class=[dict(class_id=c,metrics=pair_counts(gu_logits[truth==c],ret_logits[truth==c],truth[truth==c]))
                              for c in range(gu_logits.shape[1])]))
        rows.append(dict(cell_id=cell['cell_id'],conditions=cell['conditions'],source_output=ref['output'],
            dataset_input=old.identity['dataset_input'],graph_fingerprint=old.identity['graph_fingerprint'],
            test_mask_sha256=hashlib.sha256(mask.astype(np.uint8).tobytes()).hexdigest(),test_node_count=int(mask.sum()),
            observer_result_sha256=cell['files']['observers/'+OBS+'/result.json']['sha256'],old_state_hash=old_hash,
            endpoints=endpoints,recorded_comparison=diagnostic['old_final_comparison'],independent_comparison=comparison,
            old_final_exact=exact_final(diagnostic),gu_comparisons=comparisons))
    for file,checksum in files.items(): require(sha(file)==checksum,'file changed during audit')
    require(sha(index)==index_before,'cache index changed; require idle runner')
    return dict(status='passed',read_only=True,producer_calls=0,index_unchanged=True,index_sha256=index_before,
        scope='endpoint asset hashes, states, saved predictions, old-final comparisons; no forward or scientific acceptance',
        execution_sha=head,run_id=run['run_id'],run_sha256=args.run_sha256,
        source_run_sha256=source['run_sha256'],source_manifest_sha256=frozen['source_manifest_sha256'],
        saved_predictions_only=True,forward_calls=0,cache_mutations=0,
        frozen_manifest_sha256=args.frozen_sha256,audit_script_sha256=sha(Path(__file__)),rows=rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,required=True)
    parser.add_argument('--run',type=Path,required=True);parser.add_argument('--run-sha256',required=True)
    parser.add_argument('--expected-commit',required=True)
    parser.add_argument('--frozen-manifest',type=Path,required=True);parser.add_argument('--frozen-sha256',required=True)
    args=parser.parse_args()
    try:
        with contextlib.redirect_stdout(sys.stderr): result=audit(args)
    except Exception as exc:
        print(json.dumps(dict(status='failed',read_only=True,error_type=type(exc).__name__,error=str(exc))))
        return 1
    print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False));return 0


if __name__=='__main__': raise SystemExit(main())
