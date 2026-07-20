---
title: proper-tracin-v1 × SUP Selection Gate 验收报告
date: 2026-07-20
status: conditional-selection-gate-pass
branch: codex/feat-proper-tracin-sup-20260720
parent: main@2f0d22a
---

# proper-tracin-v1 × SUP Selection Gate 验收报告

## 1. 判定

**CONDITIONAL SELECTION-GATE PASS。**

本轮已经把 proper TracIn 的第一段正式链路跑通：一个在计算前即可确定的 `proper-tracin-v1` Recipe，经过真实 Cora/GCN/seed-2024 训练与多 checkpoint 梯度打分，生成不可变 Cache V2 Score Artifact；该 Score 再作为父 Artifact，生成唯一的 max-k Selection Artifact，并为较小 SUP 预算提供有序前缀。

本判定只接受 **Score → Selection**。它不是 production TracIn 总验收，也不是 GU 攻击效果结果。Hybrid、OpenGU canonical split/model、单 seed GU canary、C.6a surrogate transfer 和 C.6b cross-backbone 均尚未运行。

## 2. 关于 Legacy 删除与实验进度

“物理删除 Legacy 会让整个实验进度表清空”并不准确。当前 Phase B runner 的完成/跳过判定来自 `results/runs/...` 中四件套及当前 config fingerprint：

- `attack.json`；
- `collateral.json`；
- `predictions.npz`；
- `_meta.json`。

因此，删除 `results/cache`、`results/selection_cache` 或 `results/score_cache` 不会自动删除这些正式结果，也不会让四件套覆盖率凭空归零。但删除 Legacy 会丢掉已有 run/selection/score 的快速复用入口，使未完成、stale 或需要复跑的 cell 重新计算；TracIn/IM 的代价尤其高，并且旧 selector 结果的追溯能力会下降。

本轮继续执行既定政策：**Legacy 原位只读冻结，不删除、不覆盖；新计算只写隔离的 V2 evidence store。**

## 3. 本轮完成的链路

```text
pre-compute input identity
  → proper-tracin-v1 Recipe
  → experiment-owned model training + checkpoint gradients
  → immutable Score Artifact
  → source_score_artifact_id
  → one max-k Selection Artifact
  → SUP budget prefixes (k=14 → k=7 → k=3)
```

| 层 | 本轮结果 | 边界 |
|---|---|---|
| Recipe | 计算前可解析 | 不含训练后 final/checkpoint state hash |
| Score | formal immutable Artifact | producer 位于 experiment 层，Cache 不训练模型 |
| Conflict | quarantine + durable marker + index conflict | 同 Recipe 不同 content 后续 fail closed |
| Selection | formal Cache V2 Artifact | 显式绑定父 Score Artifact ID |
| SUP budget | max-k 一次物化，较小 k 取前缀 | 不创建 k=7、k=3 子 Artifact |
| Legacy | 前后 SHA-256 快照一致 | 未读写旧 Result/Selection/Score Cache |
| GU runner | 未注册 | 等 Hybrid 与 GU canary gate |

## 4. Recipe 的关键修正

原 `tracin-v2-unstable` 原型把训练结束后的 `final_state_hash` 与 checkpoint `state_hash` 放在 Recipe 中。该结构能给一次完成后的报告编号，却不能在 producer 运行前查 Cache：必须先训练，才能知道 Recipe。

`proper-tracin-v1` 改为如下分工：

| Recipe：计算前输入身份 | Score payload：计算后 provenance |
|---|---|
| data/split/candidate/target hashes | checkpoint state hashes |
| 初始化模型 state hash、参数 schema | final state hash |
| optimizer、loss、seed、epoch | final train loss |
| checkpoint schedule 与预期权重 | test accuracy |
| parameter scope、numerics、source fingerprint | hostname 与实际 numerics |

这使 warm exact lookup 真正发生在训练和梯度计算之前。Adam 路径仍明确标为 `adam_lr_weighted_gradient_heuristic`；本轮没有把它写成原始 SGD/GD TracIn 推导的严格等价物。

## 5. 真实 Cora selection-only canary

配置：Planetoid public split、Cora、two-layer GCN、seed 2024、Adam、30 epochs、checkpoints `{1,5,10,20,30}`、all-trainable parameters、validation set 作为显式目标 E、SUP budgets `{14,7,3}`。

| 运行 | Score | Selection | producer | Legacy | 判定 |
|---|---|---|---|---|---|
| cold | miss → `score_ee18e0f4_6d52213b` | miss → `sel_4744275f_1a373931` (k=14) | Score=1，Selection=1 | unchanged | pass |
| warm | exact hit，同一 Score ID | exact hit，同一 Selection ID | Score=0，Selection=0 | unchanged | pass |
| future-smaller `{7,3}` | exact hit | covering hit，复用 k=14 | Score=0，Selection=0 | unchanged | pass |

训练模型 test accuracy 为 `0.7960`。该值只作为本轮 selector model quality/provenance，不是 GU 后准确率或攻击收益。

Top-14 的稳定顺序为：

```text
[48, 51, 44, 30, 25, 40, 21, 0, 45, 4, 27, 14, 17, 19]
```

因此：

- k=7 = `[48, 51, 44, 30, 25, 40, 21]`；
- k=3 = `[48, 51, 44]`；
- 两者都来自 `sel_4744275f_1a373931` 的前缀，而不是新 Artifact 或从下游结果反推。

Selection Artifact 的父引用为 `source_score_artifact_id=score_ee18e0f4_6d52213b`。

