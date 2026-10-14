"""Real CPU request scheduling, reusable inputs and fail-closed result completion."""
import functools
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from time import perf_counter

import pytest
import torch
import yaml

from experiments.modular_artifacts import read_run
from experiments.modular_config import load_experiment
from experiments.modular_evaluation import evaluate_modular
from test_modular_consumers import tables, run, write_yaml
from test_modular_progress import prepare, invoke, recorder, assert_matches_plan
from test_unlearning_paired_evaluations import paired_tables


def request_tables(tables):
    root = paired_tables(tables)
    degree = yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    degree['budget'] = {'mode': 'ratio', 'value': .1}
    write_yaml(root/'degree.yaml', degree)
    write_yaml(root/'gif.yaml', {**tables[2], 'method': 'GIF',
                               'parameters': {'iteration': 2, 'scale': 100, 'damp': .1}})
    write_yaml(root/'gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
               'case': 'post_unlearning_utility_and_retrain_gap', 'metrics': ['gap']})
    return prepare(tables, selector_refs=['degree.yaml'], budget_ratios=[.1, .2],
        unlearning_refs=['gu.yaml', 'gif.yaml', 'retrain.yaml'],
        evaluation_refs=['utility.yaml', 'gap.yaml', 'flip.yaml'])


def test_real_request_cold_hot_and_added_metric(tables, monkeypatch):
    import experiments.modular_run as runner
    import experiments.unlearning_outputs as outputs
    import experiments.modular_model as model
    import experiments.output_lookup as lookup
    import experiments.modular_gu as gu
    root = tables[0]
    path = request_tables(tables)
    counts = Counter()
    decoded = Counter()
    def observe(module, name, label):
        original = getattr(module, name)
        @functools.wraps(original)
        def call(*args, **kwargs):
            counts[label] += 1
            if label == 'metric_output_load':
                decoded[args[0].get('artifact_id', args[0].get('path'))] += 1
            return original(*args, **kwargs)
        monkeypatch.setattr(module, name, call)
    for module, name, label in [
        (runner, 'read_dataset', 'dataset_read'), (runner, 'prepare_model', 'model_prepare'),
        (model, 'train_supervised', 'training'), (outputs, 'load_metric_output', 'metric_output_load'),
        (lookup, 'read_checkpoint_reference', 'checkpoint_metadata_read'),
        (gu, '_gu_producer', 'method_identity_prepare')]:
        observe(module, name, label)
    candidate = os.environ.get('AAGU097_CANDIDATE')
    evidence = {'candidate_commit': candidate, 'scenario': '20-node CPU fixture, one seed, two deletion budgets, Retrain/GNNDelete/GIF',
                'rounds': {}}
    def execute_round(name):
        counts.clear(); decoded.clear(); events = []
        started = perf_counter()
        from experiments.modular_execution import ExecutionContext
        context = ExecutionContext(run_id=name, level='verification', request_device='cpu',
            store_root=root/'results/cache_v2', checkpoint_root=root/'checkpoints',
            runtime_root=root/'runtime'/name, output=root/'results/runs/progress-fixture'/name/'run.json',
            executor='pytest-practical', source_git_sha=candidate)
        result = runner.execute(path, context=context, notify=recorder(events))
        elapsed = perf_counter() - started
        assert_matches_plan(load_experiment(path), events)
        document, cells = read_run(context.output, hashlib.sha256(context.output.read_bytes()).hexdigest())
        evidence['rounds'][name] = {'wall_seconds': elapsed, 'calls': dict(counts),
            'metric_loads_by_output': dict(decoded), 'trace': events, 'run': document,
            'metrics': [cell['metrics.json'] for cell in cells],
            'selections': [cell['selection.json'] for cell in cells],
            'phase_seconds': result['execution_timing'],
            'output_hits': sum(row['hit'] for row in result['unlearning']),
            'single_evaluation_hits': sum(row['evaluation_cache']['hit'] for row in result['unlearning']),
            'configured_evaluation_hits': sum(row['cache']['hit'] for e in result['evaluations'] for row in e['rows']),
            'configured_evaluation_misses': sum(not row['cache']['hit'] for e in result['evaluations'] for row in e['rows'])}
        return result, context
    cold, context = execute_round('cold')
    assert len(cold['unlearning']) == 6 and len(cold['selectors']) == 2
    assert counts['dataset_read'] == 1 and counts['model_prepare'] == 1
    assert counts['metric_output_load'] == 6 and all(value == 1 for value in decoded.values())
    events = evidence['rounds']['cold']['trace']
    starts = [e['position'] for e in events if e['kind'] == 'progress' and e['current'] == 0]
    for batch in (0, 1):
        stages = [e for e in starts if e.get('batch_index') == batch]
        assert [s['stage'] for s in stages] == ['selector', 'unlearning', 'evaluation',
            'unlearning', 'evaluation', 'unlearning', 'evaluation', 'request_complete']
        assert [s['unlearning_ref'] for s in stages if s['stage'] == 'unlearning'] == [
            './retrain.yaml', './gu.yaml', './gif.yaml']
    assert max(i for i,e in enumerate(events) if e['position'].get('batch_index') == 0) < min(
        i for i,e in enumerate(events) if e['position'].get('batch_index') == 1)
    for evaluation in cold['evaluations']:
        # Full post-hoc evaluation must select the exact same baselines and numbers.
        posthoc = evaluate_modular(evaluation['effective_config'], cold['unlearning'],
            store_root=root/'results/cache_v2', dataset_root=root)
        for actual, expected in zip(evaluation['rows'], posthoc['rows']):
            assert {k:v for k,v in actual.items() if k != 'cache'} == {k:v for k,v in expected.items() if k != 'cache'}
    def forbid(*args, **kwargs):
        raise AssertionError('warm/metric-only path executed a model')
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbid)
    try:
        hot, _ = execute_round('hot')
        assert counts['training'] == counts['model_prepare'] == counts['metric_output_load'] == 0
        assert all(row['hit'] and row['evaluation_cache']['hit'] for row in hot['unlearning'])
        assert all(row['cache']['hit'] for e in hot['evaluations'] for row in e['rows'])
        write_yaml(root/'gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
            'case': 'post_unlearning_utility_and_retrain_gap', 'metrics': ['gap', 'gap_pct']})
        added, _ = execute_round('added-metric')
        assert counts['training'] == counts['model_prepare'] == 0
        assert counts['metric_output_load'] == 6 and all(value == 1 for value in decoded.values())
        assert all(row['hit'] and row['evaluation_cache']['hit'] for row in added['unlearning'])
        for e in added['evaluations']:
            assert all(row['cache']['hit'] == (e['effective_config']['case'] != 'post_unlearning_utility_and_retrain_gap') for row in e['rows'])
    finally:
        hook.remove()
    assert [r['output'] for r in cold['unlearning']] == [r['output'] for r in hot['unlearning']] == [r['output'] for r in added['unlearning']]
    assert evidence['rounds']['cold']['metrics'] == evidence['rounds']['hot']['metrics']
    for cell in evidence['rounds']['added-metric']['run']['cells']:
        if cell['conditions']['method'] == 'Retrain':
            assert cell['cache']['post_unlearning_flip_hop'] == 'not_applicable'
            assert cell['cache']['post_unlearning_utility_and_retrain_gap'] == 'not_applicable'
            assert cell['cache']['post_unlearning_utility'] == 'hit'
    metrics = run(tables, 'independent', stage='metrics', selector_refs=[],
        evaluation_refs=['utility.yaml', 'gap.yaml', 'flip.yaml'],
        output_inputs=[{'run':str(context.output), 'sha256':hashlib.sha256(context.output.read_bytes()).hexdigest()}])
    assert [e['rows'][0]['metrics'] for e in metrics['evaluations']] == [e['rows'][0]['metrics'] for e in added['evaluations']]
    evidence['posthoc_values_and_pairs_equal'] = True
    evidence['independent_metrics_equal'] = True
    evidence['all_hot_and_added_model_forward_forbidden'] = True
    evidence['config'] = yaml.safe_load(path.read_text(encoding='utf-8'))
    evidence['dataset_manifest'] = json.loads((root/'dataset.json').read_text(encoding='utf-8'))
    evidence['audit_events'] = [json.loads(line) for line in (root/'runtime/_journal/auto_report.events.jsonl').read_text(encoding='utf-8').splitlines()]
    destination = os.environ.get('AAGU097_EVIDENCE')
    if destination:
        Path(destination).write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding='utf-8')


