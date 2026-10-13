"""Render the editable Markdown and self-contained HTML from audited statistics."""
import base64
import json
from pathlib import Path
import re
import numpy as np
import pandas as pd
from markdown_it import MarkdownIt

OUT=Path(__file__).resolve().parent

def table(df):
    def fmt(v):
        if isinstance(v,(float,np.floating)):return f'{v:.3f}' if np.isfinite(v) else 'NA'
        return str(v)
    return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(map(fmt,row))+' |' for row in df.itertuples(index=False,name=None))

def build_report():
    s=pd.read_csv(OUT/'summary.csv');a=pd.read_csv(OUT/'paired_seed_values.csv');c=pd.read_csv(OUT/'correlations.csv')
    o=pd.read_csv(OUT/'selection_overlap.csv');w=pd.read_csv(OUT/'within_source_overlap.csv')
    audit=json.loads((OUT/'audit.json').read_text(encoding='utf-8'))
    focus=s.query("dataset=='Cora' and method=='GNNDelete' and selector=='gt_full' and source=='GIN'")
    rows=[]
    for cohort in ['old3','new7','all10']:
        z=focus[focus.cohort==cohort].iloc[0]
        rows.append({'seed组':cohort,'GIN drop':z.U_mean,'GCN drop':z.U_mean-z.U_vs_direct_mean,
                     'Random drop':z.U_mean-z.U_vs_random_mean,'Degree drop':z.U_mean-z.U_vs_degree_mean,
                     'GIN−Random 95% CI':f'{z.U_vs_random_mean:.2f} [{z.U_vs_random_lo:.2f}, {z.U_vs_random_hi:.2f}]',
                     'GIN−Degree 95% CI':f'{z.U_vs_degree_mean:.2f} [{z.U_vs_degree_lo:.2f}, {z.U_vs_degree_hi:.2f}]'})
    core=focus[focus.cohort=='all10'].iloc[0]
    cor=c[c.source=='GIN'].pivot(index=['dataset','selector'],columns='cohort',values='rho').reset_index()
    cor=cor.merge(c.query("source=='GIN' and cohort=='all10'")[['dataset','selector','rho_random','rho_degree','bootstrap_lo','bootstrap_hi']],on=['dataset','selector'])
    cross=o.query("cohort=='all10'").pivot(index=['dataset','selector'],columns='source',values='mean').reset_index()
    cross=cross.merge(w.query("cohort=='all10' and source=='GCN'")[['dataset','selector','mean']].rename(columns={'mean':'GCN自身跨seed'}),on=['dataset','selector'])
    full=s.query("cohort=='all10' and source=='GIN'").copy()
    full['drop±SD']=full.apply(lambda r:f'{r.U_mean:.2f} ± {r.U_sd:.2f}',axis=1)
    for ref in ['direct','random','degree']:
        full['对'+ref+'差与CI']=full.apply(lambda r:f'{r["U_vs_"+ref+"_mean"]:.2f} [{r["U_vs_"+ref+"_lo"]:.2f}, {r["U_vs_"+ref+"_hi"]:.2f}]',axis=1)
    counts=[]
    for cohort in ['new7','all10']:
        for src,g in s[(s.cohort==cohort)&(s.source!='GCN')].groupby('source'):
            counts.append({'组':cohort,'source':src,'条件数':len(g),'均值胜Random':int((g.U_vs_random_mean>0).sum()),'Random区间下界>0':int((g.U_vs_random_lo>0).sum()),'均值胜Degree':int((g.U_vs_degree_mean>0).sum()),'Degree区间下界>0':int((g.U_vs_degree_lo>0).sum())})
    architecture=s.query("cohort=='all10' and method=='GNNDelete' and selector=='gt_full'").pivot(index='dataset',columns='source',values='U_mean').reset_index()
    baseline=a.query("source=='GCN' and method=='GNNDelete' and selector=='gt_full'").groupby('dataset')[['U_random','U_degree']].mean().reset_index()
    architecture=architecture.merge(baseline,on='dataset')
    cache=pd.DataFrame([{'层':k,**v} for k,v in audit['cache_counts'].items()]).fillna(0)
    for k in cache.columns[1:]:cache[k]=cache[k].astype(int)
    md=f'''# EXP-079：十 seed 条件性迁移结果分析

2026-10-14 · e79r5 · 完整 2520 格 · 分析完成，科学结论待用户审阅

## 结论

**新增七个 seed 复现了 Cora / GNNDelete / gt_full 的 GIN 攻击正例，支持条件性迁移；其余条件存在明显失败和关系变化，不能升级为通用代理替代结论。** 本轮原 3 seed、新增 7 seed、合计 10 seed 分开统计，没有按结果删 seed 或只挑有利方法。

- 核心正例：十 seed 的 GIN 平均 F1 drop 为 **{core.U_mean:.2f} pp**，GCN direct 为 **{core.U_mean-core.U_vs_direct_mean:.2f} pp**，Random 为 **{core.U_mean-core.U_vs_random_mean:.2f} pp**，Degree 为 **{core.U_mean-core.U_vs_degree_mean:.2f} pp**。GIN−Random 的配对差为 **{core.U_vs_random_mean:.2f} pp，95% CI [{core.U_vs_random_lo:.2f}, {core.U_vs_random_hi:.2f}]**。新增七 seed 全部高于 Random，十 seed 为 10/10。
- Degree 优势比原探索更清晰，但有限：十 seed GIN−Degree 为 **{core.U_vs_degree_mean:.2f} pp [{core.U_vs_degree_lo:.2f}, {core.U_vs_degree_hi:.2f}]**，7/10 seed 为正；新增七 seed 为 5/7。这里是未经多重比较调整的点态区间，不称全矩阵确认性显著优势。
- 迁移幅度仍有不确定性：GIN−direct 为 **{core.U_vs_direct_mean:.2f} pp [{core.U_vs_direct_lo:.2f}, {core.U_vs_direct_hi:.2f}]**，逐 seed 配对 MAE **{core.paired_MAE_direct:.2f} pp**。均值接近、区间跨零都不证明统计等效。
- 明确反例：Cora / GNNDelete / r_point 的 GIN drop 仅 9.52 pp，比 direct 少 4.19 pp、比 Random 少 3.39 pp；新增七 seed 无一胜 Random。PubMed / GNNDelete / gt_full 的 GIN−Random 为 −0.66 pp，十 seed 全部为负。
- 不能一概优选 GIN：PubMed / GNNDelete / gt_full 的 SGC drop 为 **8.03 pp**，高于 GCN 的 1.79、GIN 的 1.59、Random 的 2.25。新增七 seed 中 SGC−Random 为 **4.74 pp [3.38, 6.11]**，也保持正向优势。更强的损伤与更忠实地匹配 direct 响应是不同目标。
- 相关性的旧结论需要收窄：Cora / r_point 的 GIN 跨 GU 排序相关从原三 seed 的 1.00 降到新增七 seed 的 0.30、合计十 seed 的 0.40；Cora / gt_full 仍为 1.00，但 Random、Degree 也都是 1.00。相关不能独立证明代理选点有价值。

## 1. 证据范围与可信链

主输入：job `{audit['job_id']}`；run `e79r5`；执行 SHA `{audit['execution_sha']}`；配置 `experiments/configs/exp079/surrogate_multiseed.yaml`。

3 个数据集 × 10 个训练 seed × 12 个选点条件 × 7 个方法 = **2520 格**。12 个条件为两种算法×四种选点架构、Degree 和 Random 三次抽样。六种 GU 共 2160 格，Retrain 共 360 格。目标为 GCN；GraphEraser/GraphRevoker 是 GCN shard ensemble，图中 GCN 是 full-graph 参考，不等同于 ensemble 的严格白盒选点。

已消费 SyncMate accepted 回执，重新核对 **5041/5041** 本地文件 SHA-256 与可信索引，逐格检查 Selection、Output、相同 seed/选集的 Retrain 配对、数值有限性和矩阵覆盖。原 EXP-013 的 756 格也重新检查本地哈希，按科学条件对齐后，Selection / Output ID 及 F1 drop、retrain gap 一致；可复用旧证据。旧执行 SHA 为 `{audit['old_run_sha']}`。不同版本生成/消费来源保留在原 run 中，不把缓存结果称为本次全部重新训练。

运行于北京时间 2026-10-13 20:37:32 至 2026-10-14 02:27:31，完整 Runner 作业 **{int(audit['job_seconds'])} 秒（5:49:59）**。这是 r5 本轮耗时，历史失败和 Gate 不计入这一个数；不能把它当成从零完成整个研究的成本。有效范围仅固定 split、预算 0.1 与本次参数配置。

## 2. 统计口径

F1 drop U = 100×(F1_before−F1_after)，正值表示下降；所有差值单位为百分点 pp。G = 100×(F1_retrain−F1_GU)，保留正负号；flip 为相同请求 GU 与 Retrain 在 retained test 节点上的预测不一致比例，**不是相对原模型的翻转率**。

同一训练 seed 内先平均 Random 的三个抽样，再计算 surrogate−direct / Random / Degree；有效训练重复数是 3、7 或 10。均值区间用双侧 t 区间，配对差用逐 seed 差值构造；依赖 seed 重复的模型假设，全部是探索性点态区间。没有事先冻结确认性主对比、等效阈值或多重比较方案，因此本报告不事后制造确认性接受门槛。原始值、SD、配对差、胜出 seed 数和 MAE 均保存。

固定 dataset、算法，先跨 seed 求每个 GU 的均值，再沿 GU 计算 Spearman；GIF/IDEA 的 360 对 U 完全相同，因此相关主表保留 GIF、去掉 IDEA，只比较五种固定 GU。六方法原始表全保留，不能把重复响应计作两个独立证据。相关区间按 seed 整块重采样 2000 次，保持全部 GU 的配对关系；它刻画训练重复不确定性，不将五个 GU 当作随机方法总体。全部 54 项相关的未定义重采样次数为 {int(c.bootstrap_undefined.sum())}。三 seed bootstrap 尤其离散，仅作诊断。

## 3. 原三 seed 的核心正例是否复现

Cora / GNNDelete / gt_full，表内 drop 为均值；差值同时给点态 95% 配对区间。

{table(pd.DataFrame(rows))}

新增七 seed 的正例方向与旧三 seed 一致；其中 Degree 优势的区间也移至零上方。仍需保留 seed 波动：GIN−direct 的均值差有正负抵消，MAE 更大，不能据区间跨零宣布等效。

沿用此前尺度提案，仅作附加诊断：X=direct−Random，Y=GIN−Random，R=mean(Y)/mean(X)。本例 X 的均值为 {core.direct_random_mean:.2f} pp，95% CI [{core.direct_random_lo:.2f}, {core.direct_random_hi:.2f}]；R={core.retention:.3f}，Fieller 区间 [{core.retention_lo:.3f}, {core.retention_hi:.3f}]。它表示均值上的额外损伤保留比例，允许大于 1，不能代替等效检验。其他条件若 X 区间下界不大于零，则标记“参照增益未确立”，不解释比值、不加 epsilon；完整诊断见 summary.csv。这一口径此前仅为草案，未冒充预注册主指标。

## 4. 全范围效果与失败条件

先以 GNNDelete / gt_full 展示四个选点架构的十 seed 平均 drop，避免把 GIN 正例误读成全局最优代理：

{table(architecture[['dataset','GCN','SGC','GAT','GIN','U_random','U_degree']])}

以下两张图覆盖四种选点架构、六 GU、三数据集；每个分面使用自己的纵轴，避免大幅 drop 掩盖小幅变化。原三 seed 灰点，新增七 seed 彩点；菱形为十 seed 均值，误差线为点态 95% 均值区间，虚线为 Random，点线为 Degree。

![gt_full 完整结果](gt_full_drop.png)

![r_point 完整结果](r_point_drop.png)

GIN 的完整配对图把三种参照分开；右侧意味着损伤大于该参照。

![GIN 配对差](gin_contrasts.png)

PubMed / GraphEraser / r_point 的 GIN−Random 为 0.79 pp [0.63, 0.96]、GIN−Degree 为 0.86 pp [0.64, 1.07]，新增七 seed 仍同向且区间在零上方。PubMed / GraphRevoker / r_point 也保留正向的基线优势。它们补充条件性正例，但量级与 Cora / GNNDelete 的 22.38 pp 差异很大。CiteSeer 大多数 GIN 条件 drop 很小或为负；不能将有符号负 drop 称作攻击损伤。

下表只用于全范围扫描：每个 source 有 3×6×2=36 个条件，包含 GIF/IDEA 重复响应，不是独立成功次数；区间计数未经多重比较修正，不作为显著性发现数量。

{table(pd.DataFrame(counts))}

## 5. 跨 GU 响应关系是否稳定

GIN 表如下，完整 SGC/GAT/GIN 的 54 行见 correlations.csv。old3/new7/all10 是不同 seed 组的原始 drop 相关，右侧为十 seed 的简单基线相关和 seed bootstrap 百分位区间。

{table(cor[['dataset','selector','old3','new7','all10','rho_random','rho_degree','bootstrap_lo','bootstrap_hi']])}

稳定的例子是 Cora / gt_full：旧三 seed 与新增七 seed 的 GIN 排序相关均为 1.00。反例是 Cora / r_point：原本 1.00 的关系没有稳定复现。CiteSeer / r_point 的 GAT 从旧三 seed 0.80 变为新增七 seed −0.30，也说明代理架构不能一概替换。PubMed / r_point 的 GIN 从旧三 seed 0.30 升至新增七 seed 1.00，展示旧小样本结果的不稳定。十 seed 的 PubMed / r_point 为 0.90，Random 同为 0.90。

共同减去 Random 的相关另存 CSV，仅用于诊断，因为两侧共享参照项；不能将其解释成攻击特有的因果关系。也不能将“跨 GU 相关”写成“某个固定 GU 内跨攻击条件相关”。

## 6. 选点层：有重叠，但没有相同选集

同 seed surrogate 与 GCN 选集的平均 Jaccard（交集/并集），与 GCN 自身跨 seed 的平均 Jaccard 并列；后者 45 对共享 seed，仅作描述，不能当 45 个独立重复。

{table(cross)}

Cora / gt_full 的 GIN−GCN Jaccard 约 0.240，低于 GCN 自身跨 seed 的 0.524，但攻击正例仍然复现。因此本例的效果迁移不要求选出相同节点；本实验还不足以识别产生同类损伤的机制。SGC 自身选集在 Cora/PubMed 十 seed 下完全相同、CiteSeer 也近乎相同，却与 GCN 重叠很低；这是选集稳定性观察，不等于 SGC 有效性或十份独立选集证据。模型分数未回传，评分排序相关 **NOT OBSERVED**。

## 7. Retrain gap、预测差异与解释边界

Cora / GNNDelete / gt_full / GIN 的平均 U 为 {core.U_mean:.2f} pp，G 为 {core.G_mean:.2f} pp，说明相同选集的 Retrain 仍明显高于 GU 输出；平均预测不一致比例为 {core.flip_mean:.2f}%。这些是效用与近似误差证据，不能改写成隐私泄露成功率。

GraphRevoker 在 Cora 的 GIN / gt_full 平均 drop 为 1.81 pp，signed retrain gap 却有 20.37 pp；小 drop 不等于接近精确 Retrain。两类指标的参照不同，不能混合排名。负 G 表示本次 GU F1 高于对应 Retrain，也不等于遗忘更正确或具有一般保护机制。这里只解释观测量，不把它归因于凸性、某种优化机制或分片保护。完整 G、flip 逐 seed 值及汇总保存在 CSV；update-detection AUC 原值与状态保存在 cells.csv，本轮不据此做 MIA/隐私结论。

## 8. 工程事实与科学证据分开

{table(cache)}

方法 Output 为 2184 HIT、336 MISS；基础 Evaluation 为 756 HIT、1764 MISS。Selection/Score 按逐格访问记录，共享选集会跨 GU 重复，不能把 MISS 行数当独立生产 Artifact 数。方法 producer_called 共 336 格；原始 cache_provenance 保留在 run.json。Gate e79g4/e79g7/e79g8 及超时 r1–r3 等不加入科学样本，不以它们扩大 seed 数。本轮未重新启动 GPU 作业、修改缓存或同步 SSH。

## 9. 建议采用的结论与下一步

建议的论文表述：在固定划分、10% 删除预算和本次 GCN 目标设置下，GIN 代理的 gt_full 选点在 Cora / GNNDelete 上跨新增七个训练 seed 复现了明显效用下降，且相对 Random 保留稳定优势。迁移程度依赖数据集、选点算法和 GU；r_point 等条件存在失败，跨方法相关也可被简单基线复现，因此当前证据支持有边界的条件性迁移。

本轮可以结束“十 seed 矩阵尚未完成”的运行结论，并将当前科学分析送审。科学接受仍由用户决定；没有将 analysis complete 写成 accepted。后续若要提出普遍替代、等效性或跨 split 泛化，需要另行定义目标范围与确认性门槛；本次不据结果自动扩实验或选择最优代理后声称无偏确认。

## 附表：GIN 十 seed 全部条件

{table(full[['dataset','method','selector','drop±SD','对direct差与CI','对random差与CI','对degree差与CI']])}

## 复现与证据文件

- [可编辑报告](REPORT.md) · [自包含 HTML](REPORT.html) · [原始 2520 格表](cells.csv) · [配对 seed 值](paired_seed_values.csv)
- [全部组别统计与尺度诊断](summary.csv) · [相关与 bootstrap](correlations.csv) · [跨架构重叠](selection_overlap.csv) · [自身跨 seed 重叠](within_source_overlap.csv)
- [审核摘要](audit.json) · [分析生成器](analyze.py) · [报告生成器](report.py)
- 原始 run：`results/runs/gpu4090/exp079-surrogate-multiseed/e79r5/run.json`；SHA-256 `{audit['run_sha256']}`。
- 回传与验收：`.syncmate/deliveries/{audit['job_id']}.json`；可信索引：`.syncmate/artifact_index.json`。审计检查只消费本次与明确引用的 EXP-013 文件，未改写运行事实。
- 从仓库根复现：`python -B -X utf8 self/research/analyses/EXP-079/e79r5/analyze.py`。运行需要 numpy、pandas、scipy、matplotlib、markdown-it-py；只重建本分析目录。
'''
    (OUT/'REPORT.md').write_text(md,encoding='utf-8')
    body=MarkdownIt('commonmark',{'html':False}).enable('table').render(md)
    for name in ['gt_full_drop.png','r_point_drop.png','gin_contrasts.png']:
        body=body.replace('src="'+name+'"','src="data:image/png;base64,'+base64.b64encode((OUT/name).read_bytes()).decode()+'"')
    css='body{margin:0;background:#f4f6f8;color:#243342;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif}main{max-width:1300px;margin:auto;padding:40px 32px;background:white}h1{font-size:32px}h2{border-top:1px solid #d5dfe7;padding-top:24px;margin-top:38px;color:#143e63}table{display:block;overflow:auto;border-collapse:collapse;font-size:14px}th,td{border:1px solid #d3dce4;padding:8px 10px}th{background:#eaf1f6}img{width:100%;height:auto}a{color:#17669b}code{overflow-wrap:anywhere}p,li{overflow-wrap:anywhere}strong{color:#174a6e}'
    (OUT/'REPORT.html').write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>EXP-079 十 seed 结果分析</title><style>'+css+'</style></head><body><main>'+body+'</main></body></html>',encoding='utf-8')
    for link in re.findall(r'\]\(([^)]+)\)',md):assert (OUT/link).exists(),link
    assert len(re.findall('data:image/png;base64',body))==3
    print('REPORT.md and self-contained REPORT.html generated; links checked.')

if __name__=='__main__':build_report()
