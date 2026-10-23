# 第二轮提纲审查：证据撤回、三类审稿意见与修订决定

2026-10-24（Asia/Shanghai）。当前提纲为[详细提纲v4](../../outline/OUTLINE.html)，[Markdown源](../../outline/OUTLINE.md)。本报告是编辑源，HTML由同一内容生成。

**结论：提纲已更新，但目前不能判断论文达到Weak Accept。第二轮发现的首要问题是原主例A的GNNDelete使用测试集指标选择best checkpoint；我撤回上一轮将该案例作为论文主发现的建议。** 这不是靠措辞可以修补的问题。原A的30个GNNDelete引用隔离，其他GNNDelete支撑行在范围审计完成前暂停进入论文；其余方法不因这一事实一并失效。

这轮也增加了一项有用的已有数据分析：R-point相对Degree的GU–Retrain分歧差随预算增长，GIF/MEGU在Cora与CiteSeer均为三个seed同方向。它不依赖选定的Random曲线，但仍是条件性观察，尚不能替代失去的A或排除Retrain移动的解释。

## 1. 三种审稿风格与当前判断

先形成v4初稿并冻结[审稿输入](REVIEW_INPUT_OUTLINE.txt)及[SHA绑定](REVIEW_INPUT.json)，再由三名subagent分别审查。各自先独立审读冻结输入；重要有效性风险发现后向其他审稿角色通报，故最终稿并非完全隔离的盲评。之后主任务逐项修改当前v4。以下是**模拟倾向，不是真实会议评分，也不是录用概率或三个独立专家的投票**。

| 审稿风格 | 当前倾向 | 最强质疑 | 对应完整审查 |
| --- | --- | --- | --- |
| 偏理论／问题定义 | Weak Reject | 代理分数、实际Ret响应和GU响应是三个对象；不能把不同代理目标的差异包装成共同重要性标尺失效。D-full仍是单点source＋静态top-k近似。 | [THEORY_REVIEW](THEORY_REVIEW.html) · [源文件](THEORY_REVIEW.md) |
| 偏实验／有效性 | Reject | 原主发现实际涉及test选模；B尚未分清GU、Ret、评价图与MEGU后处理各自的贡献。 | [EXPERIMENT_REVIEW](EXPERIMENT_REVIEW.html) · [源文件](EXPERIMENT_REVIEW.md) |
| 偏分析／统计解释 | Weak Reject | 事后案例的代表性、联合选点／训练seed、单Random基线、Hop组成与原始端点的解释仍需约束。 | [ANALYSIS_REVIEW](ANALYSIS_REVIEW.html) · [源文件](ANALYSIS_REVIEW.md) |

理论审稿交付较早，其风险注记保留了“具体Output绑定仍在追溯”的当时状态；随后实验审稿已完成六个确切输出的原始创建链绑定。本报告采用后完成的证据结论，不改写独立审查的历史过程。正文中的段落ID在三份审查里指冻结输入，在处置表里指当前修订版。

## 2. 必须撤回原主例A的原因与确切范围

原A是Cora、10%、SGC选点来源下，D-full相对R-point在Ret与GNNDelete中出现相反accuracy顺序。旧输出的十seed关系仍可复算，但不能继续解释为合格的held-out测试发现；把accuracy换为CE、增加误差条或展示更多同类旧输出都不能恢复其有效性。

### 执行链已经落实到真实输出

1. [模块入口](../../../experiments/modular_gu.py)令GNNDelete每epoch评估；[训练器](../../../task/GNNDeleteTrainer.py)调用名为`val`的评估函数，按accuracy＋F1保存best。
2. 该函数实际使用`test_mask`计算上述分数；[GNNDelete适配路径](../../../unlearning/unlearning_methods/GNNDelete/gnndelete.py)在导出前重新加载best。因此测试标签参与了正式Output模型的选择。
3. 原A的30个GNNDelete引用在e79r6均为缓存HIT，不能把消费run版本当作创建版本。本轮找到其中六个Output的原始method MISS创建记录：seed42的两请求来自[exp013 e13-g1](../../../results/runs/gpu4090/exp013-surrogate-to-gcn/e13-g1/run.json)，seed212/2024的四个来自[exp013 r1](../../../results/runs/gpu4090/exp013-surrogate-to-gcn/r1/run.json)。
4. 两个创建SHA分别为`116cc714dd32774ef6b37795d81320b8e312829e`和`62926d95b843af137076eb9dd0a15e1c54c75663`。二者与后续相关版本的训练器Git blob相同：`32e93a50ba440d574aa03d3ac69e5e652cd03a73`；adapter也走同一best加载链。六个Output ID、生成指纹及源码位置见[实验审稿E1](EXPERIMENT_REVIEW.html)。

