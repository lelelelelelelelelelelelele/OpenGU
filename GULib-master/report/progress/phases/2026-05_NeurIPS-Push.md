---
tags: [progress/phase, status/frozen, neurips-push]
phase: "2026-05 NeurIPS Push"
date-range: 2026-05-03 → 2026-05-07
status: frozen
created: 2026-06-15
up: "[[_Home]]"
---

# NeurIPS Push 汇报（2026-05-03 → 2026-05-07）

> 工作日期范围: 2026-05-03 ~ 2026-05-07（5 天，127 commit）
> 生成时间: 2026-06-15（回顾性汇报）
> 范围: 休整前最后一段冲刺——从"答辩材料 + 知识库"到"代码硬化 + 服务器重跑 + paper 填实"的 NeurIPS 投稿 push。
> 配对: 全项目时间线 → [[Macro-Timeline]]；当前操作中枢 → [PROGRESS（外部）](../../../self/dashboard/PROGRESS.md)。
> ⚠️ 本段结论（脆弱性指纹 / IF-IM selector 是核心贡献）已被 2026-06 数据复查的 **C1 部分推翻**，见末尾「衔接」。

---

## 📋 概览

| | |
|---|---|
| 时长 / 提交 | 5 天 / **127 commit**（5-03:6, 5-04:8, 5-05:36, 5-06:34, 5-07:43） |
| 目标 | 把项目从"Feb 旧数据 + bug 污染"推到 NeurIPS **可投状态**：干净数据 + 填实 paper |
| 主线 | 先**修代码**（不修就重跑也是脏数据）→ 再**清盘重跑** → 同时**写 paper / 攻 arxiv** |
| 结果 | 代码硬化完成、cora 满矩阵干净数据回流、paper 全章填实 + 6 图；arxiv 仅跑出 pilot；deadline 到 |

---

## 🧵 八条工作流

### WS1 — 答辩材料 + 知识库重构（5-03~04）
- 答辩 deck（init → iterate → finalize speech + report pptx）+ report visual refresh 合并。
- **确立 `self/dashboard/` 为唯一权威落点**（SoT）；归档 CRITICAL_BUG_REPORT、`flow.md` 降级 historical；report archive 重组。
- 新增 `SERVER_RUNBOOK`（双机执行手册）。

### WS2 — Phase A 代码修复（5-04，重跑前必做）
- **MIA AUC=0 bug**：MEGU `megu.py:140` 取消注释、GraphEraser `Shard_based_pipeline.py:177` 修；IDEA 实测非零（误判）。
- **IM 固定 MC seed（A.4）**：锚 `im_selector_seed=2024`，跨 GU seed Jaccard 0.13 → 1.0。
- **hop-distance collateral decay（A.5）**：4 桶（1/2/3/>3 hop）。
- v4 摘帽（`im_v4`→`im`、`hybrid_v4`→`hybrid`）+ path/runner 重构。

### WS3 — Phase B 基建 + 数据治理（5-05，36 commit）
- **untrack 1317 个 pre-Phase-B 污染文件**；锁定 k=5 baseline 语义 + Phase B 三层路径。
- overleaf 草稿骨架 + 5 图强推；requirements 补 7 个 upstream 漏的依赖。
- **自动 gate**（pass/fail 判 yaml，替代肉眼）；`inspect_run` 健康检查工具。
- **V4→V1 strategy 合并 + ScoreCache 基建**；GraphRevoker 解除对 GraphEraser 的别名。
- B.1 arxiv 可行性闸 + probe 与 GU 稳定性分离 + prewarm cache-only 分卡路径。

### WS4 — ⭐ attack pipeline 8-9 bug 大审计（5-06，本段最关键）
> 结论：**Phase B 既有所有 attack/collateral 数据判定不可信，清盘重跑**。这是整个 push 能产出可信数据的前提。

| commit | 修的 bug |
|---|---|
| `66a90f8` | config 路径泄漏（demo_attack 剥 argv 后烘出默认 cora/0.1 路径）+ baseline 未限 train-mask（预算不匹配）+ collateral 缺 seed |
| `13f1e89` | **TracIn/Hybrid 在 random-init 模型上算梯度**（select_nodes 时序早于训练）→ train-before-select |
| `ddb7109` | cache key 不全（缺架构/loss 系数）+ 跨 strategy 训练状态污染 |
| `df47d80` | SISA selector guard + run.py fingerprint + arxiv tier split |
| `57fbdd3` | 失败 unlearning 污染 ResultCache + failure 传播到 demo_attack rc |
- 配套：5 条 invariant 测试锁行为；`proportion_unlearned` 同步。

### WS5 — arxiv-scale 工程（5-07）
- **chunked TracIn**（绕开 24GB G-matrix OOM）；**IM CELF 共享 cache + 并行 MC**（跨 method/seed 复用，CPU 并行）；topology-only seed anchor。
- `MIGRATION_RUNBOOK`（双阶段数据回收）；arxiv 三段 prewarm-then-deploy（ratio=0.01）+ `run_arxiv.sh` 部署脚本。

### WS6 — L8 IF-family 修复（5-07）
- `d674f62`：approxi() 写回 `params_esti` 到 target_model（GIF/IDEA）。
- `redo_collateral_if_family.py` + `cleanup_if_family_collateral.py` 重评工具。
- ⚠️ 代码修了，但服务器 stale `.pyc` 让它没真正生效 → 回流数据仍带 bug（这是 2026-06 复查才确认的，见 PROGRESS.md / limitations L8）。

### WS7 — paper 攻坚（5-06~07）
- overleaf 重写到 outline v2 + 4-tier access 框架 + RF-relative hop-decay。
- 术语 "MIA"→"update-detection AUC" 全局统一。
- **master scorecard**（12 cell，6 metric）+ **Structural Alignment 小节** + k=5 baseline 框架；填实全部 interim 占位；**6 图重生**；track `_phase_b_aggregate.csv`（驱动全部图）。

### WS8 — 服务器执行（5-06~07）
- cora GCN/GAT **满 6×6×5 矩阵**回流（git_sha 78872fc，5-07 当天）；arxiv **pilot**（GIF+GNNDelete×3，seed42）。

---

## 🎯 push 成果（deadline 时点）

- ✅ 代码硬化：9 条 attack 正确性 bug 全修 + invariant 测试 + 自动 gate。
- ✅ 干净数据：cora 双 backbone 满矩阵（460 行，1 failed）。
- ✅ paper：全 7 章填实 + 6 图 + master scorecard + arxiv pilot 表。
- ◐ 未竟：arxiv 仅 pilot（1 seed/2 method）；L8 数据未真正修复（stale .pyc）；4 个缺 k=5 cell。

---

## 💡 经验

- **"先修代码再重跑"是对的**——Phase A/B 不修就重跑只是更多脏数据。
- **stale `.pyc` 是 autodl 容器的隐藏坑**：代码改了不等于跑的是新代码（L8 就栽在这）。下次重跑前必清 `__pycache__`。
- selection 与 GU pipeline 解耦 + 跨 method 共享 cache，显著降低重跑成本。

---

## 📅 衔接（5.7 之后）

数据回流后 2026-06 复查**修正核心结论**：**C1** — informed selector（TracIn/IM/Hybrid）打不过 degree、TracIn 平均为负 → 原贡献被证伪，需 reframe。另有 C2（GNNDelete n=5 不显著）/ C3（hop-decay L8 污染 + CSV 列空）/ C4（ΔF_noise anchor 缺）。
→ **当前状态与待办以 [PROGRESS（外部）](../../../self/dashboard/PROGRESS.md) 为准。**
