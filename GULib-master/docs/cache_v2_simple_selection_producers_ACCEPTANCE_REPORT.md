---
title: Cache V2 Simple Selection Producers 验收报告
date: 2026-07-14
status: ssh-canary-accepted-gates-remain-partial
---

# Cache V2 Simple Selection Producers 验收报告

## 1. 验收结论

Random、Degree、PageRank 已接入与 IM 相同的 Cache V2 exact-only SelectionArtifact 主路径，并通过本机与 SSH 真实 Cora cold/warm 验收。首次 SSH 重放还真实暴露了 Degree `torch.topk` 平分边界跨环境不稳定；V2 producer 已改为“度降序、node id 升序”的完整确定性排序，并以新算法版本、全新 Recipe 重新通过两端一致性验证。

| 验收面 | 结论 | 证据 |
|---|---|---|
| Producer registry | 通过 | `registered_producers = [degree, im, pagerank, random]` |
| Artifact identity | 通过 | Random 按 seed 分离；Degree/PageRank 跨 method、model request 与实验 seed 共享 |
| cold → warm exact hit | 通过 | 本机与 SSH 均为 cold 5/5 创建；warm 5/5 `hit=true, producer_called=false` |
| producer 哨兵 | 通过 | 独立 warm 使用 `--fail-if-producer-called`，未触发 producer |
| 跨 YAML 解耦 | 通过 | 改变 YAML 路径和 `config_name` 后仍命中同一 5 个 Artifact |
| 跨环境确定性 | 通过（修复后） | Degree v1 在真机暴露同 Recipe 异 content；v2 tie-break 后本机/SSH 的 Recipe、Artifact ID、content hash 完全一致 |
| Random 可复现性 | 通过 | 显式 Recipe seed；Torch RNG fork；重复 producer 内容相同且不改变调用方 RNG state |
| Legacy 只读 | 通过 | 三个 Legacy cache 目录聚合 hash 前后完全一致 |
| Legacy 内容等价 | 未通过/未形成候选 | SSH 上 Random 三个 seed 为 `content_mismatch`；Degree/PageRank 为 `missing`；均不参与 V2 resolve |
| 现有 Cache/runner 回归 | 通过 | 本机与 SSH 均为 156 passed；SSH 仅有既有 TBB/Numba warning |
| runner 切换 | 未实施 | `experiments/run.py`、`demo_attack.py`、`eval_collateral.py` 与旧查询路径均未修改 |

这完成了 V2.2 checklist 中“注册 random / degree / PageRank producer”这一项，但不代表 Gate 2 整体通过。ScoreArtifact、Legacy promotion/conflict resolution、runner、Prediction/Evaluation 仍未完成；既有 ogbn-arxiv IM Legacy mismatch 也使 Gate 3 保持关闭。

## 2. 实现落点

- `cache_v2/selection_materializer.py`
  - 增加 Random、Degree、PageRank Recipe builder；
  - registry 支持一种 strategy 展开多个 Artifact job；
  - Random 对每个 distinct experiment seed 生成一个 Recipe；
  - Degree/PageRank 将所有 method/experiment seed 请求去重为一个 Recipe；
  - Random/PageRank producer 调用现有 strategy；Degree 的 V2 adapter 显式定义“度降序、node id 升序”，避免 Legacy `torch.topk` 的跨环境 tie 歧义；
  - Legacy 对照从 IM 专用逻辑推广为按 strategy seed/parameter fingerprint 匹配。
- `tests/test_cache_v2_materializer.py`
  - 增加 Recipe identity、consumer 去重、RNG 隔离、cold/warm、mtime、Legacy 零修改和真实 strategy class 测试。
- `experiments/configs/cache_v2_cora_simple_selection_canary.yaml`
  - 提供可重复的 simple-selector `cachectl selection` 请求；它不是 runner 切换配置。

没有新增 ScoreArtifact，也没有读写 Legacy payload。所有正式写入仅发生在显式给出的隔离 V2 store。

## 3. 三类最小 Recipe

三者共同包含：`graph_fingerprint`、`candidate_set_hash`、`node_id_space`、selector 名、selector algorithm version 与 `k`。

| Selector | 额外 identity | 明确不进入 identity | 共享范围 |
|---|---|---|---|
| Random | `random_parameters.seed` | YAML/config 名、method、base model request | 同 graph/candidates/seed/k |
| Degree | 无 | experiment seed、method、base model request | 跨 method、model request、实验 seed |
| PageRank | `pagerank_parameters.alpha` | experiment seed、method、base model request | 同 topology/candidates/alpha/k，跨实验 seed |

算法版本分别为：

```text
opengu-random-torch-randperm-v1
opengu-degree-desc-node-id-asc-v2
opengu-pagerank-undirected-networkx-topk-v1
```

