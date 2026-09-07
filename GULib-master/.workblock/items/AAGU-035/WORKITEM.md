# AAGU-035 · 多数据集实验矩阵与 SyncMate 回传

Block ID: `AAGU-035`
Item Version: 2.1
Item Type: `Block`
当前状态: `working / claimed`
Stable locator: `.workblock/items/AAGU-035/WORKITEM.md`

## Human Surface

### 核心意图

用户应能用一份普通实验 YAML 表达 Dataset × Selector × 下游方法 × Seed × 删除比例，而不必为 Cora、CiteSeer、PubMed 手工维护三份除 dataset 外相同的表。多数据集只是实验矩阵的一个维度，每个数据集仍绑定自己的正式 Dataset/Split、manifest、候选节点空间和结果证据。

### 本次增量

从当前单一 `dataset_ref` 的普通实验协议出发，形成统一的 `dataset_refs` 列表协议，并贯通配置解析、矩阵展开、运行、结果路径与汇总、SyncMate 项目侧声明/收集/验收。单数据集也使用长度为一的列表，更新受影响的当前配置和消费者，移除旧活动字段与过时入口，不增加兼容回退。

现有 seed 与 budget 维度继续工作，Selector 与下游方法的训练 seed 仍按批次配对，不互相交叉。将 extension v2 的三份表整合为一份表时保留其原有条件和新增 selector 意图；不得隐式改变任何 split、训练参数或算法。

### 核心验收

1. 一份表引用至少两个不同 Dataset/Split，配置展开数量符合五维笛卡尔积，数据集顺序/名称/指纹在每个 cell 和汇总中可追溯，单数据集列表同样成立。
2. 同一数据集的有效计算身份不因放入多数据集表、改变表名、增加或重排另一数据集而变化。CPU 冷/热实际消费者验证 Score、Selection、Output 的 MISS/HIT 与 producer_called；只改变一个数据集的 split 时不得跨数据集错误 HIT，另一个未变数据集应保持可复用。
3. 用至少两个独立、可丢弃 CPU 数据集走普通入口的选择、下游执行、指标与项目侧 SyncMate 产物声明/收集验收链；核对实际 mask、cell 身份、文件数量、路径、哈希及结果归属。缺失、重复或错误归属的产物必须被拒绝。模拟或 dry-run 不能冒充远端正式实验。
4. 三数据集 extension 对照的预期规模为 3 datasets × 10 selectors × 1 Retrain × 3 seeds × 4 ratios = 360 条件，其中保留原有 288 条件并增加 72 条件。在相关公共 selector 已固定的前提下用统一表完成 dry-run；本 Block 不执行这 360 条件的科研矩阵。
5. 提供一份可读的合并 YAML 和简短验收报告，用户能确认矩阵、每个 dataset 的 split、执行边界及增量/HIT 证据。完成候选后由用户决定接受或返工。

## Execution contract

Execution topology: `parallel`
> Apply target ref：`refs/heads/main`


> Git baseline：`c08a9e945ede7074083c91338f99825db6ec294a`

> Source branch：`refs/heads/codex/aagu-035-multi-dataset-matrix`

> Remote target：`origin refs/heads/main`
- Acceptance Route: `practical`
- Primary surface: integration / data / configuration contract
- Minimum real evidence: 独立 CPU 多数据集真实消费者的冷/热运行、选择到下游执行及产物验收；统一表的可读 dry-run；原数据集计算身份保持和错误数据绑定拒绝的检查。
- Decision owner: 用户。
- Report size: 简短 Markdown 报告，附实际结果和核验入口；不得以测试通过代替科研效果结论。
- Topology reason: 作为独立的公共矩阵能力，在 linked worktree 内形成候选，与当前 selector 配置审阅和已有实验结果保持明确责任边界。分支、路径和 owner 由后续 Claim 决定。

## Source and baseline

- Source anchor: 当前任务中用户对“一表只能绑定一个 dataset_ref”的设计反馈，以及明确指令“这部分可以建一个 block 吧”。
- 已检查的本地 Apply 目标为 `refs/heads/main`；注册时基础提交为 `a20ff808fd240b4954102f0b91bcdf9228dd8a23`。后续执行必须重新读取最新事实。
- 当前入口：`experiments/run.py`、`experiments/modular_config.py`、`experiments/modular_run.py`；矩阵现有维度是 selector、下游方法、seed、budget。
- 相关边界：`scripts/syncmate/opengu_recipes.py`、`scripts/syncmate/opengu_layout.py`、项目验收消费者与现有配置/消费者测试。优先在 OpenGU 的适配层完成，不能推定需要修改独立 SyncMate Core 仓库。
- 配置来源：`experiments/configs/aagu032_extend/` 与本任务新建的 `experiments/configs/aagu032_extend_v2/`。后者和 SGC 两次传播修改在注册时尚未提交，属于已有独立工作；本 Block 不擅自提交、撤回或吞并。使用这些配置前先核对其已固定版本。
- 核心数据要求仍为 Cora/CiteSeer/PubMed、70/10/20、split seed 2024；改变训练 seed 不重新划分数据。
- 未建立新的 Block 图关系；不从名称相似推断 depends_on，也不复制 dashboard 的旧状态。

## Scope and non-goals

范围包括统一多数据集配置协议及其直接消费者、身份/布局/汇总与项目侧 SyncMate 接缝、必要的活动配置更新、针对性验证和使用说明。

不包含 SGC 网络深度或 GT-full 数学实现修改，不调整学习率、求逆参数、候选池、数据比例或指标含义；不重建、下载或清除正式数据与缓存；不改变现行缓存清理政策或正式运行的版本约束；不运行完整正式 GPU 科研矩阵，不代替科研验收。历史不可变 Artifact 与已回传结果不得重写。

## Registration and continuation boundary

2026-09-08：按用户明确注册授权形成并登记本 Block。当前仅注册，未 Claim、未实施本 Block，未创建任务，未执行远端操作。

后续使用 `block-workflow` 读取本 locator、最新项目指令和仓库事实，Claim 同一 Block 后实施。保持已确认的 practical 路线，完成候选与验证后停在用户验收边界；注册本身不授权合并、安装、推送或正式实验运行。
