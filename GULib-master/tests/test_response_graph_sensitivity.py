"""Real saved GCN states, original checkpoints, graph replay and matched C&S."""
import copy
import functools
import hashlib
import json
import pickle
from pathlib import Path

import numpy as np
import pytest
import torch

from test_modular_consumers import tables,run,write_yaml
from experiments.response_graph_sensitivity import CASE,METRICS,graph_sensitivity,reproduce
from experiments.modular_evaluation import evaluate_modular,resolve_evaluation


@pytest.fixture
def prohibit_training(monkeypatch):
    import experiments.modular_model as model
    import experiments.modular_run as entry
    import experiments.modular_gu as gu
    import importlib
    ret=importlib.import_module('unlearning.unlearning_methods.Retrain.retrain')
    def blocked(*args,**kwargs):
        pytest.fail('graph diagnostic invoked training/producer')
    for module,name in ((model,'train_supervised'),(model,'prepare_model'),(entry,'prepare_model'),
                        (entry,'resolve_methods'),(ret,'train_supervised')):
        monkeypatch.setattr(module,name,functools.wraps(getattr(module,name))(blocked))
    for method,fn in gu.GU_METHODS.items():
        monkeypatch.setitem(gu.GU_METHODS,method,functools.wraps(fn)(blocked))
    monkeypatch.setattr(torch.optim.Adam,'step',blocked)
    monkeypatch.setattr(torch.optim.SGD,'step',blocked)


