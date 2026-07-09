---
title: WORKPLAN 同步
created: 2026-07-09
updated: 2026-07-09
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

---

## 推进顺序

1. E4 GraphRevoker 修复：先修聚合器 bug + 整 method 重跑，确保 6-method audit 底座有效。
2. W1/W2/W3 写作主线：主指标转 retrain gap，回应 degree / scope / 叙述过满。
3. E1/E2/E3/E5/E6 补证：Citeseer、L8 redo、noise anchor、arxiv scope、hop 列。
4. F3/F4 看图和看板：补 supp 图，持续维护 config_inventory。
5. W6/W9 review + AI 数据分析：把评审意见转成任务，把矩阵再过一遍找可写点。

---

## 四阶段任务入口

| 阶段 | OB 台账 | 执行源 |
|---|---|---|
| 实验 | [[02_TODO台账#实验 E]] | [WORKPLAN.md §5](../../self/dashboard/WORKPLAN.md) |
| Ablation | [[02_TODO台账#Ablation A]] | [WORKPLAN.md §6](../../self/dashboard/WORKPLAN.md) |
| 写作 | [[02_TODO台账#写作 W]] | [WORKPLAN.md §7](../../self/dashboard/WORKPLAN.md) |
| 画图 / 看板 | [[02_TODO台账#画图与看板 F]] | [WORKPLAN.md §8](../../self/dashboard/WORKPLAN.md) |
| 重跑 / cache 修复 | [[10_实验矩阵/13_重跑与缓存修复Runbook]] | GraphRevoker / TracIn rerun |
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
