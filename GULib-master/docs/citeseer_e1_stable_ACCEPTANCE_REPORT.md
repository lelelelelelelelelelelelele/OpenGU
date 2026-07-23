---
title: Citeseer E1 Stable Matrix 真机验收报告
date: 2026-07-14
status: accepted-stable-scope
---

# Citeseer E1 Stable Matrix 真机验收报告

> [!NOTE]
> **路径迁移说明（2026-07-24）**：本文显示的 SSH 文件系统路径已更新为当前 archive/canonical access 位置，不能据旧执行语境重建 `/autodl-fs/data` sibling。原始执行字符串可从 Git `41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` 与迁移报告复核；实验数值和验收结论未改。

## 1. 验收结论

**Citeseer clean E1 稳定范围验收通过：50/50 cells，0 个结构错误，0 个 attack failure，runner 返回 0。** 本次在远端 RTX 4090 的 fresh checkout 上重算 5 个稳定方法 × 2 个策略 × 5 个 seed：

- 方法：GIF、IDEA、GNNDelete、MEGU、GraphEraser；
- 策略：random、IM；
- seed：42、212、722、1337、2024；
- 数据与模型：Citeseer / GCN / unlearn ratio 0.05。

**范围边界同样重要。** TracIn 按本轮决定排除；Hybrid 原本就不在 A5 Citeseer 配置；GraphRevoker 留到独立 E4 canary/整 method 重跑。本报告不能写成原 `A5_citeseer_r0.05.yaml` 的 90/90 完成，也不能把隔离 scratch Legacy-format cache 的复用写成 Cache V2 runner 命中。

| 验收面 | 结果 | 证据 |
|---|---|---|
| 矩阵完成度 | 通过 | 50/50；全量阶段 completed 49、skipped 1（首格 gate 已完成） |
| 运行状态 | 通过 | runner rc=0；日志 0 `[FAIL]/Traceback/ERROR`；0 `failed=true` |
| 四件套 | 通过 | 每格 `attack.json`、`collateral.json`、`predictions.npz`、`_meta.json` 完整可读 |
| 被测版本 | 通过 | 50 格 meta 均为 commit `aad4e994…`，config fingerprint 逐格重算一致 |
| Selection | 通过 | 每格 133 个唯一训练节点；attack/NPZ 顺序完全相同；跨方法 exact equality 全部通过 |
| Prediction | 通过 | before/retrain/unlearn logits 全部有限；必要数组与 mask 齐全 |
| active Legacy | 通过 | path/size/mtime_ns/SHA-256 聚合 hash 前后完全相同 |
| 既有 checkout | 通过 | 原 dirty checkout 的 `git status --short` 前后完全相同 |

## 2. 被测版本与隔离环境