@pytest.fixture
def graph_outputs(tables,prohibit_training):
    from cache_v2 import ArtifactRecipe,ArtifactType,ProducerVersion,canonical_sha256
    from cache_v2.store import ArtifactStore
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.artifact_producer import FormalArtifactRequest,store_formal_artifact
    from experiments.dataset_inputs import bind_input,read_dataset
    from experiments.modular_config import load_instance
    from experiments.modular_gu import gu_producer
    from experiments.node_deletion import pairing_identity,retained_graph
    from experiments.modular_model import create_model
    from experiments.modular_megu import build_megu_output,megu_logits
    from experiments.unlearning_outputs import build_output,output_reference,load_output
    from experiments.checkpoint_references import training_identity
    from utils.target_checkpoint import data_identity,sha256_file,capture_state,save_cached_weights,state_hash
    root=tables[0]
    # A deleted training node sends a strong positive signal to held-out node 15.
    data=pickle.loads((root/'graph.pkl').read_bytes())
    data.x.zero_();data.x[:,0]=-1.;data.x[9,0]=30.
    data.edge_index=torch.cat([data.edge_index,torch.tensor([[9,15],[15,9]])],dim=1)
    (root/'graph.pkl').write_bytes(pickle.dumps(data))
    manifest=json.loads((root/'dataset.json').read_text(encoding='utf-8'))
    manifest.update(data_sha256=sha256_file(root/'graph.pkl'),data_identity=data_identity(data))
    (root/'dataset.json').write_text(json.dumps(manifest),encoding='utf-8')
    dataset=load_instance(root/'dataset.yaml','dataset_split')
    dataset['artifacts']['manifest_sha256']=sha256_file(root/'dataset.json')
    write_yaml(root/'dataset.yaml',dataset)
    data,inputs=read_dataset(dataset,root)
    common=dict(kind='unlearning',schema_version=1,model=dict(architecture='OpenGU.GCNNet',hidden_channels=4),training=dict(epochs=3))
    write_yaml(root/'gif.yaml',dict(common,method='GIF'))
    instance=load_instance(root/'gif.yaml','unlearning')
    original=create_model(instance['model'],'cpu_fixture',data,'cpu').eval()
    with torch.no_grad():
        for parameter in original.parameters():parameter.zero_()
        original.convs[0].lin.weight[0,0]=1.;original.convs[0].lin.weight[1,0]=-1.
        original.convs[1].lin.weight[0,0]=1.;original.convs[1].lin.weight[1,1]=1.
    meta=training_identity(instance,data)
    checkpoint=root/'checkpoints'/(canonical_sha256(meta)+'.pt')
    saved=save_cached_weights(checkpoint,capture_state(original),meta)
    store_root=root/'results/cache_v2'
    store=ArtifactStore(store_root,producer_version=ProducerVersion('graph-fixture','v1'));store.initialize()
    selection_recipe=ArtifactRecipe(dict(artifact_kind='selection',topology_fingerprint=inputs.graph_fingerprint,
        candidate_set_hash=inputs.candidate_set_hash,node_id_space='pyg-global-node-index-v1',selector='degree',
        selector_algorithm_version='graph-fixture',selection_rule='topk_desc',k=1))
    selected=store.store_selection(selection_recipe,[9],num_nodes=data.num_nodes,candidate_nodes=tuple(range(10)),compute_seconds=0.)
    selection=dict(artifact_id=selected.artifact_id,recipe_hash=selection_recipe.recipe_hash,content_hash=selected.content_hash)
    refs=[];sources=[]
    for method in ('GIF','MEGU','Retrain'):
        write_yaml(root/(method+'.yaml'),dict(common,method=method))
        item=load_instance(root/(method+'.yaml'),'unlearning')
        model=copy.deepcopy(original)
        with torch.no_grad():
            if method=='Retrain':model.convs[1].bias[0]+=.5
            else:model.convs[1].bias[1]+=.2
            before=original(data.x,data.edge_index)
            model.megu_pseudo_labels=before.argmax(1)
            logits=(megu_logits(model,data,retained_graph(data,[9]).train_mask,item['parameters'])
                    if method=='MEGU' else model(data.x,data.edge_index))
        producer=gu_producer(method,item['model'])
        target=dict(method=method,parameters=item['parameters'])
        if method!='Retrain':target['checkpoint_state_hash']=saved['state_hash']
        identity=dict(dataset_input=bind_input(dataset,root,root),target=target,
            pairing=pairing_identity(item,data,[9]),selection=selection,
            graph_fingerprint=inputs.graph_fingerprint,producer_version=producer.to_dict())
        payload=(build_megu_output(identity,model,logits,before) if method=='MEGU' else
                 build_output(identity,model,logits,before if method!='Retrain' else None))
        recipe=ArtifactRecipe(dict(artifact_contract=OUTPUT_CONTRACT,**identity))
        stored=store_formal_artifact(store_root,FormalArtifactRequest(ArtifactType.PREDICTION,recipe,producer),payload)
        reference=output_reference(stored,recipe.recipe_hash);refs.append(reference)
        folder=root/('source-'+method);cell=folder/'cells'/method;cell.mkdir(parents=True)
        p=cell/'selection.json';p.write_text(json.dumps(dict(cell_id=method,selection_id=selected.artifact_id,requested_k=1,selected_nodes=[9])),encoding='utf-8')
        source=dict(experiment_id='graph-fixture',run_id=method,generated_at='fixture',commit='synthetic-no-training',
            config_path='fixture.yaml',stage='unlearning',status='completed',cells=[dict(cell_id=method,path='cells/'+method,
            conditions=dict(method=method,selector='degree',model=item['model']['architecture'],seed=item['training']['seed'],
                dataset_index=0,dataset_name='cpu_fixture',budget_ratio=None,budget=dict(mode='k',value=1)),status='completed',
            files={'selection.json':dict(sha256=sha256_file(p))},results=dict(selection='completed',metrics='not_requested',scores='not_requested'),
            output=reference,selection_id=selected.artifact_id)])
        p=folder/'run.json';p.write_text(json.dumps(source),encoding='utf-8')
        sources.append(dict(run=str(p),sha256=sha256_file(p),cell_ids=[method]))
    write_yaml(root/'graph-eval.yaml',dict(kind='evaluation',schema_version=1,case=CASE))
    full=[load_output(ref,store_root,dataset_root=root) for ref in refs]
    return dict(root=root,refs=refs,sources=sources,outputs=full,checkpoint=checkpoint,original=original,data=data)


def measure(fixture,index=0):
    return graph_sensitivity(fixture['outputs'][index],fixture['outputs'][2],checkpoint_root=fixture['root']/'checkpoints',device='cpu')


