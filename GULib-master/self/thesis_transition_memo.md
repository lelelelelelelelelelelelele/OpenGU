# Thesis Transition Memo

> Status: active
> Role: thesis 线的承上启下文档；连接 2026-02 阶段实验、2026-04 课程报告，以及后续解释性研究与 proposed 收束。
> Use this when: 你要决定 thesis 下一步研究问题、可检验假说、或如何从已完成课程报告过渡到 thesis。
> Last revised: 2026-05-03（合并 from_experiments_to_mechanisms 草稿的有价值增量；该草稿已删除。同日二次修订：用户确认可昼夜无休 + 租 GPU 跑 ogbn-arxiv 扩展，§5 执行计划重写）
>
> **状态/进度/bug/finding 的实时数据 → `self/dashboard/`**（本文件保留战略层；执行细节落到 dashboard 不再回写到本文件）
> See also: `README.md`, `PROJECT_MASTER_CONTEXT.md`, `../report/paper/stage_report_2026-02-27.md`, `../report/0417_5003report/main_report/msc_project_report.md`

## 1. Purpose

2026-04 的 `report/0417_5003report/` 已经完成 EE5003 课程报告线，后续不再把 thesis 的开放问题继续混入该 deliverable。

这份 memo 的作用是：

1. 固定课程报告已经稳定的结论
2. 把尚未闭合的机制解释问题转成可检验命题
3. 定义 thesis 下一阶段的双候选 proposed 方向
4. 给出在已有数据上可立即执行的验证清单（NeurIPS 4 天窗口下的现实路径）

## 2. What Has Been Established

以下结论已经可以作为 thesis 起点，而不是重新从零开始：

### 2.1 Family-level vulnerability spectrum 已建立

- approximate graph unlearning 在 adversarial deletion 下呈现明显 family difference
- GNNDelete 在已测设置中最脆弱
- GIF 相对稳定
- GraphEraser 在已测设置中呈现 shard protection pattern
- IDEA / MEGU 在已测设置中几乎不被攻击影响（解读见 §3.5）

稳定落点：

- `../report/paper/stage_report_2026-02-27.md`
- `../report/0417_5003report/main_report/msc_project_report.md`
- `../report/0417_5003report/ppt/final_15min_script.md`

### 2.2 FIG-4b Effect Size 数据快照

来自 `../report/0417_5003report/main_report/msc_project_report.md` 的 family × strategy effect size（相对 k=5 random baseline）：

| Family | TracIn | IM | Hybrid |
|--------|--------|-----|--------|
| GIF | +4.2 | +1.0 | +1.3 |
| GNNDelete | +3.8 | **+6.8** | +3.4 |
| GraphEraser | +1.3 | +3.2 | +4.1 |
| IDEA | -0.0 | +1.3 | +0.8 |
| MEGU | -0.3 | -0.0 | +1.3 |

可被论文直接引用的几个可见现象：

- GNNDelete 对 IM 异常敏感（+6.8），是 GIF 同位置（+1.0）的 ~7 倍
- GraphEraser 出现 Hybrid > IM > TracIn 的反向排序，与 GNNDelete 的 IM >> Hybrid >> TracIn 互为镜像
- GIF 上 TracIn (+4.2) 显著优于 IM (+1.0)，而 GNNDelete 上反过来——**不存在全局最优 selector**
- IDEA / MEGU 整行接近 0，需先回答 §3.5 才能决定是否进入主对比

> **重要前提**：以上数值的 cross-seed variance 必须先在 Phase 0（§5.1）确认稳定，否则后续所有解读失效。

### 2.3 Relative metric 的必要性已建立

- 直接看 raw utility drop 会误读 shard-based family
- `relative_f1_drop` 作为相对 `k=5 random baseline` 的指标，已成为跨 family 比较的关键口径

### 2.4 Attribution logic 已建立

