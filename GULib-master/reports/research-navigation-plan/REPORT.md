# 研究入口整理方案

2026-10-23 · 供讨论的整理方案 · 未实施目录迁移、入口改写或科学结论更新

> 后续实施：入口整理及目录命名已按用户后续决定完成。当前目录采用单实验 `EXP-NNN/`、跨实验组合编号 `EXP-NNN_EXP-NNN/`；下文保留原讨论方案，现行规则见 [Work Plan 说明](../../self/research/README.md)，本次结果见[目录命名整理](OTHER_DIRECTORIES_REPORT.md)。

## 1. 建议先做什么

沿用论文结果章已有的 Q1–Q3，以“研究问题 → 对应实验 → 指定版本的分析 → 论文章节”组织阅读。保留 Work Plan 的实验管理职责，在现有论文写作主页面维护一张精简的论证导航表。先把入口、版本和用途讲清楚，再决定是否需要改目录。

当前核对到 31 份实验状态记录、27 份分析 JSON、13 个分析子目录。分析 JSON 的存在不等于分析已经完成；分析完成也不等于当前版本已被科学接受。本方案只检查本地组织、记录与引用，没有重新计算实验结果或核验远端状态。

本次新增的仅是这份方案及其 HTML 阅读版；现有入口、实验记录、分析记录、论文内容和文件路径均未修改。

## 2. 现有入口为什么难读

| 问题 | 已核对的具体例子 | 整理方向 |
|---|---|---|
| 三套问题组织没有明确互相解释 | framework.json 有 X1–X8；第 5 章保留四个实验设计问题；第 6 章采用 Q1–Q3 | 说明三者分别是研究主题、实验设计问题、论文结果问题，建立对应表，不增设第四套编号 |
| 名称混合了身份、参数、日期和主题 | EXP-013、h64-theory-20260924、shard300-20261023、validation-20260924 并列 | 阅读标题先说明内容，附实验编号和运行版本；路径暂时保留 |
| 写作入口落后于分析入口 | 第 6 章仍称 EXP-079/e79r5 为最新主分析；EXP-079.json 已指向 shard300 内 e79r6 新协议分析 | 先标出章节引用批次和待复核的新批次，逐项核对后再更新正文，不能全局替换路径 |
| 接受决定与新版分析不是同一范围 | EXP-011 的 analysis.note 明确新版待科学验收，但 decision.state 仍是 accepted，且属于历史分析 | 展示决定对应的报告和运行版本，不将顶层 accepted 直接贴到新版报告 |
| 阶段材料容易被当成当前状态 | h64-theory 的 README 写候选表尚未执行；EXP-067/068 后续校准验证已另有记录 | 标为“历史参数候选推导”，从实验分析记录进入后续验证 |
| 主页面与结果章结构不同步 | 论文主页面的写作落位仍主要指向旧 6.1–6.6；结果章已把这些材料放在 Q1–Q3 后作为支撑分析 | 主导航以 Q1–Q3 为先；旧小节明确其支撑用途，不按旧编号解释当前主线 |

这些问题不说明历史材料无用。主要缺口是：读者无法迅速判断某份材料回答什么问题、属于哪次运行、现在适合怎样使用。

## 3. 问题、实验分析与论文章节的对应

以下是建议的阅读和写作组织，不是新的科学接受决定，也不承诺所有证据都进入正文。Q1–Q3 沿用结果章现有问题；支撑行采用主题名称，不新增 Q4、Q5。

