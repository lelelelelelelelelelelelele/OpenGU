# 实验合同：组合大表与三块独立参数表

本规范由 [AAGU-001](../../.workblock/items/AAGU-001/WORKITEM.md) 提供，供科研负责人审阅。它规定实验如何定义、注册和追溯；[AAGU-026](../../.workblock/items/AAGU-026/WORKITEM.md) 才负责把当前运行代码改成这套接口。本文及示例不是已经部署的新 launcher，也不批准新的正式实验。

阅读顺序：本页（规则）→ [真实参数表](PARAMETERS.md)（当前值、来源、可改项）→ [实例文件](examples/)（具体填写）→ [001 验收入口](../../.workblock/items/AAGU-001/WORKITEM.md)。任务状态与优先级只看 [WORKPLAN](../../self/dashboard/WORKPLAN.md)。

## 1. 一张大表、三类小表

| 表 | 回答的问题 | 自己拥有的字段 | 输出/依赖 |
|---|---|---|---|
| Dataset/Split | 用哪一份已经划分的数据？ | 数据内容/版本、预处理、已持久化 split 引用与身份；划分生成信息 | 图、特征、标签、train/validation/test mask；不执行重切分 |
| Selector | 按什么模型和方法删哪些点？ | 方法、候选集合、预算、选取规则、随机种子；方法实际需要的模型/训练、参数范围、求解或轨迹配置 | 独立 Score（若适用）和带节点编号的 Selection |
| Unlearning | 对这份删除请求怎样遗忘？ | GU 方法、目标模型/训练、遗忘超参数、随机性 | 消费 Dataset/Split 和已验证 Selection；输出模型及结果证据 |
| 实验组合大表 | 这一轮研究什么，组合哪些实例，做到哪一步？ | 问题、对照、轮次、模块引用、矩阵、执行终点、评价和接纳约定 | 引用上述小表及运行记录；不覆盖小表，不成为小模块缓存键 |

三块是参数职责，不是强制执行三次任务。一次实验可以只到 Selector；另一实验可以直接拿已有 Selection 做 GU，完全不调用 Selector producer。Score、checkpoint、轨迹是模块内部可复用的产物，不再增加“第四张业务配置表”。

一轮科研合同可以描述一个矩阵；cell 是组合展开的一行，不为每个 cell 重写合同。设计定义在运行前固定；执行记录、结果分析另存，下一轮引用上一轮证据，不改写上一轮设计。

## 2. 字段和有效值规则

每个配置实例一个独立文件，同一方法的变体就是不同配置表。两个文件的规范化有效计算内容相同，则计算身份相同；仅命名不同不构成新计算。这里的字段名是待实现接口的合同示例，不是假称当前 CLI 已支持。

### 2.1 所有实例的公共约定

- `kind` 和 `schema_version`：必填，标明表类别和结构；不能混用科研轮次、算法版本、Artifact 版本。
- 方法配置必须明确 `method`；只有已注册实现及其声明的字段才能执行。新增算法不是“写一个 YAML 就自动获得实现”。
- 方法注册负责声明字段类型、必填项、有效默认值、允许范围、真实依赖和 producer 语义版本。026 落实校验；001 不增加新的运行时注册框架。
- 缺失必填项、未知字段、非有限数、越界值、冲突配置都拒绝；不能悄悄丢弃拼错参数。适用的默认值先展开再求身份；`0.01` 与 `1e-2` 这类等价值规范化一致。
- 无隐式继承、无大表 override、无 YAML merge。为了改一个参数，复制一份完整小表并改该值即可；比较工具展示差异，不需要重复算法实现。
- 参数和依赖内容决定键，名称、注释、文件路径、实验/case ID 只作定位与追踪。文件指向的实际内容变化则必须影响其真实消费者。

### 2.2 Dataset/Split 表

