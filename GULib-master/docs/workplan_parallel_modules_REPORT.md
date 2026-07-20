---
title: WORKPLAN 未完成项并行模块梳理
date: 2026-07-20
status: review-projection
source_main: b46927e86cc2f0d4783a7b544661458881b014d0
---

# WORKPLAN 未完成项并行模块梳理

> 这是一份供审阅的并行化投影，不是第二份状态中枢。任务定义和最终勾选仍以 [`self/dashboard/WORKPLAN.md`](../self/dashboard/WORKPLAN.md) 为准；本报告只整理当前证据、依赖和可并行边界。

## 一句话结论

**Cache V2 当前范围已经完成；真正未完成的核心是 IF collateral/hop、noise anchor、arxiv scope、A5 ratio 补量、TracIn 正式化与 surrogate transfer，以及对应写作和图。**

上一轮看起来像 WIP 的 IF-target 实验其实已达到本地验收条件，本轮已完成测试、提交、父线合并、主线合并和推送，不再列为未完成模块。现在唯一保留的真实代码 WIP 是 `codex/wip-tracin-promotion-20260720@3ccde63`。

## 当前基线与已关闭事项

| 项目 | 当前结论 | 证据 |
|---|---|---|
| Git 主线 | local/main 与 origin/main 均为 `b46927e` | 本轮推送后 SHA 与 ahead/behind=`0/0` |
| Worktree | 从 19 个收敛到 3 个，全部 clean | 主工作区、TracIn WIP、本报告工作区 |
| 分支 | 已删 26 条本地、6 条远端短期分支 | ancestor、patch-equivalent 或 superseded 审计 |
| Cache V2 | **当前范围 accepted**；不再作为 E7 的通用 Cache blocker | [`cache_v2_rollout_syncmate_ACCEPTANCE_REPORT.md`](../docs/cache_v2_rollout_syncmate_ACCEPTANCE_REPORT.md) |
| Legacy Cache | active authority/fallback 已收口；物理退休延后 | 970 payload、70 refs、`physical_archive_authorized=false` |
| IF/GIF target | **已进入 main**：single-seed C/D target + 三数据集三 seed A/B–C–D matrix | [`c_target_v1_REPORT.md`](../reports/c_target_v1_REPORT.md)、[`bc_target_matrix_REPORT.md`](../reports/bc_target_matrix_REPORT.md) |
| E1 / E4 / F4 | 已完成或已有接受结论 | WORKPLAN 的 E1、E4、F4 |

不要重新打开的事项：Cache Gates 2–4、E1 Citeseer stable scope、E4 GraphRevoker 40-cell 修复矩阵、IF-target 本地机制矩阵。Legacy 物理退休是独立工程，不应混入当前 rebuttal 主线。

## 数字校正

[`config_inventory.csv`](../self/dashboard/config_inventory.csv) 与当前验收报告暴露了几处 WORKPLAN 表面数字漂移：

| 项目 | WORKPLAN 表面状态 | 当前证据化状态 | 解释 |
|---|---:|---:|---|
| A3 | `0/200` | **10/200** | GCN α=0.00 已有 10 行；其余仍待 gate 决策 |
| A5 全配置空间 | 当前文字强调 190 pending | **90/450** | inventory 是全配置口径；190 是当前收窄后的 stable-strategy formal lane |
| arxiv T1–T3 | T1 `6/18` | **6/54** | inventory/YAML 为每 seed 18；T2/T3 均 0。README 的 12/seed 是旧口径 |
| TracIn | prototype gates 已合入 | **仍未 production accepted** | G1/G3 partial，G5/G6 not run |
| Cache V2 | E7 文本仍写 real-hit blocker | **real-hit 已通过** | E7 现在只被 proper TracIn/runner gate 阻塞 |

因此，后续更新 WORKPLAN 时应把 Git SHA、Cache/E7 blocker、IF-target accepted evidence、A3 进度和 arxiv cell 口径一起同步，而不是只改一处 checkbox。

