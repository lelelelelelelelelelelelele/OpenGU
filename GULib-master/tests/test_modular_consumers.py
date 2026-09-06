"""Real CPU consumers and immutable temporary Stores for AAGU-026."""
import copy
import json
import pickle
from pathlib import Path

import pytest
import torch
import yaml
from torch_geometric.data import Data
from experiments.modular_run import execute
from experiments.modular_config import gu_defaults
from experiments.modular_execution import ExecutionContext, project_context
from utils.target_checkpoint import data_identity, sha256_file


def write_yaml(path, value):
    # Disposable tables explicitly bind disposable files, never public datasets.
    if value.get('kind') == 'experiment':
        value = copy.deepcopy(value)
        if 'dataset_ref' in value:
            value['dataset_ref'] = str((path.parent / value['dataset_ref']).resolve())
        for field in ('selector_refs', 'unlearning_refs', 'evaluation_refs'):
            if field in value:
                value[field] = [str((path.parent / ref).resolve()) for ref in value[field]]
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding='utf-8')


@pytest.fixture
def tables(tmp_path, record_property):
    torch.set_num_threads(1)
    torch.manual_seed(7)
    n = 20
    edges = torch.stack([torch.arange(n-1), torch.arange(1, n)])
    data = Data(x=torch.randn(n, 3), y=torch.arange(n) % 2,
        edge_index=torch.cat([edges, edges.flip(0)], dim=1),
        train_mask=torch.arange(n) < 10, val_mask=(torch.arange(n) >= 10) & (torch.arange(n) < 15),
        test_mask=torch.arange(n) >= 15)
    data_file = tmp_path / 'graph.pkl'
    data_file.write_bytes(pickle.dumps(data))
    dataset = {'kind': 'dataset_split', 'schema_version': 1,
        'dataset': {'name': 'cpu_fixture'}, 'preprocessing': {'adapter': 'OpenGU_persisted_processed_pair'},
        'split': {'profile': 'fixture', 'train_ratio': 0.5, 'val_ratio': 0.25, 'test_ratio': 0.25, 'seed': 7}}
    manifest = {k: dataset[k] for k in ('dataset', 'preprocessing', 'split')}
    manifest.update(schema='opengu.persisted_dataset_split', version=1, data_path='graph.pkl',
                    data_sha256=sha256_file(data_file), data_identity=data_identity(data))
    manifest_file = tmp_path / 'dataset.json'
    manifest_file.write_text(json.dumps(manifest), encoding='utf-8')
    dataset['artifacts'] = {'manifest': 'dataset.json', 'manifest_sha256': sha256_file(manifest_file),
        'split_hash': data_identity(data)['split_hash'], 'node_id_space': 'pyg-global-node-index-v1'}
    write_yaml(tmp_path / 'dataset.yaml', dataset)
    model = {'architecture': 'OpenGU.GCNNet', 'hidden_channels': 4}
    training = {'epochs': 3}
    selector = {'kind': 'selector', 'schema_version': 1, 'method': 'degree',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 1}}
    write_yaml(tmp_path / 'degree.yaml', selector)
    for name in ('b_param_hutch', 'tracin_cp_point_3', 'r_point', 'legacy'):
        write_yaml(tmp_path / (name + '.yaml'), {**selector, 'method': name, 'model': model, 'training': training})
    gu = {'kind': 'unlearning', 'schema_version': 1, 'method': 'GNNDelete', 'model': model,
          'training': training, 'parameters': {'unlearning_epochs': 2}}
    write_yaml(tmp_path / 'gu.yaml', gu)
    write_yaml(tmp_path / 'utility.yaml', {'kind': 'evaluation', 'schema_version': 1,
        'case': 'post_unlearning_utility'})
    experiment = {'kind': 'experiment', 'schema_version': 1, 'experiment_id': 'cold', 'stage': 'selector',
        'dataset_ref': 'dataset.yaml', 'selector_refs': ['degree.yaml', 'b_param_hutch.yaml', 'tracin_cp_point_3.yaml'],
        'matrix': 'cartesian_product'}
    yield tmp_path, experiment, gu
    runs = [json.loads(path.read_text(encoding='utf-8')) for path in sorted(tmp_path.glob('*.json'))]
    record_property('consumer_runs', json.dumps([run for run in runs if isinstance(run, dict) and run.get('schema') == 'opengu.modular_run']))


