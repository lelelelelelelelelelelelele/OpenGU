"""Rebuild EXP-013 descriptive figures from the verified r1 return; no producers."""
import base64
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from experiments.modular_artifacts import read_run
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'results/runs/gpu4090/exp013-surrogate-to-gcn/r1'
AUDIT = ROOT / '.syncmate/recovery-exp013-full-20260930-r1'
SHA = '62926d95b843af137076eb9dd0a15e1c54c75663'
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
METHODS = ['GNNDelete', 'GIF', 'IDEA', 'MEGU', 'GraphEraser', 'GraphRevoker']
SOURCES = ['GCN', 'SGC', 'GAT', 'GIN']
SELECTORS = ['r_point', 'gt_full']
KEY = ['dataset', 'method', 'seed']
GROUP = ['dataset', 'method', 'source', 'selector']
COLORS = ['#2166ac', '#cf5b2b']


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(fig, name):
    fig.savefig(OUT / (name + '.png'), dpi=170, bbox_inches='tight', facecolor='white')
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight', facecolor='white')
    svg = OUT / (name + '.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n', encoding='utf-8')
    plt.close(fig)


def load():
    recovery = read(AUDIT / 'summary.json')
    assert recovery['ok'] and recovery['verify_summary']['status'] == 'verified'
    assert recovery['project_acceptance']['accepted_cells'] == 756
    manifest = read(AUDIT / 'manifest-response-2.json')
    prefix = 'results/runs/exp013-surrogate-to-gcn/r1/'
    expected = {x['path'][len(prefix):]: x['sha256'] for x in manifest['items'] if x['path'].startswith(prefix)}
    assert len(expected) == 1513
    for path, sha in expected.items():
        assert digest(BASE / path) == sha, path
    run, _ = read_run(BASE / 'run.json', expected['run.json'])
    assert run['commit'] == SHA and run['status'] == 'completed' and len(run['cells']) == 756
    records, selections, outputs = [], {}, {}
    for cell in run['cells']:
        assert cell['status'] == 'completed'
        c = cell['conditions']
        assert c['budget_ratio'] == .1 and c['model'] == 'OpenGU.GCNNet'
        for name, info in cell['files'].items():
            assert expected[cell['path'] + '/' + name] == info['sha256']
        stages = {x['stage']: x for x in read(BASE / cell['path'] / 'metrics.json')['rows']}
        sel = read(BASE / cell['path'] / 'selection.json')
        nodes = frozenset(sel['selected_nodes'])
        assert len(nodes) == len(sel['selected_nodes']) == sel['requested_k']
        assert sel['selection_id'] == cell['selection_id']
        selections[cell['selection_id']] = nodes
        stem = Path(c['selector_ref']).stem
        source = next((x for x in SOURCES[1:] if stem.endswith('_' + x.lower())), 'GCN') if c['selector'] in SELECTORS else 'baseline'
        u = stages['utility']['values']
        row = dict(cell_id=cell['cell_id'], dataset=c['dataset_name'], method=c['method'],
                   seed=c['training_seed'], random_seed=c.get('random_selector_seed'),
                   source=source, selector=c['selector'], selector_ref=c['selector_ref'],
                   split=c['dataset_fingerprint'], selection_id=cell['selection_id'],
                   output_id=cell['output']['artifact_id'], after=100*u['f1_after'],
                   before=None if u['f1_before'] is None else 100*u['f1_before'],
                   U=None if u['f1_before'] is None else 100*(u['f1_before']-u['f1_after']), G=None, flip=None)
        if c['method'] != 'Retrain':
            g, f = stages['post_unlearning_utility_and_retrain_gap'], stages['post_unlearning_flip_hop']
            assert g['baseline_output'] == f['baseline_output']
            row.update(G=100*g['values']['gap'], retrain=100*g['values']['perf_retrain'],
                       baseline_id=g['baseline_output']['artifact_id'], flip=100*f['values']['fraction_flipped'])
            assert abs(row['G'] - (row['retrain']-row['after'])) < 1e-8
        outputs[row['output_id']] = (row, cell['output'])
        records.append(row)
    for r in records:
        if r['method'] == 'Retrain':
            continue
        b, _ = outputs[r['baseline_id']]
        assert b['method'] == 'Retrain'
        assert all(b[k] == r[k] for k in ['dataset', 'split', 'seed', 'selection_id'])
        assert abs(b['after'] - r['retrain']) < 1e-8
    df = pd.DataFrame(records)
    assert not df[df.method != 'Retrain'][['U','G','flip']].isna().any().any()
    assert np.isfinite(df[df.method != 'Retrain'][['U','G','flip']].to_numpy()).all()
    assert set(df.dataset) == set(DATASETS) and set(df.seed) == {42,212,2024}
    cache = {layer:dict(Counter(c['cache'][layer] for c in run['cells'])) for layer in run['cells'][0]['cache']}
    (OUT/'audit.json').write_text(json.dumps(dict(job_id='exp013-full-20260930-r1',run_id='r1',execution_sha=SHA,
        manifest_sha256=expected['run.json'],verified_files=len(expected),cells=len(df),
        paired_gu_cells=648,cache_counts_per_cell_access=cache,scientific_acceptance='not_requested'),indent=2)+'\n',encoding='utf-8')
    df.to_csv(OUT/'cells.csv',index=False)
    return df, selections


