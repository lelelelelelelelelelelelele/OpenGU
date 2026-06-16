---
tags: [progress/timeline, status/frozen, macro]
date-range: 2026-02-16 → 2026-05-07
status: frozen
created: 2026-06-15
up: "[[_Home]]"
---

# 阶段汇总日志：项目启动 → NeurIPS deadline（2026-02-16 → 2026-05-07）

> 工作日期范围: 2026-02-16 ~ 2026-05-07（休整前的全部进展）
> 生成时间: 2026-06-15
> 定位: **回顾性总结/汇报**。把散落在 11 份 daily-log（2-月那批 + 5/5、5/6）、stage report、journal、dashboard 里的进展融合成一条主线。
> 配对: 5/3-7 冲刺细节 → [[2026-05_NeurIPS-Push]]；当前操作中枢 → [PROGRESS（外部）](../../../self/dashboard/PROGRESS.md)；详细覆盖矩阵 + bug 档案 → [EXPERIMENT_DASHBOARD（外部·FROZEN）](../../../self/dashboard/EXPERIMENT_DASHBOARD.md)。
> ⚠️ **诚实提醒**：本文件记录的是**截至 2026-05-07 时点**的结论。其中"脆弱性指纹 / IF-IM selector 是核心贡献"的叙事，已被 2026-06 数据回流后的复查**部分推翻**（见末尾「衔接」+ PROGRESS.md §2 的 C1）。读旧结论请对照那里。

---

## 📋 范围

本阶段 = 从 0 搭起"对 GNN unlearning 的对抗攻击"研究框架，到 NeurIPS 投稿 push 结束。三个活跃波段：

| 波段 | 时间 | 提交量 | 主题 |
|---|---|---|---|
| 奠基波 | 2026-02-16 ~ 02-28 | ~88 commit / 13 天 | 攻击框架 + 泛化矩阵 + Feb 里程碑 |
| 课程报告 | 2026-04-14 | 4 commit | EE5003 MSc 报告 deliverable |
| NeurIPS push | 2026-05-03 ~ 05-07 | **127 commit / 5 天** | bug 大审计 + 服务器重跑 + paper + arxiv |

---

## 🗓️ 阶段时间线

### Phase 0 — 框架验证（02-16~17）
- step-0：OpenGU 框架兼容性验证，**15 method × 兼容性矩阵**；跨数据集验证（cora/citeseer/pubmed × GNNDelete）。
- 确立 metric 抽取流程。

### Phase 1 — 攻击策略基础设施（02-17~19）
- `BaseStrategy` ABC + random / degree / pagerank 三 baseline（step 1-3）。
- **TracIn**（伪影响函数，step-4）、**IM-CELF + Hybrid**（IF-IM 融合，step-5）。
- AttackPipeline + demo 验证；6-strategy 跨方法跑通；collateral damage 评估编码。

### Phase 2 — 泛化矩阵 MG-0~MG-3（02-19~24）
- MG-0 稳定性（cora/GCN/5 seed）、MG-1 citeseer、MG-2 GAT、MG-3 IDEA/MEGU 扩展。
- GUIDE 对照组；seed 流统一（锚 2024）；选点 cache + 可视化。
- **IM 严重 bug → 升级 IM v4**（02-24，batch-CELF + 去耦 MC seed）。
- Ratio 敏感性扫描。

### Phase 3 — 评估打磨 + Feb 里程碑（02-25~28）
- relative-F1 评估；**f1_drop 严重 bug 修正**；GNNDelete 多处修复；**证明 GUIDE 无效并剔除其影响**。
- **里程碑 stage report（02-27）**：950 runs，7/7 阶段 100% 覆盖（mg0/1/2 各 90 + mg3 80 + ratio 240 + p2-ext 360），5 张主图，答辩 slide。

### Phase 4 — MSc 课程报告（04-14）
- MSc report draft + 图刷新 + overleaf bundle + collateral 叙事（EE5003 课程 deliverable，已封口）。

### Phase 5 — NeurIPS 准备：dashboard + Phase A 修复（05-03~04）
- 答辩 deck 定稿；**确立 `self/dashboard/` 为唯一权威落点**。
- **Phase A 代码修复**（重跑前必做）：MIA AUC=0 bug（MEGU `megu.py:140` / GraphEraser `Shard_based_pipeline.py:177`；IDEA 误判）、IM 固定 MC seed（A.4，跨 GU seed Jaccard 0.13→1.0）、hop-distance collateral decay（A.5）。
- path/runner 重构 + v4 摘帽（`im_v4`→`im`）；新增 `SERVER_RUNBOOK`。

