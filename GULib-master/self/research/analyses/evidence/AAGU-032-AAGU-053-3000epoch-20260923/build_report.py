from pathlib import Path
import json,statistics,csv,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
root=Path('.')
out=root/'self/research/analyses/evidence/AAGU-032-AAGU-053-3000epoch-20260923'
x=json.loads((out/'summary.json').read_text(encoding='utf-8'))
pairs053=list(csv.DictReader((out/'AAGU-053-all-pairs.csv').open(encoding='utf-8-sig')))
def f(v): return f'{v:.3f}'
def stat(m,sd): return f'{f(m)} ± {f(sd)}' if sd is not None else f'{f(m)} ± —'
def delta(m,sd): return f'{m:+.3f} ± {f(sd)}' if sd is not None else f'{m:+.3f} ± —'
def cell(r,prefix):
 return f"{stat(r[prefix+'_old_mean'],r[prefix+'_old_sd'])} → {stat(r[prefix+'_new_mean'],r[prefix+'_new_sd'])}; Δ {delta(r[prefix+'_delta_mean'],r[prefix+'_delta_sd'])} pp"
lines=[]
a=lines.append
a('# AAGU-032 / AAGU-053：100 → 3000 训练轮数结果对照')
a('')
a('日期：2026-09-23　｜　状态：分析已整理，等待科学审阅')
a('')
a('## 范围与核对')
a('')
a('是三套数据集：Cora、CiteSeer、PubMed。AAGU-032 与 AAGU-053 各自都覆盖这三套数据集，因此是每项实验 3 张数据集表，共 6 个数据集切片。')
a('')
a('| 实验 | 条件规模 | 旧参数运行 / SHA | 新参数运行 / SHA | 配置 SHA |')
a('| --- | ---: | --- | --- | --- |')
a('| AAGU-032 | 360（每数据集 120） | aagu032-extend-v2 / 53daf480 | aagu032-recovery-full-20260920 / ee4ea595 | c6032e4d…，旧新一致 |')
a('| AAGU-053 | 96（每数据集 32） | aagu053-table-v1 / 9a366d51 | aagu053-newtraining-full-20260920 / 38ca4e76 | b44d1319…，旧新一致 |')
a('')
a('两个实验的 YAML 配置内容和 SHA 在对应旧、新提交间一致；变化由代码默认值带入：旧提交 training.epochs / --num_epochs 为 100，新提交为 3000。')
a('')
a('对照采用旧分析明细和新运行 manifest 按实验条件配对。AAGU-032 的 360 个旧、新 cell ID 与数据集、seed、预算、selector 均对齐；其中仅 Degree 和 Random 的 72/360 个 selection_id 相同，其他 288 个选择身份变化。AAGU-053 的 48 个选择条件均能按 cell_id 与 selection_id 对齐，旧新选集身份完全相同。')
a('')
a('验证脚本逐项核对了新运行 manifest 中的文件 SHA-256：AAGU-032 为 360 格 × 2 个文件，AAGU-053 为 96 格 × 2 个文件。AAGU-032 的 360 格 method 全部缓存命中、没有 producer 调用；AAGU-053 的 96 格中 24 格由 method producer 计算、72 格命中缓存（GNNDelete 与 Retrain 各 12 格新算、36 格命中）。代码中的训练配对身份包含完整 training 配置，GU 输出身份还绑定基础 checkpoint state hash，因此新运行的缓存身份包含 3000 轮设置；缓存命中只说明复用了该身份下的产物，不代表本次恢复运行重新训练了全部模型。')
a('')
a('## 读表方式与限制')
a('')
a('- 所有 F1 和差值均用百分数 / 百分点（pp）。AAGU-032 的值是 F1-after；每格“旧 → 新”展示三训练 seed 的均值 ± 样本 SD，Δ 是同条件 seed 内先相减后计算的均值 ± 样本 SD。')
a('- AAGU-053 按数据集和 selector 类型汇总选点 seed。GU 是 GNNDelete 的 F1-after，Retrain 是全量重训练的 F1-after，P0−GU 是原模型 F1 与 GU 的差，Retrain−GU 是重训练与 GU 的配对差。Degree 只有 1 个条件，SD 不适用；其余 selector 类型各 3 个选点 seed。')
a('- 这是旧、新完整协议的描述性对照，不是只改变 epoch 的因果实验。AAGU-032 多数 IF/D-full 选择身份也发生变化；旧、新运行使用的提交 SHA 也不同，因此不能排除其他版本因素。AAGU-053 的选集完全相同，因而比 AAGU-032 更适合解释训练默认值变化下的下游输出差异，但仍不是单变量实验。SD 不是置信区间；不把三个选点 seed 当成模型训练总体的独立重复。')
a('- F1 反映效用，不足以判断遗忘质量或隐私；Retrain−GU 接近 0 也不能单独证明 GU 达到完整遗忘。')
a('')
a('## AAGU-032：Retrain 后的 F1-after')
a('')
a('每个数据集表复刻旧报告的四个代表配置。单元格格式为“旧均值 ± SD → 新均值 ± SD；Δ（新−旧）均值 ± SD”。低 F1 代表删除后留存任务效用更低，但对 288 个选择身份变化的条件，差异还包含删除集合变化。')
a('')
for ds in ['Cora','CiteSeer','PubMed']:
 a(f'### {ds}')
 a('')
 a('| 删除预算 | Degree | D-full 末层 / 2-hop | D-full 全参数 / 2-hop | D-full 全参数 / 3-hop |')
 a('| --- | --- | --- | --- | --- |')
 for row in x['032']['core_tables'][ds]:
  vals=[row['budget']]
  for key in ['Degree','D-full 末层 / 2-hop','D-full 全参数 / 2-hop','D-full 全参数 / 3-hop']:
   v=row[key]
   vals.append(f"{stat(v['old_mean_pct'],v['old_sd_pct'])} → {stat(v['new_mean_pct'],v['new_sd_pct'])}; Δ {delta(v['delta_mean_pp'],v['delta_sd_pp'])} pp")
  a('| '+' | '.join(vals)+' |')
 a('')
