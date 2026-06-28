"""
Generate a self-contained HTML report for the selection-concordance study.

Reads summary.json + jaccard_{ds}.json + figures/jaccard_{ds}.png (base64-embedded)
and the model-based TracIn-vs-GIF results (modelbased_{ds}.json) from
self/related_work/concordance/, then writes report.html.

Pure rendering. No model, no training.
"""
import json
import base64
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIGS = HERE / "figures"
OUT = HERE / "report.html"

DATE = "2026-06-27"


def b64img(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii") if path.exists() else ""


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def cell(v):
    if v is None:
        return '<td class="na">—</td>'
    try:
        x = float(v)
    except (TypeError, ValueError):
        return f"<td>{v}</td>"
    hue = int(120 * min(max(x, 0), 1))
    return f'<td style="background:hsl({hue},70%,88%)">{x:.3f}</td>'


def main():
    summary = load_json(DATA / "summary.json") or {"datasets": {}, "highlights": {}}
    datasets = summary["datasets"]
    hi = summary.get("highlights", {})

    order = ["cora", "citeseer", "pubmed", "Photo", "Computers", "CS"]
    ds_names = [d for d in order if d in datasets] + [d for d in datasets if d not in order]

    mb = {ds: load_json(DATA / f"modelbased_{ds}.json") for ds in ds_names}
    mb = {ds: v for ds, v in mb.items() if v}

    # ---- topology / cached cross-dataset table ----
    pair_keys = [
        ("degree_pagerank", "degree ↔ pagerank", "centrality family — expect high"),
        ("im_degree", "IM ↔ degree", "does IM degenerate to degree?"),
        ("im_pagerank", "IM ↔ pagerank", "does IM degenerate to pagerank?"),
        ("tracin_degree", "TracIn ↔ degree", "is the influence attack just degree?"),
        ("tracin_im", "TracIn ↔ IM", "influence vs spread"),
        ("hybrid_tracin", "Hybrid ↔ TracIn", "fusion vs IF branch"),
    ]
    rows = ""
    for key, label, note in pair_keys:
        tds = "".join(cell(datasets[ds].get(key)) for ds in ds_names)
        rows += f'<tr><th class="pair">{label}<span class="note">{note}</span></th>{tds}</tr>\n'
    header_cells = "".join(f'<th>{ds}<span class="kk">k={datasets[ds]["k"]}</span></th>' for ds in ds_names)

    figs_html = ""
    for ds in ds_names:
        src = b64img(FIGS / f"jaccard_{ds}.png")
        if src:
            figs_html += f'<figure><img src="{src}" alt="{ds}"><figcaption>{ds}</figcaption></figure>\n'

    # ---- model-based TracIn-vs-GIF table ----
    if mb:
        mbo = [d for d in ds_names if d in mb]
        mbhead = "".join(f'<th>{d}<span class="kk">F1={mb[d]["test_f1"]}</span></th>' for d in mbo)
        def mbrow(label, key, note=""):
            tds = "".join(cell(mb[d]["jaccard"].get(key)) for d in mbo)
            return f'<tr><th class="pair">{label}<span class="note">{note}</span></th>{tds}</tr>'
        gif_section = f"""
        <h2>Model-based: a cheap, scalable IF surrogate that actually tracks GIF</h2>
        <p>One authorised base-GCN train per dataset (<code>train_only</code>, no unlearning; seeded, deterministic),
        then on the <em>same</em> trained model: <strong>GIF</strong> = the real graph influence function
        (s = H⁻¹∇L<sub>test</sub> via LiSSA, then infl(v)=⟨s,∇ℓ<sub>v</sub>⟩);
        <strong>TracIn-proper</strong> = ⟨∇ℓ<sub>v</sub>, ∇L<sub>test</sub>⟩ (Hessian-free, the FIX);
        <strong>TracIn-cross</strong> = the deployed strategy ⟨∇ℓ<sub>v</sub>, Σ<sub>j</sub>∇ℓ<sub>j</sub>⟩;
        <strong>TracIn-self</strong> = ‖∇ℓ<sub>v</sub>‖. degree is topology.</p>
        <table>
        <thead><tr><th class="pair">pair</th>{mbhead}</tr></thead>
        <tbody>
        {mbrow("GIF ↔ TracIn-proper ⟨∇ℓ,∇L_test⟩ (FIX)", "gif_tracinproper", "cheap + faithful")}
        {mbrow("GIF ↔ TracIn-cross (deployed)", "gif_tracin", "the strategy as shipped")}
        {mbrow("GIF ↔ TracIn-self ‖∇ℓ‖", "gif_tracinself", "self-influence variant")}
        {mbrow("GIF ↔ degree", "gif_degree", "real IF vs structural volume")}
        {mbrow("TracIn-proper ↔ degree", "tracinproper_degree", "fixed IF vs degree")}
        </tbody>
        </table>
        <p><strong>Reading.</strong> (1) <strong>The cheap fix works: proper TracIn ≈ GIF at 0.65–0.74</strong>
        — same cost as the deployed strategy (pure gradient inner products, no Hessian, scales to arxiv), but it
        contracts each node gradient with <em>∇L<sub>test</sub></em> instead of the training-gradient sum. The
        residual ~0.25–0.35 gap to GIF is the honest H⁻¹ whitening (Hessian-free ceiling).
        (2) <strong>The deployed cross-form is a poor surrogate (0.10–0.14, ~2× the random floor)</strong>.
        <span class="warn" style="display:inline">Correction to an earlier claim:</span> this is <em>not</em>
        because Σ<sub>j</sub>∇ℓ<sub>j</sub>≈0 at convergence — measured ‖Σ∇ℓ‖ is large (69 / 68 / 255 on
        cora/citeseer/pubmed), ≈ the L2-regularisation residual (∝ θ). The cross-form simply contracts with the
        <em>wrong direction</em> (aggregate-training/regularisation, not test descent), so it ranks by the wrong
        criterion. (3) <strong>Both GIF and the fixed TracIn are ⟂ degree</strong> (0.02–0.05): even the correct
        influence selector targets a different node set than the structural-volume centrality that wins — the
        volume-driven reading survives the real IF.</p>
        <p class="warn"><strong>Caveat.</strong> LiSSA is a first-order H⁻¹ estimate (‖s‖ finite). Seeded /
        deterministic. Single ratio. A scale/iteration sensitivity sweep is still advisable before quoting exact
        magnitudes. Contracting with ∇L<sub>test</sub> uses test labels — in an attack threat model use a held-out
        val/query set or pseudo-labels instead (same math).</p>
        """
    else:
        gif_section = """<h2>Model-based: TracIn vs GIF</h2>
        <p class="warn">Pending — run <code>concordance_model_based.py</code>.</p>"""

    gif_tldr = ""
    if mb and "cora" in mb:
        c = mb["cora"]["jaccard"]
        gif_tldr = (f'<li><strong>A cheap fix recovers IF fidelity</strong>: the deployed cross-TracIn matches real '
                    f'GIF at only {c["gif_tracin"]}, but <strong>proper TracIn ⟨∇ℓ,∇L_test⟩ (same cost, no Hessian) '
                    f'hits {c["gif_tracinproper"]}</strong>. Both the fixed TracIn and GIF stay ⟂ degree '
                    f'({c["gif_degree"]}) — volume-driven survives the real IF.</li>')

    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
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
  .kk {{ display:block; font-weight:400; font-size:11px; color:var(--muted); }}
  .figs {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:10px; }}
  figure {{ margin:0; flex:1 1 300px; max-width:470px; border:1px solid var(--line); border-radius:8px; padding:8px; }}
  figure img {{ width:100%; height:auto; display:block; }}
  figcaption {{ text-align:center; color:var(--muted); font-size:12px; margin-top:4px; }}
  code {{ background:#f3f3f3; padding:1px 5px; border-radius:4px; font-size:13px; }}
  .warn {{ background:#fff8ec; border:1px solid #f3e0b8; border-radius:8px; padding:12px 16px; }}
  .foot {{ color:var(--muted); font-size:12.5px; margin-top:28px; border-top:1px solid var(--line); padding-top:12px; }}
</style></head><body>

<h1>Selection Concordance for GNN Unlearning-Attack Selectors</h1>
<p class="sub">Do the node-selection strategies pick the <em>same</em> nodes? · GCN, r=0.05,
seed 2024 · {len(ds_names)} datasets · generated {DATE} · branch
<code>research/selection-concordance-2026-06-27</code></p>

<div class="tldr">
<strong>TL;DR</strong>
<ul>
<li><strong>IM does NOT degenerate to degree</strong> — overlap with degree is low on every dataset
   (mean {hi.get('im_degree_mean')}; 0.03–0.19), most distinct on larger graphs. The "IM≈degree" guess was wrong at the
   <em>set</em> level; CELF's submodular selection diverges even when single-node spread tracks degree.</li>
<li><strong>degree ≈ pagerank, dataset-dependent</strong> — mean {hi.get('degree_pagerank_mean')} (0.50–0.83).</li>
<li><strong>TracIn near-orthogonal to degree and IM</strong> (cora {datasets.get('cora',{}).get('tracin_degree')} / {datasets.get('cora',{}).get('tracin_im')}):
   the influence attack targets different nodes, yet degree wins → the winning signal is structural volume, not influence.</li>
{gif_tldr}
</ul>
</div>

<h2>Cross-dataset set overlap (Jaccard@k)</h2>
<p>Each cell = |A∩B|/|A∪B| over the top-k selected node sets (k = r·|V<sub>train</sub>|).
Green = redundant (same nodes); orange = distinct. "—" = selector needs a trained model (TracIn/Hybrid; cora only).</p>
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

{gif_section}

<h2>What this means for the thesis</h2>
<p>The selector families are <strong>nearly orthogonal</strong>: centrality (degree≈pagerank), IM (its own
submodular set), and the influence family each target a different node set — and this holds for the
<em>real</em> Hessian-based GIF, not just the cheap TracIn proxy. Combined with the established result that
<strong>degree wins the attack on approximate unlearning</strong>, this is set-level evidence for the
<strong>volume-driven</strong> reading: high-influence nodes are not high-damage nodes; the structural
centrality is the real lever. Two side conclusions: (a) "IM is just degree" is false (0.03–0.19); (b) the
deployed cross-form TracIn is a loose IF surrogate — switch to self-influence ‖∇ℓ‖ if you need to claim
fidelity to IF.</p>

<h2>Caveats</h2>
<ul>
<li>Single seed (2024), single ratio (r=0.05), single backbone (GCN). Directional, not a finished finding.</li>
<li>Model-based (TracIn/GIF) cells: cora/citeseer (+pubmed when done). LiSSA is a first-order H⁻¹ estimate.</li>
<li>IM uses batch-CELF (im_batch_size=5); re-check distinctness with classic CELF (batch=1).</li>
</ul>

<h2>Next steps</h2>
<ol>
<li>Scale/iteration sensitivity for the LiSSA GIF scores; extend model-based cells to more datasets.</li>
<li>Seed × ratio sweep {{2024,1,2,3}} × {{0.01,0.05,0.1}} → error bars → finding.</li>
<li>Attack-outcome join: per selector, (overlap-with-degree, Δacc-under-unlearning) → "different nodes AND worse".</li>
<li>Coverage-aware damage selector prototype (submodular greedy on predicted collateral w/ receptive-field discount).</li>
</ol>

<div class="foot">
Reproduce: <code>run_topology_selectors.py</code> (topology) + <code>concordance_model_based.py --dataset_name &lt;ds&gt;</code>
(TracIn/GIF; trains a base GCN for this study only) → <code>run_analysis.py</code> → <code>gen_report.py</code>.
CPU. Artifacts under <code>self/related_work/concordance/data/</code>. Context: <code>self/related_work/NOTES.md</code>.
</div>
</body></html>"""

    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT}  ({len(html)} bytes, {len(ds_names)} datasets, model-based={list(mb)})")


if __name__ == "__main__":
    main()
