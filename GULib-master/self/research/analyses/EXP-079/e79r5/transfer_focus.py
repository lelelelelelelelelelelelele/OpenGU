"""A bounded transfer illustration: fixed GNNDelete target, all three datasets."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
SOURCES = ['GCN', 'SGC', 'GAT', 'GIN']
DATASETS = ['Cora', 'PubMed', 'CiteSeer']


def build_transfer_focus():
    s = pd.read_csv(OUT / 'summary.csv').query("cohort == 'all10' and method == 'GNNDelete'")
    a = pd.read_csv(OUT / 'paired_seed_values.csv').query("method == 'GNNDelete'")
    assert len(s) == 24 and set(s.n) == {10}
    columns = ['dataset', 'method', 'selector', 'source', 'n', 'U_vs_random_mean',
               'U_vs_random_lo', 'U_vs_random_hi', 'U_vs_direct_mean',
               'U_vs_direct_lo', 'U_vs_direct_hi', 'U_vs_degree_mean',
               'U_vs_degree_lo', 'U_vs_degree_hi']
    export = s[columns].copy()
    export['degree_minus_random_mean'] = export.apply(
        lambda z: float((a[(a.dataset == z.dataset) & (a.source == 'GCN') &
                           (a.selector == 'gt_full')].U_degree -
                         a[(a.dataset == z.dataset) & (a.source == 'GCN') &
                           (a.selector == 'gt_full')].U_random).mean()), axis=1)
    export.to_csv(OUT / 'transfer_focus_10seeds.csv', index=False, encoding='utf-8')
    plt.rcParams.update({'font.family': 'Microsoft YaHei', 'axes.unicode_minus': False,
                         'pdf.fonttype': 42, 'svg.fonttype': 'path'})
    colors = {'gt_full': '#256d95', 'r_point': '#ce7544'}
    titles = ['Cora：gt_full 的正向增益可迁移',
              'PubMed：SGC 产生额外增益',
              'CiteSeer：未观察到清晰增益']
    fig, axes = plt.subplots(1, 3, figsize=(15.8, 6.4), sharey=True)
    fig.subplots_adjust(left=.075, right=.985, bottom=.23, top=.69, wspace=.10)
    x = np.array([0., 1.35, 2.35, 3.35])
    for ax, dataset, title in zip(axes, DATASETS, titles):
        ax.axvspan(-.52, .52, color='#eef1f4', zorder=0)
        ax.axvline(.73, color='#c6d0d8', lw=1)
        ax.axhline(0, color='#52616d', lw=1.3, zorder=1)
        degree = export.loc[export.dataset == dataset, 'degree_minus_random_mean'].iloc[0]
        ax.axhline(degree, color='#7e8192', ls=(0, (5, 3)), lw=1.1, zorder=1)
        for offset, selector in [(-.18, 'gt_full'), (.18, 'r_point')]:
            g = s[(s.dataset == dataset) & (s.selector == selector)].set_index('source').loc[SOURCES]
            mu = g.U_vs_random_mean.to_numpy()
            lo = g.U_vs_random_lo.to_numpy()
            hi = g.U_vs_random_hi.to_numpy()
            ax.bar(x + offset, mu, width=.32, color=colors[selector], zorder=3)
            ax.errorbar(x + offset, mu, yerr=np.array([mu-lo, hi-mu]), fmt='none',
                        color=colors[selector], capsize=3, elinewidth=1.25, zorder=4)
            # Labels in the two effect-bearing panels; avoid clutter at zero in CiteSeer.
            if dataset != 'CiteSeer':
                for pos, m, low, high in zip(x + offset, mu, lo, hi):
                    label = '0.0' if abs(m) < .05 else f'{m:+.1f}'
                    ax.text(pos, high+.45 if m >= 0 else low-.45, label,
                            ha='center', va='bottom' if m >= 0 else 'top',
                            fontsize=10, color=colors[selector], fontweight='bold')
        ax.set_title(title, loc='left', fontsize=13, fontweight='bold', pad=43, color='#183e55')
        ax.text(0, 1.04, 'GCN 参照', transform=ax.get_xaxis_transform(), ha='center', fontsize=10, color='#506575')
        ax.text(2.35, 1.04, '更换选点模型（surrogate）', transform=ax.get_xaxis_transform(), ha='center', fontsize=10, color='#506575')
        ax.set_xticks(x, SOURCES, fontsize=11)
        ax.set_xlim(-.6, 3.93)
        ax.set_ylim(-9, 14)
        ax.set_yticks([-5, 0, 5, 10])
        ax.tick_params(length=0, pad=7)
        ax.grid(axis='y', color='#e7ecef', lw=.7, zorder=0)
        for side in ['top', 'right', 'left']:
            ax.spines[side].set_visible(False)
        ax.spines['bottom'].set_color('#c6d0d8')
    axes[0].set_ylabel('相对 Random 的额外 F1 损失（pp）', fontsize=12, labelpad=12)
    fig.text(.037, .95, '换代理模型后，攻击增益能否保留？', fontsize=23, fontweight='bold', color='#15354a')
    fig.text(.037, .90, '固定目标：GNNDelete / GCN  ·  只改变选点模型  ·  全部 10 个训练 seed', fontsize=13, color='#526674')
    handles = [Patch(facecolor=colors['gt_full'], label='gt_full：显式计入邻域影响'),
               Patch(facecolor=colors['r_point'], label='r_point：点级 IF'),
               Line2D([0], [0], color='#52616d', label='Random（零线）'),
               Line2D([0], [0], color='#7e8192', ls='--', label='Degree（均值参照）')]
    fig.legend(handles=handles, loc='upper left', bbox_to_anchor=(.035, .862), ncol=4,
               frameon=False, fontsize=11, columnspacing=2.3)
    fig.text(.08, .143, 'Cora 正例：GCN 有增益，三个 surrogate 仍有增益；损伤幅度并不相同。', fontsize=12, color='#256d95', fontweight='bold')
    fig.text(.08, .092, '柱：十 seed 配对差均值；误差棒：点态 95% t 区间。Degree 虚线仅画均值，是否超过它以配对差区间为准。', fontsize=10, color='#526674')
    fig.text(.08, .047, '固定 split、10% 删除预算；图示为 GNNDelete 的条件性迁移案例，其他 GU 见完整矩阵。未作多重比较调整。', fontsize=10, color='#526674')
    for ext in ['png', 'svg', 'pdf']:
        path = OUT / f'transfer_focus_10seeds.{ext}'
        fig.savefig(path, dpi=180, facecolor='white')
        if ext == 'svg':
            path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


if __name__ == '__main__':
    build_transfer_focus()