| 字段组 | 要求 |
|---|---|
| `dataset` | 非空名称；实际 source/version 或内容 fingerprint；不能只凭 Cora 名字确定图 |
| `preprocessing` | 可追溯 recipe/version 或内容身份，说明图构造/特征变换 |
| `split` | 已划分资产的 locator、split hash、节点空间；已固定的生成方法、比例、split seed |
| `artifacts` | 已验证图/标签/特征/划分 manifest 的引用及摘要；缺失时不能继续正式执行 |

消费者只读资产并检查实际 mask、图内容、节点空间及哈希。改变 model seed 不重新 split；改变 split 合同需要先由获准的数据准备流程生成另一份资产，不覆盖已有资产。不把 `materialize_on_miss` 当作每次配置解析的写入授权。

### 2.3 Selector 表

| 字段组 | 类型/约束与用途 |
|---|---|
| `method` | 一个已注册 selector 标识；如 degree、b_param_hutch |
| `candidate` | 候选池定义与实际有序节点身份；默认不能从“全节点”猜成“训练节点” |
| `budget` | 比例模式或绝对 K 模式二选一；比例在 (0,1]，K 为正整数且不超过候选数；比例模式必须声明分母与取整规则 |
| `selection_rule` | 排序方向、tie-break、去重/采样规则；结果记录实际 K 和明确节点序列 |
| `model` / `training` | 仅模型型 selector 必填；结构、训练配置、seed；实际依赖的 checkpoint 内容身份由运行记录绑定 |
| `parameters` | 每个方法自己的表；IF 的求导范围、目标集合、loss、LiSSA/Hutch 配置或 TracIn 的快照集合/权重等 |
| `numerics` | 方法真正依赖的 dtype、后端或确定性约定；不得机械复制整个设备环境 |

预算属于 Selector，不是 GU 的第二套独立预算。Selection 记录输入候选身份、预算请求及实际 K、节点空间、选中节点、producer 和真实依赖；GU 只消费并核验，不重新抽样、不从 ratio 重算另一套节点。

`Score` 与 `Selection` 分开：预算无关且前缀稳定的分数/排序可以被多个 K 复用；最终 Selection 仍由预算和规则确定。预算影响评分或自适应选点的方法必须把预算纳入相应上游键。不能默认所有方法都可取排序前 K 个。

### 2.4 Unlearning 表

| 字段组 | 类型/约束与用途 |
|---|---|
| `method` | 一个已注册 GU 方法标识 |
| `model` / `training` | 目标模型独立声明；包括结构、训练 seed/优化器/轮数和实际初始 checkpoint 依赖 |
| `parameters` | GU 自身的 lr、遗忘轮数、损失等；各方法只接收自己消费的字段 |
| `selection_input` | 由大表引用已验证 Selection，或引用前一阶段的输出；执行前必须解析为精确 Artifact 身份 |

Selector 模型和 GU 模型互不覆盖。Selector=SGC、GU=GCN 是允许的组合设计，但当前 formal-v2 入口仍固定 GCN/GNNDelete，不能直接执行该组合。若两边都用 GCN，两边配置与实际 checkpoint 身份匹配时自然共享；仅“两层 GCN”或一个布尔共享标记不够。

GU 结果键依赖其实际 Selection 输入及目标模型/方法参数；改变 GU 参数不反向改变 Selector 键。若 GU 只消费选中节点而不消费原始分数/轨迹，就不得把未消费的评分内容当作计算输入；仍需保留完整 provenance 链。

### 2.5 实验组合大表与运行记录

| 大表必填组 | 具体信息 |
|---|---|
| 研究合同 | 问题、轮次、假设/对照、主要指标、预先声明的可接纳/不可支持结论、负责人和批准记录 |
| 模块引用 | 一个 Dataset/Split；Selector 配置实例集合或已有 Selection 输入（二选一）；执行到 GU 时指定 GU 实例集合 |
| 展开规则 | 明确 Cartesian product 或列举具体行；不把展示顺序当作缓存依赖；每行引用解析后的小表 |
| 执行终点 | `selector` 或 `unlearning`；前者不需要 GU 参数，后者可以从已有 Selection 开始 |
| 执行绑定 | 已注册 launcher/static recipe ID、配置摘要、代码版本、运行等级、资源/数据授权、预期产物和校验流程 |

