"""Post-hoc transfer analysis: selection, effect correlation, and agreement.

Run from the repository root with Python, numpy, pandas, matplotlib, markdown-it.
All inference is descriptive; there are only three training seeds per stratum.
"""
import base64
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from markdown_it import MarkdownIt
from analyze_surrogate import load, OUT, SHA, DATASETS, METHODS, SOURCES, SELECTORS, save, md_table
from paired_reading import paired_figure, interactive_html

SEEDS = [42, 212, 2024]
PAIR_KEYS = ['dataset', 'method', 'selector', 'seed', 'split']


def corr(x, y, rank=False):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    assert np.isfinite(x).all() and np.isfinite(y).all()
    # A numerically constant effect has no defined correlation; never write zero.
    if np.ptp(x) < 1e-10 or np.ptp(y) < 1e-10:
        return np.nan
    if rank:
        # F1 counts generate exact ties; subtraction can introduce ~1e-14 pp noise.
        x, y = pd.Series(np.round(x,10)).rank(method='average'), pd.Series(np.round(y,10)).rank(method='average')
    return float(np.corrcoef(x, y)[0, 1])


def overlap_tables(df, selections):
    model = df[df.source.isin(SOURCES)]
    # Every GU/Retrain for a fixed request must consume the same selected set.
    for _, g in model.groupby(['dataset','source','selector','seed']):
        assert len(g) == 7
        assert len({selections[s] for s in g.selection_id}) == 1
    one = model.drop_duplicates(['dataset','source','selector','seed'])
    sets = {(r.dataset,r.source,r.selector,r.seed):selections[r.selection_id] for r in one.itertuples()}
    rows = []
    for d, alg in itertools.product(DATASETS, SELECTORS):
        for source in SOURCES:
            for a, b in itertools.combinations(SEEDS, 2):
                A, B = sets[d,source,alg,a], sets[d,source,alg,b]
                assert len(A) == len(B)
                rows.append(dict(dataset=d,selector=alg,source=source,comparison='within_model',
                                 seed_a=a,seed_b=b,jaccard=len(A&B)/len(A|B),overlap_fraction=len(A&B)/len(A)))
        for source in SOURCES[1:]:
            for a, b in itertools.product(SEEDS, SEEDS):
                A, B = sets[d,'GCN',alg,a], sets[d,source,alg,b]
                rows.append(dict(dataset=d,selector=alg,source=source,comparison='cross_model',
                                 seed_a=a,seed_b=b,jaccard=len(A&B)/len(A|B),overlap_fraction=len(A&B)/len(A)))
    pair = pd.DataFrame(rows)
    pair.to_csv(OUT/'post_selection_pairs.csv',index=False)
    stats=[]
    for (d,alg,source,comparison),g in pair.groupby(['dataset','selector','source','comparison']):
        diagonal=g[g.seed_a==g.seed_b]
        stats.append(dict(dataset=d,selector=alg,source=source,comparison=comparison,n_pairs=len(g),
            jaccard_mean=g.jaccard.mean(),jaccard_min=g.jaccard.min(),jaccard_max=g.jaccard.max(),
            overlap_fraction_mean=g.overlap_fraction.mean(),same_seed_jaccard=diagonal.jaccard.mean()))
    summary=pd.DataFrame(stats);summary.to_csv(OUT/'post_selection_summary.csv',index=False)
    return pair,summary


