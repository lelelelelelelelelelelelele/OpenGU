"""Fresh collector argv regression; optional bound returned-light-file validation.

Set OPENGU_RET_LIGHT_FIXTURE to a read-only fixture description for exact returned
files. Faults affect only pytest's private copies, never the source delivery.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
ARGV = [
    ['--project-root', 'collector', 'console', '--port', '0'],
    ['--project-root', 'collector', 'runner-agent', 'collect', 'gpu4090',
     '--job-id', 'exp086-20261024-e86og1-admit2', '--json'],
]


def child(code, argv, **extra):
    env = {**os.environ, 'PYTHONPATH': str(ROOT), 'PYTHONDONTWRITEBYTECODE': '1',
           'CUDA_VISIBLE_DEVICES': '-1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', **extra}
    result = subprocess.run([sys.executable, '-B', '-c', code, *argv], cwd=ROOT,
                            env=env, text=True, capture_output=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize('argv', ARGV)
def test_metric_contract_keeps_real_collector_arguments(argv):
    result = child('''
import json, sys
original = tuple(sys.argv)
from experiments.ret_reference_reading import METRICS
assert METRICS == {'final_accuracy', 'final_cross_entropy', 'repetitions'}
assert 'experiments.ret_reference_training' not in sys.modules
assert 'config' not in sys.modules
assert tuple(sys.argv) == original
print(json.dumps({'argv_unchanged': True, 'metrics': sorted(METRICS)}))
''', argv)
    assert result['argv_unchanged']


@pytest.fixture
def returned(tmp_path):
    value = os.environ.get('OPENGU_RET_LIGHT_FIXTURE')
    if not value:
        pytest.skip('Set OPENGU_RET_LIGHT_FIXTURE for an exact returned-file fixture')
    fixture = json.loads(Path(value).read_text(encoding='utf-8'))
    source = Path(fixture['source_root'])
    context = copy.deepcopy(fixture['context'])
    context['project_root'] = str(tmp_path)
    for entry in context['artifact_index']['peers']['gpu4090']['items']:
        path = source / entry['local_path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']
        target = tmp_path / entry['local_path']
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    for relative, expected in fixture['configs'].items():
        path = source / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    return fixture, context, tmp_path


ACCEPT = '''
import json, os, sys, torch
from pathlib import Path
original = tuple(sys.argv)
def blocked(*args, **kwargs): raise AssertionError('light reader performed model work')
hook = torch.nn.modules.module.register_module_forward_pre_hook(blocked)
torch.optim.Adam.step = blocked
def profile(frame, event, arg):
    if event == 'call' and frame.f_code.co_name in ('parameter_parser', 'train_reference', 'train_supervised', 'train_trajectory', 'create_model'):
        raise AssertionError('light reader called ' + frame.f_code.co_name)
sys.setprofile(profile)
request = json.loads(Path(os.environ['RET_REQUEST']).read_text(encoding='utf-8'))
from scripts.syncmate.opengu_acceptance import acceptance_payload
result = acceptance_payload('modular-output-v1', request['definition'], request['context'])
assert tuple(sys.argv) == original
assert 'experiments.ret_reference_training' not in sys.modules and 'config' not in sys.modules
sys.setprofile(None)
hook.remove()
print(json.dumps(result))
'''


@pytest.mark.parametrize('argv', ARGV)
def test_exact_returned_source_bound_acceptance_in_fresh_process(returned, argv):
    fixture, context, root = returned
    path = root / 'request.json'
    path.write_text(json.dumps(dict(definition=fixture['definition'], context=context)), encoding='utf-8')
    result = child(ACCEPT, argv, RET_REQUEST=str(path))
    assert result['passed'] and result['accepted_cells'] == 3
    assert result['scientific_acceptance'] == 'not_evaluated'


@pytest.mark.parametrize('fault', ['missing', 'bytes', 'execution', 'run_fields', 'metrics', 'trace_identity', 'trace_length'])
def test_returned_source_bound_faults_remain_rejected(returned, fault):
    fixture, context, root = returned
    entries = context['artifact_index']['peers']['gpu4090']['items']
    run_entry = next(e for e in entries if e['local_path'].endswith('/run.json'))
    run_path = root / run_entry['local_path']
    run = json.loads(run_path.read_text(encoding='utf-8'))
    cell = run['cells'][0]
    name = 'metrics.json' if fault in ('missing', 'bytes', 'metrics') else 'observers/ret_reference_trace/result.json' if fault == 'trace_identity' else 'observers/ret_reference_trace/trace.jsonl'
    path = run_path.parent / cell['path'] / name
    if fault == 'missing':
        path.unlink()
    elif fault == 'bytes':
        path.write_bytes(b'corrupt')
    elif fault == 'execution':
        context['expected_git_sha'] = 'f' * 40
    elif fault == 'run_fields':
        run['unexpected'] = True
    else:
        if fault == 'trace_length':
            path.write_bytes(b'\n'.join(path.read_bytes().splitlines()[:-1]) + b'\n')
        else:
            changed = json.loads(path.read_text(encoding='utf-8'))
            if fault == 'metrics': changed['rows'][0]['values']['unexpected_metric'] = 0
            else: changed['identity']['cell_id'] = 'wrong'
            path.write_text(json.dumps(changed), encoding='utf-8')
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        cell['files'][name]['sha256'] = checksum
        if name.startswith('observers/'):
            cell['observers'][0]['files'][name]['sha256'] = checksum
        next(e for e in entries if (root / e['local_path']).resolve() == path.resolve())['sha256'] = checksum
    if fault in ('run_fields', 'metrics', 'trace_identity', 'trace_length'):
        run_path.write_text(json.dumps(run), encoding='utf-8')
        run_entry['sha256'] = hashlib.sha256(run_path.read_bytes()).hexdigest()
    request = root / 'request.json'
    request.write_text(json.dumps(dict(definition=fixture['definition'], context=context)), encoding='utf-8')
    result = child(ACCEPT, ARGV[1], RET_REQUEST=str(request))
    assert not result['passed'] and result['status'] == 'rejected' and result['errors']


def test_preserved_source_free_run_reads_without_training(returned):
    fixture, _, _ = returned
    result = child('''
import hashlib, json, os, sys
from pathlib import Path
original = tuple(sys.argv)
path = Path(os.environ['RET_FREE_RUN'])
checksum = os.environ['RET_FREE_SHA']
assert hashlib.sha256(path.read_bytes()).hexdigest() == checksum
from experiments.modular_artifacts import read_run
run, docs = read_run(path, checksum)
assert run['stage'] == 'unlearning' and len(docs) == 4
assert all('source' not in c and 'output' in c for c in run['cells'])
assert tuple(sys.argv) == original
assert 'experiments.ret_reference_training' not in sys.modules and 'config' not in sys.modules
print(json.dumps({'cells': len(docs), 'files': 1 + sum(len(c['files']) for c in run['cells'])}))
''', ARGV[1], RET_FREE_RUN=fixture['source_free_run'], RET_FREE_SHA=fixture['source_free_sha256'])
    assert result == {'cells': 4, 'files': 17}
