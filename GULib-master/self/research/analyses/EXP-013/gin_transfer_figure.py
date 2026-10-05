"""GIN-to-GCN response across GU methods; seeds are repeated observations."""
import base64
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from markdown_it import MarkdownIt

from analyze_surrogate import load, OUT, SHA, DATASETS, METHODS, SELECTORS, md_table

SERIES = ['GCN direct', 'GIN surrogate', 'Random', 'Degree']
COLORS = ['#356AA0', '#DB7444', '#98A1AD', '#639A81']
KEY = ['dataset', 'method', 'seed']


def aggregate(df):
    gu = df[df.method != 'Retrain']
    random = gu[gu.selector == 'random']
    assert random.groupby(KEY).size().eq(3).all()
    baseline = gu[gu.selector.isin(['random', 'degree'])].groupby(KEY+['selector'], as_index=False).U.mean()
    parts = []
    for selector in SELECTORS:
        direct = gu[(gu.selector == selector) & gu.source.isin(['GCN', 'GIN'])][KEY+['source', 'U']].copy()
        direct['series'] = direct.source.map({'GCN': SERIES[0], 'GIN': SERIES[1]})
        base = baseline.copy()
        base['series'] = base.selector.map({'random': SERIES[2], 'degree': SERIES[3]})
        current = pd.concat([direct[KEY+['series', 'U']], base[KEY+['series', 'U']]], ignore_index=True)
        current['selector'] = selector
        parts.append(current)
    values = pd.concat(parts, ignore_index=True)
    group = ['selector', 'dataset', 'method', 'series']
    assert not values.duplicated(group+['seed']).any()
    summary = values.groupby(group).U.agg(mean='mean', sd='std', n='size').reset_index()
    assert len(values) == 432 and len(summary) == 144 and summary.n.eq(3).all()
    wide = values.pivot(index=['selector']+KEY, columns='series', values='U')
    contrasts = []
    for (selector, dataset, method), part in wide.groupby(level=['selector', 'dataset', 'method']):
        for ref in ['GCN direct', 'Random', 'Degree']:
            delta = part['GIN surrogate']-part[ref]
            contrasts.append(dict(selector=selector, dataset=dataset, method=method, reference=ref,
                                  mean_difference_pp=delta.mean(), sd_difference_pp=delta.std(ddof=1),
                                  mean_absolute_difference_pp=delta.abs().mean(), n_seeds=len(delta)))
    contrasts = pd.DataFrame(contrasts)
    assert np.isfinite(summary[['mean', 'sd']]).all().all()
    values.to_csv(OUT/'gin_transfer_seed_values.csv', index=False, encoding='utf-8')
    summary.to_csv(OUT/'gin_transfer_summary.csv', index=False, encoding='utf-8')
    contrasts.to_csv(OUT/'gin_transfer_contrasts.csv', index=False, encoding='utf-8')
    return values, summary, contrasts


def figure(summary, selector):
    with plt.rc_context({'font.family': 'Microsoft YaHei', 'axes.unicode_minus': False,
                         'svg.hashsalt': 'exp013-gin-methods-v1', 'pdf.fonttype': 42}):
        fig, axes = plt.subplots(3, 1, figsize=(12.6, 10.8))
        x = np.arange(len(METHODS))
        width = .18
        for ax, dataset in zip(axes, DATASETS):
            subset = summary[(summary.selector == selector) & (summary.dataset == dataset)]
            for i, (series, color) in enumerate(zip(SERIES, COLORS)):
                part = subset[subset.series == series].set_index('method').reindex(METHODS)
                ax.bar(x+(i-1.5)*width, part['mean'], width=width, color=color,
                       edgecolor='white', linewidth=.5, yerr=part.sd,
                       error_kw={'ecolor': '#334155', 'elinewidth': .85, 'capsize': 2.5, 'capthick': .85})
            ax.axhline(0, color='#5C6672', lw=.8)
            ax.set_xticks(x, METHODS, fontsize=10)
            ax.set_xlim(-.6, len(METHODS)-.4)
            ax.set_title(dataset, loc='left', fontsize=15, fontweight='bold', pad=10)
            ax.set_ylabel('F1 下降（百分点）', fontsize=11)
            ax.grid(axis='y', alpha=.16)
            ax.set_axisbelow(True)
            ax.spines[['top', 'right']].set_visible(False)
            ax.margins(y=.15)
        fig.suptitle('GIN → GCN：跨遗忘方法的效果比较', fontsize=20, y=.983)
        fig.text(.5, .945, f'选点算法：{selector}  |  删除预算：10%  |  均值 ± 标准差，3 个训练 seed', ha='center', fontsize=12)
        handles = [Patch(facecolor=c, label=s) for s, c in zip(SERIES, COLORS)]
        fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(.5, .925), ncol=4, frameon=False, fontsize=12)
        fig.text(.5, .019, '高于零表示 F1 下降；低于零表示提升。三个面板纵轴刻度不同；误差线不是置信区间。', ha='center', fontsize=10, color='#475569')
        fig.text(.5, .002, 'Random 先在每个训练 seed 内平均 3 次抽样；GIF 与 IDEA 本轮 F1 相同，仍完整展示。', ha='center', fontsize=10, color='#475569')
        fig.subplots_adjust(left=.08, right=.985, top=.855, bottom=.073, hspace=.40)
        name = 'gin_to_gcn_methods_'+selector
        for extension in ['png', 'svg', 'pdf']:
            metadata = {'Date': None} if extension == 'svg' else ({'CreationDate': None, 'ModDate': None} if extension == 'pdf' else {})
            fig.savefig(OUT/(name+'.'+extension), dpi=180, bbox_inches='tight', facecolor='white', metadata=metadata)
        path = OUT/(name+'.svg')
        path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
        plt.close(fig)


