"""Read and integrity-check the curated AutoReport legacy baseline."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


BASELINE_SCHEMA = "opengu.autoreport.baseline"
BASELINE_SCHEMA_VERSION = 1


def read_baseline(path: Optional[Path]) -> Tuple[Dict[str, Any], List[str]]:
    """Load a baseline without converting it into V3 execution events."""
    if path is None or not path.exists():
        return {}, []
    warnings: List[str] = []
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, ["could not read baseline {0}: {1}".format(path, exc)]
    if not isinstance(value, dict):
        return {}, ["baseline is not an object"]
    if (
        value.get("schema") != BASELINE_SCHEMA
        or value.get("schema_version") != BASELINE_SCHEMA_VERSION
    ):
        return {}, ["unsupported baseline schema"]

    archive = value.get("archive")
    if not isinstance(archive, dict) or not archive.get("path"):
        warnings.append("baseline archive metadata is missing")
    else:
        archive_path = (path.parent / str(archive["path"])).resolve()
        if not archive_path.exists():
            if archive.get("required_local", True):
                warnings.append("baseline archive is missing: {0}".format(archive_path))
        else:
            content = archive_path.read_bytes()
            actual_sha = hashlib.sha256(content).hexdigest()
            actual_lines = len(content.decode("utf-8").splitlines())
            if archive.get("sha256") != actual_sha:
                warnings.append("baseline archive checksum mismatch")
            if archive.get("lines") != actual_lines:
                warnings.append("baseline archive line-count mismatch")

    items = value.get("items")
    if not isinstance(items, list):
        warnings.append("baseline items are missing")
        value["items"] = []
    else:
        required = {"id", "status", "title", "fact", "boundary"}
        for index, item in enumerate(items, 1):
            if not isinstance(item, dict) or not required.issubset(item):
                warnings.append("baseline item {0} is incomplete".format(index))
    return value, warnings
