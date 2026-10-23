# Hop / locality 与 update-detection 覆盖补充审查

**Hop分层已真实计算，详细提纲遗漏了一层可直接分析的空间响应证据。** 本轮从当前e11r1/e79r6及EXP080三个采用批次逐格读取5,985份metrics，逐一验证run、delivery manifest及trusted index SHA，以及同请求Retrain完整Output引用。5,124个GU配对都有1/2/3/>3-hop的分母、分歧数、分歧率；全部20,496个分层非空，分层计数相加严格还原总D。没有只凭case名称判为完成。

| 实验/批次 | GU有完整Hop | Retrain不适用 | GU update-detection computed | Retrain missing_original_predictions |
|---|---:|---:|---:|---:|
| EXP011 / e11r1 | 1,242 | 207 | 1,242 | 207 |
| EXP079 / e79r6 | 2,160 | 360 | 2,160 | 360 |
| EXP080 / e80r305+r302+r306 | 1,722 | 294 | 1,722 | 294 |

011/079有重叠请求和训练seed，这些是字段覆盖计数，不能求和为5,124个独立科学样本。080保持旧分片协议，新011/079保持新loss+300轮协议，分别分析。

## 指标真实含义与缺失

- `experiments/flip_hop_metrics.py:27–37,40–68`：在原图edge_index上计算到删除集合的**无向、多源最短距离**；按1、2、3、>3（含不可达）分组。测试mask排除选中节点，比较GU与同请求Retrain的argmax类别。距离图与预测图语义分开保存。
- `1_hop_count / 1_hop_flipped_count / 1_hop_flip_rate`等四组字段俱全；`fraction_flipped`是整体GU–Retrain分歧。它不是GU相对Original的翻转，也不是遗忘节点成员泄漏，不应直接命名为collateral damage。
- 全部GU更新检测AUC已为computed且数值合法；全部Retrain是missing_original_predictions，值与before均为null。`experiments/output_metrics.py:31–47`实际比较原模型/删后概率向量的L2变化，用selected nodes为正、test nodes为负，按n=min(二组数量)取各自前n个。不是随机匹配采样或通用MIA。不能因Retrain缺before而声称所有GU更新检测都没计算。
- 本批metrics没有节点到shard/partition的交叉分母与分歧数。GraphRevoker的GPA+optimal方法名和num_shards元数据不等于有空间分区响应。现有本地metrics可以做hop分析；按实际分片归属归因需要独立可核验的assignment/Output证据。

## 新提取：请求覆盖几何

下表仅用EXP011/e11r1、10%预算，Random十抽样和IM三抽样先在各训练seed内平均，再对3个训练seed等权；geometry按请求去重方法坐标，不重复计六份相同分母。百分数是测试节点落入相应距离带的比例，**不是IC传播概率或RR覆盖估计**。

| 数据集 | selector | 1-hop测试节点% | <=2-hop测试节点% | >3-hop测试节点% |
|---|---|---:|---:|---:|
| Cora | random | 23.04 | 65.04 | 14.78 |
| Cora | degree | 54.24 | 77.86 | 13.47 |
| Cora | r_point | 17.71 | 53.32 | 24.54 |
| Cora | gt_full | 25.71 | 56.95 | 24.29 |
| Cora | rr_65536 | 54.80 | 83.52 | 8.55 |
| CiteSeer | random | 16.62 | 42.60 | 41.37 |
| CiteSeer | degree | 36.19 | 50.60 | 41.14 |
| CiteSeer | r_point | 15.87 | 37.34 | 45.65 |
| CiteSeer | gt_full | 16.42 | 37.49 | 45.45 |
| CiteSeer | rr_65536 | 36.04 | 59.81 | 31.38 |
| PubMed | random | 21.58 | 79.36 | 4.26 |
| PubMed | degree | 63.62 | 87.12 | 2.36 |
| PubMed | r_point | 13.61 | 57.75 | 12.10 |
| PubMed | gt_full | 28.63 | 68.46 | 7.39 |
| PubMed | rr_65536 | 39.21 | 86.49 | 1.69 |


IM-RR65536的测试节点两跳覆盖在Cora/CiteSeer/PubMed为83.52/59.81/86.49%，R-point为53.32/37.34/57.75%。这说明不同请求使测试节点处于不同的几何暴露范围，提供“传播导向选点与局部梯度选点构成不同空间请求”的描述性支撑。但它不能独立证明IM实现优化了IC扩散目标，也不证明更广覆盖导致更大GU损害。Degree在Cora/PubMed的一跳覆盖还更高，故不能称其为IM独有结构。

## 新提取：完整方法面板的局部分歧

每格为 **1-hop D / >3-hop D (%)**，仍是EXP011/e11r1、10%和3训练seed均值；所有请求重复先在训练seed内平均。GIF/IDEA近重复，表中只显示GIF；完整CSV仍保留IDEA、PageRank和三RR规模，以及079所有source、080所有预算。

