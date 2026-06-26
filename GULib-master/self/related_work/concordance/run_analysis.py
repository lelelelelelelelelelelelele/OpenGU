"""
Selection-concordance analysis.

Reads the per-dataset selection JSONs produced by run_topology_selectors.py
(self/related_work/concordance/data/*.json), folds in the cached cora
model-based selectors (tracin, hybrid) from results/selection_cache/, and
computes pairwise Jaccard@k set-overlap matrices per dataset.

Outputs:
    self/related_work/concordance/data/jaccard_{dataset}.json
    self/related_work/concordance/figures/jaccard_{dataset}.png
    self/related_work/concordance/data/summary.json

Pure analysis (reads JSON, computes set overlaps). No model, no training.
"""
import json
import glob
import itertools
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
FIGS = HERE / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
REPO = HERE.parents[2]
SEL_CACHE = REPO / "results" / "selection_cache"

# Strategy display order (topology/centrality first, then influence family)
ORDER = ["random", "degree", "pagerank", "im", "tracin", "hybrid", "gif"]


def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else float("nan")


def load_dataset_selections():
    """{dataset: {strategy: [nodes]}} from concordance/data/*.json."""
    out = {}
    for f in sorted(DATA.glob("*_GCN_r*_seed*.json")):
        p = json.loads(f.read_text(encoding="utf-8"))
        ds = p["dataset"]
        sels = {k: v for k, v in p.get("selections", {}).items() if v}
        out[ds] = {"k": p["k"], "sel": sels, "num_nodes": p.get("num_nodes"),
                   "num_candidates": p.get("num_candidates")}
    return out


def load_cached_cora_model_selectors(k_target):
    """Pull cora/GCN tracin & hybrid (model-based) selections from selection_cache."""
    found = {}
    for f in SEL_CACHE.glob("*.json"):
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        cfg = p.get("config", {}) or {}
        sr = p.get("selection_result", {}) or {}
        if (cfg.get("dataset_name") == "cora" and cfg.get("base_model") == "GCN"
                and sr.get("strategy_name") in ("tracin", "hybrid")
                and int(cfg.get("k", -1)) == int(k_target)):
            nodes = [int(x) for x in (sr.get("selected_nodes") or [])]
            if nodes:
                found[sr["strategy_name"]] = nodes
    return found


def matrix_for(sels, k):
    names = [n for n in ORDER if n in sels]
    m = np.full((len(names), len(names)), np.nan)
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            kk = min(len(sels[a]), len(sels[b]), k)
            m[i, j] = jaccard(sels[a][:kk], sels[b][:kk])
    return names, m


def heatmap(names, m, title, path):
    fig, ax = plt.subplots(figsize=(1.1 * len(names) + 2, 1.0 * len(names) + 1.5))
    im = ax.imshow(m, vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks(range(len(names)))
    ax.set_yticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")
    ax.set_yticklabels(names)
    for i in range(len(names)):
        for j in range(len(names)):
            v = m[i, j]
            if not np.isnan(v):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        color="white" if v < 0.6 else "black", fontsize=9)
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Jaccard@k")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    ds_sel = load_dataset_selections()
    summary = {"datasets": {}, "highlights": {}}

    for ds, info in ds_sel.items():
        sels = dict(info["sel"])
        k = info["k"]
        if ds == "cora":
            sels.update(load_cached_cora_model_selectors(k))  # add tracin/hybrid
        names, m = matrix_for(sels, k)
        # persist matrix
        mat_json = {
            "dataset": ds, "k": k, "num_nodes": info["num_nodes"],
            "num_candidates": info["num_candidates"], "strategies": names,
            "jaccard": [[None if np.isnan(x) else round(float(x), 4) for x in row] for row in m],
        }
        (DATA / f"jaccard_{ds}.json").write_text(json.dumps(mat_json, indent=2), encoding="utf-8")
        heatmap(names, m, f"{ds} (GCN, r=0.05, k={k}) — selection-set Jaccard",
                FIGS / f"jaccard_{ds}.png")

        # pull key pairs for the summary
        def pair(a, b):
            if a in names and b in names:
                return round(float(m[names.index(a)][names.index(b)]), 3)
            return None
        summary["datasets"][ds] = {
            "k": k, "strategies": names,
            "degree_pagerank": pair("degree", "pagerank"),
            "im_degree": pair("im", "degree"),
            "im_pagerank": pair("im", "pagerank"),
            "tracin_degree": pair("tracin", "degree"),
            "tracin_im": pair("tracin", "im"),
            "hybrid_tracin": pair("hybrid", "tracin"),
            "gif_tracin": pair("gif", "tracin"),
            "gif_degree": pair("gif", "degree"),
        }
        print(f"[{ds}] k={k} strategies={names}")
        for kk in ("degree_pagerank", "im_degree", "tracin_degree", "tracin_im"):
            print(f"    {kk}: {summary['datasets'][ds][kk]}")

    # cross-dataset highlights (mean over datasets where available)
    def mean_of(key):
        vals = [d[key] for d in summary["datasets"].values() if d.get(key) is not None]
        return round(float(np.mean(vals)), 3) if vals else None
    summary["highlights"] = {
        "degree_pagerank_mean": mean_of("degree_pagerank"),
        "im_degree_mean": mean_of("im_degree"),
        "tracin_degree_mean": mean_of("tracin_degree"),
        "tracin_im_mean": mean_of("tracin_im"),
        "n_datasets": len(summary["datasets"]),
    }
    (DATA / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n=== highlights ===")
    print(json.dumps(summary["highlights"], indent=2))


if __name__ == "__main__":
    main()
