"""Ret-only source replay, passive observation and precommitted endpoint policy."""
import copy
import functools
import hashlib
import json
import random
from pathlib import Path
from cache_v2.store import ArtifactIntegrityError

import numpy as np
import pytest
import torch

from experiments.observers.retrain_validation import RetrainValidationTrace, window_summary, validate_masks
from experiments.c_target_v1.core import train_trajectory, GateGCN, capture_state
from test_modular_consumers import tables, run, write_yaml


def same_state(a, b):
    assert a.keys() == b.keys()
    assert all(torch.equal(a[k], b[k]) for k in a)


def tiny():
    from torch_geometric.data import Data
    torch.set_num_threads(1)
    gen=torch.Generator().manual_seed(3)
    return Data(x=torch.randn(9,3,generator=gen),y=torch.arange(9)%2,
        edge_index=torch.tensor([[0,1,1,2,3,4,5,6,7],[1,0,2,1,4,3,6,5,8]]),
        train_mask=torch.arange(9)<3,val_mask=(torch.arange(9)>=3)&(torch.arange(9)<6),
        test_mask=torch.arange(9)>=6)


def observed_train(data, callback, seed=9, epochs=6):
    from attack.cache_identity import seeded_execution
    with seeded_execution(seed):
        model=GateGCN(3,4,2,.5)
    with seeded_execution(seed):
        torch_rng=torch.get_rng_state().clone()
        _, stats=train_trajectory(model,data,checkpoint_epochs=(),epochs=epochs,lr=.03,
            weight_decay=.001,milestones=(3,),gamma=.5,optimizer_name='adam',epoch_end=callback)
        end_rng=torch.get_rng_state().clone()
    return capture_state(model),end_rng,model,stats


def test_actual_training_observer_is_bitwise_passive_and_test_independent():
    data=tiny()
    plain,rng_plain,_,_=observed_train(data,None)
    obs=RetrainValidationTrace({})
    watched,rng_watched,model,_=observed_train(data,obs)
    same_state(plain,watched)
    assert torch.equal(rng_plain,rng_watched) and model.training
    changed=data.clone();changed.y[changed.test_mask]=1-changed.y[changed.test_mask]
    other=RetrainValidationTrace({})
    final,rng_other,_,_=observed_train(changed,other)
    same_state(watched,final);same_state(obs.best_state,other.best_state)
    assert obs.rows==other.rows and obs.best==other.best
    assert torch.equal(rng_watched,rng_other)


class Controlled(torch.nn.Module):
    def __init__(self):
        super().__init__();self.weight=torch.nn.Parameter(torch.tensor(0.));self.epoch=1
    def forward(self,x,edges):
        # Consume every RNG to prove the observation restores them.
        random.random();np.random.random();torch.rand(2)
        logits=torch.zeros(len(x),3);logits[:,0 if self.epoch==1 else 1]=4
        return logits


def controlled(labels):
    data=tiny();data.y[data.val_mask]=labels
    observer=RetrainValidationTrace({});model=Controlled()
    for epoch in (1,2,3):
        model.epoch=epoch
        with torch.no_grad():model.weight.fill_(epoch)
        before=(random.getstate(),np.random.get_state(),torch.get_rng_state().clone())
        observer({'phase':'epoch_end','step':epoch,'values':{'model':model,'data':data,'train_loss':1.,'update_lr':.1}})
        assert random.getstate()==before[0]
        after=np.random.get_state();assert after[0]==before[1][0] and np.array_equal(after[1],before[1][1]) and after[2:]==before[1][2:]
        assert torch.equal(torch.get_rng_state(),before[2]) and model.training
    return observer


def test_validation_decides_earliest_best_and_zero_score_still_saves():
    first=controlled(0);second=controlled(1);zero=controlled(2)
    assert first.best['epoch']==1 and second.best['epoch']==2 and zero.best['epoch']==1
    assert first.best_state['weight']==1 and second.best_state['weight']==2
    assert zero.best['accuracy']==0


def rows(before,after):
    return [dict(epoch=i,train_loss=1.,validation_cross_entropy=before if i<=2500 else after,
        validation_accuracy=.5,update_lr=.1) for i in range(1,3001)]


