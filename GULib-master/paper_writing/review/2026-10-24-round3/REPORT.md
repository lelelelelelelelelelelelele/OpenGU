# 第三轮：执行计划、已完成工作与写作门槛

2026-10-24 08:01（Asia/Shanghai）。本报告为本轮可审查快照；运行实时状态由Work Plan中的EXP-084、EXP-085维护。

**当前判断：writing_gate=not_met。** 第二轮指出的测试集选模已有通过CPU验证的修复候选，但尚无修复后的正式科学结果；B尚缺三端点归因、两评价图、匹配后处理及Ret参考质量的完整证据。因此目前不能诚实地将论文评为Weak Accept，也没有开始英文科研正文。

## 执行协议已经明确

[协议阅读版](../../protocol/ROUND3_EXECUTION_PROTOCOL.html)／[Markdown源](../../protocol/ROUND3_EXECUTION_PROTOCOL.md)规定了范围、指标、缺失条件处理和停止规则。[冻结记录](../../protocol/PROTOCOL_FREEZE.json)保存开跑前文件SHA；后续运行需绑定这一版本，改变范围先修订。

写作放行须同时满足有效性、具体贡献、证据强度、解释与边界、可写性五项，并由理论、实验、分析三类模拟审稿分别给出Weak Accept或以上，主审逐项认可。不是平均分，不把完成实验、显著结果或代码验收当成科学接受。

A的gate仅检查执行有效性。技术通过后，完整十seed范围无论方向好坏均执行；恢复方向固定为Ret的D-full−R-point accuracy为正、GNNDelete为负。两端点同时区间满足预定方向后，才进入五个新联合seed的确认；确认标准与失败分支已经固定，不逐步加seed追求显著。A若成为核心，还需自身条件下的三端点／两图解释。

B先复用已有54引用完成三端点与组成，再执行同权重两图、MEGU四端点C&S控制和Ret质量诊断。三端点诊断完成不等于全部解释闭合。新增Random draw只作有限敏感性，不冒称请求分布的一般规律。

## 实际已经完成的工作

| 项目 | 已完成的事实 | 尚未支持什么 |
| --- | --- | --- |
| GNNDelete修复AAGU-107 | 候选02206948262699bf523d4dadbb1ab2e0ae977a64；139项CPU回归通过，真实三seed测试标签扰动不改变验证轨迹、best或输出；validation可影响选择；旧Output不等价命中；已合并6fe3392并推送 | 不证明原排序交叉恢复，不是正式GPU重算 |
| A输入冻结 | 30请求坐标、21个不同Selection、30个匹配Ret；120个返回文件哈希通过；12/60端点真实dry-run通过 | 远端当前资产与新producer的精确查找仍须运行前审计 |
| B已有结果CPU分析 | 54不同Output、18请求×seed组、10不同Selection、36 GU–Ret对；217项输入／返回哈希断言通过；9/9预算请求严格嵌套 | 没有把本地统计冒称新的远端预测或两图实验 |
| B诊断实现AAGU-108 | 第一层候选3db791a6经116项聚焦回归、11项提交后验证；与107组合38项通过；已合并de948fbe并推送 | 未部署，未形成正式54引用的新增指标结果；两图/C&S不在本候选内 |
| 论文方案 | [详细提纲v5](../../outline/OUTLINE.html)已更新；按A恢复、B独立成立、证据不足三种分支安排主文 | 不提前填入预期结果，不保证最终审稿达到Weak Accept |

用户已明确接受107的具体候选，并授权本轮后续必要开发由主任务验证、验收后合并部署。主任务据具体候选和组合检查接受108第一层实现；科学写作门槛保持独立。107合并准备曾发现启动投影缺失Remote target，核验既有origin/main后补齐；本轮研究材料保存提交后恢复合并。组合测试首次因系统pytest临时目录不可访问出现17项fixture错误；保留日志，在新建workspace临时目录重跑未改动的测试后38项通过。