| 阅读问题 | 对应研究主题 | 建议先读的实验与分析 | 论文落点 | 使用边界 |
|---|---|---|---|---|
| **Q1：策略性请求改变了什么？** | X3 GU 响应；X4 效应与副作用 | EXP-011/e11r1 主矩阵；EXP-079/e79r6 的原值、Random 对照、同请求 Retrain 与预测不一致率；EXP-012、051 作独立支撑 | 第 4 章定义；第 5 章比较口径；第 6 章 Q1；第 7 章解释 | 准确率、相对 Random 增量、GU–Retrain 效用差、预测不一致率分别解读。011/079 新批次待科学验收 |
| **Q2：不同策略能否形成可区分的 GU 响应？** | X3 GU 响应；X4 效应；X5 预算 | EXP-079/e79r6 响应图谱与敏感性；EXP-011/e11r1 主矩阵；EXP-080 五策略补充与预算分析 | 第 6 章 Q2；第 7 章异质性讨论；完整方法与策略面板放附录 | 区分绝对效用与相对响应形状；保留全部相关 GU/selector。080 与新协议批次分别呈现，不拼成同一实验矩阵 |
| **Q3：换一个 surrogate 后，策略差异还能保留吗？** | X7 代理迁移 | EXP-079/e79r6 十 seed 分析优先；EXP-013 三 seed 迁移报告作为较早批次与补充 | 第 3 章权限定义；第 5 章固定目标；第 6 章 Q3；第 8 章外推边界 | 选点模型迁移不等于目标 Backbone 泛化；不同批次不合并为十三个 seed；不将条件性保留表述成普遍指纹 |
| **选点机制与近似：为什么比较这些策略？** | X1 选择机制；X2 近似有效性 | EXP-031 选集/排名；EXP-032 当前 3000 轮 Retrain 对照；EXP-053 RR 配置诊断；EXP-039 保留独立待回答问题 | 第 4 章策略说明；第 5 章设计依据；第 6 章支撑分析；附录 B | Retrain 结果不是近似 GU 误差证据；053 的现有用途决定不支持独立论文贡献；039 尚无独立分析 |
| **预算：响应是否随删除比例改变？** | X5 预算与消融 | EXP-080/full-20261021 总报告，再读 STRATEGY_REPORT；EXP-032 的 Retrain 预算对照独立引用 | 第 6 章 Q1/Q2 的预算扩展；第 5 章预算协议；附录完整曲线 | 不新增论文一级问题。080 已保存分析但未科学接受；当前主要范围是 Cora/CiteSeer，不能扩展到未覆盖条件 |
| **实施条件：观察是否建立在有效的训练与数值设置上？** | 实验有效性的支撑材料；不强行塞入某个经验发现 | EXP-059、061、062、065–068；EXP-078、081–083 的诊断/门禁记录 | 第 5 章实现与证据要求；附录 D/E；第 8 章限制 | 数值稳定、执行门禁通过和软件交付不等于遗忘正确性或方法普遍有效 |
| **成本与泛化：还有哪些结论不能写？** | X6 泛化规模；X8 成本复用 | EXP-014、058、021、022、056；EXP-039 也保留为独立缺口 | 第 6 章有证据才写结果；第 8 章局限；附录方法细节 | 无分析的项目显示缺口；不能用缓存命中访问时长代替冷启动耗时；大图选点可行性不等于大图 GU 有效性 |

### 第 5 章的四个问题怎样接入

| 现有实验设计问题 | 对应主题 | 与结果章的关系 |
|---|---|---|
| 选择机制是否产生不同删除集合 | X1 | Q2 的前置支撑；选集不同本身不构成 GU 响应不同 |
| reference/proxy 是否对齐既定目标 | X2 | 策略代表选择与附录支撑，不预设近似正确 |
| 相对同预算 Random，GU outcome 如何变化 | X3、X4 | 直接对应 Q1，并向 Q2 提供对照 |
| 响应如何随 GU、数据集、权限变化，与 Retrain 差距多大 | X3、X4、X7；预算扩展关联 X5 | 对应 Q1–Q3；X6、X8 作为范围与成本问题独立列出 |

第 5 章不必立即改成三个问题。先添加上述关系说明，避免把实验设计问题与结果叙事问题误当成同一编号系统。framework.json 的 X1–X8 继续用于研究覆盖面，不要求八个主题各占一个论文结果小节。

## 4. 最短阅读路线

