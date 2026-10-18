"""Read-only remote audit. Run on stdin with python -B; no cache writes/training."""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
from pathlib import Path
import ast
import hashlib
import io
import json
import sqlite3
import subprocess
import sys
import zipfile

ROOT = Path('/autodl-fs/data/OpenGU/GULib-master')
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
import numpy as np
import torch
torch.set_num_threads(2)
from experiments.dataset_inputs import resolve_input
from experiments.modular_model import create_model
from experiments.modular_shards import ShardEnsemble
from utils.target_checkpoint import load_weights, data_identity


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def node(source, name):
    return ast.dump(next(n for n in ast.parse(source).body if isinstance(n, (ast.FunctionDef,ast.ClassDef)) and n.name==name))


def main():
    base=ROOT/'results/runs/exp079-surrogate-multiseed/e79r5'
    run=read(base/'run.json')
    assert run['commit']=='e02b5fa40ebce66fb45e57ea23b8d6c8d7856685'
    assert sha(base/'run.json')=='115ebaa86a7fa95dd65ca64fc34d5fcc0d6033a2a9ee912ad54d947dbda38f56'
    code_checks={}
    for name,objects in {
        'experiments/modular_shards.py':['ShardEnsemble','run_grapheraser'],
        'experiments/modular_graphrevoker.py':['run_graphrevoker'],
        'experiments/modular_model.py':['create_model'],
        'model/base_gnn/gcn.py':['GCNNet'],
        'experiments/unlearning_outputs.py':['utility']}.items():
        frozen=subprocess.check_output(['git','show',run['commit']+':GULib-master/'+name])
        current=(ROOT/name).read_bytes()
        code_checks[name]={n:node(frozen,n)==node(current,n) for n in objects}
        assert all(code_checks[name].values()),name
    store=ROOT/'results/cache_v2'
    con=sqlite3.connect((store/'index.sqlite').as_uri()+'?mode=ro',uri=True)
    con.row_factory=sqlite3.Row
    checkpoints={}
    for prefix in ['grapheraser-','graphrevoker-']:
        for p in (ROOT/'results/runtime/modular/checkpoints').glob(prefix+'*.json'):
            record=read(p)
            checkpoints.setdefault(record['state_hash'],[]).append((p,record))
    records=[]; datasets={}
    selected=[c for c in run['cells'] if c['conditions']['method'] in ['GraphEraser','GraphRevoker'] and c['conditions']['selector_ref']=='gt_full.yaml']
    assert len(selected)==60
    for c in selected:
        cond=c['conditions'];ref=c['output']
        db=dict(con.execute('select * from artifacts where artifact_id=?',(ref['artifact_id'],)).fetchone())
        assert db['status']=='valid' and db['verification_status']=='verified'
        for k,v in ref.items():assert db[k]==v
        path=store/db['semantic_path'];assert path.resolve().is_relative_to(store.resolve())
        assert sha(path)==ref['content_hash']
        with zipfile.ZipFile(path) as z:
            meta=json.loads(z.read('metadata.json')); identity=meta['identity']
            def arr(name):return np.load(io.BytesIO(z.read(name+'.npy')),allow_pickle=False)
            before=arr('arrays__logits_before')
            after=arr('arrays__logits')
            canonical=arr('auxiliary__canonical_logits_before')
        ds=cond['dataset_name']
        if ds not in datasets:datasets[ds]=resolve_input(identity['dataset_input'],ROOT).cpu()
        data=datasets[ds]
        assert data_identity(data)==identity['pairing']['data_identity']
        assert identity['pairing']['deletion']['evaluation_graph']=='original'
        assert identity['target']['method']==cond['method']
        assert identity['pairing']['training']['seed']==cond['training_seed']
        mask=data.test_mask.numpy(); labels=data.y.numpy()
        def acc(a):return float(np.mean(a[mask].argmax(1)==labels[mask])*100)
        mp=base/c['path']/'metrics.json'
        assert sha(mp)==c['files']['metrics.json']['sha256']
        stages={s['stage']:s['values'] for s in read(mp)['rows']}
        assert abs(acc(before)-100*stages['utility']['f1_before'])<1e-10
        assert abs(acc(after)-100*stages['utility']['f1_after'])<1e-10
        match=checkpoints[identity['target']['ensemble_state_hash']]
        assert len(match)==1
        sidecar,cp=match[0]
        assert cp['metadata']['method']==cond['method']
        assert cp['metadata']['data_identity']==identity['pairing']['data_identity']
        assert cp['metadata']['training']==identity['pairing']['training']
        assert cp['metadata']['parameters']==identity['target']['parameters']
        row=dict(dataset=ds,method=cond['method'],seed=cond['training_seed'],cell_id=c['cell_id'],
                 output=ref,output_created_at=db['created_at'],generation_producer=identity['producer_version'],
                 saved_before_accuracy=acc(before),saved_after_accuracy=acc(after),canonical_before_accuracy=acc(canonical),
                 initial_ensemble_state_hash=cp['state_hash'],checkpoint=str(sidecar.with_suffix('.pt')),
                 checkpoint_metadata_sha256=sha(sidecar),checkpoint_metadata=cp['metadata'],
                 before_reproduced_from_initial_checkpoint=False)
        if ds=='Cora':
            loaded=load_weights(sidecar.with_suffix('.pt'))
            assert loaded['state_hash']==cp['state_hash'] and loaded['file_sha256']==cp['file_sha256']
            state=loaded['state_dict'];w=state['weights']
            models=[create_model(cp['metadata']['model'],'shard',data,torch.device('cpu')) for _ in w]
            ensemble=ShardEnsemble(models,state['assignment'],w)
            relevant={k:v for k,v in state.items() if k in ['assignment','weights'] or k.startswith('shard_models.')}
            ensemble.load_state_dict(relevant,strict=True);ensemble.eval()
            with torch.inference_mode():
                shard_logits=ensemble.shard_predictions(data.x,data.edge_index)
                logits=sum(weight*a for weight,a in zip(ensemble.weights,shard_logits)).numpy()
                uniform=torch.stack(shard_logits).mean(0).numpy()
            shard_metrics=[acc(a.numpy()) for a in shard_logits]
            label_diff=int(np.count_nonzero(logits[mask].argmax(1)!=before[mask].argmax(1)))
            row.update(before_reproduced_from_initial_checkpoint=True,
                checkpoint_file_sha256=loaded['file_sha256'],num_shards=len(w),
                recomputed_ensemble_before=acc(logits),recomputed_uniform_before=acc(uniform),
                per_shard_before=shard_metrics,weights=w.tolist(),
                max_abs_logit_diff=float(np.max(np.abs(logits-before))),test_argmax_mismatches=label_diff,
                train_nodes_per_shard=[int(((state['assignment']==i)&data.train_mask).sum()) for i in range(len(w))])
            assert label_diff==0, ('initial checkpoint disagrees',row)
        records.append(row)
        print(f"checked {ds} {cond['method']} seed {cond['training_seed']}",file=sys.stderr,flush=True)
    result=dict(run_sha256=sha(base/'run.json'),execution_sha=run['commit'],
                current_remote_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                code_checks=code_checks,read_only=True,cpu_threads=2,new_training_runs=0,
                saved_prediction_checks=60,initial_checkpoint_forward_checks=20,records=records)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
