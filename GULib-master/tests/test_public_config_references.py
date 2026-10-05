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
    for field in ('datasets', 'selectors', 'unlearnings', 'evaluations', 'configuration_sources'):
        assert actual[field] == expected[field]
    assert configuration_fingerprint(moved) == fingerprint
    assert execute(moved, dry_run=True)['logical_cells'] == 4


@pytest.mark.parametrize('field', REFERENCE_DIRECTORIES)
@pytest.mark.parametrize('reference', ['../cora.yaml', 'datasets/cora.yaml',
    '..\\cora.yaml', 'C:cora.yaml', '', None, 'missing.yaml'])
def test_invalid_public_reference_fails_for_load_and_fingerprint(tmp_path, field, reference):
    source = ('experiments/configs/aagu077/table02_gif_idea_gate.yaml'
              if field == 'parameter_profile_ref' else 'experiments/configs/aagu007/experiment.yaml')
    value = yaml.safe_load((ROOT / source).read_text(encoding='utf-8'))
    value[field] = reference if field == 'parameter_profile_ref' else [reference]
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
    assert resolve_reference('dataset_refs', str(explicit), tmp_path) == explicit


def test_fingerprint_tracks_resolved_public_content(tmp_path, monkeypatch):
    import experiments.modular_config as config
    monkeypatch.setattr(config, 'ROOT', tmp_path)
    directory = tmp_path / 'experiments/configs/datasets'
    directory.mkdir(parents=True)
    instance = directory / 'data.yaml'
    instance.write_text('value: 1')
    table = tmp_path / 'table.yaml'
    table.write_text('dataset_refs: [data.yaml]')
    before = configuration_fingerprint(table)
    instance.write_text('value: 2')
    assert configuration_fingerprint(table) != before


def test_explicit_relative_paths_resolve_from_table_not_cwd(tmp_path, monkeypatch):
    original = ROOT / 'experiments/configs/aagu007/experiment.yaml'
    value = yaml.safe_load(original.read_text())
    public = load_experiment(original)
    for field, directory in REFERENCE_DIRECTORIES.items():
        if field not in value:
            continue
        names = value[field]
        target = tmp_path / directory
        target.mkdir()
        for name in names:
            (target / name).write_bytes((ROOT / 'experiments/configs' / directory / name).read_bytes())
        refs = ['../' + directory + '/' + name for name in names]
        value[field] = refs
    table = tmp_path / 'tables/experiment.yaml'
    table.parent.mkdir()
    table.write_text(yaml.safe_dump(value))
    monkeypatch.chdir(ROOT)
    resolved = load_experiment(table)
    for field in ('datasets', 'selectors', 'unlearnings', 'evaluations'):
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


def test_public_profile_survives_table_move_and_cannot_be_shadowed(tmp_path, monkeypatch):
    original = ROOT / 'experiments/configs/aagu077/table02_gif_idea_gate.yaml'
    expected = load_experiment(original)
    value = yaml.safe_load(original.read_text(encoding='utf-8'))
    value['parameter_profile_ref'] = 'gif_idea_fixed_pt.yaml'
    table = tmp_path / 'nested/table.yaml'
    table.parent.mkdir()
    table.write_text(yaml.safe_dump(value), encoding='utf-8')
    (table.parent / 'gif_idea_fixed_pt.yaml').write_text('invalid local profile', encoding='utf-8')
    fingerprint = configuration_fingerprint(table)
    moved = tmp_path / 'moved.yaml'
    moved.write_bytes(table.read_bytes())
    monkeypatch.chdir(tmp_path)
    for path in (table, moved):
        actual = load_experiment(path)
        for field in ('datasets', 'selectors', 'unlearnings', 'effective_parameter_profiles'):
            assert actual[field] == expected[field]
        assert configuration_fingerprint(path) == fingerprint
        assert execute(path, dry_run=True)['logical_cells'] == 6


def test_profile_fingerprint_tracks_content_and_explicit_paths(tmp_path, monkeypatch):
    import experiments.modular_config as config
    monkeypatch.setattr(config, 'ROOT', tmp_path)
    profile = tmp_path / 'experiments/configs/profiles/params.yaml'
    profile.parent.mkdir(parents=True)
    profile.write_text('value: 1', encoding='utf-8')
    table = tmp_path / 'table.yaml'
    table.write_text('parameter_profile_ref: params.yaml', encoding='utf-8')
    before = configuration_fingerprint(table)
    profile.write_text('value: 2', encoding='utf-8')
    assert configuration_fingerprint(table) != before
    local = tmp_path / 'params.yaml'
    local.write_text('value: local', encoding='utf-8')
    monkeypatch.chdir(ROOT)
    for reference in ('./params.yaml', '.\\params.yaml', str(local)):
        assert resolve_reference('parameter_profile_ref', reference, table.parent) == local
    profile.unlink()
    # A local namesake must not silently replace a missing public profile.
    with pytest.raises(ValueError, match='YAML file does not exist'):
        configuration_fingerprint(table)
