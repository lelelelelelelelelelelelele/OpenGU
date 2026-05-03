# 宏观 Plan：Adversarial Attacks on Graph Unlearning

> Status: historical
> Role: 项目早期的长期规划文档，保留原始实验路线、模块拆分和阶段优先级。
> Use this when: 你想追溯项目最初是如何设计攻击方案和实验矩阵的。
> Superseded by: 当前 thesis 方向以 `thesis_transition_memo.md` 为准；方法与指标升级以 `plan_flow_v2_delta.md` 为准。
> See also: `PROJECT_MASTER_CONTEXT.md`, `plan_flow_v2_delta.md`, `../report/paper/stage_report_2026-02-27.md`

> **v2 增量补丁**：指标体系（§5）、实验方案（§4）已有增补（新增 collateral damage、Gap 统计显著性、实验判定标准等），见 [`plan_flow_v2_delta.md`](plan_flow_v2_delta.md)。本文件内容保持不变，增量变更记录于该文件。

## 1. 项目目标

通过精心选择一组节点 $D_{unlearn}$ 进行强制遗忘，诱导近似遗忘算法（Approximate Unlearning）发生性能塌缩（Performance Collapse），证明现有近似遗忘方法在对抗性场景下是脆弱的。

---

## 2. 核心方法：IF-IM 混合节点选择

### 2.1 两个维度

| 维度 | 捕捉内容 | 具体方法 |
|------|---------|---------|
| Influence Function (IF) | Feature-Model Interaction：节点特征对模型参数 $\theta$ 的敏感度 | TracIn (Gray-box), GNNExplainer (Black-box) |
| Influence Maximization (IM) | Structure Propagation：节点在图拓扑中的传播能力 | CELF 算法, Degree, PageRank |

### 2.2 融合方式

- **Linear fusion**: $Score(v) = \alpha \cdot \text{Norm}(IF(v)) + \beta \cdot \text{Norm}(IM(v))$
- **Rank-based fusion**: 对 IF 和 IM 分别排序，取 rank 加权和（对尺度不敏感）
- 消融实验比较两种融合方式，并分析 $\alpha / \beta$ 敏感性

### 2.3 从白盒到灰盒

| 方案 | 假设 | 方法 | 优先级 |
|------|------|------|--------|
| Plan A (Gray-box) | 可获取训练梯度 | TracIn: $\nabla \mathcal{L}_{train} \cdot \nabla \mathcal{L}_{test}$ | 首选 |
| Plan B (Black-box) | 仅能查询模型输出 | GNNExplainer / XAI score | 备选 |

---

## 3. 新建代码模块

### 3.1 目录结构

```
attack/
├── attack_strategies/                  # [新建] 攻击策略模块
│   ├── __init__.py
│   ├── base_strategy.py                # 抽象基类
│   ├── random_strategy.py              # Baseline: 随机选择
│   ├── degree_strategy.py              # Baseline: 度中心性
│   ├── pagerank_strategy.py            # Baseline: PageRank
│   ├── tracin_strategy.py              # 核心: TracIn pseudo-IF
│   ├── im_strategy.py                  # 核心: Influence Maximization (CELF)
│   └── hybrid_strategy.py             # 核心: IF-IM 混合策略
├── attack_manager.py                   # [填充] 策略注册与调度
├── attack_eval.py                      # [新建] 攻击效果评估工具
├── MIA_attack.py                       # [已有]
└── Attack_methods/                     # [已有]
```

### 3.2 各文件职责

| 文件 | 职责 |
|------|------|
| `base_strategy.py` | 定义 `BaseStrategy` 抽象类，统一 `select_nodes(data, model, k) -> List[int]` 接口 |
| `random_strategy.py` | 随机采样 k 个节点 |
| `degree_strategy.py` | 按节点度数降序选 top-k |
| `pagerank_strategy.py` | 按 PageRank 值降序选 top-k |
| `tracin_strategy.py` | 计算 TracIn score，选 top-k；内部封装梯度点积计算 |
| `im_strategy.py` | 基于 CELF 贪心算法做 Influence Maximization，选 top-k |
| `hybrid_strategy.py` | 融合 IF score 和 IM score，支持 linear / rank-based fusion |
| `attack_manager.py` | 类似 `UnlearningManager`，通过字符串映射实例化策略类 |
| `attack_eval.py` | 封装 F1 drop、MIA AUC、与 retrain 对比等评估逻辑 |

