# 实验运行流程

## 1. 从实验记录开始

读取 self/research/experiments/EXP-NNN.json 的当前范围、配置、阶段、依赖和下一步。运行、重跑、补算只更新该 Git 忽略的状态记录；同时读取 analyses/EXP-NNN.json 中已有的分析和科学决定（如有），分析草稿保存在忽略目录，已完成分析单独维护并提交。通过既有接口准备或维护实验 YAML、公共参数小表与提交 Recipe，以及运行、重跑、补算和分析，均不创建 Block 或 Claim。先明确本次是配置准备、新尝试、恢复、指标重算还是纯分析，避免已完成证据被重复生产。

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

读取 experiments/AGENTS.md 与当前launcher的相邻说明。复用仍有效的gate；核对代码版本、数据与split、固定参数、已有结果、共享运行条件和本实验preflight。被Block阻塞时只检查其明确交付；已接受但尚未落地执行基线也不能启动。改变程序行为或接口契约时，由对应开发 Block 交付后回到实验；通过既有接口调整科学配置、参数、矩阵范围或 Recipe 时，直接在本实验维护并完成审阅与相邻验证。

当前正式SSH版本、数据根和GPU要求仍以 experiments/AGENTS.md 为准。设备不满足就记录原因；不能降级CPU或自动改数据、预算、参数。

检查按职责消费证据：安装事实读取对应目标版本的安装回执；启动时的版本、输入和设备等动态条件由正式 preflight 核验。Agent 不在工具检查之外另写 SSH 命令重复核对同一事实。回执缺失、过期或身份不匹配时，交由对应检查入口返回具体阻塞；只有明确故障且本地证据不足时，才针对该故障连接 SSH 排查。必要的提交时检查不因此前预览或安装成功而省略。

### 中断后的缓存恢复条件

队列空闲、runner 锁释放和安装成功，只证明各自检查覆盖的条件。共享 Cache 不在启动时扫描任意 Score 锁并拒绝整个矩阵；实际访问沿用按条目锁、取得锁后的 HIT 复查、索引事务和完整性／身份冲突保护。HIT 不重新生产或覆盖 payload。

