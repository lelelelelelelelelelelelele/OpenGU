# 第二轮模拟审稿：实验公平性与可复现性

2026-10-24（Asia/Shanghai）。这是针对详细提纲 v4 的**模拟审查，不是真实会议审稿或投票**。审查输入以[冻结的 v4 提纲](REVIEW_INPUT_OUTLINE.txt)及[输入身份](REVIEW_INPUT.json)为准；不以之后修订的提纲倒推本轮判断。未阅读其他本轮审稿文件，未连接远端、运行 GPU、改动程序或实验科学状态。本文 Markdown 为编辑源，HTML 由主任务统一生成。

**当前倾向：Reject，主要原因是主例 A 已发现实际涉及测试集选取 checkpoint 的 GNNDelete 输出。** 这不是要求补更多数据集的覆盖性意见，也不意味着排序交叉一定消失。它意味着当前十 seed 数字不能继续作为无污染测试结果承担摘要和首图。主例 B 仍有值得报告的策略特定响应，但现有输出的三端点、评价图及后处理解释尚未闭合，不能单独弥补主例 A 的有效性缺口。

## 我理解的主张

论文比较在相同训练候选池和节点删除数量下，不同重要性目标构造的请求如何改变 GU 和同请求 Retrain 的响应。主例 A 是 Cora、SGC 选点来源、10%预算下，D-full 相对 R-point 的 Retrain accuracy 高约0.849 pp、GNNDelete 低约5.756 pp，十训练 seed 方向均交叉。主例 B 是 CiteSeer 预算变化中，相对同预算 Random 的 GU–Retrain 预测分歧增量依策略改变，R-point 在33%下的 GIF/MEGU 增量约14.615/14.815 pp。来源和 Hop 分层用于限定这些关系，而非声称统一的遗忘规律。

这两个经验问题可以成立；但必须区分“这些保存的预测有此关系”和“合格、无测试泄漏的实现产生了可推广的科学发现”。

## 已有优势及不应重复提出的空泛要求

- 011/079/080 的层次清楚；十 seed 的直接配对优于只比较均值，Degree 反例和完整来源家族也已保留。Output 身份、生成/消费源码及复用关系可追查，这次正是凭这些资料找到主例风险。
- 062/065–068 已有四组固定 checkpoint 校准、84格验证与独立 Random 请求，包含非零更新、HVP、移位残差及局部两图/no-update 证据。不能再写“没有数值或 Original 对照”；也不能把它们升级为高预算战略请求逐格验证。
- 078 已检查基础模型轨迹和 checkpoint 来源；082 有 Cora CPU 以及 CiteSeer/PubMed 的分片训练诊断，后两者 corrected 臂300→3000轮的 validation 变化在约±0.901 pp内。这回应了轮数任意质疑，不能证明全部方法或 retained 请求的训练充分性。
- 051、新011有请求抽样重复；Hop 有完整分母和反例；014/056 有真实大图 selector 成本。它们都应使用，分别承担请求变异、空间描述、选择成本的职责。它们不是固定请求 R–R 校准或大图 GU 端点。
- 080 旧分片与新011/079不能合并。共同10%条件非分片及 Retrain 的90/90 Output相同，说明可复用而非独立复现；两分片各18项不同。不能因旧分片问题否定全部080非分片结果，也不能将六方法预算图统一称为当前实现表现。

依据：[库存](../2026-10-24-self-audit/inventory/INVENTORY.md)、[有效性审查](../2026-10-24-self-audit/validity/VALIDITY.md)、[自审报告](../2026-10-24-self-audit/REPORT.md)。

## E1 · 阻断：主例 A 的 GNNDelete 使用测试标签挑选 best checkpoint

**段落：** I-P3、Q1-P2、Q3-P3、F1/F4、E-P2/E-P5。**分类：新实验／实现纠正后的定向重算；写作降级立即可做。**

**最强质疑。** GNNDelete 的测试端点不是只在训练结束后读取一次 held-out test。实际执行链在每个遗忘 epoch 用 test_mask 计算名为 `val` 的分数，选择最优 checkpoint，随后把该模型保存为正式 Output。因此当前主例比较混入了依请求而变的测试集模型选择，不能视为纯 held-out 请求排序。此行为通常使各请求的报告准确率偏乐观，但其对两请求差值与交叉方向的影响不定；不能用“偏差有利于 GU，所以交叉仍保守”豁免。