**边界必须准确：六个端点已直接绑定原始创建run；原A共30个端点全部隔离，另外24个的原始创建run未逐一找齐。** 不能把“未找到”解释为干净；同语义缓存登记与计算等价测试也不能修复选模泄漏。其余GNNDelete支持行暂不用于当前论文，但本轮没有完成全部历史GNNDelete生成家族的影响审计。Retrain、GIF、MEGU及分片结果各自仍需遵守原有局限，不因GNNDelete问题自动作废。

该缺陷对两请求差值方向的影响未知：不能声称修复后交叉一定消失，也不能声称泄漏偏向GU所以原结论更保守。决定必须来自正确选模后的结果。

### v4采取的实际处置

- 从摘要、引言主例、F1、来源margin和结论中撤下A；GNNDelete正向例子和反例一并暂停，避免只撤不利结果。
- 保留旧输出、第一轮分析和冻结提纲作审计；未删除、改写或“修复”任何V2 Artifact。第一轮报告及114引用计划增加了明确的第二轮更新提示。
- 主文暂围绕B1（同预算请求差异）与B2（预算改变该差异）组织；二者来自同一实验家族，不能算两份独立发现。
- 其他非GNNDelete的排序交叉格保留为完整范围，不能事后挑一个最有利格自动接替A。是否恢复A或仅用B，需要据有效证据重新评估贡献。

## 3. 本轮新分析：已有优势还剩下什么

### 3.1 不依赖指定Random曲线的Degree对照

令`K(b)=D(R-point,b)−D(Degree,b)`，每个D都比较该策略自己的GU与同请求Ret。计算`K(33%)−K(5%)`时，若从两条相对Random差构造，Random项恰好抵消。本轮给出全部两个数据集×六GU的[36条逐seed记录](analysis_reviewer/rpoint_degree_budget_seed.csv)及[12条汇总](analysis_reviewer/rpoint_degree_budget_summary.csv)，没有只生成有利格；GNNDelete标隔离，080分片标历史协议。

| 数据集／方法 | K(5%) → K(33%) | 增长：均值±样本SD（pp） | 逐seed方向 |
| --- | --- | ---: | --- |
| Cora／GIF | 1.476 → 8.180 | 6.704±1.654 | 3/3正 |
| Cora／MEGU | 0.677 → 5.658 | 4.982±0.976 | 3/3正 |
| CiteSeer／GIF | 1.451 → 16.517 | 15.065±4.508 | 3/3正 |
| CiteSeer／MEGU | 0.901 → 17.117 | 16.216±2.553 | 3/3正 |
| Cora／GraphRevoker历史变体 | 见完整表 | −6.458±5.056 | 3/3负 |

IDEA在这里与GIF重合，不增加独立确认。Cora分片的反向结果说明不能概括为所有方法同向；它也不能用来否定非分片结果，因为协议不同。Random抵消最大数值误差约`3.55e−15`，见[复算检查](analysis_reviewer/checks.json)。这证明代数及表值一致，不证明训练有效性、因果效应或对随机请求分布的期望。

### 3.2 Ret原值决定B怎样解释

CiteSeer/R-point从5%到33%时，Ret accuracy由75.275%降到64.715%，GIF由74.875%到74.374%，MEGU由74.224%到74.274%。33%的GIF–Ret和MEGU–Ret分歧分别为24.625%与24.925%。因此不能只画上升的D曲线，让读者误以为“GU自身预测被破坏”。

当前最准确的观察是：**在这些请求和实现下，近似更新与重新训练的响应分离，并且两类基线给出的比较不同。** 谁在移动、移动是否纠正错误、是否受评价图或C&S支配，仍待定向分析。`D≥|accuracy_G−accuracy_R|`可作结果自检界限，不是新的遗忘指标或归因公式。

### 3.3 十seed与空间结果的解释已纠正

079每个数据集/source的R-point、D-full各有十个不同Selection，Degree只有一份，Random三份跨seed复用。n=10描述联合选点／训练程序的变化，不能称固定请求在十次训练中稳定；也不是十个数据split。详见[Selection身份表](analysis_reviewer/selection_identity_counts.csv)。