1. [论文写作主页面](../../../../OpenGU-DocMap/40_论文写作/40_论文写作.md)：理解论文主线和章节分工。其写作落位表按本方案更新后成为统一论证导航。
2. [结果章](../../../../OpenGU-DocMap/40_论文写作/06_结果.md)：读 Q1–Q3；当前正文仍以 e79r5 为主，阅读时保留这一批次限定。
3. [EXP-011/079 新协议总报告](../../self/research/analyses/EXP-011_EXP-079/REPORT.html)：看 e11r1/e79r6 的新结果与协议差异，再分流到 [EXP-011 图册](../../self/research/analyses/EXP-011_EXP-079/EXP011_REPORT.html) 和 [EXP-079 图册](../../self/research/analyses/EXP-011_EXP-079/EXP079_REPORT.html)。这一步不自动替换正文。
4. [EXP-080 预算总报告](../../self/research/analyses/EXP-080/full-20261021/REPORT.html) → [五策略补充](../../self/research/analyses/EXP-080/full-20261021/STRATEGY_REPORT.html)：补预算与 IM 比较；保留该批次原训练协议。
5. [EXP-013 分析记录](../../self/research/analyses/EXP-013.json)、[EXP-032 分析记录](../../self/research/analyses/EXP-032.json)、[EXP-053 分析记录](../../self/research/analyses/EXP-053.json)：需要解释迁移、近似或 RR 诊断时再读。
6. 查运行、依赖和下一步时回到 [Work Plan](../../self/research/index.html)；查参数校准与执行条件时读对应 EXP 记录，不从历史 README 猜测当前进度。

## 5. 入口整理的具体改动建议

| 现有位置 | 建议改动 | 仍由谁维护事实 |
|---|---|---|
| [self/README.md](../../self/README.md) | 保留总入口；明确“实验进度看 Work Plan、论证关系看论文主页面、读文献看文献入口”。修正“当前任务与依赖”笼统归 WorkBlock 的表达 | 实验归 Work Plan；开发归 WorkItem；论文归 DocMap |
| [self/research/README.md](../../self/research/README.md) | 开头补一段用途说明和论文论证导航链接，保留字段/维护命令 | 本文件继续拥有 Work Plan 维护约定 |
| [DocMap 文档地图](../../../../OpenGU-DocMap/_文档地图.md) | “当前要读”增加论文论证导航入口；技术操作项按原职责保留 | 文档地图只导航，不复制实验状态 |
| [论文写作主页面](../../../../OpenGU-DocMap/40_论文写作/40_论文写作.md) | 将“写作落位与当前结果复核”更新为本方案第 3 节精简矩阵，区分主线、支撑、缺口；这是唯一人工维护的跨实验—章节对应表 | 问题—实验—章节关系由此维护；不再另建一份同职能门户 |
| [第 5 章总览](../../../../OpenGU-DocMap/40_论文写作/05_实验设计/00_实验设计总览.md) | 给四个设计问题加上通往 Q1–Q3/支撑分析的说明 | 本章仍只维护设计与证据要求 |
| [第 6 章结果](../../../../OpenGU-DocMap/40_论文写作/06_结果.md) | 标明正文绑定 e79r5；另列 e79r6/e11r1、080 待复核入口；核对结论、表值与协议后再逐段切换 | 章节拥有正文；分析报告拥有证据与解释范围 |
| analyses/EXP-NNN.json 与其报告 | 引用标签使用语义标题，并在需澄清的记录中说明推荐报告版本、历史报告角色及决定适用范围；通过既有 evidence/note 表达 | 实验分析记录拥有证据入口，不新建另一套状态数据库 |
| Work Plan 的 HTML 页面 | 本阶段无需改布局；如果上述源记录标签有变更，通过现有生成器重建 | 禁止手改 index.html、catalog.html 等生成物 |

静态论文导航只保留问题、实验、章节与用途，不手工复制实时运行状态或科学接受徽标。需要判断完成与接受时，链接到分析记录；特别是新旧批次并存时，必须读 note 和决定所指的证据。

如果未来要让页面自动判断“决定与当前分析是否同批次”，这属于生成器/数据合同的开发改动，应独立定义范围。本次入口整理不暗中引入这个功能。

## 6. 命名章法：身份、主题、批次分开

问题确实不只是名称不美观：`shard300` 只透露一个参数，无法告诉读者这是两项主实验的新版联合分析；`validation` 无法说明验证的是数值稳定性、执行流程还是科学假设；`theory` 也可能让人误以为得到了理论保证。

建议优先统一显示标题，路径暂不改。显示标题用“实验编号 · 回答的问题或分析主题”，副标题再写 run ID、训练协议、日期和范围。

