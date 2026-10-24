"""Render the two predeclared A phases without pooling seeds or selecting effects."""
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
ANALYSIS = ROOT / 'self/research/experiments/drafts/round3-execution-prep'


def rows(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def main():
    phases = [('e84r1', 'Ten-seed reconstruction', {42, 212, 2024, 0, 1, 2, 3, 4, 5, 6}),
              ('e84c1', 'Five-seed confirmation', {1701, 1709, 1721, 1733, 1741})]
    inputs = []
    data = []
    for rid, label, expected in phases:
        path = ANALYSIS / rid / 'endpoints.csv'
        records = rows(path)
        if {int(r['seed']) for r in records} != expected:
            raise ValueError('phase seed scope differs: ' + rid)
        keyed = {(int(r['seed']), r['selector'], r['method']): r for r in records}
        if len(keyed) != len(records) or len(records) != len(expected) * 6:
            raise ValueError('phase is not the full three-request/two-method matrix')
        for seed in expected:
            for method in ('Retrain', 'GNNDelete'):
                for selector in ('r_point_sgc.yaml', 'gt_full_sgc.yaml', 'degree.yaml'):
                    if (seed, selector, method) not in keyed:
                        raise ValueError('missing predeclared coordinate')
        inputs.append({'run': rid, 'path': str(path.relative_to(ROOT)),
                       'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'seeds': sorted(expected), 'rows': len(records)})
        data.append((label, expected, keyed))
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    fig, axes = plt.subplots(2, 2, figsize=(7.1, 4.3), sharey=True)
    colors = {'Retrain': '#27658e', 'GNNDelete': '#c56727'}
    methods = ('Retrain', 'GNNDelete')
    selectors = ('r_point_sgc.yaml', 'gt_full_sgc.yaml', 'degree.yaml')
    for column, (label, seeds, keyed) in enumerate(data):
        for row, method in enumerate(methods):
            ax = axes[row, column]
            values = np.asarray([[float(keyed[(seed, s, method)]['accuracy_pct'])
                                  for s in selectors] for seed in sorted(seeds)])
            for v in values:
                ax.plot([0, 1, 2], v, color=colors[method], alpha=.25,
                        linewidth=.7, marker='o', markersize=2.3)
            ax.plot([0, 1, 2], values.mean(axis=0), color=colors[method],
                    linewidth=1.8, marker='D', markersize=4, label='Mean')
            ax.set_xticks([0, 1, 2])
            ax.set_xticklabels(['R-point', 'D-full', 'Degree'])
            ax.grid(axis='y', color='#e2e6ea', linewidth=.6)
            ax.set_title(label + '\n' + method, fontsize=9, loc='left')
            if column == 0:
                ax.set_ylabel('Test accuracy (%)')
            ax.set_xlim(-.15, 2.15)
    fig.tight_layout(pad=1.0)
    for extension in ('pdf', 'svg', 'png'):
        fig.savefig(OUT / ('A_two_phase_endpoints.' + extension), dpi=220)
    plt.close(fig)
    (OUT / 'A_FIGURE_INPUTS.json').write_text(
        json.dumps({'inputs': inputs, 'pooled_seeds': False,
                    'emphasis': 'all three predeclared requests, every seed, raw accuracy',
                    'scientific_gate': 'read the phase decision files; plot does not decide'},
                   ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'rendered': True, 'inputs': inputs}, ensure_ascii=False))


if __name__ == '__main__':
    main()
