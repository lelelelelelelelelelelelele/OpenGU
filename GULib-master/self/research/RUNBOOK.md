# 实验运行流程

## 1. 从实验记录开始

读取 self/research/experiments/AAGU-NNN.json 的当前范围、配置、阶段、依赖和下一步。运行、重跑、补算只更新该 Git 忽略的状态记录；同时读取 analyses/AAGU-NNN.json 中已有的分析和科学决定（如有），分析草稿保存在忽略目录，已完成分析单独维护并提交；不为纯运行创建Block或Claim。先明确本次是新尝试、恢复、指标重算还是纯分析，避免已完成证据被重复生产。

### 时间预算与运行耗时

新实验/新增范围必须在首次 GPU 作业启动前写入 `time_budget`，覆盖其完整计划范围，并冻结 `estimate_status`、正数 `estimated_seconds`、`scope` 和 `basis`；`calculation` 固定为 `cache_miss_serial`，按 Cache 未命中的作业耗时串行求和。不要把预计队列、回传时间或并行收益写进估时。既有实验记录可缺少 `time_budget` 或设为 `null`；页面将其显示为估时未记录，不计算偏差。已有记录若保留了字段但无估时，可用 `legacy_unrecorded: true` 标记；不能把这个标记复制到新实验。

每次新增 `attempts[]` 时同时写入 `runtime`。既有实验中缺少 `runtime` 的尝试作为未记录历史数据显示，不推断作业状态或耗时：

- `job_started` 明确 GPU 作业是否真正启动；未启动时实际耗时和 Cache 标记为 `not_applicable`，不写 0。
- `estimate_status` / `estimated_seconds` 保留本次作业启动前冻结的分项估时；尚未记录则为 `not_recorded_before_start` / `null`，且仅既有历史尝试可带 `legacy_unrecorded: true`。
- `actual_status` 为 `recorded` 时，`actual_seconds` 取作业启动至结束的计时并提供 `actual_basis`、`actual_scope` 与 `evidence`。没有作业起止计时证据时填 `not_recorded` / `null`，不能拿单元累计时长或文件生成时间代替。
- `queue_seconds` 和 `return_seconds` 分别记录排队、回传耗时；没有证据时保留 `null`。两者不进入 GPU 作业实际耗时累计。
- `cache` 用 `observed`、`not_recorded` 或 `not_applicable` 表示状态。观察到时按 cache layer 写 `hit`、`miss`、`not_applicable`、`disabled` 计数，并链接到原始运行证据；未知不能写成 0 命中或 0 未命中。既有运行数据缺少该子字段时页面显示未记录，不补造统计。

页面累计所有已启动尝试的作业耗时，包括失败、部分运行和重跑。仅当 `time_budget` 的完整范围对应 `execution.state: completed`，且该范围的每个已启动尝试都保存了作业耗时和 Cache 统计，才显示估时偏差。偏差秒数为实际累计减预估，偏差比例以预估为分母；绝对值在 20% 内为“接近”。缺少估时、未完成范围或证据不齐时，页面说明原因并不显示匹配结论。

## 2. 核对准备条件

读取 experiments/AGENTS.md 与当前launcher的相邻说明。复用仍有效的gate；核对代码版本、数据与split、固定参数、已有结果、共享运行条件和本实验preflight。被Block阻塞时只检查其明确交付；已接受但尚未落地执行基线也不能启动。代码或定义需改变时，由对应Block交付后回到实验。

当前正式SSH版本、数据根和GPU要求仍以 experiments/AGENTS.md 为准。设备不满足就记录原因；不能降级CPU或自动改数据、预算、参数。

## 3. 准备 Recipe，再通过 SyncMate 提交

科学配置在 `experiments/configs/`，提交声明在 [scripts/syncmate/recipes/](../../scripts/syncmate/recipes/)。一份 Recipe 绑定配置、现有 SHA/指纹、run ID、超时、数据集计数和产物规则；`opengu_recipes.py` 只负责通用读取、校验和装配，不再登记具体实验。多份 Recipe 可以服务同一实验的不同已审阅运行范围，不代表多个科学实验，也不要求把普通矩阵按数据集或 seed 拆开。

### 创建或修改配置后

