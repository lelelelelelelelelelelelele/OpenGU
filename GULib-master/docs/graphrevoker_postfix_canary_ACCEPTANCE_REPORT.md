---
title: GraphRevoker Post-fix Canary 与 Cache V2 Recheck 验收报告
date: 2026-07-14
status: seed42-canary-accepted-full-e4-pending
---

# GraphRevoker Post-fix Canary 与 Cache V2 Recheck 验收报告

> [!NOTE]
> **路径迁移说明（2026-07-24）**：本文显示的 SSH 文件系统路径已更新为当前 archive/canonical access 位置，不能据旧执行语境重建 `/autodl-fs/data` sibling。原始执行字符串可从 Git `41708162a4f3e2c4fd89c30c47b6b35feb1b8d75` 与迁移报告复核；实验数值和验收结论未改。

## 1. 验收结论

**GraphRevoker 修复后的 Cora/GCN/r=0.05、seed 42 四策略 canary 通过；Cache V2 当前提交 cold/warm recheck 也通过。** 本轮执行 random、degree、pagerank、IM，明确不执行 Hybrid 与 TracIn。GraphRevoker runner 返回 0，机器验收 `accepted=true`、0 errors；当前提交的真实 Citeseer Selection V2 canary 则证明 cold miss 后的第二个独立进程 exact hit，同一 Artifact 未再次调用 producer。

这两个结论必须分开：GraphRevoker 实验仍由现有 runner 写入隔离 checkout 的 Legacy-format scratch cache；Cache V2 命中来自独立 store canary。**当前 runner 尚未接入 V2，本报告也不把 seed42 canary 写成完整 E4 method gate。**

| 验收面 | 结果 | 证据 |
|---|---|---|
| GraphRevoker 四策略 | 通过 | 4/4 四件套；completed 3 + skipped 1；0 attack failure |
| 修改后的 shard ensemble | 通过 | 10 baseline + 10 unlearned checkpoints；10 个有限非负权重且和为 1 |
| Prediction / collateral | 通过 | logits 全有限；NPZ 复算 test micro-F1 与 JSON 精确一致 |
| 策略选点 | 通过 | 每策略 108 个唯一训练节点；attack/NPZ 同序；四个有序序列互不相同 |
| Cache V2 recheck | 通过 | cold producer called；warm fail-if-called 哨兵下 producer 未调用 |
| active Legacy | 通过 | 970 个物理文件的 path/size/mtime_ns/SHA-256 前后逐项相同 |
| 回归测试 | 通过 | 本地 151 passed；远端 151 passed |

## 2. 范围、版本与隔离

| 项目 | 值 |
|---|---|
| Git branch | `codex/citeseer-e1-graphrevoker-20260714` |
| 被测 HEAD | `93095d9b8ea7e6c3972ffda70b74b232fafaf887` |
| GraphRevoker 配置 | `experiments/configs/sanity_graphrevoker_r05_notracin.yaml` |
| fresh code checkout | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiments/graphrevoker-cora-aad4e99/GULib-master` |
| GraphRevoker evidence | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/opengu-experiment-evidence/graphrevoker-cora-aad4e99` |
| V2 recheck root | `/autodl-fs/data/OpenGU/GULib-master/results/_archive_ssh_peer_layout_20260724/peer_roots/cache-v2-canary/citeseer-93095d9-recheck` |
| active Legacy root | `/autodl-fs/data/OpenGU/GULib-master/results`（只读核验） |
| GPU | RTX 4090 24 GB |

random 先作为单格 gate 在 `aad4e99` 完成；四策略 runner 随后在 `93095d9` 复用该完整 cell，所以摘要为 completed 3、skipped 1。`aad4e99..93095d9` 只新增报告、dashboard 和实验 YAML，Python 代码完全相同；random 结果不是从不同算法版本借用。

远端最初无法从 GitHub 下载 Cora，首次 canary 在数据加载前 fail closed。随后只读复制 active checkout 中 canonical processed Cora fixture 到隔离 clone；源文件复制前后 SHA-256 相同，没有复制 Legacy Cache 或旧 GraphRevoker 结果。旧 dirty checkout 从未切 branch、清理、暂存或用于运行。

## 3. GraphRevoker 执行结果

~~~text
=== Summary ===
  completed: 3
  skipped: 1
  elapsed: 2686.6s
~~~

| 策略 | attack F1 | MIA AUC | before | retrain | unlearn | gap | flipped | attack total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random | 0.7232 | 0.8466 | 0.7269 | 0.7288 | 0.7159 | +0.0129 | 0.0345 | 120.3s |
| degree | 0.7343 | 0.7296 | 0.7269 | 0.6993 | 0.7159 | -0.0166 | 0.0306 | 124.9s |
| pagerank | 0.7122 | 0.7800 | 0.7214 | 0.7177 | 0.7103 | +0.0074 | 0.0364 | 165.0s |
| IM | 0.7122 | 0.8408 | 0.7232 | 0.7177 | 0.7196 | -0.0018 | 0.0345 | 1995.5s |

口径：`before/retrain/unlearn` 是 test mask 上的 micro-F1；`gap = retrain - unlearn`；`flipped` 是 retain set 上 unlearned 与 retrained prediction 的不同占比。单 seed 的正负 gap 只说明这一次 retrain 的相对位置，不能据此给策略排机制优劣。

IM 的 selection 为 25.3s，但 attack total 为 1995.5s。主要成本不是 selector，而是 GraphRevoker MIA：对 100 个删除节点和 100 个 test negatives，逐节点重建 10 个 shard 视图并加载 before/unlearned 模型。高影响节点使首次 IM MIA 明显慢于 random/degree/pagerank；这是完整 5-seed E4 前必须纳入预算的真实性能边界。