def test_real_gcns_graph_change_matched_cs_and_export(graph_outputs,tables,record_property):
    from experiments.modular_artifacts import read_run
    f=graph_outputs
    result=run(tables,'graph-diagnostic',stage='metrics',selector_refs=[],output_inputs=f['sources'],evaluation_refs=['graph-eval.yaml'])
    rows=result['evaluations'][0]['rows']
    assert len(rows)==2 and len(result['evaluations'][0]['not_applicable'])==1
    for row in rows:
        m=row['metrics'];p=row['identity']['protocol']
        assert set(m)==set(METRICS)
        assert m['original_graph_raw_node_count']==m['retained_graph_raw_node_count']==5
        assert m['no_update_raw_graph_disagreement_count']>0
        assert p['graphs']['original']['features_hash']==p['graphs']['retained']['features_hash']
        assert p['graphs']['original']['edge_index_hash']!=p['graphs']['retained']['edge_index_hash']
        assert all(x['changed_labels']==0 for x in p['reproduction_observations'].values())
        assert p['checkpoint']['state_hash']==p['first_layer']['original_checkpoint_state_hash']
    gm,mm=[r['metrics'] for r in rows]
    assert gm['original_graph_no_update_cs_accuracy'] is None
    assert mm['original_graph_no_update_cs_cross_entropy']!=mm['original_graph_no_update_raw_cross_entropy']
    assert mm['original_graph_matched_cs_node_count']==5
    assert rows[1]['identity']['protocol']['cs']['anchors']=='saved_pseudo_labels_on_retained_train_mask'
    path=f['root']/'results/runs/graph-diagnostic/graph-diagnostic/run.json'
    saved,documents=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    assert len(saved['cells'])==2
    assert [x['metrics.json']['rows'][0]['values'] for x in documents]==[r['metrics'] for r in rows]
    record_property('graph_counterexample',json.dumps(dict(original_raw=mm['original_graph_raw_original_accuracy'],
        retained_raw=mm['retained_graph_raw_original_accuracy'],changed=mm['no_update_raw_graph_disagreement_count'],
        raw_ce=mm['original_graph_no_update_raw_cross_entropy'],cs_ce=mm['original_graph_no_update_cs_cross_entropy'])))


def test_cache_hit_does_not_reload_checkpoint_or_forward(graph_outputs,monkeypatch):
    import experiments.response_graph_sensitivity as g
    from experiments.unlearning_outputs import load_output
    f=graph_outputs;ev=resolve_evaluation(dict(kind='evaluation',schema_version=1,case=CASE))
    kwargs=dict(store_root=f['root']/'results/cache_v2',dataset_root=f['root'],checkpoint_root=f['root']/'checkpoints',device='cpu')
    first=evaluate_modular(ev,f['refs'],**kwargs)
    monkeypatch.setattr(g,'restore_original',functools.wraps(g.restore_original)(lambda *a,**k:pytest.fail('HIT restored checkpoint')))
    hook=torch.nn.modules.module.register_module_forward_pre_hook(lambda *a:pytest.fail('HIT forwarded'))
    try:second=evaluate_modular(ev,f['refs'],**kwargs)
    finally:hook.remove()
    for a,b in zip(first['rows'],second['rows']):
        assert b['cache']['hit'] and a['metrics']==b['metrics'] and a['identity']==b['identity']


@pytest.mark.parametrize('damage',['missing','sidecar_hash','wrong_target','bytes'])
def test_original_checkpoint_fails_closed(graph_outputs,damage):
    f=graph_outputs;p=f['checkpoint']
    if damage=='missing':p.unlink();p.with_suffix('.json').unlink()
    elif damage=='sidecar_hash':
        side=json.loads(p.with_suffix('.json').read_text(encoding='utf-8'));side['file_sha256']='0'*64
        p.with_suffix('.json').write_text(json.dumps(side),encoding='utf-8')
    elif damage=='wrong_target':f['outputs'][0].identity['target']['checkpoint_state_hash']='0'*64
    else:
        state=torch.load(p,weights_only=True);state['convs.1.bias']+=1.;torch.save(state,p)
    with pytest.raises((ValueError,RuntimeError),match='checkpoint|contents|Original'):
        measure(f)


