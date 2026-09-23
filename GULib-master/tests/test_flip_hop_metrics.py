"""Hand-authored CPU Outputs: no training, GU execution or forward, even at setup."""
import copy
import functools
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import torch

from test_modular_consumers import tables, run, write_yaml
from experiments.flip_hop_metrics import exact_retrain, flip_hop, hop_groups
from experiments.modular_evaluation import evaluate_modular, resolve_evaluation


def evaluation(case='post_unlearning_flip_hop', **kwargs):
    return resolve_evaluation(dict(kind='evaluation', schema_version=1, case=case, **kwargs))


def hand_pair():
    # 0--1--2--3--4; 5 isolated; 6--7. Delete 0 and 6.
    identity = {'target': {'method': 'GIF'}, 'selection': {'artifact_id': 'selection'},
        'pairing': {'evaluation_graph_identity': {'graph': 'prediction'}, 'training': {'seed': 7}},
        'dataset_input': {'graph': 'original'}, 'graph_fingerprint': 'original'}
    arrays = {'edge_index': np.array([[1, 1, 3, 3, 7], [0, 2, 2, 4, 6]]),
        'evaluation_edge_index': np.empty((2, 0), dtype=np.int64),
        'test_mask': np.ones(8, dtype=bool), 'retain_mask': np.zeros(8, dtype=bool),
        'selected_nodes': np.array([0, 6]), 'y': np.zeros(8, dtype=np.int64),
        'logits': np.array([[0., 1.], [0., 1.], [1., 0.], [0., 1.],
                            [1., 0.], [0., 1.], [0., 1.], [1., 0.]])}
    gu = SimpleNamespace(identity=identity, arrays=arrays)
    rt = copy.deepcopy(gu)
    rt.identity['target']['method'] = 'Retrain'
    rt.arrays['logits'][:] = [1., 0.]
    return gu, rt


def test_hand_calculated_mask_hops_disconnected_and_counts():
    gu, rt = hand_pair()
    metrics, protocol = flip_hop(gu, rt)
    assert metrics == {'node_count': 6, 'flipped_count': 3, 'fraction_flipped': .5,
        '1_hop_count': 2, '1_hop_flipped_count': 1, '1_hop_flip_rate': .5,
        '2_hop_count': 1, '2_hop_flipped_count': 0, '2_hop_flip_rate': 0.,
        '3_hop_count': 1, '3_hop_flipped_count': 1, '3_hop_flip_rate': 1.,
        'gt3_hop_count': 2, 'gt3_hop_flipped_count': 1, 'gt3_hop_flip_rate': .5}
    assert sum(metrics[h + '_hop_count'] for h in ('1', '2', '3', 'gt3')) == metrics['node_count']
    assert sum(metrics[h + '_hop_flipped_count'] for h in ('1', '2', '3', 'gt3')) == metrics['flipped_count']
    assert protocol['hop_graph'] == 'bound_pre_deletion_edge_index'
    # Retained prediction graph has no edges: using it for hops would fail this test.
    np.testing.assert_array_equal(hop_groups(gu.arrays['edge_index'], np.array([0, 6]), 8), [0,1,2,3,4,4,0,1])


def test_empty_groups_and_empty_evaluation_are_null():
    gu, rt = hand_pair()
    gu.arrays['test_mask'][:] = False
    gu.arrays['test_mask'][1] = True
    metrics, _ = flip_hop(gu, rt)
    assert metrics['fraction_flipped'] == 1
    for label in ('2', '3', 'gt3'):
        assert metrics[label + '_hop_count'] == metrics[label + '_hop_flipped_count'] == 0
        assert metrics[label + '_hop_flip_rate'] is None
    gu.arrays['test_mask'][:] = False
    metrics, _ = flip_hop(gu, rt)
    assert metrics['node_count'] == metrics['flipped_count'] == 0
    assert metrics['fraction_flipped'] is None
    json.dumps(metrics, allow_nan=False)


@pytest.mark.parametrize('field', ['selection', 'dataset_input', 'graph_fingerprint',
    'training', 'evaluation_graph_identity', 'model', 'selected_nodes', 'data_identity', 'deletion'])
