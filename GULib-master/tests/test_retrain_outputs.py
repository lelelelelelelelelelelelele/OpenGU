"""Real CPU evidence for independent Retrain and output-only Metrics."""
import copy
import hashlib
import json

import numpy as np
import pytest
import torch
import yaml
from test_modular_consumers import tables, run, write_yaml
from experiments.unlearning_outputs import load_output


def snapshot(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def configs(tables):
    root, _, gu = tables
    retrain = {k: copy.deepcopy(gu[k]) for k in ('kind', 'schema_version', 'model', 'training')}
    retrain['method'] = 'Retrain'
    write_yaml(root / 'retrain.yaml', retrain)
    gif = {**copy.deepcopy(gu), 'method': 'GIF', 'parameters': {'iteration': 2}}
    write_yaml(root / 'gif.yaml', gif)
    write_yaml(root / 'gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
                                 'case': 'post_unlearning_utility_and_retrain_gap'})
    selection = run(tables, 'selection', selector_refs=['degree.yaml'])
    return {key: selection['selectors'][0]['selection']['artifact'][key]
            for key in ('artifact_id', 'recipe_hash', 'content_hash')}


def method(tables, name, reference, method_file):
    return run(tables, 'run-' + name, stage='unlearning', selector_refs=[],
               selection_input=reference, unlearning_refs=[method_file])['unlearning'][0]


def forbidden(*args, **kwargs):
    raise AssertionError('training or selection producer called during read-only consumption')


def test_independent_retrain_cold_hot_cross_gu_and_metrics_only(tables, monkeypatch, record_property):
    reference = configs(tables)
    import experiments.modular_run as entry
    monkeypatch.setattr(entry, 'resolve_methods', forbidden)
    cold = method(tables, 'retrain-cold', reference, 'retrain.yaml')
    assert cold['producer_called'] and cold['checkpoint'] is None
    assert not (tables[0] / 'checkpoints').exists()
    gnn = method(tables, 'gnn', reference, 'gu.yaml')
    gif = method(tables, 'gif', reference, 'gif.yaml')
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    monkeypatch.setattr(torch.optim.SGD, 'step', forbidden)
    monkeypatch.setattr(entry, 'prepare_model', forbidden)
    warm = method(tables, 'retrain-hot', reference, 'retrain.yaml')
    assert warm['hit'] and not warm['producer_called']
    assert cold['output'] == warm['output'] and cold['result'] == warm['result']
    pairs = [{'unlearning': row['output'], 'retrain': cold['output']} for row in (gnn, gif)]
    before = snapshot(tables[0] / 'v2')
    metrics = run(tables, 'metrics', stage='metrics', selector_refs=[],
                  output_inputs=pairs, evaluation_refs=['gap.yaml'])
    again = run(tables, 'metrics-again', stage='metrics', selector_refs=[],
                output_inputs=pairs, evaluation_refs=['gap.yaml'])
    assert metrics['evaluations'] == again['evaluations']
    assert before == snapshot(tables[0] / 'v2')
    for output, row in zip((gnn, gif), metrics['evaluations'][0]['rows']):
        payload = load_output(output['output'], tables[0] / 'v2')
        rt = load_output(cold['output'], tables[0] / 'v2')
        mask = payload.arrays['test_mask']
        expected = float(np.mean(rt.arrays['logits'][mask].argmax(1) == rt.arrays['y'][mask]))
        assert row['metrics']['perf_retrain'] == expected
        assert payload.identity['pairing'] == rt.identity['pairing']
        assert rt.state and payload.state
        from experiments.unlearning_outputs import restore_model
        for saved in (payload, rt):
            restored = restore_model(saved)
            with torch.no_grad():
                logits = restored(torch.tensor(saved.arrays['x']), torch.tensor(saved.arrays['evaluation_edge_index'])).numpy()
            np.testing.assert_array_equal(logits, saved.arrays['logits'])
    record_property('aagu028_evidence', json.dumps({
        'retrain': cold['output'], 'warm': warm['output'],
        'GU_outputs': [gnn['output'], gif['output']],
        'metrics': metrics['evaluations'], 'store_unchanged_by_metrics': True,
        'selector_and_training_forbidden': True}))


