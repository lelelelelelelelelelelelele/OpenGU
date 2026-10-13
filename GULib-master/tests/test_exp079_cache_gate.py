"""Post-collection acceptance checks use only disposable result documents."""
import copy
import hashlib
import json
from pathlib import Path

import pytest
import yaml
from scripts.verify_exp079_cache_gate import verify_pair

SHA = 'a' * 40
METHODS = ('GNNDelete','GIF','IDEA','MEGU','GraphEraser','GraphRevoker','Retrain')


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding='utf-8')


@pytest.fixture
def pair(tmp_path):
    config = tmp_path/'experiment.yaml'
    config.write_text('seeds: [212]\n',encoding='utf-8')
    digest = hashlib.sha256(config.read_bytes()).hexdigest()
    for mode in ('cold','warm'):
        spec = dict(schema_version=1,id=mode,runner='experiment',config_path='experiment.yaml',config_sha256=digest,
            configuration_fingerprint='b'*64,run_identity=dict(experiment_id='test-gate',run_id=mode),
            timeout_seconds=1800,logical_cells=252,stage='unlearning',
            expected_datasets=[dict(num_nodes=10,candidate_count=5)]*3,
            outputs=dict(root='results/runs/{experiment_id}/{run_id}',layout='modular-cells-v1',
                files=['run.json','metrics.json','selection.json','scores.npz']))
        path=tmp_path/'scripts/syncmate/recipes'/f'{mode}.yaml'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(yaml.safe_dump(spec),encoding='utf-8')
        binding=dict(job_id=mode,recipe=mode,git_sha=SHA,config_path='experiment.yaml',config_sha256=digest,
            run_identity=spec['run_identity'])
        receipt=dict(state='done',submitted_at='2026-10-13T01:00:00',
            started_at='2026-10-13T01:00:10' if mode=='cold' else '2026-10-13T01:05:00',
            finished_at='2026-10-13T01:04:00' if mode=='cold' else '2026-10-13T01:05:50',output_contract=binding)
        delivery=dict(ok=True,gate_passed=True,project_acceptance=dict(passed=True,accepted_cells=252),
            verify=dict(summary=dict(status='verified',verified_current=505,missing=0,conflicts=0)),
            completed_job=dict(id=mode,state='done',recipe=mode,expected_git_sha=SHA,receipt=receipt))
        write(tmp_path/'.syncmate/deliveries'/f'{mode}.json',dict(result=delivery))
        write(tmp_path/'.syncmate/runs'/f'{mode}.json',dict(execution=binding))
        cells=[]
        run_root=tmp_path/'results/runs/gpu4090/test-gate'/mode
        for ds in ('Cora','CiteSeer','PubMed'):
            for selected in range(12):
                for method in METHODS:
                    cid=f'{ds}-{selected}-{method}'
                    cell=dict(cell_id=cid,path=cid,status='completed',
                        conditions=dict(dataset_name=ds,seed=212,training_seed=212,budget_ratio=.1,method=method),
                        cache={name:'hit' for name in ('score','selection','method')},
                        producer_called={name:False for name in ('score','selection','method')},
                        cache_provenance=dict(evaluation={'reference':cid}),output=dict(reference=cid),
                        selection_id=f'{ds}-{selected}',timing=dict(current_access=dict(phase_seconds_exclusive={'output_query':.1})),files={})
                    keys=['evaluation']
                    if method!='Retrain':
                        keys+=['post_unlearning_utility_and_retrain_gap','post_unlearning_flip_hop']
                        cell['cache_provenance']['evaluations']={k:{'reference':cid+k} for k in keys[1:]}
                    cell['cache'].update({k:'miss' if mode=='cold' else 'hit' for k in keys})
                    cell['producer_called'].update({k:mode=='cold' for k in keys})
                    for name in ('metrics.json','selection.json'):
                        write(run_root/cid/name,dict(cell=cid,value=.5))
                        cell['files'][name]=dict(sha256=hashlib.sha256((run_root/cid/name).read_bytes()).hexdigest())
                    cells.append(cell)
        write(run_root/'run.json',dict(commit=SHA,status='completed',stage='unlearning',
            experiment_id='test-gate',run_id=mode,config_path='experiment.yaml',cells=cells))
        events=[]
        entries=[('run',None,None)]+[('selector','selection','hit')]*36+[('unlearning','artifact','hit')]*252
        entries += [('evaluation','result','miss' if mode=='cold' else 'hit')]*684
        for n,(stage,kind,outcome) in enumerate(entries):
            event=dict(git_sha=SHA,stage=stage,run_id=str(n),metadata=dict(execution_run_id=mode))
            events.append(dict(copy.deepcopy(event),state='started'))
            completed=dict(copy.deepcopy(event),state='completed')
            if kind:completed['cache']=[dict(type=kind,outcome=outcome)]
            events.append(completed)
        write(tmp_path/f'{mode}-audit.json',dict(run_id=mode,events=events))
    return dict(root=tmp_path,cold_recipe='cold',warm_recipe='warm',cold_job='cold',warm_job='warm',
        cold_audit=tmp_path/'cold-audit.json',warm_audit=tmp_path/'warm-audit.json',sha=SHA)


def test_complete_trusted_pair_compares_values_refs_and_receipt_wall(pair):
    result=verify_pair(**pair)
    assert result['passed'] and result['same_scientific_cells']==252
    assert result['same_metric_and_selection_files']==504
    assert result['cold']['runner_seconds']==230 and result['warm']['runner_seconds']==50


@pytest.mark.parametrize('fault', ['unverified','wrong_sha','partial','cold_hit','warm_computed','changed_reference',
                                 'changed_file','audit_failed','audit_wrong_run','warm_before_cold','duplicate_cell'])
def test_incomplete_or_inconsistent_pair_cannot_pass(pair,fault):
    root=pair['root']
    if fault in ('unverified','wrong_sha','warm_before_cold'):
        path=root/'.syncmate/deliveries/warm.json'
        value=json.loads(path.read_text(encoding='utf-8'))
        if fault=='unverified':value['result']['verify']['summary']['verified_current']=504
        elif fault=='wrong_sha':value['result']['completed_job']['expected_git_sha']='f'*40
        else:value['result']['completed_job']['receipt'].update(started_at='2026-10-13T01:01:00',finished_at='2026-10-13T01:02:00')
    elif fault.startswith('audit'):
        path=root/'warm-audit.json';value=json.loads(path.read_text(encoding='utf-8'))
        if fault=='audit_failed':value['events'][-1]['state']='failed'
        else:value['events'][-1]['metadata']['execution_run_id']='other-run'
    else:
        mode='cold' if fault=='cold_hit' else 'warm'
        path=root/f'results/runs/gpu4090/test-gate/{mode}/run.json';value=json.loads(path.read_text(encoding='utf-8'))
        if fault=='partial':value['cells'].pop()
        elif fault=='duplicate_cell':value['cells'][1]=value['cells'][0]
        elif fault=='cold_hit':value['cells'][0]['cache']['evaluation']='hit'
        elif fault=='warm_computed':value['cells'][0]['producer_called']['evaluation']=True
        elif fault=='changed_reference':value['cells'][0]['output']['reference']='foreign'
        else:
            file=path.parent/value['cells'][0]['path']/'metrics.json'
            file.write_text('changed',encoding='utf-8')
    write(path,value)
    with pytest.raises(ValueError):verify_pair(**pair)
