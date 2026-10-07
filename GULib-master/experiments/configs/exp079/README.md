# EXP-079 · Surrogate 多 seed 验证

一份完整实验表：[surrogate_multiseed.yaml](surrogate_multiseed.yaml)。
当前续跑声明：[opengu-exp079-surrogate-multiseed-r4.yaml](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r4.yaml)。前三轮 [e79r1声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed.yaml)、[e79r2声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r2.yaml)与 [e79r3声明](../../../scripts/syncmate/recipes/opengu-exp079-surrogate-multiseed-r3.yaml)保留，用于核对历史任务身份。

完整矩阵包含三数据集、十训练seed、GCN direct与SGC/GAT/GIN、r_point/gt_full、Random/Degree、六GU及Retrain，共2520格。旧三seed对应756格，新增七seed对应1764格；精确缓存命中时复用已有计算，评价照常执行。参数只由YAML拥有。

Recipe使用 `experiment_id: exp079-surrogate-multiseed`、`run_id: e79r4`，一次提交整张表。用户确认本次沿用六小时上限，`timeout_seconds: 21600`，由现行SyncMate Core执行。它是一次作业的停止边界，不保证整表在六小时内完成，也不是将矩阵拆分的理由。

Work Plan保存的227280秒（63.1小时）是低置信度、全MISS串行工程预算，不是实测耗时，也不是这份Recipe的超时值。实际缓存命中及运行耗时须由作业证据确认。

候选验收后一次性交付主线、同步安装，再由正式dispatch preflight核验版本、数据、GPU与run ID占用。超时或失败时先确认原作业终态与可用产物，不自动重试、不复用被占用的run ID、不将部分运行称为整表完成；后续处理遵循[Runbook](../../../self/research/RUNBOOK.md)。

新增七seed先独立分析，经身份核对后汇总十seed。现有metrics提供尺度分析所需基础量，本配置不增加新的指标producer。

实时状态由原[EXP-079记录](../../../self/research/experiments/EXP-079.json)维护。

## 缓存速度 gate

[cache_speed_gate.yaml](cache_speed_gate.yaml) 是完整矩阵的 seed 42 精确子集，保留三数据集、全部选点/GU、预算及评价，共252格（10%）。[独立 Recipe](../../../scripts/syncmate/recipes/opengu-exp079-cache-speed-gate.yaml) 使用新 experiment/run identity，硬上限1800秒，不覆盖旧运行。本阶段先将代码、配置和Recipe备齐，再统一同步一次。

gate 要求 Score/Selection/Output 的适用请求全部命中，producer 未调用，已有 Output 身份和指标可核对，回传及项目校验通过。纯缓存工程目标为600秒内完成执行；这是待检验的目标，不是预测。超过目标、出现MISS或错误都不自动扩大到全量，应定位原因。现行 launcher 的 reuse 在 MISS 时会计算，所以必须检查实际命中记录；仅启动成功不能证明纯缓存。现有结果提供作业墙钟、方法计算时间与HIT记录，不能冒充源码扫描、磁盘读、完整性校验和指标的独立profile。

旧r4的约3小时对应2184请求的失败前缀，且未完成最终评价，不能与252格完整gate直接计算严格加速比。本gate首先验证当前纯缓存吞吐和正确性；没有匹配范围的旧计时就明确保留这一限制。完整矩阵的六小时上限不因此改变，gate通过不自动提交全量。
