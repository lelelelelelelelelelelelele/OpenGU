#!/usr/bin/env python3
"""
refresh.py - generate a self-contained progress dashboard from WORKPLAN.md.

Reads  self/dashboard/WORKPLAN.md  (the single source of truth; this script
never edits it) and emits  self/dashboard/progress.html  -- ONE self-contained
file: no build step, no server, no framework, no external assets. Double-click
to open, works over file://.

The HTML is a *derived snapshot*. Re-run this script after editing WORKPLAN.md
to regenerate it (a git pre-commit hook does this automatically when WORKPLAN.md
is staged). Per self/dashboard/CLAUDE.md the dashboard is never a second source
of truth -- WORKPLAN.md is. Nothing here writes back into the markdown.

What it parses out of WORKPLAN.md:
  * H1 title + "Last updated" line
  * Section 0 one-liner status            -> header banner
  * Section 1 state-snapshot table         -> status cards, colored by emoji
  * Sections "实验 / Ablation / 写作 / 画图" -> 4-stage kanban with progress bars
    (each is a markdown table; ID=col 0, task=col 1, status symbol=last col)

Usage:
    python scripts/dashboard/refresh.py
    python scripts/dashboard/refresh.py --open    # also open it in a browser

Pure standard library; runs under any Python 3.8+.
"""
from __future__ import annotations

import argparse
import datetime
import html
import json
import pathlib
import re
import sys
import webbrowser

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "self" / "dashboard" / "WORKPLAN.md"
OUT = ROOT / "self" / "dashboard" / "progress.html"

# leading emoji in the §1 status column -> (css class, fallback label)
STATUS_EMOJI = [
    ("\U0001F7E2", "ok",      "on track"),  # green
    ("\U0001F7E1", "warn",    "partial"),   # yellow
    ("\U0001F534", "blocked", "blocked"),   # red
    ("⏸️", "paused", "paused"),
    ("⏸",      "paused", "paused"),
]

# §5-§8 stage sections, matched by keyword in the H2 header.
STAGES = [
    ("实验", "实验"),
    ("ablation", "Ablation"),
    ("写作", "写作"),
    ("画图", "画图"),
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


def section_body(md: str, num: int) -> str:
    """Body of '## {num}. ...' up to the next '## ' heading (or EOF)."""
    m = re.search(r"^##\s+%d\.\s.*?$(.*?)(?=^##\s|\Z)" % num, md, re.M | re.S)
    return m.group(1).strip() if m else ""


def h2_section(md: str, keyword: str) -> str:
    """Body of the first H2 whose header text contains `keyword` (case-insensitive)."""
    m = re.search(r"^##\s+.*%s.*$" % re.escape(keyword), md, re.M | re.I)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##\s", md[start:], re.M)
    return md[start: start + nxt.start()] if nxt else md[start:]


def clean_para(body: str) -> str:
    """Collapse a section body into one line, dropping blanks and '---'."""
    keep = [ln.strip() for ln in body.splitlines()
            if ln.strip() and ln.strip() != "---"]
    return inline_md(" ".join(keep))


def parse_snapshot(body: str):
    """Parse the §1 markdown table into status-card dicts."""
    rows = []
    tlines = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    for ln in tlines[2:]:  # skip header + separator
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        dim, status, why = cells[0], cells[1], cells[2]
        cls, status_text = "warn", status
        for emo, c, lbl in STATUS_EMOJI:
            if status.startswith(emo):
                cls = c
                status_text = status[len(emo):].strip() or lbl
                break
        rows.append({
            "dim": strip_md(dim),
            "cls": cls,
            "status": inline_md(status_text),
            "why": inline_md(why),
        })
    return rows


SEP_RE = re.compile(r"^:?-{2,}:?$")


def parse_stage_items(body: str):
    """Parse a stage markdown table -> task items (ID, task html, state, blocked)."""
    items = []
    for ln in body.splitlines():
        s = ln.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        nonempty = [c for c in cells if c]
        if nonempty and all(SEP_RE.match(c) for c in nonempty):
            continue                              # separator row
        if not cells or cells[0] in ("ID", "id"):
            continue                              # header row
        if len(cells) < 2:
            continue
        idraw, taskraw, statusraw = cells[0], cells[1], cells[-1]
        if "✅" in statusraw:
            state = "done"
        elif "◐" in statusraw:
            state = "wip"
        else:
            state = "todo"
        sub = statusraw
        for ch in ("☐", "◐", "✅", "★"):
            sub = sub.replace(ch, "")
        items.append({
            "id": strip_md(idraw.replace("★", "").strip()),
            "task": inline_md(taskraw),
            "state": state,
            "blocked": "★" in s,
            "label": inline_md(sub.strip()) if sub.strip() else "",
        })
    return items


def build_stages(md: str):
    stages = []
    for kw, label in STAGES:
        items = parse_stage_items(h2_section(md, kw))
        stages.append({
            "label": label,
            "items": items,
            "done": sum(1 for i in items if i["state"] == "done"),
            "wip": sum(1 for i in items if i["state"] == "wip"),
            "total": len(items),
        })
    return stages


def build_data(md: str) -> dict:
    h1 = re.search(r"^#\s+(.*)$", md, re.M)
    lu = re.search(r"Last updated:\s*([0-9-]+)", md)
    stages = build_stages(md)
    done = sum(s["done"] for s in stages)
    wip = sum(s["wip"] for s in stages)
    total = sum(s["total"] for s in stages)
    return {
        "h1": h1.group(1).strip() if h1 else "Progress",
        "last_updated": lu.group(1) if lu else "?",
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "oneLiner": clean_para(section_body(md, 0)),
        "snapshot": parse_snapshot(section_body(md, 1)),
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
    <button data-f="blocked">★ GPU-blocked</button>
  </div>
  <div class="board" id="board"></div>

  <footer>
    Derived snapshot of <code>self/dashboard/WORKPLAN.md</code> &mdash; regenerate with
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
        (it.blocked?'<span class="badge">★ GPU</span>':'')));
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
    args = ap.parse_args(argv)

    if not SRC.exists():
        print("ERROR: source not found: %s" % SRC, file=sys.stderr)
        return 1

    md = SRC.read_text(encoding="utf-8")
    data = build_data(md)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    OUT.write_text(TEMPLATE.replace("__DATA_JSON__", payload), encoding="utf-8")

    o = data["overall"]
    print("wrote %s" % OUT)
    print("  snapshot rows: %d" % len(data["snapshot"]))
    print("  stages: %s" % ", ".join(
        "%s %d/%d" % (s["label"], s["done"], s["total"]) for s in data["stages"]))
    print("  overall: %d/%d done, %d in progress" % (o["done"], o["total"], o["wip"]))

    if args.open:
        webbrowser.open(OUT.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
