# 指标、实现与三端点对照的有效性自审

2026-10-24（Asia/Shanghai）。只读研究审计；仅在本目录新增 CPU 汇总，不修改提纲、核心程序、实验记录或科学接受决定。HTML 由父任务统一生成。

## 判断与需要纠正的认识

**详细提纲的观察性主线可以保留，但 F-B 应先补上 Original–GU–Retrain 的行为诊断，不能把“GU准确率变化小、GU–Retrain不一致率增加”直接升级为遗忘能力发现。此前把 059/061/062/065–068 主要当成数值可信度附录，遗漏了其中已有的 no-update 和双评价图证据，是需要纠正的实验理解。**

本轮直接复核四组固定 checkpoint 验证的 **460 个已收集、已在可信索引登记的文件**，重新比对 SHA-256、run manifest 和逐 cell 文件身份；重提取 **72 个 GIF/IDEA Observer 条件，其中 T100 生产条件 24 个**。固定训练 seed=42、Random 请求种子104246/104247/104248、10%训练节点预算；不增加GPU任务。

完整产物：[复算脚本](analyze_validity.py)、[逐条件CSV](calibration_rows.csv)、[汇总JSON](calibration_summary.json)、[来源及哈希](calibration_provenance.json)。

关键源证据：[062接受范围](E:/project/OpenGU/GULib-master/self/research/analyses/EXP-062/closeout-20260924.md:14)、[066原图/保留图与no-update说明](E:/project/OpenGU/GULib-master/experiments/configs/aagu066/README.md:14)、[CiteSeer数值及no-update原分析](E:/project/OpenGU/GULib-master/self/research/analyses/EXP-067/validation-h64-20260924.json)、[PubMed对应分析](E:/project/OpenGU/GULib-master/self/research/analyses/EXP-068/validation-h64-20260924.json)、[same-graph Observer的节点范围](E:/project/OpenGU/GULib-master/experiments/observers/same_graph_change.py:55)、[MEGU Before/After输出组成](E:/project/OpenGU/GULib-master/experiments/modular_megu.py:104)、[主表冻结profile](E:/project/OpenGU/GULib-master/experiments/configs/profiles/gif_idea_fixed_pt.yaml:1)、[Metrics已有case](E:/project/OpenGU/GULib-master/experiments/modular_evaluation.py:14)、[Output恢复模型入口](E:/project/OpenGU/GULib-master/experiments/unlearning_outputs.py:275)、[常规回传内容边界](E:/project/OpenGU/GULib-master/docs/experiment-result-return-contract.md:69)。

## 1. 已有 no-update 对照应承担什么职责

059 的原作者参数诊断保留了真实失败：两个宽度的十二格均未产生有效更新后效用。061 交付了作者训练超参下的 OpenGU GCN 权重，但没有证明该模型达到数学驻点或原生作者前向被精确复现。后续062/065–068采用与各固定 checkpoint 绑定的正移位参数，验证了四组条件的有限性、HVP、移位残差、写回及非零行为变化。

这些不是“仍待做的最基础数值实验”，也不是“所有主表条件已经验证”。证据的精确角色如下。

| 证据 | Original 角色 | GU 角色 | Retrain 角色 | 已有判断及缺口 |
| --- | --- | --- | --- | --- |
| 066 Cora H16/H64；067 CiteSeer H64；068 PubMed H64 | 同一固定PT在 original 和 retained 两图上的 no-update 预测；保存同图更新前后的参数及logit差 | GIF/IDEA，T100/200/400；同图更新后效用、全节点类别翻转 | 每请求一次同宽度、3000轮重训；已报告original图测试效用 | 可以排除这些校准条件下完全未写回、精确零更新或零logit变化；不能判断完整预测/参数重训接近性，也不覆盖MEGU或高预算 |
| 079/e79r6 | 每个方法自己的Before效用；Output持久化`logits_before` | 已有测试效用、GU–Retrain测试预测不一致率 | 同请求、同评估图重训端点 | 本地常规回传没有逐节点logits；Original–GU、Original–Retrain的行为三角未由当前图表闭合 |
| 080 | 同样有方法Before效用；远端Output保留更新前预测 | 5%–50%的效用与同请求Retrain不一致率 | 已有每个请求的Retrain | 预算现象可描述；不足以确定D上升主要来自GU变化、Retrain变化还是两者同时变化 |

来源：`self/research/analyses/EXP-062/closeout-20260924.md:3–16`；`experiments/configs/aagu066/README.md:3–20`；066/067/068 validation JSON；`.workblock/items/AAGU-059/REPORT.md:19–27,69–75`；`.workblock/items/AAGU-061/REPORT.md:9–14,34–57`。

### 本轮CPU提取出的具体结果

下表只展示 GIF 的T100范围，IDEA对应记录保留在CSV/JSON；它们在当前零噪声、近相同参数实现下高度接近，不能算两份独立验证。“翻转”是**全部节点**上GU与同图no-update的argmax差异；不能直接与正文测试节点上的GU–Retrain D相比。