def run(tables, name, **changes):
    root, base, _ = tables
    config = copy.deepcopy(base)
    config.update(changes)
    config['experiment_id'] = name
    write_yaml(root / (name + '.yaml'), config)
    context = ExecutionContext(run_id=name, level='verification', request_device='cpu',
        store_root=root / 'v2', checkpoint_root=root / 'checkpoints',
        runtime_root=root / 'runtime' / name, output=root / (name + '.json'),
        executor='pytest')
    return execute(root / (name + '.yaml'), context=context)


def identities(result):
    return [(x['score']['recipe_hash'], x['selection']['artifact']['artifact_id']) for x in result['selectors']]


def test_method_cold_warm_and_hutch_isolation(tables, record_property):
    cold = run(tables, 'cold')
    warm = run(tables, 'different_experiment')
    assert identities(cold) == identities(warm)
    assert all(not x['score']['hit'] and x['score']['producer_called'] for x in cold['selectors'])
    assert all(x['score']['hit'] and x['selection']['cache']['hit'] for x in warm['selectors'])
    root = tables[0]
    b = yaml.safe_load((root / 'b_param_hutch.yaml').read_text())
    b['parameters'] = {'hutchinson': {'probes': 2}}
    write_yaml(root / 'b_param_hutch.yaml', b)
    changed = run(tables, 'hutch2')
    assert [x['score']['hit'] for x in changed['selectors']] == [True, False, True]
    assert [x['selection']['cache']['hit'] for x in changed['selectors']] == [True, False, True]
    record_property('method_change_matrix', json.dumps([x['score'] for x in changed['selectors']]))


def test_real_gu_consumes_existing_selection_without_producer(tables, monkeypatch, record_property):
    cold = run(tables, 'selection_only', selector_refs=['degree.yaml'])
    import functools
    from experiments.target_direct_v1 import methods
    @functools.wraps(methods.METHODS['degree'])
    def forbidden(*args, **kwargs):
        raise AssertionError('cached Selection-to-GU recomputed degree scores')
    monkeypatch.setitem(methods.METHODS, 'degree', forbidden)
    first = run(tables, 'gu_cold', selector_refs=['degree.yaml'], stage='unlearning', unlearning_refs=['gu.yaml'])
    second = run(tables, 'gu_warm', selector_refs=['degree.yaml'], stage='unlearning', unlearning_refs=['gu.yaml'])
    assert first['selector_producer_called'] is False
    assert first['unlearning'][0]['hit'] is False
    assert second['unlearning'][0]['hit'] is True
    root, _, gu = tables
    gu['parameters']['unlearn_lr'] = 0.02
    write_yaml(root / 'gu.yaml', gu)
    changed = run(tables, 'gu_lr002', selector_refs=['degree.yaml'], stage='unlearning', unlearning_refs=['gu.yaml'])
    assert changed['unlearning'][0]['recipe_hash'] != first['unlearning'][0]['recipe_hash']
    assert changed['unlearning'][0]['producer_called'] is True
    record_property('real_gu', json.dumps([first['unlearning'][0], second['unlearning'][0], changed['unlearning'][0]]))


def test_default_expansion_and_budget_reuse(tables):
    from experiments.target_direct_v1.methods import parameter_defaults
    cold = run(tables, 'default_cold', selector_refs=['b_param_hutch.yaml'])
    root = tables[0]
    b = yaml.safe_load((root / 'b_param_hutch.yaml').read_text())
    b['parameters'] = parameter_defaults('b_param_hutch')
    write_yaml(root / 'renamed.yaml', b)
    explicit = run(tables, 'explicit', selector_refs=['renamed.yaml'])
    assert identities(cold) == identities(explicit)
    assert explicit['selectors'][0]['score']['hit']
    b['budget']['value'] = 2
    write_yaml(root / 'renamed.yaml', b)
    budget = run(tables, 'budget2', selector_refs=['renamed.yaml'])
    assert budget['selectors'][0]['score']['hit'] is True
    assert budget['selectors'][0]['selection']['cache']['hit'] is False
    assert budget['selectors'][0]['selection']['artifact_k'] == 2


