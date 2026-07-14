---
title: Cache V2 Simple Selection Producers 验收报告
date: 2026-07-14
status: producers-accepted-gates-remain-partial
---

# Cache V2 Simple Selection Producers 验收报告

## 1. 验收结论

Random、Degree、PageRank 已接入与 IM 相同的 Cache V2 exact-only SelectionArtifact 主路径，并通过真实 Cora cold/warm 验收。

| 验收面 | 结论 | 证据 |
|---|---|---|
| Producer registry | 通过 | `registered_producers = [degree, im, pagerank, random]` |
| Artifact identity | 通过 | Random 按 seed 分离；Degree/PageRank 跨 method、model request 与实验 seed 共享 |
| cold → warm exact hit | 通过 | cold 5/5 创建；warm 5/5 `hit=true, producer_called=false` |
| producer 哨兵 | 通过 | 独立 warm 使用 `--fail-if-producer-called`，未触发 producer |
| 跨 YAML 解耦 | 通过 | 改变 YAML 路径和 `config_name` 后仍命中同一 5 个 Artifact |
| Random 可复现性 | 通过 | 显式 Recipe seed；Torch RNG fork；重复 producer 内容相同且不改变调用方 RNG state |
| Legacy 只读 | 通过 | 三个 Legacy cache 目录聚合 hash 前后完全一致 |
| Legacy 内容等价 | 未形成候选 | 当前 Cora graph/split identity 没有 exact Legacy source，状态为 `missing`，不伪造 match/conflict |
| 现有 Cache/runner 回归 | 通过 | Cache V2 78 passed；Legacy/AttackManager/Phase-B 77 passed |
| runner 切换 | 未实施 | `experiments/run.py`、`demo_attack.py`、`eval_collateral.py` 与旧查询路径均未修改 |

这完成了 V2.2 checklist 中“注册 random / degree / PageRank producer”这一项，但不代表 Gate 2 整体通过。ScoreArtifact、Legacy promotion/conflict resolution、runner、Prediction/Evaluation 仍未完成；既有 ogbn-arxiv IM Legacy mismatch 也使 Gate 3 保持关闭。

## 2. 实现落点

- `cache_v2/selection_materializer.py`
  - 增加 Random、Degree、PageRank Recipe builder；
  - registry 支持一种 strategy 展开多个 Artifact job；
  - Random 对每个 distinct experiment seed 生成一个 Recipe；
  - Degree/PageRank 将所有 method/experiment seed 请求去重为一个 Recipe；
  - producer 直接调用现有 `RandomStrategy`、`DegreeStrategy`、`PageRankStrategy`；
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
opengu-degree-source-topk-v1
opengu-pagerank-undirected-networkx-topk-v1
```

Random producer 在 `torch.random.fork_rng(devices=[])` 中设置 Recipe seed，再调用现有 `RandomStrategy`。因此随机节点序列是显式 Artifact 语义，不依赖 materializer 调用前的全局 RNG 消耗。

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
| cold `--apply --verify` | 0.815264 s | 5/5 miss 后创建；每项随即 warm verify，producer 未再次调用，payload mtime 不变 |
| warm 独立进程 | 0.729433 s | 5/5 exact hit；5/5 `producer_called=false` |
| 改 YAML 名/路径后的 warm | 0.676380 s | 仍命中同一 5 个 Artifact；producer trap 未触发 |

| Selector | Artifact ID | Recipe hash | Content hash |
|---|---|---|---|
| Random seed 42 | `sel_6d58bd8e_bffcb733` | `6d58bd8e9963c4f57e8a5849ee6bd8401bd48247b405eb61594d0510e270843b` | `bffcb7331f8fd9da0c37eef6a49d02d189b874bbaa14259d059a2e5732bb8afe` |
| Random seed 212 | `sel_de12ce98_f0fd1126` | `de12ce9804d940b3280b27cd975901fa345f50a4594b8035dabfe69857e89053` | `f0fd1126bc96c36f57581ebdcf5b1ba999a42a059fc7fb8febd4df7678ea10d9` |
| Random seed 722 | `sel_e7221569_e5a94190` | `e72215693c88027d243da70f08cc769f79485f9d97efcb86fe2ec39b8da6fbc7` | `e5a94190b15d6a8f9b693608b09ded9f6901af979e1f07e1c6068d9996e8e3a7` |
| Degree | `sel_fd84330c_b5583d1a` | `fd84330cb016b89b19d67992b00507c3683dac41215b4cc562039c76b9f582f7` | `b5583d1af03f01d4ecc540d5a1be0294e8232e1283c9379891c74707dbf92de8` |
| PageRank | `sel_512a1616_982b6e54` | `512a16162e57a57f0ce90fccc7a7288202ab3240c2399c1fd48882df7794eabb` | `982b6e549460a56b07697b70c092c7e27c2bd035ddcdca0c16f336f04a28906e` |

隔离 store：

```text
C:\Users\ADMIN\AppData\Local\Temp\opengu-cache-v2-simple-cora-20260714
```

## 5. Legacy 与数据目录不变性

plan、cold、warm 和跨 YAML warm 均报告：

```text
legacy_cache_state_hash_before = 6d7752d1cd154fe6894624529a2aa7cc57404b55c9c6d250b5f6c2885cc6c19e
legacy_cache_state_hash_after  = 6d7752d1cd154fe6894624529a2aa7cc57404b55c9c6d250b5f6c2885cc6c19e
dataset_unchanged              = true
legacy_cache_unchanged         = true
```

快照覆盖 `results/cache` 9 个文件、`results/selection_cache` 10 个文件和 `results/score_cache` 27 个文件。

当前 V2 canary 的 Legacy graph fingerprint 为 `f281d15ca7aff49ca33fdab4b6b3fb01`。本机历史 Cora SelectionCache 示例使用其他 graph/split fingerprint（例如 `a3761845...`），所以 read-only compare 返回 `missing`。这不是节点 content mismatch，也不是 V2 conflict；Legacy 从未参与 resolve。

## 6. 测试结果

```powershell
E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_cache_v2.py tests/test_cache_v2_store.py `
  tests/test_cache_v2_selection_canary.py tests/test_cache_v2_materializer.py -q
# 78 passed in 2.50s

E:/conda_package/envs/gnn/python.exe -m pytest `
  tests/test_score_cache.py tests/test_attack_manager.py `
  tests/test_phase_b_invariants.py -q
# 77 passed in 0.49s
```

新增测试覆盖：

- 18 consumer → 5 Recipe 的精确去重；
- Random seed identity 与 RNG state 隔离；
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

下一步应先把这份代码提交并在 SSH 隔离 store 重放同一 simple-selector canary。之后，Gate 2 的硬项仍是 IM ScoreArtifact 与可审计 conflict resolution；二者完成后才能设计 runner canary。既有 IM Legacy mismatch 未解释前，Gate 3不能通过，Legacy也不能冻结、归档或删除。
