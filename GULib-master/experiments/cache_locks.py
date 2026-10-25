"""Read-only owner diagnostics for an individual ScoreBundle entry lock."""
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