@pytest.mark.parametrize('change', ['training', 'model', 'semantics', 'request'])
def test_retrain_identity_changes_and_pairing_rejects(tables, change):
    reference = configs(tables)
    cold = method(tables, 'retrain-original', reference, 'retrain.yaml')
    gnn = method(tables, 'gnn-original', reference, 'gu.yaml')
    root = tables[0]
    config = yaml.safe_load((root / 'retrain.yaml').read_text())
    if change == 'training':
        config['training']['lr'] = .02
    elif change == 'model':
        config['model']['hidden_channels'] = 8
    elif change == 'semantics':
        config['deletion'] = {'evaluation_graph': 'retained'}
    else:
        selector = yaml.safe_load((root / 'degree.yaml').read_text())
        selector['budget']['value'] = 2
        write_yaml(root / 'degree.yaml', selector)
        selected = run(tables, 'selection2', selector_refs=['degree.yaml'])
        reference = {key: selected['selectors'][0]['selection']['artifact'][key]
                     for key in ('artifact_id', 'recipe_hash', 'content_hash')}
    write_yaml(root / 'changed.yaml', config)
    changed = method(tables, 'changed-retrain', reference, 'changed.yaml')
    assert changed['producer_called'] and changed['recipe_hash'] != cold['recipe_hash']
    with pytest.raises(ValueError, match='same request'):
        run(tables, 'bad-pair', stage='metrics', selector_refs=[], evaluation_refs=['gap.yaml'],
            output_inputs=[{'unlearning': gnn['output'], 'retrain': changed['output']}])


def test_gu_parameters_and_metrics_do_not_change_retrain(tables):
    reference = configs(tables)
    original = method(tables, 'original', reference, 'retrain.yaml')
    root, _, gu = tables
    gu['parameters']['unlearn_lr'] = .02
    write_yaml(root / 'gu.yaml', gu)
    result = run(tables, 'changed-gu', stage='unlearning', selector_refs=[], selection_input=reference,
                 unlearning_refs=['gu.yaml'])
    result['evaluations'] = run(tables, 'changed-gu-metrics', stage='metrics', selector_refs=[],
        output_inputs=[{'unlearning': result['unlearning'][0]['output'], 'retrain': original['output']}],
        evaluation_refs=['gap.yaml'])['evaluations']
    write_yaml(root / 'small.yaml', {'kind': 'evaluation', 'schema_version': 1,
                                   'case': 'post_unlearning_utility_and_retrain_gap', 'metrics': ['gap']})
    small = run(tables, 'small-metrics', stage='metrics', selector_refs=[],
        output_inputs=[{'unlearning': result['unlearning'][0]['output'], 'retrain': original['output']}],
        evaluation_refs=['small.yaml'])
    assert small['evaluations'][0]['rows'][0]['metrics']['gap'] == result['evaluations'][0]['rows'][0]['metrics']['gap']
    warm = method(tables, 'warm-retrain', reference, 'retrain.yaml')
    assert warm['output'] == original['output'] and not warm['producer_called']


def test_retrain_removes_supervision_and_incident_edges(tables):
    reference = configs(tables)
    result = method(tables, 'retrain', reference, 'retrain.yaml')
    payload = load_output(result['output'], tables[0] / 'v2')
    a = payload.arrays
    assert not a['retain_mask'][a['selected_nodes']].any()
    assert not np.isin(a['training_edge_index'], a['selected_nodes']).any()
    assert np.array_equal(a['evaluation_edge_index'], a['edge_index'])
    assert a['x'].shape[0] == len(a['y'])
    assert payload.identity['pairing']['deletion']['features'] == 'retain_isolated_rows'
    import pickle
    from experiments.modular_model import prepare_model
    from experiments.modular_config import load_instance
    from experiments.node_deletion import retained_graph
    from utils.target_checkpoint import state_hash
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    retained = retained_graph(data, a['selected_nodes'])
    model, _, checkpoint = prepare_model(load_instance(tables[0] / 'retrain.yaml', 'unlearning'),
        data=retained, dataset_name='cpu_fixture', checkpoint_root=tables[0] / 'reference-checkpoints',
        device=torch.device('cpu'), reference_directory=tables[0])
    assert state_hash({key: torch.tensor(value) for key, value in payload.state.items()}) == checkpoint['state_hash']


