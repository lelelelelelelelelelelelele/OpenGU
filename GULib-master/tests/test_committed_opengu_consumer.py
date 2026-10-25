"""Real installed Core/consumer, real Git objects, no SSH or formal data."""
import json
from pathlib import Path
import subprocess
import sys
import os
import shutil
import time
import uuid

import pytest
import yaml

from test_syncmate_execution_contract import workspace, tables, commit, git
from test_recipe_yaml import save_spec
from scripts.syncmate.opengu_recipes import generate
from syncmate_core import context, versions
from opengu_syncmate.adapter import OpenGUProjectExtension
from test_modular_consumers import write_yaml


@pytest.fixture(autouse=True)
def isolated_control_guard(local_only_transport):
    checked = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-c',
        "import socket,asyncio; assert socket.create_connection.__module__ == 'opengu_native_test_guard'"],
        capture_output=True, text=True, encoding='utf-8')
    assert checked.returncode == 0, checked.stderr
    yield
    assert not Path(os.environ['OPENGU_TEST_TRANSPORT_DENIALS']).exists()


def native(root, *args, verification_root=None, check=True, input_data=None):
    command = [sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
               '--project-root', str(root), '--verification-root', str(verification_root or root), *args]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
        input=json.dumps(input_data) if input_data is not None else None, timeout=240,
        **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {}))
    if check:
        assert result.returncode == 0, result.stdout + result.stderr
    return result


def test_installed_smoke_uses_generic_core_fixture(workspace):
    result = json.loads(native(workspace[0], 'smoke', '--json').stdout)
    assert result['passed'] and result['cleaned'], result


def test_committed_definition_excludes_workspace_yaml_and_python(workspace):
    root, path, _ = workspace
    spec = generate('experiment.yaml', recipe_id='committed', run_id='e103-first', project_root=root)
    save_spec(root, spec)
    sha = commit(root)
    with context.use(root, extension=OpenGUProjectExtension(), node_id='runner'):
        first = versions.bind('committed', sha)
        path.write_text('not valid current YAML', encoding='utf-8')
        (root / 'parameter_parser.py').write_text('raise RuntimeError("mutable Python imported")', encoding='utf-8')
        (root / 'experiments/modular_config.py').write_text('raise RuntimeError("mutable resolver imported")', encoding='utf-8')
        (root / 'model/properties/GCN.yaml').write_text('invalid mutable defaults', encoding='utf-8')
        (root / 'paper.md').write_text('Uncommitted paper', encoding='utf-8')
        again = versions.bind('committed', sha)
        assert first['definition'] == again['definition']
        assert first['recipe_sha256'] == again['recipe_sha256']
        assert again['warnings']
        assert 'model/properties/GCN.yaml' in again['definition']['committed_inputs']
        uncommitted = root / 'scripts/syncmate/recipes/uncommitted.yaml'
        uncommitted.write_text(yaml.safe_dump({**spec, 'id': 'uncommitted'}), encoding='utf-8')
        with pytest.raises(ValueError, match='committed regular source file is missing'):
            versions.bind('uncommitted', sha)


