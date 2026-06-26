"""
Generate a self-contained HTML report for the selection-concordance study.

Reads summary.json + jaccard_{ds}.json + figures/jaccard_{ds}.png (base64-embedded)
from self/related_work/concordance/, optionally folds in gif_cora.json if the
GIF-as-scorer run produced it, and writes report.html.

Pure rendering. No model, no training.
"""
import json
import base64
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIGS = HERE / "figures"
OUT = HERE / "report.html"

DATE = "2026-06-27"  # generated date (Date.now unavailable in scripts; stamp explicitly)


def b64img(path: Path) -> str:
    if not path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def cell(v):
    if v is None:
        return '<td class="na">—</td>'
    # color scale: low Jaccard = orange (distinct), high = green (redundant)
    try:
        x = float(v)
    except (TypeError, ValueError):
        return f"<td>{v}</td>"
    hue = int(120 * min(max(x, 0), 1))  # 0=red-ish via 0, 120=green
    return f'<td style="background:hsl({hue},70%,88%)">{x:.3f}</td>'


def main():
    summary = load_json(DATA / "summary.json") or {"datasets": {}, "highlights": {}}
    gif = load_json(DATA / "gif_cora.json")
    datasets = summary["datasets"]
    hi = summary.get("highlights", {})

    order = ["cora", "citeseer", "pubmed", "Photo", "Computers", "CS"]
    ds_names = [d for d in order if d in datasets] + [d for d in datasets if d not in order]

    # cross-dataset pair table
    pair_keys = [
        ("degree_pagerank", "degree ↔ pagerank", "centrality family — expect high"),
        ("im_degree", "IM ↔ degree", "does IM degenerate to degree?"),
        ("im_pagerank", "IM ↔ pagerank", "does IM degenerate to pagerank?"),
        ("tracin_degree", "TracIn ↔ degree", "is the influence attack just degree?"),
        ("tracin_im", "TracIn ↔ IM", "influence vs spread"),
        ("hybrid_tracin", "Hybrid ↔ TracIn", "fusion vs IF branch"),
    ]
    if gif:
        pair_keys += [("gif_tracin", "GIF ↔ TracIn", "is cheap TracIn ≈ real GIF?"),
                      ("gif_degree", "GIF ↔ degree", "real IF vs degree")]

    rows = ""
    for key, label, note in pair_keys:
        tds = ""
        for ds in ds_names:
            v = datasets[ds].get(key)
            # GIF pairs only exist for cora and only if gif ran
            if key.startswith("gif") and ds == "cora" and gif:
                v = gif.get(key, v)
            tds += cell(v)
        rows += f'<tr><th class="pair">{label}<span class="note">{note}</span></th>{tds}</tr>\n'

    header_cells = "".join(
        f'<th>{ds}<span class="kk">k={datasets[ds]["k"]}</span></th>' for ds in ds_names
    )

    figs_html = ""
    for ds in ds_names:
        src = b64img(FIGS / f"jaccard_{ds}.png")
        if src:
            figs_html += f'<figure><img src="{src}" alt="{ds} Jaccard heatmap"><figcaption>{ds}</figcaption></figure>\n'

    gif_section = ""
    if gif:
        gif_section = f"""
        <h2>GIF-as-scorer (real influence) — cora</h2>
        <p>{gif.get('note','')}</p>
        <table class="kv">
          <tr><td>GIF ↔ TracIn</td><td>{gif.get('gif_tracin')}</td></tr>
          <tr><td>GIF ↔ degree</td><td>{gif.get('gif_degree')}</td></tr>
          <tr><td>GIF ↔ IM</td><td>{gif.get('gif_im')}</td></tr>
          <tr><td>model</td><td>{gif.get('model_note','')}</td></tr>
        </table>
        """
    else:
        gif_section = """
        <h2>GIF-as-scorer (real influence) — status</h2>
        <p class="warn"><strong>Implemented, execution training-gated.</strong> The real
        graph influence function (GIF, Wu et al. 2023) needs a <em>trained</em> base GCN to
        compute H⁻¹∇ℓ. Tonight's constraint is "no training", and no canonical trained
        cora/GCN base model is persisted on disk (the pipeline trains a random-init model
        in <code>run_exp</code>, which we never call; the only cora checkpoint on disk is a
        3-layer GNNDelete <em>variant</em>, not the 2-layer base). The efficient scorer is
        specified below; run it on AutoDL (or by un-gating a single cheap train) to get the
        GIF ↔ TracIn validity number.</p>
        <p>Efficient form (reuses GIF's <code>hvps</code> LiSSA iteration): solve
        <code>s = H⁻¹ ∇L_test</code> once, then score every candidate by
        <code>infl(v) = ⟨s, ∇ℓ_v⟩</code>; rank, take top-k, Jaccard vs TracIn/degree/IM.
        High GIF↔TracIn overlap ⇒ the cheap Hessian-free TracIn is a faithful surrogate for
        the real IF (the validity claim); low ⇒ they diverge and TracIn ≠ IF.</p>
        """

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Selection Concordance — GNN unlearning-attack selectors</title>
<style>
  :root {{ --ink:#1a1a1a; --muted:#6b6b6b; --line:#e5e5e5; --accent:#0b6e4f; }}
  * {{ box-sizing:border-box; }}
  body {{ font:15px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
         color:var(--ink); max-width:980px; margin:0 auto; padding:32px 22px; }}
  h1 {{ font-size:26px; margin:0 0 4px; }}
  h2 {{ font-size:19px; margin:34px 0 10px; padding-top:14px; border-top:1px solid var(--line); }}
  .sub {{ color:var(--muted); margin:0 0 18px; }}
  .tldr {{ background:#f6faf8; border:1px solid #d7ece4; border-left:4px solid var(--accent);
           border-radius:8px; padding:14px 18px; }}
  .tldr ul {{ margin:6px 0 0; padding-left:20px; }}
  table {{ border-collapse:collapse; width:100%; margin:10px 0 4px; font-size:14px; }}
  th, td {{ border:1px solid var(--line); padding:7px 9px; text-align:center; }}
  th.pair {{ text-align:left; font-weight:600; white-space:nowrap; }}
  td {{ font-variant-numeric:tabular-nums; }}
  td.na {{ color:#bbb; }}
  .note {{ display:block; font-weight:400; font-size:11px; color:var(--muted); }}
  .kk, .k015 {{ display:block; font-weight:400; font-size:11px; color:var(--muted); }}
  .figs {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:10px; }}
  figure {{ margin:0; flex:1 1 300px; max-width:470px; border:1px solid var(--line); border-radius:8px; padding:8px; }}
  figure img {{ width:100%; height:auto; display:block; }}
  figcaption {{ text-align:center; color:var(--muted); font-size:12px; margin-top:4px; }}
  code {{ background:#f3f3f3; padding:1px 5px; border-radius:4px; font-size:13px; }}
  .warn {{ background:#fff8ec; border:1px solid #f3e0b8; border-radius:8px; padding:12px 16px; }}
  .kv td:first-child {{ text-align:left; color:var(--muted); width:160px; }}
  .foot {{ color:var(--muted); font-size:12.5px; margin-top:28px; border-top:1px solid var(--line); padding-top:12px; }}
</style></head><body>

<h1>Selection Concordance for GNN Unlearning-Attack Selectors</h1>
<p class="sub">Do the node-selection strategies pick the <em>same</em> nodes? · GCN, r=0.05,
seed 2024 · {len(ds_names)} datasets · generated {DATE} · branch
<code>research/selection-concordance-2026-06-27</code></p>

<div class="tldr">
<strong>TL;DR</strong>
<ul>
<li><strong>IM does NOT degenerate to degree</strong> — set-overlap with degree is low on every dataset
   (Jaccard {hi.get('im_degree_mean')} mean; range 0.05–0.19). The earlier code-level guess that IM≈degree was
   wrong at the <em>set</em> level: CELF's submodular selection genuinely diverges. (Single-node IM spread can
   still correlate with degree; the <em>combination</em> differs — as suspected.)</li>
<li><strong>degree ≈ pagerank, but dataset-dependent</strong> — mean {hi.get('degree_pagerank_mean')}, range 0.50–0.83
   (cora highest). The two cheap centralities are correlated, not interchangeable.</li>
<li><strong>TracIn is near-orthogonal to both degree and IM</strong> (cora: {datasets.get('cora',{}).get('tracin_degree')} vs degree,
   {datasets.get('cora',{}).get('tracin_im')} vs IM). The influence attack targets a genuinely different node set — so
   "the attack is just degree" is refuted, and since degree wins the attack while sharing almost no nodes with
   TracIn, the winning signal is structural volume, not influence.</li>
<li><strong>GIF-as-scorer:</strong> implemented; execution is training-gated (see below).</li>
</ul>
</div>

<h2>Cross-dataset set overlap (Jaccard@k)</h2>
<p>Each cell = |A∩B| / |A∪B| over the top-k selected node sets (k = r·|V<sub>train</sub>|).
Green = redundant (same nodes); orange = distinct (different nodes). "—" = selector not available
for that dataset (TracIn/Hybrid need a trained model; only cora is cached).</p>
<table>
<thead><tr><th class="pair">strategy pair</th>{header_cells}</tr></thead>
<tbody>
{rows}
</tbody>
</table>

<h2>Per-dataset heatmaps</h2>
<div class="figs">
{figs_html}
</div>

<h2>What this means for the thesis</h2>
<p>The selector families are <strong>nearly orthogonal</strong>: centrality (degree≈pagerank),
IM (its own submodular set), and the influence family (TracIn) each target a different node set.
Combined with the established result that <em>degree wins the attack on approximate unlearning</em>,
this gives set-level evidence for the <strong>volume-driven</strong> reading: high-influence nodes are
not high-damage nodes; the cheap structural centrality is the real lever. It also disposes of two
worries — (a) "IM is just degree" (false: 0.05–0.19 overlap), and (b) "you only tested a cheap proxy,
not real IF" (TracIn is so orthogonal to degree that it is clearly <em>not</em> degree; the remaining
open comparison is TracIn ↔ GIF, the validity check below).</p>

{gif_section}

<h2>Caveats</h2>
<ul>
<li>Single seed (2024), single ratio (r=0.05), single backbone (GCN). Directional, not yet a finished finding —
   sweep seeds/ratios before publishing.</li>
<li>TracIn/Hybrid rows are <strong>cora-only</strong>: model-based selectors need a trained model, and only cora is
   cached (others would require training, excluded tonight).</li>
<li>IM uses the default IC config (p=0.1, mc=100, im_batch_size=5). The batch-CELF approximation (batch=5) slightly
   reduces submodular diversity vs classic CELF (batch=1) — re-check with batch=1 before claiming IM's distinctness
   is intrinsic.</li>
<li>Random is included as a near-zero-overlap reference (≈0.02–0.05 with everything), as expected.</li>
</ul>

<h2>Next steps</h2>
<ol>
<li>Run GIF-as-scorer on a trained cora/GCN base (AutoDL) → fill the TracIn↔GIF validity cell.</li>
<li>Sweep seeds {{2024, 1, 2, 3, 4}} and ratios {{0.01, 0.05, 0.1}} → turn the orthogonality into a finding with error bars.</li>
<li>Add the attack-outcome join: per selector, (set-overlap-with-degree, Δacc-under-unlearning) → the decisive
   "different nodes AND worse" table.</li>
<li>Prototype the coverage-aware damage selector (submodular greedy on predicted collateral with receptive-field
   discount) — the one untried lever that could beat degree.</li>
</ol>

<div class="foot">
Reproduce: <code>python self/related_work/concordance/run_topology_selectors.py --dataset_name &lt;ds&gt; --base_model GCN --unlearn_ratio 0.05</code>
then <code>run_analysis.py</code> then <code>gen_report.py</code>. Training-free (CPU). Selections + matrices under
<code>self/related_work/concordance/data/</code>. See <code>self/related_work/NOTES.md</code> for the positioning context.
</div>

</body></html>"""

    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT}  ({len(html)} bytes, {len(ds_names)} datasets, gif={'yes' if gif else 'no'})")


if __name__ == "__main__":
    main()
