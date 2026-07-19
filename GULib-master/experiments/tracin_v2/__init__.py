"""Isolated, unstable TracInCP experiment utilities.

This package is intentionally not registered with the attack runner or the
Cache V2 producer registry.  It exists only for the TracIn V2 gates.
"""

from .core import (
    deployed_cross_gradient_scores,
    stable_topk,
    tracin_cp_eval_scores,
    tracin_cp_self_scores,
)

__all__ = [
    "deployed_cross_gradient_scores",
    "stable_topk",
    "tracin_cp_eval_scores",
    "tracin_cp_self_scores",
]
