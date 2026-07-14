"""Lexical path normalization for Cache V2.

These helpers never call ``Path.resolve()``, inspect the filesystem, or use the
process working directory.  Relative paths stay relative; absolute Legacy
source paths must be supplied explicitly as absolute paths.
"""

from __future__ import unicode_literals

import ntpath
import posixpath
import re
import unicodedata
from pathlib import PurePath, PurePosixPath, PureWindowsPath

from .errors import PathValidationError


_WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")


def _text(value, label="path"):
    if isinstance(value, PurePath):
        value = str(value)
    if not isinstance(value, str):
        raise PathValidationError("{0} must be str or pathlib.PurePath".format(label))
    value = unicodedata.normalize("NFC", value)
    if not value:
        raise PathValidationError("{0} must not be empty".format(label))
    if "\x00" in value:
        raise PathValidationError("{0} contains a NUL byte".format(label))
    return value


def is_explicit_absolute_path(value):
    """Return whether *value* is lexically absolute on Windows or POSIX."""

    value = _text(value)
    return bool(
        _WINDOWS_ABSOLUTE_RE.match(value)
        or value.startswith("\\\\")
        or value.startswith("//")
        or PurePosixPath(value).is_absolute()
    )


def normalize_relative_path(value, label="relative path"):
    """Normalize a non-empty, non-traversing path to POSIX separators."""

    value = _text(value, label=label).replace("\\", "/")
    if value.startswith("/") or _WINDOWS_DRIVE_RE.match(value):
        raise PathValidationError("{0} must be relative: {1!r}".format(label, value))

    normalized_parts = []
    for part in value.split("/"):
        part = unicodedata.normalize("NFC", part)
        if part in ("", "."):
            continue
        if part == "..":
            raise PathValidationError("{0} must not traverse with '..'".format(label))
        normalized_parts.append(part)

    if not normalized_parts:
        raise PathValidationError("{0} must identify a path".format(label))
    return "/".join(normalized_parts)


def normalize_semantic_path(value):
    """Validate a provisional Artifact semantic path.

    V2.1 does not freeze a directory hierarchy.  It only guarantees that a
    supplied semantic path is portable, relative, and cannot escape its future
    ArtifactStore root.
    """

    normalized = normalize_relative_path(value, label="semantic_path")
    if any(":" in part for part in normalized.split("/")):
        raise PathValidationError("semantic_path must not contain ':'")
    return normalized


def normalize_absolute_source_path(value):
    """Normalize an explicitly absolute Legacy source path without I/O."""

    value = _text(value, label="absolute source path")
    is_windows = bool(
        _WINDOWS_DRIVE_RE.match(value)
        or value.startswith("\\\\")
        or value.startswith("//")
        or "\\" in value
    )

    if is_windows:
        if not (
            _WINDOWS_ABSOLUTE_RE.match(value)
            or value.startswith("\\\\")
            or value.startswith("//")
        ):
            raise PathValidationError(
                "Windows source path must include a rooted drive or UNC share: {0!r}".format(
                    value
                )
            )
        normalized = ntpath.normpath(value).replace("\\", "/")
        if _WINDOWS_DRIVE_RE.match(normalized):
            normalized = normalized[0].upper() + normalized[1:]
        return unicodedata.normalize("NFC", normalized)

    if not PurePosixPath(value).is_absolute():
        raise PathValidationError("source path must be explicitly absolute: {0!r}".format(value))
    return unicodedata.normalize("NFC", posixpath.normpath(value))


def normalize_recipe_path(value):
    """Return a stable ``(kind, value)`` pair for a Path in a Recipe."""

    value = _text(value, label="Recipe Path")
    if is_explicit_absolute_path(value):
        return "absolute", normalize_absolute_source_path(value)
    return "relative", normalize_relative_path(value, label="Recipe Path")


def normalize_source_path(value, path_kind, source_root=None):
    """Normalize a Legacy path according to an explicit ``PathKind`` value.

    ``path_kind`` may be the enum itself or its string value.  Relative source
    paths require an explicitly absolute ``source_root`` so they are never
    interpreted against the process working directory.
    """

    kind_value = getattr(path_kind, "value", path_kind)
    if kind_value == "relative":
        if source_root is None:
            raise PathValidationError("relative Legacy paths require an absolute source_root")
        return (
            normalize_relative_path(value, label="legacy_path"),
            normalize_absolute_source_path(source_root),
        )
    if kind_value == "absolute":
        if source_root is not None:
            raise PathValidationError("absolute Legacy paths must not also set source_root")
        return normalize_absolute_source_path(value), None
    raise PathValidationError("unknown path kind: {0!r}".format(kind_value))
