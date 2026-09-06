# 实验合同：组合表与公共小表

本合同来自AAGU-001；AAGU-034修正其当前配置和入口表述，保留001/026已接受的历史记录。科研问题、阈值和运行批准由各实验WorkItem拥有；本规范不批准矩阵执行。

| 表 | 拥有的配置 | 边界 |
|---|---|---|
| Dataset/Split | 数据名称/预处理、已持久化图与划分的精确引用、split seed与比例 | 不消费Selector/GU参数，不自动下载或重切分 |
| Selector | 方法、候选、预算、排序、随机性；仅模型型方法声明模型/训练及checkpoint依赖 | 不消费GU专属参数；各方法独立Score/Selection |
| Unlearning | 独立方法、模型/训练/删除语义和自身参数 | 消费已验证Selection；Retrain从头训练，不依赖GU |
| Evaluation | 单方法指标或已保存输出的配对比较 | 不反向影响评分；离线Metrics不训练或前向 |
| Experiment | 四类小表引用、stage、矩阵、两项显式覆盖 | 只覆盖训练seed与比例预算，不开放任意参数覆盖 |

Dataset/Split、Selector、Unlearning仍是三个主要执行职责；Evaluation单独持有指标配置。Score、checkpoint、轨迹是内部可复用资产，不另建业务调度层。

## 有效值与来源

大表`seeds`、`budget_ratios`指定值优先于小表填写值，小表优先于实际方法默认值。两轴只在内存展开，源文件保持不变。训练seed配对模型型Selector与GU/Retrain，Dataset/Split seed、Random抽样seed和Hutch探针seed仍归各自小表。省略大表字段沿用小表。显式checkpoint不能重新贴seed标签。

同语义小表只维护一份，放在[公共目录](../../experiments/configs/README.md)；参数不同的实例另存，例如B-Hutch64和GNNDelete lr0.02。未知字段、任意override、YAML merge、隐式文件继承均拒绝。

Selector/Unlearning只通过selector_refs声明选点，缓存自动HIT/MISS；实际Selection身份、哈希与缓存观察写入结果，不在用户配置中绑定上轮产物。执行与核验共用批次及条件展开，dry-run和summary展示有效值与来源。注册指纹绑定所有引用配置，Cache V2只绑定实际消费的有效输入与producer。公共路径、experiment/case ID、run_id不进入未消费它们的模块计算键。

## 使用顺序

1. 在WorkItem中确认问题、科学范围、预算/训练seed、指标与批准边界。
2. 复制[普通模板](../../experiments/configs/experiment.template.yaml)，引用公共小表；仅填写必要参数和有意覆盖值。
3. 用统一入口dry-run核对有效值与来源；隔离CPU执行验证软件链。
4. 正式运行通过登记的SyncMate recipe调用同一入口；共享stage check与实验预检通过后执行，不改变正式数据根或绕过GPU要求。
5. 收集、校验真实产物后进行独立Metrics和人类验收。缺失、冲突或未确认条件如实保留。

[执行说明](../modular_experiments.md)描述命令、真实Selection/Output绑定和收集合同；[当前参数](PARAMETERS.md)提供值与实现来源；[组合示例](examples/)引用同一公共目录。不同Selector/GU模型仍可独立声明，只有配置、真实数据、checkpoint及producer都相符时才共享。

## 历史接口修正

旧formal-v2专用解析/调度、扁平run.py分支与015生成器已退役。旧定义保存在[历史配置](../archive/experiment-configs-pre-aagu034/)，实际历史结果与Artifact未改写。17种方法的评分代码保留；TracIn公共表明确从真实100-epoch轨迹取3/6个指定checkpoint。软件验收报告归[同一034 WorkItem](../../.workblock/items/AAGU-034/WORKITEM.md)，不把CPU测试视为正式GPU结果。
