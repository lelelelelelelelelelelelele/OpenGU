"""Real Store/weights/GIF replay; negative guards never replace core results."""
import copy
import functools
import json
import subprocess
import sys
from pathlib import Path

import pytest
import torch
import yaml

from test_modular_consumers import tables,run,write_yaml
from test_modular_checkpoint_pt import external
from experiments.modular_config import load_experiment,load_instance,configuration_fingerprint
from experiments.modular_artifacts import planned_cells,read_run
from experiments.modular_run import execute,read_dataset
from experiments.modular_execution import ExecutionContext
from utils.target_checkpoint import data_identity,state_hash,sha256_file

def setup_assets(tables):
    root,base,gu=tables
    data,item,resolved,weights=external(tables)
    ret={k:copy.deepcopy(gu[k]) for k in ('kind','model','schema_version','training')}
    ret.update(method='Retrain',parameters={});ret['training']['seed']=17
    write_yaml(root/'ret.yaml',ret)
    baseline=run(tables,'existing',stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['ret.yaml'])
    selected=baseline['selectors'][0]['selection'];selection=selected['artifact'];nodes=selected['views']['1']['selected_nodes']
    return data,item,dict(selection={k:selection[k] for k in ('artifact_id','recipe_hash','content_hash')},selected_nodes=nodes,
        original=dict(path='weights.pt',file_sha256=sha256_file(root/'weights.pt'),state_hash=state_hash(weights),
            data_identity=data_identity(data),model=resolved['model'],execution_seed=17),retrain=baseline['unlearning'][0]['output'])

def table(tables,item,assets,iterations,name):
    root,base,_=tables;item=copy.deepcopy(item);item['parameters']=dict(iteration=iterations,scale=1000,damp=.1)
    write_yaml(root/'external.yaml',item)
    config=copy.deepcopy(base);config.update(experiment_id=name,stage='unlearning',selector_refs=['degree.yaml'],
        unlearning_refs=['external.yaml'],execution=dict(gu_cache=dict(GIF='disabled')),
        observers=[dict(name=n,methods=['GIF'],**({'parameters':{'lanczos_steps':3}} if n=='hessian_calibration' else {}))
            for n in ['linear_solver_trace','same_graph_change']+(['hessian_calibration'] if iterations==100 else [])])
    path=root/(name+'.yaml');write_yaml(path,config)
    parsed=load_experiment(path);cell=planned_cells(parsed)[0];gu=parsed['unlearnings'][0]
    row=dict(cell_id=cell['cell_id'],**copy.deepcopy(assets),parameters=gu['parameters'],deletion=gu['deletion'])
    document=dict(schema='opengu.exact-gu-inputs-v1',requests=[row])
    input_path=root/(name+'.json');input_path.write_text(json.dumps(document),encoding='utf-8')
    config['exact_inputs']=dict(path=input_path.name,sha256=sha256_file(input_path));write_yaml(path,config)
    return path,config,document,input_path

def context(root,name):
    return ExecutionContext(run_id=name,level='verification',request_device='cpu',store_root=root/'results/cache_v2',
        checkpoint_root=root/'forbidden-checkpoints',runtime_root=root/'runtime'/name,
        output=root/'results/runs'/name/name/'run.json',executor='pytest-real-exact-inputs')

def forbid_recomputation(monkeypatch):
    import experiments.modular_model as model
    import experiments.modular_run as entry
    import utils.target_checkpoint as checkpoints
    def wrap(function):
        @functools.wraps(function)
        def forbidden(*args,**kwargs):raise AssertionError('exact replay trained, resolved Selection, or scanned checkpoints')
        return forbidden
    monkeypatch.setattr(model,'train_supervised',wrap(model.train_supervised))
    monkeypatch.setattr(entry,'resolve_methods',wrap(entry.resolve_methods))
    monkeypatch.setattr(checkpoints,'resolve_cached_weights',wrap(checkpoints.resolve_cached_weights))
    monkeypatch.setattr(torch.optim.Adam,'step',wrap(torch.optim.Adam.step))
    monkeypatch.setattr(torch.optim.SGD,'step',wrap(torch.optim.SGD.step))