def test_missing_and_corrupted_outputs_rejected_without_training(tables, monkeypatch):
    reference = configs(tables)
    result = method(tables, 'retrain', reference, 'retrain.yaml')
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    wrong = {**result['output'], 'content_hash': '0' * 64}
    with pytest.raises(ValueError, match='digest'):
        load_output(wrong, tables[0] / 'v2')
    with pytest.raises(ValueError, match='MISS'):
        load_output(result['output'], tables[0] / 'absent')
    payload_path = tables[0] / 'v2/artifacts/prediction' / result['artifact_id'] / 'payload.npz'
    payload_path.write_bytes(payload_path.read_bytes() + b'corrupt disposable fixture')
    with pytest.raises(Exception, match='hash|size|mismatch'):
        load_output(result['output'], tables[0] / 'v2')


@pytest.mark.parametrize('field', ['x', 'y', 'edge_index', 'split'])
def test_actual_dataset_changes_cannot_consume_old_output(tables, field):
    import pickle
    reference = configs(tables)
    output = method(tables, 'retrain', reference, 'retrain.yaml')['output']
    data = pickle.loads((tables[0] / 'graph.pkl').read_bytes())
    if field == 'x':
        data.x[0, 0] += 1
    elif field == 'y':
        data.y[0] = 1 - data.y[0]
    elif field == 'edge_index':
        data.edge_index = data.edge_index[:, :-1]
    else:
        data.train_mask[9], data.train_mask[10] = False, True
        data.val_mask[9], data.val_mask[10] = True, False
    with pytest.raises(ValueError, match='identity mismatch'):
        load_output(output, tables[0] / 'v2', data=data)


def changed_retrain(*args, **kwargs):
    raise AssertionError('changed producer must not run during reference validation')


def test_changed_producer_and_missing_selection_dependency_rejected(tables, monkeypatch):
    from cache_v2 import CacheIndex
    import unlearning.unlearning_methods.Retrain.retrain as retrain
    reference = configs(tables)
    output = method(tables, 'retrain', reference, 'retrain.yaml')['output']
    with monkeypatch.context() as patch:
        patch.setattr(retrain, 'run_retrain', changed_retrain)
        with pytest.raises(ValueError, match='producer changed'):
            load_output(output, tables[0] / 'v2')
    record = CacheIndex(tables[0] / 'v2/index.sqlite').get_artifact(reference['artifact_id'])
    path = tables[0] / 'v2' / record['semantic_path']
    path.unlink()  # Disposable fixture only: prove missing dependencies fail closed.
    with pytest.raises(Exception, match='missing'):
        load_output(output, tables[0] / 'v2')


def test_aggregate_serialization_is_lossless():
    from attack.attack_result import AttackResult
    original = AttackResult('degree', [1], .71234567, .65432109, .123456789, .987654321)
    assert original.to_dict() == AttackResult.from_dict(original.to_dict()).to_dict()