def report(summary, contrasts):
    def value(dataset, method, series, selector='gt_full'):
        return summary[(summary.dataset == dataset) & (summary.method == method) &
                       (summary.series == series) & (summary.selector == selector)]['mean'].iloc[0]
    def v(dataset, method, series, selector='gt_full'):
        return f'{value(dataset, method, series, selector):.2f}'
    table = summary.copy()
    table['mean_sd'] = table.apply(lambda r: f'{r["mean"]:.2f} ± {r.sd:.2f}', axis=1)
    table = table.pivot(index=['selector','dataset','method'], columns='series', values='mean_sd').reindex(columns=SERIES).reset_index()
    cn = f'''在固定 GCN 目标架构、10% 节点删除预算下，我们比较 GIN 代理选点与 GCN 直接选点在六种图遗忘方法上的效用响应。图中每个柱值为三个训练 seed 的平均 F1 下降，误差线为样本标准差。gt_full 下，GIN 在 Cora/GNNDelete 上造成 {v('Cora','GNNDelete','GIN surrogate')} 个百分点的下降，接近直接选点的 {v('Cora','GNNDelete','GCN direct')}，并高于 Random 的 {v('Cora','GNNDelete','Random')}。这种接近并不限于单个 GU：在 MEGU 上，GCN 与 GIN 的平均下降分别为 Cora 的 {v('Cora','MEGU','GCN direct')} 与 {v('Cora','MEGU','GIN surrogate')}、CiteSeer 的 {v('CiteSeer','MEGU','GCN direct')} 与 {v('CiteSeer','MEGU','GIN surrogate')}、PubMed 的 {v('PubMed','MEGU','GCN direct')} 与 {v('PubMed','MEGU','GIN surrogate')} 个百分点。不过，这些 MEGU 结果的绝对变化较小，且 Cora、CiteSeer 的 seed 波动明显，因此它们体现的是平均效用响应相近，而不能单独作为强攻击或统计等效的证据。

迁移也表现出明确的条件依赖。Cora/GraphRevoker 的平均下降由 direct 的 {v('Cora','GraphRevoker','GCN direct')} 减为 GIN 的 {v('Cora','GraphRevoker','GIN surrogate')} 个百分点；在 PubMed，GIN 在 GIF、IDEA、GraphEraser 和 GraphRevoker 上的平均下降均小于 direct。与此同时，PubMed/GNNDelete 中 GIN 与 direct 分别为 {v('PubMed','GNNDelete','GIN surrogate')} 与 {v('PubMed','GNNDelete','GCN direct')} 个百分点，二者虽接近，却低于 Random 的 {v('PubMed','GNNDelete','Random')}。Cora/GNNDelete 的 Degree 也达到 {v('Cora','GNNDelete','Degree')} 个百分点。因此，效果接近 direct、攻击损伤较大、以及优于简单基线应分别判断。完整比较支持 GIN→GCN 在部分配置下的条件性效果迁移，不支持跨所有 GU 的普遍替代或一致的基线优势。r_point 的完整对照进一步显示这种关系依赖选点算法，例如 Cora/GNNDelete 的 GIN 平均下降为 {v('Cora','GNNDelete','GIN surrogate','r_point')}，低于 direct 的 {v('Cora','GNNDelete','GCN direct','r_point')} 和 Random 的 {v('Cora','GNNDelete','Random','r_point')} 个百分点。'''
    en = f'''We evaluate GIN-to-GCN transfer across six graph-unlearning methods at a fixed 10% node-deletion budget. Each bar reports the mean F1 drop over three training seeds, with error bars denoting sample standard deviations. Under gt_full, GIN-based selection retains the large loss observed for direct selection on Cora/GNNDelete ({v('Cora','GNNDelete','GIN surrogate')} versus {v('Cora','GNNDelete','GCN direct')} percentage points), exceeding the Random baseline ({v('Cora','GNNDelete','Random')}). Similar average responses also occur for MEGU across the three datasets: direct/GIN drops are {v('Cora','MEGU','GCN direct')}/{v('Cora','MEGU','GIN surrogate')} on Cora, {v('CiteSeer','MEGU','GCN direct')}/{v('CiteSeer','MEGU','GIN surrogate')} on CiteSeer, and {v('PubMed','MEGU','GCN direct')}/{v('PubMed','MEGU','GIN surrogate')} on PubMed. These MEGU effects are modest in absolute magnitude, and the variability on Cora and CiteSeer precludes interpreting proximity of the means as evidence of equivalence or strong attacks.

Transfer is nevertheless conditional on the unlearning method, dataset, and selection algorithm. On Cora/GraphRevoker, the mean drop decreases from {v('Cora','GraphRevoker','GCN direct')} with direct selection to {v('Cora','GraphRevoker','GIN surrogate')} with GIN selection. On PubMed, GIN yields smaller mean drops than direct selection for GIF, IDEA, GraphEraser, and GraphRevoker. Moreover, proximity to direct selection does not imply superiority to simple baselines: on PubMed/GNNDelete, the GIN and direct drops ({v('PubMed','GNNDelete','GIN surrogate')} and {v('PubMed','GNNDelete','GCN direct')}) are both below Random ({v('PubMed','GNNDelete','Random')}), while Degree already produces a large drop on Cora/GNNDelete ({v('Cora','GNNDelete','Degree')}). The r_point comparison also changes the picture: on Cora/GNNDelete, GIN yields {v('Cora','GNNDelete','GIN surrogate','r_point')} points versus {v('Cora','GNNDelete','GCN direct','r_point')} for direct selection and {v('Cora','GNNDelete','Random','r_point')} for Random. These results support conditional transfer of the utility response rather than universal replacement of direct selection or consistent superiority over simple baselines.'''
    md = f'''# GIN → GCN：多 GU 比较图与 Discussion 草稿

**当前结论：多个 GU 上出现平均响应接近，但强攻击保留、接近 direct、优于简单基线并不总是同时成立。** 正文围绕条件性迁移组织，保留完整三数据集×六方法结果。仅聚焦已讨论的 GIN；其他 surrogate 的证据仍在原报告中。

## 图 1：gt_full 的完整比较

![GIN跨GU迁移gt_full](gin_to_gcn_methods_gt_full.png)

[SVG](gin_to_gcn_methods_gt_full.svg) · [PDF](gin_to_gcn_methods_gt_full.pdf)

**读图：** 横轴为遗忘方法；蓝色是 GCN direct，橙色是 GIN surrogate，灰色是 Random，绿色是 Degree。比较同一方法内的柱高，不把 seed 作为横轴。纵轴为 F1_before − F1_after，单位百分点；正值为损伤、负值为提升。各数据集面板单独缩放，保留零点且没有截断柱形。

**图注草稿：** GIN→GCN 在固定 gt_full 选点算法和10%节点删除预算下的跨方法效用响应。所有柱值为三个训练 seed 的均值，误差线为样本标准差（ddof=1），不是置信区间。Random 在每个训练 seed 内先平均三次抽样，再跨训练 seed 计算均值与标准差；误差线仅表示该抽样均值的跨训练 seed 波动。GraphEraser/GraphRevoker 使用 GCN backbone 分片集成，图中 GCN direct 是 full-graph 选点参照，不声称它等于对整个集成的严格白盒选点。GIF/IDEA 的本轮 F1 相同，两列完整保留但不算两份独立证据。

## 证据与结论对照

| 问题 | 当前观察 | 支持范围 |
| --- | --- | --- |
| GIN 是否能保留较大损伤？ | Cora/GNNDelete/gt_full 中 GIN 接近 direct，并高于 Random | 具体配置正例；Degree 也强 |
| 是否仅一个 GU 有接近现象？ | MEGU 在三数据集上平均响应均接近 | 效应小且部分 seed 波动明显，不代表等效或强攻击 |
| 是否所有方法都能替代 direct？ | GraphRevoker/Cora 等条件有衰减；PubMed 的多方法下降较小 | 不支持普遍替代 |
| 接近 direct 是否一定优于基线？ | PubMed/GNNDelete 的 Random 高于 GIN 和 direct | 必须分别判断 |

## Discussion（中文草稿）

{cn}

## Discussion（英文草稿）

{en}

## 图 2：r_point 的同口径完整对照

![GIN跨GU迁移r_point](gin_to_gcn_methods_r_point.png)

[SVG](gin_to_gcn_methods_r_point.svg) · [PDF](gin_to_gcn_methods_r_point.pdf)

两图均使用全部方法与三个数据集，Random/Degree 为同一组对照。图 1 的正文示例选择属于探索阶段；新增 seed 前固定假设和统计口径，保留图 2 及不支持的结果。

## 适用边界与下一步

本节只讨论效用迁移，不据此推断遗忘正确性、隐私或机制。三 seed、单预算、固定数据划分支持描述性发现；误差线重叠与否不是显著性检验。均值接近可能包含配对差异抵消，因此另存逐 seed 差值、配对差的标准差和平均绝对差，未设事后等效阈值。选点重叠与跨方法排序相关保留在原分析中作为辅助，不单独作为有效性证明。

新增 seed 验证见 [EXP-079](../../experiments/EXP-079.html)，尚未运行。本图所用均为原 EXP-013 r1，不包含新 seed。当前为引文图数据，无视觉任务证据，本节不据此提出视觉应用上的泛化主张。

## 完整数值与复现

{md_table(table)}

- 原 job：`exp013-full-20260930-r1`；原执行 SHA：`{SHA}`；完整回传1513个文件重新核对哈希后生成图表。
- [均值与标准差](gin_transfer_summary.csv)：144行；[图中逐seed值](gin_transfer_seed_values.csv)：432行，基线为在两个算法面板中重复展示的相同对照，不是新增样本。
- [GIN与各对照的配对差](gin_transfer_contrasts.csv)：108行。三数据集×六GU×两算法×三参照；均值差、差值SD及配对MAE分开保存。
- [生成器](gin_transfer_figure.py)：`python -B -X utf8 self/research/analyses/EXP-013/gin_transfer_figure.py`。
- [整体条件性结论](transfer_conclusion_REPORT.html) · [原始全架构分析](REPORT.html)。
'''
    (OUT/'gin_transfer_discussion_REPORT.md').write_text(md, encoding='utf-8')
    body = MarkdownIt('commonmark', {'html': False}).enable('table').render(md)
    for selector in SELECTORS:
        name = 'gin_to_gcn_methods_'+selector+'.png'
        body = body.replace('src="'+name+'"', 'src="data:image/png;base64,'+base64.b64encode((OUT/name).read_bytes()).decode()+'"')
    css = 'body{margin:0;background:#f4f6f8;color:#243445;font:16px/1.85 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1250px;margin:auto;padding:32px}img{width:100%;background:white}h2{margin-top:38px;border-top:1px solid #ccd5df;padding-top:24px}table{display:block;overflow:auto;border-collapse:collapse;background:white;font-size:13px}td,th{padding:8px 12px;border:1px solid #ccd5df;white-space:nowrap}th{background:#e8eff5}a{color:#17649b}code{overflow-wrap:anywhere}'
    (OUT/'gin_transfer_discussion_REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GIN → GCN 多GU图与讨论</title><style>'+css+'</style><main>'+body+'</main></html>', encoding='utf-8')


def main():
    df, _ = load()
    values, summary, contrasts = aggregate(df)
    for selector in SELECTORS:
        figure(summary, selector)
    report(summary, contrasts)
    audit = dict(execution_sha=SHA, run_id='r1', verified_return_files=1513, training_seeds=[42,212,2024],
                 random_draws_per_training_seed=3, error_bars='sample standard deviation across training seeds, ddof=1',
                 plotted_seed_values=len(values), summary_rows=len(summary), contrast_rows=len(contrasts),
                 selectors=SELECTORS, datasets=DATASETS, methods=METHODS, new_runs_started=False)
    (OUT/'gin_transfer_figure_audit.json').write_text(json.dumps(audit, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(audit))


if __name__ == '__main__':
    main()
