---
title: Cache V2 Gate 3 四 Artifact 对照进度报告
date: 2026-07-16
status: harness-accepted-gate-open
---

# Cache V2 Gate 3 四 Artifact 对照进度报告

## 1. 结论

**COMPARISON HARNESS ACCEPTED；GATE 3 仍未通过。** 本地 CPU 已完成只读四 Artifact 对照政策、确定性机器报告和 fail-closed 回归。Selection 必须有序精确一致，Prediction/Evaluation 只能按报告中显式的浮点容差通过；缺 provenance 或非有限值直接失败。

Gate 3 没有被勾选：本机标准 checkout 没有 `predictions.npz`，无法形成 provenance 完整的真实四类型样本；已有 ogbn-arxiv IM Legacy/V2 Selection 仅交集 1252/1354，仍是明确失败。Gate 4 真实 GU/GPU runner canary 也未执行。

| 项目 | 状态 | 证据 |
|---|---|---|
| 四类型 normalized contract | 完成 | Score、Selection、Prediction、Evaluation reference dataclasses |
| 显式 tolerance policy | 完成 | 每类 `atol/rtol` 写入 canonical report |
| Selection exact rule | 完成 | 同集合不同顺序失败；set/Jaccard 仅作诊断 |
| Prediction/Evaluation comparison | 完成 | exact context + float max diff/mismatch count |
| Deterministic machine report | 完成 | canonical JSON + stable SHA-256，无 timestamp |
| Cache ownership | 通过 | `cache_v2` 不导入 comparison/Legacy policy |
| 标准 Legacy 只读 | 通过 | 三目录 aggregate hash 前后完全一致 |
| 真实四 Artifact sample | 未完成 | 本机 `results/runs` 没有 `predictions.npz` |
| Gate 3 overall | 未通过 | 已知 IM ordered/set mismatch 未解决 |

## 2. 实现

- `experiments/artifact_comparison.py`：规范化 reference observations、float policy、四类 comparer、bundle identity gate 与 canonical report。
- `tests/test_cache_v2_gate3_comparison.py`：8 项政策测试，覆盖 tolerance 内/外、ordered mismatch、已知 IM overlap、missing provenance、metric keys、non-finite、输入不变和 Cache 静态边界。

详细设计见 `docs/cache_v2_gate3_comparison_harness_DESIGN.md`。

## 3. 已知 IM 失败被保留

| 字段 | 值 |
|---|---:|
| Legacy / V2 selection size | 1354 / 1354 |
| intersection | 1252 |
| Legacy-only / V2-only | 102 / 102 |
| Jaccard | 0.859890 |
| Gate 3 verdict | failed |

Harness 同时报告 ordered hash 与 set overlap，但通过条件只看完整 ordered sequence 与 provenance；不会用 Jaccard 掩盖 mismatch。

## 4. 本机真实数据边界

只读盘点标准 checkout `E:/project/OpenGU/GULib-master/results`：

| Root | Files | Bytes | State hash |
|---|---:|---:|---|
| `score_cache` | 27 | 703,623 | `12a4d74d567807e30dada6934cb26cd68a505308f57eb91937a1cfff053d663a` |
| `selection_cache` | 10 | 22,663 | `acb9839f9f9cdd87668fff949b320494ebddd20f1cd394466f09aafe5105f8cc` |
| `runs` | 2,482 | 12,230,923 | `d7a97b63af230f42ef1e496577683bc20cc784799b36a5559bbd00f1a6e38913` |
| combined | 2,519 | 12,957,209 | `e49d959581c713dad877d999d790c1f423aa50f954ef68810547a92a83eda832` |

前后快照包含 relative path、size、mtime_ns 和每文件 SHA-256；测试前后 combined hash 相同。`runs` 有 826 组 attack/collateral，但没有 `predictions.npz`，不能把 JSON 指标反向伪装成 PredictionArtifact。

## 5. 测试

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_cache_v2_gate3_comparison.py
# 8 passed in 0.05s
```

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q `
  <all tests/test_cache_v2*.py> tests/test_auto_report_v3.py
# 145 passed in 4.62s
```

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q tests `
  --ignore=tests/test_report_figure_refresh.py `
  --deselect=<3 existing AttackPipeline stub tests>
# 527 passed, 3 deselected in 18.39s
```

3 个 deselected 仍是既有 AttackPipeline stub 缺少 `args`，不在本分支修改。CUDA 设为 `-1`，没有运行 GPU；TracIn/Hybrid 机制未改。

## 6. 完成清单

- [x] 独立 child worktree/branch，parent 为 Gate 2 accepted commit。
- [x] 四 Artifact 规范化 reference contract 与显式 tolerance policy。
- [x] Selection ordered exact、Score ranking、Prediction logits、Evaluation metrics 比较。
- [x] canonical report、稳定 hash、详细 mismatch diagnostics。
- [x] 已知 IM mismatch 固化为失败测试，不伪造等价。
- [x] Cache 静态职责边界、CPU scope/wide 回归、Legacy 快照不变。
- [x] 简洁设计与一致的 Markdown/HTML 进度报告。
- [ ] provenance 完整的真实四 Artifact old/new sample。
- [ ] 所有抽样 Selection ordered sequence 精确一致。
- [ ] Gate 3 overall pass。
- [ ] Gate 4 真实 runner/GPU canary。

## 7. 下一步

最小下一步是取得已有、只读、含 `predictions.npz` 的真实 sample（优先沿用已验过的 Cora 2708×7 cell），补齐同一 identity 的 Score/Selection reference，并用本 harness 输出机器报告。该工作需要服务器只读数据访问或已有 bundle，不应通过本地合成数据宣布 Gate 3 通过。
