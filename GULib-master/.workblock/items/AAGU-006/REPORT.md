# AAGU-006 · Dataset/Split 权威修复

> 当前验收决定：`待决定`

报告事实日期：2026-08-26
当前候选：`codex/aagu-006-dataset-split-authority` 的 clean `HEAD`；实现与父线收敛检查点 `77b03eb246a918d611c251927a65722ebb147c71`

## 这次改变了什么

目标实验现在只有一个活跃的 dataset/split/budget 执行权威：
[`syncmate_target_direct_formal_v2.yaml`](../../../experiments/configs/syncmate_target_direct_formal_v2.yaml)。WORKPLAN 中可执行的 AAGU-006 与 AAGU-007 都直接进入这个 recipe；`experiments/AGENTS.md` 明确把 historical public split、OpenGU 80/20 和固定小 `k` 降为溯源材料，不允许它们补全或覆盖当前正式参数。

Dashboard 生成器同时增加了机器校验：当 WorkItem 的显式 Fact owner 与 WORKPLAN Owner 指向不同本地文件时，检查会直接报错，不再让两个权威表面静默共存。

## 现在实际看到了什么

| 数据集 | train candidate 数 | 1% 删除数 | 5% 删除数 |
|---|---:|---:|---:|
| Cora | 1,895 | 18 | 94 |
| CiteSeer | 2,328 | 23 | 116 |
| PubMed | 13,801 | 138 | 690 |

这些值与 `planetoid_70_10_20_seed2024`、`floor_with_minimum_one`、1%/5% 两档预算一起由同一 versioned recipe 持有。AAGU-015 仍由 IF 科学定义文档拥有，但其 WorkItem 明确要求执行时继承 AAGU-006 已接受的身份，不能重新打开 public split、80/20 或 fixed-small-k 路径。

已接受的 AAGU-018 与保留注册的 AAGU-019 也已从父线合入。重建后的 WORKPLAN 同时保留它们的映射和 AAGU-006 的 recipe Owner，19 个 WorkItem 全部可映射，AAGU-006 仍是唯一 Current node。

## 最关键的判断

### 1. 活跃执行入口是否只剩一个权威 — `PASS`

从 WORKPLAN 进入 AAGU-006 或 AAGU-007 时，期待直接到达唯一正式 recipe。实际两个 Owner 都解析到同一个 `syncmate_target_direct_formal_v2.yaml`；实验规则禁止从历史 split/budget 材料派生当前参数。因此单一权威判断得到支持。

### 2. 人类表面与 WorkItem 冲突是否会被拒绝 — `PASS`

在测试中故意让 WorkItem Fact owner 指向权威 recipe、WORKPLAN Owner 指向另一个文件。期待 drift 检查失败；实际 RED 阶段未报错，加入解析与路径比较后稳定报出 `node owner disagrees with WorkItem fact owner`，修正链接后通过。

### 3. 正确 recipe 能否进入注册流程、错误环境是否 fail closed — `PASS`（scoped）

在本地对 Cora/seed42/1% gate 执行 registered dry-run。期待 recipe 合同被接受，但正式工作只能在 reviewed AutoDL/main/device/profile/receipt 条件满足时继续。实际 dry-run 绑定当前 clean candidate 后，在这些缺失条件处退出并返回 `generated_artifacts=[]`，没有静默降级或生成实验 Artifact。

### 4. 与已接受父线组合后是否仍一致 — `PASS`

将 AAGU-018 的 accepted no-ff Apply 父线合入后，期待看板投影与 target-direct 合同测试同时成立。实际联合测试 `67 passed`，dashboard `--check`、Python 编译、Git ancestry、clean-status 和 diff 检查均通过。

## Agent 建议

**建议接受。** 当前候选解决的是活跃控制面上的权威歧义，并用通用 drift 校验防止复发；它没有复制 recipe 数值、添加兼容分支或擅自运行正式实验。

决定人：刘丞毓。可选择接受、指出具体返工项，或继续等待。

## 已知缺口与边界

- `NOT OBSERVED` — 未运行 AutoDL 正式 GPU cell、完整矩阵或 downstream GU；本报告不声称任何攻击效果或科研结论。
- `NOT CONFIRMED` — AAGU-019 的旧小预算 setup 硬退役尚未实现；它是独立 Block，不属于 AAGU-006 候选。
- 本 Block 不选择 IF/selector，不删除历史 Artifact，也不把旧证据改写成新合同证据。

## 技术附录

- 权威 recipe：`experiments/configs/syncmate_target_direct_formal_v2.yaml`
- 核心校验：`scripts/dashboard/refresh.py`
- RED/GREEN 回归：`tests/test_dashboard_refresh.py`
- 联合验证：9 个定向测试文件，`67 passed in 1.41s`
- Dashboard：`python -B -X utf8 scripts/dashboard/refresh.py --check` → `PASS`
- Dry-run：Cora / seed 42 / 1% / gate-only → recipe 接受，环境 gate 拒绝，`generated_artifacts=[]`
- Apply target：`refs/heads/codex/e7-two-surrogate-groups-20260805`，观察值 `6be95c7`