def summarize(df):
    # Random sampling replicates are averaged WITHIN each training seed first.
    base = df[df.selector == 'random']
    assert base.groupby(KEY).size().eq(3).all()
    metrics = ['U','G','after','before','retrain','flip']
    random = base.groupby(KEY,as_index=False)[metrics].mean()
    gu = df[df.method != 'Retrain'].copy()
    rand = random[random.method != 'Retrain']
    gu = gu.merge(rand[KEY+['U','G']],on=KEY,validate='many_to_one',suffixes=('','_random'))
    gu['U_vs_random']=gu.U-gu.U_random
    gu['G_vs_random']=gu.G-gu.G_random
    direct=gu[gu.source=='GCN'][KEY+['selector','U','G','split']]
    attack=gu[gu.source.isin(SOURCES)].merge(direct,on=KEY+['selector','split'],validate='many_to_one',suffixes=('','_direct'))
    attack['U_vs_direct']=attack.U-attack.U_direct
    attack['G_vs_direct']=attack.G-attack.G_direct
    attack.to_csv(OUT/'paired_seed_values.csv',index=False)
    summary=attack.groupby(GROUP)[['U','G','U_vs_direct','G_vs_direct','U_vs_random','G_vs_random','after','flip']].agg(['mean','std','min','max'])
    summary.columns=['_'.join(x) for x in summary.columns]
    summary=summary.reset_index()
    summary.to_csv(OUT/'summary.csv',index=False)
    # Baselines for raw plots retain three training-seed means.
    baselines=pd.concat([rand.assign(source='baseline',selector='random'),gu[gu.selector=='degree']],ignore_index=True)
    baselines.to_csv(OUT/'baselines.csv',index=False)
    return attack, summary, baselines


def raw_plot(attack, baselines, metric):
    fig,axes=plt.subplots(3,6,figsize=(23,10),layout='constrained')
    for i,d in enumerate(DATASETS):
        for j,m in enumerate(METHODS):
            ax=axes[i,j]; a=attack[(attack.dataset==d)&(attack.method==m)]
            for si,s in enumerate(SELECTORS):
                for xi,source in enumerate(SOURCES):
                    vals=a[(a.selector==s)&(a.source==source)].sort_values('seed')[metric].to_numpy()
                    assert len(vals)==3
                    x=xi+(-.14 if si==0 else .14)
                    ax.scatter(x+np.array([-.035,0,.035]),vals,s=14,c=COLORS[si],alpha=.55)
                    ax.plot([x-.09,x+.09],[vals.mean()]*2,color=COLORS[si],lw=2.5)
            for s,color,style in [('random','#53646e','--'),('degree','#86993d',':')]:
                v=baselines[(baselines.dataset==d)&(baselines.method==m)&(baselines.selector==s)][metric]
                ax.axhline(v.mean(),color=color,ls=style,lw=1.4)
            ax.axhline(0,color='#d0d6dc',lw=.7,zorder=0)
            ax.set_xticks(range(4),SOURCES,fontsize=9)
            ax.set_title(d+' / '+m,fontsize=11)
            ax.grid(axis='y',alpha=.14)
            if j==0:ax.set_ylabel(metric+' (percentage points)')
    fig.suptitle(('Utility loss U = F1 before - F1 after' if metric=='U' else 'Signed gap G = Retrain F1 - GU F1')+'\nBlue: r_point  |  Orange: gt_full  |  dashed: Random  |  dotted: Degree\nDots: three training seeds; short bars: mean. Panel scales differ.',fontsize=14)
    save(fig,'raw_'+metric)


