# AAGU-053：10% RR 族内采样充分性研究

入口：[rr_sufficiency_10.yaml](rr_sufficiency_10.yaml)。本表替代尚未执行的5% RR充分性配置，不恢复此前取消的5% selection任务，也不改写已完成的053主表。

| 变量 | 定义 |
|---|---|
| 数据集 | Cora、CiteSeer、PubMed；原正式图与split |
| 候选池 | train_mask |
| 删除预算 | 候选池10%；预期K分别189、232、1380，正式执行核对真实候选数 |
| RR样本数 | 1024、4096、16384、65536 |
| 传播概率 | 0.1，继承RR小表 |
| 选点seed | 11、22、33 |
| 阶段 | selector；无训练seed、Retrain或GU |
| 格数 | 3×4×3＝36 |

本表的目标是研究RR数量这一族内变量，不用after F1判断IM质量。普通Selection结果需与独立RR重放结合分析；每个条件使用固定规模的独立验证样本，当前计划为65536个fresh RR sets且不提前停止。

主要记录：accepted gains与累计coverage轨迹、首次零增益位置、zero-gain比例、独立验证coverage或spread、三次selector seed的选集Jaccard，以及RR生产和选择耗时。零增益与否不是充分性单一判据；after F1只作为后续GU实验结果，不回填为RR质量指标。

判定顺序：先核对exact-K、数据/split、候选池、producer和Artifact身份；再比较相邻RR档位在独立验证上的估计值与不确定性；最后选择满足预先声明稳定性门槛的最小RR。若16384到65536仍有实质变化，再只对受影响的大图候选增加262144 selector-only探索，不直接扩大GU全表。

本表完成后形成053的RR族内研究结论；它与053主表的下游F1结论、以及AAGU-011的Table 02跨GU结论分别记录、分别验收。正式执行前仍需Core登记、版本和数据身份核对及运行gate。

权威记录：[AAGU-053 WorkItem](../../../.workblock/items/AAGU-053/WORKITEM.md)。
