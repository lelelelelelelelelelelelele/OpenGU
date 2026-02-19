# Adversarial Attacks on GNN Unlearning - 阶段性进展报告

> 日期: 2026-02-19
> 阶段: Step 0-5 + Step 7 完成，6 策略跨方法泛化验证通过
> 作者: lele

---

## 1. 研究概述

本项目研究针对图神经网络遗忘学习（GNN Unlearning）的对抗攻击。核心假设是：**近似遗忘算法可被攻击者通过精心选择遗忘节点来诱导性能塌缩**——并非所有数据点的遗忘代价相等，存在"关键锚点"（Structural & Feature-rich Anchors），一旦被强制移除会导致模型对保留数据的推理能力大幅下降。方法创新点在于采用 **TracIn（pseudo-IF）** 替代计算昂贵的 Hessian-based Influence Function，通过训练阶段梯度点积近似影响函数，实现轻量级灰盒攻击策略。

---

## 2. 实验平台

| 组件 | 说明 |
|------|------|
| 基础框架 | OpenGU（16 GU 算法、37 数据集、13+ GNN 骨干网络） |
| 攻击框架 | 自研 attack module（6 策略、模块化 pipeline、结果缓存） |
| 代码量 | 1150 行生产代码 + 1037 行单元测试 = 2187 行 |
| 环境 | PyTorch + PyG 2.6.1, CUDA, conda `gnn` 环境 |
| 开发数据集 | Cora（2708 nodes, 7 classes） |

---

## 3. 阶段性进展

### Step 0: 方法兼容性与脆弱性摸底（77+ runs）

对 OpenGU 框架中 15 个遗忘方法进行系统性兼容性测试，在 Cora/GCN 配置下覆盖 5 个 unlearn ratio（0.005, 0.02, 0.05, 0.1, 0.2）。

**兼容性结果**: 11/15 方法成功运行，4 方法因接口不兼容失败（GST, CEU, CGU, UTU）。

**脆弱性排名**（按最大 F1 下降幅度排序）:

| 排名 | 方法 | Pipeline 类型 | Max F1 Drop | 脆弱性等级 |
|------|------|-------------|-------------|----------|
| 1 | **GNNDelete** | Learning-based | **8.31%** | 高危 |
| 2 | **Projector** | 独立实现 | **5.90%** | 高危 |
| 3 | GraphEraser | Shard-based | 2.40% | 中等 |
| 4 | GraphRevoker | Shard-based | 2.40% | 中等 |
| 5 | GIF | IF-based | 2.22% | 中等 |
| 6 | IDEA | IF-based | 2.03% | 中等 |
| 7 | MEGU | Learning-based | 1.85% | 低 |
| 8 | D2DGN | Learning-based | 0.74% | 稳定 |
| 9 | SGU | Learning-based | 0.55% | 稳定 |
| 10 | GUKD | Learning-based | 0.37% | 稳定 |
| 11 | GUIDE | Shard-based | 0.00% | **免疫** |

> 详细指标见 [附录 A: Method Table](appendix_method_table.md)

**关键图表**:

![脆弱性排名](figures/vulnerability_ranking.png)
*Figure 1: 11 个方法的脆弱性排名（Max F1 Drop）*

![F1 曲线总览](figures/all_methods_combined.png)
*Figure 2: 所有方法在不同 unlearn ratio 下的 F1 变化趋势*

![类别对比](figures/category_comparison.png)
*Figure 3: 按 Pipeline 类型分组的脆弱性对比*

![时间 vs Ratio](figures/time_vs_ratio.png)
*Figure 4: Unlearning 时间随 ratio 变化趋势*

---

### Step 1-3: 攻击策略实现

实现了 6 个节点选择策略，形成完整的攻击模块。

**架构设计**:

```
BaseStrategy (ABC)
├── select_nodes(data, model, k) -> Tensor    # 核心接口
├── RandomStrategy        (17 行)   # 随机基线
├── DegreeStrategy        (26 行)   # 度中心性
├── PageRankStrategy      (36 行)   # PageRank 结构重要性
├── TracInStrategy        (172 行)  # 梯度影响力（核心策略）
├── IMStrategy            (164 行)  # Influence Maximization (CELF)
└── HybridStrategy        (115 行)  # IF-IM 融合策略

AttackManager (370 行)
├── register_strategy()       # 策略注册
├── run_attack()              # 单策略攻击
├── compare_strategies()      # 多策略对比
└── ResultCache               # 结果缓存
```

