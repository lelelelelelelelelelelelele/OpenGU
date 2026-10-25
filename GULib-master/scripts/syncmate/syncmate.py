#!/usr/bin/env python
"""Launch the installed OpenGU control, outside the execution checkout."""
from pathlib import Path
import json
import re
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    active = PROJECT_ROOT / '.syncmate/deployments/active.json'
    if active.exists():
        if active.is_symlink():
            raise ValueError('linked deployment pointer')
        sha = json.loads(active.read_text(encoding='utf-8'))['source_sha']
        if not re.fullmatch('[0-9a-f]{40}', sha):
            raise ValueError('invalid active deployment source')
        prefix = subprocess.check_output(['git', '-C', str(PROJECT_ROOT), 'rev-parse', '--show-prefix'], text=True).strip()
        code = subprocess.check_output(['git', '-C', str(PROJECT_ROOT), 'show', sha + ':' + prefix + 'opengu_syncmate/provision.py'], text=True, encoding='utf-8')
        node = argv[argv.index('--node-id') + 1] if '--node-id' in argv else None
        manifest_path = active.parent / sha / 'manifest.json'
        if manifest_path.is_symlink():
            raise ValueError('linked deployment manifest')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        base = manifest['nodes'][node]['base_python'] if node else manifest['controller']['base_python']
        request = {'action': 'ensure', 'root': str(PROJECT_ROOT), 'node': node, 'source_sha': sha}
        prepared = subprocess.run([base, '-I', '-X', 'utf8', '-B', '-c', code],
            input=json.dumps(request), text=True, encoding='utf-8', capture_output=True,
            **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {}))
        if prepared.returncode:
            print(prepared.stdout, end='')
            print(prepared.stderr, end='', file=sys.stderr)
            return prepared.returncode
        ready = json.loads(prepared.stdout)
        if ready.get('status') != 'ready' or ready.get('source_sha') != sha or ready.get('node') != node:
            raise ValueError('installed runtime was not verified for this deployment')
        return subprocess.run([ready['runtime_python'], '-I', '-X', 'utf8', '-B', '-m',
            'opengu_syncmate', '--project-root', str(PROJECT_ROOT), *argv],
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
            **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {})).returncode
    return subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
                           '--project-root', str(PROJECT_ROOT), *argv],
                          stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
                          **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {})).returncode


if __name__ == '__main__':
    raise SystemExit(main())
