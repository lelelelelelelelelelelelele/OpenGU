"""Read-only scientific startup check in a fresh, exactly prepared checkout."""
from __future__ import annotations

import json
from pathlib import Path
import sys

# Load installed control dependencies before exposing the prepared scientific tree.
from opengu_syncmate.control import dependency as installed_dependencies
from syncmate_core.versions import GitSource

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def check(request):
    from syncmate_core.identity import sha256_recipe_config
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    from scripts.syncmate.opengu_adapter import _modular_preflight
    from scripts.syncmate.opengu_execution import device_context
    from scripts.syncmate.recipe_inputs import dataset_counts
    from experiments.modular_config import load_experiment
    definition, contract = request['definition'], request['contract']
    if sha256_recipe_config(ROOT / definition['config_path']) != contract['config_sha256']:
        raise ValueError('bound startup config SHA differs')
    dependency = verify_core_dependency()
    if not dependency['ready']:
        raise ValueError('; '.join(dependency['errors']))
    dependencies = installed_dependencies(GitSource(ROOT, contract['git_sha']))
    if definition.get('preflight_profile') != 'modular-project-v1':
        return {'ready': True, 'errors': [], 'observed': {'core_payload': True}}
    plan = _modular_preflight(definition, ROOT / definition['config_path'])
    if not plan['ready']:
        return plan
    execution = device_context(definition['experiment_id'], run_id=definition['run_identity']['run_id'],
        node_id=request['node_id'], device_file=ROOT / '.syncmate/device.yaml',
        verification_root=definition.get('verification_root'))
    if execution.source_git_sha != contract['git_sha']:
        raise ValueError('scientific execution context differs from task source')
    if execution.output.parent.exists() or execution.runtime_root.exists():
        raise ValueError('scientific result/runtime identity already exists')
    counts = dataset_counts(load_experiment(ROOT / definition['config_path']), ROOT)
    if counts != definition['expected_datasets']:
        raise ValueError('bound Dataset/Split counts differ from reviewed Recipe')
    return {'ready': True, 'errors': [], 'observed': execution.receipt(), 'installed_dependencies': dependencies}


if __name__ == '__main__':
    try:
        response = check(json.load(sys.stdin))
    except Exception as exc:
        response = {'ready': False, 'errors': [type(exc).__name__ + ': ' + str(exc)]}
    print(json.dumps(response, ensure_ascii=False))
    raise SystemExit(0 if response['ready'] else 1)
