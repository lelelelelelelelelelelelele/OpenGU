"""Work Plan evidence boundaries and one-way Block integration."""
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from scripts.dashboard import workplan_model as model
from scripts.dashboard import workplan_view as view


def records():
    return model.load(view.ROOT)[1]


def test_current_experiments_preserve_numbered_identity_and_separate_stages():
    rows = records()
    assert len(rows) == 25
    lookup = {r['id']:r for r in rows}
    assert lookup['AAGU-011']['execution']['state'] == 'completed'
    assert lookup['AAGU-011']['decision']['state'] == 'pending'
    assert lookup['AAGU-066']['execution']['state'] == 'pending'
    assert lookup['AAGU-056']['execution']['state'] == 'completed'
    assert lookup['AAGU-056']['analysis']['state'] == 'not_started'
    assert lookup['AAGU-032']['decision']['state'] != 'accepted'


@pytest.mark.parametrize('defect', ['id','state','evidence','analysis','decision','cycle','unknown_dependency','block','event','config'])
def test_invalid_records_fail_closed(defect):
    rows = copy.deepcopy(records()); r = rows[0]
    if defect == 'id': r['id'] = '../oops'
    if defect == 'state': r['execution']['state'] = 'maybe'
    if defect == 'evidence': r['execution']['evidence'] = []
    if defect == 'analysis': r['analysis']['evidence'] = []
    if defect == 'decision': r['decision']['evidence'] = []
    if defect == 'cycle': r['dependencies'] = [dict(experiment=r['id'],stage='analysis',reason='x',requirement='evidence')]
    if defect == 'unknown_dependency': r['dependencies'] = [dict(experiment='AAGU-999',stage='analysis',reason='x',requirement='evidence')]
    if defect == 'block': r['blocks'] = [dict(id='bad',stage='execution',reason='x')]
    if defect == 'event': r['history'].append(copy.deepcopy(r['history'][0]))
    if defect == 'config': r['configs'][0]['path'] = 'script.py'
    with pytest.raises(ValueError): model.validate(rows)


def write_block(root, code, status):
    path=root/f'.workblock/items/{code}/WORKITEM.md';path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(f'# Block\n当前状态: `{status}`\n',encoding='utf-8')
    return path


def test_block_status_is_read_only_fail_closed_and_needs_delivery(tmp_path):
    dep=dict(id='AAGU-072',delivery_confirmed=False)
    assert not model.block_status(tmp_path,dep)['resolved']
    p=write_block(tmp_path,'AAGU-072','accepted');before=p.read_bytes()
    assert not model.block_status(tmp_path,dep)['resolved']
    dep['delivery_confirmed']=True
    assert model.block_status(tmp_path,dep)['resolved']
    assert p.read_bytes()==before
    for status in ['working / claimed','not accepted','awaiting acceptance','closed / not accepted','unknown']:
        write_block(tmp_path,'AAGU-072',status)
        assert not model.block_status(tmp_path,dep)['resolved']


def test_unrelated_block_and_graph_changes_do_not_change_experiment_or_view(tmp_path):
    frame,rows=model.load(view.ROOT);sources=view.Sources(view.ROOT,tmp_path)
    page=tmp_path/'index.html'
    before=view.index_page(frame,rows,sources,page)
    serialized=json.dumps(rows,ensure_ascii=False)
    write_block(tmp_path,'AAGU-999','accepted')
    (tmp_path/'.workblock/graph.json').write_text('invalid irrelevant data')
    assert view.index_page(frame,rows,sources,page)==before
    assert json.dumps(rows,ensure_ascii=False)==serialized
    write_block(tmp_path,'AAGU-070','accepted')
    after=view.index_page(frame,rows,sources,page)
    assert after!=before
    assert json.dumps(rows,ensure_ascii=False)==serialized


def test_010_012_stage_specific_dependencies_are_preserved():
    lookup={r['id']:r for r in records()}
    assert lookup['AAGU-010']['blocks'][0]['id']=='AAGU-072'
    dep=next(d for d in lookup['AAGU-012']['dependencies'] if d['experiment']=='AAGU-010')
    assert dep['stage']=='analysis'
    assert lookup['AAGU-012']['analysis']['state']=='review'