每次运行单独记录 experiment/case/run/job ID、实际展开配置摘要、代码 SHA、Dataset/Split/候选/checkpoint/Selection/结果身份、执行地点、起止时间、HIT/MISS 与 producer 调用、失败或恢复记录、收集校验回执和最终科学接纳决定。未知身份写“未观察”，不能填伪造哈希。全局代码 SHA 是复现/正式运行门禁，不应无条件代替局部 producer 的缓存身份。

## 3. 缓存变更影响合同

以下是目标规则，须由 026 的真实消费者测试证明；本页不是修复完成报告。HIT 的前提是旧产物确实存在且完整性/精确身份校验通过。

| 只改变这一项 | 不应受影响 | 应改变/重新核验 |
|---|---|---|
| experiment/case ID、文件名、注释 | 全部未改变的计算 | 运行追踪元数据 |
| GNNDelete `unlearn_lr`、遗忘轮数、GU 方法 | Dataset/Split、各 Selector/Score/Selection | GU 及其结果消费者 |
| B-Hutch `probes: 32 → 64` | degree、random、TracIn；相同基础训练 | B-Hutch Score/Selection 及实际消费变化输入的 GU |
| LiSSA 迭代数/scale/damp | 不使用 IHVP 的方法 | r_point、gt_simple、gt_full、B-Hutch 等实际求解消费者 |
| TracIn cp3 → cp_all | 相同训练/轨迹资产、非轨迹方法 | 对应 TracIn 分数与 Selection；不是所有方法整包失效 |
| ratio 1% → 5% | 明确预算无关的 Score 和基础训练 | Selection 的实际 K/节点，依赖其结果的 GU |
| Selector 模型/训练 seed | Dataset/Split；无需模型的 selector | 实际使用该模型的评分/选点；若两边明确共享该模型，GU 也消费新 checkpoint |
| GU 模型变化而 Selector 模型不变 | 已有选点计算 | GU 模型及下游结果 |
| 实际 split/候选/数据变化 | 仅不消费这些输入的产物 | 所有真实消费者；不允许读取同名旧资产冒充 |
| 无关 GU 源码变化 | Selector | 对应 GU producer；共享实现真正变化时才影响共享消费者 |

缓存 MISS 表示新请求条件，不表示旧缓存损坏。保留旧 Artifact 对原合同的复用；禁止手工修改、删除或改名 Cache V2 产物。库里已有 17 种评分一起计算，不妨碍内部复用共同计算，但不能继续以整包键决定每个方法的命中。

## 4. 注册、执行和接纳是三个决定

1. 定义并审阅本轮大表/小表，区分已知值、研究变量与待定选择；注册使计划可定位，不等于 GPU 授权。
2. 查明真实消费者：通用矩阵用 `experiments/run.py`；formal-v2 由 `target_direct_v1.syncmate_stage` 及已注册 SyncMate recipe 消费，不能混用入口。
3. 本地执行相邻检查。通用 `--dry_run` 仅展开/检查；formal Selection 无 dry-run 参数。GU dry-run 依赖真实 manifest/Selection，不能为通过检查捏造这些资产。
4. 正式运行前须满足项目指令规定的代码/设备/数据/产物 gate，并有本轮科学与资源授权；本地检查通过不替代它。
5. 运行后保留 job/receipt、原始产物、摘要与依赖链；按项目收集与 SHA-256 核验流程进入 trusted index，再由科研负责人接纳结论。进程成功、SyncMate done、测试 PASS 都不是科学验收。

