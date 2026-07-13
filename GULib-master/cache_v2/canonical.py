"""Canonical Recipe serialization and stable SHA-256 hashing."""

from __future__ import unicode_literals

import hashlib
import json
import math
import re
import unicodedata
from collections.abc import Mapping
from enum import Enum
from pathlib import PurePath

from .errors import CanonicalizationError, ForbiddenRecipeFieldError
from .paths import normalize_recipe_path


TYPE_TAG = "$cache_v2_type"

# Experiment/config ownership and presentation fields never participate in an
# Artifact identity.  Strict rejection is deliberate: silently accepting a
# full experiment config would make callers believe those fields were hashed.
FORBIDDEN_RECIPE_FIELDS = frozenset(
    {
        "config",
        "full_config",
        "effective_config",
        "experiment_config",
        "config_name",
        "config_path",
        "yaml",
        "yaml_path",
        "yaml_file",
        "yaml_name",
        "yaml_config",
        "experiment_id",
        "experiment_name",
        "experiment_display_name",
        "batch",
        "batch_id",
        "batch_name",
        "submission_id",
        "report",
        "report_path",
        "report_name",
        "root_path",
        "root_dir",
        "project_root",
        "workspace_root",
        "working_directory",
        "cwd",
        "output_path",
        "output_dir",
        "result_path",
        "results_path",
        "log_path",
        "log_dir",
        "cache_path",
        "cache_dir",
        "checkpoint_path",
        "checkpoint_dir",
        "run_id",
        "run_name",
        "display_name",
        "hostname",
        "machine_name",
        "cuda",
        "gpu",
        "gpu_id",
        "device",
    }
)


def _normalized_text(value):
    return unicodedata.normalize("NFC", value)


def _normalized_field_name(value):
    normalized = _normalized_text(value).strip()
    normalized = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", normalized)
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", normalized)
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", normalized)
    return normalized.strip("_").lower()


def find_forbidden_recipe_fields(value, path="$"):
    """Return all recursively nested forbidden field paths."""

    found = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                # Canonicalization reports the more specific key-type error.
                continue
            key_nfc = _normalized_text(key)
            child_path = "{0}.{1}".format(path, key_nfc)
            if _normalized_field_name(key_nfc) in FORBIDDEN_RECIPE_FIELDS:
                found.append(child_path)
            found.extend(find_forbidden_recipe_fields(child, child_path))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            found.extend(find_forbidden_recipe_fields(child, "{0}[{1}]".format(path, index)))
    return found


def reject_forbidden_recipe_fields(value):
    fields = find_forbidden_recipe_fields(value)
    if fields:
        raise ForbiddenRecipeFieldError(fields)


def canonicalize(value):
    """Convert supported values into an unambiguous JSON-compatible form.

    Mappings and sequences are tagged too, preventing a user-supplied mapping
    from colliding with the tagged representation of a float, Path, or Enum.
    """

    if value is None:
        return None
    if isinstance(value, Enum):
        enum_class = value.__class__
        enum_type = _normalized_text(
            "{0}.{1}".format(enum_class.__module__, enum_class.__qualname__)
        )
        return {
            TYPE_TAG: "enum",
            "enum_type": enum_type,
            "value": canonicalize(value.value),
        }
    if isinstance(value, PurePath):
        path_kind, normalized = normalize_recipe_path(value)
        return {TYPE_TAG: "path", "path_kind": path_kind, "value": normalized}
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise CanonicalizationError("non-finite floats are forbidden in Artifact Recipes")
        if value == 0.0:
            value = 0.0  # normalize negative zero
        return {TYPE_TAG: "float", "hex": value.hex()}
    if isinstance(value, str):
        return _normalized_text(value)
    if isinstance(value, Mapping):
        items = []
        seen_keys = set()
        for key, child in value.items():
            if not isinstance(key, str):
                raise CanonicalizationError(
                    "Artifact Recipe mapping keys must be strings, got {0}".format(
                        type(key).__name__
                    )
                )
            normalized_key = _normalized_text(key)
            if normalized_key in seen_keys:
                raise CanonicalizationError(
                    "mapping contains duplicate keys after Unicode NFC normalization: {0!r}".format(
                        normalized_key
                    )
                )
            seen_keys.add(normalized_key)
            items.append((normalized_key, canonicalize(child)))
        items.sort(key=lambda item: item[0])
        return {TYPE_TAG: "mapping", "items": [[key, child] for key, child in items]}
    if isinstance(value, list):
        return {TYPE_TAG: "list", "items": [canonicalize(child) for child in value]}
    if isinstance(value, tuple):
        return {TYPE_TAG: "tuple", "items": [canonicalize(child) for child in value]}
    if isinstance(value, (set, frozenset)):
        raise CanonicalizationError("sets are unordered and forbidden in Artifact Recipes")
    raise CanonicalizationError(
        "unsupported Artifact Recipe value type: {0}".format(type(value).__name__)
    )


def canonical_json(value):
    """Return the canonical JSON text for *value*."""

    return json.dumps(
        canonicalize(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_bytes(value):
    """Return canonical UTF-8 bytes for *value*."""

    return canonical_json(value).encode("utf-8")


def canonical_sha256(value):
    """Return the full lowercase SHA-256 of the canonical form of *value*."""

    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(payload):
    """Return the full lowercase SHA-256 for raw bytes-like payload content."""

    if not isinstance(payload, (bytes, bytearray, memoryview)):
        raise CanonicalizationError("sha256_bytes requires a bytes-like payload")
    return hashlib.sha256(bytes(payload)).hexdigest()
