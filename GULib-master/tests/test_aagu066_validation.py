import copy
import hashlib
import json
from pathlib import Path

import pytest
import torch
from torch_geometric.data import Data

from experiments import aagu066_validation as validation

ROOT = Path(__file__).resolve().parents[1]


def test_frozen_matrix_and_no_producers_in_dry_plan():
    config, policy, fingerprint = validation.load_plan(ROOT / 'experiments/configs/aagu066/table.yaml')
    assert len(validation.artifact_names(config)) == 16
    assert len(fingerprint) == 64
    assert config['unlearnings'][2]['training']['epochs'] == 3000
    assert set(policy['prior_diagnostics']) == {'104246', '104247'}


def test_trace_matches_exact_shifted_linear_solve_and_production():
    from unlearning.unlearning_methods.GIF.solver import solve_gif_system
    matrix = torch.diag(torch.tensor([-2., 3., 8.], dtype=torch.float64))
    rhs = torch.tensor([1., -2., 4.], dtype=torch.float64)
    snapshots, trace = validation.measured_update(lambda x: matrix @ x, rhs, [100, 200, 400], 10., .4)
    exact = torch.linalg.solve(matrix + 4 * torch.eye(3), rhs)
    actual, _ = solve_gif_system(lambda x: matrix @ x, rhs, iterations=100, scale=10., damp=.4)
    assert torch.allclose(snapshots[100], exact, atol=1e-8)
    assert torch.equal(actual, snapshots[100])
    assert len(trace) == 401
    assert trace[-1]['shifted_relative_residual'] < 1e-12
    assert trace[-1]['original_relative_residual'] > .1


def test_no_cache_real_method_smoke(tmp_path, monkeypatch):
    """Real GCN, Random, GIF/IDEA seam, fresh Retrain and both evaluation graphs."""
    from experiments.modular_model import create_model
    from experiments.modular_config import experiment_batches
    from utils.target_checkpoint import save_weights, capture_state
    import experiments.artifact_producer as artifacts
    import experiments.modular_model as preparation
    import experiments.target_direct_v1.method_cache as cache
    def forbidden(*args, **kwargs):
        raise AssertionError('computation cache called')
    monkeypatch.setattr(artifacts, 'resolve_formal_artifact', forbidden)
    monkeypatch.setattr(artifacts, 'store_formal_artifact', forbidden)
    monkeypatch.setattr(preparation, 'load_cached_weights', forbidden)
    monkeypatch.setattr(preparation, 'save_cached_weights', forbidden)
    monkeypatch.setattr(cache, 'resolve_methods', forbidden)
    torch.set_num_threads(2)
    torch.manual_seed(123)
    n = 40
    edges = torch.stack([torch.arange(n), torch.arange(n).roll(-1)])
    data = Data(x=torch.randn(n, 4), y=torch.arange(n) % 2,
                edge_index=torch.cat([edges, edges.flip(0)], dim=1))
    data.train_mask = torch.arange(n) < 30
    data.val_mask = (torch.arange(n) >= 30) & (torch.arange(n) < 35)
    data.test_mask = torch.arange(n) >= 35
    config, policy, _ = validation.load_plan(ROOT / 'experiments/configs/aagu066/gate.yaml')
    batch = next(experiment_batches(config))
    model = create_model(batch['unlearnings'][0]['model'], 'Cora', data, 'cpu')
    pt = tmp_path / 'fixed.pt'
    save_weights(pt, capture_state(model))
    policy = copy.deepcopy(policy)
    policy['checkpoint_sha256'] = hashlib.sha256(pt.read_bytes()).hexdigest()
    for instance in batch['unlearnings'][:2]:
        instance['checkpoint'] = str(pt)
    batch['unlearnings'][2]['training']['epochs'] = 2
    output = tmp_path / 'run'
    validation.run_request(batch, policy, data, output, tmp_path, tmp_path / 'cache')
    assert not (tmp_path / 'cache').exists()
    assert {p.name for p in output.iterdir()} == {'reference.json', 'selection.json', 'gif.json', 'idea.json', 'retrain.json'}
    rows = [json.loads((output / name).read_text()) for name in ('gif.json', 'idea.json', 'retrain.json')]
    assert len({row['selection_sha256'] for row in rows}) == 1
    assert all(set(row['metrics']) == {'original', 'retained'} for row in rows)
    assert all(row['checks']['original_weights_unchanged'] for row in rows[:2])
    assert len(rows[0]['diagnostics']['trace']) == 401
    from experiments.aagu066_report import render
    documents = {f'seed104248/{p.name}': json.loads(p.read_text()) for p in output.iterdir()}
    render({'requests': [{'seed': 104248}], 'policy': policy, 'run_id': 'synthetic-smoke-only',
            'commit': 'synthetic-test'}, documents, tmp_path / 'report')
    assert (tmp_path / 'report/evidence/solver-trajectories.png').is_file()
    page = (tmp_path / 'report/REPORT.html').read_text(encoding='utf-8')
    assert 'data-workblock-decision="pending"' in page
    assert 'data:image/png;base64,' in page


def test_prior_checksum_failure_is_closed(tmp_path):
    policy = {'prior_diagnostics': {'104246': {'files': {'prior.json': '0' * 64}}}}
    (tmp_path / 'prior.json').write_text('{}')
    with pytest.raises(ValueError, match='checksum mismatch'):
        validation.read_prior(policy, 104246, 'GIF', {}, [], {}, {}, tmp_path)


