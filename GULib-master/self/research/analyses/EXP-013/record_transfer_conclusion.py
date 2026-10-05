"""Record the agreed conditional-transfer interpretation from verified r1 data."""
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt
from scipy.stats import spearmanr

from analyze_surrogate import OUT, SHA, load, md_table


def rho(x, y):
    x, y = np.round(x, 10), np.round(y, 10)
    if np.ptp(x) < 1e-10 or np.ptp(y) < 1e-10:
        return np.nan
    return float(spearmanr(x, y).statistic)


def main():
    df, _ = load()
    gu = df[~df.method.isin(['IDEA', 'Retrain'])]
    # Random's three draws are replicates within each training seed, not extra seeds.
    random_rows = gu[gu.selector == 'random']
    assert random_rows.groupby(['dataset', 'method', 'seed']).size().eq(3).all()
    random_seed = random_rows.groupby(['dataset', 'method', 'seed']).U.mean()
    rows = []
    for (dataset, selector), direct in gu[gu.source == 'GCN'].groupby(['dataset', 'selector']):
        x = direct.groupby('method').U.mean()
        random = random_seed.loc[dataset].groupby('method').mean().reindex(x.index)
        degree = gu[(gu.dataset == dataset) & (gu.selector == 'degree')].groupby('method').U.mean().reindex(x.index)
        for source in ['SGC', 'GAT', 'GIN']:
            y = gu[(gu.dataset == dataset) & (gu.selector == selector) & (gu.source == source)].groupby('method').U.mean().reindex(x.index)
            assert len(x) == 5 and not y.isna().any()
            rows.append(dict(dataset=dataset, selector=selector, source=source, n_methods=5, n_seeds=3,
                             rho_direct_surrogate=rho(x, y), rho_direct_random=rho(x, random),
                             rho_direct_degree=rho(x, degree),
                             rho_random_adjusted=rho(x-random, y-random)))
    stats = pd.DataFrame(rows)
    stats.to_csv(OUT/'transfer_method_correlations.csv', index=False, encoding='utf-8')
    means = df[(df.dataset == 'Cora') & (df.method == 'GNNDelete')].groupby(['source', 'selector']).U.mean()
    example = pd.DataFrame([
        {'选点方式': name, 'F1下降_百分点': means.loc[key]}
        for name, key in [('GCN direct', ('GCN', 'gt_full')), ('GIN surrogate', ('GIN', 'gt_full')),
                          ('Random', ('baseline', 'random')), ('Degree', ('baseline', 'degree'))]])
    example.to_csv(OUT/'transfer_cora_example.csv', index=False, encoding='utf-8')
    cora = stats[(stats.dataset == 'Cora') & (stats.selector == 'gt_full') & (stats.source == 'GIN')].iloc[0]
    md = f'''# EXP-013 · 条件性迁移结论与多 seed 验证待办

记录日期：2026-10-05。当前证据支持**部分配置下的条件性跨架构迁移**，不支持普遍替代，也不把高相关单独当作代理选点有效的证明。

## 已明确的比较口径

- 选点层：比较相同候选集合上的选集重叠，并参照各模型自身跨 seed 的波动；节点分数若未回传，不声称已完成评分排序分析。
- 方法响应层：固定数据集、预算和选点算法，对每种遗忘方法先汇总多个训练 seed 的 F1 drop，再比较 GCN direct 与 surrogate 跨方法的响应规律。seed 是重复实验和不确定性来源，不是主比较轴。
- 某个固定 GU 内的攻击条件迁移，需不同预算或策略等条件；不能与跨 GU 的响应相关混称。
- F1 drop 定义为原模型 F1 减删除后 F1，单位百分点。效果排序、幅度接近和超过简单基线是不同判断。

## 为什么需要 Random / Degree 对照

Cora/gt_full 的 GIN 与 direct 跨方法排序相关为 {cora.rho_direct_surrogate:.3f}，但 Random 与 direct 也有 {cora.rho_direct_random:.3f}，Degree 同样为 {cora.rho_direct_degree:.3f}。相关可能反映不同 GU 的固有响应差异，不能全部归功于 surrogate 选点。两侧共同减去 Random 也会引入共享项，因此调整后的相关仅作诊断，不是因果识别。

下面的统计使用三个训练 seed 的均值。GIF/IDEA 在本轮 F1 输出相同，为避免同一响应重复加权，此表保留 GIF、去掉 IDEA，共五种 GU；原始六种方法的结果仍全部保留。保留并列排名，不做显著性或普遍替代声明。

{md_table(stats)}

## 可以支持的具体正例

Cora / GNNDelete / gt_full 的三个训练 seed 平均结果：

{md_table(example)}

GIN 保留了接近 direct 的损伤幅度，并超过 Random；Degree 本身也很强。这个例子支持条件性效果迁移，但不能据此强调相对 Degree 的稳健优势。它是探索结果，不是预先规定容许差距后的等效性检验。

## 论文中的表述与安排

可用表述：在所测试的数据集、删除预算与模型配置下，我们观察到条件性的跨架构迁移：部分代理选集在 GCN 目标模型上保留了接近直接选点的效用下降，并优于随机删除。迁移程度随代理架构、选点算法和遗忘方法变化。选点重叠及跨方法效果排序提供补充证据，但不足以证明代理模型具有普遍替代性。

正文首先展示 direct、surrogate、Random、Degree 的 F1 drop 与多 seed 波动；其次展示选点重叠及模型自身波动参照。相关性作为辅助分析并报告简单基线对应关系。原 post 报告中的按 seed 连线和混合两个算法的相关热图仅作为原始结果诊断，不作为论文的主要迁移证据。

## 多 seed Todo：EXP-079

[打开实验待办](../../experiments/EXP-079.html) · [实验状态源](../../experiments/EXP-079.json)

- 目标总数为10个训练 seed：保留 EXP-013 r1 的原3个，新增7个；新 seed 值在执行配置准备时一次性固定，不按结果挑选或提前停止。
- 原3个用于探索；新增7个先独立检查是否复现，再在代码、数据、划分、参数及指标语义一致后汇总10个。不同运行的执行 SHA 独立保留。
- 沿用 EXP-013 的对照范围，保留全部 surrogate、两个选点算法、三数据集、六 GU、Retrain、Random/Degree；不只验证当前看起来最好的组合。
- 主问题是关系稳定性和 surrogate 选择依据；不是仅凭重复次数证明模型重要性、凸性机制或普遍迁移。
- 新增矩阵按现有范围为1764个逻辑单元，正式数量由后续 YAML dry-run 确认。参数只由正式 YAML 拥有；本次不创建可执行配置、不提交 GPU 任务。
- 原先约12.2小时是含既有缓存命中的运行时长线性外推，不是 Cache 全未命中的正式预算。Todo 按原预运行组件估算作保守登记，实际批次与估时在准备时复核；每个作业仍按六小时上限规划，超时不代表完成。

## 证据与复现

- 原运行 r1，job `exp013-full-20260930-r1`，执行 SHA `{SHA}`。
- 原回传全部1513文件 SHA-256已重新检查；使用756个已完成单元，没有覆盖原始数据。
- [跨方法相关与基线对照](transfer_method_correlations.csv) · [具体效果案例](transfer_cora_example.csv) · [原逐格数据](cells.csv)。
- [原 post 诊断报告](post_REPORT.html) · [原幅度与基线报告](REPORT.html)。
- [本报告生成器](record_transfer_conclusion.py)：`python -B -X utf8 self/research/analyses/EXP-013/record_transfer_conclusion.py`。

本记录保存用户同意的结论口径和后续待办，不把分析完成或待办登记当作新实验已执行、统计等效或普遍迁移已成立。
'''
    (OUT/'transfer_conclusion_REPORT.md').write_text(md, encoding='utf-8')
    body = MarkdownIt('commonmark', {'html': False}).enable('table').render(md)
    style = 'body{max-width:1100px;margin:40px auto;padding:0 24px;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif;color:#243445}table{display:block;overflow:auto;border-collapse:collapse}td,th{padding:8px 12px;border:1px solid #ccd5df}th{background:#edf3f7}h2{margin-top:36px}a{color:#17649b}code{overflow-wrap:anywhere}'
    (OUT/'transfer_conclusion_REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EXP-013 条件性迁移结论</title><style>'+style+'</style><main>'+body+'</main></html>', encoding='utf-8')
    print('Recorded 18 across-method comparisons, baseline caveat, and EXP-079 linkage.')


if __name__ == '__main__':
    main()
