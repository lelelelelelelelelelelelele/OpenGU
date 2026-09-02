# 通用执行缓存

`AttackManager`、Score 策略、Selection 预热、collateral 和相对评价共用
`results/cache_v2/index.sqlite` 与 `artifacts/`。`cache_v2_store_root` 可以指定隔离的绝对路径；
消费者拒绝将 store 放入三个 Legacy 活动根。构造缓存对象不创建目录。

## 身份和计算

- Selection 使用现有 `opengu-selection-recipe-v2`：实际图、特征、标签、候选集、
  split、k、种子、策略参数和 producer 源码身份共同决定复用。训练型 selector 还绑定
  初始模型状态和训练参数；分片方法只能复用 canonical 全图模型产生的精确 Selection。
- Score 使用现有 typed Score Recipe/Payload。TracIn 绑定实际模型权重、数据及候选顺序；
  IM 绑定拓扑、候选集、MC 参数、selector seed 和实现后端。改变身份产生 MISS；
  同身份的损坏、依赖冲突或不同计算内容 fail closed，不覆盖已有 Artifact。
- 通用 GU 返回聚合指标，未必返回逐节点预测。Result 因此使用 Selection-dependent
  `opengu-attack-evaluation-v1` Evaluation 载荷，复用现有 FormalArtifactStore、resolver、
  index 和依赖校验；不虚构 Prediction。正式 Prediction → Evaluation 合同保持原义。
- Cache 层只解析、校验、存储。选点、训练和指标计算仍在 attack/experiment 层。
  Result HIT 跳过整次计算；Selection HIT 只跳过选点，目标 Evaluation 身份另行判断。
  Selection 和目标计算分别从请求种子开始，缓存命中不会改变下游 RNG 消耗。

## 开关与入口

默认开启 Result、Selection、Score。`demo_attack.py --no_cache`、
`AttackManager(..., use_cache=False)` 和单次 `run_attack(..., use_cache=False)`
禁用这些可选缓存的读写。`--enable_score_cache false` 只禁用 Score，Result/Selection
仍可命中；它不会要求已命中的上层结果重新计算。

`--selection_artifact_id` 指定的 Artifact 是调用者要求消费的证据输入；即使关闭可选缓存，
也必须读取并校验它。此入口不重新执行 selector。YAML `cache_v2.mode` 描述 Selection
输入的生产/外部来源，不再选择 Legacy 或 V2 后端；没有该节的通用运行也默认使用 V2。

`scripts/prewarm_selection_cache.py` 使用与通用消费者相同的精确请求；不覆盖 HIT。
Legacy payload 转换/注入脚本已退出执行链。旧 payload 的分类和物理归档仍由 AAGU-023
拥有；本次未转换旧 payload，未修改既存 Artifact，未执行正式 GPU 实验。

验证入口：`python -B -m pytest tests/test_generic_cache_v2.py tests/test_score_cache.py`。
该验证以隔离 CPU 图和真实 pipeline 编排检查行为，不提供新的研究结果。