SyncMate 只负责已审阅静态 recipe 的执行连接、回执、收集和校验，不选择 IF 定义、不批准矩阵、不判断科研结果。其本地 `sync --dry-run` 仍可联系 peer 并保存同步状态，因此不是本合同的纯本地参数 dry-run。

## 5. 已有实验的完整填写与示例边界

### 5.1 当前 formal-v2 合同投影

- 问题：在精确共享目标 checkpoint 的白盒设定下，比较已注册删除评分/选点；不把 canary 的基础设施验证解释为完整论文比较结论。
- 数据：Cora/CiteSeer/PubMed；已注册 70/10/20、split seed 2024；实际资产身份必须来自持久化 manifest，本次未读取远端资产。
- 配置：模型 GCN 两层、hidden 64、训练 100 轮；各模型 seed 为 42/212/2024；Selector 预算 1%/5%；17 种评分；GU=GNNDelete；方法细节见真实参数表。
- 矩阵：3 datasets × 3 seeds × 17 selectors × 2 ratios × 1 GU = 306 个候选 cell；现有配置明确 `candidate_full_matrix_authorized: false`。canary gate 为 2 个 cell，不能借本规范扩大执行授权。
- 入口：Selection recipe `opengu-target-direct-selection-cora-seed42-v2`（其他阶段按注册表）；GU gate 为 `opengu-target-direct-gu-gate-r001-v2` / `...-r005-v2`。精确定义以 [opengu_recipes.py](../../scripts/syncmate/opengu_recipes.py) 为准，不在这里派发。
- 接纳：预算/候选/split/checkpoint/manifest 精确一致；预期产物完整且 checksum 核验；科学结果仍由本轮负责人判断。

### 5.2 已有 sanity 实验的本地 dry-run

[sanity_one_cell.yaml](../../experiments/configs/sanity_one_cell.yaml) 已定义 Cora/GCN、GIF、random、seed 42、ratio 0.05 的一个 cell。它没有显式 split/Artifact 绑定，故只作为现有注册入口可用性示例，不是满足新合同全部要求的正式实验。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/sanity_one_cell.yaml --dry_run
```

预期 `total cells: 1`，无完成训练/遗忘计数；是否 `would_run` 或已存在而跳过取决于本地旧产物状态。本次具体观测见 001 evidence。既不改原配置、补 split，也不加 `--force` 或执行命令中建议的清理操作。

### 5.3 三类小表实例

[examples](examples/) 使用 `schema_version: 1` 的文档示例语法，均非当前 launcher 输入；所有组合大表显式 `execution_authorized: false`，实际资产引用为 null，执行前必须补齐并验证。缺失资产不影响审阅配置差异，却必须阻止真实运行。

- `selector_b_hutch32.yaml` 与 `selector_b_hutch64.yaml` 只差采样数：同一方法两个配置表。
- `unlearning_gnndelete.yaml` 与 `unlearning_gnndelete_lr002.yaml` 只差 GU 学习率，不能影响选点身份。
- `experiment_selector_only.yaml` 只到 selector，不需要 GU 表。
- `experiment_gu_from_selection.yaml` 从已验证 Selection 进入 GU，不包含 Selector 配置，也不能调用其 producer。
- 跨模型扩展只需分别声明两侧模型配置；例如 Selector 表改为已支持的 SGC 结构/训练配置，GU 仍为 GCN。当前 formal-v2 不支持自由切换，此组合需 026 验证后另行注册，不自动从 GCN YAML 继承其他模型的参数。

## 6. 001 与后续工作的边界

001 可独立验收的内容是这份规则、真实参数来源和可审阅实例，以及现有入口检查。它不修复缓存键、不新增 parser、不更改公式、不修改 formal-v2 YAML、不决定 AAGU-015 的最终 IF 方案。

026 的验收须证明真实 cold/warm/跨实验复用、单参数影响矩阵及 producer 未调用；任何文档检查或模型哈希玩具例子都不能替代它。接受 001 仅接受这份公共合同，不接受 026、不批准所有未来变量组合。
