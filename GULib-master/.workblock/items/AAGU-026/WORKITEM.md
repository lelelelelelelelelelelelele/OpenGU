# AAGU-026 · FIX · 模块化实验配置与缓存身份隔离

Block ID: `AAGU-026`
Item Version: 2.1
Item Type: `Block`
当前状态: `registered / not claimed`
Stable locator: `.workblock/items/AAGU-026/WORKITEM.md`
Acceptance Route: `formal`
Execution topology: `sequential`
> Apply target ref：`refs/heads/main`

## Human Surface

### 核心意图

让已划分数据、Selector 和 Unlearning 各自拥有清楚的配置与缓存身份，同一份选点结果能够被不同实验和 GU 方法可靠复用。更换实验编号、GU 专属参数或无关的下游实现，不应让没有改变的选点计算误判为 MISS；某个 selector 的参数改变，也不应迫使无关 selector 一起重新计算。

### 本次增量

消费 AAGU-001 接受后的三层实验配置合同，在当前通用执行链和 target-direct 执行链中落实独立配置实例及明确引用：Dataset/Split 引用已经持久化的数据与划分，Selector 拥有方法、自己的模型与训练配置、方法专属参数和删除预算，Unlearning 拥有 GU 方法、自己的目标模型与训练配置及遗忘参数；实验大表只负责组合和执行终点，不隐式覆盖小表参数。

每个配置实例使用一个文件；同一方法的变体仅通过不同配置表表达，不新增变体机制或重复算法实现。修复当前训练型 selector 将 GU 参数及无关下游源码指纹纳入键的问题，将 target-direct 整包评分的共同身份拆为方法级身份；共同模型、轨迹或其他中间计算可以在依赖相同时共享，但不得再以整包共同键决定所有方法的 HIT/MISS。

保留统一 Cache V2 Store、默认缓存能力、精确身份和完整性校验。实验可以只完成 selector；另一实验可以直接消费匹配且已验证的 Selection Artifact 执行 GU。两侧模型分别声明，只有实际身份匹配才共享 checkpoint；不改变现有科研公式、节点删除语义或已批准矩阵。

### 核心验收

- 独立配置通过实际入口校验、解析并传到对应消费者；方法变体只需不同配置实例，不新增变体代码。实验可停在 selector，也能引用已有 Selection 进入 GU，且后一路径不调用选点 producer。
- 固定 selector 的真实输入，仅更换实验 ID/case ID、GU 学习率、GU 方法或无关的 GU 实现时，Selection 身份与选点 HIT 保持不变；GU 结果身份按自身有效配置正确变化。改变 selector 实际依赖的数据、模型、方法参数或实现时，正确 MISS 或拒绝不匹配输入。
- 改变 B-Hutch 等单个方法的专属参数，只改变该方法及其真实下游的身份，无关 degree、TracIn 等方法仍可命中；共同中间依赖变化只传播给真实消费者。
- 删除预算属于 Selector 输入，最终 Selection 绑定实际 K 与选择规则；仅在明确预算无关、前缀稳定的评分合同下复用 Score。规范化等价配置不因 YAML 排版、文件名、路径或实验归属改变而误 MISS。
- 人工小表允许省略方法/OpenGU 已声明的默认值；按 method 选择实现与字段规则，展开后的有效配置和真实依赖用于身份。省略默认值与显式填写同值必须 HIT 等价；改变实际被消费的默认值或相关实现则正确失效。共享实现不导致不同方法的参数或缓存身份混在一起。
- 用户能够通过真实 CPU 消费者的 cold/warm、跨实验复用、负向身份测试和配对报告判断上述结果；测试或 dry-run 不冒充正式 GPU 实验，也不自动接受本 Block。

## Confirmed acceptance contract

- Route: `formal`.
- Primary surface: `configuration / cache identity / integration`.
- Decision owner: 用户。
- Minimum real evidence: 临时目录内的真实 CPU 小图与模型消费者运行；配置到参数到 Recipe 的映射；独立 selector 的 cold/warm 与变更影响矩阵；从已有 Selection 进入 GU 且 producer 未调用的证据；必要的源码指纹边界检查；历史缓存保护检查。身份探针只能证明键变化，不能独自代替真实消费者的缓存验证。
- Report size: 配对 `REPORT.md` / `REPORT.html`，在同一 WorkItem 目录形成；登记阶段不创建空报告或伪造完成证据。
- Post-candidate decision: Verify 后由用户明确接受、返工或拒绝；保持在人类验收边界，不能自行 Apply、push 或部署。

