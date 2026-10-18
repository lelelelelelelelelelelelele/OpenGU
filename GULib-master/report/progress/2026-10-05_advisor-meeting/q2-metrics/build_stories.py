"""Three evidence-bound figure narratives for Q2, using the audited metric export."""
import base64
import json
import re

from build_report import OUT, METHODS, DATASETS, ci, sha, read, table
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt


def main():
    provenance = read(OUT/'validation.json')
    for name in ['metrics_seed.csv', 'metrics_cells.csv']:
        assert sha(OUT/name) == provenance['output_csv_sha256'][name]
    cells = pd.read_csv(OUT/'metrics_cells.csv')
    chosen = cells.query("source == 'GCN' and selector in ['r_point','gt_full']")
    assert chosen.groupby(['dataset','seed','selector']).selection_id.nunique().eq(1).all()
    assert chosen.groupby(['dataset','seed','selector']).baseline_id.nunique().eq(1).all()
    assert chosen.groupby(['dataset','seed','selector']).method.nunique().eq(6).all()
    seed = pd.read_csv(OUT/'metrics_seed.csv')
    random = seed.query("selector == 'random'").set_index(['dataset','method','seed'])
    d = seed.query("source == 'GCN' and selector in ['r_point','gt_full']").copy()
    d['random_after'] = [random.loc[(r.dataset,r.method,r.seed),'after'] for r in d.itertuples()]
    d['A_R'] = [random.loc[(r.dataset,r.method,r.seed),'retrain_after']-r.retrain_after for r in d.itertuples()]
    d['E'] = d.delta_U-d.A_R
    assert np.allclose(d.delta_U, d.random_after-d.after)
    assert np.allclose(d.U, d.before-d.retrain_after+d.G)
    # Same retrain effect is one shared reference, not six independent observations.
    assert d.groupby(['dataset','selector','seed']).A_R.nunique().eq(1).all()
    metrics=['before','random_after','after','retrain_after','U','G','delta_U','A_R','E','flip','delta_flip']
    rows=[]
    for key,g in d.groupby(['dataset','selector','method']):
        assert len(g)==g.seed.nunique()==10
        for metric in metrics:
            mean,lo,hi=ci(g[metric])
            rows.append(dict(zip(['dataset','selector','method'],key))|dict(metric=metric,mean=mean,lo=lo,hi=hi,n=10))
    summary=pd.DataFrame(rows)
    summary.to_csv(OUT/'story_summary.csv',index=False,encoding='utf-8')
    d.to_csv(OUT/'story_seed.csv',index=False,encoding='utf-8')
    s=summary.set_index(['dataset','selector','method','metric'])

    def get(ds,sel,m,metric):return s.loc[(ds,sel,m,metric)]
    def value(ds,sel,m,metric):return get(ds,sel,m,metric)['mean']
    def interval(ds,sel,m,metric):
        r=get(ds,sel,m,metric)
        return f"{r['mean']:+.2f} [{r.lo:+.2f}, {r.hi:+.2f}]"
    def dot(ax,r,y,color,marker='o'):
        ax.errorbar(r['mean'],y,xerr=[[r['mean']-r.lo],[r.hi-r['mean']]],fmt=marker,color=color,ms=5,capsize=2,elinewidth=1)
    def axes_style(ax):
        ax.spines[['top','right','left']].set_visible(False)
        ax.spines['bottom'].set_color('#bacbd3')
        ax.tick_params(axis='y',length=0)
        ax.grid(axis='x',color='#e5edf0',lw=.7)
        ax.xaxis.set_major_locator(MaxNLocator(5))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'text.color':'#253c49','axes.labelcolor':'#253c49','xtick.color':'#526773','ytick.color':'#253c49','pdf.fonttype':42})
    figures=[]
    def save(fig,name):
        for ext in ['png','pdf']:fig.savefig(OUT/f'{name}.{ext}',dpi=180,facecolor='white')
        plt.close(fig);figures.append(name)

    fig,axs=plt.subplots(1,3,figsize=(14,7),sharey=True)
    roles=[('before','Before (configured model)','#82929c','s'),('random_after','GU / Random','#4e83ad','o'),('after','GU / D-full','#bc653c','o'),('retrain_after','Retrain / D-full','#218779','D')]
    for ax,ds in zip(axs,DATASETS):
        axes_style(ax)
        ax.set_yticks(range(6),METHODS);ax.set_ylim(5.5,-.65)
        ax.set_title(ds,loc='left',fontweight='bold',fontsize=13)
        for i,m in enumerate(METHODS):
            if i%2==0:ax.axhspan(i-.46,i+.46,color='#f3f7f8',zorder=0)
            for j,(metric,label,color,marker) in enumerate(roles):
                dot(ax,get(ds,'gt_full',m,metric),i+(j-1.5)*.2,color,marker)
        ax.set_xlabel('Test accuracy (%)')
    fig.suptitle('1  |  Where does the Retrain gap come from?',x=.055,ha='left',fontsize=17,fontweight='bold')
    fig.legend(handles=[plt.Line2D([],[],color=c,marker=k,ls='',label=l) for _,l,c,k in roles],loc='upper center',bbox_to_anchor=(.55,.925),ncol=4,frameon=False)
    fig.text(.055,.025,'Same D-full / GCN requests across all six GU methods. Before is method-specific; Retrain is the shared full-graph reference.\n10 training seeds; pointwise 95% t intervals. Dataset axes differ. GIF/IDEA are not independent replications.',fontsize=9,color='#526773')
    fig.subplots_adjust(left=.11,right=.98,top=.81,bottom=.14,wspace=.18)
    save(fig,'story01_retrain_context')

    fig,axs=plt.subplots(2,3,figsize=(14,9),sharey=True)
    for row,sel in enumerate(['gt_full','r_point']):
        for ax,ds in zip(axs[row],DATASETS):
            axes_style(ax);ax.set_yticks(range(6),METHODS);ax.set_ylim(5.5,-.6)
            ref=get(ds,sel,'GNNDelete','A_R')
            ax.axvspan(ref.lo,ref.hi,color='#218779',alpha=.10)
            ax.axvline(ref['mean'],color='#218779',ls='--',lw=1.4)
            ax.axvline(0,color='#a3b1b8',lw=1)
            for i,m in enumerate(METHODS):dot(ax,get(ds,sel,m,'delta_U'),i,'#bc653c' if sel=='gt_full' else '#536fba')
            ax.set_title(f"{ds} / {'D-full' if sel=='gt_full' else 'R-point'}",loc='left',fontweight='bold')
            ax.set_xlabel('Extra accuracy loss vs Random (pp)')
    fig.suptitle('2  |  One selector, different GU responses',x=.055,ha='left',fontsize=17,fontweight='bold')
    handles=[plt.Line2D([],[],marker='o',color='#bc653c',ls='',label='GU / D-full'),plt.Line2D([],[],marker='o',color='#536fba',ls='',label='GU / R-point'),plt.Line2D([],[],color='#218779',ls='--',label='Same-request Retrain effect (band: 95% CI)')]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.55,.95),ncol=3,frameon=False)
    fig.text(.055,.025,'GCN selection source; ten paired training seeds; Random averaged within seed. Positive = worse accuracy than Random.\nThe Retrain reference is shared across GU. Paired GU-minus-Retrain effects and intervals are in story_summary.csv (E).',fontsize=9,color='#526773')
    fig.subplots_adjust(left=.11,right=.98,top=.85,bottom=.13,hspace=.4,wspace=.2)
    save(fig,'story02_selector_across_gu')

    colors={'GNNDelete':'#b8513e','GIF':'#338b84','MEGU':'#7855a5','GraphEraser':'#b58c24','GraphRevoker':'#457fa8'}
    markers={'GNNDelete':'o','GIF':'s','MEGU':'^','GraphEraser':'D','GraphRevoker':'P'}
    for metric in ['delta_U','delta_flip']:
        a=d.query("method == 'GIF'").set_index(['dataset','selector','seed'])[metric]
        b=d.query("method == 'IDEA'").set_index(['dataset','selector','seed'])[metric]
        assert np.allclose(a,b)
    fig,axs=plt.subplots(2,3,figsize=(14,9))
    for row,sel in enumerate(['gt_full','r_point']):
        for col,ds in enumerate(DATASETS):
            ax=axs[row,col];axes_style(ax)
            ax.axvline(0,color='#9aabb4',lw=1);ax.axhline(0,color='#9aabb4',lw=1)
            for m,c in colors.items():
                x,y=get(ds,sel,m,'delta_U'),get(ds,sel,m,'delta_flip')
                ax.errorbar(x['mean'],y['mean'],xerr=[[x['mean']-x.lo],[x.hi-x['mean']]],yerr=[[y['mean']-y.lo],[y.hi-y['mean']]],fmt=markers[m],color=c,ms=6,capsize=2,elinewidth=.8,alpha=.9)
            ax.set_title(f"{ds} / {'D-full' if sel=='gt_full' else 'R-point'}",loc='left',fontweight='bold')
            ax.set_xlabel('Extra accuracy loss vs Random (pp)')
            if col==0:ax.set_ylabel('Extra GU-Retrain disagreement (pp)')
            ax.yaxis.set_major_locator(MaxNLocator(5))
            ax.margins(.13)
    fig.suptitle('3  |  Utility and prediction behavior can move differently',x=.055,ha='left',fontsize=17,fontweight='bold')
    fig.legend(handles=[plt.Line2D([],[],marker=markers[m],color=c,ls='',label='GIF / IDEA' if m=='GIF' else m) for m,c in colors.items()],loc='upper center',bbox_to_anchor=(.55,.95),ncol=5,frameon=False)
    fig.text(.055,.025,'Upper-left: accuracy improves vs Random, but GU-Retrain disagreement increases. Lower-left: both quantities decrease.\nError bars are marginal pointwise 95% intervals, not joint confidence regions. Panel scales differ; read numeric axes.',fontsize=9,color='#526773')
    fig.subplots_adjust(left=.08,right=.985,top=.85,bottom=.13,hspace=.4,wspace=.28)
    save(fig,'story03_utility_behavior')

    cases=[]
    for ds,sel,m in [('Cora','gt_full','GNNDelete'),('Cora','gt_full','GraphRevoker'),('PubMed','gt_full','GNNDelete'),('CiteSeer','r_point','GIF'),('CiteSeer','r_point','GraphEraser')]:
        cases.append({'条件':f'{ds} / {sel} / {m}','ΔU [95% CI]':interval(ds,sel,m,'delta_U'),'Retrain ΔU [95% CI]':interval(ds,sel,m,'A_R'),'E [95% CI]':interval(ds,sel,m,'E'),'Δ分歧 [95% CI]':interval(ds,sel,m,'delta_flip')})
    md=f'''# 问题 2：同一删除请求，为什么得到不同的 GU 响应？

2026-10-18 · 三张叙事图候选 · EXP-079/e79r5 · GCN 选点 · 十训练 seed

**问题 2 同时问两件事：同一 selector 对实际效用造成什么变化；这些变化与同请求 Retrain 的效用和预测行为有什么关系。** 下面按“先看端点 → 再比较 GU 响应 → 最后看效用与行为是否一致”组织。三张图共用同一批请求，不是三个独立实验。

## 图 1：大的 Retrain gap，需要结合初始性能和 Random 来理解

**方法审计更新：[原论文与当前实现对照](METHOD_AUDIT.html)。图中 GraphRevoker 实际是 GPA + optimal 配置版，当前 adapter 未接入论文的 contrastive 聚合模块，不能用于完整 GraphRevoker 的方法优劣结论。** [Before 来源核验](BEFORE_AUDIT.html)确认本批 Cora 没有误取单 shard；但数值能复算不代表完整方法实现正确。图和原数值保留为诊断，不以探索性聚合对照替换正式结果。

![删除前、Random、D-full 与同请求 Retrain 的准确率](story01_retrain_context.png)

**一句话发现：同样看到很大的 GU–Retrain gap，实际背景可能不同；只画 gap 会隐藏各方法起点和随机删除后的表现。**

以 Cora 的 D-full / GCN 请求为例，GNNDelete 从 {value('Cora','gt_full','GNNDelete','before'):.2f}% 降到 {value('Cora','gt_full','GNNDelete','after'):.2f}%，Random 后是 {value('Cora','gt_full','GNNDelete','random_after'):.2f}%，同请求 Retrain 是 {value('Cora','gt_full','GNNDelete','retrain_after'):.2f}%。因此这里既有方法对随机删除的下降，也有 D-full 的额外影响。GraphRevoker 的情况不同：初始准确率已经是 {value('Cora','gt_full','GraphRevoker','before'):.2f}%，D-full 后为 {value('Cora','gt_full','GraphRevoker','after'):.2f}%。其 {value('Cora','gt_full','GraphRevoker','G'):.2f} pp gap 不能全部称为该请求新造成的损伤。

**反例与范围。** CiteSeer 中多数端点接近，PubMed 的方法差别也不像 Cora 那样悬殊。分片方法与完整 GCN 起点不同；这里的 Retrain 是共同的 full-graph 参照，不是每个 GU 架构各自精确重训。因此图 1 是参照诊断，不是严格控制架构后的近似误差排名，也没有识别性能差异的因果机制。

**可用于正文的表述。** “The same retraining gap can arise against substantially different starting performance. Reporting the pre-deletion model and random-request outcome alongside the matched retraining endpoint distinguishes overall performance differences from the additional effect of targeted selection.”

## 图 2：同一 selector 的 Retrain 效应，不能直接当作各 GU 的损伤

![两个 selector 在六种 GU 上的额外准确率损失及 Retrain 参照](story02_selector_across_gu.png)

**一句话发现：固定请求后，各 GU 对定向选择的额外响应不同，而且这种关系随数据集改变。** 每幅面板内，各 GU 使用同一批选集，橙/蓝点是 GU 相对 Random 的额外损失 A_M；绿线是相同请求在 Retrain 上的额外损失 A_R。正值表示比 Random 更差。绿色阴影和横线属于同一个共享参照，不能算作六次复现。

Cora 的 D-full 请求在 Retrain 上额外损失 {value('Cora','gt_full','GNNDelete','A_R'):.2f} pp，到了 GNNDelete 是 {value('Cora','gt_full','GNNDelete','delta_U'):.2f} pp，而 MEGU 为 {value('Cora','gt_full','MEGU','delta_U'):.2f} pp。PubMed 则提供反向例子：同一 D-full 在 Retrain 上额外损失 {value('PubMed','gt_full','GNNDelete','A_R'):.2f} pp，GNNDelete 的均值却为 {value('PubMed','gt_full','GNNDelete','delta_U'):+.2f} pp。这表明“对 Retrain 有影响”不能直接换算成“对所有 GU 都有同样影响”。负均值的证据强弱仍应读区间。

为检验“放大或削弱”，计算逐训练 seed 的 E=A_M−A_R，再给配对区间，不能靠两组误差线是否重叠判断。下表保留该量及反例；完整六 GU、两策略、三数据集结果见 CSV。

{table(pd.DataFrame(cases))}

**反例与范围。** CiteSeer 的效用差异小，不能硬排出稳定的 GU 易受影响次序。这一图研究同 selector 在不同 GU 上的响应，不声称 D-full/R-point 优于所有策略；Degree 和完整策略范围仍由[完整指标页](REPORT.html)与 EXP-011 支撑。GIF/IDEA 数值重合，不作为独立验证。不同 GU 的训练和架构也不同，这里比较的是整个已配置系统的响应。

**可用于正文的表述。** “A request's effect on exact retraining does not determine its utility effect across approximate unlearning systems. Under matched deletion requests, the additional loss varies across GU methods and can change direction across datasets.”

## 图 3：同一 selector 的效用和行为响应，也不必同步

![相对 Random 的准确率损失与 GU–Retrain 分歧增量](story03_utility_behavior.png)

**一句话发现：某些条件下准确率提高了，与同请求 Retrain 的预测分歧却增加；另一些 GU 并不表现出这种分离。** 横轴是额外准确率损失，纵轴是额外预测分歧。左上象限表示准确率比 Random 更高、但分歧也更大；右上表示两者同时增加。零轴只是比较基准，不是遗忘正确性的阈值。

CiteSeer 的 GIF / R-point 是清楚的例子：ΔU={interval('CiteSeer','r_point','GIF','delta_U')} pp，而 Δ分歧={interval('CiteSeer','r_point','GIF','delta_flip')} pp。MEGU 的平均效用也改善、平均分歧增加，不过效用区间应单独阅读。GraphEraser 则是反例：同一 R-point 下 ΔU={interval('CiteSeer','r_point','GraphEraser','delta_U')} pp，Δ分歧={interval('CiteSeer','r_point','GraphEraser','delta_flip')} pp；它不支持“所有 GU 的分歧都会上升”。

**解释边界。** GraphEraser 的分歧变化区间跨零，因此它提供方向不同的均值，尚不能确认分歧降低。这说明单独按准确率给请求排序会遗漏预测行为变化；它不证明这种分歧就是隐私风险或遗忘失败。也尚未区分 GU 自己改变了哪些节点、Retrain 改变了哪些节点。若后续追问原因，需要核对两侧相对初始模型的逐节点变化，不能用这张散点图补写机制。横纵误差线分别为点态区间，不是二维联合置信域；这里是探索性分析。

**可用于正文的表述。** “Utility preservation does not imply preservation of prediction agreement with retraining. For the same selector, the relationship between these two responses is method-dependent: improved accuracy can coexist with increased disagreement, while other GU methods show mean decreases in both quantities.”

## 怎样放进论文

图 2 最适合作为问题 2 的主图：直接回答“一个 selector 对不同 GU 怎么样”。图 1 用来解释参照和方法起点，可压成前置概览或两个案例；图 3 支撑“效用与行为不总一致”的发现。三张候选先完整保留，成稿时再按版面选择，不要求全用双栏。

这三条经验发现可以由同一 framework 串起来：它固定请求、提供 Random 和 Retrain 参照，让不同 GU 的响应及其差异可比较。无需把三个观察强行解释成同一个机制。

## 证据、图源和复现

- [图 1 PDF](story01_retrain_context.pdf) · [图 2 PDF](story02_selector_across_gu.pdf) · [图 3 PDF](story03_utility_behavior.pdf)。
- [完整逐 seed 数据](story_seed.csv) · [完整均值与区间](story_summary.csv) · [生成脚本](build_stories.py) · [核验记录](story_validation.json)。
- [指标与原值完整页](REPORT.html) · [返回导师汇报](../REPORT.html)。
- 来源为经本轮核验的 2,520 份 metrics.json 派生表；本图使用 GCN 选点的两个 selector、三数据集、六 GU，共 360 个 GU 条件，另用同 seed 的 Random 平均值和同请求 Retrain。已检查每个 dataset/seed/selector 的 selection_id 和 Retrain output 在六 GU 间一致。
- 十个训练 seed，固定 split 2024、10% 训练候选节点删除、原图评估；Random 三请求先在 seed 内平均。点态 95% t 区间未作全矩阵多重比较校正，案例为事后探索性选例。未新增 GPU 运行，未改变科学接受状态。
'''
    (OUT/'STORIES.md').write_text(md,encoding='utf-8')
    body=MarkdownIt('commonmark',{'html':False}).enable('table').render(md)
    body=re.sub(r'src="([^"]+\.png)"',lambda m:'src="data:image/png;base64,'+base64.b64encode((OUT/m[1]).read_bytes()).decode()+'"',body)
    style='body{margin:0;background:#eef3f4;color:#253c49;font:16px/1.85 "Microsoft YaHei",sans-serif}main{max-width:1220px;margin:auto;background:white;padding:40px}h1{font-size:29px}h2{margin-top:42px;padding-top:18px;border-top:1px solid #d8e4e8}img{width:100%;height:auto}a{color:#177e78}table{font-size:12px;border-collapse:collapse;width:100%}td,th{padding:10px 8px;border-bottom:1px solid #dbe5e8;text-align:left}th{background:#edf5f5}@media(max-width:750px){main{padding:20px}table{display:block;overflow:auto}}'
    (OUT/'STORIES.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Q2：三张图讲清 GU 响应</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
    validation=dict(execution_sha=provenance['execution_sha'],upstream_csv_sha256={n:sha(OUT/n) for n in ['metrics_seed.csv','metrics_cells.csv']},selected_gu_cells=len(d),same_selection_across_six_gu=True,same_retrain_across_six_gu=True,shared_retrain_reference=True,paired_E_identity_checked=True,gif_idea_coordinates_identical=True,figures={n:sha(OUT/(n+'.png')) for n in figures},markdown_sha256=sha(OUT/'STORIES.md'),scientific_acceptance='not_requested',new_gpu_runs=0)
    (OUT/'story_validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',md):assert (OUT/target).exists(),target
    print(table(pd.DataFrame(cases)))
    print('Verified',len(d),'matched GU conditions; three PNG/PDF figures; all links exist.')


if __name__=='__main__':main()
