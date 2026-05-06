# 泛化性实验执行清单（重构版）

> Status: reference
> Role: 2026-02 阶段的实验覆盖与完成度仪表盘，记录 MG-0~MG-3、ratio 敏感性与评估缺口。
> Use this when: 你需要快速核对当时哪些泛化实验已经跑完、哪些指标已补齐、哪些脚本对应哪些输出目录。
> See also: `analysis_phase_a.md`, `plan_flow_v2_delta.md`, `../report/paper/stage_report_2026-02-27.md`, `../results/experiments/`

> 目标：把“已完成 + 待完成”的泛化实验配置集中到一个文件，便于逐项打勾推进。
> 主要依据：`self/analysis_phase_a.md`、`self/flow.md`、`self/宏观plan.md`、`self/plan_flow_v2_delta.md`、`self/experiment_params.md`。

## 1. 使用说明

- `[x]` 已完成
- `[ ]` 待完成
- `⚠️` 有缺口但已产生部分结果

## 2. 项目仪表盘

### 2.1 全局进度概览

| 模块 | 核心配置 | 规模（runs） | 状态 | 关键结论/缺口 |
|------|---------|-------------|------|---------------|
| Phase A / A+ 基线 | `Cora / GCN / ratio=0.05 / seed=2024` | 18+ | ✅ | 机制分组结论已形成；Retrain/Collateral 基础评估已跑通 |
| MG-0 稳定性 | `Cora / GCN / 5 seeds` | 90 | ✅ (2026-02-22) | 结论非 seed 偶然 |
| MG-1 跨数据集 | `Citeseer / GCN / 5 seeds` | 90 | ✅ (2026-02-27) | `GNNDelete` 已补齐（含 phase_a/collateral/relative） |
| MG-2 跨模型 | `Cora / GAT / 5 seeds` | 90 | ✅ (2026-02-22) | 最小跨模型证据完成 |
| MG-3 扩展方法 | `Citeseer(GCN)+Cora(GAT) / IDEA+MEGU` | 80 | ✅ (2026-02-22) | 5 方法扩展结果完成 |
| Ratio 敏感性 | `Cora / GCN / ratio=0.01,0.05,0.10,0.20 / 5 seeds` | 240 | ✅ (2026-02-25) | 攻击强度曲线基础完成 |
| P2-EXT 扩展比例 | `GIF / cora,citeseer / GCN,GAT,GIN / r=0.10,0.20 / 5 seeds` | 360 | ✅ (2026-02-27) | 高比例跨模型/跨数据集补强完成 |

### 2.2 当前优先待办（Top）

- [x] 补齐 **MG-1 的 `GNNDelete`**，使三类方法在 Citeseer 对齐
- [ ] 补齐 **P5：MIA + 统计检验图表**
- [ ] 跑批前通过一次 **执行前门禁（第 3 节）**

## 3. 执行前门禁（Go / No-Go）

- [ ] **Seed 独立性**：同配置下改 `seed` 会触发新实验，不复用旧结果
  - 检查点：`run_experiments.py` 支持 `--seeds 2024,2025,...`
  - 检查点：输出文件名包含 `seed`（避免覆盖）
  - 检查点：MG-0 五 seed（`42, 212, 722, 2024, 1337`）均有独立输出目录与结果文件
- [ ] **Cache 策略**：默认开启 cache（供 `eval_collateral.py` 读取 `selected_nodes`）
  - 检查点：仅在明确排查时使用 `--no_cache`
  - 检查点：`random/pagerank/im` 已启用跨方法选点复用（`results/selection_cache`）
  - 备注：当前批次仅评估 `im_v4/hybrid_v4`，`eval_collateral` 的 cache 匹配含 `strategy_name`，不会命中旧 `im/hybrid` 条目；若后续混跑不同 `k`，需重新检查
- [ ] **自动报告**：`demo_attack.py` 与 `eval_collateral.py` 均可追加 `results/_journal/auto_report.md`
  - 检查点：`eval_collateral.py` 在无结果时写 `WARN`（不是 `OK`）
- [ ] **复现实验设置**：同 seed 重跑应一致（允许极小浮动），不同 seed 存在统计波动

## 4. 最小泛化包（MG-0 ~ MG-3）

