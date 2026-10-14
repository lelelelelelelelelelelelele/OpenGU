"""Real Core cursor publication behind OpenGU's optional declaration callback."""
from dataclasses import replace
import json
from pathlib import Path
import os
import subprocess
import sys

import pytest

from experiments.modular_config import load_experiment
from experiments.modular_execution import project_context
from experiments.modular_progress import progress_steps
from scripts.syncmate.opengu_progress import make_notify, progress_plan
from syncmate_core import progress
from syncmate_core.identity import sha256_recipe_config
from test_modular_consumers import tables, write_yaml


@pytest.fixture
def publishing(tables, monkeypatch):
    root, config, _ = tables
    path = root / 'experiment.yaml'
    write_yaml(path, config)
    loaded = load_experiment(path)
    context = replace(project_context(loaded['experiment_id'], run_id='progress',
        request_device='cpu', level='verification', repository_root=root),
        source_git_sha='a' * 40)
    job = {'id': 'progress-job', 'recipe': 'progress-recipe',
        'expected_git_sha': context.source_git_sha,
        'expected_config_sha256': sha256_recipe_config(path)}
    env = progress.prepare_environment(root, job, progress_plan(loaded))
    monkeypatch.setenv(progress.ENV, env[progress.ENV])
    return root, path, loaded, context, job


def test_actual_declarations_publish_real_core_ordered_snapshots(publishing):
    root, path, config, context, job = publishing
    notify = make_notify(config, context, config_path=path)
    snapshot_path = progress.safe_path(root, job['id'], 'current.json')
    for step in progress_steps(config):
        for amount in (0, step['total']):
            assert notify('progress', position=step['position'], current=amount, total=step['total'])
            snapshot = progress.read_json(snapshot_path)
            assert snapshot['kind'] == 'update'
            assert snapshot['position'] == step['position']
            assert snapshot['current'] == amount
    assert notify('completed', position={})
    snapshot = progress.read_json(snapshot_path)
    assert snapshot['kind'] == 'completed'
    assert snapshot['position'] == {'stage': 'export'}
    assert all(row['state'] == 'completed'
               for row in progress.tree_report(progress_plan(config), snapshot))


def test_disabled_progress_never_reads_inherited_invalid_context(publishing, monkeypatch):
    _, path, config, context, _ = publishing
    monkeypatch.setenv(progress.ENV, 'invalid inherited context')
    assert make_notify(config, context, config_path=path, enabled=False) is None
    monkeypatch.delenv(progress.ENV)
    assert make_notify(config, context, config_path=path) is None


@pytest.mark.parametrize('change', ['json', 'plan', 'git', 'config', 'path'])
def test_explicit_context_setup_fails_closed(publishing, monkeypatch, change):
    root, path, config, context, job = publishing
    context_path = progress.safe_path(root, job['id'], 'context.json')
    if change == 'json':
        context_path.write_text('{broken', encoding='utf-8')
    elif change == 'path':
        elsewhere = root / 'elsewhere.json'
        elsewhere.write_bytes(context_path.read_bytes())
        monkeypatch.setenv(progress.ENV, str(elsewhere))
    else:
        saved = progress.read_json(context_path)
        if change == 'plan':
            saved['plan'][0]['match']['dataset_index'] = 99
        else:
            saved['binding']['git_sha' if change == 'git' else 'config_sha256'] = ('f' * (40 if change == 'git' else 64))
        context_path.write_text(json.dumps(saved), encoding='utf-8')
    with pytest.raises(ValueError, match='SyncMate progress setup'):
        make_notify(config, context, config_path=path)
    assert not progress.safe_path(root, job['id'], 'current.json').exists()


def test_runtime_write_failure_is_observational_and_diagnostic(publishing, monkeypatch, capsys):
    _, path, config, context, _ = publishing
    notify = make_notify(config, context, config_path=path)
    def unavailable(*args):
        raise PermissionError('temporary snapshot is read-only')
    monkeypatch.setattr(progress, 'write_json_atomic', unavailable)
    step = progress_steps(config)[0]
    assert notify('progress', position=step['position'], current=0, total=step['total']) is False
    assert 'temporary snapshot is read-only' in capsys.readouterr().err


