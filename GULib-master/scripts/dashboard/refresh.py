#!/usr/bin/env python3
"""
refresh.py - project WorkItems into WORKPLAN.md and generate its HTML dashboard.

WORKPLAN owns orchestration facts (priority, dependencies, current line and
next step).  .workblock/items/*/WORKITEM.md owns lifecycle status.  This script
joins them into the generated status region in WORKPLAN and emits
self/dashboard/progress.html.  It never copies research facts or experiment
results into either projection.

Both the status region and HTML are derived snapshots. Re-run this script after
editing orchestration nodes or WorkItem Records. Use --check in validation to
detect stale projections, broken links, duplicate mappings and lifecycle drift.

What it parses out of WORKPLAN.md:
  * H1 title + "Last updated" line
  * Section 0 one-liner status            -> header banner
  * Current node                          -> unique active-line validation
  * node tables                           -> type, priority, dependencies, owner
  * WorkItem Records                      -> lifecycle status and explicit fact owner

Usage:
    python scripts/dashboard/refresh.py
    python scripts/dashboard/refresh.py --check   # validate without writes
    python scripts/dashboard/refresh.py --open    # regenerate and open

Pure standard library; runs under any Python 3.8+.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.parse
import webbrowser
from typing import Optional

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "self" / "dashboard" / "WORKPLAN.md"
OUT = ROOT / "self" / "dashboard" / "progress.html"
WORKITEM_ROOT = ROOT / ".workblock" / "items"

STATUS_BEGIN = "<!-- WORKITEM_STATUS:BEGIN -->"
STATUS_END = "<!-- WORKITEM_STATUS:END -->"
WORKITEM_ID_RE = re.compile(r"^(?:Block|Todo) ID:\s*`?([^`\n]+)`?\s*$", re.M)
CURRENT_NODE_RE = re.compile(r"^Current node:\s*(?:\[)?(AAGU-\d+)", re.M)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

# Stage sections, matched by keyword in the H2 header.
STAGES = [
    ("修复队列", "修复"),
    ("实验 timeline", "实验"),
    ("写作", "写作"),
    ("画图", "画图"),
    ("支撑", "支撑"),
]


def inline_md(s: str) -> str:
    """Escape text, then render a safe subset of inline markdown to HTML."""
    s = html.escape(s, quote=False)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: '<span class="ref" title="%s">%s</span>'
        % (html.escape(m.group(2), quote=True), m.group(1)),
        s,
    )
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)   # bold (before italic)
    s = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", s)             # strikethrough
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)               # italic (after bold)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)             # inline code
    return s.strip()


def strip_md(s: str) -> str:
    """Plain-text version: drop bold/code/link markup, keep the words."""
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"~~([^~]+)~~", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.strip()


def _field(md: str, label: str) -> str:
    match = re.search(
        r"^%s:\s*`?([^`\n]+)`?\s*$" % re.escape(label), md, re.M
    )
    return match.group(1).strip() if match else ""


def _lifecycle_state(status: str) -> str:
    value = status.casefold()
    if "accepted" in value or "closed" in value:
        return "closed"
    if "awaiting acceptance" in value:
        return "awaiting"
    if "todo candidate" in value:
        return "todo"
    if "registered" in value and (
        "not claimed" in value or "ready after dependency" in value
    ):
        return "registered"
    if "blocked" in value:
        return "blocked"
    if "working" in value or "claimed" in value or "in progress" in value:
        return "working"
    return "unknown"


def _link_target(value: str) -> str:
    match = MARKDOWN_LINK_RE.search(value or "")
    return match.group(1).strip().strip("<>") if match else ""


def _resolved_local_link(target: str, source_path: pathlib.Path) -> Optional[pathlib.Path]:
    if not target or re.match(r"^(?:https?|mailto|obsidian):", target):
        return None
    local_target = urllib.parse.unquote(target.split("#", 1)[0])
    return (source_path.parent / local_target).resolve()


def parse_workitem(path: pathlib.Path) -> dict:
    md = path.read_text(encoding="utf-8")
    ids = {match.strip() for match in WORKITEM_ID_RE.findall(md)}
    if len(ids) != 1:
        raise ValueError("WorkItem must declare exactly one ID: %s" % path)
    code = ids.pop()
    h1 = re.search(r"^#\s+(.*)$", md, re.M)
    title = h1.group(1).strip() if h1 else code
    title = re.sub(r"^%s\s*·\s*" % re.escape(code), "", title)
    raw_status = _field(md, "当前状态")
    item_type = _field(md, "Item Type")
    if not raw_status or item_type not in {"Block", "Todo"}:
        raise ValueError("WorkItem lacks status or Item Type: %s" % path)
    fact_owner = re.search(r"^- Fact owner:\s*(.+)$", md, re.M)
    return {
        "id": code,
        "title": title,
        "raw_status": raw_status,
        "lifecycle": _lifecycle_state(raw_status),
        "item_type": item_type,
        "fact_owner_target": _link_target(
            fact_owner.group(1).strip() if fact_owner else ""
        ),
        "path": path,
    }


def load_workitems(items_root: pathlib.Path) -> dict:
    items = {}
    if not items_root.exists():
        return items
    for path in sorted(items_root.glob("*/WORKITEM.md")):
        item = parse_workitem(path)
        if item["id"] in items:
            raise ValueError("duplicate WorkItem ID: %s" % item["id"])
        items[item["id"]] = item
    return items


def _table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_plan_nodes(md: str) -> list[dict]:
    """Read orchestration node tables, never the generated status table."""
    lines = md.splitlines()
    nodes = []
    section = ""
    index = 0
    while index < len(lines):
        line = lines[index]
        heading = re.match(r"^##\s+(.*)$", line)
        if heading:
            section = heading.group(1).strip()
        if not line.strip().startswith("|"):
            index += 1
            continue
        headers = _table_cells(line)
        required = {"ID", "类型", "节点", "优先级", "前置", "Owner"}
        if not required.issubset(headers):
            index += 1
            continue
        positions = {name: headers.index(name) for name in required}
        index += 2  # header and separator
        while index < len(lines) and lines[index].strip().startswith("|"):
            cells = _table_cells(lines[index])
            if len(cells) >= len(headers):
                code = strip_md(cells[positions["ID"]])
                if re.fullmatch(r"AAGU-\d+", code):
                    dependency_text = cells[positions["前置"]]
                    nodes.append({
                        "id": code,
                        "kind": strip_md(cells[positions["类型"]]),
                        "task": cells[positions["节点"]],
                        "priority": strip_md(cells[positions["优先级"]]),
                        "dependency_text": dependency_text,
                        "dependencies": re.findall(r"AAGU-\d+", dependency_text),
                        "owner": cells[positions["Owner"]],
                        "section": section,
                        "source_index": len(nodes),
                    })
            index += 1
        continue
    return nodes


def current_node_id(md: str) -> str:
    match = CURRENT_NODE_RE.search(md)
    return match.group(1) if match else ""


def project_nodes(nodes: list[dict], items: dict, current_id: str) -> list[dict]:
    projected = []
    for node in nodes:
        item = items.get(node["id"])
        enriched = dict(node)
        if item is None:
            enriched.update({
                "projection": "missing WorkItem",
                "state": "todo",
                "blocked": True,
                "visible": True,
                "item_type": "missing",
                "lifecycle": "missing",
                "workitem_path": WORKITEM_ROOT / node["id"] / "WORKITEM.md",
            })
            projected.append(enriched)
            continue

        unresolved = [
            dependency
            for dependency in node["dependencies"]
            if dependency not in items
            or items[dependency]["lifecycle"] != "closed"
        ]
        lifecycle = item["lifecycle"]
        if lifecycle == "closed":
            projection, state, blocked = "accepted / closed", "done", False
        elif lifecycle == "awaiting":
            projection, state, blocked = "awaiting acceptance", "wip", False
        elif lifecycle == "working":
            projection, state, blocked = "in progress", "wip", False
        elif unresolved:
            projection = "blocked by %s" % ", ".join(unresolved)
            state, blocked = "todo", True
        elif item["item_type"] == "Todo":
            projection, state, blocked = "todo candidate / ready to promote", "todo", False
        elif lifecycle == "registered":
            projection, state, blocked = "registered / not claimed", "todo", False
        elif lifecycle == "blocked":
            projection, state, blocked = "blocked", "todo", True
        else:
            projection, state, blocked = item["raw_status"], "todo", False

        if node["id"] == current_id:
            projection += " / current"

        enriched.update({
            "projection": projection,
            "state": state,
            "blocked": blocked,
            "visible": not (node["kind"] == "FIX" and lifecycle == "closed"),
            "item_type": item["item_type"],
            "lifecycle": lifecycle,
            "unresolved": unresolved,
            "workitem_path": item["path"],
        })
        projected.append(enriched)
    return projected


def _priority_rank(priority: str) -> int:
    match = re.search(r"\d+", priority)
    return int(match.group()) if match else 9


def _projection_rank(node: dict, current_id: str) -> tuple:
    if node["id"] == current_id:
        group = 0
    elif node["lifecycle"] == "awaiting":
        group = 1
    elif node["blocked"]:
        group = 2
    elif node["lifecycle"] == "closed":
        group = 4
    else:
        group = 3
    return group, _priority_rank(node["priority"]), node["source_index"]


def render_status_projection(projected: list[dict], current_id: str) -> str:
    rows = [
        STATUS_BEGIN,
        "<!-- Generated by scripts/dashboard/refresh.py; lifecycle status comes from WORKITEM.md. -->",
        "| ID | 类型 | 状态投影 | 优先级 | 前置 | 唯一事实 owner |",
        "|---|---|---|---|---|---|",
    ]
    for node in sorted(projected, key=lambda value: _projection_rank(value, current_id)):
        if not node["visible"]:
            continue
        locator = pathlib.Path(
            os.path.relpath(node["workitem_path"], SRC.parent)
        ).as_posix()
        rows.append(
            "| [%s](%s) | %s | %s | %s | %s | %s |"
            % (
                node["id"], locator, node["kind"], node["projection"],
                node["priority"], node["dependency_text"], node["owner"],
            )
        )
    hidden_fixes = sum(
        1 for node in projected
        if node["kind"] == "FIX" and node["lifecycle"] == "closed"
    )
    if hidden_fixes:
        rows.append("")
        rows.append("已关闭 FIX 节点已从活动投影隐藏：%d 个；历史保留在对应 WorkItem 与 Git。" % hidden_fixes)
    rows.append(STATUS_END)
    return "\n".join(rows)


def replace_status_projection(md: str, projection: str) -> str:
    if md.count(STATUS_BEGIN) != 1 or md.count(STATUS_END) != 1:
        raise ValueError("WORKPLAN must contain exactly one generated status region")
    pattern = re.compile(
        re.escape(STATUS_BEGIN) + r".*?" + re.escape(STATUS_END), re.S
    )
    return pattern.sub(lambda _match: projection, md)


def _canonical_docmap_target(target: str) -> Optional[pathlib.Path]:
    marker = "OpenGU-DocMap/"
    normalized = target.replace("\\", "/")
    if marker not in normalized:
        return None
    relative = normalized.split(marker, 1)[1]
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-common-dir"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    common = pathlib.Path(result.stdout.strip())
    if not common.is_absolute():
        common = (ROOT / common).resolve()
    return common.parent.parent / "OpenGU-DocMap" / relative


def _broken_links(md: str, plan_path: pathlib.Path) -> list[str]:
    errors = []
    for raw_target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", md):
        target = raw_target.strip().strip("<>")
        if re.match(r"^(?:https?|mailto|obsidian):", target) or target.startswith("#"):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0])
        resolved = (plan_path.parent / target).resolve()
        if resolved == OUT.resolve():
            continue  # generated in this same refresh transaction
        if resolved.exists():
            continue
        fallback = _canonical_docmap_target(target)
        if fallback is not None and fallback.exists():
            continue
        errors.append("broken link: %s" % raw_target)
    return errors


def validate_drift(
    md: str,
    plan_path: pathlib.Path,
    nodes: list[dict],
    items: dict,
    current_id: str,
) -> list[str]:
    errors = []
    counts = {}
    for node in nodes:
        counts[node["id"]] = counts.get(node["id"], 0) + 1
    for code, count in sorted(counts.items()):
        if count > 1:
            errors.append("duplicate node mapping: %s" % code)
    for code in sorted(set(counts) - set(items)):
        errors.append("node has no WorkItem: %s" % code)
    for code in sorted(set(items) - set(counts)):
        errors.append("WorkItem is not mapped in WORKPLAN: %s" % code)
    for code, item in sorted(items.items()):
        if item["lifecycle"] == "unknown":
            errors.append("WorkItem has unknown lifecycle status: %s" % code)

    node_by_id = {}
    for node in nodes:
        node_by_id.setdefault(node["id"], node)
    if not current_id:
        errors.append("WORKPLAN has no Current node")
    elif current_id not in node_by_id or current_id not in items:
        errors.append("current node is not mapped: %s" % current_id)
    else:
        current_item = items[current_id]
        if current_item["lifecycle"] == "closed":
            errors.append("current node is already accepted/closed: %s" % current_id)
        unresolved = [
            dependency
            for dependency in node_by_id[current_id]["dependencies"]
            if dependency not in items
            or items[dependency]["lifecycle"] != "closed"
        ]
        if unresolved:
            errors.append(
                "current node has unresolved dependencies: %s -> %s"
                % (current_id, ", ".join(unresolved))
            )

    for code, node in node_by_id.items():
        item = items.get(code)
        if item is not None and item.get("fact_owner_target"):
            fact_owner = _resolved_local_link(
                item["fact_owner_target"], item["path"]
            )
            plan_owner = _resolved_local_link(
                _link_target(node["owner"]), plan_path
            )
            if fact_owner is None or plan_owner != fact_owner:
                errors.append(
                    "node owner disagrees with WorkItem fact owner: %s" % code
                )
        if item is None or item["item_type"] != "Todo" or item["lifecycle"] != "blocked":
            continue
        dependencies_closed = all(
            dependency in items and items[dependency]["lifecycle"] == "closed"
            for dependency in node["dependencies"]
        )
        if dependencies_closed:
            errors.append(
                "Todo %s remains blocked after all dependencies closed" % code
            )
    errors.extend(_broken_links(md, plan_path))
    return errors


def section_body(md: str, num: int) -> str:
    """Body of '## {num}. ...' up to the next '## ' heading (or EOF)."""
    m = re.search(r"^##\s+%d\.\s.*?$(.*?)(?=^##\s|\Z)" % num, md, re.M | re.S)
    return m.group(1).strip() if m else ""


def clean_para(body: str) -> str:
    """Collapse a section body into one line, dropping blanks and '---'."""
    keep = [ln.strip() for ln in body.splitlines()
            if ln.strip() and ln.strip() != "---"]
    return inline_md(" ".join(keep))


def build_stages(projected: list[dict]):
    stages = []
    for kw, label in STAGES:
        items = []
        for node in projected:
            if kw.casefold() not in node["section"].casefold() or not node["visible"]:
                continue
            items.append({
                "id": node["id"],
                "task": inline_md(node["task"]),
                "state": node["state"],
                "blocked": node["blocked"],
                "label": inline_md(node["projection"]),
            })
        stages.append({
            "label": label,
            "items": items,
            "done": sum(1 for i in items if i["state"] == "done"),
            "wip": sum(1 for i in items if i["state"] == "wip"),
            "total": len(items),
        })
    return stages


def build_snapshot(projected: list[dict], current_id: str) -> list[dict]:
    current = next((node for node in projected if node["id"] == current_id), None)
    blocked = sum(1 for node in projected if node["blocked"] and node["visible"])
    awaiting = sum(1 for node in projected if node["lifecycle"] == "awaiting")
    ready = sum(
        1 for node in projected
        if node["visible"] and not node["blocked"]
        and node["lifecycle"] in {"registered", "todo"}
    )
    current_text = (
        "%s · %s" % (current_id, strip_md(current["task"]))
        if current else "not mapped"
    )
    return [
        {"dim": "当前唯一线", "cls": "ok", "status": inline_md(current_text),
         "why": inline_md(current["projection"] if current else "drift")},
        {"dim": "等待验收", "cls": "warn" if awaiting else "ok",
         "status": "%d item(s)" % awaiting,
         "why": "decision required before closeout"},
        {"dim": "依赖阻塞", "cls": "blocked" if blocked else "ok",
         "status": "%d item(s)" % blocked,
         "why": "derived from WORKPLAN dependencies and WorkItem lifecycle"},
        {"dim": "可领取/Promote", "cls": "warn" if ready else "paused",
         "status": "%d item(s)" % ready,
         "why": "registration is not a claim"},
    ]


def build_data(md: str, projected: list[dict], current_id: str) -> dict:
    h1 = re.search(r"^#\s+(.*)$", md, re.M)
    lu = re.search(r"Last updated:\s*([0-9-]+)", md)
    stages = build_stages(projected)
    done = sum(s["done"] for s in stages)
    wip = sum(s["wip"] for s in stages)
    total = sum(s["total"] for s in stages)
    return {
        "h1": h1.group(1).strip() if h1 else "Progress",
        "last_updated": lu.group(1) if lu else "?",
        "generated": lu.group(1) if lu else "?",
        "oneLiner": clean_para(section_body(md, 0)),
        "snapshot": build_snapshot(projected, current_id),
        "stages": stages,
        "overall": {"done": done, "wip": wip, "total": total},
    }


TEMPLATE = r'''<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Progress</title>
<style>
  :root{
    --bg:#0d1117; --panel:#161b22; --panel2:#1c2330; --border:#2a313c;
    --text:#e6edf3; --muted:#8b949e; --accent:#6ea8fe; --track:#21262d;
    --ok:#3fb950; --warn:#d29922; --blocked:#f85149; --paused:#8b949e;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",
      "PingFang SC","Microsoft YaHei",sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased}
  a{color:var(--accent)}
  .wrap{max-width:1240px;margin:0 auto;padding:32px 24px 64px}
  code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.86em;
    background:var(--panel2);border:1px solid var(--border);border-radius:5px;
    padding:1px 5px;color:#c9d1d9}
  .ref{border-bottom:1px dotted var(--muted);color:var(--muted);cursor:help}
  strong{color:#fff;font-weight:650}
  em{font-style:italic;color:#cdd6e0}
  del{color:var(--muted);text-decoration:line-through;text-decoration-color:#5a6473}

  header{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
  h1#h1{font-size:21px;margin:0;font-weight:700;letter-spacing:.2px}
  #meta{color:var(--muted);font-size:12.5px;margin-top:4px}
  .grow{flex:1 1 240px;min-width:240px}

  .ring{--pct:0;width:118px;height:118px;border-radius:50%;flex:0 0 auto;
    background:conic-gradient(var(--accent) calc(var(--pct)*1%), var(--track) 0);
    display:grid;place-items:center;box-shadow:0 0 0 1px var(--border) inset}
  .ring-hole{width:90px;height:90px;border-radius:50%;background:var(--panel);
    display:grid;place-items:center;text-align:center}
  .ring-num{font-size:25px;font-weight:750;font-variant-numeric:tabular-nums}
  .ring-lbl{font-size:11px;color:var(--muted)}
  #overall-sub{font-size:12px;color:var(--muted);margin-top:6px;text-align:center}

  .banner{background:var(--panel);border:1px solid var(--border);border-left:3px solid var(--accent);
    border-radius:8px;padding:12px 16px;margin:18px 0 26px;font-size:14px;color:#cdd6e0}

  h2{font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);
    margin:30px 0 14px;font-weight:650}

  .snap{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:12px}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:9px;
    padding:13px 15px;border-top:2px solid var(--paused)}
  .card.ok{border-top-color:var(--ok)} .card.warn{border-top-color:var(--warn)}
  .card.blocked{border-top-color:var(--blocked)} .card.paused{border-top-color:var(--paused)}
  .card-head{display:flex;align-items:center;gap:8px;margin-bottom:5px}
  .dot{width:9px;height:9px;border-radius:50%;background:var(--paused);flex:0 0 auto}
  .card.ok .dot{background:var(--ok)} .card.warn .dot{background:var(--warn)}
  .card.blocked .dot{background:var(--blocked)} .card.paused .dot{background:var(--paused)}
  .dim{font-weight:650;font-size:14px}
  .card .status{font-size:13px;margin-bottom:6px;color:#dbe3ec}
  .card .why{font-size:12px;color:var(--muted)}

  .filters{display:flex;gap:8px;align-items:center;margin:30px 0 14px}
  .filters .lbl{font-size:13px;text-transform:uppercase;letter-spacing:.09em;color:var(--muted);
    font-weight:650;margin-right:4px}
  .filters button{background:var(--panel);color:var(--muted);border:1px solid var(--border);
    border-radius:999px;padding:5px 13px;font-size:12.5px;cursor:pointer;font:inherit;font-weight:600}
  .filters button:hover{color:var(--text);border-color:var(--muted)}
  .filters button.active{background:var(--accent);color:#04101f;border-color:var(--accent)}

  .board{display:grid;grid-template-columns:repeat(auto-fit,minmax(248px,1fr));gap:16px;align-items:start}
  .col{background:var(--panel);border:1px solid var(--border);border-radius:11px;
    padding:15px 15px 6px;align-self:start}
  .col-title{font-size:14px;font-weight:650;margin-bottom:9px}
  .col-prog{display:flex;align-items:center;gap:9px;margin-bottom:12px}
  .col-prog span{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;white-space:nowrap}
  .bar{flex:1;height:6px;background:var(--track);border-radius:99px;overflow:hidden}
  .bar > span{display:block;height:100%;background:var(--accent);border-radius:99px}

  .item{display:flex;gap:9px;align-items:flex-start;padding:9px 2px;
    border-top:1px solid var(--border);font-size:13.5px}
  .item:first-child{border-top:none}
  .box{flex:0 0 auto;width:18px;height:18px;border-radius:5px;border:1.5px solid var(--muted);
    display:grid;place-items:center;font-size:12px;color:#04101f;margin-top:1px;line-height:1}
  .item.done .box{background:var(--ok);border-color:var(--ok);font-weight:800}
  .item.wip .box{background:var(--accent);border-color:var(--accent);font-weight:800}
  .item .txt{flex:1;min-width:0}
  .tid{color:var(--accent);font-weight:750;font-size:12px;font-family:ui-monospace,Consolas,monospace}
  .item.wip .tid{color:var(--accent)}
  .item .task,.item .sub,.item code,.item .ref{
    overflow-wrap:anywhere;word-break:break-word}
  .sub{display:block;color:var(--muted);font-size:11.5px;
    white-space:normal;margin-top:4px;line-height:1.4}
  .item.done .txt{color:var(--muted);text-decoration:line-through;text-decoration-color:#475061}
  .item.done .tid{color:var(--muted)}
  .badge{flex:0 0 auto;font-size:10.5px;font-weight:700;color:var(--warn);
    border:1px solid var(--warn);border-radius:5px;padding:1px 5px;margin-top:1px;
    white-space:nowrap;letter-spacing:.03em}

  body.f-todo .item.done{display:none}
  body.f-blocked .item:not(.blocked){display:none}

  .legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:16px}
  .legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
  footer{margin-top:40px;color:var(--muted);font-size:11.5px;border-top:1px solid var(--border);padding-top:14px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="grow">
      <h1 id="h1"></h1>
      <div id="meta"></div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center">
      <div class="ring" id="ring"><div class="ring-hole">
        <div class="ring-num" id="ring-num"></div><div class="ring-lbl">done</div>
      </div></div>
      <div id="overall-sub"></div>
    </div>
  </header>

  <div class="banner" id="oneliner"></div>

  <h2>State snapshot &mdash; §1</h2>
  <div class="snap" id="snapshot"></div>
  <div class="legend">
    <span><i style="background:var(--ok)"></i>on track</span>
    <span><i style="background:var(--warn)"></i>partial</span>
    <span><i style="background:var(--blocked)"></i>blocked</span>
    <span><i style="background:var(--paused)"></i>paused</span>
  </div>

  <div class="filters">
    <span class="lbl">TODO &mdash; 阶段计划</span>
    <button class="active" data-f="all">all</button>
    <button data-f="todo">open only</button>
    <button data-f="blocked">blocked</button>
  </div>
  <div class="board" id="board"></div>

  <footer>
    Derived projection of <code>WORKPLAN.md + WORKITEM.md</code> &mdash; regenerate with
    <code>python scripts/dashboard/refresh.py</code> (auto on commit via pre-commit hook).
    Single source of truth stays the markdown.
  </footer>
</div>

<script>
const DATA = __DATA_JSON__;
const $ = (s, r=document) => r.querySelector(s);
function elem(tag, cls, htmlStr){const e=document.createElement(tag);
  if(cls)e.className=cls; if(htmlStr!=null)e.innerHTML=htmlStr; return e;}
function bar(pct){return '<div class="bar"><span style="width:'+pct+'%"></span></div>';}
function esc(s){const d=document.createElement('div'); d.textContent=s; return d.innerHTML;}

function render(){
  $('#h1').textContent = DATA.h1;
  $('#meta').textContent = 'source updated ' + DATA.last_updated +
    '  ·  snapshot generated ' + DATA.generated;
  $('#oneliner').innerHTML = DATA.oneLiner;

  const o = DATA.overall, pct = o.total ? Math.round(o.done/o.total*100) : 0;
  $('#ring').style.setProperty('--pct', pct);
  $('#ring-num').textContent = pct + '%';
  $('#overall-sub').textContent = o.done + '/' + o.total + ' done' +
    (o.wip ? '  ·  ' + o.wip + ' in progress' : '');

  const grid = $('#snapshot'); grid.innerHTML = '';
  DATA.snapshot.forEach(r=>{
    grid.appendChild(elem('div','card '+r.cls,
      '<div class="card-head"><span class="dot"></span><span class="dim">'+esc(r.dim)+'</span></div>'+
      '<div class="status">'+r.status+'</div><div class="why">'+r.why+'</div>'));
  });

  const board = $('#board'); board.innerHTML = '';
  DATA.stages.forEach(st=>{
    const p = st.total ? Math.round(st.done/st.total*100) : 0;
    const prog = st.done + '/' + st.total + (st.wip ? '  ·  ' + st.wip + '◐' : '');
    const col = elem('div','col',
      '<div class="col-title">'+esc(st.label)+'</div>'+
      '<div class="col-prog"><span>'+prog+'</span>'+bar(p)+'</div>');
    const list = elem('div','list');
    st.items.forEach(it=>{
      const cls = 'item'+(it.state==='done'?' done':'')+(it.state==='wip'?' wip':'')+
        (it.blocked?' blocked':'');
      const mark = it.state==='done'?'✓':(it.state==='wip'?'◐':'');
      list.appendChild(elem('div',cls,
        '<span class="box">'+mark+'</span>'+
        '<span class="txt"><span class="task"><span class="tid">'+esc(it.id)+'</span> '+it.task+'</span>'+
        (it.label?'<span class="sub">'+it.label+'</span>':'')+'</span>'+
        (it.blocked?'<span class="badge">blocked</span>':'')));
    });
    col.appendChild(list);
    board.appendChild(col);
  });
}

document.querySelectorAll('.filters button').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.body.classList.remove('f-todo','f-blocked');
    const f = b.dataset.f;
    if(f==='todo') document.body.classList.add('f-todo');
    if(f==='blocked') document.body.classList.add('f-blocked');
    document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
  });
});
render();
</script>
</body>
</html>
'''


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate progress.html from WORKPLAN.md")
    ap.add_argument("--open", action="store_true", help="open the result in a browser")
    ap.add_argument("--check", action="store_true", help="validate projections without writing")
    args = ap.parse_args(argv)

    if not SRC.exists():
        print("ERROR: source not found: %s" % SRC, file=sys.stderr)
        return 1

    md = SRC.read_text(encoding="utf-8")
    try:
        items = load_workitems(WORKITEM_ROOT)
        nodes = parse_plan_nodes(md)
        current_id = current_node_id(md)
        projected = project_nodes(nodes, items, current_id)
        expected_md = replace_status_projection(
            md, render_status_projection(projected, current_id)
        )
        errors = validate_drift(
            expected_md, SRC, nodes, items, current_id
        )
    except (OSError, ValueError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print("DRIFT: %s" % error, file=sys.stderr)
        return 2

    data = build_data(expected_md, projected, current_id)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    expected_html = TEMPLATE.replace("__DATA_JSON__", payload)

    if args.check:
        stale = []
        if md != expected_md:
            stale.append("WORKPLAN generated status region is stale")
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != expected_html:
            stale.append("progress.html is stale")
        if stale:
            for error in stale:
                print("DRIFT: %s" % error, file=sys.stderr)
            return 2
        print("dashboard projection check: PASS")
        return 0

    if md != expected_md:
        SRC.write_text(expected_md, encoding="utf-8")
    OUT.write_text(expected_html, encoding="utf-8")

    o = data["overall"]
    print("wrote %s" % OUT)
    print("  WorkItems: %d; mapped nodes: %d" % (len(items), len(nodes)))
    print("  snapshot rows: %d" % len(data["snapshot"]))
    print("  stages: %s" % ", ".join(
        "%s %d/%d" % (s["label"], s["done"], s["total"]) for s in data["stages"]))
    print("  overall: %d/%d done, %d in progress" % (o["done"], o["total"], o["wip"]))

    if args.open:
        webbrowser.open(OUT.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