def test_exact_windows_thresholds_and_zero_denominator():
    r=rows(1.,1.1)
    # Epoch 2000 is excluded; the complete 2001..2500 and 2501..3000 are consumed.
    r[1999]['validation_cross_entropy']=9000.
    result=window_summary(r,{'accuracy':.5})
    assert result['ce_2001_2500']==1. and result['ce_2501_3000']==pytest.approx(1.1)
    assert result['ce_trigger']
    assert window_summary(rows(0.,0.),{'accuracy':.51})['accuracy_trigger']
    assert not window_summary(rows(0.,0.),{'accuracy':.5})['ce_trigger']
    assert window_summary(rows(0.,.1),{'accuracy':.5})['ce_relative_increase_status']=='zero_to_positive'
    with pytest.raises(ValueError,match='exactly'):window_summary(r[:-1],{'accuracy':.5})
    r[2500]['validation_cross_entropy']=float('nan')
    with pytest.raises(ValueError,match='nonfinite'):window_summary(r,{'accuracy':.5})


@pytest.mark.parametrize('invalid',['empty','overlap','dtype'])
def test_validation_masks_fail_before_training(invalid):
    d=tiny()
    if invalid=='empty':d.val_mask[:]=False
    elif invalid=='overlap':d.val_mask[0]=True
    else:d.val_mask=d.val_mask.long()
    with pytest.raises(ValueError,match='masks'):validate_masks(d)


def test_bad_epoch_nonfinite_and_incomplete_observer_rejected(tmp_path):
    model=Controlled();d=tiny();o=RetrainValidationTrace({})
    event={'phase':'epoch_end','step':2,'values':dict(model=model,data=d,train_loss=1.,update_lr=.1)}
    with pytest.raises(ValueError,match='order'):o(event)
    event['step']=1;event['values']['train_loss']=float('nan')
    with pytest.raises(ValueError,match='nonfinite'):o(event)
    with pytest.raises(ValueError,match='completed'):o.save(tmp_path,{'status':'completed'})


@pytest.fixture
def source_ret(tables):
    from experiments.modular_config import load_instance
    from experiments.modular_artifacts import read_run
    root=tables[0]
    write_yaml(root/'ret.yaml',dict(kind='unlearning',schema_version=1,method='Retrain',
        model=dict(architecture='OpenGU.GCNNet',hidden_channels=4),training=dict(epochs=3000)))
    result=run(tables,'source-ret',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['ret.yaml'])
    path=root/'results/runs/source-ret/source-ret/run.json'
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    actual,_=read_run(path,digest)
    return root,dict(run=str(path),sha256=digest,cell_ids=[actual['cells'][0]['cell_id']]),actual


def forbid(*a,**k):raise AssertionError('Selector, Original or GU dispatch executed')


def test_actual_3000_epoch_source_to_diagnostic_export_and_readback(source_ret,tables,monkeypatch,record_property):
    from experiments.modular_artifacts import read_run,output_paths
    from experiments.modular_config import load_experiment
    from experiments.unlearning_outputs import load_output
    root,source,old=source_ret
    before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'results/cache_v2/artifacts').rglob('*') if p.is_file()}
    monkeypatch.setattr('experiments.modular_run.prepare_model',forbid)
    monkeypatch.setattr('experiments.modular_run.resolve_methods',forbid)
    monkeypatch.setattr('experiments.modular_model.prepare_model',forbid)
    import experiments.modular_gu as gu
    for method,fn in gu.GU_METHODS.items():monkeypatch.setitem(gu.GU_METHODS,method,functools.wraps(fn)(forbid))
    result=run(tables,'ret-diagnostic',stage='retrain_diagnostics',selector_refs=[],output_inputs=[source])
    path=root/'results/runs/ret-diagnostic/ret-diagnostic/run.json'
    document,files=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    cell=document['cells'][0]
    assert 'output' not in cell and cell['source']['output']==old['cells'][0]['output']
    assert cell['producer_called']==dict(selection=False,original=False,method=True)
    trace=[json.loads(line) for line in files[0]['observers/retrain_validation_trace/trace.jsonl'].decode().splitlines()]
    observed=json.loads(files[0]['observers/retrain_validation_trace/result.json'])
    d=observed['diagnostics']
    assert len(trace)==3000 and d['final']['epoch']==3000
    assert d['validation_graph']=='retained' and d['test_policy']=='fixed_best_and_final_only'
    assert d['old_final_comparison']['state_hash_equal'] is True
    assert d['old_final_comparison']['all_node_prediction_changes']==0
    assert d['old_final_comparison']['maximum_absolute_logit_error']==0
    old_payload=load_output(old['cells'][0]['output'],root/'results/cache_v2',dataset_root=root)
    for role in ('best','final'):
        from utils.target_checkpoint import load_weights
        entry=d[role];assert entry['checkpoint_role']==role
        assert load_weights(root/entry['weights']['path'])['state_hash']==entry['state_hash']
        assert hashlib.sha256((root/entry['predictions']['path']).read_bytes()).hexdigest()==entry['predictions']['sha256']
    after={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in before}
    assert before==after
    config=load_experiment(root/'ret-diagnostic.yaml')
    declared=output_paths(path.relative_to(root),config)
    assert len(declared)==4 and all((root/p).is_file() for p in declared)
    record_property('ret_diagnostic',json.dumps({'epochs':3000,'old_final_state_equal':True,
        'old_final_logits_equal':True,'immutable_artifacts_unchanged':True,'collected_files':len(declared)}))