def test_metrics_cli_and_target_direct_shared_consumer(tables, monkeypatch, record_property):
    import subprocess
    import sys
    from pathlib import Path
    from experiments.modular_config import load_instance
    from experiments.modular_run import read_dataset, verified_selection
    from experiments.modular_model import prepare_model
    from experiments.target_direct_v1.run_outputs import execute_bound_method
    from utils.target_checkpoint import load_target_checkpoint
    reference = configs(tables)
    root = tables[0]
    data, inputs = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    selection = verified_selection(reference, store_root=root / 'v2', data=data, inputs=inputs)
    gu = load_instance(root / 'gu.yaml', 'unlearning')
    retrain = load_instance(root / 'retrain.yaml', 'unlearning')
    _, _, cp = prepare_model(gu, data=data, dataset_name=inputs.dataset_name,
        checkpoint_root=root / 'checkpoints', device=torch.device('cpu'), reference_directory=root)
    checkpoint = load_target_checkpoint(cp['path'], expected_file_sha256=cp['file_sha256'])
    rows = [execute_bound_method(instance=instance, selection=selection, data=data,
        dataset_name=inputs.dataset_name, checkpoint=bound_checkpoint, store_root=root / 'v2',
        runtime_root=root / 'target-stage') for instance, bound_checkpoint in ((gu, checkpoint), (retrain, None))]
    pairs = [{'strategy': 'degree', 'unlearning': rows[0]['output'], 'retrain': rows[1]['output']}]
    (root / 'references.json').write_text(json.dumps(pairs))
    store_before = snapshot(root / 'v2')
    command = [sys.executable, '-B', '-X', 'utf8', 'eval_collateral.py',
        '--store-root', str(root / 'v2'), '--inputs', str(root / 'references.json'),
        '--evaluation', str(root / 'gap.yaml'), '--output-dir', str(root / 'cli-metrics')]
    completed = subprocess.run(command, cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert snapshot(root / 'v2') == store_before
    raw = json.loads((root / 'cli-metrics/collateral.json').read_text())
    assert raw['training_producer_called'] is False
    assert raw['results'][0]['perf_unlearn'] == rows[0]['result']['f1_after']
    record_property('aagu028_cli', json.dumps({'command': command, 'result': raw, 'store_unchanged': True}))


def test_independent_method_metrics_survive_collection_without_forward(tables, monkeypatch, record_property):
    import shutil
    from experiments.modular_evaluation import evaluate_modular, resolve_evaluation
    from experiments.target_direct_v1.run_outputs import save_method_result
    from cache_v2.unlearning_output import UnlearningOutputPayload
    reference = configs(tables)
    root = tables[0]
    # GU completes first; there is no Retrain output to consume at this point.
    gnn = method(tables, 'independent-gnn', reference, 'gu.yaml')
    rt = method(tables, 'independent-retrain', reference, 'retrain.yaml')
    gif = method(tables, 'independent-gif', reference, 'gif.yaml')
    exported = []
    for name, row in (('GNNDelete', gnn), ('Retrain', rt), ('GIF', gif)):
        folder = root / 'exports' / name
        save_method_result(row, store_root=root / 'v2', output_dir=folder,
                           strategy='degree', meta={'method': name})
        payload = UnlearningOutputPayload.from_bytes((folder / 'predictions.npz').read_bytes())
        assert payload.content_hash == row['content_hash']
        assert payload.state
        raw = json.loads((folder / 'attack.json').read_text())['results']['degree']
        assert raw['evaluation'] == row['evaluation']
        assert not (folder / 'collateral.json').exists()
        exported.append(raw)
    collected = root / 'collected-store'
    shutil.copytree(root / 'v2', collected)
    before = snapshot(collected)
    # A global forward hook blocks inference without changing fingerprinted method source.
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    monkeypatch.setattr(torch.optim.SGD, 'step', forbidden)
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbidden)
    try:
        single = resolve_evaluation({'kind': 'evaluation', 'schema_version': 1, 'case': 'post_method_metrics'})
        measured = evaluate_modular(single, [row['output'] for row in (gnn, rt, gif)], store_root=collected)
        for row, original in zip(measured['rows'], (gnn, rt, gif)):
            assert row['metrics'] == original['evaluation']['metrics']
            assert row['metrics']['f1'] == original['result']['f1_after']
        gap = resolve_evaluation({'kind': 'evaluation', 'schema_version': 1, 'case': 'post_unlearning_utility_and_retrain_gap'})
        differences = evaluate_modular(gap, [{'unlearning': row['output'], 'retrain': rt['output']}
                                           for row in (gnn, gif)], store_root=collected)
    finally:
        hook.remove()
    assert differences['rows'][0]['metrics']['gap'] == rt['result']['f1_after'] - gnn['result']['f1_after']
    assert before == snapshot(collected)
    assert measured['rows'][1]['metrics']['update_detection_auc_status'] == 'missing_original_predictions'
    record_property('aagu028_independent_collection', json.dumps({'per_method': exported,
        'recomputed': measured, 'differences': differences, 'store_unchanged': True,
        'training_and_forward_forbidden': True}))


def test_auc_reports_missing_classes_without_producing_data():
    from types import SimpleNamespace
    from experiments.output_metrics import method_metrics, update_detection
    payload = SimpleNamespace(arrays={'logits': np.array([[2., -1.], [3., 0.]]),
        'y': np.array([0, 0]), 'test_mask': np.array([True, True])})
    result = method_metrics(payload)
    assert result['f1'] == 1.0 and result['classification_auc'] is None
    assert result['classification_auc_status'] == 'missing_test_classes'
    assert update_detection(payload)['update_detection_auc_status'] == 'missing_original_predictions'