Random producer 在 `torch.random.fork_rng(devices=[])` 中设置 Recipe seed，再调用现有 `RandomStrategy`。因此随机节点序列是显式 Artifact 语义，不依赖 materializer 调用前的全局 RNG 消耗。

Degree producer 不改 Legacy `DegreeStrategy`，也不改变 runner；V2 只在独立 materializer 内把所有候选节点按 `(-degree, node_id)` 排成全序。算法与 producer semantic version 同步提升到 v2，因此旧的非确定性 Recipe 不会被新 producer 误命中。

## 4. 真实 Cora cold / warm

### 4.1 请求规模

| 字段 | 值 |
|---|---|
| dataset | Cora，2708 nodes |
| split | transductive 80/0/20，split seed 42 |
| candidate nodes | 2166 |
| ratio / k | 0.05 / 108 |
| methods | GIF、GraphRevoker |
| strategies | random、degree、pagerank |
| experiment seeds | 42、212、722 |
| consumer requests | 18 |
| unique Recipes | 5 |
| deduplicated requests | 13 |

18 个请求被编译为：Random 3 个 seed Recipe、Degree 1 个 Recipe、PageRank 1 个 Recipe。plan 阶段 `producer_calls=0`、`writes=[]`，store 不存在时也不会创建目录。

### 4.2 结果

| 阶段 | 总耗时 | 结果 |
|---|---:|---|
| 本机 cold `--apply --verify` | 0.969880 s | 5/5 miss 后创建；每项随即 warm verify |
| 本机 warm 独立进程 | 0.800032 s | 5/5 exact hit；5/5 `producer_called=false` |
| SSH cold `--apply --verify` | 3.556464 s | 5/5 miss 后创建；正式写入仅位于隔离 V2 store |
| SSH warm 独立进程 | 2.435275 s | 5/5 exact hit；producer trap 未触发；payload mtime 全部不变 |
| SSH 改 YAML 名/路径后的 warm | 通过 | 仍命中同一 5 个 Artifact；Artifact ID/content/mtime 与前次 warm 完全相同 |
| SSH ratio 改变后的 plan | 通过 | `k` 改变，5/5 `no_exact_candidate`；`producer_calls=0`、`writes=[]`、store 不变 |

| Selector | Artifact ID | Recipe hash | Content hash |
|---|---|---|---|
| Random seed 42 | `sel_6d58bd8e_bffcb733` | `6d58bd8e9963c4f57e8a5849ee6bd8401bd48247b405eb61594d0510e270843b` | `bffcb7331f8fd9da0c37eef6a49d02d189b874bbaa14259d059a2e5732bb8afe` |
| Random seed 212 | `sel_de12ce98_f0fd1126` | `de12ce9804d940b3280b27cd975901fa345f50a4594b8035dabfe69857e89053` | `f0fd1126bc96c36f57581ebdcf5b1ba999a42a059fc7fb8febd4df7678ea10d9` |
| Random seed 722 | `sel_e7221569_e5a94190` | `e72215693c88027d243da70f08cc769f79485f9d97efcb86fe2ec39b8da6fbc7` | `e5a94190b15d6a8f9b693608b09ded9f6901af979e1f07e1c6068d9996e8e3a7` |
| Degree | `sel_5bc434cd_7e66e515` | `5bc434cdb68a652e5f4e4ae5974eafc56decfbdbad79ce27787baf47d28136de` | `7e66e5153fdd003d633d7e2fe9459f524b5aa738bfb649f9a6dd398d990c232a` |
| PageRank | `sel_512a1616_982b6e54` | `512a16162e57a57f0ce90fccc7a7288202ab3240c2399c1fd48882df7794eabb` | `982b6e549460a56b07697b70c092c7e27c2bd035ddcdca0c16f336f04a28906e` |

隔离 store 与 SSH 证据：

```text
local:  C:\Users\ADMIN\AppData\Local\Temp\opengu-cache-v2-degree-v2-1784017625
SSH:    /autodl-fs/data/cache-v2-materializer/simple-eb7c2d8-cora
evidence:/autodl-fs/data/opengu-experiment-evidence/cache-v2-simple-eb7c2d8
```

SSH index 的 `PRAGMA integrity_check` 为 `ok`，`schema_version=1`、正式 Artifact 5 个、conflict 0 个。隔离 checkout 固定在 `eb7c2d82a0d5ef9d5afd8010f70246d9acc034e2`；active master 始终保持原 HEAD `3f631fb057a42e62db5f612e66e53edc2937459a` 与原 dirty 列表。

### 4.3 真机发现并关闭的 Degree 风险

修复前，本机和 SSH 对完全相同的 v1 Degree Recipe `fd84330c...` 分别产生 content `b5583d1a...` 与 `4673b877...`，且连选中节点集合都不同。根因是大量同度节点跨越 `k=108` 边界时，`torch.topk` 没有可移植的 tie 顺序。这正是“同 Recipe 重算不得静默产生不同 content”需要防住的情况。

