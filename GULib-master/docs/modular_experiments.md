# 普通 YAML 的统一执行链

[配置目录](../experiments/configs/README.md) 是现行表规范，模板为 [experiment.template.yaml](../experiments/configs/experiment.template.yaml)。AAGU-034 将原通用 dry-run 和专用 target-direct 实际运行收敛到一个入口；AAGU-001 的合同、026 的方法级缓存和 028 的独立输出继续由原模块承担。

## 同一解析与执行路径

原生命令调用 `experiments/run.py <config.yaml> --run-id <id> --device <cpu/cuda/cuda:N>`，SyncMate 注册在同一入口追加 `--syncmate`，共用 `modular_run.execute` 和 `modular_config.load_experiment` / `experiment_batches`。一个组合表用非空 `dataset_refs` 列表绑定多个 Dataset/Split；单数据集也用列表，重复实例和旧字段被拒绝。展开顺序为数据集、训练 seed、比例、方法、Selector，训练 seed 仍在两侧配对。

- `--dry_run` 展开真实有效值、字段来源、训练 seed/预算批次与逻辑条件数；不读数据、建 Store 或调用 producer。
- 原生入口显式传 `--device cpu`、`cuda` 或 CUDA 索引，不加载 Core 或 `scripts/syncmate`。正式执行仍要求活跃 checkout 与可用 CUDA；设备缺失或不可用立即失败，不设默认设备。
- 显式 `--syncmate` 时，适配组件用 Core 读取 `.syncmate/device.yaml` 的 `repo_path`、`execution_device`；不能同时传 `--device`。`--device-config` 只用于该模式，缺少 Core 或无效接入上下文即拒绝。
- 隔离验证另需 `--verification-root <temporary-root>`，输入资产必须在其中；接入模式还要求该根等于 device 的 `repo_path`。配置不改写，硬件不进入科学 YAML。
- `execute(..., notify=None)` 的通知只传当前位置与完成量。计划来自实际预算降序批次，覆盖数据准备、Selector/GU、evaluation 和 export。执行器不导入 Core，训练 epoch 和求解内部不增加 SyncMate 调用。缓存 HIT 仍推进已完成量，失败保留科学异常且不汇报全局完成；通知错误只作诊断。

## Selector → 固定 Selection → 独立方法

Selector 与 Unlearning 组合表只通过 `selector_refs` 声明选点规则，并在各表声明本轮训练 seed 和预算。有效输入与 producer 身份确定缓存查找：精确 HIT 复用真实 Selection，MISS 才计算；无需填写上一轮 summary、SHA-256 或 Artifact ID。实际 Artifact 身份、哈希及 HIT/MISS 写入结果，独立方法继续消费经过校验的 Selection。执行与收集核验共用 `experiment_batches`、`selector_entries`、`unlearning_entries`，避免两套条件展开。

GNNDelete、GIF、Retrain 各自执行、缓存、保存 Output。Retrain 使用真实删除集合，从头训练；不加载 GU checkpoint，也不调用其他方法。

## 输出与收集后 Metrics

每次运行写 `results/runs/<experiment-id>/<run-id>/run.json`，cell 目录保存实际 `metrics.json`、`selection.json` 和按需导出的已有 `scores.npz`。项目自己的 `experiments/modular_layout.py` 拥有公共路径；适配器消费同一布局。完整内容和 Observer 合同见 [结果回传合同](experiment-result-return-contract.md)。

原生执行自行保存结果；接入执行由项目声明精确回传集合，Core 负责 apply_collect → verify_collect → SHA-256 → artifact index。进度快照属于运行状态，不进入科学结果或不可变索引。`job-progress` 只读取本地缓存；最后阶段完成不等于结果回传或科研接受。

Metrics 是普通 `stage: metrics` 表，通过 `output_inputs: [{run: <完成的 run.json>, sha256: <摘要>}]` 在持有输入与 Output Cache 的执行端重算。缺失、冲突或过时引用拒绝。常规本地结果读取不依赖图、模型或预测；不把远端 Cache payload 作为结果副本回传。

各 cell 记录真实 Dataset/Split、Selection/Output 引用、条件、HIT/MISS 与计时；无通知、通知启用和 Core 接入不进入计算缓存身份。run ID 只影响结果目录和运行记录。

## 计算身份与配置指纹

`configuration_fingerprint` 绑定整组引用 YAML，供注册、预检和结果核验。计算缓存仍只读取已展开的实际有效输入和 producer，不使用公共文件路径作为计算键。仅预算变化复用预算无关评分并产生不同 Selection；模型训练 seed 影响模型型 Selector 与方法 Output，不改变 Degree/Random。实现指纹变化导致 MISS 时保留旧 Artifact，并如实记录。

保留共享计算：`target_direct_v1/{methods,scoring,recipe,method_cache}`、`c_target_v1/{core,score_store}`、`modular_model`、`modular_gu`、`unlearning_outputs`。旧专用调度与扁平解析已退役；无活跃消费者的旧 manifest 装配器与 adapter 同步删除；Dataset/Split profile 工具及历史数据/证据保留。

## 纯权重输入与训练缓存

GIF、IDEA、MEGU、GNNDelete 以及无需轨迹的模型型 Selector 可以声明 `checkpoint: <path.pt>`。相对路径以小表目录为基准。PT 只包含非空 `state_dict`；严格核对键、shape、dtype与有限性。显式路径直接加载，不查询基础训练缓存、不训练，不要求 SHA、元数据或 sidecar。基础训练 epochs/optimizer/lr/weight_decay/scheduler 被标为不适用；seed仅用于本次执行，不被认作该PT的训练seed。

Retrain-gap 与 flip-hop 配对时，显式 PT 的 epochs/optimizer/lr/weight_decay/scheduler 不参与和 Retrain 的相等比较，仍保留为不适用；本次执行 seed、模型结构、数据/split、Selection、删除语义及训练图/评价图必须一致。Retrain 使用自身声明的训练配置从头训练，PT 状态哈希仍保留用于来源追溯。内部训练模型的训练参数继续严格匹配。

未指定PT时根据实际数据/split、结构、训练参数和实现查缓存，MISS只保存最终纯权重及独立来源JSON。文件身份由框架计算，替换同路径权重会改变下游计算身份。内部缓存来源记录损坏会明确失败，不回退训练。旧封装不再支持，也不自动迁移。

MEGU 的遗忘 SGD 设置由 `parameters.unlearn_lr` 和 `parameters.unlearn_weight_decay` 独立控制，不再借用基础训练参数。TracIn按自己的checkpoint_steps/view管理独立轨迹；普通GU不读写全epoch。GraphEraser/GraphRevoker保留分片模型、分配和聚合状态，不接受单模型PT替换ensemble；Retrain仍从头训练。

新旧训练参数对照和正式运行命令见[063配置](../experiments/configs/aagu063/README.md)。