Hop表已有足够的分子分母，但分组组成会影响解释。例如e11r1/Cora/GraphRevoker变体的R-point、IM一跳D为33.522%、26.498%，整体D却为22.263%、24.867%，顺序不同。这个例子说明一跳大小不能代表整体；不是严格Simpson悖论或因果传播证据。应在每个请求内按`sum_h(w_h D_h)`还原整体，再平均draw/seed，不能将平均权重乘平均带内率。原GNNDelete同类例子只留内部审计。见[全方法组成表](analysis_reviewer/hop_composition_example.csv)。

### 3.4 保留下来的实验层次

011机制广度、079联合重复与来源、080独立预算轴、固定checkpoint校准、078/082训练诊断、Hop分层和真实大图selector成本仍各有用途。它们的职责互不替代：原模型质量不证明retained Ret质量；GU求解校准不证明IF selector忠实性；大图selector运行不证明大图GU效果；共同Output不是新的独立复现。详细库存沿用[第一轮库存](../2026-10-24-self-audit/inventory/INVENTORY.html)及[有效性核验](../2026-10-24-self-audit/validity/VALIDITY.html)，采用范围由本轮更新。

## 4. 二十项意见的处置与剩余缺口

“写作已改”只表示提纲已改变，不表示实验问题闭合；“分析完成”仅限指定已有数据复算。完整论据、反结果分支和建议在三份审稿报告内。

| ID | 当前处置与提纲位置 | 尚未解决的部分 |
| --- | --- | --- |
| T1 代理目标与实际响应混同 | **写作已改**：中心句、I-P2、M-P3区分请求构造与实测响应；不再主张共同重要性顺序失效。 | 若要评价代理忠实性，需直接比较预测目标与真实同目标变化。当前不作此主张。 |
| T2 验证CE与测试效用跨目标 | **写作已改**：M-P3明确验证Q上的CE、外部测试指标；停止用旧A的CE提升证据。 | 未测量各主例评分与Q上真实变化的吻合。不是当前描述性论文的默认新增矩阵。 |
| T3 单点source与集合优化 | **写作已改**：D-full明确为单点图耦合source、静态top-k及集合可加代理。 | 未证明大预算联合删除近似准确；不能归因理想图影响目标。 |
| T4 有限solver与理论逆矩阵 | **写作已改**：实际score使用有限迭代输出；selector与GU校准分开。 | 未认证IF估计准确，不把小shifted残差当原方程或selector保证。 |
| T5 D增加的响应归属 | **诊断待做**：D-P2、A-P4加入B组三端点、真值、两图与C&S。 | 谁移动及其正确性尚不明；禁止GU损伤机制结论。 |
| T6 权限与删除语义 | **写作已改**：I-P1、Problem明确平台评估者、全候选池、原图评价和保留特征行。 | 未验证普通用户现实权限、永久擦除或部署防御。 |
| T7 贡献及采用门槛 | **已撤回A；门槛未通过**：近邻比较不再以普通accuracy–fidelity分离为新颖性。 | B是否足以独立承担WWW贡献仍未确定；需有效性与解释证据。 |
| E1 GNNDelete测试集选模 | **来源绑定＋隔离完成；实现未修复**：六个原始MISS已绑定，A共30引用隔离，其他GNN支持行暂停。 | 全历史影响范围、合规选模、缓存语义及定向重算均未完成。 |
| E2 B组三端点和两图 | **范围已准备**：A-P4保留B组54引用及对应Original，不仅看R-point。 | 预测payload／权重可用性与实际推理诊断尚未核验完成。 |
| E3 GIF/IDEA与MEGU实例 | **写作已改；解释未闭合**：E-P2/E-P5、A-P3准确命名移位profile、零噪声IDEA、MEGU pipeline。 | 高预算数值状态、匹配no-update+C&S四端点仍待查。 |
| E4 单Random与重复层级 | **写作已改＋Degree对照完成**：T1、E-P3、F3区分联合程序与请求重复。 | 对Random请求分布的总体结论仍需额外draw；当前收窄为既定请求。 |
| E5 retained Ret训练质量 | **待查日志**：E-P2、A-P3加入两个冻结Ret的validation轨迹优先检查。 | 078/082不能填补此缺口；仅日志不足或发现异常后定向诊断。 |
| E6 名义k与实际删除负荷 | **待补已有选集统计**：R0-P2加入唯一删边数、类别监督与局部mask覆盖。 | 未完成这些统计；因果独立效应需要额外匹配控制，当前不声称。 |
| A1 事后主例与家族范围 | **A撤下、范围要求加强**：Q1-P2、附录E保留完整采用家族；不挑替补主例。 | 原72条件等计数仅作内部审计，最终采用家族还须重绘。 |
| A2 联合seed解释 | **身份核查＋写作完成**：T1/E-P3明确十个IF Selection、Degree一份、Random三份。 | 未分离selector方差与固定S训练方差，不把区间解释成它们。 |
| A3 Degree直接对照 | **已有数据分析完成**：36条逐seed、12条汇总，F3加入两基线，保留反向和隔离行。 | 不产生Random总体期望，不构成独立确认。 |
| A4 三角关系缺正确性 | **规格已扩展、计算待做**：A-P4在五类标签关系内增加O/G/R真值正确性。 | O=G≠R不足以判定Ret伤害；尚无类别计数结果。 |
| A5 Hop组成与汇总 | **复算＋写作完成**：增加非GNN例子、整体D、分母和请求内汇总规则。 | 尚无共同权重或逐节点迁移分解；现有描述不宣称局部因果。 |
| A6 有限、可反驳的主张 | **写作已改**：B1/B2分别限定同预算与预算差；Q2-P5列相反分支，不声称单调。 | 预先固定的独立确认仍缺失；没有将探索分析写成预注册。 |
| A7 主图负担 | **布局已改**：F1原值、F2固定预算、F3两基线预算；来源F4改正文T3＋附录E1。 | 尚未生成正式论文图或完成实际双栏可读性检查；不能把提纲HTML当图形验收。 |

