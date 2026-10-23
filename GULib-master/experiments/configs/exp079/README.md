# EXP-079 · Surrogate 多 seed 验证

## AAGU-096 最终效果测试：seed212 的252格冷热 Gate

[seed212配置](cache_speed_gate_s212.yaml)保留Cora、CiteSeer、PubMed，每个数据集12种选点条件×七种方法，共252格。与seed2024 Gate相比只改变训练seed，并显式声明七种方法使用原默认 `gu_cache=reuse`；预算0.1、Dataset/Split、方法参数和两套配对评价保持。两份Recipe绑定同一配置SHA和指纹，RID分别为e79g8c/e79g8w，均通过普通 `experiments/run.py --syncmate` 执行。

| 轮次 | Recipe | RID | 硬上限 |
|---|---|---|---|
| 冷轮 | [252-s212-cold](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-252-s212-cold.yaml) | e79g8c | 1800秒 |
| 热轮 | [252-s212-warm](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-252-s212-warm.yaml) | e79g8w | 1800秒 |

2026-10-13只读预检在已安装版本35f7df93上确认252/252方法Output、36/36 Selection精确命中，无关联Evaluation；原始逐点证据及报告位于 `.syncmate/exp079-gate-precheck-096-20261013/`。这份预检不替代最终执行版本的检查：096软件接受后，将代码、配置与两份Recipe统一落到main、同步一次；再由正式preflight核对三端同SHA、GPU、正式数据、锁及新RID占用，并以该执行版本只读复核每个真实请求。任何Output/Selection MISS或关联Evaluation已生成都停止冷轮准备，保留证据并由Work Plan调整未提交身份；不删除或改写Artifact制造冷态。

两轮各252点、684个Evaluation请求（252基础、216 utility/retrain-gap、216 flip-hop）。冷轮要求上游全部HIT、684次Evaluation MISS并计算保存；冷轮完整执行、可信回传及项目核验通过后才提交热轮，热轮要求684次Evaluation HIT且计算回调全部未调用。两份Recipe采用现有数据声明接口，不能单靠文件名强制这些缓存状态：实际状态须在启动前复核，并在回传后自动核验。两轮各505份结果通过SyncMate收集、SHA核验和项目结果检查；AutoReport原始事件快照必须绑定各自RID和同一完整执行SHA。

回传后使用[效果核验器](../../../scripts/verify_exp079_cache_gate.py)。以下大写参数由本次实际回执和事件快照填写，不能复制历史值：

```powershell
E:/conda_package/envs/gnn/python.exe scripts/verify_exp079_cache_gate.py `
  --cold-job COLD_JOB_ID --warm-job WARM_JOB_ID `
  --cold-audit COLD_AUDIT_SNAPSHOT --warm-audit WARM_AUDIT_SNAPSHOT `
  --expected-sha LANDED_EXECUTION_SHA --output EFFECT_CHECK_JSON
