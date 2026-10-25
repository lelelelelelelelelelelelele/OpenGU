"""CPU integration-test transport boundary, inherited by Python child processes."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

import pytest


class ExternalTransportForbidden(RuntimeError):
    pass


def install_guard(setattr_fn=setattr):
    if getattr(subprocess.Popen, '_opengu_local_only', False):
        return
    launch = subprocess.Popen
    def denied(kind, argv):
        path=os.environ.get('OPENGU_TEST_TRANSPORT_DENIALS')
        if path:
            with open(path,'a',encoding='utf-8') as handle:
                handle.write(json.dumps({'kind':kind,'argv':argv},default=str)+'\n')
        raise ExternalTransportForbidden('CPU test forbids external transport before launch: '+kind)
    def local_popen(args,*positional,**kwargs):
        # Python's Windows platform reader uses this fixed local kernel query.
        if kwargs.get('shell') and isinstance(args,str) and args.lower() in ('ver','cmd /c ver','command /c ver'):
            return launch(args,*positional,**kwargs)
        if kwargs.get('shell') or isinstance(args,(str,bytes)):
            denied('shell/string command',args)
        argv=[str(x) for x in args]
        program=Path(argv[0]).name.lower()
        if program not in ('git','git.exe','python','python.exe','python3','python3.exe'):
            denied(program,argv)
        if program.startswith('python') and any(x in ('-S','-I','-E') for x in argv[1:]):
            denied('Python environment bypass',argv)
        if program.startswith('git'):
            if any(x in ('push','pull','ls-remote') for x in argv[1:]) or any('://' in x or x.startswith(('git@','\\\\','//')) for x in argv[1:]):
                denied('Git network transport',argv)
            # Even a child Git process may use only its explicit local files.
            argv=argv[:1]+['-c','protocol.allow=never','-c','protocol.file.allow=always']+argv[1:]
        return launch(argv,*positional,**kwargs)
    local_popen._opengu_local_only=True
    setattr_fn(subprocess,'Popen',local_popen)
    def no_network(*args,**kwargs):
        denied('network socket',repr(args)[:250])
    setattr_fn(socket,'create_connection',no_network)
    setattr_fn(socket,'getaddrinfo',no_network)
    setattr_fn(socket.socket,'connect',no_network)
    setattr_fn(socket.socket,'connect_ex',no_network)
    setattr_fn(os,'system',lambda command:denied('os.system',command))


@pytest.fixture(autouse=True)
def local_only_transport(monkeypatch,tmp_path):
    """Default for deployment/UI tests; -p enables it for the whole selected run."""
    folder=tmp_path/'local-transport-guard'
    folder.mkdir()
    (folder/'sitecustomize.py').write_text('from local_transport_guard import install_guard\ninstall_guard()\n',encoding='utf-8')
    monkeypatch.setenv('PYTHONPATH',str(folder)+os.pathsep+str(Path(__file__).parent)+os.pathsep+os.environ.get('PYTHONPATH',''))
    monkeypatch.setenv('OPENGU_TEST_TRANSPORT_DENIALS',str(tmp_path/'transport-denied.jsonl'))
    install_guard(monkeypatch.setattr)


if os.environ.get('OPENGU_CPU_TESTS_ONLY') == '1':
    install_guard()