def test_real_exp079_plan_stays_within_core_capacity(tmp_path, monkeypatch):
    from scripts.syncmate.opengu_recipes import ROOT, resolve_recipe
    definition = resolve_recipe(ROOT, 'opengu-exp079-surrogate-multiseed')
    config = load_experiment(ROOT / definition['config_path'])
    plan = progress_plan(config)
    assert plan == definition['progress_plan']
    assert len(plan) == 124
    from scripts.syncmate.opengu_progress import _transport_steps
    requests = [s for s in _transport_steps(config)[0] if s['position']['stage'] == 'output_evaluation']
    assert len(requests) == 360
    assert all(s['total'] == 7 for s in requests)
    assert sum(s['total'] for s in requests) == 2520
    batch_nodes = [n for n in plan if 'children' in n]
    assert len(batch_nodes) == 120
    from collections import Counter
    assert Counter(len(n['children']) for n in batch_nodes) == {9: 30, 1: 90}
    assert len(list(progress.leaves(plan))) == 724
    for batch in batch_nodes:
        for request in batch['children']:
            assert [n['label'] for n in request['children']] == ['Selection', 'Output + Evaluation']
            assert len({n['match']['step'] for n in request['children']}) == 2
    assert len(progress_steps(config)) == 5764
    assert sum(s['total'] for s in progress_steps(config)
               if s['position']['stage'] == 'unlearning') == 2520
    assert progress.validate_plan(plan) == plan
    # Validate the actual serialized context, not only the smaller plan object.
    from types import SimpleNamespace
    path = ROOT / definition['config_path']
    job = {'id': 'full-tree', 'recipe': 'full-tree', 'expected_git_sha': 'a' * 40,
           'expected_config_sha256': sha256_recipe_config(path)}
    env = progress.prepare_environment(tmp_path, job, plan)
    monkeypatch.setenv(progress.ENV, env[progress.ENV])
    notify = make_notify(config, SimpleNamespace(store_root=tmp_path/'cache/store',
        source_git_sha='a' * 40), config_path=path)
    for step in progress_steps(config)[:10]:
        assert notify('progress', position=step['position'], current=step['total'], total=step['total'])
    assert progress.read_json(progress.safe_path(tmp_path, job['id'], 'current.json'))['current'] == 3


