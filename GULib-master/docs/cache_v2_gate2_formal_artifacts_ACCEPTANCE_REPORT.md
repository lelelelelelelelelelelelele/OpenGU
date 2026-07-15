---
title: Cache V2 Gate 2 正式 Artifact 验收报告
date: 2026-07-16
status: accepted-local-gate2
---

# Cache V2 Gate 2 正式 Artifact 验收报告

## 1. 验收结论

**GATE 2 ACCEPTED（本地 CPU）。** Dataset/Selection 职责越界修复保持有效；Score、Prediction、Evaluation 现在具备正式 Recipe、版本化 payload、不可变 Artifact、依赖 DAG、冲突隔离和递归完整性校验。exact HIT 零 producer、零写入；clean MISS 只由 experiment 层调用注入 producer，再把显式 payload 交给 Cache。

这不等于“整个 Cache V2 rollout 已完成”：Gate 3 的四 Artifact 完整对照和 Gate 4 的真实 GU/GPU canary 仍未完成。服务器最小 CPU smoke 是单独的非阻塞 TODO，不影响本地 Gate 2 判定。

| 验收项 | 结论 | 证据 |
|---|---|---|
| Cache ownership | 通过 | formal Cache 模块没有 experiment/dataset/selector/evaluator/Torch/PyG/OGB/download import |
| Score Artifact | 通过 | v1 Recipe；deterministic ordered ranking/scores codec；finite 与 identity 校验 |
| Prediction Artifact | 通过 | 三组 N×C logits、labels/masks/selection/class order；Selection 依赖 |
| Evaluation Artifact | 通过 | versioned metric Recipe；canonical JSON metrics；Prediction 依赖 |
| HIT / MISS | 通过 | warm exact HIT 零写入、零 producer；clean MISS producer 恰好一次 |
| Integrity / conflict | 通过 | 三类型 payload/header corruption fail-closed；冲突 marker + quarantine；递归父依赖校验 |
| Legacy / protected paths | 通过 | 测试哨兵不变；没有双写或修改受保护 results/archive |
| Runner / AutoReport | 通过 | 继承回归保持 selection-only、attack-only、complete、failed:collateral 与 provenance |
| Gate 3 / Gate 4 | 未完成 | full old/new comparison 与真实 GU/GPU canary 不在本分支 |

## 2. 实现落点

- `cache_v2/formal_artifacts.py`：Score/Prediction/Evaluation v1 Recipe builders、严格 payload contracts 与确定性 codecs。
- `cache_v2/formal_store.py`：exact-only typed store/read、依赖注册、递归 payload/header verification、conflict marker/quarantine。
- `experiments/artifact_producer.py`：experiment-owned resolve-then-produce seam；只在 `no_exact_candidate` 时调用 producer。
- `cache_v2/store.py`：补齐既有完整性异常路径需要的 `CacheV2Error` import；Selection 对外行为不变。
- `tests/test_cache_v2_formal_artifacts.py`：19 项 Gate 2 contract、HIT/MISS、corruption、dependency、Legacy sentinel 与 canonical Cora shape 测试。

详细契约见 `docs/cache_v2_gate2_formal_artifacts_DESIGN.md`。

## 3. 关键行为

### 3.1 Exact HIT

```text
Recipe + Artifact type
  -> exact resolver
  -> own payload/header verification
  -> recursive dependency bytes/identity verification
  -> return existing Artifact
```

warm test 在调用前记录整个 V2 store 的文件 hash、mtime 与 size，返回后完全相同；forbidden producer 没有被调用。若 exact candidate 损坏，调用直接抛出 integrity error，producer 调用数仍为 0。

### 3.2 Clean MISS

```text
Cache proves no_exact_candidate
  -> experiments layer producer()
  -> typed payload validation
  -> immutable write + index/dependency transaction
```

Cache API 不接受 dataset provider、GU method、selector 或 evaluator callback。producer 返回错误 payload type 时不会初始化或写入 store。

### 3.3 依赖与冲突

- Prediction Recipe/payload 绑定 Selection Artifact ID 与 ordered selected-node hash。
- Evaluation Recipe/payload 绑定 Prediction Artifact ID。
- Evaluation HIT 会递归检查 Prediction 与 Selection 的真实 payload/header；父文件损坏会阻断子 HIT。
- 相同 Recipe 的不同内容对三种 Artifact 都会进入 quarantine 并写 durable conflict marker；此后 exact resolver fail closed。

## 4. Canonical Cora 形状 fixture

新增 CPU-only fixture 使用现有 canonical processed Cora 的形状边界：

| 字段 | 值 |
|---|---:|
| nodes | 2708 |
| classes | 7 |
| persisted candidates | 2166 |
| selected nodes | 108 |
| logits | 3 × `[2708, 7]` float32 |
| execution | NumPy + SQLite，CUDA 禁用 |

fixture 验证 Selection→Prediction→Evaluation store/read roundtrip，不下载数据、不创建临时 dataset path、不运行 GPU。

## 5. 测试证据

### 5.1 Gate 2 focused

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
E:/conda_package/envs/gnn/python.exe -m pytest -q tests/test_cache_v2_formal_artifacts.py
# 19 passed in 1.09s
```

### 5.2 Cache、runner、AutoReport 范围回归

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest -q `
  <all tests/test_cache_v2*.py> tests/test_auto_report_v3.py
# 137 passed in 5.19s
```

该范围包含 dataset boundary、Legacy freeze、conflict resolution、selection-only / attack-only / complete / failed:collateral 与 AutoReport authority/source/Recipe 表达。

### 5.3 宽 CPU 回归

```powershell
$env:CUDA_VISIBLE_DEVICES='-1'
E:/conda_package/envs/gnn/python.exe -m pytest -q tests `
  --ignore=tests/test_report_figure_refresh.py `
  --deselect=<3 existing AttackPipeline stub tests>
# 519 passed, 3 deselected in 16.97s
```

3 个 deselected 仍是父分支记录的既有 `AttackPipeline` stub 缺少 `args`，不在本 Gate 修改。首次使用空 CUDA 环境变量时本机 RTX 5070 仍可见，9 个 TracIn/Hybrid 测试尝试不兼容 kernel；改为 `-1` 后全部通过，未修改其机制。

## 6. 完成清单

- [x] 从已接受的 dataset 解耦分支创建独立 child worktree/branch。
- [x] 定义 Score、Prediction、Evaluation 正式 Recipe 与 payload v1 契约。
- [x] Cache 只保存/解析上游 payload，不调用 producer 或访问 dataset。
- [x] exact HIT 零写入、零 producer；clean MISS 由 experiment 层注入 producer。
- [x] 三类 Artifact 的 ID、header、payload、冲突、quarantine 与损坏 fail-closed 测试。
- [x] Prediction→Selection、Evaluation→Prediction 依赖注册和递归实际字节校验。
- [x] canonical Cora 形状 CPU fixture、范围回归和宽 CPU 回归。
- [x] 简洁设计说明与一致的 Markdown/HTML Gate 2 验收报告。
- [ ] Gate 3 四类 Artifact full old/new comparison。
- [ ] Gate 4 真实 GU runner/GPU canary。
- [ ] 标准服务器根最小 CPU smoke（非阻塞环境 TODO）。

## 7. Git 与边界状态

本改动位于 `codex/cache-v2-gate2-artifacts-20260716`，parent 为 `codex/cache-v2-decouple-dataset-20260715`。没有 push、merge、Legacy promotion、results/cache/results/runs 修改或服务器 archive 修改；是否合入 parent 由后续验收决定。