def test_prior_identity_and_production_change_are_checked(tmp_path, monkeypatch):
    from types import SimpleNamespace
    nodes = [1, 3]
    checkpoint = {'state_hash': 'weights', 'file_sha256': 'pt'}
    params = {'scale': 9000, 'damp': 2048 / 9000}
    run = {'commit': 'old', 'status': 'diagnostic_complete', 'data_identity': {'split': 'fixed'},
           'selection': {'selected_nodes_sha256': hashlib.sha256(json.dumps(nodes, separators=(',', ':')).encode()).hexdigest()},
           'contract': {'selector': {'seed': 104246}}}
    files = {'run.json': run}
    for t in (100, 200, 400):
        files[f'gif-{t}.json'] = {'method': 'GIF', 'iteration': t, 'checkpoint': checkpoint,
            **params, 'status': 'finite_truncation', 'original_weights_unchanged': True, 'delta_l2': .01,
            'trace': [{'iteration': t, 'shifted_relative_residual': 1e-7}]}
    for name, value in files.items():
        validation.write(tmp_path / name, value)
    policy = {'diagnostic_iterations': [100, 200, 400], 'prior_diagnostics': {'104246': {'files': {
        name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() for name in files}}}}
    monkeypatch.setattr(validation.subprocess, 'run', lambda *a, **k: SimpleNamespace(returncode=0))
    result = validation.read_prior(policy, 104246, 'GIF', {'split': 'fixed'}, nodes, checkpoint, params, tmp_path)
    assert result['budget_norm_relative_difference'] == 0
    with pytest.raises(ValueError, match='identity mismatch'):
        validation.read_prior(policy, 104246, 'GIF', {'split': 'fixed'}, [1, 4], checkpoint, params, tmp_path)
    monkeypatch.setattr(validation.subprocess, 'run', lambda *a, **k: SimpleNamespace(returncode=1))
    with pytest.raises(ValueError, match='production system changed'):
        validation.read_prior(policy, 104246, 'GIF', {'split': 'fixed'}, nodes, checkpoint, params, tmp_path)


def test_syncmate_registration_and_changed_fingerprint_rejected():
    from scripts.syncmate.opengu_recipes import recipe_definitions
    from scripts.syncmate.opengu_adapter import OpenGUProjectExtension
    adapter = OpenGUProjectExtension()
    for name in ('opengu-aagu066-h16-gate-v1', 'opengu-aagu066-h16-v1'):
        definition = recipe_definitions()[name]
        path = ROOT / definition['config_path']
        assert adapter.preflight(definition['preflight_profile'], definition, path)['ready']
        bad = {**definition, 'configuration_fingerprint': '0' * 64}
        assert not adapter.preflight(definition['preflight_profile'], bad, path)['ready']
        assert len(definition['expected_artifact_paths']) == (6 if 'gate' in name else 16)


def test_syncmate_rejects_unverified_delivery(tmp_path):
    from scripts.syncmate.opengu_acceptance import acceptance_payload
    from scripts.syncmate.opengu_recipes import recipe_definitions
    verdict = acceptance_payload('aagu066-validation-v1', recipe_definitions()['opengu-aagu066-h16-v1'],
        {'project_root': str(tmp_path), 'node_id': 'gpu4090', 'artifact_index': {}, 'expected_git_sha': '0' * 40})
    assert not verdict['passed']
    assert verdict['accepted_cells'] == 0


def test_collected_run_rejects_relabeling_even_with_updated_file_hash(tmp_path):
    config, policy, fingerprint = validation.load_plan(ROOT / 'experiments/configs/aagu066/gate.yaml')
    nodes = list(range(189))
    selected_hash = hashlib.sha256(json.dumps(nodes, separators=(',', ':')).encode()).hexdigest()
    selection = {'seed': 104248, 'requested_k': 189, 'selected_nodes': nodes, 'selected_nodes_sha256': selected_hash}
    documents = {'seed104248/selection.json': selection,
                 'seed104248/reference.json': {'checkpoint': {'file_sha256': policy['checkpoint_sha256']}}}
    for method in ('GIF', 'IDEA', 'Retrain'):
        documents[f'seed104248/{method.lower()}.json'] = {'method': method, 'seed': 104248,
            'status': 'completed', 'selection_sha256': selected_hash,
            'checks': {'finite': True}, 'numerical_passed': True}
    for name, doc in documents.items():
        validation.write(tmp_path / name, doc)
    run = {'schema': validation.SCHEMA, 'status': 'completed', 'experiment_id': config['experiment_id'],
           'configuration_fingerprint': fingerprint, 'policy': policy, 'data_identity': policy['data_identity'],
           'commit': 'test-commit', 'requests': [{'seed': 104248, 'status': 'completed', 'numerical_passed': True}],
           'numerical_passed': True,
           'files': {name: hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() for name in documents}}
    validation.write(tmp_path / 'run.json', run)
    validation.verify_run(tmp_path / 'run.json', ROOT / 'experiments/configs/aagu066/gate.yaml', 'test-commit')
    documents['seed104248/gif.json']['seed'] = 104246
    validation.write(tmp_path / 'seed104248/gif.json', documents['seed104248/gif.json'])
    run['files']['seed104248/gif.json'] = hashlib.sha256((tmp_path / 'seed104248/gif.json').read_bytes()).hexdigest()
    validation.write(tmp_path / 'run.json', run)
    with pytest.raises(ValueError, match='unpaired'):
        validation.verify_run(tmp_path / 'run.json', ROOT / 'experiments/configs/aagu066/gate.yaml', 'test-commit')