def paired_plot(attack,metric):
    fig,axes=plt.subplots(3,6,figsize=(23,10),layout='constrained')
    labels=[src+' / '+s for src in SOURCES[1:] for s in SELECTORS]
    for i,d in enumerate(DATASETS):
        for j,m in enumerate(METHODS):
            ax=axes[i,j];a=attack[(attack.dataset==d)&(attack.method==m)]
            for yi,(src,s) in enumerate((src,s) for src in SOURCES[1:] for s in SELECTORS):
                v=a[(a.source==src)&(a.selector==s)].sort_values('seed')[metric+'_vs_direct'].to_numpy()
                ax.scatter(v,yi+np.array([-.1,0,.1]),s=15,color=COLORS[SELECTORS.index(s)],alpha=.55)
                ax.scatter(v.mean(),yi,s=35,color=COLORS[SELECTORS.index(s)],marker='D')
            ax.axvline(0,color='#263846',lw=1);ax.grid(axis='x',alpha=.15)
            ax.set_yticks(range(6),labels if j==0 else ['']*6,fontsize=9);ax.invert_yaxis()
            ax.set_title(d+' / '+m,fontsize=11)
            if i==2:ax.set_xlabel('Surrogate - GCN direct (pp)')
    fig.suptitle(metric+' paired difference from direct\nRight of zero = larger '+('utility loss' if metric=='U' else 'signed retrain gap')+'; dots: paired seeds; diamonds: mean. Panel scales differ.',fontsize=14)
    save(fig,'paired_'+metric)


def heatmap(summary,metric):
    columns=[(d,m) for d in DATASETS for m in METHODS]
    rows=[(src,s) for src in SOURCES[1:] for s in SELECTORS]
    values=np.array([[summary[(summary.dataset==d)&(summary.method==m)&(summary.source==src)&(summary.selector==s)][metric+'_vs_random_mean'].iloc[0] for d,m in columns] for src,s in rows])
    lim=max(abs(values.min()),abs(values.max()),1)
    fig,ax=plt.subplots(figsize=(21,5),layout='constrained')
    im=ax.imshow(values,cmap='RdBu_r',vmin=-lim,vmax=lim,aspect='auto')
    for i in range(6):
        for j in range(18):ax.text(j,i,f'{values[i,j]:.1f}',ha='center',va='center',fontsize=9,color='white' if abs(values[i,j])>lim*.55 else '#182731')
    ax.set_xticks(range(18),[d+'\n'+m for d,m in columns],rotation=45,ha='right',fontsize=9)
    ax.set_yticks(range(6),[src+' / '+s for src,s in rows]);ax.set_title(metric+' excess over Random (pp) | red = larger than Random\nMean of three seed-paired contrasts; Random first averaged over three sampling seeds',fontsize=13)
    for x in [5.5,11.5]:ax.axvline(x,color='white',lw=3)
    fig.colorbar(im,ax=ax,shrink=.85,label='percentage points');save(fig,'random_'+metric)


