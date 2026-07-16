---
title: Cache V2 Dataset 解耦与 Rollout 设计
date: 2026-07-17
status: accepted-design
---

# Cache V2 Dataset 解耦与 Rollout 设计

## 结论

Cache V2 是 exact-only Artifact store，不是 dataset 或 selection runtime。Dataset 加载、canonical processed pair 解析、candidate/split identity 和 selector 计算都属于 OpenGU experiment/GU 层；Cache 只负责 Recipe、Artifact、store、resolver、依赖、冲突与完整性。

## 职责边界

| 层 | 负责 | 禁止 |
|---|---|---|
| Dataset / experiment | canonical processed dataset、`SelectionInputs`、candidate set、fingerprint、producer 调用 | 把 dataset provider 塞进 Cache |
| GU / selector producer | 根据 strategy/seed/k 计算 ordered selected nodes | 在 Cache HIT 时重新计算 |
| Cache V2 | Recipe canonicalization、Artifact ID、immutable payload、exact resolve、integrity/conflict | Planetoid/OGB、下载、split/candidate 决策、producer callback |
| Runner / AutoReport | 按显式 Artifact ID 复用，并记录 phase/provenance | 查询失败后回退 Legacy |

## Identity

Selection Recipe v2 至少绑定：

- dataset fingerprint 与 graph fingerprint；
- candidate set hash 与 node ID space；
- strategy、seed、k 与算法版本；
- producer version；
- 必要的上游 Artifact identity。

Prediction 绑定 Selection Artifact，Evaluation 绑定 Prediction Artifact；HIT 会递归验证父依赖的真实 header/payload。

## HIT / MISS

```text
MISS
canonical processed pair
  -> experiment-owned SelectionInputs
  -> exact lookup miss
  -> injected producer
  -> selected nodes validation
  -> immutable Cache V2 Artifact

HIT
Recipe / explicit Artifact ID
  -> exact resolver
  -> header + payload + dependency verification
  -> Artifact
```

HIT API 没有 dataset provider 或 producer 参数，因此不会加载 dataset、下载数据、重建 split 或改变 candidate set。损坏、版本不兼容、冲突或 identity 不完整均 fail closed。

## 路径边界

- `processed_root`：experiment-owned canonical processed pair。
- `root_path`：代码与模型属性读取。
- `runtime_root`：日志、方法数据、checkpoint 和 unlearning task 等可变运行副作用。
- Cache V2 store 与 Gate evidence 使用独立绝对路径。

显式 `processed_root` 缺少任一 canonical pickle 时直接失败，不回退 raw loader、Planetoid/OGB、下载或 split reconstruction。

## Legacy

Legacy Result/Selection/Score Cache 保留为冻结、原位只读的 rollback/migration/diagnostic source。显式 V2 runner 不创建或查询 Legacy cache，完整性或查询失败也不会回退。

物理移动或删除是独立 retirement 任务，必须先清零 consumer refs、验证 V2 覆盖与 rollback window，并获得单独授权；它不是 Cache V2 正确性的验收条件。

## SyncMate

SyncMate 只负责 bounded dispatch、增量收集、SHA-256 验证、trusted index 和 acceptance gate。Runner job 只能选择静态 recipe；新 job envelope 可绑定 controller 观察到的 clean exact Git SHA，runner 执行前再次核验。实验是否可信仍由收集后的 Artifact gate 决定，queue `done` 本身不构成 acceptance。
