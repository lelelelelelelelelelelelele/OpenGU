"""Shared policy helpers for optional experiment metrics."""

from __future__ import annotations

from typing import Any, Mapping


_TRUE_VALUES = {"1", "true", "t", "yes", "y", "on"}
_FALSE_VALUES = {"0", "false", "f", "no", "n", "off"}


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in _TRUE_VALUES:
            return True
        if normalized in _FALSE_VALUES:
            return False
    return bool(value)


def update_detection_auc_enabled(args: Mapping[str, Any]) -> bool:
    """Return whether the posterior-change membership AUC should be computed.

    ``run_update_detection_auc`` is the canonical switch. ``run_mia`` remains
    a read-only compatibility alias for callers that construct argument
    dictionaries directly. The default stays enabled so older configs retain
    their previous behavior until they opt out explicitly.
    """

    if "run_update_detection_auc" in args:
        return _as_bool(args["run_update_detection_auc"])
    if "run_mia" in args:
        return _as_bool(args["run_mia"])
    return True


def update_detection_auc_result_value(args: Mapping[str, Any], value: Any) -> Any:
    """Normalize disabled AUC output to JSON ``null`` semantics.

    This also protects the transition period where a Legacy ResultCache hit
    may contain an AUC computed under an older configuration whose cache key
    did not include the new policy field.
    """

    return value if update_detection_auc_enabled(args) else None
