---
title: TODO 台账
created: 2026-07-09
updated: 2026-07-20
type: todo-ledger
source:
  - ../规划手记.md
  - ../../self/dashboard/WORKPLAN.md
  - ../30_评审与汇报/AI审稿_2026-06-28.md
tags: [todo, workplan, opengu]
---

# TODO 台账

这个台账把 `规划手记`、AI 审稿、WORKPLAN 里的散点任务统一到一个 OB 入口。正式实验 / 消融 / 写作任务的执行状态以 [WORKPLAN.md](../../self/dashboard/WORKPLAN.md) 为准；这里负责分区、解释和链接。一次性的工程验收 check 不抬升为 `WORKPLAN` 任务，独立记录在“工程验收 Check”区；运行后才把实际证据追加到 [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)。

> [!note] 论文阅读状态
> W7 的跨项目阅读状态统一维护在 Learning vault 的 [全局论文阅读台账](obsidian://open?vault=Learning&file=10%20Topics%2F%E7%A0%94%E7%A9%B6%E9%98%85%E8%AF%BB%E7%B3%BB%E7%BB%9F%2F00%20%E5%85%A8%E5%B1%80%E8%AE%BA%E6%96%87%E9%98%85%E8%AF%BB%E5%8F%B0%E8%B4%A6)；本页保留 OpenGU 为什么要读以及项目任务入口。

---

## 实验 E

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| E4 | GraphRevoker 修复与四策略整 method 重跑 | [[10_实验矩阵/13_重跑与缓存修复Runbook]] | ✅ 代码 + 远端 40/40；◐ 本地 evidence import / manifest 待闭环；旧数据永久 invalid | WORKPLAN §5 / GraphRevoker E4 验收报告 |
| E1 | 跑干净 Citeseer，堵 scope 漏洞 | [[10_实验矩阵/10_实验-框架总览]] | ✅ stable scope 50/50 accepted | AI 审稿痛点：实验完成度 |
| E2 | L8 redo：清 `.pyc` 后重跑 GIF/IDEA collateral | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §5 |
| E3 | 本地算 k=5 noise anchor | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §5 |
| E5 | arxiv 补量，避免只剩 pilot 口径 | [[10_实验矩阵/10_实验-框架总览]] | ◐ | AI 审稿痛点：scope |
| E6 | hop_decay 列灌进 aggregate CSV | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §5 |
| E7 | C.6 surrogate-transfer umbrella（严格门控）：Cache V2 Selection Artifact cold/warm exact hit + versioned `proper-tracin-v1` 通过后，先 C.6a GCN→GCN，再 C.6b GCN→GAT/GIN；比较 target-direct TracIn / same-seed random / degree，主指标为 retrain-gap transfer ratio，辅以 selection Jaccard。Legacy IF / Selection Cache 只读；换版建新 V2 Recipe，旧 V2 Artifact 仅在明确退役时显式 retire | [[10_实验矩阵/19_Cache架构重设计与迁移方案]] / [[10_实验矩阵/12_近似策略重合度实验]] | ☐ blocked by Cache V2 real-hit + proper-TracIn gate | WORKPLAN §5 |

---

## 工程验收 Check

| ID | Check | 状态 | 依据 |
|---|---|---|---|
| AC-1 | 大图 AUC disabled-policy GPU canary | ☐ 待运行；本地 CPU 实现已验收 | [AUC 数据集策略验收报告](../../docs/auc_metric_policy_ACCEPTANCE_REPORT.md) |

### AC-1：大图 AUC disabled-policy GPU canary

- **触发条件**：任何 `phase_b_arxiv*.yaml` 正式大图批跑前，在 AutoDL `gnn_20` 上先运行一格；这是一项配置 / 路径验收，不改变宏观 `WORKPLAN` 排期。
- **通过条件**：
  - [ ] 运行日志没有进入 update-detection AUC 或 posterior 查询路径（例如没有 `Average AUC Score` 这类实际计算输出）。
  - [ ] 该 cell 的 `attack.json` 中 `mia_auc` 为 JSON `null`，不是 `0.0` 或缺字段。
  - [ ] 该 cell 的 `_meta.json` 中 `metric_policy.update_detection_auc` 记录 `enabled=false` 且 `status=disabled_by_config`。
- **收口**：三项均通过后，将 AC-1 标为 ✅，并在 [VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md) 追加该 cell 的命令 / run 路径 / git SHA 与三项检查结果；若失败，保留 ☐ 并记录阻塞原因，不把失败结果写成已验收。

---

## Ablation A

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| A3 | alpha-sweep，等主矩阵 fingerprint 稳定后再决定是否值得跑 | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §6 |
| A5 | ratio-sweep：补 r0.10 / r0.20，先 sanity GraphEraser | [[10_实验矩阵/10_实验-框架总览]] | ◐ | WORKPLAN §6 |
| A7 | GNNDelete 加 seed 或改写成 volume-driven，处理统计偏弱 | [[10_实验矩阵/10_实验-框架总览]] | ☐ | AI 审稿痛点：统计力度 |
| A9 | 是否加新 GU 方法，增强 audit 广度 | [[20_研究框架/20_方法与策略框架]] | ☐ option | 规划手记 |

---

## 写作 W

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| W1 | 主指标从 raw-F1 切到 retrain gap，头条压 heterogeneity | [[20_研究框架/20_方法与策略框架]] | ☐ | WORKPLAN §7 |
| W2 | 准备两道 rebuttal 必答题：vs degree、Citeseer/arxiv scope | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | AI 审稿 / WORKPLAN |
| W3 | 清 caveat：未完成语句、过满措辞、统计显著性对冲 | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | AI 审稿痛点 |
| W4 | paper 多版融合与表格重查 | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | WORKPLAN §7 |
| W5 | 术语审计：MIA 改为 update-detection AUC | [[20_研究框架/20_方法与策略框架]] | ☐ | `self/paper_todo.md` |
| W6 | review collection：评审/导师/AI 意见统一入口 | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | 规划手记 |
| W7 | 读 GraphRevoker / MEGU / UTU 等未读论文，补 related work 和防审稿引用 | [[20_研究框架/20_方法与策略框架]] | ☐ | WORKPLAN §7 |
| W8 | Supplementary 整理：hop / 460 行说明 / 诊断 suite | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | WORKPLAN §7 |
| W9 | AI 辅助数据分析：让 AI 过结果矩阵，找异质性、反例、可写点 | [[10_实验矩阵/10_实验-框架总览]] | ☐ | 规划手记 |

---

## 画图与看板 F

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| F1 | 方法 / pipeline 示意图 | [[20_研究框架/20_方法与策略框架]] | ☐ | WORKPLAN §8 |
| F2 | 收敛图生成器收敛：`test1.py` vs `plot_neurips_figures.py` | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §8 |
| F3 | Supp 图：alpha / ratio / hop-decay | [[10_实验矩阵/10_实验-框架总览]] | ☐ | WORKPLAN §8 |
| F4 | exp 看盘改进：config_inventory 一眼看懂跑了啥、缺啥 | [[00_工作台入口]] | ✅ conditional | 规划手记 / WORKPLAN §8 |

---

## 评审与 rebuttal R

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| R1 | 把 AI 模拟审稿三痛点转成 W/E/A 任务 | [[30_评审与汇报/31_评审意见与rebuttal]] | ✅ 已拆入本台账 | [[30_评审与汇报/AI审稿_2026-06-28]] |
| R2 | 把已有 abstract / draft / figure review 汇总成 reviewer pressure list | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | `report/paper/review/` |
| R3 | 后续真实 reviewer 意见进入同一页，不再散放根目录 | [[30_评审与汇报/31_评审意见与rebuttal]] | ☐ | 规划手记 |
| R4 | produced / usable / accepted-remote / invalid 口径同步：GraphRevoker 与 TracIn 都不能只写“跑过” | [[10_实验矩阵/13_重跑与缓存修复Runbook]] | ✅ 测试台账与 config inventory 四态已同步 | 当前同步规则 |

---

## 2026-07-09 同步记录

| ID | TODO | 放在哪个板块 | 状态 | 来源 |
|---|---|---|---|---|
| F4.1 | config_inventory 增加 supplementary overlap/validity 面板块，纳入 selector 重叠度和 GIF/TracIn 近似有效性实验 | [[10_实验矩阵/10_实验-框架总览]] / [config_inventory.html](../../self/dashboard/config_inventory.html) | 已完成 | 当前同步 |
| E8 | overlap-vs-damage join：versioned V2 proper-TracIn / Hybrid Artifact 与 E7 C.6a/C.6b 结果就绪后，把 selector overlap 与 attack outcome 连接 | [[10_实验矩阵/12_近似策略重合度实验]] | 待 gate / rerun 后做 | concordance next step |
