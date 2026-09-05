# AAGU-007 旧接口展开草案（留存对照）

当前审阅入口已改为同一 WorkItem 下的 [理想 YAML 文档](../../../.workblock/items/AAGU-007/IDEAL_CONFIG.md) 与 [理想 YAML 文件](../../../.workblock/items/AAGU-007/experiment.ideal.yaml)。本目录的逐 seed 小表是旧解析器下已检查的展开草案，只保留作对照，不作为最终提交版本。理想稿由大表声明 seed 与预算，并引用公共小表，待 AAGU-034 统一入口支持后绑定验证。以下说明保留既定科学范围和结果审查约定；真实实验未启动，生命周期以 [同一 WorkItem](../../../.workblock/items/AAGU-007/WORKITEM.md) 和 live Claim 为准。

## 审阅范围

| 项目 | 本次配置 |
|---|---|
| 数据 | Cora，2708 节点；使用已有持久化图与 split，启动时核验 |
| 划分 | 70% / 10% / 20%，split seed 2024 |
| 删除请求 | Degree，训练候选池的 1%，向下取整且至少 1；候选数 1895 经核验后对应 18 个节点 |
| 模型 | GCN，2 层，hidden 64，dropout 0.5 |
| 训练 | seeds 122、722；各 100 epochs，Adam，lr 0.005，weight decay 0.000001 |
| 方法：GNNDelete | seeds 122、722；各自遗忘 50 epochs，unlearn lr 0.01，alpha 0.5；独立保存 Output |
| 方法：Retrain | seeds 122、722；各自从头训练 100 epochs；独立保存 Output |
| 单方法指标 | F1、accuracy、交叉熵、分类 AUC、已有更新检测 AUC 及可用性状态 |
| 配对指标 | 收集后单独计算 perf_before / perf_unlearn / perf_retrain / drop_retrain / gap / gap_pct |

当前矩阵准确表示为 **1 个 Dataset/Split × 1 个 Degree × 2 个同级方法（GNNDelete、Retrain）× 2 个训练 seed（122、722）**，共 4 个独立方法输出。删除预算固定为 1%。两种方法都直接消费同一个已验证 Selection，分别配置、执行、查询缓存和保存 Output；GNNDelete 不调用 Retrain，Retrain 不依赖 GNNDelete 的执行或输出。大表中的共同枚举不把两种方法合并成一次成对训练。

后续独立 Metrics 才读取已完成的输出，形成两组相同 seed 的比较。Retrain 在 retrain-gap 指标中提供参照值，这个评价角色不改变它在方法表和执行层中的同级地位。Retrain 缺少原模型预测时，更新检测 AUC 按消费者报告缺失状态，不虚构数值。

本组小表显式固定当前消费者展开的参数。节点删除排除选中节点的监督并移除关联边，保留孤立特征行；两种方法在原图上用同一评价口径保存输出。

## 与已跑过的实验比较

已直接读取本地回传的 `results/runs/sm005-gpu4090/modular/sm005-cora-degree-gnndelete/sm005-gpu-v1/summary.json`：Cora、Degree、GNNDelete、1%（18 节点）、seed 42 的单元确实已在 RTX 4090 上真实执行。该文件 SHA-256 为 `16208bf6150576d975f7bd0f9def6a0d01b6ed09c04dafb74b073859de5545b1`。本草案原先沿用 seed 42；用户本轮将训练 seed 改为 122、722，其他模型和方法超参数保持不变。

旧运行只包含一个 GNNDelete 结果和 `post_unlearning_utility`，未包含独立 Retrain 或配对 retrain-gap。它使用旧版执行/指标实现；本次拟验证两个训练 seed 下当前已接受的独立 Output、Retrain 和收集后比较链。旧 seed 42 的方法结果不能充当 seed 122 或 722 的方法结果。

实验运行完全交给 SyncMate：通过其登记入口提交获批配置，由正常流程负责运行预检、执行、状态管理、结果收集、校验和 Result 交付。运行中的 Cache 系统依据实际请求自动判定复用，消费者按缓存结果读取产物或在合法的精确 MISS 时调用 producer。Agent 的职责是审阅 SyncMate 交付的 Result，判断 HIT/MISS 是否符合本次配置和预期，以验证 Cache 及相关功能是否正常；运行、缓存选择和产物处理不由 Agent 人工替代。

## 本次缓存预测与观测口径

本次改变的是方法小表的 `training.seed`；Dataset/Split 小表的 `split.seed: 2024` 不变。当前 Degree 不消费模型或训练 seed，其 Score 身份只包含实际输入、有效 selector 参数和 producer；Selection 另绑定 Score、候选集合、删除预算和排序规则。GNNDelete 与 Retrain 的 Output 身份均包含完整训练合同，因而包含各自的训练 seed。

用户明确 Degree 已有缓存，因此本轮预测是 Cache 自动让整个 Degree Selector 链均 HIT，Score 与 Selection 的 `producer_called` 均为 false。预测用于对照真实 Result，不转化为强制 HIT、预先指定缓存产物或禁止正常 MISS 生产的执行条件；该预测尚待真实运行核验，不能写成已观测结果。

