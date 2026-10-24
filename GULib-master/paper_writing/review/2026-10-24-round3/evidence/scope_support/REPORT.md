# 第三轮已有证据采用清单：完整范围、反例与成本

结论：已有011/079/080材料足够支撑完整范围与反例，不必把主文限制成A/B几个有利坐标。但它们只承担科学发现的背景、边界和实际量级；“策略不同”本身不构成新的核心贡献。A的确认、B的端点解释及两图/C&S/Ret质量门槛仍由冻结协议独立判断，本清单不提前放行写作。

本轮仅本地只读整理。当前v6提纲和第一/二轮审查为采用依据；所有输出在本独有ignored目录。采用CSV完全排除历史GNNDelete，保留IDEA原值但标记不增加独立方法证据；080历史分片另表。没有新增GPU、方法或主张，也没有改动提纲或Work Plan状态。

## 1. 可执行的图表采用表

| id | target | admission | figure_action |
| --- | --- | --- | --- |
| S1 | Q1 / F2 / Appendix C | adopt descriptive support; not new A replication | Regenerate F2 with all 3 datasets x 6 endpoint columns; show full 8 settings in Appendix C; old plots contain excluded method and cannot be pasted unchanged Label both shard methods as project instances in axes/caption. If a table claims faithful original-algorithm comparison, omit these coordinates or move them to an explicitly variant-labelled appendix. |
| S2 | Q1 local interpretation / R0 / Appendix C | historical full metric audit + current source manifest rehash; no fresh metric-cell rehash | Pair within-band D with band share; never overlay different node populations as paired intervention Label both shard methods as project instances in axes/caption. If a table claims faithful original-algorithm comparison, omit these coordinates or move them to an explicitly variant-labelled appendix. |
| S3 | Q3 / T3 / Appendix E | current derived hashes + all adopted direct differences independently recomputed; 10 joint seeds | T3 compact range and examples; Appendix E all direct pair intervals + raw GU/Ret values; shared Degree/Random not duplicated as independent observations Label both shard methods as project instances in axes/caption. If a table claims faithful original-algorithm comparison, omit these coordinates or move them to an explicitly variant-labelled appendix. |
| S4 | Q2 / F3 / Appendix D | current audited raw CSV hash + seed/mean/SD recomputation; not new graph control result | Main 2 datasets x 2 GU with R-point minus Random/Degree; preserve small dips and zero/negative early points, raw GU/Ret table adjacent |
| S5 | Appendix D historical implementation boundary | historical-only panel; Cora50% absent, never zero-imputed | Separate old-protocol panel; never splice e79r6 10% into 080 curve Label both shard methods as project instances in axes/caption. If a table claims faithful original-algorithm comparison, omit these coordinates or move them to an explicitly variant-labelled appendix. |
| S6 | Appendix B / Table B3 | 014 Selection physically rechecked; 056 historical audit only; failure receipt current | Table separated stage clocks/config/version/cache; replace v6 running with timeout, no acceleration ratio or large-graph GU claim |
| S7 | Experimental design / Appendix A | historical inventory only in this pass; no new physical validation; cannot replace strategic B Ret/no-update controls | Short validity scope table, not extra RQ or independent scientific replication |
| X1 | Excluded / unresolved | not supported; pending A/B controls governed elsewhere | Old figure files cannot be reused unchanged; A/B new evidence is separately adjudicated |

每项精确输入、筛选规则、待生成图及输出文件写入CLAIM_SOURCE_FIGURE_MAP.json。旧011/079图册含已隔离GNNDelete，旧080图册还混有历史分片，不能直接粘贴进最终论文；必须由这里的限定CSV重绘。这里给采用计划与数据，不冒充已经排版完成的论文图。

## 1.1 分片方法语义：修正聚合损失，不等于忠实复现原算法

