"""Build bounded human-readable AutoReport V3 status views from JSONL."""
from __future__ import annotations

import argparse
import html
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .baseline import read_baseline
from .events import (
    DEFAULT_EVENT_PATH,
    DEFAULT_STATUS_HTML_PATH,
    DEFAULT_STATUS_MD_PATH,
    read_event_stream,
)


DEFAULT_BASELINE_PATH = DEFAULT_EVENT_PATH.parent / "auto_report_baseline.json"


def _escape_md(value: Any) -> str:
    return str(value if value is not None else "-").replace("|", "\\|").replace("\n", " ")


def _identity_label(identity: Mapping[str, Any]) -> str:
    parts = [
        identity.get("dataset"),
        identity.get("model"),
        identity.get("method"),
        identity.get("strategy"),
        "seed{0}".format(identity.get("seed")) if identity.get("seed") is not None else None,
        "r{0}".format(identity.get("ratio")),
    ]
    return " / ".join(str(part) for part in parts if part not in (None, ""))


def _latest_run_events(events: Sequence[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    if not events:
        return []
    latest_run_id = events[-1].get("run_id")
    selected = [event for event in events if event.get("run_id") == latest_run_id]
    return selected or [events[-1]]


def _derive_state(events: Sequence[Mapping[str, Any]]) -> str:
    latest = list(events)
    for event in reversed(latest):
        if event.get("stage") == "run" and event.get("state") == "failed":
            return "failed"
        if event.get("stage") == "run" and event.get("state") == "completed":
            return "complete"
        if event.get("stage") == "run" and event.get("state") == "skipped":
            reason = str((event.get("metadata") or {}).get("reason") or "")
            return "legacy-skip" if "legacy" in reason.lower() else "complete (cached)"

    for event in reversed(latest):
        if event.get("state") == "failed":
            return "failed:{0}".format(event.get("stage"))
    for stage, label in (
        ("collateral", "collateral"),
        ("attack", "attack-only"),
        ("selection", "selection-only"),
    ):
        if any(event.get("stage") == stage and event.get("state") == "completed" for event in latest):
            return label
    for event in reversed(latest):
        if event.get("state") in {"started", "retrying"}:
            return "{0}:{1}".format(event.get("state"), event.get("stage"))
    return "unknown"


def _stage_summary(events: Sequence[Mapping[str, Any]]) -> str:
    latest_by_stage: Dict[str, str] = {}
    for event in events:
        latest_by_stage[str(event.get("stage"))] = str(event.get("state"))
    return ", ".join(
        "{0}={1}".format(stage, latest_by_stage[stage])
        for stage in ("selection", "attack", "collateral", "run")
        if stage in latest_by_stage
    ) or "-"


def _cache_summary(events: Sequence[Mapping[str, Any]]) -> str:
    for event in reversed(events):
        observations = event.get("cache") or []
        if not observations:
            continue
        parts = []
        for observation in observations:
            cache_type = observation.get("type", "?")
            outcome = observation.get("outcome", "unknown")
            source = observation.get("hit_source")
            text = "{0}:{1}".format(cache_type, outcome)
            if outcome == "hit" and source:
                text += "@{0}".format(Path(str(source)).name or source)
            parts.append(text)
        return ", ".join(parts)
    return "-"


def build_status_rows(
    events: Iterable[Mapping[str, Any]], max_cells: int = 200
) -> Tuple[List[Dict[str, Any]], int]:
    by_cell: Dict[str, List[Mapping[str, Any]]] = defaultdict(list)
    for event in events:
        by_cell[str(event.get("cell_id"))].append(event)

    rows: List[Dict[str, Any]] = []
    for cell_events in by_cell.values():
        latest_events = _latest_run_events(cell_events)
        latest = latest_events[-1]
        rows.append(
            {
                "updated": latest.get("timestamp", ""),
                "cell_id": latest.get("cell_id", ""),
                "identity": _identity_label(latest.get("identity") or {}),
                "state": _derive_state(latest_events),
                "stages": _stage_summary(latest_events),
                "cache": _cache_summary(latest_events),
                "run_id": latest.get("run_id", ""),
                "attempt": latest.get("attempt", 1),
                "config_fingerprint": latest.get("config_fingerprint", ""),
            }
        )
    rows.sort(key=lambda row: str(row["updated"]), reverse=True)
    total = len(rows)
    return rows[: max(1, int(max_cells))], total


def _baseline_markdown(baseline: Mapping[str, Any]) -> List[str]:
    if not baseline:
        return []
    archive = baseline.get("archive") or {}
    items = baseline.get("items") or []
    lines = [
        "## Legacy baseline",
        "",
        "The former live Markdown journal was frozen byte-for-byte. The items below are a curated carry-forward, not reconstructed V3 run events.",
        "",
        "- Archived source: `{0}`".format(archive.get("path", "-")),
        "- Integrity: `{0}`; {1} lines; {2} parsed entries".format(
            archive.get("sha256", "-"),
            archive.get("lines", "-"),
            archive.get("legacy_entries", "-"),
        ),
        "- Fixed next-step prose: retired; it is preserved only inside the archive",
        "",
        "| Status | Item | Carried-forward fact | Boundary |",
        "|---|---|---|---|",
    ]
    for item in items:
        lines.append(
            "| {status} | {title} | {fact} | {boundary} |".format(
                status=_escape_md(item.get("status")),
                title=_escape_md(item.get("title")),
                fact=_escape_md(item.get("fact")),
                boundary=_escape_md(item.get("boundary")),
            )
        )
    return lines + [""]


def _baseline_html(baseline: Mapping[str, Any]) -> str:
    if not baseline:
        return ""
    archive = baseline.get("archive") or {}
    rows = "".join(
        "<tr><td><span class=\"pill\">{status}</span></td><td>{title}</td>"
        "<td>{fact}</td><td>{boundary}</td></tr>".format(
            status=html.escape(str(item.get("status", "-"))),
            title=html.escape(str(item.get("title", "-"))),
            fact=html.escape(str(item.get("fact", "-"))),
            boundary=html.escape(str(item.get("boundary", "-"))),
        )
        for item in baseline.get("items") or []
    )
    return (
        "<section><h2>Legacy baseline</h2>"
        "<p class=\"meta\">Frozen source: <code>{path}</code> · {lines} lines · "
        "{entries} parsed entries · SHA-256 <code>{sha}</code>. Fixed next-step prose is retired.</p>"
        "<div class=\"table-wrap\"><table><thead><tr><th>Status</th><th>Item</th>"
        "<th>Carried-forward fact</th><th>Boundary</th></tr></thead><tbody>{rows}</tbody>"
        "</table></div></section>"
    ).format(
        path=html.escape(str(archive.get("path", "-"))),
        lines=html.escape(str(archive.get("lines", "-"))),
        entries=html.escape(str(archive.get("legacy_entries", "-"))),
        sha=html.escape(str(archive.get("sha256", "-"))),
        rows=rows,
    )


def render_status_markdown(
    events: Sequence[Mapping[str, Any]],
    warnings: Sequence[str],
    max_cells: int = 200,
    baseline: Optional[Mapping[str, Any]] = None,
) -> str:
    rows, total_cells = build_status_rows(events, max_cells=max_cells)
    counts = Counter(row["state"] for row in rows)
    count_text = ", ".join("{0}={1}".format(key, counts[key]) for key in sorted(counts)) or "none"
    lines = [
        "# AutoReport",
        "",
        "> Rebuildable projection of the append-only V3 event stream. This file is not the audit log.",
        "",
        "- Machine events: `{0}`".format(DEFAULT_EVENT_PATH.name),
        "- Events parsed: {0}".format(len(events)),
        "- Cells shown: {0} of {1} (bounded to {2})".format(len(rows), total_cells, max_cells),
        "- Current states: {0}".format(count_text),
        "- Parse warnings: {0}".format(len(warnings)),
        "",
    ]
    lines.extend(_baseline_markdown(baseline or {}))
    lines.extend(
        [
        "## Current V3 cells",
        "",
        "| Updated (UTC) | Cell | State | Stages | Cache | Attempt | Run | Config |",
        "|---|---|---|---|---|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| {updated} | {identity} | {state} | {stages} | {cache} | {attempt} | `{run}` | `{config}` |".format(
                updated=_escape_md(row["updated"]),
                identity=_escape_md(row["identity"]),
                state=_escape_md(row["state"]),
                stages=_escape_md(row["stages"]),
                cache=_escape_md(row["cache"]),
                attempt=row["attempt"],
                run=_escape_md(row["run_id"]),
                config=_escape_md(row["config_fingerprint"]),
            )
        )
    if not rows:
        lines.append("| - | No V3 events yet | - | - | - | - | - | - |")
    if warnings:
        lines.extend(["", "## Parse warnings", ""])
        lines.extend("- {0}".format(_escape_md(item)) for item in warnings[:20])
        if len(warnings) > 20:
            lines.append("- ... {0} more".format(len(warnings) - 20))
    lines.extend(
        [
            "",
            "Audit authority stays in `auto_report.events.jsonl`; archived v1/v2 Markdown and the curated baseline are read-only evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def render_status_html(
    events: Sequence[Mapping[str, Any]],
    warnings: Sequence[str],
    max_cells: int = 200,
    baseline: Optional[Mapping[str, Any]] = None,
) -> str:
    rows, total_cells = build_status_rows(events, max_cells=max_cells)
    counts = Counter(row["state"] for row in rows)
    cards = "".join(
        '<div class="card"><span>{0}</span><strong>{1}</strong></div>'.format(
            html.escape(state), counts[state]
        )
        for state in sorted(counts)
    ) or '<div class="card"><span>state</span><strong>none</strong></div>'
    body_rows = []
    for row in rows:
        body_rows.append(
            "<tr><td>{updated}</td><td>{identity}</td><td><span class=\"pill\">{state}</span></td>"
            "<td>{stages}</td><td>{cache}</td><td>{attempt}</td><td><code>{run}</code></td>"
            "<td><code>{config}</code></td></tr>".format(
                updated=html.escape(str(row["updated"])),
                identity=html.escape(str(row["identity"])),
                state=html.escape(str(row["state"])),
                stages=html.escape(str(row["stages"])),
                cache=html.escape(str(row["cache"])),
                attempt=html.escape(str(row["attempt"])),
                run=html.escape(str(row["run_id"])),
                config=html.escape(str(row["config_fingerprint"])),
            )
        )
    if not body_rows:
        body_rows.append('<tr><td colspan="8" class="empty">No V3 events yet.</td></tr>')
    warning_html = ""
    if warnings:
        warning_html = "<section><h2>Parse warnings</h2><ul>{0}</ul></section>".format(
            "".join("<li>{0}</li>".format(html.escape(item)) for item in warnings[:20])
        )
    template = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AutoReport</title>
<style>
:root { color-scheme: dark; --bg:#0b1020; --panel:#121a2d; --line:#26324b; --text:#e8edf7; --muted:#93a4c3; --accent:#6ee7b7; }
* { box-sizing:border-box; } body { margin:0; background:var(--bg); color:var(--text); font:14px/1.5 system-ui,Segoe UI,sans-serif; }
main { max-width:1500px; margin:auto; padding:32px; } h1 { margin:0 0 8px; font-size:30px; } .lede { color:var(--muted); margin:0 0 22px; }
.cards { display:flex; flex-wrap:wrap; gap:10px; margin:18px 0; } .card { min-width:130px; padding:12px 14px; background:var(--panel); border:1px solid var(--line); border-radius:10px; }
.card span { display:block; color:var(--muted); } .card strong { display:block; font-size:22px; color:var(--accent); }
.meta { color:var(--muted); margin:12px 0 20px; } .table-wrap { overflow:auto; border:1px solid var(--line); border-radius:12px; }
table { border-collapse:collapse; width:100%; min-width:1180px; background:var(--panel); } th,td { text-align:left; padding:11px 12px; border-bottom:1px solid var(--line); vertical-align:top; }
th { position:sticky; top:0; background:#172138; color:#b7c5df; } tr:last-child td { border-bottom:0; } code { color:#a5b4fc; }
.pill { white-space:nowrap; color:var(--accent); } .empty { color:var(--muted); text-align:center; } footer { color:var(--muted); margin-top:18px; }
section { margin:28px 0; } section table { min-width:900px; }
</style>
</head>
<body><main>
<h1>AutoReport</h1>
<p class="lede">Rebuildable projection of the append-only V3 event stream. This page is not the audit log.</p>
<div class="cards">__CARDS__</div>
<p class="meta">Events parsed: __EVENT_COUNT__ · Cells shown: __SHOWN__ of __TOTAL__ (bounded to __LIMIT__) · Parse warnings: __WARNING_COUNT__</p>
__BASELINE_HTML__
<section><h2>Current V3 cells</h2>
<div class="table-wrap"><table><thead><tr><th>Updated (UTC)</th><th>Cell</th><th>State</th><th>Stages</th><th>Cache</th><th>Attempt</th><th>Run</th><th>Config</th></tr></thead>
<tbody>__ROWS__</tbody></table></div></section>
__WARNING_HTML__
<footer>Audit authority stays in <code>auto_report.events.jsonl</code>; archived v1/v2 Markdown and the curated baseline are read-only evidence.</footer>
</main></body></html>
"""
    replacements = {
        "__CARDS__": cards,
        "__EVENT_COUNT__": str(len(events)),
        "__SHOWN__": str(len(rows)),
        "__TOTAL__": str(total_cells),
        "__LIMIT__": str(max_cells),
        "__WARNING_COUNT__": str(len(warnings)),
        "__ROWS__": "".join(body_rows),
        "__BASELINE_HTML__": _baseline_html(baseline or {}),
        "__WARNING_HTML__": warning_html,
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(".{0}.{1}.tmp".format(path.name, os.getpid()))
    with temporary.open("w", encoding="utf-8", newline="\n") as file_obj:
        file_obj.write(content)
    os.replace(str(temporary), str(path))


def write_status_views(
    *,
    event_path: Path,
    markdown_path: Path,
    html_path: Path,
    max_cells: int = 200,
    baseline_path: Optional[Path] = None,
) -> Tuple[str, str]:
    events, event_warnings = read_event_stream(event_path)
    resolved_baseline_path = baseline_path or event_path.parent / "auto_report_baseline.json"
    baseline, baseline_warnings = read_baseline(resolved_baseline_path)
    warnings = event_warnings + baseline_warnings
    markdown = render_status_markdown(
        events, warnings, max_cells=max_cells, baseline=baseline
    )
    browser = render_status_html(
        events, warnings, max_cells=max_cells, baseline=baseline
    )
    _atomic_write(markdown_path, markdown)
    _atomic_write(html_path, browser)
    return str(markdown_path), str(html_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENT_PATH)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_STATUS_MD_PATH)
    parser.add_argument("--html", type=Path, default=DEFAULT_STATUS_HTML_PATH)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE_PATH)
    parser.add_argument("--max-cells", type=int, default=200)
    args = parser.parse_args()
    markdown, browser = write_status_views(
        event_path=args.events.resolve(),
        markdown_path=args.markdown.resolve(),
        html_path=args.html.resolve(),
        max_cells=args.max_cells,
        baseline_path=args.baseline.resolve(),
    )
    print("Wrote {0}".format(markdown))
    print("Wrote {0}".format(browser))


if __name__ == "__main__":
    main()
