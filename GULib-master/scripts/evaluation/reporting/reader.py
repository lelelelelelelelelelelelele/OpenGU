"""Compatibility readers for AutoReport v1/v2 Markdown and V3 JSONL."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .events import read_event_stream


_ENTRY_HEADING = re.compile(r"^### \[(?P<timestamp>[^\]]+)\]\s*(?P<title>.*)$")
_SESSION_HEADING = re.compile(r"^## Session\s+(?P<session>.+)$")
_FIELD_LINE = re.compile(r"^-\s*(?P<name>[^：:]+)[：:]\s*(?P<value>.*)$")


def parse_legacy_markdown(path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Parse legacy entries without normalizing or rewriting their source file."""
    records: List[Dict[str, Any]] = []
    warnings: List[str] = []
    if not path.exists():
        return records, warnings
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return records, ["could not read {0}: {1}".format(path, exc)]

    current: Optional[Dict[str, Any]] = None

    def finish() -> None:
        nonlocal current
        if current is not None:
            records.append(current)
            current = None

    for line_number, line in enumerate(lines, 1):
        session_match = _SESSION_HEADING.match(line)
        if session_match:
            finish()
            records.append(
                {
                    "schema": "opengu.autoreport.legacy",
                    "schema_version": 2,
                    "kind": "session",
                    "session": session_match.group("session").strip(),
                    "line": line_number,
                }
            )
            continue

        entry_match = _ENTRY_HEADING.match(line)
        if entry_match:
            finish()
            title = entry_match.group("title").strip()
            is_decision = "DECISION" in title.upper()
            current = {
                "schema": "opengu.autoreport.legacy",
                "schema_version": 2 if is_decision else 1,
                "kind": "decision" if is_decision else "experiment",
                "timestamp": entry_match.group("timestamp").strip(),
                "title": title,
                "fields": {},
                "line": line_number,
                "raw_lines": [line],
            }
            continue

        if current is not None:
            current["raw_lines"].append(line)
            field_match = _FIELD_LINE.match(line)
            if field_match:
                current["fields"][field_match.group("name").strip()] = field_match.group(
                    "value"
                ).strip()

    finish()
    if lines and not records:
        warnings.append("no v1/v2 entries recognized")
    return records, warnings


def load_auto_report(
    *, legacy_path: Optional[Path] = None, event_path: Optional[Path] = None
) -> Dict[str, Any]:
    legacy_records: List[Dict[str, Any]] = []
    legacy_warnings: List[str] = []
    if legacy_path is not None:
        legacy_records, legacy_warnings = parse_legacy_markdown(legacy_path)
    events, event_warnings = read_event_stream(event_path)
    return {
        "legacy_records": legacy_records,
        "events": events,
        "warnings": legacy_warnings + event_warnings,
    }