def test_accepted_negative_result_does_not_unlock_cross_dataset_run(tmp_path):
    rows=records();lookup={r['id']:r for r in rows}
    parent=lookup['AAGU-066'];child=lookup['AAGU-067']
    parent['decision']['state']='accepted'
    parent['decision']['success_confirmed']=False
    assert not model.dependencies(child,rows,tmp_path)[0]['resolved']
    parent['decision']['success_confirmed']=True
    assert model.dependencies(child,rows,tmp_path)[0]['resolved']


def test_yaml_rendering_uses_actual_file_and_escapes_html(tmp_path):
    p=tmp_path/'experiments/configs/test.yaml';p.parent.mkdir(parents=True)
    p.write_text('kind: experiment\nbudget_ratios: [0.1]\nlabel: "<script>"\n')
    config=dict(path='experiments/configs/test.yaml',label='config',role='current')
    sources=view.Sources(tmp_path,tmp_path)
    text=view.config_preview(config,sources,tmp_path/'index.html')
    assert '0.1' in text and '&lt;script&gt;' in text
    p.write_text('budget_ratios: [')
    with pytest.raises(ValueError,match='Invalid YAML'):view.config_preview(config,sources,tmp_path/'index.html')


def test_catalog_classifies_development_without_registering_experiments():
    rows=records();catalog=view.catalog(view.ROOT,rows)
    assert any(c['owner']=='AAGU-032' for c in catalog)
    assert any(c['owner']=='AAGU-063' and c['kind']=='development' for c in catalog)
    assert not any(r['id']=='AAGU-063' for r in rows)
    assert len({c['path'] for c in catalog})==len(catalog)


@pytest.mark.parametrize('path',['../secret','/absolute','C:/secret','bad\\path','../../OpenGU-DocMap/../secret'])
def test_unsafe_source_paths_rejected(path,tmp_path):
    with pytest.raises(ValueError):model.resolve(tmp_path,tmp_path,path)


def test_diagram_valid_and_all_explicit_dependencies_present(tmp_path):
    rows=records();svg=view.diagram(rows,tmp_path)
    root=ET.fromstring(svg)
    targets=[x.attrib['href'] for x in root.iter() if x.tag.endswith('}a')]
    assert set(targets)=={'experiments/'+r['id']+'.html' for r in rows if r['blocks'] or r['dependencies']}
    assert 'Block AAGU-072' in svg


def test_repeated_generation_is_deterministic_and_escapes_data(tmp_path):
    frame,rows=model.load(view.ROOT); sources=view.Sources(view.ROOT,tmp_path)
    assert view.index_page(frame,rows,sources,tmp_path/'index.html')==view.index_page(frame,rows,sources,tmp_path/'index.html')
    rows[0]['title']='</text><script>alert(1)</script>'
    content=view.index_page(frame,rows,sources,tmp_path/'index.html')
    assert '</text><script>alert(1)' not in content and '&lt;script&gt;alert(1)' in content


def test_manifest_binding_checks_identity_count_and_file_hash(tmp_path):
    p=tmp_path/'results/run/run.json';p.parent.mkdir(parents=True)
    artifact=p.parent/'cells/a/metrics.json';artifact.parent.mkdir(parents=True);artifact.write_text('{}')
    run=dict(run_id='r1',experiment_id='e1',commit='a'*40,cells=[dict(cell_id='a',path='cells/a',status='completed',files={'metrics.json':{'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}})])
    p.write_text(json.dumps(run))
    bound=dict(path='results/run/run.json',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),experiment_id='e1',commit='a'*40,completed=1)
    rows=[{'attempts':[dict(run_id='r1',manifest=bound)]}]
    assert model.verify_manifests(rows,tmp_path,tmp_path)==2
    bound['completed']=2
    with pytest.raises(ValueError,match='count mismatch'):model.verify_manifests(rows,tmp_path,tmp_path)
    bound['completed']=1;artifact.write_text('changed')
    with pytest.raises(ValueError,match='checksum mismatch'):model.verify_manifests(rows,tmp_path,tmp_path)


def test_missing_evidence_not_silently_omitted(tmp_path):
    with pytest.raises(ValueError,match='Missing sources'):
        model.check_links({},[{'evidence':[dict(label='result',path='missing.json')]}],tmp_path,tmp_path)
