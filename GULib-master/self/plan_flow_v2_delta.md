# plan_flow_v2_delta.md — 增量更新文档

> Status: reference
> Role: `flow.md` 与 `宏观plan.md` 的 v2 补丁层，集中记录归因框架、collateral damage、Gap 显著性和实验设计升级。
> Use this when: 你需要查当前项目最关键的方法学升级，尤其是 attribution 和多指标评估。
> See also: `flow.md`, `宏观plan.md`, `thesis_transition_memo.md`, `../report/progress/0417_5003report/main_report/msc_project_report.md`

> 本文件是 `flow.md` + `宏观plan.md` 的增量补充（v2 delta）。
> 创建于 2026-02-19，记录 Step 7 (eval 模块) 设计讨论中产生的新论点、新设计和新指标。
> **原则：`flow.md` 和 `宏观plan.md` 是项目基础文档，不直接改动。所有增量变更记录于此。**
>
> **`update.md` 吸收声明**：`update.md` 是讨论过程中的临时文件，其全部有价值内容已融入本文件（§2 归因框架、§6 实验判定）。后续以本文件为准，`update.md` 不再更新。
>
> **`paper_library_synthesis` 吸收声明**：`paper_library_synthesis_2026-02-16.md` 中与实验设计直接相关的已采纳结论（§1.5 Experiment Checklist 的指标集、消融矩阵、核心图表清单；Thread A 的归因对照组角色；Thread D + Reviewer Checklist #5 的多指标原则）已融入本文件（§3 指标集汇总、§6 Phase 2 增补、§6.4 核心图表清单）。原文件作为文献详细卡片和 Related Work 素材继续保留，不做删改。

---

## 1. 文档定位

| 本文件章节 | 对应 v1 文档 | v1 章节 | 关系 |
|-----------|-------------|--------|------|
| §2 归因框架升级 | `flow.md` | §5.3 `evaluate_retrain_gap()` | 扩展 |
| §3 新增指标 | `宏观plan.md` | §5 指标体系 | 新增 |
| §4 指标命名统一 | `flow.md` | §5 全局 | 修正 |
| §5 Eval 模块差异 | `flow.md` | §5 + Step 7 实现 | 对照 |
| §6 实验设计更新 | `宏观plan.md` | §4 实验方案 | 增补 |
| §7 Future Work | 新增 | — | 新增 |
| §8 代码状态快照 | 新增 | — | 新增 |

补充来源：`update.md`（归因框架理论，**已吸收**）、`paper_library_synthesis_2026-02-16.md`（文献启发）、Step 7 实现讨论。

> **双向绑定**：`flow.md` 和 `宏观plan.md` 头部已各加一行指针指向本文件。本文件不替代原文档，而是作为其 v2 补丁层。

---

## 2. 归因框架升级

> 对应 `flow.md` §5.3 + `update.md`（已吸收）

### 2.1 核心立场（源自 `update.md`）

我们不预设"近似遗忘一定存在漏洞"，而是提出并检验一个**可证伪假设**：在相同删除请求下，近似遗忘方法相对于 retrain-after-deletion 是否出现稳定的额外性能损失（Approximation Gap）。

- **RQ**：近似遗忘的性能下降，多少来自"删除集本身"，多少来自"近似误差"？
- **H1**：存在稳定正的 Approximation Gap。
- **H0**：Approximation Gap ≈ 0。

> **一句话版本（组会可用）**：我们的贡献不是"发明了更强选点启发式"，而是建立了一套可证伪的归因框架，用来区分"删除集本身造成的损失"与"近似遗忘额外引入的误差损失"。

### 2.2 v1 → v2 变更

**v1 (flow.md §5.3)**：`evaluate_retrain_gap()` 接收 2 个模型 (unlearned, retrained)，返回 `{f1_unlearned, f1_retrained, gap, gap_pct}`。

**v2 升级**：

- 接收 **3 个模型**：`model_before`, `model_unlearned`, `model_retrained`
- 分解公式：

```
Total = Drop_retrain + Gap
      = (Perf_before - Perf_retrain) + (Perf_retrain - Perf_unlearn)
      = Perf_before - Perf_unlearn
```

| 分量 | 公式 | 含义 |
|------|------|------|
| `Drop_retrain` | `Perf_before - Perf_retrain` | 删除集的应有损失（retrain 也会有的损失） |
| `Gap` | `Perf_retrain - Perf_unlearn` | 近似遗忘的额外损失 = **over-forgetting** |
| `Total` | `Perf_before - Perf_unlearn` | 总性能下降 |