```

核验器默认消费本节两份seed212 Recipe，检查完整回传、配置/代码/运行身份、三数据集各84格、七方法各36格、上游HIT且不调用producer、冷热684次指标缓存状态、无失败或悬空审计事件，以及252格逐点指标/Selection文件和Output/Selection/Evaluation引用一致。Runner完整作业wall取原receipt的started_at至finished_at；排队独立列出，回传不计入。AutoReport条目分项与方法条目分项分别输出，不能相加或冒充完整作业时间。核验失败返回非零，不提交、不重试、不更新Work Plan或科研接受。

不补做修复前前测：以已核验的seed2024 **790秒/91秒**为历史工程基准，seed42的941秒/278秒仅作更早参照。核验结果列出耗时变化及是否低于300秒，但它们是观察项，不是预设通过阈值；披露跨seed、GPU/数值环境和主机负载差异后，由用户判断实际改善。当前只完成软件/Recipe准备，正式效果仍为NOT OBSERVED，既不代表2520点全矩阵完成，也不自动启动两轮。

## seed2024 的252格冷热 Gate（2026-10-13）

用户授权在 AAGU-095 已交付版本上运行 [seed2024 配置](cache_speed_gate_s2024.yaml)：Cora、CiteSeer、PubMed，各12种选点条件×七种方法，共252格；预算、Split、参数及评价均沿用完整矩阵。只执行本组冷热两轮，不重跑前测；以已完成的 seed42 `e79g4c` 941秒和 `e79g4w` 278秒作为历史工程参考。

| 轮次 | Recipe | RID | 硬上限 |
|---|---|---|---|
| 冷轮 | [252-s2024-cold](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-252-s2024-cold.yaml) | e79g7c | 1800秒 |
| 热轮 | [252-s2024-warm](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-252-s2024-warm.yaml) | e79g7w | 1800秒 |

提交前的只读检查已按当前请求匹配36组Selection及252份Output，未发现关联Evaluation。正式结果仍须验证Score/Selection/Output适用请求全部命中、producer未调用，冷轮684个Evaluation请求首次计算保存，热轮全部命中；两轮逐格指标及Selection/Output引用一致，回传、SHA-256、可信索引和项目核验通过。热轮仅在冷轮完整核验后提交；不清空缓存、不自动重试或扩大到2520格。

比较采用完整Runner作业起止耗时，排队和回传另列。历史冷轮已有19个Evaluation HIT、665个MISS，本轮预期684个MISS，且训练seed不同；据实报告工程改善，不能把历史对比当作严格同seed受控实验。每轮全MISS串行预算沿用3×7576=22728秒，仅为预算记录，不是缓存命中耗时预测。

## 历史84格准备（已由上述252格范围替代）

为缓存访问性能优化保留两组 Cora 请求：沿用正式 Split、12 个选点条件、七种方法、预算和评价定义，仅从完整 EXP-079 表选择不同的既有训练 seed。不增加 Cache 测试环境，不删除或修改正式 Artifact 来制造 MISS。

| 用途 | 配置 | 首轮 RID / Recipe | 热轮 RID / Recipe |
|---|---|---|---|
| 优化前基线 | [seed 212](cache_speed_gate_cora_s212.yaml) | e79g5c / [s212-cold](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora-s212-cold.yaml) | e79g5w / [s212-warm](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora-s212-warm.yaml) |
| 优化后验证 | [seed 2024](cache_speed_gate_cora_s2024.yaml) | e79g6c / [s2024-cold](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora-s2024-cold.yaml) | e79g6w / [s2024-warm](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora-s2024-warm.yaml) |

每组 84 格；每轮 600 秒硬上限，属于有界验证而非完成时间承诺。每组预计有 84 个基础指标请求、72 个 utility/retrain-gap 请求及 72 个 flip-hop 请求，共 228 个 Evaluation 请求；Retrain 自身不做配对评价。两份配置及四份 Recipe 已通过既有解析、dry-run、绑定 Dataset/Split 计数读取和装配验证；准备不代表已提交或已通过正式 preflight。

首轮必须核验所选请求是 Output HIT、Evaluation 尚未生成；首次计算和保存指标后，完成回传及结果核验，再运行同组热轮。登记时只读库存显示两组候选 Output 均没有关联 Evaluation，但候选库存不等于当前配置 84 格的精确覆盖；启动前以当前身份核验，启动后按逐项审计统计，出现非预期 Output MISS 或首轮指标已热则该轮不满足此对照口径，不删除缓存或自动重试。

用户已确认这两组可用于工程性能对比：数据集、矩阵形状、方法和缓存起点相同，训练 seed 差异随结果记录，不作为阻断条件。比较完整作业耗时及查询、输入读取、公式、写入校验、审计/终态报告等已有逐项计时；同时记录每层 HIT/MISS 和真实计算调用，不能仅凭 SQL 次数减少宣称整轮提速。优化后必须保持指标、Output/Selection 引用和缓存身份语义正确。历史 Cora seed42 的 263.62 秒是单元累计，不与新 gate 的整轮 wall 混用。

上述为2026-10-12的准备方案。2026-10-13的 `e79g5c` 在实验开始前因CUDA不可用失败；用户随后取消前测，改为本页顶部的seed2024三数据集252格冷热两轮。旧配置及声明用于追溯原准备与失败任务，不表示仍需执行其余三轮。

一份完整实验表：[surrogate_multiseed.yaml](surrogate_multiseed.yaml)。
历史第四轮声明：[opengu-exp079-surrogate-multiseed-r4.yaml](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r4.yaml)。前三轮 [e79r1声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed.yaml)、[e79r2声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r2.yaml)与 [e79r3声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r3.yaml)保留，用于核对历史任务身份；这些身份不可再次提交。

完整矩阵包含三数据集、十训练seed、GCN direct与SGC/GAT/GIN、r_point/gt_full、Random/Degree、六GU及Retrain，共2520格。旧三seed对应756格，新增七seed对应1764格；精确缓存命中时复用已有计算，评价照常执行。参数只由YAML拥有。

历史第四轮Recipe使用 `experiment_id: exp079-surrogate-multiseed`、`run_id: e79r4`，一次提交整张表。当轮使用六小时上限，`timeout_seconds: 21600`。它是一次作业的停止边界，不保证整表在六小时内完成，也不是将矩阵拆分的理由。后续先完成下述缓存gate；全表新尝试须另有未占用的运行身份及已审阅Recipe。

Work Plan保存的227280秒（63.1小时）是低置信度、全MISS串行工程预算，不是实测耗时，也不是这份Recipe的超时值。实际缓存命中及运行耗时须由作业证据确认。

候选验收后一次性交付主线、同步安装，再由正式dispatch preflight核验版本、数据、GPU与run ID占用。超时或失败时先确认原作业终态与可用产物，不自动重试、不复用被占用的run ID、不将部分运行称为整表完成；后续处理遵循[Runbook](../../../self/research/RUNBOOK.md)。

新增七seed先独立分析，经身份核对后汇总十seed。现有metrics提供尺度分析所需基础量，本配置不增加新的指标producer。

实时状态由原[EXP-079记录](../../../self/research/experiments/EXP-079.json)维护。

## 缓存速度 gate

[cache_speed_gate.yaml](cache_speed_gate.yaml) 是完整矩阵的 seed 42 精确子集，保留三数据集、全部选点/GU、预算及评价，共252格（10%）。[独立 Recipe](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate.yaml) 使用新 experiment/run identity，硬上限1800秒，不覆盖旧运行。本阶段先将代码、配置和Recipe备齐，再统一同步一次。

gate 要求 Score/Selection/Output 的适用请求全部命中，producer 未调用，已有 Output 身份和指标可核对，回传及项目校验通过。纯缓存工程目标为600秒内完成执行；这是待检验的目标，不是预测。超过目标、出现MISS或错误都不自动扩大到全量，应定位原因。现行 launcher 的 reuse 在 MISS 时会计算，所以必须检查实际命中记录；仅启动成功不能证明纯缓存。现有结果提供作业墙钟、方法计算时间与HIT记录，不能冒充源码扫描、磁盘读、完整性校验和指标的独立profile。

[cache_speed_gate_cora.yaml](cache_speed_gate_cora.yaml) 是上述 gate 的 Cora 精确子集：全部12个选点条件、七种方法、训练seed42、预算及两套评价均保留，共84格。[独立 Recipe](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora.yaml) 使用新身份 `exp079-cache-speed-gate-cora / e79g2c`，硬上限300秒。它保留为后续扩大范围的准备配置；当前先执行下述7格gate。首轮缺少的 Evaluation 正常计算并保存，随后相同请求的指标HIT与首轮成本分别核对。启动前核对已知参考Artifact、数据与输入身份，实际是否HIT由gate记录验证，不另设要求预先证明全部HIT的运行。

[热轮 Recipe](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora-warm.yaml) 绑定同一份 Cora 配置和指纹，使用独立 `e79g2w`，硬上限同为300秒。首轮和热轮声明一起审阅、交付并同步；热轮必须等待首轮84格完整、回传校验与缓存/指标核对通过。首轮允许新增 Evaluation，热轮要求对应 Evaluation 精确命中；两轮均不清理已有缓存。预先生成声明不代表已提交或占用运行身份，提交前再次核对结果目录、共享 runtime 及队列。

计时核验使用完整进程/Runner回执与当前 AutoReport 事实。单列作业起止耗时、排队、回传；AutoReport 的 `run` 墙钟不包含全部 Python 导入及退出，不能当作完整进程。逐条检查 started/completed/failed 配对、当前 `wall_seconds`、`phase_seconds_exclusive`、缓存来源与 producer 状态；分别汇总共享准备、查询/校验、指标输入消费、新指标公式/写入、导出及 `audit_projection`。各层调用数按实际请求去重，不能将重复展示坐标算成独立 Artifact；嵌套条目、整批阶段和 audit 总计不重复相加。记录逐条最大值及分布，缺失计时保留未知，不以历史 producer `compute_seconds` 代替本轮缓存访问时间。

放行依据为两轮实际84格条件、Selection/Output引用、指标数值一致，适用上游缓存全部HIT且producer未调用，热轮Evaluation全部HIT、AutoReport事实与MD/HTML投影一致，完整回传SHA-256及可信索引通过。超时、非预期MISS、身份或指标不一致、审计不完整均停止扩展。SQLite健康和缓存库存数量不代表这84格的精确覆盖；旧252格失败记录及旧Recipe保留。

旧r4的约3小时对应2184请求的失败前缀，且未完成最终评价，不能与252格完整gate直接计算严格加速比。本gate首先验证当前纯缓存吞吐和正确性；没有匹配范围的旧计时就明确保留这一限制。完整矩阵的六小时上限不因此改变，gate通过不自动提交全量。

## 当前最小 gate：7格冷热两轮

[cache_speed_gate_cora7.yaml](cache_speed_gate_cora7.yaml) 使用Cora原Split、训练seed42、Random选点seed11、预算0.1，保留原七种方法及两套评价，共7个真实条件。它是84格配置的精确子集，不修改公共小表或方法参数。模型型Selector及其他选点条件不在本轮覆盖范围。

| 轮次 | Recipe | RID | 核验内容 | 硬上限 |
|---|---|---|---|---|
| 首轮 | [cora7](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora7.yaml) | e79g3c | 上游Output HIT，缺少的Evaluation正常计算、保存 | 300秒 |
| 热轮 | [cora7-warm](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate-cora7-warm.yaml) | e79g3w | 同一请求Evaluation HIT，直接读取已保存指标 | 300秒 |

gate本身验证缓存命中、访问耗时、指标与引用一致性及AutoReport。首轮Evaluation MISS符合预期，不称完整缓存HIT；若指标此前已经存在则如实记录HIT，不清空缓存制造冷轮。Selection/Output等预期HIT层出现MISS即不满足纯缓存gate，应按已写入的审计定位；普通reuse并非cache-only，MISS仍会进入正常计算，因此保留小范围与硬超时，不自动重试或扩大。热轮等待首轮结果核验后才提交。

AutoReport逐条fsync，超时或强杀后已保存的started/completed及当前wall仍可读取；被杀条目可能只有started，不能编造其结束时间或耗时。MD/HTML可能落后于JSONL，在需要处理失败终态时使用现有精确job审计重建入口，不手改历史事件。两轮都有独立RID；未完成时可以分析已完成条目的性能，但不能判整轮通过或推断252格/2520格总耗时。

## ETR 补充（2026-10-24）

[surrogate_multiseed_etr.yaml](surrogate_multiseed_etr.yaml) 保留原十训练 seed、三数据集、四种选点模型及 Random/Degree、抽样种子、10% 预算和两套评价，仅声明 ETR 与同请求 Retrain：360 个请求，共 720 格。ETR 使用公共实例参数和既有 GCN 目标侧；GAT/GIN/SGC 仍只是选点模型。原六 GU 配置、已提交 Recipe 和既有结果保持不变。

[exp079-etr-r1](../../../scripts/syncmate/recipes/exp079-etr-r1.yaml) 使用新 RID `e79etr1`，硬上限 21600 秒。先通过 EXP-011 的[共用 12 格 ETR gate](../aagu011/table02_etr_gate.yaml)及可信回传核验，再按 EXP-011 → EXP-079 顺序补充。已有输入、Selection、checkpoint、Retrain 只有身份精确匹配才能复用；不预先宣称全 HIT。

全 MISS 串行工程预算为 135120 秒（低置信度规划额度，非实测或上界）；共用 gate 只在 EXP-011 计一次，不扣缓存收益，不含排队回传。该预算超过单次六小时上限，不保证一次完成，不自动重跑。具体分项、部署阻塞与下一步由原 Work Plan 实验记录维护；本配置不代表 GPU 已启动或新结果已被科学接受。
