"""Recovery partitions retain exact scientific inputs and immutable run roots."""
import json
from pathlib import Path

from experiments.modular_config import load_experiment, experiment_batches, unlearning_entries, configuration_fingerprint
from scripts.syncmate.opengu_recipes import recipe_definitions
from syncmate_core.identity import sha256_recipe_config

ROOT = Path(__file__).resolve().parents[1]


def conditions(path):
    config = load_experiment(ROOT / path)
    result = set()
    for batch in experiment_batches(config):
        dataset = config['datasets'][batch['matrix_values']['dataset_index']]
        for gu, _, selector, _ in unlearning_entries(batch):
            result.add(json.dumps([dataset, selector, gu, config['evaluations']], sort_keys=True))
    return result


def test_recovery_partitions_are_disjoint_exact_subsets():
    main = conditions('experiments/configs/aagu011/table02.yaml')
    assert len(main) == 1035
    union = set()
    roots = set()
    partitions = {name: value for name, value in recipe_definitions().items()
                  if name.startswith('opengu-aagu011-v1-recovery-') and not name.endswith('-full')}
    assert len(partitions) == 5
    for recipe in partitions.values():
        subset = conditions(recipe['config_path'])
        assert len(subset) == recipe['logical_cells'] == 115
        assert subset <= main and not subset & union
        union |= subset
        root = tuple(recipe['run_identity'].values())
        assert root not in roots
        roots.add(root)
        assert recipe['timeout_seconds'] <= 21600
    assert len(union) == 575
    full = recipe_definitions()['opengu-aagu011-v1-recovery-full']
    original = recipe_definitions()['opengu-aagu011-table02-v1']
    assert full['config_path'] == original['config_path']
    assert full['configuration_fingerprint'] == original['configuration_fingerprint']
    assert full['run_identity']['run_id'] != original['run_identity']['run_id']


def test_recovery_registration_matches_core_normalized_config_hashes():
    for name, recipe in recipe_definitions().items():
        if name.startswith('opengu-aagu011-v1-recovery-'):
            path = ROOT / recipe['config_path']
            assert sha256_recipe_config(path) == recipe['config_sha256']
            assert configuration_fingerprint(path) == recipe['configuration_fingerprint']
