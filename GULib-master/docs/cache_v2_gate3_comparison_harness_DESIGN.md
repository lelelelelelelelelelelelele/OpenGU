---
title: Cache V2 Gate 3 四 Artifact 对照 Harness 设计
date: 2026-07-16
status: implemented-local-harness
---

# Cache V2 Gate 3 四 Artifact 对照 Harness 设计

## 1. 设计结论

Gate 3 的“新旧结果对照”属于 experiment/migration 层，不属于 Cache。`experiments/artifact_comparison.py` 接收已经规范化的 Legacy/reference observations 与正式 V2 payload，按预先声明的 equality/tolerance policy 生成确定性机器报告；它不扫描、不修改 Legacy 文件，也不改变 Cache exact resolver。

Harness 完成不等于 Gate 3 通过。Gate 3 只有在真实、provenance 完整的 Score、Selection、Prediction、Evaluation 样本全部满足规则后才能关闭；当前已知 ogbn-arxiv IM Selection mismatch 仍然是失败证据。

## 2. 对照规则

| Artifact | 精确比较 | 容差比较 | Fail-closed 条件 |
|---|---|---|---|
| Score | graph/candidate/node-space、ordered ranking、scores presence | score values 使用显式 `atol/rtol` | ranking 顺序不同、score 缺失状态不同、identity 缺失 |
| Selection | graph/candidate/node-space、ordered selected nodes | 无 | set 相同但顺序不同仍失败；只给 Jaccard 不通过 |
| Prediction | graph/split/node-space、y、masks、selected nodes、class order | 三组 logits 分别使用显式 `atol/rtol` | shape、mask、node/class 或 provenance 不一致 |
| Evaluation | graph、metric name/version、metric key 集合 | 每个 numeric scalar 使用显式 `atol/rtol` | key、version、非有限/非 scalar metric 不一致 |

默认验收证据使用 `atol=1e-6, rtol=0`，但 policy 必须显式写入每份报告，不能依赖调用方隐含默认。

## 3. 输入与输出

```text
Normalized reference bundle
  + Formal V2 payload bundle
  + Formal Artifact IDs
  + Explicit comparison policy
  -> per-type result
  -> deterministic Gate3ComparisonReport JSON
```

机器报告记录：

- comparison contract 与三类 float tolerance；
- reference IDs 与四个 formal Artifact IDs；
- 每类 reasons、identity old/new 值、shape、mismatch count 与 max absolute difference；
- Score/Selection ordered hashes、intersection、双方独有节点数与 Jaccard；
- Evaluation 每个 metric 的 old/new 实值与差异；
- overall `passed/failed` 与稳定 report SHA-256。

报告不带生成时间，因此同一输入和 policy 产生相同 canonical JSON/hash。

## 4. 边界与已知失败

- `cache_v2` 静态测试禁止导入 `artifact_comparison`；Legacy interpretation 不回流 Cache。
- 缺 graph/split/candidate/metric version 等 provenance 时生成明确 failure reason。
- 非有限值、重复节点、错误 shape、断裂的 formal Score→Selection→Prediction→Evaluation identity 在比较前 fail closed。
- 已知 IM 案例的 1252/1354 intersection、双方各 102 个独有节点、Jaccard 0.859890 被固化为失败测试；不会因“相似度高”改判通过。

## 5. 后续真实 Gate 3 入口

下一步需要只读取得一个 provenance 完整且含 `predictions.npz` 的真实 old/new 四 Artifact 样本，先由 experiment adapter 规范化，再交给本 harness。当前本机标准 checkout 没有 `predictions.npz`，因此本分支不伪造真实 Prediction 对照，也不启动 SSH/GPU。
