"""Render the current figure atlas and evidence-bound narrative from CSV outputs."""
import base64
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from markdown_it import MarkdownIt

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
DATASETS = ['PubMed','Cora','CiteSeer']
METHODS = ['Retrain','GNNDelete','GIF','MEGU','GraphEraser','GraphRevoker']
LABELS = {'random':'Random','degree':'Degree','r_point':'R-point','gt_full':'D-full',
          'pagerank':'PageRank','rr_4096':'IM 4k','rr_16384':'IM 16k','rr_65536':'IM 65k'}


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def table(df):
    def fmt(x): return f'{x:.3f}' if isinstance(x,(float,np.floating)) else str(x)
    return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))
def fig(name,title):
    return f'![{title}]({name}.png)\n\n[PNG]({name}.png) · [PDF]({name}.pdf) · [SVG]({name}.svg)\n'


CSS = '''
:root{color-scheme:light;--ink:#253c49;--muted:#61747b;--line:#dbe4e5;--teal:#176f73}
*{box-sizing:border-box}body{margin:0;background:#eef2f1;color:var(--ink);font:16px/1.8 "Segoe UI","Microsoft YaHei",sans-serif}
header{background:#163c46;color:#fff;padding:18px max(24px,calc((100% - 1260px)/2));display:flex;gap:24px;flex-wrap:wrap}
header a{color:#d7ede7}main{max-width:1360px;margin:24px auto 60px;background:#fff;padding:36px 42px;border-radius:8px}
h1{font-size:32px;line-height:1.4;margin-top:0}h2{margin:40px 0 18px;border-top:1px solid var(--line);padding-top:24px;font-size:25px}h3{font-size:20px;margin-top:30px}
p{margin:14px 0}a{color:var(--teal);text-underline-offset:3px}strong{color:#145d61}img{width:100%;height:auto;display:block;margin:18px 0;border:1px solid #edf0f2}
.scroll{overflow-x:auto}table{border-collapse:collapse;min-width:600px;width:100%;font-size:14px;margin:18px 0}th,td{border:1px solid var(--line);padding:9px 11px;text-align:left}th{background:#244b56;color:white}tr:nth-child(even){background:#f4f8f7}
code{overflow-wrap:anywhere;background:#f0f4f4;padding:2px 5px;font-size:.9em}blockquote{margin:20px 0;background:#edf6f2;border-left:4px solid #3d8b80;padding:14px 20px}li{margin-bottom:7px}
.status{font-size:13px;color:var(--muted);margin:20px 0} @media(max-width:760px){main{margin:10px;padding:20px 16px}h1{font-size:25px}h2{font-size:22px}header{padding:14px 16px;gap:10px;font-size:14px}img{min-width:0}body{font-size:15px}}
@media print{header{display:none}main{padding:0;margin:0}img,tr{break-inside:avoid}}
'''


def render(name,md):
    (OUT/f'{name}.md').write_text(md,encoding='utf-8')
    body=MarkdownIt('commonmark',{'html':True}).enable('table').render(md)
    body=body.replace('<table>','<div class="scroll"><table>').replace('</table>','</table></div>')
    for image in set(re.findall(r'<img src="([^"]+)"',body)):
        p=OUT/image
        body=body.replace(f'src="{image}"',f'src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}" loading="lazy"')
    title=md.splitlines()[0].lstrip('# ')
    html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>'+CSS+'</style></head><body><header><b>OPENGU · 300 轮新协议</b><a href="REPORT.html">结论与重点图</a><a href="EXP011_REPORT.html">011 完整图册</a><a href="EXP079_REPORT.html">079 完整图册</a><a href="'+name+'.md">Markdown</a></header><main>'+body+'</main></body></html>'
    (OUT/f'{name}.html').write_text(html,encoding='utf-8')


