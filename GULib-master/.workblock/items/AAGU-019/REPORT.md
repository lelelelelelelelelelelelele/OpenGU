# AAGU-019 · 旧小预算实验 setup 退役验收报告

报告新鲜度：`2026-08-31 03:09 +08:00；在本轮候选形成前重跑 focused verification`

> 当前验收决定：`接受`

## 这次改变了什么

这个 Block 把仍可执行的历史 `k=3/7/14` / fixed-`k=7` 实验面，改成了
“历史证据继续只读保留、当前只允许 ratio-conditioned target-direct
合同执行”。旧包、旧配置和旧 SyncMate recipe 被硬删除；当前仍需使用的
dataset-source、scoring、Recipe validation 和 Planetoid I/O 原语被迁入中性或
target-direct 模块，没有兼容层或旧路径 fallback。

## 现在实际看到了什么

基线 registry 有 76 条 recipe，其中 44 条属于已退役 small-selection lane；
当前 registry 有 32 条，旧 recipe ID 为 0，29 条 target-direct recipe 和 3 条
通用 recipe 保持可用。正式配置仍只接受 1%/5%，对应 Cora `18/94`、
CiteSeer `23/116`、PubMed `138/690`，没有 fixed-`k=7` fallback。

历史 `results/` 与 `reports/` tracked 子树没有任何 diff；A.6 仍提供历史
导航，但明确排除这些材料作为新图表或当前 formal claim 的输入。

## 最关键的证据

| 判断面 | 基线 | 本轮待接受状态 | 结果 |
|---|---:|---:|---|
| 活动 recipe 总数 | 76 | 32 | PASS |
| 活动 legacy recipe | 44 | 0 | PASS |
| 活动 target-direct recipe | 29 | 29 | PASS |
| 旧 executable config | 13 | 0 | PASS |
| target-direct 比例 | 1% / 5% | 1% / 5% | PASS |
| 历史 `results/` / `reports/` tracked diff | 不适用 | 0 | PASS |
| formal GPU 新结果 | 未要求 | 未运行 | NOT OBSERVED |

focused suites 共 331 个测试明确退出为 green。额外的全仓 pytest 在约 12
分钟后仍持续 CPU 执行且无失败输出，随后被人工中止；它没有终态，因此不计
入 PASS 数量。

## Agent 建议

`建议接受`。验收合同中的四个实质判断均有直接的源码、registry、配置和
回归测试证据；唯一未观察的是 formal GPU，而它明确属于本 Block 的 non-goal，
不能被解释成新研究证据。

## 验收决定

- 需要决定：由用户判断是否接受“旧设置不可再执行、历史证据仍可追溯、
  当前 formal lane 身份不变”的本轮候选。
- 决定对象：本报告所绑定的 AAGU-019 clean source-branch HEAD。
- 决定依据：接受或返工后填写。
- 决定时间：接受或返工后填写。

## 判断详情

### 旧 setup 已无法从活动入口启动 — PASS

在操作员通过 SyncMate 或 OpenGU CLI 选择实验时，期待旧 package、旧 config
和旧 recipe 不再形成可调度入口。实际观察到三个旧 package 的 tracked Python
source、13 个旧配置、44 条 registry 定义及对应 preflight/acceptance wrapper
均已移除；活动 registry 对旧 recipe ID 的计数为 0，因此该判断得到支持。

### target-direct 已脱离旧包 — PASS

在当前 formal lane 导入 split、scoring 和 Recipe identity 时，期待不依赖被
退役的模块。全仓活动 Python surface 审计未发现三个旧模块 import；当前实现
从 `planetoid_source.py`、`target_direct_v1/scoring.py`、
`target_direct_v1/planetoid_io.py` 和自包含 Recipe 构建器读取所需原语，因此
该判断得到支持。

### ratio-conditioned 合同没有被改写 — PASS

在 Cora、CiteSeer、PubMed formal 配置被加载时，期待只接受 1%/5% 与已注册
exact-k。实际配置与测试观察到 `18/94`、`23/116`、`138/690`，rounding 仍为
`floor_with_minimum_one`，且缺少/错误 manifest、candidate count、checkpoint
身份会 fail closed，因此该判断得到支持。

### 历史证据保留但不再充当当前输入 — PASS

在审计历史证据边界时，期待 accepted result payload、报告和 Cache V2 identity
不被删除或重写，同时不再进入当前 figure/paper 输入。实际 Git diff 对
`results/` 与 `reports/` 为空，树 identity 分别仍为
`3bbc950bcb0906621c8bf682eda00b70555c4bad` 和
`4e9e6ecf8d991c6e38008dcf40f97d3d96231f6f`；A.6 只保留历史导航并明确排除
当前 claim，因此该判断得到支持。

### formal GPU 行为 — NOT OBSERVED

本 Block 没有 dispatch GPU gate 或 matrix，也没有生成新实验结果。此项不能
证明研究结果，只能证明执行入口与身份边界已准备好。

## 已知缺口与边界

- 未完成的全仓 pytest 没有终态，不作为 green 或 red 证据；所有直接受影响
  surface 均由明确退出的 focused suites 覆盖。
- 本次不判断 GPU runtime、科学指标、formal matrix 是否通过，也不接受任何
  新论文 claim。
- 本次不 Apply、不 push、不安装、不清理其他 Claim；AAGU-009 未被修改。

## 下次接手

- 当前状态：AAGU-019 focused Verify 完成，等待用户决定。
- 已确认变化：旧 setup 的活动入口已退役，历史 tracked evidence 未变。
- 下一步：用户接受则交给 `block-closeout`；返工则在同一 Claim/WorkItem 修正。
- 不要重复：不要重跑旧 fixed-k setup，不要把历史结果改写成 1%/5%。
- 关键入口：本目录 `WORKITEM.md`、`REPORT.md`、`REPORT.html`。

## 技术附录

- Git baseline：`cdfb8a0ece41922beb447c2279569ae9448396aa`
- Source branch：`refs/heads/codex/aagu-019-retire-legacy-budgets`
- Apply target（未改变）：`refs/heads/codex/e7-two-surrogate-groups-20260805`
- 候选：由本次 `block-workflow finish` 形成的同一 clean source-branch HEAD；
  精确 SHA 以 WorkItem/Claim runtime 记录为准。
- Verify：44 个 retirement/target-direct/adapter/deployment tests；230 个
  SyncMate/Cache/report tests；57 个 dataset-source consumer/selection tests；
  均 exit 0，合计 331 passed。
- 静态检查：受影响 Python `compileall`、registry inventory、活动引用 `rg`、
  `git diff --check`。
- 证据边界：只证明代码/registry/config/历史 tracked tree 的候选行为；不证明
  GPU 或研究指标。
- HTML 渲染检查：`PASS`；在 1280×720 桌面视口真实打开，首屏完整显示
  变化、观察、Agent 建议和唯一决定投影，无横向溢出、断图或层级问题。
