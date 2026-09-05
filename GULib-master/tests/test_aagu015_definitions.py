"""Definition-only guards: no models, data preparation, Cache V2 or results."""
import builtins
import io
import shutil
from pathlib import Path

import pytest
import yaml

from experiments.aagu015.definitions import CONFIG, dry_run, check_generated, load_tables
from experiments.effective_config import ConfigurationError
from experiments.modular_config import load_experiment
from experiments.modular_execution import ExecutionContext
from experiments.modular_run import execute


def test_full_matrix_uses_real_parser_without_writes_or_producers(monkeypatch):
    import experiments.modular_run as entry

    def forbidden(*args, **kwargs):
        raise AssertionError('definition-only expansion crossed a write/producer boundary')

    for name in ('read_dataset', 'prepare_model', 'resolve_methods', 'verified_selection'):
        monkeypatch.setattr(entry, name, forbidden)
    monkeypatch.setattr(Path, 'mkdir', forbidden)
    original_open = io.open
    original_builtin = builtins.open

    def guarded(original):
        def call(file, mode='r', *args, **kwargs):
            if any(flag in mode for flag in ('w', 'a', 'x', '+')):
                forbidden()
            return original(file, mode, *args, **kwargs)
        return call

    monkeypatch.setattr(io, 'open', guarded(original_open))
    monkeypatch.setattr(builtins, 'open', guarded(original_builtin))
    result = dry_run()
    assert result['counts'] == {'stage_s': 306, 'stage_u': 612,
        'conditional_preparation_groups': 9, 'conditional_score_groups': 141,
        'conditional_selection_groups': 282}
    assert result['generated_result_artifacts'] == []
    assert result['execution_ready'] is False
    rows = result['stage_s']
    assert {tuple(r['checkpoint_steps']) for r in rows if r['selector'].endswith('_3')} == {(1, 50, 100)}
    assert {tuple(r['checkpoint_steps']) for r in rows if r['selector'].endswith('_6')} == {(1, 10, 25, 50, 75, 100)}
    assert {(r['dataset'], r['planned_k']) for r in rows} == {
        ('Cora', 18), ('Cora', 94), ('CiteSeer', 23), ('CiteSeer', 116), ('PubMed', 138), ('PubMed', 690)}
    assert all(not r['selector_refs'] and not any(r['selection_input'].values()) for r in result['stage_u'])


def test_stage_u_refuses_missing_retrain_consumer_before_any_write(tmp_path, monkeypatch):
    import experiments.modular_run as entry

    def forbidden(*args, **kwargs):
        raise AssertionError('unready Stage U reached a data/model/selector operation')

    for name in ('read_dataset', 'prepare_model', 'resolve_methods'):
        monkeypatch.setattr(entry, name, forbidden)
    context = ExecutionContext(run_id='guard-only', level='verification', request_device='cpu',
        store_root=tmp_path / 'store', checkpoint_root=tmp_path / 'checkpoints',
        runtime_root=tmp_path / 'runtime', output=tmp_path / 'result.json', executor='pytest')
    path = CONFIG / 'generated/stage_u/cora-seed42-r0.01-degree.yaml'
    with pytest.raises(ConfigurationError, match='not implemented by modular_cpu_v1'):
        execute(path, context=context)
    assert list(tmp_path.iterdir()) == []


def test_stage_s_refuses_unbound_dataset_before_any_write(tmp_path, monkeypatch):
    import experiments.modular_run as entry

    def forbidden(*args, **kwargs):
        raise AssertionError('unbound dataset reached a model/selector operation')

    monkeypatch.setattr(entry, 'prepare_model', forbidden)
    monkeypatch.setattr(entry, 'resolve_methods', forbidden)
    context = ExecutionContext(run_id='guard-only', level='verification', request_device='cpu',
        store_root=tmp_path / 'store', checkpoint_root=tmp_path / 'checkpoints',
        runtime_root=tmp_path / 'runtime', output=tmp_path / 'result.json', executor='pytest')
    with pytest.raises(ConfigurationError, match='persisted Dataset/Split artifacts are required'):
        execute(CONFIG / 'generated/stage_s/cora-seed42-r0.01.yaml', context=context)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('fault', ['unknown_matrix_field', 'wrong_reference_kind', 'unknown_selector_field', 'generated_drift'])
def test_configuration_drift_and_mismatched_references_fail_closed(tmp_path, fault):
    target = tmp_path / 'config'
    shutil.copytree(CONFIG, target)
    if fault == 'unknown_matrix_field':
        path = target / 'stage_s.yaml'
        value = yaml.safe_load(path.read_text(encoding='utf-8'))
        value['device'] = 'cuda'
    elif fault == 'wrong_reference_kind':
        path = target / 'stage_s.yaml'
        value = yaml.safe_load(path.read_text(encoding='utf-8'))
        value['selector_refs'][0] = 'unlearning/gif.yaml'
    elif fault == 'unknown_selector_field':
        path = target / 'selectors/degree.yaml'
        value = yaml.safe_load(path.read_text(encoding='utf-8'))
        value['unused_parameter'] = True
    else:
        path = target / 'generated/stage_s/cora-seed42-r0.01.yaml'
        value = yaml.safe_load(path.read_text(encoding='utf-8'))
        value['experiment_id'] = 'drift'
    path.write_text(yaml.safe_dump(value), encoding='utf-8')
    with pytest.raises(ConfigurationError):
        check_generated(target)


def test_stage_u_independent_selection_lineage_and_seeds():
    for path in (CONFIG / 'generated/stage_u').glob('*.yaml'):
        config = load_experiment(path)
        assert not config['selectors']
        assert config['selection_input'] == {'artifact_id': None, 'recipe_hash': None, 'content_hash': None}
        seed = int(config['case_id'].split('-seed')[1].split('-')[0])
        assert {gu['training']['seed'] for gu in config['unlearnings']} == {seed}
        assert {gu['method'] for gu in config['unlearnings']} == {'GIF', 'GNNDelete'}
