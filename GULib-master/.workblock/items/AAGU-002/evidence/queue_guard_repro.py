"""Exercise installed Core in disposable local repositories, without SSH.

The fixture preflight is the controlled input; queue submission, disk writes,
job binding and runner refusal use the real installed Core implementation.
This records failures of the gate, and never treats reproduction success as
product acceptance. No process runner is permitted to launch a command.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from syncmate_core import context, queue, recipes
from syncmate_core.project import StaticProjectExtension


class Fixture(StaticProjectExtension):
    def __init__(self, definition, response):
        super().__init__('aagu002-fixture', {'readiness-fixture': definition}, ('metrics.json',))
        self.response = response
        self.calls = 0

    def preflight(self, profile, definition, config_path):
        self.calls += 1
        return copy.deepcopy(self.response)


def run_case(response, execute_refusal=False):
    with tempfile.TemporaryDirectory(prefix='aagu002-readiness-') as directory:
        root = Path(directory)
        config_bytes = b'{"fixture": "readiness-only"}\n'
        (root / 'fixture.json').write_bytes(config_bytes)
        (root / '.gitignore').write_text('/.syncmate/\n/results/\n')
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=str(root), stderr=subprocess.STDOUT).decode().strip()
        git('init', '-b', 'main')
        git('add', 'fixture.json', '.gitignore')
        git('-c', 'user.name=AAGU002 fixture', '-c', 'user.email=fixture@invalid', 'commit', '-m', 'fixture')
        sha = git('rev-parse', 'HEAD')
        definition = {
            'id': 'readiness-fixture', 'argv': ['{python}', '-c', 'raise SystemExit(99)'],
            'config_path': 'fixture.json', 'config_sha256': hashlib.sha256(config_bytes).hexdigest(),
            'timeout_seconds': 5, 'expected_artifact_paths': [],
            'git_binding_policy': 'job-exact-main-v1',
            'preflight_profile': 'controlled-readiness', 'collector_acceptance': 'not-eligible',
        }
        extension = Fixture(definition, response)
        process_calls = []
        def forbidden_process(*args, **kwargs):
            process_calls.append(True)
            raise AssertionError('No fixture process is permitted to launch')
        with context.use(root, extension=extension):
            observed = {'preflight_input': response, 'git_head': sha}
            try:
                result = queue.runner_queue_submit('aagu002-fixture', 'readiness-fixture', expected_git_sha=sha)
                observed['submitted'] = result['submitted']
            except SystemExit as exc:
                observed.update(submitted=False, refusal=str(exc))
            observed['preflight_calls_before_enqueue'] = extension.calls
            observed['inbox_created'] = queue.runner_queue_job_path('inbox', 'aagu002-fixture').is_file()
            observed['binding'] = {key: value for key, value in recipes.runner_recipe_binding('readiness-fixture').items()
                                   if key in ('ready', 'errors', 'runtime_preflight')}
            if execute_refusal and observed['submitted']:
                observed['run_once'] = queue.runner_queue_run_once(
                    {'device_id': 'fixture', 'role': 'runner'}, process_runner=forbidden_process)
            observed['process_calls'] = len(process_calls)
            observed['gate_check'] = 'PASS' if not observed['submitted'] else 'FAIL'
            return observed


if __name__ == '__main__':
    cases = {
        'explicit_refusal': run_case({'ready': False, 'errors': ['EXPECTED_GPU_MISSING']}, True),
        'missing_readiness': run_case({}),
    }
    print(json.dumps({'evidence_kind': 'local-isolated-installed-core-reproduction',
                      'python': sys.version.split()[0], 'cases': cases,
                      'remote_submissions': 0}, ensure_ascii=False, indent=2))
