---
title: WORKPLAN 同步
created: 2026-07-09
updated: 2026-07-20
type: workplan-sync
source: ../../self/dashboard/WORKPLAN.md
tags: [workplan, sync, dynamic]
---

# WORKPLAN 同步

这页是 OB 内的人读版工作计划。执行真相仍是 [WORKPLAN.md](../../self/dashboard/WORKPLAN.md)；这里负责把当前推进顺序、看板、TODO 入口连起来。

---

## 当前状态

- 已投 NeurIPS，处于 rebuttal-prep / 完善期。
- thesis 锁死：systematic audit + extreme heterogeneity + Vulnerability Fingerprint。
- 本轮不做重投式 reframe；先在现有 thesis 内补证、改写、清硬伤。
- 本地 GPU 不可用，GPU 实验走 AutoDL 镜像 `gnn_20`；本地用于 CPU 分析和文档。
- Git 分支与 worktree 状态不在本页固化；每次操作前以 `git status --short --branch` 和 `git worktree list` 为准。

---

## 推进顺序

1. GraphRevoker E4：代码与远端 40/40 已通过；只剩本地 evidence import / manifest 闭环，旧数据永久 invalid。
2. E7 两组独立门控（不是跳过 gate 直接开跑）：Group 1 为 `proper-tracin-v1` + Cache V2 cold/warm exact hit → GCN→GAT/GIN；Group 2 为 `d-gif-sgc-v1` + SGC selector 单元验证 + Cache V2 cold/warm exact hit → SGC→GCN/GAT/GIN。target-direct 只作 white-box reference；不做 GCN-B→GCN-A，不以 60% 阈值串联两组，也不预设放大 approximation gap。Legacy IF / Selection Cache 只读，换版只建新 V2 Recipe，明确退役才显式 retire。→ [[10_实验矩阵/24_E7代理选集迁移实验计划]]。
3. W1/W2/W3 写作主线：主指标转 retrain gap，回应 degree / scope / 叙述过满。
4. E2/E3/E5/E6 + A5 补证：L8 redo、noise anchor、arxiv scope、hop 列、ratio/dataset sweep；E1 已完成。
5. F3/F4 看图和看板：补 supp 图，持续维护 config_inventory。
6. W6/W9 review + AI 数据分析：把评审意见转成任务，把矩阵再过一遍找可写点。

---

## 四阶段任务入口

| 阶段 | OB 台账 | 执行源 |
|---|---|---|
| 实验 | [[02_TODO台账#实验 E]] | [WORKPLAN.md §5](../../self/dashboard/WORKPLAN.md) |
| Ablation | [[02_TODO台账#Ablation A]] | [WORKPLAN.md §6](../../self/dashboard/WORKPLAN.md) |
| 写作 | [[02_TODO台账#写作 W]] | [WORKPLAN.md §7](../../self/dashboard/WORKPLAN.md) |
| 画图 / 看板 | [[02_TODO台账#画图与看板 F]] | [WORKPLAN.md §8](../../self/dashboard/WORKPLAN.md) |
| 修复验收 / Artifact 版本 | [[10_实验矩阵/13_重跑与缓存修复Runbook]] | GraphRevoker archive boundary / E7 versioned V2 Recipe |
| 评审 / rebuttal | [[30_评审与汇报/31_评审意见与rebuttal]] | [WORKPLAN.md §7 W6](../../self/dashboard/WORKPLAN.md) |

---

## 看板挂钩

- 阶段 kanban：[progress.html](../../self/dashboard/progress.html)
- 实验覆盖：[config_inventory.html](../../self/dashboard/config_inventory.html)
- 看板验收：[CONFIG_INVENTORY_ACCEPTANCE.md](../../self/dashboard/CONFIG_INVENTORY_ACCEPTANCE.md)
- paper 硬伤：[PAPER_LIABILITIES_MAP.md](../../self/dashboard/PAPER_LIABILITIES_MAP.md)
- 验证记录：[VALIDATION_LOG.md](../../self/dashboard/VALIDATION_LOG.md)

---

## 同步检查

- [ ] 改过 `WORKPLAN.md` 后，同步本页“当前状态 / 推进顺序”。
- [ ] 改过任务状态后，同步 [[02_TODO台账]]。
- [ ] 发生 method / selector 修复后，同步 [[10_实验矩阵/13_重跑与缓存修复Runbook]] 的受影响范围。
- [ ] 新增 review/advisor 意见后，同步 [[30_评审与汇报/31_评审意见与rebuttal]]。
- [ ] 看板生成后，检查 `progress.html` 和 `config_inventory.html` 能反映最新口径。
