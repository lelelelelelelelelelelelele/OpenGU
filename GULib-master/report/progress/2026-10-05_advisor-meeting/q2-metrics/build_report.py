"""Q2 figure prototypes from verified e79r5 metrics; no model execution."""
from pathlib import Path
import ast
import base64
import hashlib
import json
import re
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
from scipy.stats import t
from markdown_it import MarkdownIt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
DATA = ROOT / 'self/research/analyses/EXP-079/e79r5'
RUN = ROOT / 'results/runs/gpu4090/exp079-surrogate-multiseed/e79r5'
METHODS = ['GNNDelete', 'GIF', 'IDEA', 'MEGU', 'GraphEraser', 'GraphRevoker']
DATASETS = ['Cora', 'CiteSeer', 'PubMed']
REQUESTS = ['random', 'degree', 'r_point', 'gt_full']
COLORS = dict(zip(REQUESTS, ['#80909c', '#ca942e', '#288b87', '#ae5b85']))
LABELS = dict(zip(REQUESTS, ['Random', 'Degree', 'R-point', 'D-full']))
KEY = ['dataset', 'method', 'seed']
HOPS = ['1_hop', '2_hop', '3_hop', 'gt3_hop']


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ci(v):
    v = np.asarray(v, float)
    assert len(v) == 10 and np.isfinite(v).all()
    m = float(v.mean())
    h = float(t.ppf(.975, 9) * v.std(ddof=1) / np.sqrt(10))
    return m, m-h, m+h


def table(df):
    def fmt(v):
        return f'{v:.3f}' if isinstance(v, (float, np.floating)) else str(v)
    return '| ' + ' | '.join(df.columns) + ' |\n| ' + ' | '.join(['---']*len(df.columns)) + ' |\n' + '\n'.join('| ' + ' | '.join(map(fmt, r)) + ' |' for r in df.itertuples(index=False, name=None))


