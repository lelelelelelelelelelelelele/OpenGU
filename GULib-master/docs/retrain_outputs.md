# 独立 Retrain 与持久化 Metrics

本说明覆盖节点删除、已支持的 GCN/SGC、GNNDelete/GIF 和 Retrain 软件消费者。研究结论仍需各实验自己的正式定义、输入绑定、设备、执行批准和证据接纳。

## 从配置到指标

~~~text
Dataset/Split 小表 -> 校验 manifest、图与 split 哈希 -> 只读真实输入
Selector 小表 -> Score -> Selection Artifact
                            |
                     精确 Selection 引用
                      /               \
             GU 小表 + 原 checkpoint   Retrain 小表
             GNNDelete / GIF            随机初始化 + 现有监督训练器
                      |                |
               独立 GU Output     独立 Retrain Output
                      \                /
                  显式 Output 引用 + Evaluation 小表
                            |
                  只读 Metrics -> 指标与 receipt
~~~

modular_config.py 解析独立实例；modular_run.execute 由项目 stage 提供 ExecutionContext。科研 YAML 不携带设备、Store、输出目录或运行授权。

Retrain 在既有 GU_METHODS 注册表中选择，唯一实现是 unlearning/unlearning_methods/Retrain/retrain.py 中的 run_retrain，复用 modular_model.train_supervised 和现有 train_trajectory。旧 AttackPipeline.run_retrain 已删除。没有从 Metrics 进入训练的调用。

最小小表：

~~~yaml
kind: unlearning
schema_version: 1
method: Retrain
~~~

模型与训练默认值由现有方法所有者展开，也可在小表显式填写 model 和 training。Retrain 不接受原模型 checkpoint 或 GNNDelete/GIF 专属参数。

## 删除与评价语义

deletion 合同默认展开为：

~~~yaml
deletion:
  task: node
  supervision: exclude_selected
  training_graph: remove_incident_edges
  features: retain_isolated_rows
  evaluation_graph: original
~~~

请求必须是非空、唯一、属于训练集的节点，并留下至少一个监督节点。Retrain 从训练监督中排除这些节点，移除全部关联边，重新初始化模型并按相同的模型、优化器、学习率、权重衰减、训练轮数和 seed 训练。原 Dataset/Split 不修改。

节点编号和特征行保留；删除节点在训练图中孤立，其标签不参与监督。这是明确的节点删除合同，**不声称覆盖特征清零、物理移除节点编号或任意 edge/feature 删除**。GCN 自环不把孤立节点的特征传给保留节点。

评价图可选 original 或 retained。前者在原图上评价所有模型，后者统一在删边图上评价；baseline、GU、Retrain 的 logits 使用同一评价图。GNNDelete/GIF 自有训练算法保持原实现，最终公共指标从明确评价图上重新前向并持久化的预测计算，不混用方法内部评价值。改变评价图形成新的产物身份。

## 精确输出与复用

每个 Output 是统一 Cache V2 中的一个 prediction Artifact，合同为 opengu-node-unlearning-output-v1。NPZ 保存原始 logits、完整模型 state、GNNDelete 的 deletion masks、标签、原始 split masks、保留监督、实际请求、特征、原始边、训练边和评价边。没有先舍入再重算的中间环节。

计算身份包含真实数据/划分哈希、实际节点请求、模型/训练/删除合同、该方法的有效参数、producer 源码和执行实现。GU 额外绑定原 checkpoint state；Retrain 不绑定 GU 方法、GU 参数、实验编号或 Evaluation。Selection 的精确引用及内容依赖可复核；跨 GU 计算复用使用同一已验证 Selection 引用。Metrics 配对另核对实际请求和共同训练、评价语义。

冷运行仅在精确 MISS 时调用所选方法；热运行核验 Output 字节、header、recipe、producer 和 Selection 依赖。缺失或不同身份不允许 Metrics 自动计算、修复或查找近似结果。恢复出的 CPU 模型可用 unlearning_outputs.restore_model 重做前向核对。

原有通用 AttackResult 序列化也保存完整浮点精度，显示时再格式化。其 producer 指纹包含序列化源文件，因此新计算不覆盖旧舍入产物。

## 三种独立运行

Retrain-only 大表使用 stage: unlearning、一个 selection_input 精确引用和 unlearning_refs: [retrain.yaml]。不会调用 Selector，也不会训练原模型。

GU 执行可显式提供 retrain_input 引用，或把 Retrain 作为独立 Unlearning 实例一起调度。未提供 Retrain 时，retrain-gap 在训练之前拒绝。

独立 Metrics 大表：

~~~yaml
kind: experiment
schema_version: 1
experiment_id: metrics-only
stage: metrics
dataset_ref: dataset.yaml
matrix: cartesian_product
output_inputs:
  - unlearning: {artifact_id: <GU id>, recipe_hash: <full sha256>, content_hash: <full sha256>}
    retrain: {artifact_id: <Retrain id>, recipe_hash: <full sha256>, content_hash: <full sha256>}
evaluation_refs: [gap.yaml]
~~~

Metrics stage 没有 Selector、Unlearning 或 checkpoint 生产入口；读取 Dataset/Split 只为再次校验输入身份。post_unlearning_utility 和 post_unlearning_utility_and_retrain_gap 均由 modular 消费者实现。对单标签多分类，micro-F1 与 accuracy 相同；gap = perf_retrain - perf_unlearn，gap_pct 分母为 perf_retrain，分母为零时依原合同返回 0。

## 可重跑 CPU 示例

在项目根目录使用新的 disposable 目录：

~~~powershell
$env:CUDA_VISIBLE_DEVICES = '-1'
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/examples/retrain_cpu.py --directory .workblock/runtime/retrain-demo
~~~

该例生成并持久化 24 节点图和真实 split，逐步执行 Selection、独立 Retrain、GNNDelete/GIF、Retrain 热读取和两次 Metrics。读取阶段禁止优化器训练；receipt.json 保存引用、数值及重复一致性。输出目录已存在时拒绝覆盖。

之后可独立运行只读 CLI：

~~~powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 eval_collateral.py --store-root .workblock/runtime/retrain-demo/store --inputs .workblock/runtime/retrain-demo/output-references.json --evaluation .workblock/runtime/retrain-demo/gap.yaml --output-dir .workblock/runtime/retrain-demo/metrics-cli
~~~

它只读取已验证输出，生成 collateral.json 和无舍入预测导出。旧 --dataset_name 等训练参数已移除，不保留兼容重训路径。

## Target-direct 接入

已注册的 syncmate_stage -> experiments/run.py 调用链通过 target_direct_v1/run_outputs.py 显式执行两个独立输出，再调用只读 Metrics。方法表和 Evaluation 表引用进入 cell 指纹。已存在但身份不一致、缺失或损坏的 cell 被拒绝，不自动覆盖或重训。

该 lane 保持 GCN、GNNDelete/GIF 的已支持边界；其他旧矩阵若仍请求隐式 collateral 路线，会明确失败。它们须提供新的持久化输出消费者，不能退回旧训练路径。

新生成 target checkpoint 记录明确的训练条件；旧 checkpoint 若没有该必要身份字段，本消费链拒绝接纳。历史文件保留，不补写、迁移或自动重训。该变化只通过本地共享消费者与绑定检查验证，本 Block 未执行 SSH/GPU gate 或完整科研矩阵。