- `retrain_gap` 用于分离删除集本身的影响与 approximate unlearning 的额外误差
- collateral metrics 用于度量 retained-set disturbance
- 这条归因链已经是当前项目最重要的方法论资产之一

### 2.5 Attack strategy comparison 已从"random vs smart"推进到"informed selectors among themselves"

- TracIn / IM / Hybrid 不存在统一全局最优
- selector effectiveness 是 method-dependent 的

## 3. What Remains Unresolved

课程报告已经回答了"是否存在 family-level vulnerability difference"，但尚未充分回答下面这些 thesis 级问题：

### 3.1 GNNDelete 为什么对 IM 极度脆弱？

是其梯度更新机制对结构中心节点本身敏感，还是其近似误差在 high-propagation 节点上被放大？

### 3.2 为什么 selector 效果是 family-specific 的？

- GIF：TracIn (+4.2) >> IM (+1.0)——为什么 feature/model interaction 比 structure propagation 更危险？
- GNNDelete：IM (+6.8) >> TracIn (+3.8)——为什么相反？
- GraphEraser：Hybrid (+4.1) > IM (+3.2) > TracIn (+1.3)——为什么"结构+特征"组合最有效？

### 3.3 GraphEraser 的"shard protection"是普遍鲁棒还是局部现象？

- 是否依赖 partition simplification 的特定条件
- 是否依赖 bridge / boundary / hub 节点的选择/回避

### 3.4 当前 attack signals 真的在刻画 mechanism weakness 吗？

- 还是只是 proxy for "important node deletion"？
- 这是 referee 必问问题

**预先反驳证据**（已存在数据，paper 直接引用）：

1. **跨 family selector 排序翻转**：GIF 上 TracIn (+4.2) >> IM (+1.0)；GNNDelete 上 IM (+6.8) >> TracIn (+3.8)。若 selector 只是 importance proxy，所有 family 排序应一致——不一致即证伪 proxy 假说。
2. **PageRank ≠ IM ≠ TracIn 的效果差**：MG-0 cora/GCN/r=0.05 上 GNNDelete×PageRank=10.83，×IM_v4=12.32，×TracIn=8.46。**3 个 selector 同样在"选 k 个节点"，但效果差距明显且方向不一致**。
3. **Jaccard 显示选点本质不同**：PageRank=1.0，IM_v4=0.13，TracIn=0.42——**物理上不是同一群节点**。
4. **family-specific 响应**：IDEA/MEGU 对所有 selector 几乎免疫（§3.5），若 selector 只是 importance proxy，免疫就解释不了——必然涉及 mechanism。

paper 里建议单列一节 "Are informed selectors just importance proxies?" 直接 preempt 这条 critique。

### 3.5 IDEA / MEGU 的 ~0 effect 该怎么解读？

**默认立场（2026-05-04 决定）：B. Mechanism-incomparable**

两个候选解释：

- **A. 真鲁棒**：unlearning 机制对 adversarial deletion 抵抗强
- **B. 不可比（DEFAULT）**：MEGU 保留 `x_unlearn` 节点特征只做参数微调；IDEA 的梯度型更新对节点选择不敏感——attack signals 在它们身上根本不适用，**但这不等于"安全"，只等于"当前 selector 信号失效"**

**为什么承诺 B 作为默认**：

- A 等于承认攻击对 IDEA/MEGU 失败——立场被动
- B 等于把 0 effect 转成 **mechanism finding**：paper 里写"We identify a class of GU methods (feature-retention, gradient-variant) whose architecture intrinsically dampens deletion-set-selection signals; future selectors must target their specific update rules"——立场主动，且有进一步 future work 钩子
- B 的代价：要写一节解释 mechanism 为什么免疫；候选解释已在本节给出
- A 不被否认，作为 supplementary audit：若 Phase B 有时间，对 IDEA/MEGU 跑额外 selector（如直接扰动 `x_unlearn` 或 gradient-objective-aware 选点）验证；若那也无效，A 才有支持

