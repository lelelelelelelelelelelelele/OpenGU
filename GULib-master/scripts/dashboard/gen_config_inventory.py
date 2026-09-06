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
    n_seeds,n_cells,done,src,methods,strategies,seeds,valid,rerun,warning,
    accepted_remote

`done` means an output row/artifact exists. `valid` means it is currently
usable for paper-facing conclusions. `rerun` marks produced cells that must be
rerun before they should count as clean evidence (for example GraphRevoker E4).

`accepted_remote` marks cells whose formal remote gate passed but whose complete
evidence bundle has not yet been imported into the local archive. They are not
counted as local `valid` until that archive boundary closes.

`cat` long names are mapped to short block keys (CORA/ARXIV/SUPP/A3/A5/A6/SANITY).
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
    "supplementary overlap/validity": "SUPP",
    "sanity": "SANITY",
}

STORY_FIELDS = ("Question", "Setup", "Why", "Current read", "Next decision")

GROUP_STORY = {
    "CORA": {
        "Question": "What is the core vulnerability fingerprint across methods and selectors?",
        "Setup": "Cora, GCN/GAT, r=0.05, 6 GU methods, 6 selectors, 5 seeds.",
        "Why": "This is the audit backbone: it gives the advisor a per-method comparison before we argue about mechanisms.",
        "Current read": "GraphRevoker random/degree/pagerank/IM passed the remote E4 gate (20 cells per backbone), but local evidence import is pending; every TracIn/Hybrid row still needs a proper-TracIn refresh.",
        "Next decision": "Import the GraphRevoker E4 manifest/artifacts, then promote remote-accepted cells to local usable; refresh TracIn/Hybrid independently.",
    },
    "A5": {
        "Question": "Does the story survive budget and dataset changes?",
        "Setup": "Ratio sweep on Cora/GCN plus Citeseer scope cells.",
        "Why": "It separates a one-budget anecdote from a stable vulnerability pattern and supports advisor questions about scope.",
        "Current read": "r=0.01 is produced, but its GraphRevoker cells were not covered by the r=0.05 E4 gate and every old TracIn row remains invalid.",
        "Next decision": "Use r=0.01 as a partial anchor; run r=0.10/r=0.20 and Citeseer after the clean-selector path is settled.",
    },
    "ARXIV": {
        "Question": "Can the finding scale beyond small citation graphs?",
        "Setup": "ogbn-arxiv, GCN, mostly r=0.01 pilot cells plus planned r=0.05 queue.",
        "Why": "This answers the advisor's scale concern, but it is remote-GPU work rather than a local analysis task.",
        "Current read": "Only a pilot exists; produced TracIn pilot/smoke cells also need proper-TracIn refresh after IF-concordance before becoming paper evidence.",
        "Next decision": "Rent the remote GPU when ready and rerun the pilot/queue with the corrected selector semantics.",
    },
    "SUPP": {
        "Question": "Are selector and approximation signals actually distinct and valid?",
        "Setup": "Concordance/top-k overlap across 6 datasets plus model-based GIF vs TracIn checks on Cora/Citeseer/Pubmed.",
        "Why": "This is the evidence layer behind the selector story: it tests whether IM is just degree, whether proper TracIn tracks real GIF, and whether deployed TracIn/Hybrid need refresh.",
        "Current read": "Topology overlap is produced for 6/6 datasets; model-based GIF/proper-TracIn overlap is produced for 3/3 datasets. Exact GIF magnitudes still need LiSSA sensitivity before strong quoting.",
        "Next decision": "Keep this as a supplementary validity panel and join overlap with attack outcomes after proper-TracIn/Hybrid reruns.",
    },
    "A3": {
        "Question": "Is IF/IM fusion adding mechanism value or just interpolating two axes?",
        "Setup": "Hybrid alpha sweep over Cora, GCN/GAT, r=0.05.",
        "Why": "This connects the selector story to the fingerprint story: alpha is a diagnostic axis, not the main contribution.",
        "Current read": "The alpha=0.00 GCN corner has 10 produced cells; the rest is still pending.",
        "Next decision": "Run only if the refreshed main matrix shows that an alpha curve is worth explaining to the advisor.",
    },
    "A6": {
        "Question": "Should we broaden beyond two message-passing backbones?",
        "Setup": "Deferred GIN exploratory cells on Cora.",
        "Why": "It is useful for future work, but it risks diluting the rebuttal-prep story.",
        "Current read": "Not started by design; current claim should stay scoped to GCN/GAT-style message passing.",
        "Next decision": "Keep deferred unless advisor explicitly asks for cross-architecture evidence.",
    },
    "SANITY": {
        "Question": "Are repair paths and one-cell checks behaving before larger reruns?",
        "Setup": "Small GraphRevoker and GIF diagnostic configs.",
        "Why": "These cells are guardrails; they prevent full-matrix reruns from hiding a broken method path.",
        "Current read": "Useful as diagnostics, not paper evidence.",
        "Next decision": "Run/update sanity cells before each expensive repair batch.",
    },
}


