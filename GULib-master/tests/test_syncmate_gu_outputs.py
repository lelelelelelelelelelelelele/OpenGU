"""Ordinary command -> registered queue contract -> real local collect -> verified Result."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import torch
import yaml
from test_modular_consumers import tables,write_yaml
from test_unified_execution import matrix
from experiments.modular_config import configuration_fingerprint
from experiments.modular_run import execute
from experiments.modular_artifacts import ARTIFACT_NAMES,output_paths
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from opengu_recipes import recipe_definitions
from syncmate_core import collection,context,devices,index
from syncmate_core.identity import sha256_recipe_config
from syncmate_core.run_handoff import build_execution_contract

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture
def exported(matrix):
    runner,path=matrix
    config=yaml.safe_load(path.read_text());config['selector_refs']=['degree.yaml'];write_yaml(path,config)
    subprocess.run(['git','init','-q','-b','main',str(runner)],check=True)
    subprocess.run(['git','-C',str(runner),'-c','user.name=CPU fixture','-c','user.email=fixture@example.invalid',
        'commit','-q','--allow-empty','-m','isolated CPU runtime'],check=True)
    sha=subprocess.check_output(['git','-C',str(runner),'rev-parse','HEAD'],text=True).strip()
    definition=copy.deepcopy(recipe_definitions()['opengu-aagu007-v1'])
    summary='results/runs/modular/cpu-matrix/registered/summary.json'
    definition.update(config_path='experiment.yaml',config_sha256=sha256_recipe_config(path),
        configuration_fingerprint=configuration_fingerprint(path),logical_cells=8,
        expected_dataset={'num_nodes':20,'candidate_count':10},
        run_identity={'experiment_id':'cpu-matrix','run_id':'registered'},
        expected_artifact_paths=[summary]+list(output_paths(summary,8)),
        collector_result_roots=[str(Path(summary).parent).replace('\\','/')])
    (runner/'definition.json').write_text(json.dumps(definition))
    running=runner/'.syncmate/runner_queue/running';running.mkdir(parents=True)
    receipts=running.parent/'receipts';receipts.mkdir()
    job={'id':'cpu-job','recipe':definition['id'],'expected_git_sha':sha}
    write_yaml(running/'cpu-job.yaml',job)
    contract=build_execution_contract(definition,project='opengu',job_id='cpu-job',git_sha=sha)
    (receipts/'cpu-job.json').write_text(json.dumps({'output_contract':contract}))
    # Only OS/device policy is substituted for disposable CPU verification. The
    # real CLI, parser, queue identity, handoff, executor and output checks run.
    code=r"""
import json,sys,runpy
from pathlib import Path
from dataclasses import replace
from functools import partial
from scripts.syncmate import opengu_recipes
from experiments import syncmate_stage,modular_execution
root=Path(sys.argv[1]);definition=json.loads((root/'definition.json').read_text())
opengu_recipes.recipe_definitions=lambda:{definition['id']:definition}
def cpu_preflight(recipe_id,root):
    from experiments.modular_config import configuration_fingerprint
    from experiments.modular_run import execute
    assert configuration_fingerprint(root/definition['config_path'])==definition['configuration_fingerprint']
    assert execute(root/definition['config_path'],dry_run=True)['logical_cells']==8
    return {'ready':True,'errors':[],'level':'isolated_cpu_policy'}
