# AAGU-036 · 回传内容与文件夹格式

本合同由用户逐项讨论并确认，作为 AAGU-036（已合并038）的实施依据。当前为已确认设计，尚不代表实现或验收完成。早期平铺文件方案与共享输入收集方案被本合同替代。

## 分工

远端持有正式图、划分和 Cache，执行 Selector / GU / Retrain，并从缓存输出计算 Metrics。常规回传是实验结果，不是 Cache 副本。本地可以直接使用收到的结果，也可通过 SSH 访问远端完成分析；不要求全部分析都能完全离线执行。

## 一个运行结果文件夹

```text
results/runs/<experiment-id>/<run-id>/
├── run.json
└── cells/
    └── cora_GCN_r0.05/
        └── GIF_degree/
            └── seed1337/
                ├── metrics.json      # 有指标时生成
                ├── selection.json    # 有选点时生成
                └── scores.npz        # 可选：已有分数/排名或选点收益
```

外层按 experiment-id / run-id 区分执行；内层按具体实验条件组织，保留按条件查找的直观性。run.json 统一列出每个 cell 的相对目录与条件，不能靠目录名推断唯一身份。示例不是穷尽命名规则：同方法存在不同参数、层数或配置变体时，使用可读变体名或稳定 cell 标识区分，禁止写入同一路径。Selector-only 不伪造 GU 方法，可按实际 Selector 名建立对应层。

Metrics、Selection 和可选 scores 位于各 cell 目录，不再将整次矩阵的全部结果平铺在根目录。不存在对应结果时不生成空文件；run.json 区分不适用、未请求、尚未完成和失败。每份常规结果主要是信息，不携带 Cache payload。run ID 只影响结果目录和运行记录，不引入计算 Cache Key；用户明确不再重复调查或修改已有缓存机制。

### run.json

- experiment_id、run_id、生成时间、实际执行 commit、提交的 experiment YAML 在仓库内的路径。
- cell_id 及用于读表/配对的简要条件：dataset、selector、GU/Retrain 方法、seed、预算等；不是把所有默认值和子 YAML 再展开复制。
- 计划 cell 与实际完成/失败状态；已有计时、HIT/MISS、实际计算或复用记录，以及简短错误信息。缺失计时明确表示未知，不新增虚构计时。
- cell 对应的 selection ID、metrics 行和可选 scores 数组键；文件实际包含哪些结果。
- 已提交的配置由 commit + 仓库内路径定位，不再回传整份展开配置。若允许运行时覆盖，仅记录实际覆盖项；没有覆盖则不保存差异副本。
- commit 是普通执行记录。Metrics 更新时记录本次生成所用 commit，不另外扩展多套版本或审批机制；远端已有 Cache 来源记录继续保留。

### metrics.json

- 本目录 cell / seed 的指标名与值，如 accuracy、F1、loss，以及该实验已要求的 before/after、drop、gap 等。按实际阶段生成，不要求每行都包含全部指标。
- 以 cell_id 与 run.json 对应；条件相同的基线按引用配对，不只保存跨 seed 的平均值。
- 不含 logits、逐节点预测、模型参数或图数据。
- Metrics 不是计算 Cache。修正指标逻辑时复用仍有效的远端输出 Cache，重算并回传更新结果；本地当前 Metrics 可刷新，不因重复收集跳过更新。
- 既有不可变 Cache、历史 run-bound 文件和审计记录不原位改写。通过新的结果生成/收集更新当前展示；具体更新落点在实施时对齐已有机制，不为本任务引入新的缓存层或复杂版本体系。

### selection.json

- 本目录 cell 实际选中的节点 ID、顺序和请求 K；cell_id 与 run.json 的条件对应。
- HIT 仍返回本次实际请求的选点；跨预算复用不能把来源大选集误报为本次小选集。
- IM 返回实际选出的 K 个节点，不把它解释为全节点固定排名，也不要求继续计算到所有节点。

### scores.npz（可选）

- 对 IF、Degree 等已产生全候选分数/排名的方法，可以交付 candidate_ids、scores、ranking；数组键与所属评分实例在 run.json 中对应，排序规则从配置/实现或必要的简短元数据定位。
- 对 IM，只能交付实际计算并记录的 K 步选点收益或其他实际输出，并标明其语义；不称为全候选分数或全量排名。
- 是否回传由具体运行的交付需求确定，不因“本地可能分析”自动强制。未回传可以通过 SSH 分析远端已有产物。
- 不为回传增加评分或扩大 K；不生成伪造的缺失排名。NPZ 仅是数值数组容器，不能直接复制 Cache payload 填充此文件。