def overlap(attack,selections):
    unique=attack.drop_duplicates(['dataset','seed','source','selector'])
    direct={(r.dataset,r.seed,r.selector):selections[r.selection_id] for r in unique.itertuples() if r.source=='GCN'}
    rows=[]
    for r in unique.itertuples():
        if r.source=='GCN':continue
        a=selections[r.selection_id];b=direct[r.dataset,r.seed,r.selector]
        rows.append(dict(dataset=r.dataset,seed=r.seed,source=r.source,selector=r.selector,jaccard=len(a&b)/len(a|b)))
    ov=pd.DataFrame(rows);ov.to_csv(OUT/'selection_overlap.csv',index=False)
    fig,axes=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
    for ax,d in zip(axes,DATASETS):
        for si,s in enumerate(SELECTORS):
            for xi,src in enumerate(SOURCES[1:]):
                v=ov[(ov.dataset==d)&(ov.source==src)&(ov.selector==s)].jaccard.to_numpy()
                x=xi+(-.13 if si==0 else .13)
                ax.scatter(x+np.array([-.03,0,.03]),v,c=COLORS[si],s=20,alpha=.6)
                ax.plot([x-.08,x+.08],[v.mean()]*2,color=COLORS[si],lw=2)
        ax.set_xticks(range(3),SOURCES[1:]);ax.set_ylim(0,1);ax.set_title(d);ax.set_ylabel('Jaccard with GCN direct');ax.grid(axis='y',alpha=.15)
    fig.suptitle('Selection overlap | Blue: r_point; orange: gt_full | dots: three seeds')
    save(fig,'selection_overlap')
    return ov


def focus(attack,baselines):
    fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
    for i,d in enumerate(['Cora','PubMed']):
        for j,metric in enumerate(['U','G']):
            ax=axes[i,j]
            for xi,src in enumerate(SOURCES):
                v=attack[(attack.dataset==d)&(attack.method=='GNNDelete')&(attack.selector=='gt_full')&(attack.source==src)].sort_values('seed')[metric].to_numpy()
                ax.scatter(xi+np.array([-.09,0,.09]),v,color='#cf5b2b',s=38,alpha=.7)
                ax.plot([xi-.19,xi+.19],[v.mean()]*2,color='#753516',lw=3)
                ax.annotate(f'{v.mean():.2f}',(xi,v.max()),xytext=(0,9),textcoords='offset points',ha='center',fontsize=11)
            for s,color,style in [('random','#53646e','--'),('degree','#86993d',':')]:
                v=baselines[(baselines.dataset==d)&(baselines.method=='GNNDelete')&(baselines.selector==s)][metric]
                ax.axhline(v.mean(),color=color,ls=style,label=s.title())
            ax.set_xticks(range(4),['GCN direct','SGC','GAT','GIN']);ax.set_ylabel(metric+' (pp)');ax.set_title(d+' / GNNDelete / gt_full');ax.grid(axis='y',alpha=.13);ax.margins(y=.24);ax.legend(fontsize=9)
    fig.suptitle('Two observed transfer cases: similar to direct, or stronger than direct\nU = F1 before - after; G = Retrain F1 - GU F1; dots are seeds; bars and labels are means.',fontsize=13)
    save(fig,'focus_gt_full')


def md_table(frame):
    cols=list(frame.columns)
    def fmt(x):
        return f'{x:.2f}' if isinstance(x,(float,np.floating)) else str(x)
    return '\n'.join(['| '+' | '.join(cols)+' |','| '+' | '.join(['---']*len(cols))+' |']+['| '+' | '.join(fmt(x) for x in row)+' |' for row in frame.itertuples(index=False,name=None)])


