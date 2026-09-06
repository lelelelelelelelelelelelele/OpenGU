"""AAGU-034 frozen behavior: declarations in YAML, reuse and identity in results."""
import copy
import hashlib
import json

import pytest
import yaml
from test_modular_consumers import tables, write_yaml
from test_unified_execution import matrix, command
from test_syncmate_execution_contract import workspace, commit, cli, declaration, FixtureRegistration
from test_syncmate_gu_outputs import collect
from experiments.modular_config import load_experiment, experiment_batches
from experiments.modular_run import execute
from scripts.syncmate import syncmate
from opengu_adapter import OpenGUProjectExtension
from syncmate_core import context, devices, queue


@pytest.mark.parametrize('stage', ['selector', 'unlearning'])
@pytest.mark.parametrize('legacy', [None, {}, {'artifact_id': 'old'},
    {'experiment_ref': 'source.yaml', 'summary': None, 'sha256': None}])
def test_removed_selection_input_is_rejected_even_when_empty(tables, stage, legacy):
    root, config, _ = tables
    config.update(stage=stage, selector_refs=['degree.yaml'], selection_input=legacy)
    if stage == 'unlearning':
        config['unlearning_refs'] = ['gu.yaml']
    path = root / 'rejected.yaml'
    write_yaml(path, config)
    with pytest.raises(ValueError, match='selection_input'):
        execute(path, dry_run=True)
    assert not (root / 'v2').exists()


@pytest.mark.parametrize('dataset', ['cora', 'citeseer', 'pubmed'])
@pytest.mark.parametrize('stage, count', [('u', 204), ('retrain', 102)])
def test_registered_followup_declares_same_selectors_and_axes(dataset, stage, count):
    from experiments.aagu015.definitions import CONFIG
    source = load_experiment(CONFIG / ('stage_s_' + dataset + '.yaml'))
    path = CONFIG / ('stage_' + stage + '_' + dataset + '.yaml')
    target = load_experiment(path)
    assert 'selection_input' not in target
    assert target['selector_refs'] == source['selector_refs']
    assert target['seeds'] == [42, 212, 2024]
    assert target['budget_ratios'] == [.01, .05]
    for before, after in zip(experiment_batches(source), experiment_batches(target)):
        assert before['selectors'] == after['selectors']
        assert before['matrix_values'] == after['matrix_values']
        assert {gu['training']['seed'] for gu in after['unlearnings']} == {after['matrix_values']['training_seed']}
    assert execute(path, dry_run=True)['logical_cells'] == count


def test_selector_then_unlearning_reuses_without_summary_binding(matrix, record_property):
    root, path = matrix
    config = yaml.safe_load(path.read_text())
    source = copy.deepcopy(config)
    source.update(stage='selector', unlearning_refs=[], evaluation_refs=[])
    write_yaml(root / 'source.yaml', source)
    selected = command(root, root / 'source.yaml', 'selected')
    before = path.read_bytes()
    first = command(root, path, 'gu-cold')
    warm = command(root, path, 'gu-warm', poison=True)
    expected = [r['selection']['artifact'] for r in selected['selectors']]
    assert [r['selection']['artifact'] for r in first['selectors']] == expected
    assert all(r['score']['hit'] and r['selection']['cache']['hit'] for r in first['selectors'])
    assert first['selector_producer_called'] is False
    assert all(r['producer_called'] for r in first['unlearning'])
    assert all(r['hit'] and not r['producer_called'] for r in warm['unlearning'])
    assert [r['output'] for r in first['unlearning']] == [r['output'] for r in warm['unlearning']]
    assert path.read_bytes() == before
    assert json.loads((root / 'gu-warm.trace.json').read_text()) == {'training_seeds': [], 'score_calls': []}
    record_property('automatic_reuse', json.dumps({'selectors': expected,
        'cells': len(first['unlearning']), 'warm_outputs': [r['output'] for r in warm['unlearning']]}))


def test_cold_unlearning_and_core_warm_collect_share_declared_rows(workspace, record_property):
    runner, path, config = workspace
    degree = yaml.safe_load((runner / 'degree.yaml').read_text())
    degree['budget'] = {'mode': 'ratio', 'value': .1}
    write_yaml(runner / 'degree.yaml', degree)
    config.update(stage='unlearning', selector_refs=['degree.yaml', 'score.yaml'],
                  unlearning_refs=['gu.yaml', 'retrain.yaml'])
    write_yaml(path, config)
    sha = commit(runner)
    # No earlier selector stage and no user-supplied output/Selection references.
    cold = cli(runner, path, 'cold')
    assert cold.returncode == 0, cold.stdout + cold.stderr
    first = json.loads(cold.stdout)
    assert first['selector_producer_called'] is True and len(first['unlearning']) == 16
    definition = declaration(runner, path, 'unlearning')
    summary = definition['expected_artifact_paths'][0]
    definition['expected_artifact_paths'] = [summary] + [
        summary[:-5] + '.outputs/{}/{}'.format(i, name)
        for i in range(16) for name in ('attack.json', 'output-references.json', 'predictions.npz', '_meta.json')]
    with context.use(runner, extension=FixtureRegistration(definition)):
        assert queue.runner_queue_submit('selector-contract', definition['id'], expected_git_sha=sha)['submitted']
        device, warnings = devices.load_device(runner / '.syncmate/device.yaml')
        assert not warnings
        completed = queue.runner_queue_run_once(device)
        assert completed['status'] == 'done', completed
    warm = json.loads((runner / summary).read_text())
    assert all(r['score']['hit'] and r['selection']['cache']['hit'] for r in warm['selectors'])
    assert [r['output'] for r in warm['unlearning']] == [r['output'] for r in first['unlearning']]
    collector = runner / 'collector'
    collector.mkdir()
    for source in runner.glob('*.yaml'):
        (collector / source.name).write_bytes(source.read_bytes())
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        collected, _, _ = collect((runner, collector, sha, definition))
        accepted = extension.accept('modular-output-v1', definition, collected)
        assert accepted['passed'], accepted['errors']
        assert accepted['accepted_cells'] == 16
        # Even with a transport-valid digest, a false Selection identity is rejected.
        entry = next(r for r in collected['artifact_index']['peers']['cpu-runner']['items']
                     if r['remote_path'].endswith('/summary.json'))
        local = collector / entry['local_path']
        changed = json.loads(local.read_text())
        changed['selectors'][0]['selection']['artifact']['content_hash'] = 'f' * 64
        local.write_text(json.dumps(changed))
        entry['sha256'] = hashlib.sha256(local.read_bytes()).hexdigest()
        rejected = extension.accept('modular-output-v1', definition, collected)
        assert not rejected['passed'] and rejected['errors']
    record_property('collection', json.dumps({'accepted_cells': 16,
        'artifact_count': len(definition['expected_artifact_paths']), 'false_selection_rejected': True}))