def test_pair_identity_mismatch_rejected(field):
    gu, rt = hand_pair()
    if field in ('selection', 'dataset_input', 'graph_fingerprint'):
        rt.identity[field] = 'wrong'
    else:
        rt.identity['pairing'][field] = 'wrong'
    with pytest.raises(ValueError, match='exactly one verified Retrain'):
        exact_retrain(gu, [({'artifact_id': 'rt'}, rt)])


@pytest.mark.parametrize('field', ['y', 'selected_nodes', 'test_mask', 'edge_index', 'evaluation_edge_index', 'logits'])
def test_resolved_input_mismatch_rejected(field):
    gu, rt = hand_pair()
    rt.arrays[field] = rt.arrays[field][:-1]
    with pytest.raises(ValueError, match='differ'):
        exact_retrain(gu, [({'artifact_id': 'rt'}, rt)])


@pytest.mark.parametrize('count', [0, 2])
def test_missing_and_duplicate_retrain_rejected(count):
    gu, rt = hand_pair()
    with pytest.raises(ValueError, match='exactly one verified Retrain'):
        exact_retrain(gu, [({'artifact_id': 'rt'}, rt)] * count)


def forbidden(*args, **kwargs):
    raise AssertionError('training, producer or forward called in Metrics-only test')


@pytest.fixture
def no_compute(monkeypatch):
    import experiments.modular_model as model
    import experiments.modular_gu as gu
    import experiments.modular_run as entry
    for name in ('train_supervised', 'prepare_model'):
        original = getattr(model, name)
        monkeypatch.setattr(model, name, functools.wraps(original)(lambda *a, **k: forbidden()))
    monkeypatch.setattr(entry, 'prepare_model', forbidden)
    monkeypatch.setattr(entry, 'resolve_methods', forbidden)
    # Preserve source identity with __wrapped__; do not fake gu_producer or load_output.
    for name, original in gu.GU_METHODS.items():
        monkeypatch.setitem(gu.GU_METHODS, name, functools.wraps(original)(lambda *a, **k: forbidden()))
    monkeypatch.setattr(torch.optim.Adam, 'step', forbidden)
    monkeypatch.setattr(torch.optim.SGD, 'step', forbidden)
    hook = torch.nn.modules.module.register_module_forward_pre_hook(forbidden)
    yield
    hook.remove()