def report(attack,summary,baselines,ov):
    s=summary[summary.source!='GCN']
    def value(d,m,src,sel,col):
        return summary[(summary.dataset==d)&(summary.method==m)&(summary.source==src)&(summary.selector==sel)][col].iloc[0]
    def val(d,src,col):return value(d,'GNNDelete',src,'gt_full',col)
    highlights=s[((s.method=='GNNDelete')&(s.selector=='gt_full')&(((s.dataset=='Cora')&(s.source=='GIN'))|((s.dataset=='PubMed')&(s.source=='SGC'))))|((s.dataset=='PubMed')&(s.method=='GraphEraser')&(s.source=='GAT')&(s.selector=='r_point'))|((s.dataset=='Cora')&(s.method=='GNNDelete')&(s.source=='GAT')&(s.selector=='r_point'))]
    table_cols=['dataset','method','source','selector','U_mean','G_mean','U_vs_direct_mean','G_vs_direct_mean','U_vs_random_mean','G_vs_random_mean']
    md=f'''# EXP-013 · Surrogate → GCN：哪些攻击效果能迁移？

这轮结果支持**特定数据集、方法和选点算法上的迁移**，不支持“任意代理模型都能复现白盒效果”。最清晰的现象来自 GNNDelete + gt_full：Cora 的 GIN 代理接近 direct，PubMed 的 SGC 代理明显超过 direct。完整结果同时包含弱效果、负增益和 utility / retrain-gap 分离的组合。

## 先看这张图

![GNNDelete gt_full 的两个迁移案例](focus_gt_full.png)

这张图是观察结果后选取的示例，不能代表全部组合。下文给出全部 108 个 surrogate 分组及 direct / Random / Degree 对照。每个点为一个训练 seed，每条短线及数字为三个 seed 的均值；Random 先对同一训练 seed 的三个抽样 seed 求均值。

## 关键观察

1. **Cora / GNNDelete / gt_full / GIN：接近 direct 的正例。** U 为 {val('Cora','GIN','U_mean'):.2f} pp，GCN direct 为 {val('Cora','GCN','U_mean'):.2f} pp；配对差为 {val('Cora','GIN','U_vs_direct_mean'):+.2f} pp。G 为 {val('Cora','GIN','G_mean'):.2f} pp，相比 direct 差 {val('Cora','GIN','G_vs_direct_mean'):+.2f} pp。相对 Random 的 U/G 增量分别为 {val('Cora','GIN','U_vs_random_mean'):+.2f}/{val('Cora','GIN','G_vs_random_mean'):+.2f} pp，三个 seed 均高于各自 Random 均值。这是描述性的“接近”，不是统计等效结论。
2. **PubMed / GNNDelete / gt_full / SGC：surrogate 超过 direct。** U/G 为 {val('PubMed','SGC','U_mean'):.2f}/{val('PubMed','SGC','G_mean'):.2f} pp，相对 direct 为 {val('PubMed','SGC','U_vs_direct_mean'):+.2f}/{val('PubMed','SGC','G_vs_direct_mean'):+.2f} pp，相对 Random 为 {val('PubMed','SGC','U_vs_random_mean'):+.2f}/{val('PubMed','SGC','G_vs_random_mean'):+.2f} pp。三个配对 seed 的两项增量均为正。direct 在这里并不是攻击强度上界，也不适合作为“迁移百分比”的分母。
3. **迁移不是普遍成立。** 108 个 dataset × GU × surrogate × selector 分组中，U 均值高于 Random 的有 {int((s.U_vs_random_mean>0).sum())} 个，G 有 {int((s.G_vs_random_mean>0).sum())} 个。这只是正负号计数，不是成功率、显著性检验或独立重复；GIF/IDEA 的本轮 F1 结果相同，不能把它们算作两份独立支持证据。Cora / GNNDelete / GAT / r_point 的 U 相对 Random 为 {value('Cora','GNNDelete','GAT','r_point','U_vs_random_mean'):+.2f} pp，构成直接反例。
4. **utility 迁移与 GU-gap 迁移需要分开。** PubMed / GraphEraser / GAT / r_point 的 U 相对 Random 为 {value('PubMed','GraphEraser','GAT','r_point','U_vs_random_mean'):+.2f} pp，但 G 为 {value('PubMed','GraphEraser','GAT','r_point','G_vs_random_mean'):+.2f} pp：更大的总损失不等于更大的近似遗忘偏差。

下表单位均为百分点（pp），全部是三个训练 seed 的均值。`vs_direct` 为同 selector 的配对差；`vs_random` 为同数据集、方法、训练 seed 下相对 Random 均值的差。

{md_table(highlights[table_cols])}

**Degree 是更强的必要参照。** Cora / GNNDelete 的 Degree 均值 U/G 为 19.00/18.88 pp，因此 GIN + gt_full 相比它仅高约 1.23/0.49 pp；相对 Random 的大增量不能用来声称显著优于拓扑基线。PubMed 的 Degree U/G 为 1.36/1.63 pp，SGC + gt_full 的对应增量约为 8.95/8.79 pp。这里同样只报告观察差异，不作显著性声明。

## 全部组合相对 Random 的变化

红色表示比 Random 更大的损失或 signed gap，蓝色表示更小。两图颜色范围各自标定，比较时应读数值；这里不把微小正数标为显著效果。

![所有 surrogate 的 utility 增量](random_U.png)

![所有 surrogate 的 signed gap 增量](random_G.png)

## 原始效果与 direct 配对差

U = 100 × (F1_before − F1_after)，越大表示总性能下降越多，负数表示性能提高。

G = 100 × (F1_Retrain − F1_GU)，保持符号；正数表示 GU 差于同请求 Retrain，负数表示 GU 优于它。本报告的 G 与原始 `gap` 同号，**不能与 EXP-011 报告中采用相反方向的 GU − Retrain 列直接混用**。

![全部 utility 原始值](raw_U.png)

![全部 signed gap 原始值](raw_G.png)

上述图的蓝色为 r_point、橙色为 gt_full，虚线为 Random 均值、点线为 Degree 均值。各面板纵轴独立，不能以视觉高度跨面板排名。Random/Degree 的逐 seed 数值在 baselines.csv。

![utility 相对 direct 的配对差](paired_U.png)

![signed gap 相对 direct 的配对差](paired_G.png)

配对图横轴为 surrogate − GCN direct，零线右侧表示该指标更大。圆点为三个同 seed 配对差，菱形为均值；各面板横轴独立。未设等效容差，不作“等效”“100%迁移”或 p 值声明。

## 选集是否相似？

![代理与 direct 选集的 Jaccard](selection_overlap.png)

Jaccard 只解释选集重叠，不代表效果。在 PubMed / gt_full 中，SGC 与 GCN direct 的平均 Jaccard 仅 {ov[(ov.dataset=='PubMed')&(ov.source=='SGC')&(ov.selector=='gt_full')].jaccard.mean():.3f}，却产生上述更强的 GNNDelete U/G。低重叠与强效果在本例中并存；这不是关于重叠与效果因果关系的证明。每个选集跨 GU 复用，重叠统计按 dataset × seed × source × selector 去重，不重复计六次。

## 范围、核验与解释边界

- 范围：Cora、CiteSeer、PubMed；训练 seeds 42/212/2024；删除训练候选节点的 10%；GCN/SGC/GAT/GIN × r_point/gt_full，外加 Degree 和三个独立 Random 抽样；六种 GU + 同请求 Retrain。合计 756 个单元，其中 648 个 GU 单元、108 个 Retrain。
- Victim 固定为 GCN backbone；GraphEraser/GraphRevoker 是分片集成，其全图 Retrain 参照与单模型 GU 的解释边界不同，不称其为 ensemble-direct。
- 本实验为共享图、训练划分及 validation labels 假设下的灰盒、无 victim 查询迁移；不能推广到完全黑盒、其他 victim 架构、其他预算或不同 split。
- 1513 个文件逐一匹配可信回传 manifest 的 SHA-256，原始 read_run 消费器通过；648 个 GU 的同请求 Retrain 身份、选集、seed、split 和数值关系均核对。未排除任何已完成单元。
- 原始 Retrain 没有 f1_before，所以不虚构 Retrain 自身的 U；它在本报告中作为各 GU 的配对 G 参照，完整 after 数值见 cells.csv。
- 样本量为三个训练 seed，不把 Random 抽样、六种 GU、两个算法或同一选集重复当作独立样本。统计量均为描述性；summary.csv 提供均值、样本标准差、最小/最大值。
- 执行成功、回传 verified、项目产物 accepted 均已确认；**科学结论仍待用户评议**。

## 对论文问题的回答

可支持的表述是：在固定 GCN victim 和本轮共享数据假设下，部分 surrogate 选集能够产生与 direct 接近或更强的损失及 signed retrain-gap，且现象依赖 dataset、GU 和 selector；GNNDelete/gt_full 是本轮最明确的展示案例。不能据此写成所有 GU、所有 surrogate 都稳定迁移。

建议放在“跨架构迁移”结果小节：主图候选为 focus_gt_full，紧随 random_U/random_G 的全范围检查；四张完整分面图、重叠图和全表保留在附录。示例是事后选择，正文应同时交代反例。后续若要主张等效或泛化，需要在新结果出现前明确容差与额外重复范围；本分析不启动新实验。

## 可复用数据与复现

- [逐单元数据 cells.csv](cells.csv)：全部 756 个单元、来源及原始效果。
- [配对 seed 数据 paired_seed_values.csv](paired_seed_values.csv)：432 个 source × GU × seed × selector 观测及 direct/Random 差值。
- [完整统计 summary.csv](summary.csv)：144 个含 direct 的分组及均值、标准差和范围。
- [简单基线 baselines.csv](baselines.csv)、[选集重叠 selection_overlap.csv](selection_overlap.csv)、[身份核验 audit.json](audit.json)。
- 每张图同时生成 PNG 和可编辑矢量 SVG；报告 HTML 内嵌 PNG，可以独立打开。
- 生成器：[analyze_surrogate.py](analyze_surrogate.py)。在仓库根运行 `python -X utf8 self/research/analyses/EXP-013/analyze_surrogate.py`，依赖现有 matplotlib/numpy/pandas/markdown-it-py，不运行模型或读取远端 Cache。
- 原始执行 SHA：`{SHA}`；job：`exp013-full-20260930-r1`；run：`r1`。
- run.json 的可信 SHA-256：`70588d5793760e44ae268dfe55b3648e0638b71fde3a4db0eee998dc51760a49`。
- 恢复证据：`.syncmate/recovery-exp013-full-20260930-r1/summary.json`；输入：`results/runs/gpu4090/exp013-surrogate-to-gcn/r1/`。这些运行文件保持原样。

矢量图下载：[重点案例](focus_gt_full.svg) · [Random U](random_U.svg) · [Random G](random_G.svg) · [原始 U](raw_U.svg) · [原始 G](raw_G.svg) · [配对 U](paired_U.svg) · [配对 G](paired_G.svg) · [选集重叠](selection_overlap.svg)。

## 完整分组表

下表包含 GCN direct 和全部 surrogate，没有按结果好坏删行。精度更高的数值、标准差和逐 seed 记录见 CSV。

{md_table(summary[table_cols])}
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body=MarkdownIt('commonmark',{'html':False}).enable('table').render(md)
    for img in OUT.glob('*.png'):
        data=base64.b64encode(img.read_bytes()).decode('ascii')
        body=body.replace('src="'+img.name+'"','src="data:image/png;base64,'+data+'"')
    style='''body{font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif;color:#233444;background:#f4f7fa;margin:0}main{max-width:1500px;margin:auto;padding:35px}h1{font-size:34px}h2{border-top:1px solid #ccd7df;padding-top:24px;margin-top:40px}img{width:100%;background:white;border:1px solid #dde5eb}p,li{max-width:1250px}table{font-size:12px;border-collapse:collapse;width:100%;background:white;display:block;overflow:auto}td,th{padding:8px;border:1px solid #d9e1e7;white-space:nowrap}th{background:#e9f0f5}a{color:#17659c}code{overflow-wrap:anywhere}strong{color:#07576c}@media(max-width:700px){main{padding:16px}}'''
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EXP-013 · Surrogate transfer</title><style>'+style+'</style><main>'+body+'</main></html>',encoding='utf-8')


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
    df,selections=load();attack,summary,baselines=summarize(df)
    for metric in ['U','G']:
        raw_plot(attack,baselines,metric);paired_plot(attack,metric);heatmap(summary,metric)
    ov=overlap(attack,selections);focus(attack,baselines);report(attack,summary,baselines,ov)
    print('Verified 1513 files; 756 cells; generated 8 PNG/SVG figures, CSVs and REPORT.md/REPORT.html')


if __name__=='__main__':main()
