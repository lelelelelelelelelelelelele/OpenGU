# AAGU-005 修复验证

产品检查点：`f7956bb994b20b629b60e8f1a4da20fc78ea6b88`。完整测试对应同一产品文件；提交后只更新 item 证据、报告、WorkItem 与看板，没有算法、配置或测试变化。最终 HEAD 与实际差异在本 linked worktree `.workblock/runtime/aagu005-report-qa/final-candidate.md` 读回。

| 人的问题 | 实际观察 | 判断 |
|---|---|---|
| 原来 20 个 GU 配方还会漏掉 Retrain 或要求旧文件吗 | 注册清单直接消费执行器枚举，20/20 相等；每个 gate 8 文件，每个 stage 136 文件 | PASS |
| 预检是否拿到正确参数和配置 | 20 个真实 stage 预检调用收到 ratio/config/gate 标志；当前正式 YAML 摘要匹配；3 个 seed 下配方方法条件与真实矩阵消费者相等 | PASS，仅证明代码传播，设备/数据边界被隔离 |
| 新格式能不能被真正收集并消费 | 临时 CPU 图真实运行 GNNDelete 与 Retrain，使用真实 Git runner、Core local transport、文件收集、SHA 校验、trusted index、OpenGU 接受检查及结果表；gate/stage 路径均通过 | PASS |
| 是否会偷偷重训或依赖远端缓存 | 检查期间禁止模型 forward 与训练更新；collector 没有远端 Cache V2，源 Store 前后哈希一致；重复收集 fetched=0 | PASS |
| 坏结果会不会被放过 | 12 类错误均拒绝：缺少 Retrain、重复索引、未验证索引、Git 不符、字节损坏、Output 引用不符、指标不符、checkpoint 不符、Selection 不符、预测缺失、预测无效、方法参数不符 | PASS |
| 相关功能是否回归 | 311 passed、0 failure/error/skip；包括完整 SyncMate、基础/完整 Adapter、Core 依赖、原子 stage、target-direct stage、独立输出和本轮接入测试。CLI 编译与独立 smoke 通过 | PASS |
| 修复是否已经在远端 GPU 上执行 | 未新增 GPU 作业，SSH 主线仍是此前已落地 c9e094c5；新修复尚未合入或部署 | NOT OBSERVED / 尚未执行，符合当前代码验证范围 |

原始数据入口：`repair-tests.xml`、`repair-verification.json`、`repair-observations.json`。临时 CPU fixture 的候选数、预算与训练规模仅用于测试，未更改正式配置或形成新的正式实验结果。历史 `observations.json` 与 `verification.md` 保持为修复前证据。

报告由 `render_report.py` 成对生成；实际渲染和链接检查记录在本工作区 `.workblock/runtime/aagu005-report-qa/`。最终候选重建报告无差异、结构与看板检查通过后，沿用本 WorkItem 等待用户接受。

报告实际检查：1440×1000 桌面首屏与全页、390×844 窄屏已查看，标题、正文和决定区清楚；两个尺寸均无横向溢出、断图或无效证据链接，决定区均在首屏。7 项看板回归通过，投影由生成器重建。
