# AAGU-015 两阶段定义

本目录是 [AAGU-015](../../../.workblock/items/AAGU-015/WORKITEM.md) 的第一项配置产物。
015 交付实验方案与可执行链路，并用必要的最小验证确认接通。306/612 表示方案展开范围，
全量执行和完整科研结果不属于本次验收要求。当前配置仍未绑定数据或 Selection，链路尚在实现中。

## 配置入口

- [stage_s.yaml](stage_s.yaml)：三个 Dataset/Split、17 个 Selector、训练 seeds 和预算的生成源表。
- [stage_u.yaml](stage_u.yaml)：固定 Stage S Selection 对应的 GNNDelete/GIF 和 retrain-gap 评价。
- `datasets/`、`selectors/`、`unlearning/`、`evaluations/`：独立模块实例。
- `generated/stage_s/`：18 张已接受 modular schema 的大表，每表包含 17 个独立 selector cell。
- `generated/stage_u/`：306 张已接受 modular schema 的大表，每表只引用一个既有 Selection，并包含两种 GU。

两份源表由本目录的配置生成器消费；`generated/` 中的普通实验 YAML 才直接交给
已接受入口 `experiments/run.py`。没有扩展或替换其 schema，也没有增加一个实验执行入口。
生成器将训练 seed 和预算放回各自的方法实例，避免用批次身份污染缓存。
17 个 Selector 源表只维护一次；94 个 seed/budget 实例和 6 个 GU 实例由源表生成。

从项目目录执行：

```powershell
& 'E:/conda_package/envs/gnn/python.exe' -B -X utf8 -m experiments.aagu015.definitions generate
& 'E:/conda_package/envs/gnn/python.exe' -B -X utf8 -m experiments.aagu015.definitions check
& 'E:/conda_package/envs/gnn/python.exe' -B -X utf8 -m experiments.aagu015.definitions dry-run
& 'E:/conda_package/envs/gnn/python.exe' -B -X utf8 experiments/run.py experiments/configs/aagu015/generated/stage_s/cora-seed42-r0.01.yaml --dry_run
& 'E:/conda_package/envs/gnn/python.exe' -B -X utf8 experiments/run.py experiments/configs/aagu015/generated/stage_u/cora-seed42-r0.01-degree.yaml --dry_run
```

`generate` 仅写配置。`check` 和 `dry-run` 只读文件并向 stdout 返回结果；调用者可以另行保存展开证据。
展开不会加载数据、训练、写 Cache V2 或创建研究结果。所有 generated 文件由生成器拥有；
修改源表后重建。后续绑定真实 Selection 时，应由受验证的收集回执生成运行计划，不能手工填造哈希。

## 当前参数与解释边界

GCN 默认两层、hidden=64、dropout=0.5；100 epochs、Adam、lr=0.005、weight decay=0.000001、
无 scheduler。模型型 Selector 的参数范围默认 `last_layer`，目标损失只读取 validation。
这里使用当前模块默认值，不继承历史 public-split 报告的 hidden=16、200 epochs、all-trainable 或固定小 K。
完整展开值与逐字段来源见本 WorkItem 的定义展开证据。

TracIn 显式指定 `[1,10,25,50,75,100]`：6-checkpoint 消费全部六点，3-checkpoint 消费
`[1,50,100]`。底层训练入口捕获每个 epoch；评分只依赖所选 checkpoint，不能把方法名 `_6`
解释为默认的 100 个 checkpoint。`random` 继承方法默认 seed 104245；训练 seed 不改变 random/degree。

| 数据集 | 节点数预期 | 训练候选数预期 | 1% K 预期 | 5% K 预期 |
|---|---:|---:|---:|---:|
| Cora | 2708 | 1895 | 18 | 94 |
| CiteSeer | 3327 | 2328 | 23 | 116 |
| PubMed | 19717 | 13801 | 138 | 690 |

节点数是配置校验预期，候选数/K 是按 AAGU-006 已接受的 70/10/20、split seed 2024 与 floor 规则计算的预测值。
它们不是实际读入 mask 的证据；真实 candidate count/hash 必须在正式前置重新验证。

306 个 S cell 对应 141 个条件 Score 依赖组、282 个条件 Selection 依赖组和 9 个条件训练准备组。
这些组由有效配置比较得到，并不是 Recipe/Artifact 哈希、实际训练次数或 cache HIT。
GU 和 Selector 的相同模型配置也必须经过数据、训练、checkpoint、数值与实现身份核验后才能共享。

## 链路实现待办

1. 三个 `datasets/*.yaml` 的 manifest、manifest SHA 和 split hash 当前为空，需要实现读取、验证和绑定接缝，
   并验证候选与 checkpoint 准备/复用。当前生成器不自动下载或准备数据；空引用不能视为链路已接通。
2. Stage S 需要接通完整 Score、排名和 Selection 的输出、Q1–Q4 比较和时间拆分消费者，以最小验证核对语义。
3. Stage U 的配置直接保留 `selection_input`，没有 `selector_refs`；当前均未绑定。
   已有 modular GU 仅支持 utility 消费；`post_unlearning_utility_and_retrain_gap` 会在写入前拒绝，
   不得降为 utility-only 来宣称接通。还需完整重训练及删除目标、保留节点、测试、collateral、预测变化的真实消费者链。
4. 最小端到端验证需经过实际消费者，证明固定 Selection 复用及正确模型进入评价，记录输入、代码和产物身份。
   软件 fixture 与隔离 smoke 只能支持实现判断，不写成三数据集的科学结果。

## 后续正式运行边界

正式数据只能使用 `/autodl-fs/data/OpenGU/GULib-master/data/processed` 中验证过的 canonical pair。
实际 SSH/GPU 运行仍需注册 launcher、设备配置、三端同一已落地 main、明确的 canary 范围、成本门槛和调度批准。
这些规则服务后续正式执行；不再以缺全量科研结果或未完成正式部署来阻塞 015 的本地链路实现。
旧 target-direct recipe 不替代本轮调度授权；不从本配置直接铺开 306/612 矩阵。

验收所需证据是方案、链路实现与最小验证证据；完整排名对照、三数据集成本和攻击效果结论由后续获准运行产生。
