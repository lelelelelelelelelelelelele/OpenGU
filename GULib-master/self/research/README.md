# Work Plan · 实验管理

[打开实验总表](index.html) · [运行流程](RUNBOOK.md) · [实验归属整理](MIGRATION.md)

Work Plan 与 Block 平行。这里拥有实验创建、定义修订、运行尝试、重跑原因、分析、科学决定和实验依赖。Block 只拥有开发变更。SyncMate 负责提交、监控、回传、校验；SSH AutoReport 是按需追查的运行审计，不是日常工作计划。

## 阅读入口与命名

这里负责实验过程及其已保存分析；跨实验的“研究问题 → 分析报告 → 论文章节”关系统一在[论文论证导航](../../../../OpenGU-DocMap/40_论文写作/40_论文写作.md#研究问题、分析与章节导航)维护。查运行进度使用[实验总表](index.html)，写论文先从论证导航进入，不按目录日期猜测最新结论。

实验编号、分析主题和运行批次分别表达：目录按实验编号组织，单实验使用 `EXP-NNN/`，跨实验使用按编号升序排列的 `EXP-NNN_EXP-NNN/`。显示标题写“实验编号 · 内容主题”，副标题或引用标签注明 run ID、训练协议和范围。历史 AAGU 文件名保留来源身份，阅读标签使用对应的现行 EXP 编号。

| 现有位置 | 阅读名称与用途 |
|---|---|
| analyses/EXP-013/ | EXP-013 · 代理选点迁移：三 seed 分析；十 seed 扩展看 EXP-079 |
| analyses/EXP-080/full-20261021/ | EXP-080 · 删除预算与多 GU 响应；总报告与五策略/IM 专题分别进入 |
| analyses/EXP-011_EXP-079/ | EXP-011 / EXP-079 · 主矩阵与迁移响应联合分析；e11r1 / e79r6，新损失、分片 300 轮 |
| analyses/EXP-067_EXP-068/ | EXP-067 / EXP-068 · H64 历史参数候选推导与共享验证脚本；各阶段状态见 README 和对应 EXP 分析记录 |
| analyses/EXP-032_EXP-053/ | EXP-032 / EXP-053 · 3000 轮结果表、配对数据与复算脚本；论文用途分析和训练协议对照分别阅读 |
| analyses/AAGU-032-AAGU-053-3000-only-paper-analysis-20260923.md | EXP-032 / EXP-053 · 3000 轮结果的论文用途分析 |
| analyses/AAGU-032-AAGU-053-3000epoch-comparison-20260923.md | EXP-032 / EXP-053 · 训练协议变更对照；与 current-only 结果分开阅读 |

读取 `analysis` 与 `decision` 时同时核对 note、报告和运行范围：新版分析可以与旧版接受决定并存，旧 `accepted` 不自动覆盖新版。EXP-011 的 e11r1、EXP-079 的 e79r6 已有分析但仍待科学验收；各自历史决定只适用于原证据。此处为 2026-10-24 的入口说明，后续状态以各 EXP 记录为准。

新增单实验报告放入所属 EXP 目录，批次优先使用真实 run ID；跨实验专题放入对应的组合编号目录，并列出关联实验和全部运行身份。主题写在报告标题和文件名中。总入口使用 REPORT.md / REPORT.html，独立专题使用语义名称。日期只标识批次，避免仅用 final、latest、new 或参数简称命名。已有 EXP 目录内的运行与验证批次名称保留，以区分新旧证据。不复制实验状态或建立另一套验收台账。

## 事实来源

- `experiments/EXP-NNN.json` 是持续维护的本地实验状态，整个子目录不由 Git 跟踪；它不是可随意清理的缓存。保存当前范围、配置引用、准备/运行阶段、依赖、attempts 和下一步。实验编号使用 EXP-NNN；既有配置和证据目录保留原路径。
- `configs` 只引用原 YAML，分别标注现行、辅助、历史和候选。配置参数由 YAML 拥有，界面直接解析，禁止复制出第二套参数。`candidate` 文件尚未创建时，只允许记录处于 `draft` / `preparing` 阶段；页面明确显示待创建，不生成死链接。进入 `defined` 后，配置必须实际存在并通过 YAML 解析。
- `attempts` 按 run_id 保存每次尝试与证据；重跑追加独立记录，保留失败及被替代运行，不覆盖旧结果。计数只适用于该次运行范围，不跨配置或历史累加。
- 不维护过程流水 `history`；当前事实直接更新到对应字段。每次实际运行保留在 `attempts`，科学决定及其范围、证据保留在 `decision`。
- `analyses/EXP-NNN.json` 由 Git 跟踪，独立保存 `analysis`、`decision`、记录日期、所述范围、配置引用、运行身份/manifest、来源与科学决定。这里的范围和 attempts 是该分析的证据上下文，不随当前运行进度自动刷新。软件通过、运行完成、文件校验均不自动成为科学接受。
- `dependencies` 引用其他实验及所需证据、分析或科学接受；要求验证成功的扩展使用successful_acceptance，并要求父实验decision.success_confirmed明确为true，接受否定结果不会放行。`blocks` 只引用明确开发依赖，写明阻塞阶段和原因。
- Block 状态从指定 WORKITEM.md 只读读取。还需 `delivery_confirmed` 表明已核对本实验所需交付。缺失、未知、未接受或未确认落地均不自动解除；解除不触发运行。禁止扫描全体 WorkItems、复制Block图或强制映射每个Block。
- `framework.json` 保存研究问题说明；`config_groups.json` 只声明配置目录归属。开发验证 YAML 可以存在而不成为科研实验。

## 时间预算与实际耗时

新实验及新增运行范围必须在启动前提供 `time_budget`，冻结正数 `estimated_seconds`、完整覆盖范围和估算依据，并将 `estimate_status` 设为 `estimated`、`calculation` 设为 `cache_miss_serial`。估时依据应能复算为完整计划范围内各作业的 Cache 未命中耗时之和；按串行相加，不扣除 Cache 命中、不假设作业并行。范围变化时同步修订估时范围与依据。既有实验记录允许缺少或将 `time_budget` 设为 `null`；页面显示“估时未记录”，不计算偏差。

既有范围若没有启动前保存的估时，保留 `estimated_seconds: null`、`estimate_status: not_recorded` 和 `legacy_unrecorded: true`，说明未记录原因，不从历史运行时长倒推；更早的记录也可缺少整个 `time_budget` 字段。既有运行尝试可缺少 `runtime`，或缺少历史 Cache/估时子字段；页面将这些信息显示为“未记录”，不补造数值。`not_applicable` 仅用于 `execution.state` 为 `not_required` 的记录。新实验与新运行仍必须按上述格式写入预算和运行元数据，不能用缺字段或 legacy 标记跳过。

每条新 `attempts[]` 都记录 `runtime`：启动前的估时状态、作业是否启动、GPU 作业实际秒数及其范围/依据、单列的排队和回传秒数，以及 Cache 状态、分层命中统计和证据。实际作业耗时只计作业启动到结束；排队与回传不并入。失败、部分运行和重跑只要作业已启动，都累计实际耗时；未启动尝试不计为 0 秒。缺少原始计时或 Cache 证据时分别标记 `not_recorded`，不能用 0 代替未知。Cache 计数按逐格结果记录各层 `hit`、`miss`、`not_applicable` 或 `disabled` 数量。旧 `attempts[]` 缺少 `runtime` 时按未知显示，不参与偏差计算。

实验页仅在估时范围完整、`execution.state` 为 `completed`、范围内每个已启动尝试都有实际作业耗时和 Cache 统计时计算偏差：`累计实际秒数 - 预估秒数`，比例为该差值除以预估秒数；绝对偏差不超过 20% 显示为接近。否则展示当前阻塞原因，不显示部分范围的匹配结论。

## Agent 维护

维护运行元数据时，将起止时间写入 `attempts[].runtime.started_at` / `finished_at`，页面不读取 attempt 顶层同名字段。提交时间使用同一 job 的 Runner receipt `submitted_at`，或新版 job-status 的 `created_at`；不要混用本地 dispatch 开始时间或 Handoff 创建时间。先核对 job_id、run_id、执行 SHA（有 execution_digest 时一并核对），再关联 Controller/Handoff；终态回执比旧 running 快照完整时，保留并引用终态来源。历史诊断没有匹配回执时保留缺项，不能用 manifest 生成时间倒推。实验主说明写研究问题、范围与当前结果覆盖；重绑、恢复、回传和旧证据排除原因放到运行详情中的证据说明。

实验创建及日常运行状态更新只维护被忽略的 experiments/，不提交、不为每次更新创建 Block、Claim、分支或候选。通过既有接口新增、修改、校验或退役科学 YAML、公共参数小表与提交 Recipe，也由 Work Plan 管理，不创建开发 Block；这些 Git 跟踪文件仍须审阅并一起提交，正式运行前完成版本同步与 preflight。分析草稿留在 experiments/drafts/ 子目录，完成分析后才显式维护 analyses/ 中对应记录并独立提交。需要改变程序行为或接口契约（如解析器、算法、执行器、指标实现、缓存或结果格式）时，使用开发 Block，并在实验记录引用其交付。新实验采用独立的 EXP-NNN 编号，读取现有实验编号后分配下一个未占用编号；不调用 Block allocator。新建实验配置目录使用 expNNN，既有 aaguNNN 目录继续按 configs 引用使用。WorkBlock 编号及 blocks 引用继续使用 AAGU-NNN；两套编号独立分配。 创建新实验时同时写入时间估算、完整计划范围和可复算依据。

更新 JSON 后运行校验与重建；不编辑 HTML。状态记录不得包含 analysis/decision，生成器从 analyses/ 读取它们；尚无分析文件时显示尚未分析/尚未提交决定。分析中等工作进度记录在状态的 next_step，不为进度改动已保存分析。新增实验按已有记录字段形成独立文件；没有证据的运行用 unknown/not_recorded，不把缺失当成0或已完成。维护接口是文件与生成器，当前前端为只读视图，不是在线编辑器或实时调度台。

```powershell
python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --check-links
python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --check --check-links --verify-evidence
python -B -X utf8 -m pytest --noconftest tests/test_research_overview.py -q
```

上述测试仅依赖 pytest、PyYAML，不加载全局图训练 conftest。缺少依赖时可通过 `uv run --with pytest --with pyyaml python ...` 执行同一命令。

页面在 `self/research/index.html`。linked worktree 通过 canonical-root 读取本地实验状态、既有证据与指定Block，源码/YAML及已保存分析仍来自当前候选。HTML/SVG是忽略的生成物；普通Block变化不修改实验记录或Git跟踪文件。只有被引用依赖的只读展示会在重建后变化。

## 科学与交付边界

本轮迁入是2026-09-22本地材料核对，不代表SSH实时盘点。绑定manifest的哈希核查只验证这些指定本地文件；可信回传、索引与项目接纳仍由SyncMate负责。来源报告确认的完成与本轮重新核查的原始manifest分别标识。已失效的旧032映射不进入当前结果。

## Git 与执行版本

- 运行前照常核对本地 main、origin/main、SSH main 的完整 SHA 一致并绑定实际执行 SHA。运行、停止、回传等只更新忽略的状态，不触发 Git commit、push 或 SSH checkout 更新。
- 分析完成后审阅并显式提交本次 `analyses/<id>.json` 及其分析报告；不能使用 `git add .`，不能夹带其他 Block 的修改。该提交不是科学验收，也不得把运行 SHA 改成分析提交 SHA。
- 分析提交会推动本地 HEAD。下一次正式运行前再同步三端；有活跃任务时不得为了同步更新其 SSH checkout。跨阶段批次若需要立即继续，可先保留分析草稿，待当前执行批次结束再提交分析。
- 状态内容不随 clone/pull 分发。新设备或新克隆需显式取回维护中的状态副本；生成器缺失状态时明确失败，不从历史分析推断实时状态。主目录状态自行保留和备份，不使用 git clean -x 清理它。
- 分析文件保留支撑结论的 run ID、实际代码 SHA、配置与证据引用；历史资料没有具体身份时保留原报告引用并注明缺失，不补造。分析范围或配置与当前计划不一致时，不自动放行依赖。

既有估时若只覆盖部分运行或范围已变，页面保留原估值并显示范围不一致；缺少 calculation 时显示估算口径待确认。两种情况均不计算偏差。任何已有尝试缺少 runtime 时均显示未记录，即使实验已有估时也不将未知耗时当成零；新记录仍按上面的完整字段约定维护。

## 实验页阅读顺序

实验定义与已保存分析为正文；范围、完整 YAML、时间口径可展开。运行尝试只展示一次，提交时间取显式 `submitted_at` 或关联 controller 的 `watch.job.receipt.submitted_at`，Recipe 同样来自明确关联记录；缺失时显示未记录，不解析 run_id 猜测日期。时间缺失不改变执行状态。

分析记录可用 `analysis.highlights`（字符串列表）和 `analysis.tables`（caption、columns、rows）展示原证据中的关键观察；须保留原始来源、执行 SHA 和科学决定，不重新推断结果。参数摘要直接读取现行 YAML，不另存参数副本。

实验组按现行 `kind: experiment` 配置组织；提交 Recipe 的 `config_path` 归入该配置。运行按明确 Recipe ID、run_id 或 manifest.config_path 关联；分析按 config_path/run_id（含校准 cases[].run）关联。未匹配的准备和历史文件折叠保留，不按文件名猜测运行状态。相同路径的证据只显示一次。