a('### AAGU-032 汇总')
a('')
a('| 数据集 | 配对条件数 | F1-after 均值：旧 → 新 | Δ（新−旧） | 单条件 Δ 范围 | Degree / D-full（12 个预算×配置比较） |')
a('| --- | ---: | --- | ---: | ---: | --- |')
for ds in ['Cora','CiteSeer','PubMed']:
 v=x['032']['datasets'][ds]; e=x['032']['degree_vs_dfull'][ds]
 lo,hi=v['delta_range_pp']
 a(f"| {ds} | {v['n']} | {v['all_condition_old_mean_pct']:.3f}% → {v['all_condition_new_mean_pct']:.3f}% | {v['all_condition_delta_mean_pp']:+.3f} pp | {lo:+.3f} 到 {hi:+.3f} pp | D-full 更低 {e['dfull_lower_f1']}/12、相同 {e['equal']}/12、更高 {e['dfull_higher_f1']}/12；均值差 {e['mean_df_minus_degree_pp']:+.3f} pp |")
a('')
a('解释：D-full 相对 Degree 的方向随数据集不同。3000 轮结果中，Cora 与 PubMed 的多数 D-full 配置在同预算均值下留下更低 F1；CiteSeer 则多数更高。与旧参数报告一致，结果不支持“D-full 对所有数据集和预算都优于 Degree”的统一结论。')
a('')
a('## AAGU-053：GNNDelete 与 Retrain 的配对结果')
a('')
a('每行按 selector 类别汇总：Degree 1 个请求；Random、CELF、RR-1024、RR-4096、RR-16384 各 3 个选点 seed。每格为“旧均值 ± SD → 新均值 ± SD；配对 Δ 均值 ± SD”。')
a('')
lookup={(r['dataset'],r['selector']):r for r in x['053']['groups']}
for ds in ['Cora','CiteSeer','PubMed']:
 a(f'### {ds}')
 a('')
 a('| Selector | n | GU F1-after | P0−GU | Retrain F1-after | P0−Retrain | Retrain−GU |')
 a('| --- | ---: | --- | --- | --- | --- | --- |')
 for sel in ['Degree','Random','CELF','RR-1024','RR-4096','RR-16384']:
  r=lookup[(ds,sel)]
  vals=[stat(r['gu_old_mean'],r['gu_old_sd'])+' → '+stat(r['gu_new_mean'],r['gu_new_sd'])+'; Δ '+delta(r['gu_delta_mean'],r['gu_delta_sd'])+' pp',
        stat(r['p0_gu_old_mean'],r['p0_gu_old_sd'])+' → '+stat(r['p0_gu_new_mean'],r['p0_gu_new_sd'])+'; Δ '+delta(r['p0_gu_delta_mean'],r['p0_gu_delta_sd'])+' pp',
        stat(r['retrain_old_mean'],r['retrain_old_sd'])+' → '+stat(r['retrain_new_mean'],r['retrain_new_sd'])+'; Δ '+delta(r['retrain_delta_mean'],r['retrain_delta_sd'])+' pp',
        stat(r['p0_retrain_old_mean'],r['p0_retrain_old_sd'])+' → '+stat(r['p0_retrain_new_mean'],r['p0_retrain_new_sd'])+'; Δ '+delta(r['p0_retrain_delta_mean'],r['p0_retrain_delta_sd'])+' pp',
        stat(r['gap_old_mean'],r['gap_old_sd'])+' → '+stat(r['gap_new_mean'],r['gap_new_sd'])+'; Δ '+delta(r['gap_delta_mean'],r['gap_delta_sd'])+' pp']
  a(f"| {sel} | {r['n']} | "+' | '.join(vals)+' |')
 a('')
