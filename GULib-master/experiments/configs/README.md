# 公共实验配置

活动配置只有一种规范：`kind: experiment` 组合表引用四类公共小表。解析与真实执行均经过 `experiments/run.py` → `modular_config` → `modular_run`。

数据轴统一写作 `dataset_refs: [cora.yaml, citeseer.yaml, pubmed.yaml]`，单数据集写作 `dataset_refs: [cora.yaml]`。同一表内不能重复同一个 Dataset/Split 实例。每个数据集独立绑定 manifest、划分和候选空间；加入或重排其他数据集不改变原有计算身份。

[extension v2 合并表](aagu032_extend_v2/experiment.yaml) 展开为 3 数据集 × 10 Selector × 1 Retrain × 3 seed × 4 比例 = 360 条件；原有 288 条件和新增 72 条件的配置保持不变。三者都使用 70/10/20、split seed 2024。该表及 `opengu-aagu032-extend-v2` recipe 的存在不代表已获准执行正式科研矩阵。

引用支持两种写法：只写文件名时按字段定位本目录下的公共小表，例如 `unlearning_refs: [gnndelete.yaml]` 读取 `unlearning/gnndelete.yaml`；显式相对路径（如 `../unlearning/gnndelete.yaml`、`./custom.yaml`）以组合表所在目录为起点。明确的绝对路径也可使用，隔离验证据此绑定临时资产。文件名引用不搜索组合表邻近目录，不受工作目录影响；加载与配置指纹使用同一解析规则。

| 目录 | 职责 |
|---|---|
| [datasets](datasets/) | 已持久化 Dataset/Split 和真实资产引用；不同 split 保留独立实例 |
| [selectors](selectors/) | 16 种 Selector 的有效参数；另有明确的 B-Hutch64 变体 |
| [unlearning](unlearning/) | 独立 GNNDelete、GIF、Retrain；另有明确 lr=0.02 变体 |
| [evaluations](evaluations/) | 单方法指标、utility、远端重算的 retrain-gap |
| [aagu015](aagu015/) | 每数据集四张普通阶段表，无逐 seed/预算生成 YAML |
| [aagu007](aagu007/) | 本轮最小实验组合表；运行仍需审阅批准 |
| [aagu032](aagu032/) | 42 条件接口参考；科学方案由 032 单独验收 |

复制 [可复用模板](experiment.template.yaml) 后，只修改本轮引用、`seeds` 与 `budget_ratios` 等组合字段。两种覆盖仅在内存生效：大表显式值优先于小表，小表优先于方法默认值。训练 seed 配对模型型 Selector 与 GU/Retrain，不改变 split seed、Random 抽样 seed 或 Hutch 探针 seed。未知字段、任意 overrides、YAML merge 和给显式 checkpoint 换标签都拒绝。

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/experiment.template.yaml --dry_run
```

真实本地验证需要先准备独立临时图、manifest、配置及目录，然后对该临时组合表运行 `experiments/run.py <临时实验.yaml> --verification-root <临时绝对目录> --run-id <新身份>`。此路径固定 CPU，所有数据必须位于临时根内。正式任务从 SyncMate 的登记入口进入相同命令与内核，由项目执行上下文提供 CUDA、路径、运行身份和正式检查。

TracIn 公共表显式选择 steps `[1,10,25,50,75,100]`；`_3` 消费 `[1,50,100]`，`_6` 消费六个。基础训练保存每个 epoch 不代表每个 epoch 都被评分消费；`_6` 没有恰好六个输入时拒绝，不静默扩大范围。

Selector/Unlearning只以 `selector_refs` 声明选点；后续方法使用相同有效规则自动查找或计算，无需手填上轮Selection产物。实际Artifact身份、哈希、HIT/MISS保存在结果中。

新结果采用 [结果回传合同](../../docs/experiment-result-return-contract.md) 的 `results/runs/<experiment-id>/<run-id>/run.json` 与 cell 条件目录。常规回传 Metrics/Selection，`return_scores: true` 才交付已有评分数组，禁止为回传扩大计算。目录存在即拒绝覆盖；Metrics 使用新的 run 重算，收集后重建当前结果表，历史 run 保留。Cache V2 根据有效输入和 producer 自动 HIT/MISS；表路径、实验名称、run_id、输出位置不进入计算身份。

旧扁平配置与 formal-v2 配方已退出执行，原文保存在 [历史配置](../../docs/archive/experiment-configs-pre-aagu034/)。历史结果和 Cache V2 不被迁移或清空。完整合同见 [实验规范](../../docs/experiment_contract/README.md)。

IM的独立selector seed轴、单值/多值普通表示例及选集复用见 [AAGU-040](aagu040/README.md)。

IM 默认小表 `selectors/im.yaml` 使用固定 RR 最大覆盖贪心；显式 RR 实例为 `selectors/im_rr_greedy.yaml`。MC-CELF 保留在 `selectors/im_celf.yaml`，只在主动引用时作为备用运行。可与 IF 小表并列引用（不是 Hybrid 融合），见 [组合与参数语义](aagu040/README.md)。
