"""Explicit SyncMate assembly for the project-owned execution context."""
from __future__ import annotations

from pathlib import Path

from experiments.effective_config import ConfigurationError
from experiments.modular_execution import REPO_ROOT, native_context
from scripts.syncmate.opengu_progress import make_notify


def device_context(experiment_id, *, run_id, device_file, verification_root=None):
    """Read the optional Core device contract, then use OpenGU's native policy."""
    try:
        from syncmate_core.context import use
        from syncmate_core.devices import load_device
    except ImportError as exc:
        raise ConfigurationError('SyncMate integration requires the installed Core') from exc
    from scripts.syncmate.verify_core_dependency import verify_core_dependency
    dependency = verify_core_dependency()
    if not dependency['ready']:
        raise ConfigurationError('SyncMate integration: ' + '; '.join(dependency['errors']))
    with use(REPO_ROOT):
        config, warnings = load_device(Path(device_file))
    if warnings:
        raise ConfigurationError('device configuration: ' + '; '.join(warnings))
    root = Path(config['repo_path']).expanduser()
    if not root.is_absolute() or not root.is_dir():
        raise ConfigurationError('device repo_path must be an existing absolute directory')
    root = root.resolve()
    if verification_root is not None and Path(verification_root).resolve() != root:
        raise ConfigurationError('verification root differs from device repo_path')
    return native_context(experiment_id, run_id=run_id,
        request_device=config.get('execution_device'), repository_root=root,
        verification_root=verification_root)