a('### AAGU-053 数据集平均（每个选择请求等权）')
a('')
a('| 数据集 | 旧 → 新 GU F1 | Δ GU | 旧 → 新 Retrain F1 | Δ Retrain | 旧 → 新 P0−GU | Δ P0−GU | 旧 → 新 Retrain−GU | Δ gap |')
a('| --- | --- | ---: | --- | ---: | --- | ---: | --- | ---: |')
for ds in ['Cora','CiteSeer','PubMed']:
 v=x['053']['datasets'][ds]
 a(f"| {ds} | {v['old_gu_mean_pct']:.3f}% → {v['new_gu_mean_pct']:.3f}% | {v['gu_delta_mean_pp']:+.3f} pp | {v['old_retrain_mean_pct']:.3f}% → {v['new_retrain_mean_pct']:.3f}% | {v['retrain_delta_mean_pp']:+.3f} pp | {v['old_p0_minus_gu_mean_pp']:.3f} → {v['new_p0_minus_gu_mean_pp']:.3f} pp | {v['p0_minus_gu_delta_mean_pp']:+.3f} pp | {v['old_gap_mean_pp']:.3f} → {v['new_gap_mean_pp']:.3f} pp | {v['gap_delta_mean_pp']:+.3f} pp |")
a('')
a('原模型 P0 的总体均值也随参数变化。逐数据集比较 P0 变化和 P0−Retrain 时，仍应结合上表逐 selector 结果阅读；它们是配对效用差，不是遗忘充分性判据。')
for ds in ['Cora','CiteSeer','PubMed']:
 v=x['053']['datasets'][ds]
 rows=[r for r in pairs053 if r['dataset']==ds]
 oldp0=statistics.mean(float(r['p0_old_pct']) for r in rows)
 newp0=statistics.mean(float(r['p0_new_pct']) for r in rows)
 oldp0r=statistics.mean(float(r['p0_old_pct'])-float(r['retrain_old_pct']) for r in rows)
 newp0r=statistics.mean(float(r['p0_new_pct'])-float(r['retrain_new_pct']) for r in rows)
 a(f"- {ds}：P0 {oldp0:.3f}% → {newp0:.3f}%（Δ {newp0-oldp0:+.3f} pp）；P0−Retrain {oldp0r:+.3f} → {newp0r:+.3f} pp。")
