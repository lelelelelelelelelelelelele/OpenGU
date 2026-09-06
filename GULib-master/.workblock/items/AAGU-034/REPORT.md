# AAGU-034 · 实验配置与统一执行入口修正

## Human Result

### 实际增量

普通 YAML 现在通过同一入口完成检查和真实执行，项目注册也复用该内核。公共小表统一持有参数；015 的逐条件配置生成器及旧专用执行路径已退役，原科学范围保留。

### 核心观察

临时 CPU 图上，两训练 seed、两预算产生 24 个独立方法输出；再次运行禁用训练和评分后全部 HIT，输出身份一致。真实 100-epoch 轨迹分别选出约定的 3/6 个 checkpoint。349 项相关测试通过，活动 YAML 从 522 张减至 46 张。主要证据：[真实观察](evidence/observations.json)、[迁移审计](evidence/configuration-audit.json)。正式 SSH/GPU 实验尚未执行。

### 当前决定

> 当前验收决定：`待决定`

Agent **建议接受本次软件修正**：统一入口、有效配置、缓存和注册/收集接缝已有约定证据。由用户判断接受或返工；接受对象是本任务 source branch 的当前干净 HEAD。正式运行与科研结论仍由后续任务验收。

## 迁移前后：减少维护文件，保留逻辑条件

| 对象 | 基线 | 当前候选 |
|---|---|---|
| 活动配置目录 | 522 张 YAML，多种规格 | 46 张：28 张公共小表、18 张普通组合表 |
| 公共小表 | 分散在015、formal-v2、007、SM005及合同示例 | 3 Dataset/Split、18 Selector、4 Unlearning、3 Evaluation；其中包含明确的 Hutch64、GNNDelete lr=0.02 变体 |
| 17 Selector | 015/V2 两套字段规则 | 以015为基准的同一规范；有效参数和真实依赖逐方法核对 |
| 015 维护文件 | 449 张，其中424张生成 YAML | 每数据集 S、U、Retrain、Metrics 各一张，共12张；不再生成叶配置 |
| 015 科学条件 | 3数据集 × 17方法 × 3训练seed × 2预算 | Stage S 306；两种 GU 的 Stage U 612；独立 Retrain 306作为原有评价参照 |
| 032 参考配置 | 7方法 × 2预算 × 3训练seed | 42条件，公共引用；科学方案仍由032单独验收 |
| 007 最小组合 | 8张按seed等拆分的小表 + 组合表 | 1张普通组合表引用公共小表，2seed × 1预算 × 2方法 = 4输出 |
| 历史配置 | 35张旧扁平/配方 YAML 在活动目录 | 退出执行，原Git内容留在历史目录；A3/A5说明同时归档 |
| 合同示例 | 重复的小表与组合表 | 4张组合示例引用公共小表 |
| 执行注册 | 38项，含旧专用与SM005注册 | smoke、preflight及1项普通007实验注册；旧36项删除，新增1项 |

18张组合表中，12张属于015，007与032各1张，1张通用模板，3张保留的SM005接口参考。参考表不提供活动作业注册，也不赋予运行批准。

015仍为 Cora/CiteSeer/PubMed、训练seed `[42,212,2024]`、预算 `[0.01,0.05]`。9组训练准备、141组Score、282组Selection是有效输入相同所导出的分组预测；没有把它们当作三数据集真实缓存命中或成本证据。Metrics预期形成612组GU/Retrain比较，数量需由后续真实绑定输出确认。

完整文件清单与参数对照：[配置迁移](evidence/configuration-migration.json)、[归档/示例映射](evidence/retired-configs.json)、[逐表展开与35项原文核对](evidence/configuration-audit.json)。

## 当前规范与可复用模板

一张组合表绑定一个 Dataset/Split，引用独立 Selector、Unlearning、Evaluation。仅开放训练 `seeds` 和 `budget_ratios` 两种大表覆盖：大表显式值优先于小表，小表优先于方法默认；只在内存展开，来源随结果保存。训练seed配对模型型Selector与GU/Retrain，不改split、Random抽样或Hutch探针seed；不支持任意override或给显式checkpoint换标签。

下面就是仓库中的[通用模板](../../../experiments/configs/experiment.template.yaml)，放在 `experiments/configs/` 时可直接 dry-run，展开8个条件。真实执行仍需绑定并验证输入资产。

```yaml
kind: experiment
schema_version: 1
experiment_id: example-cora-retrain
stage: unlearning
dataset_ref: datasets/cora.yaml
selector_refs: [selectors/degree.yaml, selectors/gt_full.yaml]
unlearning_refs: [unlearning/retrain.yaml]
evaluation_refs: [evaluations/post_method_metrics.yaml]
seeds: [42, 212]
budget_ratios: [0.01, 0.05]
matrix: cartesian_product
```

