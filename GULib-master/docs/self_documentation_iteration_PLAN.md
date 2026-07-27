---
title: Self 文档迭代计划
created: 2026-07-26
status: proposed
scope: self documentation inventory and orchestration only
---

# Self 文档迭代计划

## 结论与边界

`self/dashboard/WORKPLAN.md` 是唯一的当前状态/任务权威；`self/` 不是另一个实时计划库。此次后续迭代应先修正入口、状态标签和 V3 语义路由，再以证据刷新少量仍被当作 current 的辅助文档。旧资料默认**保留路径、显式降级并由入口索引**，不应先移动、删除或改写历史正文。

本计划只编排工作，**不改写任何 `self/` 文档**。执行时仍在主 Local 环境完成，不能创建或切换 worktree，不能提交；现有未提交的 `audit_results.txt` 删除、`AGENTS_DRAFT.md` 与两份 CLAUDE/AGENTS 报告必须保留原状。

## 盘点证据

- 盘点范围：`self/` 的 32 份人读文档（29 Markdown、3 HTML），不把程序、数据 JSON、图片或缓存当作文档。
- 当前治理：根 `AGENTS.md` 指定 dashboard 为 live operational hub，禁止手改生成 dashboard；`self/dashboard/CLAUDE.md` 是唯一的 `self/` 局部说明。`AGENTS_DRAFT.md` 是未跟踪的审阅草稿，明确不取代根 `AGENTS.md`。
- 链接：本地 Markdown 目标检查没有真实断链；唯一命中是 `flow.md` 代码块里的 `strategy_map[name](args)`，不是 Markdown 链接。`文档规划/_文档地图.md` 的 Obsidian 目标也都存在。
- 入口问题：根目录多数文档只有 code-style `See also`，不形成可点击/可追踪导航；`self/README.md` 没有索引近期 review、limitations、AutoReport/V3 或 concordance，并列出一个不存在的 `.bak` 文件。
- 时间判断采用正文、权威入口和 Git 最近内容变更，不只使用文件 mtime。例如 `attack_flow.md` 与 `flow.md` 在本地显示较新 mtime，但最近内容提交仍是 2026-05-07。

## 不可混淆的 live / V3 边界

| Surface | 权威内容 | 写入/更新方式 | 绝不能做 |
|---|---|---|---|
| `self/dashboard/WORKPLAN.md` | 当前状态、原因、任务、依赖和入口 | 手写 source；变动后由 `scripts/dashboard/refresh.py` 重生看板 | 从旧报告、分支名或历史 dashboard 推断 current state |
| `self/dashboard/progress.html` | WORKPLAN 的浏览器看板 | 仅由 refresh 生成 | 手改 HTML 或把它当第二个计划源 |
| `self/dashboard/VALIDATION_LOG.md` | 人/AI 验证与 sanity evidence | append-only；错误用新 `SUPERSEDED` 条目纠正 | 删除或改写既有条目；把它当运行事件流 |
| `results/_journal/auto_report.events.jsonl` | V3 机器运行审计原件 | producer 在真实阶段转换时 append；身份/去重失败即 fail-closed | 为补历史手造 V3 event；在 dry-run、重复 hit/skip 时追加 |
| `results/_journal/auto_report.md` / `.html` | JSONL + baseline 的有界、可重建当前视图 | generator 在同一锁内刷新 | 手改、追加、或把它说成审计原件 |
| `results/_journal/auto_report_baseline.json` | 可保留的历史事实与失效边界 | 经审计的 curated baseline | 把 baseline 伪装为当前 V3 completion |
| `results/_journal/archive/auto_report_*.md` | v1/v2 冻结原文 | 只读证据 | 清洗、截断、续写或回填 V3 |

本地目前没有 `auto_report.events.jsonl`，而 `auto_report.md` 明确显示 `Events parsed: 0`。这是空 V3 投影，不是缺口；只有下一次真实、合规的 producer 事件才能创建它。

### 已知 V3 路由漂移

