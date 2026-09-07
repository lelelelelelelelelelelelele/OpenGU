# AAGU-015 · 八组 Selector 实验表（031 执行）

当前执行入口为 [stage_s.yaml](stage_s.yaml)，experiment_id 为 `aagu031-selector-stage-s-v2`。本表按用户最新讨论替代本轮原 17 组执行范围：以预筛选可行性、评分与排序时间为主，保留两组辅助机制对照。结果分析由 [033](../../../.workblock/items/AAGU-033/WORKITEM.md) 承接。

| 组 | Selector 配置 | 作用 |
|---|---|---|
| A | a_grad_norm.yaml | 梯度范数；与 B 比较收益与成本 |
| B | b_param_hutch.yaml | 曲率修正的参数变化范数估计 |
| Degree | degree.yaml | 拓扑参照；排名后处理判断预筛选可行性 |
| D-full 两跳 | gt_full.yaml | 现有两跳计算范围参照 |
| D-full 三跳（last_layer） | gt_full_last_layer_hops3.yaml | 与 last_layer 两跳比较计算范围 |
| D-full 三跳（all_trainable） | gt_full_all_trainable_hops3.yaml | 与 last_layer 三跳比较参数范围及成本 |
| GT-simple 三跳 | gt_simple_last_layer_hops3.yaml | 与三跳 D-full 比较 graph 修正项 |
| P-graph 三跳 | p_graph_last_layer_hops3.yaml | 与三跳 D-full 比较逆 Hessian 处理 |

| 公共轴 | 当前配置 |
|---|---|
| 数据集 | Cora、CiteSeer、PubMed；公共 Dataset/Split |
| 划分 | 持久化 70/10/20，split seed 2024 |
| 模型 | 两层 GCN，hidden 64、dropout 0.5 |
| 训练 | seeds 42/212/2024；100 epochs；Adam；lr 0.005；weight decay 1e-6 |
| 参数范围 | A/B、D-full 两跳/三跳、GT-simple、P-graph 使用 last_layer；另有一组 D-full 三跳使用 all_trainable；Degree 不使用模型 |
| 候选与目标 | train_mask 候选；目标条件方法用 val_mask；test 不参与选点 |
| 数值设置 | 消费逆 Hessian 的方法：LiSSA iterations 20、scale 25、damp 0.01；B 为 32 probes、seed 1729 |
| 运行预算 | 原训练候选数的 10%；覆盖小表的预算默认值 |
| 规模 | 3 数据集 × 8 组 × 3 seed × 1 预算 = 72 个逻辑条件 |
| 输出 | 完整 candidate IDs、scores、ranking、10% Selection、身份与现有计时记录 |

本轮移除 legacy、Random、TracIn 和其他 point/simple 组合；不增加预筛选 Selector，不运行预筛选后精排，也不执行 GU/Retrain。032 的已有/新增匹配结果用于分析下游效用，不由本表触发。旧 015 文档及配置是原方案来源，不是本轮执行入口。

033 从同一完整排名取 Degree 前 10%/20% 与 D-full 前 1%/5%/10%。包含率为交集大小除以 D-full 目标集合大小；K=max(1,floor(N_train×r))，各比例均以原训练候选数为分母。20% Degree 从完整排名截取，无须再次评分或新增 Selection Artifact。已有 A/B 排名可按同一口径补充分析。高包含率支持初步可行性，不证明实际加速或攻击效果。

时间分析只加一张表，利用现有计时字段读取或推导共享 function、逐点评分、排序及总时间，标明实测/推导/无法独立估计，不新增埋点或页面。共享计算不重复累计；HIT 读取不当作冷计算；不能按候选比例线性缩放全部运行时间。

last_layer 两跳/三跳仅改变 affected_hops；两个三跳辅助对照与 last_layer D-full 三跳统一参数范围、训练和跳数。D-full 三跳的 last_layer/all_trainable 配对仅改变 parameter_scope。效果接近且额外耗时不大时优先三跳；实际取舍由匹配结果与时间支持。

Cache 按实际配置、输入、producer 与依赖身份判断 HIT/MISS。Degree 及部分 D-full 有复用机会；all_trainable 与旧 last_layer 不是相同身份，不能承诺全部 HIT，也不清理历史缓存。

配置检查：

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu031/stage_s.yaml --dry_run
```

队列注册为 `opengu-aagu031-stage-s-v2`，run ID 为 `aagu031-stage-s-v2`，由普通 `experiments/run.py` 消费本表；绑定配置及全部引用指纹、72 条件、三数据集候选数和 Selector summary 产物。超时上限为 21600 秒（6 小时），沿用现有矩阵上限，不是完成时间估计。正式运行仍需落地版本及运行前置审验；注册不提交作业。