后续阶段通过 `selection_input: {experiment_ref, summary, sha256}` 读取真实 Stage S 摘要及其精确Selection，继承源表批次并核对方法、预算和身份；不会重新选点。Metrics通过 `output_inputs: [{summary, sha256}]` 读取已收集的独立输出。当前015后续引用为null，必须在真实阶段完成后填入，不以占位文件冒充资产。

规范入口：[001合同](../../../docs/experiment_contract/README.md)、[字段与实际依赖](../../../docs/experiment_contract/PARAMETERS.md)、[执行数据流](../../../docs/modular_experiments.md)。

## 验收问题与实际观察

### 普通命令是否真正执行 — PASS

在20节点、10训练候选的临时图上，普通组合表经过 `run.py` 的 `__main__`、同一解析/展开器和执行内核，完成 Degree、Random、a_grad_norm × seed122/722 × 预算0.1/0.2 × GNNDelete/Retrain，共24输出。实际优化器step处记录的训练seed集合为 `{122,722}`；每次删除节点数为1或2，原YAML字节不变。另一次无测量包装的直接CLI先执行Stage S，再绑定其摘要执行独立Retrain，Selection引用逐项相同，没有重新选点。

关键测试：`test_command_cold_warm_seed_budget_retrain_and_metrics`、`test_stage_s_summary_binds_real_selections_without_resampling`。前者在新Python进程中通过runpy进入真实命令，仅添加seed记录及producer阻断；不是用手工summary替代运行。

### 覆盖与缓存是否遵循真实依赖 — PASS

第二次执行同时阻断训练和评分producer，24项方法输出均HIT且身份与冷运行相同，训练/评分调用列表为空。只改预算时，Degree、Random、a_grad_norm的Score分组数分别为1、1、2；对应Selection分组为2、2、4。第二训练seed不影响无需模型的Degree/Random，模型型评分按训练seed区分。实际方法实现和Hutch参数变化的既有消费者测试也观察到相关MISS，其他评分继续HIT；移动/重命名小表不改变计算身份。

本次TracIn checkpoint选择函数增加拒绝错误轨迹的检查，会改变依赖它的producer指纹；这些Score及下游Selection/Output不能承诺复用旧身份。Metrics读取与配对实现的指纹也会更新评价回执。普通YAML路径迁移本身不进入计算键；没有清空或改写历史Artifact。正式旧缓存上的命中率与重算成本未测量。

### 17方法与TracIn 3/6语义是否保持 — PASS

17方法在同一小图上与保留的原评分公式逐项比较，最大绝对误差均为0。公共方法参数核对一致，TracIn的差别来自轨迹消费方式：通用训练真实保存100个epoch后，公共point `_3`评分实际绑定steps `[1,50,100]`，`_6`绑定 `[1,10,25,50,75,100]`。六种TracIn配置共用该checkpoint选择函数，静态展开全部满足3/6数量；没有给`_6`显式六步的100-epoch输入被拒绝。

这保留原约定的checkpoint语义，不将两套YAML字段差异直接解释成不同算法。实际轨迹及Score ID见[观察记录](evidence/observations.json)。

### 独立Retrain与收集后指标是否可复核 — PASS

保存的Retrain输出包含实际删除集合、模型与原始预测。被删除节点不再参与训练监督，所有关联边从训练图移除；训练seed与当前批次一致。普通Metrics命令读取保存输出后得到12行配对指标，没有训练/评分调用。独立输出回归进一步在禁止全局模型forward、优化器step且Store快照不变时重算指标。配对要求同一Selection身份、Dataset/Split、模型、训练及删除语义，缺失或多义时拒绝。

这些小图数值证明数据流和复用行为，不用于比较方法效果。

### 注册、预检、精确输出和收集是否一致 — PASS（隔离本地/CPU）

当前 `opengu-aagu007-v1` 绑定整组引用YAML指纹、运行身份和17个文件（1 summary + 4输出 × 4文件）。测试使用相同注册形状的两seed两预算CPU实例，真实进入 `run.py --recipe`、running queue身份和receipt契约、同一执行内核，产生33文件/8输出。正常 `apply_collect → verify_collect → artifact index → accept/results` 链路通过；重复收集fetched=0，无远端Store依赖。

隔离测试仅将正式OS/GPU策略替换成临时CPU策略，不声称实际使用了SSH或4090。生产预检在本机确实拒绝错误checkout与缺失GPU，未继续读取正式数据。缺文件、未核验索引、重复索引、错误Git SHA、损坏字节、错误配置，以及预算/Selector/Dataset语义错配共9类注入均失败关闭。

### 旧路径与当前说明是否收敛 — PASS

`run.py` 不再有旧flat解析与专用target-direct调度分支，`--recipe`只补充项目上下文后调用同一内核。旧atomic stage、target-direct stage/selection/config/output脚本和无活跃消费者的manifest assembler/adapter删除；过时注册、424份生成YAML及活动引用同步退役。001合同、配置说明、受影响WorkItem owner链接和看板投影已更新。完整测试集750项可正常收集，349项相关回归实际执行通过。

