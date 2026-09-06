# AAGU-034 · 实验配置与统一执行入口修正

## Human Result

### 实际增量

**核心问题：** 已有解析器和执行内核没有被直接接到 Core，专用 stage 又写死设备、检查队列。上一版还用替换生产预检的测试宣称接缝通过。

**本次修正：** 删除该 stage；Core 直接提交普通 YAML 命令。设备读取同一 `device.yaml`，回传由 Core 收集和核验；已有 007、032 模板继续使用。

### 核心观察

真实 Core 队列已执行 Selector、Unlearning、Metrics，分别回传 1、33、1 个文件；与直接命令的配置和数据身份一致，热运行复用缓存，损坏或缺失文件被拒绝。先写的 33 条行为断言未改；夹具更正和分批验证见[本轮证据](evidence/core-rework-observations.json)。正式 SSH/GPU 尚未运行。

### 当前决定

> 当前验收决定：`待决定`

Agent **建议接受这版软件修正**，依据是现有入口、设备配置和真实 Core 链路已经接通。接受对象为本 source branch 的当前干净 HEAD，决定权归用户；正式运行和科研结论另行验收。

## 为什么注册 034：原始问题与修正对照

034 于 2026-09-06 注册为 `correction_of AAGU-026` 的独立 FIX。原始 WorkItem 写明：

> 本项是 AAGU-026 的后续返工修正，解决其入口与配置规格未统一的问题，并接管 015 的冗余配置生成和 001 文档表述修正。

因此，本项验收要回答的是：**一份普通实验配置，是否已经能沿同一套规则进入真实训练、选点、遗忘/重训、缓存及注册收集，而无需为实验再维护专用解析器和成批 YAML？**

下面按注册时“本次增量”的六项对应整理。第 1–4 项有登记时的代码/配置问题记录；第 5 项是当时明确的覆盖语义要求，第 6 项是文档与职责要求，不能把要求本身当成曾发生过错误实验的证据。

| 注册时的真实问题或明确要求 | 本次对应修正 | 用什么判断修正是否成立 |
|---|---|---|
| **1. 公共配置没有一套共同规格。** 015 与 V2 各有 17 份 Selector 表；同一 `gt_full` 参数相同，但一边要求 `candidate/budget`，另一边拒绝这些字段。 | 公共目录持有同一套小表，组合表引用；同语义实例共用，不同参数变体明确区分。 | [配置审计](evidence/configuration-audit.json)核对全部活动引用；[实际观察](evidence/observations.json)包含17方法公式对照和真实TracIn 3/6轨迹。 |
| **2. “能检查配置”与“能实际执行”脱节。** `run.py` 对普通 `kind: experiment` 只放行 dry-run；已有真实内核没有成为统一命令路径。 | 普通检查、临时CPU执行、注册项目调用均进入同一解析/展开/执行链。 | [真实命令证据](evidence/observations.json)产生24个独立输出，另从Stage S真实摘要执行Retrain；不是仅调用解析函数。 |
| **3. 旧专用路径仍被消费。** `opengu_recipes/opengu_adapter` 仍调用旧 target-direct stage，活动注册不能只靠迁移文件名完成修正。 | 迁移预检、指纹、输出及收集契约后退役旧解析/调度与注册；本次复核又清除了M1 helper及其旧Adapter。 | [删除清单](evidence/retired-code.json)与零活动引用审计；[本轮真实Core验证](evidence/core-rework-observations.json)覆盖队列、设备、校验和结果读取。M1残留属于实施后补查，未冒充注册时已点名的问题。 |
| **4. 015 用文件复制表示实验条件。** 449份YAML中424份位于 `generated/`，按seed/预算生成，造成重复维护。 | 改为12张普通维护表和内存展开；保留原三数据集、17方法、三seed、两预算及阶段语义。 | [迁移审计](evidence/configuration-audit.json)：424副本退役；Stage S 306、Stage U 612、独立Retrain 306，文件减少未缩小科学范围。 |
| **5. 大表覆盖规则必须落实到实际消费者。** 只允许训练seed和预算，明确优先级、来源、模型型Selector与GU/Retrain配对；不能任意override或写回小表。 | 展开有效配置并记录来源，训练、选点和缓存使用实际消费值；Dataset/Split与Random抽样seed保持各自含义。 | [CPU冷/热观察](evidence/observations.json)：实际训练seed为122/722、选点数1/2、源YAML不变；阻断producer后HIT且输出身份一致。 |
| **6. 合同、模板和责任范围必须对齐。** 用户要求把公共整改独立登记为034，032继续只负责科学方案及最终配置验收。 | 更新001合同和配置/入口说明；通用规范适配已有007、032两份表，公共整改由034承担。 | [两份表的实际CLI检查](evidence/rework-observations.json)：跨工作目录引用正确，007为4条件、032为42条件，源表未改。正式实验及032科学接受仍由各自任务决定。 |

