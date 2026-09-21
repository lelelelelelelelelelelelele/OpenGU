# 实验运行流程

## 1. 从实验记录开始

读取 self/research/experiments/AAGU-NNN.json 的当前范围、配置、阶段、依赖和下一步。运行、重跑、补算、分析都更新同一个实验记录；不为纯运行创建Block或Claim。先明确本次是新尝试、恢复、指标重算还是纯分析，避免已完成证据被重复生产。

## 2. 核对准备条件

读取 experiments/AGENTS.md 与当前launcher的相邻说明。复用仍有效的gate；核对代码版本、数据与split、固定参数、已有结果、共享运行条件和本实验preflight。被Block阻塞时只检查其明确交付；已接受但尚未落地执行基线也不能启动。代码或定义需改变时，由对应Block交付后回到实验。

当前正式SSH版本、数据根和GPU要求仍以 experiments/AGENTS.md 为准。设备不满足就记录原因；不能降级CPU或自动改数据、预算、参数。

## 3. 通过已有 SyncMate 入口提交

选择已注册的recipe与运行节点，使用SyncMate“运行与回传”前端的检查就绪、提交运行。Agent需要命令行时读取 scripts/syncmate/README.md 与已安装CLI的 --help，按其中当前run/handoff/runner-agent提交接口操作，不从历史示例猜测调用参数。

SyncMate已有 runbook、checklist 和 handoff 命令。它们提供设备级操作指导，本文件提供实验级统一流程。当前配方仍在 scripts/syncmate/opengu_recipes.py；独立recipe YAML改造归AAGU-071，在它实际交付前不得使用假定的新接口，也不将071设为所有既有实验的阻塞。

提交后把实际 job_id、run_id、代码版本、配置入口、范围及handoff/回执引用追加到该实验 attempts 和 history。提交中断时先找回原请求；running时不自动重试。需要重跑时新增运行身份并明确retry_of和原因，不覆盖旧attempt。

## 4. 监控与回传

运行过程由SyncMate观察，Work Plan只保存已确认的阶段事实与最新观察日期。进程done不代表回传或可信校验完成。沿用现有链：完成运行 → 收集 → SHA-256校验 → 可信索引 → 项目结果检查。

需要排查精确阶段或缓存事件时再读取SSH AutoReport。无需把日志全文复制进Work Plan。运行失败、部分完成、输入缺失分别记录，恢复按已有重跑与缓存修复Runbook确认范围。

## 5. 分析与科学决定

分析绑定具体运行/配置范围及报告，明确哪些结果被采用或排除。可先分析可信子集；不能把部分分析显示成全矩阵完成。记录计算或缓存命中、结果身份正确、结论支持范围三类事实。用户接受的是明确结论范围，不从Block accepted、校验PASS或程序退出推断。

## 6. 更新总表

更新实验阶段与下一步，追加有证据的history事件，再运行 README.md 中的生成和检查命令。实验依赖及Block阻塞在前端可见；它们不会改变原Block，也不会自动提交下一项实验。
