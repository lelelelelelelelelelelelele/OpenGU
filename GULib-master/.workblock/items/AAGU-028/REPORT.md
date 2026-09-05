# AAGU-028 · Retrain 独立方法与 Metrics 输出复用

## Human Result

### 实际增量

GU 与 Retrain 的成对调用已删除。每个方法由自己的 YAML 独立执行，保存模型、原始预测和单方法指标；GU 不要求 Retrain 先完成。差值和预测比较在结果收集后单独处理。

### 核心观察

当前登记的评价指标没有要求 GU 与 Retrain 同时运行的情况。真实 CPU 结果复制到独立 Store 后，禁止训练和模型前向仍能重算单方法指标与差值，数值一致。163 项测试及 24 节点示例通过，3,995 个受保护历史文件哈希未变。

主要证据：[真实 CPU 观察](evidence/observations.json) 与下方场景。

### 当前决定

Agent 建议接受本次软件修复：独立执行、真实输出复用和错误身份拒绝已有约定证据。当前由用户决定接受、返工或拒绝；正式 GPU 运行与完整研究矩阵尚未执行，仍需后续实验各自的运行门槛。

> 当前验收决定：`接受`

## 验收场景与实际观察

### 方法各自完成

矩阵先完成 GNNDelete，此时没有 Retrain 结果；随后单独调度 Retrain。两个 cell 各自保存完整输出，不生成或依赖 collateral。禁止执行适配器后两者均能热复用；更改有效方法参数时拒绝旧输出。

**PASS** · `test_matrix_runs_one_requested_method_without_inline_comparison`

### 收集后无训练、无推理

将真实 GNNDelete、Retrain、GIF 输出及依赖复制到新的 Store；全局阻断模型 forward 和优化器 step 后，单方法 F1、分类 AUC、交叉熵及跨方法差值仍能精确重算。完整 NPZ 含模型 state 与评价输入；Store 字节未变。

**PASS** · `test_independent_method_metrics_survive_collection_without_forward`

### 独立方法与冷／热运行

已有 Selection 进入独立 Retrain YAML，冷运行没有创建原模型 checkpoint，也没有调用 Selector producer；再次读取时 producer_called=false，引用和数值一致。

**PASS** · `test_independent_retrain_cold_hot_cross_gu_and_metrics_only`

### 跨 GU 复用和只读评价

同一请求的 GNNDelete、GIF 共用一个 Retrain 引用。阻断 Selector、prepare_model、Adam/SGD step 后，热读和两次 Metrics 仍成功；Store 全文件快照相同。改变 GU 参数或指标集合后，Retrain 继续命中。

**PASS** · `test_independent_retrain_cold_hot_cross_gu_and_metrics_only；test_gu_parameters_and_metrics_do_not_change_retrain`

### 删除语义与模型可复核

删除节点不再参与监督，全部关联边被移除；节点编号和特征行保留。保存的模型 state 重建后，前向 logits 与保存数组逐元素相等。Retrain state 与既有监督训练器在相同保留图上的 state 哈希相同。

**PASS** · `test_retrain_removes_supervision_and_incident_edges；test_independent_retrain_cold_hot_cross_gu_and_metrics_only`

### 不同身份明确拒绝

模型、训练、评价图语义或请求改变时产生新身份，旧配对被拒绝。分别修改真实特征、标签、边、split 后，旧输出不能被消费；输出损坏、完整哈希不符、producer 改变、Selection 依赖缺失均拒绝，没有隐式重训。

**PASS** · `test_retrain_identity_changes_and_pairing_rejects；test_actual_dataset_changes_cannot_consume_old_output；test_missing_and_corrupted_outputs_rejected_without_training；test_changed_producer_and_missing_selection_dependency_rejected`

### CLI 与活动调用链

独立 eval_collateral CLI 只读已有输出，返回 training_producer_called=false，Store 未变。target-direct 每次调用一个方法；正式表显式列出 GNNDelete 与 Retrain，单方法完成检查不要求另一方结果。正式 stage 的 GPU 调用未执行。

**PASS** · `test_metrics_cli_and_target_direct_shared_consumer；既有 target-direct 配置／stage 回归`

### 精度与历史数据

