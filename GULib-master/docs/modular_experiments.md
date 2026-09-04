# 独立实验配置与真实消费者

本入口落实 [AAGU-001 合同](experiment_contract/README.md) 的配置与缓存隔离；
实际能力由 `experiments/modular_config.py` 校验。它用于本地 CPU 验证。
正式 GPU 仍走已注册的 SyncMate stage，不能把 `level` 改成 formal 绕过正式门。

## 配置到消费者

每个 Dataset/Split、Selector、Unlearning 实例各用一份 YAML。实验大表只引用文件，
不接受 defaults、override、YAML merge 或重复字段。相同方法的变体就是另一份小表。
相对路径按拥有该路径的配置文件解析，路径和文件原文不进入计算身份。

```yaml
kind: experiment
schema_version: 1
experiment_id: cpu-selection-check
stage: selector
dataset_ref: dataset.yaml
selector_refs: [degree.yaml, b_hutch.yaml]
matrix: cartesian_product
execution_authorized: true
execution_binding:
  level: verification
  device: cpu
  store_root: runtime/cache_v2
  runtime_root: runtime/models
  output: runtime/selection-run-001.json
```

```yaml
# b_hutch.yaml
kind: selector
schema_version: 1
method: b_param_hutch
candidate: {pool: train_mask}
budget: {mode: k, value: 2}
model: {architecture: OpenGU.GCNNet, hidden_channels: 4}
training: {epochs: 3}
parameters: {hutchinson: {probes: 2}}
```

degree 表只需 kind/schema_version/method/candidate/budget，不声明模型。
K 必须落在实际候选集合内；比例预算使用 `train_candidate_count` 与
`floor_with_minimum_one`。Score 不绑定 K，Selection 绑定规范化预算、实际 K 和同分规则。

```powershell
python -B -X utf8 experiments/run.py path/to/experiment.yaml --dry_run
python -B -X utf8 experiments/run.py path/to/experiment.yaml
```

dry-run 解析小表并验证已有 Dataset/Split 和 Selection 引用，不训练、不写 Store。
实际执行必须显式授权，并使用尚不存在的输出文件；warm run 换一个输出文件名。
运行 JSON 保存全部 effective 配置、每字段来源、实际 checkpoint、Score/Selection/GU
身份、命中与 producer 调用情况。`evaluation` 是实验计划注释；本入口实际输出评分、排序
以及 GU 前后测试集 micro-F1，不据此宣称已完成 retrain-gap 或科学接纳阈值验证。

## 只读 Dataset/Split

dataset.yaml 沿用合同的 `dataset / preprocessing / split / artifacts` 四部分。
当前 adapter 为 `OpenGU_persisted_processed_pair`；artifacts 需要 manifest 路径、
其 SHA256、实际 split_hash 和 `pyg-global-node-index-v1`。空引用直接失败。

本入口的 manifest 合同如下，须由已授权的数据准备步骤提供；执行入口不会生成它，
也不会下载、重切、修复或转换已有数据。现有 formal profile manifest 仍由原正式入口消费。

```text
schema = opengu.persisted_dataset_split; version = 1
dataset / preprocessing / split = 对应小表的有效元数据
data_path = 相对本 manifest 的已持久化 PyG Data pickle
data_sha256 = pickle 文件 SHA256
data_identity = utils.target_checkpoint.data_identity(data) 的完整结果
```

检查文件 SHA、元数据、features/labels/edges/split 内容身份；三个非空布尔 mask 必须
划分全部节点。当前模型消费者接受有限 float32 特征。仅加载受信任的数据准备产物。
临时小图和 manifest 的完整生成例见 `tests/test_modular_consumers.py:tables`；该 fixture
只生成验证数据，不能成为正式 Cora/CiteSeer/PubMed 证据。

## 默认值与实现边界

| 小表 | 默认值权威 | 当前消费者 |
|---|---|---|
| Selector 方法参数 | target_direct_v1/methods.py 的 parameter_defaults | 原有 17 个评分公式 |
| 模型/训练 | modular_config.py；实际 model/properties/GCN.yaml 或 SGC.yaml | GCN 两层、SGC 三层；Adam/SGD，无调度器 |
| GU 参数 | parameter_parser.py + gu_defaults 的固定实现约束 | GNNDelete/GCN 节点删除；GIF/GCN 或 SGC 节点删除 |

人工表可省略默认字段；解析后完整展开，再进入 Recipe。省略与显式同值相同。
不支持的模型、字段、数值类型和方法参数直接拒绝。GNNDelete 只支持当前
`both_layerwise / mse_mean / Adam / zero decay` 实现。GIF 可声明 GIF 或 IF。
TracIn 的 checkpoint_steps 选实际 epoch，cp3 再取 first/middle/final，cp_all 消费全部
所选快照。省略 steps 时消费当前轨迹；`_3/_6` 是既有方法名，不新增变体分发机制。

Score 每方法独立读写统一 Cache V2 Store，复用既有 ScoreBundle 存储格式，每个载荷
只含一种方法。共同梯度/IHVP 可以在本次 MISS 计算中复用；它们没有共同整包身份。
Recipe 绑定真实数据/候选、有效方法参数、被消费的模型状态或快照及其 update_lr、
模型前向与算法函数指纹、数值环境；不绑定实验 ID 或下游 GU。

Selector 的训练使用自己的监督配置，不借 GU 的 train/unlearn 参数。模型 forward 与
GU 专用 reason_once 指纹分开。GU Result 绑定自己的配置、训练 checkpoint、实现和
精确 Selection 引用。基础训练配置、数据、数值环境及实际训练实现一致时，两侧才共享
checkpoint。显式引用不同 metadata/state/file hash 的 checkpoint 会失败。

## 已有 Selection → GU

把上面的 stage 改成 `unlearning`，移除 selector_refs，使用刚刚生成的三个原样身份：

```yaml
selection_input:
  artifact_id: <真实 Selection artifact_id>
  recipe_hash: <真实 Selection recipe_hash>
  content_hash: <真实 Selection content_hash>
unlearning_refs: [gu.yaml]
```

```yaml
# gu.yaml
kind: unlearning
schema_version: 1
method: GNNDelete
model: {architecture: OpenGU.GCNNet, hidden_channels: 4}
training: {epochs: 3}
parameters: {unlearning_epochs: 2, unlearn_lr: 0.01}
```

此分支验证 Store 完整性、Dataset/Split/候选和三个身份后，直接调用原 GU 消费者，
不调用任何 selector producer。也可在 unlearning stage 同时引用 selector_refs 与
unlearning_refs 形成笛卡尔积；每个实例保持独立配置。checkpoint 引用属于其模型小表，
包含 path/file_sha256/state_hash，不能由实验大表隐式覆盖。

## 正式链路的机械变更

target-direct 保留原来已批准的 17 方法、模型、数据、seed、两种预算和启动边界。
selection summary / receipt 更新为 version 3，按方法保存 Score 身份；两预算之间
分别复用每一种方法的 Score。旧整包活动键已移除。旧 Artifact 留在原 Store，
不删除、不覆写、不迁移，也不将身份不同视为损坏。正式运行及远端部署本次未观察。
