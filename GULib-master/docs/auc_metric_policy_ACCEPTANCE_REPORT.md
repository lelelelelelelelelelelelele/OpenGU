---
title: Update-Detection AUC 数据集策略验收报告
date: 2026-07-16
status: local-cpu-accepted
---

# Update-Detection AUC 数据集策略验收报告

## 1. 验收结论

**本地 CPU 实现验收通过。** OpenGU 现在可以通过 YAML 显式决定是否运行 update-detection AUC：Cora/Citeseer 等小数据集保留该 secondary metric，所有 `phase_b_arxiv*.yaml` 大数据集配置关闭。关闭后昂贵 posterior/AUC 路径不执行，`attack.json::mia_auc` 明确为 `null`，gate 不再把它当作缺失或失败。

| 验收面 | 结论 | 证据 |
|---|---|---|
| YAML 策略 | 通过 | 小图主配置显式 `true`；9 份 arxiv phase 配置显式 `false` |
| 方法执行 | 通过 | IF/GIF、IDEA、GNNDelete、MEGU、GraphEraser、GraphRevoker 均受统一 helper 控制 |
| 输出语义 | 通过 | 关闭时统一写 `mia_auc: null`，不使用 `0.0` |
| 完成门 | 通过 | gate 开启时检查有限/不塌缩；关闭时要求 `null` |
| Cache 防混 | 通过 | Score/Selection identity 不变；完整 cell fingerprint 包含开关 |
| Legacy 边界 | 接受 | 不扩展待退役 ResultCache key；旧完整结果命中后按当前 policy 归一为 `null` |
| CPU 回归 | 通过 | 40 passed；相关改动文件 `compileall` 通过 |

本报告不把本地单元测试扩大解释为 GPU 真机或科学指标复验；尚未运行大图端到端 canary。

## 2. 锁定的配置契约

~~~yaml
defaults:
  run_update_detection_auc: true   # 小数据集：计算 secondary AUC
~~~

~~~yaml
defaults:
  run_update_detection_auc: false  # 大数据集：跳过 secondary AUC
~~~

- 只接受 YAML boolean；旧 YAML 缺省时保持 `true`，兼容原行为。
- 不在代码里根据 dataset 名称、节点数或 GPU 型号自动猜测。
- `false` 表示“按配置未运行”，不是 AUC=0，也不是运行失败。
- `_meta.json::metric_policy.update_detection_auc` 保存 enabled/status，便于审计。

## 3. 执行与输出路径

~~~text
YAML defaults.run_update_detection_auc
        │
        ├─ true  → method posterior/query → ROC-AUC → attack.json finite value
        │
        └─ false → skip expensive AUC path → attack.json null
                                      └────→ gate accepts disabled policy
~~~

`experiments/run.py` 把同一个值同时传给 `demo_attack.py` 和 `eval_collateral.py`，避免 attack 路径关闭但 collateral 重跑时又计算一次。GIF 原先在自身 `unlearn()` 与 IF base pipeline 重复计算 AUC；现在由 IF base pipeline 统一执行一次。

## 4. Cache 与身份边界

| 对象 | 是否因 AUC 开关分叉 | 说明 |
|---|---|---|
| TracIn / IM Score | 否 | AUC 不改变 selector score |
| Selection | 否 | AUC 不改变 selected nodes |
| V2 Prediction | 否 | 设计上同一预测观测可服务多个 Evaluation |
| AUC Evaluation | 是 | 启用时才请求，且 metric recipe/version 决定身份 |
| 当前完整 run 目录 | 是 | runner fingerprint 包含 `defaults`，避免开/关产物混用 |

当前实现完成的是“真正停止计算 + null 语义 + gate/fingerprint 防混”。独立、可离线推导的 AUC EvaluationArtifact 仍属于 V2.3；GraphEraser/GraphRevoker 的逐 shard query posterior 也必须先锁定统一协议，不能直接宣称由现有全图 logits 严格复现。

## 5. 验证证据

~~~text
python -m pytest \
  tests/test_update_detection_auc_policy.py \
  tests/test_attack_manager.py \
  tests/test_legacy_cache_freeze.py \
  tests/test_cache_v2_selection_canary.py \
  tests/test_cache_v2_runtime.py -q

40 passed in 0.39s
~~~

新增策略测试覆盖：

- canonical flag、legacy `run_mia` 只读兼容与 `null` 归一；
- AUC 开/关两种 gate 行为；
- 所有 arxiv phase YAML 均关闭；
- 开/关策略产生不同 cell fingerprint。

相关 Python 文件 `compileall -q` 通过。验证环境为本地 CPU；未使用本机 CUDA。

## 6. 文档落点

- `文档规划/10_实验矩阵/17_CPU-GPU估时与资源分工.md`：解释 Selection 与 AUC 的 CPU/GPU 成本，以及 small/large YAML 策略。
- `文档规划/10_实验矩阵/19_Cache架构重设计与迁移方案.md/.html`：记录 Score/Selection/Prediction/Evaluation identity 边界与 Legacy 退役处理。
- `self/dashboard/METRICS_CATALOG.md`：把 update-detection AUC 标为可选 secondary metric，并锁定 `null`/gate 口径。

## 7. 已知边界与下一道门

1. 独立 EvaluationCache 尚未接入当前 runner；本次没有伪称已经完成 V2.3。
2. 小数据集启用时仍使用各方法现有 method-specific AUC producer。
3. Legacy ResultCache key 没有新增该字段，符合用户确认的退役方向；过渡期只做读取后输出归一。
4. 若要投入正式大图批跑，下一步只需做一格 GPU canary，确认日志中没有进入 AUC/posterior 查询路径，并检查 `attack.json = null` 与 `_meta.json = disabled_by_config`。