**代码统计**:

| 模块 | 文件数 | 行数 |
|------|--------|------|
| 策略实现 (`attack/attack_strategies/`) | 8 | 569 |
| 攻击管理器 (`attack/attack_manager.py`) | 1 | 370 |
| 攻击评估 (`attack/attack_eval.py`) | 1 | 211 |
| 单元测试 (`tests/test_*.py`) | 4 | 1037 |
| **合计** | **14** | **2187** |

**TracIn 策略核心原理**:

```
Score(v) = Σ_t η_t · ⟨∇L(v, θ_t), ∇L(D_test, θ_t)⟩
```

通过计算每个训练节点在训练过程中各 checkpoint 上的梯度与测试集梯度的点积，近似该节点对模型测试性能的影响力。选择影响力最大的 Top-K 节点作为遗忘目标。

---

### Step 4: 端到端 Demo 验证（核心结果）

在 Cora/GCN/GNNDelete 配置下，对 6 个策略进行端到端对比验证。

**实验配置**:
- Dataset: Cora (2708 nodes)
- Model: GCN (2-layer, 92,231 params)
- Unlearning: GNNDelete (50 epochs)
- Unlearn ratio: 5% (135 nodes)
- Training: 100 epochs per run

**核心结果表（6 策略）**:

| 排名 | 策略 | F1 Drop | Drop 比率 | 选择耗时 | vs Random |
|------|------|---------|----------|---------|-----------|
| 1 | **IM** | **0.1384** | **15.59%** | 30.55s | **2.03x** |
| 2 | **TracIn** | **0.0904** | **10.17%** | 7.11s | **1.32x** |
| 3 | **Hybrid** | **0.0886** | **10.02%** | 7.41s | **1.30x** |
| 4 | Random | 0.0683 | 7.72% | 0.00s | (baseline) |
| 5 | Degree | 0.0535 | 6.05% | 0.04s | 0.78x |
| 6 | PageRank | 0.0535 | 6.02% | 0.04s | 0.78x |

**结果分析**:

1. **IM 策略最强**: IM（Influence Maximization）策略在 GNNDelete 上产生 15.59% 的 F1 下降，是随机基线的 **2.03 倍**，超越 TracIn 成为最有效的攻击策略。CELF 优化的贪心选择在结构传播层面精准识别了对 GNNDelete 学习式遗忘机制最具破坏力的节点集合。

2. **TracIn 和 Hybrid 接近**: TracIn（10.17%）和 Hybrid（10.02%）效果相近，均显著优于随机基线。Hybrid 在 GNNDelete 上并未超越 TracIn，原因是 IM 与 TracIn 选择的节点重叠度较高，混合后未产生额外协同。

3. **结构启发式仍然失效**: Degree 和 PageRank 策略均 **劣于** 随机基线（0.78x），进一步确认 **脆弱性 ≠ 结构重要性**。

4. **计算开销合理**: IM 选择耗时 30.55s（CELF 优化），TracIn 7.11s，Hybrid 7.41s，均在可接受范围内。

**Bug 修复记录**: Demo 开发过程中修复了 3 个关键 bug：
- 遗忘节点文件注入路径不匹配
- TracIn 梯度计算的 device 不一致
- AttackManager 结果缓存的 key 冲突

> 完整 Demo 输出见 [附录 B: Demo Output](appendix_demo_output.txt)

---

### Step 5: Influence Maximization + Hybrid 融合策略

实现了两个高级攻击策略，完成 IF-IM 融合研究方向：

**IMStrategy (164 行)**: 基于 Influence Maximization 的 CELF (Cost-Effective Lazy Forward) 优化算法，通过贪心选择在图传播中影响力最大的节点集合。利用子模性保证近似比，CELF 加速避免冗余边际贡献计算。

**HybridStrategy (115 行)**: 融合 TracIn（特征影响力）与 IM（结构传播力）的混合策略：

```
Score(v) = α · Norm(IF(v)) + β · Norm(IM(v))
```

支持可调权重参数 α/β，默认 α=0.5, β=0.5。两个分数分别归一化后加权求和，选取 Top-K。

**测试覆盖**: `tests/test_im_hybrid.py` (221 行)，覆盖 CELF 收敛性、混合权重敏感性、边界条件。