def main():
    audit = read(DATA/'audit.json')
    assert sha(RUN/'run.json') == audit['run_sha256']
    run = read(RUN/'run.json')
    assert run['commit'] == audit['execution_sha'] and len(run['cells']) == 2520
    code = subprocess.check_output(['git', 'show', f"{run['commit']}:GULib-master/experiments/output_metrics.py"], cwd=ROOT)
    frozen_functions = {n.name: ast.dump(n) for n in ast.parse(code).body if isinstance(n, ast.FunctionDef)}
    current_functions = {n.name: ast.dump(n) for n in ast.parse((ROOT/'experiments/output_metrics.py').read_text(encoding='utf-8')).body if isinstance(n, ast.FunctionDef)}
    for name in ['method_metrics', 'update_detection']:
        assert frozen_functions[name] == current_functions[name], name
    records = []
    for c in run['cells']:
        p = RUN/c['path']/'metrics.json'
        assert sha(p) == c['files']['metrics.json']['sha256']
        doc = read(p)
        assert doc['cell_id'] == c['cell_id']
        stages = {s['stage']: s for s in doc['rows']}
        m, u = stages['method']['values'], stages['utility']['values']
        assert m['accuracy'] == m['f1'] == u['f1_after']
        cond = c['conditions']
        r = dict(cell_id=c['cell_id'], output_id=c['output']['artifact_id'], raw_selection_id=c['selection_id'],
                 raw_dataset=cond['dataset_name'], raw_method=cond['method'], raw_seed=cond['training_seed'], raw_selector=cond['selector'],
                 raw_after=100*m['accuracy'], raw_before=None if u['f1_before'] is None else 100*u['f1_before'],
                 CE=m['cross_entropy'], AUC=100*m['classification_auc'],
                 auc_status=m['classification_auc_status'],
                 update_auc=m['update_detection_auc'], update_status=m['update_detection_auc_status'])
        if c['conditions']['method'] != 'Retrain':
            f = stages['post_unlearning_flip_hop']
            g = stages['post_unlearning_utility_and_retrain_gap']
            assert f['baseline_output'] == g['baseline_output']
            assert f['identity']['protocol']['comparison'] == 'argmax_gu_vs_same_request_retrain_first_index_ties'
            assert f['identity']['protocol']['evaluation_mask'] == 'test_mask_excluding_selected_nodes'
            r.update(baseline_id=g['baseline_output']['artifact_id'], raw_G=100*g['values']['gap'], raw_flip=100*f['values']['fraction_flipped'])
            h = f['values']
            assert sum(h[k+'_count'] for k in HOPS) == h['node_count']
            assert sum(h[k+'_flipped_count'] for k in HOPS) == h['flipped_count']
            for k in HOPS:
                count, flips = h[k+'_count'], h[k+'_flipped_count']
                rate = h[k+'_flip_rate']
                assert (rate is None and count == 0) or np.isclose(rate, flips/count)
                r[k+'_count'], r[k+'_flipped_count'] = count, flips
                r[k+'_rate'] = None if rate is None else 100*rate
        records.append(r)
    raw = pd.DataFrame(records)
    cells = pd.read_csv(DATA/'cells.csv')
    assert len(cells) == 2520 and cells.cell_id.is_unique
    x = cells.merge(raw, on=['cell_id', 'output_id'], validate='one_to_one', suffixes=('', '_raw'))
    for name in ['dataset', 'method', 'seed', 'selector', 'selection_id']:
        assert (x[name] == x['raw_'+name]).all(), name
    assert np.allclose(x.after, x.raw_after)
    gu = x[x.method != 'Retrain'].copy()
    assert len(gu) == 2160
    for name, col in [('before', 'raw_before'), ('G', 'raw_G'), ('flip', 'raw_flip')]:
        assert np.allclose(gu[name], gu[col])
    assert (gu.baseline_id == gu.baseline_id_raw).all()
    assert gu.groupby(KEY).before.nunique().eq(1).all()
    retrain = x[x.method == 'Retrain'].set_index('output_id')
    assert retrain.index.is_unique
    for name in ['dataset', 'seed', 'split', 'selection_id']:
        assert (gu[name] == gu.baseline_id.map(retrain[name])).all(), name
    for name in ['after', 'CE', 'AUC']:
        gu['retrain_'+name] = gu.baseline_id.map(retrain[name])
    assert np.allclose(gu.retrain_after, gu.retrain)
    assert np.isfinite(gu[['CE', 'AUC', 'retrain_CE', 'retrain_AUC']]).all().all()
    # All sources retained in exported tables. Q2 plots hold selection source at GCN;
    # Q3 owns the change of source. Each Random mean has three requests per seed.
    vals = ['after', 'before', 'U', 'G', 'flip', 'CE', 'AUC', 'retrain_after', 'retrain_CE', 'retrain_AUC']
    random = gu[gu.selector == 'random']
    assert random.groupby(KEY).size().eq(3).all()
    refs = random.groupby(KEY)[vals].mean().add_suffix('_random').reset_index()
    gu = gu.merge(refs, on=KEY, validate='many_to_one')
    gu['delta_U'] = gu.U-gu.U_random
    gu['delta_CE'] = gu.CE-gu.CE_random
    gu['delta_AUC_loss'] = gu.AUC_random-gu.AUC
    gu['delta_flip'] = gu.flip-gu.flip_random
    metrics = vals + ['delta_U', 'delta_CE', 'delta_AUC_loss', 'delta_flip']
    seed = gu.groupby(KEY+['selector', 'source'], as_index=False)[metrics].mean()
    rows = []
    for key, group in seed.groupby(['dataset', 'method', 'selector', 'source']):
        assert len(group) == group.seed.nunique() == 10
        for metric in metrics:
            m, lo, hi = ci(group[metric])
            rows.append(dict(zip(['dataset', 'method', 'selector', 'source'], key)) | dict(metric=metric, mean=m, lo=lo, hi=hi, n=10))
    summary = pd.DataFrame(rows)
    gu.to_csv(OUT/'metrics_cells.csv', index=False, encoding='utf-8')
    seed.to_csv(OUT/'metrics_seed.csv', index=False, encoding='utf-8')
    summary.to_csv(OUT/'metrics_summary.csv', index=False, encoding='utf-8')
    hoprows = []
    for key, group in gu.groupby(['dataset', 'method', 'selector', 'source']):
        for hop in HOPS:
            # Average rates within seed, excluding undefined empty strata; counts remain visible.
            z = group.groupby('seed')[[hop+'_rate', hop+'_count']].mean()
            hoprows.append(dict(zip(['dataset', 'method', 'selector', 'source'], key)) | dict(hop=hop, valid_seeds=int(z[hop+'_rate'].notna().sum()), mean_rate=z[hop+'_rate'].mean(), mean_node_count=z[hop+'_count'].mean(), empty_request_strata=int(group[hop+'_count'].eq(0).sum())))
    pd.DataFrame(hoprows).to_csv(OUT/'hop_summary.csv', index=False, encoding='utf-8')
    coverage = x.groupby('method').agg(cells=('cell_id', 'size'), CE=('CE', 'count'), classification_AUC=('AUC', 'count'), update_detection_AUC=('update_auc', 'count'), before_accuracy=('raw_before', 'count'), GU_Retrain_disagreement=('raw_flip', 'count')).reset_index()
    coverage.to_csv(OUT/'metric_coverage.csv', index=False, encoding='utf-8')

    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10, 'axes.spines.top':False, 'axes.spines.right':False, 'axes.spines.left':False, 'axes.edgecolor':'#c7d2d9', 'text.color':'#243947', 'axes.labelcolor':'#243947', 'xtick.color':'#526572', 'ytick.color':'#243947', 'pdf.fonttype':42})
    direct = summary[summary.source.isin(['GCN', 'baseline'])].set_index(['dataset','method','selector','metric'])

    def point(ax, ds, method, selector, metric, y, marker='o', hollow=False):
        r = direct.loc[(ds,method,selector,metric)]
        ax.errorbar(r['mean'], y, xerr=[[r['mean']-r.lo],[r.hi-r['mean']]], fmt=marker, ms=4.3, color=COLORS[selector], mfc='white' if hollow else COLORS[selector], capsize=1.8, elinewidth=.9, zorder=3)

    def frame(ax):
        ax.set_ylim(5.5,-.65)
        ax.set_yticks(range(6), METHODS)
        ax.tick_params(axis='y',length=0)
        ax.grid(axis='x',color='#e5ebee',lw=.7)
        ax.xaxis.set_major_locator(MaxNLocator(5))
        for i in range(6):
            if i%2 == 0: ax.axhspan(i-.46,i+.46,color='#f4f7f8',zorder=0)

    figures=[]
    for ds in DATASETS:
        fig, axes = plt.subplots(1,3,figsize=(15,8), sharey=True, gridspec_kw={'width_ratios':[1.3,1,1]})
        for ax in axes: frame(ax)
        axes[0].set_title('(a) Actual test accuracy',loc='left',fontweight='bold')
        axes[1].set_title('(b) Extra loss vs Random',loc='left',fontweight='bold')
        axes[2].set_title('(c) GU-Retrain disagreement',loc='left',fontweight='bold')
        for i, method in enumerate(METHODS):
            before=direct.loc[(ds,method,'random','before'),'mean']
            axes[0].vlines(before,i-.43,i+.43,color='#243947',ls=':',lw=1.25,zorder=4)
            for j, selector in enumerate(REQUESTS):
                y=i+(j-1.5)*.21
                a=direct.loc[(ds,method,selector,'after'),'mean']
                b=direct.loc[(ds,method,selector,'retrain_after'),'mean']
                axes[0].plot([a,b],[y,y],color=COLORS[selector],alpha=.4,lw=1)
                point(axes[0],ds,method,selector,'after',y)
                point(axes[0],ds,method,selector,'retrain_after',y,marker='D',hollow=True)
                point(axes[1],ds,method,selector,'delta_U',y)
                point(axes[2],ds,method,selector,'flip',y)
        axes[0].set_xlabel('Accuracy (%)  |  higher is better')
        axes[1].set_xlabel('Random accuracy - selected accuracy (pp)')
        axes[1].axvline(0,color='#6c7d88',lw=1)
        axes[2].set_xlabel('Different predicted labels (%)')
        axes[2].set_xlim(left=0)
        fig.suptitle(f'{ds}  |  Q2: utility and prediction behavior',x=.07,ha='left',fontsize=17,fontweight='bold')
        handles=[plt.Line2D([],[],color=COLORS[k],marker='o',ls='',label=LABELS[k]) for k in REQUESTS]
        handles += [plt.Line2D([],[],color='#243947',marker='o',ls='',label='GU'),plt.Line2D([],[],color='#243947',mfc='white',marker='D',ls='',label='Same-request Retrain'),plt.Line2D([],[],color='#243947',ls=':',label='Method-specific before (mean)')]
        fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.54,.94),ncol=4,frameon=False)
        fig.text(.07,.025,'GCN selection source; 10 training seeds; fixed split and 10% budget. Error bars: pointwise 95% t intervals.\nRandom: three requests averaged within each training seed. GIF/IDEA are shown separately, not independent replications.',fontsize=9,color='#526572')
        fig.subplots_adjust(left=.105,right=.985,top=.82,bottom=.13,wspace=.2)
        name=f'{ds.lower()}_q2_overview'
        for ext in ['png','pdf']:fig.savefig(OUT/f'{name}.{ext}',dpi=170,facecolor='white')
        plt.close(fig);figures.append(name)

        fig, axes = plt.subplots(1,2,figsize=(10,7.5),sharey=True)
        for ax in axes:frame(ax);ax.axvline(0,color='#6c7d88',lw=1)
        for i, method in enumerate(METHODS):
            for j, selector in enumerate(REQUESTS[1:]):
                y=i+(j-1)*.24
                point(axes[0],ds,method,selector,'delta_CE',y)
                point(axes[1],ds,method,selector,'delta_AUC_loss',y)
        axes[0].set_title('Cross-entropy increase',loc='left',fontweight='bold')
        axes[1].set_title('Classification AUC loss',loc='left',fontweight='bold')
        axes[0].set_xlabel('Selected CE - Random CE')
        axes[1].set_xlabel('Random AUC - selected AUC (pp)')
        fig.suptitle(f'{ds}  |  Does utility change beyond accuracy?',x=.07,ha='left',fontsize=15,fontweight='bold')
        fig.legend(handles=handles[1:4],loc='upper center',bbox_to_anchor=(.55,.94),ncol=3,frameon=False)
        fig.text(.07,.025,'GCN selection source; 10 paired seeds; pointwise 95% t intervals. Positive values indicate worse utility.\nCE and classification AUC are task metrics, not output distances or privacy measurements.',fontsize=9,color='#526572')
        fig.subplots_adjust(left=.15,right=.97,top=.83,bottom=.14,wspace=.18)
        name=f'{ds.lower()}_q2_metrics'
        for ext in ['png','pdf']:fig.savefig(OUT/f'{name}.{ext}',dpi=170,facecolor='white')
        plt.close(fig);figures.append(name)

    examples = seed.query("source == 'GCN' and selector == 'r_point' and method == 'GIF'").groupby('dataset')[['delta_U','flip','delta_flip','delta_CE','delta_AUC_loss']].mean().reindex(DATASETS).reset_index()
    inventory = '''| 指标 | 已有数据 / 可直接分析 | 建议位置与作用 |
|---|---|---|
| 删除前与删除后 accuracy、同请求 Retrain accuracy | 六 GU、三数据集、十 seed；当前 f1 字段与 accuracy 数值相同 | Q2 主图原值端点：展示实际性能水平及方法起点 |
| 总损失 U、相对 Random 额外损失 ΔU、效用 gap G | 已有配对量；无需新训练 | 主图重点突出 ΔU；原值端点间距表达 G，分解表解释 U |
| GU–Retrain 预测不一致率、相对 Random 的增量 | 六 GU 全覆盖 | Q2 主图另一面板，检验准确率较稳时行为是否仍改变 |
| 测试交叉熵 CE、分类 macro OvR AUC | GU 和 Retrain 均已记录；原始 metrics 未保存对应删除前 CE/AUC | 配套图检查置信度与类别排序变化；可比较 Random、定向请求和 Retrain，不编造 before |
| 1/2/3/>3 hop 的分歧率及分母 | 六 GU 全覆盖，但个别 hop 层为空 | 附属分析：偏离集中在何处；空层不记为零，选点改变了分层成员，不直接解释为因果传播 |
| update-detection AUC | 保存数值及状态，详见覆盖表 | 附录诊断：根据前后概率变化区分 selected nodes 与测试节点；不是通用 MIA 或遗忘成功率 |
| GU/初始模型、Retrain/初始模型的预测分歧；概率或 logit 距离 | 本轮回传的 metrics.json 中未直接记录 | 需要另查持久化预测及节点/评估图匹配后补算；不能由现有 GU–Retrain 分歧反推 |
'''
    md = f'''# 问题 2：同时展示效用变化与重训行为偏离

2026-10-18 · 图表方案与已有指标核对 · EXP-079/e79r5 · 不新增 GPU 实验

**建议保留三个主要问题：选点能否影响 Retrain → GU 如何响应同一请求 → 响应能否跨选点模型保留。问题 2 用效用原值、相对 Random 的增量和预测行为三部分展开，附属实验检查预算、选点近似、更多效用指标与空间分布。** 框架让这些发现可以在统一请求和参照下比较；各项 insight 不必服从同一个机制解释。

当前 OB 结果章采用另一套 Q 编号（响应量、GU 区分、跨来源），与汇报的三个问题不同。此处 Q2 专指汇报的“GU 怎样改变删除的影响”；正式成稿时应统一编号，将 GU 间差异放入这个问题下。

**新增：[围绕 Retrain 和同一 selector 跨 GU 的三张叙事图](STORIES.html)。** 该页将完整指标图组织为三条可讨论的发现，并保留反例和配对区间。

**方法审计更新：[GraphRevoker 原论文与执行链核对](METHOD_AUDIT.html)。当前 GraphRevoker 是 GPA + optimal 配置版，未接入论文的 contrastive 聚合模块；其数值保留为诊断，不用于完整原方法的优劣结论。** [Before 来源核验](BEFORE_AUDIT.html)确认本批 Cora 未误取单 shard，但不能替代方法实现审查。

## 1. 哪些指标已有，哪些仍需要补算？

{inventory}

{table(coverage)}

覆盖表中的计数为输出条件数，不能当成独立样本量。Retrain 没有 before 或 update-detection 值时保留缺失。当前 f1 字段实际为单标签测试 accuracy，与 micro-F1 数值相同，不应重复列成两种独立指标。分类 AUC 与 update-detection AUC 回答不同问题，图注必须写全称。

## 2. 主图方案：原值与差值放在同一张组合图

每个数据集一张三面板图，行顺序固定为六种 GU，颜色固定为 Random、Degree、R-point、D-full。Q2 暂固定 GCN 选点，避免同时混入四个 surrogate；跨来源保留给 Q3。EXP-011 的 IM、PageRank 等完整策略仍保留为独立覆盖实验，不能把 EXP-079 称作十 seed 的全部策略比较。

- **左图：实际准确率。** 实心点是 GU，空心菱形是同请求 Retrain，同色线连接配对端点；短虚线是各 GU 自身删除前的均值。Random 本身也有自己的 Retrain 端点，不能用定向请求的 Retrain 替代。线段只表示效用差，不表示时间轨迹。
- **中图：相对 Random 的额外损失。** 以同训练 seed 的 Random 均值作配对差后再计算区间。正值表示额外降低准确率，负值表示改善。保留 Degree，避免只与弱参照比较。
- **右图：预测不一致率原值。** Random 与定向请求在同一坐标系出现，便于直接看绝对偏离及增量。它比较 GU 与同请求 Retrain，不能读成遗忘前后翻转。

原值图回答“最后模型有多好”，差值图回答“策略额外改变多少”。无需在正文同时堆 U、ΔU、G、ΔG 四张大图；这些量有代数关系，分解放在一张小表或典型案例中即可。

'''
    for ds in DATASETS:
        md += f'### {ds}\n\n![{ds} 效用原值、相对 Random 增量与预测分歧]({ds.lower()}_q2_overview.png)\n\n[矢量 PDF]({ds.lower()}_q2_overview.pdf)。端点区间是各自十 seed 的区间，中图是先配对作差后的区间；不能从左图区间重叠判定配对差异。左图各数据集横轴不同，且不一定从零开始，跨图比较需读数。\n\n'
    md += f'''## 3. 更多指标如何帮助解释，而不是增加指标数量？

CE 对预测置信度敏感，分类 AUC 描述类别分数的排序；二者能检查 accuracy 未变化时是否仍有任务效用变化。它们不是 GU–Retrain 输出距离，也不是新增独立实验。下面保留全部 GU、两个选择器和 Degree 的对照，不只挑改善论点的格子。三数据集分别作图，指标尺度不同，不混成一个分数。

GIF / GCN / R-point 的例子如下。ΔU 和 ΔAUC_loss 为 pp，flip 为 %，Δflip 为 pp，CE 为原单位；均为十训练 seed 的均值，区间见完整 CSV。

{table(examples)}

这些方向应共同解释：准确率、CE、AUC 和预测分歧可以给出不同结果，不能在看到数值后把最有利的指标换成唯一主指标。正文优先保留“效用与行为是否一致”的问题，CE/AUC 作为检验该观察的补充。

'''
    for ds in DATASETS:
        md += f'![{ds} 交叉熵与分类 AUC 的配对变化]({ds.lower()}_q2_metrics.png)\n\n'
    md += '''## 4. 实验部分的落位

| 主问题 | 主体证据 | 附属分析 |
|---|---|---|
| Q1 选点依据能否预测删除后的 Retrain 变化？ | 真实 Retrain 的策略比较；保留 Random 和结构基线 | IF 近似、删除预算、选集重合；各自标清实验批次 |
| Q2 同一请求经过 GU 后，效用与行为怎样改变？ | 上述原值 + ΔU + GU–Retrain 分歧；全 GU 与数据集反例 | CE/AUC、hop 分布、局部 GU 差异；update-detection 单独限定解释 |
| Q3 换模型选点后，哪些响应仍保留？ | 十 seed 的强度、行为与 GU 相对关系 | 去除单一 GU 的敏感性、重复选集与方向反转 |

图形形式已可用于讨论，最终排版仍需缩减：正文可选一张紧凑概览配代表案例，其余完整面板放附录。不要将本页六张审阅图全部塞进正文，也不靠增加指标数量凑页数。现有数据具备把 Q2 写得更充分的基础。

## 5. 数据和复核

- [逐条件原值与配对量](metrics_cells.csv)、[逐训练 seed 数据](metrics_seed.csv)、[完整均值及区间](metrics_summary.csv)、[hop 分母与分歧](hop_summary.csv)、[指标覆盖](metric_coverage.csv)。完整 CSV 保留四个选点模型，图中固定 GCN。
- [复现脚本](build_report.py)、[核验记录](validation.json)、[返回汇报](../REPORT.html)。
- 本轮重新核验 run manifest 哈希及 2,520 份 metrics.json 哈希，并与现有 cells.csv 的端点、gap、分歧逐条比对。按 baseline output 身份绑定同请求 Retrain，未重新读取 selection.json 或逐节点预测。
- 每个训练 seed 内先平均三次 Random 请求；十个训练 seed 为重复单位。误差线为探索性点态 95% t 区间，未作全矩阵多重检验；GIF/IDEA 不作为独立复现。原图评估、固定 split、10% 预算，不外推其他部署图和预算。
- 本页为写作与图表候选，不改变既有科学接受状态，也未启动或重跑实验。
'''
    (OUT/'REPORT.md').write_text(md, encoding='utf-8')
    body=MarkdownIt('commonmark', {'html':False}).enable('table').render(md)
    body=re.sub(r'src="([^"]+\.png)"', lambda m:'src="data:image/png;base64,'+base64.b64encode((OUT/m[1]).read_bytes()).decode()+'"',body)
    style='body{margin:0;background:#f1f5f5;color:#243947;font:16px/1.85 "Microsoft YaHei",sans-serif}main{max-width:1200px;margin:auto;padding:40px;background:white}h1{font-size:30px}h2{margin-top:45px;border-top:1px solid #d8e3e6;padding-top:20px}img{width:100%;height:auto}a{color:#157c7c}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;border-bottom:1px solid #dce5e8;padding:9px}th{background:#edf5f4}code{overflow-wrap:anywhere}@media(max-width:750px){main{padding:20px}table{display:block;overflow-x:auto}}'
    page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Q2 指标与图表方案</title><style>'+style+'</style></head><body><main>'+body+'</main></body></html>'
    (OUT/'REPORT.html').write_text(page, encoding='utf-8')
    validation=dict(execution_sha=run['commit'],run_sha256=sha(RUN/'run.json'),verified_metrics=2520,paired_GU_cells=2160,training_seeds=10,figure_count=len(figures),raw_csv_endpoint_agreement=True,method_specific_before_constant=True,matched_retrain_output_verified=True,scientific_acceptance='not_requested',new_gpu_runs=0,metric_implementation_sha256=hashlib.sha256(code).hexdigest(),input_csv_sha256=sha(DATA/'cells.csv'),source_sha256=sha(OUT/'REPORT.md'),figures={n:sha(OUT/(n+'.png')) for n in figures})
    validation['output_csv_sha256'] = {n:sha(OUT/n) for n in ['metrics_cells.csv','metrics_seed.csv','metrics_summary.csv','hop_summary.csv','metric_coverage.csv']}
    (OUT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)',md):
        assert (OUT/target.split('#')[0]).exists(), target
    assert page.count('data:image/png;base64,') == 6
    print(table(examples))
    print(json.dumps(validation, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
