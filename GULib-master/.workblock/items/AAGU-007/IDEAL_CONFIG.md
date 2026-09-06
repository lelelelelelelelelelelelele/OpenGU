# AAGU-007 理想 YAML 与审阅说明

这份文档先固定 007 想表达的实验，供用户审阅。统一规范与执行入口由 [AAGU-034](../AAGU-034/WORKITEM.md) 实现；本稿不是已验证的可提交配置，也没有启动真实实验。007 的生命周期由 [WORKITEM.md](WORKITEM.md) 持有。

可直接查看 [experiment.ideal.yaml](experiment.ideal.yaml)。正式组合表已位于 `experiments/configs/aagu007/experiment.yaml`，科学范围与本稿一致。034 已接受并合入统一入口；后续修正已让文件名按字段定位公共目录，同时支持按组合表位置解析显式相对路径。执行基线与修正记录见 [WorkItem](WORKITEM.md#034-收口后的执行基线--2026-09-07)。

## 一张组合表

```yaml
kind: experiment
schema_version: 1
experiment_id: aagu007-cora-degree-r001-v1
stage: unlearning

dataset_ref: cora.yaml
selector_refs:
  - degree.yaml
unlearning_refs:
  - gnndelete.yaml
  - retrain.yaml
evaluation_refs:
  - post_method_metrics.yaml

seeds: [122, 722]
budget_ratios: [0.01]
matrix: cartesian_product
```

改 seed 或预算只改这张表。两个 Unlearning 方法各引用一份公共小表，运行时在内存中展开，不生成或维护 `gnndelete_seed122.yaml` 等逐条件副本。实验目录只拥有组合表；这份人读的审阅说明放在同一 WorkItem 下。

引用字段与公共目录固定对应：

| 字段 | 自动定位的目录 |
|---|---|
| `dataset_ref` | `experiments/configs/datasets/` |
| `selector_refs` | `experiments/configs/selectors/` |
| `unlearning_refs` | `experiments/configs/unlearning/` |
| `evaluation_refs` | `experiments/configs/evaluations/` |

因此组合表省略 `../` 和公共目录名；例如 `selector_refs: [degree.yaml]` 就定位公共 `selectors/degree.yaml`。Result 仍应记录系统解析出的配置来源及最终有效值。

## 公共小表表达什么

| 公共目录中的目标文件 | 拥有的配置及本轮预期有效值 |
|---|---|
| `datasets/cora.yaml` | 已持久化 Cora 图与划分身份；70% / 10% / 20%，split seed 2024；不得因训练 seed 改变重切分 |
| `selectors/degree.yaml` | Degree、train_mask 候选池、排序与取整规则；本轮预算由大表覆盖为 1%，1895 个候选经系统核验后对应 18 个节点 |
| `unlearning/gnndelete.yaml` | 独立 GNNDelete；当前约定为 GCN 2 层、hidden 64、dropout 0.5，原模型训练 100 epochs，遗忘 50 epochs、unlearn lr 0.01、alpha 0.5 |
| `unlearning/retrain.yaml` | 独立 Retrain；同样的 GCN 与训练规则，从头训练 100 epochs；不依赖 GNNDelete 的运行或输出 |
| `evaluations/post_method_metrics.yaml` | 单方法 F1、accuracy、交叉熵、分类 AUC、已有更新检测 AUC 及可用性状态 |

上述文件均位于 `experiments/configs/` 对应的公共目录中。共同训练规则仍为 Adam、lr 0.005、weight decay 0.000001、无 scheduler；公共小表只填写必要值和有意覆盖值，其他值由实际方法默认值解析。最终有效值及来源由系统写入 Result，不能只用本文列值代替运行记录。

删除语义保持现有合同：排除所选节点监督、移除关联边、保留孤立特征行，在原图上按相同口径评价。预算取训练候选数的比例，向下取整且至少一个。

## 两项大表覆盖

- `seeds` 覆盖实际消费者的训练 seed；模型型 Selector 与对应 GU/Retrain 按相同训练 seed 配对。Degree 不消费训练 seed，不因这两个 seed 生成两个不同的 Selector 身份；Dataset/Split seed 与 Random 抽样 seed 保持各自所属配置。
- `budget_ratios` 覆盖 Selector 的比例预算。本轮只有 0.01；规则为大表指定值优先于小表，小表优先于方法默认值。覆盖只作用于内存中的有效配置，不写回公共文件。

大表中的实验 ID、路径和矩阵标签只用于追踪，不进入不消费它们的模块缓存身份。这里只提出 seed 和预算两项显式覆盖，不提出任意参数 override。

## 四个独立方法输出

| 方法 | 训练 seed | 消费的 Selection |
|---|---:|---|
| GNNDelete | 122 | 同一 Degree、1% 的 Selection |
| Retrain | 122 | 同一 Degree、1% 的 Selection |
| GNNDelete | 722 | 同一 Degree、1% 的 Selection |
| Retrain | 722 | 同一 Degree、1% 的 Selection |

GNNDelete 和 Retrain 是同级方法，各自执行、判断缓存、保存 Output。后续独立 Metrics 任务分别比较 GNNDelete-122 与 Retrain-122、GNNDelete-722 与 Retrain-722，计算 retrain-gap；比较发生在结果层，不把两种方法合并为一个生产过程。

Metrics 使用公共 `evaluations/post_unlearning_utility_and_retrain_gap.yaml` 及真实已完成 Output 的引用，由正常登记和绑定流程提交。当前没有本轮 Output，不伪造引用，不在上面的 unlearning 表中混入需要双方输出的配对指标。

## 由 Result 验证的预测

| 环节 | 本轮预测 |
|---|---|
| Degree Score / Selection | 已有缓存，整体 HIT，producer 不调用 |
| GNNDelete-122 / GNNDelete-722 | 两个训练身份；对应产物不存在时分别 MISS |
| Retrain-122 / Retrain-722 | 两个独立训练身份；对应产物不存在时分别 MISS |
| 跨方法、跨 seed 的选集消费 | 共享同一 Degree Selection，不重复计算 Selector |

SyncMate 负责实验运行与 Result 交付，Cache 系统自动决定复用。Agent 只审阅 Result，判断实际 HIT/MISS、生产记录及配置身份是否支持预测和功能结论。预测不变成强制 HIT、指定旧产物或拦截合法 MISS 的运行条件；Result 信息不足时报告可观测性缺口。

## 文档验证边界

文件名与显式相对路径均由统一入口解析；配置检查核对公共引用、最终有效值、配置指纹及四个方法实例。软件检查不等于真实Result或科研gate验证；真实提交仍遵循本轮配置审阅和运行批准。