**FIG-4b 的处置**：保留 5 行，但 IDEA/MEGU 那两行加阴影/标注 "mechanism-incomparable family"；caption 里明确说明。

**这是 framing 决定**——数据本身（5 个 cell 接近 0）已经稳定，不是数据缺失。

## 4. Testable Hypotheses

每条假说都给出**支持判据**和**证伪判据**，避免退化成 post hoc story。

### H1. Propagation Reach Hypothesis

**命题**：删除目标的传播范围越大，越容易造成 retained-set damage。

**可观测方向**：spread / topology influence 与 `fraction_flipped`、`mean_pred_shift` 是否正相关；这种相关性在不同 family 上是否强弱不同。

**支持判据**：在至少 2 个 family（含 GNNDelete）上 Spearman ρ > 0.4；GNNDelete 的 ρ 显著大于 GIF。
**证伪判据**：所有 family 的 ρ < 0.2，或 ρ 方向不一致。

### H2. Training Influence Hypothesis

**命题**：删除目标的 training influence 或 gradient alignment 越强，越容易放大 approximate unlearning 的 `retrain_gap`。

**可观测方向**：TracIn-like score 与 `retrain_gap` 的关系，在 GIF 与 GNNDelete 上是否一致。

**支持判据**：GIF 上 TracIn-`retrain_gap` 的 Spearman ρ > 0.4，且 GIF 的 ρ 显著高于 GNNDelete（与 §2.2 的 +4.2 vs +3.8 排序一致）。
**证伪判据**：两 family ρ 都 < 0.2，或排序与 effect size 反向。

### H3. Family-Specific Sensitivity Hypothesis ⚠️

**命题**：family-specific selector 排序在**未见过的设置**（新数据集 / 新 backbone / 新 seed）下保持一致。

> 当前 §2.2 的排序仅来自已见设置，重述这个排序不是假说。H3 的真正命题是"排序是否可迁移"，否则它只是 §2.2 的同义改写。

**可观测方向**：在 MG-1（跨数据集）/ MG-2（跨 backbone）/ MG-0 多 seed 上重新计算 family × strategy 排序，检查 Kendall τ 是否稳定。

**支持判据**：跨 ≥3 个设置 Kendall τ > 0.6。
**证伪判据**：τ < 0.3，或 GNNDelete 在某些 backbone 下不再以 IM 为最强 selector。

### H4. Conditional Shard Protection Hypothesis ⚠️

**命题**：shard-based methods 的异常增益主要发生在某些 partition simplification 条件下，而不是普遍鲁棒。

**可观测方向**：GraphEraser 的增益是否依赖 bridge / boundary / hub 类节点；若选择 shard-boundary-disruptive 节点，保护效应是否减弱。

**前置缺口**："shard-boundary-disruptive node" 当前没有操作定义。NeurIPS 4 天窗口下，先用三种近似定义之一并标注：
- (a) 跨 shard cut edge 的端点
- (b) partition 后跨 shard 邻居数 / 同 shard 邻居数比值高的节点
- (c) 经典 graph centrality（betweenness）在 shard 划分上的高分节点

**支持判据**：(a/b/c) 任一定义下，boundary 节点构成的删除集，在 GraphEraser 上 effect size 显著高于 shard 内部高度数节点。
**证伪判据**：boundary 选择无优势，则 H4 退回到 §8 open question。

## 5. Execution Plan（4 天 NeurIPS 窗口 · 含租 GPU + arxiv 扩展）

> 用户决策（2026-05-03）：可昼夜无休，并租用算力卡跑 ogbn-arxiv 扩展。新实验回到 scope。
> 4 天 ≈ 80 工时，按下面 5 阶段排布。每阶段独立可中止——如果上游结论不成立，下游不要硬跑。

### 5.1 Phase 0：FIG-4b 稳定性确认（必须，半天）

不做这一步，H1–H4 全部失效。

