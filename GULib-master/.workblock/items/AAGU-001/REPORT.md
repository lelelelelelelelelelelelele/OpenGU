# AAGU-001 · 实验合同与注册规范验收

## Human Result

### 实际增量

将讨论落实为一份可审阅合同：实验大表只组合 Dataset/Split、Selector、Unlearning 三块独立参数表；预算归 Selector，两侧模型分别声明，方法变体只用不同配置表。已交付[公共规范](../../../docs/experiment_contract/README.md)、[真实参数表](../../../docs/experiment_contract/PARAMETERS.md)和 8 份独立实例。

### 核心观察

现在可以查到具体有效值和代码来源，而不只有抽象字段名：GCN 训练 lr=0.005、GU lr=0.01；基础训练 100 轮、节点遗忘 50 轮；LiSSA=20/25/0.01、Hutch=32/1729，且列明各自影响哪些评分。两组变体各只改变一个参数；已有 sanity 实验 dry-run 实际返回一个 `would_run` cell。配置/文档检查通过，但没有执行正式实验或修复缓存实现。[验证回执](evidence/verification.json)

### 当前决定

> 当前验收决定：`待决定`

建议接受 001 的公共合同：它已覆盖参数归属、当前来源、变体与缓存影响，以及可复核的注册入口示例。请由研究负责人决定接受或返工；接受对象仅是 001，不代表 026 已完成，也不批准新的 GPU 矩阵。

## 关键交付

| 交付 | 审阅重点 |
|---|---|
| [公共合同](../../../docs/experiment_contract/README.md) | 大表/小表职责、字段约束、缓存变更矩阵、注册/执行/接纳分离 |
| [真实参数表](../../../docs/experiment_contract/PARAMETERS.md) | YAML 显式值、代码有效默认值、可比较变量、仍待科研决定的部分 |
| [Selector 32](../../../docs/experiment_contract/examples/selector_b_hutch32.yaml) / [64](../../../docs/experiment_contract/examples/selector_b_hutch64.yaml) | 同一 b_param_hutch 方法只改探针数，没有新的变体实现 |
| [GU 0.01](../../../docs/experiment_contract/examples/unlearning_gnndelete.yaml) / [0.02](../../../docs/experiment_contract/examples/unlearning_gnndelete_lr002.yaml) | 只改 GU 学习率，不应污染已完成的 Selector |
| [Selector-only](../../../docs/experiment_contract/examples/experiment_selector_only.yaml) / [已有 Selection → GU](../../../docs/experiment_contract/examples/experiment_gu_from_selection.yaml) | 小模块与实验大表解耦；示例显式无执行授权，未伪造资产哈希 |

## 对核心验收的观察

### 参数共识是否具体 — PASS

沿 formal YAML、stage、runner、模型属性和 GU trainer 追踪，找到了不在 YAML 中的实际默认值。特别区分 GCN 属性 0.005/1e-6 与 runner 的后备值，也区分基础训练 num_epochs 与节点遗忘 unlearning_epochs。表格给出值、源码链接、配置比较边界与消费者；这是源码/配置证据，不是实测优化效果。

### 三块配置和方法变体是否表达清楚 — PASS（合同/实例层）

8 份 YAML 可解析，引用存在。检查逐字段差异：Hutch 两表仅 probes 不同，GU 两表仅 unlearn_lr 不同；degree 没有模型字段；Selector-only 不要求 GU，已有 Selection → GU 不要求 selector_refs。检查证明实例表达符合合同，不证明当前运行器已接受新格式或缓存已正确命中。

### 现有注册入口能否使用 — PASS（本地 dry-run）

没有改动 sanity_one_cell.yaml，通过其既有 `experiments/run.py --dry_run` 入口得到 total cells=1、would_run=1、exit=0。另调用 formal-v2 的真实只读 load_config，得到 Cora 1895 个计划候选、K=18/94；cp3 实际映射到 epochs [1,50,100]。这些观察支持入口/参数追溯，不证明远端数据存在或已执行 train/unlearn。

### 科学职责和实现边界是否分开 — PASS（规范层）

合同明确注册不等于执行授权，SyncMate done 不等于科学接纳；001 不选择 015 的最终 IF 方案。当前 GU→Selector 参数污染和 17-score 整包键仍交 026；未来真实 cold/warm、跨实验复用、producer 未调用必须另验。

### 配套文档是否可用 — PASS（结构与链接）

两个规范文件的 25 个本地链接可解析；看板生成一致性检查及 7 项看板测试通过。HTML 实际渲染观察记录在技术附录，不能用结构检查代替。

## 未观察与非目标

- 正式数据/split/checkpoint/Selection 的远端真实哈希：NOT OBSERVED；示例填 null，不填假值。
- 新格式生产 parser、按方法缓存隔离、真实跨实验 HIT：本次未实施，属于 026。
- 正式 GPU 训练/遗忘、科学效果和完整 306-cell 矩阵：NOT OBSERVED，未运行且未扩大授权。
- 人类验收：NOT CONFIRMED；当前仍需用户决定。

## 技术附录

- 审查基线：`8383e30239398c5268965e088afdfba7abc74ca9`。
- 内容检查 checkpoint：`c0c433f66eb1def3dab06e05ac7ebd4ecbef026c`；[原始回执](evidence/verification.json)绑定该 checkpoint，不冒充正式实验结果。
- 待决定候选为本报告所在 source branch `refs/heads/codex/aagu-001-experiment-contract` 的干净 HEAD；报告与看板下一步对齐后的最终复验另存[最终回执](../../runtime/evidence/AAGU-001/verify-final-aligned.json)，由相同脚本复验当前候选。
- 命令：项目 gnn Python 运行 `evidence/verify_contract.py --checkpoint <精确提交> --output <本 Block runtime evidence 路径>`；另运行 `scripts/dashboard/refresh.py --check` 和 `python -m unittest tests.test_dashboard_refresh -v`。
- HTML 渲染检查：PASS。实际用 headless Edge 渲染并查看 1366×900 桌面与 390×844 窄屏首尾截图；标题、正文与决定区可读，无页面横向溢出或断图，桌面首屏完整呈现建议与决定。窄屏正文自然纵向滚动。[桌面首屏](../../runtime/evidence/AAGU-001/report-desktop-top.png)、[窄屏首屏](../../runtime/evidence/AAGU-001/report-narrow-top.png)。
- 当前没有 Apply、push、install、SSH 写入或 026 Claim。下一步是用户对 001 的 formal 决定，不自动进入 026。
