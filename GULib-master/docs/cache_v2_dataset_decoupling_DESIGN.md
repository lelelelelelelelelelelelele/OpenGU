---
title: Cache V2 Dataset 职责解耦设计
date: 2026-07-15
updated: 2026-07-16
status: implemented-local-accepted
---

# Cache V2 Dataset 职责解耦设计

## 1. 设计结论

Cache V2 不再拥有 dataset、split、candidate 或 Selection 计算。OpenGU 的 dataset/experiment 层从现有 `data/processed` pickle 读取图与持久化训练集合，构造规范化 `SelectionInputs`，并且只在 Cache exact miss 后调用 selector。Cache V2 只验证 Recipe identity、解析或写入不可变 Selection Artifact，并执行完整性与冲突处理。

## 2. 职责边界

| 层 | 负责 | 明确不负责 |
|---|---|---|
| `experiments/selection_inputs.py` | canonical processed pickle、persisted `train_mask/train_indices`、dataset/graph/candidate fingerprint | 下载、Planetoid/OGB、重新随机 split |
| `experiments/selection_producer.py` | 请求展开、producer version、selector 调用、候选集校验、Legacy 只读对照 | Cache index、Artifact ID、不可变写入 |
| `cache_v2/selection_materializer.py` | Selection Recipe v2、exact resolve、显式 selected nodes materialization | dataset loader、selector import、producer callback |
| `cache_v2/store.py` | payload/header、Artifact ID、原子写入、完整性、conflict/quarantine | `get_or_compute`、recomputation callback、dataset/candidate 构造 |
| runtime consumer | 按显式 Artifact ID 读取，并在 GU 已加载数据后复核 candidate membership | compatible/prefix fallback、Legacy promotion |

## 3. 两条执行路径

```text
HIT
upstream Selection identity
  -> Cache exact resolve
  -> header/payload/integrity verification
  -> Selection Artifact

MISS
OpenGU processed provider
  -> normalized SelectionInputs
  -> Cache exact miss
  -> experiment/GU selector producer
  -> selected-node count/uniqueness/candidate validation
  -> Cache immutable store
```

Cache HIT API 没有 dataset provider 或 producer 参数，因此 Cache 内部不可能加载 dataset、下载数据、重新决定 split 或调用 selector。上游负责在进入 Cache 前提供完整 identity。

## 4. Selection Recipe v2 identity

新 Recipe 使用 `selection_recipe_contract = opengu-selection-recipe-v2`，并绑定：

- `dataset_fingerprint`、`graph_fingerprint`、`candidate_set_hash`；
- `num_nodes`、`candidate_count`、`node_id_space`；
- `selector`、`selector_seed`、`k`、algorithm version 与参数；
- 完整 `producer_version`，包含 semantic version 与 source fingerprint。

配置文件名、YAML 路径、method/base-model request 和普通实验标签仍只属于 request envelope，不进入 Artifact identity。

## 5. 兼容与 fail-closed 边界

- Artifact ID 公式和 `sel_<recipe-prefix>_<content-prefix>` 形式不变。
- 已有 Artifact 仍可由 runtime 通过显式 Artifact ID、索引中的原 Recipe 与 header 读取。
- 新的 producer resolution 只接受 Selection Recipe v2；缺少 dataset fingerprint、candidate hash 或 producer version 的旧 Recipe 明确拒绝，不会被错误命中。
- producer owner/source 改变后 semantic version 与 source fingerprint 同步变化，因此不会把旧 materializer 结果伪装成新 producer 的 hit。
- exact-only resolver、immutable write、conflict marker、quarantine、Legacy freeze 和 AutoReport authoritative provenance 保持原语义。

## 6. 非目标

本次不注册或修改 TracIn/Hybrid producer，不修改其算法机制；不实现 compatible/prefix hit、Legacy promotion、结果迁移或历史 archive 重写。

## 7. 验收与后续验证边界

canonical processed Cora cold/warm、Cache 边界静态测试及 CPU 回归已经构成本设计的验收依据。服务器最小 CPU smoke 只用于排查部署环境与路径差异，是合并后的非阻塞 TODO，不重新决定本设计或 Cache V2 的有效性。
