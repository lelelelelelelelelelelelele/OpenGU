"""CPU integration-test transport boundary, inherited by Python child processes."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile



class ExternalTransportForbidden(RuntimeError):
    pass


def install_guard(setattr_fn=setattr):
    if os.environ.get('OPENGU_TEST_READ_ONLY_SCIENCE') == '1':
        def read_only_profile(frame, event, arg):
            module = frame.f_globals.get('__name__', '')
            name = frame.f_code.co_name
            if event == 'call' and ((module.startswith('torch.optim.') and name == 'step')
                    or (module == 'torch.nn.modules.module' and name in ('_call_impl', '_wrapped_call_impl'))):
                raise RuntimeError('read-only scientific check called a producer: ' + module + '.' + name)
        sys.setprofile(read_only_profile)
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
            return args
        if kwargs.get('shell') or isinstance(args,(str,bytes)):
            denied('shell/string command',args)
        argv=[str(x) for x in args]
        program=Path(argv[0]).name.lower()
        if program not in ('git','git.exe','python','python.exe','python3','python3.exe'):
            denied(program,argv)
        isolated_guard = (os.environ.get('OPENGU_TEST_INSTALLED_GUARD') == '1'
                          and (Path(sys.prefix) / 'Lib/site-packages/opengu_test_guard.pth').is_file())
        if program.startswith('python') and (any(x in ('-S','-E') for x in argv[1:])
                or ('-I' in argv[1:] and not isolated_guard)):
            denied('Python environment bypass',argv)
        if program.startswith('git'):
            if any(x in ('push','pull','ls-remote') for x in argv[1:]) or any('://' in x or x.startswith(('git@','\\\\','//')) for x in argv[1:]):
                denied('Git network transport',argv)
            # Even a child Git process may use only its explicit local files.
            argv=argv[:1]+['-c','protocol.allow=never','-c','protocol.file.allow=always']+argv[1:]
        return argv
    class LocalPopen(launch):
        _opengu_local_only = True

        def __init__(self, args, *positional, **kwargs):
            self._created_venv = (Path(args[-1]) if isinstance(args, (list, tuple))
                and '-m' in args and 'venv' in args and '--without-pip' in args else None)
            super().__init__(local_popen(args, *positional, **kwargs), *positional, **kwargs)

        def wait(self, *args, **kwargs):
            result = super().wait(*args, **kwargs)
            if result == 0 and self._created_venv is not None:
                # Install the same transport guard in real disposable child venvs.
                prefix = self._created_venv.resolve()
                prefix.relative_to(Path(tempfile.gettempdir()).resolve())
                guard = Path(sys.prefix) / 'Lib/site-packages/opengu_test_guard.pth'
                destination = prefix / 'Lib/site-packages/opengu_test_guard.pth'
                destination.write_bytes(guard.read_bytes())
                self._created_venv = None
            return result
    setattr_fn(subprocess,'Popen',LocalPopen)
    def no_network(*args,**kwargs):
        denied('network socket',repr(args)[:250])
    create_connection,getaddrinfo=socket.create_connection,socket.getaddrinfo
    connect,connect_ex=socket.socket.connect,socket.socket.connect_ex
    def loopback(address):
        return (os.environ.get('OPENGU_TEST_LOOPBACK')=='1' and isinstance(address,tuple)
                and len(address)>=2 and address[0]=='127.0.0.1'
                and isinstance(address[1],int) and 0<address[1]<65536)
    def local_connection(address,*args,**kwargs):
        if not loopback(address):return no_network(address)
        return create_connection(address,*args,**kwargs)
    def local_address(host,port,*args,**kwargs):
        if not loopback((host,port)):return no_network(host,port)
        return getaddrinfo(host,port,*args,**kwargs)
    def local_connect(sock,address):
        if not loopback(address):return no_network(address)
        return connect(sock,address)
    def local_connect_ex(sock,address):
        if not loopback(address):return no_network(address)
        return connect_ex(sock,address)
    setattr_fn(socket,'create_connection',local_connection)
    setattr_fn(socket,'getaddrinfo',local_address)
    setattr_fn(socket.socket,'connect',local_connect)
    setattr_fn(socket.socket,'connect_ex',local_connect_ex)
    setattr_fn(os,'system',lambda command:denied('os.system',command))


