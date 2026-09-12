# AAGU-053：5% RR 采样充分性检查大表

入口：[rr_sufficiency_05.yaml](rr_sufficiency_05.yaml)。本表为2026-09-13确认的补充范围，使用独立experiment_id，不恢复此前取消的selection_05任务。

| 变量 | 定义 |
|---|---|
| 数据集 | Cora、CiteSeer、PubMed；原正式图与split |
| 候选池 | train_mask |
| 删除预算 | 候选池5%；预期K分别94、116、690，正式执行核对真实候选数 |
| RR样本数 | 1024、4096、16384 |
| 传播概率 | 0.1，继承原三份RR小表 |
| 选点seed | 11、22、33 |
| 阶段 | selector；无训练seed、Retrain或GU |
| 格数 | 3×3×3＝27 |

大表0.05覆盖小表默认0.10；不修改小表，避免影响现有10%实验。合法前缀缓存复用由原消费者负责；MISS可能生产选集，不手工截断或覆盖Artifact。

本表的普通Selection回传不包含完整accepted_gains/coverage_trace，因此27格完成只能证明选点执行与身份。充分性诊断还需同身份RR覆盖重放，记录可覆盖样本数、K步覆盖、首次零增益位置、零增益比例，并在独立验证样本上评价覆盖变化。独立验证的样本规模/停止准则尚未定稿；本表不声称具备理论近似证书。

本地dry-run仅验证配置展开，不访问正式图或证明缓存HIT。正式执行前仍需Core登记、版本和数据身份核对及运行gate；本次只建立大表，不表示已经派发。

权威记录：[AAGU-053 WorkItem](../../../..//.workblock/items/AAGU-053/WORKITEM.md)。