- 返回 6 个字段：`perf_before, perf_retrain, perf_unlearn, drop_retrain, gap, gap_pct`

**评估集合约定**：

| 评估集 | 定义 | 用途 |
|--------|------|------|
| **主评估集** `test_mask` | 标准 test split（含 retained + unlearned test nodes） | 论文主表，与标准 GU 评估对齐 |
| **辅评估集** `retained_test_mask` | `test_mask & ~unlearn_mask`（仅 retained test nodes，排除被删节点） | 辅助分析，更严格的 collateral-only 视角 |

> - 论文主表报 `test_mask` 上的 Perf/Gap（与现有 GU 文献对齐，reviewer 可直接比较）
> - 辅助分析报 `retained_test_mask`（排除被删节点后，更纯粹地反映波及效应）
> - Collateral Damage (#5) 始终在 `retain_mask`（训练+测试中的保留节点）上评估，与上述 test-only 评估集互补

**over-forgetting 定义**：`Gap > 0` 表示近似遗忘"过度遗忘"，即删除了比应有量更多的模型知识。这是攻击可利用的核心漏洞。

---

## 3. 新增指标

> 对应 `宏观plan.md` §5 的扩展

### v2 完整指标集（最小指标集，6 类）

> 来源：`paper_library_synthesis` Thread D + Reviewer Checklist #5 的核心结论——仅靠 MIA AUC 无法全面评估攻击效果（GraphToxin 的批评）。以下 6 类指标构成 v2 的**最小指标集**，论文实验必须全部覆盖，不可仅报告子集。

| # | 指标类别 | 核心量 | 含义 | 实现位置 |
|---|---------|--------|------|---------|
| 1 | **F1 Drop** | `f1_before - f1_after` | 攻击导致的直接性能下降 | `attack_eval.py::evaluate_f1_drop()` |
| 2 | **MIA AUC** | ROC-AUC | 隐私泄漏信号（MIA 成功率） | `attack_eval.py::evaluate_mia()` |
| 3 | **Selection Time** | 秒 | 攻击策略的计算开销 | `attack_manager.py` 计时 |
| 4 | **Approximation Gap** | `Perf_retrain - Perf_unlearn` | 单次运行的近似遗忘额外损失（over-forgetting）及 3-model 归因分解 | `attack_eval.py::evaluate_retrain_gap()`（单 run） |
| 5 | **Collateral Damage** | `mean_pred_shift`, `fraction_flipped` | 保留节点上 unlearn vs retrain 的预测差异（隔离近似误差的波及效应） | `attack_eval.py::evaluate_collateral_damage()` |
| 6 | **Gap 统计显著性** | t-test p-value, 95% CI | 多 seed（≥5）聚合：Gap 是否显著大于 0 的假设检验 | `attack_eval.py::compute_gap_statistics()`（跨 run 汇总） |

> **设计原则**：指标 1-2 衡量攻击效果，指标 3 衡量攻击可行性，指标 4-6 提供归因证据。缺少任一类都会被 reviewer 质疑（参见 synthesis Reviewer Checklist #5："multi-metric leakage — don't rely solely on MIA AUC"）。
>
> **#4 vs #6 分工**：#4 = 单 run 归因分解（`evaluate_retrain_gap()` 返回单次 Gap 值及 3-model 分解），#6 = 跨 run 假设检验（`compute_gap_statistics()` 聚合多 seed 的 Gap 值做 t-test）。两者输入输出不同，不重叠。

---

**v1 指标（4 个）**：F1 Drop, MIA AUC, Selection Time, Retrain Gap

**v2 新增（2 个）**：

### 3.1 Collateral Damage（UtU-style Δp）

衡量**保留节点**上 `model_unlearned` 与 `model_retrained` 的预测差异，隔离近似误差的波及效应。

**关键设计**：主对比对象为 `model_unlearned` vs `model_retrained`（而非 before vs after）。两者共享同一删除集 S，因此差异纯粹来自近似误差——若用 before vs after，会把"删除本身导致的合理预测变化"混入 collateral damage，导致指标不纯。

| 子指标 | 含义 |
|--------|------|
| `mean_pred_shift` | 保留节点上 unlearn 与 retrain 预测概率偏移的均值（L-inf per node, 再取 mean） |
| `max_pred_shift` | 保留节点中最大的预测概率偏移 |
| `fraction_flipped` | 保留节点中 unlearn 与 retrain 预测类别不一致的比例 |

- **函数签名**：`evaluate_collateral_damage(model_unlearned, model_retrained, data, retain_mask)`
- **动机**：攻击的理想效果不仅是拉低全局 F1，还要观察近似误差对未被删除节点的波及程度
- **已实现**：`attack/attack_eval.py::evaluate_collateral_damage()`

### 3.2 Gap 统计显著性

多 seed Gap 值的 one-sample t-test（H0: Gap = 0）。

| 子指标 | 含义 |
|--------|------|
| `mean` | Gap 均值 |
| `std` | Gap 标准差 |
| `ci_lower`, `ci_upper` | 95% 置信区间（z = 1.96） |
| `p_value` | t-test p 值 |
| `reject_h0` | `p_value < 0.05` 时为 True |

- **动机**：支持 `update.md` 的可证伪假设检验——若 Gap 不显著则拒绝漏洞假设
- **已实现**：`attack/attack_eval.py::compute_gap_statistics()`

---

## 4. 指标命名统一

> 对应 `flow.md` §5 全局

v1 中存在命名不一致（如 `f1_unlearned` vs `perf_unlearn`）。v2 统一为以下约定：

| 统一名称 | 含义 | 评估集合 | 出处 |
|----------|------|---------|------|
| `Perf_before` | 删除前性能 | `test_mask`（主）/ `retained_test_mask`（辅） | `update.md` |
| `Perf_retrain` | 重训后性能 | `test_mask`（主）/ `retained_test_mask`（辅） | `update.md` |
| `Perf_unlearn` | 近似遗忘后性能 | `test_mask`（主）/ `retained_test_mask`（辅） | `update.md` |
| `Drop_retrain` | `Perf_before - Perf_retrain` | 同上 | `update.md` |
| `Gap` | `Perf_retrain - Perf_unlearn` | 同上 | `update.md` |
| `f1_before` / `f1_after` | F1 Drop 函数内部使用 | `test_mask` | `attack_eval.py` |
| `mean_pred_shift` / `fraction_flipped` | Collateral Damage | `retain_mask` | `attack_eval.py` |

> 注意：`evaluate_f1_drop()` 内部仍用 `f1_before`/`f1_after`，因为该函数关注的是任意两模型的 F1 差异，不涉及 3-model 归因。两套命名不冲突。

---

## 5. Eval 模块实现差异总结

> 对应 `flow.md` §5 + Step 7 实现

| 项目 | flow.md v1 | 实际实现 v2 |
|------|-----------|------------|
| 公开函数数 | 3 | 5 |
| `evaluate_retrain_gap` 参数 | 2 个模型 (unlearned, retrained) | 3 个模型 (before, unlearned, retrained) |
| `evaluate_retrain_gap` 返回 | 4 字段 | 6 字段 |
| collateral damage | 无 | `evaluate_collateral_damage()` |
| 统计检验 | 无 | `compute_gap_statistics()` |
| `_predict` helper | 无 | 统一处理 `f(x)` / `f(x, edge_index)` 签名差异 |
| config.py 依赖 | 未明确 | **明确无依赖**（纯函数设计） |
| 外部依赖 | sklearn | sklearn + scipy.stats |

---

## 6. 实验设计更新

> 对应 `宏观plan.md` §4 的增补 + `update.md` 实验判定标准（已吸收）

### 实验判定标准（最小可行，源自 `update.md`）

1. 固定同一删除集 S，同时跑 Retrain 和 Unlearn
2. 对多 seed 计算 Gap 的均值、置信区间、显著性
3. 若 Gap 在多设置下显著大于 0 → 支持漏洞假设（H1）
4. 若 Gap 不显著 → 拒绝漏洞假设，结论转为"主要是删除重要性效应"（H0）

### 结果叙事（两种都可发表，源自 `update.md`）

- **若支持 H1**：近似误差是关键脆弱性来源，攻击者可通过选择性删除放大此误差
- **若支持 H0**：当前系统主要受删除集重要性影响，近似误差不是主导因素——这本身也是有价值的发现

### Phase 2 增补

- 每组实验**必须同时跑 Retrain 和 Unlearn**，计算完整的 Gap 分解
- 多 seed (>=5) 运行，用 `compute_gap_statistics()` 做假设检验
- 结果叙事遵循上述双向逻辑

#### Partition-based 方法作为归因对照组

> 来源：`paper_library_synthesis` Thread A 的核心结论。

GraphEraser / GraphRevoker 等 partition-based 方法在实验中的角色**不是**"又一个被攻击目标"，而是**归因对照组**。具体逻辑：

- 若同一删除集 S 下，partition-based 方法（GraphEraser / GraphRevoker）抗住了攻击（F1 Drop 小、Gap ≈ 0），而 IF-based 方法（GIF/GST）出现显著塌缩（Gap >> 0），则证明塌缩**源于近似误差**而非删除集本身的节点重要性。
- 这直接回应 reviewer 最可能的质疑："you are just removing important nodes"（synthesis Reviewer Checklist #1 + Gap 1 biggest risk）。
- 实验报告中，partition-based 结果应与 approximate 结果**并排呈现**，而非分开讨论。

#### 消融矩阵明细

> 来源：`paper_library_synthesis` §1.5 Experiment Checklist — Ablations 项。

Phase 2 消融实验须覆盖以下维度，构成完整消融矩阵：

| 消融维度 | 变量 | 目的 |
|---------|------|------|
| 策略组件 | IF-only vs IM-only vs Hybrid | 证明融合优于单一组件 |
| 融合方式 | linear combination vs rank fusion | 验证融合函数的选择敏感性 |
| 融合权重 | α/β sweep (0.0–1.0, step 0.2) | 找到最优权重区间并验证鲁棒性 |
| 删除预算 | K = {5, 10, 20, 50, 100} 或按 ratio | 绘制 attack success vs budget 曲线 |
| 删除比例 | unlearn_ratio = {0.01, 0.05, 0.10, 0.20} | 验证攻击在不同强度下的表现 |
| 随机稳定性 | >=5 seeds, 报告均值 ± std | 排除随机波动 |
| 节点位置 | boundary-node vs core-node | 对 partition-based 方法尤其重要：跨分区边界节点可能放大攻击效果 |

#### Threat Model Table（Phase 2 必做）

论文须包含明确的 Threat Model 描述，成本低但 reviewer 基本必问。

| 维度 | 选项 | 本文设定 |
|------|------|---------|
| 攻击者能力 | 自有节点注入（inject） / 任意节点选择（select） | select（攻击者可提交删除请求指定任意自有节点） |
| 信息获取 | white-box / gray-box（可查询模型） / black-box（仅观察输出） | gray-box（可获取模型预测概率，用于 TracIn/MIA） |
| 删除请求渠道 | 法规驱动（GDPR）/ 平台自助 / API | 法规驱动（合理性：用户可依据 GDPR 请求删除自己的数据） |
| 攻击者目标 | 模型性能下降 / 隐私泄漏 / 两者兼顾 | 两者兼顾（F1 Drop + MIA AUC 同时评估） |

> **注意**：上表中"本文设定"列为初始设定，Phase 2 实验中可能根据结果调整。最终版本以论文 §3 Threat Model 为准。

### Phase 3 增补

- 每组跨方法/跨数据集实验增加 **collateral damage 报告**
- 对比不同近似遗忘方法的 over-forgetting 程度排序
- 绘制 Gap vs Collateral Damage 散点图，观察两个维度是否正相关

### 6.4 核心图表清单（论文最小图表集）

> 来源：`paper_library_synthesis` §1.5 Experiment Checklist — Core tables/figures 项。

论文至少需要以下 5 类图表。前 4 类为 **must**，第 5 类为 **optional but strong**。

| # | 图表类型 | X 轴 | Y 轴 / 内容 | 支撑论点 |
|---|---------|------|-------------|---------|
| 1 | **Attack Success vs Deletion Budget** | 删除预算 K | F1 Drop（各策略分线） | 证明攻击随预算增长的有效性，对比策略间差异 |
| 2 | **Approximation Gap vs Deletion Budget** | 删除预算 K | Gap = Perf_retrain - Perf_unlearn | 证明 Gap 随预算增长而放大（核心归因证据） |
| 3 | **Cross-GU-Family Robustness Summary Table** | GU 方法族（行）× 攻击策略（列） | F1 Drop + Gap 双指标 | 证明不同 GU 族的脆弱性差异，partition-based 作为对照 |
| 4 | **Efficiency vs Attack Strength Trade-off** | Selection Time | F1 Drop 或 Gap | 证明高级策略（IF/IM/Hybrid）相比基线的效率-效果权衡 |
| 5 | **Sequential Deletion Curves** (optional) | 删除轮次 (round) | 累积 F1 / 累积 Gap | 展示多轮删除下 Gap 的累积效应（若实现 sequential protocol） |

> **使用建议**：图表 1-2 可合并为左右子图；图表 3 为主表格（Table 1 候选）；图表 4 可用散点图 + Pareto 前沿标注；图表 5 作为补充实验或 appendix。

---

## 7. Future Work / 备选实验

> 来自 `paper_library_synthesis` 讨论的启发，暂不实现，记录备查

1. **Influence 校准协议**
   - TracIn top-k 节点逐个 retrain-without 验证 actual influence
   - 报告 Spearman ρ（TracIn score 排序 vs actual influence 排序）
   - 目的：验证 TracIn 选点策略的理论基础是否成立

2. **NIM/SGU baseline**
   - 若 `2501.11823` 有公开代码，可作为第 7 个 strategy
   - 与现有 6 个 strategy 做对比

3. **Sequential unlearning**
   - 2-3 轮连续删除，展示 Gap 累积效应
   - 验证假设：多轮近似遗忘是否导致 Gap 单调递增

---

## 8. v3 增量：候选指标扩展（2026-02-19）

> **状态**：仅记录备查，不纳入最小指标集。视实验进展和论文需求决定是否实现。
> **动机**：v2 最小指标集（6 类）覆盖了 efficacy / utility / locality / fidelity / efficiency 五个维度，但在以下方面仍有盲区。这些指标在现有 GNN unlearning 论文中较少出现，属于潜在的差异化贡献点。

### 8.1 维度覆盖审计

| 维度 | v2 指标 | 覆盖程度 | v3 候选补充 |
|------|---------|----------|------------|
| **Efficacy** (模型是否真正遗忘) | MIA AUC (confidence-based) | 部分 — 仅用 max softmax，未检查遗忘节点的具体预测行为 | Forgotten Node Accuracy (#8.2) |
| **Utility** (保留数据性能) | F1 Drop | ✓ 充分 | — |
| **Locality** (影响范围控制) | Collateral Damage (pred_shift, fraction_flipped) | 全局聚合 — 未考虑图距离的空间衰减 | Hop-distance Decay (#8.3) |
| **Fidelity** (与 retrain 接近度) | Retrain Gap, Gap Statistics | ✓ 充分 | — |
| **Efficiency** (计算开销) | Selection Time, Unlearn Time | ✓ 充分 | Budget Efficiency (#8.4) |
| **Stealthiness** (攻击隐蔽性) | 无 | ❌ 完全缺失 | Stealthiness (#8.5) |

### 8.2 Forgotten Node Accuracy（Efficacy 补充）

**问题**：MIA AUC 衡量的是隐私泄漏，但没有直接回答"模型是否还记得被删节点"。

**定义**：

```
FNA = Accuracy(model_unlearned, data, unlearn_mask)
```

遗忘后，模型在被删除节点上的预测准确率。

| 场景 | FNA 表现 | 含义 |
|------|---------|------|
| 理想遗忘 | FNA ≈ 1/C (随机猜测) | 模型完全忘记了这些节点 |
| 不完全遗忘 | FNA ≈ Acc_before | 模型仍然"记得"，遗忘失败 |
| 攻击场景 | FNA 介于两者之间 | 可与 retrain 后的 FNA 对比，量化近似误差 |

**实现难度**：极低，已有 `_predict` 和 `f1_score` 基础设施，加一个 mask 即可。

**论文价值**：中等。补全 efficacy 维度的直觉性指标，但多数 GNN unlearning 论文不报告此指标（它们通常假设遗忘有效，关注的是 utility preservation）。对于攻击论文，展示"攻击选点使得遗忘更不彻底"可以是一个附加论点。

**决策条件**：若 MIA AUC 在实验中区分度不够（多数方法 AUC ≈ 0.5），则实现此指标作为替代 efficacy 度量。

### 8.3 Hop-distance Collateral Decay（Locality 补充，GNN 特有）

**问题**：当前 collateral damage 是全局聚合值（mean/max over all retained nodes），丢失了图结构上的空间信息。

**定义**：

```
对 hop ∈ {1, 2, 3, >3}:
    nodes_at_hop = BFS(unlearn_nodes, hop) ∩ retain_mask
    collateral_at_hop = fraction_flipped(model_unlearned, model_retrained, nodes_at_hop)
```

按距离遗忘节点的跳数分组，报告每组的 collateral damage。

**预期结果**：

```
hop=1: fraction_flipped = 0.15  (直接邻居，受影响最大)
hop=2: fraction_flipped = 0.06  (二阶邻居，衰减)
hop=3: fraction_flipped = 0.01  (三阶，接近零)
hop>3: fraction_flipped ≈ 0     (远处节点几乎不受影响)
```

**实现难度**：中等。需要 BFS 按跳数分层（PyG 的 `k_hop_subgraph` 或手写 BFS），然后对每层分别计算 collateral 指标。

**论文价值**：高。这是 GNN unlearning 论文中极少有人做的分析，直接利用了图结构特性解释 collateral damage 的传播机制。可以画成衰减曲线图，视觉冲击力强。

**与消息传递层数的关系**：GNN 的感受野由层数决定（L 层 GCN 的感受野 = L-hop）。若 collateral damage 在 L-hop 外趋近于零，说明 GNN 的消息传递范围恰好界定了 collateral damage 的影响半径。这个观察本身就可以作为一个 insight。

**决策条件**：若论文需要 GNN-specific 贡献点（区别于通用 ML unlearning 攻击），优先实现此指标。

### 8.4 Budget Efficiency（Efficiency 补充）

**问题**：当前 F1 drop 是固定 ratio 下的绝对值，无法比较不同预算下攻击的"性价比"。

**定义**：

```
Efficiency = F1_drop / k           # 每节点边际损害
MinBudget(τ) = min k s.t. F1_drop ≥ τ   # 达到阈值 τ 所需最少节点
```

**实现难度**：极低。`Efficiency` 只需除法；`MinBudget` 需要 ratio 敏感性实验（Phase C）数据，从曲线上读取。

**论文价值**：中等。在 ratio 敏感性实验（Phase C）中自然可得，无需额外实验，但能回答 reviewer 的"攻击实际可行吗"问题。

**决策条件**：Phase C ratio 敏感性实验完成后自然可计算，不需要单独决策。

### 8.5 Stealthiness（攻击隐蔽性，全新维度）

**问题**：当前框架完全没有从防御者视角评估攻击。如果攻击选择的节点在统计上与正常删除请求有显著差异，防御者可以检测并拒绝。

**可能的度量**：

```
# 攻击选点 vs 随机选点的统计可区分性
KS_degree = KS_test(degree[attack_nodes], degree[random_nodes])
KS_pagerank = KS_test(pagerank[attack_nodes], pagerank[random_nodes])
# p < 0.05 → 攻击可被检测
```

**实现难度**：低。KS 检验用 scipy 一行代码。

**论文价值**：中高。攻击论文的 completeness 指标——展示"攻击不仅有效，而且难以检测"。但如果 TracIn/IM 选出的节点确实与随机节点统计特征显著不同（很可能如此），那这个指标反而会暴露攻击的弱点，需要谨慎处理叙事。

**决策条件**：
- 若 reviewer 质疑 "defender can just filter abnormal deletion requests" → 必须回应，实现此指标
- 若不被质疑 → 可放入 limitation / future work 讨论

### 8.6 v3 候选指标优先级总结

| 优先级 | 指标 | 触发条件 | 工作量 |
|--------|------|----------|--------|
| ★★★ | Hop-distance Decay (#8.3) | 需要 GNN-specific 贡献点 | 中 |
| ★★☆ | Forgotten Node Accuracy (#8.2) | MIA AUC 区分度不够 | 极低 |
| ★★☆ | Budget Efficiency (#8.4) | Phase C 完成后自动可得 | 极低 |
| ★☆☆ | Stealthiness (#8.5) | Reviewer 质疑隐蔽性 | 低 |

---

## 9. 代码状态快照

> 截至 2026-02-19（v3 更新）

| Step | 状态 | 关键产出 |
|------|------|---------|
| 0 | ✅ | 15 方法兼容性矩阵 (11/15 通过) |
| 1-3 | ✅ | Random/Degree/PageRank + AttackManager (tag: `v0.1-baseline`) |
| 4 | ✅ | TracIn 策略 + 攻击基础设施 |
| 5 | ✅ | IMStrategy (CELF) + HybridStrategy (tag: `v0.2-core`) |
| 6 | — | (无独立 step 6) |
| 7 | ✅ | `attack/attack_eval.py` (5 函数, 18 测试全通过) |
| 8 | ✅ | Retrain 基础设施: `train_only` flag + `pipeline_adapter.py` + `eval_collateral.py` (110 tests, 0 failures) |
| 9 | ⏳ | 待执行实验 (Phase A+ collateral → Phase B 跨数据集 → Phase C ratio 敏感性) |
