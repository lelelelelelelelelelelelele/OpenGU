# EXP-079 · Surrogate 多 seed 验证

一份完整实验表：[surrogate_multiseed.yaml](surrogate_multiseed.yaml)。
一份提交声明：[opengu-exp079-surrogate-multiseed.yaml](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed.yaml)。

完整矩阵包含三数据集、十训练seed、GCN direct与SGC/GAT/GIN、r_point/gt_full、Random/Degree、六GU及Retrain，共2520格。旧三seed对应756格，新增七seed对应1764格；精确缓存命中时复用已有计算，评价照常执行。参数只由YAML拥有。

Recipe使用 `experiment_id: exp079-surrogate-multiseed`、`run_id: e79r1`，一次提交整张表。当前SyncMate Core强制 `timeout_seconds <= 21600`，因此本次Recipe保持六小时上限。它是一次作业的停止边界，不保证整表在六小时内完成，也不是将矩阵拆分的理由。

Work Plan保存的227280秒（63.1小时）是低置信度、全MISS串行工程预算，不是实测耗时，也不是这份Recipe的超时值。实际缓存命中及运行耗时须由作业证据确认。

候选验收后一次性交付主线、同步安装，再由正式dispatch preflight核验版本、数据、GPU与run ID占用。超时或失败时先确认原作业终态与可用产物，不自动重试、不复用被占用的run ID、不将部分运行称为整表完成；后续处理遵循[Runbook](../../../self/research/RUNBOOK.md)。

新增七seed先独立分析，经身份核对后汇总十seed。现有metrics提供尺度分析所需基础量，本配置不增加新的指标producer。

实时状态由原[EXP-079记录](../../../self/research/experiments/EXP-079.json)维护。
