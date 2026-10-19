"""Raw Q2 task metrics, with one Retrain reference and all e79r5 GCN requests."""
import base64
import json
import re

from build_report import OUT, DATASETS, REQUESTS, LABELS, COLORS, ci, read, sha, table
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt


def main():
    provenance = read(OUT / 'validation.json')
    assert sha(OUT / 'metrics_seed.csv') == provenance['output_csv_sha256']['metrics_seed.csv']
    source = pd.read_csv(OUT / 'metrics_seed.csv')
    gu = source[source.source.isin(['GCN', 'baseline'])].copy()
    keys = ['dataset', 'seed', 'selector']
    for metric in ['after', 'CE', 'AUC']:
        assert gu.groupby(keys)['retrain_' + metric].nunique().eq(1).all()
    retrain = gu.drop_duplicates(keys)[keys + ['retrain_after', 'retrain_CE', 'retrain_AUC']].rename(
        columns={'retrain_' + k: k for k in ['after', 'CE', 'AUC']})
    retrain['method'] = 'Retrain'
    retrain['before'] = np.nan  # No saved before value for this endpoint.
    values = pd.concat([gu[keys + ['method', 'after', 'before', 'CE', 'AUC']], retrain], ignore_index=True)
    assert values.groupby(['dataset', 'method', 'selector']).size().eq(10).all()
    assert not values.duplicated(keys + ['method']).any()
    # These two methods share task-metric coordinates to numerical precision.
    a = gu[gu.method.eq('GIF')].set_index(keys).sort_index()
    b = gu[gu.method.eq('IDEA')].set_index(keys).sort_index()
    tolerances = {'after': 0, 'CE': 1e-8, 'AUC': .001}
    max_diffs = {}
    for metric in ['after', 'CE', 'AUC']:
        max_diffs[metric] = float((a[metric] - b[metric]).abs().max())
        assert max_diffs[metric] <= tolerances[metric]
    values.to_csv(OUT / 'primary_seed.csv', index=False, encoding='utf-8')
    rows, contrasts = [], []
    for (ds, method, selector), group in values.groupby(['dataset', 'method', 'selector']):
        for metric in ['after', 'CE', 'AUC']:
            mean, lo, hi = ci(group[metric])
            rows.append(dict(dataset=ds, method=method, selector=selector, metric=metric,
                             mean=mean, lo=lo, hi=hi, seed_sd=group[metric].std(ddof=1), n=10))
            if selector != 'random':
                baseline = values[(values.dataset == ds) & (values.method == method) & values.selector.eq('random')].set_index('seed')
                delta = group.set_index('seed')[metric] - baseline[metric]
                dm, dl, dh = ci(delta)
                contrasts.append(dict(dataset=ds, method=method, selector=selector, metric=metric,
                                      selected_minus_random=dm, lo=dl, hi=dh, n=10))
    summary = pd.DataFrame(rows)
    effects = pd.DataFrame(contrasts)
    summary.to_csv(OUT / 'primary_summary.csv', index=False, encoding='utf-8')
    effects.to_csv(OUT / 'primary_paired_vs_random.csv', index=False, encoding='utf-8')
    indexed = summary.set_index(['dataset', 'method', 'selector', 'metric'])
    methods = ['Retrain', 'GNNDelete', 'GIF', 'MEGU', 'GraphEraser', 'GraphRevoker']
    titles = {'GIF': 'GIF / IDEA', 'GraphRevoker': 'GraphRevoker'}
    specs = {'after': ('Test accuracy (%)', 'higher is better', 'accuracy'),
             'CE': ('Test cross-entropy', 'lower is better', 'ce'),
             'AUC': ('Classification macro OvR AUC (%)', 'higher is better', 'auc')}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'text.color': '#253c49',
                         'axes.labelcolor': '#253c49', 'xtick.color': '#526773',
                         'ytick.color': '#526773', 'pdf.fonttype': 42})
    figures = []
    for ds in DATASETS:
        for metric, (ylabel, direction, suffix) in specs.items():
            fig, axes = plt.subplots(2, 3, figsize=(14, 8.7))
            # Share the raw scale across the five main panels; diagnostic implementation is separate.
            main = values[(values.dataset == ds) & ~values.method.isin(['GraphRevoker', 'IDEA'])]
            ss = summary[(summary.dataset == ds) & summary.metric.eq(metric) & ~summary.method.isin(['GraphRevoker', 'IDEA'])]
            lo, hi = min(main[metric].min(), ss.lo.min()), max(main[metric].max(), ss.hi.max())
            if metric == 'after':
                lo, hi = min(lo, main.before.min()), max(hi, main.before.max())
            pad = max((hi - lo) * .13, .002 if metric == 'CE' else .05)
            for ax, method in zip(axes.flat, methods):
                sub = values[(values.dataset == ds) & values.method.eq(method)]
                diagnostic = method == 'GraphRevoker'
                ax.set_title(titles.get(method, method), loc='left', fontweight='bold', fontsize=12)
                ax.spines[['top', 'right']].set_visible(False)
                ax.grid(axis='y', color='#e5edf0', lw=.7)
                ax.set_axisbelow(True)
                if not diagnostic:
                    ax.set_ylim(lo - pad, hi + pad)
                else:
                    ax.set_facecolor('#f5f5f5')
                    ax.margins(y=.22)
                for j, sel in enumerate(REQUESTS):
                    g = sub[sub.selector.eq(sel)].sort_values('seed')
                    x = j if method == 'Retrain' else j - .10
                    # Fixed jitter identifies the same seed position in every request.
                    ax.scatter(x + np.linspace(-.065, .065, 10), g[metric], s=13,
                               color=COLORS[sel], alpha=.32, edgecolors='none')
                    r = indexed.loc[(ds, method, sel, metric)]
                    ax.errorbar(x, r['mean'], yerr=[[r['mean'] - r.lo], [r.hi - r['mean']]],
                                fmt='D' if method == 'Retrain' else 'o', color=COLORS[sel],
                                mfc='white' if method == 'Retrain' else COLORS[sel], ms=7, capsize=3, lw=1.5, zorder=4)
                    if method != 'Retrain':
                        ref = indexed.loc[(ds, 'Retrain', sel, metric)]
                        ax.plot([x, j + .10], [r['mean'], ref['mean']], color=COLORS[sel], alpha=.5, lw=1, zorder=2)
                        ax.errorbar(j + .10, ref['mean'], yerr=[[ref['mean'] - ref.lo], [ref.hi - ref['mean']]],
                                    fmt='D', color=COLORS[sel], mfc='white', ms=6, capsize=3, lw=1.2, zorder=4)
                if metric == 'after' and method != 'Retrain':
                    bef = sub[sub.selector.eq('random')].before.mean()
                    ax.axhline(bef, color='#7a8790', ls='--', lw=1)
                    ax.text(.98, .97, f'Before mean: {bef:.2f}%', transform=ax.transAxes,
                            ha='right', va='top', fontsize=9, color='#66737a')
                elif metric == 'after':
                    ax.text(.98, .97, 'Before: not recorded', transform=ax.transAxes,
                            ha='right', va='top', fontsize=9, color='#66737a')
                ax.set_xticks(range(4), [LABELS[x] for x in REQUESTS])
                ax.set_xlim(-.45, 3.45)
                ax.set_ylabel(ylabel)
            fig.suptitle(f'{ds} | {ylabel} under four deletion requests', x=.065, ha='left',
                         fontsize=18, fontweight='bold')
            fig.text(.065, .925, f'Raw endpoints: {direction}. No subtraction of Random or Retrain.', fontsize=12)
            fig.legend(handles=[plt.Line2D([], [], marker='o', color='#526773', ls='', label='GU'),
                                plt.Line2D([], [], marker='D', color='#526773', mfc='white', ls='', label='Same-selector Retrain'),
                                plt.Line2D([], [], color='#7a8790', ls='--', label='GU Before mean (accuracy only)')],
                       loc='upper center', bbox_to_anchor=(.52, .905), ncol=3, frameon=False)
            fig.text(.065, .025, 'Faint dots: ten training seeds. Large dots: means; bars: pointwise 95% t intervals (not seed SD).\n'
                     'Same-selector Retrain is repeated for comparison, not independent evidence. Main five panels share a y scale.\n'
                     'Requests are separate conditions. GIF represents GIF/IDEA: identical accuracy; CE difference <1e-8; AUC difference <0.001 pp.', fontsize=9, color='#526773')
            fig.subplots_adjust(left=.065, right=.985, top=.82, bottom=.15, wspace=.29, hspace=.35)
            name = f'primary_{ds.lower()}_{suffix}'
            for ext in ['png', 'pdf']:
                fig.savefig(OUT / f'{name}.{ext}', dpi=170, facecolor='white')
            plt.close(fig)
            figures.append(name)
    pub = summary[summary.dataset.eq('PubMed') & summary.metric.eq('after')].pivot(
        index='method', columns='selector', values='mean').reindex(methods)[REQUESTS].round(2)
    pub = pub.rename(columns=LABELS).reset_index()
    paired = effects[effects.dataset.eq('PubMed') & effects.metric.eq('after') & effects.method.isin(['GIF','MEGU','GraphEraser','GNNDelete'])]
    paired = paired[paired.selector.isin(['r_point','gt_full'])].copy()
    paired['selected_minus_random [95% CI]'] = paired.apply(lambda r: f'{r.selected_minus_random:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}]', axis=1)
    paired = paired[['method','selector','selected_minus_random [95% CI]']]
    sections = []
    for ds in ['PubMed', 'Cora', 'CiteSeer']:
        sections.append(f'## {ds}：先看原值，再看配对变化\n')
        for metric, (_, _, suffix) in specs.items():
            label = {'after':'准确率：请求后模型实际有多好', 'CE':'交叉熵：正确标签的预测概率是否变差', 'AUC':'分类 AUC：类别分数的排序是否变化'}[metric]
            name = f'primary_{ds.lower()}_{suffix}'
            sections.append(f'### {label}\n\n![{ds} {label}]({name}.png)\n\n[矢量 PDF]({name}.pdf)。\n')
    md = '''# 问题 2：先比较各 selector 下的原始效用

2026-10-19 · EXP-079/e79r5 · 十训练 seed · GCN 选点 · 固定 split、10% 删除预算

**第一层先问：每种请求之后，模型本身的准确率、交叉熵和分类 AUC 是多少？第二层再问：相对 Random 改变多少，以及这种响应与 Retrain 有何不同。** 原值和参照差值都保留，但主图不要求读者先理解四项相减。

本页展示这批实验在 GCN 来源下的全部四类请求：Random、Degree、R-point、D-full。它不是所有选点算法的完整覆盖；EXP-011 的 IM、PageRank 等属于另一批实验，不能混成十 seed 的同一矩阵。

**IM 做过实验，只是没有纳入这批 EXP-079 十 seed 矩阵。** EXP-011 的 `exp011-t2/0925-v1` 包含 IM/RR-4096、RR-16384、RR-65536，覆盖三数据集、六 GU 和 Retrain；训练 seed 为 42、212、2024，每个训练 seed 内有三次 IM 选点重复。汇总表中 IM 的 n=9 是 3×3，不能读成九个训练 seed。Random 是三个训练 seed 各十次选点。见[EXP-011 原始汇总](../../../../self/research/analyses/EXP-011/table02-v2-summary.csv)及[原汇报第 3 节的完整策略比较](../REPORT.html)。这批原值图的缺席不代表 IM 无效或没跑过。

## 怎样读图

- 每个面板是一个系统，横轴是四种独立请求，纵轴是直接测得的任务指标；横轴顺序不是连续删除过程。
- Retrain 保留一个完整面板，且按 selector 叠加在各 GU 面板：实心圆是 GU，空心菱形是同 selector 的 Retrain。同色短线连接两个均值，只表示同请求的两个原值，不表示先后执行。重复的 Retrain 是同一份参照，不是新增重复实验。
- 浅色小点是十个训练 seed，大点为均值，误差线为均值的点态 95% t 区间。均值区间不是运行稳定性；逐 seed 标准差另存于 CSV。Random 先在每个训练 seed 内平均三次请求，其散布不等于单次随机请求的散布。
- 准确率图中的虚线是该 GU 自己的 Before 均值。Retrain 未保存对应 Before，CE/AUC 也没有保存 Before，不补造数值。
- 前五个面板共享纵轴，便于看效应的实际量级；Cora 的大幅下降会让其他方法的小变化显得紧凑，精确比较读原值表和配对区间。GraphRevoker 当前是 GPA + optimal 配置版，仅在灰色诊断面板保留，使用独立纵轴，不参与完整原方法的判断。
- GIF/IDEA 面板用 GIF 原值代表：两者准确率完全相同，逐 seed CE 差小于 1e-8，分类 AUC 最大相差约 0.00071 pp。CSV 保留两者，不能作为两份独立证据。准确率与当前 f1 字段数值相同，不作为两种独立指标。

## 当前原值已经能回答什么

PubMed 的平均准确率（%）：

''' + table(pub) + '''

**不能说其他 selector 在 GU 上都无效。** GIF/IDEA 和 GraphEraser 的定向请求仍有可见的准确率下降；MEGU 的变化更小；GNNDelete 的 R-point 则高于 Random。是否有额外损伤，需针对方法和 selector 分别说，而不是由“比 Retrain 的变化小”推成“无效”。以下是同 seed 的 Selected − Random，正值表示准确率提高，负值表示降低（注意它与旧图的损失方向相反）：

''' + table(paired) + '''

区间跨零表示当前数据没有给出明确方向，不能证明等效或无效。若要声称变化小到可忽略，需要预先定义有意义的效应阈值并做等效检验；本页没有补设事后阈值。上述点态区间未进行全矩阵多重检验校正。

**更小的 selector 响应不等于更稳定。** 前者是不同请求的均值变化，后者需看同条件跨 seed 或跨请求的变异。本页展示 seed 点并保存 SD，但没有完成方差差异推断，不能把更窄的均值误差线直接写成稳定性贡献。

**Selector 可以作为检查 GU 是否保留重训响应的探针。** 当同一批请求在 Retrain 上呈现的效用变化，在 GU 上被削弱或反转时，可以报告“相对于重训参照，效用响应不同”。仅凭这一点不能认定 GU 没有反映真实数据变化、遗忘失败或保留了应删除的信息；效用只是预测行为的一个摘要，而且当前 full-graph Retrain 与部分 GU 的模型结构并不相同。

## 不依赖 Retrain 的简单指标还能看什么

| 指标 | 回答的问题 | 当前可用性 |
|---|---|---|
| 删除后准确率 | 模型实际还能正确预测多少？ | 本页主图；与当前 f1 同值 |
| 删除前后准确率变化 Before − After | 相对该模型自身，删除后损伤多少？ | 已有 U；不依赖 Retrain；各 GU Before 不同 |
| 测试交叉熵 CE | 对真实标签的概率赋值是否变差？ | 本页画原值，越低越好；对自信错误敏感，不是校准误差 |
| 分类 macro OvR AUC | 类别分数排序是否改变？ | 本页画原值，越高越好；不是 membership/update-detection AUC |
| 同 seed 的 Selected − Random | 定向请求相对随机请求额外改变多少？ | 配对 CSV；仍是简单对照，未减 Retrain |
| 模型自身 Before/After 预测翻转、概率变化 | 准确率相近时，预测是否仍在变化？ | 当前指标表未直接记录，需要另核对保存预测、节点和评估图后补算 |

CE/AUC 的作用是检查准确率看不见的任务效用变化，不是再堆一组攻击指标。现有 update-detection AUC 可以作为另一个限定诊断，但它区分 selected 与测试节点，不能代替通用隐私或遗忘正确性结论。

**一个完全不需要 Retrain 的例子：PubMed / MEGU / R-point。** Random 与 R-point 的准确率分别为 87.052% 和 86.940%，CE 为 0.6135 和 0.5635，分类 AUC 为 96.367% 和 96.437%。准确率略降，但概率损失和类别排序改善；不能把三者压成“有效”或“无效”一个标签。Selected − Random 的配对变化分别为准确率 −0.112 pp [−0.223, −0.002]、CE −0.0500 [−0.0791, −0.0210]、分类 AUC +0.0696 pp [+0.0204, +0.1187]。准确率变化很小且区间接近零，仍需保留量级和探索性、多重比较限制，不称为重大退化。

作为不同方向的对照，同一 MEGU 的 Degree 准确率为 86.775%，CE 为 0.7285，分类 AUC 为 96.282%；相对 Random 三项均变差。因此不能泛称“MEGU 对不同 selector 没区别”，也不能泛称“准确率与 CE 必然反向”。

''' + '\n'.join(sections) + '''
## 与第二层图如何衔接

读完原值，再看 [跨 GU 的相对 Random 损失，以及效用与预测分歧](STORIES.html)。Random 差值把选择效应单独拎出；GU − Retrain 响应差和 GU–Retrain 预测分歧用于参照诊断。这些量帮助解释原值，不替代原值，也不把 Retrain 自动当作真实世界的因果真值。

## 证据与复现

- [逐 seed 原值](primary_seed.csv) · [均值、点态区间及 seed SD](primary_summary.csv) · [同 seed Selected − Random](primary_paired_vs_random.csv)。
- [生成器](build_primary.py) · [验证记录](primary_validation.json) · [方法实现审计](METHOD_AUDIT.html)。
- 输入为已核验的 metrics_seed.csv，本轮再次核对其 SHA256；同请求 Retrain 的准确率、CE、AUC 在六 GU 引用中一致后只取一份，未把六份引用当六次重复。
- 现有六 GU 加共享 Retrain、三数据集、四请求、十训练 seed，共 840 个汇总条件；Random 的每个条件已平均三请求。未新增模型执行，未改科学接受状态。
'''
    (OUT / 'PRIMARY.md').write_text(md, encoding='utf-8')
    body = MarkdownIt('commonmark', {'html': False}).enable('table').render(md)
    body = re.sub(r'src="([^"]+\.png)"', lambda m: 'src="data:image/png;base64,' + base64.b64encode((OUT/m[1]).read_bytes()).decode() + '"', body)
    style = 'body{margin:0;background:#edf2f4;color:#253c49;font:16px/1.8 "Microsoft YaHei",sans-serif}main{max-width:1280px;margin:auto;background:white;padding:36px}img{width:100%;height:auto}h2{margin-top:42px;border-top:1px solid #dbe5e9;padding-top:20px}table{border-collapse:collapse;font-size:14px;width:100%}th,td{padding:9px;border-bottom:1px solid #dbe5e9;text-align:left}th{background:#f0f5f6}a{color:#177e78}@media(max-width:700px){main{padding:16px}table{display:block;overflow:auto}}'
    (OUT / 'PRIMARY.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Q2 一级指标：所有请求的原始效用</title><style>' + style + '</style></head><body><main>' + body + '</main></body></html>', encoding='utf-8')
    validation = dict(execution_sha=provenance['execution_sha'], input_sha256=sha(OUT/'metrics_seed.csv'),
                      conditions=len(values), shared_retrain_verified=True, gif_idea_max_differences=max_diffs,
                      missing_before_preserved=True, figures=figures, new_gpu_runs=0,
                      scientific_acceptance='not_requested')
    validation['sha256'] = {n:sha(OUT/n) for n in ['PRIMARY.md','PRIMARY.html','primary_seed.csv','primary_summary.csv','primary_paired_vs_random.csv'] + [f'{f}.{ext}' for f in figures for ext in ['png','pdf']]}
    (OUT/'primary_validation.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', md):
        assert (OUT / target).exists(), target
    print(f'Validated {len(values)} conditions, {len(figures)} raw-metric figures, all report links.')


if __name__ == '__main__':
    main()
