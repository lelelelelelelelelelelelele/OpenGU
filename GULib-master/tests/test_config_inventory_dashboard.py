"""Research inventory evidence boundaries and record-edit isolation."""
from __future__ import annotations
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import pytest
from scripts.dashboard import gen_config_inventory as gen


def sources():
    data = json.loads(gen.DATA_PATH.read_text(encoding='utf-8'))
    with gen.CSV_PATH.open(encoding='utf-8-sig', newline='') as fh:
        return data, list(csv.DictReader(fh))


def first(data):
    return data['groups'][0]['configs'][0]


def test_historical_counts_and_current_evidence_are_separate():
    data, rows = sources()
    gen.validate(data, rows)
    history = {r['name']: r for r in rows}
    assert history['A3_cora_GCN_alpha0.00']['done'] == '10'
    assert history['phase_b_cora_gcn']['valid'] == '100'
    assert history['phase_b_cora_gcn']['accepted_remote'] == '20'
    assert history['phase_b_cora_gcn']['rerun'] == '60'
    assert history['phase_b_arxiv_tracin_smoke']['valid'] == '0'
    # Absent validity stays unknown; no done -> valid fallback.
    assert history['A3_cora_GAT_alpha0.25']['valid'] == ''
    assert [c['completed'] for g in data['groups'] for c in g['configs'] if c['run_state']=='completed'] == [72,360]


@pytest.mark.parametrize('mutation', ['missing_run','bad_count','duplicate_config','unknown_analysis_input','duplicate_category','pending_without_config'])
def test_rejects_unsupported_or_ambiguous_progress(mutation):
    data, rows = sources()
    c=first(data)
    if mutation=='missing_run': c['runs']=[]
    if mutation=='bad_count': c['completed']=c['expected']+1
    if mutation=='duplicate_config': data['groups'][1]['configs'].append(c)
    if mutation=='unknown_analysis_input': data['groups'][0]['analyses'][0]['inputs']=['absent']
    if mutation=='duplicate_category': data['groups'][0]['legacy_categories']=['sanity']
    if mutation=='pending_without_config': c.update(run_state='pending',completed=0,configs=[])
    with pytest.raises(ValueError): gen.validate(data,rows)


def test_cross_config_analysis_does_not_require_one_report_per_config():
    data, rows=sources()
    analysis=data['groups'][1]['analyses'][0]
    assert analysis['inputs']==['selector-stage-s','retrain-v2']
    gen.validate(data,rows)


def test_missing_link_is_an_error_not_a_fake_live_source(tmp_path):
    with pytest.raises(ValueError,match='Missing linked sources'):
        gen.check_links({'link':{'label':'missing','path':'missing.md'}},tmp_path)


def fixture_run(tmp_path):
    artifact=tmp_path/'run/cells/a/metrics.json';artifact.parent.mkdir(parents=True)
    artifact.write_text('{"f1":0.8}',encoding='utf-8')
    manifest={'experiment_id':'exp','run_id':'run-1','commit':'a'*40,'config_path':'config.yaml','cells':[{'cell_id':'a','path':'cells/a','status':'completed','files':{'metrics.json':{'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}}}]}
    run=tmp_path/'run/run.json';run.write_text(json.dumps(manifest))
    entry={'path':'run/run.json','experiment_id':'exp','run_id':'run-1','commit':'a'*40,'sha256':hashlib.sha256(run.read_bytes()).hexdigest()}
    data={'groups':[{'configs':[{'configs':[{'path':'config.yaml'}],'runs':[entry],'completed':1}]}]}
    return data,run,artifact


def test_evidence_requires_matching_identity_and_hashes(tmp_path):
    data,run,artifact=fixture_run(tmp_path)
    assert gen.verify_evidence(data,tmp_path)==2
    artifact.write_text('altered')
    with pytest.raises(ValueError,match='checksum mismatch'):gen.verify_evidence(data,tmp_path)


def test_changed_manifest_and_duplicate_attempts_cannot_inflate_completion(tmp_path):
    data,run,artifact=fixture_run(tmp_path)
    config=data['groups'][0]['configs'][0]
    config['runs'].append(dict(config['runs'][0]))
    config['completed']=2
    with pytest.raises(ValueError,match='Completion count'):gen.verify_evidence(data,tmp_path)
    run.write_text('{}')
    with pytest.raises(ValueError,match='manifest changed'):gen.verify_evidence(data,tmp_path)


def test_payload_escapes_script_termination():
    data=gen.load_data()
    data['groups'][0]['title']='</script><script>window.INJECTED=true</script>'
    html=gen.render(data)
    assert '</script><script>window.INJECTED' not in html
    assert '\\u003c/script>' in html


def test_record_changes_and_refresh_leave_code_git_clean(tmp_path):
    root=tmp_path
    dashboard=root/'self/dashboard';dashboard.mkdir(parents=True)
    (dashboard/'experiment_inventory.json').write_bytes(gen.DATA_PATH.read_bytes())
    (dashboard/'config_inventory.csv').write_bytes(gen.CSV_PATH.read_bytes())
    output=dashboard/'config_inventory.html'
    output.write_text(gen.render(gen.load_data(root),root),encoding='utf-8')
    (root/'.gitignore').write_text('.workblock/\n',encoding='utf-8')
    def git(*args):return subprocess.check_output(['git','-C',str(root),*args],text=True,stderr=subprocess.STDOUT).strip()
    git('init','-q')
    git('add','.gitignore','self/dashboard/experiment_inventory.json','self/dashboard/config_inventory.csv','self/dashboard/config_inventory.html')
    git('-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','-qm','fixture baseline')
    assert git('status','--porcelain')==''
    before=output.read_bytes()
    item=root/'.workblock/items/AAGU-TEST/WORKITEM.md';item.parent.mkdir(parents=True)
    for state in ['registered / not claimed','registered / not claimed\n合同编辑','working / claimed','awaiting acceptance']:
        item.write_text(state,encoding='utf-8')
        (root/'.workblock/graph.json').write_text(json.dumps({'assignments':{'AAGU-TEST':'research'},'state':state}))
        output.write_text(gen.render(gen.load_data(root),root),encoding='utf-8')
        assert output.read_bytes()==before
        assert git('status','--porcelain')==''


def test_current_output_is_deterministic():
    data=gen.load_data()
    assert gen.render(data)==gen.render(data)==gen.OUT_PATH.read_text(encoding='utf-8')
