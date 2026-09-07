# AAGU-032 extend

这是独立的扩展实验配置包，原032实验及结果保持原样。用户要求：检查正常后经SyncMate提交，完成回传核验，交付结果等待验收。

| 配置 | 数据集 | 条件 |
|---|---|---:|
| [experiment.yaml](experiment.yaml) | Cora | 96 |
| [experiment.citeseer.yaml](experiment.citeseer.yaml) | CiteSeer | 96 |
| [experiment.pubmed.yaml](experiment.pubmed.yaml) | PubMed | 96 |

统一70/10/20划分，split seed2024；训练seeds42/212/2024；预算1%/5%/10%/15%；8个Selector配置与独立Retrain，共288个输出。每张表使用独立experiment_id，执行时还需绑定独立run_id。结果分别导出，再合并呈现三数据集主比较与辅助对照。

## 参数范围对照与提交状态

按用户后续要求，保留gt_full.yaml作为last_layer对照，新增[gt_full_all_trainable.yaml](../selectors/gt_full_all_trainable.yaml)。两者method均为gt_full；唯一有效参数差异是parameter_scope。Hessian归一化、LiSSA和其他设置相同，用于独立检验参数范围的影响，不宣称完全复现GIF默认设置。先前的[核对说明](REVIEW.md)记录新增此对照之前的252条件检查。

提交准备已按公共数据YAML在SSH固定data/processed目录生成CiteSeer、PubMed缺失的70/10/20 seed2024划分，并绑定真实manifest摘要；Cora复用原资产。三个划分均与seed2024重新计算的节点集合逐项一致，互斥且覆盖全部节点。普通训练入口仍只消费已核验绑定，本次自动准备在提交前完成。

正式运行由三个opengu-aagu032-extend-<dataset>-v1静态recipe提交，执行、回传和核验状态以SyncMate收据为准。准备与核验记录位于忽略目录`.syncmate/aagu032-extend-submit/`。配置本身不表示运行已经成功。

## 条件满足后的执行

定义和数据绑定完成后，对最终配置重新dry-run并登记SyncMate静态recipe；固定本地main、origin/main与SSH main为同一已验证SHA，再提交正式作业。运行完成后通过SyncMate收集、校验、索引和项目gate，形成extend结果与报告交给用户验收。

保留现有缓存，逐层核对Score、Selection、Output的实际HIT/MISS。未变的Cora条件可复用；定义修正、预算新增或数据集改变涉及的身份必须重新计算。此处不提前保证命中数量。