| 位置 | 现象 | 计划修复 | 风险 |
|---|---|---|---|
| `self/dashboard/CLAUDE.md` | 已正确描述 JSONL/投影/baseline，但仍保留“`refresh.py` 待建”、过宽的“每个文件都有 Last updated”与 `scripts/experiments/` 路径表述 | 改为 V3-first 的短链接；将 timestamp 约束限定为手写 active Markdown；指向实际 `experiments/` 和当前生成器 | 低：只澄清已有规则 |
| `results/_journal/RULES.md` | V3 规则正确，但 v1/v2 模板在文件前部，容易被只读开头的人误当作新写法 | 增加位于文件开头的“新运行只读 V3”导航，保留 v1/v2 原文作为 archive compatibility | 低：不改变 V3 contract 或 archive |
| `文档规划/10_实验矩阵/16_4090小数据集运行与回收.md` | 把 `auto_report.md` 称作 append-only 运行日志 | 指向 JSONL 为审计权威，MD/HTML 为投影；不修改任何 journal data | 低：纠正导航语义 |
| `results/_journal/archive/README.md` | 仍把读者引向退役 `self/dashboard/PROGRESS.md` | 指向 `WORKPLAN.md`；明确 archive 只读且不承担 live state | 低：修复退役入口 |

## 治理关系

1. 根 `AGENTS.md` 是全部表中 Markdown 的最高约束：文档变更要核对链接/生成物/路径；任何生成 dashboard、HTML、CSV、figure 或 manifest 都不能手改。
2. `self/dashboard/CLAUDE.md` 只补充 dashboard 的文件分工，不得与根 `AGENTS.md` 竞争 Git、数据、cache 或正式实验权威。
3. `results/_journal/RULES.md` 只管理 AutoReport V3 及 archive 边界；它不取代 `VALIDATION_LOG.md`，也不取代 `WORKPLAN.md`。
4. `AGENTS_DRAFT.md` 可以在将来作为根说明重构的输入，但在被显式接受前不得在任何文档中被链接为现行指令。

## Self 文档逐项归位

“Obsidian/链接”指当前可读性和导航质量，而不是把 Markdown 源检查误报为实际 Reading View 验收；执行批次需在注册的 Obsidian vault 中再做一次目视检查。

