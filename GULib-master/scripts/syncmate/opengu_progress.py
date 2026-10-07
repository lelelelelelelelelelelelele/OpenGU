"""Map OpenGU's optional batch/stage declarations to Core's ordered cursor."""
from __future__ import annotations

import os
from pathlib import Path
import sys

from experiments.effective_config import ConfigurationError


def progress_plan(config):
    """Generate the transport plan from the same steps used by the executor."""
    from experiments.modular_progress import progress_steps
    from syncmate_core.progress import validate_plan
    return validate_plan([
        {'id': f'step-{index}', 'label': step['label'], 'match': step['position']}
        for index, step in enumerate(progress_steps(config))
    ])


def make_notify(config, context, *, config_path=None, enabled=True):
    """No runner context disables progress; malformed explicit contexts fail setup.

    Publishing is observational. Core write errors are diagnosed on stderr and
    never replace scientific failures or control computation.
    """
    if not enabled:
        return None
    try:
        from syncmate_core import progress
        from syncmate_core.contracts import JOB_ID_RE, GIT_SHA_RE, SHA256_RE
        from syncmate_core.identity import sha256_recipe_config
    except ImportError as exc:
        raise ConfigurationError('SyncMate integration requires the installed Core') from exc
    value = os.environ.get(progress.ENV)
    if not value:
        return None
    try:
        path = Path(value)
        if not path.is_absolute() or path.is_symlink():
            raise ValueError('progress context must be an absolute regular file')
        supplied = progress.read_json(path)
        binding = supplied['binding']
        if set(binding) != {'job_id', 'recipe', 'git_sha', 'config_sha256', 'plan_sha256'}:
            raise ValueError('invalid progress binding fields')
        for key, pattern in (('job_id', JOB_ID_RE), ('recipe', JOB_ID_RE),
                             ('git_sha', GIT_SHA_RE), ('config_sha256', SHA256_RE),
                             ('plan_sha256', SHA256_RE)):
            if not isinstance(binding[key], str) or not pattern.fullmatch(binding[key]):
                raise ValueError('invalid progress binding: ' + key)
        root = context.store_root.parent.parent
        expected_path = progress.safe_path(root, binding['job_id'], 'context.json')
        if path.resolve() != expected_path.resolve():
            raise ValueError('progress context belongs to a different execution root')
        plan = progress_plan(config)
        if supplied.get('protocol') != progress.PROTOCOL or supplied.get('plan') != plan:
            raise ValueError('progress plan differs from the actual experiment steps')
        if binding['plan_sha256'] != progress.plan_sha(plan):
            raise ValueError('progress plan digest mismatch')
        if not context.source_git_sha or binding['git_sha'] != context.source_git_sha:
            raise ValueError('progress source Git identity mismatch')
        if config_path is None or binding['config_sha256'] != sha256_recipe_config(Path(config_path)):
            raise ValueError('progress configuration identity mismatch')
        publisher = progress.Progress(path)
        if not publisher.enabled:
            raise ValueError(publisher.error or 'progress publisher is unavailable')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ConfigurationError('SyncMate progress setup: ' + str(exc)) from exc

    last_position = plan[-1]['match']
    last_error = None

    def notify(kind, *, position, current=None, total=None):
        nonlocal last_error
        try:
            if kind == 'progress':
                written = publisher.update(current=current, total=total, **position)
            elif kind == 'completed' and not position and current is None and total is None:
                written = publisher.completed(**last_position)
            else:
                raise ValueError('unsupported experiment progress declaration')
            error = publisher.error if not written else None
        except Exception as exc:
            written, error = False, str(exc)
        if error and error != last_error:
            print('SyncMate progress publication failed: ' + error, file=sys.stderr)
        last_error = error
        return written

    return notify