## 不在结果文件夹中

| 内容 | 处理 |
|---|---|
| graph、边、特征、标签 | 留在远端正式输入；不新增 collect-inputs 收集 |
| train/val/test masks、节点名单、划分说明副本 | 不单独回传；正式输入按既有配置及远端核验保证 |
| logits / logits_before、逐节点概率与预测 | 留在远端 Output Cache，供 Metrics 重算或 SSH 分析 |
| 模型 checkpoint、模型状态和方法张量 | 留在远端 Cache |
| 梯度、Hessian/逆近似、优化器和其他临时状态 | 留在计算/缓存端 |
| 全量 experiment/子 YAML 展开副本、源码 | 不回传；已提交配置由 commit + 路径定位 |
| 传输临时 manifest、checksum 文件 | 由 SyncMate 执行核验并管理，不作为实验结果文件；按现有机制清理临时物，不删除 Cache 自身校验/来源记录 |
| 默认整份训练日志、远端报告副本 | 不进入常规包；run.json 保留简短失败信息，详细排障按需通过 SSH；本地由结果生成报告 |

## 036需要修正的实现

保留固定输入不再嵌入每份 Output 的改动；撤掉新增 collect-inputs。把目前直接复制完整缓存 payload 的 predictions.npz 导出替换为上述结果导出与收集声明。GU/Retrain 常规传 Metrics；Selection 与可选评分按实际产物交付。使用已有缓存能力，重点验证新的结果导出、声明、收集与 Metrics 更新；不再次调查或重做缓存机制，不修改其身份规则。验证 IM 不被迫生成完整排名，常规包不包含图/模型/logits。


## 实施归属

本修复归 OpenGU：结果生成、OpenGU 的 SyncMate 项目适配/产物声明/核验、本地结果读取及相关测试和文档。scripts/syncmate 下的 OpenGU 适配代码仍属于 OpenGU。SyncMate Core 的通用调度、传输和校验不在计划修改范围；若发现现有公开接口确实无法支持合同，先给出具体接口缺口再讨论，不扩大修改。用户已授权新任务实施，完成候选及实际回传验证后交用户接受；未授权正式科研实验或部署。

## 当前实现接口

普通执行入口沿用 `experiments/run.py <experiment.yaml> --run-id <新run>`。结果目录已存在时拒绝覆盖；运行中的 run.json 记录 pending/completed/failed，未开始的 cell 保持 pending，失败记录简短错误。回传文件只从 cell 的 files 声明产生，注册配方以相同矩阵展开枚举精确路径。

组合表默认不交付评分；`return_scores: true` 仅导出已经产生的数值数组。当前普通 target-direct 注册的 Selector 提供 candidate_ids/scores/ranking。AAGU-040 将现有 MC/Batch-CELF（im）与固定 RR 最大覆盖贪心（im_rr_greedy）接入普通入口，按实际 K 保存 Selection。IM 的 selection.json 额外包含 im_selector_seed、training_seed、selection_reference（artifact_id / recipe_hash / content_hash）和 selector_seed_source；两条 seed 与 run 条件交叉核验，HIT 同样回传。Score 状态为 not_applicable。当前 Selection Store 没有保留收益数组，包含 IM 的表拒绝 return_scores: true，不为回传新增计算。

独立 Metrics 表使用 `output_inputs: [{run: <已有run.json路径>, sha256: <文件SHA256>}]`，在持有正式输入和 Cache 的执行端重算。生成新 run 后走普通收集，既有 results 表按原实验和 cell 选择最新完成的指标；不把旧轮未请求指标混入新轮，也不改写历史 run。Metrics 的来源 run 以简要引用保存。没有通用运行时配置覆盖入口，因此不创建空 overrides 或配置副本。

`read_run(path, sha256)` 读取已校验的结果目录。机器交付核验包含配置/身份/预算/文件集合与哈希检查，不以本地复算 logits 作为常规回传前提。软件验证、正式 SSH 实验和人的科研接受分别记录。
