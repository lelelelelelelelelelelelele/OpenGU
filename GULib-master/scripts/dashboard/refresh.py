#!/usr/bin/env python3
"""
refresh.py - generate a self-contained progress dashboard from PROGRESS.md.

Reads  self/dashboard/PROGRESS.md  (the single source of truth; this script
never edits it) and emits  self/dashboard/progress.html  -- ONE self-contained
file: no build step, no server, no framework, no external assets. Double-click
to open, works over file://.

The HTML is a *derived snapshot*. Re-run this script after editing PROGRESS.md
to regenerate it. Per self/dashboard/CLAUDE.md rule 2 (no-duplication), the
dashboard is never a second source of truth -- PROGRESS.md is. Nothing here
writes back into the markdown.

What it parses out of PROGRESS.md:
  * H1 title + "Last updated" line
  * Section 0 one-liner status (header banner)
  * Section 1 state-snapshot table  -> status cards, colored by emoji
  * Section 3 TODO framework         -> P0/P1/P2 kanban with progress bars

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
SRC = ROOT / "self" / "dashboard" / "PROGRESS.md"
OUT = ROOT / "self" / "dashboard" / "progress.html"

# leading emoji in the §1 status column -> (css class, fallback label)
STATUS_EMOJI = [
    ("\U0001F7E2", "ok",      "on track"),  # green
    ("\U0001F7E1", "warn",    "partial"),   # yellow
    ("\U0001F534", "blocked", "blocked"),   # red
    ("⏸️", "paused", "paused"),   # pause (with variation selector)
    ("⏸",      "paused", "paused"),    # pause (bare)
]


def inline_md(s: str) -> str:
    """Escape text, then render a safe subset of inline markdown to HTML."""
    s = html.escape(s, quote=False)
    # [text](target) -> a non-navigating ref chip (avoids file:// breakage)
    s = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: '<span class="ref" title="%s">%s</span>'
        % (html.escape(m.group(2), quote=True), m.group(1)),
        s,
    )
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)   # bold
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)             # inline code
    return s.strip()


def strip_md(s: str) -> str:
    """Plain-text version: drop bold/code/link markup, keep the words."""
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s.strip()


def section_body(md: str, num: int) -> str:
    """Body of '## {num}. ...' up to the next '## ' heading (or EOF)."""
    m = re.search(
        r"^##\s+%d\.\s.*?$(.*?)(?=^##\s|\Z)" % num, md, re.M | re.S
    )
    return m.group(1).strip() if m else ""


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


TIER_RE = re.compile(r"^###\s+(P\d)\s*(?:[—–-]\s*(.*))?$")
ITEM_RE = re.compile(r"^\s*-\s*\[([ xX])\]\s*(.*\S)\s*$")


def parse_todo(body: str):
    """Parse §3 into tiers, each with checkbox items + progress counts."""
    tiers, cur = [], None
    for ln in body.splitlines():
        mh = TIER_RE.match(ln.strip())
        if mh:
            cur = {"id": mh.group(1),
                   "title": strip_md((mh.group(2) or "").strip()),
                   "items": []}
            tiers.append(cur)
            continue
        mi = ITEM_RE.match(ln)
        if mi and cur is not None:
            raw = mi.group(2)
            cur["items"].append({
                "done": mi.group(1).lower() == "x",
                "blocked": "★" in raw,            # the ★ env-blocked marker
                "text": inline_md(raw.replace("★", "").strip()),
            })
    for t in tiers:
        t["done"] = sum(1 for i in t["items"] if i["done"])
        t["total"] = len(t["items"])
    return tiers


def build_data(md: str) -> dict:
    h1 = (re.search(r"^#\s+(.*)$", md, re.M) or [None, "Progress"])
    h1 = h1[1].strip() if isinstance(h1, list) else h1.group(1).strip()
    lu = re.search(r"Last updated:\s*([0-9-]+)", md)
    tiers = parse_todo(section_body(md, 3))
    done = sum(t["done"] for t in tiers)
    total = sum(t["total"] for t in tiers)
    return {
        "h1": h1,
        "last_updated": lu.group(1) if lu else "?",
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "oneLiner": clean_para(section_body(md, 0)),
        "snapshot": parse_snapshot(section_body(md, 1)),
        "tiers": tiers,
        "overall": {"done": done, "total": total},
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
  .wrap{max-width:1180px;margin:0 auto;padding:32px 24px 64px}
  code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:.86em;
    background:var(--panel2);border:1px solid var(--border);border-radius:5px;
    padding:1px 5px;color:#c9d1d9}
  .ref{border-bottom:1px dotted var(--muted);color:var(--muted);cursor:help}
  strong{color:#fff;font-weight:650}

  header{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
  h1#h1{font-size:22px;margin:0;font-weight:700;letter-spacing:.2px}
  #meta{color:var(--muted);font-size:12.5px;margin-top:4px}
  .grow{flex:1 1 240px;min-width:240px}

  .ring{--pct:0;width:118px;height:118px;border-radius:50%;flex:0 0 auto;
    background:conic-gradient(var(--accent) calc(var(--pct)*1%), var(--track) 0);
    display:grid;place-items:center;
    box-shadow:0 0 0 1px var(--border) inset}
  .ring-hole{width:90px;height:90px;border-radius:50%;background:var(--panel);
    display:grid;place-items:center;text-align:center}
  .ring-num{font-size:25px;font-weight:750;font-variant-numeric:tabular-nums}
  .ring-lbl{font-size:11px;color:var(--muted)}
  #overall-sub{font-size:12.5px;color:var(--muted);margin-top:6px;text-align:center}

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
    border-radius:999px;padding:5px 13px;font-size:12.5px;cursor:pointer;font:inherit;
    font-weight:600}
  .filters button:hover{color:var(--text);border-color:var(--muted)}
  .filters button.active{background:var(--accent);color:#04101f;border-color:var(--accent)}

  .board{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
  @media(max-width:860px){.board{grid-template-columns:1fr}}
  .col{background:var(--panel);border:1px solid var(--border);border-radius:11px;
    padding:15px 15px 6px;align-self:start}
  .col-title{font-size:14px;font-weight:650;margin-bottom:9px}
  .tier{display:inline-block;background:var(--panel2);border:1px solid var(--border);
    border-radius:6px;padding:1px 7px;font-size:12px;font-weight:750;color:var(--accent);
    margin-right:6px}
  .col-prog{display:flex;align-items:center;gap:9px;margin-bottom:12px}
  .col-prog span{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums;
    white-space:nowrap}
  .bar{flex:1;height:6px;background:var(--track);border-radius:99px;overflow:hidden}
  .bar > span{display:block;height:100%;background:var(--accent);border-radius:99px}

  .item{display:flex;gap:9px;align-items:flex-start;padding:8px 2px;
    border-top:1px solid var(--border);font-size:13.5px}
  .item:first-child{border-top:none}
  .box{flex:0 0 auto;width:17px;height:17px;border-radius:5px;border:1.5px solid var(--muted);
    display:grid;place-items:center;font-size:12px;color:#04101f;margin-top:2px;line-height:1}
  .item.done .box{background:var(--ok);border-color:var(--ok);font-weight:800}
  .item .txt{flex:1}
  .item.done .txt{color:var(--muted);text-decoration:line-through;text-decoration-color:#475061}
  .badge{flex:0 0 auto;font-size:10.5px;font-weight:700;color:var(--warn);
    border:1px solid var(--warn);border-radius:5px;padding:1px 5px;margin-top:1px;
    white-space:nowrap;letter-spacing:.03em}

  body.f-todo .item.done{display:none}
  body.f-blocked .item:not(.blocked){display:none}

  .legend{display:flex;gap:16px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin-top:16px}
  .legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;
    vertical-align:middle}
  footer{margin-top:40px;color:var(--muted);font-size:11.5px;border-top:1px solid var(--border);
    padding-top:14px}
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
        <div class="ring-num" id="ring-num"></div><div class="ring-lbl">total</div>
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
    <span class="lbl">TODO &mdash; §3</span>
    <button class="active" data-f="all">all</button>
    <button data-f="todo">open only</button>
    <button data-f="blocked">★ env-blocked</button>
  </div>
  <div class="board" id="board"></div>

  <footer>
    Derived snapshot of <code>self/dashboard/PROGRESS.md</code> &mdash; regenerate with
    <code>python scripts/dashboard/refresh.py</code>. Single source of truth stays the markdown.
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
  $('#overall-sub').textContent = o.done + '/' + o.total + ' tasks done';

  const grid = $('#snapshot'); grid.innerHTML = '';
  DATA.snapshot.forEach(r=>{
    grid.appendChild(elem('div','card '+r.cls,
      '<div class="card-head"><span class="dot"></span><span class="dim">'+esc(r.dim)+'</span></div>'+
      '<div class="status">'+r.status+'</div><div class="why">'+r.why+'</div>'));
  });

  const board = $('#board'); board.innerHTML = '';
  DATA.tiers.forEach(t=>{
    const p = t.total ? Math.round(t.done/t.total*100) : 0;
    const col = elem('div','col',
      '<div class="col-title"><span class="tier">'+esc(t.id)+'</span>'+esc(t.title)+'</div>'+
      '<div class="col-prog"><span>'+t.done+'/'+t.total+'</span>'+bar(p)+'</div>');
    const list = elem('div','list');
    t.items.forEach(it=>{
      list.appendChild(elem('div','item'+(it.done?' done':'')+(it.blocked?' blocked':''),
        '<span class="box">'+(it.done?'✓':'')+'</span>'+
        '<span class="txt">'+it.text+'</span>'+
        (it.blocked?'<span class="badge">★ env</span>':'')));
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
    ap = argparse.ArgumentParser(description="Generate progress.html from PROGRESS.md")
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
    print("  tiers: %s" % ", ".join(
        "%s %d/%d" % (t["id"], t["done"], t["total"]) for t in data["tiers"]))
    print("  overall: %d/%d done" % (o["done"], o["total"]))

    if args.open:
        webbrowser.open(OUT.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
