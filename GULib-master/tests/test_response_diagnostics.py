"""Scientific diagnostic partitions and the persisted Metrics execution path."""
import copy
import hashlib
import json
from types import SimpleNamespace

import numpy as np
import pytest

from experiments.response_diagnostics import (
    CORRECTNESS, RELATIONS, METRICS, prediction_triangle, request_composition, response_diagnostics)
from experiments.modular_artifacts import metric_source_cells
from experiments.modular_evaluation import evaluate_modular, resolve_evaluation
from test_modular_consumers import tables, run, write_yaml
from test_flip_hop_metrics import persisted, no_compute, sources


def ev():
    return resolve_evaluation(dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))


def test_all_relation_and_truth_states_reconstruct_all_endpoints():
    # Every possible truth pattern for each equality relation, including all-wrong.
    triples = np.array([[0,0,0],[1,1,1],[0,0,1],[0,0,1],[0,1,0],[0,1,0],
                        [1,0,0],[1,0,0],[0,1,2],[0,1,2],[0,1,2],[0,1,2]])
    y=np.array([0,0,0,1,0,1,0,1,0,1,2,3])
    a=[np.eye(4)[triples[:,i]] for i in range(3)]
    m=prediction_triangle(*a,y)
    assert [m[r+'_count'] for r in RELATIONS]==[2,2,2,2,4]
    expected=dict(all_equal=['111','000'], original_gu_equal=['110','001'],
                  original_retrain_equal=['101','010'],gu_retrain_equal=['011','100'],
                  all_different=['100','010','001','000'])
    for relation in RELATIONS:
        for bits in CORRECTNESS:
            assert m[relation+'_correct_'+bits+'_count']==int(bits in expected[relation])
    for i,name in enumerate(('original','gu','retrain')):
        restored=sum(m[r+'_correct_'+bits+'_count'] for r in RELATIONS for bits in CORRECTNESS if bits[i]=='1')
        assert restored/12==m[name+'_accuracy']
    for name,equal in (('original_gu','original_gu_equal'),('original_retrain','original_retrain_equal'),('gu_retrain','gu_retrain_equal')):
        assert m[name+'_disagreement_count']==12-m['all_equal_count']-m[equal+'_count']
    assert sum(m[r+'_count'] for r in RELATIONS)==m['node_count']


def test_empty_predictions_and_invalid_values():
    empty=np.zeros((0,2))
    m=prediction_triangle(empty,empty,empty,np.array([],dtype=np.int64))
    assert m['node_count']==0 and m['original_cross_entropy'] is None
    assert m['gu_retrain_disagreement'] is None
    json.dumps(m,allow_nan=False)
    bad=np.array([[np.nan,1.]])
    with pytest.raises(ValueError,match='invalid'):
        prediction_triangle(bad,bad,bad,np.array([0]))


def test_unique_incident_edges_reciprocals_self_loops_and_class_supervision():
    a=dict(y=np.array([0,1,1,0,1]),train_mask=np.array([1,1,1,0,0],bool),
           selected_nodes=np.array([0]),edge_index=np.array([[0,1,0,0,1,2],[1,0,1,0,2,3]]))
    mask=np.array([0,0,0,1,1],bool)
    m=request_composition(a,mask)
    assert m['original_edge_column_count']==6 and m['removed_edge_column_count']==4
    assert m['original_unique_undirected_edge_count']==4
    assert m['removed_unique_undirected_edge_count']==2
    assert m['deleted_class_counts']==[1,0] and m['retained_class_counts']==[0,2]
    assert m['test_3_hop_count']==1 and m['test_gt3_hop_count']==1


@pytest.mark.parametrize('ids',[[],['a','a'],['missing'],['b'],[1]])
def test_source_subset_rejects_invalid_or_non_output_cells(ids):
    source=dict(cells=[dict(cell_id='a',output={"artifact_id":"p"}),dict(cell_id='b')])
    with pytest.raises(ValueError,match='cell_ids'):
        metric_source_cells(source,dict(cell_ids=ids))


def test_subset_preserves_original_coordinate_order_and_matching_documents():
    cells=[dict(cell_id=x,output={'artifact_id':x}) for x in ('a','b','c')]
    chosen=metric_source_cells(dict(cells=cells),dict(cell_ids=['c','a']),['A','B','C'])
    assert chosen==[(cells[0],'A'),(cells[2],'C')]
    assert metric_source_cells(dict(cells=cells),{})==cells


def test_real_persisted_loader_metrics_export_and_cache_reuse(persisted,tables):
    from experiments.modular_artifacts import read_run
    from experiments.unlearning_outputs import load_metric_output
    root,refs=persisted
    write_yaml(root/'eval-response.yaml',dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))
    inputs=sources(root)
    for src in inputs:
        previous=json.loads(__import__('pathlib').Path(src['run']).read_text(encoding='utf-8'))
        src['cell_ids']=[c['cell_id'] for c in previous['cells']]
    result=run(tables,'response',stage='metrics',selector_refs=[],output_inputs=inputs,evaluation_refs=['eval-response.yaml'])
    e=result['evaluations'][0]
    assert len(e['rows'])==1 and len(e['not_applicable'])==1
    metrics=e['rows'][0]['metrics']
    assert set(metrics)==set(METRICS)
    assert metrics['node_count']==5 and metrics['gu_retrain_disagreement']==.6
    assert metrics['original_gu_disagreement']==.6 and metrics['original_retrain_disagreement']==0
    assert metrics['original_retrain_equal_count']==3
    path=root/'results/runs/response/response/run.json'
    actual,documents=read_run(path,hashlib.sha256(path.read_bytes()).hexdigest())
    assert len(actual['cells'])==1
    assert documents[0]['metrics.json']['rows'][0]['values']==metrics
    repeated=evaluate_modular(ev(),refs,store_root=root/'results/cache_v2',dataset_root=root)
    assert repeated['rows'][0]['metrics']==metrics
    gu,ret=[load_metric_output(ref,root/'results/cache_v2',dataset_root=root) for ref in refs]
    del gu.arrays['logits_before']
    with pytest.raises(ValueError,match='persisted Original'):
        response_diagnostics(gu,ret)


def test_subset_cannot_hide_corrupt_source_or_omit_required_retrain(persisted,tables):
    root,refs=persisted
    write_yaml(root/'eval-response.yaml',dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))
    inputs=sources(root)
    with pytest.raises(ValueError,match='exactly one verified Retrain'):
        run(tables,'missing-ret',stage='metrics',selector_refs=[],output_inputs=inputs[:1],evaluation_refs=['eval-response.yaml'])
    inputs[0]['sha256']='0'*64
    with pytest.raises(ValueError,match='checksum|digest|hash'):
        run(tables,'corrupt-source',stage='metrics',selector_refs=[],output_inputs=inputs,evaluation_refs=['eval-response.yaml'])
