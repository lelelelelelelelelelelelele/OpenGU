"""Pytest configuration for GULib tests.

Patches sys.argv to prevent parameter_parser() from failing when config.py
is imported during test collection (config.py calls parameter_parser() at
module level, which uses argparse on sys.argv).

Also redirects the default ScoreCache directory to a per-session tmp path so
unit tests never write into ./results/score_cache.
"""
import sys
import tempfile
from pathlib import Path

# Save original argv and replace with minimal valid args so that
# parameter_parser() doesn't choke on pytest's own arguments.
_original_argv = sys.argv[:]
sys.argv = [sys.argv[0]]

# Redirect the default ScoreCache cache_dir to a tmp path before any strategy
# is constructed. Tests that pass an explicit score_cache_dir still win.
_SCORE_CACHE_TMP_DIR = Path(tempfile.mkdtemp(prefix="gulib-score-cache-"))


def pytest_configure(config):
    from attack import score_cache as _sc

    _orig_init = _sc.ScoreCache.__init__

    def _patched_init(self, namespace, cache_dir="./results/score_cache"):
        if cache_dir == "./results/score_cache":
            cache_dir = str(_SCORE_CACHE_TMP_DIR)
        _orig_init(self, namespace=namespace, cache_dir=cache_dir)

    _sc.ScoreCache.__init__ = _patched_init
