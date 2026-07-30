# experiments/ Agent Guide

> 本文件提供 `experiments/` 的目录级架构心智模型与行动导航；根 `AGENTS.md` 继续提供项目定位、总体执行链与仓库级边界。

## 1. 目录使命

`experiments/` 把研究意图组织为可运行单元，并把执行连接到可追溯证据；它编排图遗忘、攻击策略和 Cache V2，而不拥有这些模块的内部实现。
目录包含通用 `run.py + YAML` 矩阵、跨实验复用的 Selection/Artifact 证据接缝，以及拥有独立 recipe、runner、gate、adapter 或 aggregate 的专题包。
`configs/` 是配置容器，不表示所有 YAML 都由同一个入口消费。

## 2. 按需加载实验上下文

根级上下文及其信息入口已经生效，不在本文件重复。

- 需要确认当前注册、准备状态或阻塞项时，只读取 WORKPLAN 中与目标实验相关的条目及其计划链接。
- 准备正式启动或收集结果时，只读取[实验运行入口与脚本](../文档规划/10_实验矩阵/15_实验运行入口与脚本.md)中当前 launcher 对应的部分。
- 出现失败、恢复、重跑或缓存问题时，只读取 repair Runbook 的相关部分。
- 仅做源码阅读或局部测试时，不加载正式运行和修复材料；dry-run 或 disposable smoke 只加载当前配置与 launcher 所需的相邻验证材料，不加载失败恢复材料。

不要预先加载全部实验文档，也不要把实时状态复制进本文件。

## 3. 先判断实验是否已经定型

先从当前研究意图与实时任务的权威来源确认目标，不在本目录复制其当前状态。

- **已定型实验**：若已有注册计划、配置或 versioned Recipe、明确消费者、launcher 和 acceptance gate，则沿用既有 setup；先确认版本、阶段并运行相邻验证，不重新选择数据、划分、种子、预算、路径或临时改写 launcher。
- **临时或新实验**：没有已确认定义时，先声明问题、对照、变量、矩阵、指标、证据和结论边界；完成注册、身份绑定和正式 gate 前，只属于探索或验证。
- **稳定 ID**：可作为注册计划的导航别名，但不能替代配置、Git、数据和 Artifact 身份。

只有当前研究意图改变 claim、数据或划分、方法语义、核心指标或矩阵范围时，才建立新的实验定义；配置存在不等于它仍是当前注册实验。

## 4. 找到正确的配置消费者

- 含 `dataset`、`base_model`、`ratio`、`methods`、`strategies`、`seeds` 的配置通常属于 `run.py` 矩阵。
- 含 `schema`、`version`、`recipe_id`、阶段定义或多数据集结构的配置通常由对应专题包解析。
- 不根据文件名猜入口；先查找哪个模块加载、校验或绑定该配置。

专题包常按 `recipe → core → runner/stage → manifest/adapter → aggregate/render` 分层；先读 recipe 和 runner，aggregate 和报告只是已有事实的投影。
**SyncMate 执行通道**：部分已注册实验从 `scripts/syncmate/syncmate.py` 及专题 `syncmate_*` recipe/stage 进入，由它把已审阅配置、阶段和预期完整 Git SHA 绑定到 SSH runner，并支持状态、回执和 Artifact 收集。
SyncMate 不定义研究 claim 或矩阵，也不替代共享 stage check、专题 preflight 和 acceptance gate。
注册计划指定 SyncMate 时不得改写成临时 SSH 命令或 `run.py`；未指定时也不自行切换，具体操作使用当前注册计划的命令。

### 最小执行导航

通用矩阵在本地先用 `E:/conda_package/envs/gnn/python.exe experiments/run.py <registered-config.yaml> --dry_run` 验证定义；正式执行只使用注册计划指定的 launcher。
注册计划指定 SyncMate 时使用对应 recipe/stage，不把它临时改写为裸 SSH 命令或通用 `run.py` 调用。

## 5. 通用矩阵与证据接缝

一个 `run.py` YAML 固定数据集、模型和删除比例，并展开 `methods × strategies × seeds`。
`YAML → Selection 计划或 Artifact → demo_attack.py → 可选 collateral 评估 → metadata 与审计事件`
默认 cell 位于 `run_root/{dataset}_{model}_r{ratio}/{method}_{strategy}/seed{seed}/`，完整叶子通常包括 `attack.json`、`collateral.json`、`predictions.npz` 和 `_meta.json`。
完整性还要求内容可解析、目标策略存在和配置指纹匹配；`--dry_run` 只展开并验证计划，不代表已经执行。