def test_missing_and_wrong_identity_fail_before_execution(tables):
    cold = run(tables, 'selection', selector_refs=['degree.yaml'])
    reference = {k: cold['selectors'][0]['selection']['artifact'][k] for k in ('artifact_id', 'recipe_hash', 'content_hash')}
    reference['content_hash'] = '0' * 64
    from experiments.modular_run import read_dataset, verified_selection
    from experiments.modular_config import load_instance
    root = tables[0]
    data, inputs = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    with pytest.raises(ValueError, match='digest mismatch'):
        verified_selection(reference, store_root=root / 'v2', data=data, inputs=inputs)
    assert not (root / 'runtime/unlearning').exists()



def test_real_gu_method_and_default_equivalence(tables):
    root, _, gu = tables
    first = run(tables, 'combined', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['gu.yaml'])
    effective_defaults = gu_defaults('GNNDelete')
    gu['parameters'] = {**effective_defaults, 'unlearning_epochs': 2}
    write_yaml(root / 'explicit_gu.yaml', gu)
    explicit = run(tables, 'gu_explicit_run', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['explicit_gu.yaml'])
    assert identities(first) == identities(explicit)
    assert explicit['unlearning'][0]['hit'] is True
    gu['method'] = 'GIF'
    gu['parameters'] = {'iteration': 2}
    write_yaml(root / 'gif.yaml', gu)
    gif = run(tables, 'gif_run', stage='unlearning', selector_refs=['degree.yaml'], unlearning_refs=['gif.yaml'])
    assert identities(first) == identities(gif)
    assert gif['selectors'][0]['score']['hit'] is True
    assert gif['unlearning'][0]['hit'] is False
    assert gif['unlearning'][0]['recipe_hash'] != first['unlearning'][0]['recipe_hash']


def test_different_selector_and_gu_backbones(tables):
    root = tables[0]
    selector = yaml.safe_load((root / 'r_point.yaml').read_text())
    selector['model'] = {'architecture': 'OpenGU.SGCNet'}
    selector['parameters'] = {'lissa': {'iterations': 2}}
    write_yaml(root / 'sgc.yaml', selector)
    result = run(tables, 'sgc_to_gcn', selector_refs=['sgc.yaml'], stage='unlearning', unlearning_refs=['gu.yaml'])
    assert result['selectors'][0]['checkpoint']['state_hash'] != result['unlearning'][0]['checkpoint']['state_hash']
    assert result['unlearning'][0]['producer_called']