已有A101/A105记录明确：两方法交叉熵前多余softmax已修正，并进入独立shard_epochs=300的正式配置；本轮又只读比较e11r1/e79r6执行SHA bab1781与A101修正候选7491b59，两聚合器Git blob分别完全相同（GraphEraser d9cee2f5f8b569658825b1160837ae43b4301396；GraphRevoker 3b06716899f41b09edd9689f790512694b72ed53）。所以不能把079简单归为仍执行旧double-softmax的结果；但这一核验只绑定执行checkout代码，并未逐个追溯所有HIT Output的原始MISS producer。表格字节正确不能代替方法语义审计。

GraphRevoker已知仍是项目GPA+optimal变体，A101明确没有补齐原论文全部模块，e79r6原报告也明确未转成完整对比聚合实现。GraphEraser已确认共同loss修正，但本清单没有对其全流程与原论文逐模块做忠实性审计。因此079两者仅可命名为as-implemented项目实例，用于条件性source描述和反例；不能将Cora/GIN与SGC反例写成已证实的原论文算法性质、缺陷或新A的跨source确认。

具体采用边界：在明确列出实现、聚合、分片预算和运行身份的经验表中保留原值，轴标签/图注同时标明项目实例；如主文表宣称比较忠实复现的原论文算法，则两者应移出该表或进入单独变体附录，待具体producer/完整方法审计后再决定更强采用。尚无证据要求把整个079分片矩阵当数值损坏隔离；必须隔离的是不带实现限定的算法级论断。旧080分片仍仅作其原历史协议记录，旧GNNDelete仍全部隔离，不因本段恢复。METHOD_SEMANTICS.json保留已知证据和未审范围。

## 2. 011：让IM/topology进入主图，同时保留相反条件

| dataset | method | random | degree | rr_65536 | r_point | gt_full |
| --- | --- | --- | --- | --- | --- | --- |
| Cora | GIF | 90.117 | 90.344 | 90.303 | 89.914 | 89.606 |
| Cora | MEGU | 89.403 | 89.852 | 89.422 | 89.729 | 89.483 |
| Cora | GraphEraser | 85.357 | 84.194 | 84.522 | 84.071 | 84.994 |
| Cora | GraphRevoker | 74.182 | 73.063 | 72.981 | 75.215 | 73.801 |
| Cora | Retrain | 89.760 | 89.975 | 89.340 | 88.745 | 89.791 |
| CiteSeer | GIF | 74.595 | 74.575 | 74.741 | 75.025 | 75.025 |
| CiteSeer | MEGU | 74.044 | 74.625 | 74.558 | 74.274 | 73.824 |
| CiteSeer | GraphEraser | 74.635 | 74.775 | 74.641 | 75.125 | 74.825 |
| CiteSeer | GraphRevoker | 73.564 | 73.824 | 73.757 | 72.923 | 73.223 |
| CiteSeer | Retrain | 74.885 | 75.025 | 75.475 | 74.925 | 74.825 |
| PubMed | GIF | 88.458 | 88.294 | 88.435 | 87.779 | 87.517 |
| PubMed | MEGU | 86.841 | 86.579 | 86.793 | 86.663 | 86.646 |
| PubMed | GraphEraser | 87.017 | 87.120 | 86.990 | 85.759 | 86.367 |
| PubMed | GraphRevoker | 86.564 | 86.604 | 86.455 | 84.669 | 85.370 |
| PubMed | Retrain | 88.513 | 88.751 | 88.382 | 86.114 | 86.486 |

表为10%预算accuracy原值（%），三联合运行均值；完整八设置、IDEA、CE、AUC、GU–Ret gap/D及点态区间在fixed10_endpoints.csv和fixed10_random_contrasts.csv。图F2可用相对Random变化压缩，但原始Ret与GU端点不能丢。PubMed GraphEraser在R-point为85.759%、Random为87.017%；CiteSeer对应75.125%与74.635%，方向不同。不能把单一选择器命名为普遍最强，或把高于Random解释为防御成功。GraphRevoker始终按当前已披露变体标注。

