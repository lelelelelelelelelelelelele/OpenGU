# AAGU-015 普通组合表

科学范围沿用已接受 015：Cora、CiteSeer、PubMed；17 种 Selector；训练 seeds `[42,212,2024]`；预算 `[0.01,0.05]`。公共接口修正由 AAGU-034 承担，正式矩阵与分析由后续获批任务执行。

每个数据集各维护四张表，共 **12 张 YAML**，不生成逐条件/逐 seed 小表：

| 表 | 每数据集条件数 | 三数据集合计 | 输入 |
|---|---:|---:|---|
| `stage_s_<dataset>.yaml` | 102 | 306 | 公共 Dataset/Split 与17 Selector |
| `stage_u_<dataset>.yaml` | 204 | 612 | 相同公共 Selector 与轴值；独立 GNNDelete、GIF |
| `stage_retrain_<dataset>.yaml` | 102 | 306 | 相同公共 Selector 与轴值；独立 Retrain 参照 |
| `metrics_<dataset>.yaml` | 随已绑定 Output | 612 组配对比较预期 | 已收集 GU、Retrain 输出；不训练 |

独立 Retrain 是原有 Stage U 科学评价所需的参照，不增加攻击方法或改变原612个 GU条件。12张维护文件与306/612个逻辑条件属于不同计数。原424份生成 YAML 已删除，旧 `generate` 命令退役。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu015/stage_s_cora.yaml --dry_run
& E:/conda_package/envs/gnn/python.exe -B -X utf8 -m experiments.aagu015.definitions check
```

后者仅审计普通表展开，使用相同解析器，不是另一个执行器。配置分组仍为9组训练准备、141组 Score、282组 Selection；这是条件相同的预测，不能替代实际 HIT 证据。

Cora 公共表沿用已记录的 SM-005 manifest 身份；CiteSeer/PubMed 尚未绑定真实资产。所有真实字节均由执行时验证。Stage S、U、Retrain显式引用相同17张公共Selector表与原有seed/预算；缓存按有效身份自动复用，MISS才计算，无需绑定上轮Selection或summary。Metrics的summary/sha256仍须填写真实完成并收集的Output；缺失或不匹配时失败关闭。

本表可 dry-run 不等于正式运行就绪。设备、三端 main、完整 SHA、预检、获批最小 gate 与成本边界仍归正式任务。公共格式见 [配置规范](../README.md)。