## Source and relations

- Source anchor: 本次 AAGU-001 参数共识讨论，以及对 `main@1ad0a6c417c3a1de9bf02c398f0cfcdaa167c7e3` 的只读架构审查。
- 现有定位：[训练型 selector 的键组装](../../../attack/attack_manager.py)、[通用目标参数集合](../../../attack/cache_identity.py)、[target-direct ScoreBundle Recipe](../../../experiments/target_direct_v1/recipe.py)、[独立 Selection 到 GU 接口](../../../experiments/target_direct_v1/adapter.py)。执行前重新核对当前代码，不把注册时定位当成已修复结果。
- 已观察反例：同一 CPU fixture 中仅将 `unlearn_lr` 从 0.01 改为 0.02，TracIn Selection Recipe hash 改变；实验 ID/case ID 和 GU 方法名变化未改变该键。原审查的 26 项检查通过不覆盖这一修复的完成验收。
- 已观察边界：当前 target-direct 同一个 ScoreBundle 绑定 17 种评分及共同 Hessian/轨迹配置；正式配置和消费者仍绑定 GCN、GNNDelete 与 last_layer，不能称为已经完成自由组合的通用三层框架。
- Fact owner: [本 WorkItem](WORKITEM.md) 拥有实现与验收范围；[AAGU-001](../AAGU-001/WORKITEM.md) 拥有接受后的参数与配置合同。
- Confirmed relation: `AAGU-026 depends_on AAGU-001`。001 可以独立完成合同，不反向依赖本实现；本 Block 在 001 的合同被接受后执行。
- Reuse context: 沿用 [AAGU-025](../AAGU-025/WORKITEM.md) 已接受的统一 Cache V2 基础；不重开其历史验收或另建 Legacy/V2 切换。
- Graph placement: `repair`。未另行指定优先级，不推断为 P0。
- Blueprint scope: 已划分数据输入、实验配置、Selector/Score/Selection 和 GU 消费边界；不虚构未登记的 Blueprint 节点。

## Scope and safety boundaries

- 实现只覆盖上述配置、身份与复用边界及其必要消费者和测试，不增加新 selector/GU 算法、改变 IF/GIF 公式或替 AAGU-015 选择最终科研方案。
- 配置实例的有效计算字段、producer 语义版本和实际依赖形成键；全局实验编号、展示字段、配置文件原文或整张大表不得直接成为小模块身份。下游 GU 引用 Selection，依赖关系不是反向的参数污染。
- 新计算条件产生新的请求身份；旧 Artifact 仍可服务其原合同，不自动删除、覆写、迁移、重标为损坏或放宽旧证据的接纳条件。`results/cache_v2` 与历史实验产物禁止手工修改。
- 保留一个统一 Store 和正常缓存默认值。移除被替代的活动耦合路径，不增加兼容层、隐藏回退、复杂配置继承或深层隐式 override。
- 已划分数据在消费阶段只读解析与校验；缺失输入应按已有数据准备授权边界停止，不因配置加载而自动下载或重切。
- 本次仅登记。未 Claim、未实现、未运行正式 GPU、未创建后续 Codex task、未执行 SSH 写入、push、install、Apply 或清理。

## Restart and next action

先确认 AAGU-001 已接受并读取其最新合同。后续使用 `block-workflow` Claim 这个精确 locator，在主检出的独立功能分支中实施已确认范围；用隔离 CPU 输入和临时 Store 验证，不触碰历史产物。形成精确候选与配对报告后停在 `formal` 人类决定边界。

## Status history

- 2026-09-04: 用户再次要求登记 commit 到 main；原登记已在 main@8383e30239398c5268965e088afdfba7abc74ca9。本次补充人工表省略默认值、方法分发和默认值等价命中的验收要求；继续 registered / not claimed，不执行实现。

- 2026-09-04: 用户要求确定实验配置并创建 Block，在完整登记预览后确认方法变体仅需不同配置表；登记本独立 FIX，状态为 `registered / not claimed`。AAGU-001 保留原编号与公共合同职责，具体实现移交本 Block。
