# 公共实验配置

活动配置只有一种规范：`kind: experiment` 组合表引用四类公共小表。解析与真实执行均经过 `experiments/run.py` → `modular_config` → `modular_run`。

| 目录 | 职责 |
|---|---|
| [datasets](datasets/) | 已持久化 Dataset/Split 和真实资产引用；不同 split 保留独立实例 |
| [selectors](selectors/) | 17 种 Selector 的有效参数；另有明确的 B-Hutch64 变体 |
| [unlearning](unlearning/) | 独立 GNNDelete、GIF、Retrain；另有明确 lr=0.02 变体 |
| [evaluations](evaluations/) | 单方法指标、utility、收集后的 retrain-gap |
| [aagu015](aagu015/) | 每数据集四张普通阶段表，无逐 seed/预算生成 YAML |
| [aagu007](aagu007/) | 本轮最小实验组合表；运行仍需审阅批准 |
| [aagu032](aagu032/) | 42 条件接口参考；科学方案由 032 单独验收 |

复制 [可复用模板](experiment.template.yaml) 后，只修改本轮引用、`seeds` 与 `budget_ratios` 等组合字段。两种覆盖仅在内存生效：大表显式值优先于小表，小表优先于方法默认值。训练 seed 配对模型型 Selector 与 GU/Retrain，不改变 split seed、Random 抽样 seed 或 Hutch 探针 seed。未知字段、任意 overrides、YAML merge 和给显式 checkpoint 换标签都拒绝。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/experiment.template.yaml --dry_run
```

真实本地验证需要先准备独立临时图、manifest、配置及目录，然后对该临时组合表运行 `experiments/run.py <临时实验.yaml> --verification-root <临时绝对目录> --run-id <新身份>`。此路径固定 CPU，所有数据必须位于临时根内。正式任务从 SyncMate 的登记入口进入相同命令与内核，由项目执行上下文提供 CUDA、路径、运行身份和正式检查。

TracIn 公共表显式选择 steps `[1,10,25,50,75,100]`；`_3` 消费 `[1,50,100]`，`_6` 消费六个。基础训练保存每个 epoch 不代表每个 epoch 都被评分消费；`_6` 没有恰好六个输入时拒绝，不静默扩大范围。

新结果使用独立 summary 和对应的 `summary.outputs/<序号>/`，输出目录存在即拒绝覆盖。Cache V2 根据有效输入和 producer 自动 HIT/MISS；表路径、实验名称、run_id、输出位置不进入计算身份。

旧扁平配置与 formal-v2 配方已退出执行，原文保存在 [历史配置](../../docs/archive/experiment-configs-pre-aagu034/)。历史结果和 Cache V2 不被迁移或清空。完整合同见 [实验规范](../../docs/experiment_contract/README.md)。