syncmate_stage.preflight=cpu_preflight
original=modular_execution.project_context
modular_execution.project_context=lambda *a,**k: replace(original(*a,**k),request_device='cpu',level='verification')
syncmate_stage.run=partial(syncmate_stage.run,root=root)
import torch;torch.set_num_threads(1)
sys.argv=['experiments/run.py','--recipe',definition['id']]
runpy.run_path('experiments/run.py',run_name='__main__')
"""
    result=subprocess.run([sys.executable,'-B','-X','utf8','-c',code,str(runner)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0,result.stdout+result.stderr
    assert json.loads(result.stdout)['passed']
    collector=runner/'collector';collector.mkdir()
    # Collector configuration is the same reviewed small tables; no Cache or data copy.
    for source in runner.glob('*.yaml'):(collector/source.name).write_bytes(source.read_bytes())
    return runner,collector,sha,definition


def collect(exported):
    runner,collector,sha,definition=exported
    peer=devices.build_peer_config('runner',None,str(runner),transport='local')
    args=('cpu-runner',devices.transport_ssh_value(peer),str(runner),
        definition['collector_result_roots'],'results/runs/cpu-runner')
    options={'artifact_names':definition['collector_artifact_names'],
        'expected_paths':definition['expected_artifact_paths'],'expected_git_sha':sha,'save':True}
    result=collection.apply_collect(*args,**options)
    assert not result.get('errors'),result
    verified=collection.verify_collect(*args,**options)
    assert verified['summary']['status']=='verified',verified
    return {'project_root':collector,'node_id':'cpu-runner','expected_git_sha':sha,
        'artifact_index':index.load_artifact_index()},args,options


def test_real_queue_command_collect_verify_accept_results_and_repeat(exported,monkeypatch,record_property):
    runner,collector,sha,definition=exported;extension=OpenGUProjectExtension()
    def forbidden(*a,**k):raise AssertionError('collection or metrics called a producer')
    monkeypatch.setattr(torch.optim.Adam,'step',forbidden)
    hook=torch.nn.modules.module.register_module_forward_pre_hook(forbidden)
    try:
        with context.use(collector,extension=extension):
            collected,args,options=collect(exported)
            checked=extension.accept('modular-output-v1',definition,collected)
            assert checked['passed'],checked['errors']
            assert checked['accepted_cells']==8
            rows=extension.results(collected['artifact_index'],{'project_root':collector})
            assert len(rows['rows'])==8 and not rows['parse_errors'],rows
            assert all(r['status']=='ok' for r in rows['rows'])
            repeated=collection.apply_collect(*args,**options)
            assert repeated['summary']['fetched']==0
            record_property('actual_collection',json.dumps({'checked':checked,'row_count':len(rows['rows']),
                'repeat_fetched':0,'artifact_count':len(definition['expected_artifact_paths'])}))
    finally:hook.remove()
    assert not (collector/'results/cache_v2').exists()


@pytest.mark.parametrize('fault',['missing_output','unverified_index','duplicate_index','wrong_sha','bytes','config','semantic_budget','semantic_selector','semantic_dataset'])
def test_collection_faults_fail_closed(exported,fault):
    runner,collector,sha,definition=exported;extension=OpenGUProjectExtension()
    with context.use(collector,extension=extension):
        collected,_,_=collect(exported);peer=collected['artifact_index']['peers']['cpu-runner']
        if fault=='missing_output':peer['items'].pop()
        if fault=='unverified_index':peer['summary']['status']='incomplete'
        if fault=='duplicate_index':peer['items'].append(copy.deepcopy(peer['items'][0]))
        if fault=='wrong_sha':collected['expected_git_sha']='f'*40
        if fault=='bytes':(collector/peer['items'][0]['local_path']).write_bytes(b'corrupt')
        if fault=='config':definition['configuration_fingerprint']='f'*64
        if fault.startswith('semantic_'):
            entry=next(i for i in peer['items'] if i['remote_path'].endswith('/summary.json'))
            path=collector/entry['local_path'];summary=json.loads(path.read_text())
            if fault=='semantic_budget':summary['unlearning'][0]['matrix_values']['budget_ratio']=.9
            if fault=='semantic_selector':summary['selectors'][0]['selector_ref']='wrong.yaml'
            if fault=='semantic_dataset':summary['dataset']['split']['seed']=999
            path.write_text(json.dumps(summary));entry['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        result=extension.accept('modular-output-v1',definition,collected)
        assert not result['passed'] and result['errors']


def test_live_registration_uses_one_entry_and_all_reference_fingerprints():
    registry=recipe_definitions()
    assert set(registry)=={'smoke','opengu-preflight-v1','opengu-aagu007-v1'}
    definition=registry['opengu-aagu007-v1'];path=ROOT/definition['config_path']
    assert definition['argv']==('{python}','experiments/run.py','--recipe','opengu-aagu007-v1')
    assert configuration_fingerprint(path)==definition['configuration_fingerprint']
    assert sha256_recipe_config(path)==definition['config_sha256']
    assert execute(path,dry_run=True)['logical_cells']==definition['logical_cells']==4
    assert len(definition['expected_artifact_paths'])==17


def test_real_formal_preflight_refuses_cpu_before_dataset(monkeypatch):
    from experiments import syncmate_stage,modular_run
    from scripts.syncmate import verify_core_dependency
    monkeypatch.setattr(torch.cuda,'is_available',lambda:False)
    monkeypatch.setattr(verify_core_dependency,'verify_core_dependency',lambda:{'errors':[]})
    def forbidden(*a,**k):raise AssertionError('unavailable GPU reached formal data')
    monkeypatch.setattr(modular_run,'read_dataset',forbidden)
    checked=syncmate_stage.preflight('opengu-aagu007-v1')
    assert not checked['ready']
    assert any('no CPU fallback' in e for e in checked['errors'])
    assert any('canonical SSH' in e for e in checked['errors'])