| 现有名字或路径 | 建议的入口显示名称 | 实际归属与角色 |
|---|---|---|
| EXP-013/ | EXP-013 · 代理选点迁移：三 seed 分析 | 单实验；补充与较早证据，十 seed 扩展见 079 |
| EXP-080/full-20261021/ | EXP-080 · 删除预算与多 GU 响应：完整覆盖范围分析 | 单实验分析批次；范围在副标题注明 Cora/CiteSeer、2016 条件及排除项 |
| EXP-080/.../STRATEGY_REPORT | EXP-080 · 五策略响应对照与 IM 补充 | 同批次专题；不与总报告竞争“最新”入口 |
| shard300-20261023/ | EXP-011 / EXP-079 · 主矩阵与迁移响应联合分析 | 跨实验专题；副标题：e11r1 / e79r6，聚合损失修正，分片训练 300 轮 |
| h64-theory-20260924/ | EXP-067 / EXP-068 · H64 数值参数候选推导 | 历史推导批次；有限谱估计不等于完整谱保证，后续校准验证另见记录 |
| validation-20260924/ | EXP-067 / EXP-068 · 固定参数验证分析脚本 | 目前只有共享分析脚本，不能当作独立报告入口 |
| AAGU-032-AAGU-053-3000-only-paper-analysis-20260923.md | EXP-032 / EXP-053 · 3000 轮结果的论文用途分析 | 跨实验报告；旧文件名保留原身份痕迹，显示名称用现行 EXP 编号 |
| AAGU-032-AAGU-053-3000epoch-comparison-20260923.md | EXP-032 / EXP-053 · 训练协议变更对照 | 历史协议比较，不能与 current-only 报告混成同一条件结果 |

后续新增材料建议遵守五条简单规则：

- 单实验分析放在所属 `EXP-NNN/` 下；一个独立运行分析批次优先使用真实 run ID。一个报告汇总多次运行时用内容主题，正文列出完整运行身份，不虚构一个运行 ID。
- 跨实验分析按主题命名，不伪装成新的 EXP 实验。报告头明确关联哪些实验，及各自适用范围。
- 日期表示批次时间，不承担内容分类；参数放副标题或元数据，只有参数本身是研究对象时才放主标题。
- 总阅读入口使用 `REPORT.md` / `REPORT.html`；确有独立问题的专题使用有意义的名称，例如 `strategy-response_REPORT.md`。避免 final、latest、new、v2 作为主要内容标识。
- 报告首部写清：研究问题、关联实验、run ID/执行 SHA、范围、推荐阅读顺序、决定适用批次；图表名说明变量或比较对象。字段只引用既有身份，不改历史 ID。

这些是新增文件与显示标题的建议，不是本次批量重命名指令。将来若迁移，需同时更新所有引用和生成器路径；不通过兼容副本、重定向或重复索引长期维持两套位置。

## 7. 实施顺序与完成标准

| 顺序 | 工作 | 完成标准 |
|---|---|---|
| 1 | 整理现有入口和唯一论证导航表 | Q1–Q3 都能直接找到实验、明确版本的报告和章节；支撑与缺口有单独位置 |
| 2 | 澄清新旧批次及决定范围 | 011/079 新版不继承历史 accepted；080 与新分片协议分开；013 与079重复数不混用 |
| 3 | 统一显示标题和报告用途 | 本方案列出的模糊目录均有语义名称、归属实验和主阅读入口；脚本、推导、科学报告不会混淆 |
| 4 | 对齐章节入口和既有生成页面 | 失效的“最新”说法已修正；更新源记录后运行既有生成器与链接检查；不借整理新增科学结论 |
| 5 | 评估是否需要物理迁移 | 只有入口整理后仍有明显维护困难，才另列精确迁移清单；本阶段不执行 |

本方案建议第一轮只做 1–4，并且先完成入口澄清，再推进正文证据批次更新。正文结论修订需要逐项核对，不能把目录整理当作科学审阅。

## 8. 核对来源与局限