| 文档 | 当前角色 | Obsidian / 链接状态 | 过时风险 | 建议归位与处理 |
|---|---|---|---|---|
| `self/README.md` | **live source（导航）**，但内容已落后 | 结构清楚；Fast Path 未从 WORKPLAN 开始，近期材料缺索引 | 高 | 继续作为 `self/` 入口；第一批改为 link-first current path，并移除不存在 `.bak` 条目 |
| `self/thesis_transition_memo.md` | **handoff / 战略背景** | 标题与边界清楚，但主要是 code-style 引用 | 高：仍称 active，正文含 2026-05 4-day window / 100 元预算 | 保留路径；加 current-pointer，降为战略 handoff，不作为执行入口 |
| `self/PROJECT_MASTER_CONTEXT.md` | **frozen background** | 有明确 reference/superseded 头 | 低 | 原地保留，README 作为背景入口，不做正文刷新 |
| `self/plan_flow_v2_delta.md` | **durable design** | 说明完整，但非链接化 cross-reference 偏多 | 中 | 保留为方法/指标历史补丁；只在定义变更时更新，不承载 live coverage |
| `self/flow.md` | **stale**（明确承认 code refs 漂移） | 已有风险提示；局部链接少 | 已知高 | 原地保留为架构快照；入口必须显示“仅结构参考，代码用 grep” |
| `self/宏观plan.md` | **frozen background** | 状态/替代入口完整 | 高但可控 | 原地只读；不再列入 current reading path |
| `self/experiment_params.md` | **stale reference** | 仅 code-style See also；参数/矩阵为早期假设 | 高 | 原地保留作 Phase B 历史参数；入口改指 canonical YAML/runbook，不作为可执行规范 |
| `self/generalization_experiment_checklist.md` | **frozen background** | 状态清楚，引用多为裸路径 | 高 | 保留为 2026-02 coverage snapshot；当前 coverage 只看 config inventory/WORKPLAN |
| `self/analysis_phase_a.md` | **frozen background** | Historical/superseded metadata 完整 | 低 | 保留作 Phase A 机制叙事溯源 |
| `self/GU代码综述_2026-02-16.md` | **durable design（代码导航）** | 阅读性良好，路径是历史式 | 中高 | 保留；下一次 code-map 维护时核实路径，未核实时标“implementation-era reference” |
| `self/paper_library_synthesis_2026-02-16.md` | **frozen background / literature reference** | 结构可读，缺当前 reading-note 入口 | 中 | 原地保留；从 related-work 入口链接，不应混作 current claim source |
| `self/paper_todo.md` | **frozen handoff / closed audit** | 完成状态和原始审计理由完整 | 低 | 保留正文；README 索引为“已关闭术语审计”，不重新当 TODO |
| `self/attack_flow.md` | **durable design，含 stale operational estimates** | 图示适合阅读；无状态头/链接 | 中高 | 保留为诊断流程图；加范围与当前 runner pointer，耗时只作历史估算 |
| `self/limitations.md` | **live-support evidence register** | 内容可读但缺更新时间/明确 current pointer | 中 | 继续维护实测限制与决定；仅写已验证限制，任务状态回链 WORKPLAN |
| `self/idea_cross_arch_consensus.md` | **handoff / future work** | metadata、关系链接具备 | 中 | 保留；明确为 future/resubmission research，不进入 rebuttal live queue |
| `self/research_path_degree_severity_decomposition.md` | **handoff，当前标记过强** | frontmatter 友好；策略范围与 current plan 冲突 | 高 | 保留假说与反证路径；状态改为 resubmission/dormant，强版不作为 rebuttal 工作项 |
| `self/neurips_2026_submission21636_reviews.md` | **handoff（当前审稿综合）** | note/callout 适合 Obsidian；无主页入口 | 中低 | 保持为 review synthesis；从 README、OB 评审区和 WORKPLAN 互链，不复制 live state |
| `self/related_work/NOTES.md` | **durable design / literature handoff** | 内容充分但导航弱 | 中 | 保留；增设 current-evidence 与 paper-review 的明确入口 |
| `self/related_work/concordance/report.html` | **derived frozen study report** | 浏览器可读；生成器存在 | 中 | 不手改；需要更新时改 study source/`gen_report.py` 后重生 |
| `self/related_work/concordance/HANDOFF.md` | **stale handoff** | 有复现入口但仍把 retired “proper TracIn”当 current 叙述 | 高 | 不删；第一批加历史状态与 `FINDING`/current evidence pointer，后续再决定是否重写结论 |
| `self/related_work/concordance/FINDING_tracin_misspecification.md` | **frozen background / corrected finding** | 已明确 historical、label retired、链接 current report | 低 | 维持原地，作为 HANDOFF 的上游纠偏入口 |
| `self/dashboard/WORKPLAN.md` | **live source** | Markdown 入口、链接索引和生成关系清楚 | 低 | 必须保持唯一 live hub；只放状态/原因/任务/链接 |
| `self/dashboard/progress.html` | **duplicate（合法派生）** | 浏览器看板 | 低 | 仅由 `refresh.py` 重生；不手改 |
| `self/dashboard/PROGRESS.md` | **duplicate（故意 redirect）** | 指向 WORKPLAN 的兼容入口 | 低 | 必须保留，不恢复旧正文 |
| `self/dashboard/config_inventory.html` | **duplicate（合法派生）** | cell 级浏览入口 | 中 | CSV 是 source；仅以 `gen_config_inventory.py` 重生 |
| `self/dashboard/CONFIG_INVENTORY_ACCEPTANCE.md` | **frozen background** | 已明确 frozen snapshot 与新 GraphRevoker 边界 | 低 | 保留验收证据；不当作 current matrix status |
| `self/dashboard/EXPERIMENT_DASHBOARD.md` | **frozen background** | 冻结头存在，但仍指向退役 PROGRESS | 中 | 保留历史矩阵/bug archive；第一批只修 redirect 到 WORKPLAN |
| `self/dashboard/METRIC_FIELD_SEMANTICS.md` | **durable design** | 语义边界清晰 | 中 | 保持为读取 `*_before` 前的定义门；仅随字段语义变化更新 |
| `self/dashboard/METRICS_CATALOG.md` | **live-support + durable design（混合）** | 定义可读，但维护规则仍把当前 bug 指向 frozen dashboard | 中高 | 先修 current links；后续评估是否将 live coverage 抽到 inventory/validation，定义留在本页 |
| `self/dashboard/PAPER_LIABILITIES_MAP.md` | **stale live-support document** | 表格可读；正文数据已被 E1/E4 后证据部分改变 | 高 | 保持当前 paper line-map 职能；必须先做 evidence refresh，再恢复 current 标签 |
| `self/dashboard/VALIDATION_LOG.md` | **live source（append-only evidence）** | 格式与用途清晰 | 低 | 必须持续 append-only；不要搬迁或压缩 |
| `self/dashboard/CLAUDE.md` | **durable design / local governance** | 表格清晰；V3/生成器部分有小漂移 | 中 | 第一批做 V3-first 和 generator/路径澄清；不重复根 AGENTS |

## 分批迭代计划

### Batch 0 — 先冻结边界与验收方式

