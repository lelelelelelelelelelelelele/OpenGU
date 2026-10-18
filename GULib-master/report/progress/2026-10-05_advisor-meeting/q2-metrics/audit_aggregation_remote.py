"""Frozen-checkpoint exploratory control, never a formal GraphRevoker rerun.

Supply AUDIT (before_audit.json) and UPSTREAM (method_upstream_sources.json)
before this source on python -B stdin. All fits are CPU/in-memory. No files,
checkpoints, artifacts, dataset copies, or cache entries are written remotely.
Fixed: Cora ten existing seeds, sample 1000 train nodes, 20 epochs, AdamW
lr=.01 / decay=1e-5, batch512, upstream ContraAggr (128/16), aux=0 or 1e-4.
Test/validation outcomes are observed only after the fixed final epoch.
"""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import ast
import copy
import hashlib
import io
import json
import random
import signal
import sqlite3
import subprocess
import sys
import time
import zipfile
from pathlib import Path
signal.alarm(900)
ROOT = Path('/autodl-fs/data/OpenGU/GULib-master')
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
import numpy as np
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch_geometric.utils import subgraph, to_dense_adj
torch.set_num_threads(2)
from experiments.dataset_inputs import resolve_input
from experiments.modular_model import create_model
from experiments.modular_shards import ShardEnsemble
from utils.target_checkpoint import load_weights, data_identity, capture_state, state_hash
from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.contra_aggregator_v2 import ContraAggr, ContrastiveAggregator
from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.opt_dataset import NegSamplingDataset

def sha(b): return hashlib.sha256(b).hexdigest()
def seed(n):
    random.seed(n); np.random.seed(n); torch.manual_seed(n)
def metric(logits, labels):
    return dict(accuracy=float((logits.argmax(-1)==labels).double().mean())*100,
                cross_entropy=float(F.cross_entropy(logits,labels)))

# Bind actual consumed code, including classes verified against pinned upstream.
source_paths=['experiments/modular_shards.py','experiments/modular_model.py',
    'model/base_gnn/gcn.py','unlearning/unlearning_methods/GraphRevoker/lib_aggregator/contra_aggregator_v2.py',
    'unlearning/unlearning_methods/GraphRevoker/lib_aggregator/opt_dataset.py']
code={p:sha((ROOT/p).read_bytes()) for p in source_paths}
for p, expected in LOCAL_SOURCE_HASHES.items():
    assert sha((ROOT/p).read_text(encoding='utf-8').encode())==expected,p
for p in source_paths[:3]:
    frozen=subprocess.check_output(['git','show',AUDIT['execution_sha']+':GULib-master/'+p]).decode('utf-8')
    current=(ROOT/p).read_text(encoding='utf-8')
    names={'experiments/modular_shards.py':['ShardEnsemble'],
           'experiments/modular_model.py':['create_model'], 'model/base_gnn/gcn.py':['GCNNet']}[p]
    for name in names:
        def node(s):return ast.dump(next(n for n in ast.parse(s).body if getattr(n,'name',None)==name))
        assert node(frozen)==node(current),(p,name)