@pytest.mark.parametrize('damage',['missing','different','retained_recomputed'])
def test_saved_pseudo_labels_are_required_and_not_regenerated(graph_outputs,damage):
    f=graph_outputs;p=f['outputs'][1]
    if damage=='missing':p.auxiliary.pop('megu_pseudo_labels')
    elif damage=='different':p.auxiliary['megu_pseudo_labels']=1-p.auxiliary['megu_pseudo_labels']
    else:
        from experiments.node_deletion import retained_graph
        d=retained_graph(f['data'],[9])
        p.auxiliary['megu_pseudo_labels']=f['original'](d.x,d.edge_index).argmax(1).detach().numpy()
    with pytest.raises(ValueError,match='pseudo-label'):
        measure(f,1)


@pytest.mark.parametrize('method,index',[('Original',0),('GIF',0),('MEGU',1),('Retrain',2)])
def test_original_reproduction_mismatch_stops_before_retained_graph(graph_outputs,monkeypatch,method,index):
    import experiments.response_graph_sensitivity as g
    f=graph_outputs
    target=f['outputs'][index];key='logits_before' if method=='Original' else 'logits'
    target.arrays[key]=target.arrays[key]+np.array([.25,-.25],dtype=np.float32)
    actual=g._graph
    forwarded=[]
    original_edges=f['data'].edge_index
    def before_forward(module,args):
        if len(args)==2 and isinstance(args[1],torch.Tensor) and args[1].ndim==2 and args[1].shape[0]==2:
            forwarded.append(args[1].shape[1])
    hook=torch.nn.modules.module.register_module_forward_pre_hook(before_forward)
    try:
        with pytest.raises(ValueError,match='reproduction failed'):
            measure(f,1 if method=='MEGU' else 0)
    finally:hook.remove()
    # GCNConv forwards add no full graph call with a different edge count before failure.
    assert forwarded and set(forwarded)=={original_edges.shape[1]}


def test_fixed_tolerance_rejects_label_change_even_when_values_close():
    with pytest.raises(ValueError,match='changed_labels=1'):
        reproduce(np.array([[1e-8,0.]]),np.array([[0.,1e-8]]),'near tie')
    assert reproduce(np.array([[2.,0.]]),np.array([[2.+1e-6,0.]]),'roundoff')['changed_labels']==0


def test_new_metric_environment_and_policy_are_bound(graph_outputs):
    from experiments.evaluation_cache import metric_environment,evaluation_request
    from experiments.modular_evaluation import _formula_functions
    env=metric_environment(CASE)
    assert {'numpy','torch','torch_geometric'}<=set(env)
    ev=resolve_evaluation(dict(kind='evaluation',schema_version=1,case=CASE))
    request=evaluation_request(CASE,ev['metrics'],[],_formula_functions(CASE),ev['producer_version'])
    assert request.recipe.fields['evaluation_identity']['metric_libraries']==env
    assert len(_formula_functions(CASE))>=10


def test_failure_is_retained_in_real_run(graph_outputs,tables,monkeypatch):
    import experiments.response_graph_sensitivity as g
    f=graph_outputs
    original=g.restore_original
    @functools.wraps(original)
    def wrong_state(*args,**kwargs):
        model,ref=original(*args,**kwargs)
        with torch.no_grad():model.convs[1].bias[0]+=1.
        return model,ref
    monkeypatch.setattr(g,'restore_original',wrong_state)
    with pytest.raises(ValueError,match='reproduction failed'):
        run(tables,'reproduction-failed',stage='metrics',selector_refs=[],output_inputs=f['sources'],evaluation_refs=['graph-eval.yaml'])
    failure=json.loads((f['root']/'results/runs/reproduction-failed/reproduction-failed/run.json').read_text(encoding='utf-8'))
    assert failure['status']=='failed' and 'reproduction failed' in failure['error']


def test_graph_case_rejects_training_lane_before_run_creation(graph_outputs,tables):
    f=graph_outputs
    with pytest.raises(ValueError,match='explicit Metrics stage'):
        run(tables,'bad-lane',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['GIF.yaml','Retrain.yaml'],evaluation_refs=['graph-eval.yaml'])
    assert not (f['root']/'results/runs/bad-lane').exists()