> 目的：在可控算力下，先拿到可发表级的最小泛化证据。
> 核心方法组：IF-based `GIF`、Learning-based `GNNDelete`、Shard-based `GraphEraser`。
> 可选扩展：`IDEA`、`MEGU`。

### 4.1 最小泛化模块状态

| 模块 | 配置 | 方法/策略 | 状态 |
|------|------|-----------|------|
| MG-0 稳定性 | `Cora / GCN / ratio=0.05 / 5 seeds` | `GIF,GNNDelete,GraphEraser` × `random,degree,pagerank,tracin,im,hybrid` | ✅ |
| MG-1 跨数据集 | `Citeseer / GCN / ratio=0.05 / 5 seeds` | 同上 | ✅ |
| MG-2 跨模型 | `Cora / GAT / ratio=0.05 / 5 seeds` | 同上 | ✅ |
| MG-3 扩展方法 | `Citeseer(GCN)+Cora(GAT)` | `IDEA,MEGU`（建议先 `random,tracin,im,hybrid`） | ✅ |

### 4.2 最小泛化通过标准

- [ ] 在 `Citeseer/GCN` 与 `Cora/GAT` 上，三类方法（IF/Learning/Shard）仍保持机制差异趋势
- [ ] 关键结论在 `5 seeds（42, 212, 722, 2024, 1337）` 下方向一致（不要求每个点都显著）
- [ ] 每个配置至少有 `F1 Drop + Gap + Collateral` 三类指标

<details>
<summary>展开：MG-0~MG-3 指标摘要（保留原结论）</summary>

- MG-0（✅，2026-02-22）
  - F1 Drop: GIF=`1.6%±0.8`, GNNDelete=`9.7%±3.8`, GraphEraser=`-5.2%±2.7`
  - MIA AUC: GIF=`0.60`, GNNDelete=`0.64`, GraphEraser=`0.00`
  - Relative: GIF=`1.7%±1.1`, GNNDelete=`13.7%±4.0`, GraphEraser=`3.7%±2.5`
- MG-1（✅，2026-02-27）
  - F1 Drop: GIF=`2.6%±0.6`, GNNDelete=`-19.3%±1.7`, GraphEraser=`-8.8%±1.8`
  - MIA AUC: GIF=`0.60`, GNNDelete=`0.00`, GraphEraser=`0.00`
  - Relative: GIF=`0.0%±0.3`, GNNDelete=`已补齐（见 results/relative/GNNDelete/citeseer/GCN）`, GraphEraser=`0.2%±0.7`
- MG-2（✅，2026-02-22）
  - F1 Drop: GIF=`5.4%±1.1`, GNNDelete=`14.4%±5.1`, GraphEraser=`-7.9%±3.4`
  - MIA AUC: GIF=`0.49`, GNNDelete=`0.68`, GraphEraser=`0.00`
  - Relative: GIF=`2.8%±1.9`, GNNDelete=`-`, GraphEraser=`3.9%±2.9`
- MG-3（✅，2026-02-22）
  - F1 Drop: IDEA=`5.6%±0.9`, MEGU=`1.4%±1.1`
  - MIA AUC: IDEA=`0.43`, MEGU=`0.00`
  - Relative: IDEA=`1.7%±1.0`, MEGU=`0.9%±0.8`

</details>

## 5. Ratio 敏感性（攻击强度曲线）

- [x] `Cora / GCN / GIF,GNNDelete / ratio=0.01,0.05,0.10,0.20 / 5 seeds`（240 runs，2026-02-25）
  - F1 Drop: GIF=`2.4%±1.1`, GNNDelete=`13.8%±5.0`
  - MIA AUC: GIF=`0.61`, GNNDelete=`0.71`
  - Relative: GIF=`1.7%±1.1`, GNNDelete=`13.7%±4.0`
- [x] `P2-EXT`：`GIF / cora,citeseer / GCN,GAT,GIN / r=0.10,0.20 / 5 seeds`（360 runs，2026-02-27）

## 6. 评估缺口审计（2026-02-26）

- [x] 当前批次 `collateral / relative` 无缺口
- [x] 已完成：GIF 全 phase+ratio、GNNDelete 全 phase+ratio、GraphEraser(MG-0/1/2, r=0.05)、IDEA/MEGU(MG-3)