| dataset | selector | hop1_share_pct | within2_share_pct | gt3_share_pct |
| --- | --- | --- | --- | --- |
| Cora | r_point | 17.71217712177122 | 53.321033210332104 | 24.538745387453876 |
| Cora | degree | 54.24354243542435 | 77.85977859778598 | 13.468634686346864 |
| Cora | random | 23.04428044280443 | 65.03690036900369 | 14.77859778597786 |
| Cora | rr_65536 | 54.79704797047971 | 83.51783517835177 | 8.54858548585486 |
| CiteSeer | r_point | 15.865865865865866 | 37.33733733733734 | 45.645645645645644 |
| CiteSeer | degree | 36.186186186186184 | 50.6006006006006 | 41.14114114114114 |
| CiteSeer | random | 16.62162162162162 | 42.5975975975976 | 41.366366366366364 |
| CiteSeer | rr_65536 | 36.03603603603604 | 59.80980980980981 | 31.38138138138138 |
| PubMed | r_point | 13.607167004732927 | 57.7501690331305 | 12.102772143340095 |
| PubMed | degree | 63.61561866125761 | 87.11967545638946 | 2.3580121703853956 |
| PubMed | random | 21.57707910750507 | 79.36105476673428 | 4.264705882352941 |
| PubMed | rr_65536 | 39.20723461798513 | 86.48580121703854 | 1.6903313049357673 |

以上为test节点的距离带构成（%）；IM-RR65536两跳覆盖Cora/CiteSeer/PubMed为83.52/59.81/86.49%，R-point为53.32/37.34/57.75%。Cora GIF一跳D的R-point/IM为26.87/3.63%，MEGU为21.59/4.53%，而远处均近零；Cora GraphEraser在>3-hop仍为9.86/14.54%，GraphRevoker为18.63/14.08%。这些反例要求同图给每带分母：覆盖广不自动等于带内D大，带内D顺序不自动等于整体D顺序，也不能把不同selector的节点带当作配对因果处理。

## 3. 079：来源采用应保留整个家族，而不是只留PubMed示例

| dataset | method | selector | GCN_delta_accuracy_pp | SGC_delta_accuracy_pp | GAT_delta_accuracy_pp | GIN_delta_accuracy_pp |
| --- | --- | --- | --- | --- | --- | --- |
| CiteSeer | GIF | r_point | 0.375 | -0.075 | 0.646 | 0.120 |
| CiteSeer | GraphEraser | r_point | 0.756 | -0.325 | -0.025 | 0.966 |
| CiteSeer | GraphRevoker | r_point | -0.140 | -0.350 | -1.657 | 0.280 |
| CiteSeer | MEGU | r_point | 0.205 | 0.175 | 0.295 | 0.145 |
| CiteSeer | Retrain | r_point | 0.335 | -0.145 | -0.070 | -0.295 |
| Cora | GIF | r_point | -0.092 | 0.203 | -0.000 | -0.074 |
| Cora | GraphEraser | r_point | -0.406 | -1.236 | 0.240 | 0.498 |
| Cora | GraphRevoker | r_point | 0.658 | 0.344 | 2.854 | 1.968 |
| Cora | MEGU | r_point | -0.049 | 0.320 | 0.062 | 0.062 |
| Cora | Retrain | r_point | -1.193 | -1.378 | -1.064 | -1.064 |
| PubMed | GIF | r_point | -0.641 | 0.034 | -0.225 | -0.308 |
| PubMed | GraphEraser | r_point | -0.969 | -0.421 | -1.306 | -0.695 |
| PubMed | GraphRevoker | r_point | -1.315 | -0.387 | -1.911 | -1.363 |
| PubMed | MEGU | r_point | -0.112 | -0.046 | -0.128 | -0.105 |
| PubMed | Retrain | r_point | -2.032 | 0.045 | -2.359 | -1.274 |

