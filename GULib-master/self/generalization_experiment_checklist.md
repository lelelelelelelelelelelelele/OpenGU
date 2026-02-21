# 泛化性实验配置清单（可勾选）

> 目标：把“已完成 + 待完成”的泛化实验配置集中到一个文件，便于逐项打勾推进。
> 主要依据：`self/analysis_phase_a.md`、`self/flow.md`、`self/宏观plan.md`、`self/plan_flow_v2_delta.md`、`self/experiment_params.md`。

## 0. 勾选说明

- `[x]` 已完成
- `[ ]` 待完成

## 1. 已完成配置（基线与阶段结论）

- [x] `Phase A`：`Cora / GCN / unlearn_ratio=0.05 / seed=2024`，`3 methods × 6 strategies`
  - methods: `GIF, GNNDelete, GraphEraser`（已完成）
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 输出：F1 Drop + 初步机制分组结论（Learning-based: IM最强, IF-based: Hybrid最强, Shard-based: 免疫）
- [x] `Phase A+`：`Cora / GCN / unlearn_ratio=0.05` 的 Retrain/Collateral 基础评估已跑通
  - 已有 retrain gap + collateral 基础设施与结果
  - 核心发现：GNNDelete Gap大(6-30%), GIF Gap≈0(<1.5%), GraphEraser无一致方向

## 1.5 Sh 文件配置对照表

| Sh 文件 | 实验阶段 | Dataset | Model | Methods | Strategies | Seeds | 输出目录 |
|---------|---------|---------|-------|---------|------------|-------|----------|
| `run_mg0_completion.sh` | MG-0 稳定性 | cora | GCN | GIF,GNNDelete,GraphEraser,GUIDE | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg0_completion` |
| `run_mg1_citeseer.sh` | MG-1 跨数据集 | citeseer | GCN | GIF,GNNDelete,GraphEraser | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg1_citeseer` |
| `run_mg2_gat.sh` | MG-2 跨模型 | cora | GAT | GIF,GNNDelete,GraphEraser | random,degree,pagerank,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg2_gat` |
| `run_mg3_extended.sh` | MG-3 扩展方法 | citeseer(cora) | GCN(GAT) | IDEA,MEGU | random,tracin,im,hybrid | 42,212,722,1337,2024 | `results/experiments/mg3_citeseer`, `mg3_gat` |

> 📌 运行全部：`bash run_all_generalization.sh`（跳过 MG-1：`bash run_all_mg.sh`）

## 1.5 执行前工作流体检（必须先过）

- [ ] **Seed 独立性**：同配置下改 `seed` 会触发新实验，不复用旧结果
  - 检查点：`run_experiments.py` 已支持 `--seeds 2024,2025,...`
  - 检查点：输出文件名包含 `seed`（避免覆盖）
  - 检查点：MG-0 五 seed（`42, 212, 722, 2024, 1337`）均生成独立输出目录与独立结果文件（含 seed 后缀）
- [ ] **Cache 策略**：默认开启 cache（供 `eval_collateral.py` 读取 selected_nodes）
  - 检查点：仅在明确排查时使用 `--no_cache`
  - 检查点：`random/pagerank/im` 已启用跨方法选点复用（`results/selection_cache`）
- [ ] **自动报告**：`demo_attack.py` 与 `eval_collateral.py` 均能追加 `results/_journal/auto_report.md`
  - 检查点：`eval_collateral.py` 在无结果时写 `WARN`（不是 `OK`）
- [ ] **复现实验设置**：同 seed 重跑结果应一致（允许极小浮动），不同 seed 有统计波动

## 2. 最小泛化阶段（推荐先做）

> 目的：在可控算力下，先拿到”可发表级”的最小泛化证据。
> 核心方法组（4 个）：
> - IF-based: `GIF`
> - Learning-based: `GNNDelete`
> - Shard-based: `GraphEraser`, `GUIDE`
> 可选扩展组（+2 个）：`IDEA`（IF-based）, `MEGU`（Learning-based）。

> 📋 **Sh 文件对应**：`run_mg0_completion.sh`, `run_mg1_citeseer.sh`, `run_mg2_gat.sh`, `run_mg3_extended.sh`

### 2.1 MG-0 稳定性（非泛化，但必做）

- [ ] `Cora / GCN / ratio=0.05 / 5 seeds`
  - seeds: `42, 212, 722, 2024, 1337`
  - methods: `GIF, GNNDelete, GraphEraser, GUIDE`（2 Shard-based + 1 Learning-based + 1 IF-based）
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 产出：`mean ± std`，确认结论不是 seed 偶然
  - 规模：`4 methods × 6 strategies × 5 seeds = 120 runs`
  - **状态**：🔄 部分完成
    - GIF/GNNDelete: ✅ 4 seeds (42,212,722,1337)，❌ 缺 2024
    - GraphEraser/GUIDE: ✅ 5 seeds (42,212,722,1337,2024) 🎉
  - **需补跑**：seed 2024 的 GIF/GNNDelete

### 2.2 MG-1 最小跨数据集泛化

- [ ] `Citeseer / GCN / ratio=0.05 / 5 seeds`
  - methods: `GIF, GNNDelete, GraphEraser`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral, Selection Time`
  - 规模：`3 × 6 × 5 = 90 runs`
  - **状态**：🔄 接近完成
    - GIF: ✅ 5 seeds
    - GraphEraser: ✅ 5 seeds
    - GNNDelete: ⚠️ 4 seeds (seed 212 运行失败，日志截断)
  - **需补跑**：seed 212 的 GNNDelete（检查错误原因）