## 5. 文章现在怎样组织

| 部分 | v4的主要变化 | 必须保留的边界 |
| --- | --- | --- |
| Abstract／Introduction | 撤A；用CiteSeer的Ret/GIF/MEGU原始端点说明B；平台评估者作为场景主语。 | 一条主观察的两个比较层次；不能靠强措辞补创新。 |
| Related Work／Problem | 明确近邻已有普通accuracy–fidelity分离；权限、图操作与评价图前置。 | 暂不主张真实部署攻击、物理擦除或新遗忘认证。 |
| Method | 有限score、验证CE、单点source与静态top-k；同请求Ret与Random职责分开。 | IM/IF原则不是新算法；不假设代理已实现理想目标。 |
| Experimental Design | 三模块、采用方法、共同Output复用、联合seed及方法训练规则可见。 | GNNDelete隔离、080分片历史协议、GIF/IDEA近重复不能藏在附录。 |
| Q1／F2 | 展示固定预算的可采用方法全策略范围，保留原值、Degree和空间组成。 | 删除受影响方法后重新生成，旧完整图册不能直接复制。 |
| Q2／F3 | 两数据集、GIF/MEGU、Random与Degree两基线、七预算点；邻接Ret/GU原值。 | 三seed、单Random、Ret移动、历史分片反例；不推导单调或普遍规律。 |
| Q3／T3 | 压缩为完整来源范围与反例，详细区间移附录E1。 | source变化不是目标架构泛化；旧margin暂停。 |
| Discussion／Appendix | 将三端点真值、两图、匹配C&S、Ret质量与请求组成列为明确待验证分支。 | 未完成不能写成控制已通过；内部故障与待办不会原样塞进投稿正文。 |

用户要求的“章节—段落—小部分—目标／写法／注意点”和图的内容、布局、caption组织仍保留。当前文件是详细组织稿；没有生成第一版英文科研正文。

## 6. 达到可认真讨论Weak Accept的最小路径

### P0：先恢复证据有效性

若继续采用GNNDelete，必须修复stage与mask映射，并在看测试结果前决定validation选模或固定epoch规则。验证应能检查测试标签不影响checkpoint选择；只证明函数可运行不够。

修复必须有新的代码与生成身份；不得把语义改变登记为与旧训练等价、继续命中受影响Output，也不得改写旧V2证据。沿实际生产路径绑定新结果，才有资格恢复论文采用。

