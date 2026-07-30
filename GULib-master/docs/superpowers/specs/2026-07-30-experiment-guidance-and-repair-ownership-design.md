# Experiment Guidance And Repair Ownership Design

## 目标

收敛实验入口、运行环境、正式 GPU 边界、修复操作和历史验收记录的
信息所有权，使每条稳定事实只有一个真源，同时保持现有 Obsidian 链接和
代码侧导航可用。

本设计只调整文档职责和路由，不改变实验实现、当前注册计划、数据、
Cache、结果或运行状态。

## 设计原则

- 根 `AGENTS.md` 只保留仓库级定位、总体执行链和职责路由，不保存
  `run.py`、SyncMate、解释器路径或具体 dry-run 命令。
- `experiments/AGENTS.md` 是实验入口、执行层级、正式 SSH/GPU 边界和
  数据根策略的唯一目录级真源。
- 操作规范、历史验收台账和兼容入口分离；导航文件不复制操作步骤，
  台账不重新定义修复协议。
- 当前正式数据策略保持不变：正式输入和获准准备出的 dataset 内容统一
  materialize 到 SSH 活跃检出的规范 `data/processed` 根目录。
- 实时实验状态继续只由 `self/dashboard/WORKPLAN.md` 和注册计划拥有。

## 文件职责

| 文件 | 唯一职责 | 不再承载 |
|---|---|---|
| `AGENTS.md` | 仓库级定位、总体执行链、实验目录职责路由 | `run.py`、解释器路径、具体 dry-run/launcher 规则 |
| `experiments/AGENTS.md` | 通用矩阵与专题 launcher 导航、本地验证命令、正式 SSH/GPU 和数据边界 | 修复步骤、历史修复结论 |
| `文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md` | 兼容既有 Obsidian 链接的简短导航页 | 操作细节、历史台账正文 |
| `文档规划/10_实验矩阵/13A_OpenGU_Cache与结果修复操作规范.md` | OpenGU 修复、隔离、重跑、回收和重新验收的唯一操作真源 | 当前任务状态、历史方法结论 |
| `文档规划/10_实验矩阵/13B_修复验收与回归台账.md` | GraphRevoker、TracIn 等修复结论、测试、失效范围和归档边界 | 通用修复操作步骤 |
| `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md` | 代码目录中的兼容跳转页 | 独立操作规范副本 |

## 根级与实验目录级入口

根 `AGENTS.md` 删除两类具体事实：

1. `experiments/run.py + YAML` 是正式入口；
2. 本地 Python 是 `E:/conda_package/envs/gnn/python.exe`。

根级执行链改为从“已注册实验定义与 launcher”进入配置、数据、模型、
遗忘、攻击和证据链，并把入口选择与运行细节明确路由到
`experiments/AGENTS.md`。

`experiments/AGENTS.md` 独占以下事实：

- `experiments/run.py + YAML` 是通用矩阵入口，而不是所有正式实验的
  唯一入口；
- 专题实验使用注册计划指定的 runner、stage 或 SyncMate recipe；
- 本地通用矩阵 dry-run 使用
  `E:/conda_package/envs/gnn/python.exe`；
- 通用矩阵 dry-run 只读取运行入口文档中对应的配置和 launcher 小节；
- 纯源码阅读和局部测试不加载正式运行或修复材料；
- 失败、恢复、重跑或身份冲突才加载修复操作规范。

## 正式 GPU 与数据边界

`experiments/AGENTS.md` 在共享 stage check 后明确：

> 正式 GPU gate 或 matrix 必须枚举到至少一张 GPU；GPU 不可用时立即
> 停止，禁止自动降级到 CPU。

本规则只约束正式 GPU 运行，不禁止经任务明确声明的本地 CPU 分析、
局部测试或 disposable smoke。

新版数据策略保持为唯一有效策略：正式实验读取的数据，以及获准准备
生成的正式 dataset 内容，都解析到 SSH 活跃检出的规范
`data/processed` 根目录。旧版把 public raw/PyG 直接列作正式输入通道的
表述不恢复。

## 修复文档迁移

### Obsidian 兼容入口

现有 `13_重跑与缓存修复Runbook.md` 被 12 个 Markdown 文件引用，不能
直接删除。它改为不超过一个屏幕的导航页，只回答：

- 当前任务和阻塞看 `WORKPLAN.md`；
- 修复、隔离、重跑和重新验收操作看 `13A`；
- 历史修复结论、失效数据和归档边界看 `13B`。

### 操作真源

把 `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md` 的实质内容迁移到
Obsidian vault 内的 `13A`，并新增“正式身份重启不变量”小节。该小节统一
覆盖修复版本接受、运行与缓存身份替换、registered gate 重新验收和旧新
证据隔离；规范性措辞只写在 `13A`，本设计不形成第二份操作规则。

上述完整规则只在 `13A` 出现。`experiments/AGENTS.md` 只保留“停止并路由
到 `13A`”的行为边界。

### 历史验收真源

把当前 `13_...` 的 GraphRevoker、TracIn、Hybrid、状态定义、测试证据和
失效范围迁移到 `13B`。其中与通用操作重复的流程改为链接 `13A`，不在
台账内保留第二套修复协议。

代码侧原 Runbook 文件改为短跳转页，说明真源已经迁入 `13A`。SyncMate
README 和目录指导直接链接 `13A`；保留旧路径仅用于兼容外部引用。

## 迁移顺序

1. 从当前 `13_...` 提取历史台账到 `13B`，确认结论和失效范围无丢失。
2. 将代码侧 OpenGU repair Runbook 迁入 `13A`，合并必要的通用修复流程
   和正式身份重启不变量。
3. 把原 `13_...` 改成 Obsidian 导航页，把代码侧 Runbook 改成兼容跳转页。
4. 按用途更新文档地图、实验入口、Cache 分层、SyncMate README 和
   `experiments/AGENTS.md` 的链接。
5. 从根 `AGENTS.md` 移除具体入口和解释器事实，在
   `experiments/AGENTS.md` 完成唯一落点。
6. 补入正式 GPU 禁止 CPU fallback，保持新版 `data/processed` 策略。

## 验证

- 根 `AGENTS.md` 不再包含 `experiments/run.py`、
  `E:/conda_package/envs/gnn/python.exe` 或具体 launcher 命令。
- `experiments/AGENTS.md` 对通用入口、专题入口、本地 dry-run 和正式
  GPU 边界各有一个明确落点，且不与根级规则冲突。
- `13_...` 的现有入链继续解析，并能在 Obsidian vault 内到达 `13A`
  和 `13B`。
- `13A` 是唯一完整修复协议；`13B` 是唯一历史验收台账；代码侧旧路径
  只包含迁移说明和链接。
- 所有新增或修改的 Markdown 相对链接存在，文档地图能到达新的真源。
- 在实时操作文档中搜索正式身份重启规则时，完整规范性定义只出现在
  `13A`；历史设计说明不作为运行输入。
- Git diff 不包含实验代码、配置、Cache、结果、WORKPLAN 实时状态或
  无关 dirty 文件。

## 非目标

- 修改任何实验矩阵、注册计划、Recipe、runner 或 SyncMate 实现。
- 运行、恢复或清理正式实验及其数据、Cache 和结果。
- 重写已有 GraphRevoker、TracIn 或 Hybrid 的历史结论。
- 把当前任务状态复制进 AGENTS 或 Runbook。