def test_evaluation_failure_stops_before_next_method_and_request(tables, monkeypatch):
    import experiments.modular_run as runner
    path = request_tables(tables)
    original = runner.evaluate_modular
    def fail(instance, rows, **kwargs):
        if rows[0]['target']['method'] == 'GNNDelete':
            raise RuntimeError('owned evaluation failure')
        return original(instance, rows, **kwargs)
    monkeypatch.setattr(runner, 'evaluate_modular', fail)
    events = []
    with pytest.raises(RuntimeError, match='owned evaluation failure'):
        invoke(path, tables[0], 'failed-evaluation', recorder(events))
    assert not any(e['position'].get('stage') == 'request_complete' for e in events)
    assert not any(e['position'].get('batch_index') == 1 for e in events)
    result = json.loads((tables[0]/'results/runs/progress-fixture/failed-evaluation/run.json').read_text(encoding='utf-8'))
    assert result['status'] == 'failed'
    assert next(c for c in result['cells'] if c['status'] == 'failed')['conditions']['method'] == 'GNNDelete'
    assert all(c['status'] != 'completed' for c in result['cells'])
    assert not any(e['position'].get('unlearning_ref') == './gif.yaml' for e in events)
    monkeypatch.setattr(runner, 'evaluate_modular', original)
    resumed, _ = invoke(path, tables[0], 'fresh-after-failure')
    retained = [r for r in resumed['unlearning'] if r['hit']]
    assert len(retained) == 2
    assert {r['target']['method'] for r in retained} == {'Retrain', 'GNNDelete'}
    assert all(r['matrix_values']['budget_ratio'] == .2 for r in retained)


