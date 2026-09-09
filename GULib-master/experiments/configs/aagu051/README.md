# Random 多选集实验：最终设计

单张执行表 [table.yaml](table.yaml)。实时执行状态以 canonical 项目 `.workblock/items/AAGU-051/WORKITEM.md` 为准。

| 配置项 | 最终值 |
|---|---|
| 数据集 | Cora、CiteSeer、PubMed，各自固定 Dataset/Split |
| 模型 | GCN |
| 删除预算 | train 候选池的 10% |
| Selector | 公共 random.yaml |
| Random 抽样 seed | 11、22、33、44、55、66、77、88、99、104245 |
| 所有方法的训练 seed | 42 |
| 方法 | GNNDelete、MEGU、GraphEraser、GraphRevoker、Retrain |
| 条件数 | 每数据集50；总计150（120 GU + 30 Retrain） |

研究问题是固定训练seed42下，不同Random删除选集带来的响应分布；不估计训练seed方差，不声称训练seed影响小。每个数据集10组选集跨五种方法共享。不同抽样seed允许选集重合，保留实际清单、哈希及每数据集45对Jaccard，不重抽、不挑seed。

## 本地核验

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu051/table.yaml --dry_run
```

## 评价与分析

evaluation_refs仅引用post_method_metrics.yaml，与原表01一致。unlearning结果的metrics.json自动包含utility行（f1_before、f1_after、f1_drop、f1_drop_ratio），无需额外utility eval。回传后基于已核验数值计算分布统计；缺失before必须保留未知，不能用额外eval补造。每个GU的未删除基线为B_m，分片方法使用未删除ensemble；完整模型P0另行区分。比较同一评价集合/协议下的B_m-U_m,R、P0-R_R、R_R-U_m,R，差异保留符号，不预设下降。GU与Retrain均为seed42，但配对仍必须核验Selection、Dataset/Split、训练配置和删除/评价语义，不能仅凭seed相同认定完整身份匹配。

每数据集、每方法以10组选集为统计单位，报告均值、样本标准差、中位数、范围及逐抽样seed明细。三个数据集分别汇总，不混为30次同分布重复。保存原始输入、Selection和Output引用；缺失和失败不填补、不隐藏。单训练seed不估计GU或Retrain训练方差；重训练差异不可直接称纯遗忘误差，F1不降不能证明遗忘成功。

## 执行边界

正式运行沿用experiments/AGENTS.md的验证、smoke、注册最小gate、版本一致性和可信收集要求。本轮移除GIF/IDEA，不等待049，不作两者的科学结论。保留方法仍需实际before/after语义核验。配置dry-run不是正式GPU证据。后续离线汇总及REPORT.md/REPORT.html必须明确固定训练seed42的结论边界。

## 最小gate

[gate.yaml](gate.yaml)取全表内的104245和11两个抽样seed，覆盖三数据集、五方法，共30格。104245验证默认选集HIT，11验证另一选集执行链；不强迫已有缓存MISS。输出须全部可校验，before/after有限、Selection跨方法一致，seed/预算/输入身份与全表匹配，失败停止扩展。全表使用独立Result并复用gate缓存，保留gate结果。
