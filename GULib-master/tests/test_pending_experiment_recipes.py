"""Pending scientific registrations must match the real Core and YAML parser."""
from pathlib import Path

import pytest
from experiments.modular_run import execute
from scripts.syncmate.opengu_recipes import resolve_recipe
from syncmate_core.identity import sha256_recipe_config


@pytest.mark.parametrize('recipe_id,expected_files', [
    ('opengu-aagu007-v2', 9),
    ('exp079-etr-r2', 1441),
    ('exp092-confirm', 161),
])
def test_pending_registration_matches_ordinary_entry(recipe_id, expected_files):
    recipe = resolve_recipe(Path(__file__).resolve().parents[1], recipe_id)
    path = Path(__file__).resolve().parents[1] / recipe['config_path']
    plan = execute(path, dry_run=True)
    assert sha256_recipe_config(path) == recipe['config_sha256']
    assert plan['configuration_fingerprint'] == recipe['configuration_fingerprint']
    assert plan['experiment_id'] == recipe['experiment_id']
    assert plan['logical_cells'] == recipe['logical_cells']
    assert plan['stage'] == recipe['stage']
    assert not plan['producer_called']
    paths = recipe['expected_artifact_paths']
    assert len(paths) == len(set(paths)) == expected_files