def test_real_existing_inputs_two_endpoints_and_native_metrics(tables,monkeypatch,record_property):
    root=tables[0];data,item,assets=setup_assets(tables)
    # Import producer dependencies before forbidden instrumentation, preserving identity.
    from experiments.modular_gu import gu_producer
    before=gu_producer('GIF',assets['original']['model']).to_dict()
    forbid_recomputation(monkeypatch)
    outputs=[]
    for iterations in (100,400):
        name='exact'+str(iterations);path,config,document,input_path=table(tables,item,assets,iterations,name)
        result=execute(path,context=context(root,name))
        current=root/'results/runs'/name/name/'run.json';run_value,docs=read_run(current,sha256_file(current))
        cell=run_value['cells'][0];output=result['unlearning'][0]['output'];outputs.append(output)
        assert result['selector_producer_called'] is False and cell['producer_called']['selection'] is False
        assert cell['cache']['method']=='disabled' and cell['producer_called']['method'] is True
        assert cell['cache_provenance']['exact_inputs']['sha256']==sha256_file(input_path)
        assert result['unlearning'][0]['checkpoint']['state_hash']==assets['original']['state_hash']
        trace=[json.loads(line) for line in docs[0]['observers/linear_solver_trace/trace.jsonl'].splitlines()]
        assert [r['step'] for r in trace]==list(range(iterations+1))
        assert {r['name'] for r in cell['observers']}==({'linear_solver_trace','same_graph_change','hessian_calibration'} if iterations==100 else {'linear_solver_trace','same_graph_change'})
        if iterations==100:
            hvp=json.loads(docs[0]['observers/hessian_calibration/calibration.json'])['measurements']['hvp']
            assert hvp['probe_absolute_error']>=0 and hvp['probe_reference_l2']>=0
        metrics=run(tables,'metrics'+str(iterations),stage='metrics',selector_refs=[],
            output_inputs=[dict(run=str(current),sha256=sha256_file(current))],evaluation_refs=['utility.yaml'])
        assert metrics['evaluations']
        record_property('exact_endpoint_'+str(iterations),json.dumps(dict(cell_id=cell['cell_id'],output=output,trace_rows=len(trace))))
    assert outputs[0]['recipe_hash']!=outputs[1]['recipe_hash'] and outputs[0]['path']!=outputs[1]['path']
    assert sha256_file(root/'weights.pt')==assets['original']['file_sha256']
    assert not (root/'forbidden-checkpoints').exists()
    assert gu_producer('GIF',assets['original']['model']).to_dict()==before

@pytest.mark.parametrize('defect',['missing_selection','selection_hash','ordered_nodes','missing_original','original_file',
    'original_state','data','model','seed','deletion','parameters','ret_selection','missing_ret','wrong_ret_pairing'])
def test_real_input_mismatches_fail_before_gif(tables,monkeypatch,defect):
    root=tables[0];_,item,assets=setup_assets(tables)
    path,config,doc,input_path=table(tables,item,assets,100,'bad')
    row=doc['requests'][0]
    if defect=='missing_selection':row['selection']['artifact_id']='missing-selection'
    elif defect=='selection_hash':row['selection']['content_hash']='0'*64
    elif defect=='ordered_nodes':row['selected_nodes']=[(row['selected_nodes'][0]+1)%10]
    elif defect=='missing_original':row['original']['path']='absent.pt'
    elif defect=='original_file':row['original']['file_sha256']='0'*64
    elif defect=='original_state':row['original']['state_hash']='0'*64
    elif defect=='data':row['original']['data_identity']['split_hash']='0'*64
    elif defect=='model':row['original']['model']['hidden_channels']=99
    elif defect=='seed':row['original']['execution_seed']=99
    elif defect=='deletion':row['deletion']['evaluation_graph']='retained'
    elif defect=='parameters':row['parameters']['scale']=1.
    elif defect=='ret_selection':row['retrain']=dict(row['selection'])
    elif defect=='missing_ret':row['retrain']['artifact_id']='missing-ret'
    elif defect=='wrong_ret_pairing':
        selector=yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
        selector['budget']['value']=2;write_yaml(root/'other-degree.yaml',selector)
        other=run(tables,'other-existing',stage='unlearning',selector_refs=['other-degree.yaml'],unlearning_refs=['ret.yaml'])
        row['retrain']=other['unlearning'][0]['output']
    input_path.write_text(json.dumps(doc),encoding='utf-8');config['exact_inputs']['sha256']=sha256_file(input_path);write_yaml(path,config)
    forbid_recomputation(monkeypatch)
    from experiments.modular_gu import GU_METHODS
    def no_gif(*args,**kwargs):raise AssertionError('bad exact inputs reached GIF algorithm')
    monkeypatch.setitem(GU_METHODS,'GIF',no_gif)
    with pytest.raises(Exception) as error:execute(path,context=context(root,'negative'))
    assert 'bad exact inputs reached GIF algorithm' not in str(error.value)
    assert not list((root/'results/runs/negative').rglob('output.npz'))