def test_installed_core_serves_a_standalone_consumer_without_opengu(tmp_path):
    """An actual child publishes through Core with no project code on its path."""
    (tmp_path / 'config.yaml').write_text('consumer: independent\n', encoding='utf-8')
    (tmp_path / 'producer.py').write_text(
        'from syncmate_core.progress import from_env\n'
        'p = from_env()\n'
        'assert p.update(phase="work", current=1, total=2), p.error\n'
        'assert p.completed(phase="work"), p.error\n'
        'print(\'{"passed": true}\')\n', encoding='utf-8')
    script = '''
import importlib.abc, json, sys
from pathlib import Path
class NoOpenGU(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'experiments', 'scripts', 'attack', 'cache_v2', 'model', 'task', 'unlearning'}:
            raise AssertionError('Core attempted OpenGU import: ' + fullname)
sys.meta_path.insert(0, NoOpenGU())
from syncmate_core import progress
from syncmate_core.contracts import Recipe, sha256_text
from syncmate_core.runner import run_job
root = Path.cwd()
plan = [{'id': 'work', 'label': 'Independent work', 'match': {'phase': 'work'}}]
recipe = Recipe('independent', ('{python}', 'producer.py'), 'config.yaml',
    sha256_text((root / 'config.yaml').read_text(encoding='utf-8')), 20, progress_plan=plan)
class Consumer:
    def resolve_recipe(self, recipe_id):
        assert recipe_id == recipe.id
        return recipe
    def preflight(self, *args):
        return {'ready': True}
job = {'id': 'independent-job', 'recipe': recipe.id,
    'protocol': 'syncmate-job/v1', 'version': 1, 'created_at': progress.now(),
    'expected_git_sha': 'a' * 40, 'expected_config_sha256': recipe.config_sha256}
result = run_job(job, Consumer(), root, observed_git_sha='a' * 40)
assert result['status'] == 'done', result
snapshot = progress.read_json(progress.safe_path(root, job['id'], 'current.json'))
assert snapshot['kind'] == 'completed'
assert not any(name.split('.')[0] in {'experiments', 'attack', 'cache_v2'} for name in sys.modules)
print(json.dumps({'status': result['status'], 'snapshot': snapshot, 'opengu_imported': False}))
'''
    env = dict(os.environ)
    env.pop('PYTHONPATH', None)
    result = subprocess.run([sys.executable, '-B', '-c', script], cwd=tmp_path,
        env=env, capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert result.returncode == 0, result.stdout + result.stderr
    observed = json.loads(result.stdout)
    assert observed['status'] == 'done' and observed['opengu_imported'] is False


@pytest.mark.parametrize('with_evaluations', [True, False])
def test_request_counter_counts_finished_output_evaluation_groups(publishing, monkeypatch, with_evaluations):
    from experiments.modular_config import selector_entries
    from experiments.modular_progress import execution_batches, request_entries
    root, path, _, context, job = publishing
    import yaml
    raw = yaml.safe_load(path.read_text(encoding='utf-8'))
    raw.update(stage='unlearning', selector_refs=['degree.yaml', 'r_point.yaml'],
               unlearning_refs=['gu.yaml'], seeds=[7, 19],
               evaluation_refs=['utility.yaml'] if with_evaluations else [])
    write_yaml(path, raw)
    config = load_experiment(path)
    job['expected_config_sha256'] = sha256_recipe_config(path)
    env = progress.prepare_environment(root, job, progress_plan(config))
    monkeypatch.setenv(progress.ENV, env[progress.ENV])
    notify = make_notify(config, context, config_path=path)
    snapshot_path = progress.safe_path(root, job['id'], 'current.json')
    totals = {(index, ref): len(request_entries(batch, ref))
              for index, batch in enumerate(execution_batches(config)) for _, ref in selector_entries(batch)}
    finished = dict.fromkeys(totals, 0)
    for step in progress_steps(config):
        for amount in range(step['total'] + 1):
            assert notify('progress', position=step['position'], current=amount, total=step['total'])
            snapshot = progress.read_json(snapshot_path)
            if 'batch_index' not in step['position']:
                continue
            if step['position']['stage'] == 'selector':
                leaf = next(n for n in progress.leaves(progress_plan(config)) if n['match'] == snapshot['position'])
                assert leaf['label'] == 'Selection'
                assert snapshot['current'] == amount and snapshot['total'] == 1
                continue
            index = (step['position']['batch_index'], step['position']['selector_ref'])
            terminal = 'evaluation' if with_evaluations else 'unlearning'
            if step['position']['stage'] == terminal and amount == step['total']:
                finished[index] += 1
            assert snapshot['current'] == finished[index]
            assert snapshot['total'] == totals[index]
            leaf = next(n for n in progress.leaves(progress_plan(config)) if n['match'] == snapshot['position'])
            assert leaf['label'] == 'Output + Evaluation'

    assert finished == totals
    assert notify('completed', position={})


@pytest.mark.parametrize('fail_evaluation', [False, True])
def test_real_execution_counts_only_after_evaluation(publishing, monkeypatch, fail_evaluation):
    import yaml
    import experiments.modular_run as runner
    root, path, _, context, job = publishing
    raw = yaml.safe_load(path.read_text(encoding='utf-8'))
    raw.update(stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'],
               evaluation_refs=['utility.yaml'])
    write_yaml(path, raw)
    config = load_experiment(path)
    job['expected_config_sha256'] = sha256_recipe_config(path)
    env = progress.prepare_environment(root, job, progress_plan(config))
    monkeypatch.setenv(progress.ENV, env[progress.ENV])
    notify = make_notify(config, context, config_path=path)
    snapshots = []
    def observe(kind, **kwargs):
        assert notify(kind, **kwargs)
        snapshot = progress.read_json(progress.safe_path(root, job['id'], 'current.json'))
        snapshots.append((kind, kwargs, snapshot))
    if fail_evaluation:
        def fail(*args, **kwargs):
            raise RuntimeError('evaluation failed')
        monkeypatch.setattr(runner, 'evaluate_modular', fail)
        with pytest.raises(RuntimeError, match='evaluation failed'):
            runner.execute(path, context=context, notify=observe)
        assert snapshots[-1][2]['current'] == 0
        assert snapshots[-1][2]['total'] == 1
        assert progress.tree_report(progress_plan(config), snapshots[-1][2])[1]['state'] == 'in_progress'
    else:
        runner.execute(path, context=context, notify=observe)
        assert any(k == 'progress' and v['position']['stage'] == 'evaluation'
                   and v['current'] == 1 and s['current'] == 1 for k, v, s in snapshots)
    output_done = [s for k, v, s in snapshots if k == 'progress'
                   and v['position']['stage'] == 'unlearning' and v['current'] == 1]
    assert output_done and all(s['current'] == 0 for s in output_done)