def test_source_and_protocol_errors_do_not_train(source_ret,tables,monkeypatch):
    root,source,old=source_ret
    monkeypatch.setattr('experiments.modular_model.train_supervised',forbid)
    for name,change,error in [('hash',dict(sha256='0'*64),'checksum'),('cell',dict(cell_ids=['bad']),'cell_ids')]:
        with pytest.raises(ValueError,match=error):run(tables,'invalid-'+name,stage='retrain_diagnostics',selector_refs=[],output_inputs=[{**source,**change}])
    with pytest.raises(ValueError,match='exact cell_ids'):
        run(tables,'no-cell',stage='retrain_diagnostics',selector_refs=[],output_inputs=[{k:v for k,v in source.items() if k!='cell_ids'}])
    with pytest.raises(ValueError,match='repeat axes'):
        run(tables,'repeat',stage='retrain_diagnostics',selector_refs=[],output_inputs=[source],seeds=[42])
    with pytest.raises(ValueError,match='only exact'):
        run(tables,'observer-custom',stage='retrain_diagnostics',selector_refs=[],output_inputs=[source],observers=[dict(name='same_graph_change',methods=['Retrain'])])

    # Verified alternative run documents expose mismatches before any optimizer.
    changes = [('non-ret', 'original'), ('seed-conflict', 'conditions'), ('dataset-conflict', 'conditions'), ('bad-output', 'digest')]
    for name, message in changes:
        document=copy.deepcopy(old)
        if name=='non-ret':document['cells'][0]['conditions']['method']='GIF'
        elif name=='seed-conflict':document['cells'][0]['conditions']['seed']+=1
        elif name=='dataset-conflict':document['cells'][0]['conditions']['dataset_fingerprint']='0'*64
        else:document['cells'][0]['output']['content_hash']='0'*64
        changed=Path(source['run']).with_name(name+'.json')
        changed.write_text(json.dumps(document),encoding='utf-8')
        ref={**source,'run':str(changed),'sha256':hashlib.sha256(changed.read_bytes()).hexdigest()}
        with pytest.raises(ValueError,match=message):
            run(tables,'reject-'+name,stage='retrain_diagnostics',selector_refs=[],output_inputs=[ref])
    payload=root/'results/cache_v2/artifacts/prediction'/old['cells'][0]['output']['artifact_id']/'payload.npz'
    payload.unlink()
    with pytest.raises(ArtifactIntegrityError,match='cached payload is missing'):
        run(tables,'missing-payload',stage='retrain_diagnostics',selector_refs=[],output_inputs=[source])


def test_registered_retrain_audit_stage_is_not_attack():
    from scripts.evaluation.reporting.events import build_event, make_cell_id
    from scripts.evaluation.reporting.summary import _derive_state, _stage_summary
    identity=dict(dataset='fixture',model='GCN',method='Retrain',strategy='degree',ratio=.33,seed=42)
    event=build_event(identity=identity,stage='retrain_diagnostics',state='completed',producer='test',
        config_fingerprint='fixture',git_sha='fixture',cell_id=make_cell_id(identity),run_id='run_fixture')
    assert event['stage']=='retrain_diagnostics'
    assert _derive_state([event])=='retrain-diagnosed'
    assert _stage_summary([event])=='retrain_diagnostics=completed'
