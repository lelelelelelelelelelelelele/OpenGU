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


from test_syncmate_execution_contract import workspace, commit, declaration, FixtureRegistration
from syncmate_core import queue


@pytest.fixture
def exported(workspace):
    runner, path, config = workspace
    config.update(stage='unlearning', unlearning_refs=['gu.yaml', 'retrain.yaml'])
    write_yaml(path, config)
    sha = commit(runner)
    definition = declaration(runner, path, 'unlearning')
    with context.use(runner, extension=FixtureRegistration(definition)):
        submitted = queue.runner_queue_submit('cpu-job', definition['id'], expected_git_sha=sha)
        assert submitted['submitted'], submitted
        device, warnings = devices.load_device(runner / '.syncmate/device.yaml')
        assert not warnings
        result = queue.runner_queue_run_once(device)
        assert result['status'] == 'done', result
    collector = runner / 'collector'
    collector.mkdir()
    for source in runner.glob('*.yaml'):
        (collector / source.name).write_bytes(source.read_bytes())
    return runner, collector, sha, definition


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

