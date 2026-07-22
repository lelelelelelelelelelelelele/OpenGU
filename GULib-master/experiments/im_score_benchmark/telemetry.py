"""Small wall-time and process-RSS measurement helper."""

from __future__ import annotations

import threading
import time
import tracemalloc
from typing import Any, Callable, Dict, Tuple


try:
    import psutil
except ImportError:  # pragma: no cover - fallback is exercised by environments without psutil
    psutil = None


def measure_call(
    function: Callable[..., Any],
    *args: Any,
    poll_interval_seconds: float = 0.01,
    **kwargs: Any
) -> Tuple[Any, Dict[str, Any]]:
    """Return function result plus wall-time and peak-memory telemetry."""

    process = psutil.Process() if psutil is not None else None
    stop_event = threading.Event()
    peak_rss = (
        int(process.memory_info().rss) if process is not None else None
    )

    def poll() -> None:
        nonlocal peak_rss
        if process is None:
            return
        while not stop_event.wait(float(poll_interval_seconds)):
            observed = int(process.memory_info().rss)
            peak_rss = max(int(peak_rss), observed)

    monitor = threading.Thread(target=poll, daemon=True)
    tracemalloc.start()
    monitor.start()
    started = time.perf_counter()
    try:
        result = function(*args, **kwargs)
    finally:
        elapsed = time.perf_counter() - started
        stop_event.set()
        monitor.join(timeout=1.0)
        _, python_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        if process is not None:
            peak_rss = max(int(peak_rss), int(process.memory_info().rss))
    return result, {
        "wall_seconds": float(elapsed),
        "peak_rss_bytes": peak_rss,
        "python_tracemalloc_peak_bytes": int(python_peak),
        "rss_backend": "psutil_poll" if process is not None else None,
        "rss_poll_interval_seconds": (
            float(poll_interval_seconds) if process is not None else None
        ),
    }
