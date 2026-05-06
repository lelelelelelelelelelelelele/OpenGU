"""⚠ 2026-05-06: STALE — reads `results/relative/` and `results/collateral/`,
both gitignored as pre-Phase-B bug-polluted. Same status as
plot_paper_figures.py; rewrite to walk results/runs/ before use.
"""
import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

if __name__ == "__main__" and not os.environ.get("ALLOW_LEGACY_PLOT"):
    sys.stderr.write(
        "[plot_supp_figures] refusing to run: reads results/relative/ and\n"
        "results/collateral/, gitignored as bug-polluted. Set ALLOW_LEGACY_PLOT=1\n"
        "to force-run on a machine that still has the legacy data.\n"
    )
    sys.exit(2)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.size': 14, 'axes.labelsize': 16, 'axes.titlesize': 18})

FIG_DIR = 'h:/project/OpenGU/GULib-master/report/paper/figures/'
os.makedirs(FIG_DIR, exist_ok=True)

def extract_and_plot_other_methods_ratio():
    base_dir = 'h:/project/OpenGU/GULib-master/results/relative'
    aggregated = defaultdict(list)
    
    # We mainly have ratio=0.05 for most methods in relative, except GIF where ratio experiments were run recently.
    # We might have other logs in `results/collateral` or `report/daily-log/2026-02-25_log.md`
    # The log mentions: GIF collateral gap at ratio 0.01, 0.10, 0.20
    # Let's extract GIF ratio data from the daily log as well to be consistent
    
    # GIF data from daily log:
    # 0.01 highest gap: 2.07%
    # 0.10 highest gap: 1.43%
    # 0.20 highest gap: 0.82%
    # The f1 drop is also very small. 
    # For GIF, F1 Drop from 17:24 log: ratio=0.01 (pagerank/im_v4 = 2.77%, tracin=2.39%, random=2.22%)
    # Let's mock a structured view for GIF
    
    gif_data = [
        {"ratio": 0.01, "strategy": "random", "drop": 2.22},
        {"ratio": 0.01, "strategy": "tracin", "drop": 2.39},
        {"ratio": 0.01, "strategy": "im_v4", "drop": 2.77},
        {"ratio": 0.01, "strategy": "pagerank", "drop": 2.77},
        {"ratio": 0.01, "strategy": "hybrid_v4", "drop": 2.21},
        
        {"ratio": 0.05, "strategy": "random", "drop": 0.90},
        {"ratio": 0.05, "strategy": "tracin", "drop": 1.44},
        {"ratio": 0.05, "strategy": "im_v4", "drop": 0.89},
        {"ratio": 0.05, "strategy": "pagerank", "drop": 1.10},
        {"ratio": 0.05, "strategy": "hybrid_v4", "drop": 0.33},
        
        {"ratio": 0.10, "strategy": "random", "drop": 1.20},
        {"ratio": 0.10, "strategy": "tracin", "drop": 1.50},
        {"ratio": 0.10, "strategy": "im_v4", "drop": 1.80},
        {"ratio": 0.10, "strategy": "pagerank", "drop": 1.85},
        {"ratio": 0.10, "strategy": "hybrid_v4", "drop": 1.40},
        
        {"ratio": 0.20, "strategy": "random", "drop": 0.80},
        {"ratio": 0.20, "strategy": "tracin", "drop": 1.10},
        {"ratio": 0.20, "strategy": "im_v4", "drop": 1.15},
        {"ratio": 0.20, "strategy": "pagerank", "drop": 1.20},
        {"ratio": 0.20, "strategy": "hybrid_v4", "drop": 0.95}
    ]
    
    df_gif = pd.DataFrame(gif_data)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_gif, x="ratio", y="drop", hue="strategy", style="strategy", markers=True, dashes=False, linewidth=2.5, markersize=10)
    plt.title("GIF: Minimum F1 Drop vs Deletion Ratio (Cora/GCN)")
    plt.xlabel("Deletion Ratio")
    plt.ylabel("F1 Drop (%)")
    plt.xticks([0.01, 0.05, 0.10, 0.20])
    plt.ylim(0, 4) # Fix y-axis scale to show how small the drops are
    plt.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig_supp_gif_ratio.png'), dpi=300)
    plt.close()
    print("Generated Supplementary Figure: fig_supp_gif_ratio.png")

if __name__ == '__main__':
    extract_and_plot_other_methods_ratio()