旧入口与Cache V1私有API测试中失效的断言按[替换清单](evidence/retired-tests.json)退役；有效参数、数据split、AutoReport与缓存消费者检查保留。迁移中暴露的旧注册断言已更新到新注册，未通过恢复兼容层来让旧测试通过。文档检查120链接通过，其中13个DocMap链接以canonical项目位置解析；历史记录及归档材料不冒充现行运行说明。

## 保留的共享模块与入口映射

| 模块/入口 | 当前职责 |
|---|---|
| `experiments/run.py` | 普通配置dry-run、隔离CPU命令、已注册项目命令的同一入口 |
| `modular_config` / `modular_run` | 公共小表、两轴展开、真实Selection绑定、统一执行 |
| `syncmate_stage` / OpenGU adapter | 正式位置/设备/数据/队列/输出契约政策；无第二套实验解析器 |
| `target_direct_v1/{methods,scoring,recipe,method_cache}` | 17种共享评分算法及方法级Score/Selection消费者；名称留在计算身份中 |
| `c_target_v1/{core,score_store}` | 已有张量计算、稳定排序和Score存储 |
| `modular_model` / `modular_gu` / `unlearning_outputs` | 训练、GU/Retrain独立输出和真实消费；未新增平行GU实现 |
| `modular_artifacts` / `opengu_method_output` | 同一已验证Output的便携导出与收集后读取 |
| `modular_evaluation` / `output_metrics` | 保存输出上的独立指标与配对比较 |
| `target_direct_v1/{split_profile,planetoid_io}` | 现有Dataset/Split工具与真实冷/热测试；本轮不运行正式数据准备 |
| `aagu015/definitions.py` | 只读审计普通表；旧generate命令已删除 |

GULib基础训练入口及历史证据读取功能保留其原职责，不构成另一套新实验格式。删除文件的精确清单见[入口退役](evidence/retired-code.json)。

## Verify、复跑与证据定位

2026-09-06，在干净软件检查点 `380105002579c99ad003418648a85e67da413a0a` 执行：

| 检查 | 结果 |
|---|---|
| 18个相关测试文件 | 349 passed，0 failed，224.90s；2条依赖警告 |
| 公共配置/所有引用/逻辑展开/归档原文审计 | exit 0 |
| dashboard refresh --check | PASS |
| SyncMate smoke --json | passed=true，errors=[] |
| 全测试收集 | 750项，无import错误；不声称全部750项执行过 |

完整参数和退出码：[命令回执](evidence/verify-checkpoint.json)；逐测试结果、实测seed/轨迹、输出引用及原始JUnit SHA-256：[观察记录](evidence/observations.json)；[测试日志](evidence/pytest.log)。原始fixture独立保留在回执的临时路径，原始JUnit位于canonical `.workblock/runtime/aagu-034-verify/`。所有测试数据与Store均为隔离临时资产。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/experiment.template.yaml --dry_run
& E:/conda_package/envs/gnn/python.exe -B -X utf8 -m experiments.aagu015.definitions check
& E:/conda_package/envs/gnn/python.exe -B -m pytest tests/test_unified_execution.py tests/test_syncmate_gu_outputs.py -q
```

真实临时命令形状为 `experiments/run.py <临时组合表> --verification-root <临时绝对根> --run-id <新身份>`。新根和新run_id避免覆盖；pytest会建立所需的小图、manifest与参数表。正式项目命令为注册的 `experiments/run.py --recipe opengu-aagu007-v1`，本报告不授权执行它。

当前待决定候选由[同一WorkItem](WORKITEM.md)的source branch干净HEAD唯一确定。报告/证据加入后对实际diff复核，复用上述检查点中未受影响的软件证据，并单独验证新增报告与状态投影；详见WorkItem Verify记录。

## 尚未观察与人类边界

**NOT OBSERVED：** SSH/GPU正式运行、正式数据上的训练与缓存命中、耗时/峰值显存、015完整矩阵、007科研gate及032科学方案验收。CiteSeer/PubMed真实资产绑定尚缺，015后续阶段的Selection/Output摘要引用待正式阶段完成后填写。Cora配置记录的manifest身份也须在真实checkout重验字节；本轮未准备正式数据。

本轮没有启动SSH/GPU、push、Apply、安装、历史缓存修复或清理。软件支持范围仍是已有节点删除、GCN/SGC和GNNDelete/GIF/Retrain消费者，不能推导任意模型或遗忘方法已适配。当前目标是确认统一配置和执行修正是否完成，后续正式任务必须消费人类接受后的版本。

HTML呈现检查：**PASS**。已实际查看headless Edge的1440×1000桌面、390×844窄屏首屏以及正文/边界截图；决定入口分别在485px和626px内，标题、正文、表格和命令可读，无页面横向溢出、断图或页面错误。观察层是本地HTML渲染，不代表SSH/GPU运行。[桌面](evidence/report-desktop.png) · [窄屏](evidence/report-narrow.png) · [呈现测量](evidence/render-qa.json)。