| 项目 | 值 |
|---|---|
| Git branch | `codex/citeseer-e1-graphrevoker-20260714` |
| 被测 commit | `aad4e994a199499126e39491c4e31ba9d86c6578` |
| fresh outer clone | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiments/citeseer-e1-aad4e99` |
| code checkout | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiments/citeseer-e1-aad4e99/GULib-master` |
| evidence root | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiment-evidence/citeseer-e1-aad4e99` |
| active Legacy root | `/autodl-fs/data/OpenGU/GULib-master/results`（只读核验） |
| GPU | RTX 4090 24 GB |
| runner 配置 | `experiments/configs/A5_citeseer_r0.05_stable_notracin.yaml` |

旧 dirty checkout 没有被切 branch、清理、暂存或用于运行。所有实验输出、模型分片和 scratch cache 都落在 fresh checkout；机器证据放在 outer Git clone 之外，避免让 evidence 本身污染被测 worktree。

## 3. 执行结果

首格 `GIF/random/seed42` 先作为完整 gate 运行，耗时 105.7 秒，14/14 检查通过。随后执行全矩阵；首格被 runner 按完整四件套与 fingerprint 正确跳过：

~~~text
=== Summary ===
  completed: 49
  skipped: 1
  elapsed: 4610.4s
~~~

全矩阵结束时共有 50 个 `_meta.json`，runner rc=0。强验收器没有把“文件存在”当作成功，而是重新读取每格 JSON/NPZ、重算 runner fingerprint、检查 finite logits、selected nodes、train/retain mask 和数值范围；最终 `accepted=true`、`validated_cells=50`、`error_count=0`。

## 4. Selection 与 cache 证据

### 4.1 节点序列不变量

- 每格选择 133 个节点，全部唯一并属于该格 NPZ 的训练候选集；
- `attack.json` 与 `predictions.npz` 的 selected nodes 顺序逐项相同；
- random：同一个 seed 下 5 个方法的节点序列完全相同，5/5 seeds 通过；
- IM：5 个方法 × 5 个训练 seed 的 25 格节点序列全部完全相同，符合固定 `im_selector_seed=2024` 的 recipe；
- 被删除节点在 retain mask 中均为 false。

这些 exact comparisons 能排除“各方法重新算出不同 selection，却只凭日志声称 cache hit”的假阳性。

### 4.2 scratch cache 统计

| scratch 层 | 数量 | 解释 |
|---|---:|---|
| ResultCache | 50 JSON | `eval_collateral.py` 当前 runner 依赖；仅存在于隔离 checkout |
| SelectionCache | 6 JSON | 5 个 random seed recipe + 1 个 IM fixed-seed recipe |
| ScoreCache | 2 个逻辑 entry / 4 files | `im` 与 `im_celf` 各一组 JSON sidecar + NPZ |

这些都是现有 runner 在隔离目录中写出的 **Legacy-format scratch cache**。它们证明当前 runner 的 selection 复用和结果链条可运行，但不证明 Cache V2 已接入 runner。真实 Cache V2 Citeseer IM cold/warm exact hit 已由单独 canary 验收；两条证据必须分开描述。

## 5. 聚合指标

下表是 5 seeds 均值。`gap = perf_retrain - perf_unlearn`；正值代表 unlearn 低于 retrain，负值代表 unlearn 高于该次 retrain。`perf_before` 对 GraphEraser 是 method-specific shard/SISA before，不等同于 vanilla GCN baseline。

| 方法 | 策略 | perf_before | perf_retrain | perf_unlearn | gap | flipped |
|---|---|---:|---:|---:|---:|---:|
| GIF | random | 0.7511 | 0.7526 | 0.7508 | +0.0018 | 0.0408 |
| GIF | IM | 0.7511 | 0.7489 | 0.7508 | -0.0018 | 0.0399 |
| IDEA | random | 0.7511 | 0.7526 | 0.7508 | +0.0018 | 0.0408 |
| IDEA | IM | 0.7511 | 0.7489 | 0.7508 | -0.0018 | 0.0399 |
| MEGU | random | 0.7511 | 0.7520 | 0.7498 | +0.0021 | 0.0399 |
| MEGU | IM | 0.7511 | 0.7489 | 0.7505 | -0.0015 | 0.0397 |
| GNNDelete | random | 0.7511 | 0.7508 | 0.7387 | +0.0120 | 0.0900 |
| GNNDelete | IM | 0.7511 | 0.7465 | 0.7003 | **+0.0462** | **0.1320** |
| GraphEraser | random | 0.7036 | 0.6880 | 0.6886 | -0.0006 | 0.2862 |
| GraphEraser | IM | 0.7036 | 0.6880 | 0.6952 | -0.0072 | 0.2817 |

最清晰的效果差异出现在 GNNDelete：IM 的平均 retrain gap 为 +0.0462，random 为 +0.0120；其 prediction flip fraction 也由 0.0900 升至 0.1320。GIF、IDEA 与 MEGU 在该 Citeseer/r=0.05 范围接近 noise-floor。GraphEraser 的平均 shard/SISA before 为 0.7036，单格范围 0.6712–0.7252，明显低于其余方法的约 0.7511；这是真实观察项，后续写作必须保留 method-specific before 的口径说明，不能直接解释为攻击造成的退化。

## 6. Legacy 只读证明

扫描前后递归记录 active `results/cache`、`results/selection_cache`、`results/score_cache` 每个文件的：

1. 相对路径；
2. size；
3. mtime ns；
4. SHA-256。

两次聚合状态 hash 均为：

~~~text
b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa
~~~

物理文件计数保持 ResultCache 784、SelectionCache 111、ScoreCache 75。这里包含目录内 `CLAUDE.md`，且 ScoreCache JSON/NPZ 分开计数。原 dirty checkout 的短状态也前后一致；验收器初稿曾因扫描前使用目录折叠、扫描后使用 `--untracked-files=all` 展开而产生一次假报警，统一命令后重跑全验收为 0 errors。

## 7. 测试

本地：

~~~powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_phase_b_invariants.py `
  tests/test_cache_v2_selection_canary.py `
  tests/test_cache_v2_store.py -q
# 70 passed in 1.28s
~~~

远端 fresh checkout：

~~~bash
/root/miniconda3/bin/python -m pytest \
  tests/test_phase_b_invariants.py \
  tests/test_cache_v2_selection_canary.py \
  tests/test_cache_v2_store.py -q
# 70 passed in 3.17s（E1 checkout）
# 70 passed in 7.30s（GraphRevoker fresh checkout preflight）
~~~

## 8. 机器证据

| 文件 | 内容 |
|---|---|
| `gate1_acceptance.json` | 首格 14/14 gate |
| `full.log` / `full.rc` | 全量 runner 日志与返回码 |
| `e1_acceptance.json` | 50-cell 强验收、选点等价、聚合指标、Legacy 不变量 |
| `pytest_preflight.log` | 远端相关回归 |

远端证据根：

~~~text
/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiment-evidence/citeseer-e1-aad4e99
~~~

## 9. 未完成边界与下一步

1. GraphRevoker 不属于本次 50-cell 接受集。E4 必须验证旧 aggregator 修复和 2026-07-10 shard-ensemble wrapper，先 random/seed42 canary，再扩 random/degree/pagerank/IM；
2. TracIn 与 Hybrid 本轮明确不做，不能把其缺失写成失败或补齐；
3. 当前 runner 尚未接 Cache V2；E1 的 scratch hit 不改变这一事实；
4. 本次没有把远端大 payload 搬回 repo，也没有修改、迁移或删除任何 active Legacy Cache；
5. GraphRevoker canary 通过后，才讨论 4-strategy × 5-seed 的整 method E4 重跑；若出现低 `perf_before`、checkpoint/weight 不一致或 aggregate 越界，应 fail closed 并先排错。

