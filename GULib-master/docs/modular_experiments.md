# 普通 YAML 的统一执行链

[配置目录](../experiments/configs/README.md) 是现行表规范，模板为 [experiment.template.yaml](../experiments/configs/experiment.template.yaml)。AAGU-034 将原通用 dry-run 和专用 target-direct 实际运行收敛到一个入口；AAGU-001 的合同、026 的方法级缓存和 028 的独立输出继续由原模块承担。

## 同一解析与执行路径

`experiments/run.py` 的配置路径模式与 `--recipe` 模式都调用 `modular_run.execute`，并使用 `modular_config.load_experiment` / `experiment_batches`。不存在只供检查的新配置规格，也没有逐条件 YAML 生成器。一个组合表只绑定一个 Dataset/Split。

- `--dry_run` 展开真实有效值、字段来源、训练 seed/预算批次与逻辑条件数；不读数据、建 Store 或调用 producer。
- 本地命令须显式提供 `--verification-root` 与 `--run-id`。目录必须在源码 checkout 外，输入资产也须在该根内；运行固定 CPU。
- `--recipe` 由 SyncMate 调用，不能混入其他配置、路径或覆盖参数。登记固定配置指纹、全部引用表指纹、运行身份、超时和精确产物清单。

## Selector → 固定 Selection → 独立方法

组合表可以直接引用 `selector_refs`。后续阶段也可使用精确三元 Selection 引用，或者 `selection_input: {experiment_ref: stage_s.yaml, summary: <实际路径>, sha256: <实际摘要>}`。后者只读取已经完成的 Selector summary，逐批继承它的 seed/预算与真实 Selection 引用；不启动前一阶段、不重新选点、不生成逐条件配置。summary 的配置指纹、数据身份、数量与轴值须匹配源普通表。

GNNDelete、GIF、Retrain 各自执行、缓存、保存 Output。Retrain 使用真实删除集合，从头训练；不加载 GU checkpoint，也不调用其他方法。

## 输出与收集后 Metrics

每个运行写一个 `summary.json`，以及 `summary.outputs/<序号>/attack.json`、`output-references.json`、`predictions.npz`、`_meta.json`。summary 记录有效值、来源、配置指纹、运行回执、Score/Selection/Output 身份和相对导出路径及摘要。每个 Output 保存实际训练图、删除集合、预测和模型状态，可脱离远端 Store 验证。

SyncMate 的 apply_collect → verify_collect → artifact index 仍是收集权威。项目验收消费者重核精确文件集合、字节摘要、运行 SHA、配置与方法身份、Selection、保存预测和指标。其通过仅表示软件证据核验，人的科研验收仍由 WorkItem 决定。

Metrics 是普通 `stage: metrics` 表，`output_inputs` 可以是精确 Output 引用，或 `{summary: <已收集文件>, sha256: <摘要>}` 列表。后者读完整导出，不访问远端 Cache，不调用模型前向或训练。retrain-gap 必须配对同 Selection、Dataset/Split、模型、训练 seed 和删除语义；缺失或多义时拒绝。

## 计算身份与配置指纹

`configuration_fingerprint` 绑定整组引用 YAML，供注册、预检和结果核验。计算缓存仍只读取已展开的实际有效输入和 producer，不使用公共文件路径作为计算键。仅预算变化复用预算无关评分并产生不同 Selection；模型训练 seed 影响模型型 Selector 与方法 Output，不改变 Degree/Random。实现指纹变化导致 MISS 时保留旧 Artifact，并如实记录。

保留共享计算：`target_direct_v1/{methods,scoring,recipe,method_cache}`、`c_target_v1/{core,score_store}`、`modular_model`、`modular_gu`、`unlearning_outputs`。旧专用调度与扁平解析已退役；无活跃消费者的旧 manifest 装配器与 adapter 同步删除；Dataset/Split profile 工具及历史数据/证据保留。
