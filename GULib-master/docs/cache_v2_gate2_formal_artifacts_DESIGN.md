---
title: Cache V2 Gate 2 正式 Artifact 设计
date: 2026-07-16
status: implemented-local-accepted
---

# Cache V2 Gate 2 正式 Artifact 设计

## 1. 设计结论

Gate 2 将 Score、Prediction、Evaluation 提升为正式、版本化的 Cache V2 Artifact，同时保持 dataset 解耦后的职责边界：Cache 只接收 Recipe 与已经产生的 payload，负责 exact resolve、不可变存储、依赖关系、冲突隔离和完整性校验；Score/GU/metric producer 只能由 `experiments` 层在可证明的 exact miss 后调用。

这是一条非默认、可审查的上游 materialization seam，不改变现有 runner 默认执行路径，也不把 TracIn/Hybrid、dataset、split 或 evaluator 重新放进 Cache。

## 2. Artifact 契约

| Artifact | Recipe identity | Payload | 直接依赖 |
|---|---|---|---|
| Score | graph fingerprint、candidate hash、node space、selector identity、score algorithm/version、parameters、producer version | 有序 node IDs 与可选 finite scores；确定性 ZIP/NPY | 无 |
| Prediction | graph/split fingerprints、Selection Artifact ID、selected hash、N/C、class order、target method/model recipe、run seed、producer version | 三组 `float32 [N,C]` logits、`int64` labels/nodes/classes、boolean masks | Selection |
| Evaluation | Prediction Artifact ID、graph fingerprint、metric name/version/parameters、producer version | canonical JSON metrics | Prediction |

Score 保存完整 ordered ranking/scores 时，`k` 不进入 Score Recipe；不同 `k` 的 Selection 可复用同一 Score identity。三类 Recipe 分别用 `opengu-*-artifact-v1` 作为明确版本边界，未知或不完整契约不做隐式升级。

## 3. 执行边界

```text
HIT
Formal Artifact request
  -> Cache exact resolver
  -> payload/header/dependency recursive verification
  -> existing Artifact
  -> zero producer call / zero Cache write

MISS
Formal Artifact request
  -> Cache proves no_exact_candidate
  -> experiments layer invokes injected producer once
  -> typed payload validation
  -> Cache immutable store + dependency rows
```

冲突、损坏、无效状态、未验证状态、缺失依赖或依赖祖先异常都不是 MISS；它们直接 fail closed，不能触发 producer 重算。

## 4. 存储与完整性

- Artifact ID 继续使用 `<type>_<recipe8>_<content8>`，没有改变现有 ID 公式。
- Score/Prediction 使用固定成员顺序、固定 ZIP timestamp、`ZIP_STORED` 和禁止 pickle 的 NPY；Evaluation 使用严格 canonical JSON。
- payload 与 sidecar 都绑定完整 SHA-256、schema/version/size、Recipe、producer、status 与 verification status。
- Prediction→Selection、Evaluation→Prediction 在同一索引事务中注册依赖；读取子 Artifact 时递归验证父 payload/header 的实际字节和 identity。
- 同一 `(artifact_type, recipe_hash)` 出现不同 content 时写 durable marker、quarantine observation 并阻断 exact hit。
- exact HIT 是只读路径，不创建 index、trace、lock 或任何其他文件。

## 5. 兼容边界

- 已接受的 Selection store/materializer API 与 `sel_*` Artifact 不变。
- 新 formal Recipe 必须携带对应 v1 contract 和完整 producer version；旧或未知 formal Recipe 不自动迁移、不作为 producer resolution 命中。
- Legacy cache、`results/cache`、`results/cache_v2`、`results/runs` 与历史 archive 没有双写、promotion、repair、移动或删除。
- AutoReport V3 与 staged runner 继续消费原有 Selection/运行 provenance；本 Gate 不宣称 default runner 已切到三类新 Artifact。

## 6. 非目标与后续门

- Gate 3：四类 Artifact 的完整旧/新比较与容差验收，尚未完成。
- Gate 4：真实 GU runner/GPU canary，尚未执行。
- TracIn/Hybrid producer 接入及算法机制修改不在本 Gate。
- server 最小 CPU smoke 只作为非阻塞部署环境 TODO，不重新决定本地 Gate 2 架构有效性。