**原始来源：**[同一 WorkItem](WORKITEM.md) 的 Human Surface、Source and relations、Observed baseline and evidence boundaries。已与首次登记提交 `619d0f75135727ad09d00d658ef48d16e9bf4841` 核对；[原文摘录与来源定位](evidence/registration-problem-source.json)保留登记原文和Git对象身份。上表是对应说明，不改写原始合同，也不撤销026此前已接受的缓存/消费者证据。

## 本轮为什么再次返工

上一版虽然共用实验内核，仍在新建的 `experiments/syncmate_stage.py` 中写死 RTX 4090、CUDA 和 SSH 绝对目录，手读 running queue 与 receipt。测试又替换了整个生产预检并强改 CPU，因此它证明的是经过替换的链路，不能证明真实设备配置已经进入执行上下文。此前对此接缝的“通过”表述不充分，本报告以本轮真实 Core 观察替换该结论。

现在的职责如下：

| 现有组件 | 当前职责 |
|---|---|
| `device.yaml` / Core 的 peer 配置 | 声明执行设备、目录和 SSH 解释器。普通入口使用 Core 已有 reader；缺少 `execution_device` 或指定设备不可用时拒绝，不选默认设备。 |
| `experiments/run.py` / 原解析器及内核 | 同一普通 YAML 完成检查和执行；使用传入设备，保存本阶段结果。没有专用 recipe 分支、第二次生成 YAML 或手读队列。 |
| OpenGU adapter / 注册 | 绑定普通配置及引用表指纹、运行身份和阶段文件清单；消费已有结果身份核验。 |
| SyncMate Core | 正常提交、版本绑定、真实子进程、队列状态、收集、checksum 和可信索引。未修改独立 Core。 |

`syncmate_stage.py` 与无消费者的 CPU context helper 已删除，旧测试中的手写 running/receipt、替换生产预检和强改设备也已移除。没有添加新的实验调度器或配置生成器。

**测试先行的实际记录：** `cdc08804` 先提交行为测试并记录 7 项 RED。随后修正了夹具缺少模型资源、预算格式、训练型评分和本地 transport 四处设置，33 条断言的 AST 逐条未变。原始及更正后文件 hash 见[冻结记录](evidence/core-contract-freeze.json)。另退役了要求旧 stage 报错文案和整份注册表固定 hash 的两条实现快照断言；白名单、配置绑定、路径与真实消费者检查保留。

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

本次通用模板适配的具体对象就是已经存在的 **007 与 032 两份配置**，没有另建一份实验方案。两份 YAML 在本轮清理中保持原文：

| 现有配置 | 实际命令检查 | 展开结果 |
|---|---|---|
| [007](../../../experiments/configs/aagu007/experiment.yaml) | `run.py …/aagu007/experiment.yaml --dry_run` | 2批次、4独立方法输出条件 |
| [032](../../../experiments/configs/aagu032/experiment.yaml) | `run.py …/aagu032/experiment.yaml --dry_run` | 6批次、42条件 |

测试从不同临时工作目录启动真实命令，证明相对引用从各自 YAML 的所在位置解析。两者均进入 `run.py → modular_run.execute → modular_config`，没有调用 producer，所有活动源 YAML 字节保持不变；实际参数与结果见[本轮命令证据](evidence/rework-observations.json)。032 的科学配置接受仍由其自身 Block 决定。

以下[通用模板](../../../experiments/configs/experiment.template.yaml)只用于说明同一结构，放在 `experiments/configs/` 时可直接 dry-run，展开8个条件。真实执行仍需绑定并验证输入资产。

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

### 注册、设备与 Core 回传是否接通 — PASS（真实本地进程 / 临时 CPU）

在干净临时 runner checkout 中，由 Core 的正常 submit / run 接口完成三个阶段，未替换预检、设备读取、进程或队列状态：Selector 是两 seed × 两预算的4个选择结果，回传1份摘要；Unlearning 是8个独立方法输出，回传33文件；Metrics 从已保存输出读出4组配对指标，回传1份摘要。

直接命令与 Core 命令读取同一份源 YAML，配置指纹和 Dataset/Split 身份一致；运行后源 YAML 字节未变。执行回执记录实际 Python、cwd、设备和临时 Git SHA。先直接执行、再由 Core 执行时，Selector/Unlearning 都命中缓存，Output 身份一致。Core 实际收集并核验文件，重复收集 fetched=0；篡改和删除落地文件后均不再 verified。设备字段缺失、非法设备及越界 CUDA 索引在 producer 前失败。