**实测结果（Cora/GCN, 5% unlearn ratio）**:

| 方法 | IM F1 Drop | IM 选择耗时 | Hybrid F1 Drop | Hybrid 选择耗时 |
|------|-----------|------------|---------------|----------------|
| GNNDelete | 0.1384 (15.59%) | 30.55s | 0.0886 (10.02%) | 7.41s |
| GIF | 0.0166 (1.87%) | 31.04s | 0.0277 (3.10%) | 7.43s |
| GraphEraser | -0.0517 (-6.44%) | ~31s | -0.0627 (-7.83%) | ~7.4s |

IM 在 Learning-based 方法（GNNDelete）上效果最强；Hybrid 在 IF-based 方法（GIF）上效果最强（3.00x vs Random），验证了 flow.md Step 6 核心假设。

---

### Step 7: 攻击评估模块

实现了标准化的攻击效果评估框架 (`attack/attack_eval.py`, 211 行)：

**5 个评估函数**:
- `f1_drop`: 遗忘前后 F1 下降量
- `f1_drop_ratio`: 相对下降比例
- `mia_auc`: Membership Inference Attack AUC
- `retrain_gap`: 与完全重训练的性能差距
- `comprehensive_eval`: 综合评估（v2 归因框架）

**v2 归因框架**: `comprehensive_eval` 将多个指标聚合为统一的攻击效果评分，支持自定义权重。

**测试覆盖**: `tests/test_attack_eval.py` (232 行)，18 测试全通过。

### Step 4+5 补充: 跨方法泛化验证（3 方法 × 6 策略）

在 3 个代表性 unlearning 方法上对全部 6 个攻击策略进行端到端对比，验证攻击泛化性。

**实验矩阵（F1 Drop，Cora/GCN, 5% unlearn ratio, seed=2024）**:

| 策略 | GNNDelete (Learning) | GIF (IF-based) | GraphEraser (Shard) |
|------|---------------------|----------------|---------------------|
| **IM** | **0.1384 (2.03x)** | 0.0166 (1.80x) | -0.0517 |
| **TracIn** | 0.0904 (1.32x) | 0.0203 (2.20x) | -0.0480 |
| **Hybrid** | 0.0886 (1.30x) | **0.0277 (3.00x)** | -0.0627 |
| Random | 0.0683 (1.00x) | 0.0092 (1.00x) | -0.0701 |
| Degree | 0.0535 (0.78x) | 0.0185 (2.00x) | -0.0443 |
| PageRank | 0.0535 (0.78x) | 0.0129 (1.40x) | -0.0295 |

**跨方法泛化结论**:

1. **GNNDelete（Learning-based）**: IM 最强（2.03x），纯结构传播力在参数级遗忘机制上破坏力最大。结构启发式（Degree/PageRank）劣于随机。

2. **GIF（IF-based）**: **Hybrid 最强（3.00x）**，验证了 IF-IM 融合假设——在影响函数近似的遗忘方法上，结合梯度影响力（TracIn）与结构传播力（IM）产生协同效应。所有 6 策略均显著优于随机基线，说明 GIF 对定向攻击普遍脆弱。

3. **GraphEraser（Shard-based）**: 所有策略 F1 Drop 均为负值（遗忘后 F1 反而上升），**分片聚合架构天然抗攻击**。PageRank 的负 Drop 最小（-0.0295），可能因为移除高 PageRank 节点减少了分片间的信息冗余，但整体上攻击无效。

4. **最佳策略因方法而异**: 不存在一个"万能"策略——IM 适合攻击 Learning-based 方法，Hybrid 适合攻击 IF-based 方法，而 Shard-based 方法对所有策略免疫。这意味着实际攻击需要根据目标方法的 pipeline 类型选择策略。

---

## 4. 关键发现与洞察

### 发现 1: GNNDelete 最脆弱，GUIDE 完全免疫

GNNDelete 在随机遗忘下即出现 8.31% 的 F1 下降（ratio=0.2 时），是最脆弱的方法。而 GUIDE 在所有 ratio 下 F1 恒为 0.8303，完全不受遗忘操作影响。

**推测原因**: GNNDelete 通过学习删除权重来实现遗忘，这种参数级别的修改对节点选择敏感；GUIDE 采用子图修复策略（MixUp），遗忘后通过重新聚合邻域信息恢复性能，天然具有鲁棒性。

