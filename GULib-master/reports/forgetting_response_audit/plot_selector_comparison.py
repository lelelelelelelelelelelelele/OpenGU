"""Paper-style selector curves from the verified EXP-032 analysis (no training)."""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
CORE = ['random', 'degree', 'r_point', 'gt_full']
STYLES = {
    'random': ('Random', '#44423c', 's', '--'),
    'degree': ('Degree', '#79943b', '^', '--'),
    'r_point': ('r_point', '#1675ac', 'o', '-'),
    'gt_full': ('gt_full', '#b84050', 'D', '-'),
    'gt_simple': ('gt_simple', '#af7f22', 'v', ':'),
    'p_graph': ('p_graph', '#9671b5', 'P', '-.'),
    'p_point': ('p_point', '#38a398', 'X', '-.'),
    'gt_full_all_trainable': ('gt_full / all trainable', '#c26c25', '>', ':'),
    'gt_full_all_trainable_hops3': ('gt_full / all trainable / 3 hops', '#9b8267', '<', ':'),
    'gt_full_sgc_all_trainable_hops3': ('gt_full / SGC / all trainable / 3 hops', '#ac63a0', '*', ':'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def draw(data, selectors, stem, show_sd):
    paper = '#f5edda'
    ink = '#514537'
    plt.rcParams.update({
        'font.family': 'DejaVu Serif', 'font.size': 11,
        'text.color': ink, 'axes.labelcolor': ink, 'axes.edgecolor': '#8d806b',
        'xtick.color': ink, 'ytick.color': ink, 'grid.color': '#b5aa94',
        'axes.facecolor': paper, 'figure.facecolor': paper,
        'svg.fonttype': 'none', 'pdf.fonttype': 42,
    })
    fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.25))
    for index, (ax, dataset) in enumerate(zip(axes, DATASETS)):
        for selector in selectors:
            group = data[(data.dataset == dataset) & (data.selector == selector)].sort_values('ratio')
            assert group.ratio.tolist() == [.01, .05, .10, .15]
            x = group.ratio_percent.to_numpy(float)
            y = group['mean'].to_numpy(float)
            sd = group.sd.to_numpy(float)
            label, color, marker, line = STYLES[selector]
            ax.plot(x, y, label=label, color=color, marker=marker,
                    linestyle=line, linewidth=2.2 if selector in CORE else 1.25,
                    markersize=6 if selector in CORE else 4.5, zorder=3)
            if show_sd:
                ax.fill_between(x, y-sd, y+sd, color=color, alpha=.095, linewidth=0, zorder=1)
        ax.set_xticks([1, 5, 10, 15], ['1%', '5%', '10%', '15%'])
        ax.set_xlim(.35, 15.65)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
        ax.set_xlabel('Deletion ratio', fontsize=14, labelpad=8)
        ax.set_ylabel('Retrain accuracy (%)', fontsize=13, labelpad=6)
        ax.tick_params(labelsize=10)
        ax.grid(linestyle=':', alpha=.65, linewidth=.7)
        ax.set_axisbelow(True)
        ax.text(.5, -.31, f'({chr(97+index)}) {dataset}', ha='center',
                transform=ax.transAxes, fontsize=18)
    handles, labels = axes[0].get_legend_handles_labels()
    ncol = 4 if len(selectors) == 4 else 5
    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(.5, .91),
               ncol=ncol, frameon=False, fontsize=11 if show_sd else 8.5,
               handlelength=2.5, columnspacing=2)
    fig.suptitle('Retraining accuracy under different deletion selectors',
                 fontsize=19, y=.99)
    footnote = ('Lines: means over 3 training seeds. Shading: +/- 1 sample SD (not CI). '
                if show_sd else 'All 10 selector configurations; lines are 3-seed means. Parameter variants are not independent methods. ')
    fig.text(.5, .018, footnote + '\nEXP-032 | Retrain only | Measured ratios: 1%, 5%, 10%, 15% | Panel y-scales differ; no 0% baseline.',
             ha='center', fontsize=9, color='#685d50')
    fig.subplots_adjust(left=.055, right=.985, top=.78 if show_sd else .73,
                        bottom=.255, wspace=.28)
    assert all(len(ax.lines) == len(selectors) for ax in axes)
    for ext in ['png', 'svg', 'pdf']:
        fig.savefig(OUT / f'{stem}.{ext}', dpi=220, facecolor=paper, bbox_inches='tight')
    plt.close(fig)


def main():
    receipt = json.loads((OUT/'ratio_verification.json').read_text(encoding='utf-8'))
    source = OUT/'ratio_condition_summary.csv'
    assert digest(source) == receipt['output_sha256'][source.name]
    data = pd.read_csv(source)
    assert len(data) == 120 and data.n.eq(3).all()
    assert set(data.selector) == set(STYLES)
    raw_path = OUT/'ratio_cells.csv'
    assert digest(raw_path) == receipt['output_sha256'][raw_path.name]
    raw = pd.read_csv(raw_path)
    grouped = raw.groupby(['dataset', 'selector', 'ratio']).accuracy.agg(['mean', 'std']).sort_index()
    source_values = data.set_index(['dataset', 'selector', 'ratio']).sort_index()
    assert np.allclose(grouped['mean'], source_values['mean'], atol=1e-10, rtol=0)
    assert np.allclose(grouped['std'], source_values.sd, atol=1e-10, rtol=0)
    draw(data, CORE, 'selector_retrain_accuracy', True)
    draw(data, list(STYLES), 'selector_retrain_accuracy_all', False)
    result = {
        'experiment': 'EXP-032', 'execution_sha': receipt['execution_sha'],
        'source': source.name, 'source_sha256': digest(source),
        'checks': {'all_120_means_and_sample_sd_match_seed_rows': True,
                   'ratios_only_1_5_10_15': True, 'n_training_seeds': 3,
                   'main_series_per_panel': 4, 'all_config_series_per_panel': 10},
        'limitations': ['Retrain only; no GU, Original, fidelity, or logit-distance curve.',
                        'Main figure shading is sample SD, not a confidence interval.',
                        'Panel y-scales differ. All-config figure displays means only.'],
        'delivery_top_level_status': receipt['delivery_top_level_status'],
        'new_gpu_runs': 0,
        'output_sha256': {f'{stem}.{ext}': digest(OUT/f'{stem}.{ext}')
                          for stem in ['selector_retrain_accuracy', 'selector_retrain_accuracy_all']
                          for ext in ['png', 'svg', 'pdf']},
        'script_sha256': digest(Path(__file__)),
        'visual_review': 'NOT OBSERVED',
    }
    (OUT/'selector_plot_verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result['checks'], ensure_ascii=False))


if __name__ == '__main__':
    main()
