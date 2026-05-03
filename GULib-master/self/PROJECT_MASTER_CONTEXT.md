# PROJECT_MASTER_CONTEXT.md

> Status: reference
> Role: 项目总背景与早期统一口径文档；保留原始研究目标、攻击思路和实现概览。
> Use this when: 你需要回看项目的原始 framing、方法族划分、攻击策略设计或 repo 层面的总背景。
> Superseded by: `thesis_transition_memo.md` 用于当前 thesis 方向；课程结论以 `../report/0417_5003report/main_report/msc_project_report.md` 为准。
> See also: `README.md`, `flow.md`, `../report/paper/stage_report_2026-02-27.md`

## 1. 项目概览 (Project Overview)

*   **项目名称**: Adversarial Attacks on Graph Unlearning (GNN 遗忘攻击研究)
*   **当前阶段**: 实验评估与论文写作阶段
*   **核心目标**:
    *   设计一种针对 **GNN Unlearning（图遗忘学习）** 的攻击机制。
    *   通过精心选择一组节点（$D_{unlearn}$）进行强制遗忘，诱导模型发生 **灾难性遗忘 (Catastrophic Forgetting)** 或 **性能塌缩 (Performance Collapse)**。
    *   证明现有的近似遗忘算法（Approximate Unlearning）在特定攻击下是脆弱的。
*   **基础框架**: 基于 `bwfan-bit/OpenGU` (Open Graph Unlearning) 进行二次开发。

---

## 2. 核心假设与思维路径 (Hypothesis & Reasoning)

### 2.1 攻击动机
现有的 GNN Unlearning 研究多关注"如何遗忘"，而忽略了"遗忘机制的安全性"。我的假设是：**并非所有数据点的遗忘代价都是相等的。** 存在某些"关键点（Structural & Feature-rich Anchors）"，一旦被强制移除，会导致模型对保留数据的推理能力大幅下降。

### 2.2 攻击目标与核心发现 (Attack Targets & Key Findings)
攻击目标覆盖两大类 GNN Unlearning 方法，通过对比实验揭示不同架构的脆弱性差异：

*   **Shard-based 方法（GraphEraser）**: 基于分区-聚合架构的精确遗忘方法。
    *   *攻击假设*: 移除关键分区中的高影响力节点可能破坏子模型质量。
    *   *实验发现*: 表现出 **"保护效应"**——unlearn 后 F1 不降反升或无显著下降，分区-聚合架构天然隔离了攻击传播。这一发现本身具有论文价值。
    *   *应对*: 引入 **Relative F1 Drop**（vs k=5 random baseline）作为归一化指标，使跨架构比较成为可能。
*   **近似遗忘方法（GIF/GNNDelete）**: 基于梯度更新或影响函数近似的方法。
    *   *攻击假设*: 这类方法依赖局部近似，存在数学上的不稳定性，可通过 IF 反向利用进行攻击。
    *   *实验发现*: **确实可被攻击**——策略性节点选择可造成显著 F1 下降，验证了核心假设。

### 2.3 方法论创新：IF-IM 混合机制 (The Hybrid Mechanism)
单一指标存在局限性，提出了 **IF-IM 混合选择策略**：
1.  **Influence Function (IF)**: 捕捉 **"Feature-Model Interaction"**。衡量节点特征对模型参数 $\theta$ 的敏感度。
    *   实现：**TracIn** (gray-box IF proxy) → `attack/attack_strategies/tracin_strategy.py`
2.  **Influence Maximization (IM)**: 捕捉 **"Structure Propagation"**。衡量节点在图拓扑中的传播能力（CELF 算法优化）。
    *   实现：**IM v4** (CELF-optimized) → `attack/attack_strategies/im_v4_strategy.py`
3.  **融合公式**: $Score(v) = \alpha \cdot \text{Norm}(IF(v)) + \beta \cdot \text{Norm}(IM(v))$
    *   实现：**Hybrid v4** (IF-IM fusion) → `attack/attack_strategies/hybrid_v4_strategy.py`

### 2.4 现实挑战与解决方案 (From White-box to Gray-box)
*   **挑战**: 原始 IF 计算需要 $H^{-1}$ (Hessian 逆) 和完整模型参数 $\theta$，属于强白盒攻击，且计算昂贵。
*   **解决方案 (Pseudo-IF)**:
    *   **Plan A (Gray-box, 已实现)**: **TracIn**。使用训练阶段的梯度点积近似 IF ($\nabla \mathcal{L}_{train} \cdot \nabla \mathcal{L}_{test}$)，避免求逆。已实现并在用。
    *   **Plan B (Black-box, 未追求)**: **GNNExplainer / XAI**。使用解释性模型的输出作为重要性得分。保留为 future work。

---

