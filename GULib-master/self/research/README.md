# Work Plan · 实验管理

[打开实验总表](index.html) · [运行流程](RUNBOOK.md) · [实验归属整理](MIGRATION.md)

Work Plan 与 Block 平行。这里拥有实验创建、定义修订、运行尝试、重跑原因、分析、科学决定和实验依赖。Block 只拥有开发变更。SyncMate 负责提交、监控、回传、校验；SSH AutoReport 是按需追查的运行审计，不是日常工作计划。

## 事实来源

- `experiments/AAGU-NNN.json` 是每项实验的唯一过程记录，沿用原编号，不因来源编号重排或移动 YAML。`category` 区分当前维护、待准备和历史；四个阶段分别记录状态、说明与证据。
- `configs` 只引用原 YAML，分别标注现行、辅助、历史和候选。配置参数由 YAML 拥有，界面直接解析，禁止复制出第二套参数。
- `attempts` 按 run_id 保存每次尝试与证据；重跑追加独立记录，保留失败及被替代运行，不覆盖旧结果。计数只适用于该次运行范围，不跨配置或历史累加。
- `history` 保存有日期和来源的过程事件。只追加事件；纠错新增说明，现行状态直接改为已核实事实。不把迁入日期伪装为历史实际运行日期。
- `analysis` 和 `decision` 分别记录分析交付与科学决定。软件通过、运行完成、文件校验均不自动成为科学接受。
- `dependencies` 引用其他实验及所需证据、分析或科学接受；要求验证成功的扩展使用successful_acceptance，并要求父实验decision.success_confirmed明确为true，接受否定结果不会放行。`blocks` 只引用明确开发依赖，写明阻塞阶段和原因。
- Block 状态从指定 WORKITEM.md 只读读取。还需 `delivery_confirmed` 表明已核对本实验所需交付。缺失、未知、未接受或未确认落地均不自动解除；解除不触发运行。禁止扫描全体 WorkItems、复制Block图或强制映射每个Block。
- `framework.json` 保存研究问题说明；`config_groups.json` 只声明配置目录归属。开发验证 YAML 可以存在而不成为科研实验。

## Agent 维护

实验创建及日常运行/分析更新直接维护本目录，不需要为每次更新创建 Block、Claim、分支或候选。需要修改算法、执行器、指标能力或正式可执行配置时，使用开发 Block，并在实验记录引用其交付。新实验采用唯一 AAGU 编号；不调用 Block allocator 创建伪开发任务，暂未分配的编号必须先核对现有实验及共享编号占用。

更新 JSON 后运行校验与重建；不编辑 HTML。新增实验按已有记录字段形成独立文件；没有证据的运行用 unknown，不把缺失当成0或已完成。维护接口是文件与生成器，当前前端为只读视图，不是在线编辑器或实时调度台。

```powershell
python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --check-links
python -B -X utf8 scripts/dashboard/gen_research_overview.py --canonical-root E:/project/OpenGU/GULib-master --check --check-links --verify-evidence
python -B -X utf8 -m pytest tests/test_research_overview.py -q
```

页面在 `self/research/index.html`。linked worktree 通过 canonical-root 读取既有证据与指定Block，源码/YAML仍来自当前候选。HTML/SVG是忽略的生成物；普通Block变化不修改实验记录或Git跟踪文件。只有被引用依赖的只读展示会在重建后变化。

## 科学与交付边界

本轮迁入是2026-09-22本地材料核对，不代表SSH实时盘点。绑定manifest的哈希核查只验证这些指定本地文件；可信回传、索引与项目接纳仍由SyncMate负责。来源报告确认的完成与本轮重新核查的原始manifest分别标识。已失效的旧032映射不进入当前结果。