| 环节 | seed 122 与 722 的关系 | 对本轮的预测 |
|---|---|---|
| 持久化图与 split | 同一精确输入 | 只读复用，不重切分 |
| Degree Score / Selection | 同一计算身份，已有缓存 | 本次第一次访问即应双 HIT，Score 与 Selection 均不调用 producer |
| 四个方法消费 Selection | 同一已缓存 Selection 引用 | 两个 seed、两种方法全都消费缓存命中的选集，不重算 Selector |
| GNNDelete 原模型 checkpoint | training.seed 不同 | 两个身份；各自精确缓存不存在时训练 |
| GNNDelete Output | training.seed 及原 checkpoint 绑定不同 | 两个身份；无各自精确产物时均 MISS，不能跨 seed 命中 |
| Retrain Output | training.seed 不同，且 method 与 GNNDelete 不同 | 两个独立身份；无各自精确产物时均 MISS |

Agent 只依据 SyncMate 交付的 Result 审查功能表现：Degree Score 与 Selection 是否均 HIT、是否未调用 producer，四个独立方法实例是否消费同一 Selection，以及 GNNDelete 和 Retrain 的 122、722 是否各有正确的输出身份和 HIT/MISS。Result 中的身份和调用记录用于解释缓存判断，不意味着 Agent 另行操作远端缓存或手工处理产物。

若 Result 与预测不符，从 Result 已提供的配置、身份和生产记录分析原因并报告功能判断。预测不符不触发 Agent 干预执行、指定旧产物、清缓存、强制命中或追加重跑；系统已有的拒绝规则照常生效。Result 缺少必要信息时，指出结果可观测性缺口，保持该判断为无法核验，不通过手工执行或收集绕过 Result，也不把一个 HIT 标签或耗时变短直接当作复用正确的证据。

依赖模型的 selector 会消费自己的训练合同和 checkpoint；改变这些实际输入会改变其身份。随机 selector 的随机种子也属于其自身有效参数。只改变下游 GU 的 seed，不能无条件使所有 selector 失效。若改变 split seed，候选集合或实际输入可能改变，即使 Degree 的公式不使用随机数，也不能继续沿用旧 Selection 身份。

## 运行入口与批准边界

本草案使用现有 modular experiment 消费者，不能直接作为旧 `syncmate_target_direct_formal_v2.yaml` 的替换文件。旧配方有双预算及更多 selector，本次提案缩为单预算并提供独立 experiment 入口；未经本次批准，不改写旧配方或把它的运行许可套用到本草案。

用户批准这组配置后，通过同一 AAGU-007 对应的 SyncMate 登记入口运行。该入口须绑定本次范围、所有小表的配置身份、完整 Git SHA 和新的结果身份，并由现有门禁检查三端 main 一致性、共享 stage check 与专题 preflight。目标为既有 `autodl-opengu`、唯一活跃检出 `/autodl-fs/data/OpenGU/GULib-master` 和 RTX 4090；拟沿用现有原子作业的 1800 秒超时。设备、超时、运行路径由 SyncMate 执行合同拥有，不塞入科学 YAML。

当前代码已有独立方法与离线 Metrics 消费者，但尚未登记本草案的可提交 recipe；该接入缺口须通过正常登记与验证流程补齐，不能把配置可解析说成 SyncMate 已可提交。数据身份沿用已记录的 SM-005 配置，运行条件以 SyncMate 及 OpenGU 消费端门禁的真实检查和 Result 为准。Agent 不用临时 SSH 命令、手工执行或手工 collect 替代 SyncMate；检查失败时保留系统 Result 并报告。

Cache 自动复用的实际情况从 Result 如实报告；新作业完成不等于各 producer 都做了冷计算。已存在结果不得覆盖，真实耗时需区分首次生产和本次读取。

## 收集后的比较

四个方法实例独立保存 Output，收集和校验由 SyncMate 正常流程负责。后续比较也通过 SyncMate 登记的独立 Metrics 任务执行：使用已完成输出的真实引用，分别配对 GNNDelete-122 ↔ Retrain-122、GNNDelete-722 ↔ Retrain-722，消费 [retrain_gap.yaml](retrain_gap.yaml)，交付比较 Result。方法运行与 Metrics 的任务绑定均须完成正常接入，Agent 不自行执行离线计算或手工拼接产物。本轮尚无 Output，故不预填或编造引用。

Metrics 消费者只读产物，不调用训练或模型前向，并按现有合同校验配对语义。Agent 审阅其 Result 中的配对和指标表现，汇总 007 功能验证结论供用户验收。该单请求验证不证明其他 selector、预算、数据集或后续矩阵已通过。

## 本地配置检查

```powershell
& E:/conda_package/envs/gnn/python.exe -B -X utf8 experiments/run.py experiments/configs/aagu007/experiment.yaml --dry_run
```

该命令只展开定义与有效参数，不读取正式数据或调用 producer，也不代表远端运行条件已通过。