1. 确认实验记录允许的范围，审阅 `experiment.yaml` 及引用的小表，按 [experiments/AGENTS.md](../../experiments/AGENTS.md) 完成相邻验证。
2. 按 [Recipe 命令说明](../../scripts/syncmate/README.md#independent-recipe-yaml) 使用 `recipe.py generate`，显式指定 recipe ID、新 run ID、超时及按配置顺序排列的真实数据集/候选计数。计数来自已核验数据，不猜测或临时下载。命令只将 YAML 打印到 stdout；创建 `experiment.yaml` 本身不会自动生成 Recipe。审阅后以 UTF-8 保存到 `scripts/syncmate/recipes/<id>.yaml`，文件名必须与声明 ID 相同。
3. 配置或引用输入改变后，显式重新生成并审阅 SHA/指纹，将配置和 Recipe 一起提交。读取、预览或提交不会自动刷新哈希。仅改变 run ID 或超时也须审阅新的声明；不覆盖旧运行目录。
4. Recipe 纳入 Git 跟踪后，用 `recipe.py preview <recipe-id> --node <peer-id> --device-config .syncmate/device.yaml` 检查完整 commit、配置、节点、SSH 工作目录、解释器、命令、run ID、执行输出和本地接收位置。`peer-id` 是设备配置中的节点 ID，例如 `gpu4090`，不是 SSH 别名。预览只读且不连接 SSH；脏工作区可以检查，但不具备正式提交资格。
5. 代码与配置经开发 Block 交付后，单独完成已授权的代码同步，再核对本地 main、origin/main、SSH 干净 main 的完整 SHA 一致及正式 preflight。预览、dispatch 均不负责同步工作区修改；候选工作树预览不代表部署完成。
6. 使用 SyncMate“运行与回传”前端选择已审阅的 Recipe 与节点，检查就绪后提交。Recipe 生成和完整提交预览目前通过上述 CLI 完成，前端接入留待后续。Agent 需要提交命令时读取已安装 CLI 的 `--help` 和上述 README，不从历史示例猜测接口。

### 回执和目录

Recipe 是提交前维护的输入；提交时 Core 自动保存 `.syncmate/runs/<job_id>.json` handoff，队列执行产生对应 receipt/result。它们记录实际提交与执行事实，不由用户手写，也不会因为只创建或预览 Recipe 就产生一次执行回执。收集和校验记录在执行相应操作后生成；`dispatch --wait` 可在成功后自动收集校验，控制端必须持续运行，否则按 README 的 `runner-agent collect` 对原 job 收集。

`outputs.root: results/runs/{experiment_id}/{run_id}` 指执行端目录，正式实验通常位于 SSH 活跃检出下。本地回传落到 `results/runs/<peer-id>/<experiment_id>/<run_id>/`，例如 `results/runs/gpu4090/<experiment_id>/<run_id>/`。具体绝对位置以设备配置和该 job 已保存的 handoff 为准；开发 worktree 预览显示其本地接收路径，不代表正式结果已经回传。

SyncMate 的 runbook、checklist 和 handoff 命令提供设备级操作指导，本文件拥有实验级流程。新流程只能用于已交付并同步了相应接口的执行版本，不把候选文档当作远端现状。

### 已提交或正在运行时发生修改

先按原 job ID、handoff 和 receipt 确认当前状态。旧任务固定原提交身份，不会自动采用新的 Recipe；不要改写旧 job、回执、结果或为正在运行的任务更新共享 SSH checkout。新需求在本地准备，等活跃任务完成或按既有流程明确停止后，再安排执行端版本更新。

后续运行使用新的 run ID；若原 Recipe 仍被排队或运行中的任务引用，保留其声明，为新提交使用新的 recipe ID 和文件。配置变更则重新生成哈希并完成审阅、提交、同步与 readiness。不要在同一目录原地覆盖产物；失败恢复先按已有恢复流程确认范围，不因修改了 YAML 就自动重跑。

提交后把实际 job_id、run_id、代码版本、配置入口、范围及handoff/回执引用追加到该实验 attempts 和 history。提交中断时先找回原请求；running时不自动重试。需要重跑时新增运行身份并明确retry_of和原因，不覆盖旧attempt。

## 4. 监控与回传

运行过程由SyncMate观察，Work Plan只保存已确认的阶段事实与最新观察日期。进程done不代表回传或可信校验完成。沿用现有链：完成运行 → 收集 → SHA-256校验 → 可信索引 → 项目结果检查。

需要排查精确阶段或缓存事件时再读取SSH AutoReport。无需把日志全文复制进Work Plan。运行失败、部分完成、输入缺失分别记录，恢复按已有重跑与缓存修复Runbook确认范围。

## 5. 分析与科学决定

分析绑定具体运行/配置范围及报告，明确哪些结果被采用或排除。可先分析可信子集；不能把部分分析显示成全矩阵完成。记录计算或缓存命中、结果身份正确、结论支持范围三类事实。用户接受的是明确结论范围，不从Block accepted、校验PASS或程序退出推断。

分析完成后，将所述范围、采用/排除理由、配置引用、实际运行 SHA、run ID、manifest/报告引用与科学决定保存在 `analyses/AAGU-NNN.json`，检查通过后独立提交对应分析和报告。不要用分析提交 SHA 替换实际运行 SHA。批次仍在运行时可先保留草稿，避免提交推动本地 HEAD 后影响下一阶段的三端就绪检查；不得更新活跃任务的 SSH checkout。

## 6. 更新总表

更新实验阶段与下一步，追加有证据的history事件，再运行 README.md 中的生成和检查命令。实验依赖及Block阻塞在前端可见；它们不会改变原Block，也不会自动提交下一项实验。

运行中的状态更新和页面重建不做 commit。分析提交后，下一次正式运行前重新同步并核对三端 SHA。状态目录缺失时先取回维护副本，不用 Git 历史里的旧计划或已完成分析推断当前状态。
