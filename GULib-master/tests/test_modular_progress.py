"""Real disposable CPU lanes and batch notification noninterference."""
import copy
import json
from pathlib import Path

import pytest
import yaml

from experiments.modular_config import load_experiment
from experiments.modular_execution import ExecutionContext
from experiments.modular_progress import execution_batches, progress_steps
from experiments.modular_run import execute
from test_modular_consumers import tables, write_yaml
from test_cache_v2_formal_artifacts import _tree_state
from utils.target_checkpoint import sha256_file


def prepare(tables, stage='unlearning', **changes):
    root, base, _ = tables
    config = copy.deepcopy(base)
    config.update(experiment_id='progress-fixture', stage=stage, selector_refs=['degree.yaml'])
    if stage == 'unlearning':
        config.update(unlearning_refs=['gu.yaml'], evaluation_refs=['utility.yaml'])
    config.update(changes)
    path = root/'progress.yaml'
    write_yaml(path, config)
    return path


def invoke(path, root, name, notify=None):
    context = ExecutionContext(run_id=name, level='verification', request_device='cpu',
        store_root=root/'results/cache_v2', checkpoint_root=root/'checkpoints',
        runtime_root=root/'runtime'/name, output=root/'results/runs/progress-fixture'/name/'run.json',
        executor='pytest')
    return execute(path, context=context, notify=notify), context


def recorder(events):
    def notify(kind, **values):
        events.append({'kind': kind, **copy.deepcopy(values)})
    return notify


def assert_matches_plan(config, events):
    expected = []
    for step in progress_steps(config):
        expected.extend({'kind': 'progress', 'position': step['position'],
                         'current': index, 'total': step['total']}
                        for index in range(step['total'] + 1))
    expected.append({'kind': 'completed', 'position': {}})
    assert events == expected
    assert all(type(value) in (str, int) for event in events for value in event['position'].values())


def scientific_values(result):
    return {
        'selectors': [(row['score']['artifact_id'], row['score']['recipe_hash'],
                       row['score']['content_hash'], row['selection']['artifact'],
                       {key: {name: value for name, value in view.items() if name != 'cache_outcome'}
                        for key, view in row['selection']['views'].items()}, row['matrix_values'])
                      for row in result['selectors']],
        'unlearning': [(row['output'], row['recipe_hash'], row['matrix_values'])
                       for row in result['unlearning']],
        'evaluations': result['evaluations'],
    }


@pytest.mark.parametrize('stage', ['selector', 'unlearning'])
def test_optional_events_complete_real_cold_and_hit_lanes(tables, stage):
    root = tables[0]
    path = prepare(tables, stage)
    events = []
    cold, _ = invoke(path, root, 'cold-on', recorder(events))
    assert_matches_plan(load_experiment(path), events)
    assert cold['selector_producer_called']
    cache_before = _tree_state(root/'results/cache_v2')
    warm_events = []
    warm, _ = invoke(path, root, 'warm-on', recorder(warm_events))
    plain, _ = invoke(path, root, 'warm-off')
    assert_matches_plan(load_experiment(path), warm_events)
    assert not warm['selector_producer_called'] and not plain['selector_producer_called']
    assert scientific_values(cold) == scientific_values(warm) == scientific_values(plain)
    assert [row['selection']['views'] for row in warm['selectors']] == [row['selection']['views'] for row in plain['selectors']]
    assert _tree_state(root/'results/cache_v2') == cache_before
    if stage == 'unlearning':
        assert all(row['hit'] and not row['producer_called'] for row in warm['unlearning'] + plain['unlearning'])


def test_plan_and_execution_share_descending_budget_order(tables):
    root = tables[0]
    degree = yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    degree['budget'] = {'mode': 'ratio', 'value': .2}
    write_yaml(root/'degree.yaml', degree)
    path = prepare(tables, budget_ratios=[.2, .4], seeds=[7, 19])
    events = []
    result, _ = invoke(path, root, 'ordered', recorder(events))
    config = load_experiment(path)
    batches = execution_batches(config)
    assert [batch['matrix_values']['budget_ratio'] for batch in batches] == [.4, .4, .2, .2]
    assert [row['matrix_values'] for row in result['selectors']] == [batch['matrix_values'] for batch in batches]
    assert [batch['matrix_values']['budget_ratio'] for batch in result['batches']] == [.2, .4, .2, .4]
    assert_matches_plan(config, events)
    assert all(row['selection']['artifact_k'] == 4 for row in result['selectors'])


def test_metrics_only_reports_input_loading_evaluation_and_export(tables):
    root = tables[0]
    path = prepare(tables)
    source, context = invoke(path, root, 'source')
    path = prepare(tables, stage='metrics', selector_refs=[],
        output_inputs=[{'run': str(context.output), 'sha256': sha256_file(context.output)}],
        evaluation_refs=['utility.yaml'])
    events = []
    result, _ = invoke(path, root, 'metrics', recorder(events))
    assert_matches_plan(load_experiment(path), events)
    assert result['evaluations'] == source['evaluations']
    assert not result['selector_producer_called'] and not result['selectors'] and not result['unlearning']


