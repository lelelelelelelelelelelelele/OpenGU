# Table 02：10% IF / IM 跨GU比较

归属AAGU-011；原Table01及历史结果保留。Table02取代误归053的rr_gu_05配置；053仅保留其IM组内实验与RR充分性检查。本表把四种GU和同条件Retrain放在一个统一实验矩阵中。

| 轴 | 配置 |
|---|---|
| 数据集 | Cora / CiteSeer / PubMed |
| 候选池与预算 | 原正式train_mask候选池的10% |
| IF | R-point、D-full末层两跳，消费当前公共小表有效参数 |
| IM | RR-4096 / 16384 / 65536，传播概率0.1，各选点seed11/22/33 |
| 基线 | Degree、PageRank、Random；Random选点seed11/22/33/44/55/66/77/88/99/104245 |
| 训练seed | 42 / 212 / 2024，沿用011 |
| GU | GNNDelete / MEGU / GraphEraser / GraphRevoker |
| 独立参照 | 同条件Retrain |

每个数据集、训练seed下有23个选点请求：2个IF＋9个RR＋Degree＋PageRank＋10个Random。三数据集、三训练seed共207个选点条件；[table02.yaml](table02.yaml)在同一个矩阵中展开四种GU和Retrain，共207×5＝1035个method cell，其中828个GU cell和207个Retrain cell，形成207组GU/Retrain配对。训练seed与选点seed是独立轴，不能将重复使用的同一RR/Random选集当作新的独立抽样。Random保留此前确认的十选集基线；旧Table01的单Random设置不覆盖此轴。

GIF、IDEA暂不参与；CELF不新增。普通配置不产出完整RR增益轨迹，采样充分性不能由dry-run或成功选点证明。053的RR族内充分性研究独立记录，不由本表替代；本表也不预先声明任一RR数量充分。

使用正常入口和完整计算身份复用缓存，新增表名本身不意味着重算，预算/输入/生产实现等变化可能导致MISS。053已完成的10%主表不能替代本表的四种GU方法与三训练seed；合法Selection复用仍须按完整身份核对。正式运行使用独立run身份，保留旧结果。当前只建立/校验/提交配置，Core登记、实际HIT、GPU执行与收集尚待完成。

论文评价固定原图测试节点/标签，报告各GU自身before/after、同预算Random对比及配对Retrain；分片方法使用自身ensemble before，与普通GCN Retrain之差含架构/聚合差异。所有预算/R/seed按预定条件展示，零增益补齐和弱效果如实披露，F1不等于遗忘正确性证明。
