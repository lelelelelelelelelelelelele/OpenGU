# Random 多选集实验

本目录实现 AAGU-051 已登记设计。实时执行状态和授权边界以 canonical 项目 `.workblock/items/AAGU-051/WORKITEM.md` 为准。

| 执行表 | 数据集 | Random seed | 方法 | 训练 seed | 条件 |
|---|---|---|---|---|---:|
| gu.yaml | Cora/CiteSeer/PubMed | 11,22,33,44,55,66,77,88,99,110 | GIF/GNNDelete/MEGU/IDEA/GraphEraser/GraphRevoker | 42,212,2024 | 540 |
| retrain.yaml | 同上 | 同上 | Retrain | 42 | 30 |

两表只引用公共 random.yaml，采用 GCN、固定 Dataset/Split 和 10% train 候选池预算。不同抽样 seed 可以得到重合集合；不重抽、不按结果挑选 seed，不强行纳入旧默认104245。训练 seed 不改变 Selection。两表保存单方法指标和自身 before/after utility；不调用严格三 seed Retrain 配对指标。

## 本地核验

在项目根执行：

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu051/gu.yaml --dry_run
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu051/retrain.yaml --dry_run
```

## 分析口径

每个数据集以10个选集为独立抽样单位；3个GU训练seed是每个选集内的交叉观测，不能当作30次独立抽样。分别报告每个训练seed跨选集的均值、样本标准差、中位数、最小和最大值，以及每组选集内的训练波动和逐seed明细。保存30个Selection引用、内容哈希、实际节点清单及每数据集45对Jaccard；相同集合不删除。

比较同一测试集合/评价图下的自身未删除模型 B_m 与 U_m,R，完整模型 P0 与固定seed42重训练 R_R，以及描述性固定参照差异 R_R-U_m,R；所有差异保留符号。分片方法 B_m 必须来自未删除ensemble，不能以P0替代。只有GU seed42与Retrain训练seed匹配；212/2024保留完整身份，称相同请求的固定参照差异。离线分析必须核验Selection、Dataset/Split、评价协议、配置和Output身份，不能改动现有严格配对校验。

单次Retrain没有估计训练方差；固定参照差异不等于纯遗忘误差。F1不降不能证明遗忘成功。缺失和失败保留，不填均值、不隐藏异常，不因前5组结果有利提前停止。

## 正式运行前置

配置准备不代表GPU实验已获准进入执行阶段。先完成配置和分析软件验证、disposable smoke、注册最小gate；按 experiments/AGENTS.md 核对本地main、origin/main与SSH active main完整SHA一致及tracked tree干净、GPU可用、正式输入manifest、已有run与缓存身份、可信收集路径。

GIF/IDEA正式扩展必须消费049有效性结论。不得将未通过有效性核验的旧GIF缓存或待验收修复冒充本实验有效生产路径；具体前置状态读取canonical WorkItem。其余方法同样需要实际before/after语义核验。不得用CPU fixture替代正式gate或科学证据。

后续需完成可复跑离线汇总、固定参照描述性指标的身份校验、最小gate登记、可信收集和配对REPORT.md/REPORT.html，再审查完整570条件。当前两表不自行绕过上述前置。

