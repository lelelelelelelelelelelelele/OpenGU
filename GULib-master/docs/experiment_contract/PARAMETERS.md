# 当前有效参数与缓存影响

参数由[通用解析器](../../experiments/modular_config.py)、[Selector默认值](../../experiments/target_direct_v1/methods.py)、[真实GU默认值](../../parameter_parser.py)及[GCN属性](../../model/properties/GCN.yaml)提供。下表解释公共表当前展开值，不能替代实际运行summary的输入与字节核验。

| 配置 | 默认/公共值 | 覆盖与身份 |
|---|---|---|
| Dataset/Split | Cora/CiteSeer/PubMed，70/10/20，split seed2024 | 资产与实际mask核验；训练seed不重切分 |
| Selector预算 | train候选的1%，floor且至少1 | 大表budget_ratios可覆盖；实际K来自真实候选数 |
| GCN | 2层、hidden64、dropout0.5 | 模型型Selector与GU分别声明 |
| 基础训练 | 100 epochs、Adam、lr0.005、weight_decay1e-6、无scheduler、seed42 | 大表seeds优先；使用模型的计算绑定对应训练身份 |
| LiSSA | iterations20、scale25、damp0.01 | 仅IHVP消费者 |
| Hutch | 32探针、seed1729 | 仅B-Hutch；64探针为独立变体表 |
| Random | 抽样seed104245 | 大表训练seed不覆盖它 |
| 求导范围 | last_layer | 梯度/IF/TracIn消费者；不是Degree/Random参数 |
| 图源 | affected_hops2，目标validation_mask，源train_mask | 各实际使用方法绑定其依赖 |
| TracIn | 指定steps[1,10,25,50,75,100]；_3取[1,50,100]，_6取六个 | 模型保存100份轨迹，评分只绑定实际选定快照与update_lr |
| GNNDelete | unlearn_lr0.01，50轮，alpha0.5，mse_mean/both_layerwise | 遗忘参数只影响方法Output |
| GIF | 参数默认值由parameter_parser展开 | 自身方法表与Output，不反向污染Selector |
| Retrain | 同级独立方法；按对应seed从头训练 | 排除真实选点监督并移除关联边，不消费GUcheckpoint |
| Evaluation | 单方法F1/accuracy/CE/AUC等；另行retrain-gap | 读已保存预测；缺少输入不虚构数值 |

## 17种方法的真实依赖

| 方法 | 数值实际依赖（除候选/数据/基础模型外） |
|---|---|
| degree | 原图出度；不需要基础模型、标签梯度或轨迹 |
| random | 候选序列和随机 seed；不需要基础模型/图梯度 |
| a_grad_norm | 最终候选梯度范数、参数范围 |
| b_param_hutch | 最终候选梯度、训练 Hessian、LiSSA、Hutch probes/seed、参数范围；不消费 validation 目标梯度 |
| legacy | 最终候选梯度与候选梯度之和的负内积；不消费 validation 目标 |
| p_point | 最终候选梯度与 validation 目标梯度 |
| r_point | 最终候选梯度与 validation 目标 IHVP（LiSSA） |
| p_simple / p_graph | 图源梯度/差分、validation 目标梯度、affected_hops |
| gt_simple / gt_full | 图源梯度/差分、validation 目标 IHVP、affected_hops、LiSSA |
| tracin_cp_point_3 / _6 | 指定快照的 point 内积与对应 update_lr 权重；不消费 LiSSA/Hutch |
| tracin_cp_simple_3 / _6 | 指定快照的 simple 图源内积、hops、权重；不消费 LiSSA/Hutch |
| tracin_cp_graph_3 / _6 | 指定快照的 graph 差分内积、hops、权重；不消费 LiSSA/Hutch |


每个方法独立形成Score身份；预算仅影响Selection。真实实现变化会改变对应producer并产生MISS；旧Artifact不被清空。路径改名不影响计算键，注册的整组配置指纹则会反映引用变更。模型型方法中训练seed变化影响模型与评分，Degree/Random不因它变化失效。