- 用 MG-0 已有 5-seed 结果，计算 §2.2 表中每个 cell 的 std 与 95% CI
- **门限**：若 max std > 1.0（即与最小 effect 量级相当），先扩 seed 再谈解读
- 输出：FIG-4b 的 error bar 版本，可直接进 paper

### 5.2 Phase 1：已有 cache 的 re-aggregation（不是新实验，半天）

> 这部分本质是 join 已有表 + 跑 Spearman/Kendall，**不需要新跑模型**。已经在 selection cache 里的 IM score、TracIn score、retrain_gap、fraction_flipped、mean_pred_shift 直接拉出来回归即可。

| 任务 | 服务于 | 输出 |
|------|--------|------|
| IM score × `mean_pred_shift` 散点 + Spearman（按 family 分面） | H1 | 1 张图 + 表 |
| TracIn score × `retrain_gap` 散点 + Spearman（GIF / GNNDelete 对比） | H2 | 1 张图 + 表 |
| family × strategy 排序在 MG-0/1/2 上的 Kendall τ 矩阵 | H3 | 1 张表 |

### 5.3 Phase 2：arxiv 扩展（核心新增，~2 天，租 GPU）

**目标**：在 ogbn-arxiv（107K train nodes）上复现 family × strategy 矩阵，强化 §2.1 family-level 主张的外部效度，并提供 scalability evidence。

#### 5.3.1 GPU 选型与预算

| 配置 | 价格参考 | 适用 |
|------|---------|------|
| 4090 24GB | ~2 元/h | TracIn G 矩阵（4.3GB）+ GU 方法 retrain，**推荐** |
| A100 40GB | ~3 元/h | 若 GIF inverse-Hessian 在 4090 上 OOM |

**预算上限建议**：50–100 元（≤2 天 × 24h × 2 元/h，留 buffer）。

#### 5.3.2 阶段 2A：可行性闸（半天，必须先做）

> 不要直接铺全矩阵——先在 arxiv 上验证每个 GU family 至少能跑通一次，否则白烧钱。

每个 family × random selector × 1 seed，跑通即停：

| Family | 已知风险 | 失败 fallback |
|--------|---------|--------------|
| GIF | inverse-Hessian O(P²)；P=10,856 → ~470MB Hessian，可行但慢 | 改用 ScaleGUN |
| GNNDelete | 仅梯度更新，应直接可行 | — |
| GraphEraser | partition 算法在 107K 节点上耗时未知 | 减小 num_shards |
| IDEA | 未验证 | 若 OOM 则跳过 arxiv |
| MEGU | 未验证 | 若 OOM 则跳过 arxiv |

**闸门规则**：任一 family 在 arxiv 上不可行，§3.5 IDEA/MEGU 的"mechanism-incomparable"框架可以直接覆盖它，论文中诚实标注"X family on arxiv is intractable, see Appendix"，而不是隐瞒。

##### 5.3.2.1 Metrics 验证清单（每个 family 的 random 试跑必须全部 pass）

> 跑通 ≠ 数据可用。修复了 MIA bug + 加了 hop-decay 之后，arxiv 是第一次新代码在大图上跑，每个 metric 都要 sanity check，否则铺全矩阵后才发现某个 metric 全是 NaN/0 就废了 24 小时。

