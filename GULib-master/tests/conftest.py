"""Pytest configuration for GULib tests.

Patches sys.argv to prevent parameter_parser() from failing when config.py
is imported during test collection (config.py calls parameter_parser() at
module level, which uses argparse on sys.argv).
"""
import sys

# Save original argv and replace with minimal valid args so that
# parameter_parser() doesn't choke on pytest's own arguments.
_original_argv = sys.argv[:]
sys.argv = [sys.argv[0]]