def test_matrix_runs_one_requested_method_without_inline_comparison(tables, monkeypatch):
    from experiments import run as matrix
    from experiments.target_direct_v1 import run_outputs as lane
    from experiments.modular_config import load_instance
    from experiments.modular_run import read_dataset, verified_selection
    from experiments.modular_model import prepare_model
    from utils.target_checkpoint import load_target_checkpoint
    reference = configs(tables)
    root = tables[0]
    data, inputs = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    selection = verified_selection(reference, store_root=root / 'v2', data=data, inputs=inputs)
    gu = load_instance(root / 'gu.yaml', 'unlearning')
    _, _, cp = prepare_model(gu, data=data, dataset_name=inputs.dataset_name,
        checkpoint_root=root / 'checkpoints', device=torch.device('cpu'), reference_directory=root)
    checkpoint = load_target_checkpoint(cp['path'], expected_file_sha256=cp['file_sha256'])
    cfg = {'name': 'cpu-matrix', 'dataset': inputs.dataset_name, 'base_model': 'GCN', 'ratio': .1,
           'methods': ['GNNDelete', 'Retrain'], 'strategies': ['degree'], 'seeds': [42],
           'unlearning_refs': ['gu.yaml', 'retrain.yaml'], '_source_path': str(root / 'matrix.yaml'),
           'run_root': str(root / 'matrix-results'), 'runtime_root': str(root / 'matrix-runtime'),
           'processed_root': str(root), 'defaults': {'run_collateral': False}}
    calls = []
    def cpu_cell(cfg, name, strategy, seed, artifact, *, output_dir, fingerprint, git_sha):
        calls.append(name)
        instance = load_instance(root / ('gu.yaml' if name == 'GNNDelete' else 'retrain.yaml'), 'unlearning')
        row = lane.execute_bound_method(instance=instance, selection=selection, data=data,
            dataset_name=inputs.dataset_name, checkpoint=checkpoint if name == 'GNNDelete' else None,
            store_root=root / 'v2', runtime_root=root / 'matrix-runtime')
        lane.save_method_result(row, store_root=root / 'v2', output_dir=output_dir, strategy=strategy,
                                meta={'config_fingerprint': fingerprint, 'method': name})
        return 'completed'
    monkeypatch.setattr(lane, 'execute_cell', cpu_cell)
    # Paths/data are a disposable CPU backend; the real matrix skip/dispatch and algorithms run.
    monkeypatch.setattr(matrix, '_content_fingerprint', lambda cfg, method, *_: 'cpu-' + method)
    monkeypatch.setattr(matrix, 'cache_v2_settings', lambda _: {'mode': 'fixture'})
    monkeypatch.setattr(matrix, '_record_autoreport_event', lambda **_: None)
    monkeypatch.setattr(matrix, 'prior_attempt_context', lambda *a, **k: (1, None))
    monkeypatch.setattr(lane, 'cell_instance', lambda cfg, name, seed:
                        load_instance(root / ('gu.yaml' if name == 'GNNDelete' else 'retrain.yaml'), 'unlearning'))
    artifact = {**reference, 'store_root': str(root / 'v2'), 'k': len(selection.selected_nodes),
                'target_checkpoint': cp}
    assert matrix.run_cell(cfg, 'GNNDelete', 'degree', 42, force=False, dry_run=False,
                           selection_artifact=artifact) == 'completed'
    assert calls == ['GNNDelete']
    assert not matrix.cell_dir(cfg, 'Retrain', 'degree', 42).exists()
    assert matrix.run_cell(cfg, 'Retrain', 'degree', 42, force=False, dry_run=False,
                           selection_artifact=artifact) == 'completed'
    assert calls == ['GNNDelete', 'Retrain']
    monkeypatch.setattr(lane, 'execute_cell', forbidden)
    for name in cfg['methods']:
        assert matrix.run_cell(cfg, name, 'degree', 42, force=False, dry_run=False,
                               selection_artifact=artifact) == 'skipped'
    changed = yaml.safe_load((root / 'gu.yaml').read_text())
    changed['parameters']['unlearn_lr'] = gu['parameters']['unlearn_lr'] * 2
    write_yaml(root / 'gu.yaml', changed)
    with pytest.raises(ValueError, match='method conditions'):
        matrix.run_cell(cfg, 'GNNDelete', 'degree', 42, force=False, dry_run=False,
                        selection_artifact=artifact)
    with pytest.raises(ValueError, match='post-processing'):
        matrix.run_cell({**cfg, 'defaults': {'run_collateral': True}}, 'GNNDelete', 'degree', 42,
                        force=False, dry_run=False, selection_artifact=artifact)