def effect_tables(df):
    gu=df[df.method!='Retrain']
    direct=gu[gu.source=='GCN'][PAIR_KEYS+['U','after','before','selection_id']]
    paired=gu[gu.source.isin(SOURCES[1:])].merge(direct,on=PAIR_KEYS,validate='many_to_one',suffixes=('','_direct'))
    assert len(paired)==324
    assert np.allclose(paired.before,paired.before_direct)
    rand=gu[gu.selector=='random'].groupby(['dataset','method','seed'],as_index=False).U.mean().rename(columns={'U':'U_random'})
    paired=paired.merge(rand,on=['dataset','method','seed'],validate='many_to_one')
    paired['drop_difference']=paired.U-paired.U_direct
    paired['absolute_drop_difference']=paired.drop_difference.abs()
    paired['excess_random']=paired.U-paired.U_random
    paired['direct_excess_random']=paired.U_direct-paired.U_random
    paired.to_csv(OUT/'post_effect_pairs.csv',index=False)
    records=[]
    for (d,m,src),g in paired.groupby(['dataset','method','source']):
        assert len(g)==6 and g.seed.nunique()==3 and g.selector.nunique()==2
        for selector in ['both']+SELECTORS:
            t=g if selector=='both' else g[g.selector==selector]
            row=dict(dataset=d,method=m,source=src,selector=selector,n=len(t),n_seeds=t.seed.nunique(),
                pearson_drop=corr(t.U_direct,t.U),spearman_drop=corr(t.U_direct,t.U,True),
                pearson_f1=corr(t.after_direct,t.after),spearman_f1=corr(t.after_direct,t.after,True),
                bias_pp=t.drop_difference.mean(),mae_pp=t.absolute_drop_difference.mean(),
                rmse_pp=np.sqrt(np.mean(t.drop_difference**2)),direct_drop_range_pp=np.ptp(t.U_direct),
                surrogate_drop_range_pp=np.ptp(t.U),
                spearman_excess_random=corr(t.direct_excess_random,t.excess_random,True))
            if selector=='both':
                # Center each selector separately: remove its between-selector mean contrast.
                x=t.U_direct-t.groupby('selector').U_direct.transform('mean')
                y=t.U-t.groupby('selector').U.transform('mean')
                row['pearson_within_selector']=corr(x,y)
                loo=[corr(t[t.seed!=seed].U_direct,t[t.seed!=seed].U,True) for seed in SEEDS]
                finite=[x for x in loo if np.isfinite(x)]
                row.update(leave_one_seed_out_rho_min=min(finite) if finite else np.nan,
                           leave_one_seed_out_rho_max=max(finite) if finite else np.nan,
                           leave_one_seed_out_defined=len(finite))
            records.append(row)
    stats=pd.DataFrame(records);stats.to_csv(OUT/'post_correlations.csv',index=False)
    return paired,stats


def relationship_table(paired,selpairs):
    cross=selpairs[(selpairs.comparison=='cross_model')&(selpairs.seed_a==selpairs.seed_b)]
    joined=paired.merge(cross[['dataset','selector','source','seed_a','jaccard']].rename(columns={'seed_a':'seed'}),
                        on=['dataset','selector','source','seed'],validate='many_to_one')
    rows=[]
    for (d,m),g in joined.groupby(['dataset','method']):
        for alg in ['both']+SELECTORS:
            t=g if alg=='both' else g[g.selector==alg]
            rows.append(dict(dataset=d,method=m,selector=alg,n=len(t),n_seeds=t.seed.nunique(),
                rho_jaccard_vs_absolute_drop_difference=corr(t.jaccard,t.absolute_drop_difference,True)))
    out=pd.DataFrame(rows);out.to_csv(OUT/'post_overlap_effect.csv',index=False)
    return out


def matrix_figure(stats,metric,name,title,cmap='RdBu_r',limits=(-1,1)):
    fig,axes=plt.subplots(3,1,figsize=(11.5,7.4),layout='constrained')
    for ax,d in zip(axes,DATASETS):
        data=stats[(stats.dataset==d)&(stats.selector=='both')].pivot(index='source',columns='method',values=metric).reindex(index=SOURCES[1:],columns=METHODS).to_numpy()
        im=ax.imshow(data,aspect='auto',cmap=cmap,vmin=limits[0],vmax=limits[1])
        for i,j in itertools.product(range(3),range(6)):
            value=data[i,j]
            color='white' if (abs(value)>.65 if limits==(-1,1) else value>limits[1]*.60) else '#162533'
            ax.text(j,i,'NA' if not np.isfinite(value) else f'{value:.2f}',ha='center',va='center',color=color,fontsize=12)
        ax.set_xticks(range(6),METHODS);ax.set_yticks(range(3),SOURCES[1:]);ax.set_title(d,loc='left',fontweight='bold')
    fig.colorbar(im,ax=axes,shrink=.8,label='Spearman rho' if 'spearman' in metric else 'percentage points')
    fig.suptitle(title+'\nEach cell: 2 selectors x 3 matched training seeds (n=6). Descriptive, not a significance test.',fontsize=13)
    save(fig,name)


