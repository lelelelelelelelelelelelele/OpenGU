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

Retrain-only 大表使用 stage: unlearning、selector_refs 和 unlearning_refs: [retrain.yaml]。Selector通过有效配置自动查询缓存，HIT不重复评分或选点，MISS才计算；实际Selection身份保存在结果。Retrain自身从头训练、不加载原模型；模型型Selector若缓存缺失，仍需其声明的模型训练。

GU 与 Retrain 均按 unlearning_refs 独立调度，执行阶段只生成各自输出及单方法评价。retrain_input 已删除；执行阶段声明 retrain-gap 会在训练前拒绝，必须在独立 Metrics 阶段引用双方已经完成的结果。

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

已注册的 syncmate_stage -> experiments/run.py 按 unlearning_refs 展开独立 method cell。每次 execute_bound_method 只调用当前方法；没有 GU→Retrain 成对函数，没有 retrain_ref。正式表把 GNNDelete 与 Retrain 显式列为同级方法。已有研究的 306 个 GU 比较单元不变，Retrain 从每个 GU 单元内部隐式执行改为单独保存；两预算 canary 的每个请求分别产出两个方法结果，未放行正式矩阵。

每个方法的叶子为 attack.json（单方法原始指标、评价身份、实际调用/缓存/耗时记录）、output-references.json、predictions.npz（单个完整模型 state、logits、标签、mask 与图输入）和 _meta.json。完成检查不要求 collateral.json，也不要求另一方法先完成。方法表只允许 method 与方法参数，共同模型/训练轴由正式大表绑定；不悄悄忽略小表里的重复模型配置。

差值与 collateral 的输入引用在结果收集后建立，单独调用 eval_collateral.py 或 modular Metrics stage。通过 Cache V2 重算时，收集所引用 Output 的 Recipe、Artifact 和完整 Selection/Score 依赖及索引到本地 Store，保留内容和身份，不能只复制一个不带依赖的 NPZ 冒充已验证 Store。导出的完整 predictions.npz 可用于独立检查模型/数组，attack.json 可直接比较其原始标量及评价口径。

既有不匹配、缺失或损坏的 cell 被拒绝，不覆盖历史结果。GCN GNNDelete/GIF/Retrain 是该单方法适配器的支持范围；正式 recipe 仍只声明 GNNDelete 和参照 Retrain。其他旧矩阵若仍请求隐式 collateral 路线，会明确失败。

新 target checkpoint 记录明确训练条件。GU 消费时拒绝缺失这些字段的旧 checkpoint；Retrain 本身不读取或训练原 checkpoint。历史文件不补写、迁移或自动重训。本 Block 只做 CPU 软件验证，没有执行正式 SSH/GPU gate。

## 指标是否必须立即计算

当前注册指标没有要求 GU 和 Retrain 同时运行的情况。保存足够输入后，以下计算均可在结果收集后进行；不得把两个方法的训练绑在评价函数里。

| 指标 | 必须保存的输入 | 收集后能否计算 | 当前边界 |
|---|---|---|---|
| F1 / accuracy | 标签、test mask、预测类别或 logits | 可以；同口径标量也可直接比较 | 单标签分类，F1 使用 micro 平均 |
| 分类 AUC | 标签、test mask、每类概率或 logits | 可以 | 二分类使用正类分数，多分类 OvR macro；缺少测试类别时为 null 并说明原因 |
| 交叉熵 | 标签、test mask、logits | 可以 | 与训练 loss 分开记录 |
| retrain-gap / gap_pct | 配对的原始 F1 标量、双方身份 | 可以直接做差；当前验证器从数组复核 | 保留同数据/划分、请求、模型、训练和评价图配对检查 |
| 预测偏移、翻转率、图上分组诊断 | 双方逐节点预测、节点 ID、mask，分组时还需图 | 可以 | 不能仅靠两个 F1 数值恢复；现有偏移/翻转计算均只读数组 |
| update_detection_auc | 原模型和单方法输出的预测、删除节点及对照节点 | 可以 | 这是项目现有预测变化检测协议；没有原预测时明确报告缺少输入 |
| 泛指 MIA | 具体攻击协议所需的成员/非成员分数、标签或攻击模型 | 取决于已声明的攻击协议与保存内容 | 当前未注册通用 MIA evaluator，不能用 update_detection_auc 替代所有 MIA |
| 训练/遗忘耗时、峰值显存 | 执行时计时/设备观测 | 无法由最终模型倒推 | 需要执行时采集；缓存热读时间不是原冷训练成本 |

post_method_metrics 对 GNNDelete、GIF、Retrain 使用同一评价入口，保存 f1、accuracy、cross_entropy、classification_auc 以及可用性状态；当前更新检测 AUC 另用明确名称。Retrain 默认没有原模型预测，因此这项为 missing_original_predictions，不自动前向或重训。若后续指标缺少输入，应显式进行补充评价或报告缺失，而非让 Metrics 隐式补算。

改变指标公式/库版本只改变评价 receipt；方法输出身份不包含评价配置。输出生成之后，后处理阶段不调用 model.forward、Selector 或训练入口。实际运行的时长记录按冷计算与热读区分，不能从命中结果声称获得新的训练耗时测量。