**已核实代码链。**

| 环节 | 源码证据 | 实际行为 |
|---|---|---|
| 模块化入口 | [modular_gu.py](../../../experiments/modular_gu.py)，`gnndelete_node`及`run_unlearning` | 设置 `test_freq=1`；`gnndelete_node`调用`delete_node(nodes)`，最后返回 trainer 当前模型。 |
| 选模型 | [GNNDeleteTrainer.py](../../../task/GNNDeleteTrainer.py)，约445、461–471行 | 每 epoch 调`eval_node_fullbatch_del('val')`；按`dt_acc + dt_f1`保存`model_best.pt`。 |
| “val”实际标签 | 同文件约599–635行 | `stage`仅进入日志名称；loss、预测、accuracy、F1均使用`self.data.test_mask`，没有按stage切换。 |
| 导出前加载 | [gnndelete.py](../../../unlearning/unlearning_methods/GNNDelete/gnndelete.py)，约591行；trainer约481、511–513行 | `delete_node`调用默认`ckpt='best'`的测试函数，重新加载best；adapter返回的正是该模型，随后生成Output。 |

这不是对当前代码的泛化猜测。e79r6 的30个主例 GNNDelete 引用全部为HIT，不能说它们是在e79r6新训练的。本轮沿其**真实 Output ID**查到六个原始创建端点：

| 主例条件 | Output ID | 本地创建记录 | 创建 SHA |
|---|---|---|---|
| seed42，R-point/SGC | `pred_501a6889_d6678d5d` | [exp013 e13-g1/run.json](../../../results/runs/gpu4090/exp013-surrogate-to-gcn/e13-g1/run.json)，method MISS | `116cc714dd32774ef6b37795d81320b8e312829e` |
| seed42，D-full/SGC | `pred_b9a86ea2_6fd276d1` | 同上，method MISS | 同上 |
| seed212，R-point/SGC | `pred_820b7773_0c246d20` | [exp013 r1/run.json](../../../results/runs/gpu4090/exp013-surrogate-to-gcn/r1/run.json)，method MISS | `62926d95b843af137076eb9dd0a15e1c54c75663` |
| seed212，D-full/SGC | `pred_86613601_39072011` | 同上，method MISS | 同上 |
| seed2024，R-point/SGC | `pred_73b2f559_a6da278b` | 同上，method MISS | 同上 |
| seed2024，D-full/SGC | `pred_3f123791_d620a164` | 同上，method MISS | 同上 |

两创建 SHA、AAGU-099 基线`bf843abbad2cd40ff83d0ed6c1c90ca663666446`与e79r6执行SHA`bab1781e182254e0b02cbeb1de138d58f7f1cd50`中的`GULib-master/task/GNNDeleteTrainer.py`，Git blob均为 **`32e93a50ba440d574aa03d3ac69e5e652cd03a73`**；上述test-mask选择代码完全相同。两创建SHA的adapter也明确`test_freq=1`，并走相同best加载返回链。

**范围与不确定性。** [e79r6原始run](../../../results/runs/gpu4090/exp079-surrogate-multiseed/e79r6/run.json)中，Cora、GNNDelete、`r_point_sgc.yaml / gt_full_sgc.yaml / degree.yaml`、十seed共30个端点的生成指纹分别为：25个`89028226…`、2个`b7eecaea…`、3个`05197336…`。这些均属于[已审阅的同语义组](../../../cache_v2/source_compatibility.json)；[来源说明](../../../docs/cache-source-identity.md)称差异为Observer/查询、未使用分支和等价边mask优化，没有训练评价修正。**六个端点已直接绑定原始MISS创建版本；其余24个本轮未找到原始创建run，但不能据HIT或等价登记视为干净。最小隔离范围为主例A全部30个GNNDelete端点，完整受影响家族仍需另行审计。** Retrain、GIF、MEGU未因这一事实自动判无效；新分片损失修正也不修复此链。

**已有回应。** AAGU-099 的掩码等价与109项测试只支持优化前后计算一致，恰恰保留了训练评价逻辑；062校准针对GIF/IDEA，078基础模型诊断及082分片诊断也不覆盖这一GNNDelete选择泄漏。v4没有回应此问题。