def test_full_reader_and_first_layer_are_both_usable_in_one_run(graph_outputs,tables):
    f=graph_outputs
    write_yaml(f['root']/'response-eval.yaml',dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))
    result=run(tables,'combined-graphs',stage='metrics',selector_refs=[],output_inputs=f['sources'],evaluation_refs=['response-eval.yaml','graph-eval.yaml'])
    first,second=result['evaluations']
    assert len(first['rows'])==len(second['rows'])==2
    for a,b in zip(first['rows'],second['rows']):
        assert a['metrics']['gu_retrain_disagreement_count']==b['metrics']['original_graph_published_gu_retrain_disagreement_count']
        assert abs(a['metrics']['gu_cross_entropy']-b['metrics']['original_graph_published_gu_cross_entropy'])<=1e-4


def test_matched_cs_uses_same_saved_labels_parameters_and_retained_mask(graph_outputs,monkeypatch):
    import experiments.response_graph_sensitivity as g
    f=graph_outputs;original=g.megu_logits;seen=[]
    def observed(model,evaluation,retain_mask,parameters):
        seen.append((model.megu_pseudo_labels.detach().cpu().numpy().copy(),retain_mask.detach().cpu().numpy().copy(),copy.deepcopy(parameters),evaluation.edge_index.shape[1]))
        return original(model,evaluation,retain_mask,parameters)
    monkeypatch.setattr(g,'megu_logits',observed)
    measure(f,1)
    assert len(seen)==6
    for pseudo,mask,parameters,edges in seen:
        np.testing.assert_array_equal(pseudo,f['outputs'][1].auxiliary['megu_pseudo_labels'])
        np.testing.assert_array_equal(mask,f['outputs'][1].arrays['retain_mask'])
        assert not mask[9]
        assert parameters==f['outputs'][1].identity['target']['parameters']
    assert len({x[3] for x in seen})==2


def test_graph_replay_catches_mutation_in_final_cs_call(graph_outputs,monkeypatch):
    import experiments.response_graph_sensitivity as g
    original=g.megu_logits;calls=[]
    def mutating(model,*args):
        result=original(model,*args);calls.append(1)
        if len(calls)==6:
            with torch.no_grad():model.convs[1].bias[0]+=1.
        return result
    monkeypatch.setattr(g,'megu_logits',mutating)
    with pytest.raises(ValueError,match='mutated model state'):
        measure(graph_outputs,1)


def test_restore_rejects_dtype_conversion_of_saved_state(graph_outputs):
    f=graph_outputs
    f['outputs'][0].state['convs.1.bias']=f['outputs'][0].state['convs.1.bias'].astype(np.float64)
    with pytest.raises(ValueError,match='restored Output weights differ'):
        measure(f)