## 7. 全量泛化主清单（待做）

### 7.1 跨遗忘方法（同数据集/模型）

- [ ] 配置 `Cora / GCN / ratio=0.05 / >=5 seeds`
  - methods: `GIF, GST, GNNDelete, MEGU`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral, Selection Time`

### 7.2 跨数据集（同方法/模型）

- [ ] 配置 `GCN / GIF / ratio=0.05 / >=5 seeds`
  - datasets: `Cora, Citeseer, PubMed, Physics`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral`

### 7.3 跨模型（同方法/数据集）

- [ ] 配置 `Cora / GIF / ratio=0.05 / >=5 seeds`
  - models: `GCN, GAT, GIN, SAGE`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral`

### 7.4 Ratio 敏感性扩展

- [ ] 输出统一图：`Attack Success vs Ratio`、`Gap vs Ratio`（跨数据集/跨模型并列）

### 7.5 Retrain 对照与统计显著性（每组必做）

- [ ] 每个主配置都同时跑 `Unlearn` 与 `Retrain-after-deletion`（同一删除集）
- [ ] 每个主配置都做 `>=5 seeds` 并汇总 `mean ± std`
- [ ] 每个主配置都计算 `Gap` 统计显著性（t-test, 95% CI）

### 7.6 MIA 与多指标完整性

- [ ] 每个主配置补齐 `Update-Detection AUC`（legacy: MIA AUC；JSON 字段 `mia_auc`）
- [ ] 每个主配置至少报告 6 类最小指标：
  - `F1 Drop`
  - `Update-Detection AUC`（legacy: MIA AUC）
  - `Selection Time`
  - `Approximation Gap`
  - `Collateral Damage`
  - `Gap 统计显著性`

## 8. 推荐执行顺序（按风险）

- [x] `P0`：`scripts/experiments/run_mg0_completion.sh`（稳定性）
- [x] `P1`：`scripts/experiments/run_mg1_citeseer.sh`（跨数据集）
- [x] `P2`：`GIF` 在 `ratio=0.10/0.20`（已被 `P2-EXT` 覆盖）
- [x] `P2-EXT`：`GIF / cora,citeseer / GCN,GAT,GIN / r=0.10,0.20 / 5 seeds`
- [x] `P3`：`scripts/experiments/run_mg2_gat.sh`（跨模型）
- [x] `P4`：`scripts/experiments/run_mg3_extended.sh`（扩展方法）
- [ ] `P5`：补齐 `Update-Detection AUC`（legacy: MIA）与完整统计检验图表

## 9. 脚本与输出目录对照

| Sh 文件 | 实验阶段 | Dataset | Model | Methods | Strategies | Seeds | 输出目录 |
|---------|---------|---------|-------|---------|------------|-------|----------|
| `scripts/experiments/run_mg0_completion.sh` | MG-0 稳定性 | cora | GCN | GIF,GNNDelete,GraphEraser | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg0_completion` |
| `scripts/experiments/run_mg1_citeseer.sh` | MG-1 跨数据集 | citeseer | GCN | GIF,GNNDelete,GraphEraser | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg1_citeseer` |
| `scripts/experiments/run_mg2_gat.sh` | MG-2 跨模型 | cora | GAT | GIF,GNNDelete,GraphEraser | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg2_gat` |
| `scripts/experiments/run_mg3_extended.sh` | MG-3 扩展方法 | citeseer(cora) | GCN(GAT) | IDEA,MEGU | random,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg3_citeseer`, `mg3_gat` |

- 一键运行全部：`bash scripts/experiments/run_all_generalization.sh`
- 跳过 MG-1：`bash scripts/experiments/run_all_mg.sh`

## 10. 记录规范（每条实验最小字段）

- [ ] 固定 seeds：`42, 212, 722, 2024, 1337`
- [ ] 每条记录至少包含：
  - `dataset, model, method, strategy, ratio, seed`
  - `f1_before, f1_after, f1_drop`
  - `perf_before, perf_retrain, perf_unlearn, gap, gap_pct`
  - `mean_pred_shift, fraction_flipped`
  - `mia_auc, selection_time_s`
