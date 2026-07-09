#!/usr/bin/env python3
"""
IM progress monitor.

This is an external estimator: it cannot attach to the process internals, but
it can watch CPU/RSS and whether IM cache files are written.

Usage:
    python scripts/im_progress_monitor.py <pid>
"""

import glob
import os
import subprocess
import sys
import time
from datetime import datetime


PID = int(sys.argv[1]) if len(sys.argv) > 1 else None
if PID is None:
    print("Usage: python im_progress_monitor.py <pid>")
    sys.exit(1)

IM_CELF_DIR = "./results/score_cache/im_celf"
IM_DIR = "./results/score_cache/im"


def get_ps_info(pid):
    try:
        out = subprocess.check_output(
            ["ps", "-o", "etime=,pcpu=,rss=", "-p", str(pid)],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        parts = out.split()
        if len(parts) >= 3:
            return parts[0], parts[1], parts[2]
    except Exception:
        pass
    return None, None, None


def get_latest_im_cache_mtime():
    files = glob.glob(os.path.join(IM_CELF_DIR, "*.npz")) + glob.glob(
        os.path.join(IM_DIR, "*.npz")
    )
    if not files:
        return None
    return max(os.path.getmtime(f) for f in files)


def parse_etime(etime_str):
    """Parse ps etime format: [[dd-]hh:]mm:ss -> total seconds."""
    etime_str = etime_str.strip()
    days = 0
    if "-" in etime_str:
        days_part, etime_str = etime_str.split("-")
        days = int(days_part)
    parts = etime_str.split(":")
    if len(parts) == 3:
        h, m, s = map(int, parts)
    elif len(parts) == 2:
        h, m, s = 0, int(parts[0]), int(parts[1])
    else:
        h, m, s = 0, 0, int(parts[0])
    return days * 86400 + h * 3600 + m * 60 + s


def main():
    print(f"[IM Monitor] Tracking PID {PID}")
    print("[IM Monitor] Refresh every 10s. Press Ctrl+C to stop.")
    print("-" * 60)

    last_cache_mtime = get_latest_im_cache_mtime()

    while True:
        if not os.path.exists(f"/proc/{PID}"):
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] PID {PID} ended")
            break

        etime_str, cpu_pct, rss = get_ps_info(PID)
        runtime_sec = parse_etime(etime_str) if etime_str else 0

        cur_cache_mtime = get_latest_im_cache_mtime()
        cache_hint = ""
        if cur_cache_mtime and (
            last_cache_mtime is None or cur_cache_mtime > last_cache_mtime
        ):
            cache_hint = "  [CACHE WRITE DETECTED]"
            last_cache_mtime = cur_cache_mtime

        eta_str = "--"
        if runtime_sec > 2400:
            eta_str = "maybe finishing soon (<5min)"
        elif runtime_sec > 1200:
            eta_str = "maybe 5-15min left"
        elif runtime_sec > 600:
            eta_str = "maybe 15-30min left"
        elif runtime_sec > 0:
            eta_str = "uncertain, keep waiting"

        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"runtime={runtime_sec // 60}m{runtime_sec % 60}s  "
            f"CPU={cpu_pct}%  RSS={rss}KB  "
            f"ETA={eta_str}{cache_hint}",
            flush=True,
        )

        time.sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[IM Monitor] Stopped.")