@pytest.fixture
def gnndelete_output(graph_outputs):
    from cache_v2 import ArtifactRecipe
    from cache_v2.unlearning_output import OUTPUT_CONTRACT
    from experiments.artifact_producer import FormalArtifactRequest,store_formal_artifact
    from cache_v2 import ArtifactType
    from experiments.modular_config import load_instance
    from experiments.modular_gu import gu_producer
    from experiments.modular_model import runtime_defaults
    from experiments.unlearning_outputs import build_output,output_reference,load_output
    from model.base_gnn.deletion import GCNDelete
    from utils.target_checkpoint import sha256_file
    f=graph_outputs; root=f['root']; data=f['data']
    common=dict(kind='unlearning',schema_version=1,model=dict(architecture='OpenGU.GCNNet',hidden_channels=4),training=dict(epochs=3))
    write_yaml(root/'GNNDelete.yaml',dict(common,method='GNNDelete'))
    instance=load_instance(root/'GNNDelete.yaml','unlearning')
    args=runtime_defaults();args.update(gcn_num_layers=2,gcn_hidden=4,out_dim=2,base_model='GCN',dataset_name='cpu_fixture',downstream_task='node')
    first=torch.zeros(data.num_nodes,dtype=torch.bool);first[[9,15]]=True
    second=torch.zeros_like(first);second[[15,16]]=True
    model=GCNDelete(args,3,2,mask_1hop=first,mask_2hop=second).eval()
    missing,unexpected=model.load_state_dict(f['original'].state_dict(),strict=False)
    assert set(missing)=={'deletion1.deletion_weight','deletion2.deletion_weight'} and not unexpected
    with torch.no_grad():
        model.deletion1.deletion_weight.copy_(torch.eye(4))
        model.deletion2.deletion_weight.copy_(torch.tensor([[0.,1.],[1.,0.]]))
        before=f['original'](data.x,data.edge_index);after=model(data.x,data.edge_index)
    producer=gu_producer('GNNDelete',instance['model'])
    identity=copy.deepcopy(f['outputs'][0].identity)
    identity['target']=dict(method='GNNDelete',parameters=instance['parameters'],checkpoint_state_hash=identity['target']['checkpoint_state_hash'])
    identity['producer_version']=producer.to_dict()
    payload=build_output(identity,model,after,before)
    recipe=ArtifactRecipe({'artifact_contract':OUTPUT_CONTRACT,**identity})
    stored=store_formal_artifact(root/'results/cache_v2',FormalArtifactRequest(ArtifactType.PREDICTION,recipe,producer),payload)
    reference=output_reference(stored,recipe.recipe_hash)
    source=json.loads(Path(f['sources'][0]['run']).read_text(encoding='utf-8'))
    source['run_id']='GNNDelete';cell=source['cells'][0]
    cell.update(cell_id='GNNDelete',path='cells/GNNDelete',output=reference)
    cell['conditions']['method']='GNNDelete'
    folder=root/'source-GNNDelete';directory=folder/'cells/GNNDelete';directory.mkdir(parents=True)
    selection=json.loads((root/'source-GIF/cells/GIF/selection.json').read_text(encoding='utf-8'))
    selection['cell_id']='GNNDelete';path=directory/'selection.json';path.write_text(json.dumps(selection),encoding='utf-8')
    cell['files']['selection.json']['sha256']=sha256_file(path)
    path=folder/'run.json';path.write_text(json.dumps(source),encoding='utf-8')
    result=dict(f)
    result['outputs']=[load_output(reference,root/'results/cache_v2',dataset_root=root),f['outputs'][1],f['outputs'][2]]
    result['sources']=[dict(run=str(path),sha256=sha256_file(path),cell_ids=['GNNDelete']),f['sources'][2]]
    result['gnndelete_model']=model
    return result


def test_gnndelete_saved_masks_two_graphs_and_response_export(gnndelete_output,tables,monkeypatch,record_property):
    from model.base_gnn.deletion import GCNDelete
    from experiments.response_diagnostics import RELATIONS,CORRECTNESS
    from experiments.modular_artifacts import read_run
    f=gnndelete_output; observed=[]; actual=GCNDelete.forward
    def observe(model,x,edges,*args,**kwargs):
        assert model.deletion1.mask.device==x.device==model.deletion2.mask.device
        assert np.array_equal(model.deletion1.mask.cpu().numpy(),f['outputs'][0].auxiliary['deletion1_mask'])
        assert np.array_equal(model.deletion2.mask.cpu().numpy(),f['outputs'][0].auxiliary['deletion2_mask'])
        observed.append(edges.shape[1])
        return actual(model,x,edges,*args,**kwargs)
    monkeypatch.setattr(GCNDelete,'forward',functools.wraps(actual)(observe))
    write_yaml(f['root']/'response.yaml',dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))
    result=run(tables,'gnn-two-graph',stage='metrics',selector_refs=[],output_inputs=f['sources'],evaluation_refs=['response.yaml','graph-eval.yaml'])
    assert len(result['evaluations'])==2
    for evaluation in result['evaluations']:
        assert len(evaluation['rows'])==len(evaluation['not_applicable'])==1
    response=result['evaluations'][0]['rows'][0]['metrics']
    row=result['evaluations'][1]['rows'][0];values=row['metrics'];protocol=row['identity']['protocol']
    assert response['selected_node_count']==1 and response['retained_train_count']==9
    assert observed==[f['data'].edge_index.shape[1],f['outputs'][0].arrays['training_edge_index'].shape[1],f['data'].edge_index.shape[1]]
    assert protocol['cs']=={'status':'not_applicable'}
    assert protocol['deletion_masks']['source']=='saved_output_auxiliary'
    assert protocol['deletion_masks']['masks']['deletion1']['count']==2
    assert protocol['deletion_masks']['masks']['deletion2']['count']==2
    assert protocol['reproduction_observations']['GNNDelete']['changed_labels']==0
    for graph in ('original','retained'):
        prefix=graph+'_graph_raw_'
        assert sum(values[prefix+r+'_count'] for r in RELATIONS)==5
        for i,name in enumerate(('original','gu','retrain')):
            correct=sum(values[prefix+r+'_correct_'+bits+'_count'] for r in RELATIONS for bits in CORRECTNESS if bits[i]=='1')
            assert correct/5==values[prefix+name+'_accuracy']
        mismatch=sum(values[prefix+r+'_count'] for r in ('original_gu_equal','original_retrain_equal','all_different'))
        assert mismatch==values[prefix+'gu_retrain_disagreement_count']
        assert all(v is None for k,v in values.items() if k.startswith(graph+'_graph_') and ('matched_cs_' in k or 'no_update_cs_' in k or 'updated_cs_' in k or '_vs_no_update_cs_' in k or '_vs_updated_cs_' in k))
    assert values['updated_raw_graph_disagreement_count']>0
    saved_path=f['root']/'results/runs/gnn-two-graph/gnn-two-graph/run.json'
    saved,docs=read_run(saved_path,hashlib.sha256(saved_path.read_bytes()).hexdigest())
    assert len(saved['cells'])==1 and len(docs[0]['metrics.json']['rows'])==2
    record_property('gnndelete_graph_counterexample',json.dumps({k:values[k] for k in ('updated_raw_graph_disagreement_count','original_graph_raw_gu_accuracy','retained_graph_raw_gu_accuracy','original_graph_raw_gu_retrain_disagreement_count','retained_graph_raw_gu_retrain_disagreement_count')}))