条目锁等待超时保留原 job、失败日志和锁，不自动重试或删除；获授权的再次提交使用新运行身份。锁归属、缓存损坏或内容冲突须按[机器恢复流程](../../scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md#scorebundle-遗留锁恢复)核对，不能仅因本容器看不到某 PID 就判定其他节点 owner 已不存在，也不一概视为重跑即可解决。保留实际失败与诊断证据，不改写原作业身份。

GU 在 `reuse` 下先按当前输入和已有 checkpoint 元数据查找 Output，HIT 不构造 GU 模型、不加载初始权重或 ensemble；MISS 才进入原计算路径并校验实际权重。元数据引用标记为 `verification=metadata_only`，不冒充权重文件校验；没有可信 sidecar 的外部 PT 仍须读取状态以确定身份。模型型 Selector 的准备不在此跳过范围。

同一次执行可复用固定源码指纹和计算路径所需的已验证初始模型快照；每个计算消费者取得独立模型副本，新运行重新确定身份。Artifact 内容与身份校验、基础指标和后续评价照常执行。缓存相关改动须同时验证冷路径和真实 warm 命中，记录模型/ensemble 准备调用数与分项耗时；不能只凭 HIT 或请求数量乘假定单次时间承诺整个矩阵的六小时上限。

## 3. 准备 Recipe，再通过 SyncMate 提交

科学配置在 `experiments/configs/`，提交声明在 [scripts/syncmate/recipes/](../../scripts/syncmate/recipes/)。一份 Recipe 绑定配置、现有 SHA/指纹、run ID、超时、数据集计数和产物规则；`opengu_recipes.py` 只负责通用读取、校验和装配，不再登记具体实验。多份 Recipe 可以服务同一实验的不同已审阅运行范围，不代表多个科学实验，也不要求把普通矩阵按数据集或 seed 拆开。

### 创建或修改配置后

每次运行先备齐本阶段代码、科学配置、引用小表与 Recipe，完成审阅和相邻验证，再明确提交版本。生成可以读取工作区草稿；预览和提交只消费选定提交。未来步骤可选择不同的新提交；已入队、运行或完成的 job 保持原 SHA、Recipe/config 和验证合同，不会随 main 前进或文稿修改漂移。

首次 Core/控制包部署通过登记 bootstrap/install 边界，精确 wheel 安装到项目独立运行环境，保留原科学基础环境。离线节点记为待更新，上线后由同一授权部署材料核验就绪；在线节点无须等待它开机。共享源码切换仍检查全部登记节点在共享文件系统上的队列及安全停点，离线或占用未知不等于空闲。正常任务提交中的 private-bundle 来源导入只增加 Git 对象，不切换 checkout、环境或 origin 引用；实际切版归 Core，必须覆盖全部相关 node 的安全准入。同版本可双节点执行。不得向公开 GitHub 推送，不能临时手写远端 fetch/pull、停掉正常任务或升级环境来绕过入队条件。

1. 确认实验记录允许的范围，审阅配置和引用小表，按 [experiments/AGENTS.md](../../experiments/AGENTS.md) 完成相邻验证。
2. 按 [Recipe 命令说明](../../scripts/syncmate/README.md#independent-recipe-yaml) 生成新 ID、新 RID 的独立 Recipe。节点数与候选数来自绑定的现存 Dataset/Split；缺失或不符就拒绝，不手填计数，不下载或物化正式数据。
3. 显式重新生成并审阅改变后的哈希/指纹，把配置和 Recipe 一起提交。预览或提交不刷新旧声明，也不覆盖已有运行目录。
4. 使用 `recipe.py preview <recipe-id> --node <peer-id> --source-ref <full-sha> --device-config .syncmate/device.yaml` 检查源 SHA、配置、命令、节点、输出、接收位置和排除未提交内容的提示。预览不连接 SSH、不检查 GPU，也不表示已经执行。
5. 用已安装控制包的 OpenGU 入口提交：`syncmate.py --source-ref <full-sha> runner-agent dispatch <peer-id> --recipe <id> --job-id <new-id> --json`。它核验注册 peer、依赖和私有来源，只导入执行端缺少的提交对象并保存冻结 handoff/科学声明，再由 Core 预留独立 node 任务。执行端仍为 S1 不阻止 B@S2 入队。生成或预览不产生 attempt；实际提交后才把 job、SHA、Recipe、范围和回执写入 Work Plan。
6. 实际启动时 Core 取得租约，所有相关 node 安全后才准备精确版本；绑定 checkout 中的新进程核验代码、依赖、科学配置、Dataset/Split、CUDA 与结果/runtime 身份。未通过时不记录 producer 已启动。只读查询区分 queued、preparing/preflight、executing、awaiting_return、verified 和失败；查询中断不等于实验失败。

OpenGU 当前提交通路是上述固定 CLI；不能把通用 Core console 的提交通路当作已接入的 OpenGU 自定义控制入口。新接口仅在对应控制包、Core 和源码已交付后生效；本地候选文档不代表生产已经部署。

### Run ID 命名

新运行默认使用短 `run_id`（RID），如 `r1`、`r2`；`experiment_id` 已标识实验，不再把实验全名复制进 RID。纯数字也合法，但 YAML 中必须写成字符串，例如 `run_id: '1'`。只有需要区分特殊用途或避免路径冲突时加短说明，如 `gate1`、`retry1`、`e13-r1`。

沿用现有身份及不覆盖规则：同一实验的新尝试使用未占用的 RID；跨实验并发还须检查实际共享 runtime 路径，必要时加短实验前缀。现有执行器的 runtime 路径包含 RID，不能仅凭结果目录按 experiment 分层就假定跨实验同名无冲突。已提交或已有产物的历史 RID 不重命名；仅修改尚未提交的 Recipe 时也须重新审阅声明和预览，不伪造一次运行记录。

### 回执和目录

Recipe 是提交前维护的输入；提交时 Core 自动保存 `.syncmate/runs/<job_id>.json` handoff，队列执行产生对应 receipt/result。它们记录实际提交与执行事实，不由用户手写，也不会因为只创建或预览 Recipe 就产生一次执行回执。收集和校验记录在执行相应操作后生成；按 README 的 `runner-agent collect` 对原 job 收集。传输校验后再用 `scientific-check <node> --job-id <id>` 按该任务冻结声明及原提交验证器检查项目结果；不读取当前 Recipe/config 来定义旧任务，也不把项目检查通过当作科学接受。

`outputs.root: results/runs/{experiment_id}/{run_id}` 指执行端目录，正式实验通常位于 SSH 活跃检出下。本地回传落到 `results/runs/<peer-id>/<experiment_id>/<run_id>/`，例如 `results/runs/gpu4090/<experiment_id>/<run_id>/`。具体绝对位置以设备配置和该 job 已保存的 handoff 为准；开发 worktree 预览显示其本地接收路径，不代表正式结果已经回传。

SyncMate 的 runbook、checklist 和 handoff 命令提供设备级操作指导，本文件拥有实验级流程。新流程只能用于已交付并同步了相应接口的执行版本，不把候选文档当作远端现状。

### 已提交或正在运行时发生修改

先按原 job ID、handoff 和 receipt 确认当前状态。旧任务固定原提交身份，不会自动采用新的 Recipe；不要改写旧 job、回执、结果或为正在运行的任务更新共享 SSH checkout。新需求在本地准备并明确选择新提交后即可入队；执行文件和共享环境的更新必须等待全部相关节点安全停点，不主动停止正常任务。

后续运行使用新的 run ID；若原 Recipe 仍被排队或运行中的任务引用，保留其声明，为新提交使用新的 recipe ID 和文件。配置变更则重新生成哈希并完成审阅、提交和冻结来源；真正启动前再检查任务版本与科学 readiness。不要在同一目录原地覆盖产物；失败恢复先按已有恢复流程确认范围，不因修改了 YAML 就自动重跑。

提交后把实际 job_id、run_id、代码版本、配置入口、范围及handoff/回执引用追加到该实验 attempts。提交中断时先找回原请求；running时不自动重试。需要重跑时新增运行身份并明确retry_of和原因，不覆盖旧attempt。

## 4. 监控与回传

运行过程由SyncMate观察，Work Plan只保存已确认的阶段事实与最新观察日期。进程done不代表回传或可信校验完成。沿用现有链：完成运行 → 收集 → SHA-256校验 → 可信索引 → 项目结果检查。

Agent 按确切 job_id 读取本地 controller、delivery 和 handoff 回执，运行观察、收集与传输校验由 SyncMate 执行；不另行 SSH 轮询进程、扫描缓存或重复验证已可信回传的远端文件。仅在本地回执指出具体故障且现有证据不足时，针对该故障读取 SSH AutoReport 等必要证据。无需把日志全文复制进 Work Plan。失败、阻塞或可信回传均结束该次运行的等待；可信回传后进入项目科学分析，失败恢复按已有重跑与缓存修复 Runbook 确认范围。

## 5. 分析与科学决定

分析绑定具体运行/配置范围及报告，明确哪些结果被采用或排除。可先分析可信子集；不能把部分分析显示成全矩阵完成。记录计算或缓存命中、结果身份正确、结论支持范围三类事实。用户接受的是明确结论范围，不从Block accepted、校验PASS或程序退出推断。

分析完成后，将所述范围、采用/排除理由、配置引用、实际运行 SHA、run ID、manifest/报告引用与科学决定保存在 `analyses/EXP-NNN.json`，检查通过后独立提交对应分析和报告。不要用分析提交 SHA 替换实际运行 SHA。批次运行中可以继续编辑并提交论文或分析；它们不改写已冻结任务。下一步骤明确选择来源 SHA；不得更新活跃任务的执行 checkout。

## 6. 更新总表

更新实验阶段与下一步，将证据归入对应运行或科学决定，再运行 README.md 中的生成和检查命令。实验依赖及Block阻塞在前端可见；它们不会改变原Block，也不会自动提交下一项实验。

运行中的状态更新和页面重建不做 commit。分析提交后，下一次任务显式选择已审阅 SHA；入队导入所需私有 Git 对象，实际启动前核对本任务合同、执行 HEAD 与科学 preflight。状态目录缺失时先取回维护副本，不用 Git 历史里的旧计划或已完成分析推断当前状态。