- [Work Plan 约定](../../self/research/README.md)、[目录指导](../../self/research/AGENTS.md)、[研究主题 X1–X8](../../self/research/framework.json)、[历史迁入说明](../../self/research/MIGRATION.md)。
- 本地 `self/research/experiments/EXP-*.json` 共 31 份；`self/research/analyses/EXP-*.json` 共 27 份。后者包括尚未分析条目，不能作为完成数量。
- [EXP-011 分析记录](../../self/research/analyses/EXP-011.json)、[EXP-079 分析记录](../../self/research/analyses/EXP-079.json)、[EXP-080 分析记录](../../self/research/analyses/EXP-080.json)用于核对当前报告入口和版本边界。
- [H64 候选推导说明](../../self/research/analyses/EXP-067_EXP-068/README.md)、[共享验证脚本](../../self/research/analyses/EXP-067_EXP-068/analyze.py)用于确定专题角色；没有执行这些实验脚本。
- 论文结构以当前 DocMap 独立章节为准；[投稿源码入口说明](../../report/paper/README.md)明确 Overleaf 与 DocMap 章节尚非同一更新状态，本方案不声称已对齐正式稿。
- report-writing 技能及其文件地图包含早期论文路径和历史经验判断；本方案仅使用其证据优先原则及已确认的写作归属，不将其中旧结果或旧投稿格式当成当前结论。
- 本方案是组织建议，未检查全部历史报告的统计正确性，未宣布缺少分析 JSON 的实验没有执行，也未改变任何科学接受状态。

## 附录：31 项实验的导航覆盖

下表是本次整理建议的完整覆盖清单，角色为建议落位；不是新的实验计划或状态台账。编号均链接到现有本地状态记录。分析入口有则链接，没有则明确记录文件未见。