| 固定checkpoint | 参数相对L2变化，三请求均值 | 原图logit最大绝对变化范围 | 原图全节点翻转，三请求均值 | 原图测试accuracy变化范围（pp） |
| --- | ---: | ---: | ---: | ---: |
| Cora H16 | 0.0002487 | 0.391–0.526 | 0.369% | +0.185至+0.554 |
| Cora H64 | 0.0002557 | 0.347–0.615 | 0.431% | 0.000至+0.185 |
| CiteSeer H64 | 0.0001643 | 0.194–0.257 | 0.321% | −0.150至+0.150 |
| PubMed H64 | 0.0001381 | 0.100–0.200 | 0.093% | −0.051至−0.025 |

**精确判断：存在真实的参数写回和同图logit变化，同时类别变化与测试效用变化较小。** 它排除这些格子的“完全不更新”，没有排除较强正移位导致的小更新、分类margin掩盖更新、保留信息过多等解释，也没有证明任何一种解释。参数相对L2对重参数化敏感，不能单独衡量遗忘充分性。

72格写回检查均为`actual_vs_expected_max_abs=0`；移位方程相对残差最大 **3.4860e−7**，但**原方程相对残差为0.1965–0.5559**。这清楚地区分了“准确求解当前移位系统”和“准确求解未移位的删除近似方程”。不能将前者称为原方程已收敛，更不能从该通过推导遗忘正确。

## 2. 平稳效用与D上升尚存哪些替代解释

### GIF/IDEA：已验证的是固定条件的移位实现

当前主表`experiments/configs/profiles/gif_idea_fixed_pt.yaml`按数据集、架构和宽度提供冻结scale/damp；`gif_h64.yaml`与`idea_h64.yaml`均`checkpoint: null`，每个训练seed使用自己的checkpoint。参数校准绑定seed42的一组固定PT，不能视作对另外九个seed、所有selector和080高预算逐格完成了数值校准。提纲E-P2目前只有“参数冻结、输出近重合”，需要补这项适用范围。

此外，IDEA当前配置`gaussian_std=0`，使用OpenGU GCN和本项目adapter；GIF/IDEA共享近乎相同的局部source/移位数值行为。可以报告这两个具体实例，不应无条件把结果归结为完整原论文算法或将IDEA这一实例称为已验证的certified unlearning。

具体方法解释先补：同一测试mask上的Original–GU类别差异、logit/probability变化、GU与Original各自到Retrain的差异。若GU近似保持Original，而Retrain随请求变化很大，D上升主要反映两条更新响应不同，不能写成GU自身预测在预算轴上同幅改变。

### MEGU：不能把Before→After全部当作权重更新

`experiments/modular_megu.py:104–123`的Before是原始GCN直接前向；After经过`megu_logits`的Correction & Smoothing，使用保留监督mask与原始预测生成的pseudo labels。`task/MEGUTrainer.py:103–119`保存了这些更新前pseudo labels。**当前pipeline前后比较包含参数更新及输出后处理两部分。**

因此要区分原始no-update GCN、no-update GCN+相同C&S、更新后GCN原始输出、更新后GCN+C&S四种观察。C&S对照须使用同请求的retained supervision、同评价图和相同pseudo labels，避免把删除标签重新作为anchor。当前066–068没有MEGU Observer，不能借用GIF/IDEA的“非零更新已验证”结论解释MEGU。

这项是已确认的比较组成差异，不是已确认的程序错误；也不能据此断言C&S解释了全部平稳现象。

## 3. 节点删除与评价图不能被过度统一

`experiments/node_deletion.py:9–22,26–42`明确声明：训练节点监督被排除、训练关联边移除、特征行保留；默认在original graph评价。`Retain`构图保留节点索引和特征行；原图评价时原边与原特征重新参与前向。GU与Retrain使用同一评价图，这是当前配对的明确协议，不是证据错配。

但“所有GU都在相同保留图上训练”不准确：Retrain确实在retained graph重新优化；IF类沿原checkpoint的原图Hessian和删除source近似更新；GNNDelete处理其删除mask和局部约束；MEGU还有保留监督与C&S；分片方法保留自己的训练与聚合路径。**统一的是请求身份、参照和评价契约，不是每个方法的内部目标或训练过程。**

原图测试结果可称“删除训练信息后回到原图的响应”，不能无条件解释为部署时永久移除节点及关联信息的效果。retained-graph敏感性检查尚未在079/080闭合；066–068已有两个图上的GU/no-update对照，但没有retained-graph Retrain输出，不能直接填作主表的新图敏感性结果。

共享full-graph GCN Retrain对GraphEraser/GraphRevoker包含模型家族差异；GraphRevoker必须标明GPA+optimal实现。`E_M`扣除Random gap会改变参照问题，但不会自动消除架构、请求交互、优化和评估图的全部差异。

## 4. 哪些可以无新训练补，哪些本地仍做不了

### 4.1 本轮已经补完

已独立复算上文校准no-update/双图/写回/残差证据。由可信raw文件直接生成，全部来源与输出哈希在`calibration_provenance.json`。这应进入设置与解释证据链，而非只在附录写一句“校准通过”。