## 可并行模块

| 模块 | 对应 ID | 当前状态 | 资源 | 前置依赖 | 完成定义 |
|---|---|---|---|---|---|
| **M0 当前真相同步** | dashboard maintenance | ready | 本地 CPU / 文档 | 本报告审阅 | WORKPLAN 更新到 `b46927e`；同步 Cache、IF-target、A3、arxiv 口径；重生 `progress.html` |
| **M1 IF collateral 修复与 hop 闭环** | E2 → E6 → W3-L3 / W8 / F3-hop | 未开始 | AutoDL GPU + 本地聚合 | E2 先于 E6 | 120 个 GIF/IDEA collateral cell 通过；aggregate 460/460 有 4 个 hop 字段；caveat 与 hop 图回填 |
| **M2 noise anchor** | E3 → W3-L4 | ready | 本地 CPU | 无 | 完成 k=5 `f1_after` 与主矩阵 `perf_before` join；同时给出 `relative_f1_drop` sanity；锁定论文采用口径 |
| **M3 arxiv scope** | AC-1 → E5 → W2-② / W3-L7 | 部分完成 | AutoDL GPU | AC-1 必须先过 | AUC disabled-policy canary 1/1；T1–T3 authoritative matrix 54 格中补齐缺失 48 格，或先书面收窄 scope；更新 scope 结论 |
| **M4 ratio 补量** | A5 → F3-ratio | 部分完成 | AutoDL GPU | r0.20 先做 1-cell gate | 按当前 formal lane 完成 190 个 stable-strategy cells；同步 inventory；生成 ratio-elasticity 数据 |
| **M5 TracIn 正式化与迁移攻击** | TracIn G1/G3/G5/G6 → E7 C.6a → C.6b | blocked / WIP | 本地代码 + AutoDL GPU | proper versioned Recipe 和 runner gate | WIP 与 main 对齐；formal ScoreArtifact/store；G5 Hybrid、G6 GU canary 通过；再跑 C.6a 5 格与 C.6b 10 格 |
| **M6 统计与 ablation 决策** | A3、A7 | decision required | 本地分析 + 可选 GPU | 先做价值/功效判断 | A3 明确 go/no-go；若 go，补到 200/200。A7 明确追加 seed 数或改为 volume-driven/n.s. 表述 |
| **M7 写作证据线** | W1–W9、W3 子项、W4 收口 | 未验收 | 写作 / 本地分析 | 部分子项依赖 M1–M3 | 立即完成 W1/W5、W3 可写 caveat、W6/W7/W9；实验回填后完成 W2/W3/W8；最后 W4 融合并逐表核对 |
| **M8 图与生成器线** | F1、F2、F3 | 未验收 | 本地绘图 | F3 依赖 M1/M4，alpha 图依赖 M6 | F1 pipeline 图；F2 生成器单一权威入口；F3 三类 supp 图由正式数据重生 |
| **M9 非当前主线** | A8、A9、Legacy 物理退休 | option / deferred | 独立项目 | rebuttal 主线完成或 reviewer 点名 | 只有明确升级优先级后再建独立 branch；不得混进 M1–M8 |

## 模块 M5 的真实缺口

TracIn 是现在最容易被“原型已合并”误判成“已经完成”的部分。正式报告的结论仍是 [`CONDITIONAL PROTOTYPE PASS; KEEP UNSTABLE`](../docs/tracin_v2_gates_ACCEPTANCE_REPORT.md)：

- G1 Recipe identity：partial pass，formal ScoreArtifact/store/conflict gate 缺失；
- G3 Legacy replay/isolation：partial pass，formal store snapshot gate 缺失；
- G5 Hybrid：未运行；
- G6 GU canary：未运行；
- 默认 runner/production registry：有意没有接入。

本轮合入的 IF/GIF-target 证据解决了“A 对 B 的排序代理、B 的数值估计、C-IF/D-GIF 分界与 same-source proxy 是否有效”的机制问题，但它没有自动完成 TracIn production registration，也没有完成 E7 surrogate transfer。两者应作为 M5 的输入证据，而不是把 M5 标成完成。