def selection_figure(summary):
    fig,axes=plt.subplots(2,3,figsize=(13.5,7),layout='constrained')
    for i,alg in enumerate(SELECTORS):
        for j,d in enumerate(DATASETS):
            ax=axes[i,j]
            s=summary[(summary.dataset==d)&(summary.selector==alg)]
            gcn=s[(s.source=='GCN')&(s.comparison=='within_model')].jaccard_mean.iloc[0]
            ax.axhline(gcn,c='#303840',ls='--',label='GCN across seeds')
            for k,src in enumerate(SOURCES[1:]):
                for cmp,offset,color in [('cross_model',-.13,'#2875a4'),('within_model',.13,'#d36d37')]:
                    r=s[(s.source==src)&(s.comparison==cmp)].iloc[0]
                    ax.scatter(k+offset,r.jaccard_mean,c=color,s=44)
                    ax.vlines(k+offset,r.jaccard_min,r.jaccard_max,color=color,alpha=.65,lw=2)
            ax.set_xticks(range(3),SOURCES[1:]);ax.set_ylim(0,1.05);ax.set_title(d+' / '+alg)
            if j==0:ax.set_ylabel('Jaccard')
            ax.grid(axis='y',alpha=.12)
    fig.suptitle('Selection agreement needs a within-model reference\nBlue: GCN vs surrogate, all 9 seed pairs | Orange: surrogate across seeds, 3 pairs\nDashed: GCN across seeds; dots: means; bars: observed ranges (not confidence intervals)',fontsize=12)
    save(fig,'post_selection_reference')


def scatter_figures(paired,stats):
    for method in METHODS:
        fig,axes=plt.subplots(3,3,figsize=(11,10.4),layout='constrained')
        for i,d in enumerate(DATASETS):
            g=paired[(paired.dataset==d)&(paired.method==method)]
            low=min(g.U.min(),g.U_direct.min());high=max(g.U.max(),g.U_direct.max());margin=max((high-low)*.12,.15)
            for j,src in enumerate(SOURCES[1:]):
                ax=axes[i,j];t=g[g.source==src]
                for alg,color in [('r_point','#2875a4'),('gt_full','#d36d37')]:
                    for seed,marker in zip(SEEDS,['o','s','^']):
                        a=t[(t.selector==alg)&(t.seed==seed)]
                        ax.scatter(a.U_direct,a.U,c=color,marker=marker,s=45,label=alg if seed==42 else None)
                ax.plot([low-margin,high+margin],[low-margin,high+margin],ls='--',c='#707c85',lw=1)
                ax.set(xlim=(low-margin,high+margin),ylim=(low-margin,high+margin));ax.set_aspect('equal');ax.grid(alpha=.15)
                st=stats[(stats.dataset==d)&(stats.method==method)&(stats.source==src)&(stats.selector=='both')].iloc[0]
                ax.set_title(f'{d} / {src}\nrho={st.spearman_drop:.2f}; MAE={st.mae_pp:.2f} pp',fontsize=10)
                if i==2:ax.set_xlabel('GCN direct F1 drop (pp)')
                if j==0:ax.set_ylabel('Surrogate F1 drop (pp)')
                if i==0 and j==2:ax.legend(fontsize=8)
        fig.suptitle(method+': effect correspondence on the same GCN victim\nBlue: r_point; orange: gt_full. Circle: seed42; square: seed212; triangle: seed2024\nSame dataset, selector, seed and budget; dashed line y=x. No pooled fit.',fontsize=12)
        save(fig,'post_scatter_'+method)


