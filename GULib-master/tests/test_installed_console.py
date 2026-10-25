"""Installed console integration: frozen submissions, no mutable science import."""
from argparse import Namespace
import importlib.util
import io
import json
from pathlib import Path
import sys

from syncmate_core import context
from opengu_syncmate import console


def test_console_cli_routes_to_installed_project_console(tmp_path, monkeypatch):
    from opengu_syncmate import control
    monkeypatch.setattr(control, 'installed', lambda: None)
    seen = []
    monkeypatch.setattr(console, 'serve', lambda *a, **kw: seen.append((a, kw)) or 0)
    assert control.main(['--project-root',str(tmp_path),'--source-ref','HEAD','console','--port','0']) == 0
    assert seen[0][1]['source_ref'] == 'HEAD'
    assert seen[0][0][1].port == 0


def test_dispatch_uses_saved_commit_and_selected_node(tmp_path, monkeypatch):
    from opengu_syncmate import control
    seen=[]
    def dispatch(args, **kwargs):
        seen.append((args,kwargs,context.runner_node_id()))
        return {'status':'submitted'}
    monkeypatch.setattr(control,'dispatch',dispatch)
    with context.use(tmp_path,extension=console.ConsoleExtension(source_ref='HEAD')) as project:
        owner=console.OpenGUConsole(project,source_ref='HEAD')
        saved={'job_id':'original','recipe':'chosen','node_id':'node-b','binding':{'git_sha':'a'*40}}
        result=owner.dispatch_job(saved,{},[])
    assert result['status']=='submitted'
    assert seen[0][1]['source_ref']=='a'*40
    assert seen[0][2]=='node-b'
    assert seen[0][0].job_id=='original' and not seen[0][0].wait


def test_readiness_never_bypasses_private_consumer_failure(tmp_path, monkeypatch):
    from opengu_syncmate import control
    monkeypatch.setattr(console.versions,'GitSource',lambda *a:Namespace(sha='a'*40))
    def refused(*a,**kw):
        raise ValueError('installed payload differs')
    monkeypatch.setattr(control,'preview',refused)
    def forbidden(*a,**kw):
        raise AssertionError('generic readiness must not bypass private verification')
    monkeypatch.setattr(console,'readiness',forbidden)
    with context.use(tmp_path,extension=console.ConsoleExtension(source_ref='HEAD')) as project:
        result=console.OpenGUConsole(project,source_ref='HEAD').readiness('node-b','chosen')
    assert not result['ready'] and result['errors']==['installed payload differs']


def test_deployed_launcher_preserves_owner_stdin(tmp_path, monkeypatch):
    source=Path(__file__).resolve().parents[1]/'scripts/syncmate/syncmate.py'
    spec=importlib.util.spec_from_file_location('_installed_console_launcher',source)
    entry=importlib.util.module_from_spec(spec);spec.loader.exec_module(entry)
    monkeypatch.setattr(entry,'PROJECT_ROOT',tmp_path)
    folder=tmp_path/'.syncmate/deployments';folder.mkdir(parents=True)
    sha='a'*40
    (folder/'active.json').write_text(json.dumps({'source_sha':sha}),encoding='utf-8')
    (folder/sha).mkdir()
    (folder/sha/'manifest.json').write_text(json.dumps({'controller':{'base_python':sys.executable}}),encoding='utf-8')
    monkeypatch.setattr(entry.subprocess,'check_output',lambda command,**kw:'' if '--show-prefix' in command else '# reviewed provision source')
    calls=[]
    def run(command,**kwargs):
        calls.append((command,kwargs))
        if len(calls)==1:
            request=json.loads(kwargs['input'])
            assert request['action']=='ensure' and 'stdin' not in request
            return Namespace(returncode=0,stdout=json.dumps({'status':'ready','source_sha':sha,'node':None,'runtime_python':sys.executable}),stderr='')
        return Namespace(returncode=0)
    monkeypatch.setattr(entry.subprocess,'run',run)
    owner=io.StringIO('owner input remains a live stream')
    monkeypatch.setattr(entry.sys,'stdin',owner)
    assert entry.main(['console','--desktop'])==0
    assert calls[1][1]['stdin'] is owner
    assert owner.tell()==0