## 4. 修改代码的正确性证据

### 4.1 结构与数据链

- 四个策略均有 `_meta.json`、`attack.json`、`collateral.json`、`predictions.npz`；
- 每策略 108 个 selected nodes，全部唯一且属于 train mask；
- `attack.json` 与 NPZ 的 selected nodes 顺序逐项相同；
- 四个策略的 ordered-selection SHA-256 均不同；
- before、retrained、unlearned logits 均为 `[2708, 7]` 且全部 finite；
- 从 NPZ 重新 argmax 并计算 test micro-F1，与 collateral 三个 performance 字段精确一致；
- `fraction_flipped` 按正式代码定义，在 retain mask 上对比 unlearned 与 retrained prediction，四策略均复算一致。

机器验收初稿曾把 `fraction_flipped` 错写成 test mask 上 before vs unlearned 的比较，因此四策略同时误报。对照 `attack/attack_eval.py` 的正式定义后修正验收器并重跑，最终 10/10 checks、0 errors；实验文件没有被改写。

### 4.2 GraphRevoker shard ensemble

当前 wrapper 不再把一个 shard 当作完整模型，而是加载 10 个 shard checkpoint 和 GraphRevoker optimal weights。最终状态满足：

| 检查 | 结果 |
|---|---|
| baseline shard checkpoints | 10 |
| unlearned shard checkpoints | 10 |
| weights | 10；min 0.08564；max 0.11205 |
| weight sum | 0.99999994 |
| finite / non-negative | 全部通过 |

旧 C5 的 0.50–0.58 collateral before 来自通用路径错误抽取单 shard。当前四格 before 为 0.7214–0.7269，且 random gate 中 wrapper 输出与 GraphRevoker 自身 aggregator 的 0.7269/0.7159/0.7288 相符；因此单 shard regression 已关闭。不同策略的 logits 数组并不相同，即使个别 accuracy 恰好相同，也不是复用同一 prediction 的假结果。

## 5. Scratch Cache 与 V2 边界

GraphRevoker 四策略在隔离 checkout 中生成 4 个 ResultCache JSON、4 个 SelectionCache JSON；IM 还产生 `im` 与 `im_celf` 两个逻辑 ScoreCache entry。它们都是现有格式的 scratch cache，未触碰 active Legacy，但也**不是 Cache V2 runner hit**。

当前提交另行创建全新 V2 store：

| 字段 | cold | warm |
|---|---:|---:|
| `hit` | false | true |
| `producer_called` | true | false |
| producer call count | 1 | 1 |
| resolve | 32.551s | 0.133s |
| end-to-end | 36.409s | 2.901s |

cold 与 warm 的共同 identity：

- Artifact ID：`sel_82ce3701_c25a3ec2`；
- Recipe hash：`82ce3701ea07851534a0b77a615472d25f7af649a3d88f0c0751e34fb6783a02`；
- content/payload SHA-256：`c25a3ec2d9e44806fbe98444eadacb974b11bbceea78d595bfb0b42524ed0597`；
- 133 个有序节点逐项相同，payload mtime/size 不变；
- warm 更改了 `config_name`、YAML path 与 experiment ID，但仍命中相同 Recipe；
- SQLite `integrity_check=ok`、schema v1、1 Artifact、0 conflict。

warm 由独立进程运行并启用 fail-if-called producer 哨兵；如果 resolver 先重算再声称命中，该进程会失败。本次 warm 返回 0，因此这是真实 V2 exact hit。它仍是隔离 Selection canary，不代表 `experiments/run.py` 已接入 V2。

## 6. Legacy 与环境不变量

GraphRevoker 前后对 active `results/cache`、`results/selection_cache`、`results/score_cache` 的 970 个物理文件逐项记录相对路径、size、mtime ns 和 SHA-256。相同算法的聚合状态 hash 前后均为：

~~~text
c5ee3a75ff92d4fa10997085ea83309887210c44aff4efee72ff7094835980b2
~~~

Cache V2 canary 自己的 canonical Legacy state hash 在 cold/warm 前后均为：

~~~text
b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa
~~~

两个 hash 的序列化算法不同，不能互相比较；各自在扫描前后保持相同。旧 checkout 的 `git status --short` 前后 SHA-256 均为 `f671c50f…`，证明本轮没有覆盖其它 session 的 dirty files。

## 7. 测试

本地与远端都在当前 branch 运行同一组相关回归：

~~~text
tests/test_cache_v2.py
tests/test_cache_v2_store.py
tests/test_cache_v2_selection_canary.py
tests/test_score_cache.py
tests/test_attack_manager.py
tests/test_phase_b_invariants.py
tests/test_config_inventory_dashboard.py

151 passed
~~~

本地只有既有 `llvmlite/pkg_resources` deprecation warning；远端只有 TBB 版本 warning，均无测试失败。

## 8. 未完成边界与下一 Gate

本次关闭的是 **GraphRevoker post-fix seed42 四策略 canary**，不是完整 E4：

1. E4 仍需按正式 seed 集扩展，并决定是否同时覆盖 GCN/GAT；
2. 扩展前按 IM cold MIA 约 33 分钟/格制定预算，必要时先做不改变语义的 profile；
3. 多 seed 结果继续用 NPZ 复算、shard/weight 检查和 active Legacy 不变量验收；
4. Hybrid 与 TracIn 继续排除，除非另开 selector gate；
5. Cache V2 runner 接入是独立架构 gate：不得把 scratch hit 当作 V2，不得在 V2 查询异常时静默回退 Legacy；
6. 在 runner V2 gate、迁移覆盖率和回滚窗口通过前，Legacy 继续只读，不能归档或删除。
