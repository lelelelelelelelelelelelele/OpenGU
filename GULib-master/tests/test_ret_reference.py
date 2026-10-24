"""Real CPU execution for independently identified deterministic Ret references."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from experiments.ret_reference_policy import DETERMINISTIC


@pytest.fixture(autouse=True)
def policy_isolation(monkeypatch):
    import experiments.ret_reference_policy as policy
    old = policy.backend_settings()
    monkeypatch.setattr(policy, '_configured', None)
    monkeypatch.delenv('CUBLAS_WORKSPACE_CONFIG', raising=False)
    yield
    torch.use_deterministic_algorithms(old['deterministic_algorithms'], warn_only=old['deterministic_warn_only'])
    torch.backends.cudnn.deterministic = old['cudnn_deterministic']
    torch.backends.cudnn.benchmark = old['cudnn_benchmark']
    torch.backends.cuda.matmul.allow_tf32 = old['matmul_tf32']
    torch.backends.cudnn.allow_tf32 = old['cudnn_tf32']


def reference_config(tables, arms=('joint',)):
    root, base, gu = tables
    refs=[]
    for arm in arms:
        ref='ret-'+arm+'.yaml'; refs.append(ref)
        write_yaml(root/ref, {**gu,'method':'Retrain','parameters':{},
            'training':{'epochs':3000},'reference':{'policy':DETERMINISTIC,'arm':arm}})
    return dict(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=refs,
        execution={'gu_cache':{'Retrain':'disabled'}},
        observers=[{'name':'ret_reference_trace','methods':['Retrain']}])


def test_minimal_reference_runs_and_exports(tables, record_property):
    root,_,_=tables
    run(tables,'prepare',selector_refs=['degree.yaml'])
    result=run(tables,'ret-new',**reference_config(tables))
    path=root/'results/runs/ret-new/ret-new/run.json'
    from experiments.modular_artifacts import read_run
    manifest,documents=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    cell=manifest['cells'][0]
    saved=json.loads(documents[0]['observers/ret_reference_trace/result.json'])
    replay=saved['diagnostics']['replays'][0]
    assert cell['cache']['method']=='disabled'
    assert replay['identity']['arm']=='joint'
    assert replay['identity']['environment']['backend']['deterministic_algorithms']
    assert replay['prior_comparison'] is None
    assert replay['endpoints']['final']['epoch']==3000
    assert len(saved['events'])>=3002
    from utils.target_checkpoint import load_weights
    for role in ('best','final'):
        end=replay['endpoints'][role]
        assert load_weights(root/end['weights']['path'])['state_hash']==end['state_hash']
        for graph in ('original','retained'):
            entry=end['probes'][graph]
            assert hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()==entry['sha256']
    from experiments.ret_reference_reading import load_endpoints,validate_trace
    hook=torch.nn.modules.module.register_module_forward_pre_hook(lambda *a:pytest.fail('read-only endpoint loader forwarded'))
    try:
        loaded=load_endpoints(path,hashlib.sha256(path.read_bytes()).hexdigest(),cell['cell_id'],
                             dataset_root=root,store_root=root/'results/cache_v2')
    finally:hook.remove()
    assert loaded['mode']=='read_only_no_forward'
    reference=cell['observers'][0]
    trace=documents[0]['observers/ret_reference_trace/trace.jsonl']
    for fault in ('identity','backend','late_best','final_rng','endpoints','truncated'):
        changed=copy.deepcopy(saved); damaged_trace=trace
        r=changed['diagnostics']['replays'][0]
        if fault=='identity':changed['identity']['cell_id']='wrong'
        elif fault=='backend':r['identity']['environment']['backend']['deterministic_warn_only']=True
        elif fault=='late_best':r['validation_best']['epoch']+=1
        elif fault=='final_rng':r['final_rng']['cpu']='0'*64
        elif fault=='endpoints':del r['endpoints']['final']
        else:damaged_trace=b'\n'.join(trace.splitlines()[:-1])+b'\n'
        with pytest.raises((ValueError,KeyError)):
            validate_trace(changed,damaged_trace,reference,cell)
    logit_path=root/replay['endpoints']['best']['probes']['original']['path']
    original=logit_path.read_bytes();logit_path.write_bytes(b'bad')
    with pytest.raises(ValueError,match='checksum'):
        load_endpoints(path,hashlib.sha256(path.read_bytes()).hexdigest(),cell['cell_id'],dataset_root=root,store_root=root/'results/cache_v2')
    logit_path.write_bytes(original)
    record_property('ret_new',json.dumps({'epochs':3000,'source_free':True,'checkpoints':'pure_state_dict',
        'probes':['original','retained'],'final_state':replay['endpoints']['final']['state_hash']}))


@pytest.mark.parametrize('policy',[DETERMINISTIC,'ret-observed-v1'])
def test_source_probe_exact_repeats(tables,monkeypatch,record_property,policy):
    root,_,gu=tables
    write_yaml(root/'oldret-instance.yaml',{**gu,'method':'Retrain','parameters':{},'training':{'epochs':3000}})
    run(tables,'oldret',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['oldret-instance.yaml'])
    source=root/'results/runs/oldret/oldret/run.json'
    import experiments.modular_run as runner
    def forbidden(*a,**kw):raise AssertionError('source-bound reference attempted producer')
    monkeypatch.setattr(runner,'prepare_model',forbidden)
    monkeypatch.setattr(runner,'resolve_methods',forbidden)
    result=run(tables,'probe',stage='retrain_diagnostics',selector_refs=[],
        output_inputs=[{'run':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'cell_ids':[json.loads(source.read_text(encoding='utf-8'))['cells'][0]['cell_id']]}],
        ret_reference={'policy':policy,'mode':'probe','arms':['joint']})
    from experiments.modular_artifacts import read_run
    path=root/'results/runs/probe/probe/run.json'
    manifest,docs=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    saved=json.loads(docs[0]['observers/ret_reference_trace/result.json'])
    diagnostics=saved['diagnostics']
    assert [r['repeat'] for r in diagnostics['replays']]==['off1','off2','on1','on2']
    assert len(docs[0]['observers/ret_reference_trace/trace.jsonl'].splitlines())==12000
    for r in diagnostics['probe_comparisons']:
        assert all(r[k] for k in ('initial_state_equal','initial_rng_equal','final_state_equal','final_rng_equal'))
        assert r['all_node_prediction_changes']==0 and r['maximum_absolute_logit_error']==0
    assert all(r['prior_comparison']['state_hash_equal'] for r in diagnostics['replays'])
    assert manifest['cells'][0]['producer_called']=={'selection':False,'original':False,'method':True}
    assert diagnostics['replays'][0]['validation_best'] is None
    assert diagnostics['replays'][2]['validation_best']['epoch']<=3000
    record_property('cpu_probe',json.dumps(diagnostics['probe_comparisons']))


def test_four_arms_and_common_validation(tables,record_property):
    root,_,_=tables
    from experiments.ret_reference_policy import ARMS
    run(tables,'prepare',selector_refs=['degree.yaml'])
    run(tables,'arms',**reference_config(tables,ARMS))
    from experiments.modular_artifacts import read_run
    path=root/'results/runs/arms/arms/run.json'
    manifest,docs=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    replays=[json.loads(d['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0] for d in docs]
    assert [r['identity']['arm'] for r in replays]==list(ARMS)
    assert len({r['initial_state_hash'] for r in replays})==1
    assert len({json.dumps(r['identity']['validation_graph_identity'],sort_keys=True) for r in replays})==1
    graphs=[r['identity']['training_graph_identity'] for r in replays]
    assert graphs[0]['split_hash']==graphs[1]['split_hash']!=graphs[2]['split_hash']==graphs[3]['split_hash']
    assert graphs[0]['edge_index_hash']==graphs[2]['edge_index_hash']!=graphs[1]['edge_index_hash']==graphs[3]['edge_index_hash']
    assert len({c['output']['recipe_hash'] for c in manifest['cells']})==4
    assert all(c['cache']['method']=='disabled' for c in manifest['cells'])
    import yaml
    selector=yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    selector['budget']['value']=2
    write_yaml(root/'degree.yaml',selector)
    run(tables,'prepare-second',selector_refs=['degree.yaml'])
    run(tables,'none-second-request',**reference_config(tables,('none',)))
    second=root/'results/runs/none-second-request/none-second-request/run.json'
    _,docs2=read_run(second,hashlib.sha256(second.read_bytes()).hexdigest())
    other=json.loads(docs2[0]['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0]
    assert other['endpoints']['final']['state_hash']==replays[-1]['endpoints']['final']['state_hash']
    assert other['identity']['validation_graph_identity']!=replays[-1]['identity']['validation_graph_identity']
    record_property('factorial',json.dumps([r['identity'] for r in replays]))


def test_none_final_external_original_and_joint_metrics(tables,monkeypatch,record_property):
    root,_,gu=tables
    run(tables,'prepare',selector_refs=['degree.yaml'])
    run(tables,'newrefs',**reference_config(tables,('joint','none')))
    from experiments.modular_artifacts import read_run
    from experiments.response_graph_sensitivity import CASE, restore_original
    from experiments.unlearning_outputs import load_output
    refpath=root/'results/runs/newrefs/newrefs/run.json'
    refs,docs=read_run(refpath,hashlib.sha256(refpath.read_bytes()).hexdigest())
    none=json.loads(docs[1]['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0]
    weights=root/none['endpoints']['final']['weights']['path']
    for method in ('GIF','MEGU'):
        write_yaml(root/(method+'.yaml'),{**gu,'method':method,'parameters':{},'training':{'seed':42},'checkpoint':str(weights)})
    run(tables,'external-gu',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['GIF.yaml','MEGU.yaml'])
    gupath=root/'results/runs/external-gu/external-gu/run.json'
    gus,_=read_run(gupath,hashlib.sha256(gupath.read_bytes()).hexdigest())
    assert all(c['cache_provenance']['original_checkpoint']['state_hash']==none['endpoints']['final']['state_hash'] for c in gus['cells'])
    import experiments.modular_run as runner
    import experiments.modular_model as modeling
    import functools
    def forbidden(*a,**kw):raise AssertionError('Metrics trained or selected')
    for module,name in ((runner,'prepare_model'),(runner,'resolve_methods'),(modeling,'train_supervised')):
        monkeypatch.setattr(module,name,functools.wraps(getattr(module,name))(forbidden))
    write_yaml(root/'twograph.yaml',dict(kind='evaluation',schema_version=1,case=CASE))
    inputs=[dict(run=str(gupath),sha256=hashlib.sha256(gupath.read_bytes()).hexdigest()),
            dict(run=str(refpath),sha256=hashlib.sha256(refpath.read_bytes()).hexdigest(),cell_ids=[refs['cells'][0]['cell_id']])]
    measured=run(tables,'external-analysis',stage='metrics',selector_refs=[],output_inputs=inputs,evaluation_refs=['twograph.yaml'])
    rows=measured['evaluations'][0]['rows']
    assert len(rows)==2 and all(r['identity']['protocol']['checkpoint']['source']=='external_state_dict' for r in rows)
    assert all(r['metrics']['original_graph_raw_node_count']==5 for r in rows)
    from experiments.ret_reference_reading import load_endpoints
    from experiments.response_diagnostics import prediction_triangle,RELATIONS,CORRECTNESS
    endpoints=load_endpoints(refpath,hashlib.sha256(refpath.read_bytes()).hexdigest(),refs['cells'][0]['cell_id'],
                             dataset_root=root,store_root=root/'results/cache_v2')
    direct=[]
    for c in gus['cells']:
        current=load_output(c['output'],root/'results/cache_v2',dataset_root=root)
        a=current.arrays; mask=a['test_mask']
        for role in ('best','final'):
            logits=endpoints['endpoints']['reference'][role]['logits']['original']
            m=prediction_triangle(a['logits_before'][mask],a['logits'][mask],logits[mask],a['y'][mask])
            assert sum(m[r+'_count'] for r in RELATIONS)==m['node_count']==5
            assert sum(m[r+'_correct_'+bits+'_count'] for r in RELATIONS for bits in CORRECTNESS if bits[2]=='1')/5==m['retrain_accuracy']
            assert sum(m[r+'_count'] for r in ('original_gu_equal','original_retrain_equal','all_different'))==m['gu_retrain_disagreement_count']
            direct.append(dict(method=c['conditions']['method'],endpoint=role,metrics=m))
    output=load_output(gus['cells'][0]['output'],root/'results/cache_v2',dataset_root=root)
    import pickle
    data=pickle.loads((root/'graph.pkl').read_bytes())
    original=gus['cells'][0]['cache_provenance']['original_checkpoint']
    for damage in ('missing','file_hash','state','dataset','model','seed','path'):
        receipt=copy.deepcopy(original)
        if damage=='missing':receipt=None
        elif damage=='file_hash':receipt['file_sha256']='0'*64
        elif damage=='state':receipt['state_hash']='0'*64
        elif damage=='path':receipt['path']=str(root/'missing.pt')
        elif damage=='dataset':receipt['effective_identity']['data_identity']['features_hash']='0'*64
        elif damage=='model':receipt['effective_identity']['model']['hidden_channels']=99
        else:receipt['effective_identity']['execution_seed']+=1
        with pytest.raises((ValueError,FileNotFoundError)):
            restore_original(output,data,root/'checkpoints','cpu',receipt)
    record_property('external_original',json.dumps(dict(methods=['GIF','MEGU'],graphs=['original','retained'],
        none_final_state=none['endpoints']['final']['state_hash'],faults=7,training_forbidden=True,direct_best_final=direct)))


def test_test_labels_do_not_select_or_train_and_callbacks_preserve_state(tables,record_property):
    import pickle
    from experiments.modular_config import load_instance
    from experiments.ret_reference_policy import configure_for_experiment
    from experiments.ret_reference_training import train_reference
    from experiments.observers import ObserverSession
    from experiments.observers.ret_reference import rng_identity
    from utils.target_checkpoint import state_hash
    root,_,_=tables
    reference_config(tables)
    instance=load_instance(root/'ret-joint.yaml','unlearning')
    configure_for_experiment({'unlearnings':[instance]})
    data=pickle.loads((root/'graph.pkl').read_bytes())
    checks=[]
    class Checked(ObserverSession):
        def __call__(self,event):
            if event['phase']!='epoch_end':return super().__call__(event)
            model=event['values']['model']
            state=state_hash(model.state_dict());rng=rng_identity(model)
            modes=[m.training for m in model.modules()]
            gradients=[None if p.grad is None else p.grad.clone() for p in model.parameters()]
            super().__call__(event)
            assert state_hash(model.state_dict())==state and rng_identity(model)==rng
            assert [m.training for m in model.modules()]==modes
            assert all((p.grad is None and g is None) or torch.equal(p.grad,g) for p,g in zip(model.parameters(),gradients))
            checks.append(event['step'])
    results=[]
    for i in range(2):
        graph=data.clone()
        if i:graph.y[graph.test_mask]=1-graph.y[graph.test_mask]
        observer=Checked([dict(name='ret_reference_trace',parameters={})],root/('observed'+str(i)),{})
        train_reference(instance,graph,[1],'cpu_fixture',observer=observer,
                        asset_root=root/('assets'+str(i)),dataset_root=root)
        results.append(observer.items[0][1].result['replays'][0])
    assert len(checks)==6000
    for role in ('final','best'):
        assert results[0]['endpoints'][role]['state_hash']==results[1]['endpoints'][role]['state_hash']
        assert results[0]['endpoints'][role]['epoch']==results[1]['endpoints'][role]['epoch']
    assert results[0]['validation_best']==results[1]['validation_best']
    record_property('passive_labels',json.dumps(dict(callbacks=6000,state_rng_grad_modes_unchanged=True,
        changed_test_labels=True,best_and_final_equal=True)))


@pytest.mark.parametrize('damage',['cache','missing_policy','unknown_arm','observed_reference','epochs','retained_primary','mixed_gu'])
def test_invalid_reference_configuration_fails_before_execution(tables,damage):
    import yaml
    root,base,_=tables
    config=reference_config(tables)
    item=yaml.safe_load((root/'ret-joint.yaml').read_text(encoding='utf-8'))
    if damage=='cache':config['execution']['gu_cache']['Retrain']='reuse'
    elif damage=='missing_policy':del item['reference']
    elif damage=='unknown_arm':item['reference']['arm']='arbitrary'
    elif damage=='observed_reference':item['reference']['policy']='ret-observed-v1'
    elif damage=='epochs':item['training']['epochs']=2999
    elif damage=='retained_primary':item['deletion']={'evaluation_graph':'retained'}
    else:config['unlearning_refs'].append('gu.yaml')
    write_yaml(root/'ret-joint.yaml',item)
    write_yaml(root/'invalid.yaml',{**base,**config})
    from experiments.modular_run import execute
    with pytest.raises(ValueError):execute(root/'invalid.yaml',dry_run=True)
    assert not (root/'results').exists()


def test_determinism_configuration_conflicts_fail_closed(monkeypatch):
    import experiments.ret_reference_policy as p
    config={'ret_reference':{'policy':DETERMINISTIC,'mode':'probe','arms':['joint']}}
    monkeypatch.setattr(torch.cuda,'is_initialized',lambda:True)
    with pytest.raises(ValueError,match='before CUDA'):p.configure_for_experiment(config)
    monkeypatch.setattr(torch.cuda,'is_initialized',lambda:False)
    monkeypatch.setenv('CUBLAS_WORKSPACE_CONFIG',':16:8')
    with pytest.raises(ValueError,match='CUBLAS'):p.configure_for_experiment(config)
    monkeypatch.delenv('CUBLAS_WORKSPACE_CONFIG')
    p.configure_for_experiment(config)
    torch.use_deterministic_algorithms(True,warn_only=True)
    with pytest.raises(ValueError,match='readback'):p.configure_for_experiment(config)


@pytest.mark.parametrize('missing',['score','selection','proxy'])
def test_reference_assets_miss_never_runs_producer(tables,missing):
    import yaml
    root,_,_=tables
    config=reference_config(tables)
    if missing=='selection':
        run(tables,'prepared-one',selector_refs=['degree.yaml'])
        selector=yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
        selector['budget']['value']=2
        write_yaml(root/'degree.yaml',selector)
    elif missing=='proxy':
        config['selector_refs']=['r_point.yaml']
    with pytest.raises(Exception,match='(?i)score|selection|checkpoint MISS'):
        run(tables,'reference-miss',**config)
    saved=json.loads((root/'results/runs/reference-miss/reference-miss/run.json').read_text(encoding='utf-8'))
    assert saved['status']=='failed'
    assert not list((root/'runtime/reference-miss').rglob('*.pt'))
    assert not list((root/'checkpoints').glob('*.pt'))


def test_prepared_proxy_score_selection_exact_hit(tables,monkeypatch,record_property):
    import yaml
    import functools
    root,_,_=tables
    selector=yaml.safe_load((root/'r_point.yaml').read_text(encoding='utf-8'))
    selector['parameters']={'lissa':{'iterations':2,'scale':25.,'damp':.01}}
    write_yaml(root/'r_point.yaml',selector)
    prepared=run(tables,'prepared-proxy',selector_refs=['r_point.yaml'])['selectors'][0]
    import experiments.modular_model as modeling
    train=modeling.train_supervised
    def forbidden(*a,**kw):
        if kw.get('epoch_end') is None:raise AssertionError('Ret reference retrained its proxy')
        return train(*a,**kw)
    monkeypatch.setattr(modeling,'train_supervised',functools.wraps(modeling.train_supervised)(forbidden))
    config=reference_config(tables);config['selector_refs']=['r_point.yaml']
    result=run(tables,'prepared-reference',**config)['selectors'][0]
    assert result['checkpoint']['hit'] and result['checkpoint']['state_hash']==prepared['checkpoint']['state_hash']
    assert result['selection']['artifact']==prepared['selection']['artifact']
    assert result['score']['recipe_hash']==prepared['score']['recipe_hash']
    assert not result['selection']['cache']['producer_called'] and not result['score']['producer_called']
    record_property('prepared_proxy',json.dumps(dict(checkpoint_hit=True,score_hit=True,selection_hit=True,
        checkpoint_state=result['checkpoint']['state_hash'],selection=result['selection']['artifact'])))


def test_unsupported_training_operation_fails_without_fallback(tables,monkeypatch):
    import functools
    from experiments import ret_reference_training as training
    root,_,_=tables
    run(tables,'prepare',selector_refs=['degree.yaml'])
    def unsupported(*a,**kw):raise RuntimeError('simulated unsupported deterministic operator')
    monkeypatch.setattr(training,'train_supervised',functools.wraps(training.train_supervised)(unsupported))
    with pytest.raises(RuntimeError,match='unsupported deterministic'):
        run(tables,'unsupported',**reference_config(tables))
    path=root/'results/runs/unsupported/unsupported/run.json'
    failed=json.loads(path.read_text(encoding='utf-8'))
    assert failed['status']=='failed'
    files=list(path.parent.rglob('observers/ret_reference_trace/result.json'))
    assert len(files)==1
    diagnostic=json.loads(files[0].read_text(encoding='utf-8'))
    assert diagnostic['status']=='failed' and 'unsupported deterministic' in diagnostic['error']
    assert not list((root/'runtime/unsupported').rglob('*.pt'))
