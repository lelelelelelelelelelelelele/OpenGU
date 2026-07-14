---
title: Cache V2 Prediction to Evaluation 单 Cell Smoke
date: 2026-07-14
status: accepted-read-only-smoke
---

# Cache V2 Prediction → Evaluation 单 Cell Smoke

## 结论

**通过。** 对远端已完成的 `cora / GAT / GraphRevoker / im / seed42` cell 做只读复算后，`predictions.npz` 可独立导出的 9 个 Evaluation 指标与 `collateral.json` 一致。8 个指标逐值一致；`max_pred_shift` 的绝对差为 `1.1920928955078125e-7`，小于预先采用的 float32 容差 `1e-6`。

这是一项轻量下游 smoke，不是 Cache V2 runner 验收。它只证明该 cell 的 Prediction payload、selection 引用和 Evaluation 序列化彼此自洽，不要求新版 Selection producer 精确复制 provenance 不完整的 Legacy 节点序列。

## 验证范围

| 项目 | 值 |
|---|---|
| 远端实验 checkout | `/autodl-fs/data/opengu-experiments/e4-graphrevoker-multiseed-648a6f1-20260714/GULib-master` |
| cell | `results/runs/cora_GAT_r0.05/GraphRevoker_im/seed42` |
| producer commit | `648a6f10dae167fa238427427cbf7c1f660b4e57` |
| Prediction shape | 2708 nodes × 7 classes，float32 |
| selected nodes | 108 |
| 复算设备 | CPU；未连接 GPU |
| 浮点容差 | absolute tolerance `1e-6` |

## 复算结果

| 指标 | `collateral.json` | 从 `predictions.npz` 复算 | 绝对差 |
|---|---:|---:|---:|
| `perf_before` | 0.6051660516605166 | 0.6051660516605166 | 0 |
| `perf_unlearn` | 0.6383763837638377 | 0.6383763837638377 | 0 |
| `perf_retrain` | 0.6180811808118081 | 0.6180811808118081 | 0 |
| `drop_retrain` | -0.012915129151291449 | -0.012915129151291449 | 0 |
| `gap` | -0.02029520295202958 | -0.02029520295202958 | 0 |
| `gap_pct` | -3.2835820895522483 | -3.2835820895522483 | 0 |
| `mean_pred_shift` | 0.1041107252240181 | 0.1041107252240181 | 0 |
| `max_pred_shift` | 0.6046002507209778 | 0.6046003699302673 | 1.1920928955078125e-7 |
| `fraction_flipped` | 0.13848397135734558 | 0.13848397135734558 | 0 |

复算遵循当前正式定义：test mask 上计算 micro-F1；retain mask 上比较 unlearned 与 exact-retrained softmax 的逐节点 L-infinity shift，并比较两者预测类别得到 `fraction_flipped`。

## 结构与只读检查

| 检查 | 结果 |
|---|---|
| 三组 logits 全部 finite | 通过 |
| NPZ selected nodes 与 `attack.json` 有序序列一致 | 通过 |
| retain mask 等于 train mask 去除 selected nodes | 通过 |
| 9 个指标均在 `1e-6` 容差内 | 通过 |
| 验证前后源文件 size、mtime、SHA-256 不变 | 通过 |

源文件 SHA-256：

- `attack.json`: `9f61750aa79305f2f4069d9f5f1caa13cbfff55fb98dfbdc1c50b139a064862a`
- `collateral.json`: `1a903ca1346eed16864e24899c45c55d1badb70fc1973266e10cedb5c39ad3a7`
- `predictions.npz`: `b71a70d0236604480df965548a77582b24aea8c23701303e050d91da3e05681d`

## 边界

- 本 smoke 不运行 GU、retrain 或 GPU 计算。
- 本 smoke 不写 Cache、results 或远端实验文件。
- 本 smoke 不比较 Legacy Selection 与 V2 Selection，也不要求两者节点完全相同。
- 本 smoke 不证明 Score、Prediction、Evaluation 已成为正式 V2 Artifact。
- 本 smoke 不改变 runner 尚未接入 V2、conflict resolution 尚未完成的总体状态。

因此，下游指标一致性可以保留为轻量 smoke，而不应成为 Selection Cache 迁移的主要阻塞门槛。