a('')
a('结果要点：')
a('')
a('- Cora 的 16 个选择请求中，GU F1 平均变化 +1.995 pp，Retrain 变化 +1.672 pp；selector 间方向不一致。Random 的 GU F1 平均增加 8.610 pp，而 RR-1024 平均下降 3.506 pp。')
a('- CiteSeer 平均 GU F1 增加 +0.638 pp，但 Retrain F1 平均下降 1.483 pp；平均 Retrain−GU gap 从 2.290 降至 0.169 pp。')
a('- PubMed 六类 selector 的 GU F1 均上升（每类约 +5.071 至 +10.658 pp），Retrain F1 约 +2.882 至 +3.347 pp；总体 P0−GU 从 7.648 降至 2.764 pp，说明新旧参数下 GU 的绝对效用表现变化明显，不能把旧表的损害幅度直接套用到新表。')
a('')
a('## 结论与下一步')
a('')
a('1. 两项新结果均已覆盖三数据集，且当前回传的结果文件校验通过。')
a('2. AAGU-032 在 3000 轮设置下可复刻旧报告的分层比较框架；结果仍表现为数据集依赖。由于 80% 条件的 selection_id 不同，只能作为匹配配置的整套协议对照，不能叫作同删除集严格复跑。')
a('3. AAGU-053 48/48 选集身份相同，旧新 downstream 对照更直接；PubMed 尤其显示 GU F1 与 Retrain F1 均明显上升，原先的 GU−Retrain 差距缩小。该变化是待审阅结果，不等同“3000 轮提升遗忘质量”。')
a('4. 本报告不重做 AAGU-053 已接受的 RR10 采样稳定性 36 格分析；该分析和这里的 96 格下游效果分属不同范围。')
a('5. 当前两个 Work Plan 科学决定维持 pending，分析状态为 review；请审阅差异和解释边界后再确定接受的科学结论。')
a('')
a('## 证据与可复算产物')
a('')
a('- 新 AAGU-032 manifest：results/runs/gpu4090/aagu032-extended-v2-multi-gcn-retrain/aagu032-recovery-full-20260920/run.json；旧逐格结果：.workblock/items/AAGU-033/analysis/20260908/retrain_cells.csv；旧报告：.workblock/items/AAGU-033/analysis/20260908/REPORT.md。')
a('- 新 AAGU-053 manifest：results/runs/gpu4090/aagu053-im-group-budget10/aagu053-newtraining-full-20260920/run.json；旧逐条件比较：.workblock/items/AAGU-053/evidence/table-detail.json；RR10 独立历史报告：.workblock/items/AAGU-053/REPORT.md。')
a('- 完整逐格配对与摘要 CSV、summary.json 和复算脚本归档在 evidence/AAGU-032-AAGU-053-3000epoch-20260923/。从仓库根目录运行 python self/research/analyses/evidence/AAGU-032-AAGU-053-3000epoch-20260923/analyze_comparison.py 可复算配对摘要；再运行同目录 build_report.py 可重建本报告。')
a('- 参数身份依据：experiments/modular_config.py（默认训练轮数）；experiments/node_deletion.py 中 pairing_identity（把完整 training 参数写入配对身份）；experiments/modular_gu.py（GU 输出身份再绑定基础 checkpoint state hash）。')
report='\n'.join(lines)+'\n'
target=root/'self/research/analyses/AAGU-032-AAGU-053-3000epoch-comparison-20260923.md'
target.write_text(report,encoding='utf-8')
print(target, 'bytes',len(report.encode('utf-8')))
