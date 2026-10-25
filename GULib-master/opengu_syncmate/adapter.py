"""Installed adapter: Core owns jobs; committed project code owns science."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

from syncmate_core import context
from syncmate_core.project import GenericProjectExtension
from syncmate_core.versions import GitSource


def implementation():
    files = {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
             for path in sorted(Path(__file__).parent.glob('*.py'))}
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def worker(source, action, **values):
    request = {'action': action, 'project_root': str(source.root), 'git_sha': source.sha, **values}
    result = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate.source_worker'],
        input=json.dumps(request), capture_output=True, text=True, encoding='utf-8', timeout=180)
    try:
        response = json.loads(result.stdout)
    except ValueError as exc:
        raise ValueError('committed project worker did not return JSON: ' + result.stderr[-2000:]) from exc
    if result.returncode or not response.get('ok'):
        raise ValueError(response.get('error') or 'committed project worker failed')
    return response['result']


class OpenGUProjectExtension(GenericProjectExtension):
    extension_id = 'opengu'

    def __init__(self, *, verification_root=None):
        self.verification_root = verification_root

    def result_roots(self):
        return ('results/runs',)

    def recipe_ids(self, project_root):
        source = GitSource(project_root)
        return tuple(Path(path).stem for path in source.files('scripts/syncmate/recipes') if path.endswith('.yaml'))

    def resolve_recipe(self, project_root, recipe_id):
        return self.resolve_committed_recipe(GitSource(project_root, 'HEAD'), recipe_id)

    def resolve_committed_recipe(self, source, recipe_id):
        definition = worker(source, 'resolve', recipe=recipe_id,
            node_id=context.runner_node_id(), verification_root=self.verification_root)
        definition['installed_adapter'] = implementation()
        return definition

    def artifact_names(self, device, peer):
        policy = (peer or {}).get('artifact_policy') or (device or {}).get('artifact_policy') or {}
        return tuple(policy.get('include') or ('attack.json', 'collateral.json', '_meta.json'))

    def accept(self, profile, definition, details):
        source = GitSource(context.current().root, details['expected_git_sha'])
        details = {**details, 'project_root': str(details['project_root'])}
        return worker(source, 'accept', definition=definition, context=details)

    def results(self, index, options):
        options = {**options, 'project_root': str(options['project_root'])}
        return worker(GitSource(context.current().root, 'HEAD'), 'results', index=index, options=options)
