"""Native saved-endpoint Metrics, compact collection and fail-closed pair inputs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
import torch
import yaml

from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, cli, commit, declaration
from test_syncmate_gu_outputs import collect
from experiments.ret_reference_policy import DETERMINISTIC
from experiments.ret_endpoint_metrics import CASE, METRICS, planned_pairs, validate_inputs, validate_pair
from experiments.response_diagnostics import prediction_triangle, prediction_by_label


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


GUARD = '''
import torch, sys
def blocked(*args, **kwargs): raise AssertionError('saved endpoint consumer performed model work')
torch.nn.modules.module.register_module_forward_pre_hook(blocked)
torch.optim.Adam.step = blocked
torch.optim.SGD.step = blocked
def profile(frame, event, arg):
    if event == 'call' and frame.f_code.co_name in ('train_reference','train_supervised','prepare_model','resolve_methods'):
        raise AssertionError('saved endpoint consumer called '+frame.f_code.co_name)
sys.setprofile(profile)
'''


def no_forward_cli(root, path, run_id):
    code = GUARD + "\nimport runpy\nrunpy.run_path('experiments/run.py', run_name='__main__')"
    return subprocess.run([sys.executable, '-B', '-c', code, str(path), '--run-id', run_id,
        '--syncmate', '--device-config', '.syncmate/device.yaml', '--verification-root', str(root)],
        cwd=root, capture_output=True, text=True, encoding='utf-8', timeout=120)


def test_per_label_complete_triangle_and_empty_class():
    o=np.array([[4,1,0],[1,4,0],[4,1,0],[1,4,0]], dtype=float)
    g=np.array([[4,1,0],[4,1,0],[1,4,0],[0,1,4]], dtype=float)
    r=np.array([[4,1,0],[1,4,0],[0,1,4],[4,1,0]], dtype=float)
    y=np.array([0,1,0,1])
    all_values=prediction_triangle(o,g,r,y)
    rows=prediction_by_label(o,g,r,y)
    assert len(rows)==3 and rows[2]['node_count']==0 and rows[2]['gu_accuracy'] is None
    assert sum(row['node_count'] for row in rows)==4
    assert all(sum(row[k] for row in rows)==v for k,v in all_values.items() if k.endswith('_count'))


@pytest.mark.parametrize('source_bound',[False,True])
def test_native_endpoint_metrics_collection_and_faults(workspace,source_bound,record_property):
    from experiments.modular_artifacts import read_run
    from experiments.modular_config import load_experiment
    from experiments.ret_reference_reading import load_endpoints, validate_trace
    from experiments.unlearning_outputs import load_metric_output
    from scripts.syncmate.opengu_acceptance import acceptance_payload
    from opengu_adapter import OpenGUProjectExtension
    from syncmate_core import context

    root,path,config=workspace
    reference_arm='joint' if source_bound else 'supervision_only'
    for key in ('seeds','budget_ratios'):config.pop(key,None)
    ret=yaml.safe_load((root/'retrain.yaml').read_text(encoding='utf-8'))
    ret['training']={'epochs':3000}
    write_yaml(root/'retrain.yaml',ret)
    base=dict(kind='experiment',schema_version=1,experiment_id='contract',
              dataset_refs=['dataset.yaml'],matrix='cartesian_product')
    if source_bound:
        config={**base,'stage':'unlearning','selector_refs':['degree.yaml'],'unlearning_refs':['retrain.yaml']}
        write_yaml(path,config);commit(root)
        old=cli(root,path,'old');assert old.returncode==0,old.stdout+old.stderr
        oldpath=root/'results/runs/contract/old/run.json'
        oldrun,_=read_run(oldpath,sha(oldpath))
        config={**base,'stage':'retrain_diagnostics','output_inputs':[dict(run=str(oldpath),sha256=sha(oldpath),cell_ids=[oldrun['cells'][0]['cell_id']])],
                'ret_reference':dict(policy=DETERMINISTIC,mode='reference',arms=['joint'])}
    else:
        write_yaml(path,{**base,'stage':'selector','selector_refs':['degree.yaml']});commit(root)
        prepared=cli(root,path,'prepare');assert prepared.returncode==0,prepared.stdout+prepared.stderr
        for arm in (reference_arm,'none'):
            write_yaml(root/('ret-'+arm+'.yaml'),{**ret,'reference':dict(policy=DETERMINISTIC,arm=arm)})
        config={**base,'stage':'unlearning','selector_refs':['degree.yaml'],
                'unlearning_refs':['ret-'+reference_arm+'.yaml','ret-none.yaml'],
                'execution':{'gu_cache':{'Retrain':'disabled'}},'observers':[dict(name='ret_reference_trace',methods=['Retrain'])]}
    write_yaml(path,config);commit(root)
    refs_result=cli(root,path,'refs');assert refs_result.returncode==0,refs_result.stdout+refs_result.stderr
    refpath=root/'results/runs/contract/refs/run.json'
    refs,docs=read_run(refpath,sha(refpath))
    replay=json.loads(docs[0]['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0]
    assert replay['endpoints']['best']['state_hash']!=replay['endpoints']['final']['state_hash']
    assert replay['validation_best']['epoch']<3000
    gu={**ret,'method':'GIF','parameters':{}}
    if not source_bound:
        none=json.loads(docs[1]['observers/ret_reference_trace/result.json'])['diagnostics']['replays'][0]
        gu['training']={'seed':42};gu['checkpoint']=str(root/none['endpoints']['final']['weights']['path'])
    gu_refs=[]
    for method in ('GIF','MEGU'):
        name=method+'.yaml';gu_refs.append(name)
        write_yaml(root/name,{**gu,'method':method})
    write_yaml(path,{**base,'stage':'unlearning','selector_refs':['degree.yaml'],'unlearning_refs':gu_refs});commit(root)
    updated=cli(root,path,'gu');assert updated.returncode==0,updated.stdout+updated.stderr
    gupath=root/'results/runs/contract/gu/run.json'
    gus,_=read_run(gupath,sha(gupath))
    descriptor=dict(run=str(refpath),sha256=sha(refpath),cell_id=refs['cells'][0]['cell_id'],
                    repeat='reference',policy=DETERMINISTIC,arm=reference_arm,endpoints=['final','best'])
    write_yaml(root/'endpoint.yaml',dict(kind='evaluation',schema_version=1,case=CASE))
    config={**base,'stage':'metrics','evaluation_refs':['endpoint.yaml'],
        'output_inputs':[dict(run=str(gupath),sha256=sha(gupath),cell_ids=[c['cell_id'] for c in gus['cells']])],
        'ret_endpoint_inputs':[descriptor]}
    write_yaml(path,config)
    definition=declaration(root,path,'metrics');execution_sha=commit(root)
    executed=no_forward_cli(root,path,'registered')
    assert executed.returncode==0,executed.stdout+executed.stderr
    measured=json.loads(executed.stdout)
    assert set(measured['generated_artifacts'])==set(definition['expected_artifact_paths'])
    assert len(definition['expected_artifact_paths'])==5
    out=root/'results/runs/contract/registered/run.json'
    manifest,measure_docs=read_run(out,sha(out))
    assert len(manifest['cells'])==2
    loaded=load_endpoints(refpath,sha(refpath),descriptor['cell_id'],dataset_root=root,store_root=root/'results/cache_v2')
    for cell,document,gu_cell in zip(manifest['cells'],measure_docs,gus['cells']):
        row=document['metrics.json']['rows'][0]
        assert set(row['values'])==set(METRICS) and 'baseline_output' not in row
        assert row['identity']['ret_endpoints']['input']==descriptor
        payload=load_metric_output(gu_cell['output'],root/'results/cache_v2',dataset_root=root)
        a=payload.arrays;mask=a['test_mask']
        from cache_v2 import canonical_sha256
        labels=row['identity']['protocol']['request_labels']
        assert labels['labels_hash']==payload.identity['pairing']['data_identity']['labels_hash']
        assert labels['k']==len(a['selected_nodes'])
        assert labels['ordered_nodes_hash']==canonical_sha256(a['selected_nodes'].tolist())
        assert labels['selected_label_sequence_sha256']==canonical_sha256(a['y'][a['selected_nodes']].tolist())
        assert sum(labels['deleted_class_counts'])==labels['k']
        assert sum(labels['retained_class_counts'])==int(a['train_mask'].sum())-labels['k']
        assert labels['count_basis']=='original_train_mask_not_reference_arm_supervision'
        for role in ('final','best'):
            r=loaded['endpoints']['reference'][role]['logits']['original']
            direct=prediction_triangle(a['logits_before'][mask],a['logits'][mask],r[mask],a['y'][mask])
            assert {k:row['values'][role+'_'+k] for k in direct}==direct
            by_class=row['identity']['protocol']['by_label'][role]
            assert all(sum(c[k] for c in by_class)==v for k,v in direct.items() if k.endswith('_count'))
        if gu_cell['conditions']['method']=='MEGU':assert row['identity']['protocol']['gu_prediction']=='MEGU_updated_C&S'
    collector=root/'collector';collector.mkdir()
    for p in root.glob('*.yaml'):(collector/p.name).write_bytes(p.read_bytes())
    with context.use(collector,extension=OpenGUProjectExtension()):
        collected,_,_=collect((root,collector,execution_sha,definition))
    request=collector/'accept-request.json'
    request.write_text(json.dumps(dict(definition=definition,context=collected),default=str),encoding='utf-8')
    fresh=GUARD+'''
import json, pathlib, sys
original=tuple(sys.argv)
from scripts.syncmate.opengu_acceptance import acceptance_payload
r=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
result=acceptance_payload('modular-output-v1',r['definition'],r['context'])
assert result['passed'] and result['accepted_cells']==2, result
assert tuple(sys.argv)==original and 'config' not in sys.modules
assert 'experiments.ret_reference_training' not in sys.modules
print(json.dumps(result))
'''
    accepted=subprocess.run([sys.executable,'-B','-c',fresh,str(request),'--project-root',str(collector),'console','--port','0'],
        cwd=root,capture_output=True,text=True,encoding='utf-8',timeout=60)
    assert accepted.returncode==0,accepted.stdout+accepted.stderr
    assert not list(collector.rglob('*.pt')) and not list(collector.rglob('*.npz'))
    assert not (collector/'results/cache_v2').exists()
    effective=load_experiment(path)
    for fault in ('missing','checksum','cell','arm','repeat','duplicate'):
        damaged=copy.deepcopy(effective)
        spec=damaged['ret_endpoint_inputs'][0]
        if fault=='missing':spec['run']=str(root/'missing.json')
        elif fault=='checksum':spec['sha256']='0'*64
        elif fault=='cell':spec['cell_id']='unknown'
        elif fault=='arm':spec['arm']='none'
        elif fault=='repeat':spec['repeat']='off1'
        else:damaged['ret_endpoint_inputs'].append(copy.deepcopy(spec))
        with pytest.raises((ValueError,KeyError,OSError)):planned_pairs(damaged)
    endpoint=next(iter(planned_pairs(effective).values()))
    payload=load_metric_output(gus['cells'][0]['output'],root/'results/cache_v2',dataset_root=root)
    for fault in ('selection','split','seed','graph'):
        altered=copy.deepcopy(payload)
        if fault=='selection':altered.identity['selection']['artifact_id']='wrong'
        elif fault=='split':altered.identity['pairing']['data_identity']['split_hash']='0'*64
        elif fault=='seed':altered.identity['pairing']['training']['seed']+=1
        else:altered.identity['pairing']['evaluation_graph_identity']['edge_index_hash']='0'*64
        with pytest.raises(ValueError):validate_pair(altered,endpoint,loaded)
    saved=json.loads(docs[0]['observers/ret_reference_trace/result.json'])
    saved['diagnostics']['replays'][0]['initial_state_hash']='0'*64
    with pytest.raises(ValueError):validate_trace(saved,docs[0]['observers/ret_reference_trace/trace.jsonl'],refs['cells'][0]['observers'][0],refs['cells'][0])
    asset=root/replay['endpoints']['best']['probes']['original']['path']
    original=asset.read_bytes()
    try:
        asset.write_bytes(b'bad')
        with pytest.raises(ValueError,match='checksum'):load_endpoints(refpath,sha(refpath),descriptor['cell_id'],dataset_root=root,store_root=root/'results/cache_v2')
    finally:asset.write_bytes(original)
    record_property('native_endpoint_metrics',json.dumps(dict(source_bound=source_bound,files=5,cells=2,
        final_epoch=3000,best_epoch=replay['validation_best']['epoch'],endpoint_states_differ=True,
        no_forward=True,fresh_collection_accepted=True,execution_sha=execution_sha)))