| 检查项 | 期望 | 失败处置 |
|--------|------|---------|
| `f1_before` | ∈ [0.55, 0.85]（arxiv 训练后合理范围） | 模型训练有问题，停 |
| `f1_after < f1_before` | True | unlearn 没生效，查 path |
| `mia_auc` | **不为 0.000，且 ∈ [0.3, 0.9]** | MIA bug 修复未覆盖该 family，回查 patch |
| `mia_auc != NaN` | True | MIA evaluator 异常，看 log |
| `retrain_gap` 字段存在 | True | 3-model 框架失败 |
| `gap` 数值 | ∈ [-0.5, 0.5]（绝对值，arxiv 上可接受范围）| retrain 异常 |
| `mean_pred_shift` | ∈ [0, 1] | collateral damage 计算异常 |
| `fraction_flipped` | ∈ [0, 1] | 同上 |
| `hop_decay` 字段存在（若 A.5 已应用）| 含 keys `{1, 2, 3, '>3'}` | hop-decay patch 未生效 |
| `hop_decay[1] >= hop_decay[2] >= hop_decay[3]` | 大体单调（允许 ±0.02 抖动）| 衰减性质不成立，论文不能 claim "decay" |
| `selection_time` (IM_v4) | < 30 min（candidate_fraction=0.1）| numba/candidate 配置失效，IM 退回纯 Python |
| `unlearn_time` | < 1 hour（任一 family）| 大图上效率不可接受，需 ScaleGUN 或减规模 |

**操作流程**：每个 family 的 1-seed random 跑完后，用 `scripts/dashboard/refresh.py`（或临时 1 行脚本）对照清单——**全 pass 才进 5.3.3 主矩阵**。

#### 5.3.3 阶段 2B：arxiv 主矩阵（1.5 天）

通过 2A 的 family × {random, tracin, im_v4, hybrid_v4} × 3 seeds：

- **必须使用 `im_v4_strategy`**（已含 numba + candidate_fraction），不要用旧 `im_strategy`
- `candidate_fraction=0.1`（10K 候选 ≈ Cora 规模），先跑通再考虑加大
- 若 hybrid_v4 在 arxiv 上不稳定，退回到只报 random/tracin/im_v4

**预期产出**：5 family × 4 strategy × 3 seed = 60 runs。在 4090 上单 run ≈ 15–30 min（GU + retrain），总时长 ~15–30 GPU-hours，可控。

#### 5.3.4 阶段 2C（可选）：补一个 mid-scale 数据集

> 当前 4 数据集（Cora/Citeseer/PubMed/Chameleon）都偏小。若 arxiv 主矩阵跑得顺，**用剩余 GPU 时间补 Computers**（13.7K nodes, 245K edges, 767 features，TracIn G 矩阵仅 ~2.6GB），论文中 family-level 主张就能横跨小/中/大三个量级，比单纯加 arxiv 说服力强。

### 5.4 Phase 3：MEGU / IDEA 定位裁决（必须，半天）

这是 §3.5 的论文级判定，不能拖到 thesis 后续。

- **路径选择**：在 §5.3.2 可行性闸的结果基础上写 §3.5 的 framing
  - 若 IDEA/MEGU 在 arxiv 上效果依旧 ~0 → "robust across scales" 论点强化（Lane A 主线得利）
  - 若 IDEA/MEGU 在 arxiv 上 OOM/无法运行 → "mechanism-incomparable + computational-incomparable" 双重单列
- **必须输出**：paper §X 一节明确解释 `x_unlearn` / 梯度型 update 与 adversarial deletion signal 的失配机制

### 5.5 Phase 4：Synthesis + Paper Drafting（最后 1–1.5 天）

- 若 H1 + H2（或 H1 + H3）被支持 + arxiv 复现 → **Lane A 主线**，论文标题/abstract 围绕 "family-aware vulnerability diagnosis"
- 若 H4 在某个 boundary 定义下被强支持 → 加 **Lane B 子贡献**作为支撑章节
- 若 Phase 0 不通过 → 论文叙事降级为"observation-level finding + open mechanism question"，arxiv 数据仍可作为 scalability evidence 进 appendix

### 5.6 不做的事（明确 out of scope）

- 新 backbone（GAT 之外不增加）
- Physics 数据集（feature 维度 8,415，TracIn G 矩阵 44GB，不值得）
- 新 selector 设计（Lane B 留 future work）
- ScaleGUN 全 family 适配（除非 GIF on arxiv 失败时才用）

## 6. Dual Proposed Lanes

当前 thesis 不宜直接拍板单一路线，而应保留两条连贯的候选主线。

