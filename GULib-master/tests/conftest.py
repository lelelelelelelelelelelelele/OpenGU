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

# Redirect every default generic cache consumer before constructing strategies.
_CACHE_TMP_DIR = Path(tempfile.mkdtemp(prefix="gulib-cache-v2-"))


def pytest_configure(config):
    from attack import cache_identity
    cache_identity.DEFAULT_STORE_ROOT = str(_CACHE_TMP_DIR)