@pytest.mark.parametrize('fault',['missing','integer','wrong_shape'])
def test_gnndelete_bad_saved_masks_fail_before_forward(gnndelete_output,monkeypatch,fault):
    import experiments.response_graph_sensitivity as module
    output=gnndelete_output['outputs'][0]
    if fault=='missing':del output.auxiliary['deletion1_mask']
    elif fault=='integer':output.auxiliary['deletion1_mask']=output.auxiliary['deletion1_mask'].astype(np.int64)
    else:output.auxiliary['deletion1_mask']=np.zeros(1,dtype=bool)
    monkeypatch.setattr(module,'restore_original',lambda *a,**k:pytest.fail('invalid mask reached model restoration'))
    with pytest.raises(ValueError,match='saved boolean node mask'):measure(gnndelete_output)


def test_gnndelete_original_mismatch_stops_before_retained(gnndelete_output,monkeypatch):
    from model.base_gnn.deletion import GCNDelete
    f=gnndelete_output;f['outputs'][0].arrays['logits']=f['outputs'][0].arrays['logits'][:,::-1].copy()+.1
    actual=GCNDelete.forward;edges=[]
    def observe(model,x,e,*a,**kw):
        edges.append(e.shape[1]);return actual(model,x,e,*a,**kw)
    monkeypatch.setattr(GCNDelete,'forward',observe)
    with pytest.raises(ValueError,match='GNNDelete: reproduction failed'):measure(f)
    assert edges==[f['data'].edge_index.shape[1]]


def test_gnndelete_mask_mutation_on_retained_is_rejected(gnndelete_output,monkeypatch):
    from model.base_gnn.deletion import GCNDelete
    f=gnndelete_output;actual=GCNDelete.forward;calls=[]
    def corrupt(model,x,e,*a,**kw):
        result=actual(model,x,e,*a,**kw);calls.append(e.shape[1])
        if len(calls)==2:model.deletion1.mask[0]=~model.deletion1.mask[0]
        return result
    monkeypatch.setattr(GCNDelete,'forward',corrupt)
    with pytest.raises(ValueError,match='changed saved deletion mask'):measure(f)
    assert len(calls)==2


def test_gnndelete_wrong_saved_mask_cannot_pass_original_reproduction(gnndelete_output):
    output=gnndelete_output['outputs'][0]
    output.auxiliary['deletion2_mask']=np.zeros_like(output.auxiliary['deletion2_mask'])
    with pytest.raises(ValueError,match='GNNDelete: reproduction failed'):measure(gnndelete_output)