**最小修复。** 先从摘要/F1中撤下A的已验证发现地位，并保留历史证据。修复stage对应mask，预先决定validation选点或固定epoch，不按test结果选方案。用原Selection、原初始checkpoint，先重算三seed×两请求的6个GNNDelete端点作诊断；这不是新预训练。若要恢复原十seed主张及Degree反例，需重算十seed×三请求的30个GNNDelete端点，Retrain只在完整身份一致时复用。三seed试跑不能恢复原十seedCI。修复后的其他GNNDelete图表是否重算，应按实际依赖范围决定，不能把新旧端点混成一表。

**会推翻当前解释的结果。** 正确选点下交叉消失、方向不再一致，或主要来自不同请求的测试最优epoch差异，就应放弃A作为核心发现；若交叉保留，也须以新协议重新报告效应量，而不是沿用旧数字。

## E2 · 重要：主例 B 的额外D尚未分清谁在改变，且原图推理决定任务语义

**段落：** P-P3、Q2-P2/P3、A-P4、D-P2。**分类：已有数据上的新分析，不默认新训练。**

**最强质疑。** R-point下CiteSeer Retrain在5%→33%从75.275%降到64.715%，GIF/MEGU效用近稳。仅凭D_extra无法分辨GU额外扰动、GU保持Original而Ret移动、或二者同时变化。更新后又在原图恢复全部边与特征做推理，会进一步改变这一关系的部署含义。相同评价图使当前配对定义清楚，不使“永久删除后的系统”解释自动成立。

**证据与已有回应。** [node_deletion.py](../../../experiments/node_deletion.py)定义保留特征行、移除监督及关联边、默认原图评价；[有效性审查](../2026-10-24-self-audit/validity/VALIDITY.md)明确066–068已有局部no-update和两图证据，但079/080战略主例未闭合。v4已诚实缩限为描述性关系，并准备[114引用方案](../2026-10-24-self-audit/VALIDATION_PLAN.md)，这比泛称遗忘失败准确；方案存在不等于得到结果。

**最小修复。** 优先执行B的54个现存端点引用：CiteSeer、5%/33%、R-point/Random/Degree、三个seed、GIF/MEGU/Ret。固定同一test mask，给D(O,G)、D(O,R)、D(G,R)及五种三者标签关系；再用同一已存权重比较原图与retained图。只做R-point的18引用不能回答论文主张的相对Random增量。A的现存输出仍可用于诊断，但E1修复前该分析不能重新认证A。

**会推翻当前解释的结果。** 若主要新增类别为O=G≠R，则应将B解释为两条更新响应分离，不能称GU预测被额外破坏；若D_extra在retained图显著缩小或反向，必须把主张限定为原图协议并同步修改摘要/主图。即使如此，保存预测间的原图差值仍是事实。

## E3 · 重要：被测实例的行为可能由移位求解及C&S决定，不能直接归给原算法家族

**段落：** E-P2/E-P5、Q2-P2、A-P3/A-P4。**分类：已有数据／实现说明；只有保存状态不足才考虑定向新运行。**

**最强质疑。** GIF/IDEA用seed42固定PT校准的正移位profile覆盖主表其他seed和高预算；“成功求解移位方程”不等于当前删后目标的有效近似。MEGU的Before是raw GCN，After含Correction & Smoothing，若将两者变化解释成参数遗忘，会把后处理混入结论。两个问题都可能产生GU效用近稳、与Ret分离的观察。

**证据与已有回应。** [校准汇总](../2026-10-24-self-audit/validity/calibration_summary.json)与[VALIDITY](../2026-10-24-self-audit/validity/VALIDITY.md)已证明真实非零更新；shifted残差最大约3.486e−7，但原方程残差仍约0.1965–0.5559。IDEA零噪声且与GIF近重合，不能算独立认证遗忘验证。[modular_megu.py](../../../experiments/modular_megu.py)保存raw before，after调用`megu_logits`；[MEGUTrainer.py](../../../task/MEGUTrainer.py)提供pseudo-label/C&S路径。没有证据证明这些选择导致全部现象，也没有证据支持将其忽略。

