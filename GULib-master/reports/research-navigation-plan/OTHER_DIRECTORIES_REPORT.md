# 分析目录命名整理

2026-10-24 · 已完成目录移动与引用更新 · 空目录保留

分析目录按实验编号命名，内容主题与运行版本保留在报告标题、文件名和批次目录中。当前入口见 [Work Plan 说明](../../self/research/README.md)，研究问题与章节对应关系见[论文论证导航](../../../../OpenGU-DocMap/40_论文写作/40_论文写作.md#研究问题、分析与章节导航)。

| 原位置（相对 analyses/） | 当前位置 | 用途 |
|---|---|---|
| shard300-20261023/（此前已完成） | [EXP-011_EXP-079/](../../self/research/analyses/EXP-011_EXP-079/REPORT.html) | e11r1 / e79r6 联合分析；不替代旧版接受范围 |
| evidence/AAGU-032-AAGU-053-3000epoch-20260923/ | [EXP-032_EXP-053/](../../self/research/analyses/EXP-032_EXP-053/) | 3000 轮结果表、配对数据与复算脚本 |
| h64-theory-20260924/ | [EXP-067_EXP-068/](../../self/research/analyses/EXP-067_EXP-068/README.md) | H64 历史参数候选推导 |
| validation-20260924/analyze.py | [EXP-067_EXP-068/analyze.py](../../self/research/analyses/EXP-067_EXP-068/analyze.py) | 两项实验的共享验证分析脚本 |

已有单实验目录及其运行批次名称保留。EXP-079 的 e79r5、gate252 等批次和 EXP-080 的 full-20261021 继续区分证据范围。散落的历史分析文件名保留来源身份，其入口与相关引用已指向现行目录。

## 引用与状态

已更新 Work Plan 说明、涉及路径的分析记录、论文主页面、结果章、附录表格入口、导师报告和对应生成脚本。生成页面使用各自原生成器重建；032/053 目录变浅一级后，复算脚本的仓库根目录定位已同步修正。

H64 README 将候选推导阶段与后续验证明确分开。原始结果、运行身份、结论和接受范围保持原样；EXP-011/e11r1 与 EXP-079/e79r6 仍不因入口整理获得科学接受。历史收据、运行 ID 和旧核验快照保留原始出处，不把它们改写成新的执行记录。

## 核验

- 本次移动 28 个文件：23 个文件 SHA-256 完全一致；其余 5 个仅为 README 入口说明和分析脚本路径调整。
- 58 份分析与实验状态记录已比较：除目录引用替换外，JSON 内容一致。
- 18 份源文件与原文比较，仅替换路径；其中包括重新生成的 032/053 协议比较报告，科学正文未改变。
- 288 个本地文档链接全部存在；4 个迁移后的 Python 脚本语法检查通过，仓库根目录解析正确。
- Work Plan 的 36 个页面/SVG 已重建，并通过一致性及 1633 个来源引用检查。导师报告、结果章与论文阅读版也已通过各自生成器核验。

文件移动清单见 [other-directory-renames.json](other-directory-renames.json)，本次核验见 [other-directory-verification.json](other-directory-verification.json)。本次未启动实验、未重新计算科学分析。

`self/research/analyses/evidence/` 和 `self/research/analyses/validation-20260924/` 已核对为空目录，按用户要求保留。本次未执行删除，也未移入 rubbish。
