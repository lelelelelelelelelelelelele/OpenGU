# 普通 YAML 的统一执行链

[配置目录](../experiments/configs/README.md) 是现行表规范，模板为 [experiment.template.yaml](../experiments/configs/experiment.template.yaml)。AAGU-034 将原通用 dry-run 和专用 target-direct 实际运行收敛到一个入口；AAGU-001 的合同、026 的方法级缓存和 028 的独立输出继续由原模块承担。

## 同一解析与执行路径

普通命令和 SyncMate 注册都直接调用 `experiments/run.py <config.yaml> --run-id <id>`，共用 `modular_run.execute` 和 `modular_config.load_experiment` / `experiment_batches`。一个组合表用非空 `dataset_refs` 列表绑定多个 Dataset/Split；单数据集也用列表，重复实例和旧字段被拒绝。展开顺序为数据集、训练 seed、比例、方法、Selector，训练 seed 仍在两侧配对。

- `--dry_run` 展开真实有效值、字段来源、训练 seed/预算批次与逻辑条件数；不读数据、建 Store 或调用 producer。
- 设备只由 Core 读取的 `.syncmate/device.yaml` 决定：`repo_path` 指定执行根，`execution_device` 明确指定 `cpu`、`cuda` 或 CUDA 索引；没有设备默认值。正式执行要求在配置的 runner checkout 中使用可用 CUDA。
- 隔离验证另需 `--verification-root <temporary-root>`；该根等于设备配置的 `repo_path`，输入资产必须在其内部。`--device-config` 可指定临时设备文件。Core 注册直接指向普通配置路径，绑定文件及引用表指纹、运行身份、超时和阶段产物；没有专用 `--recipe` 分支。

## Selector → 固定 Selection → 独立方法

Selector 与 Unlearning 组合表只通过 `selector_refs` 声明选点规则，并在各表声明本轮训练 seed 和预算。有效输入与 producer 身份确定缓存查找：精确 HIT 复用真实 Selection，MISS 才计算；无需填写上一轮 summary、SHA-256 或 Artifact ID。实际 Artifact 身份、哈希及 HIT/MISS 写入结果，独立方法继续消费经过校验的 Selection。执行与收集核验共用 `experiment_batches`、`selector_entries`、`unlearning_entries`，避免两套条件展开。

GNNDelete、GIF、Retrain 各自执行、缓存、保存 Output。Retrain 使用真实删除集合，从头训练；不加载 GU checkpoint，也不调用其他方法。

## 输出与收集后 Metrics

每个阶段写一个 `summary.json`；Unlearning 另写独立方法的 `summary.outputs/<序号>/attack.json`、`output-references.json`、`predictions.npz`、`_meta.json`。Selector 和 Metrics 不声明不存在的方法文件。summary 记录有效值、来源、配置指纹、运行回执、Score/Selection/Output 身份和相对导出路径及摘要。每个 Output 保存实际训练图、删除集合、预测和模型状态，可脱离远端 Store 验证。

SyncMate 的 apply_collect → verify_collect → artifact index 仍是收集权威。项目验收消费者重核精确文件集合、字节摘要、运行 SHA、配置与方法身份、Selection、保存预测和指标。其通过仅表示软件证据核验，人的科研验收仍由 WorkItem 决定。

Metrics 是普通 `stage: metrics` 表，多数据集时 `output_inputs` 使用 `{summary: <已收集文件>, sha256: <摘要>}` 列表；单数据集还可读取精确 Output 引用。读取完整导出后按 Dataset/Split 身份分组，不访问远端 Cache，不调用模型前向或训练。输入中未声明的数据集、错误归属或缺失文件均拒绝。retrain-gap 必须配对同 Selection、Dataset/Split、模型、训练 seed 和删除语义；缺失或多义时拒绝。

summary v3 的 `datasets` 按声明顺序记录各实例、真实 data identity、节点数与候选数。每条选择与下游结果的 `matrix_values` 保存 `dataset_index`、`dataset_name`、`dataset_fingerprint`；导出 `_meta.json` 保存相同坐标。SyncMate 的 `expected_datasets` 逐数据集声明节点和候选数量，产物序号在整张表内连续，核验时不得跨数据集配对。旧 summary 保留原文，当前消费者不迁移或重写历史结果。

## 计算身份与配置指纹

`configuration_fingerprint` 绑定整组引用 YAML，供注册、预检和结果核验。计算缓存仍只读取已展开的实际有效输入和 producer，不使用公共文件路径作为计算键。仅预算变化复用预算无关评分并产生不同 Selection；模型训练 seed 影响模型型 Selector 与方法 Output，不改变 Degree/Random。实现指纹变化导致 MISS 时保留旧 Artifact，并如实记录。

保留共享计算：`target_direct_v1/{methods,scoring,recipe,method_cache}`、`c_target_v1/{core,score_store}`、`modular_model`、`modular_gu`、`unlearning_outputs`。旧专用调度与扁平解析已退役；无活跃消费者的旧 manifest 装配器与 adapter 同步删除；Dataset/Split profile 工具及历史数据/证据保留。

## 纯权重输入与训练缓存

GIF、IDEA、MEGU、GNNDelete 以及无需轨迹的模型型 Selector 可以声明 `checkpoint: <path.pt>`。相对路径以小表目录为基准。PT 只包含非空 `state_dict`；严格核对键、shape、dtype与有限性。显式路径直接加载，不查询基础训练缓存、不训练，不要求 SHA、元数据或 sidecar。基础训练 epochs/optimizer/lr/weight_decay/scheduler 被标为不适用；seed仅用于本次执行，不被认作该PT的训练seed。

Retrain-gap 与 flip-hop 配对时，显式 PT 的 epochs/optimizer/lr/weight_decay/scheduler 不参与和 Retrain 的相等比较，仍保留为不适用；本次执行 seed、模型结构、数据/split、Selection、删除语义及训练图/评价图必须一致。Retrain 使用自身声明的训练配置从头训练，PT 状态哈希仍保留用于来源追溯。内部训练模型的训练参数继续严格匹配。

未指定PT时根据实际数据/split、结构、训练参数和实现查缓存，MISS只保存最终纯权重及独立来源JSON。文件身份由框架计算，替换同路径权重会改变下游计算身份。内部缓存来源记录损坏会明确失败，不回退训练。旧封装不再支持，也不自动迁移。

MEGU 的遗忘 SGD 设置由 `parameters.unlearn_lr` 和 `parameters.unlearn_weight_decay` 独立控制，不再借用基础训练参数。TracIn按自己的checkpoint_steps/view管理独立轨迹；普通GU不读写全epoch。GraphEraser/GraphRevoker保留分片模型、分配和聚合状态，不接受单模型PT替换ensemble；Retrain仍从头训练。

新旧训练参数对照和正式运行命令见[063配置](../experiments/configs/aagu063/README.md)。
