# Random 独立抽样重复

[random_expanded.yaml](random_expanded.yaml) 保留011表01的全部原条件，仍只引用一个公共 `random.yaml`，新增顶层 `random_selector_seeds: [104245, 11, 22]`。这是完整扩表示例，不是012正式扩表运行许可。

| 条件 | 原表 | 完整扩表 |
|---|---:|---:|
| Random：3数据集 × 3训练seed × 6方法 | 54 | 162 |
| 其余4个selector | 216 | 216 |
| 合计 | 270 | 378 |

每个数据/划分/预算下，Random的3个抽样seed与3个训练seed形成9个条件和3个Selection身份。不同抽样seed可以偶然选到相同集合，身份仍以有效seed区分。Degree、PageRank、IF没有Random轴，不重复展开。

优先级是大表 `random_selector_seeds`、Random小表 `parameters.seed`、原默认104245。省略新轴保留原行为；显式单值104245保留原有效参数及计算身份。实际覆盖来源记录在batch的 `configuration_sources`，有效seed在Score参数及带轴batch的 `matrix_values.random_selector_seed` 中可查。

每次执行使用新run identity生成完整Result：旧条件正常校验、读取并回传，只有真实MISS才调用producer。Score/Selection与GU/Retrain身份仍按原Cache V2合同校验；旧Result及Artifact不覆盖或迁移。正式012旧产物是否匹配，还需核对真实生产版本、数据/划分、预算、Selection及Output依赖，临时CPU验证不能替代该结论。

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu050/random_expanded.yaml --dry_run
```

本次实现仅拥有Random；IM轴及混合表由后续集成验证，不把未落地主线的040代码带入本候选。