表为R-point相对同seed内Random均值的accuracy差（pp），source_scope.csv另保留D-full与全部点态区间范围；source_direct_contrasts.csv覆盖D-full−R-point、R-point−Degree、D-full−Degree的accuracy与D，source_endpoints.csv保留GU/Ret原值。两分片行均按上节as-implemented语义解释：PubMed项目GraphEraser实例四source为−0.969/−0.421/−1.306/−0.695pp，各点态区间低于零，但Cora同实例在GIN为+0.498pp、SGC为−1.236pp，CiteSeer在GCN/GIN为正、GAT/SGC均值为负。只有在明确实例限定的T3中才可展示这些反例，不能只突出一致的一行，也不能据此声称原论文算法的source性质。

n=10是联合选点/训练流程。每dataset/source的R-point、D-full各十个不同Selection，Degree一份、Random三份跨seed复用；四source共享参照，不能当四次独立确认，也不是四目标backbone。完整源表包含五GU实现坐标加Ret，但GIF/IDEA近重合意味着独立方法模式不能按五份计。旧GNNDelete的方向频率、margin或源稳定性统计全部不采用。

## 4. 080：七预算形态和原值决定5%→33%该怎么写

| dataset | method | baseline | r0.05 | r0.075 | r0.1 | r0.15 | r0.22 | r0.33 | r0.5 | descending_adjacent_steps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cora | GIF | random | 2.276 | 2.583 | 3.690 | 4.674 | 6.888 | 10.517 | 15.990 | 0 |
| Cora | GIF | degree | 1.476 | 1.415 | 2.645 | 4.121 | 7.196 | 8.180 | 15.867 | 1 |
| Cora | MEGU | random | 0.923 | 0.984 | 1.292 | 2.768 | 5.228 | 7.995 | 15.560 | 0 |
| Cora | MEGU | degree | 0.677 | 0.000 | 0.246 | 1.907 | 3.444 | 5.658 | 14.268 | 1 |
| CiteSeer | GIF | random | 0.551 | 0.601 | 2.753 | 2.703 | 5.806 | 14.615 | 27.277 | 1 |
| CiteSeer | GIF | degree | 1.451 | 1.101 | 2.553 | 4.004 | 7.407 | 16.517 | 28.579 | 1 |
| CiteSeer | MEGU | random | -0.200 | 1.552 | 3.604 | 3.353 | 5.956 | 14.815 | 29.179 | 1 |
| CiteSeer | MEGU | degree | 0.901 | 2.152 | 3.654 | 5.305 | 8.709 | 17.117 | 30.330 | 0 |

表为D(R-point)−D(指定baseline)（pp），所有七个预算均保留；逐seed配对SD与两边GU/Ret accuracy及原始D在budget_seven_point_curves.csv。这里八条展示曲线中五条存在相邻预算均值回落，不能概括成全程单调：CiteSeer GIF相对Random在10%→15%为2.753→2.703pp，MEGU为3.604→3.353pp；Cora MEGU相对Degree在5%→7.5%为0.677→0。小幅回落也不单独证明总体非单调，只是要求保留观察曲线。

F3建议主画GIF/MEGU的两数据集、两baseline差值曲线，紧邻GU和Ret原始端点表。完整280个非分片/Ret条件原值在budget_current_nonshard.csv，IM三draw先seed内平均，保留IDEA但不作额外确认。CiteSeer33%时IM相对Random的D约+0.350/+0.234pp，R-point约+14.615/+14.815pp（GIF/MEGU）；这支持具体有限请求比较，不能解释成IM正确遗忘。Random/Degree每预算只有一份请求跨三seed复用；5%→33%为探索性端点，不是预设阈值或随机请求期望。