---

## 4. 实验计划

### Phase 1: 基础设施 + Baseline

| # | 实验 | 数据集 | 模型 | 遗忘方法 | 攻击策略 | 目标 |
|---|------|--------|------|---------|---------|------|
| 1 | Random baseline | Cora | GCN | GIF | Random | 确认 pipeline 跑通，记录 F1 drop 基准 |
| 2 | Random baseline | Cora | GCN | GST | Random | 同上 |
| 3 | Degree baseline | Cora | GCN | GIF, GST | Degree | 结构启发式对比 |
| 4 | PageRank baseline | Cora | GCN | GIF, GST | PageRank | 结构启发式对比 |

### Phase 2: 核心攻击验证（Cora 快速迭代）

| # | 实验 | 攻击策略 | 遗忘方法 | 说明 |
|---|------|---------|---------|------|
| 6 | TracIn 单独 | TracIn | GIF | 验证 pseudo-IF 是否优于 random |
| 7 | IM 单独 | CELF-IM | GIF | 验证结构指标有效性 |
| 8 | Hybrid | IF-IM Hybrid | GIF | 验证混合优于单一指标 |
| 9 | 融合消融 | Linear vs Rank-based | GIF | 比较融合方式 |
| 10 | 超参消融 | $\alpha/\beta$ grid | GIF | 验证超参敏感性 |

### Phase 3: 泛化性验证

| # | 实验 | 变量 | 固定条件 | 说明 |
|---|------|------|---------|------|
| 11 | 跨遗忘方法 | GIF, GST, GNNDelete, MEGU | Cora, GCN | 攻击对不同方法的效果 |
| 12 | 跨数据集 | Cora, Citeseer, PubMed, Physics | GCN, GIF | 数据集泛化性 |
| 13 | 跨模型 | GCN, GAT, GIN | Cora, GIF | 模型泛化性 |
| 14 | Unlearn ratio | 1%, 5%, 10%, 20% | Cora, GCN, GIF | 比例敏感性 |
| 15 | Retrain 对比 | 攻击后 vs 精确重训 | Cora, GCN, GIF | 量化近似误差贡献 |

### Phase 4: 对照 + MIA

| # | 实验 | 说明 |
|---|------|------|
| 16 | GraphEraser 抗攻击 | Shard-based 方法抗攻击能力（预期强于 IF-based） |
| 17 | MIA 评估 | 攻击后模型 MIA AUC |

---

## 5. 评估指标

| 指标 | 含义 | 预期 |
|------|------|------|
| F1 Drop (%) | 遗忘后 vs 遗忘前在 $D_{test}$ 上的 F1 变化 | 攻击策略 >> Random |
| MIA AUC | 成员推断攻击 AUC | 偏离 0.5 表示信息残留/泄露 |
| Selection Time (s) | 节点选择算法耗时 | TracIn < 原始 IF |
| Retrain Gap | 攻击后 F1 - Retrain 后 F1 | 正值越大 → 近似误差越大 |

---

## 6. 优先级

```
高优先级（搭骨架 + 跑通 baseline）:
  ├── base_strategy.py + random/degree/pagerank
  ├── attack_manager.py
  ├── Phase 1 实验
  └── tracin_strategy.py

中优先级（验证核心假设）:
  ├── im_strategy.py + hybrid_strategy.py
  ├── Phase 2 实验
  └── attack_eval.py

低优先级（扩展论文完整性）:
  ├── Phase 3 & 4 实验
  └── GNNExplainer (Plan B)
```

---

## 7. 注意事项

1. **TracIn 适配 GNN**: 节点不独立，一个节点的梯度受邻居影响。先用 node-level gradient dot product 做 baseline，再考虑邻域处理。
2. **IF-IM 融合**: 线性加权的 $\alpha/\beta$ 选择问题——优先尝试 rank-based fusion 避免尺度问题。
3. **Retrain 作为 ground truth**: 每组实验必须有 retrain from scratch 对照，这是证明"攻击利用了近似误差"的直接证据。
4. **数据集多样性**: 不能只用引文网络，至少加一个 Physics 或 ogbn-arxiv。
5. **ScaleGUN**: 在 `unlearning_manager.py` 中被注释掉，暂不纳入实验。
