# Work Plan · 实验管理

[打开实验总表](index.html) · [运行流程](RUNBOOK.md) · [实验归属整理](MIGRATION.md)

Work Plan 与 Block 平行。这里拥有实验创建、定义修订、运行尝试、重跑原因、分析、科学决定和实验依赖。Block 只拥有开发变更。SyncMate 负责提交、监控、回传、校验；SSH AutoReport 是按需追查的运行审计，不是日常工作计划。

## 事实来源

- `experiments/EXP-NNN.json` 是持续维护的本地实验状态，整个子目录不由 Git 跟踪；它不是可随意清理的缓存。保存当前范围、配置引用、准备/运行阶段、依赖、attempts、history 和下一步。实验编号使用 EXP-NNN；既有配置和证据目录保留原路径。
- `configs` 只引用原 YAML，分别标注现行、辅助、历史和候选。配置参数由 YAML 拥有，界面直接解析，禁止复制出第二套参数。
- `attempts` 按 run_id 保存每次尝试与证据；重跑追加独立记录，保留失败及被替代运行，不覆盖旧结果。计数只适用于该次运行范围，不跨配置或历史累加。
- `history` 保存有日期和来源的过程事件。只追加事件；纠错新增说明，现行状态直接改为已核实事实。不把迁入日期伪装为历史实际运行日期。
- `analyses/EXP-NNN.json` 由 Git 跟踪，独立保存 `analysis`、`decision`、记录日期、所述范围、配置引用、运行身份/manifest、来源与科学事件。这里的范围和 attempts 是该分析的证据上下文，不随当前运行进度自动刷新。软件通过、运行完成、文件校验均不自动成为科学接受。
- `dependencies` 引用其他实验及所需证据、分析或科学接受；要求验证成功的扩展使用successful_acceptance，并要求父实验decision.success_confirmed明确为true，接受否定结果不会放行。`blocks` 只引用明确开发依赖，写明阻塞阶段和原因。
- Block 状态从指定 WORKITEM.md 只读读取。还需 `delivery_confirmed` 表明已核对本实验所需交付。缺失、未知、未接受或未确认落地均不自动解除；解除不触发运行。禁止扫描全体 WorkItems、复制Block图或强制映射每个Block。
- `framework.json` 保存研究问题说明；`config_groups.json` 只声明配置目录归属。开发验证 YAML 可以存在而不成为科研实验。

## Agent 维护

实验创建及日常运行更新只维护被忽略的 experiments/，不提交、不为每次更新创建 Block、Claim、分支或候选。分析草稿留在 experiments/drafts/ 子目录，完成分析后才显式维护 analyses/ 中对应记录并独立提交。需要修改算法、执行器、指标能力或正式可执行配置时，使用开发 Block，并在实验记录引用其交付。新实验采用独立的 EXP-NNN 编号，读取现有实验编号后分配下一个未占用编号；不调用 Block allocator。新建实验配置目录使用 expNNN，既有 aaguNNN 目录继续按 configs 引用使用。WorkBlock 编号及 blocks 引用继续使用 AAGU-NNN；两套编号独立分配。

更新 JSON 后运行校验与重建；不编辑 HTML。状态记录不得包含 analysis/decision，生成器从 analyses/ 读取它们；尚无分析文件时显示尚未分析/尚未提交决定。分析中等工作进度记录在状态的 next_step/history，不为进度改动已保存分析。新增实验按已有记录字段形成独立文件；没有证据的运行用 unknown，不把缺失当成0或已完成。维护接口是文件与生成器，当前前端为只读视图，不是在线编辑器或实时调度台。

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
