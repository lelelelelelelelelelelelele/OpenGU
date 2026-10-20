# -*- coding: utf-8 -*-
"""Five-selector descriptive comparisons from the verified EXP-080 table."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent
ROOT = next(p for p in OUT.parents if (p / 'experiments/modular_run.py').exists())
proof = json.loads((OUT / 'statistics_validation.json').read_text(encoding='utf-8'))
assert proof['passed']
assert hashlib.sha256((OUT / 'cells.csv').read_bytes()).hexdigest() == proof['input_sha256']
raw = pd.read_csv(OUT / 'cells.csv')
keys = ['dataset', 'method', 'selector', 'ratio']
methods = ['GIF', 'MEGU', 'GNNDelete', 'GraphEraser', 'GraphRevoker']
selectors = ['random', 'degree', 'r_point', 'gt_full', 'im_rr_greedy']
labels = ['Random', 'Degree', 'r_point', 'gt_full', 'IM-RR']
ratios = [.05, .075, .1, .15, .22, .33, .5]
seed = raw.groupby(keys + ['seed'], as_index=False)[['accuracy', 'disagreement']].mean()
random = seed[seed.selector == 'random'].drop(columns='selector')
paired = seed.merge(random, on=['dataset', 'method', 'ratio', 'seed'],
                    suffixes=('', '_random'), validate='many_to_one')
paired['H'] = paired.accuracy_random - paired.accuracy
paired['D_extra'] = paired.disagreement - paired.disagreement_random
retrain = paired[paired.method == 'Retrain'][['dataset', 'selector', 'ratio', 'seed', 'H']]
paired = paired.merge(retrain.rename(columns={'H': 'H_retrain'}),
                      on=['dataset', 'selector', 'ratio', 'seed'], validate='many_to_one')
paired['interaction'] = paired.H - paired.H_retrain
paired.to_csv(OUT / 'strategy_seed_contrasts.csv', index=False, encoding='utf-8')
summary = paired.groupby(keys)[['H', 'D_extra', 'interaction']].agg(['mean', 'std'])
summary.columns = ['_'.join(c) for c in summary.columns]
summary = summary.reset_index()
summary.to_csv(OUT / 'strategy_summary.csv', index=False, encoding='utf-8')

# Keep repeated training seeds distinct from independent deletion requests.
requests = raw[raw.method == 'Retrain'].groupby(['dataset', 'selector', 'ratio'])[
    'selected_nodes_sha256'].nunique().reset_index(name='distinct_node_sets')
assert requests[requests.selector.isin(['random', 'degree'])].distinct_node_sets.eq(1).all()
assert requests[requests.selector == 'im_rr_greedy'].distinct_node_sets.eq(3).all()
requests.to_csv(OUT / 'strategy_request_counts.csv', index=False, encoding='utf-8')

# Inspect the unaveraged IM draws without treating the 3x3 grid as 9 independent seeds.
im = raw[raw.selector == 'im_rr_greedy']
random_raw = raw[raw.selector == 'random']
draws = im.merge(random_raw[['dataset', 'method', 'ratio', 'seed', 'accuracy']],
                 on=['dataset', 'method', 'ratio', 'seed'], suffixes=('', '_random'),
                 validate='many_to_one')
draws['H'] = draws.accuracy_random - draws.accuracy
draws[['dataset', 'method', 'ratio', 'seed', 'im_seed', 'accuracy', 'H']].to_csv(
    OUT / 'im_draw_contrasts.csv', index=False, encoding='utf-8')
spread = im.groupby(['dataset', 'method', 'ratio', 'seed']).accuracy.agg(
    ['min', 'max']).reset_index()
spread['range_pp'] = spread['max'] - spread['min']
spread.to_csv(OUT / 'im_draw_ranges.csv', index=False, encoding='utf-8')

# Raw strength and centered GU profile shape are separate summaries.
# Only 5-33% has all five nonduplicate GU coordinates on both datasets.
distances = []
for ds in ['Cora', 'CiteSeer']:
    for ratio in ratios[:-1]:
        for training_seed in [42, 212, 2024]:
            rows = paired[(paired.dataset == ds) & (paired.ratio == ratio) &
                          (paired.seed == training_seed)]
            for scope, used in [('five_GU', methods), ('without_GNNDelete', [m for m in methods if m != 'GNNDelete'])]:
                vectors = rows[rows.method.isin(used)].pivot(index='selector', columns='method', values='H').loc[selectors, used]
                a = vectors.loc['im_rr_greedy'].to_numpy()
                for comparator in selectors[:-1]:
                    b = vectors.loc[comparator].to_numpy()
                    distances.append(dict(dataset=ds, ratio=ratio, seed=training_seed, scope=scope,
                                          comparator=comparator, raw_rms_pp=float(np.sqrt(np.mean((a-b)**2))),
                                          centered_rms_pp=float(np.sqrt(np.mean(((a-a.mean())-(b-b.mean()))**2)))))
pd.DataFrame(distances).to_csv(OUT / 'im_profile_distances.csv', index=False, encoding='utf-8')

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                     'axes.spines.top': False, 'axes.spines.right': False})


def save(fig, name):
    fig.savefig(OUT / (name + '.png'), dpi=180, bbox_inches='tight')
    fig.savefig(OUT / (name + '.pdf'), bbox_inches='tight')
    plt.close(fig)

# Within-selector views: every GU shares a panel, datasets sit side by side.
# Retain paired uncertainty for H and training-seed uncertainty for raw metrics.
shown_methods = ['Retrain'] + methods
method_colors = dict(zip(shown_methods, ['#20252e', '#196f91', '#bd7a18', '#c54236', '#2b8b65', '#6e6c9b']))
curve_rows = []
for metric, label, name in [
    ('accuracy', 'Test accuracy (%)', 'selector_gu_accuracy'),
    ('H', 'Extra accuracy loss vs Random (pp)', 'selector_gu_extra_loss'),
    ('disagreement', 'GU vs Retrain disagreement (%)', 'selector_gu_disagreement')
]:
    source = paired if metric == 'H' else seed
    curves = source[source.method.isin(shown_methods)].groupby(keys)[metric].agg(['mean', 'std', 'count']).reset_index()
    measured = curves[curves['count'] > 0].copy()
    assert measured['count'].eq(3).all()
    measured['metric'] = metric
    curve_rows.append(measured)
    fig, axes = plt.subplots(5, 2, figsize=(13, 18))
    for i, (selector, selector_label) in enumerate(zip(selectors, labels)):
        scope = measured[measured.selector == selector]
        lo = float((scope['mean'] - scope['std']).min())
        hi = float((scope['mean'] + scope['std']).max())
        if metric == 'H':
            extent = max(1.0, np.ceil(max(abs(lo), abs(hi)) * 1.08))
            limits = (-extent, extent)
        elif metric == 'disagreement':
            limits = (-2, max(5, np.ceil(hi * 1.08)))
        else:
            padding = max(1.0, (hi-lo)*.08)
            limits = (max(0, lo-padding), min(100, hi+padding))
        for j, ds in enumerate(['Cora', 'CiteSeer']):
            ax = axes[i, j]
            for method in shown_methods:
                values = scope[(scope.dataset == ds) & (scope.method == method)].sort_values('ratio')
                if values.empty:
                    continue
                x = 100 * values.ratio.to_numpy()
                y, sd = values['mean'].to_numpy(), values['std'].to_numpy()
                display = {'GIF': 'GIF / IDEA', 'GraphRevoker': 'GraphRevoker*'}.get(method, method)
                ax.plot(x, y, marker='o', ms=3.5, lw=1.8, color=method_colors[method], label=display)
                ax.fill_between(x, y-sd, y+sd, color=method_colors[method], alpha=.08)
            if metric == 'disagreement':
                ax.plot([5, 50], [0, 0], ':', color=method_colors['Retrain'], lw=1.3,
                        label='Retrain vs itself = 0')
            if metric == 'H':
                ax.axhline(0, color='#6b7280', lw=.7, ls=':')
                if selector == 'random':
                    ax.text(.03, .83, 'All methods = 0 by definition', transform=ax.transAxes, fontsize=9)
            ax.set_ylim(*limits)
            ax.set_title(selector_label + ' | ' + ds, fontsize=12, fontweight='bold')
            ax.set_xticks([5, 10, 15, 22, 33, 50])
            ax.set_xlabel('Deleted training candidates (%)')
            ax.set_ylabel(label)
            ax.grid(alpha=.18)
    handles, legend_labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(.5, .958),
               ncol=3, fontsize=11, frameon=False)
    fig.suptitle('Within each selector: all GU methods across deletion budgets\n' + label, fontsize=16, y=.992)
    fig.text(.5, .012, 'Mean +/- sample SD across 3 training seeds; IM draws averaged first.\n'
             'Same y scale within each row; y scales differ across selectors. * GraphRevoker = GPA + optimal.\n'
             'Cora sharded curves stop at 33% (50% unavailable). GIF/IDEA overlap and are drawn once.',
             ha='center', fontsize=10)
    fig.tight_layout(rect=[.01, .06, .99, .92], h_pad=2)
    save(fig, name)
pd.concat(curve_rows, ignore_index=True).to_csv(OUT / 'selector_gu_curve_values.csv', index=False, encoding='utf-8')


# Every selector, every budget, shared color scale. Grey cells are infeasible, not zero.
for metric, title, limit, name in [
    ('H_mean', 'Extra accuracy loss vs Random (pp); positive = more loss', 27, 'strategy_loss_atlas'),
    ('D_extra_mean', 'Extra GU-Retrain disagreement vs Random (pp)', 30, 'strategy_disagreement_atlas')
]:
    fig, axes = plt.subplots(2, 6, figsize=(18, 6.6))
    shown = ['Retrain'] + methods
    cmap = plt.get_cmap('RdBu_r').copy()
    cmap.set_bad('#dedede')
    for i, ds in enumerate(['Cora', 'CiteSeer']):
        for j, method in enumerate(shown):
            ax = axes[i, j]
            z = summary[(summary.dataset == ds) & (summary.method == method)]
            matrix = z.pivot(index='selector', columns='ratio', values=metric).reindex(index=selectors, columns=ratios)
            if metric == 'D_extra_mean' and method == 'Retrain':
                ax.axis('off'); ax.text(.5, .5, ds + '\nRetrain self-reference\nNo measured disagreement', ha='center')
                continue
            implot = ax.imshow(matrix.to_numpy(), vmin=-limit, vmax=limit, cmap=cmap, aspect='auto')
            ax.set_xticks(range(7)); ax.set_xticklabels(['5', '7.5', '10', '15', '22', '33', '50'], fontsize=7)
            ax.set_yticks(range(5)); ax.set_yticklabels(labels if j == 0 else [''] * 5)
            ax.set_title(ds + ' | ' + method + ('*' if method == 'GraphRevoker' else ''), fontsize=10)
            ax.set_xlabel('Deletion (%)')
    fig.subplots_adjust(left=.075, right=.92, top=.84, bottom=.12, wspace=.22, hspace=.45)
    fig.colorbar(implot, cax=fig.add_axes([.935, .2, .012, .55]), label='Percentage points')
    fig.suptitle(title + '\n3 training seeds; IM draws averaged within seed; GIF/IDEA represented once', fontsize=13)
    fig.text(.5, .02, '* GraphRevoker = GPA + optimal. Grey = unavailable Cora sharded 50%. Random is the zero reference.', ha='center', fontsize=9)
    save(fig, name)

colors = dict(zip(selectors, ['#20252e', '#2b8b65', '#c54236', '#9c53a5', '#196f91']))
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
for j, ds in enumerate(['Cora', 'CiteSeer']):
    for sel, label in zip(selectors, labels):
        z = seed[(seed.dataset == ds) & (seed.method == 'GNNDelete') & (seed.selector == sel)]
        g = z.groupby('ratio').accuracy.agg(['mean', 'std']).reindex(ratios)
        x = 100 * np.array(ratios)
        axes[0, j].plot(x, g['mean'], marker='o', color=colors[sel], label=label)
        z = summary[(summary.dataset == ds) & (summary.method == 'GNNDelete') & (summary.selector == sel)].set_index('ratio').reindex(ratios)
        axes[1, j].plot(x, z.H_mean, marker='o', color=colors[sel])
        if sel == 'im_rr_greedy':
            axes[1, j].fill_between(x, (z.H_mean-z.H_std).to_numpy(), (z.H_mean+z.H_std).to_numpy(), color=colors[sel], alpha=.15)
    axes[0, j].set_title(ds + ' | GNNDelete accuracy')
    axes[1, j].set_title(ds + ' | Extra loss relative to Random')
    axes[0, j].set_ylabel('Accuracy (%)')
    axes[1, j].set_ylabel('Extra loss (pp)')
    for ax in axes[:, j]:
        ax.set_xticks([5, 15, 22, 33, 50]); ax.set_xlabel('Deletion (%)'); ax.grid(alpha=.2)
    axes[1, j].axhline(0, color='grey', lw=.8)
fig.legend(*axes[0, 0].get_legend_handles_labels(), loc='lower center', ncol=5)
fig.suptitle('All selectors on GNNDelete: absolute performance and moving Random reference\nOnly IM paired sample SD is shaded; 3 training seeds, not a confidence interval', fontsize=12)
fig.tight_layout(rect=[0, .05, 1, .92])
save(fig, 'strategy_gnndelete')


def table(headers, rows):
    return '| ' + ' | '.join(headers) + ' |\n| ' + ' | '.join(['---'] * len(headers)) + ' |\n' + '\n'.join('| ' + ' | '.join(map(str, row)) + ' |' for row in rows)


def number(ds, method, sel, ratio, metric='H_mean'):
    return float(summary[(summary.dataset == ds) & (summary.method == method) &
                         (summary.selector == sel) & (summary.ratio == ratio)].iloc[0][metric])


mainrows = []
for ds in ['Cora', 'CiteSeer']:
    for sel, label in zip(selectors, labels):
        mainrows.append([ds, label] + [f'{number(ds, m, sel, .33):+.2f}' for m in ['Retrain'] + methods])
imrows = []
for ds in ['Cora', 'CiteSeer']:
    for ratio in ratios:
        z = draws[(draws.dataset == ds) & (draws.method == 'GNNDelete') & (draws.ratio == ratio)]
        imrows.append([ds, f'{100*ratio:g}%', f'{number(ds,"GNNDelete","im_rr_greedy",ratio):+.2f}',
                       f'{number(ds,"GNNDelete","im_rr_greedy",ratio,"H_std"):.2f}',
                       f'{(z.H>0).sum()}/9', f'{z.H.min():+.2f} 至 {z.H.max():+.2f}'])
distance_df = pd.DataFrame(distances)
distance_summary = distance_df.groupby(['dataset','scope','comparator'])[['raw_rms_pp','centered_rms_pp']].mean().reset_index()
distance_summary.to_csv(OUT / 'im_profile_distance_summary.csv', index=False, encoding='utf-8')
distance_rows = [[r.dataset, r.scope, r.comparator, f'{r.raw_rms_pp:.2f}', f'{r.centered_rms_pp:.2f}'] for r in distance_summary.itertuples()]

md = f'''# EXP-080：五种策略放在一起，IM有没有响应模式？

2026-10-21 · 完整2,016条件 · [主报告](REPORT.html) · 现有数据重分析

**结论：可以辨认局部的“策略×GU×预算”响应，但没有证据把IM称为跨数据集、跨预算稳定的策略族指纹。** IM最明显的局部现象是Cora/GNNDelete的小预算额外损伤，随后相对Random发生转向；CiteSeer上这一强度未重现，Degree也有类似转向。与此同时，GIF/IDEA和MEGU的效用平稳，以及分片方法的高预算损失，更多表现为方法与数据集共同决定的响应。

这里的IM专指本批`im_rr_greedy`：RR=65,536，传播概率0.1，三个选点seed=11/22/33。没有比较CELF、其他RR规模或传播概率，因此能讨论本配置的pattern，不能归纳整个IM算法族。GIF/IDEA是遗忘方法轴，不能与IM选点策略混为一谈。

## 1. 先分开三件事：绝对强度、Random增量、GU相对响应

- 绝对accuracy曲线回答“模型最终表现怎样”，见主报告。
- 定义 **H=accuracy(Random)−accuracy(selector)**，同训练seed、同GU、同预算配对；正值表示比Random多损失，单位pp。Random本身随预算变化，H的符号变化不等于策略自身准确率出现同幅度转变。
- 定义 **Q=H(GU)−H(Retrain)**，作为对照的交互差：正值表示选点相对Random带来的损失更集中在GU。Q和H都不能直接证明遗忘是否充分，也不能混用各方法不同的before。
- 另看 **D_extra=D(selector)−D(Random)**，比较GU与各自同请求Retrain的不一致率增量；不同策略的Retrain也不同，因此不是GU预测间的直接距离。

所有图表保留五种策略；profile计算将GIF/IDEA合并为一个坐标。IM三次抽样先在每个训练seed内平均，再计算三训练seed的均值和样本SD。所有比例上Random和Degree各只有一个节点集合跨训练seed重用，IM各有三个集合；这些不是独立数据划分或九个独立训练seed。

## 2. 五种策略的作用对象和预算响应不同

### 同一selector内，直接比较所有GU

下面每张折线图的**每行是一种selector，两列分别为Cora与CiteSeer；每个面板内的颜色表示不同GU方法或Retrain**。沿横轴看同一方法的预算响应，在同一面板内看哪些方法一起变化、哪些方法分离。GIF与IDEA在这些指标上完全重合，合并标为GIF/IDEA；六种GU均被覆盖，没有只画GNNDelete。

每行的两个数据集使用相同纵轴范围，便于跨数据集比较；不同行允许不同纵轴范围，以看清较弱的响应，**跨selector比较幅度必须读数值，不能比较线条的视觉陡峭程度**。阴影是三个训练seed的±1样本SD，不是置信区间。图表可点击放大。

**准确率图：** 看绝对效用。IM行中，GIF/IDEA与MEGU较平稳，GNNDelete和分片方法的预算响应不同；这比只展示GNNDelete更完整。Retrain黑线提供同请求重训练参照。

[![同selector跨GU：准确率预算曲线](selector_gu_accuracy.png)](selector_gu_accuracy.png)

**相对Random图：** 去掉同GU、同预算的Random参照后，看额外影响集中在哪里。正值为更多损失，负值为比Random表现更好。IM行的Cora/GNNDelete转向与分片方法损失出现在不同预算，不能用一条“IM强度”曲线概括。Random行所有方法定义上均为零。

[![同selector跨GU：相对Random额外损失](selector_gu_extra_loss.png)](selector_gu_extra_loss.png)

**预测不一致率图：** 看各GU是否随预算远离对应Retrain。准确率平稳的方法也可能出现上升的D。黑色点线是Retrain与自身比较的0%定义参照，不是两次独立Retrain实验；纵轴20表示20%的评估节点预测类别不同。

[![同selector跨GU：与Retrain预测不一致率](selector_gu_disagreement.png)](selector_gu_disagreement.png)

### 统一色标复核策略间的幅度

[![全策略全预算额外准确率损失](strategy_loss_atlas.png)](strategy_loss_atlas.png)

统一色标：红色为比Random更差，蓝色为更好，灰色为未运行的Cora50%分片端点。颜色是均值，不是显著性。先看同一列中不同策略，再看同一行跨GU的变化；不要仅按整图平均值给策略排名。

共同具备全部方法的33%端点，H均值（pp）：

{table(['数据集','策略','Retrain','GIF/IDEA','MEGU','GNNDelete','GraphEraser','GraphRevoker*'],mainrows)}

**Random：预算增加本身就会产生效用变化和预测偏离，必须保留为随预算变化的参照。** Cora/GNNDelete从15%到22%的accuracy由77.49%降至67.90%，约−9.59pp；IM同期76.51%降至75.38%，仅−1.13pp。IM在22%相对Random变好，主要体现两条曲线变化不同，不能讲成“提高预算后IM反而恢复了模型”。

**Degree：在CiteSeer上没有普遍强化损伤，在Cora低预算GNNDelete和高预算分片上却有明显作用。** CiteSeer50%时Retrain比Random高2.80pp；Cora5%的GNNDelete比Random低11.25pp，33%的GraphEraser/GraphRevoker分别低3.75/4.67pp。Degree并非一个始终弱于模型型策略的基线。

**r_point：高预算最明显地改变Retrain，并在CiteSeer连带造成GNNDelete和分片方法损失；GIF/MEGU仍保持较高accuracy。** 但Cora33%时GNNDelete平均比Random高4.18pp，而GraphEraser低6.64pp。即使同一强策略，也没有跨GU统一损伤排序。

**gt_full：更像局部GU响应，而不是一致削弱Retrain。** Cora50%时GNNDelete比Random低5.97pp，Retrain只低1.78pp，Q为+4.18pp；CiteSeer同条件GNNDelete反而比Random高0.35pp。Cora的作用对象不能直接迁移到CiteSeer。

**IM-RR：Cora小预算GNNDelete额外损伤明显，高预算分片有一定损失；CiteSeer总体更靠近Random，MEGU往往略优。** 因而不能说IM完全无效，也不能概括成持续增强的强攻击。它的局部作用见下一节。

## 3. IM有局部pattern，但三条证据限制了“稳定指纹”的说法

以下GNNDelete图只用于解释局部转向，所有GU的主比较已经在上一节展示。

[![局部案例：五策略GNNDelete绝对表现与Random增量](strategy_gnndelete.png)](strategy_gnndelete.png)

**第一，Cora/GNNDelete的小预算损伤在本次抽样网格上反复出现。** IM的H在5%、7.5%、10%分别为+10.21、+6.93、+4.94pp；每个比例的三个训练seed×三个IM抽样组合均比对应Random更差。22%时9个组合全部反向，IM更好；到50%时平均H又回到+1.95pp。33%只有1/9组合更差，但该组合的幅度较大，不能只看平均或方向计数。

{table(['数据集','预算','IM H均值(pp)','训练seed SD','H>0的组合数','九组合H范围(pp)'],imrows)}

这些9格共享三个训练seed和固定Random请求，比例间还是嵌套节点前缀，**不能当作9个独立样本，更不能把各比例加总成独立重复**。Cora/GNNDelete在固定训练seed内的IM三抽样accuracy极差最大达到15.13pp（33%、seed212），说明平均后的曲线会掩盖请求敏感性。

**第二，该强模式没有在CiteSeer重现。** CiteSeer/GNNDelete的IM H均值在所有比例仅约+0.05～+1.17pp，九组合中也有相反方向。GIF/IDEA在两数据集的IM相对Random效用差都很小（全部预算绝对均值差不超过0.24pp）；MEGU没有持续额外损伤。IM不是普遍降低所有GU准确率的策略。

**第三，这个局部形状不是IM独有。** Degree在Cora/GNNDelete上也表现为小预算比Random更差、22%和33%均值反向、50%再次更差。IM和Degree是否能够被稳定区分，需要在独立数据或请求上验证，当前不能由“曲线看起来相似/不同”直接宣布族指纹。

高预算另有较弱的候选现象：IM相对Random在Cora33%的GraphEraser/GraphRevoker上多损失2.15/3.26pp；CiteSeer33%为0.32/0.90pp，50%为−0.28/+1.50pp。因此GraphRevoker较高预算的损伤在两数据集均值上出现，但GraphEraser并不一致，Degree和gt_full也可能产生分片损失。不能据此建立IM专属的分片攻击机制。

## 4. 预测不一致率提供另一个观察轴，但仍不是IM专属

[![全策略全预算预测不一致率增量](strategy_disagreement_atlas.png)](strategy_disagreement_atlas.png)

IM在CiteSeer50%时，GIF与MEGU相对Random的D分别多2.07、2.65pp，但accuracy分别比Random高0.08、0.22pp；这是较小的“效用平稳、预测偏离增加”实例。Cora50%的MEGU也有D多2.05pp、accuracy高0.88pp。r_point的对应偏离大得多，而Degree、gt_full也能产生偏离；这支持额外观察预测对齐，不支持该现象是IM特有。

分片方法与共享单GCN Retrain存在模型家族差异；GraphRevoker*始终指原执行的GPA+optimal。高D、低accuracy和方法实现审计必须分别解释。

## 5. 用距离检查“形状”时，结果也依赖GU坐标

为避免仅凭肉眼判断，对5%～33%的共同范围，在每个训练seed/预算上计算IM与另一策略的GU向量RMS距离。原始距离保留整体强度，去均值距离先从各向量减去其GU均值，仅比较相对形状。单位pp。下面再对六个预算、三个训练seed取描述性平均，**这些相关条件不作为18个独立样本，不给p值或稳定性声明**。

{table(['数据集','GU集合','IM对照','原始RMS(pp)','去均值RMS(pp)'],distance_rows)}

five_GU包含GIF、MEGU、GNNDelete、GraphEraser、GraphRevoker，IDEA不重复计票；without_GNNDelete是删去该坐标的敏感性检查。不同GU集合的距离尺度和解释不同，只在同一集合内比较。距离小只表示这些已观察坐标接近，不能说明策略等价；是否能在未知数据上识别IM仍未验证。

五GU的去均值距离中，Cora的IM更接近Degree（1.52pp），而非Random（2.51pp）；CiteSeer则更接近Random（0.64pp），Degree与gt_full分别为0.77/0.73pp。删去GNNDelete后，Cora的IM–Random距离降至0.89pp，说明此前差异相当依赖该坐标；CiteSeer删去它后最近参照也从Random变为Degree，但两者距离仅0.49/0.47pp。**这是局部相似性的描述，不是可跨数据集识别的固定族结构。**

## 6. 现在可以写进结论的范围

> 五种删除策略没有统一的跨方法强弱排序。预算响应由选择策略、GU方法与数据集共同决定：r_point在高预算下明显改变重训练参照，gt_full与IM在部分Cora/GNNDelete条件下产生额外损伤，而Degree可以形成相近的局部响应。IM-RR在Cora小预算GNNDelete上的损伤具有本次抽样网格内的一致方向，但其Random相对效应随预算反转，且未以同等强度迁移到CiteSeer。因此当前证据支持条件性的响应结构，尚不足以支持IM策略族的稳定、独有指纹。

原始效用、相对Random增量、相对Retrain响应和预测对齐回答不同问题；不能选其中最有利的一条替代其他三条。固定split、三个训练seed、一种IM配置、有限请求重复和未校准的Retrain自然波动仍是边界。本次没有新增GPU作业或更改科学接受决定。

## 7. 数据和复现

- [全部逐seed对照与交互差](strategy_seed_contrasts.csv)、[均值和SD](strategy_summary.csv)。
- [同selector跨GU三组折线图的数值与SD](selector_gu_curve_values.csv)；每张图均可点击放大，并有同名PDF。
- [IM未平均的三抽样对照](im_draw_contrasts.csv)、[固定训练seed内抽样极差](im_draw_ranges.csv)。
- [各预算独立节点集合数](strategy_request_counts.csv)、[逐seed/预算的profile距离](im_profile_distances.csv)、[距离描述性汇总](im_profile_distance_summary.csv)。
- [输入核验](statistics_validation.json)、[原始回传核验](verification.json)、[增量与形状的独立复算](strategy_statistics_validation.json)、[生成脚本](strategy_patterns.py)。

本脚本以已经独立核验的cells.csv哈希为输入门槛，从原始行重新分层统计。图中灰格不补零，Retrain的D不造测量值；PDF与PNG均可导出。HTML由同一Markdown生成。
'''
(OUT / 'STRATEGY_REPORT.md').write_text(md, encoding='utf-8')
receipt = {'source_cells_sha256': proof['input_sha256'], 'training_seeds': 3,
           'IM_draws_per_training_seed': 3, 'distinct_random_sets_per_dataset_ratio': 1,
           'distinct_IM_sets_per_dataset_ratio': 3, 'deduplicated_GU_coordinates': methods,
           'profile_common_ratios': ratios[:-1], 'new_gpu_jobs': 0,
           'scope': 'Descriptive patterns only; no independent family validation or hypothesis tests.'}
(OUT / 'strategy_verification.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print('Five-selector report generated; raw, paired, draw-level and shape summaries saved.')
