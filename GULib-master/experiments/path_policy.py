"""Fail-closed path policy for the AutoDL active OpenGU checkout."""

from __future__ import annotations

from pathlib import Path
from typing import Any


AUTODL_ACTIVE_REPO_ROOT = Path("/autodl-fs/data/OpenGU/GULib-master")


def is_autodl_active_checkout(repository_root: Path) -> bool:
    """Return whether *repository_root* is the canonical AutoDL checkout."""

    return Path(repository_root).resolve() == AUTODL_ACTIVE_REPO_ROOT


def require_active_checkout_owned(
    repository_root: Path,
    path: Path,
    label: str,
) -> Path:
    """Reject an AutoDL runtime path that escapes the active checkout."""

    root = Path(repository_root).resolve()
    resolved = Path(path).expanduser().resolve()
    if not is_autodl_active_checkout(root):
        return resolved
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            "{0} must resolve inside the AutoDL active checkout {1}; got {2}".format(
                label,
                root,
                resolved,
            )
        ) from exc
    return resolved


def resolve_owned_path(repository_root: Path, value: Any, label: str) -> Path:
    """Resolve a repository-relative path and enforce AutoDL ownership."""

    root = Path(repository_root).resolve()
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    return require_active_checkout_owned(root, path, label)
