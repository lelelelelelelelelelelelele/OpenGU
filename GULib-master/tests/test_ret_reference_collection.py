"""Real native CLI, Recipe assembly and lightweight collection for both Ret lanes."""
import copy
import hashlib
import json

import pytest
import yaml

from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, cli, commit, declaration
from test_syncmate_gu_outputs import collect
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context
from experiments.ret_reference_policy import ARMS, DETERMINISTIC


@pytest.mark.parametrize('source_bound',[False,True])
def test_native_ret_reference_collection(workspace,source_bound,record_property):
    from experiments.modular_artifacts import read_run
    root,path,config=workspace
    ret=yaml.safe_load((root/'retrain.yaml').read_text(encoding='utf-8'))
    ret['training']['epochs']=3000
    write_yaml(root/'retrain.yaml',ret)
    for key in ('seeds','budget_ratios'):config.pop(key,None)
    config.update(stage='unlearning',selector_refs=['degree.yaml'],unlearning_refs=['retrain.yaml'])
    if source_bound:
        alternate=copy.deepcopy(yaml.safe_load((root/'dataset.yaml').read_text(encoding='utf-8')))
        alternate['dataset']['name']='alternate_cpu_fixture'
        manifest=json.loads((root/alternate['artifacts']['manifest']).read_text(encoding='utf-8'))
        manifest['dataset']=alternate['dataset']
        alt=root/'data/processed/alternate.json'
        alt.write_text(json.dumps(manifest),encoding='utf-8')
        alternate['artifacts'].update(manifest='data/processed/alternate.json',manifest_sha256=hashlib.sha256(alt.read_bytes()).hexdigest())
        write_yaml(root/'alternate.yaml',alternate)
        config['dataset_refs']=['alternate.yaml','dataset.yaml']
        write_yaml(path,config);commit(root)
        source=cli(root,path,'source')
        assert source.returncode==0,source.stdout+source.stderr
        sourcepath=root/'results/runs/contract/source/run.json'
        sourcehash=hashlib.sha256(sourcepath.read_bytes()).hexdigest()
        source_run,_=read_run(sourcepath,sourcehash)
        assert source_run['cells'][1]['conditions']['dataset_index']==1
        config=dict(kind='experiment',schema_version=1,experiment_id='contract',stage='retrain_diagnostics',
            dataset_refs=['dataset.yaml'],matrix='cartesian_product',
            output_inputs=[dict(run=str(sourcepath),sha256=sourcehash,cell_ids=[source_run['cells'][1]['cell_id']])],
            ret_reference=dict(policy=DETERMINISTIC,mode='reference',arms=list(ARMS)))
    else:
        preparation={**config,'stage':'selector'}
        preparation.pop('unlearning_refs')
        write_yaml(path,preparation);commit(root)
        prepared=cli(root,path,'prepare')
        assert prepared.returncode==0,prepared.stdout+prepared.stderr
        refs=[]
        for arm in ARMS:
            name='ret-'+arm+'.yaml';refs.append(name)
            write_yaml(root/name,{**ret,'reference':dict(policy=DETERMINISTIC,arm=arm)})
        config.update(unlearning_refs=refs,execution={'gu_cache':{'Retrain':'disabled'}},
                      observers=[dict(name='ret_reference_trace',methods=['Retrain'])])
    write_yaml(path,config)
    definition=declaration(root,path,config['stage'])
    sha=commit(root)
    executed=cli(root,path,'registered')
    assert executed.returncode==0,executed.stdout+executed.stderr
    summary=json.loads(executed.stdout)
    assert set(summary['generated_artifacts'])==set(definition['expected_artifact_paths'])
    assert len(definition['expected_artifact_paths'])==17
    collector=root/'collector';collector.mkdir()
    for p in root.glob('*.yaml'):(collector/p.name).write_bytes(p.read_bytes())
    extension=OpenGUProjectExtension()
    with context.use(collector,extension=extension):
        collected,_,_=collect((root,collector,sha,definition))
        checked=extension.accept('modular-output-v1',definition,collected)
        assert checked['passed'],checked
        assert checked['accepted_cells']==4 and checked['scientific_acceptance']=='not_evaluated'
        results=extension.results(collected['artifact_index'],{'project_root':collector})
        assert len(results['rows'])==4 and not results['parse_errors'],results
    assert not (collector/'results/cache_v2').exists()
    assert not list(collector.rglob('*.pt')) and not list(collector.rglob('*.npz'))
    record_property('native_ret_reference',json.dumps(dict(source_bound=source_bound,arms=list(ARMS),
        files=17,accepted_cells=4,sha=sha,transport='local',device='cpu',scientific_acceptance='not_evaluated')))
