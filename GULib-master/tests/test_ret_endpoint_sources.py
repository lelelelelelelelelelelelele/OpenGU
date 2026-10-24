"""Call-local reuse of strictly read Ret runs; descriptor checks remain per input."""
import copy
import json
from pathlib import Path

import pytest

from experiments import modular_artifacts
from experiments.effective_config import ConfigurationError
from experiments.ret_endpoint_metrics import endpoint_sources, planned_pairs
from experiments.ret_reference_policy import DETERMINISTIC


@pytest.fixture
def sources(tmp_path, monkeypatch):
    cells=[];documents=[];descriptors=[]
    for number in range(2):
        cell=dict(cell_id='ret'+str(number),selection_id='selection'+str(number),conditions=dict(
            method='Retrain',seed=42,model='GCN',dataset_name='tiny',dataset_fingerprint='fp'))
        replay=dict(repeat='reference',identity=dict(policy=DETERMINISTIC,arm='joint'),
                    endpoints=dict(final=dict(state_hash='final'),best=dict(state_hash='best')))
        document={'selection.json':dict(selected_nodes=[number]),
                  'observers/ret_reference_trace/result.json':json.dumps(dict(diagnostics=dict(replays=[replay]))).encode()}
        cells.append(cell);documents.append(document)
        descriptors.append(dict(run='ret/run.json',sha256='a'*64,cell_id=cell['cell_id'],
            repeat='reference',policy=DETERMINISTIC,arm='joint',endpoints=['final','best']))
    calls=[]
    def reader(path,expected):
        calls.append((Path(path).resolve(),expected))
        if expected!='a'*64:raise ValueError('run checksum mismatch')
        if Path(path).name=='gu.json':
            gu=copy.deepcopy(cells[:1]);gu[0]['conditions']['method']='GIF';gu[0]['cell_id']='gu'
            gu[0]['output']={'fixture':'persisted-output'}
            return dict(cells=gu),documents[:1]
        return dict(cells=cells),documents
    monkeypatch.setattr(modular_artifacts,'read_run',reader)
    config=dict(source_directory=str(tmp_path),ret_endpoint_inputs=descriptors,
                output_inputs=[dict(run='gu.json',sha256='a'*64,cell_ids=['gu'])])
    return config,cells,documents,calls


def test_one_strict_read_per_unique_run_and_fresh_next_call(sources):
    config,cells,documents,calls=sources
    rows=endpoint_sources(config)
    assert len(calls)==1 and len(rows)==2
    assert [row['cell'] for row in rows]==cells
    assert [row['document'] for row in rows]==documents
    assert [row['input'] for row in rows]==config['ret_endpoint_inputs']
    assert all(set(row['replay']['endpoints'])=={'final','best'} for row in rows)
    assert endpoint_sources(config)==rows
    assert len(calls)==2


def test_resolved_path_alias_reuses_but_preserves_declared_path(sources):
    config,_,_,calls=sources
    config['ret_endpoint_inputs'][1]['run']='ret/../ret/run.json'
    rows=endpoint_sources(config)
    assert len(calls)==1
    assert rows[1]['path']==Path(config['source_directory'])/'ret/../ret/run.json'
    assert rows[1]['input']['run']=='ret/../ret/run.json'


def test_distinct_path_is_a_distinct_strict_read(sources):
    config,_,_,calls=sources
    config['ret_endpoint_inputs'][1]['run']='another/run.json'
    assert len(endpoint_sources(config))==2
    assert len(calls)==2 and calls[0][0]!=calls[1][0]


def test_same_path_different_declared_sha_is_not_reused(sources):
    config,_,_,calls=sources
    config['ret_endpoint_inputs'][1]['sha256']='b'*64
    with pytest.raises(ValueError,match='checksum'):endpoint_sources(config)
    assert len(calls)==2 and calls[0][1]!=calls[1][1]


@pytest.mark.parametrize('field,value', [('cell_id','missing'),('arm','none'),('repeat','on1'),
                                      ('repeat','off1'),('endpoints',['final'])])
def test_each_descriptor_still_rejects_invalid_coordinates(sources,field,value):
    config,_,_,_=sources
    config['ret_endpoint_inputs'][1][field]=value
    with pytest.raises(ConfigurationError):endpoint_sources(config)


def test_different_policy_and_missing_best_remain_rejected(sources):
    from experiments.ret_reference_policy import OBSERVED
    config,_,documents,_=sources
    config['ret_endpoint_inputs'][1]['policy']=OBSERVED
    with pytest.raises(ConfigurationError,match='policy'):endpoint_sources(config)
    config['ret_endpoint_inputs'][1]['policy']=DETERMINISTIC
    saved=json.loads(documents[1]['observers/ret_reference_trace/result.json'])
    del saved['diagnostics']['replays'][0]['endpoints']['best']
    documents[1]['observers/ret_reference_trace/result.json']=json.dumps(saved).encode()
    with pytest.raises(ConfigurationError,match='final/best'):endpoint_sources(config)


def test_second_call_revalidates_modified_source(sources):
    config,cells,_,calls=sources
    endpoint_sources(config)
    cells[1]['conditions']['method']='GIF'
    with pytest.raises(ConfigurationError,match='Ret cell'):endpoint_sources(config)
    assert len(calls)==2


def test_planned_pairs_rejects_unused_descriptor(sources):
    config,_,_,_=sources
    with pytest.raises(ConfigurationError,match='unused Ret'):planned_pairs(config)


def test_planned_pairs_rejects_alias_ambiguity(sources):
    config,_,_,_=sources
    second=copy.deepcopy(config['ret_endpoint_inputs'][0]);second['run']='ret/../ret/run.json'
    config['ret_endpoint_inputs'][1]=second
    with pytest.raises(ConfigurationError,match='ambiguous'):planned_pairs(config)


def test_planned_pairs_request_key_remains_exact(sources):
    config,_,_,_=sources
    config['ret_endpoint_inputs']=config['ret_endpoint_inputs'][1:]
    with pytest.raises(ConfigurationError,match='exactly one'):planned_pairs(config)