**最小修复。** 用E2同一小范围给GIF相对Original的变化量与GU/Original各自到Ret的距离，并核对已有高预算求解日志是否有限/非退化。对MEGU列raw no-update、no-update+同C&S、updated raw、updated+C&S四端点，保持retained监督和pseudo labels匹配。主文用“所评估的移位GIF/零噪声IDEA实例、MEGU pipeline”准确归因；不要先盲目加一圈参数搜索，也不要按最终攻击大小挑参数。

**会推翻当前解释的结果。** 若MEGU的R-point增量主要由匹配no-update+C&S复现，应将其归为pipeline后处理响应；若GIF近Original且仅Ret大幅移动，应放弃“GU自身响应被放大”的机制解释。若主例数值异常超出既有校准，需先修复/验证实例，再讨论科学关系。

## E4 · 重要：080的单一Random请求不能承担跨请求分布基线，训练seed并未解除这一条件性

**段落：** E-P1/E-P3、Q2-P1/P5、D-A2；同时影响Q3的seed解释。**分类：现有数据整理；更强总体表述需要小范围新实验。**

**最强质疑。** 080每预算的Random/Degree请求跨训练seed复用，R-point则随source训练seed改变选集。三seed差值因此同时含模型训练与模型依赖选集变化；不能称固定一对请求的独立三次更新重复，也不能把D_extra当作对Random请求分布期望的精确增量。某个Random请求的预算前缀若特别有利或有害，会改变差中之差。

**证据与已有回应。** [080配置](../../../experiments/configs/exp080/cc_base.yaml)、[逐seed相对表](../2026-10-24-self-audit/analysis/budget_random_seed_contrasts.csv)及v4已披露单Random与n=3；[051/新011库存](../2026-10-24-self-audit/inventory/INVENTORY.md)证明请求重复不是完全空白。新011的10% Random重复可以量化共同预算的请求变异，却不能代替33%的请求分布。079十seed也是source与目标训练随机性联动的实验单位，不是十个固定S的重复重训。

**最小修复。** 若保留描述性B，写成“相对本实验固定Random请求”，并把source/目标训练seed、Random draw、IM draw、split seed的复用关系画成一张紧凑表。先用011的现成Random重复在10%展示请求内/训练seed层次。只有要声称高预算对一般Random请求仍成立，才预先固定CiteSeer 5%/33%、GIF+Ret、三个训练seed，增加两组预先指定且跨预算嵌套的Random draws：共24个方法端点，其中12个Retrain；MEGU可随后复用同一Ret增加12个更新端点。这个小检验应报告所有draw，不能选有利的一组。

**会推翻当前解释的结果。** 若R-point增量落在Random请求分布常见范围，或策略×预算方向因Random draw改变，应把结论收窄为具体请求实例。固定S的R–R仍是另一问题；只有声称“超出重训自然波动”才需要它，不能用这里的Random多请求替代。

## E5 · 重要：基础模型质量控制尚未检验主例 B 的 retained Retrain 参考质量

**段落：** E-P2/E-P5、Q2-P2、A-P3。**分类：先检查已有日志；不足时只做定向训练诊断。**

**最强质疑。** 同请求、同seed、同架构配对并不保证某次有限轮数Retrain是足够好的参照。B最醒目的变化是R-point下Ret约10.561 pp下降；这可以来自删除了关键监督/结构，也可能夹杂删后目标上的优化或checkpoint规则影响。只有原图P0训练诊断，不能区分这两种原因。

**证据与已有回应。** [modular_model.py](../../../experiments/modular_model.py)的监督训练默认交付最终权重；[Retrain实现](../../../unlearning/unlearning_methods/Retrain/retrain.py)使用retained graph重训。078确实已有CiteSeer终轮/validation峰值差别，且候选没有替换正式checkpoint；Cora早停也并非总更好。082的300轮证据属于分片，不适用于GIF/MEGU/GNNDelete或这一Ret曲线。这些材料支持训练来源清楚，尚未支持B对Ret checkpoint选择不敏感。

**最小修复。** 在方法表明示Original/Ret最终3000轮、GNNDelete遗忘50轮及其checkpoint规则、MEGU更新和C&S、分片300轮的不同职责；不要要求所有算法相同epoch或相同时间。先查B的CiteSeer33%、seed42、R-point与Random两个Ret是否保留validation轨迹。若没有，只为这两个冻结请求记录相同训练配置的validation轨迹及预先指定终轮/validation选点对照；目标是判断Ret是否明显失配，不按test找最有利参照。只有发现问题后才扩展到三个seed/两个预算。E1的泄漏修复优先于任何此类敏感性训练。

