# 实验运行流程

## 1. 从实验记录开始

读取 self/research/experiments/AAGU-NNN.json 的当前范围、配置、阶段、依赖和下一步。运行、重跑、补算只更新该 Git 忽略的状态记录；同时读取 analyses/AAGU-NNN.json 中已有的分析和科学决定（如有），分析草稿保存在忽略目录，已完成分析单独维护并提交；不为纯运行创建Block或Claim。先明确本次是新尝试、恢复、指标重算还是纯分析，避免已完成证据被重复生产。

## 2. 核对准备条件

读取 experiments/AGENTS.md 与当前launcher的相邻说明。复用仍有效的gate；核对代码版本、数据与split、固定参数、已有结果、共享运行条件和本实验preflight。被Block阻塞时只检查其明确交付；已接受但尚未落地执行基线也不能启动。代码或定义需改变时，由对应Block交付后回到实验。

当前正式SSH版本、数据根和GPU要求仍以 experiments/AGENTS.md 为准。设备不满足就记录原因；不能降级CPU或自动改数据、预算、参数。

## 3. 准备 Recipe，再通过 SyncMate 提交

科学配置在 `experiments/configs/`，提交声明在 [scripts/syncmate/recipes/](../../scripts/syncmate/recipes/)。一份 Recipe 绑定配置、现有 SHA/指纹、run ID、超时、数据集计数和产物规则；`opengu_recipes.py` 只负责通用读取、校验和装配，不再登记具体实验。多份 Recipe 可以服务同一实验的不同已审阅运行范围，不代表多个科学实验，也不要求把普通矩阵按数据集或 seed 拆开。

### 创建或修改配置后

每次运行准备以一次同步为目标：先在本地备齐本阶段所需代码、实验配置、引用小表和全部 Recipe，完成审阅与相邻验证，并将完整交付落到同一主线目标版本，再统一同步一次。不得先同步代码、到提交前才补配置或 Recipe 而重复同步。同步完成并通过正式 preflight 后，直接按已授权顺序提交已准备好的运行。同一版本已同步就绪时不重复同步；依赖上游结果才能确定的后续阶段，在结果确定后独立备齐该阶段输入，再按同样流程处理。

1. 确认实验记录允许的范围，审阅 `experiment.yaml` 及引用的小表，按 [experiments/AGENTS.md](../../experiments/AGENTS.md) 完成相邻验证。
2. 按 [Recipe 命令说明](../../scripts/syncmate/README.md#independent-recipe-yaml) 使用 `recipe.py generate`，显式指定 recipe ID、新 run ID、超时及按配置顺序排列的真实数据集/候选计数。计数来自已核验数据，不猜测或临时下载。命令只将 YAML 打印到 stdout；创建 `experiment.yaml` 本身不会自动生成 Recipe。审阅后以 UTF-8 保存到 `scripts/syncmate/recipes/<id>.yaml`，文件名必须与声明 ID 相同。
3. 配置或引用输入改变后，显式重新生成并审阅 SHA/指纹，将配置和 Recipe 一起提交。读取、预览或提交不会自动刷新哈希。仅改变 run ID 或超时也须审阅新的声明；不覆盖旧运行目录。
4. Recipe 纳入 Git 跟踪后，用 `recipe.py preview <recipe-id> --node <peer-id> --device-config .syncmate/device.yaml` 检查完整 commit、配置、节点、SSH 工作目录、解释器、命令、run ID、执行输出和本地接收位置。`peer-id` 是设备配置中的节点 ID，例如 `gpu4090`，不是 SSH 别名。预览只读且不连接 SSH；脏工作区可以检查，但不具备正式提交资格。
5. 本阶段代码、配置与全部 Recipe 完整交付后，对同一主线目标版本统一完成一次已授权的同步，再核对本地 main、origin/main、SSH 干净 main 的完整 SHA 一致及正式 preflight。预览、dispatch 均不负责同步工作区修改；候选工作树预览不代表部署完成。
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