修复没有覆盖或复用旧 v1 Artifact，而是：

- 将 Degree algorithm version 改为 `opengu-degree-desc-node-id-asc-v2`；
- 将 producer semantic version 提升为 v2；
- 生成新 Recipe `5bc434cd...`；
- 在全新本机/SSH store 中均得到同一 Artifact `sel_5bc434cd_7e66e515` 与同一 content `7e66e515...`。

旧 SSH v1 store `/autodl-fs/data/cache-v2-materializer/simple-f1fcd2c-cora` 保留为失败证据，没有删除或覆盖。

## 5. Legacy 与数据目录不变性

SSH plan、cold、warm、跨 YAML warm 与 changed-k plan 均报告：

```text
legacy_cache_state_hash_before = b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa
legacy_cache_state_hash_after  = b7488cb14f32e9482fd268f31bada5bca3561e81f953db4ed1f117ff32e98ffa
dataset_unchanged              = true
legacy_cache_unchanged         = true
```

SSH 快照覆盖 `results/cache` 784 个文件、`results/selection_cache` 111 个文件和 `results/score_cache` 75 个文件。作为输入的远端真实 Cora pickle hash 始终为 `1dcbb6be57c174bcad6fe8186ec5eadfeb01196dd7ee33772e697aa5057ad6e4`，size/mtime 前后不变；仅在隔离数据目录导出 canary 所需的 `data.pt`。

当前 V2 canary 的 Legacy graph fingerprint 为 `f281d15ca7aff49ca33fdab4b6b3fb01`。SSH read-only compare 对 Random 三个 seed 找到候选但均为 `content_mismatch`，Degree/PageRank 为 `missing`。这些状态只用于报告，从未参与 resolve，也没有被伪造成正式 V2 conflict；因此 Gate 3 仍保持关闭。

## 6. 测试结果

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_cache_v2.py tests/test_cache_v2_store.py `
  tests/test_cache_v2_selection_canary.py tests/test_cache_v2_materializer.py -q
# 79 passed（新增 Degree portable tie-break 测试）

E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_score_cache.py tests/test_attack_manager.py `
  tests/test_phase_b_invariants.py -q
# 77 passed
```

合并结果：本机 `156 passed in 3.09s`；SSH `156 passed in 30.63s`。SSH 唯一 warning 是环境中 TBB 版本不足导致 Numba 并行层禁用，不是本次回归。

新增测试覆盖：

- 18 consumer → 5 Recipe 的精确去重；
- Random seed identity 与 RNG state 隔离；
- Degree 同分边界按 node id 确定性排序；
- PageRank alpha 改变导致 Recipe miss；
- real strategy class fixture cold/warm；
- 同 Recipe warm hit 不调用 producer、不改变 payload mtime；
- simple selector 的 Legacy exact comparison 与 Legacy 零修改。

## 7. CLI 复现

```powershell
$PY = 'E:/conda_package/envs/gnn/python.exe'
$ROOT = 'E:/project/OpenGU/GULib-master'
$STORE = 'C:/path/to/fresh/cache-v2-simple-cora'

& $PY "$ROOT/scripts/cachectl.py" selection plan `
  --config "$ROOT/experiments/configs/cache_v2_cora_simple_selection_canary.yaml" `
  --dataset-root "$ROOT/data/raw" `
  --store-root $STORE `
  --legacy-results-root "$ROOT/results"

& $PY "$ROOT/scripts/cachectl.py" selection materialize `
  --config "$ROOT/experiments/configs/cache_v2_cora_simple_selection_canary.yaml" `
  --dataset-root "$ROOT/data/raw" `
  --store-root $STORE `
  --legacy-results-root "$ROOT/results" `
  --apply --verify --compare-legacy

& $PY "$ROOT/scripts/cachectl.py" selection materialize `
  --config "$ROOT/experiments/configs/cache_v2_cora_simple_selection_canary.yaml" `
  --dataset-root "$ROOT/data/raw" `
  --store-root $STORE `
  --legacy-results-root "$ROOT/results" `
  --apply --fail-if-producer-called --compare-legacy
```

## 8. 未完成边界与下一 gate

本轮没有：

- 接入 runner 或旧 Cache 查询路径；
- 双写、迁移、修改或删除 Legacy；
- 新建 Degree/PageRank ScoreArtifact；
- 实现 compatible/prefix hit；
- 注册 TracIn/Hybrid producer；
- 实现 promotion、conflict resolution、repair、retire 或 GC。

SSH 隔离重放已经完成。下一步 Gate 2 的硬项仍是 IM ScoreArtifact 与可审计 conflict resolution；二者完成后才能设计 runner canary。既有 IM/Random Legacy mismatch 未解释前，Gate 3 不能通过，Legacy 也不能冻结、归档或删除。