| 范围 | 最小计算量 | 允许恢复什么 |
| --- | --- | --- |
| 原A先行诊断 | 3 seed × R-point/D-full = **6个GNNDelete更新** | 判断修复后是否值得继续；不能恢复原十seed区间。 |
| 原A和Degree完整范围 | 10 seed × R-point/D-full/Degree = **30个GNNDelete更新** | 在完整身份与预先固定协议下重新评估原A及Degree。 |
| 其他Random/source/预算GNN结果 | 按实际采用范围另列 | 上述30个不覆盖它们；若恢复对应图或相对Random主张，需补相关输出。 |

现有Ret只在Selection、split、训练配置和评价身份完整一致时复用。当前任务没有实施修复、创建新训练run或进行GPU实验。若作者选择彻底不采用GNNDelete，可以不为投稿恢复A，但必须接受论文贡献重新评估，不能沿用原主发现。

### P1：优先使用B组现有资产回答“谁在改变”

B组是CiteSeer、5%/33%、R-point/Random/Degree、三个seed、GIF/MEGU/Ret，共**54个已有端点引用**。这是资产范围，不是54个独立样本，也不保证全部权重已在本地可用。对应Original需要单独绑定。

1. 先检查预测、标签、mask、Original和权重身份，重现已有accuracy与D；缺失明确报出，不隐式重新训练。
2. 计算O–G、O–R、G–R以及五类预测标签关系；每类再统计O/G/R的真值正确性，区分保留正确、保留错误与纠错。
3. 同一权重在原图和retained图评估相同测试节点；报告效应保留、减弱或反转。
4. MEGU比较raw no-update、匹配C&S的no-update、updated raw、updated+C&S；GIF检查主例的非退化与求解日志。不能按产生最大差异的配置选择报告。

若新增D主要为O=G≠R，应改写为两种更新响应分离；若Ret在纠正Original错误，解释又不同。若效应主要来自C&S或原图评价，应准确归因pipeline／协议。**这些结果即使削弱原设想，也比更多泛化矩阵更能决定论文是否站得住。**

### P2：最小排除替代解释，然后再决定是否扩展

- **Ret质量：** 先查CiteSeer33%、seed42、R-point与Random的已有validation轨迹。资料不足才做这两个冻结请求的训练诊断；不按test选择参考模型，发现问题再扩展。
- **请求组成：** 由已有Selection／图计算唯一删边数、类别删除／保留监督和相关局部mask覆盖。先给描述；只有独立于结构／类别的机制主张才需要匹配控制。
- **请求分布：** 当前描述不强求新Random。如果要声称高预算相对一般Random仍成立，可预先固定两组额外嵌套draw、两预算、三seed、GIF＋Ret，共24方法端点（含12个Ret）；MEGU可复用Ret增加12更新端点。这是可选扩大声明，尚未创建实验。
- **固定S重训噪声、目标backbone、新split：** 分别服务“超出自然波动”、目标架构与数据划分泛化。不要为描述性主张默认扩成全矩阵，也不要在没有它们时写对应更强结论。

当前最可能改变拒稿倾向的组合是：有效性修正后仍有足够大的具体关系、B的响应归属清楚、关键替代解释得到检查、主文范围与完整反例清楚。没有任何一组检查可以保证Weak Accept；若修复后关系消失或只剩已知的普通指标分离，应据实降低贡献判断。

## 7. 本轮交付与核验边界

- 已完成：冻结审稿输入、三类模拟审稿、六个主例Output的原始创建链追溯、已有表CPU复算、20项处置、逐章提纲v4及历史报告采用范围提示。
- 未完成：程序修复、完整历史GNNDelete影响审计、新训练、三端点／两图／C&S计算、Ret新增诊断、请求负荷统计、正式论文图和英文第一稿；没有远端同步、GPU运行或实验科学状态变更。
- Markdown和HTML均由现有渲染器生成；源哈希、文档链接、导航锚点、段落结构及关键统计交叉检查记录在[DOCUMENT_VALIDATION.json](DOCUMENT_VALIDATION.json)。冻结输入身份与最后修订版身份分开保存。HTML未经过浏览器视觉验收，正式双栏图尚未绘制。

入口：[当前提纲](../../outline/OUTLINE.html) · [理论审稿](THEORY_REVIEW.html) · [实验审稿](EXPERIMENT_REVIEW.html) · [分析审稿](ANALYSIS_REVIEW.html) · [第一轮历史报告](../2026-10-24-self-audit/REPORT.html) · [第一轮历史输入清单](../2026-10-24-self-audit/VALIDATION_PLAN.html)。
