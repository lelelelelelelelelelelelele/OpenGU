from __future__ import annotations

from pathlib import Path

def _modular_preflight(definition, config_path):
    from experiments.modular_run import execute
    plan = execute(config_path, dry_run=True)
    errors = []
    if plan['configuration_fingerprint'] != definition['configuration_fingerprint']:
        errors.append('referenced configuration fingerprint changed')
    if plan['logical_cells'] != definition['logical_cells']:
        errors.append('expanded conditions differ from registration')
    if plan['experiment_id'] != definition['experiment_id']:
        errors.append('experiment identity differs from registration')
    return {'ready': not errors, 'errors': errors}


_PREFLIGHT_HANDLERS = {'modular-project-v1': _modular_preflight}


def bind_execution_node(definition, node_id):
    """Bind only execution argv; reviewed Recipe and scientific identity stay fixed."""
    from syncmate_core.context import validate_node_id
    node_id = validate_node_id(node_id)
    argv = tuple(definition['argv'])
    if argv[1] == 'scripts/syncmate/syncmate.py':
        argv = argv[:2] + ('--node-id', node_id) + argv[2:]
    else:
        argv += ('--node-id', node_id)
    return {**definition, 'argv': argv}