| 数据集 | GU | Random | R-point | D-full | IM-RR65536 |
|---|---|---:|---:|---:|---:|
| Cora | GIF | 4.08 / 0.50 | 26.87 / 0.25 | 10.44 / 0.26 | 3.63 / 0.00 |
| Cora | GNNDelete | 28.80 / 0.50 | 52.61 / 0.25 | 64.35 / 0.26 | 26.14 / 0.00 |
| Cora | MEGU | 4.42 / 1.26 | 21.59 / 0.25 | 10.59 / 1.01 | 4.53 / 0.00 |
| Cora | GraphEraser | 13.20 / 12.64 | 26.74 / 9.86 | 23.41 / 7.32 | 13.13 / 14.54 |
| Cora | GraphRevoker | 23.49 / 19.91 | 33.52 / 18.63 | 35.15 / 18.97 | 26.50 / 14.08 |
| CiteSeer | GIF | 11.26 / 3.43 | 24.95 / 2.53 | 12.56 / 3.85 | 6.48 / 3.55 |
| CiteSeer | GNNDelete | 15.26 / 3.38 | 30.97 / 2.72 | 29.30 / 3.63 | 10.00 / 3.50 |
| CiteSeer | MEGU | 10.50 / 5.36 | 26.77 / 4.77 | 17.88 / 5.69 | 6.25 / 5.67 |
| CiteSeer | GraphEraser | 15.36 / 23.12 | 27.76 / 18.76 | 26.91 / 19.80 | 12.08 / 25.09 |
| CiteSeer | GraphRevoker | 17.16 / 25.59 | 29.66 / 21.94 | 27.36 / 22.70 | 14.43 / 26.63 |
| PubMed | GIF | 1.68 / 3.26 | 11.46 / 2.23 | 3.81 / 2.36 | 2.34 / 2.00 |
| PubMed | GNNDelete | 7.49 / 3.22 | 20.64 / 2.67 | 14.24 / 3.33 | 14.05 / 2.27 |
| PubMed | MEGU | 3.41 / 9.09 | 19.04 / 5.25 | 9.95 / 6.27 | 4.75 / 9.64 |
| PubMed | GraphEraser | 6.58 / 10.50 | 11.50 / 8.20 | 9.35 / 7.91 | 8.44 / 12.71 |
| PubMed | GraphRevoker | 7.56 / 11.02 | 12.73 / 8.63 | 10.34 / 9.06 | 9.41 / 14.17 |


可供写作检验的候选认识：在Cora，R-point对GIF/GNNDelete/MEGU的1-hop D为26.87/52.61/21.59%，>3-hop均约0.25%；IM对应1-hop为3.63/26.14/4.53%、远处约0。分片方法则有明显远处背景分歧：GraphEraser在R-point/IM的>3-hop D为9.86/14.54%，GraphRevoker为18.63/14.08%。CiteSeer同样要保留分片的远处分歧，PubMed MEGU等条件还存在远处高于近处的反例。**不能把全方法面板概括为分歧仅局部传播。** 分片与单GCN Retrain的架构差异仍在背景D中。

这些数据支持把“几何覆盖广度”与“条件距离带内的分歧强度”分开，而不是用一个整体D解释空间机制。跨selector的hop组成员不相同、分母不同；在更大预算下大批测试节点会移入近距离带，曲线变化也可能受组构成影响。当前数据没有给出因果中介/反事实对照，不能宣布IM传播机制或IF局部机制已被因果验证。

## 对提纲与后续分析的建议

1. 在R0“请求差异”或附录B加入紧凑的**测试节点距离分布**表，补选集overlap以外的结构差异；使用“two-hop reach of the request”而非IC spread。
2. 在Q2或附录D加入**按hop分层的GU–Retrain分歧**图，必须同时给节点占比/分母。可用3数据集×5去重方法、selector不同颜色的1/2/3/>3带剖面；完整矩阵已经可从本目录CSV生成，无需GPU补算。
3. 若主文空间不足，只在机制解释段给一个严格限定的近/远对照，并指向全矩阵附录。不能只展示Cora/GIF而忽略分片远处背景与PubMed的反例。
4. 当前只能称“空间分层响应”或“locality diagnostic”；GU–Original collateral、概率距离、实际shard assignment、重复Ret自然变化仍需其各自证据。update-detection已有值，但不应为了填隐私主题将它升级成MIA结论。

## 复核材料与统计层级

- `hop_cells.csv`：20,496行，每个原始GU×四距离带的nodes/flipped/rate及完整坐标。
- `hop_seed_values.csv`：先在训练seed内对请求draw等权平均；另保留按draw节点数合并的比率供敏感性检查，两者不混用。
- `hop_summary.csv`：每条件训练seed均值/样本SD、有效seed数及节点分母；没有把节点或draw当作独立seed。
- `request_geometry.csv`、`request_geometry_summary.csv`：对方法坐标去重后的请求结构；<=2-hop是几何描述。
- `locality_cells.csv`：每cell的1-hop/远处D、差值及<=2-hop分歧份额；零分歧时份额保留null。
- `update_detection_coverage.csv`：5,985个cell的状态与AUC，缺失原预测明确保留。
- `HOP_VALIDATION.json`：来源SHA、5,985 metrics哈希/精确baseline/分子分母检查、全部case覆盖；080既有hop_summary每行均独立重算一致。没有重新加载正式Dataset或远端预测张量，因此未声称本轮重算了逐节点BFS/概率，只审计可信持久化计数与协议。

本轮仅本地CPU读取与生成分析，科学接受状态未改变。