## 6. Legacy 快照证据

本地 canary 覆盖当前 checkout 中实际存在的 46 个 Legacy cache 文件，共 789,634 bytes：

| Root | 文件数 | bytes | aggregate SHA-256 |
|---|---:|---:|---|
| `results/cache` | 9 | 63,348 | `421a06f63dc747df2508d329acb0ea3fd4aa4dd71e072da6957f38656e3a3077` |
| `results/selection_cache` | 10 | 22,663 | `10197dc26400d016426eb26da9215131031810efae64a256e1c865d9af7c7d1b` |
| `results/score_cache` | 27 | 703,623 | `daba3f962ee9def5e679918d436377183465136a0436dadae733ac7dd57536cd` |
| combined | 46 | 789,634 | `c3465e6d65469147c24316e81c0bf2f48f5465a79f088a428b30142ce2c538c7` |

cold、warm 和 future-smaller 三次执行均记录 `legacy_unchanged=true`。这里的 46 是本地 checkout 当前实际文件数，不替代此前服务器/历史 retirement inventory 的更大计数。

## 7. 自动化验证

### Focused

```text
36 passed in 0.61s
```

覆盖 formal Recipe、Score payload、cold/warm、fail-if-called、same-Recipe/different-content quarantine、max-k Selection、future-smaller covering hit，以及既有 TracIn V2 prototype gates。

### 联合回归

```text
255 passed in 7.18s
```

覆盖 Cache V2 全部 `test_cache_v2*.py`、proper TracIn、SUP max-k planner、TracIn unstable prototype、strategy goldens、ScoreCache、Phase B invariants 与旧策略 tests。`CUDA_VISIBLE_DEVICES=-1`，未调用本机不兼容 GPU。

## 8. 代码与旧 WIP 的处理

新增：

- `cache_v2/score_store.py`：通用 formal Score payload/store；
- `experiments/tracin_v2/formal_recipe.py`：pre-compute `proper-tracin-v1` Recipe；
- `experiments/tracin_v2/run_formal_selection_gate.py`：真实 Score → max-k Selection canary；
- `tests/test_proper_tracin_v1_artifacts.py`：Artifact 与 SUP gate tests。

旧 WIP `3ccde63` 没有被整体合并。只择取了它正确的术语结论：现有 `attack/attack_strategies/tracin_strategy.py` 是 `deployed-cross-gradient-legacy`，不是 multi-checkpoint proper TracIn。公式、Legacy cache key 和旧 runner 行为均未改变。

## 9. 对 SUP 与论文的当前含义

现在可以安全推进的结论有两条：

1. proper TracIn 的 Score 身份与 SUP 多预算 Selection 身份已经可审计、可复用；
2. 旧论文/代码中把 deployed cross-gradient 直接称作 TracIn 的表述需要逐步改成 Legacy compatibility 说明。

现在还不能写入论文结果表的结论：

- proper TracIn 比 random/degree/IM 的 GU damage 更强或更弱；
- surrogate selection 能迁移到 target model；
- Hybrid 存在正协同；
- C.6a/C.6b 的 retrain-gap transfer ratio。

这些必须等待 OpenGU canonical profile 与 GU 结果四件套。当前 `0.7960` 与 Top-14 只能作为 selection gate evidence。

## 10. 下一批顺序

1. 把 formal producer 从 Planetoid public split 对齐到 OpenGU canonical processed split/model/checkpoint entry；
2. 做 Hybrid parent identity、alpha/normalization 与 miss/conflict gate；
3. 运行单 seed、单 GU 的 isolated canary，并把 Selection Artifact ref 写入 `_meta.json`；
4. 先跑 C.6a same-architecture surrogate；transfer ratio gate 通过后才展开 C.6b；
5. 把 selection Jaccard 与 retrain-gap transfer ratio 分别写入论文证据链。

下一 server 小矩阵优先采用现有 B/C 报告建议的选择器：random、B-LiSSA、GT-full、P-graph、TracInCP-graph-6；GU 先限 GNNDelete/GraphEraser，且每个 cell 使用独立 GU Recipe。

## 11. 复现与机器证据

入口：

```powershell
E:/conda_package/envs/gnn/python.exe -m experiments.tracin_v2.run_formal_selection_gate `
  --data-root E:/project/OpenGU/GULib-master/data/raw/Planetoid `
  --score-store-root <ABSOLUTE_SCORE_STORE> `
  --selection-store-root <ABSOLUTE_SELECTION_STORE> `
  --legacy-results-root E:/project/OpenGU/GULib-master/results `
  --output <ABSOLUTE_OUTPUT_JSON> `
  --dataset Cora --model gcn --seed 2024 --optimizer adam `
  --epochs 30 --checkpoint-epochs 1,5,10,20,30 --budgets 14,7,3
```

Warm 运行增加 `--fail-if-producer-called`。

本轮 evidence JSON SHA-256：

| File | SHA-256 |
|---|---|
| `cold.json` | `19b6df4b2b5823f77a9ed0d7763f861181dc4e477fd4d9f0fbefa13cf82acdc2` |
| `warm.json` | `50baea01e6bb4cafa96a375367327b7a462120bfce3df254558954d8a05da7a6` |
| `covering.json` | `70f0f5af23ba65614dc7f7f214258446eff1a71cf3472014bb2d54f9531a9e16` |

在这个边界内，阶段 2 的 formal Score→Selection gate 已通过；阶段 3 的 Hybrid 与 GU canary 仍保持关闭。
