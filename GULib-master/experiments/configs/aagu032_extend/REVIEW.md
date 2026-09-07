# 032 扩展配置与 GT-full / GIF 核对

> 本文保留新增all_trainable对照之前的252条件检查记录；当前288条件配置、数据准备及提交说明见[README](README.md)。下文“未绑定”和“未提交”描述当时的检查状态。

已整理为独立extend配置包。用户要求一切正常后提交；当前定义一致性与两份正式数据绑定仍未满足，尚未提交SyncMate运行。

## 扩展配置

| 配置 | 数据集 | 划分 | 预算 | 条件数 |
|---|---|---|---|---:|
| [experiment.yaml](experiment.yaml) | Cora | 70/10/20，seed 2024 | 1%、5%、10%、15% | 84 |
| [experiment.citeseer.yaml](experiment.citeseer.yaml) | CiteSeer | 同上 | 同上 | 84 |
| [experiment.pubmed.yaml](experiment.pubmed.yaml) | PubMed | 同上 | 同上 | 84 |

每表保留原来的7个Selector、Retrain和训练seeds 42/212/2024。当前普通配置契约每表绑定一个Dataset/Split，因此三数据集对应三张表。原始032 YAML不变；扩展表使用新的experiment_id。主结果可以按用户截图呈现Random、Degree、GT-full三行，其余四个Selector作为辅助对照。

预算仍以训练候选节点数为分母并向下取整。例如Cora有1895个训练候选，四个预算分别为18、94、189、284个节点。截图本身无法确定其预算分母、划分、模型和训练设置，不能仅按表格数值声称复现同一实验。

三张表dry-run均通过：12批次、84条件，producer_called=false；总计252条件。[展开证据](../../../.syncmate/aagu032-extension-review/dry-run.json)。

## 核对的实际公式

定义候选v的源方向为 q_v = grad(loss_before_on_affected_training_nodes) - grad(loss_after_on_affected_training_neighbors_excluding_v)。两项在相同模型参数处计算；删除图移除v关联边，保留图上的其余消息传递。

验证目标是 g_val = grad(mean validation cross entropy)，不是标量loss本身。GT-full分数为 q_v^T A(H) g_val，其中A(H)是实际有限步、带damping的LiSSA算子；只有在相应条件和收敛精度成立时才可将其视作逆Hessian近似。

现有实现已先计算共享u=A(H)g_val，再为每个候选算q_v^T u。对于同一个固定、对称Hessian及同一LiSSA设置，这与先计算每个候选A(H)q_v，再和g_val点乘在数学上等价。不能在候选之间更换Hessian后仍复用同一个u。

- [共享IHVP及记忆化](../../target_direct_v1/methods.py:104)：同一次GT-full Score生产中计算一次。不同checkpoint、训练seed、参数范围或求解设置不共享这个向量；目前各独立Selector的Score MISS也可能各自计算。
- [实际LiSSA](../../c_target_v1/core.py:277)：训练mean CE的Hessian、验证mean CE的梯度，默认20步、scale=25、damp=0.01。该递推的收敛目标对应H+scale*damp*I；20步不代表精确求逆。
- [两次源梯度及内积](../../c_target_v1/core.py:381)：grad1-grad2与inverse_target点乘；使用autograd.grad而非累积到参数.grad，功能上仍是反向求导。原图forward可以跨候选共享，删点图forward按候选计算。

独立float64 CPU小图检查通过：直接在候选侧执行LiSSA与共享目标侧计算的标量差约2.78e-17；现有GT-full与手算两次梯度差的结果一致，误差0；IHVP与显式Hessian有限多项式误差约5.20e-17。另有4项图源梯度测试通过。此检查证明计算顺序与当前公式吻合，不证明全参数GIF与现有默认配置数值相同，也不证明LiSSA在正式数据上收敛。[检查代码](../../../.syncmate/aagu032-extension-review/check_direction.py)、[数值证据](../../../.syncmate/aagu032-extension-review/direction-check.json)。

## 与仓库GIF仍有的区别

| 项目 | 当前GT-full | 仓库GIF节点遗忘实现 |
|---|---|---|
| 源方向 | 原图/删除图梯度之差 | 同样使用grad1-grad2 |
| 参数范围 | 默认last_layer | 全部requires_grad参数 |
| Hessian loss | 训练CE，mean | 训练CE，sum |
| 默认LiSSA | 20步，scale25，damp0.01 | CLI默认100步，scale1e9，damp0 |
| 源loss标签集合 | 受影响节点与train_mask交集 | get_grad使用influence_nodes；邻居构造未在该路径显式与train_mask取交集 |
| 消费结果 | 验证集loss变化的线性近似，用于排序 | 将参数变化实际加到模型权重后评估 |

GIF证据：[get_grad](../../../unlearning/unlearning_methods/GIF/gif.py:443)、[approxi](../../../unlearning/unlearning_methods/GIF/gif.py:771)、[邻居构造](../../../unlearning/unlearning_methods/GIF/gif.py:712)。源loss限制在训练标签的边界应保留；不能为字面复制历史实现而把测试标签纳入选点。

因此当前可以称为“GIF型梯度差投影”，不能称为“完全等同于仓库GIF”。若下一步要求严格对齐，需要先明确并对齐参数空间、Hessian归一化与LiSSA设置，同时核验前向图和源集合边界。本次仅检查，没有暗改公共gt_full.yaml或实现代码；扩展表目前仍引用原gt_full。

已有计算优化之外，Computations.graph目前通过point()取得验证梯度时，还会计算一整份候选逐点梯度矩阵；GT-full最终评分不需要这份矩阵。后续可将验证梯度提取独立出来，并验证分数与排序不变。正式数据上的IHVP残差、方向与g_val的夹角也值得测量；不能仅因GT-full与p_graph重合就断定公式错误或逆Hessian收敛。

## 数据与HIT边界

Cora的70/10/20 seed2024正式数据和manifest已绑定。CiteSeer、PubMed的公共小表中manifest、manifest_sha256和split_hash目前均为null；本次SSH只读检查在固定transductive目录下只发现其public_fixed或旧80/0/20资产，未发现要求的70/10/20资产。两张配置可展开，但还不能执行；需要准备并绑定指定划分的正式资产，不能给旧数据改标签冒充。

本次保留现存缓存。若生产实现、有效输入与依赖身份不变，Cora原1%/5%的42个输出有望精确HIT；新增10%/15%可复用Score，新的Selection与Retrain输出需要计算。跨数据集不复用Cora的Score、Selection或模型输出。若之后修改GT-full以对齐GIF，其受影响Score及下游输出应形成新身份，不能预先承诺这些条件仍HIT。实际命中以SyncMate运行回传的HIT/MISS收据为准。
