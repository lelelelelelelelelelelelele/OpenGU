"""Pending scientific registrations must match the real Core and YAML parser."""
from pathlib import Path

import pytest

from experiments.modular_run import execute
from scripts.syncmate.opengu_recipes import recipe_definitions
from syncmate_core.identity import sha256_recipe_config


@pytest.mark.parametrize('recipe_id', [
    'opengu-aagu031-stage-s-v2', 'opengu-aagu032-extend-v2',
])
def test_pending_registration_matches_ordinary_entry(recipe_id):
    recipe = recipe_definitions()[recipe_id]
    path = Path(__file__).resolve().parents[1] / recipe['config_path']
    plan = execute(path, dry_run=True)
    assert sha256_recipe_config(path) == recipe['config_sha256']
    assert plan['configuration_fingerprint'] == recipe['configuration_fingerprint']
    assert plan['experiment_id'] == recipe['run_identity']['experiment_id']
    assert plan['logical_cells'] == recipe['logical_cells']
    assert plan['stage'] == recipe['stage']
    assert not plan['producer_called']
    paths = recipe['expected_artifact_paths']
    count = 1 if plan['stage'] == 'selector' else 1 + 4 * plan['logical_cells']
    assert len(paths) == len(set(paths)) == count