AttackResult 的 JSON 往返保留原始浮点值，Metrics 从原始 logits 计算。source 与 canonical 的 10 个 cache/result 根逐文件核对，3,995 个现有文件未变；原本不存在的根没有被创建。

**PASS** · `test_aggregate_serialization_is_lossless；TestAttackResult.test_to_dict；protected-before/after.json`

## 24 节点可重跑示例

表中保留实际存储精度。两种 GU 引用同一 Retrain，独立 Metrics 两次结果完全相同。

| 方法 | perf_unlearn | perf_retrain | gap |
|---|---:|---:|---:|
| GNNDelete | 0.42857142857142855 | 0.42857142857142855 | 0.0 |
| GIF | 0.42857142857142855 | 0.42857142857142855 | 0.0 |

Retrain 引用：`pred_b492204e_7b61c0bd`。完整 recipe/content 哈希见 observations.json。

### 各方法自己的指标

| 方法 | F1 micro | 分类 AUC | 交叉熵 | 更新检测 AUC |
|---|---:|---:|---:|---|
| GNNDelete | 0.42857142857142855 | 0.75 | 0.706565594273937 | 1.0 |
| GIF | 0.42857142857142855 | 0.75 | 0.706565594273937 | 0.5 |
| Retrain | 0.42857142857142855 | 0.75 | 0.7009000715050294 | 缺少原预测 |

以上均由已保存的预测离线重算；这些小图数值是软件证据，不用于评价方法优劣。

## 边界与尚未观察

- 指标审查：F1、分类 AUC、交叉熵、retrain-gap、预测偏移/翻转及当前更新检测均可由保存的数据后处理。耗时和峰值显存须在实际执行时记录，不能从最终模型倒推；热读时间不能代替冷运行成本。完整输入清单见数据流说明。
- 分类 AUC 采用二分类正类分数或多分类 OvR macro，测试类别不完整时给出 null 和原因。当前 update_detection_auc 是预测变化检测，Retrain 缺少原模型预测时报告 missing_original_predictions；不自动补训或推理。通用 MIA evaluator 未注册，不伪造它已完整实现。
- 软件证据范围是本地 CPU、节点删除和已支持的 GCN/SGC 消费者，主要集成覆盖 GNNDelete、GIF、Retrain。不是任意 GU、模型或 edge/feature 删除的承诺。
- 默认删除语义：排除选中节点的监督、删除全部关联边、保留孤立特征行；默认在原图统一评价，也可明确选择保留图。GU 自有训练算法沿用现有实现。
- 跨 GU 计算复用使用同一已验证 Selection 引用；Metrics 再核对实际节点请求及共同模型、训练和评价语义。不能把不同来源或相近身份的输出猜配成同一结果。
- 新 target checkpoint 明确记录训练条件；旧 checkpoint 缺少这些字段时拒绝接纳，保留历史文件。其他旧矩阵若仍依赖隐式 collateral 路径，会明确失败，须在其所属任务接入输出消费者。
- NOT OBSERVED：SSH/GPU 正式 stage、真实正式数据上的成本与完整矩阵。样例的 utility 相等且 gap=0 只用于核对数据流，不证明任何方法效果或科研结论。

## 证据与复核

- [权威 WorkItem 与当前 source branch](WORKITEM.md)
- [数据流、删除语义与可重跑命令](../../../docs/retrain_outputs.md)
- [163 项结果、原始证据哈希及输出引用](evidence/observations.json)
- [隔离 CPU Verify 脚本](evidence/verify.py)
- [最小可运行示例](../../../experiments/examples/retrain_cpu.py)

原始日志目录：`E:\project\OpenGU-worktrees\aagu-028-retrain-metrics\GULib-master\GULib-master\.workblock\runtime\aagu-028-rework-verify3`。该目录为本机 ignored 运行证据；持久摘要与原始文件哈希保存在 observations.json。

统一 Verify 在干净软件检查点运行。报告、Record 与证据投影加入后的当前候选由 source branch 的 clean HEAD 唯一确定，最终 diff 复核与新增报告检查记入 WorkItem。测试日志不替代人的决定。

若返工改变待接受代码，在同一 WorkItem 更新候选和当前报告，决定保持待决定；若接受，由同一次 Closeout 同步当前决定并按项目流程执行。
