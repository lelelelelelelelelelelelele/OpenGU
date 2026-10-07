"""Read-only recovery checks for host-local ScoreBundle lock files."""
from pathlib import Path
import os
import stat


def owner_status(pid):
    if pid == os.getpid():
        return 'active'
    # os.kill(pid, 0) is a liveness probe on POSIX, not on Windows.
    if os.name != 'posix':
        return 'unknown'
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return 'orphan'
    except OSError:
        return 'unknown'
    return 'active'


def inspect_score_lock(path):
    path = Path(path)
    result = {'path': str(path), 'owner_pid': None, 'status': 'unknown'}
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > 32:
            return result
        raw = path.read_text(encoding='ascii')
        if not raw.isdigit() or not 0 < int(raw) <= 2147483647:
            return result
        result.update(owner_pid=int(raw), mtime_ns=info.st_mtime_ns,
                      status=owner_status(int(raw)))
    except FileNotFoundError:
        result['status'] = 'absent'
    except (OSError, UnicodeError, ValueError):
        pass
    return result


def score_lock_preflight(store_root):
    """Only control files are inspected; no payload scan or automatic deletion."""
    folder = Path(store_root) / '.locks'
    if folder.is_symlink():
        return {'ready': False, 'locks': [], 'errors': ['ScoreBundle lock directory is a symlink: ' + str(folder)]}
    if folder.exists() and not folder.is_dir():
        return {'ready': False, 'locks': [], 'errors': ['ScoreBundle lock directory is not a directory: ' + str(folder)]}
    locks = []
    if folder.exists():
        for path in sorted(folder.glob('score-*.lock')):
            item = inspect_score_lock(path)
            if item['status'] != 'absent':
                locks.append(item)
    errors = ['ScoreBundle lock {status}: {path} (PID {owner_pid}); resolve recovery before starting'.format(**item)
              for item in locks]
    return {'ready': not errors, 'locks': locks, 'errors': errors}


def require_score_locks_clear(store_root):
    from cache_v2.errors import CacheResolutionError
    result = score_lock_preflight(store_root)
    if not result['ready']:
        raise CacheResolutionError('; '.join(result['errors']))
