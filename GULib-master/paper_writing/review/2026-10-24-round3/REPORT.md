# 第三轮：正式执行、候选发现与写作门槛

2026-10-24 08:34（Asia/Shanghai）快照。实时状态由 Work Plan 的 EXP-084／EXP-085 维护。

**当前判断：writing_gate=not_met。** GNNDelete 的验证集选模修复已合并部署，原十 seed 的限定重算已可信完成，顺序交叉通过预定恢复判据。但五个新 seed 的独立确认、A自身解释、B解释控制及Ret质量尚未闭合，不能将论文评为Weak Accept。尚未开始英文科研正文。

## 已执行的科学结果

A固定为Cora、SGC-source、10%预算、R-point／D-full／Degree、十个原联合seed。正式技术gate运行123秒，主矩阵416秒；六个GU重复条件精确复用，独立新GU共30个，匹配Ret30个。累计作业执行539秒，不含排队、准备和回传；实际缓存命中不能反过来改写开跑前18100秒全MISS预算。

主矩阵121份返回文件通过正式验收。逐GU取证验证30个Output确实导出validation选择的checkpoint，含原图模型状态、运行身份和生成来源；审计producer调用为0、缓存索引不变。主矩阵24个GU MISS、6个gate GU HIT、30个Ret HIT，均精确绑定。

| D-full−R-point | 配对均值（pp） | 样本SD（pp） | 两条主要差的同时95%区间 |
| --- | ---: | ---: | --- |
| Retrain accuracy | +0.848708 | 0.663523 | [+0.285328,+1.412089] |
| GNNDelete accuracy | −6.494465 | 3.100509 | [−9.127030,−3.861900] |

十个seed均为同seed双向交叉。每条主要差使用97.5%双侧t区间组成Bonferroni同时95%区间；普通95%区间、逐seed和原值也保留。CE差为Ret −0.022276、GU +0.203553，仅作次要检查。此结果是固定split上联合请求／训练程序的候选关系，不是普遍规律或独立确认。

证据：[A分析报告](../../../self/research/experiments/drafts/round3-execution-prep/e84r1/REPORT.html)、[决定与哈希](../../../self/research/experiments/drafts/round3-execution-prep/e84r1/DECISION.json)、[逐seed](../../../self/research/experiments/drafts/round3-execution-prep/e84r1/paired_contrasts.csv)、[全部端点](../../../self/research/experiments/drafts/round3-execution-prep/e84r1/endpoints.csv)。执行SHA为eb5e0d79950cf983bbe14b85c63961ce68ab7b0e。旧GNNDelete输出仍隔离，不能与新结果拼表；本批不恢复其他source、Random、其他预算或数据集。

## 当前阻塞与正在完成的开发

B第一层技术gate已在远端完成，2个GU诊断、3个既有引用，用时61秒。后台observer先因旧parser拒绝cell_ids；当前版本collector完成5文件校验后，项目验收又暴露expected_cells声明缺失。因此B结果当前仍不可采用，完整36对尚未启动。

修复已纳入AAGU-109，由真实配置→CLI→收集验收测试覆盖，随后对同一已完成任务重新收集。不重跑GPU，不手工改可信索引，不绕过验收。原失败状态和日志保留。

AAGU-109同时实现固定保存权重的两评价图、MEGU匹配C&S，以及A所需GNNDelete保存掩码检查；仍待最终候选审查。AAGU-110在隔离树实现显式Ret验证轨迹，真实CPU训练证明观察不改变权重与RNG；最终候选及组合验证尚待完成。必要开发按用户授权由根任务验收、合并和部署，科学结论独立审查。

107／108已接受、合并、推送、部署，受管工作树与临时运行目录已清理，永久验证证据保留；这只完成实现交付，不自动接受论文。

## 协议与下一阶段

开跑前冻结的[执行协议](../../protocol/ROUND3_EXECUTION_PROTOCOL.html)与[冻结记录](../../protocol/PROTOCOL_FREEZE.json)保持原样。写作必须同时通过有效性V、具体贡献C、证据强度E、解释与边界I、可写性P，且理论／实验／分析三类模拟审稿均至少Weak Accept，根任务逐项认可。不能平均分或用运行成功代替科学判断。

| 接下来的步骤 | 固定范围与判据 | 全MISS串行预算 |
| --- | --- | ---: |
| A独立确认 | seed1701/1709/1721/1733/1741；三策略，15GU+15Ret；至少4/5同seed双向交叉且两同时区间完全位于预定方向 | 7025秒 |
| A解释gate＋完整20对 | 原十seed×R-point/D-full；O/G/R真值、同权重两图、请求组成；先seed42两对，完整范围不按方向裁剪 | 600+1500=2100秒 |
| B两图／C&S gate＋完整 | 同一54引用、36GU对；原图精确复现后才解释retained图；四端点固定pseudo-label、参数与mask | 600+2040=2640秒 |
| Ret质量pilot＋补全 | CiteSeer33%三策略，先seed42，再补212/2024；3000轮retained图validation，best/final固定测试端点 | 420+660=1080秒 |

这些为待提交下一阶段的低置信工程预算，不是已发生耗时或承诺完成时间；每项须在开跑前完成配置、Recipe、版本和资产核验。详细分项与不变性条件见[下一阶段草案](../../../self/research/experiments/drafts/round3-execution-prep/NEXT_STAGE_PROTOCOL_DRAFT.html)。B第一层完整诊断仍沿用已冻结1680秒预算。

确认seed已查现存62个远端运行声明／26221个单元，无五候选seed；唯一旧格式声明按cells[].training.seed核对后四项均42。此审计不覆盖已删除或没有manifest的历史；保留完整审计和补充解析，不把可见范围夸大为所有历史。确认集保持预定不变。

先完成旧Original权重的全部推理控制，再部署可能改变训练身份的Ret观察实现。缺资产／原图不复现时停止该阶段并保留失败，不能隐式重训填补。若B作为核心，Ret九条轨迹全部完成，不因seed42无触发而跳过其他seed。

## 文章如何随结果改变

[详细提纲v6](../../outline/OUTLINE.html)保留逐章逐段结构，增加新A的两阶段证据和20对解释面板。候选framing是：请求在重训上的效用顺序未必保留到近似更新，GU–Ret分歧还需判断是哪一个端点改变。这个表述必须由确认与解释支持，不能以更强措辞补不足。

- A确认且解释闭合：以请求顺序交叉作主例，B解释预算下的响应与pipeline边界。
- A未确认：保留探索及否定结果，撤其核心地位；B须独立证明超出普通accuracy–fidelity分离的具体认识。
- 两条均不足：记录writing_gate=not_met，报告缺口，不增加seed追求接受评分。

最终证据包将把核心主张、数据、图表、反例和范围一一绑定，再进行三类复审。当前文档是执行与写作方案，不是正式第一稿。

[执行进度快照](../../../self/research/experiments/drafts/round3-execution-prep/EXECUTION_PROGRESS.html)／[EXP-084](../../../self/research/experiments/EXP-084.json)／[EXP-085](../../../self/research/experiments/EXP-085.json)。本报告HTML由同一Markdown生成；静态哈希与链接检查不能冒称浏览器视觉验收。
