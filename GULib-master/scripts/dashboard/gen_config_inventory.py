#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate self/dashboard/config_inventory.html (coverage-heatmap view) from
self/dashboard/config_inventory.csv.

Single source of truth = the CSV. Every roll-up (per-category bar, per-track
summary, by-dataset, overall %, done/partial/not-started counts) is DERIVED in
the page's JS from the injected config list — so to refresh progress you only
ever edit ONE thing: the `done` column of the CSV. Then:

    E:/conda_package/envs/gnn/python.exe scripts/dashboard/gen_config_inventory.py

CSV columns (header order):
    file,name,cat,dataset,model,ratio,hybrid_alpha,n_methods,n_strategies,
    n_seeds,n_cells,done,src,methods,strategies,seeds

`cat` long names are mapped to short block keys (CORA/ARXIV/A3/A5/A6/SANITY).
"""
import csv
import datetime
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
# scripts/dashboard/gen_config_inventory.py -> repo root is two parents up
ROOT = HERE.parents[2]
CSV_PATH = ROOT / "self" / "dashboard" / "config_inventory.csv"
OUT_PATH = ROOT / "self" / "dashboard" / "config_inventory.html"

CAT_MAP = {
    "main-matrix (cora)": "CORA",
    "main-matrix (arxiv)": "ARXIV",
    "ablation A3 (alpha)": "A3",
    "ablation A5 (ratio/dataset)": "A5",
    "ablation A6 (backbone)": "A6",
    "sanity": "SANITY",
}


def js_str(s: str) -> str:
    s = "" if s is None else str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def js_int(s: str) -> str:
    s = (s or "").strip()
    return str(int(float(s))) if s not in ("", "None") else "0"


def build_configs_array(rows):
    lines = []
    for r in rows:
        cat_raw = (r.get("cat") or "").strip()
        catkey = CAT_MAP.get(cat_raw)
        if catkey is None:
            raise SystemExit(f"[gen] unknown cat value: {cat_raw!r} (row {r.get('file')})")
        alpha = (r.get("hybrid_alpha") or "").strip()
        alpha_js = ('"%.2f"' % float(alpha)) if alpha not in ("", "None") else "null"
        obj = (
            "  {file:%s, name:%s, cat:%s, ds:%s, model:%s, ratio:%s, alpha:%s, "
            "nm:%s,ns:%s,nse:%s, total:%s, done:%s, src:%s, methods:%s, strategies:%s, seeds:%s},"
            % (
                js_str(r["file"]), js_str(r["name"]), js_str(catkey), js_str(r["dataset"]),
                js_str(r["model"]), js_str(r["ratio"]), alpha_js,
                js_int(r["n_methods"]), js_int(r["n_strategies"]), js_int(r["n_seeds"]),
                js_int(r["n_cells"]), js_int(r["done"]), js_str(r["src"]),
                js_str(r["methods"]), js_str(r["strategies"]), js_str(r["seeds"]),
            )
        )
        lines.append(obj)
    return "\n".join(lines)


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"[gen] CSV not found: {CSV_PATH}")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit("[gen] CSV has no data rows")

    configs_js = build_configs_array(rows)
    today = datetime.date.today().isoformat()
    nconfigs = len(rows)

    # quick console summary (sanity for the operator)
    done = sum(int(float(r["done"] or 0)) for r in rows)
    total = sum(int(float(r["n_cells"] or 0)) for r in rows)
    print(f"[gen] {nconfigs} configs · {done}/{total} cells done · -> {OUT_PATH.relative_to(ROOT)}")

    html = (
        TEMPLATE
        .replace("/*__CONFIGS__*/", configs_js)
        .replace("__GENERATED_DATE__", today)
        .replace("__NCONFIGS__", str(nconfigs))
    )
    OUT_PATH.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# TEMPLATE — coverage-heatmap page. The CONFIGS array is injected; everything
# else (blocks, summary, percentages, status counts) is derived in JS so a
# single edit to the CSV propagates everywhere. Do not use str.format on this
# (it contains literal { } from CSS/JS); only the explicit .replace() tokens
# above are substituted.
# ---------------------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Experiment Config Inventory · Coverage Heatmap</title>
<style>
  :root{
    --bg:#0d1117; --panel:#161b22; --panel2:#1c2330; --border:#2a313c; --text:#e6edf3;
    --muted:#8b949e; --accent:#6ea8fe; --track:#21262d;
    --ok:#3fb950; --warn:#d29922; --blocked:#f85149; --paused:#6e7681;
    --ok-dim:#1c3a26; --warn-dim:#3a2f12; --blocked-dim:#3a1c1c;
    --radius:10px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    background:var(--bg); color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
    font-size:13px; line-height:1.45;
    -webkit-font-smoothing:antialiased;
    padding:22px 26px 60px;
  }
  .mono{font-family:ui-monospace,Consolas,monospace;}
  .num{font-variant-numeric:tabular-nums; font-feature-settings:"tnum";}

  /* ---- Title bar ---- */
  header.titlebar{
    display:flex; align-items:baseline; justify-content:space-between;
    gap:18px; flex-wrap:wrap;
    border-bottom:1px solid var(--border); padding-bottom:14px; margin-bottom:18px;
  }
  .titlebar h1{
    font-size:21px; font-weight:650; margin:0; letter-spacing:-0.2px;
    display:flex; align-items:center; gap:10px;
  }
  .titlebar h1 .tag{
    font-size:10px; font-weight:600; letter-spacing:.5px; text-transform:uppercase;
    color:var(--accent); border:1px solid #2c4a78; background:#16243b;
    padding:2px 7px; border-radius:20px; position:relative; top:-2px;
  }
  .titlebar .sub{
    color:var(--muted); font-size:11.5px; margin-top:5px;
    font-family:ui-monospace,Consolas,monospace;
  }
  .titlebar .sub b{color:#b9c4d0; font-weight:600;}

  /* ---- Summary strip ---- */
  .summary{
    display:grid; grid-template-columns: minmax(280px,1.1fr) minmax(260px,1fr) minmax(300px,1.3fr);
    gap:14px; margin-bottom:22px;
  }
  @media(max-width:1100px){ .summary{grid-template-columns:1fr;} }
  .card{
    background:var(--panel); border:1px solid var(--border); border-radius:var(--radius);
    padding:13px 15px;
  }
  .card h3{
    margin:0 0 10px; font-size:10.5px; font-weight:600; letter-spacing:.6px;
    text-transform:uppercase; color:var(--muted);
    display:flex; align-items:center; justify-content:space-between;
  }
  .card h3 .pct{color:var(--text); font-weight:650; font-size:11px;}

  /* big global figure */
  .global{display:flex; align-items:baseline; gap:10px; margin-bottom:10px;}
  .global .big{font-size:30px; font-weight:700; letter-spacing:-1px;}
  .global .big small{font-size:15px; color:var(--muted); font-weight:500;}
  .global .delta{font-size:12px; color:var(--warn); font-weight:600;}
  .gbar{height:8px; border-radius:5px; background:var(--track); overflow:hidden; display:flex;}
  .gbar i{display:block; height:100%;}

  /* category / dataset mini rows */
  .rollrow{display:flex; align-items:center; gap:8px; margin:5px 0; font-size:11.5px;}
  .rollrow .lbl{flex:0 0 132px; color:#c2ccd6; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  .rollrow .mini{flex:1; height:7px; border-radius:4px; background:var(--track); overflow:hidden;}
  .rollrow .mini i{display:block; height:100%;}
  .rollrow .val{flex:0 0 70px; text-align:right; color:var(--muted);}
  .rollrow .val b{color:var(--text);}

  .caveat{
    font-size:11px; color:#b9b07a; line-height:1.5;
    background:var(--warn-dim); border:1px solid #4a3d14; border-radius:8px;
    padding:9px 11px;
  }
  .caveat b{color:#e8d98e;}
  .caveat .k{font-family:ui-monospace,Consolas,monospace; color:#f0e6a8;}

  /* ---- Controls ---- */
  .controls{
    display:flex; align-items:center; gap:14px; flex-wrap:wrap;
    margin-bottom:16px; padding:10px 13px;
    background:var(--panel); border:1px solid var(--border); border-radius:var(--radius);
  }
  .controls .grp{display:flex; align-items:center; gap:8px;}
  .controls label{font-size:11px; color:var(--muted); user-select:none; cursor:pointer; display:flex; align-items:center; gap:6px;}
  .controls input[type=checkbox]{accent-color:var(--accent); width:14px; height:14px; cursor:pointer;}
  .seg{display:flex; border:1px solid var(--border); border-radius:7px; overflow:hidden;}
  .seg button{
    background:transparent; color:var(--muted); border:none; padding:5px 11px;
    font-size:11px; cursor:pointer; font-family:inherit; border-right:1px solid var(--border);
  }
  .seg button:last-child{border-right:none;}
  .seg button.active{background:var(--panel2); color:var(--text); box-shadow:inset 0 -2px 0 var(--accent);}
  .controls .spacer{flex:1;}
  .controls .count-hint{font-size:11px; color:var(--muted); font-family:ui-monospace,Consolas,monospace;}
  .controls .count-hint b{color:var(--text);}

  /* ---- Legend ---- */
  .legend{
    display:flex; align-items:center; gap:18px; flex-wrap:wrap;
    font-size:11px; color:var(--muted);
  }
  .legend .item{display:flex; align-items:center; gap:6px;}
  .legend .sw{width:13px; height:13px; border-radius:3px; border:1px solid rgba(255,255,255,.12);}
  .legend .prov{display:inline-flex; align-items:center; gap:5px;}
  .legend .dot{
    width:15px; height:15px; border-radius:4px; display:inline-grid; place-items:center;
    font-size:9px; font-weight:700; font-family:ui-monospace,Consolas,monospace; color:#0d1117;
  }

  /* ---- Blocks ---- */
  .block{margin-bottom:24px;}
  .block-head{
    display:flex; align-items:center; gap:11px; margin:0 0 11px; padding-bottom:7px;
    border-bottom:1px dashed var(--border);
  }
  .block-head .name{font-size:14px; font-weight:650; letter-spacing:-.2px;}
  .block-head .badge{
    font-size:10px; font-family:ui-monospace,Consolas,monospace; color:var(--muted);
    border:1px solid var(--border); border-radius:20px; padding:2px 9px; background:var(--panel);
  }
  .block-head .badge b{color:var(--text);}
  .block-head .blockbar{
    flex:0 0 130px; height:6px; border-radius:4px; background:var(--track); overflow:hidden; margin-left:auto;
  }
  .block-head .blockbar i{display:block; height:100%;}
  .block-head .blockpct{font-size:11px; color:var(--muted); font-family:ui-monospace,Consolas,monospace; flex:0 0 auto;}
  .block-head .blockpct b{color:var(--text);}

  .subgroup-label{
    font-size:10px; letter-spacing:.5px; text-transform:uppercase; color:var(--muted);
    margin:6px 0 7px; font-family:ui-monospace,Consolas,monospace;
  }
  .grid{
    display:grid; gap:11px;
    grid-template-columns:repeat(auto-fill, minmax(218px,1fr));
  }
  .grid.cols4{grid-template-columns:repeat(4, minmax(170px,1fr));}
  @media(max-width:900px){ .grid.cols4{grid-template-columns:repeat(2,1fr);} }

  /* ---- Tile ---- */
  .tile{
    position:relative; background:var(--panel); border:1px solid var(--border);
    border-radius:var(--radius); padding:12px 13px 13px; overflow:hidden;
    transition:transform .12s ease, box-shadow .12s ease, border-color .12s ease;
    cursor:default;
  }
  .tile:hover{transform:translateY(-2px); box-shadow:0 8px 22px rgba(0,0,0,.45); border-color:#3a4452; z-index:3;}
  /* left status spine */
  .tile::before{
    content:""; position:absolute; left:0; top:0; bottom:0; width:4px;
    background:var(--status); opacity:.9;
  }
  /* faint fill wash from bottom encoding completion */
  .tile .wash{
    position:absolute; left:0; right:0; bottom:0; pointer-events:none;
    background:linear-gradient(180deg, transparent, var(--washcol));
    opacity:.16;
  }
  .tile-status-ok{--status:var(--ok); --washcol:var(--ok);}
  .tile-status-partial{--status:var(--warn); --washcol:var(--warn);}
  .tile-status-blocked{--status:var(--blocked); --washcol:var(--blocked);}

  .tile .tname{
    font-family:ui-monospace,Consolas,monospace; font-size:11.5px; font-weight:600;
    color:var(--text); margin:0 0 9px; padding-right:20px; word-break:break-all; line-height:1.3;
    position:relative; z-index:1;
  }
  .tile .frac{
    display:flex; align-items:baseline; gap:6px; position:relative; z-index:1; margin-bottom:8px;
  }
  .tile .frac .d{font-size:22px; font-weight:700; letter-spacing:-.5px;}
  .tile .frac .t{font-size:13px; color:var(--muted); font-weight:500;}
  .tile .frac .p{margin-left:auto; font-size:11px; font-weight:600; color:var(--muted); font-family:ui-monospace,Consolas,monospace;}
  .tile.tile-status-ok .frac .d{color:var(--ok);}
  .tile.tile-status-ok .frac .p{color:var(--ok);}
  .tile.tile-status-partial .frac .d{color:var(--warn);}
  .tile.tile-status-partial .frac .p{color:var(--warn);}
  .tile.tile-status-blocked .frac .d{color:#e6edf3;}
  .tile.tile-status-blocked .frac .p{color:var(--blocked);}

  .tile .fillbar{height:6px; border-radius:4px; background:var(--track); overflow:hidden; margin-bottom:10px; position:relative; z-index:1;}
  .tile .fillbar i{display:block; height:100%; background:var(--status);}

  .chips{display:flex; flex-wrap:wrap; gap:5px; position:relative; z-index:1;}
  .chip{
    font-size:9.5px; font-family:ui-monospace,Consolas,monospace; color:#c2ccd6;
    background:var(--panel2); border:1px solid var(--border); border-radius:5px; padding:1.5px 6px;
    white-space:nowrap;
  }
  .chip.ds{color:#aaccff; border-color:#2c4a78;}
  .chip.shape{color:var(--muted);}

  /* provenance corner badge */
  .tile .prov{
    position:absolute; top:10px; right:10px; z-index:2;
    width:16px; height:16px; border-radius:4px; display:grid; place-items:center;
    font-size:9px; font-weight:700; font-family:ui-monospace,Consolas,monospace; color:#0d1117;
  }
  .prov-csv{background:var(--accent);}
  .prov-disk{background:var(--paused);}

  /* hover detail popover */
  .tile .detail{
    position:absolute; left:10px; right:10px; bottom:10px; z-index:5;
    background:#0b0f16; border:1px solid #3a4452; border-radius:8px;
    padding:9px 10px; font-size:10px; line-height:1.55;
    opacity:0; transform:translateY(6px); pointer-events:none;
    transition:opacity .13s ease, transform .13s ease;
    box-shadow:0 10px 26px rgba(0,0,0,.6);
  }
  .tile:hover .detail{opacity:1; transform:translateY(0);}
  .detail .row{display:flex; gap:7px; margin-bottom:3px;}
  .detail .row:last-child{margin-bottom:0;}
  .detail .row .k{flex:0 0 56px; color:var(--muted); text-transform:uppercase; letter-spacing:.3px; font-size:8.5px; padding-top:1px;}
  .detail .row .v{flex:1; font-family:ui-monospace,Consolas,monospace; color:#d4dce4; word-break:break-word;}
  .detail .row .v.acc{color:var(--accent);}

  /* hidden state for filter */
  .tile.is-hidden{display:none;}
  .subgroup.is-empty{display:none;}
  .block.is-empty{display:none;}

  /* footer */
  footer{
    margin-top:34px; padding-top:16px; border-top:1px solid var(--border);
    color:var(--muted); font-size:11px; line-height:1.7;
  }
  footer .fhead{font-size:10px; letter-spacing:.6px; text-transform:uppercase; color:#71798a; margin-bottom:7px;}
  footer code{font-family:ui-monospace,Consolas,monospace; color:#aab4c0; background:var(--panel2); padding:1px 5px; border-radius:4px;}
  footer .note{margin-top:9px; padding-left:13px; border-left:2px solid #3a4452; color:#9aa4b0;}
  footer b{color:#c2ccd6;}
</style>
</head>
<body>

<header class="titlebar">
  <div>
    <h1>Experiment Config Inventory <span class="tag">Coverage Heatmap</span></h1>
    <div class="sub">__NCONFIGS__ configs · join: <b>_phase_b_aggregate.csv</b> (cora) + disk scan (arxiv) · source <b>experiments/configs/</b> · generated __GENERATED_DATE__</div>
  </div>
</header>

<!-- ============ SUMMARY STRIP (derived in JS from CONFIGS) ============ -->
<section class="summary" id="summary"></section>

<!-- ============ CONTROLS + LEGEND ============ -->
<div class="controls">
  <div class="grp">
    <span style="font-size:10px; letter-spacing:.5px; text-transform:uppercase; color:var(--muted);">Filter</span>
    <label><input type="checkbox" id="hideComplete"> 隐藏已完成 hide 100%</label>
    <label><input type="checkbox" id="onlyRed"> 仅看红 only 0%</label>
  </div>
  <div class="grp">
    <span style="font-size:10px; letter-spacing:.5px; text-transform:uppercase; color:var(--muted);">Provenance</span>
    <div class="seg" id="provSeg">
      <button data-prov="all" class="active">all</button>
      <button data-prov="csv">csv</button>
      <button data-prov="disk">disk</button>
    </div>
  </div>
  <div class="spacer"></div>
  <div class="count-hint">showing <b id="shownCount" class="num">0</b> / <span id="totalCount" class="num">0</span> configs</div>
</div>

<div class="controls legend" style="margin-top:-6px;">
  <div class="item"><span class="sw" style="background:var(--ok);"></span> complete · 100% done</div>
  <div class="item"><span class="sw" style="background:var(--warn);"></span> partial · 1–99%</div>
  <div class="item"><span class="sw" style="background:var(--blocked);"></span> not started · 0%</div>
  <span style="color:#4a525e;">|</span>
  <div class="prov"><span class="dot prov-csv">C</span> <span>csv — from <code style="font-family:ui-monospace,Consolas,monospace;">_phase_b_aggregate.csv</code></span></div>
  <div class="prov"><span class="dot prov-disk">D</span> <span>disk — scanned from <code style="font-family:ui-monospace,Consolas,monospace;">results/runs/</code></span></div>
  <span style="color:#4a525e;">|</span>
  <div class="item" style="color:#71798a;">tile fill = done/total at <b style="color:#9aa4b0;">config granularity</b> (no per-cell state)</div>
</div>

<!-- ============ HEATMAP BLOCKS ============ -->
<main id="board"></main>

<footer>
  <div class="fhead">Provenance &amp; legend</div>
  <div>
    <b>src</b> column: <code>csv</code> = completion read from <code>results/_phase_b_aggregate.csv</code>
    (cora main results) · <code>disk</code> = cell count scanned from <code>results/runs/</code>
    (arxiv + non-cora; not in the aggregate CSV). Source of configs:
    <code>experiments/configs/</code>. Status mapping: <b style="color:var(--ok);">complete</b> /
    <b style="color:var(--warn);">partial</b> / <b style="color:var(--blocked);">not-started</b>.
  </div>
  <div class="note">
    <b>arxiv (ogbn-arxiv) is GPU-bound</b> — the TracIn G-matrix and collateral retrain need an
    80&nbsp;GB GPU (H800/A100) and cannot run on the local card, so they are deferred to a remote
    machine; this is why the arxiv main matrix is stalled. The cora ablations (A3 / A6 / A5-cora)
    are <b>not GPU-blocked — they are simply not started yet.</b>
  </div>
  <div class="note" style="border-color:#2c4a78; color:#9bb4d8;">
    <b>Refresh after a run finishes:</b> update the <code>done</code> column in
    <code>self/dashboard/config_inventory.csv</code>, then run
    <code>python scripts/dashboard/gen_config_inventory.py</code> — every bar, percentage and
    status count is re-derived from the CSV automatically.
  </div>
</footer>

<script>
"use strict";

/* ---- authoritative data (config granularity only; injected from CSV) ---- */
const CONFIGS = [
/*__CONFIGS__*/
];

/* ---- block metadata: order + labels only; numbers are DERIVED ---- */
const BLOCK_META = [
  {key:"CORA",   title:"main-matrix · cora",          slabel:"main · cora",       sub:"production",            track:"prod",     alphaGrid:false},
  {key:"ARXIV",  title:"main-matrix · arxiv",         slabel:"main · arxiv",      sub:"production · GPU-bound", track:"prod",     alphaGrid:false},
  {key:"A3",     title:"ablation A3 · alpha",         slabel:"A3 alpha",          sub:"2 model × 4 α grid",    track:"ablation", alphaGrid:true},
  {key:"A5",     title:"ablation A5 · ratio/dataset", slabel:"A5 ratio/dataset",  sub:"",                      track:"ablation", alphaGrid:false},
  {key:"A6",     title:"ablation A6 · backbone",      slabel:"A6 backbone",       sub:"",                      track:"ablation", alphaGrid:false},
  {key:"SANITY", title:"sanity",                      slabel:"sanity",            sub:"",                      track:"sanity",   alphaGrid:false},
];
const TRACK_META = [
  {key:"prod",     label:"Production main"},
  {key:"ablation", label:"Ablations"},
  {key:"sanity",   label:"Sanity"},
];
const CAT_TRACK = {};
BLOCK_META.forEach(b => { CAT_TRACK[b.key] = b.track; });

const A3_ALPHAS = ["0.00","0.25","0.75","1.00"];
const A3_MODELS = ["GAT","GCN"];

/* ---- derivation helpers ---- */
function statusOf(c){
  if(c.done >= c.total) return "ok";
  if(c.done <= 0) return "blocked";
  return "partial";
}
function pct(d,t){ return t ? (100*d/t) : 0; }
function fmtPct(d,t){ const p = pct(d,t); return (p===100?"100":(p===0?"0":p.toFixed(p<10?1:0)))+"%"; }
function agg(cs){ return {done:cs.reduce((a,c)=>a+c.done,0), total:cs.reduce((a,c)=>a+c.total,0), n:cs.length}; }
function statusColor(d,t){ return d>=t ? "var(--ok)" : (d<=0 ? "var(--blocked)" : "var(--warn)"); }

/* ---- summary strip (fully derived) ---- */
function rollrow(label, d, t){
  const w = pct(d,t);
  return `<div class="rollrow"><span class="lbl">${label}</span>`
       + `<span class="mini"><i style="width:${w}%; background:${statusColor(d,t)};"></i></span>`
       + `<span class="val num"><b>${d}</b>/${t}</span></div>`;
}
function renderSummary(){
  const all = agg(CONFIGS);
  const opct = pct(all.done, all.total);
  const opctLabel = all.total ? (100*all.done/all.total).toFixed(1)+"%" : "0%";

  let trackRows = "";
  for(const tm of TRACK_META){
    const a = agg(CONFIGS.filter(c => CAT_TRACK[c.cat] === tm.key));
    trackRows += rollrow(`${tm.label} (${a.n})`, a.done, a.total);
  }
  let catRows = "";
  for(const b of BLOCK_META){
    const a = agg(CONFIGS.filter(c => c.cat === b.key));
    catRows += rollrow(b.slabel, a.done, a.total);
  }
  const dsMap = {};
  CONFIGS.forEach(c => { (dsMap[c.ds] = dsMap[c.ds] || []).push(c); });
  const dsKeys = Object.keys(dsMap).sort((x,y) => agg(dsMap[y]).total - agg(dsMap[x]).total);
  let dsRows = "";
  for(const k of dsKeys){ const a = agg(dsMap[k]); dsRows += rollrow(k, a.done, a.total); }

  let nd=0, np=0, nb=0;
  CONFIGS.forEach(c => { const s = statusOf(c); if(s==="ok") nd++; else if(s==="blocked") nb++; else np++; });

  document.getElementById("summary").innerHTML = `
  <div class="card">
    <h3>Overall <span class="pct">${opctLabel}</span></h3>
    <div class="global">
      <div class="big num">${all.done}<small>&thinsp;/&thinsp;${all.total}</small></div>
      <div class="delta num">${all.total-all.done} cells outstanding</div>
    </div>
    <div class="gbar" title="${all.done} done of ${all.total} configured">
      <i style="width:${opct}%; background:var(--ok);"></i>
      <i style="width:${100-opct}%; background:var(--blocked-dim);"></i>
    </div>
    <div style="height:11px;"></div>
    ${trackRows}
  </div>

  <div class="card">
    <h3>By category <span class="pct num">${BLOCK_META.length}</span></h3>
    ${catRows}
    <h3 style="margin-top:13px;">By dataset</h3>
    ${dsRows}
  </div>

  <div class="card" style="display:flex; flex-direction:column; gap:10px;">
    <h3>Dedup caveat <span class="pct" style="color:var(--warn);">upper bound</span></h3>
    <div class="caveat">
      <b>“cells configured” (${all.total})</b> is the raw config matrix (methods × strategies × seeds)
      <b>before cache-reuse dedup.</b> A3 alpha endpoints alias to im/tracin
      (<span class="k">α=0.00 ≈ tracin</span>, <span class="k">α=1.00 ≈ im</span>, reusing main-matrix results),
      an A5 <span class="k">r0.05</span> cora point would just reuse the main matrix, and the arxiv
      smoke configs are subsets of the arxiv main matrix. So <b>${all.total} is an UPPER BOUND on distinct
      work, not a run count.</b>
    </div>
    <div style="font-size:10.5px; color:var(--muted);">
      Config status (n=${CONFIGS.length}): <b style="color:var(--ok);">${nd} done</b> ·
      <b style="color:var(--warn);">${np} partial</b> ·
      <b style="color:var(--blocked);">${nb} not-started</b>.
    </div>
  </div>`;
}

/* ---- one tile ---- */
function tileHTML(c){
  const s = statusOf(c);
  const p = pct(c.done, c.total);
  const provLetter = c.src==="csv" ? "C" : "D";
  const provClass  = c.src==="csv" ? "prov-csv" : "prov-disk";
  const shape = `${c.nm}m×${c.ns}s×${c.nse}seed`;
  const alphaChip = c.alpha!==null ? `<span class="chip">α=${c.alpha}</span>` : "";
  return `
  <div class="tile tile-status-${s}" data-status="${s}" data-prov="${c.src}" data-done="${c.done}" data-total="${c.total}">
    <div class="wash" style="height:${Math.max(p,3)}%;"></div>
    <div class="prov ${provClass}" title="src = ${c.src}">${provLetter}</div>
    <div class="tname">${c.name}</div>
    <div class="frac">
      <span class="d num">${c.done}</span><span class="t num">/ ${c.total}</span>
      <span class="p num">${fmtPct(c.done,c.total)}</span>
    </div>
    <div class="fillbar" title="${c.done}/${c.total} cells">
      <i style="width:${p}%;"></i>
    </div>
    <div class="chips">
      <span class="chip ds">${c.ds}</span>
      <span class="chip">${c.model}</span>
      <span class="chip">r${c.ratio}</span>
      ${alphaChip}
      <span class="chip shape">${shape}</span>
    </div>
    <div class="detail">
      <div class="row"><span class="k">methods</span><span class="v">${c.methods.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">strat</span><span class="v acc">${c.strategies.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">seeds</span><span class="v">${c.seeds.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">shape</span><span class="v">${shape} = ${c.total} cells · ${c.done} done</span></div>
      <div class="row"><span class="k">src</span><span class="v">${c.src} &nbsp;·&nbsp; ${c.file}</span></div>
    </div>
  </div>`;
}

/* ---- render board ---- */
function render(){
  const board = document.getElementById("board");
  let html = "";
  for(const b of BLOCK_META){
    const cs = CONFIGS.filter(c => c.cat === b.key);
    const a = agg(cs);
    const p = pct(a.done, a.total);
    html += `<section class="block" data-block="${b.key}">
      <div class="block-head">
        <span class="name">${b.title}</span>
        <span class="badge"><b class="num">${cs.length}</b> config${cs.length===1?'':'s'}</span>
        ${b.sub?`<span class="badge">${b.sub}</span>`:""}
        <span class="blockbar"><i style="width:${p}%; background:${statusColor(a.done,a.total)};"></i></span>
        <span class="blockpct"><b class="num">${a.done}</b>/<span class="num">${a.total}</span> · ${fmtPct(a.done,a.total)}</span>
      </div>`;

    if(b.alphaGrid){
      // A3: 2 model rows x 4 alpha cols, labelled
      html += `<div class="subgroup-label">2 model (rows) × 4 alpha (cols) — α=0.00 ≈ tracin, α=1.00 ≈ im (alias reuse)</div>`;
      for(const m of A3_MODELS){
        html += `<div class="subgroup" data-sub="${m}">
          <div class="subgroup-label" style="color:#aaccff;">${m}</div>
          <div class="grid cols4">`;
        for(const al of A3_ALPHAS){
          const c = cs.find(x => x.model===m && x.alpha===al);
          if(c) html += tileHTML(c);
        }
        html += `</div></div>`;
      }
    } else {
      html += `<div class="subgroup" data-sub="all"><div class="grid">`;
      for(const c of cs){ html += tileHTML(c); }
      html += `</div></div>`;
    }
    html += `</section>`;
  }
  board.innerHTML = html;
}

/* ---- filtering ---- */
const state = { hideComplete:false, onlyRed:false, prov:"all" };

function applyFilters(){
  const tiles = document.querySelectorAll(".tile");
  let shown = 0;
  tiles.forEach(t => {
    const st = t.dataset.status;
    const pv = t.dataset.prov;
    let vis = true;
    if(state.hideComplete && st==="ok") vis = false;
    if(state.onlyRed && st!=="blocked") vis = false;
    if(state.prov!=="all" && pv!==state.prov) vis = false;
    t.classList.toggle("is-hidden", !vis);
    if(vis) shown++;
  });
  document.querySelectorAll(".subgroup").forEach(sg => {
    sg.classList.toggle("is-empty", !sg.querySelector(".tile:not(.is-hidden)"));
  });
  document.querySelectorAll(".block").forEach(bl => {
    bl.classList.toggle("is-empty", !bl.querySelector(".tile:not(.is-hidden)"));
  });
  document.getElementById("shownCount").textContent = shown;
}

/* ---- wire up ---- */
renderSummary();
render();
document.getElementById("totalCount").textContent = CONFIGS.length;
applyFilters();

document.getElementById("hideComplete").addEventListener("change", e => {
  state.hideComplete = e.target.checked; applyFilters();
});
document.getElementById("onlyRed").addEventListener("change", e => {
  state.onlyRed = e.target.checked; applyFilters();
});
document.querySelectorAll("#provSeg button").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("#provSeg button").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    state.prov = btn.dataset.prov;
    applyFilters();
  });
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(main())