**目的：** 让后续文档工作不把 frozen 文本、generated view、live state 或 V3 audit 混为一谈。

1. 将本计划作为唯一执行 checklist，不改 `self/` 正文。
2. 在执行任一后续批次前记录 `git status --short --branch` 与 `git worktree list`；只读取/编辑已列路径，不接触现有未提交文件。
3. 每次触及 `self/dashboard/` 时先读 `self/dashboard/CLAUDE.md`；每次触及 AutoReport 时先读 `results/_journal/RULES.md`。
4. 验收中把“Markdown 目标存在”“Obsidian Reading View 可读”“生成物由 generator 更新”分成三项，不互相代替。

### Batch 1 — 安全的入口、链接与归档说明修复

**可直接执行；不改实验语义、不移动资料、不改生成物、不删任何文件。**

| 顺序 | 改动源 | 操作 | 验收 |
|---:|---|---|---|
| 1 | `self/README.md` | 把 Fast Path 改为 `WORKPLAN → README role map → 按任务进入`；补 review、limitations、related-work/concordance、journal V3 的链接；删除不存在 `.bak` 的 inventory 行；历史资料只列为按需阅读 | 本地链接全过；Obsidian 可从一个入口区分 current/strategy/history |
| 2 | `self/dashboard/CLAUDE.md` | 明确 hand-written active Markdown 与 generated files 的维护差异；把 `refresh.py`、`gen_config_inventory.py`、`experiments/` 路径改为现行；链接 `RULES.md` 而非复制 V3 细节 | 不新增第二套 V3 规则；不要求 generated HTML 自带 `Last updated` |
| 3 | `results/_journal/RULES.md`、`results/_journal/archive/README.md` | 加 V3-first 导航；保留 v1/v2 模板/archive 原文；把 retired PROGRESS 指向 WORKPLAN | `RULES.md` 开头即可看出新运行只写 JSONL；archive 文本不动 |
| 4 | `文档规划/_文档地图.md` 与 `10_实验矩阵/16_4090小数据集运行与回收.md` | 加“运行审计 V3”入口；将 `auto_report.md` 改称投影并指向 JSONL/RULES；不复制 events 内容 | Wiki 和 Markdown 目标存在，OB map 不把投影说成 append-only 日志 |
| 5 | `self/dashboard/EXPERIMENT_DASHBOARD.md`、`self/dashboard/METRICS_CATALOG.md` | 将 retired `PROGRESS`/frozen-dashboard 的“当前”路由改为 WORKPLAN/VALIDATION_LOG；保留历史链接和历史事实 | 历史快照仍可读，所有 current-state 指针只到 WORKPLAN |
| 6 | `self/thesis_transition_memo.md`、`self/research_path_degree_severity_decomposition.md`、`self/related_work/concordance/HANDOFF.md` | 只加顶部 status/current-pointer：战略 memo、resubmission hypothesis、historical concordance handoff；不重写其证据正文 | 无文档继续被误读成 live execution plan 或 current TracIn acceptance source |

### Batch 2 — 有证据的 current-support 刷新

**前提：** 先锁定 `WORKPLAN`、accepted reports 和 source artifact；对每个结论标注 `current / historical / do_not_claim`，不以 mtime 代替证据。

1. 刷新 `self/dashboard/PAPER_LIABILITIES_MAP.md`：把 E1 Citeseer 50/50、E4 GraphRevoker 40/40 remote pass/local archive pending、E3 fresh K5 0/60、E8 formal environment block 等写为当前边界；逐项复核 Overleaf line map 后再改变 L1–L9 状态。
2. 收敛 `self/limitations.md`：保留可复核的 scaling/bug evidence，移除或显式标记已经被 WORKPLAN supersede 的运行下一步；把任务排序只链接回 WORKPLAN。
3. 收敛 `METRICS_CATALOG.md`：字段定义和 paper semantics 留在本页；coverage、bug status 与追踪入口用 links 指向 config inventory、VALIDATION_LOG、WORKPLAN，而不是手抄动态数字。
4. 对 `attack_flow.md`、`experiment_params.md`、`GU代码综述_2026-02-16.md` 做“保留正文 + 明确适用版本/替代入口”的薄层校准；遇到参数、代码路径或耗时判断，先核对 canonical runner/代码再写。

### Batch 3 — Obsidian 可读性与导航收敛