原有8输出的项目结果读取与9类错误注入也保持有效：文件/索引/Git SHA/字节/配置/预算/Selector/Dataset错配不能进入可信结果。当前007注册仍绑定4输出/17文件；科学结果核验与人类接受保留各自边界。完整[真实观察与分批回执](evidence/core-rework-observations.json)记录检查点及复用理由。

现有设备文件已有连接、目录和解释器字段，但未声明实验进程的 CPU/CUDA 值。本次只在同一文件中增加明确的 `execution_device` 消费约定及示例。远端设备文件未修改，正式 runner 需在该文件声明实际值；没有用本地子进程冒充 SSH 或正式 GPU 观察。

### 旧路径与当前说明是否收敛 — PASS

`run.py` 不再有旧flat解析与专用target-direct调度分支，本轮进一步删除了 `--recipe` 分支和新的 `syncmate_stage.py`，注册直接调用普通配置路径。旧atomic stage、target-direct stage/selection/config/output脚本和无活跃消费者的manifest assembler/adapter删除；过时注册、424份生成YAML及活动引用同步退役。001合同、配置说明、受影响WorkItem owner链接和看板投影已更新。本轮再删除 `scripts/syncmate/syncmate_m1.py`、无当前消费者的 `OpenGUAdapter/ADAPTER` 以及七项仅验证旧 M1 支路的测试；旧“尚未批准替换”标记和活动引用清零。当前 `scripts/syncmate/syncmate.py` 仍是独立 Core 的有效项目入口，保留 `OpenGUProjectExtension`。上一轮745项仅为收集结果、205项为当时回归结果；本轮的有效验证单独列在下文。

旧入口与Cache V1私有API测试中失效的断言按[替换清单](evidence/retired-tests.json)退役；有效参数、数据split、AutoReport与缓存消费者检查保留。迁移中暴露的旧注册断言已更新到新注册，未通过恢复兼容层来让旧测试通过。文档检查120链接通过，其中13个DocMap链接以canonical项目位置解析；历史记录及归档材料不冒充现行运行说明。

## 保留的共享模块与入口映射

| 模块/入口 | 当前职责 |
|---|---|
| `experiments/run.py` | 普通配置dry-run、隔离CPU命令、已注册项目命令的同一入口 |
| `modular_config` / `modular_run` | 公共小表、两轴展开、真实Selection绑定、统一执行 |
| `syncmate_stage` / `OpenGUProjectExtension` | 正式位置/设备/数据/队列/输出契约政策；无第二套实验解析器 |
| `target_direct_v1/{methods,scoring,recipe,method_cache}` | 17种共享评分算法及方法级Score/Selection消费者；名称留在计算身份中 |
| `c_target_v1/{core,score_store}` | 已有张量计算、稳定排序和Score存储 |
| `modular_model` / `modular_gu` / `unlearning_outputs` | 训练、GU/Retrain独立输出和真实消费；未新增平行GU实现 |
| `modular_artifacts` / `opengu_method_output` | 同一已验证Output的便携导出与收集后读取 |
| `modular_evaluation` / `output_metrics` | 保存输出上的独立指标与配对比较 |
| `target_direct_v1/{split_profile,planetoid_io}` | 现有Dataset/Split工具与真实冷/热测试；本轮不运行正式数据准备 |
| `aagu015/definitions.py` | 只读审计普通表；旧generate命令已删除 |

GULib基础训练入口及历史证据读取功能保留其原职责，不构成另一套新实验格式。删除文件的精确清单见[入口退役](evidence/retired-code.json)。

## Verify、复跑与证据定位

当前软件检查点：`c40ee9dae7e63c3e921e221554fbc41fccabd27e`。本轮按受影响范围分批验证，最终覆盖 **257 项有效通过结果**，不是把失败运行整体标为通过：

| 证据范围 | 有效结果及检查点 |
|---|---|
| 新的 Core/设备行为、原消费者、Retrain/输出 | 44项，`c01f31dc`；包含全部7项新验收 |
| 完整 SyncMate、原24输出冷/热命令、Core依赖 | 193项，`18051bc4`；后续删除未调用helper和更正测试import不改变其实际路径 |
| 当前 adapter / 007、032 跨目录解析 | 10项，`c40ee9da`，整文件重跑通过 |
| 项目结果读取、正常回传及9类故障 | 10项，本轮真实Core临时运行；后续变化不改变该执行/收集路径 |
| 配置审计、Core smoke、依赖核验 | 均exit 0；46张活动YAML，015仍306 S / 612 U / 306独立Retrain |