### 4.2 080关键案例的最小CPU闭环规格

**本地不可直接闭环，远端已有Output支持不新增训练的定向分析。** 主表run回传仅`metrics.json`与`selection.json`；索引中080的模型/预测npz或PT为0。常规回传边界见`scripts/syncmate/AGENTS.md:27`与`docs/experiment-result-return-contract.md:46,69`。

现有独立Metrics入口确实可以读取既有Output重算已有四种evaluation case，但没有三端点行为case，也不重新forward另一张图（`experiments/modular_evaluation.py:14–43`、`experiments/modular_run.py:153–208`、`experiments/unlearning_outputs.py:75–82`）。不能把“有Metrics接口”写成“该分析已能通过任意YAML直接得到”。

建议只做以下定向、只读CPU分析，不在本任务提交：

1. **范围：** CiteSeer、R-point、5%和33%、训练seed42/212/2024。先取GIF和MEGU，共12个GU输出及6个同请求Retrain；IDEA因高度重复不是最低必要条件。逐一冻结原run、cell、Output/Selection身份与hash。原始来源为`exp080-cc-base/e80r305`，不得重构为后来的协议。
2. **原图行为三角：** 从每个GU Output已存`logits_before`、`logits`和同请求Retrain logits计算`D(O,GU)`、`D(O,R)`、`D(GU,R)`，固定相同test mask；同时报概率变化、CE及accuracy。枚举O=GU=R、O=GU≠R、O=R≠GU、GU=R≠O、三者皆不同五类节点。这样可区分GU停留在Original、GU发生额外变化、GU跟随Retrain变化。它们仍不是隐私或完整遗忘测试。
3. **retained图敏感性：** 若原checkpoint及保存的GU/R权重均可按身份只读恢复，用`restore_model`及`retained_graph`做CPU前向，不更改现存Output。6个原模型、12个GU和6个R的基本覆盖为24次retained图模型前向；MEGU另计算匹配的C&S有/无更新对照。若复用同一forward得到的概率，C&S无需额外模型前向；直接调用含forward的`megu_logits`则应按调用次数增加计数。若原checkpoint缺失，明确缺口，禁止以自动prepare_model的训练回退补齐。
4. **交付：** 新分析目录保存精确引用、图/mask/状态hash、每seed每请求结果、归并规则及校验；默认只回传新的统计证据，遵循现有预测payload不进入常规包的边界。必要时单独批准/设计远端分析接口，不篡改不可变Artifact或替换原run。

原图三角只需读取预测数组，不训练；retained图敏感性只需恢复现存模型并前向，也不训练。它们当前是可执行分析规格，**本轮未远端执行**。

### 4.3 Retrain–Retrain校准：按主张决定是否需要新训练

仅写“GU与此同请求R的D为多少”“accuracy与该D变化不同”，无需先证明R是唯一正确函数。若写“异常偏离”“遗忘失败”“不一致明显超过重训自然波动”，则需要同请求R–R参照，不能画`R对自身=0`充当实验校准。

可先对现有080中实际请求完全相同的Random/Degree跨训练seed Retrain输出计算R–R差异，无需新训练；先验证节点集合、split、训练/评价图一致。这只能提供这些请求的经验自然波动，不能直接替代R-point的每请求校准。

R-point按训练seed改变所选节点，不能把不同请求的R_i与R_j当作同请求重训噪声。若要对上述六个R-point请求做最低限度三seed的请求内R分布，每个固定S已有一个R，还需两个独立初始化R，共 **12个新增Retrain训练**；固定S、其训练数据和全部超参，只改重训初始化seed。它是尚未启动的条件性科学增强，也不应因缺它而否认现有描述性结果。此规格还需按Runbook核查现有冻结Selection提交能力、估时和新运行身份。

## 5. 对详细提纲的准确修订建议

| 当前位置 | 应补内容 | 不能升级为 |
| --- | --- | --- |
| E-P2，约289–297行 | 四固定checkpoint、Random10%的数值与no-update验证；说明主表沿用冻结profile而非逐格校准；说明IDEA零噪声与MEGU C&S | 所有主表输出均数值收敛、原算法完整复现 |
| Q2-P2，约404–412行 | F-B仍是观察性分离；紧接Original三角和no-update替代解释的状态；三seed变化不是统计等效 | GU不更新、未遗忘、已建立机制 |
| D-P2，约527–535行 | 区分“已有校准条件no-update证据”与“主表关键条件还缺行为三角/retained图” | 把所有no-update诊断统一写成尚未做过 |
| 方法与限制 | `E_M<0`是signed gap变化；D是相对某次重训输出；图与方法变体具体声明 | 绝对误差下降、遗忘质量提升、法律删除完成 |

**最小结论：** 已有证据足以保留F-A和描述性F-B；有价值且可立即补的关键工作是现有输出上的行为三角与评价图敏感性，而不是先扩大GPU实验数量。是否开展R–R新增训练，取决于作者是否要把观察提升为经过自然波动校准的遗忘偏离结论。