def main():
    audit=json.loads((OUT/'input_audit.json').read_text(encoding='utf-8'))
    summary=pd.read_csv(OUT/'summary.csv');effects=pd.read_csv(OUT/'paired_vs_random.csv')
    old=pd.read_csv(OUT/'historical_summary.csv');change=pd.read_csv(OUT/'protocol_change_paired.csv')
    margins=pd.read_csv(OUT/'response_consistency_margin.csv')
    def effect(exp,ds,method,selector,metric='after'):
        r=effects[(effects.experiment==exp)&(effects.dataset==ds)&(effects.method==method)&(effects.selector==selector)&(effects.metric==metric)&effects.source.isin(['GCN','baseline'])].iloc[0]
        return f'{r["mean"]:+.3f} [{r.lo:+.3f}, {r.hi:+.3f}]'
    pub=summary[(summary.experiment=='EXP-079')&(summary.dataset=='PubMed')&(summary.metric=='after')&summary.source.isin(['GCN','baseline'])]
    pubtable=pub.pivot(index='method',columns='selector',values='mean').reindex(METHODS)[list(LABELS)[:4]].rename(columns=LABELS).reset_index()
    pubtable.loc[pubtable.method=='GIF','method']='GIF / IDEA'
    contrasts=pd.DataFrame([{'数据集':d,'方法':m,'请求':LABELS[s],'准确率相对 Random（pp，95% CI）':effect('EXP-079',d,m,s)}
        for d in DATASETS for m in ['GraphEraser','GraphRevoker'] for s in ['r_point','gt_full']])
    geometry=margins[(margins.metric=='U')&(margins['mode']=='centered')&margins.coordinates.isin(['dedup5','drop_GNNDelete'])][['dataset','coordinates','margin_cv2','lo','hi']]
    geometry=geometry.rename(columns={'dataset':'数据集','coordinates':'GU 维度','margin_cv2':'跨来源模式 margin（pp²）','lo':'95%下限','hi':'95%上限'})
    shifts=[]
    for ds in DATASETS:
        for m in ['GraphEraser','GraphRevoker']:
            row={'数据集':ds,'方法':m}
            for s in ['random','r_point','gt_full']:
                r=change[(change.experiment=='EXP-079')&(change.dataset==ds)&(change.method==m)&(change.selector==s)&(change.metric=='after')].iloc[0]
                row[LABELS[s]+' 新−旧（pp）']=r['mean']
            shifts.append(row)
    report='''# 两张主表的新结果：先看原值，再看请求响应

2026-10-23 · EXP-011/e11r1 与 EXP-079/e79r6 · 新损失 / shard_epochs=300 · 分析已生成，等待科学验收

**你选的这张 PubMed 原始准确率图已用 e79r6 重做。主要观察保留：R-point 和 D-full 在两种分片方法上都低于 Random；不同 GU 的响应方向与幅度仍然不同。** 这组规律不能外推为每个数据集上的普遍攻击：CiteSeer 的 GraphEraser 在这两类请求下反而高于 Random。

本轮共重建 **32 组图，每组提供 PNG、PDF、SVG（96 个图文件）**：两张表的三数据集原始准确率、CE、分类 AUC；Random 配对差值、GU–Retrain 差值与预测分歧；新旧分片协议对照；079 十 seed 的跨选点模型响应与敏感性分析。

## 重点图：PubMed，四种请求与同请求 Retrain

'''+fig('e79r6_pubmed_accuracy','EXP-079 e79r6 PubMed 原始准确率')+'''
这张图适合放在分析的前面，因为它直接回答三个问题：模型本身表现怎样、换请求之后改变多少、与同请求 Retrain 相差多少。实心圆为 GU，空心菱形为同请求 Retrain，虚线为该 GU 自己的 Before 均值。横轴是独立请求条件，不是连续删除过程。

PubMed 原始准确率均值（%）：

'''+table(pubtable)+'''

GraphEraser 从 Random 的 87.051% 降至 R-point 的 86.083%、D-full 的 86.476%；GraphRevoker 从 86.429% 降至 85.114%、85.614%。GIF/IDEA 也呈下降，GNNDelete 的 R-point 则高于 Random。**因此要保留完整方法面板，不能把方向不同的响应压成一个统一排名。**

## Q1 / Q2：下降是否超出同 seed 的 Random 波动

以下是 Selected − Random 的准确率变化，负值表示准确率降低。先在训练 seed 内平均 Random 重复，再逐 seed 配对相减；区间为点态 95% t 区间，未做全表多重比较校正。

'''+table(contrasts)+'''

**PubMed 的四项分片对照区间均低于零；CiteSeer 的 GraphEraser 两项均高于零；Cora 两种分片方法的 R-point / D-full 区间均跨零。** 这支持有条件的请求响应，不支持普遍伤害。区间跨零也不是等效或“没有影响”的证明。

准确率只是效用的一面。完整图册同时给出测试 CE 与分类 macro OvR AUC，后者不是隐私攻击 AUC。GU–Retrain 预测分歧是同请求的预测差异，不能单独证明遗忘成功或失败。

## EXP-011：把 IM 和 PageRank 补回同一视图

'''+fig('e11r1_pubmed_accuracy','EXP-011 e11r1 PubMed 八类请求')+f'''
011 展示八类请求，覆盖 R-point、D-full、Degree、PageRank、三种 IM/RR 预算及 Random。PubMed 下 GraphEraser / R-point 相对 Random 为 **{effect('EXP-011','PubMed','GraphEraser','r_point')} pp**；GraphRevoker / R-point 为 **{effect('EXP-011','PubMed','GraphRevoker','r_point')} pp**。三种 IM 在两种分片方法上的这些 PubMed 区间均跨零，而 GNNDelete 的 IM 响应明显不同，具体量级见[011 图册](EXP011_REPORT.html)。

**011 只有三个训练 seed。** Random 的十次选点、IM 的三次选点先在每个训练 seed 内平均；误差线使用 n=3，而不是把 30 次 Random 或 9 次 IM 当作独立训练 seed。固定 split 下的训练 seed 区间不覆盖重新划分数据带来的不确定性。011 和 079 的公共条件有重叠，不合并成 13 个独立训练 seed，也不累计为独立科学样本。

## Q3：跨选点模型的响应模式重新计算

复用此前审阅的 response_pattern.py 统计函数，但输入仅来自当前 e79r6；没有复用旧报告结论。GIF/IDEA 在推断几何中只计一个坐标，同时保留六方法敏感性版本。

'''+table(geometry)+'''

这里的正 margin 表示“不同策略、不同选点模型之间的距离”大于“同策略、不同选点模型之间的距离”；单位是 pp²，区间是十个训练 seed 的近似 jackknife 区间。

**Cora 的模式区分仍主要由 GNNDelete 驱动：保留五个独立 GU 坐标时区间为正，去掉 GNNDelete 后跨零。CiteSeer 不支持稳定的整体区分；PubMed 五坐标整体区间也跨零。** PubMed 去掉 GNNDelete 后的正区间属于敏感性结果，不能事后挑选它来宣布全方法普遍迁移。跨来源、逐方法的对照与 Holm 校正结果均保留在 CSV 中。

'''+fig('response_margin_sensitivity_10seeds','EXP-079 e79r6 跨来源响应模式敏感性')+'''
## 和旧图相比，真正变化在哪里

已按数据集、训练 seed、请求与 Selection 身份逐格对齐新旧结果。**非分片方法及 Retrain 的 Output 身份、准确率、CE、AUC、Before、重训差值与分歧值均保持一致（数值容差 1e-8）。** 新变化集中于两个分片方法；下表只列 079 的新−旧原始准确率均值变化。

'''+table(pd.DataFrame(shifts))+'''

这次同时改变了损失实现和 shard_epochs；此对照是协议变化前后的描述，不能归因成“只把轮数减至300就导致某个准确率变化”。旧 Result、旧分析图和原有科学决定保持原样。新图的 Before 也读取新 run，未沿用旧分片 Before。

GraphRevoker 仍是本项目 YAML 声明的 GPA + optimal 实现，本轮没有把它变成论文完整对比聚合实现。它保留独立纵轴，前五个面板共享纵轴；跨面板量级比较要读刻度或 CSV。GIF 与 IDEA 的准确率坐标相同，CE 最大差约 1.01e-8、分类 AUC 最大差约 0.00071 pp，合并面板不等于算法等价。误差线是均值区间，不能直接当作稳定性或方差比较。

## 完整图册与复算入口

- [EXP-011 全部图与数据说明](EXP011_REPORT.html) · [MD](EXP011_REPORT.md)
- [EXP-079 全部图与响应分析](EXP079_REPORT.html) · [MD](EXP079_REPORT.md)
- [逐 cell 数据](cells.csv) · [按训练 seed 汇总](seed_values.csv) · [均值、SD 与区间](summary.csv)
- [逐 seed Random 配对差值](paired_seed_values.csv) · [配对区间](paired_vs_random.csv)
- [新旧逐格对照](old_new_matched_cells.csv) · [新旧配对差值](protocol_change_paired.csv)
- [输入与身份核验](input_audit.json) · [生成器](rebuild.py) · [报告生成器](report.py) · [图册验证](validation.json)

## 证据范围与状态

当前输入为 011 的 1,449 格 / 1,242 个 GU–Retrain 配对，以及 079 的 2,520 格 / 2,160 个配对。重新核对两次可信 delivery、项目检查、可信索引、全部 7,940 个当前文件的 SHA-256；对历史参照另外核对 7,940 个文件及配对身份。图中没有使用未回传的模型或本地重新运行结果。

执行 SHA：`bab1781e182254e0b02cbeb1de138d58f7f1cd50`。图册生成与科学接受分开：本轮完成可复算的描述性分析，尚未把它写成用户已经接受的新论文结论。

复现：用带 numpy、pandas、scipy、matplotlib、markdown-it-py 的 Python 先运行 `rebuild.py`，再运行 `report.py`。全流程只读本地可信结果，不启动 GPU、不修改远端缓存。
'''
    render('REPORT',report)
    for exp,rid,n in [('EXP-011','e11r1',3),('EXP-079','e79r6',10)]:
        name='EXP011_REPORT' if n==3 else 'EXP079_REPORT'
        md=f'# {exp} / {rid}：完整分析图册\n\n2026-10-23 · {n} 个训练 seed · 新损失 / shard_epochs=300 · [重点结论](REPORT.html)\n\n'
        md+='所有图绑定本次可信 run；每个训练 seed 内先平均选点重复。误差线为训练 seed 均值的点态 95% t 区间。详细限定、方法实现范围和新旧比较见重点报告。\n\n'
        if n==3:
            md+='011 有 1,449 个输出条件，Random 每训练 seed 十次选点，IM 每训练 seed 三次选点；统计样本量始终是三个训练 seed。IM 4k/16k/65k 分别是 4096/16384/65536 RR 采样数，不是删除节点数。\n\n'
        else:
            md+='079 有 2,520 个输出条件。原值与对照图固定 GCN 选点来源，并保留 Random、Degree；后面的响应模式图覆盖 GCN、SGC、GAT、GIN 四种选点模型。Random 每训练 seed 三次选点，推断样本量为十个训练 seed。\n\n'
        for ds in DATASETS:
            md+=f'## {ds}：原始效用与请求对照\n\n'
            if ds=='PubMed':
                md+='先看原始准确率，再区分相对 Random 的额外损伤、相对同请求 Retrain 的差距。R-point 对分片方法的效用下降最值得检查；不同方法方向并不一致。\n\n'
            elif ds=='CiteSeer':
                md+='这是不能忽略的反例：GraphEraser 在 R-point / D-full 下的准确率没有呈现 PubMed 的下降方向；完整均值和配对区间见 CSV。\n\n'
            else:
                md+='GNNDelete 的大幅变化和 GraphRevoker 自身的较低 Before 需要分开理解。避免把不同 Before 或不同纵轴下的原始准确率直接压成算法优劣排名。\n\n'
            for metric,label in [('accuracy','准确率原值'),('ce','测试交叉熵原值'),('auc','分类 macro OvR AUC 原值'),('contrasts','Random 对照、重训差距与预测分歧')]:
                md+=f'### {label}\n\n'+fig(f'{rid}_{ds.lower()}_{metric}',f'{exp} {ds} {label}')+'\n'
        md+='## 新旧分片协议对照\n\n'+fig(rid+'_protocol_comparison',exp+' 新旧分片结果')+'\n'
        if n==10:
            md+='## 跨选点模型响应与敏感性\n\n所有图重新从 e79r6 的十 seed 结果计算。此处 U=Before−After，G=Retrain−GU；均值区间、模式距离、Holm 检验和去掉某个 GU 的敏感性属于不同统计问题。主报告已解释目前能支持的有条件结论。\n\n'
            for file,title in [('response_atlas_U_G_10seeds','U / G 全条件图谱'),('response_profiles_U_10seeds','跨选点模型的绝对效用响应'),('response_selectivity_U_10seeds','相对其他 GU 的请求选择性'),('response_distance_matrix_U_10seeds','中心化响应距离'),('response_margin_sensitivity_10seeds','跨来源模式的 GU 敏感性'),('response_disagreement_10seeds','与同请求 Retrain 的预测分歧')]:
                md+=f'### {title}\n\n'+fig(file,title)+'\n'
            md+='[响应摘要](response_profile_summary.csv) · [选择性与 Holm 校正](response_selectivity.csv) · [方法间交互](response_GU_pair_interactions.csv) · [跨来源保持](response_interaction_preservation.csv) · [模式 margin](response_consistency_margin.csv) · [复用统计函数的身份绑定](response_generator_binding.json)。\n\n'
        md+='## 数据与验证\n\n[逐 cell 数据](cells.csv) · [逐 seed 数据](seed_values.csv) · [摘要](summary.csv) · [配对区间](paired_vs_random.csv) · [输入核验](input_audit.json) · [图册验证](validation.json)。\n'
        render(name,md)
    # Verify links and render parity from the same Markdown source.
    links=[]
    for p in OUT.glob('*REPORT.md'):
        md=p.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)',md):
            if link=='validation.json':continue
            assert (OUT/link).exists(),(p.name,link)
            links.append(link)
        html=(p.with_suffix('.html')).read_text(encoding='utf-8')
        assert len(re.findall(r'^## ',md,re.M))==html.count('<h2>')
        assert len(re.findall(r'!\[',md))==html.count('<img ')
    figures=sorted(p.stem for p in OUT.glob('*.pdf'))
    assert len(figures)==32
    assert all((OUT/(name+'.'+ext)).exists() for name in figures for ext in ['png','svg'])
    proof=dict(status='passed',figures=len(figures),figure_exports=3*len(figures),local_links_checked=len(links),
        report_sources={p.name:sha(p) for p in OUT.glob('*REPORT.md')},
        outputs={p.name:sha(p) for p in OUT.iterdir() if p.suffix in ['.csv','.png','.pdf','.svg']},
        input_audit_sha256=sha(OUT/'input_audit.json'),same_markdown_render=True,scientific_acceptance='not_requested')
    (OUT/'validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in proof.items() if k!='outputs'},ensure_ascii=False))


if __name__=='__main__':main()