[本轮证据](evidence/core-rework-observations.json)列出每个入选测试、JUnit SHA-256、源检查点、实际观察及复用理由。前序349项中的方法公式、配置迁移及其他未改动问题保留原检查点；不把它们报成本轮新运行。

验证过程的失败保留：示例配置曾按原始CRLF字节算hash，与Core的文本归一化规则不符，已修正；并行Torch检查曾耗尽Windows提交内存，已停止并改串行；清理旧快照测试时误删仍需使用的hashlib import，已恢复并重跑整文件。这些失败轮次不计作整体通过，详情见同一证据的 `attempts_not_counted`。

首轮历史验证：2026-09-06，在干净软件检查点 `380105002579c99ad003418648a85e67da413a0a` 执行：

| 检查 | 结果 |
|---|---|
| 18个相关测试文件 | 349 passed，0 failed，224.90s；2条依赖警告 |
| 公共配置/所有引用/逻辑展开/归档原文审计 | exit 0 |
| dashboard refresh --check | PASS |
| SyncMate smoke --json | passed=true，errors=[] |
| 全测试收集 | 750项，无import错误；不声称全部750项执行过 |

完整参数和退出码：[命令回执](evidence/verify-checkpoint.json)；逐测试结果、实测seed/轨迹、输出引用及原始JUnit SHA-256：[观察记录](evidence/observations.json)；[测试日志](evidence/pytest.log)。原始fixture独立保留在回执的临时路径，原始JUnit位于canonical `.workblock/runtime/aagu-034-verify/`。所有测试数据与Store均为隔离临时资产。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu007/experiment.yaml --dry_run
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu032/experiment.yaml --dry_run
& E:/conda_package/envs/gnn/python.exe -B -X utf8 -m experiments.aagu015.definitions check
& E:/conda_package/envs/gnn/python.exe -B -m pytest tests/test_unified_execution.py tests/test_syncmate_gu_outputs.py -q
```

真实临时命令形状为 `experiments/run.py <临时组合表> --device-config <临时device.yaml> --verification-root <临时绝对根> --run-id <新身份>`。新根和新run_id避免覆盖；pytest会建立所需的小图、manifest与参数表。正式项目命令为注册的 `experiments/run.py experiments/configs/aagu007/experiment.yaml --run-id aagu007-v1`，本报告不授权执行它。

当前待决定候选由[同一WorkItem](WORKITEM.md)的source branch干净HEAD唯一确定。报告/证据加入后对实际diff复核，复用上述检查点中未受影响的软件证据，并单独验证新增报告与状态投影；详见WorkItem Verify记录。

## 尚未观察与人类边界

**检查偏差与修复：** 补充检查中的一次仓库全域 `pytest --collect-only` 误导入 `tests/` 外有顶层执行副作用的旧 IM 基准脚本，触发了本地数据下载/处理和 CPU 计算；该进程已停止。随后明确限定 `pytest tests --collect-only`，745项收集通过。逐文件核对创建时间、路径、Git忽略状态和SHA-256后，移除了本次误操作新增的57个文件（40数据、11日志、6编译缓存），并验证均不存在；没有删除既有文件或历史证据。这次误操作及其产物不计入任何正式实验通过结论。详见[新增文件与清理核验](evidence/collection-side-effects.json)及命令回执的interrupted_checks。

**NOT OBSERVED：** SSH/GPU正式运行、正式数据上的训练与缓存命中、耗时/峰值显存、015完整矩阵、007科研gate及032科学方案验收。CiteSeer/PubMed真实资产绑定尚缺，015后续阶段的Selection/Output摘要引用待正式阶段完成后填写。Cora配置记录的manifest身份也须在真实checkout重验字节；本轮没有执行获准的正式数据准备流程；误触的本地生成文件已按上述清单移除。

本轮没有启动远端正式SSH/GPU作业、push、Apply、安装或历史缓存修复。软件支持范围仍是已有节点删除、GCN/SGC和GNNDelete/GIF/Retrain消费者，不能推导任意模型或遗忘方法已适配。当前目标是确认统一配置和执行修正是否完成，后续正式任务必须消费人类接受后的版本。

HTML呈现检查：**PASS**。已实际查看headless Edge的1440×1000桌面、390×844窄屏首屏以及正文/边界截图；首屏可见决定入口，标题、正文、表格和命令可读，无页面横向溢出、断图或页面错误。观察层是本地HTML渲染，不代表SSH/GPU运行。[桌面](evidence/report-desktop.png) · [窄屏](evidence/report-narrow.png) · [呈现测量](evidence/render-qa.json)。
