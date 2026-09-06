"""Public YAML names resolve by type, never by table location or cwd."""
from pathlib import Path

import pytest
import yaml

from experiments.modular_config import (
    ROOT, REFERENCE_DIRECTORIES, configuration_fingerprint, load_experiment,
    resolve_reference,
)
from experiments.modular_run import execute


def test_moved_table_and_cwd_keep_public_instances_and_fingerprint(tmp_path, monkeypatch):
    original = ROOT / 'experiments/configs/aagu007/experiment.yaml'
    expected = load_experiment(original)
    fingerprint = configuration_fingerprint(original)
    moved = tmp_path / 'elsewhere/table.yaml'
    moved.parent.mkdir()
    moved.write_bytes(original.read_bytes())
    # Local names must not shadow the public instances.
    (moved.parent / 'cora.yaml').write_text('not: a dataset')
    monkeypatch.chdir(tmp_path)
    actual = load_experiment(moved)
    for field in ('dataset', 'selectors', 'unlearnings', 'evaluations', 'configuration_sources'):
        assert actual[field] == expected[field]
    assert configuration_fingerprint(moved) == fingerprint
    assert execute(moved, dry_run=True)['logical_cells'] == 4


@pytest.mark.parametrize('field', REFERENCE_DIRECTORIES)
@pytest.mark.parametrize('reference', ['../cora.yaml', 'datasets/cora.yaml',
    '..\\cora.yaml', 'C:cora.yaml', '', None, 'missing.yaml'])
def test_invalid_public_reference_fails_for_load_and_fingerprint(tmp_path, field, reference):
    value = yaml.safe_load((ROOT / 'experiments/configs/aagu007/experiment.yaml').read_text())
    value[field] = reference if field == 'dataset_ref' else [reference]
    path = tmp_path / 'invalid.yaml'
    path.write_text(yaml.safe_dump(value))
    for consumer in (load_experiment, configuration_fingerprint):
        with pytest.raises(ValueError):
            consumer(path)


def test_same_name_uses_field_directory_and_explicit_file_is_unambiguous(tmp_path, monkeypatch):
    import experiments.modular_config as config
    monkeypatch.setattr(config, 'ROOT', tmp_path)
    for field, directory in REFERENCE_DIRECTORIES.items():
        path = tmp_path / 'experiments/configs' / directory / 'same.yaml'
        path.parent.mkdir(parents=True)
        path.write_text('kind: fixture')
        assert resolve_reference(field, 'same.yaml', tmp_path) == path
    explicit = tmp_path / 'temporary.yaml'
    explicit.write_text('kind: fixture')
    assert resolve_reference('dataset_ref', str(explicit), tmp_path) == explicit


def test_fingerprint_tracks_resolved_public_content(tmp_path, monkeypatch):
    import experiments.modular_config as config
    monkeypatch.setattr(config, 'ROOT', tmp_path)
    directory = tmp_path / 'experiments/configs/datasets'
    directory.mkdir(parents=True)
    instance = directory / 'data.yaml'
    instance.write_text('value: 1')
    table = tmp_path / 'table.yaml'
    table.write_text('dataset_ref: data.yaml')
    before = configuration_fingerprint(table)
    instance.write_text('value: 2')
    assert configuration_fingerprint(table) != before


def test_explicit_relative_paths_resolve_from_table_not_cwd(tmp_path, monkeypatch):
    original = ROOT / 'experiments/configs/aagu007/experiment.yaml'
    value = yaml.safe_load(original.read_text())
    public = load_experiment(original)
    for field, directory in REFERENCE_DIRECTORIES.items():
        names = [value[field]] if field == 'dataset_ref' else value[field]
        target = tmp_path / directory
        target.mkdir()
        for name in names:
            (target / name).write_bytes((ROOT / 'experiments/configs' / directory / name).read_bytes())
        refs = ['../' + directory + '/' + name for name in names]
        value[field] = refs[0] if field == 'dataset_ref' else refs
    table = tmp_path / 'tables/experiment.yaml'
    table.parent.mkdir()
    table.write_text(yaml.safe_dump(value))
    monkeypatch.chdir(ROOT)
    resolved = load_experiment(table)
    for field in ('dataset', 'selectors', 'unlearnings', 'evaluations'):
        assert resolved[field] == public[field]
    assert execute(table, dry_run=True)['logical_cells'] == 4
    before = configuration_fingerprint(table)
    (tmp_path / 'selectors/degree.yaml').write_text(
        (tmp_path / 'selectors/degree.yaml').read_text().replace('degree', 'random'))
    assert configuration_fingerprint(table) != before
    local = table.parent / 'degree.yaml'
    local.write_bytes((ROOT / 'experiments/configs/selectors/degree.yaml').read_bytes())
    assert resolve_reference('selector_refs', './degree.yaml', table.parent) == local
    assert resolve_reference('selector_refs', '.\\degree.yaml', table.parent) == local