def validate_statistics(paired,stats):
    from scipy.stats import spearmanr, pearsonr
    checked=0
    for row in stats.itertuples():
        t=paired[(paired.dataset==row.dataset)&(paired.method==row.method)&(paired.source==row.source)]
        if row.selector!='both':t=t[t.selector==row.selector]
        x,y=t.U_direct.to_numpy(),t.U.to_numpy()
        if np.ptp(x)<1e-10 or np.ptp(y)<1e-10:
            assert np.isnan(row.spearman_drop) and np.isnan(row.pearson_drop)
        else:
            assert np.isclose(row.spearman_drop,spearmanr(np.round(x,10),np.round(y,10)).statistic)
            assert np.isclose(row.pearson_drop,pearsonr(x,y).statistic)
        assert np.isclose(row.mae_pp,np.abs(t.after-t.after_direct).mean())
        assert row.mae_pp+1e-10>=abs(row.bias_pp)
        checked+=1
    return checked


def make_report(stats,selsummary,relationship,checked,paired):
    both=stats[stats.selector=='both']
    def row(d,m,s):return both[(both.dataset==d)&(both.method==m)&(both.source==s)].iloc[0]
    examples=pd.DataFrame([row('CiteSeer','MEGU','GIN'),row('PubMed','MEGU','GIN'),
        row('Cora','GNNDelete','GAT'),row('Cora','GNNDelete','GIN'),
        row('PubMed','GNNDelete','SGC'),row('CiteSeer','GraphEraser','GAT'),row('Cora','GraphRevoker','GIN')])
    columns=['dataset','method','source','spearman_drop','pearson_drop','spearman_f1','mae_pp','bias_pp']
    example_table=md_table(examples[columns])
    cgn=row('Cora','GNNDelete','GIN');pgs=row('PubMed','GNNDelete','SGC')
    mgc=row('CiteSeer','MEGU','GIN');mgp=row('PubMed','MEGU','GIN')
    selection_table=md_table(selsummary[['dataset','selector','source','comparison','n_pairs','jaccard_mean','overlap_fraction_mean','same_seed_jaccard']])
    section=[]
    for method in METHODS:
        section.append('### '+method+'\n\n![F1 drop配对散点：'+method+'](post_scatter_'+method+'.png)\n\n[矢量 SVG](post_scatter_'+method+'.svg)\n')
    md=f'''# EXP-013 Post 分析 · 选点、效果排序与效果接近程度

当前采用的结论与比较口径见[条件性迁移结论与多 seed 待办](transfer_conclusion_REPORT.html)：seed 用于重复与波动估计，跨 GU 响应需与 Random/Degree 对照。本页保留原始配对及混合条件统计作为诊断，不作为论文主迁移证据。

**本轮发现：选点一致性、效果相关性与效果幅度是不同层次。** GAT/GIN 存在共同选点倾向；一些先前被“攻击弱”掩盖的组合（如 MEGU）呈现很高的效果排序相关。另一些组合则“排序一致但幅度不同”，或“代理攻击更强但排序不一致”。不能据此宣称某个 surrogate 可在所有 GU 上替代 GCN direct。

本报告是用户提出新分析视角后的探索性 post 分析，基于既有、可信回传的 r1。没有新运行、参数调整或结果筛除；原幅度报告保留为[补充分析](REPORT.html)。主要指标是 F1 drop 和删除后 F1，retrain-gap 不参与本报告主结论。

## 先看一张：同一个 seed，换模型选点后 F1 下降改变多少？

![同seed真实F1下降配对](post_paired_reading.png)

先固定 **GNNDelete × gt_full × GIN**，只读三条实际配对线。左端是 GCN 选点，右端是 GIN 选点；同色连接同一个 seed，纵轴是 F1 下降百分点。线水平表示下降相同，向上表示换成 GIN 后下降更多。各数据集单独缩放纵轴，只在面板内部比较斜率；负值代表 F1 提升。两端最终都评估 GCN victim。

这是延续讨论的一个阅读示例，不代表 GIN 是所有条件下最优。HTML 可切换全部六种遗忘方法、两个选点算法和三种 surrogate，并显示九对原始数值；一次只看一个组合。JavaScript 不可用时保留默认静态图。

在这个示例中，Cora 的三次均值从 20.48 到 20.23 pp，三对绝对差均约 0.74 pp；PubMed 从 1.41 到 1.43 pp，三对绝对差约 0.05～0.51 pp。**在这些具体配对上下降幅度相近**，但不等于通过统计等效检验。CiteSeer 两边的变化都在 1 pp 内，并未显示明显 F1 损伤。判断攻击是否优于 Random 仍需基线。

这个图让幅度、方向和 seed 差异可直接检查，不能取代相关性问题。后者仍保留在下方作为补充。旧主图把两个算法合并，PubMed/GNNDelete/GIN 的 0.03 不能概括当前 gt_full 子集的幅度差，更不能直接判断其攻击效果很差。

## 补充：六个混合条件的排序相关

![分层 F1 drop Spearman 相关](post_drop_correlation.png)

每格固定一个 dataset × GU × surrogate。横纵比较的是：GCN direct 选集 vs surrogate 选集，**都在同一个 GCN victim 上评估**。每格仅有 r_point/gt_full × 三个训练 seed，共六个配对观测；三个 seed 是重复来源，不是六次独立训练。

红色趋近 +1：direct 下降较大的条件，surrogate 也倾向下降较大；接近 0：未观察到清晰单调关系；负值：顺序有反转。它不是成功率，也不是显著性结果。GIF/IDEA 本轮的 F1 相同，两个列不算两份独立证据。

## 关键证据与解读

{example_table}

- **高相关、也接近：MEGU / GIN。** CiteSeer 的 Spearman 为 {mgc.spearman_drop:.3f}，平均绝对差仅 {mgc.mae_pp:.3f} pp；PubMed 为 {mgp.spearman_drop:.3f}，平均绝对差 {mgp.mae_pp:.3f} pp。两数据集分别去掉任意一个 seed 后，Spearman 范围为 {mgc.leave_one_seed_out_rho_min:.3f}～{mgc.leave_one_seed_out_rho_max:.3f}、{mgp.leave_one_seed_out_rho_min:.3f}～{mgp.leave_one_seed_out_rho_max:.3f}。但 PubMed direct 的六点 drop 范围只有 {mgp.direct_drop_range_pp:.3f} pp，不能把微小变化的排序一致称为强攻击。
- **高相关、幅度仍不同：Cora / GNNDelete / GAT。** Spearman {row('Cora','GNNDelete','GAT').spearman_drop:.3f}，平均有符号差 {row('Cora','GNNDelete','GAT').bias_pp:.3f} pp（surrogate − direct）。代理保留了总体强弱趋势，却系统地造成较小下降。相关性与攻击大小给出互补信息。
- **攻击更强、但排序不保留：PubMed / GNNDelete / SGC。** 平均有符号差 {pgs.bias_pp:+.3f} pp，但 Spearman 仅 {pgs.spearman_drop:.3f}。之前的强攻击正例，不能直接当作“复现 direct 效果规律”的正例。
- **另一个较一致的条件：CiteSeer / GraphEraser / GAT。** Spearman {row('CiteSeer','GraphEraser','GAT').spearman_drop:.3f}、MAE {row('CiteSeer','GraphEraser','GAT').mae_pp:.3f} pp；去掉算法间均值差后的 Pearson 仍为 {row('CiteSeer','GraphEraser','GAT').pearson_within_selector:.3f}。这表明本轮观察不限于 GNNDelete。
- **反例仍然存在：Cora / GraphRevoker。** 三种代理的 Spearman 都为负，不能把 GAT/GIN 的选点重叠外推成所有方法的效果可替代。

## 相关不等于接近

![F1 drop平均绝对配对差](post_drop_agreement.png)

MAE = mean(|drop_surrogate − drop_direct|)，单位 pp，越小越接近；bias 为有符号均差；RMSE 同时保存在 CSV。双方用同一个 before F1，因此 **drop 的绝对配对差等于删除后 F1 的绝对配对差**，已经逐组数值核对。但跨 seed 的 before F1 可以不同，故 drop 的相关系数不等于 after F1 的相关系数。

没有预先指定可接受差距，报告不以事后阈值划分“等效”“成功”。例如高相关、MAE 小可能表示弱效应共同变化，并不证明攻击实用性；幅度是否超过 Random/Degree 应回看原始效果报告。

## 删除后 F1 本身

![删除后F1 Spearman相关](post_f1_correlation.png)

CSV 同时给出 Pearson/Spearman after F1。两种指标回答不同问题：after F1 对应最终任务性能；drop 对应从原模型性能下降多少。以 CiteSeer / GraphEraser / GAT 为例，drop Spearman 为 {row('CiteSeer','GraphEraser','GAT').spearman_drop:.3f}，after F1 Spearman 为 {row('CiteSeer','GraphEraser','GAT').spearman_f1:.3f}，因此报告不能混用二者。

## 选点一致性：加入模型自身波动参照

![选点跨模型与模型内参照](post_selection_reference.png)

蓝色使用每个 surrogate 三个 seed 与 GCN 三个 seed 的 **全部九种配对**；橙色是 surrogate 自身三种跨 seed 配对；虚线是 GCN 自身跨 seed 均值。误差线只是观察范围，不是置信区间。这些配对共享选集，不能视为九次或三次独立重复。

- SGC 模型内 Jaccard 为 0.994～1.000，和 GCN 之间却只有约 0.027～0.082。支持“稳定但不同的选点”，不支持直接把差异归因于凸性。
- GCN 模型内均值约 0.358～0.503，是自然波动参照，**不是上限**。GAT/GIN 的若干跨模型值与这一量级接近，支持共同选点倾向；Cora/gt_full 等条件仍明显低于 GCN 模型内均值。
- 同数字 seed 在不同架构上并无相同权重或同一随机轨迹的含义。旧图用同 seed 配对，可能受对齐方式影响；本图补全交叉配对。PubMed/r_point/GAT 从同 seed 0.436 变为全部配对 0.329，gt_full 从 0.396 变为 0.291，说明不能只凭那三个对角配对宣称跨 seed 普遍一致。
- `overlap_fraction_mean` 按每个配对的交集/选集大小计算后平均，没有把均值 Jaccard 非线性换算成平均重合比例。10%预算下独立均匀随机选集的预期重合比例约10%，只是简单参照；图结构、标签和选择偏好并非均匀随机。

{selection_table}

## 敏感性检查：高相关来自哪里？

1. **算法分层。** 主图每格六点，可能主要反映两个算法的均值差。另算各 selector 内三点的相关，以及去掉各 selector 均值后的 Pearson。Cora/GNNDelete/GIN 总体 Spearman 为 {cgn.spearman_drop:.3f}，但去掉算法均值差后的 Pearson 为 {cgn.pearson_within_selector:.3f}。所以应说“混合两个算法的总体排序对应”，不能说同一算法内部稳定对应。
2. **逐 seed 留出。** 每次移除一个 seed 的两个点，再计算四点 Spearman；范围保存在 CSV。只有三个 seed，这仅展示敏感性，不是泛化验证或置信区间。报告保留所有正、负和未定义结果。
3. **相对 Random 的效果。** 按同一 dataset/GU/seed，减去三个 Random 抽样的平均 drop，再比较两侧 excess 的 Spearman。PubMed/MEGU/GIN 的原始 drop 相关为 {mgp.spearman_drop:.3f}，excess 相关降至 {mgp.spearman_excess_random:.3f}；CiteSeer 对应为 {mgc.spearman_drop:.3f}→{mgc.spearman_excess_random:.3f}。提示某些原始高相关可能包含共享的 victim/seed 响应。共同减去 Random 并不消除所有依赖，也不是因果调整。
4. **数值并列。** F1 来源于有限测试节点，存在真正的并列。Spearman 在 pp 单位保留10位小数后以平均秩处理并列，避免浮点减法约1e-14的差别制造虚假排序。Pearson 保留原数值。任一向量近常数时相关记 NA，不以0代替。
5. **原始动态范围。** 保存每格 direct/surrogate 的最大最小差；范围很小的高相关不能与几十 pp 变化的相关性等量齐观。没有 pooled correlation、p值、显著性星号或从多重探索中筛选出的“成功率”。

## 选集更像，效果就更接近吗？

按 dataset × GU，将同 seed 的 Jaccard 与 |drop_surrogate − drop_direct| 做 Spearman：负值表示重叠更高时差距更小。每层18个点来自三个 surrogate × 两个算法 × 三个 seed，共享 direct 和 seed，不是18次独立重复。另保存每个 selector 内的九点描述统计。

{md_table(relationship[relationship.selector=='both'])}

这些关系并非一致：例如 PubMed/GNNDelete 呈负相关，而 Cora、CiteSeer/GNNDelete 并非如此。跨 source/selector 的结构差异也可能驱动关系，不能作因果解释。SGC 的低重叠与 MEGU 的高效果相关并存，说明选点重叠不能独自代替效果分析。

## 逐方法配对散点

每张图固定 GU，行是 dataset，列是 surrogate；横轴 direct drop，纵轴 surrogate drop，蓝色 r_point、橙色 gt_full；圆形 seed42、方形 seed212、三角形 seed2024。完全重合的点不人为抖动，精确坐标见配对CSV。虚线 y=x，用来同时判断趋势和幅度。每个 dataset 行共享坐标范围，不画跨数据集拟合线。

{''.join(section)}

## 当前可以写成什么发现？

建议的证据表述：**在本轮固定 GCN victim、10%节点删除及共享数据条件下，跨架构选点重叠、F1效果排序相关和幅度接近程度表现为可区分的现象。部分 surrogate/GU 条件保留强弱排序，即使选集不同或攻击幅度有系统差异；也存在更强攻击但低排序相关的条件。**

这比只比较攻击大小提供了更多信息，但不支持“GAT/GIN在所有方法上可替代GCN”，也不证明相关来自 surrogate 本身：两侧共享 victim、训练 seed、数据划分，且本轮 selector seed 与 victim seed 同轴。模型内随机性、算法均值差与模型特异选点贡献尚未被独立操控。SGC 的凸性/表示差异仍是机制假设。

三个 seed、单预算、固定划分使当前结论属于描述性 post 分析；没有预注册假设或等效阈值。若后续需要确认性结果，再单独决定扩展 seed、预算或解耦 selector/victim seed；本次不启动新实验。文献新颖性不由本报告认定，科学接受待用户审阅。

## 复现与数据

- 原 job：`exp013-full-20260930-r1`；run：`r1`；原执行 SHA：`{SHA}`。
- 原 run.json 哈希：`70588d5793760e44ae268dfe55b3648e0638b71fde3a4db0eee998dc51760a49`。
- 再次检查1513个回传文件哈希，读取全部756单元，核对648个GU与同请求Retrain的身份；post主分析使用324个 surrogate-GU 单元与108个 direct-GU 单元配对。
- [全部相关性与敏感性统计](post_correlations.csv)：54个六点分组 + 108个三点分组；含 drop/F1 Pearson与Spearman、MAE、RMSE、bias和动态范围。
- [逐效果配对](post_effect_pairs.csv)、[逐选集配对](post_selection_pairs.csv)、[选集统计](post_selection_summary.csv)、[重叠与效果关系](post_overlap_effect.csv)。
- [核验记录](post_audit.json)：{checked}组相关统计与 scipy 独立实现对照；配对drop和after F1的绝对差一致。
- [生成器](post_analysis.py)：仓库根运行 `python -X utf8 self/research/analyses/EXP-013/post_analysis.py`。本地依赖 numpy/pandas/matplotlib/markdown-it-py/scipy，无GPU或远端模型输入。
- [配对主图SVG](post_paired_reading.svg) · [相关性补充SVG](post_drop_correlation.svg) · [幅度差SVG](post_drop_agreement.svg) · [选点参照SVG](post_selection_reference.svg) · [F1相关SVG](post_f1_correlation.svg)。HTML内嵌所有图像和配对数据，可独立查看；CSV/SVG作为配套下载文件。

## 完整六点统计

{md_table(both[columns+['pearson_within_selector','spearman_excess_random','leave_one_seed_out_rho_min','leave_one_seed_out_rho_max']])}
'''
    (OUT/'post_REPORT.md').write_text(md,encoding='utf-8')
    body=MarkdownIt('commonmark',{'html':False}).enable('table').render(md)
    reader_image='<p><img src="post_paired_reading.png" alt="同seed真实F1下降配对" /></p>'
    assert reader_image in body
    body=body.replace(reader_image,reader_image+interactive_html(paired))
    for p in OUT.glob('post_*.png'):
        body=body.replace('src="'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'"')
    style='body{margin:0;background:#f5f7fa;color:#233444;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1250px;margin:auto;padding:32px}h2{border-top:1px solid #ccd5df;padding-top:24px;margin-top:38px}img{max-width:100%;background:white}table{display:block;overflow:auto;border-collapse:collapse;background:white;font-size:12px}td,th{border:1px solid #d9e1e7;padding:7px;white-space:nowrap}th{background:#e7eef5}a{color:#17649b}code{overflow-wrap:anywhere}strong{color:#095b73}'
    (OUT/'post_REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EXP-013 Post · Transfer correspondence</title><style>'+style+'</style><main>'+body+'</main></html>',encoding='utf-8')


