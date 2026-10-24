"""Metrics Recipe -> real CLI -> light collection -> exact cell acceptance."""
import copy
import hashlib
import json

from test_syncmate_execution_contract import workspace,cli,commit,declaration
from test_syncmate_gu_outputs import collect
from test_modular_consumers import tables,write_yaml
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context


def test_metrics_recipe_exact_subset_collects_and_accepts(workspace,record_property):
    root,path,config=workspace
    common=dict(kind='unlearning',schema_version=1,model=dict(architecture='OpenGU.GCNNet',hidden_channels=4),training=dict(epochs=3))
    write_yaml(root/'gif.yaml',dict(common,method='GIF'))
    write_yaml(root/'megu.yaml',dict(common,method='MEGU',parameters=dict(unlearning_epochs=1)))
    write_yaml(root/'degree.yaml',dict(kind='selector',schema_version=1,method='degree',candidate=dict(pool='train_mask'),budget=dict(mode='ratio',value=.1)))
    config.update(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['gif.yaml','megu.yaml','retrain.yaml'],seeds=[42],budget_ratios=[.1,.2])
    write_yaml(path,config)
    commit(root)
    produced=cli(root,path,'producer')
    assert produced.returncode==0,produced.stdout+produced.stderr
    source=root/'results/runs/contract/producer/run.json'
    document=json.loads(source.read_text(encoding='utf-8'))
    assert len(document['cells'])==6
    selected=[c for c in document['cells'] if c['conditions']['budget_ratio']==.1]
    assert len(selected)==3
    ids=[c['cell_id'] for c in selected]
    write_yaml(root/'response.yaml',dict(kind='evaluation',schema_version=1,case='post_unlearning_response_diagnostics'))
    config=dict(kind='experiment',schema_version=1,experiment_id='contract',stage='metrics',dataset_refs=['dataset.yaml'],matrix='cartesian_product',evaluation_refs=['response.yaml'],output_inputs=[dict(run=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),cell_ids=ids)])
    write_yaml(path,config)
    definition=declaration(root,path,'metrics')
    expected=[c for c in selected if c['conditions']['method']!='Retrain']
    assert len(definition['expected_cells'])==2
    assert [c['cell_id'] for c in definition['expected_cells']]==[c['cell_id'] for c in expected]
    assert len(definition['expected_artifact_paths'])==5
    sha=commit(root)
    executed=cli(root,path,'registered')
    assert executed.returncode==0,executed.stdout+executed.stderr
    actual=json.loads((root/definition['expected_artifact_paths'][0]).read_text(encoding='utf-8'))
    assert len(actual['cells'])==2 and actual['commit']==sha
    assert all(not c['producer_called'].get('method',False) for c in actual['cells'])
    collector=root/'collector';collector.mkdir()
    for source_yaml in root.glob('*.yaml'):(collector/source_yaml.name).write_bytes(source_yaml.read_bytes())
    extension=OpenGUProjectExtension()
    with context.use(collector,extension=extension):
        collected,_,_=collect((root,collector,sha,definition))
        accepted=extension.accept('modular-output-v1',definition,collected)
        assert accepted['passed'],accepted['errors']
        assert accepted['accepted_cells']==2
        missing=copy.deepcopy(definition);missing['expected_cells'].pop()
        assert not extension.accept('modular-output-v1',missing,collected)['passed']
        wrong=copy.deepcopy(definition);wrong['expected_cells'][0]['conditions']['seed']=999
        assert not extension.accept('modular-output-v1',wrong,collected)['passed']
    assert not (collector/'data').exists() and not (collector/'results/cache_v2').exists()
    assert not (collector/'results/runs/contract/producer').exists()
    record_property('metrics_collection',json.dumps(dict(source_cells=6,exact_input_cells=3,expected_cells=2,verified_artifacts=5,accepted_cells=accepted['accepted_cells'],wrong_count_and_conditions_rejected=True,source_run_collected=False,scientific_acceptance=accepted['scientific_acceptance'])))