### Lane A: Diagnosis-Oriented Proposed

目标：

- 解释为什么不同 family 在 adversarial deletion 下表现出系统性差异
- 产出一个 family-aware vulnerability diagnosis / mechanism audit 框架

适合的 thesis 价值：

- 机制解释清楚
- 与课程报告形成自然延续
- 不依赖必须做出一个"大新算法"

### Lane B: Small Attack Improvement Proposed

目标：

- 在诊断信号的基础上，提出一个小而解释驱动的 attack selector 改进
- 不是重新发明一套巨大方法，而是在已知 TracIn / IM / Hybrid 之上做 mechanism-aware refinement

适合的 thesis 价值：

- 与已有 attack pipeline 连贯
- 结果更容易体现在定量提升上
- 但前提是要有足够强的机制证据支撑，不然容易退化成 heuristic stacking

## 7. Decision Gates

后续 thesis 应如何在两条 lane 之间收束，取决于下面这些判断：

### 7.1 优先收束到 Lane A 的条件

- family-specific mechanism pattern 能被稳定复现（Phase 0 通过 + H3 被支持）
- 假说 H1–H4 中至少有 2 条获得比较清晰的支持
- 小改 selector 带来的提升不稳定，或难以超越解释性贡献

### 7.2 优先收束到 Lane B 的条件

- 至少识别出一个稳定、可迁移的 vulnerability signal
- 该 signal 能转化为一个小而明确的 selector refinement
- 改进在多个配置上优于现有 informed selectors，且不是纯粹随机波动

### 7.3 NeurIPS 4 天窗口下的默认立场（2026-05-03 更新）

- 默认收束到 **Lane A**：Phase 0 稳定性 + Phase 1 re-aggregation + Phase 2 arxiv 扩展 + Phase 3 MEGU/IDEA 裁决
- arxiv 扩展是论文的 **scalability/external-validity argument**，不替代 Lane A 的 mechanism story
- Lane B 仍留 future work，**除非** Phase 1/2 中 H4 出现强支持（Spearman ρ > 0.5 + arxiv 复现）才考虑写一个 appendix-level proof of concept
- **预算红线**：GPU 租金 ≤ 100 元；超过该值前必须重审 §5.3.2 可行性结果

## 8. Open Questions（不进入 4 天窗口）

1. **Effect size 的统计显著性更高阶分析**：bootstrap CI、跨 backbone × 跨 dataset 的 mixed-effect model（thesis 第二阶段做）
2. **Retrain gap 与 attack strategy 的因果链验证**：retrain_gap 是否真的能分离两类影响（thesis 第二阶段做）
3. **H4 的精确 boundary 定义**：若 §5.2 的快速近似支持 H4，再投入精确定义（thesis 第二阶段做）

## 9. Current Working Position

当前推荐立场：

- thesis 第一阶段优先做解释性研究，而不是直接扩展课程报告或急于定义一个大 proposed
- 解释性研究的输出形式必须是 testable hypotheses，而不是 post hoc story
- 如果解释证据足够稳定，再从 Lane A 自然过渡到 Lane B
- **NeurIPS 提交版本聚焦 Lane A**，Lane B 留作 future work

## 10. Relation To Existing Docs

- `PROJECT_MASTER_CONTEXT.md`
  保存项目的早期统一背景和原始目标设定，适合作为背景参考。
- `flow.md` + `plan_flow_v2_delta.md`
  保存方法、指标与归因框架的实现参考。
- `generalization_experiment_checklist.md`
  保存 2026-02 阶段实验覆盖与完成度。
- `../report/paper/stage_report_2026-02-27.md`
  对应中期阶段的阶段报告。
- `../report/0417_5003report/main_report/msc_project_report.md`
  对应已经完成的课程报告，FIG-4b 数据来源。

这份 memo 不替代这些文档，而是给出一个当前 thesis 线的解释与收束入口。
