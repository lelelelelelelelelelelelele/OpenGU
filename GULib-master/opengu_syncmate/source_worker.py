"""One isolated invocation against reviewed project modules in a Git commit.

No checkout, archive extraction, persistent source cache or workspace import.
Third-party dependencies come from the interpreter; project files come from the
same GitSource as the configuration and scientific validator.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.abc
import importlib.util
import io
import json
from pathlib import Path
import sys

from syncmate_core.versions import GitSource


class CommittedModules(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, source):
        self.source = source
        self.files = set(source.files())
        self.roots = {path.split('/')[0].split('.')[0] for path in self.files if path.endswith('.py')}
        self.roots.discard('opengu_syncmate')

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] not in self.roots:
            return None
        relative = fullname.replace('.', '/')
        for filename, package in ((relative + '/__init__.py', True), (relative + '.py', False)):
            if filename in self.files:
                spec = importlib.util.spec_from_loader(fullname, self, is_package=package)
                spec.origin = str(self.source.root / filename)
                spec.loader_state = filename
                return spec
        if any(name.startswith(relative + '/') for name in self.files):
            spec = importlib.util.spec_from_loader(fullname, self, is_package=True)
            spec.loader_state = None
            spec.origin = str(self.source.root / relative)
            return spec
        raise ModuleNotFoundError('project module missing from bound commit: ' + fullname)

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        filename = module.__spec__.loader_state
        module.__file__ = module.__spec__.origin
        if filename is not None:
            exec(compile(self.source.read_bytes(filename), module.__file__, 'exec'), module.__dict__)


def resolve(source, request):
    import yaml
    from scripts.syncmate.opengu_recipes import UniqueLoader, validate_declaration, assemble, RECIPE_DIRECTORY
    from scripts.syncmate.opengu_adapter import bind_execution_node
    from experiments.effective_config import committed_files
    from syncmate_core.contracts import JOB_ID_RE
    recipe = request['recipe']
    if not JOB_ID_RE.fullmatch(recipe):
        raise ValueError('invalid Recipe ID')
    path = (RECIPE_DIRECTORY / (recipe + '.yaml')).as_posix()
    spec = validate_declaration(yaml.load(source.read_text(path), Loader=UniqueLoader))
    if spec['id'] != recipe:
        raise ValueError('committed Recipe filename/id mismatch')
    with committed_files(source) as inputs:
        definition = assemble(spec, source.root)
        if spec['runner'] == 'experiment':
            from experiments.modular_run import execute
            plan = execute(source.root / spec['config_path'], dry_run=True)
            if (plan['configuration_fingerprint'] != spec['configuration_fingerprint']
                    or plan['logical_cells'] != spec['logical_cells']):
                raise ValueError('committed configuration differs from reviewed Recipe')
    definition['committed_inputs'] = {path: hashlib.sha256(raw).hexdigest() for path, raw in sorted(inputs.items())}
    definition = bind_execution_node(definition, request['node_id'])
    definition['scientific_verifier'] = {
        'protocol': 'opengu.scientific-return/v1',
        'git_sha': source.sha,
        'sha256': hashlib.sha256(source.read_bytes('scripts/syncmate/opengu_acceptance.py')).hexdigest()}
    verification = request.get('verification_root')
    if verification is not None:
        import tempfile
        execution_root = Path(verification).resolve()
        execution_root.relative_to(Path(tempfile.gettempdir()).resolve())
        definition['argv'] = (*definition['argv'], '--verification-root', str(execution_root))
        definition['verification_root'] = str(execution_root)
    return definition


def accept(source, request):
    from experiments.effective_config import committed_files
    from scripts.syncmate.opengu_acceptance import acceptance_payload
    definition = request['definition']
    expected = definition['scientific_verifier']
    if expected != {'protocol': 'opengu.scientific-return/v1', 'git_sha': source.sha,
                    'sha256': hashlib.sha256(source.read_bytes('scripts/syncmate/opengu_acceptance.py')).hexdigest()}:
        raise ValueError('frozen scientific verifier identity differs')
    with committed_files(source, root=request['context']['project_root']):
        return acceptance_payload(request['profile'], definition, request['context'])


def main():
    request = json.load(sys.stdin)
    source = GitSource(request['project_root'], request['git_sha'])
    finder = CommittedModules(source)
    sys.meta_path.insert(0, finder)
    captured = io.StringIO()
    try:
        with contextlib.redirect_stdout(captured):
            if request['action'] == 'resolve':
                result = resolve(source, request)
            elif request['action'] == 'accept':
                result = accept(source, request)
            elif request['action'] == 'results':
                from scripts.syncmate.opengu_results import results_payload
                result = results_payload(request['index'], request['options'])
            else:
                raise ValueError('unsupported committed worker action')
        response = {'ok': True, 'result': result}
    except (Exception, SystemExit) as exc:
        response = {'ok': False, 'error': type(exc).__name__ + ': ' + str(exc)}
    if captured.getvalue():
        print(captured.getvalue(), file=sys.stderr, end='')
    print(json.dumps(response, ensure_ascii=False, allow_nan=False))
    return 0 if response['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