| 实验 | 当前记录标题 | 建议角色与落点 | 已保存分析入口 |
|---|---|---|---|
| [EXP-007](../../self/research/experiments/EXP-007.json) | 最小正式实验 Gate | 执行门禁 → 第5章 / 附录D | [分析记录](../../self/research/analyses/EXP-007.json) |
| [EXP-008](../../self/research/experiments/EXP-008.json) | K5 噪声参照 | 小预算噪声参照 → Q1支撑；不校正其他预算 | [分析记录](../../self/research/analyses/EXP-008.json) |
| [EXP-010](../../self/research/experiments/EXP-010.json) | Flip/Hop 指标补齐 | 预测/跳数指标完整性 → Q1支撑 | [分析记录](../../self/research/analyses/EXP-010.json) |
| [EXP-011](../../self/research/experiments/EXP-011.json) | GU 主矩阵 · Table02 | 主矩阵 → Q1 / Q2 | [分析记录](../../self/research/analyses/EXP-011.json) |
| [EXP-012](../../self/research/experiments/EXP-012.json) | 退化分解与副作用分析 | 效应分解与副作用 → Q1 / 附录E | [分析记录](../../self/research/analyses/EXP-012.json) |
| [EXP-013](../../self/research/experiments/EXP-013.json) | 代理模型选集迁移 | 三seed代理迁移 → Q3补充 | [分析记录](../../self/research/analyses/EXP-013.json) |
| [EXP-014](../../self/research/experiments/EXP-014.json) | ogbn-arxiv Selector 可运行性 | 大图GU扩展 → 泛化缺口 / 第8章 | [分析记录](../../self/research/analyses/EXP-014.json) |
| [EXP-015](../../self/research/experiments/EXP-015.json) | IF 分阶段实验设计 | 历史设计 → 031/032的来源 | [分析记录](../../self/research/analyses/EXP-015.json) |
| [EXP-021](../../self/research/experiments/EXP-021.json) | 小图 D-full 计时与拟合 | 小图计时 → 成本缺口 | [分析记录](../../self/research/analyses/EXP-021.json) |
| [EXP-022](../../self/research/experiments/EXP-022.json) | 大图 D-full 计时与外推 | 大图计时 → 成本与规模缺口 | [分析记录](../../self/research/analyses/EXP-022.json) |
| [EXP-027](../../self/research/experiments/EXP-027.json) | IF-family collateral 证据恢复 | 旧collateral证据恢复 → Q1支撑缺口 | [分析记录](../../self/research/analyses/EXP-027.json) |
| [EXP-031](../../self/research/experiments/EXP-031.json) | IF 选择机制与完整排名 | 选点与排名 → X1 / 第4章 / 附录B | [分析记录](../../self/research/analyses/EXP-031.json) |
| [EXP-032](../../self/research/experiments/EXP-032.json) | D-full 近似对照与 Retrain 效果 | 近似与Retrain → X2/X5 / 支撑分析 | [分析记录](../../self/research/analyses/EXP-032.json) |
| [EXP-039](../../self/research/experiments/EXP-039.json) | Graph CP3/CP6 独立比较 | CP3/CP6独立比较 → X2 / 独立待回答问题 | [分析记录](../../self/research/analyses/EXP-039.json) |
| [EXP-051](../../self/research/experiments/EXP-051.json) | Random 多选集响应分布 | 随机请求波动 → Q1支撑 | [分析记录](../../self/research/analyses/EXP-051.json) |
| [EXP-053](../../self/research/experiments/EXP-053.json) | IM 采样稳定性与删除效果 | RR配置诊断 → 策略说明 / 附录 | [分析记录](../../self/research/analyses/EXP-053.json) |
| [EXP-056](../../self/research/experiments/EXP-056.json) | 大图 RR-1024 Selector 可行性 | 大图RR选点 → 成本可行性，分析待补 | [分析记录](../../self/research/analyses/EXP-056.json) |
| [EXP-058](../../self/research/experiments/EXP-058.json) | Backbone 泛化对照 | 目标Backbone泛化 → 第8章缺口 | [分析记录](../../self/research/analyses/EXP-058.json) |
| [EXP-059](../../self/research/experiments/EXP-059.json) | GIF/IDEA 作者参数收敛诊断 | GIF/IDEA收敛诊断 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-059.json) |
| [EXP-061](../../self/research/experiments/EXP-061.json) | 作者超参基础模型 PT | 基础模型权重交付 → 第5章 / 附录D | [分析记录](../../self/research/analyses/EXP-061.json) |
| [EXP-062](../../self/research/experiments/EXP-062.json) | 065–068 Batch · GIF/IDEA 固定 PT 校准与验证 | 固定PT校准验证批次 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-062.json) |
| [EXP-065](../../self/research/experiments/EXP-065.json) | Cora H16/H64 固定 PT 参数校准 | Cora参数校准 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-065.json) |
| [EXP-066](../../self/research/experiments/EXP-066.json) | Cora H16/H64 固定参数 Random 请求验证 | Cora固定参数验证 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-066.json) |
| [EXP-067](../../self/research/experiments/EXP-067.json) | CiteSeer H64 固定 PT 校准与验证（H16暂缓） | CiteSeer校准验证 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-067.json) |
| [EXP-068](../../self/research/experiments/EXP-068.json) | PubMed H64 固定 PT 校准与验证（H16暂缓） | PubMed校准验证 → 第5章 / 附录E | [分析记录](../../self/research/analyses/EXP-068.json) |
| [EXP-078](../../self/research/experiments/EXP-078.json) | GCN H16/H64 baseline P0终轮与checkpoint诊断 | 基础模型checkpoint诊断 → 第5章 / 附录D | 未见独立分析JSON；不据此判断执行情况 |
| [EXP-079](../../self/research/experiments/EXP-079.json) | Surrogate 条件性迁移的多 seed 验证（总10个） | 十seed条件性迁移与响应 → Q1 / Q2 / Q3 | [分析记录](../../self/research/analyses/EXP-079.json) |
| [EXP-080](../../self/research/experiments/EXP-080.json) | 删除比例与多GU效用响应：Retrain对照初步分析 | 五策略与预算响应 → Q1 / Q2扩展 | [分析记录](../../self/research/analyses/EXP-080.json) |
| [EXP-081](../../self/research/experiments/EXP-081.json) | GraphRevoker 随机删除5节点诊断 | GraphRevoker小删除诊断 → Q1支撑候选 | 未见独立分析JSON；不据此判断执行情况 |
| [EXP-082](../../self/research/experiments/EXP-082.json) | GraphEraser / GraphRevoker 分片训练轮数隔离诊断 | 分片训练轮数诊断 → 第5章 / 协议说明 | 未见独立分析JSON；不据此判断执行情况 |
| [EXP-083](../../self/research/experiments/EXP-083.json) | 300轮分片训练与聚合损失修正正式最小 Gate | 分片新协议正式Gate → 第5章 / 附录D | 未见独立分析JSON；不据此判断执行情况 |