1. 将 active/handoff/frozen 三种文档统一为简短 metadata block：`Status`、`Role`、`Use this when`、`Current source / Superseded by`。不为 frozen archive 伪造新的更新时间。
2. 把重要的 code-style `See also` 路径替换成相对 Markdown 链接（Obsidian 兼容）；仅在 `文档规划/` 保留可解析的 `[[wiki link]]` 风格。
3. 在 `_文档地图.md` 增加一个不复制内容的“研究材料与证据边界”入口：指向 `self/README.md`、review synthesis、limitations、concordance finding、V3 rules；不把 WORKPLAN 内容搬进 OB。
4. 对宽表与数学内容用 Obsidian Reading View 目视检查；保留有对齐价值的表，按根 AGENTS 的数学分隔符规则修小问题，不把长表改成 callout 堆砌。

### Batch 4 — 需要用户决定的归档/删改

在得到明确选择前，默认是“原地保留 + 状态头 + 入口降级”，**不移动、删除、合并或改名**。

| 决策 | 选项 | 建议默认 | 为什么需要用户决定 |
|---|---|---|---|
| 早期资料物理归档 | A. 原地、索引化；B. 移入新的 `self/archive/`；C. 移到 `report/`/`docs/` | A | 移动 `analysis_phase_a`、`flow`、`宏观plan`、`experiment_params`、`generalization checklist`、代码综述、文献综合会改路径、外部 vault link 和历史引用 |
| 已关闭 `paper_todo.md` | A. 原地作 closed audit；B. 迁到 paper archive；C. 合并后删除 | A | 它含术语决策审计，合并/删除会损失可追溯性 |
| `thesis_transition_memo` 与 degree research path | A. 仅降为 handoff/resubmission；B. 以当前 rebuttal 方向重写；C. 移到 follow-up notebook | A | B/C 改变研究叙事，不是纯文档整理 |
| concordance HANDOFF 正文 | A. 顶部加历史/当前 pointer；B. 以新 TracIn evidence 整篇重写；C. archive only | A | 正文重写需要重新裁定哪些数值、术语和 production recommendation 仍有效 |
| Paper Liabilities Map | A. 用 current evidence 全量刷新；B. 冻结旧 map，另建新 map | A，但须先确认目标 paper revision scope | 该表直接影响可保留 claim、Overleaf 行号与 rebuttal/resubmission工作量 |

### Batch 5 — 最终验证与交付

1. 运行仅针对改动 Markdown 的本地链接检查；排除 fenced code，分别报告真实坏链与示例文本。
2. 在 Obsidian Reading View 打开 README、文档地图、WORKPLAN、PAPER_LIABILITIES_MAP 和至少一个 historical/handoff 样本，检查表格、callout、中文路径和数学。
3. 对 `progress.html`、`config_inventory.html`、concordance `report.html` 只验证其 generator/source relationship；除非相应 source/generator 变更，禁止触碰派生文件。
4. 若变更 WORKPLAN，运行 `E:/conda_package/envs/gnn/python.exe scripts/dashboard/refresh.py` 并核对生成看板；本计划本身不触发此操作。
5. 检查 `git diff --check`、`git diff --name-status` 和 `git status --short`，确保只出现批准的文档源文件及其合法生成物，且用户原有未提交文件仍存在。

## 必须保持 live 的文件

- `self/dashboard/WORKPLAN.md`（唯一 live operational source）
- `self/dashboard/VALIDATION_LOG.md`（append-only 人/AI evidence）
- `self/dashboard/METRICS_CATALOG.md`（定义保留；其 coverage 必须链接 live evidence）
- `self/dashboard/PAPER_LIABILITIES_MAP.md`（刷新后继续作为 paper line-map）
- `self/dashboard/config_inventory.csv`（数据 source；虽不在上述 32 份人读清单内）及其生成的 HTML
- `self/limitations.md`（仅限实测限制与 decision status，任务排序回链 WORKPLAN）
- `self/README.md`（导航 source，不复制 live 内容）
- V3 的 `RULES.md`、JSONL 原件、baseline 与投影视图（各自按前述边界维护）

其余 `self/` 文档以 durable design、frozen background 或 handoff 身份存在；它们可被链接和追溯，但不能覆盖上述 live sources。

## 本计划的完成条件

- 每份 `self/` 文档都有角色、过时风险和归位路径；generated duplicates、redirects 和 archive 不被误删。
- 所有 current-state 入口只指向 WORKPLAN；所有 V3 运行审计入口只说明 JSONL 为原件。
- dashboard 的 human validation 与 journal 的 machine events 被明确分开。
- 物理归档、删除、合并、重写研究叙事和改写 paper liabilities 之前都有用户选择或可复核 evidence gate。
