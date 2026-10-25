"""Real HTTP -> installed OpenGU dispatch -> Core CPU fixture -> verified return."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid
from urllib.parse import urlencode
from urllib.request import Request,urlopen

import pytest
import yaml

from local_transport_guard import local_only_transport
from test_syncmate_execution_contract import workspace,tables,commit
from test_recipe_yaml import save_spec
from test_modular_consumers import write_yaml
from scripts.syncmate.opengu_recipes import generate
from syncmate_core.versions import GitSource
from test_committed_opengu_consumer import native


@pytest.fixture(autouse=True)
def local_only(local_only_transport,monkeypatch):
    monkeypatch.setenv('OPENGU_TEST_LOOPBACK','1')
    yield


def test_console_uses_private_frozen_dispatch_and_recovers_same_cpu_job(workspace,record_property):
    root,path,config=workspace
    config.update(selector_refs=['degree.yaml']);config.pop('seeds');config.pop('budget_ratios')
    write_yaml(path,config)
    save_spec(root,generate('experiment.yaml',recipe_id='desktop-cpu',run_id='desktop-cpu',project_root=root))
    device_file=root/'.syncmate/device.yaml'
    device=yaml.safe_load(device_file.read_text(encoding='utf-8'))
    device.update(role='runner+collector',peers={'runner':{'role':'runner','transport':'local',
        'repo_path':str(root),'python_executable':sys.executable}})
    write_yaml(device_file,device)
    sha=commit(root)

    def start():
        process=subprocess.Popen([sys.executable,'-I','-X','utf8','-B','-m','opengu_syncmate',
            '--project-root',str(root),'--verification-root',str(root),'--source-ref',sha,
            'console','--port','0','--desktop'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf-8')
        line=process.stdout.readline().strip()
        assert line.startswith('SyncMate console: '),line
        return process,line[len('SyncMate console: '):]

    process,url=start()
    token=json.load(urlopen(url+'/api/projects'))['token']
    def call(endpoint,values=None,post=False):
        values={'project':root.name,**(values or {})}
        req=Request(url+endpoint+('' if post else '?'+urlencode(values)),
            data=json.dumps(values).encode() if post else None,
            headers={'Content-Type':'application/json','X-SyncMate-Token':token})
        return json.load(urlopen(req,timeout=120))
    try:
        original=path.read_bytes()
        path.write_text('invalid uncommitted configuration',encoding='utf-8')
        preview=call('/api/recipe',{'recipe':'desktop-cpu','node_id':'runner'})
        assert preview['git_sha']==sha and preview['content']==GitSource(root,sha).read_text('experiment.yaml')
        assert preview['warnings']
        path.write_bytes(original)
        checked=call('/api/readiness',{'recipe':'desktop-cpu','node_id':'runner'},True)
        assert checked['ready'],checked
        operation={'recipe':'desktop-cpu','node_id':'runner','request_id':str(uuid.uuid4())}
        job=call('/api/submit',operation,True)['job_id']
        assert call('/api/submit',operation,True)['job_id']==job
        deadline=time.monotonic()+60
        queue_path=root/'.syncmate/runner_queues/runner/inbox'/(job+'.yaml')
        while not queue_path.exists() and time.monotonic()<deadline:
            receipt=json.loads((root/'.syncmate/controller'/(job+'.json')).read_text(encoding='utf-8'))
            assert not receipt.get('error'),receipt
            time.sleep(.2)
        assert queue_path.exists()
        # Only the private consumer creates these frozen scientific/source facts.
        assert (root/'.syncmate/science'/(job+'.json')).is_file()
        assert (root/'.syncmate/source-imports'/(job+'.json')).is_file()
        stopped=native(root,'console','--stop')
        assert stopped.returncode==0
        assert process.wait(timeout=20)==0
        ran=json.loads(native(root,'--node-id','runner','runner-queue','run','--once','--json').stdout)
        assert ran['status']=='done',ran
        handoff=root/'.syncmate/runs'/(job+'.json')
        handoff_hash=hashlib.sha256(handoff.read_bytes()).hexdigest()
        process,url=start()
        token=json.load(urlopen(url+'/api/projects'))['token']
        deadline=time.monotonic()+45
        while time.monotonic()<deadline:
            detail=call('/api/job-status',{'job_id':job})
            if detail.get('collection',{}).get('status')=='accepted':break
            if detail.get('collection',{}).get('verify',{}).get('summary',{}).get('status')=='verified':break
            time.sleep(.3)
        assert detail.get('collection',{}).get('verify',{}).get('summary',{}).get('status')=='verified',detail
        assert hashlib.sha256(handoff.read_bytes()).hexdigest()==handoff_hash
        done=list((root/'.syncmate/runner_queues/runner/done').glob('*.yaml'))
        assert [p.stem for p in done]==[job]
        raw=call('/api/job-records',{'job_id':job})
        assert raw['read_only'] and raw['records']['runs']['sha256']==handoff_hash
        record_property('actual_console_chain',json.dumps({'job_id':job,'source_sha':sha,
            'private_dispatch':True,'submissions':1,'completed_jobs':1,'return':'verified',
            'restart_same_job':True,'handoff_unchanged':True,'formal_gpu':False}))
    finally:
        if process.poll() is None:
            process.stdin.close()
            process.wait(timeout=30)
