"""Work Plan evidence boundaries and one-way Block integration."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
import pytest
from scripts.dashboard import workplan_model as model
from scripts.dashboard import workplan_view as view


def records():
    """Synthetic state: tests must work in a fresh clone without local plans."""
    evidence = [dict(label='report', path='report.md')]
    rows = []
    for code in ('AAGU-001', 'AAGU-002'):
        r = dict(id=code, title=code, family='main', category='active',
                 question='Question', scope='Frozen scope', next_step='Review',
                 reviewed_at='2026-09-22', sources=evidence,
                 configs=[dict(label='config', path='experiments/configs/test.yaml', role='current')],
                 preparation=dict(state='defined', note='Defined', evidence=[]),
                 execution=dict(state='completed', note='Complete', evidence=evidence),
                 analysis=dict(state='complete', note='Analysis', evidence=evidence),
                 decision=dict(state='accepted', note='Decision', evidence=evidence, success_confirmed=True),
                 dependencies=[], blocks=[], attempts=[],
                 history=[dict(id='observed', at='2026-09-22', stage='analysis', note='Observed', evidence=evidence)])
        r['published_analysis'] = {k:copy.deepcopy(r[k]) for k in
                                  ('id','title','question','scope','configs','sources','attempts','analysis','decision','history')}
        r['published_analysis']['recorded_at'] = r['reviewed_at']
        rows.append(r)
    rows[0]['blocks'] = [dict(id='AAGU-072',stage='execution',reason='software',
                             delivery_confirmed=True,delivery_note='verified')]
    rows[1]['dependencies'] = [dict(experiment='AAGU-001',stage='analysis',reason='parent',requirement='successful_acceptance')]
    return rows


def frame():
    return model.read_json(view.SOURCE / 'framework.json')


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
    framework,rows=frame(),records();sources=view.Sources(view.ROOT,tmp_path)
    page=tmp_path/'index.html'
    before=view.index_page(framework,rows,sources,page)
    serialized=json.dumps(rows,ensure_ascii=False)
    write_block(tmp_path,'AAGU-999','accepted')
    (tmp_path/'.workblock/graph.json').write_text('invalid irrelevant data')
    assert view.index_page(framework,rows,sources,page)==before
    assert json.dumps(rows,ensure_ascii=False)==serialized
    write_block(tmp_path,'AAGU-072','accepted')
    after=view.index_page(framework,rows,sources,page)
    assert after!=before
    assert json.dumps(rows,ensure_ascii=False)==serialized


def test_accepted_negative_result_does_not_unlock_cross_dataset_run(tmp_path):
    rows=records();lookup={r['id']:r for r in rows}
    parent=lookup['AAGU-001'];child=lookup['AAGU-002']
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
    rows=list(model.read_records(view.SOURCE / 'analyses').values());catalog=view.catalog(view.ROOT,rows)
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
    framework,rows=frame(),records(); sources=view.Sources(view.ROOT,tmp_path)
    assert view.index_page(framework,rows,sources,tmp_path/'index.html')==view.index_page(framework,rows,sources,tmp_path/'index.html')
    rows[0]['title']='</text><script>alert(1)</script>'
    content=view.index_page(framework,rows,sources,tmp_path/'index.html')
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


def write_split(root, rows):
    source = root / 'self/research'
    (source / 'experiments').mkdir(parents=True)
    (source / 'analyses').mkdir()
    (source / 'framework.json').write_text(json.dumps(frame()), encoding='utf-8')
    for row in rows:
        state = {k:v for k,v in row.items() if k not in ('analysis','decision','published_analysis')}
        for directory, data in [('experiments', state), ('analyses', row['published_analysis'])]:
            (source / directory / (row['id'] + '.json')).write_text(json.dumps(data), encoding='utf-8')


def test_split_load_preserves_information_and_uses_canonical_state(tmp_path):
    rows = records()
    write_split(tmp_path, rows)
    assert model.load(tmp_path)[1] == rows
    candidate = tmp_path / 'candidate'
    write_split(candidate, rows)
    for p in (candidate / 'self/research/experiments').glob('*.json'):
        p.unlink()
    assert model.load(candidate, tmp_path)[1] == rows
    with pytest.raises(ValueError, match='Missing local experiment state'):
        model.load(candidate)


def test_missing_analysis_is_pending_and_mixed_state_rejected(tmp_path):
    write_split(tmp_path, records())
    (tmp_path / 'self/research/analyses/AAGU-001.json').unlink()
    rows = model.load(tmp_path)[1]
    assert rows[0]['analysis']['state'] == 'not_started'
    assert not model.dependencies(rows[1], rows, tmp_path)[0]['resolved']
    p = tmp_path / 'self/research/experiments/AAGU-001.json'
    state = json.loads(p.read_text())
    state['analysis'] = records()[0]['analysis']
    p.write_text(json.dumps(state))
    with pytest.raises(ValueError, match='belongs in analyses'):
        model.load(tmp_path)


def test_old_analysis_does_not_release_expanded_scope(tmp_path):
    rows = records()
    rows[0]['scope'] = 'Expanded scope'
    assert not model.dependencies(rows[1], rows, tmp_path)[0]['resolved']


def test_published_analysis_cannot_contain_live_state(tmp_path):
    rows = records()
    rows[0]['published_analysis']['execution'] = rows[0]['execution']
    write_split(tmp_path, rows)
    with pytest.raises(ValueError, match='Live state belongs'):
        model.load(tmp_path)


def test_state_edits_leave_git_head_and_status_unchanged_analysis_is_tracked(tmp_path):
    write_split(tmp_path, records())
    source = tmp_path / 'self/research'
    (source / '.gitignore').write_bytes((view.SOURCE / '.gitignore').read_bytes())
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args], text=True).strip()
    git('init', '-q')
    git('add', 'self/research/.gitignore', 'self/research/framework.json', 'self/research/analyses')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'baseline')
    head = git('rev-parse', 'HEAD')
    p = source / 'experiments/AAGU-001.json'
    state = json.loads(p.read_text())
    state['next_step'] = 'Updated while running'
    p.write_text(json.dumps(state))
    assert git('status', '--porcelain') == ''
    assert git('rev-parse', 'HEAD') == head
    assert not git('ls-files', 'self/research/experiments')
    p = source / 'analyses/AAGU-001.json'
    p.write_text(p.read_text() + '\n')
    assert 'self/research/analyses/AAGU-001.json' in git('status', '--porcelain')
