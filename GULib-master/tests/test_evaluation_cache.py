"""Cold/hot values, metadata-only metric HIT, and actual input consumption."""
import copy
import functools
from pathlib import Path

import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from test_unlearning_paired_evaluations import paired_tables


def setup(tables):
    root=paired_tables(tables)
    return root, dict(stage='unlearning',selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml','retrain.yaml'],evaluation_refs=['gap.yaml','flip.yaml'])


def forbid(patch, module, name):
    original=getattr(module,name)
    @functools.wraps(original)
    def blocked(*a,**k):raise AssertionError('hot evaluation invoked '+name)
    patch.setattr(module,name,blocked)


def test_hot_entry_reuses_complete_values_without_output_decode_or_formula(tables,monkeypatch,record_property):
    import experiments.unlearning_outputs as outputs
    import experiments.evaluation_cache as evaluation
    import experiments.modular_evaluation as modular
    import experiments.modular_model as model
    import experiments.output_metrics as metrics
    from cache_v2.unlearning_output import UnlearningOutputPayload
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    from experiments.c_target_v1.score_store import ScoreBundleStore
    monkeypatch.setattr(ScoreBundleStore, 'initialize',
                        lambda self: pytest.fail('warm Score opened writer initialization'))
    monkeypatch.setattr(ScoreBundleStore, '_load_candidate',
                        lambda *a, **k: pytest.fail('selection HIT loaded unused Score payload'))
    for row in cold['unlearning']:
        assert not row['evaluation_cache']['hit']
    for module,name in ((outputs,'load_output'),(evaluation,'single_values'),(modular,'_measure'),
            (model,'prepare_model'),(model,'train_supervised'),(metrics,'method_metrics'),(metrics,'update_detection')):
        forbid(monkeypatch,module,name)
    monkeypatch.setattr(UnlearningOutputPayload,'from_bytes',classmethod(lambda cls,*a:pytest.fail('hot NPZ decode')))
    reads=[]
    from cache_v2 import CacheIndex
    index=CacheIndex(root/'results/cache_v2/index.sqlite')
    output_directories={(root/'results/cache_v2'/index.get_artifact(r['artifact_id'])['semantic_path']).parent
                        for r in cold['unlearning']}
    original=Path.read_bytes
    def observed(path):
        if path.parent in output_directories:
            reads.append(path)
            pytest.fail('metric HIT opened unused Output payload/header')
        return original(path)
    monkeypatch.setattr(Path,'read_bytes',observed)
    hook=torch.nn.modules.module.register_module_forward_pre_hook(lambda *a:pytest.fail('hot forward'))
    try:
        warm=run(tables,'new-log-identity',**options)
    finally:hook.remove()
    assert not reads
    for before,after in zip(cold['unlearning'],warm['unlearning']):
        assert before['output']==after['output']
        assert before['result']==after['result'] and before['evaluation']==after['evaluation']
        assert after['hit'] and after['evaluation_cache']['hit']
        assert after['evaluation_cache']['artifact_id']==before['evaluation_cache']['artifact_id']
        assert after['evaluation_cache']['access_seconds']>0
    for before,after in zip(cold['evaluations'],warm['evaluations']):
        for a,b in zip(before['rows'],after['rows']):
            assert a['metrics']==b['metrics'] and a['identity']==b['identity']
            assert b['cache']['hit'] and not b['cache']['producer_called']
            assert b['cache']['artifact_id']==a['cache']['artifact_id']
    record_property('hot_complete_evaluation',str(dict(full_output_reads=0,npz_decode=0,formula_calls=0,
        dependency_npz_reads=len(reads),same_values=True,all_evaluations_hit=True)))


def test_selection_hit_does_not_consume_scores_until_requested(tables):
    from cache_v2 import CacheIndex
    from experiments.c_target_v1.score_store import ScoreBundleIntegrityError
    root, options = setup(tables)
    cold = run(tables, 'cold-selection', **options)
    reference = cold['selectors'][0]['score']
    index = CacheIndex(root/'results/cache_v2/index.sqlite')
    (root/'results/cache_v2'/index.get_artifact(reference['artifact_id'])['semantic_path']).unlink()
    warm = run(tables, 'selection-only', **options)
    assert warm['selectors'][0]['score']['artifact_id'] == reference['artifact_id']
    assert warm['selectors'][0]['selection']['cache']['hit']
    assert 'scores' not in warm['selectors'][0] and 'ranking' not in warm['selectors'][0]
    with pytest.raises(ScoreBundleIntegrityError, match='missing'):
        run(tables, 'actual-scores', return_scores=True, **options)


@pytest.mark.parametrize('dependency',['selection','graph','manifest','evaluation'])
def test_corruption_of_actually_consumed_input_is_refused(tables,monkeypatch,dependency):
    from cache_v2 import CacheIndex
    import experiments.modular_run as runner
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    index=CacheIndex(root/'results/cache_v2/index.sqlite')
    if dependency=='selection':
        path=root/'results/cache_v2'/index.get_artifact(cold['selectors'][0]['selection']['artifact']['artifact_id'])['semantic_path']
    elif dependency=='evaluation':
        aid=cold['unlearning'][0]['evaluation_cache']['artifact_id']
        path=root/'results/cache_v2'/index.get_artifact(aid)['semantic_path']
    else:path=root/('graph.pkl' if dependency=='graph' else 'dataset.json')
    original=path.read_bytes()
    path.write_bytes(original+b'broken owned dependency')
    forbid(monkeypatch,runner,'prepare_model')
    try:
        with pytest.raises(Exception,match='hash|digest|mismatch|canonical|size|JSON|assets'):
            run(tables,'refused',**options)
    finally:
        if dependency=='manifest':path.write_bytes(original)


@pytest.mark.parametrize('unused',['method','retrain','selection','graph','manifest'])
def test_cached_metrics_do_not_open_unused_upstream_files(tables,monkeypatch,unused):
    from cache_v2 import CacheIndex
    from experiments.modular_evaluation import evaluate_modular
    import experiments.unlearning_outputs as outputs
    import experiments.modular_evaluation as modular
    import utils.target_checkpoint as checkpoint
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    item=cold['evaluations'][1]['effective_config']
    index=CacheIndex(root/'results/cache_v2/index.sqlite')
    if unused in ('method','retrain'):
        aid=cold['unlearning'][0 if unused=='method' else 1]['artifact_id']
        path=root/'results/cache_v2'/index.get_artifact(aid)['semantic_path']
    elif unused=='selection':
        aid=cold['selectors'][0]['selection']['artifact']['artifact_id']
        path=root/'results/cache_v2'/index.get_artifact(aid)['semantic_path']
    else:path=root/('graph.pkl' if unused=='graph' else 'dataset.json')
    # Only this test's owned fixture is changed. These files are not consumed
    # by the requested cached metric and their absence must not cause a scan.
    path.unlink()
    forbid(monkeypatch,outputs,'load_output')
    forbid(monkeypatch,modular,'_measure')
    forbid(monkeypatch,checkpoint,'data_identity')
    forbid(monkeypatch,checkpoint,'sha256_file')
    warm=evaluate_modular(item,cold['unlearning'],store_root=root/'results/cache_v2',dataset_root=root)
    assert [r['metrics'] for r in warm['rows']]==[r['metrics'] for r in cold['evaluations'][1]['rows']]
    assert all(r['cache']['hit'] and not r['cache']['producer_called'] for r in warm['rows'])


def test_metric_miss_loads_required_output_and_reports_missing_file(tables,monkeypatch):
    from cache_v2 import CacheIndex
    from experiments.modular_evaluation import evaluate_modular
    import experiments.modular_evaluation as modular
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    index=CacheIndex(root/'results/cache_v2/index.sqlite')
    path=root/'results/cache_v2'/index.get_artifact(cold['unlearning'][0]['artifact_id'])['semantic_path']
    path.unlink()
    item={**cold['evaluations'][1]['effective_config'],'producer_version':'new-metric-protocol'}
    forbid(monkeypatch,modular,'_measure')
    with pytest.raises(Exception,match='missing'):
        evaluate_modular(item,cold['unlearning'],store_root=root/'results/cache_v2',dataset_root=root)


def test_cached_metric_rejects_foreign_registered_reference(tables):
    from experiments.modular_evaluation import evaluate_modular
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    foreign=copy.deepcopy(cold['unlearning'])
    foreign[0]['output']['content_hash']='0'*64
    with pytest.raises(Exception,match='identity mismatch'):
        evaluate_modular(cold['evaluations'][1]['effective_config'],foreign,
                         store_root=root/'results/cache_v2',dataset_root=root)


def test_protocol_libraries_and_actual_output_change_invalidate_only_evaluation(tables,monkeypatch):
    import numpy as np
    from experiments.modular_evaluation import resolve_evaluation,evaluate_modular
    root,options=setup(tables)
    cold=run(tables,'cold',**options)
    item=resolve_evaluation(dict(kind='evaluation',schema_version=1,case='post_unlearning_utility'))
    arguments=dict(store_root=root/'results/cache_v2',dataset_root=root)
    first=evaluate_modular(item,cold['unlearning'],**arguments)
    assert all(not r['cache']['hit'] for r in first['rows'])
    warm=evaluate_modular(item,cold['unlearning'],**arguments)
    assert all(r['cache']['hit'] for r in warm['rows'])
    changed={**item,'producer_version':'changed-scientific-protocol'}
    assert all(not r['cache']['hit'] for r in evaluate_modular(changed,cold['unlearning'],**arguments)['rows'])
    with monkeypatch.context() as patch:
        patch.setattr(np,'__version__','changed-numerical-library')
        assert all(not r['cache']['hit'] for r in evaluate_modular(item,cold['unlearning'],**arguments)['rows'])
    assert all(r['cache']['hit'] for r in evaluate_modular(item,cold['unlearning'],**arguments)['rows'])
    gu=copy.deepcopy(tables[2]);gu['parameters']['unlearn_lr']=.02;write_yaml(root/'gu.yaml',gu)
    new=run(tables,'changed-real-output',**options)
    assert new['unlearning'][0]['output']!=cold['unlearning'][0]['output']
    assert not new['unlearning'][0]['evaluation_cache']['hit']
    assert new['unlearning'][1]['output']==cold['unlearning'][1]['output']
    assert new['unlearning'][1]['evaluation_cache']['hit']
    assert all(not e['rows'][0]['cache']['hit'] for e in new['evaluations'])


def test_distinct_declared_budgets_share_science_without_aliasing_audit(tables):
    import yaml
    from scripts.evaluation.reporting.events import read_event_stream
    root,options=setup(tables)
    selector=yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    selector['budget']={'mode':'ratio','value':.1}
    write_yaml(root/'degree.yaml',selector)
    # One GU only; both ratios select exactly the same one of ten candidates.
    result=run(tables,'budget-coordinates',**{**options,'unlearning_refs':['gu.yaml'],
        'evaluation_refs':['utility.yaml'],'budget_ratios':[.1,.19]})
    assert result['unlearning'][0]['output']==result['unlearning'][1]['output']
    events,_=read_event_stream(root/'runtime/_journal/auto_report.events.jsonl')
    evaluated=[e for e in events if e['stage']=='evaluation' and e['state']=='completed'
        and not e['identity'].get('evaluation_part')]
    assert {e['identity']['budget_ratio'] for e in evaluated}=={'0.1','0.19'}
    assert len({e['cell_id'] for e in evaluated})==2
    import json
    run_path=root/'results/runs/budget-coordinates/budget-coordinates/run.json'
    exported=json.loads(run_path.read_text(encoding='utf-8'))
    for cell in exported['cells']:
        ratio=cell['conditions']['budget_ratio']
        measured=next(row for row in result['evaluations'][0]['rows'] if row['execution_conditions']==cell['conditions'])
        assert cell['cache']['post_unlearning_utility']==('hit' if measured['cache']['hit'] else 'miss')
        assert cell['producer_called']['post_unlearning_utility']==measured['cache']['producer_called']
        assert cell['timing']['post_unlearning_utility_access_seconds']==measured['cache']['access_seconds']
        document=json.loads((run_path.parent/cell['path']/'metrics.json').read_text(encoding='utf-8'))
        assert len([r for r in document['rows'] if r['stage']=='post_unlearning_utility'])==1


def test_uncached_run_outputs_still_support_ordinary_metrics(tables):
    import hashlib
    root,options=setup(tables)
    cold=run(tables,'disabled',**options,execution={'gu_cache':{'GNNDelete':'disabled','Retrain':'disabled'}})
    assert all(row['output']['storage']=='run' for row in cold['unlearning'])
    source=root/'results/runs/disabled/disabled/run.json'
    measured=run(tables,'disabled-metrics',stage='metrics',selector_refs=[],evaluation_refs=['gap.yaml','flip.yaml'],
        output_inputs=[{'run':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}])
    for before,after in zip(cold['evaluations'],measured['evaluations']):
        assert [r['metrics'] for r in before['rows']]==[r['metrics'] for r in after['rows']]
        assert all(r['cache'] is None for r in after['rows'])


def test_same_request_preparation_is_shared_within_run_but_not_between_runs(tables, monkeypatch):
    import yaml
    import experiments.node_deletion as deletion
    import experiments.modular_gu as gu
    root, options = setup(tables)
    selector = yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    selector['budget'] = {'mode':'ratio','value':.1}
    write_yaml(root/'degree.yaml',selector)
    options = {**options,'budget_ratios':[.1,.19]}
    cold = run(tables,'prepared-cold',**options)
    calls = {'pairing':0,'producer':0}
    def observe(name, original):
        @functools.wraps(original)
        def measured(*args,**kwargs):
            calls[name] += 1
            return original(*args,**kwargs)
        return measured
    monkeypatch.setattr(deletion,'pairing_identity',observe('pairing',deletion.pairing_identity))
    monkeypatch.setattr(gu,'_gu_producer',observe('producer',gu._gu_producer))
    for name in ('prepared-hot-1','prepared-hot-2'):
        warm = run(tables,name,**options)
        assert [r['output'] for r in warm['unlearning']] == [r['output'] for r in cold['unlearning']]
        assert all(r['evaluation_cache']['hit'] for r in warm['unlearning'])
    assert calls == {'pairing':0,'producer':4}
