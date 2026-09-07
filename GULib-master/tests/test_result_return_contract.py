"""Real result delivery and regeneration, with no computation-cache redesign."""
import copy
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from test_modular_consumers import tables, write_yaml
from test_syncmate_execution_contract import workspace, commit, cli, declaration
from test_syncmate_gu_outputs import collect
from test_unified_execution import command
from experiments.modular_artifacts import existing_scores, read_run, output_paths
from experiments.modular_config import load_experiment
from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
from syncmate_core import context, collection, index


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_existing_scores_optional_variants_and_requested_order(tables):
    root, config, gu = tables
    config.update(experiment_id='score-delivery', selector_refs=['degree.yaml'],
                  return_scores=True, budget_ratios=[.2, .1])
    selector = __import__('yaml').safe_load((root/'degree.yaml').read_text())
    selector['budget'] = {'mode':'ratio', 'value':.2}
    write_yaml(root/'degree.yaml', selector)
    path = root/'experiment.yaml'; write_yaml(path, config)
    summary = command(root, path, 'scores')
    run_path = Path(summary['execution_receipt']['output'])
    run, documents = read_run(run_path, digest(run_path))
    assert len(run['cells']) == 2
    assert all(c['conditions']['method'] is None for c in run['cells'])
    assert {Path(p).name for p in output_paths(run_path, load_experiment(path))} == {'scores.npz','selection.json'}
    assert [d['selection.json']['requested_k'] for d in documents] == [2,1]
    for doc in documents:
        arrays = doc['scores.npz']
        assert arrays['ranking'][:doc['selection.json']['requested_k']].tolist() == doc['selection.json']['selected_nodes']
        assert len(arrays['scores']) == 10
    # Different instances of the same method must not share a result directory.
    write_yaml(root/'gu2.yaml', {**gu, 'parameters': {**gu['parameters'], 'unlearn_lr':.02}})
    config.update(stage='unlearning', unlearning_refs=['gu.yaml','gu2.yaml'])
    write_yaml(path, config)
    from experiments.modular_artifacts import planned_cells
    cells = planned_cells(load_experiment(path))
    assert len(cells) == len({c['path'] for c in cells}) == 4


def test_im_projection_never_demands_full_ranking():
    # The ordinary target-direct selector registry does not implement IM. This
    # tests only the shared result projector's boundary for an existing IM result.
    result = {'selection': {'strategy':'im'}, 'selected_gains':[.6,.2]}
    arrays, semantics = existing_scores(result, range(100000))
    assert set(arrays) == {'selected_gains'} and len(arrays['selected_gains']) == 2
    assert semantics == 'recorded_selection_step_gains'
    with pytest.raises(ValueError, match='no recorded'):
        existing_scores({'selection':{'strategy':'im'}}, range(100000))


def test_real_metrics_fix_refreshes_current_collected_results(workspace, record_property):
    runner, path, config = workspace
    config.update(stage='unlearning', unlearning_refs=['gu.yaml','retrain.yaml'])
    write_yaml(path, config)
    old_sha = commit(runner)
    result = cli(runner, path, 'registered')
    assert result.returncode == 0, result.stdout + result.stderr
    first = json.loads(result.stdout)
    source = Path(first['execution_receipt']['output'])
    original = {p: p.read_bytes() for p in source.parent.rglob('*') if p.is_file()}
    original_values = [r['evaluation']['metrics']['cross_entropy'] for r in first['unlearning']]
    old_definition = declaration(runner, path, 'unlearning')
    collector = runner/'collector'; collector.mkdir()
    for p in runner.glob('*.yaml'):
        (collector/p.name).write_bytes(p.read_bytes())
    extension = OpenGUProjectExtension()
    with context.use(collector, extension=extension):
        old_context, _, _ = collect((runner,collector,old_sha,old_definition))
        assert extension.accept('modular-output-v1', old_definition, old_context)['passed']
        assert len(extension.results(old_context['artifact_index'], {'project_root':collector})['rows']) == 8
    # A real metric-code correction in the disposable runner. Training code,
    # methods and cache identities are not changed or mocked.
    metric_code = runner/'experiments/output_metrics.py'
    code = metric_code.read_text()
    old = "float(torch.nn.functional.cross_entropy(logits, torch.tensor(labels)))"
    assert old in code
    metric_code.write_text(code.replace(old, old+' + 0.125'))
    write_yaml(runner/'metric_case.yaml', {'kind':'evaluation','schema_version':1,'case':'post_method_metrics'})
    metrics = {'kind':'experiment','schema_version':1,'experiment_id':'metrics-refresh','stage':'metrics',
        'matrix':'cartesian_product','dataset_refs':['dataset.yaml'], 'evaluation_refs':['metric_case.yaml'],
        'output_inputs':[{'run':source.relative_to(runner).as_posix(),'sha256':digest(source)}]}
    metric_path = runner/'refresh.yaml'; write_yaml(metric_path, metrics)
    new_sha = commit(runner)
    fresh = cli(runner, metric_path, 'refreshed')
    assert fresh.returncode == 0, fresh.stdout + fresh.stderr
    output = Path(json.loads(fresh.stdout)['execution_receipt']['output'])
    refreshed, docs = read_run(output, digest(output))
    assert [d['metrics.json']['rows'][0]['values']['cross_entropy'] for d in docs] == pytest.approx([v+.125 for v in original_values])
    definition = declaration(runner, metric_path, 'metrics')
    definition.update(config_path='refresh.yaml', run_identity={'experiment_id':'metrics-refresh','run_id':'refreshed'},
        expected_artifact_paths=[output.relative_to(runner).as_posix()]+list(output_paths(output.relative_to(runner), load_experiment(metric_path))),
        collector_result_roots=[output.parent.relative_to(runner).as_posix()])
    for p in runner.glob('*.yaml'):
        (collector/p.name).write_bytes(p.read_bytes())
    with context.use(collector, extension=extension):
        current, args, options = collect((runner,collector,new_sha,definition))
        accepted = extension.accept('modular-output-v1', definition, current)
        assert accepted['passed'], accepted
        rows = extension.results(current['artifact_index'], {'project_root':collector})
        assert not rows['parse_errors'], rows
        assert len(rows['rows']) == 8
        assert all(r['run_id'] == 'refreshed' and r['git_sha'] == new_sha for r in rows['rows'])
        by_cell = {r['cell_id']:r for r in rows['rows']}
        for cell, doc in zip(refreshed['cells'], docs):
            assert by_cell[cell['cell_id']]['cross_entropy'] == doc['metrics.json']['rows'][0]['values']['cross_entropy']
        assert collection.apply_collect(*args, **options)['summary']['fetched'] == 0
    assert all(p.read_bytes() == value for p,value in original.items())
    assert not (collector/'data').exists() and not (collector/'results/cache_v2').exists()
    record_property('metrics_refresh', json.dumps({'original_commit':old_sha,'metrics_commit':new_sha,
        'cells':8,'actual_delta':.125,'current_run':'refreshed','old_run_unchanged':True,
        'input_free_collector':True,'artifact_count':len(definition['expected_artifact_paths'])}))
