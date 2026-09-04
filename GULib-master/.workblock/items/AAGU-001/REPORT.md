# AAGU-001 · 实验合同与注册规范验收

## Human Result

### 实际增量

已形成三块独立参数表的合同，并按本轮讨论区分“人工填写的覆盖值”和“解析后的完整有效配置”：OpenGU 默认值可省略；方法名分发实现，共享代码不等于共享配置或缓存身份。已交付[公共规范](../../../docs/experiment_contract/README.md)、[真实参数表](../../../docs/experiment_contract/PARAMETERS.md)和 10 份独立实例，补充 LiSSA 20 次递推的具体含义。

### 核心观察

两份省略 parameters 的示例，按已审查的实际默认值展开后，与显式填写版本逐项相等；10 份实例、25 个文档链接检查通过，已有 sanity dry-run 返回一个 `would_run` cell。001 已在独立 worktree 继续同一分支/Claim，026 登记补充已提交 main。上述证据支持合同表达，不证明生产加载器或真实缓存 HIT 已实现。[本轮回执](evidence/defaults-verification.json)

### 当前决定

> 当前验收决定：`待决定`

建议接受更新后的 001 公共合同：它允许简短配置，同时保留有效参数、方法分发和缓存依赖的明确边界。请由研究负责人决定接受或返工；接受对象仅是 001，不代表 026 已完成，也不批准新的 GPU 矩阵。

## 关键交付

| 交付 | 审阅重点 |
|---|---|
| [公共合同](../../../docs/experiment_contract/README.md) | 大表/小表职责、字段约束、缓存变更矩阵、注册/执行/接纳分离 |
| [真实参数表](../../../docs/experiment_contract/PARAMETERS.md) | YAML 显式值、代码有效默认值、可比较变量、仍待科研决定的部分 |
| [Selector 默认值](../../../docs/experiment_contract/examples/selector_b_hutch_defaults.yaml) / [GU 默认值](../../../docs/experiment_contract/examples/unlearning_gnndelete_defaults.yaml) | 人工表省略 parameters；按实际默认值展开后与完整实例等价 |
| [Selector 32](../../../docs/experiment_contract/examples/selector_b_hutch32.yaml) / [64](../../../docs/experiment_contract/examples/selector_b_hutch64.yaml) | 同一 b_param_hutch 方法只改探针数，没有新的变体实现 |
| [GU 0.01](../../../docs/experiment_contract/examples/unlearning_gnndelete.yaml) / [0.02](../../../docs/experiment_contract/examples/unlearning_gnndelete_lr002.yaml) | 只改 GU 学习率，不应污染已完成的 Selector |
| [Selector-only](../../../docs/experiment_contract/examples/experiment_selector_only.yaml) / [已有 Selection → GU](../../../docs/experiment_contract/examples/experiment_gu_from_selection.yaml) | 小模块与实验大表解耦；示例显式无执行授权，未伪造资产哈希 |

## 对核心验收的观察

### 参数共识是否具体 — PASS

沿 formal YAML、stage、runner、模型属性和 GU trainer 追踪，找到了不在 YAML 中的实际默认值。特别区分 GCN 属性 0.005/1e-6 与 runner 的后备值，也区分基础训练 num_epochs 与节点遗忘 unlearning_epochs。表格给出值、源码链接、配置比较边界与消费者；这是源码/配置证据，不是实测优化效果。

### 三块配置和方法变体是否表达清楚 — PASS（合同/实例层）

10 份 YAML 可解析，引用存在。检查逐字段差异：Hutch 两表仅 probes 不同，GU 两表仅 unlearn_lr 不同；两份省略 parameters 的实例展开已审查默认值后与完整实例相等。degree 没有模型字段；Selector-only 不要求 GU，已有 Selection → GU 不要求 selector_refs。验证器是文档检查工具，不是生产加载器；本项不声称真实 HIT。

### 方法分发与数值含义是否明确 — PASS（源码审查/合同层）

具体 method 选择方法实现及字段规则；不同方法可共享内核，但参数实例和缓存身份独立。固定算法细节不强制做成配置开关；IF 求导/目标/求解配置和 TracIn 快照/权重按实际需要保留。LiSSA iterations=20 指固定模型上每个向量的 20 次 HVP 递推，非训练轮数或节点数；B-Hutch 32 个探针对应该分支 640 次递推，不代表总 runner 开销或近似精度已达标。

### worktree 与 main 登记是否落实 — PASS（本地 Git/Claim）

保留原分支、baseline、既有候选和同一 Claim，将 001 挂入 E:/project/OpenGU-worktrees/aagu-001-contract，再由标准 parallel-resume 恢复。026 原登记在 main@8383e30，默认值/方法分发验收补充与 001 parallel 声明在 main@cdbc977；没有把 001 的待验收内容合入 main，没有 026 Claim。

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
- 不同 SGC/GCN/GAT backbone 的节点排序比较：仅记录待定义问题，尚无实验运行或结论；正式设计前须确认“相关性”指评分排序还是表示相似度。

## 技术附录

- 审查基线：`8383e30239398c5268965e088afdfba7abc74ca9`。
- 内容检查 checkpoint：`c0c433f66eb1def3dab06e05ac7ebd4ecbef026c`；[原始回执](evidence/verification.json)绑定该 checkpoint，不冒充正式实验结果。
- 本轮内容 checkpoint：`53d0ed22d8baafe39a3f1eca5255f64c05d0f608`；[本轮内容回执](evidence/defaults-verification.json)绑定该提交。待决定候选为本报告所在 source branch `refs/heads/codex/aagu-001-experiment-contract` 的干净 HEAD；报告对齐后的复验另存[最终回执](../../runtime/evidence/AAGU-001/verify-defaults-final-aligned.json)。
- 命令：项目 gnn Python 运行 `evidence/verify_contract.py --checkpoint <精确提交> --output <本 Block runtime evidence 路径>`；另运行 `scripts/dashboard/refresh.py --check` 和 `python -m unittest tests.test_dashboard_refresh -v`。
- HTML 渲染检查：PASS。已实际渲染并查看 1366×900 桌面与 390×844 窄屏首尾；无页面横向溢出或断图，正文可读。桌面首屏完整决定区底部为 640.75px；窄屏正文自然纵向滚动，不声称整块建议都在首屏。[桌面首屏](../../runtime/evidence/AAGU-001/defaults-desktop-top.png)、[窄屏首屏](../../runtime/evidence/AAGU-001/defaults-narrow-top.png)。
- 当前没有 Apply、push、install、SSH 写入或 026 Claim。下一步是用户对 001 的 formal 决定，不自动进入 026。