def tree_hash(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


@pytest.fixture
def persisted(tables, no_compute):
    from cache_v2 import ArtifactRecipe, ArtifactType, ProducerVersion
    from cache_v2.store import ArtifactStore
    from cache_v2.unlearning_output import OUTPUT_CONTRACT, UnlearningOutputPayload
    from experiments.artifact_producer import FormalArtifactRequest, store_formal_artifact
    from experiments.dataset_inputs import bind_input, read_dataset
    from experiments.modular_config import load_instance
    from experiments.modular_gu import gu_producer
    from experiments.node_deletion import pairing_identity
    from experiments.unlearning_outputs import output_reference
    root = tables[0]
    dataset = load_instance(root / 'dataset.yaml', 'dataset_split')
    data, inputs = read_dataset(dataset, root)
    instance = load_instance(root / 'gu.yaml', 'unlearning')
    store_root = root / 'results/cache_v2'
    store = ArtifactStore(store_root, producer_version=ProducerVersion('hand-fixture', 'v1'))
    store.initialize()
    selection_recipe = ArtifactRecipe({'artifact_kind': 'selection',
        'topology_fingerprint': inputs.graph_fingerprint,
        'candidate_set_hash': inputs.candidate_set_hash, 'node_id_space': 'pyg-global-node-index-v1',
        'selector': 'degree', 'selector_algorithm_version': 'hand-fixture',
        'selection_rule': 'topk_desc', 'k': 1})
    selected = store.store_selection(selection_recipe, [9], num_nodes=data.num_nodes,
        candidate_nodes=tuple(range(10)), compute_seconds=0.)
    references = []
    for method in ('GNNDelete', 'Retrain'):
        producer = gu_producer(method, instance['model'])
        identity = {'dataset_input': bind_input(dataset, root, root),
            'target': {'method': method, 'parameters': {}},
            'pairing': pairing_identity(instance, data, [9]),
            'selection': output_reference(selected, selection_recipe.recipe_hash),
            'graph_fingerprint': inputs.graph_fingerprint, 'producer_version': producer.to_dict()}
        logits = np.tile([2., 0.], (20, 1))
        if method == 'GNNDelete':
            logits[[0, 15, 16, 19]] = [0., 2.]
        arrays = {'logits': logits, 'selected_nodes': np.array([9])}
        if method != 'Retrain':
            arrays['logits_before'] = np.tile([2., 0.], (20, 1))
        payload = UnlearningOutputPayload(identity, arrays, {'synthetic_fixture_tensor': np.zeros(1)}, {})
        recipe = ArtifactRecipe({'artifact_contract': OUTPUT_CONTRACT, **identity})
        stored = store_formal_artifact(store_root, FormalArtifactRequest(ArtifactType.PREDICTION, recipe, producer), payload)
        reference = output_reference(stored, recipe.recipe_hash)
        references.append(reference)
        # Completed source documents, explicitly synthetic. Real reader checks all digests.
        folder = root / ('source-' + method)
        folder.mkdir()
        selection_doc = {'cell_id': method, 'selection_id': selected.artifact_id,
                         'requested_k': 1, 'selected_nodes': [9]}
        cell_folder = folder / 'cells' / method
        cell_folder.mkdir(parents=True)
        selection_file = cell_folder / 'selection.json'
        selection_file.write_text(json.dumps(selection_doc))
        source = {'experiment_id': 'hand-fixture', 'run_id': method, 'generated_at': 'fixture',
            'commit': 'synthetic-no-training', 'config_path': 'fixture.yaml', 'stage': 'unlearning',
            'status': 'completed', 'cells': [{'cell_id': method, 'path': 'cells/' + method, 'conditions': {
                'method': method, 'selector': 'degree', 'model': instance['model']['architecture'],
                'seed': instance['training']['seed'], 'dataset_index': 0, 'dataset_name': 'cpu_fixture',
                'budget_ratio': None, 'budget': {'mode': 'k', 'value': 1}}, 'status': 'completed',
                'files': {'selection.json': {'sha256': hashlib.sha256(selection_file.read_bytes()).hexdigest()}},
                'results': {'selection': 'completed', 'metrics': 'not_requested', 'scores': 'not_requested'},
                'output': reference, 'selection_id': selected.artifact_id}]}
        (folder / 'run.json').write_text(json.dumps(source))
    for name, case in (('flip', 'post_unlearning_flip_hop'), ('single', 'post_method_metrics'),
                       ('gap', 'post_unlearning_utility_and_retrain_gap')):
        write_yaml(root / (name + '.yaml'), dict(kind='evaluation', schema_version=1, case=case))
    return root, references


def sources(root):
    return [{'run': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(root.glob('source-*/run.json'))]


def test_metrics_entry_export_readback_and_original_evaluations(persisted, tables, record_property):
    from experiments.modular_artifacts import read_run
    root, references = persisted
    before = tree_hash(root / 'results/cache_v2')
    inputs_before = {p: (root / p).read_bytes() for p in ('graph.pkl', 'dataset.json')}
    previous = evaluate_modular(evaluation('post_method_metrics'), references,
        store_root=root / 'results/cache_v2', dataset_root=root)
    result = run(tables, 'combined', stage='metrics', selector_refs=[], output_inputs=sources(root),
        evaluation_refs=['single.yaml', 'utility.yaml', 'gap.yaml', 'flip.yaml'])
    assert result['evaluations'][0]['rows'] == previous['rows']
    flip = result['evaluations'][3]['rows'][0]
    assert flip['metrics']['fraction_flipped'] == .6  # 3/5 test nodes, not 1/9 retained train nodes.
    assert flip['metrics']['gt3_hop_count'] == 5
    assert flip['metrics']['1_hop_flip_rate'] is None
    assert result['evaluations'][2]['rows'][0]['metrics']['gap'] == pytest.approx(-.2)
    only = run(tables, 'flip-only', stage='metrics', selector_refs=[], output_inputs=sources(root),
        evaluation_refs=['flip.yaml'])
    assert only['evaluations'][0]['rows'][0] == flip
    path = root / 'results/runs/flip-only/flip-only/run.json'
    exported, docs = read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())
    assert len(exported['cells']) == 1
    row = docs[0]['metrics.json']['rows'][0]
    assert row['values'] == flip['metrics'] and row['identity'] == flip['identity']
    assert row['evaluation_receipt_id'] == flip['evaluation_receipt_id']
    assert row['baseline_output'] == references[1]
    combined_path = root / 'results/runs/combined/combined/run.json'
    combined, documents = read_run(combined_path, hashlib.sha256(combined_path.read_bytes()).hexdigest())
    assert len(combined['cells']) == 2
    assert before == tree_hash(root / 'results/cache_v2')
    assert inputs_before == {p: (root / p).read_bytes() for p in inputs_before}
    record_property('flip_hop_evidence', json.dumps({'fixture': 'hand-authored-no-training',
        'training_gu_forward_forbidden': True, 'artifacts_unchanged': True,
        'combined_cells': len(combined['cells']), 'paired_only_cells': 1, 'exported': row}))


def test_explicit_pair_cli_does_not_overwrite_flip(persisted):
    from eval_collateral import evaluate_outputs
    root, refs = persisted
    result = evaluate_outputs(evaluation(), [{'strategy': 'fixture', 'unlearning': refs[0], 'retrain': refs[1]}],
        store_root=root / 'results/cache_v2', dataset_root=root, output_dir=root / 'cli')
    assert result['results'][0]['fraction_flipped'] == .6
    assert result == json.loads((root / 'cli/collateral.json').read_text())
    assert 'mean_pred_shift' not in result['results'][0]


def test_receipt_tracks_mask_graph_rules_version_and_requested_metrics(persisted, monkeypatch):
    from experiments.unlearning_outputs import load_output
    import experiments.flip_hop_metrics as module
    root, refs = persisted
    kwargs = dict(store_root=root / 'results/cache_v2', dataset_root=root)
    original = evaluate_modular(evaluation(), refs, **kwargs)['rows'][0]
    smaller = evaluate_modular(evaluation(metrics=['fraction_flipped']), refs, **kwargs)['rows'][0]
    assert smaller['evaluation_receipt_id'] != original['evaluation_receipt_id']
    gu, rt = [load_output(ref, **kwargs) for ref in refs]
    _, protocol = flip_hop(gu, rt)
    gu.arrays['test_mask'] = gu.arrays['test_mask'].copy()
    gu.arrays['test_mask'][0] = True
    assert flip_hop(gu, rt)[1]['evaluation_mask_sha256'] != protocol['evaluation_mask_sha256']
    gu.identity = copy.deepcopy(gu.identity)
    gu.identity['graph_fingerprint'] = 'new-graph'
    assert flip_hop(gu, rt)[1]['graph_fingerprint'] != protocol['graph_fingerprint']
    monkeypatch.setattr(module, 'implementation_fingerprint', lambda *args: 'changed-implementation')
    assert evaluate_modular(evaluation(), refs, **kwargs)['rows'][0]['evaluation_receipt_id'] != original['evaluation_receipt_id']


def test_real_loader_digest_rejection_and_missing_duplicate_pair(persisted):
    root, refs = persisted
    kwargs = dict(store_root=root / 'results/cache_v2', dataset_root=root)
    for candidates in ([refs[0]], [refs[0], refs[1], refs[1]]):
        with pytest.raises(ValueError, match='exactly one verified Retrain'):
            evaluate_modular(evaluation(), candidates, **kwargs)
    with pytest.raises(ValueError, match='digest mismatch'):
        evaluate_modular(evaluation(), [refs[0], {**refs[1], 'content_hash': '0' * 64}], **kwargs)


def test_public_configuration_dry_run():
    from experiments.modular_run import execute
    root = Path(__file__).resolve().parents[1]
    planned = execute(root / 'experiments/configs/flip_hop_metrics.template.yaml', dry_run=True)
    assert planned['producer_called'] is False
    assert planned['effective_evaluations'][-1]['case'] == 'post_unlearning_flip_hop'


def test_paired_case_cannot_execute_in_unlearning_stage(persisted, tables):
    with pytest.raises(ValueError, match='independent metrics stage'):
        run(tables, 'invalid-stage', stage='unlearning', selector_refs=['degree.yaml'],
            unlearning_refs=['gu.yaml'], evaluation_refs=['flip.yaml'])


def test_corrupt_bound_dataset_fails_closed(persisted):
    root, refs = persisted
    # Only this disposable fixture is changed, never a historical input.
    graph = root / 'graph.pkl'
    graph.write_bytes(graph.read_bytes() + b'fixture-corruption')
    with pytest.raises(ValueError, match='graph digest mismatch'):
        evaluate_modular(evaluation(), refs, store_root=root / 'results/cache_v2', dataset_root=root)


def test_export_rejects_metric_identity_tampering(persisted, tables):
    from experiments.modular_artifacts import read_run
    root, _ = persisted
    run(tables, 'tamper-export', stage='metrics', selector_refs=[], output_inputs=sources(root),
        evaluation_refs=['flip.yaml'])
    path = root / 'results/runs/tamper-export/tamper-export/run.json'
    document = json.loads(path.read_text())
    cell = document['cells'][0]
    metrics_file = path.parent / cell['path'] / 'metrics.json'
    metrics = json.loads(metrics_file.read_text())
    metrics['rows'][0]['identity']['protocol']['grouping'] = 'wrong'
    metrics_file.write_text(json.dumps(metrics))
    cell['files']['metrics.json']['sha256'] = hashlib.sha256(metrics_file.read_bytes()).hexdigest()
    path.write_text(json.dumps(document))
    with pytest.raises(ValueError, match='metric identity mismatch'):
        read_run(path, hashlib.sha256(path.read_bytes()).hexdigest())


def test_collector_acceptance_and_flat_result_projection(persisted, tables):
    from experiments.modular_config import configuration_fingerprint
    from scripts.syncmate.opengu_acceptance import acceptance_payload
    from scripts.syncmate.opengu_results import _run_results
    root, _ = persisted
    run(tables, 'collected', stage='metrics', selector_refs=[], output_inputs=sources(root),
        evaluation_refs=['single.yaml', 'flip.yaml'])
    path = root / 'results/runs/collected/collected/run.json'
    document = json.loads(path.read_text())
    paths = [path] + [path.parent / cell['path'] / name
                     for cell in document['cells'] for name in cell['files']]
    items = [{'remote_path': p.relative_to(root).as_posix(), 'local_path': p.relative_to(root).as_posix(),
              'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
    index = {'peers': {'fixture': {'summary': {'status': 'verified'},
        'remote': {'git': {'sha': document['commit']}}, 'items': items}}}
    definition = {'expected_artifact_paths': [i['remote_path'] for i in items],
        'config_path': 'collected.yaml', 'configuration_fingerprint': configuration_fingerprint(root / 'collected.yaml'),
        'stage': 'metrics', 'run_identity': {'run_id': 'collected', 'experiment_id': 'collected'},
        'expected_cells': [{k: c[k] for k in ('cell_id', 'path', 'conditions')} for c in document['cells']],
        'expected_datasets': [{'num_nodes': 20, 'candidate_count': 10}]}
    context = {'node_id': 'fixture', 'artifact_index': index, 'expected_git_sha': document['commit'], 'project_root': root}
    acceptance = acceptance_payload('modular-output-v1', definition, context)
    assert acceptance['passed'], acceptance
    rows, errors, _ = _run_results(index, root, [])
    assert not errors and len(rows) == 2
    gu = next(row for row in rows if row['method'] == 'GNNDelete')
    assert gu['fraction_flipped'] == .6 and gu['gt3_hop_flipped_count'] == 3
    assert gu['1_hop_flip_rate'] is None
    rt = next(row for row in rows if row['method'] == 'Retrain')
    assert 'fraction_flipped' not in rt and 'accuracy' in rt
