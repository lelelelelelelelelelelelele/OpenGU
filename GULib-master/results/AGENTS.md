# results/ Agent Guide

> 本文件递归约束 `results/`。这里是 SSH 回传实验产物在本地的落地、核验、组织和归档区域，不是正式实验执行或远端修复入口。

## 1. 职责边界

- `results/` 管理已经回传到本地的实验产物及其可追溯组织；实验定义、运行身份和正式 launcher 由注册计划与 `experiments/AGENTS.md` 拥有。
- 收到文件不等于证据被接受。只有完成来源核对、SHA-256 校验并进入 SyncMate trusted index 的产物，才能进入可信结果表、aggregate、报告或研究结论。
- SSH 上的代码修改、Cache/Artifact 失效、结果隔离、删除和重跑不由本目录决定或执行。

## 2. 修复与回传路由

发现 Selection/selector 或 GU method 缺陷时，先由[重跑与缓存修复 Runbook](../文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md)判断修复链、失效范围和证据边界。

范围确认后，机器端操作才进入 [OpenGU machine repair Runbook](../scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md)；结果回传、校验和 trusted-index 规则由 `scripts/syncmate/AGENTS.md` 与其 README 拥有。不要在 `results/` 内另写一套远端命令、Cache key 或修复协议。

## 3. 本地证据状态

- 回传落地文件、checksum-accepted trusted state、可信结果表和派生投影是不同层级；不得把未核验文件直接当作可信输入。
- 保留产物自身的 metadata、完整 Git SHA、配置或 Recipe 身份、目录归属和校验链；不得通过手工改名、覆盖或补写内容来制造一致性。
- `done`、进程成功退出、文件存在或报告已生成都不能替代完整性与 provenance 验证。
- Cache V2 Artifact、append-only audit facts 和 generator-owned outputs 继续服从根级规则；修改 producer 或 generator 后重建，不手改派生文件。

## 4. 整理与归档

- 整理只改变本地的可读组织，不改变实验身份、可信状态或远端事实。存在正式消费者的路径不得为了“更整齐”而擅自移动。
- 归档前必须明确批次、来源、身份、校验状态、引用者和可恢复位置；历史对照数据默认冻结，不能从“看起来过时”推断为可删除。
- 冲突、partial、stale、corrupt、孤儿文件或身份不明内容先隔离并记录，不自动合并、覆盖、修补或清空。
- 任何删除、批量移动或覆盖都需要当前任务的明确授权和已核对的精确目标；正式修复仍回到第 2 节的决策链。

## 5. 验证与交接

使用 SyncMate 拥有的 collection、verify、index、trace 和 gate 契约验证回传内容，不在此复制具体命令。交接时分别说明：

1. 哪些文件已落地；
2. 哪些已通过 checksum 与 trusted-index 验证；
3. 哪些 aggregate 或报告由可信输入生成；
4. 哪些仍未验证、被隔离或阻塞。

本地归档完成不代表 SSH 端内容可以删除；远端清理必须由已确认的修复范围和机器 Runbook 单独授权。