正式启动前先检查目标 run identity 和已有 cell 状态。不得为了继续运行而自行使用 `--force`，也不得手动删除、移动或覆盖已有正式产物；发现 complete、partial、stale、corrupt 或身份冲突时停止，按 repair Runbook 判断恢复、重跑或建立新结果身份。

Selection 输入必须来自持久化图、划分和候选集合；多预算前缀复用只适用于显式 prefix-stable 的排序；正式 Artifact 只在验证后的精确 MISS 上调用 producer，身份或依赖不清楚时 fail closed。

### SSH 正式数据固定位置

SSH 上正式数据的默认且固定根目录是 `/autodl-fs/data/OpenGU/GULib-master/data/processed`。正式实验读取的数据，以及获准执行的数据准备操作所写入的正式 dataset 内容，都必须解析到该目录下。
“获准的数据准备”仅指当前注册计划或独立数据准备任务明确授权的操作，不由执行 agent 因数据缺失而自行推断。
只使用其中 `transductive/`、`inductive/` 的 OpenGU canonical graph/split pair 或已注册 `processed_profile`；不得直接使用 PyG `processed/data.pt`、临时重建 split/candidate set，或把其他数据通道改名为 OpenGU processed split。
不得在当前工作目录、其他 checkout、工具默认缓存或临时路径中新建 dataset 内容。执行任何可能写入数据的操作前先核对最终目标；目标不是上述目录、所需 artifact 缺失或身份不清楚时立即停止，不得自动下载、搜索同名副本或切换路径。该目录之外的同名数据不得作为正式输入，也不得自动修补或删除。

## 6. 实验等级与递进验证流程

`探索 / 验证 / 正式` 描述结果能支持什么结论；`test / dry-run / smoke / gate / matrix` 描述怎样执行，二者不能混为一类。

- **探索**：快速缩小问题或检验现象；输出只作为线索。
- **验证**：检查配置、契约或真实执行链是否正确；不证明研究假设。
- **正式实验**：使用已注册定义和正式身份生成可进入研究结论的证据。

递进流程固化为：`targeted tests → dry-run → disposable smoke → registered minimal gate → full matrix → collection/acceptance`。
Smoke 用最小数据或 cell 跑通真实 lane，暴露依赖、路径、参数传播和 Artifact 生产问题；它是可丢弃的 pre-gate 验证，不是正式证据。
Minimal gate 必须在正式 SSH 环境代表真实 lane，并与后续扩展保持相同代码、配置或 Recipe、数据与划分、缓存语义、输出身份和 acceptance logic。
任一步失败都停止向后推进；已接受 gate 在完整身份未失效时可以复用，不因开始新会话或重复检查而强制重跑。

## 7. 正式运行版本一致性与 SSH 边界

本地用于代码与配置修改、CPU 测试、dry-run 和结果审阅；正式 GPU gate、矩阵、正式数据及运行态位于 SSH 活跃检出。正式执行前，所有相关工作先审阅并接受进 `main`，并确认 `本地 main = origin/main = SSH 活跃检出 main = 同一已记录的完整 Git SHA`。
本地与 SSH tracked tree 必须干净，SSH 只使用唯一正式活跃检出。
该要求只保证一次正式运行的代码与配置一致；它不是 cache key，也不要求清空缓存。
Cache 命中仍由 Recipe、producer、数据、候选集合和依赖 Artifact 身份决定：语义身份未变时可跨无关提交精确复用，生产语义或输入身份变化时必须形成新 Recipe、MISS 或 fail-closed；专题显式绑定 Git SHA 时服从其契约。

SSH 正式启动分两层：

1. **共享 stage check**：三方 `main` 与完整 SHA 一致、tracked tree 干净、活跃检出正确、GPU 可用、运行路径归属明确；
2. **实验专属 preflight**：配置或 Recipe、数据与划分、manifest、设备要求、已有产物和恢复条件符合本实验定义。

正式 GPU gate 或 matrix 必须枚举到至少一张 GPU；GPU 不可用时立即停止，禁止自动降级到 CPU。

两层通过后才使用已注册 launcher；任一条件不满足时先恢复版本或身份边界，不启动正式实验。

## 8. 证据闭环

进程成功退出不等于可信证据；需核对 Artifact 完整可解析，metadata 的 Git SHA、配置指纹和运行身份一致，并验证 Selection、manifest 与依赖链。远端产物完成收集与核验后才进入本地结论；交接时分别说明执行、验证、可支持结论和未知项。
正式运行暴露代码、配置、数据、指标、缓存或 provenance 缺陷时，立即停止受影响矩阵并将相关证据标为未验证；后续失效范围、修复、重跑与恢复遵循[重跑与缓存修复 Runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md)，在其重新建立可信身份前不恢复矩阵或混用受影响产物。