def test_missing_committed_reference_does_not_use_workspace_copy(workspace):
    root, path, _ = workspace
    spec = generate('experiment.yaml', recipe_id='missing', run_id='e103-missing', project_root=root)
    save_spec(root, spec)
    git(root, 'add', '.')
    git(root, 'rm', '--cached', 'score.yaml')
    git(root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Missing source reference')
    assert (root / 'score.yaml').is_file()
    with context.use(root, extension=OpenGUProjectExtension(), node_id='runner'):
        with pytest.raises(ValueError, match='YAML file does not exist'):
            versions.bind('missing')


def test_installed_preview_queue_execute_and_frozen_scientific_return(workspace, record_property):
    root, path, config = workspace
    config.update(selector_refs=['degree.yaml'])
    config.pop('seeds')
    config.pop('budget_ratios')
    write_yaml(path, config)
    spec = generate('experiment.yaml', recipe_id='real-chain', run_id='e103-chain', project_root=root)
    save_spec(root, spec)
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    device.update(role='runner+collector', peers={'runner': {
        'role': 'runner', 'transport': 'local', 'repo_path': str(root), 'python_executable': sys.executable}})
    write_yaml(device_file, device)
    sha = commit(root)
    view = json.loads(native(root, 'preview', 'real-chain', '--node', 'runner').stdout)
    assert view['commit'] == sha and view['local_checks_passed']
    dispatched = json.loads(native(root, 'runner-agent', 'dispatch', 'runner', '--recipe', 'real-chain',
        '--job-id', 'chain-job', '--json').stdout)
    assert dispatched['status'] == 'submitted'
    executed = json.loads(native(root, '--node-id', 'runner', 'runner-queue', 'run', '--once', '--json').stdout)
    assert executed['status'] == 'done', executed
    # Paper/config drift on the controller must not define old scientific validation.
    (root / 'paper.md').write_text('uncommitted manuscript', encoding='utf-8')
    path.write_text('invalid current config', encoding='utf-8')
    returned = json.loads(native(root, 'runner-agent', 'collect', 'runner', '--job-id', 'chain-job', '--json').stdout)
    assert returned['verify']['summary']['status'] == 'verified', returned
    checked = json.loads(native(root, 'scientific-check', 'runner', '--job-id', 'chain-job').stdout)
    assert checked['passed'], checked
    assert checked['scientific_acceptance'] == 'not_evaluated'
    record_property('actual_chain', json.dumps({'source_sha': sha, 'node': 'runner',
        'execution': executed['status'], 'return': returned['status'], 'scientific_validation': checked,
        'installed_entry': True, 'formal_gpu': False}))


@pytest.mark.parametrize('fault', ['dirty_source', 'dataset_bytes', 'runtime_exists', 'wrong_device'])
def test_real_startup_refuses_invalid_execution_conditions(workspace, fault):
    root, path, config = workspace
    config.update(selector_refs=['degree.yaml'])
    config.pop('seeds')
    config.pop('budget_ratios')
    write_yaml(path, config)
    save_spec(root, generate('experiment.yaml', recipe_id='blocked', run_id='blocked-run', project_root=root))
    device_file = root / '.syncmate/device.yaml'
    device = yaml.safe_load(device_file.read_text(encoding='utf-8'))
    device.update(role='runner+collector', peers={'runner': {'role': 'runner', 'transport': 'local',
        'repo_path': str(root), 'python_executable': sys.executable}})
    write_yaml(device_file, device)
    # Production datasets are untracked; integrity must be checked independently of Git dirt.
    with (root / '.gitignore').open('a', encoding='utf-8') as handle:
        handle.write('data/\n')
    commit(root)
    native(root, 'runner-agent', 'dispatch', 'runner', '--recipe', 'blocked', '--job-id', 'blocked-job', '--json')
    if fault == 'dirty_source':
        (root / 'experiments/run.py').write_text('raise AssertionError("must never run")', encoding='utf-8')
    elif fault == 'dataset_bytes':
        graph = root / 'data/processed/graph.pkl'
        graph.write_bytes(graph.read_bytes() + b'corrupt')
    elif fault == 'runtime_exists':
        (root / 'results/runtime/modular/blocked-run').mkdir(parents=True)
    else:
        device['execution_device'] = 'cuda:999'
        write_yaml(device_file, device)
    ran = native(root, '--node-id', 'runner', 'runner-queue', 'run', '--once', '--json', check=False)
    observed = json.loads(ran.stdout)
    assert ran.returncode != 0 and observed['status'] != 'done', observed
    assert not (root / 'results/runs/contract/blocked-run').exists()
    assert not (root / '.syncmate/runner_queues/runner/done/blocked-job.yaml').exists()


def test_s1_s2_shared_checkout_and_delayed_return(workspace, record_property):
    old_root, _, config = workspace
    # Actual Git subdirectory layout, with a single shared execution checkout.
    controller = old_root / 'GULib-master'
    controller.mkdir()
    for entry in list(old_root.iterdir()):
        if entry.name not in ('.git', 'GULib-master'):
            shutil.move(str(entry), str(controller / entry.name))
    config.update(selector_refs=['degree.yaml'])
    config.pop('seeds')
    config.pop('budget_ratios')
    path = controller / 'experiment.yaml'
    write_yaml(path, config)
    script = controller / 'experiments/run.py'
    code = script.read_text(encoding='utf-8')
    barrier = '''if __name__ == '__main__':
    if '--run-id' in sys.argv and sys.argv[sys.argv.index('--run-id') + 1] == 'e103-A':
        import time
        gate = ROOT / '.syncmate/test-barrier'
        gate.mkdir(parents=True, exist_ok=True)
        (gate / 'started').write_text('producer running', encoding='utf-8')
        while not (gate / 'release').exists():
            time.sleep(0.05)
'''
    script.write_bytes(code.replace("if __name__ == '__main__':", barrier).encode('utf-8'))
    a = generate('experiment.yaml', recipe_id='a', run_id='e103-A', project_root=controller)
    save_spec(controller, a)
    d = generate('experiment.yaml', recipe_id='d', run_id='e103-D', project_root=controller)
    save_spec(controller, d)
    s1 = commit(controller)
    runner_git = old_root.parent / ('execution-' + uuid.uuid4().hex)
    git(old_root, 'clone', '-q', str(old_root), str(runner_git))
    runner = runner_git / 'GULib-master'
    (runner / '.syncmate').mkdir()
    runner_device = yaml.safe_load((controller / '.syncmate/device.yaml').read_text(encoding='utf-8'))
    runner_device.update(repo_path=str(runner), role='runner', peers={})
    write_yaml(runner / '.syncmate/device.yaml', runner_device)
    peers = {node: {'role': 'runner', 'transport': 'local', 'repo_path': str(runner),
                   'python_executable': sys.executable} for node in ('alpha', 'beta')}
    device = {**runner_device, 'repo_path': str(controller), 'role': 'collector', 'peers': peers}
    write_yaml(controller / '.syncmate/device.yaml', device)
    launched_a = json.loads(native(controller, 'runner-agent', 'dispatch', 'alpha', '--recipe', 'a',
        '--job-id', 'job-A', '--json', verification_root=runner).stdout)
    command = [sys.executable, '-I', '-X', 'utf8', '-B', '-m', 'opengu_syncmate',
        '--project-root', str(runner), '--verification-root', str(runner), '--node-id', 'alpha',
        'runner-queue', 'run', '--once', '--json']
    producer = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding='utf-8', **({'creationflags': subprocess.CREATE_NO_WINDOW} if sys.platform == 'win32' else {}))
    gate = runner / '.syncmate/test-barrier'
    try:
        deadline = time.monotonic() + 90
        while not (gate / 'started').exists() and time.monotonic() < deadline:
            assert producer.poll() is None, producer.communicate()
            time.sleep(0.05)
        assert (gate / 'started').exists(), 'real producer did not reach its controlled barrier'
        native(controller, 'runner-agent', 'dispatch', 'beta', '--recipe', 'd', '--job-id', 'job-D',
               '--json', verification_root=runner)
        d_executed = json.loads(native(runner, '--node-id', 'beta', 'runner-queue', 'run', '--once', '--json').stdout)
        assert d_executed['status'] == 'done' and producer.poll() is None
        assert git(runner, 'rev-parse', 'HEAD') == s1
        degree_path = controller / 'degree.yaml'
        degree = yaml.safe_load(degree_path.read_text(encoding='utf-8'))
        degree['budget']['value'] = 2
        write_yaml(degree_path, degree)
        b = generate('experiment.yaml', recipe_id='b', run_id='e103-B', project_root=controller)
        save_spec(controller, b)
        write_yaml(controller / 'collision.yaml', {**config, 'experiment_id': 'other-experiment'})
        collision = generate('collision.yaml', recipe_id='collision', run_id='e103-D', project_root=controller)
        save_spec(controller, collision)
        s2 = commit(controller)
        (controller / 'paper.md').write_text('Uncommitted manuscript from another chat', encoding='utf-8')
        launched_b = json.loads(native(controller, '--source-ref', s2, 'runner-agent', 'dispatch', 'beta',
            '--recipe', 'b', '--job-id', 'job-B', '--json', verification_root=runner).stdout)
        assert launched_b['expected_git_sha'] == s2 and launched_b['warnings']
        assert launched_b['source_import']['checkout_unchanged'] is True
        assert git(runner, 'rev-parse', 'HEAD') == s1
        collided = native(controller, '--source-ref', s2, 'runner-agent', 'dispatch', 'beta',
            '--recipe', 'collision', '--job-id', 'collision-job', '--json', verification_root=runner, check=False)
        assert collided.returncode != 0 and 'identity already reserved' in collided.stdout
        assert not (runner / '.syncmate/runner_queues/beta/inbox/collision-job.yaml').exists()
        degree['budget']['value'] = 3
        write_yaml(degree_path, degree)
        git(controller, 'add', 'degree.yaml')
        git(controller, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'Main advances')
        s3 = git(controller, 'rev-parse', 'HEAD')
        waiting_result = native(runner, '--node-id', 'beta', 'runner-queue', 'run', '--once', '--json', check=False)
        waiting = json.loads(waiting_result.stdout)
        assert waiting['processed'] is False
        assert git(runner, 'rev-parse', 'HEAD') == s1
        from syncmate_core import maintenance
        with context.use(runner, extension=OpenGUProjectExtension(verification_root=str(runner)), node_id='beta'):
            with pytest.raises(maintenance.Busy):
                with maintenance.installation(node_ids=['alpha', 'beta']):
                    pytest.fail('maintenance entered while a producer was running')
            with pytest.raises(maintenance.Busy):
                with maintenance.installation(node_ids=['beta']):
                    pytest.fail('maintenance omitted the active node')
    finally:
        gate.mkdir(parents=True, exist_ok=True)
        (gate / 'release').write_text('release fixture barrier', encoding='utf-8')
        try:
            stdout, stderr = producer.communicate(timeout=240)
        except subprocess.TimeoutExpired:
            producer.kill()
            stdout, stderr = producer.communicate()
    assert producer.returncode == 0, stdout + stderr
    assert json.loads(stdout)['status'] == 'done'
    from syncmate_core import queue as core_queue, maintenance
    with context.use(runner, node_id='unknown'):
        core_queue.ensure_runner_queue_dirs()
        unknown_lock = maintenance.execution_lock()
        unknown_lock.mkdir()
        (unknown_lock / 'owner.json').write_text(json.dumps({'pid': -1, 'node_id': 'unknown'}), encoding='utf-8')
    try:
        unknown_wait = json.loads(native(runner, '--node-id', 'beta', 'runner-queue', 'run', '--once', '--json', check=False).stdout)
        assert unknown_wait['processed'] is False
        assert git(runner, 'rev-parse', 'HEAD') == s1
    finally:
        (unknown_lock / 'owner.json').unlink()
        unknown_lock.rmdir()
    ran_b = json.loads(native(runner, '--node-id', 'beta', 'runner-queue', 'run', '--once', '--json').stdout)
    assert ran_b['status'] == 'done'
    assert git(runner, 'rev-parse', 'HEAD') == s2
    assert git(controller, 'rev-parse', 'HEAD') == s3
    # The execution checkout is already S2 before A is collected.
    for node, job in [('beta', 'job-B'), ('alpha', 'job-A'), ('beta', 'job-D')]:
        returned = json.loads(native(controller, 'runner-agent', 'collect', node, '--job-id', job,
            '--json', verification_root=runner).stdout)
        assert returned['verify']['summary']['status'] == 'verified'
    (controller / 'experiments/modular_config.py').write_text('raise RuntimeError("current parser must not load")', encoding='utf-8')
    (controller / 'scripts/syncmate/opengu_acceptance.py').write_text('raise RuntimeError("current validator must not load")', encoding='utf-8')
    a_checked = json.loads(native(controller, 'scientific-check', 'alpha', '--job-id', 'job-A', verification_root=runner).stdout)
    b_checked = json.loads(native(controller, 'scientific-check', 'beta', '--job-id', 'job-B', verification_root=runner).stdout)
    assert a_checked['passed'] and a_checked['git_sha'] == s1
    assert b_checked['passed'] and b_checked['git_sha'] == s2
    wrong = native(controller, 'scientific-check', 'beta', '--job-id', 'job-A', verification_root=runner, check=False)
    assert wrong.returncode != 0 and 'peer differs' in wrong.stdout
    frozen_path = controller / '.syncmate/science/job-A.json'
    frozen_bytes = frozen_path.read_bytes()
    frozen = json.loads(frozen_bytes)
    frozen['scientific_verifier']['git_sha'] = s2
    frozen_path.write_text(json.dumps(frozen), encoding='utf-8')
    wrong_source = native(controller, 'scientific-check', 'alpha', '--job-id', 'job-A',
                          verification_root=runner, check=False)
    assert wrong_source.returncode != 0 and 'differs from saved Core contract' in wrong_source.stdout
    frozen_path.write_bytes(frozen_bytes)
    assert not (controller / 'results/cache_v2').exists()
    record_property('actual_s1_s2', json.dumps({'S1': s1, 'S2': s2, 'S3': s3,
        'running_S1_dirty_manuscript_S2_queued': True, 'shared_maintenance_refused': True,
        'same_SHA_two_node_execution': d_executed['status'], 'unknown_occupancy_refused': unknown_wait,
        'cross_experiment_runtime_RID_collision_refused': True,
        'foreign_node_waited': waiting, 'B_execution': ran_b['status'],
        'A_delayed_return': a_checked, 'B_return': b_checked,
        'wrong_node_and_frozen_source_refused': True, 'transport': 'real local installed CLI', 'formal_gpu': False}))
