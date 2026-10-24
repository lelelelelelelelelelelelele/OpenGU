# 第三轮第二阶段执行补充：确认与解释控制

版本：1.0 · 2026-10-24。本文细化既有[冻结协议](ROUND3_EXECUTION_PROTOCOL.md)的S3.2／S4。原主要差、方向、确认seed、样本数、停止规则、三类复审门槛均不改变。本文及配置身份在本阶段首次派发前冻结；不能用后续测试结果回改。

## 进入本阶段的已知证据

EXP-084/e84r1已通过正式可信回传和30个GU实际validation checkpoint取证；十seed的ΔR、ΔG两个97.5%双侧t区间分别完全高于、低于零，10/10同seed双向成立。该事实仅触发原协议的五seed确认分支，不等于确认成功或写作通过。旧GNNDelete输出保持隔离。

B第一层gate已执行但当前项目回传验收被expected_cells缺失阻塞。先以经过真实CLI／collection验证的AAGU-109修复声明，对同一已完成job重新验收；不得绕过可信链或为此重复GPU。其完整第一层范围保持原54引用。

## A：预定五seed确认

- seed固定1701、1709、1721、1733、1741，Cora固定split、10%、SGC-source、R-point／D-full／Degree，GNNDelete与同请求Ret共30端点。
- 现存62份远端run声明、26221个cell未出现上述seed；唯一旧schema以hash相同本地声明的cells[].training.seed补核为四项42。保留原审计与补充解析，明确不覆盖已删除／无manifest历史。
- 完成全部五seed后一次判断：至少4/5同seed满足ΔR>0且ΔG<0；两个97.5%双侧t区间还须完全位于预定方向。任一未满足记未确认；不增加seed、不合并探索十seed补显著性、不换主要指标。
- 新确认需要新的联合请求／训练生成，允许既定unlearning链按配置构建资产；必须逐请求核对GU与Ret的Dataset/Split／Selection／模型与训练seed，不能把旧十seed请求换标签复用。
- GNNDelete仍按validation选择，使用与十seed重算相同的生成指纹；运行后逐Output绑定runtime best checkpoint与导出权重，所有15个新GU条件均须有原生生成证据。
- 单次预算7025秒，沿用既有冷预算的分项：5×[2×Selector300+2×模型准备120+固定400]+30×IO20+15×[GNNDelete3+Ret12]。1240秒的每seed部分不含GU更新，最后225秒同时含15个GU及15个Ret；固定／IO项包括必须完成的checkpoint来源与权重取证和导出开销。这是全MISS串行的低置信工程估计，不因旧十seed跑得快而改低。timeout14400秒不是预计完成时间，排队与传输另记，作业与额外取证实际耗时分别记录。

## A：同一十seed的20对解释

固定e84r1 SHA256为3f9eb5f4d51c1153153d53ce466e1bbcb2050969f58f6e78541ea9d6f7a45307。引用十seed×R-point/D-full的20个GU及20个精确匹配Ret；Degree只保留效用边界表，不把解释缺失冒称已覆盖三策略。

先运行seed42两策略的2对技术gate；技术有效后完整20对均执行，不按科学方向裁剪。每对输出第一层O/G/R三角、五类关系×真值、请求删边／类别／局部覆盖，以及同权重两评价图。GNNDelete两个deletion masks均使用Output保存的布尔数组，显式移动到执行设备，原图、retained图及原图回放不变；不按新图重算掩码，不使用C&S。

全MISS预算：gate600秒=固定读取300+每对90×2+导出120；完整1500秒=固定开销300+每对60×20。两作业合计2100秒，不扣除可能精确复用的gate条件，不假设跨方法共享权重；timeout分别1800／3600秒。

## B：两图与匹配C&S

继续使用e80r305的原54个精确Output引用，源SHA256为c3749e44045e0b770c95ceea066c68d1892c9a99d57377dd286f61c863ab7582。CiteSeer、5%／33%、R-point／Random／Degree、seed42/212/2024、GIF/MEGU/Ret；有效诊断为36GU–Ret对，18Ret引用不单独产生自配对输出。

gate为33%／R-point／seed42的2GU对；技术通过后无条件完成全36对。Original由GU的精确初始checkpoint恢复，GU与Ret由保存权重恢复；缺失或错配即失败，不能隐式训练。

每张评价图使用相同节点、特征、真值和test mask，仅改变删除节点incident edges对应的边集。MEGU四端点为raw Original、匹配C&S Original、updated raw、updated+C&S；固定Output保存的同一Original原图pseudo-label、retained监督mask及原参数。两图不重新生成pseudo-label，不以真值替换锚点。C&S常量及Torch/PyG环境进入评价身份。

原图复现容差预先固定：raw logits atol1e−5、rtol1e−4；MEGU归一概率最大绝对误差1e−5；CE差1e−4；全节点argmax与真值整数计数必须相同。先原图复现，再换图，最后原图回放；权重、输入、保存mask与pseudo-label保持不变。超出容差保留失败并停止扩展，不根据结果放宽阈值。

gate预算600秒=初始化／读取300+每GU90×2+导出120；完整2040秒=固定240+每GU50×36，合计2640秒。全MISS串行、未假定跨方法共享；新forward/C&S未实测，属于低置信工程估计。timeout分别1800／3600秒。换图效应减弱／消失也是结果，不能删条件。

## Ret质量：在旧权重推理之后

本阶段先完成A五seed确认、其checkpoint取证与判断，以及A/B既有Original权重的全部推理，再合并部署AAGU-110共享训练循环观察改动。确认须保持与十seed相同的相关生成指纹；不能在新训练身份下运行后再追认等价。此顺序同时防止旧Original资产定位失效，不添加相似权重搜索或兼容映射。

Ret validation固定在retained训练图、原split val_mask上，每轮只读记录train CE、validation CE／accuracy及学习率。3000轮后只测试best（最大validation accuracy、并列最早）与final两个预定端点，主test仍为原图。保存新run-owned权重与预测，不覆盖旧Output，不把best冒称旧fixed-final参照。真实CPU验证须证明有／无observer的最终权重和RNG相同，test标签变化不影响选择。

pilot仍为CiteSeer33%／seed42／三策略；最优−终轮validation accuracy≥1pp或末500轮val CE比前500轮增加≥10%触发优化敏感。无论pilot是否触发，只要B承担核心且解释删除数据引起Ret响应，就完整覆盖三seed×三策略九条轨迹；复用合格pilot三条，不重复训练。

正式pilot须比较新final与绑定旧Ret的权重／预测／固定test端点；未经解释的差异停止扩展，不能仅用CUDA随机性一句带过。任何缺轮次／非有限值为失败。预算pilot420秒=固定180+80×3，余六条660秒=固定180+80×6；总1080秒。该部分配置与实现尚需另在自身开跑前固定，本文不冒充已经派发。

## 完成规则与文章出口

所有阶段记录实际执行SHA、配置与Recipe身份、源run／Output、全MISS预算、实际作业时间、失败attempt和可信回传状态。一个控制通过只回答相应问题；C&S差或关系计数分解不能当可加因果贡献，请求组成不能冒称已被匹配控制。

A确认不足时按v1降为探索案例；B控制显示主要为Ret变化、后处理或评价图边界时据实改写，不称GU额外破坏或遗忘失败。只有完整证据包经V/C/E/I/P检查、理论／实验／分析三类均至少Weak Accept、根任务同意，才将writing_gate置pass。当前not_met。
