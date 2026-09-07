# AAGU-031 · 原 Selector Stage S 合并提交表

[stage_s.yaml](stage_s.yaml) 合并 AAGU-015 原有三个数据集的 Stage S 表，沿用已接受的 17 个 Selector 和 Q1–Q4 比较设计。按用户 2026-09-08 的明确调整，只运行 10% 选集，后处理评估 1% / 5% / 10% 的重合度；不再将运行预算称为与原表完全一致。原方案由 [AAGU-015](../../../.workblock/items/AAGU-015/EXPERIMENT_PLAN.md) 拥有，正式运行与分析由 [AAGU-031](../../../.workblock/items/AAGU-031/WORKITEM.md) 承接。

| 轴 | 配置 |
|---|---|
| 数据集 | Cora、CiteSeer、PubMed，引用现有公共 Dataset/Split |
| 划分 | 持久化 70/10/20，split seed 2024 |
| 模型 | 两层 GCN，hidden 64、dropout 0.5 |
| 训练 | seeds 42/212/2024；100 epochs；Adam；lr 0.005；weight decay 1e-6 |
| 候选与目标 | 候选 train_mask；目标条件方法读取 val_mask，test 不参与选点 |
| 参数范围 | 原 last_layer；graph/simple source 原 affected_hops=2 |
| 运行预算 | 训练候选的 10% |
| 后处理比例 | 1% / 5% / 10%，分别从同一完整排名取前缀 |
| 运行范围 | 3 数据集 × 17 Selector × 3 seed × 1 预算 = 153 条件 |
| 阶段 | selector；输出分数、完整排名、Selection、身份与成本，不执行 GU/Retrain |

方法包括原参数变化参考、point/simple/graph IF/GIF 参考与 Hessian-free 代理、六种 checkpoint 累积方法，以及 degree/random/legacy 控制。不是单独 D-GIF 的新消融表。032 extension v2 的 all_trainable、3-hop 与 SGC 变体不混入。

组内/组间及 checkpoint 比较沿用原方案 Q1–Q4：收集核验后计算 Spearman/Kendall、common fraction/Jaccard 和成本。全候选相关系数每个方法对、数据集、seed 只计算一次；三个比例不是三次独立评分实验。YAML 负责生成这些分析的原始证据，不会自动把相关性当攻击效果，也不把数值参考当精确重训练真值。

后处理对每个比例 r 使用 K=max(1,floor(N_train×r))，从保存的稳定完整排名截取前 K 个节点；不能对 10% 选集长度再次乘 1%/5%。同一方法的三个选集自然嵌套，指标比较的是不同方法在相同 K 下的重合。先验证完整 candidate ID、分数/排名与持久化 10% Selection 一致，分析派生的小选集不冒充新写入的 Cache Artifact。

Cache 按实际有效身份自动 HIT/MISS。原 032 及 extension 已覆盖的一部分评分与选集具备复用机会；其余方法由 Cache 自行判断，不能从 153 个逻辑条件推算实际新计算次数或提前宣称命中率。

当前 Score 与预算无关并保存完整排名。底层 Selection resolver 支持除顶层 K 外身份一致时的大 K 覆盖小 K，但当前 IF 消费入口还把具体 ratio/K 写入 selector_parameters.budget，跨比例请求不会仅因倒序填写就命中大选集。本表只请求 10%，后处理前缀不依赖这个跨比例缓存能力；本次不修改缓存实现或历史 Artifact。

配置检查：

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu031/stage_s.yaml --dry_run
```

本次仅准备原实验的合并配置并核对等价性，未 Claim/完成 031、提交正式 GPU 作业或产生本轮科研结果。新文件需纳入落地 Git 版本，并按项目现有配置登记/提交入口绑定后才能在远端运行；本次未新增固定 SyncMate recipe。已接受 015 的原表仍由其定义检查器消费，作为原方案来源保留。
