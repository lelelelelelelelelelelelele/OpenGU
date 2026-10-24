"""Figures from the complete accepted first-layer B analysis, with all controls."""
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'self/research/experiments/drafts/round3-b-diagnostics/e85r1'


def save(fig, name):
    for extension in ('pdf', 'svg', 'png'):
        fig.savefig(OUT / (name + '.' + extension), dpi=220)
    plt.close(fig)


def main():
    check_path = SOURCE / 'checks.json'
    checks = json.loads(check_path.read_text(encoding='utf-8'))
    if checks['status'] != 'passed' or checks['diagnostic_cells'] != 36:
        raise ValueError('B complete analysis is not verified')
    source = SOURCE / 'endpoints.csv'
    with source.open(encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(handle))
    keyed = {(r['method'], r['selector'], float(r['ratio']), int(r['seed'])): r for r in rows}
    methods, selectors, seeds = ('GIF', 'MEGU'), ('r_point', 'random', 'degree'), (42, 212, 2024)
    expected = {(m, s, b, seed) for m in methods for s in selectors for b in (.05, .33) for seed in seeds}
    if len(keyed) != len(rows) or set(keyed) != expected:
        raise ValueError('Incomplete or changed fixed B matrix')
    if any(int(r['node_count']) != 666 for r in rows):
        raise ValueError('test denominator drift')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    labels = {'r_point': 'R-point', 'random': 'Random', 'degree': 'Degree'}
    fig, axes = plt.subplots(2, 3, figsize=(7.1, 4.0), sharex=True, sharey=True)
    endpoints = [('original', 'Original', '#79838c', 's'), ('gu', 'GU', '#27658e', 'o'),
                 ('retrain', 'Retrain', '#c56727', '^')]
    for i, method in enumerate(methods):
        for j, selector in enumerate(selectors):
            ax = axes[i, j]
            for field, label, color, marker in endpoints:
                values = np.asarray([[float(keyed[(method, selector, budget, seed)][field + '_accuracy']) * 100
                                      for budget in (.05, .33)] for seed in seeds])
                ax.errorbar([5, 33], values.mean(axis=0), yerr=values.std(axis=0, ddof=1),
                            color=color, marker=marker, capsize=2, linewidth=1.2, markersize=3.5, label=label)
            ax.set_title(method + ' / ' + labels[selector], fontsize=8.5, loc='left')
            ax.set_xticks([5, 33])
            ax.set_xlim(2, 36)
            ax.grid(axis='y', color='#e2e6ea', linewidth=.6)
            if j == 0:
                ax.set_ylabel('Test accuracy (%)')
            if i == 1:
                ax.set_xlabel('Deletion budget (%)')
    handles, names = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, names, loc='upper center', ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, .91), pad=.9)
    save(fig, 'B_original_gu_retrain_accuracy')

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.3), sharey=True)
    components = [('ret_only_corrects', 'Ret-only corrects', '#388b7d'),
                  ('ret_only_harms', 'Ret-only harms', '#c56727'),
                  ('ret_only_both_wrong', 'Ret-only: both wrong', '#a7aeb4'),
                  ('other', 'Other GU-Ret disagreements', '#74618e')]
    groups = [(s, b) for s in selectors for b in (.05, .33)]
    totals_for_check = []
    for ax, method in zip(axes, methods):
        data = np.zeros((len(groups), 3, 4))
        totals = np.zeros((len(groups), 3))
        for j, (selector, budget) in enumerate(groups):
            for k, seed in enumerate(seeds):
                r = keyed[(method, selector, budget, seed)]
                total = round(float(r['gu_retrain_disagreement']) * 666)
                parts = [int(r[field]) for field, _, _ in components[:3]]
                parts.append(total - sum(parts))
                if min(parts) < 0 or sum(parts[:3]) != int(r['original_gu_equal_count']):
                    raise ValueError('Truth relation partition mismatch')
                data[j, k, :] = np.asarray(parts) / 666 * 100
                totals[j, k] = total / 666 * 100
        means = data.mean(axis=1)
        bottom = np.zeros(len(groups))
        for column, (_, label, color) in enumerate(components):
            ax.bar(np.arange(len(groups)), means[:, column], bottom=bottom,
                   color=color, width=.68, label=label)
            bottom += means[:, column]
        for k in range(3):
            ax.scatter(np.arange(len(groups)) + (k - 1) * .11, totals[:, k],
                       color='#202a32', marker='.', s=17, zorder=5)
        if not np.allclose(bottom, totals.mean(axis=1), atol=1e-12, rtol=0):
            raise ValueError('Stack does not reconstruct full disagreement')
        totals_for_check.append({'method': method, 'stack_reconstructs_all_D': True})
        ax.set_xticks(np.arange(len(groups)))
        ax.set_xticklabels([labels[s] + '\n' + str(int(b * 100)) + '%' for s, b in groups], fontsize=7)
        ax.set_title(method, fontsize=9, loc='left')
        ax.grid(axis='y', color='#e2e6ea', linewidth=.6)
        ax.set_axisbelow(True)
    axes[0].set_ylabel('GU-Ret disagreement (% of test nodes)')
    handles, names = axes[0].get_legend_handles_labels()
    fig.legend(handles, names, loc='upper center', ncol=2, frameon=False, fontsize=7.5)
    fig.tight_layout(rect=(0, 0, 1, .84), pad=.9)
    save(fig, 'B_truth_partition')
    record = {'source_csv': str(source.relative_to(ROOT)),
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'analysis_checks_sha256': hashlib.sha256(check_path.read_bytes()).hexdigest(),
              'matrix': {'methods': methods, 'selectors': selectors, 'budgets': [.05, .33], 'seeds': seeds},
              'accuracy_errors': 'sample SD across the three joint seeds',
              'truth_bars': 'equal-seed mean count / fixed N=666; black dots show each seed total D',
              'checks': totals_for_check,
              'scope': 'first-layer original evaluation graph; MEGU published postprocessing; no claim that graph/CS/training-quality controls pass'}
    (OUT / 'B_FIGURE_INPUTS.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps({'rendered': True, 'rows': len(rows), 'checks': totals_for_check}))


if __name__ == '__main__':
    main()