**会推翻当前解释的结果。** 若合规validation选点或有根据的训练充分性修正使R-point Ret大幅恢复，并消除B的额外D，则B主要反映所选有限训练协议，而非稳定的请求响应特征。若Ret下降在合理训练规则下保留，才更有理由将其解释为删后数据条件变化。

## E6 · 重要：相同节点数控制了名义预算，尚未解释实际删除负荷和请求组成

**段落：** M-P1/M-P3、R0-P1/P2、Q1-P2/P4、Q2-P2。**分类：已有Selection/图上的统计；若宣称因果机制才追加匹配对照。**

**最强质疑。** 等k节点是合法且清楚的预算，但不同策略可能移除不同数量的监督类别、incident edges及训练连通结构。GNNDelete的局部mask由删除边端点扩展而来，R-point大预算可能集中于某些类别；因此“点损失/图耦合损失目标对应不同响应”成立，不代表损失定义本身已与简单请求组成效应区分。Degree更破坏GU也不能只当一句弱化最强攻击宣称的脚注。

**证据与已有回应。** [GNNDelete节点路径](../../../unlearning/unlearning_methods/GNNDelete/gnndelete.py)围绕incident-edge端点构造一/二跳mask；[Hop几何表](../2026-10-24-self-audit/inventory/request_geometry_summary.csv)已给测试覆盖广度，纠正了“没有结构证据”的误读。但它没有给同一请求实际删边数、保留训练类别组成、GU具体mask覆盖；跨selector的Hop分组成员也不同。现有几何不能单独解释A/B。

**最小修复。** 只对A/B已冻结Selection统计k、移除的唯一incident edges、各类别删除数/保留训练数及关键局部mask覆盖，附原图/retained图身份，无需新训练。这不是要求抹平所有策略差异：请求组成正可能是策略的作用路径。若只作描述，保留这些协变量与限制即可；若要称IF定义引起独立于结构/类别的机制效应，再为一个确定主例追加degree/class匹配Random，其他矩阵暂不动。

**会推翻当前解释的结果。** 若R-point Ret下降集中于几乎失去监督的类别，或A主要随GNNDelete mask覆盖改变，则应将解释落到请求组成/实现覆盖，放弃未经控制的损失机制归因。这不抹掉策略实例差异，但会显著改变其新颖性与适用范围。

## 改变判断所需的最小证据与顺序

| 优先级 | 必须先拿到的结果 | 对判断的作用 |
|---|---|---|
| P0 | E1的stage/mask修正及无测试选模的A定向重算；若继续主张十seed，恢复对应十seed证据。 | 决定主发现A能否进入论文。没有这一项，文字修订和推理补算不能使我转向接受。 |
| P1 | B的54引用三端点/两图分析，加MEGU匹配C&S；原始D重现检查通过。 | 决定B究竟是GU变化、Ret变化或pipeline/评价语义现象，并据结果重写贡献。 |
| P1 | 正式参数/选模表、数据/Selection/Output身份与复用层级；080旧分片与当前结果分栏。 | 使主文和匿名材料可复核；不需要先新增全部模型/数据集。 |
| P2 | B主例Ret的定向训练诊断；使用既有Random重复说明变异；补请求组成统计。 | 排除最直接的训练与请求负荷替代解释。新训练仅在既有日志不足或需要更强总体声明时启动。 |

E1若修复后A保留，B完成E2/E3后仍体现明确的策略特定关系，且全文坚持当前固定split/目标模型/所评估实现的范围，我会重新评估为接近边界的经验论文；并不因实验数量多就自动给Weak Accept。若A消失，必须重新判断剩余B及结构分析能否独立承担相对已有工作的贡献，不能把历史交叉藏进附录继续当主证据。

本轮新增的最关键事实是**GNNDelete测试集选模的实际产物绑定**。没有证据证明所有观察都由该问题造成；同样，也没有理由在污染被确认后继续把当前A当作干净结果。正式修复、受影响产物处置与科学采用由后续独立流程决定，本报告不替它们改状态。
