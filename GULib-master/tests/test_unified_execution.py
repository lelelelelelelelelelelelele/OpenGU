"""AAGU-034: real command entry, temporary assets, real training and portable outputs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import torch
import yaml
from test_modular_consumers import tables, write_yaml
from experiments.modular_config import load_experiment, experiment_batches, load_instance
from experiments.modular_run import execute
from experiments.modular_artifacts import read_summary_outputs

ROOT = Path(__file__).resolve().parents[1]

# Instrument the real entry in a fresh process. wraps preserves the production
# fingerprint; optimizer stepping proves the RNG seed at actual training time.
INSTRUMENTED_ENTRY = r'''
import functools,json,os,runpy,sys
from pathlib import Path
import torch
from experiments.target_direct_v1 import methods
poison=os.environ.get('AAGU034_POISON')=='1'
trace={'training_seeds':[],'score_calls':[]}
original_step=torch.optim.Adam.step
@functools.wraps(original_step)
def step(self,*a,**k):
    trace['training_seeds'].append(torch.initial_seed())
    if poison:raise AssertionError('warm command called training producer')
    return original_step(self,*a,**k)
torch.optim.Adam.step=step
for name in ('degree','random','a_grad_norm'):
    original=methods.METHODS[name]
    def wrap(name,original):
        @functools.wraps(original)
        def score(*a,**k):
            trace['score_calls'].append(name)
            if poison:raise AssertionError('warm command called score producer')
            return original(*a,**k)
        return score
    methods.METHODS[name]=wrap(name,original)
sys.argv=['experiments/run.py']+sys.argv[1:]
try:runpy.run_path('experiments/run.py',run_name='__main__')
finally:Path(os.environ['AAGU034_TRACE']).write_text(json.dumps(trace))
'''


def command(root, config, run_id, *, poison=False, instrument=True):
    env = dict(os.environ, AAGU034_TRACE=str(root / (run_id + '.trace.json')),
               AAGU034_POISON='1' if poison else '0')
    argv = [sys.executable, '-B', '-X', 'utf8']
    argv += ['-c', INSTRUMENTED_ENTRY] if instrument else ['experiments/run.py']
    device = root / '.syncmate/device.yaml'
    device.parent.mkdir(exist_ok=True)
    write_yaml(device, {'version': 1, 'device_id': 'temporary-cpu', 'role': 'runner',
        'repo_path': str(root), 'execution_device': 'cpu', 'peers': {}})
    argv += [str(config), '--verification-root', str(root), '--run-id', run_id,
             '--device-config', str(device)]
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


@pytest.fixture
def matrix(tables):
    root, config, gu = tables
    for name in ('degree', 'random', 'a_grad_norm'):
        selector = {'kind': 'selector', 'schema_version': 1, 'method': name,
            'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'ratio', 'value': .9}}
        if name == 'a_grad_norm':
            selector.update(model=gu['model'], training={'epochs': 3, 'seed': 7})
        if name == 'random': selector['parameters'] = {'seed': 104245}
        write_yaml(root / (name + '.yaml'), selector)
    retrain = {**gu, 'method': 'Retrain', 'parameters': {}}
    write_yaml(root / 'retrain.yaml', retrain)
    write_yaml(root / 'metrics.yaml', {'kind': 'evaluation', 'schema_version': 1, 'case': 'post_method_metrics'})
    config.update(experiment_id='cpu-matrix', stage='unlearning',
        selector_refs=['degree.yaml','random.yaml','a_grad_norm.yaml'],
        unlearning_refs=['gu.yaml','retrain.yaml'], evaluation_refs=['metrics.yaml'],
        seeds=[122,722], budget_ratios=[.1,.2])
    path = root / 'experiment.yaml';write_yaml(path,config)
    return root, path


def test_command_cold_warm_seed_budget_retrain_and_metrics(matrix, record_property):
    root, path = matrix
    before = {p.name:p.read_bytes() for p in root.glob('*.yaml')}
    dry = subprocess.run([sys.executable,'-B','experiments/run.py',str(path),'--dry_run'],
                         cwd=ROOT,capture_output=True,text=True)
    assert dry.returncode == 0, dry.stdout+dry.stderr
    assert json.loads(dry.stdout)['logical_cells'] == 24
    assert not (root/'results').exists()
    cold = command(root,path,'cold')
    warm = command(root,path,'warm',poison=True)
    assert before == {p.name:p.read_bytes() for p in root.glob('*.yaml')}
    trace = json.loads((root/'cold.trace.json').read_text())
    assert set(trace['training_seeds']) == {122,722}
    assert json.loads((root/'warm.trace.json').read_text()) == {'training_seeds':[],'score_calls':[]}
    assert len(cold['unlearning']) == 24
    assert [r['output'] for r in cold['unlearning']] == [r['output'] for r in warm['unlearning']]
    assert all(r['hit'] and not r['producer_called'] for r in warm['unlearning'])
    score_ids, selection_ids = {}, {}
    for row in cold['selectors']:
        method = row['selector_ref'];axes = row['matrix_values']
        score_ids.setdefault(method,set()).add(row['score']['artifact_id'])
        selection_ids.setdefault(method,set()).add(row['selection']['artifact']['artifact_id'])
        assert row['selection']['artifact_k'] == int(10*axes['budget_ratio'])
        if axes['budget_ratio'] == .2:
            assert row['score']['hit']
        if axes['training_seed']==722 and method != 'a_grad_norm.yaml':
            assert row['selection']['cache']['hit']
    assert {k:len(v) for k,v in score_ids.items()} == {'degree.yaml':1,'random.yaml':1,'a_grad_norm.yaml':2}
    assert {k:len(v) for k,v in selection_ids.items()} == {'degree.yaml':2,'random.yaml':2,'a_grad_norm.yaml':4}
    summary_path=Path(cold['execution_receipt']['output'])
    _, outputs = read_summary_outputs(summary_path, hashlib.sha256(summary_path.read_bytes()).hexdigest())
    for row, result in zip(cold['unlearning'],outputs):
        payload=result['payload'];selected=payload.arrays['selected_nodes']
        assert len(selected)==int(10*row['matrix_values']['budget_ratio'])
        assert not payload.arrays['retain_mask'][selected].any()
        assert not set(selected).intersection(payload.arrays['training_edge_index'].reshape(-1))
        assert payload.identity['pairing']['training']['seed']==row['matrix_values']['training_seed']
    # Metrics uses collected portable outputs; it does not need the producer Store.
    write_yaml(root/'gap.yaml',{'kind':'evaluation','schema_version':1,'case':'post_unlearning_utility_and_retrain_gap'})
    config={'kind':'experiment','schema_version':1,'experiment_id':'cpu-metrics','stage':'metrics',
        'dataset_ref':'dataset.yaml','output_inputs':[{'summary':str(summary_path),
        'sha256':hashlib.sha256(summary_path.read_bytes()).hexdigest()}],
        'evaluation_refs':['gap.yaml'],'matrix':'cartesian_product'}
    write_yaml(root/'read.yaml',config)
    metrics=command(root,root/'read.yaml','metrics',poison=True)
    assert len(metrics['evaluations'][0]['rows'])==12
    assert metrics['selector_producer_called'] is False
    record_property('command_evidence',json.dumps({'cold_trace':trace,'warm_trace':{'training_seeds':[],'score_calls':[]},
        'logical_cells':24,'score_groups':{k:len(v) for k,v in score_ids.items()},'metrics_rows':12,
        'cold_output':str(summary_path),'warm_output':warm['execution_receipt']['output']}))


def test_stage_s_summary_binds_real_selections_without_resampling(matrix):
    root,path=matrix
    config=yaml.safe_load(path.read_text());config.update(stage='selector',unlearning_refs=[],evaluation_refs=[])
    write_yaml(path,config)
    source=command(root,path,'selector',instrument=False)
    output=Path(source['execution_receipt']['output'])
    gu={'kind':'experiment','schema_version':1,'experiment_id':'bound-gu','stage':'unlearning',
        'dataset_ref':'dataset.yaml','selection_input':{'experiment_ref':'experiment.yaml',
        'summary':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()},
        'unlearning_refs':['retrain.yaml'],'matrix':'cartesian_product'}
    write_yaml(root/'bound.yaml',gu)
    actual=command(root,root/'bound.yaml','bound',instrument=False)
    assert actual['selectors']==[] and actual['selector_producer_called'] is False
    expected=[r['selection']['artifact']['artifact_id'] for r in source['selectors']]
    _,rows=read_summary_outputs(Path(actual['execution_receipt']['output']),
        hashlib.sha256(Path(actual['execution_receipt']['output']).read_bytes()).hexdigest())
    assert [r['payload'].identity['selection']['artifact_id'] for r in rows]==expected
    assert {r['payload'].identity['pairing']['training']['seed'] for r in rows}=={122,722}


def test_public_tracin_uses_real_100_epoch_trajectory(tables, record_property):
    from experiments.modular_model import prepare_model
    from experiments.modular_run import read_dataset
    from experiments.target_direct_v1.methods import selected_checkpoint_indices
    from experiments.target_direct_v1.method_cache import resolve_methods
    root=tables[0]
    data,inputs=read_dataset(load_instance(root/'dataset.yaml','dataset_split'),root)
    instance=load_instance(ROOT/'experiments/configs/selectors/tracin_cp_point_6.yaml','selector')
    instance['model']['hidden_channels']=4
    model,trajectory,_=prepare_model(instance,data=data,dataset_name=inputs.dataset_name,
        checkpoint_root=root/'cp100',device=torch.device('cpu'),reference_directory=root)
    assert len(trajectory)==100
    incomplete = dict(instance['parameters'], checkpoint_steps=[])
    with pytest.raises(ValueError, match='exactly six'):
        selected_checkpoint_indices(trajectory,incomplete)
    observations={}
    for name,steps in [('tracin_cp_point_3',[1,50,100]),('tracin_cp_point_6',[1,10,25,50,75,100])]:
        item=load_instance(ROOT/('experiments/configs/selectors/'+name+'.yaml'),'selector')
        indices=selected_checkpoint_indices(trajectory,item['parameters'])
        assert [trajectory[i]['global_step'] for i in indices]==steps
        item['model']=instance['model'];item['budget']={'mode':'k','value':1,'k':1}
        result=resolve_methods(store_root=root/'tracin',data=data,dataset_name=inputs.dataset_name,
            model=model,checkpoints=trajectory,selectors=[item],model_config=item['model'],training=item['training'])[name]
        assert [c['global_step'] for c in result['score']['recipe']['fields']['trajectory']]==steps
        observations[name]={'steps':steps,'score':result['score']['artifact_id']}
    record_property('actual_trajectory',json.dumps(observations))


@pytest.mark.parametrize('field,value', [('seeds',[]),('seeds',[True]),('seeds',[1,1]),
    ('budget_ratios',[0]),('budget_ratios',[float('nan')]),('device','cuda'),('overrides',{'training':{'epochs':1}})])
def test_invalid_axes_fail_before_execution(matrix,field,value):
    root,path=matrix
    config=yaml.safe_load(path.read_text());config[field]=value;write_yaml(path,config)
    with pytest.raises(ValueError):execute(path,dry_run=True)
    assert not (root/'results').exists()