def test_command_requires_context_and_gu_reuses_declared_selection(tables):
    import subprocess
    import sys
    root, config, _ = tables
    config['selector_refs'] = ['degree.yaml']
    command = [sys.executable, '-B', '-X', 'utf8', 'experiments/run.py', str(root / 'entry.yaml')]
    repository = Path(__file__).resolve().parents[1]
    write_yaml(root / 'entry.yaml', config)
    dry = subprocess.run(command + ['--dry_run'], cwd=repository, capture_output=True, text=True)
    assert dry.returncode == 0, dry.stdout + dry.stderr
    assert not (root / 'v2').exists()
    first = subprocess.run(command, cwd=repository, capture_output=True, text=True)
    assert first.returncode != 0
    result = run(tables, 'entry-selection', selector_refs=['degree.yaml'])
    config.update(stage='unlearning', unlearning_refs=['gu.yaml'])
    write_yaml(root / 'entry.yaml', config)
    result = run(tables, 'gu-entry', stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml'])
    assert result['selector_producer_called'] is False
    assert result['unlearning'][0]['producer_called'] is True


@pytest.mark.parametrize('bad', [{'unknown': 1}, {'hutchinson': {'probes': True}}, {'lissa': {'scale': float('nan')}}])
def test_invalid_method_configuration_fails_before_store(tables, bad):
    root = tables[0]
    item = yaml.safe_load((root / 'b_param_hutch.yaml').read_text())
    item['parameters'] = bad
    write_yaml(root / 'b_param_hutch.yaml', item)
    with pytest.raises(ValueError):
        run(tables, 'invalid')
    assert not (root / 'v2').exists()


def test_all_seventeen_methods_match_pre_refactor_formulas(tables, record_property):
    from experiments.modular_config import load_instance, resolve_budget
    from experiments.modular_model import prepare_model
    from experiments.modular_run import read_dataset
    from experiments.target_direct_v1.method_cache import resolve_methods
    from experiments.target_direct_v1.methods import SCORE_NAMES, resolve_parameters
    from experiments.c_target_v1.core import checkpoint_point_gradients, inverse_hessian_target, deployed_cross_gradient_scores
    from experiments.target_direct_v1.scoring import (checkpoint_graph_scores, checkpoint_view_indices,
        degree_scores, deterministic_random_scores, inverse_hessian_vectors,
        hutchinson_parameter_change_scores, weighted_checkpoint_scores)
    root = tables[0]
    data, inputs = read_dataset(load_instance(root / 'dataset.yaml', 'dataset_split'), root)
    instance = load_instance(root / 'r_point.yaml', 'selector')
    instance['training']['epochs'] = 6
    model, checkpoints, _ = prepare_model(instance, data=data, dataset_name=inputs.dataset_name,
        checkpoint_root=root / 'checkpoints', device=torch.device('cpu'), reference_directory=root)
    candidates, targets = data.train_mask.nonzero().flatten(), data.val_mask.nonzero().flatten()
    lissa = dict(iterations=2, scale=25., damp=.01)
    points = [checkpoint_point_gradients(model, data, state=item['state'], candidate_ids=candidates,
        target_ids=targets, parameter_scope='last_layer') for item in checkpoints]
    inverse = inverse_hessian_target(model, data, state=checkpoints[-1]['state'], hessian_train_ids=candidates,
        target_ids=targets, parameter_scope='last_layer', **lissa)[1]
    graph = checkpoint_graph_scores(model, data, checkpoints=checkpoints, candidate_ids=candidates,
        source_ids=candidates, target_gradients=[p[1] for p in points], parameter_scope='last_layer',
        affected_hops=2, final_inverse_target=inverse)
    matrix = points[-1][0]
    probes = torch.randint(0, 2, (2, matrix.shape[1]), generator=torch.Generator().manual_seed(1729)).to(matrix.dtype).mul(2).sub(1)
    inverse_probes = inverse_hessian_vectors(model, data, state=checkpoints[-1]['state'],
        hessian_train_ids=candidates, parameter_scope='last_layer', vectors=probes, **lissa)[0]
    expected = dict(a_grad_norm=matrix.norm(dim=1), b_param_hutch=hutchinson_parameter_change_scores(matrix, inverse_probes),
        degree=degree_scores(data.edge_index, candidates, data.num_nodes), random=deterministic_random_scores(len(candidates), 104245),
        r_point=matrix.mv(inverse), p_point=matrix.mv(points[-1][1]), legacy=deployed_cross_gradient_scores(matrix),
        **graph['final_scores'])
    views = checkpoint_view_indices(len(checkpoints))
    for source, vectors in [('point', [m.mv(t).to(torch.float64) for m,t in points]),
                            ('simple', graph['simple_vectors']), ('graph', graph['graph_vectors'])]:
        for suffix, view in [('3','cp3'), ('6','cp_all')]:
            expected['tracin_cp_' + source + '_' + suffix] = weighted_checkpoint_scores(vectors,
                [item['update_lr'] for item in checkpoints], views[view])
    selectors = []
    for name in SCORE_NAMES:
        p = resolve_parameters(name)
        if 'lissa' in p:
            p['lissa'] = lissa
        if 'hutchinson' in p:
            p['hutchinson']['probes'] = 2
        selectors.append({'method':name, 'parameters':p, 'budget':resolve_budget({'mode':'k','value':1},len(candidates))})
    kwargs = dict(store_root=root/'v2', data=data, dataset_name=inputs.dataset_name, model=model,
        checkpoints=checkpoints, selectors=selectors, model_config=instance['model'], training=instance['training'])
    cold = resolve_methods(**kwargs)
    warm = resolve_methods(**kwargs, fail_if_score_called=True, fail_if_selection_called=True)
    errors = {}
    for name in SCORE_NAMES:
        actual = torch.tensor(cold[name]['scores'], dtype=torch.float64)
        torch.testing.assert_close(actual, expected[name].to(torch.float64), rtol=1e-6, atol=1e-9)
        errors[name] = float((actual-expected[name]).abs().max())
        assert not cold[name]['score']['hit'] and warm[name]['score']['hit']
    assert len({item['score']['recipe_hash'] for item in cold.values()}) == 17
    record_property('seventeen_method_max_abs_error', json.dumps(errors))


def gu_reason_once_variant(self, data):
    return ORIGINAL_REASON_ONCE(self, data)


def degree_implementation_variant(c, p):
    from experiments.target_direct_v1.methods import score_degree
    return score_degree(c, p) + 1


def test_actual_dependency_implementation_changes(tables, monkeypatch):
    import experiments.target_direct_v1.methods as methods
    from model.base_gnn.gcn import GCNNet
    global ORIGINAL_REASON_ONCE
    ORIGINAL_REASON_ONCE = GCNNet.reason_once
    root, _, gu = tables
    gu['method'], gu['parameters'] = 'GIF', {'iteration': 2}
    write_yaml(root / 'gif.yaml', gu)
    kwargs = dict(selector_refs=['degree.yaml', 'b_param_hutch.yaml'], stage='unlearning', unlearning_refs=['gif.yaml'])
    first = run(tables, 'code_cold', **kwargs)
    monkeypatch.setattr(GCNNet, 'reason_once', gu_reason_once_variant)
    changed = run(tables, 'gu_code_changed', **kwargs)
    assert identities(first) == identities(changed)
    assert all(x['score']['hit'] for x in changed['selectors'])
    assert all(x['producer_called'] for x in changed['unlearning'])
    assert all(a['recipe_hash'] != b['recipe_hash'] for a,b in zip(first['unlearning'], changed['unlearning']))
    monkeypatch.setitem(methods.METHODS, 'degree', degree_implementation_variant)
    related = run(tables, 'selector_code_changed', selector_refs=['degree.yaml', 'b_param_hutch.yaml'])
    assert [x['score']['hit'] for x in related['selectors']] == [False, True]
    monkeypatch.setattr(methods, 'LISSA_DEFAULTS', {'iterations': 2, 'scale': 25., 'damp': .01})
    default_changed = run(tables, 'declared_default_changed', selector_refs=['degree.yaml', 'b_param_hutch.yaml'])
    assert [x['score']['hit'] for x in default_changed['selectors']] == [True, False]


def test_mismatched_persisted_data_and_checkpoint_rejected(tables):
    root = tables[0]
    first = run(tables, 'base_checkpoint', selector_refs=['b_param_hutch.yaml'])
    item = yaml.safe_load((root / 'b_param_hutch.yaml').read_text())
    checkpoint = first['selectors'][0]['checkpoint']
    item['checkpoint'] = {k: checkpoint[k] for k in ('path', 'file_sha256', 'state_hash')}
    item['training']['lr'] = .02
    write_yaml(root / 'mismatch.yaml', item)
    with pytest.raises(RuntimeError, match='metadata'):
        run(tables, 'checkpoint_mismatch', selector_refs=['mismatch.yaml'])
    raw = (root / 'graph.pkl').read_bytes()
    (root / 'graph.pkl').write_bytes(raw + b'tampered disposable input')
    with pytest.raises(ValueError, match='graph digest'):
        run(tables, 'wrong_graph', selector_refs=['degree.yaml'])


def test_yaml_duplicate_and_implicit_override_rejected(tables):
    root = tables[0]
    with (root / 'degree.yaml').open('a') as handle:
        handle.write('\nmethod: random\n')
    with pytest.raises(ValueError, match='duplicate field'):
        run(tables, 'duplicate', selector_refs=['degree.yaml'])
    with pytest.raises(ValueError, match='unknown'):
        run(tables, 'override', defaults={'unlearn_lr': .1})
    assert not (root / 'v2').exists()


def test_operational_fields_are_rejected_and_context_is_external(tables):
    root, base, _ = tables
    path = root / 'operational.yaml'
    for field, value in (
        ('execution_authorized', True),
        ('execution_binding', {'device': 'cpu'}),
        ('device', 'cpu'), ('store_root', 'other'), ('runtime_root', 'other'),
        ('output', 'other.json'),
    ):
        config = copy.deepcopy(base)
        config[field] = value
        write_yaml(path, config)
        with pytest.raises(ValueError, match='unknown'):
            execute(path, dry_run=True)
    clean = root / 'clean.yaml'
    write_yaml(clean, base)
    with pytest.raises(ValueError, match='execution context must be supplied'):
        execute(clean)


def test_project_context_owns_fixed_store_runtime_device_and_output(tmp_path):
    context = project_context('five-selectors-two-gu', run_id='job-7',
        request_device='cuda', level='formal', repository_root=tmp_path)
    assert context.store_root == (tmp_path / 'results/cache_v2').resolve()
    assert context.checkpoint_root == (tmp_path / 'results/runtime/modular/checkpoints').resolve()
    assert context.runtime_root == (tmp_path / 'results/runtime/modular/job-7').resolve()
    assert context.output == (tmp_path / 'results/runs/modular/five-selectors-two-gu/job-7/summary.json').resolve()
    assert context.request_device == 'cuda'


def test_device_and_library_build_are_execution_provenance_not_recipe_identity():
    from experiments.modular_model import numerical_environment
    data = Data(x=torch.ones(2, 1), y=torch.tensor([0, 1]),
        edge_index=torch.empty((2, 0), dtype=torch.long))
    assert numerical_environment(data) == {'dtype': 'torch.float32'}
    assert not ({'device_type', 'torch', 'torch_geometric', 'cuda_version'}
                & set(numerical_environment(data)))


def test_minimal_method_files_expand_real_defaults(tables):
    from experiments.modular_config import load_instance
    root = tables[0]
    minimal = {'kind': 'selector', 'schema_version': 1, 'method': 'b_param_hutch',
        'candidate': {'pool': 'train_mask'}, 'budget': {'mode': 'k', 'value': 1},
        'parameters': {'parameter_scope': 'last_layer'}}
    write_yaml(root / 'minimal-b-hutch.yaml', minimal)
    resolved = load_instance(root / 'minimal-b-hutch.yaml', 'selector')
    assert resolved['model']['architecture'] == 'OpenGU.GCNNet'
    assert resolved['training']['epochs'] == 100
    assert resolved['parameters']['parameter_scope'] == 'last_layer'
    assert resolved['parameters']['hutchinson']['probes'] == 32
    minimal_gu = {'kind': 'unlearning', 'schema_version': 1, 'method': 'GNNDelete'}
    write_yaml(root / 'minimal-gu.yaml', minimal_gu)
    resolved_gu = load_instance(root / 'minimal-gu.yaml', 'unlearning')
    assert resolved_gu['model']['architecture'] == 'OpenGU.GCNNet'
    assert resolved_gu['parameters']['unlearn_lr'] == gu_defaults('GNNDelete')['unlearn_lr']


def test_documented_atomic_and_multi_reference_plans_are_same_cell_contract():
    examples = Path(__file__).resolve().parents[1] / 'docs/experiment_contract/examples'
    atomic = execute(examples / 'experiment_one_selector_one_gu.yaml', dry_run=True)
    assert len(atomic['effective_selectors']) == 1
    assert len(atomic['effective_unlearning']) == 1
    assert len(atomic['effective_evaluations']) == 1
    multi = execute(examples / 'experiment_five_selectors_two_gu.yaml', dry_run=True)
    assert len(multi['effective_selectors']) == 5
    assert len(multi['effective_unlearning']) == 2
    assert len(multi['effective_evaluations']) == 1
    assert multi['schema'] == atomic['schema'] == 'opengu.modular_run'


def test_evaluation_is_independent_and_missing_retrain_fails_closed(tables):
    root = tables[0]
    first = run(tables, 'eval-full', stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml'], evaluation_refs=['utility.yaml'])
    write_yaml(root / 'utility-small.yaml', {'kind': 'evaluation', 'schema_version': 1,
        'case': 'post_unlearning_utility', 'metrics': ['f1_after']})
    second = run(tables, 'eval-small', stage='unlearning', selector_refs=['degree.yaml'],
        unlearning_refs=['gu.yaml'], evaluation_refs=['utility-small.yaml'])
    assert identities(first) == identities(second)
    assert second['selectors'][0]['score']['hit'] is True
    assert second['unlearning'][0]['hit'] is True
    assert first['evaluations'][0]['rows'][0]['evaluation_receipt_id'] != second['evaluations'][0]['rows'][0]['evaluation_receipt_id']
    write_yaml(root / 'retrain-gap.yaml', {'kind': 'evaluation', 'schema_version': 1,
        'case': 'post_unlearning_utility_and_retrain_gap'})
    with pytest.raises(ValueError, match='independent metrics stage'):
        run(tables, 'unsupported-eval', stage='unlearning', selector_refs=['degree.yaml'],
            unlearning_refs=['gu.yaml'], evaluation_refs=['retrain-gap.yaml'])