def js_str(s: str) -> str:
    s = "" if s is None else str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def js_int(s: str) -> str:
    s = (s or "").strip()
    return str(int(float(s))) if s not in ("", "None") else "0"


def build_story_meta_js():
    lines = ["const STORY_META = {"]
    for key, story in GROUP_STORY.items():
        lines.append(f"  {key}: {{")
        for field in STORY_FIELDS:
            if field not in story:
                raise SystemExit(f"[gen] missing story field {field!r} for {key}")
            lines.append(f"    {js_str(field)}:{js_str(story[field])},")
        lines.append("  },")
    lines.append("};")
    return "\n".join(lines)


def build_configs_array(rows):
    lines = []
    for r in rows:
        cat_raw = (r.get("cat") or "").strip()
        catkey = CAT_MAP.get(cat_raw)
        if catkey is None:
            raise SystemExit(f"[gen] unknown cat value: {cat_raw!r} (row {r.get('file')})")
        alpha = (r.get("hybrid_alpha") or "").strip()
        alpha_js = ('"%.2f"' % float(alpha)) if alpha not in ("", "None") else "null"
        done = js_int(r["done"])
        valid = js_int(r.get("valid") or r["done"])
        rerun = js_int(r.get("rerun") or "0")
        accepted_remote = js_int(r.get("accepted_remote") or "0")
        obj = (
            "  {file:%s, name:%s, cat:%s, ds:%s, model:%s, ratio:%s, alpha:%s, "
            "nm:%s,ns:%s,nse:%s, total:%s, done:%s, valid:%s, rerun:%s, acceptedRemote:%s, "
            "src:%s, methods:%s, strategies:%s, seeds:%s, warning:%s},"
            % (
                js_str(r["file"]), js_str(r["name"]), js_str(catkey), js_str(r["dataset"]),
                js_str(r["model"]), js_str(r["ratio"]), alpha_js,
                js_int(r["n_methods"]), js_int(r["n_strategies"]), js_int(r["n_seeds"]),
                js_int(r["n_cells"]), done, valid, rerun, accepted_remote, js_str(r["src"]),
                js_str(r["methods"]), js_str(r["strategies"]), js_str(r["seeds"]),
                js_str(r.get("warning", "")),
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
    story_js = build_story_meta_js()
    today = datetime.date.today().isoformat()
    nconfigs = len(rows)

    # quick console summary (sanity for the operator)
    done = sum(int(float(r["done"] or 0)) for r in rows)
    valid = sum(int(float((r.get("valid") or r["done"] or 0))) for r in rows)
    rerun = sum(int(float(r.get("rerun") or 0)) for r in rows)
    accepted_remote = sum(int(float(r.get("accepted_remote") or 0)) for r in rows)
    total = sum(int(float(r["n_cells"] or 0)) for r in rows)
    print(
        f"[gen] {nconfigs} configs | {done}/{total} produced | "
        f"{valid}/{total} usable | {accepted_remote} accepted remote | {rerun} rerun"
    )
    print(f"[gen] wrote {OUT_PATH.relative_to(ROOT)}")

    html = (
        TEMPLATE
        .replace("/*__CONFIGS__*/", configs_js)
        .replace("/*__STORY_META__*/", story_js)
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
  .story{
    display:grid; grid-template-columns:minmax(160px,.75fr) minmax(260px,1.25fr) minmax(260px,1.2fr);
    gap:10px; margin:0 0 12px; padding:11px 12px;
    background:#111722; border:1px solid #263445; border-radius:8px;
  }
  @media(max-width:950px){ .story{grid-template-columns:1fr;} }
  .story .cell{
    min-width:0; border-left:2px solid #30445d; padding-left:9px;
  }
  .story .label{
    font-size:9px; letter-spacing:.55px; text-transform:uppercase;
    color:#7f8da0; font-family:ui-monospace,Consolas,monospace; margin-bottom:3px;
  }
  .story .text{font-size:11.3px; color:#c7d0da; line-height:1.42;}
  .story .cell.focus{border-color:var(--accent);}
  .story .cell.focus .text{color:#dbe7f5;}
  .story .cell.warn{border-color:var(--warn);}
  .story .cell.warn .text{color:#e3d38f;}
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
  .tile .usable{
    position:relative; z-index:1; margin:-3px 0 8px;
    font-size:10.5px; color:var(--muted); font-family:ui-monospace,Consolas,monospace;
  }
  .tile .usable b{color:var(--text); font-weight:650;}
  .tile .usable .rerun{color:var(--warn);}

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
  .chip.warn{color:#e8d98e; border-color:#6b5515; background:#2b240f;}
  .warnline{
    position:relative; z-index:1; margin-top:9px; padding:7px 8px;
    border:1px solid #5b4614; border-radius:7px; background:#231d0d;
    color:#d7c778; font-size:10px; line-height:1.4;
  }
  .repair-line{
    position:relative; z-index:1; display:flex; justify-content:space-between; gap:8px;
    margin:7px 0 0; padding:5px 7px; border-radius:6px;
    background:#2a210c; border:1px solid #604914;
    font-size:10px; color:#d7c778; font-family:ui-monospace,Consolas,monospace;
  }
  .repair-line b{color:#f0d36a; font-weight:700;}

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
    <div class="sub">__NCONFIGS__ configs · join: <b>_phase_b_aggregate.csv</b> (cora) + disk scan (arxiv) · historical definitions <b>docs/archive/experiment-configs-pre-aagu034/</b> · generated __GENERATED_DATE__</div>
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
  <div class="item" style="color:#71798a;">tile fill = usable/total; headline count = produced artifacts</div>
</div>

<!-- ============ HEATMAP BLOCKS ============ -->
<main id="board"></main>

<footer>
  <div class="fhead">Provenance &amp; legend</div>
  <div>
    <b>src</b> column: <code>csv</code> = completion read from <code>results/_phase_b_aggregate.csv</code>
    (cora main results) · <code>disk</code> = cell count scanned from <code>results/runs/</code>
    (arxiv + non-cora; not in the aggregate CSV). Source of configs:
    <code>docs/archive/experiment-configs-pre-aagu034/</code> (historical evidence inventory; not active execution configs). Status mapping: <b style="color:var(--ok);">complete</b> /
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

/* ---- advisor-facing story layer (not CSV data) ---- */
/*__STORY_META__*/

/* ---- block metadata: order + labels only; numbers are DERIVED ---- */
const BLOCK_META = [
  {key:"SUPP",   title:"supplementary / overlap-validity", slabel:"supp overlap", sub:"selector + IF validity", track:"supp",     alphaGrid:false},
  {key:"CORA",   title:"main-matrix · cora",          slabel:"main · cora",       sub:"production",            track:"prod",     alphaGrid:false},
  {key:"ARXIV",  title:"main-matrix · arxiv",         slabel:"main · arxiv",      sub:"production · GPU-bound", track:"prod",     alphaGrid:false},
  {key:"A3",     title:"ablation A3 · alpha",         slabel:"A3 alpha",          sub:"2 model × 4 α grid",    track:"ablation", alphaGrid:true},
  {key:"A5",     title:"ablation A5 · ratio/dataset", slabel:"A5 ratio/dataset",  sub:"",                      track:"ablation", alphaGrid:false},
  {key:"A6",     title:"ablation A6 · backbone",      slabel:"A6 backbone",       sub:"",                      track:"ablation", alphaGrid:false},
  {key:"SANITY", title:"sanity",                      slabel:"sanity",            sub:"",                      track:"sanity",   alphaGrid:false},
];
const TRACK_META = [
  {key:"prod",     label:"Production main"},
  {key:"supp",     label:"Supplementary validity"},
  {key:"ablation", label:"Ablations"},
  {key:"sanity",   label:"Sanity"},
];
const EXEC_ORDER = ["CORA","SUPP","A5","ARXIV","A3","A6","SANITY"];
const EXEC_LABELS = {
  CORA:  {title:"1. main-matrix / cora",         sub:"GraphRevoker remote-accepted/archive-pending; TracIn/Hybrid refresh pending"},
  SUPP:  {title:"2. supplementary / overlap-validity", sub:"selector concordance + GIF/TracIn validity"},
  A5:    {title:"3. A5 ratio / dataset",         sub:"r0.01 done; higher ratios pending"},
  ARXIV: {title:"4. arxiv pilot / remote queue", sub:"GPU-bound"},
  A3:    {title:"5. A3 alpha",                   sub:"2 model x 4 alpha grid"},
  A6:    {title:"6. A6 backbone",                sub:"deferred / future-work"},
  SANITY:{title:"7. sanity",                     sub:"diagnostic"},
};
BLOCK_META.sort((a,b) => EXEC_ORDER.indexOf(a.key) - EXEC_ORDER.indexOf(b.key));
BLOCK_META.forEach(b => Object.assign(b, EXEC_LABELS[b.key] || {}));
const CAT_TRACK = {};
BLOCK_META.forEach(b => { CAT_TRACK[b.key] = b.track; });

const A3_ALPHAS = ["0.00","0.25","0.75","1.00"];
const A3_MODELS = ["GAT","GCN"];

/* ---- derivation helpers ---- */
function statusOf(c){
  if(c.valid >= c.total) return "ok";
  if(c.done <= 0) return "blocked";
  return "partial";
}
function pct(d,t){ return t ? (100*d/t) : 0; }
function fmtPct(d,t){ const p = pct(d,t); return (p===100?"100":(p===0?"0":p.toFixed(p<10?1:0)))+"%"; }
function agg(cs){
  return {
    done:cs.reduce((a,c)=>a+c.done,0),
    valid:cs.reduce((a,c)=>a+c.valid,0),
    rerun:cs.reduce((a,c)=>a+c.rerun,0),
    acceptedRemote:cs.reduce((a,c)=>a+c.acceptedRemote,0),
    total:cs.reduce((a,c)=>a+c.total,0),
    n:cs.length
  };
}
function statusColor(d,t){ return d>=t ? "var(--ok)" : (d<=0 ? "var(--blocked)" : "var(--warn)"); }

/* ---- summary strip (fully derived) ---- */
function rollrow(label, a){
  const d = a.valid, t = a.total;
  const w = pct(d,t);
  const suffix = a.done !== a.valid ? ` prod ${a.done}` : "";
  const remote = a.acceptedRemote ? ` remote ${a.acceptedRemote}` : "";
  const rerun = a.rerun ? ` rerun ${a.rerun}` : "";
  return `<div class="rollrow"><span class="lbl">${label}</span>`
       + `<span class="mini"><i style="width:${w}%; background:${statusColor(d,t)};"></i></span>`
       + `<span class="val num"><b>${d}</b>/${t}${suffix}${remote}${rerun}</span></div>`;
}
function renderSummary(){
  const all = agg(CONFIGS);
  const opct = pct(all.valid, all.total);
  const remotePct = pct(all.acceptedRemote, all.total);
  const rerunPct = pct(all.rerun, all.total);
  const outstandingPct = Math.max(0, 100 - opct - remotePct - rerunPct);
  const opctLabel = all.total ? (100*all.valid/all.total).toFixed(1)+"%" : "0%";

  let trackRows = "";
  for(const tm of TRACK_META){
    const a = agg(CONFIGS.filter(c => CAT_TRACK[c.cat] === tm.key));
    trackRows += rollrow(`${tm.label} (${a.n})`, a);
  }
  let catRows = "";
  for(const b of BLOCK_META){
    const a = agg(CONFIGS.filter(c => c.cat === b.key));
    catRows += rollrow(b.slabel, a);
  }
  const dsMap = {};
  CONFIGS.forEach(c => { (dsMap[c.ds] = dsMap[c.ds] || []).push(c); });
  const dsKeys = Object.keys(dsMap).sort((x,y) => agg(dsMap[y]).total - agg(dsMap[x]).total);
  let dsRows = "";
  for(const k of dsKeys){ const a = agg(dsMap[k]); dsRows += rollrow(k, a); }

  let nd=0, np=0, nb=0;
  CONFIGS.forEach(c => { const s = statusOf(c); if(s==="ok") nd++; else if(s==="blocked") nb++; else np++; });

  document.getElementById("summary").innerHTML = `
  <div class="card">
    <h3>Usable coverage <span class="pct">${opctLabel}</span></h3>
    <div class="global">
      <div class="big num">${all.valid}<small>&thinsp;/&thinsp;${all.total}</small></div>
      <div class="delta num">${all.done} produced · ${all.acceptedRemote} remote accepted/archive pending · ${all.rerun} rerun pending</div>
    </div>
    <div class="gbar" title="${all.valid} local usable, ${all.acceptedRemote} remote accepted/archive pending, ${all.rerun} rerun pending, ${all.done} produced of ${all.total} configured">
      <i style="width:${opct}%; background:var(--ok);"></i>
      <i style="width:${remotePct}%; background:var(--accent);"></i>
      <i style="width:${rerunPct}%; background:var(--warn);"></i>
      <i style="width:${outstandingPct}%; background:var(--blocked-dim);"></i>
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
  const p = pct(c.valid, c.total);
  const provLetter = c.src==="csv" ? "C" : "D";
  const provClass  = c.src==="csv" ? "prov-csv" : "prov-disk";
  const rerunChip = c.rerun ? `<span class="chip warn">rerun ${c.rerun}</span>` : "";
  const remoteChip = c.acceptedRemote ? `<span class="chip">remote ${c.acceptedRemote}</span>` : "";
  const rerunBasis = (() => {
    if(!c.rerun) return "";
    const basis = [];
    if(/GraphRevoker[^.;]*(invalid|rerun|refresh)/i.test(c.warning)) basis.push("GraphRevoker post-fix rerun");
    if(/proper-TracIn|TracIn\/Hybrid|TracIn/i.test(c.warning)) basis.push("proper-TracIn refresh");
    return basis.length ? basis.join(" + ") : "rerun pending";
  })();
  const repairLine = c.rerun ? `<div class="repair-line"><span>rerun basis</span><b>${rerunBasis}</b></div>` : "";
  const warningLine = c.warning ? `<div class="warnline">${c.warning}</div>` : "";
  const shape = `${c.nm}m×${c.ns}s×${c.nse}seed`;
  const alphaChip = c.alpha!==null ? `<span class="chip">α=${c.alpha}</span>` : "";
  return `
  <div class="tile tile-status-${s}" data-status="${s}" data-prov="${c.src}" data-done="${c.done}" data-valid="${c.valid}" data-accepted-remote="${c.acceptedRemote}" data-rerun="${c.rerun}" data-total="${c.total}">
    <div class="wash" style="height:${Math.max(p,3)}%;"></div>
    <div class="prov ${provClass}" title="src = ${c.src}">${provLetter}</div>
    <div class="tname">${c.name}</div>
    <div class="frac">
      <span class="d num">${c.done}</span><span class="t num">/ ${c.total}</span>
      <span class="p num">${fmtPct(c.done,c.total)} produced</span>
    </div>
    <div class="usable">local usable <b>${c.valid}/${c.total}</b> (${fmtPct(c.valid,c.total)})${c.acceptedRemote ? ` · <span>${c.acceptedRemote} remote accepted/archive pending</span>` : ""}${c.rerun ? ` · <span class="rerun">${c.rerun} rerun</span>` : ""}</div>
    <div class="fillbar" title="${c.valid}/${c.total} usable; ${c.done}/${c.total} produced">
      <i style="width:${p}%;"></i>
    </div>
    <div class="chips">
      <span class="chip ds">${c.ds}</span>
      <span class="chip">${c.model}</span>
      <span class="chip">r${c.ratio}</span>
      ${alphaChip}
      ${remoteChip}
      ${rerunChip}
      <span class="chip shape">${shape}</span>
    </div>
    ${repairLine}
    ${warningLine}
    <div class="detail">
      <div class="row"><span class="k">methods</span><span class="v">${c.methods.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">strat</span><span class="v acc">${c.strategies.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">seeds</span><span class="v">${c.seeds.replace(/\|/g,' · ')}</span></div>
      <div class="row"><span class="k">shape</span><span class="v">${shape} = ${c.total} cells | ${c.done} produced | ${c.valid} usable | ${c.rerun} rerun</span></div>
      ${c.warning ? `<div class="row"><span class="k">warn</span><span class="v">${c.warning}</span></div>` : ""}
      <div class="row"><span class="k">src</span><span class="v">${c.src} &nbsp;·&nbsp; ${c.file}</span></div>
    </div>
  </div>`;
}

function storyHTML(key){
  const s = STORY_META[key];
  if(!s) return "";
  const cells = [
    ["Question", s["Question"], "focus"],
    ["Setup", s["Setup"], ""],
    ["Why", s["Why"], ""],
    ["Current read", s["Current read"], "warn"],
    ["Next decision", s["Next decision"], "focus"],
  ];
  return `<div class="story">` + cells.map(([label,text,klass]) =>
    `<div class="cell ${klass}"><div class="label">${label}</div><div class="text">${text}</div></div>`
  ).join("") + `</div>`;
}

/* ---- render board ---- */
function render(){
  const board = document.getElementById("board");
  let html = "";
  for(const b of BLOCK_META){
    const cs = CONFIGS.filter(c => c.cat === b.key);
    const a = agg(cs);
    const p = pct(a.valid, a.total);
    html += `<section class="block" data-block="${b.key}">
      <div class="block-head">
        <span class="name">${b.title}</span>
        <span class="badge"><b class="num">${cs.length}</b> config${cs.length===1?'':'s'}</span>
        ${b.sub?`<span class="badge">${b.sub}</span>`:""}
        <span class="blockbar"><i style="width:${p}%; background:${statusColor(a.valid,a.total)};"></i></span>
        <span class="blockpct"><b class="num">${a.valid}</b>/<span class="num">${a.total}</span> usable · ${a.done} produced · ${a.rerun} rerun</span>
      </div>`;
    html += storyHTML(b.key);

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