另有明确的取证要求：默认collector不收runtime的model_best.pt，不能因此判断逐cell的epoch／选模阶段已核验。补充只读脚本将run/cell的Output recipe_hash与runtime checkpoint、保存权重、选模元信息绑定；取证不成功时A技术gate不得科学放行，不修改V2旧Artifact。

## 新CPU分析怎样改变下一步

以下均为CiteSeer、5%→33%、R-point、三个联合seed的配对变化，均值±样本SD：

| 端点 | accuracy变化（pp） | CE变化 |
| --- | ---: | ---: |
| Retrain | −10.561±2.790 | +0.3813±0.1259 |
| GIF | −0.501±0.229 | +0.00244±0.00265 |
| MEGU | +0.050±0.229 | −0.3508±0.3969 |

MEGU包含C&S，因此CE差异尤其需要匹配后处理解释。Ret下降不能仅凭这张表归因为训练不足；现有Ret链没有保存所需validation轨迹，必须按协议作有边界的训练诊断。

33%时R-point平均一跳测试覆盖37.688%，低于Random43.844%和Degree58.559%；三跳内分别71.972%、79.580%、75.676%，每请求666个test节点。较大GU–Ret分歧并未伴随更广的这些几何覆盖，但覆盖不是因果控制，不能据此断言传播机制。完整证据见[B分析报告](../../../self/research/experiments/drafts/round3-b-diagnostics/REPORT.html)及[逐请求覆盖](../../../self/research/experiments/drafts/round3-b-diagnostics/request_test_hop_coverage.csv)。

## 已登记的运行范围与预算

| 实验 | 当前阶段 | 全MISS串行预算 | 执行状态 |
| --- | --- | ---: | --- |
| EXP-084 | gate 6 GU＋6 Ret，再完整30 GU＋30 Ret；重合6 GU精确复用，独立GU条件共30 | 4050＋14050＝18100秒，约5.03小时 | 配置与Recipe已准备；正式任务未提交 |
| EXP-085 | 第一层3引用gate＋54引用完整诊断；有效GU诊断分别2/36，Ret不适用 | 2085秒，约34.75分钟 | 精确子集配置、Recipe与2/36输出dry-run通过；正式任务未提交 |

预算为低置信工程估计，按全MISS串行计算，不扣HIT、不计并行收益或排队与回传，也不是完成上界。A确认、A解释控制、B两图/C&S及Ret诊断尚未包含在这两项数字中，必须在各阶段启动前另列完整预算与配置，不能以首阶段预算代表全部论文补强成本。

运行定义：[EXP-084记录](../../../self/research/experiments/EXP-084.json)、[EXP-085记录](../../../self/research/experiments/EXP-085.json)。A准备与冻结输入见[执行准备报告](../../../self/research/experiments/drafts/round3-execution-prep/REPORT.html)。

远端此前由exp014-20261024-e14r4占用，控制端07:53:39观察到recipe_timeout终态；不能据此认定执行资源或Score锁已恢复。下一次部署与dispatch仍由登记安装动作和正式preflight检查，不能擅自清锁或重启其他任务。本轮正式GPU任务是否开始，以实际提交回执为准。

## 下一阶段顺序

1. 完成本轮必要候选的审查、合并及配置提交，统一安装同一主线SHA；保留旧Output与失败记录。
2. 审计A的固定Selection、原始checkpoint、Ret精确身份及新GNNDelete生成身份，缺失或错配即停。
3. 运行EXP-084技术gate和EXP-085第一层gate，可信收集核验后才扩展完整预定范围。
4. 依据协议进入解释控制、Ret质量及条件确认，不把中途观察当最终主张。
5. 冻结证据包做三类复审。只有全部满足写作门槛才开始Results与Experimental Design，最后写Introduction和Abstract。

本报告和提纲的HTML从Markdown生成；文档检查核对内容哈希、链接及逐段结构。浏览器视觉检查尚未完成，不能把静态检查写成视觉验收。