## 3. 技术栈与环境 (Technical Stack)

*   **Language**: Python 3.9+
*   **DL Framework**: PyTorch, PyTorch Geometric (PyG) 2.6.1
*   **Base Framework**: OpenGU
*   **Datasets**: Cora, Citeseer, PubMed, CS, Physics, Flickr, Photo, Computers, ogbn-arxiv
*   **Key Libraries**: `networkx`, `torch_scatter`, `torch_sparse`, `cvxpy`, `deeprobust`, `scikit-learn`, `ogb`
*   **Environment**: conda `gnn` 环境（包含所有依赖）

---

## 4. 项目进展 (Progress Summary)

### 已完成

1.  **攻击框架全模块实现**：9 个策略（random, degree, pagerank, tracin, im, im_v4, hybrid, hybrid_v4, base）+ AttackPipeline + ResultCache + SelectionCache
2.  **批量实验基础设施**：`run_experiments.py` Phase A/B/C + MG-0~3 实验脚本（`scripts/experiments/`）
3.  **MG-0 稳定性实验**：Cora/GCN, 4 method × 6 strategy × 5 seed
4.  **MG-1 跨数据集实验**：Citeseer/GCN
5.  **MG-2 跨模型实验**：Cora/GAT
6.  **MG-3 扩展实验**：Citeseer/GAT 等
7.  **Collateral damage 评估框架**：`eval_collateral.py`
8.  **相对指标计算**：`eval_relative.py`（vs k=5 random baseline）
9.  **发现 Shard 保护效应**：Shard-based 方法天然抵抗攻击，成为论文重要发现

### 当前聚焦

1.  k=5 基准实验完善
2.  论文 Results + Analysis 写作
3.  泛化实验补全（更多 dataset × model 组合）

---

## 5. 实验设计与评估体系 (Experimental Design)

### 5.1 攻击流程
1.  **Pre-train**: 训练标准 GNN 模型。
2.  **Select**: 使用攻击策略选出 Top-K 个节点作为 $D_{unlearn}$。支持 SelectionCache 缓存选择结果。
3.  **Unlearn**: 运行目标 Unlearning 算法移除 $D_{unlearn}$。支持 ResultCache 缓存 pipeline 结果。
4.  **Evaluate**: 评估遗忘后模型在 $D_{test}$ (保留集) 上的表现。

### 5.2 核心指标 (Metrics)
*   **F1 Score Drop**: Node Classification F1 下降幅度（vs 未遗忘基线）。
*   **Relative F1 Drop**: 相对于 k=5 random baseline 的归一化下降（由 `eval_relative.py` 计算）。
*   **MIA AUC**: Membership Inference Attack AUC（隐私泄露程度）。
*   **Retrain Gap**: 近似遗忘与精确重训练之间的性能差距。
*   **Collateral Damage**: 攻击对非目标节点的波及影响。
*   **Efficiency**: 节点选择算法的时间复杂度。

### 5.3 攻击策略 (Strategies)

| 策略 | 类型 | 文件 |
|------|------|------|
| Random | Baseline | `random_strategy.py` |
| Degree | Baseline | `degree_strategy.py` |
| PageRank | Baseline | `pagerank_strategy.py` |
| TracIn | Core (IF proxy) | `tracin_strategy.py` |
| IM v4 | Core (CELF) | `im_v4_strategy.py` |
| Hybrid v4 | Core (IF-IM fusion) | `hybrid_v4_strategy.py` |

另有早期版本 `im_strategy.py` 和 `hybrid_strategy.py` 保留在代码中。

### 5.4 实验矩阵设计

| 实验阶段 | 目标 | Dataset | Model | 内容 |
|----------|------|---------|-------|------|
| MG-0 | 稳定性 | Cora | GCN | 4 method × 6 strategy × 5 seed |
| MG-1 | 跨数据集 | Citeseer | GCN | 同 MG-0 策略组合 |
| MG-2 | 跨模型 | Cora | GAT | 同 MG-0 策略组合 |
| MG-3 | 扩展 | Citeseer | GAT | 交叉验证 |
| 泛化 | 覆盖 | 多数据集 | 多模型 | 全量组合 |

### 5.5 关键发现摘要

*   **Shard 保护效应**: GraphEraser 的分区-聚合架构天然隔离攻击传播，unlearn 后 F1 不降反升。这是本研究的重要发现，说明架构选择本身就是一种防御。
*   **GNNDelete 对 degree 敏感**: 基于度中心性的选择对 GNNDelete 有较强攻击效果。
*   **GIF 的 collateral 接近 0**: GIF 方法的攻击波及效应极小，说明其遗忘机制相对局部化。
*   **近似方法的脆弱性分层**: 不同近似方法对不同策略的敏感度存在显著异质性。
