"""Independent experiment sheet semantics and research view integration."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import pytest
import yaml
from scripts.dashboard import gen_research_overview as gen


def test_framework_has_phases_families_and_all_core_questions():
    frame,sheets=gen.load()
    assert {p['id'] for p in frame['phases']}=={'phase-1','phase-2','im-track'}
    assert {t['id'] for t in frame['topics']}=={f'X{i}' for i in range(1,9)}
    assert sum(s['family']=='if' for s in sheets)==3
    assert sum(s['phase']=='im-track' for s in sheets)==1
    assert all(s['question'] and s['comparison'] and s['narrative'] and s['metrics'] and s['outputs'] for s in sheets)
    assert not any('WORKITEM.md' in c['path'] for s in sheets for c in s['configs'])


@pytest.mark.parametrize('defect',['missing_design','workitem_as_config','fake_complete','invalid_count','invalid_family','duplicate_id','analysis_without_source','cycle','pending_unbound','missing_run'])
def test_invalid_sheet_cannot_claim_valid_experiment(defect):
    frame,sheets=gen.load();s=sheets[0]
    if defect=='missing_design':s['narrative']=[]
    if defect=='workitem_as_config':s['configs'][0]['path']='.workblock/items/AAGU-031/WORKITEM.md'
    if defect=='fake_complete':s['execution']['runs']=[]
    if defect=='invalid_count':s['execution']['completed']=1000
    if defect=='invalid_family':s['family']='invented'
    if defect=='duplicate_id':sheets.append(copy.deepcopy(s))
    if defect=='analysis_without_source':s['analysis']['links']=[]
    if defect=='cycle':s['analysis']['inputs']=[sheets[1]['id']]
    if defect=='pending_unbound':s['configs']=[];s['preparation']['state']='draft';s['execution'].update(state='pending',completed=0)
    if defect=='missing_run':s['execution'].update(state='running',completed=0,runs=[])
    with pytest.raises(ValueError):gen.validate(frame,sheets)


def test_configured_axes_match_existing_yaml_without_running_experiments():
    _,sheets=gen.load()
    for s in sheets:
        if s['execution']['total'] is None:continue
        config=yaml.safe_load((gen.ROOT/s['configs'][0]['path']).read_text(encoding='utf-8'))
        count=len(config['dataset_refs'])*len(config['budget_ratios'])
        if 'im_selector_seeds' in config:
            # Existing IM table: three RR configs, CELF, Degree and Random.
            count*=4*len(config['im_selector_seeds'])+1+len(config['random_selector_seeds'])
        else:
            count*=len(config['selector_refs'])*len(config.get('random_selector_seeds',[0]))
        count*=len(config.get('seeds',[0]))*len(config.get('unlearning_refs',[0]))
        assert count==s['execution']['total'],s['id']


def test_diagram_and_pages_have_same_sheet_navigation(tmp_path):
    frame,sheets=gen.load();built=gen.outputs(frame,sheets,gen.Sources(gen.ROOT,gen.ROOT),tmp_path)
    assert len(built)==9
    svg=ET.fromstring(built[tmp_path/'diagram/research-framework.svg'])
    targets=[x.attrib['href'] for x in svg.iter() if x.tag.endswith('}a')]
    assert targets==['../experiments/'+s['id']+'.html' for s in sheets]
    for s in sheets:
        content=built[tmp_path/'experiments'/f'{s["id"]}.html']
        assert '<h2>实验设计</h2>' in content
        assert '<h2>配置与准备</h2>' in content
        assert '<h2>运行与结果</h2>' in content
        assert '<h2>结果分析</h2>' in content


def test_html_and_svg_escape_research_text(tmp_path):
    frame,sheets=gen.load();sheets[0]['title']='</text><script>alert(1)</script>'
    for content in gen.outputs(frame,sheets,gen.Sources(gen.ROOT,gen.ROOT),tmp_path).values():
        assert '</text><script>alert(1)' not in content
        if 'alert(1)' in content:assert '&lt;script&gt;alert(1)' in content


def test_record_and_legacy_changes_do_not_change_generated_content_or_git(tmp_path):
    folder=tmp_path/'self/research';(folder/'experiments').mkdir(parents=True)
    owned=[]
    for p in [gen.SOURCE/'framework.json',gen.SOURCE/'.gitignore',*(gen.SOURCE/'experiments').glob('*.json')]:
        dest=folder/p.relative_to(gen.SOURCE);dest.write_bytes(p.read_bytes());owned.append(str(dest.relative_to(tmp_path)))
    (tmp_path/'.gitignore').write_text('.workblock/\nself/dashboard/\n');owned.append('.gitignore')
    def git(*args):return subprocess.check_output(['git','-C',str(tmp_path),*args],text=True,stderr=subprocess.STDOUT).strip()
    git('init','-q');git('add',*owned);git('-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','-qm','research baseline')
    frame,sheets=gen.load(tmp_path)
    for sheet in sheets:
        for config in sheet['configs']:
            dest=tmp_path/config['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((gen.ROOT/config['path']).read_bytes())
            git('add',config['path'])
    git('-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','-qm','config fixtures')
    sources=gen.Sources(tmp_path,tmp_path)
    before=gen.outputs(frame,sheets,sources,folder)
    item=tmp_path/'.workblock/items/TEST/WORKITEM.md';item.parent.mkdir(parents=True)
    csv=tmp_path/'self/dashboard/config_inventory.csv';csv.parent.mkdir(parents=True)
    for state in ['registered','edited contract','working','awaiting acceptance']:
        item.write_text(state);csv.write_text('deliberately invalid legacy CSV: '+state)
        (tmp_path/'.workblock/graph.json').write_text(json.dumps({'fixture_state':state}))
        frame,sheets=gen.load(tmp_path);after=gen.outputs(frame,sheets,sources,folder)
        assert before==after
        for path,content in after.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
        assert git('status','--porcelain')==''


def test_config_sheet_exists_before_yaml_and_results(tmp_path):
    frame,sheets=gen.load();draft=next(s for s in sheets if s['id']=='if-trajectory')
    assert draft['preparation']['state']=='draft' and not draft['configs'] and not draft['execution']['runs']
    built=gen.outputs(frame,sheets,gen.Sources(gen.ROOT,gen.ROOT),tmp_path)
    assert '尚未形成独立执行表' in built[tmp_path/'experiments/if-trajectory.html']


def test_link_missing_is_reported_instead_of_silently_omitted(tmp_path):
    with pytest.raises(ValueError,match='Missing sources'):
        gen.check_sources({'link':{'label':'definition','path':'missing.md'}},[],gen.Sources(tmp_path,tmp_path))


def test_run_hash_and_count_are_verified(tmp_path):
    artifact=tmp_path/'results/run/cells/a/metrics.json';artifact.parent.mkdir(parents=True);artifact.write_text('{}')
    run={'experiment_id':'exp','run_id':'r1','commit':'a'*40,'config_path':'experiments/configs/test.yaml','cells':[{'cell_id':'a','path':'cells/a','status':'completed','files':{'metrics.json':{'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}}}]}
    path=tmp_path/'results/run/run.json';path.write_text(json.dumps(run))
    bound=dict(path='results/run/run.json',experiment_id='exp',run_id='r1',commit='a'*40,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    sheets=[{'configs':[{'path':run['config_path']}],'execution':{'runs':[bound],'completed':1}}];sources=gen.Sources(tmp_path,tmp_path)
    assert gen.verify_runs(sheets,sources)==2
    sheets[0]['execution']['runs'].append(dict(bound));sheets[0]['execution']['completed']=2
    with pytest.raises(ValueError,match='count mismatch'):gen.verify_runs(sheets,sources)
    sheets[0]['execution']['runs']=[bound];sheets[0]['execution']['completed']=1
    artifact.write_text('changed')
    with pytest.raises(ValueError,match='checksum mismatch'):gen.verify_runs(sheets,sources)
    path.write_text('{}')
    with pytest.raises(ValueError,match='manifest changed'):gen.verify_runs(sheets,sources)


def test_yaml_preview_reads_actual_file_and_rejects_invalid_yaml(tmp_path):
    path=tmp_path/'experiments/configs/test.yaml';path.parent.mkdir(parents=True)
    ref={'path':'experiments/configs/test.yaml','label':'config'}
    sources=gen.Sources(tmp_path,tmp_path);page=tmp_path/'index.html'
    path.write_text('budget_ratios: [0.1]\nlabel: "<script>"\n',encoding='utf-8')
    first=gen.config_preview(ref,sources,page)
    assert 'test.yaml' in first and '0.1' in first and '&lt;script&gt;' in first
    path.write_text('budget_ratios: [0.05]\n',encoding='utf-8')
    assert '0.05' in gen.config_preview(ref,sources,page)
    path.write_text('budget_ratios: [',encoding='utf-8')
    with pytest.raises(ValueError,match='Invalid YAML'):gen.config_preview(ref,sources,page)
    path.write_text('- not a mapping',encoding='utf-8')
    with pytest.raises(ValueError,match='must be a mapping'):gen.config_preview(ref,sources,page)


def test_every_sheet_has_reverse_question_links_and_yaml_is_not_hand_copied(tmp_path):
    frame,sheets=gen.load();built=gen.outputs(frame,sheets,gen.Sources(gen.ROOT,gen.ROOT),tmp_path)
    for sheet in sheets:
        page=built[tmp_path/'experiments'/f'{sheet["id"]}.html']
        assert all('../index.html#question-'+topic in page for topic in sheet['topics'])
        assert '固定条件</h3>' not in page and '变化的因素</h3>' not in page
        assert page.count('class="yaml-content"')==len(sheet['configs'])
