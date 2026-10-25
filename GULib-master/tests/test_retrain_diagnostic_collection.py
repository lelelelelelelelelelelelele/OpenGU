"""Real Ret diagnostic CLI and lightweight local collection through existing Core."""
import copy
import hashlib
import json

from test_modular_consumers import tables,write_yaml
from test_syncmate_execution_contract import workspace,cli,commit,declaration
from test_syncmate_gu_outputs import collect
from syncmate_core.project import GenericProjectExtension
from scripts.syncmate.opengu_acceptance import acceptance_payload
from scripts.syncmate.opengu_results import results_payload
from syncmate_core import context


def test_retrain_diagnostic_cli_collect_accept_and_results(workspace,record_property):
    import yaml
    from experiments.modular_artifacts import read_run
    runner,path,config=workspace
    ret=yaml.safe_load((runner/'retrain.yaml').read_text(encoding='utf-8'))
    ret['training']['epochs']=3000
    write_yaml(runner/'retrain.yaml',ret)
    alternate=copy.deepcopy(yaml.safe_load((runner/'dataset.yaml').read_text(encoding='utf-8')))
    alternate['dataset']['name']='alternate_cpu_fixture'
    manifest=json.loads((runner/alternate['artifacts']['manifest']).read_text(encoding='utf-8'))
    manifest['dataset']=alternate['dataset']
    alternate_path=runner/'data/processed/alternate.json'
    alternate_path.write_text(json.dumps(manifest),encoding='utf-8')
    alternate['artifacts'].update(manifest='data/processed/alternate.json',
        manifest_sha256=hashlib.sha256(alternate_path.read_bytes()).hexdigest())
    write_yaml(runner/'alternate.yaml',alternate)
    config.update(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['retrain.yaml'],
        dataset_refs=['alternate.yaml','dataset.yaml'])
    for key in ('seeds','budget_ratios'):config.pop(key,None)
    write_yaml(path,config);commit(runner)
    produced=cli(runner,path,'source')
    assert produced.returncode==0,produced.stdout+produced.stderr
    old_path=runner/'results/runs/contract/source/run.json'
    old_sha=hashlib.sha256(old_path.read_bytes()).hexdigest()
    old,_=read_run(old_path,old_sha)
    assert old['cells'][1]['conditions']['dataset_index']==1
    config=dict(kind='experiment',schema_version=1,experiment_id='contract',stage='retrain_diagnostics',
        dataset_refs=['dataset.yaml'],matrix='cartesian_product',
        output_inputs=[dict(run=str(old_path),sha256=old_sha,cell_ids=[old['cells'][1]['cell_id']])])
    write_yaml(path,config)
    definition=declaration(runner,path,'retrain_diagnostics')
    sha=commit(runner)
    executed=cli(runner,path,'registered')
    assert executed.returncode==0,executed.stdout+executed.stderr
    summary=json.loads(executed.stdout)
    assert set(summary['generated_artifacts'])==set(definition['expected_artifact_paths'])
    assert len(definition['expected_artifact_paths'])==5
    assert definition['expected_cells'][0]['conditions']['dataset_index']==1
    assert len(definition['expected_datasets'])==1
    collector=runner/'collector';collector.mkdir()
    for p in runner.glob('*.yaml'):(collector/p.name).write_bytes(p.read_bytes())
    extension=GenericProjectExtension()
    with context.use(collector,extension=extension):
        collected,_,_=collect((runner,collector,sha,definition))
        checked=acceptance_payload('modular-output-v1',definition,collected)
        assert checked['passed'],checked
        assert checked['accepted_cells']==1 and checked['scientific_acceptance']=='not_evaluated'
        results=results_payload(collected['artifact_index'],{'project_root':collector})
        assert len(results['rows'])==1 and not results['parse_errors'],results
    assert not (collector/'results/cache_v2').exists()
    assert not list(collector.rglob('*.pt')) and not list(collector.rglob('*.npz'))
    assert list(collector.rglob('trace.jsonl'))
    record_property('ret_real_collection',json.dumps(dict(accepted_cells=1,files=5,
        source_sha=sha,transport='local',formal_gpu=False,scientific_acceptance='not_evaluated')))
