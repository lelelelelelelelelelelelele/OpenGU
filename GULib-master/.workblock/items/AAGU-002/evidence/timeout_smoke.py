"""Three real local queue jobs: normal, forced timeout, and normal after failure.

Only a disposable Git checkout is used. No SSH, scientific dataset, cache or
registered experiment recipe is changed. The real installed Core starts and
times out real child processes; subprocess.run is never mocked.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import psutil
from syncmate_core import context, queue
from syncmate_core.project import StaticProjectExtension

WORKLOAD = '''import json, os, pathlib, sys, time
name = sys.argv[1]
root = pathlib.Path('results/runs') / name
root.mkdir(parents=True, exist_ok=True)
(root / 'started.json').write_text(json.dumps({'pid': os.getpid()}))
print('STARTED ' + name, file=sys.stderr, flush=True)
if name == 'timeout':
    time.sleep(4)
(root / 'metrics.json').write_text(json.dumps({'passed': True, 'case': name}))
print(json.dumps({'passed': True}))
'''


class Fixture(StaticProjectExtension):
    def preflight(self, profile, definition, config_path):
        return {'ready': True, 'errors': [], 'profile': profile,
                'observed': {'fixture_config_exists': config_path.is_file()}}


def main():
    with tempfile.TemporaryDirectory(prefix='aagu002-timeout-') as directory:
        root = Path(directory)
        payload = b'{"purpose":"bounded local timeout verification"}\n'
        (root/'fixture.json').write_bytes(payload)
        (root/'workload.py').write_text(WORKLOAD, encoding='utf-8')
        (root/'.gitignore').write_text('/.syncmate/\n/results/\n')
        def git(*args):
            return subprocess.check_output(['git', *args], cwd=str(root), stderr=subprocess.STDOUT, text=True).strip()
        git('init', '-b', 'main')
        git('add', 'fixture.json', 'workload.py', '.gitignore')
        git('-c', 'user.name=AAGU002 fixture', '-c', 'user.email=fixture@invalid', 'commit', '-m', 'bounded timeout fixture')
        sha = git('rev-parse', 'HEAD')
        definitions = {}
        for name in ('control', 'timeout', 'after-timeout'):
            definitions[name] = {
                'id': name, 'argv': ['{python}', '-B', 'workload.py', name],
                'config_path': 'fixture.json', 'config_sha256': hashlib.sha256(payload).hexdigest(),
                'timeout_seconds': 1 if name == 'timeout' else 5,
                'expected_artifact_paths': ['results/runs/'+name+'/metrics.json'],
                'git_binding_policy': 'job-exact-main-v1', 'preflight_profile': 'local-fixture',
                'collector_acceptance': 'not-eligible',
            }
        extension = Fixture('aagu002-timeout-fixture', definitions, ('metrics.json',))
        cases = []
        with context.use(root, extension=extension):
            for name, definition in definitions.items():
                job_id = 'aagu002-' + name
                submitted = queue.runner_queue_submit(job_id, name, expected_git_sha=sha)
                assert submitted['output_contract']['timeout_seconds'] == definition['timeout_seconds']
                started = time.perf_counter()
                observed = queue.runner_queue_run_once({'device_id': 'local-fixture', 'role': 'runner'})
                elapsed = time.perf_counter()-started
                pid = json.loads((root/'results/runs'/name/'started.json').read_text())['pid']
                process_exited = not psutil.pid_exists(pid)
                artifact = root/'results/runs'/name/'metrics.json'
                saved = json.loads(queue.runner_queue_receipt_path(job_id).read_text())
                expected_state = 'failed' if name == 'timeout' else 'done'
                checks = {
                    'expected_terminal_state': observed['status'] == expected_state and saved['state'] == expected_state,
                    'child_exited': process_exited,
                    'artifact_presence_correct': artifact.is_file() == (name != 'timeout'),
                    'running_queue_empty': not list(queue.runner_queue_state_dir('running').glob('*.yaml')),
                }
                if name == 'timeout':
                    checks['explicit_timeout_reason'] = 'timed out after 1s' in observed['result']['reason']
                    checks['bounded_elapsed'] = 0.8 <= elapsed < 3.5
                    checks['not_successfully_exited'] = observed['result']['exit_code'] is None
                assert all(checks.values()), (name, checks, observed)
                cases.append({'case': name, 'timeout_seconds': definition['timeout_seconds'],
                    'elapsed_seconds': elapsed, 'pid': pid, 'checks': checks,
                    'receipt': saved, 'queue_result': observed})
            idle = queue.runner_queue_run_once({'device_id': 'local-fixture', 'role': 'runner'})
            assert idle['status'] == 'idle' and idle['processed'] is False
        report = {'passed': True, 'evidence_kind': 'real-process-disposable-local-queue',
            'fixture_git_sha': sha, 'cases': cases, 'after_all_jobs': idle,
            'remote_jobs': 0, 'scientific_experiments': 0,
            'limit': 'Direct child termination checked; arbitrary descendant process trees not exercised.'}
    report['temporary_checkout_removed'] = not root.exists()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