contra=next(f for f in UPSTREAM['files'] if f['path'].endswith('/contra_aggregator_v2.py'))
assert all(c['ast_equal'] for c in contra['local_definitions'])
store=ROOT/'results/cache_v2'
con=sqlite3.connect((store/'index.sqlite').as_uri()+'?mode=ro',uri=True)
con.row_factory=sqlite3.Row
results=[]
started=time.perf_counter()
for old in AUDIT['records']:
    if old['dataset']!='Cora' or old['method']!='GraphRevoker':continue
    row_start=time.perf_counter()
    ref=old['output']; db=dict(con.execute('select * from artifacts where artifact_id=?',(ref['artifact_id'],)).fetchone())
    assert all(db[k]==v for k,v in ref.items())
    assert db['status']=='valid' and db['verification_status']=='verified'
    p=store/db['semantic_path'];assert p.resolve().is_relative_to(store.resolve())
    assert sha(p.read_bytes())==ref['content_hash']
    with zipfile.ZipFile(p) as z:
        identity=json.loads(z.read('metadata.json'))['identity']
        saved=np.load(io.BytesIO(z.read('arrays__logits_before.npy')),allow_pickle=False)
    data=resolve_input(identity['dataset_input'],ROOT).cpu()
    assert data_identity(data)==identity['pairing']['data_identity']
    cp=Path(old['checkpoint']);assert cp.resolve().is_relative_to((ROOT/'results/runtime/modular/checkpoints').resolve())
    loaded=load_weights(cp)
    assert loaded['file_sha256']==old['checkpoint_file_sha256']
    assert loaded['state_hash']==old['initial_ensemble_state_hash']
    state=loaded['state_dict'];w=state['weights']; assignment=state['assignment']
    ensemble=ShardEnsemble([create_model(old['checkpoint_metadata']['model'],'shard',data,torch.device('cpu')) for _ in w],assignment,w)
    ensemble.load_state_dict({k:v for k,v in state.items() if k in ['weights','assignment'] or k.startswith('shard_models.')},strict=True)
    ensemble.eval()
    for parameter in ensemble.parameters():parameter.requires_grad_(False)
    frozen_hash=state_hash(capture_state(ensemble))
    diagnostic_seed=9000+old['seed']; seed(diagnostic_seed)
    nodes=data.train_mask.nonzero().flatten()
    nodes=nodes[torch.tensor(np.random.choice(len(nodes),1000,replace=False))].sort().values
    assert data.train_mask[nodes].all() and not data.test_mask[nodes].any() and not data.val_mask[nodes].any()
    edges,_=subgraph(nodes,data.edge_index,relabel_nodes=True,num_nodes=data.num_nodes)
    train_features=[];test_features=[];val_features=[];individual=[]
    with torch.no_grad():
        for i,model in enumerate(ensemble.shard_models):
            _,f=model(data.x[nodes],edges,return_feature=True)
            train_features.append(f.detach())
            allowed=(assignment==i)|(assignment<0)
            keep=allowed[data.edge_index[0]]&allowed[data.edge_index[1]]
            logits,f=model(data.x,data.edge_index[:,keep],return_feature=True)
            test_features.append(f[data.test_mask].detach())
            val_features.append(f[data.val_mask].detach())
            individual.append(F.log_softmax(logits,dim=-1))
        baseline=sum(a*b for a,b in zip(w,individual))
        assert np.array_equal(baseline[data.test_mask].argmax(-1).numpy(),saved[data.test_mask.numpy()].argmax(-1))
    features={i:f for i,f in enumerate(train_features)}
    adj=to_dense_adj(edges,max_num_nodes=len(nodes))[0]
    seed(diagnostic_seed)
    ds=NegSamplingDataset(features,data.y[nodes],adj,assignment[nodes].numpy())
    assert data.y[nodes].unique().numel()==7
    # Use existing upstream mask construction; its 19 replacement draws are recorded.
    masks=ContrastiveAggregator._generate_mask(type('MaskContext',(),{'args':{'num_shards':10},'device':torch.device('cpu')})(),19,512)
    seed(diagnostic_seed)
    initial=ContraAggr(10,train_features[0].shape[-1],128,16,7)
    fit_results={}
    for mode,aux in [('attention_ce_only',0.),('attention_contrastive_reconstruction',1e-4)]:
        seed(diagnostic_seed)
        head=copy.deepcopy(initial)
        opt=torch.optim.AdamW(head.parameters(),lr=.01,weight_decay=1e-5)
        loader=DataLoader(ds,batch_size=512,shuffle=True,num_workers=0,
            generator=torch.Generator().manual_seed(diagnostic_seed))
        losses=[]
        for epoch in range(20):
            head.train();total=0.
            for e,cn,tp,tn,y,_ in loader:
                opt.zero_grad()
                out,cl,tl=head(e,cn,tp,tn,masks[:len(y)])
                loss=F.cross_entropy(out,y)+aux*(cl+tl)
                assert torch.isfinite(loss),(old['seed'],mode,epoch)
                loss.backward();opt.step();total+=float(loss.detach())*len(y)
            losses.append(total/len(ds))
        head.eval()
        with torch.no_grad():
            fit_results[mode]=dict(
                train=metric(head(torch.stack(train_features,1),is_eval=True),data.y[nodes]),
                validation=metric(head(torch.stack(val_features,1),is_eval=True),data.y[data.val_mask]),
                test=metric(head(torch.stack(test_features,1),is_eval=True),data.y[data.test_mask]),
                loss_by_epoch=losses)
        assert state_hash(capture_state(ensemble))==frozen_hash
    result=dict(seed=old['seed'],diagnostic_seed=diagnostic_seed,output=ref,
        initial_checkpoint_state_hash=loaded['state_hash'],initial_checkpoint_file_sha256=loaded['file_sha256'],
        train_sample_sha256=sha(nodes.numpy().tobytes()),train_sample_count=len(nodes),
        baseline=metric(baseline[data.test_mask],data.y[data.test_mask]),
        shard_weights_unchanged=True,results=fit_results,seconds=time.perf_counter()-row_start)
    results.append(result)
    print(json.dumps({'seed':old['seed'],'baseline':result['baseline']['accuracy'],
        **{k:v['test']['accuracy'] for k,v in fit_results.items()},'seconds':result['seconds']}),file=sys.stderr,flush=True)
assert len(results)==10
print(json.dumps(dict(kind='exploratory frozen-shard aggregation control',
    remote_files_written=False,formal_results_replaced=False,new_shard_training_runs=0,
    new_in_memory_aggregation_fits=20,cpu_threads=2,epochs=20,optimizer='AdamW',lr=.01,weight_decay=1e-5,
    batch_size=512,projection_dim=128,attention_dim=16,mask_draws_with_replacement=19,
    original_execution_sha=AUDIT['execution_sha'],upstream_repository_sha=UPSTREAM['commit'],
    remote_sha=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),code_sha256=code,
    data_identity=data_identity(data),wall_seconds=time.perf_counter()-started,records=results),indent=2))
