# 模块化实验计划与 SyncMate 执行上下文

本入口落实 [AAGU-001 合同](experiment_contract/README.md) 的配置和缓存隔离。
科研 YAML 说明要运行什么；SyncMate／项目策略决定在哪运行、使用哪个设备、读写哪一个
Cache V2 Store，以及 runtime 和结果的固定位置。

## 原子运行单元

入口的基本能力是一行独立的 `1 Dataset/Split × 1 Selector × 1 GU × 1 Evaluation`。
Selector 可以单独运行；GU 也可以直接消费已有 Selection，不必再次调用 Selector。
下面是一份可解析的 `1×1×1` 计划：

```yaml
kind: experiment
schema_version: 1
experiment_id: one-selector-one-gu
stage: unlearning
dataset_ref: dataset_cora.yaml
selector_refs:
  - selector_degree.yaml
unlearning_refs:
  - unlearning_gnndelete.yaml
evaluation_refs:
  - evaluation_post_unlearning_utility.yaml
matrix: cartesian_product
```

如果一轮实验需要五个 Selector 和两个 GU，大表可以分别列出五个 `selector_refs` 和两个
`unlearning_refs`；调度器只是把它展开成若干个相互独立的 `1×1×1` cell，每个 cell 都走
同一条接口，不产生整包缓存身份。完整多引用例子见
[`experiment_five_selectors_two_gu.yaml`](experiment_contract/examples/experiment_five_selectors_two_gu.yaml)。

科研表不含
`device/store_root/runtime_root/output/execution_authorized`。这些字段若出现在实验 YAML 中会
被拒绝，而不是被忽略。

## 小表只写必填输入和本次覆盖值

```yaml
# selector_b_hutch32.yaml
kind: selector
schema_version: 1
method: b_param_hutch
candidate: {pool: train_mask}
budget: {mode: ratio, value: 0.01}
parameters:
  parameter_scope: last_layer
```

```yaml
# selector_b_hutch64.yaml
kind: selector
schema_version: 1
method: b_param_hutch
candidate: {pool: train_mask}
budget: {mode: ratio, value: 0.01}
parameters:
  parameter_scope: last_layer
  hutchinson: {probes: 64}
```

32 是注册方法的当前默认探针数，所以第一份不重复写 LiSSA、Hutch seed、训练轮数、学习率
等默认值；64 是这次真正改变的值，所以第二份只增加 `probes: 64`。解析器从实际方法、
OpenGU parser 和模型 properties 展开完整有效配置，并在运行回执中逐字段记录来源。省略
当前默认值与显式写同值拥有相同计算身份；默认值或其实现真正改变时，实际消费者 MISS。

模型型 Selector 和 GU 未写 `model/training` 时使用已注册的 GCN/OpenGU 默认值，也可在
自己的小表中显式覆盖。模型字段放在哪不是组合协议的关键；两侧最终仍以各自完整有效配置
和 checkpoint 内容判定是否共享。

## Evaluation 是独立实例

```yaml
kind: evaluation
schema_version: 1
case: post_unlearning_utility
metrics: [f1_before, f1_after, f1_drop, f1_drop_pct]
```

当前能力边界：

| case | modular CPU | target-direct SyncMate | 说明 |
|---|---:|---:|---|
| post_unlearning_utility | 可执行 | 可执行 | 从已验证 GU Output 的原始预测计算 |
| post_unlearning_utility_and_retrain_gap | 可执行 | 可执行 | 显式配对相同实际请求、训练与删除语义的 GU/Retrain Output |

Retrain 已注册为独立 Unlearning 方法；Metrics 不执行训练。独立小表、输出身份、节点删除语义、Metrics-only 配置和可重跑 CPU 示例见 [独立 Retrain 与 Metrics](retrain_outputs.md)。

## 执行方式

本地只解析计划：

```powershell
python -B -X utf8 experiments/run.py path/to/experiment.yaml --dry_run
```

`experiments/run.py` 不接受模块化实际执行。注册 SyncMate recipe 时，由项目 stage 构造
`ExecutionContext` 并传入 `modular_run.execute`；job ID 和 RequestDevice 来自 SyncMate，
不从科研 YAML 或任意队列参数读取。现有 target-direct formal recipe 继续走已注册的
`target_direct_v1.syncmate_stage`，其科研表现在引用 17 个 Selector 小表、一个 GNNDelete
小表和一个 Evaluation 小表；设备选择由 SyncMate preflight profile 负责。

项目执行策略固定使用 `results/cache_v2`，checkpoint 位于
`results/runtime/modular/checkpoints`，本次 scratch 位于
`results/runtime/modular/<job-id>`，结果位于
`results/runs/modular/<experiment-id>/<job-id>/summary.json`。RequestDevice 和实际
Torch/CUDA/GPU 信息只写 execution receipt，不进入科研配置或默认缓存身份。同一 Recipe 在
可见同一／已同步 Store 时可以跨 device HIT；另一台机器看不到该 Artifact 时仍是物理 MISS，
不能用逻辑身份相同冒充已有文件。

## Dataset/Split 与缓存边界

Dataset/Split 小表只读引用已持久化的图和划分 manifest，并校验 manifest SHA、数据 SHA、
split hash、节点空间和三个 mask。入口不会下载、重切或修复数据。Score 以方法为单位进入
统一 Cache V2 Store；预算无关且前缀稳定的 Score 可被不同 K 复用，Selection 仍绑定规范化
预算、实际 K 和 tie-break。GU 只依赖它实际消费的 Selection、目标模型和自身方法参数。

运行 JSON 保存完整有效配置及来源、checkpoint、Score/Selection/GU 身份、Evaluation
receipt、HIT/MISS、producer 调用和 execution receipt。展示 ID、YAML 文件名、设备、路径和
下游 Evaluation 不反向进入 Selector Recipe。