def test_two_selectors_finish_in_request_order(tables):
    path = request_tables(tables)
    root = tables[0]
    other = yaml.safe_load((root/'degree.yaml').read_text(encoding='utf-8'))
    other['method'] = 'random'
    other['parameters'] = {'seed': 17}
    write_yaml(root/'random.yaml', other)
    config = yaml.safe_load(path.read_text(encoding='utf-8'))
    config.update(selector_refs=['degree.yaml', 'random.yaml'], budget_ratios=[.2])
    write_yaml(path, config)
    events = []
    result, _ = invoke(path, root, 'two-selectors', recorder(events))
    assert_matches_plan(load_experiment(path), events)
    positions = [e['position'] for e in events if 'selector_ref' in e['position']]
    assert max(i for i,p in enumerate(positions) if p['selector_ref'] == './degree.yaml') < min(
        i for i,p in enumerate(positions) if p['selector_ref'] == './random.yaml')
    assert len(result['unlearning']) == 6


def test_retrain_only_marks_pairs_inapplicable_and_no_retrain_is_invented(tables):
    root = paired_tables(tables)
    only = run(tables, 'only-retrain', stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['retrain.yaml'], evaluation_refs=['utility.yaml', 'gap.yaml', 'flip.yaml'])
    assert len(only['evaluations'][0]['rows']) == 1
    assert all(not e['rows'] and len(e['not_applicable']) == 1 for e in only['evaluations'][1:])
    plain = run(tables, 'no-retrain', stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml'], evaluation_refs=['utility.yaml'])
    assert [r['target']['method'] for r in plain['unlearning']] == ['GNNDelete']
    with pytest.raises(ValueError, match='explicit Retrain'):
        run(tables, 'missing-retrain', stage='unlearning', selector_refs=['degree.yaml'],
            unlearning_refs=['gu.yaml'], evaluation_refs=['gap.yaml'])