## 推荐并行波次

### Wave A：现在即可并行

| Lane | 立即动作 | 原因 |
|---|---|---|
| 本地数据 | M2 noise anchor | 无 GPU 依赖，直接关闭 C4/W3-L4 |
| 状态治理 | M0 WORKPLAN 同步 | 避免继续按旧 SHA、旧 Cache blocker 和旧 cell 数排期 |
| 代码研究 | M5a：把 TracIn WIP 与 main 对齐并补 formal gate 设计 | 可与 GPU 队列并行，但未过 gate 前不合 main |
| 写作 | M7 的 W1/W5、W3 即时 caveat、W6/W7/W9 | 不等待新实验即可推进 |
| 图 | M8 的 F1/F2 | 不依赖实验结果 |

### Wave B：单 GPU 队列，按关键路径串行

1. **AC-1**：先验证大图 AUC disabled-policy；失败则禁止开 E5。
2. **E2**：优先于其它大批量任务，因为它同时解锁 E6、W3-L3、W8 和 hop 图。
3. **E5**：补 arxiv scope，解锁 W2-② 与 W3-L7 的最终表述。
4. **A5**：完成 ratio formal lane；r0.20 shard 方法先 1-cell gate。
5. **A7 / A3**：只在 M6 决策为 go 后排队，避免无效烧卡。

### Wave C：依赖回填

- E2 完成后：E6 → W3-L3 / W8 → F3-hop；
- E3 完成后：W3-L4；
- E5 完成后：W2-② / W3-L7；
- A5/A3 完成后：F3 ratio/alpha；
- W1–W3 完成后：W4 全文融合与表格重查；
- TracIn G1/G3/G5/G6 全过后：E7 C.6a，再按 transfer ratio gate 决定 C.6b 后续扩展。

## 建议的优先级

| 优先级 | 模块 | 理由 |
|---|---|---|
| **P0** | M0、M1、M2、M3 | 直接修正状态源并关闭 C3/C4/L7 的证据硬伤 |
| **P1** | M4、M5、M7、M8 | 补规模、完成 proper TracIn 路径并形成可交付 paper/figure |
| **P2 / gated** | M6 | A3 价值有限，A7 需先决定追加 seed 还是收缩 claim |
| **不排期** | M9 | follow-up 或独立 retirement，不属于当前 rebuttal 主线 |

如果只看“还有哪些没有修改完”，当前应关注的是 **M1–M8**；M0 是状态同步，M9 是明确不在当前主线。最短可见成果路径是 **M2 + M0 + W1/W5 + F1/F2**，关键实验路径是 **AC-1 → E2 → E6**，最长研究路径是 **TracIn production gates → E7**。

## Git 收口审计

| 动作 | 结果 |
|---|---:|
| 第一次 main 推送 | `3f631fb → a41efe1`，97 个领先提交进入 origin |
| IF-target 接收 | child `e335885` → parent merge `8a648d2` → main merge `b46927e` |
| IF-target 测试 | 合并前后均 9/9 passed |
| Dirty worktree | 4 个全部 clean；IF-target 正式接收，TracIn 保留 WIP，2 份旧稿转 archive tag |
| Worktree 删除 | 16 个 clean 历史 worktree |
| 本地分支删除 | 26 条 |
| 远端分支删除 | 6 条 |
| Archive tags | `archive/docs-residue-20260720`、`archive/runner-residue-20260720`，均已推送 |

## 审阅后建议

审阅本报告后，只需要决定三件事：

1. M6 的 A3/A7 是继续跑，还是收缩 claim；
2. M3 的 arxiv 是否按 54-cell 完整口径补齐，还是书面收窄 scope；
3. M5 是否升级为当前主线，还是先只完成 proper TracIn production gate、暂缓 E7。

决定后再回写 WORKPLAN 和重生 dashboard，避免报告与状态中枢继续漂移。
