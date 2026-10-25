"""Bounded startup callback; no scientific imports in the long-lived service."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


def execution_readiness(*, source, definition, contract, node_id):
    entry = source.root / 'scripts/syncmate/startup.py'
    if entry.read_text(encoding='utf-8') != source.read_text('scripts/syncmate/startup.py').replace('\r\n', '\n'):
        return {'ready': False, 'errors': ['bound startup implementation differs from checkout']}
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(entry)], cwd=source.root,
        input=json.dumps({'definition': definition, 'contract': contract, 'node_id': node_id}),
        text=True, encoding='utf-8', capture_output=True, timeout=180)
    try:
        response = json.loads(result.stdout)
    except ValueError:
        return {'ready': False, 'errors': ['bound startup returned invalid JSON', result.stderr[-1500:]]}
    return response