### 2.3 MG-2 最小跨模型泛化

- [ ] `Cora / GAT / ratio=0.05 / 5 seeds`
  - methods: `GIF, GNNDelete, GraphEraser`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral`
  - 规模：`3 × 6 × 5 = 90 runs`
  - **状态**：❌ 未开始（sh 文件已配置）

### 2.4 MG-3（可选）扩展到 5 方法

- [ ] 在 MG-1 + MG-2 基础上增加 `IDEA` 与 `MEGU`
  - methods: `GIF, GNNDelete, GraphEraser, IDEA, MEGU`
  - 建议先只跑 `random, tracin, im, hybrid` 四策略做筛选
  - 说明：`GST` 当前有兼容问题，不建议放在最小泛化主线
  - **状态**：❌ 未开始（sh 文件已配置）

### 2.5 最小泛化通过标准

- [ ] 在 `Citeseer/GCN` 与 `Cora/GAT` 上，三类方法（IF/Learning/Shard）仍保持机制差异趋势
- [ ] 关键结论在 `5 seeds（42, 212, 722, 2024, 1337）` 下方向一致（不要求每个点都显著）
- [ ] 每个配置至少有 `F1 Drop + Gap + Collateral` 三类指标

## 3. 全量泛化实验主清单（待做）

### 3.1 跨遗忘方法（同一数据集/模型）

- [ ] 配置 `Cora / GCN / ratio=0.05 / >=5 seeds`，比较跨方法泛化
  - methods: `GIF, GST, GUIDE, GNNDelete, MEGU`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral, Selection Time`

### 3.2 跨数据集（同一方法/模型）

- [ ] 配置 `GCN / GIF / ratio=0.05 / >=5 seeds`，比较跨数据集泛化
  - datasets: `Cora, Citeseer, PubMed, Physics`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral`

### 3.3 跨模型（同一方法/数据集）

- [ ] 配置 `Cora / GIF / ratio=0.05 / >=5 seeds`，比较跨模型泛化
  - models: `GCN, GAT, GIN, SAGE`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 指标：`F1 Drop, Gap, Collateral`

### 3.4 Ratio 敏感性（攻击强度曲线）

- [ ] 配置 `Cora / GCN / GIF / >=5 seeds`，做比例敏感性
  - `unlearn_ratio`: `0.01, 0.05, 0.10, 0.20`
  - strategies: `random, degree, pagerank, tracin, im, hybrid`
  - 输出：`Attack Success vs Ratio`、`Gap vs Ratio`

### 3.5 Retrain 对照与统计显著性（每组必做）

- [ ] 每个主配置都同时跑 `Unlearn` 和 `Retrain-after-deletion`（同一删除集）
- [ ] 每个主配置都做 `>=5 seeds` 并汇总 `mean ± std`
- [ ] 每个主配置都计算 `Gap` 的统计显著性（t-test, 95% CI）

### 3.6 MIA 与多指标完整性

- [ ] 每个主配置补齐 `MIA AUC`
- [ ] 每个主配置至少报告 6 类最小指标：
  - `F1 Drop`
  - `MIA AUC`
  - `Selection Time`
  - `Approximation Gap`
  - `Collateral Damage`
  - `Gap 统计显著性`

## 4. 推荐执行顺序（按你当前结论风险）

- [ ] `P0`：`run_mg0_completion.sh` - 稳定性实验（5 seeds 验证结论不是 seed 偶然）
  - sh 已配置：`--methods GIF,GNNDelete,GraphEraser,GUIDE --datasets cora --base_model GCN`
- [ ] `P1`：`run_mg1_citeseer.sh` - Citeseer / GCN 复现实验（优先验证当前机制分组是否泛化）
  - sh 已配置：`--methods GIF,GNNDelete,GraphEraser --datasets citeseer --base_model GCN`
- [ ] `P2`：做 `GIF` 在 `ratio=0.10/0.20`（排查”攻击幅度偏小”是否仅是低比例效应）
- [ ] `P3`：`run_mg2_gat.sh` - 跨模型（`GAT`）
  - sh 已配置：`--methods GIF,GNNDelete,GraphEraser --datasets cora --base_model GAT`
- [ ] `P4`：`run_mg3_extended.sh` - 扩展到 IDEA/MEGU
  - sh 已配置：Citeseer(GCN) + Cora(GAT) 各跑 IDEA, MEGU
- [ ] `P5`：最后补齐 `MIA` 与完整统计检验图表

## 5. 建议的种子与记录规范

- [ ] 固定 seeds：`42, 212, 722, 2024, 1337`
- [ ] 每条记录至少包含：
  - `dataset, model, method, strategy, ratio, seed`
  - `f1_before, f1_after, f1_drop`
  - `perf_before, perf_retrain, perf_unlearn, gap, gap_pct`
  - `mean_pred_shift, fraction_flipped`
  - `mia_auc, selection_time_s`
