"""Render the historical EXP-080 CiteSeer budget responses for the paper draft.

Input: versioned full-20261021 curve summaries, with IM draws averaged within
training seed. Original execution provenance remains owned by that analysis.
Run with matplotlib installed; no experiment is launched or pooled with later runs.
"""

import csv
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullLocator

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'report/paper/overleaf/figures/citeseer_selector_responses.pdf'
SOURCE = ROOT / 'self/research/analyses/EXP-080/full-20261021/condition_summary.csv'
SELECTORS = ['random', 'degree', 'r_point', 'gt_full', 'im_rr_greedy']
TITLES = ['Random', 'Degree', 'R-point', 'D-full', 'IM-RR']
METHODS = ['GIF', 'IDEA', 'MEGU', 'GNNDelete', 'GraphEraser', 'GraphRevoker', 'Retrain']
COLORS = ['#286AAB', '#4EA8CF', '#26988C', '#D37B22', '#925BA1', '#B94F56', '#000000']
MARKERS = ['o', 's', 's', '^', 'D', 'P', 'x']
LINESTYLES = ['-', '--', '-', '-', '-', '-', '--']
RATIOS = [.05, .075, .1, .15, .22, .33, .5]

with SOURCE.open(encoding='utf-8', newline='') as f:
    rows = [r for r in csv.DictReader(f)
            if r['dataset'] == 'CiteSeer' and r['selector'] in SELECTORS]
# Read each method's own summary, including IDEA's independent source rows.
assert len(rows) == len(SELECTORS) * len(METHODS) * len(RATIOS)
assert len({(r['selector'], r['method'], r['ratio']) for r in rows}) == len(rows)

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 7,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': .55, 'xtick.major.width': .5, 'ytick.major.width': .5,
    'xtick.major.size': 2.2, 'ytick.major.size': 2.2,
    'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
    'pdf.fonttype': 42,
})
fig, axes = plt.subplots(2, len(SELECTORS), figsize=(7.05, 2.85), sharex=True, sharey='row')
for col, (selector, title) in enumerate(zip(SELECTORS, TITLES)):
    for row, metric in enumerate(['accuracy', 'disagreement']):
        ax = axes[row, col]
        for method, color, marker, linestyle in zip(METHODS, COLORS, MARKERS, LINESTYLES):
            if method == 'Retrain' and metric == 'disagreement':
                ax.axhline(0, color=color, lw=.8, ls='--')
                continue
            points = sorted([r for r in rows if r['selector'] == selector
                             and r['method'] == method],
                            key=lambda r: float(r['ratio']))
            assert [float(r['ratio']) for r in points] == RATIOS, (selector, metric, method)
            assert all(int(r[metric + '_count']) == 3 for r in points), (selector, metric, method)
            x = [100 * float(r['ratio']) for r in points]
            y = [float(r[metric + '_mean']) for r in points]
            sd = [float(r[metric + '_std']) for r in points]
            ax.fill_between(x, [a-b for a, b in zip(y, sd)],
                            [a+b for a, b in zip(y, sd)],
                            color=color, alpha=.075, linewidth=0)
            ax.plot(x, y, color=color, lw=1.35 if method == 'GIF' else 1.05,
                    ls=linestyle, marker=marker, ms=3.3 if method == 'IDEA' else 2.4,
                    markerfacecolor='none' if method == 'IDEA' else color,
                    markeredgewidth=.55 if method == 'IDEA' else .3,
                    zorder=4 if method == 'Retrain' else 3, label=method)
        ax.set_xscale('log')
        ax.set_xlim(4.5, 55)
        ax.set_xticks([5, 10, 22, 50], labels=['5', '10', '22', '50'])
        ax.xaxis.set_minor_locator(NullLocator())
        ax.tick_params(pad=2)
        ax.grid(axis='y', color='#e5e8ec', lw=.45)
        ax.set_axisbelow(True)
    axes[0, col].set_title(title, fontsize=7, fontweight='normal', pad=5)

axes[0, 0].set_ylim(45, 80)
axes[0, 0].set_yticks([50, 60, 70, 80])
axes[1, 0].set_ylim(-2, 50)
axes[1, 0].set_yticks([0, 20, 40])
axes[0, 0].set_ylabel('Accuracy (%)', fontsize=7.5, labelpad=4)
axes[1, 0].set_ylabel('Disagreement (%)', fontsize=7.5, labelpad=4)
fig.supxlabel('Deletion budget (% of training candidates; log scale)', fontsize=7.5, y=.015)
handles = [Line2D([0], [0], color=c, lw=.8,
                  ls=ls, marker=m, ms=2.8 if method == 'IDEA' else 2.3,
                  markerfacecolor='none' if method == 'IDEA' else c,
                  markeredgewidth=.4 if method == 'IDEA' else .25, label=method)
           for c, method, m, ls in zip(COLORS, METHODS, MARKERS, LINESTYLES)]
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52, 1.006),
           ncol=7, frameon=False, columnspacing=1.25, handlelength=1.6,
           handletextpad=.4, prop={'size': 6, 'weight': 'normal'})
fig.subplots_adjust(left=.074, right=.994, top=.817, bottom=.155,
                    wspace=.13, hspace=.19)
fig.savefig(OUT, facecolor='white')
plt.close(fig)
print('Validated 5 selectors x 7 methods x 7 budgets, with 3 training seeds per series; GIF and IDEA drawn from separate source rows. Saved ' + str(OUT))