130个历史分片条件单列budget_historical_shards.csv。Cora50%两分片没有可用端点，必须留空/断线，不能补零；Cora历史GraphRevoker的R-point−Degree D差从5%到33%反而减少6.458±5.056pp，三个seed均负，仅作为旧协议边界，不移植为当前变体结论。共同10%非分片+Ret的72个可采用引用在079/080复用同一Output（另18个旧GNNDelete隔离），不能累加成独立证据；两分片的36个匹配引用均不同，不得将新079点接进旧080曲线。

## 5. 大图成本必须包含未完成和超时

| selector | status | cell_access_seconds | model_prepare_seconds | selector_access_seconds | selector_compute_seconds | job_wall_seconds | sampled_container_peak_GiB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| degree | accepted_execution | 4.642 | None | 4.642 | 2.382 | 54.000 | None |
| random | accepted_execution | 2.601 | None | 2.601 | 1.142 | 54.000 | None |
| r_point | accepted_execution | 324.512 | 48.060 | 276.452 | 1.145 | 364.000 | None |
| IM-RR1024 | accepted_execution_historical | None | None | None | 366.546 | 380.390 | 7.592 |
| IM-RR65536 | recipe_timeout_at_7200s | None | None | None | None | 7202.000 | None |
| D-full | not_submitted | None | None | None | None | None | None |

图规模169,343节点、118,540候选，k=5,927。014 Random/Degree同一完整job的wall均引用54s，不能相加成108s；各自cell访问为2.601/4.642s。R-point cell324.512s=模型准备48.060s+selector访问276.452s（另有极小调度差），完整job364s。selector_compute在不同实现中只覆盖其记录阶段，R-point的大头score访问275.244s不能被1.145s的末端选集提取掩盖。

014 IM-RR65536已recipe_timeout：7200s硬上限，Core完整wall7202s，无可信完成产物。v6仍写“运行中”已过时；应改成明确失败边界。D-full尚未提交，不填0。056 RR1024的selector366.546s、进程380.390s、5s采样容器峰值7.592GiB为历史已接受执行，原始文件本轮未重新物理核验；该内存不是精确进程峰值。RR1024与65536配置/版本不同，不能推加速比或外推完成耗时；全部成本结果没有大图GU/Ret端点。selector_costs.csv保留每行job、执行SHA、节点、缓存与计时边界；硬件利用率和device-specific时间本轮未复核。

## 6. 验证层级与仍不可采用的内容

本轮物理SHA核对23项；五个旧科学run的manifest及delivery字节与既有完整审计一致，当前CSV与既有哈希一致。重新计算5940项已采用来源差/区间数值与4900项预算raw-cell→seed→均值/SD；014三份Selection重新核对哈希、5927唯一ID及范围。candidate-mask成员资格仍引用项目验收，本轮没有加载正式Dataset。

并未再次逐文件核验011/079/080全部returned cell或重算模型预测；历史可信链依赖input_audit、verification、HOP_VALIDATION、claim_audit及独立复核记录。Hop派生表本轮读取并记录哈希，原metric的5985文件核验沿用第一轮审计。056只重读历史accepted核验；062/065–068、078、082只是库存层引用，本轮未重核其payload。机器映射记录每个来源的当前哈希及这一边界，不把本次整理写成新完整科学验收。

可采用的有效性背景：固定PT、10%三个新Random请求的84格数值/非退化验证；baseline checkpoint诊断；分片300→3000验证变化±0.901pp。它们不能替代B战略大预算的Ret训练质量、同权重两图或matched C&S。既有Random多请求也不是同一固定请求的R–R重训噪声。没有目标backbone、多split、真实请求权限、因果传播、隐私泄漏或认证遗忘证据；这些强主张仍不能采用。

最终采用顺序：先由新A/B完成冻结门槛并确定具体新增认识；再以S1/S2给机制与空间边界，以S3限制source外推，以S4/S5展示完整预算及版本反例，以S6给可运行成本与失败。上述材料丰富证据范围，不增加核心发现数量，也不能用来掩盖A/B贡献不足。
