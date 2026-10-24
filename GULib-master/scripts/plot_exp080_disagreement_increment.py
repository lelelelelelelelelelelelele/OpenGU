"""Plot signed disagreement increments against same-budget Random for EXP-080.

Uses the existing CiteSeer seed aggregates; IM draws have already been averaged
within training seed. Differences and sample SD are computed from paired seeds.
The paper's Fig. 4 remains unchanged.
"""

import csv
from collections import defaultdict
from pathlib import Path
import statistics

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import NullLocator

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'self/research/analyses/EXP-080/full-20261021/seed_values.csv'
OUT = ROOT / 'report/paper/figures/exp080-ratio-response-20261025'
SELECTORS = ['degree', 'r_point', 'gt_full', 'im_rr_greedy']
TITLES = ['Degree', 'R-point', 'D-full', 'IM-RR']
METHODS = ['GIF', 'IDEA', 'MEGU', 'GNNDelete', 'GraphEraser', 'GraphRevoker']
COLORS = ['#286AAB', '#4EA8CF', '#26988C', '#D37B22', '#925BA1', '#B94F56']
MARKERS = ['o', 's', 's', '^', 'D', 'P']
STYLES = ['-', '--', '-', '-', '-', '-']
RATIOS = [.05, .075, .1, .15, .22, .33, .5]


def main():
    with SOURCE.open(encoding='utf-8', newline='') as stream:
        rows = [r for r in csv.DictReader(stream)
                if r['dataset'] == 'CiteSeer' and r['method'] in METHODS]
    indexed = {(r['selector'], r['method'], float(r['ratio']), r['seed']): r for r in rows}
    assert len(indexed) == len(rows) == 5 * 6 * 7 * 3
    groups = defaultdict(list)
    paired = []
    for selector in SELECTORS:
        for method in METHODS:
            for ratio in RATIOS:
                for seed in ['42', '212', '2024']:
                    r = indexed[(selector, method, ratio, seed)]
                    baseline = indexed[('random', method, ratio, seed)]
                    value, random_value = float(r['disagreement']), float(baseline['disagreement'])
                    delta = value - random_value
                    groups[(selector, method, ratio)].append(delta)
                    paired.append({'selector': selector, 'method': method, 'ratio': ratio, 'seed': seed,
                                   'disagreement_selector': value, 'disagreement_random': random_value,
                                   'delta_disagreement_pp': delta})
    assert len(paired) == 504 and len(groups) == 168
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / 'disagreement_increment_seed_values.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(paired[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(paired)

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.linewidth': .55, 'xtick.major.width': .5, 'ytick.major.width': .5,
                         'xtick.major.size': 2.2, 'ytick.major.size': 2.2,
                         'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5, 'pdf.fonttype': 42})
    fig, axes = plt.subplots(1, 4, figsize=(7.05, 2.25), sharex=True, sharey=True)
    for ax, selector, title in zip(axes, SELECTORS, TITLES):
        for method, color, marker, style in zip(METHODS, COLORS, MARKERS, STYLES):
            values = [groups[(selector, method, ratio)] for ratio in RATIOS]
            mean = [statistics.mean(v) for v in values]
            sd = [statistics.stdev(v) for v in values]
            x = [100 * ratio for ratio in RATIOS]
            ax.fill_between(x, [m-s for m, s in zip(mean, sd)], [m+s for m, s in zip(mean, sd)],
                            color=color, alpha=.085, linewidth=0)
            ax.plot(x, mean, color=color, lw=1.3 if method == 'GIF' else 1.05,
                    ls=style, marker=marker, ms=3.3 if method == 'IDEA' else 2.4,
                    markerfacecolor='none' if method == 'IDEA' else color,
                    markeredgewidth=.55 if method == 'IDEA' else .3)
        ax.axhline(0, color='black', ls='--', lw=.8, zorder=1)
        ax.set_title(title, fontsize=7, fontweight='normal', pad=5)
        ax.set_xscale('log')
        ax.set_xlim(4.5, 55)
        ax.set_xticks([5, 10, 22, 50], labels=['5', '10', '22', '50'])
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_ylim(-6, 38)
        ax.set_yticks([-5, 0, 10, 20, 30])
        ax.grid(axis='y', color='#e5e8ec', lw=.45)
        ax.set_axisbelow(True)
        ax.tick_params(pad=2)
    axes[0].set_ylabel('Disagreement increment\nvs Random (pp)', fontsize=7.5, labelpad=4)
    fig.supxlabel('Deletion budget (% of training candidates; log scale)', fontsize=7.5, y=.015)
    handles = [Line2D([0], [0], color=color, lw=.8, ls=style, marker=marker,
                      ms=2.8 if method == 'IDEA' else 2.3,
                      markerfacecolor='none' if method == 'IDEA' else color,
                      markeredgewidth=.4 if method == 'IDEA' else .25, label=method)
               for method, color, marker, style in zip(METHODS, COLORS, MARKERS, STYLES)]
    fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.52, 1.005),
               ncol=6, frameon=False, columnspacing=1.7, handlelength=1.6,
               handletextpad=.4, prop={'size': 6, 'weight': 'normal'})
    fig.subplots_adjust(left=.089, right=.994, top=.76, bottom=.235, wspace=.14)
    fig.savefig(OUT / 'disagreement_increment.pdf', facecolor='white', metadata={'CreationDate': None})
    fig.savefig(OUT / 'disagreement_increment.png', dpi=240, facecolor='white')
    plt.close(fig)
    print('Saved 168 signed mean/SD points from 504 paired seed contrasts; negative values retained.')


if __name__ == '__main__':
    main()
