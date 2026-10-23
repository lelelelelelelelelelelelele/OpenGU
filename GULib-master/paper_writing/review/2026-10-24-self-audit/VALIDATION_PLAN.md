# 主案例的最小补强验证

> **第二轮执行范围更新（2026-10-24）：** 这份114引用清单保留为历史输入，不再按A/B两组直接执行科学验证。A组60引用中的30个GNNDelete输出受测试集选模影响，旧输出只可诊断，须修复并重新生成后再恢复A。B组54引用可优先推进，增加五类三端点标签关系内的真值正确／错误计数，并保持两图及匹配C&S；权重可用性仍须核对。当前顺序与恢复条件见[第二轮报告](../2026-10-24-round2/REPORT.html)。

2026-10-24 · 方案与精确输入已准备，尚未远端执行。  
目的：检查新主发现的解释是否依赖Original响应、MEGU后处理或评价图语义。优先消费已有Output与checkpoint，不先新增GPU训练。

## 已冻结的两个输入范围

| 范围 | 已有条件 | 现存端点引用数 | 回答的问题 |
| --- | --- | ---: | --- |
| A：策略排序交叉 | e79r6，Cora，10%，十训练seed；SGC来源R-point/D-full＋Degree；GNNDelete与Retrain | 60 | 相反效用排序对应怎样的Original/GU/Retrain行为，换评价图后是否保留？ |
| B：额外预测分歧 | 080/e80r305，CiteSeer，5%与33%，三个训练seed；R-point/Random/Degree；GIF、MEGU与Retrain | 54 | 相对Random/Degree的额外D来自哪些预测变化，是否受评价图或C&S影响？ |

所有cell、请求、Output及原运行身份已从可信汇总中逐项列入[VALIDATION_COHORTS.json](VALIDATION_COHORTS.json)，总计114条**引用**，不是114次新增训练。两组源CSV哈希同时冻结。Original参照需沿每个方法端点的真实checkpoint／logits_before身份恢复，不能按文件名猜测或另训替代。

B的更小诊断可以只取R-point：12个GU＋6个Retrain引用；但它不能直接核验论文要强调的Random/Degree相对差，因此推荐仍执行54引用的完整小范围。

## 第一阶段：现存预测上的行为三角

1. 在执行端按精确Output身份只读加载更新前与更新后预测、同请求Retrain预测及绑定的test mask。不下载正式Dataset／Cache payload，不改原始Artifact。
2. 同一评价图、同一测试节点上计算D(O,G)、D(O,R)、D(G,R)，同时给accuracy、CE及适当的概率差；保留每seed值。
3. 将测试节点分为五个互斥类型：O=G=R、O=G≠R、O=R≠G、G=R≠O、三者皆不同。计数和必须等于测试节点数；各D与相应类别计数精确对应。
4. 原图D(G,R)必须复现现有表中同一端点的D；若不一致，先查图／mask／argmax／Output身份，不继续解释。
5. MEGU分别标注raw GCN和含C&S的端点。不能把raw Before与postprocessed After的全部差异都归于权重更新。

这一阶段不训练、不重新forward模型，只读预测。若Output未包含所需Original预测，记录精确缺口；不得自动回退到prepare_model或训练流程。

## 第二阶段：相同权重在删除后图上的敏感性

1. 按绑定的Selection恢复retained图及监督mask，用现存权重做前向；保持测试节点及标签不变。原图与retained图分别报告，不替换既有原图结果。
2. 对A，每个请求／seed有Original、GNNDelete、Retrain三个模型状态；按30组请求／seed计算，至多90次基本前向。原模型在不同retained图上不能无条件共用前向结果。
3. 对B，18组请求／seed需要Original、GIF、MEGU、Retrain四端点，至多72次基本前向；若已有完全相同输入的前向可复用，应记录其身份。C&S使用同请求retained supervision与匹配pseudo labels，可复用模型输出，若调用内含forward的helper则另计。
4. MEGU额外比较no-update raw、no-update+同C&S、updated raw、updated+C&S。只读现有状态，不将删除标签重新引入锚点。
5. 重新计算A的D-full−R-point及GU−R交互，B的D_extra及5%→33%增量；只在同一评价图内部作差。

本阶段是推理补算，不是新训练。CPU用时尚未实测，不能先承诺完成时间；正式提交前按项目流程冻结范围、估时和运行身份。

## 如何根据结果修改论文

| 核验结果 | 允许的解释 | 论文动作 |
| --- | --- | --- |
| 主关系在两评价图下方向与量级相近 | 对这些条件，结论不完全由原图推理引起。 | 将敏感性结果接入主案例，仍保留任务与模型范围。 |
| GU接近Original，Retrain随策略显著变化 | D_extra主要体现两端更新响应不同。 | 诚实解释谁在变化，不把D全部归为GU新预测损伤。 |
| MEGU差异主要出现在C&S而非raw输出 | pipeline后处理是观察的重要组成。 | 将结论标为所评估MEGU pipeline，不将其全部解释成参数遗忘。 |
| 排序或D_extra对评价图敏感 | 原图协议限制实质影响主张。 | 报告反例，收窄或重写部署含义；不能只在脚注隐藏。 |
| 缺checkpoint／身份不匹配／原图D无法复现 | 当前补算证据不足。 | 停在明确缺口，不猜测、训练回退或覆盖旧Artifact。 |

## 不默认追加的实验

- **固定请求R–R校准：** 若只报告配对响应，不把D称异常或遗忘失败，可保留为边界。若需要自然重训波动基线，先验证Random/Degree已有同请求跨seed输出；R-point不同seed的不同请求不能直接混用。对六个固定R-point请求扩至每请求三次重训，理论上还需12次新Retrain，具体仍须核查冻结Selection提交能力与成本。
- **当前分片预算桥接：** 只有主文要推广到修正后六GU的预算结论时才需要。先固定Cora/CiteSeer、33%、R-point/Random、两分片方法、三个训练seed等最小范围；与现有10%新协议衔接，Retrain仅在精确身份匹配时复用。新运行不能覆盖080旧结果。
- **独立split／目标backbone：** 用于扩大结论范围，先固定一条主关系和一个反例；不以所有维度全扫作为默认方案。

## 执行与产物边界

现有独立Metrics只有既定case，没有完整三端点及另一评价图重新forward能力。不能声称只改一个YAML即可执行。本轮准备的是输入清单与分析规格；下一步需只读分析实现及必要的正式入口检查。若修改共享指标接口，按项目开发流程交付；实验配置、版本、回传与科学采用仍按Work Plan Runbook。

交付应包括精确输入身份、图／mask绑定、逐节点分类计数、逐seed指标、配对差、失败记录及复算检查，只回传约定的新统计证据。代码成功、证据可信与作者科学采用分别记录。原始结果和科学决定不会因方案已准备而被改写。

实现依据与已有诊断详见[有效性审查](validity/VALIDITY.html)；本轮已完成的CPU对照见[主自审报告](REPORT.html)。