def main():
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.hashsalt':'exp013-post-v1'})
    df,selections=load()
    selpairs,selsummary=overlap_tables(df,selections)
    paired,stats=effect_tables(df)
    relationship=relationship_table(paired,selpairs)
    paired_figure(paired)
    matrix_figure(stats,'spearman_drop','post_drop_correlation','F1-drop ordering: direct vs surrogate')
    matrix_figure(stats,'spearman_f1','post_f1_correlation','Post-unlearning F1 ordering: direct vs surrogate')
    matrix_figure(stats,'mae_pp','post_drop_agreement','F1-drop agreement: mean absolute paired difference',cmap='YlOrRd',limits=(0,max(stats.mae_pp)))
    selection_figure(selsummary);scatter_figures(paired,stats)
    checked=validate_statistics(paired,stats)
    audit=dict(execution_sha=SHA,run_id='r1',verified_files=1513,source_cells=756,paired_surrogate_cells=len(paired),
               selection_pairs=len(selpairs),correlation_rows=len(stats),scipy_crosschecked_rows=checked,
               stratum_observations=6,independent_training_seeds=3,rank_rounding_decimals_pp=10,
               undefined_drop_correlations=int(stats.spearman_drop.isna().sum()),excluded_completed_cells=0,
               figures=11,paired_view_settings=36,paired_view_observations_per_setting=9,scientific_decision='not_requested')
    (OUT/'post_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    make_report(stats,selsummary,relationship,checked,paired)
    print(json.dumps(audit))


if __name__=='__main__':main()
