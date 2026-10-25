"""Local PID observations for a ScoreBundle lock, not owner liveness proof."""
from pathlib import Path
import os
import stat


def owner_status(pid):
    """Visibility in this PID namespace cannot establish the lock owner's liveness."""
    if pid == os.getpid():
        return 'local_pid_visible'
    # Signal zero observes only this POSIX PID namespace; Windows differs.
    if os.name != 'posix':
        return 'unknown'
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return 'local_pid_not_visible'
    except OSError:
        return 'unknown'
    return 'local_pid_visible'


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