### Phase 6 — Phase B 基建硬化 + bug 大审计（05-05~06）
- untrack 1317 个 pre-Phase-B 污染文件；锁定 k=5 baseline 语义 + Phase B 三层路径；overleaf 骨架 + 5 图强推。
- **attack pipeline 8-9 bug 审计**（`fix/blocker-1-train-before-select`，**Phase B 既有数据全判不可信、清盘重跑**）：config 路径泄漏、baseline 未限 train-mask（预算不匹配）、collateral 缺 seed、**TracIn/Hybrid 在 random-init 模型上算梯度**（train-before-select）、cache key 不全、跨 strategy 训练状态污染、SISA guard、失败 unlearning 污染 ResultCache、`proportion_unlearned` 不同步。
- GraphRevoker 解除对 GraphEraser 的别名；alpha sweep 启用；术语 "MIA"→"update-detection AUC"。

### Phase 7 — 服务器重跑 + paper + arxiv（05-07，43 commit）
- arxiv-scale 工程：**chunked TracIn**（24GB OOM）、**IM CELF 共享 cache + 并行 MC**、topology-only seed anchor；`MIGRATION_RUNBOOK` 双阶段回收；arxiv 三段部署。
- **L8 修复 `d674f62`**（IF-family approxi 写回 params_esti）+ `redo_collateral_if_family.py` / `cleanup_if_family_collateral.py`。
- **paper**：用 Phase B 数据填实 interim + 重生 6 图；**master scorecard + Structural Alignment 小节 + k=5 baseline 框架**；track `_phase_b_aggregate.csv`（驱动全部图）。
- 服务器实跑：cora GCN/GAT 满矩阵 + arxiv pilot（数据 5-07 当天回流）。

---

## ✅ 截至 5.7 的交付物

- **代码**：6 attack strategy（random/degree/pagerank/tracin/im/hybrid）+ AttackPipeline + 三层 cache（Result/Selection/Score）+ canonical runner `experiments/run.py` + gate/redo/cleanup 工具链。
- **数据**：Feb 950 runs（pre-Phase-B，后判污染已 untrack）；Phase B cora GCN/GAT 满 6×6×5 + r0.01 切片 + α=0 ablation（460 行）；arxiv pilot（GIF+GNNDelete×3，seed42）。
- **paper**：overleaf 全 7 章填实、6 图、master scorecard（12 cell）、arxiv pilot 表。
- **文档**：dashboard 体系、SERVER_RUNBOOK、MIGRATION_RUNBOOK、limitations L1-L8、METRICS_CATALOG。

---

## 🐛 重大 bug 修复史（按影响）

1. **IM 病态（02-24）** → IM v4（batch-CELF + 去耦 MC seed）。
2. **f1_drop / GUIDE 无效（02-26）** → 修正 f1_drop，剔除 GUIDE。
3. **MIA AUC=0（Phase A, 05-04）** → MEGU/GraphEraser 取消注释/修 shard。
4. **attack pipeline 8-9 bug（Phase B, 05-06）** → 清盘重跑的真正起因，最关键。
5. **L8 IF-family 写回（05-07, d674f62）** → 代码已修；**但数据因服务器 stale `.pyc` 仍坏**（见 PROGRESS.md）。

> 详细 bug 定位见 `EXPERIMENT_DASHBOARD.md §3.6` + `limitations.md`。

---

## 🎯 成果总结（5.7 时点）

- 从 0 建成可发表级攻击框架：16 GU method × 多 backbone × 6 selector，三层指标（F1 drop / update-detection AUC / collateral）。
- 形成主叙事（**当时**）：跨方法族脆弱性差异（Learning / IF / Shard）、Shard Protection、ratio/seed/跨模型泛化证据。
- NeurIPS push 在 deadline 内完成代码硬化 + 服务器重跑 + paper 填实。

---

## 📅 衔接（5.7 之后 → 看 PROGRESS.md）

5.7 之后休整一个月，数据回流后复查（2026-06-15）**修正了关键结论**，不要再按上面旧叙事走：
- **C1（决定性）**：informed selector（TracIn/IM/Hybrid）打不过 degree baseline，TracIn 平均为负 → 原"我们提出 IF selector"贡献被证伪，需 reframe 成"结构杠杆是主攻击轴 / influence 失配"。
- C2/C3/C4：GNNDelete n=5 不显著、hop-decay 被 L8 污染且 CSV 列空、ΔF_noise anchor 缺失。
- 环境待重建（盘迁成 E:）、大方向（rebuttal vs 重投）待定。

→ **当前状态与待办一律以 [PROGRESS（外部）](../../../self/dashboard/PROGRESS.md) 为准。**
