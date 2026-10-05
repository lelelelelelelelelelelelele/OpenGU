# EXP-079 · Surrogate 多 seed 验证

`surrogate_multiseed.yaml` 是完整科学范围（2520格）的核对基准。实际执行使用下表15个原生配置及对应Recipe；不要额外提交完整矩阵。

每个作业覆盖一个数据集和两个训练seed（168格）。全部作业并集保持完整10seed，不遗漏原3seed；原有计算仅在精确缓存身份匹配且产物存在时复用，评价照常执行。跨作业共用同一 `experiment_id`，各自使用独立短run ID。

## 运行范围

| 顺序 | 数据集 | 训练seed | 配置 | Recipe | run ID |
| --- | --- | --- | --- | --- | --- |
| 1 | cora | 42, 212 | [cora_b01.yaml](cora_b01.yaml) | [opengu-exp079-cora-b01](../../../scripts/syncmate/recipes/opengu-exp079-cora-b01.yaml) | `e79c1` |
| 2 | cora | 2024, 0 | [cora_b02.yaml](cora_b02.yaml) | [opengu-exp079-cora-b02](../../../scripts/syncmate/recipes/opengu-exp079-cora-b02.yaml) | `e79c2` |
| 3 | cora | 1, 2 | [cora_b03.yaml](cora_b03.yaml) | [opengu-exp079-cora-b03](../../../scripts/syncmate/recipes/opengu-exp079-cora-b03.yaml) | `e79c3` |
| 4 | cora | 3, 4 | [cora_b04.yaml](cora_b04.yaml) | [opengu-exp079-cora-b04](../../../scripts/syncmate/recipes/opengu-exp079-cora-b04.yaml) | `e79c4` |
| 5 | cora | 5, 6 | [cora_b05.yaml](cora_b05.yaml) | [opengu-exp079-cora-b05](../../../scripts/syncmate/recipes/opengu-exp079-cora-b05.yaml) | `e79c5` |
| 6 | citeseer | 42, 212 | [citeseer_b01.yaml](citeseer_b01.yaml) | [opengu-exp079-citeseer-b01](../../../scripts/syncmate/recipes/opengu-exp079-citeseer-b01.yaml) | `e79s1` |
| 7 | citeseer | 2024, 0 | [citeseer_b02.yaml](citeseer_b02.yaml) | [opengu-exp079-citeseer-b02](../../../scripts/syncmate/recipes/opengu-exp079-citeseer-b02.yaml) | `e79s2` |
| 8 | citeseer | 1, 2 | [citeseer_b03.yaml](citeseer_b03.yaml) | [opengu-exp079-citeseer-b03](../../../scripts/syncmate/recipes/opengu-exp079-citeseer-b03.yaml) | `e79s3` |
| 9 | citeseer | 3, 4 | [citeseer_b04.yaml](citeseer_b04.yaml) | [opengu-exp079-citeseer-b04](../../../scripts/syncmate/recipes/opengu-exp079-citeseer-b04.yaml) | `e79s4` |
| 10 | citeseer | 5, 6 | [citeseer_b05.yaml](citeseer_b05.yaml) | [opengu-exp079-citeseer-b05](../../../scripts/syncmate/recipes/opengu-exp079-citeseer-b05.yaml) | `e79s5` |
| 11 | pubmed | 42, 212 | [pubmed_b01.yaml](pubmed_b01.yaml) | [opengu-exp079-pubmed-b01](../../../scripts/syncmate/recipes/opengu-exp079-pubmed-b01.yaml) | `e79p1` |
| 12 | pubmed | 2024, 0 | [pubmed_b02.yaml](pubmed_b02.yaml) | [opengu-exp079-pubmed-b02](../../../scripts/syncmate/recipes/opengu-exp079-pubmed-b02.yaml) | `e79p2` |
| 13 | pubmed | 1, 2 | [pubmed_b03.yaml](pubmed_b03.yaml) | [opengu-exp079-pubmed-b03](../../../scripts/syncmate/recipes/opengu-exp079-pubmed-b03.yaml) | `e79p3` |
| 14 | pubmed | 3, 4 | [pubmed_b04.yaml](pubmed_b04.yaml) | [opengu-exp079-pubmed-b04](../../../scripts/syncmate/recipes/opengu-exp079-pubmed-b04.yaml) | `e79p4` |
| 15 | pubmed | 5, 6 | [pubmed_b05.yaml](pubmed_b05.yaml) | [opengu-exp079-pubmed-b05](../../../scripts/syncmate/recipes/opengu-exp079-pubmed-b05.yaml) | `e79p5` |

## 预算与执行

每个作业的工程预算为15152秒（约4小时13分），超时上限21600秒（6小时）。这是沿用EXP-079登记的全MISS串行估时：每个dataset×seed为7576秒；总预算227280秒（约63.1小时）。估时置信度低，不能保证六小时内完成；实际命中和时长由运行证据记录。排队、回传不计入GPU运行预算。

按表顺序逐个执行并完成回传核验后再推进；当前Recipe是输入声明，不代表任务已提交。任一作业失败、超时或身份检查不通过时停止后续提交，保留原作业身份和产物，按既有恢复流程处理，不原地覆盖或自动重试。所有批次应使用同一已审阅、已安装的主线版本；活跃运行期间不切换SSH检出。

完整配置、执行分片及全部Recipe一起交付后，只进行一次已授权安装。正式启动时仍需由既有dispatch preflight核验三端版本、数据、GPU和run ID占用；本地dry-run及Recipe生成不替代它。

后续分析先单独检查新增7seed，再经身份核对汇总10seed。现有utility及retrain-gap metrics已提供尺度分析所需基础量；本次不新增指标producer、不冻结仍在讨论的归一化统计口径。

实验状态由[EXP-079](../../../self/research/experiments/EXP-079.json)维护，执行流程见[Runbook](../../../self/research/RUNBOOK.md)。修改任何配置或其引用时，须通过既有生成命令重新产生并审阅Recipe哈希；分片与完整矩阵的有效参数及覆盖须重新验证。