def test_notification_exception_is_warning_and_does_not_fail_science(tables, capsys):
    root = tables[0]
    path = prepare(tables)
    plain, _ = invoke(path, root, 'baseline')
    events = []
    def broken(kind, **values):
        events.append({'kind': kind, **values})
        raise OSError('unavailable notification transport')
    observed, context = invoke(path, root, 'broken-notify', broken)
    assert scientific_values(observed) == scientific_values(plain)
    assert_matches_plan(load_experiment(path), events)
    assert 'optional progress notification failed: OSError' in capsys.readouterr().err
    assert json.loads(context.output.read_text(encoding='utf-8'))['status'] == 'completed'


def test_scientific_observer_keeps_its_events_with_optional_progress(tables):
    root, _, gu = tables
    gu.update(method='GIF', parameters={'iteration': 2, 'scale': 100, 'damp': .1})
    write_yaml(root/'gu.yaml', gu)
    path = prepare(tables, execution={'gu_cache': {'GIF': 'disabled'}},
        observers=[{'name': 'linear_solver_trace', 'methods': ['GIF']}])
    plain, plain_context = invoke(path, root, 'observer-off')
    events = []
    observed, context = invoke(path, root, 'observer-on', recorder(events))
    assert_matches_plan(load_experiment(path), events)
    assert observed['evaluations'][0]['rows'][0]['metrics'] == plain['evaluations'][0]['rows'][0]['metrics']
    for current in (plain_context, context):
        result = json.loads(current.output.read_text(encoding='utf-8'))
        cell = result['cells'][0]
        assert cell['observers'][0]['status'] == 'completed'
        folder = current.output.parent/cell['path']/'observers/linear_solver_trace'
        metadata = json.loads((folder/'result.json').read_text(encoding='utf-8'))
        assert [event['step'] for event in metadata['events'] if event['phase'] == 'solver_step'] == [0, 1, 2]
        trace = (folder/'trace.jsonl').read_text(encoding='utf-8')
        if current is plain_context:
            baseline = trace
        else:
            assert trace == baseline


@pytest.mark.parametrize('failure', ['data', 'selector', 'unlearning', 'evaluation', 'export'])
def test_scientific_errors_propagate_without_completed(tables, monkeypatch, failure):
    import experiments.modular_run as entry
    import experiments.modular_artifacts as artifacts
    import experiments.modular_gu as gu
    root = tables[0]
    path = prepare(tables)
    events = []
    error = RuntimeError('scientific ' + failure + ' failure')
    def forbidden(*args, **kwargs):
        raise error
    module, name = {'data': (entry, 'read_dataset'), 'selector': (entry, 'resolve_methods'),
                    'unlearning': (gu, 'run_unlearning'), 'evaluation': (entry, 'evaluate_modular'),
                    'export': (artifacts, 'export_outputs')}[failure]
    monkeypatch.setattr(module, name, forbidden)
    with pytest.raises(RuntimeError) as raised:
        invoke(path, root, 'failed', recorder(events))
    assert raised.value is error
    assert not any(event['kind'] == 'completed' for event in events)
    assert events[-1]['position']['stage'] == failure
    assert events[-1]['current'] == 0
    result = json.loads((root/'results/runs/progress-fixture/failed/run.json').read_text(encoding='utf-8'))
    assert result['status'] == 'failed' and result['error'] == str(error)


def test_metric_input_error_propagates_without_completed(tables, monkeypatch):
    import experiments.unlearning_outputs as outputs
    root = tables[0]
    path = prepare(tables)
    _, context = invoke(path, root, 'source')
    path = prepare(tables, stage='metrics', selector_refs=[],
        output_inputs=[{'run': str(context.output), 'sha256': sha256_file(context.output)}],
        evaluation_refs=['utility.yaml'])
    events = []
    error = RuntimeError('scientific metric-input failure')
    def forbidden(*args, **kwargs):
        raise error
    monkeypatch.setattr(outputs, 'load_output', forbidden)
    with pytest.raises(RuntimeError) as raised:
        invoke(path, root, 'metrics-failed', recorder(events))
    assert raised.value is error
    assert not any(event['kind'] == 'completed' for event in events)
    assert events[-1] == {'kind': 'progress', 'position': {'stage': 'metric_inputs'}, 'current': 0, 'total': 1}


def test_dry_run_never_notifies(tables):
    path = prepare(tables)
    events = []
    result = execute(path, dry_run=True, notify=recorder(events))
    assert result['dry_run'] and events == []


def test_exp079_batch_plan_covers_real_matrix_without_per_cell_nodes():
    root = Path(__file__).resolve().parents[1]
    config = load_experiment(root/'experiments/configs/exp079/surrogate_multiseed.yaml')
    steps = progress_steps(config)
    assert len(execution_batches(config)) == 120
    assert len(steps) == 247
    assert sum(step['total'] for step in steps if step['position']['stage'] == 'selector') == 360
    assert sum(step['total'] for step in steps if step['position']['stage'] == 'unlearning') == 2520
    assert len({json.dumps(step['position'], sort_keys=True) for step in steps}) == len(steps)
    assert all(type(step['total']) is int and step['total'] > 0 for step in steps)