@pytest.mark.parametrize('defect',['sha','unknown','duplicate','missing_cell','extra_cell','no_checkpoint','reuse','wrong_stage','wrong_observers'])
def test_exact_config_and_recursive_binding_rejects(tables,defect):
    root=tables[0];_,item,assets=setup_assets(tables);path,config,doc,input_path=table(tables,item,assets,100,'config')
    if defect=='sha':config['exact_inputs']['sha256']='0'*64
    elif defect=='unknown':doc['requests'][0]['invented']=True
    elif defect=='duplicate':doc['requests'].append(copy.deepcopy(doc['requests'][0]))
    elif defect=='missing_cell':doc['requests']=[]
    elif defect=='extra_cell':doc['requests'][0]['cell_id']='0'*20
    elif defect=='no_checkpoint':
        item.pop('checkpoint');item['training']={'epochs':3,'seed':17};write_yaml(root/'external.yaml',item)
    elif defect=='reuse':config['execution']['gu_cache']['GIF']='reuse'
    elif defect=='wrong_stage':config['stage']='selector';config.pop('unlearning_refs')
    elif defect=='wrong_observers':config['observers']=config['observers'][:2]
    if defect not in ('sha','no_checkpoint'):
        input_path.write_text(json.dumps(doc),encoding='utf-8');config['exact_inputs']['sha256']=sha256_file(input_path)
    write_yaml(path,config)
    with pytest.raises(Exception):load_experiment(path)

def test_native_recipe_closes_exact_json_and_ordinary_cells(tables,record_property):
    from scripts.syncmate.opengu_recipes import generate,assemble
    from scripts.syncmate.opengu_adapter import _modular_preflight
    root=tables[0];_,item,assets=setup_assets(tables)
    path,config,doc,input_path=table(tables,item,assets,100,'native')
    spec=generate(path.name,recipe_id='exact-fixture',run_id='r1',project_root=root)
    definition=assemble(spec,root)
    assert definition['argv']==('{python}','experiments/run.py',path.name,'--run-id','r1','--syncmate')
    assert definition['logical_cells']==1 and spec['expected_datasets']==[dict(num_nodes=20,candidate_count=10)]
    assert _modular_preflight(definition,path)['ready']
    assert len(definition['expected_artifact_paths'])==7
    assert all(p.startswith('results/runs/native/r1/') for p in definition['expected_artifact_paths'])
    command=[sys.executable,'-B',str(Path(__file__).resolve().parents[1]/'experiments/run.py'),str(path),
        '--run-id','r1','--device','cpu','--verification-root',str(root)]
    completed=subprocess.run(command,cwd=Path(__file__).resolve().parents[1],capture_output=True,timeout=90)
    assert completed.returncode==0,completed.stdout.decode('utf-8')+completed.stderr.decode('utf-8')
    actual=json.loads(completed.stdout)
    assert actual['passed'] is True and set(actual['generated_artifacts'])==set(definition['expected_artifact_paths'])
    returned=root/definition['expected_artifact_paths'][0]
    read_run(returned,sha256_file(returned))
    record_property('native_exact_recipe',json.dumps(dict(argv=definition['argv'],config_sha256=spec['config_sha256'],
        configuration_fingerprint=spec['configuration_fingerprint'],artifacts=len(actual['generated_artifacts']),native_cli_passed=True)))
    initial=configuration_fingerprint(path)
    doc['requests'][0]['original']['state_hash']='0'*64
    input_path.write_text(json.dumps(doc),encoding='utf-8')
    with pytest.raises(ValueError,match='SHA mismatch'):load_experiment(path)
    config['exact_inputs']['sha256']=sha256_file(input_path);write_yaml(path,config)
    assert configuration_fingerprint(path)!=initial
    assert _modular_preflight(definition,path)['ready'] is False

def test_zero_reference_hvp_has_absolute_evidence():
    from types import SimpleNamespace
    import torch.nn.functional as F
    from experiments.observers.hessian_calibration import HessianCalibration,flat
    from unlearning.unlearning_methods.GIF.solver import solve_gif_system
    class ZeroFeatures(torch.nn.Module):
        def __init__(self):
            super().__init__();self.weight=torch.nn.Parameter(torch.zeros(2,2))
        def reason_once(self,data):return data.x@self.weight
    model=ZeroFeatures();data=SimpleNamespace(x=torch.zeros(4,2),y=torch.tensor([0,1,0,1]),train_mask=torch.ones(4,dtype=torch.bool))
    params=list(model.parameters());loss=F.cross_entropy(model.reason_once(data),data.y,reduction='sum')
    grad=torch.autograd.grad(loss,params,create_graph=True)
    def matvec(v):return flat(torch.autograd.grad(grad,params,grad_outputs=[v.reshape_as(params[0])],retain_graph=True))
    observer=HessianCalibration(dict(lanczos_steps=2))
    observer(dict(method='GIF',phase='loss_ready',values=dict(model=model,data=data,parameters=params,loss=loss,loss_reduction='sum')))
    rhs=torch.zeros(4)
    observer(dict(method='GIF',phase='solver_system_ready',values=dict(rhs=rhs,matvec=matvec,parameters=params,scale=1000.,damp=.1,iterations=100)))
    update,diagnostic=solve_gif_system(matvec,rhs,iterations=100,scale=1000.,damp=.1)
    assert torch.equal(update,rhs)
    hvp=observer.measurements['hvp']
    for key in ('probe','rhs','repeat'):
        assert hvp[key+'_reference_l2']==hvp[key+'_absolute_error']==0.
        assert hvp[key+'_relative_error'] is None