### 发现 2: 脆弱性 ≠ 结构重要性（GNNDelete 特异性）

在 GNNDelete 上，TracIn/IM（梯度/传播策略）有效而 Degree/PageRank（结构策略）失效。但在 GIF 上，**Degree 表现优异（2.00x）**，说明结构启发式的有效性取决于目标方法的遗忘机制。GNNDelete 的参数级修改对结构变化有适应能力，而 GIF 的影响函数近似对结构变化更敏感。

### 发现 3: Shard-based 方法天然抗攻击

GraphEraser 在所有 6 个攻击策略下 F1 Drop 均为负值（遗忘后性能反而提升），证明分片聚合架构对定向攻击具有天然免疫力。推测原因：分片独立训练+聚合的架构使得单个节点的移除只影响其所在分片，聚合机制可以补偿局部损失。

### 发现 4: 最佳攻击策略因 Pipeline 而异

不存在一个"万能"攻击策略。IM 在 Learning-based（GNNDelete, 2.03x）上最强，Hybrid 在 IF-based（GIF, 3.00x）上最强，Shard-based 对所有策略免疫。这意味着自适应攻击（根据目标方法选择策略）是必要的研究方向。

### 发现 5: Pipeline 类型影响脆弱性模式

从 Step 0 数据可以观察到：
- **Learning-based 方法** (GNNDelete, MEGU, GUKD, D2DGN, SGU) 脆弱性分化最大（0.37% ~ 8.31%），取决于具体的遗忘机制设计
- **Shard-based 方法** (GraphEraser, GraphRevoker, GUIDE) 两极分化：GraphEraser/GraphRevoker 中等（2.40%），GUIDE 完全免疫（0.00%）
- **IF-based 方法** (GIF, IDEA) 中等且一致（2.03% ~ 2.22%）
- **独立实现** (Projector) 高危（5.90%）

---

## 5. 下一步计划

### Phase A: 系统性攻击对比实验（部分完成）

6 策略 × 3 方法矩阵已完成（见 Step 4+5 补充），GUIDE 对照组待补：

| | Random | Degree | PageRank | TracIn | IM | Hybrid |
|---|---|---|---|---|---|---|
| GNNDelete (高危) | ✅ 0.0683 | ✅ 0.0535 | ✅ 0.0535 | ✅ 0.0904 | ✅ **0.1384** | ✅ 0.0886 |
| GIF (中等) | ✅ 0.0092 | ✅ 0.0185 | ✅ 0.0129 | ✅ 0.0203 | ✅ 0.0166 | ✅ **0.0277** |
| GraphEraser (中等) | ✅ -0.0701 | ✅ -0.0443 | ✅ -0.0295 | ✅ -0.0480 | ✅ -0.0517 | ✅ -0.0627 |
| GUIDE (对照组) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

### Phase B: 跨数据集泛化验证

在 3 个数据集上验证攻击效果的泛化性：
- Cora (2,708 nodes, 已完成初步验证)
- Citeseer (3,327 nodes)
- Pubmed (19,717 nodes, 测试规模可扩展性)

### Phase C: Ratio 敏感性分析

对 Phase A 的最佳攻击组合，进一步分析 unlearn ratio 对攻击效果的影响曲线（0.01 ~ 0.2）。

### 后续研究方向

1. ~~**IF-IM Hybrid 策略**~~: **已实现并验证**（Step 5，GIF 上 3.00x 效果）
2. **自适应攻击策略**: 根据目标方法 pipeline 类型自动选择最佳攻击策略（发现 4 的直接延伸）
3. **MIA 评估**: 引入 Membership Inference Attack AUC 作为隐私泄露指标
4. **黑盒攻击**: 探索基于 GNNExplainer 的解释性方法作为完全黑盒攻击策略
5. **Collateral Damage**: 实现 retrain 逻辑，量化攻击对保留节点的附带损害

---

## 6. 附录

- [附录 A: 11 个方法的详细指标表](appendix_method_table.md)
- [附录 B: Demo 完整输出摘录](appendix_demo_output.txt)
- [Figure 1: 脆弱性排名图](figures/vulnerability_ranking.png)
- [Figure 2: 全方法 F1 曲线](figures/all_methods_combined.png)
- [Figure 3: 类别对比图](figures/category_comparison.png)
- [Figure 4: 时间-Ratio 关系图](figures/time_vs_ratio.png)
