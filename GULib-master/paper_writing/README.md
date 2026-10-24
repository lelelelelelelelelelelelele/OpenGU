# WWW27 本地写作工作区

本目录用于提纲审查、证据修复和后续论文写作。2026-10-24：详细提纲v6已纳入正式EXP-084重算，保留摘要、八章正文及附录的段落层级。旧GNNDelete输出继续隔离；新十seed顺序交叉为待五新seed确认与解释控制的候选发现。第一版科研正文须等有效证据包经理论、实验、分析三类复审均达到Weak Accept或以上，并由主审认可后才开始，当前门槛未达到。

- [OUTLINE.md](outline/OUTLINE.md)：本轮待审提纲的可编辑源文件；每段列目标、写法与关键边界，每幅主图列内容、布局和caption要素。
- [OUTLINE.html](outline/OUTLINE.html)：由同一提纲生成的阅读版。
- [第三轮执行协议](protocol/ROUND3_EXECUTION_PROTOCOL.html)：固定范围、判断与停止规则、A/B分支和正式写作门槛；[可编辑源](protocol/ROUND3_EXECUTION_PROTOCOL.md)。
- [第三轮执行报告](review/2026-10-24-round3/REPORT.html)：实际完成的CPU分析／代码验证、正式GPU执行状态、预算和下一步；[可编辑源](review/2026-10-24-round3/REPORT.md)。
- [第二轮审查与处置](review/2026-10-24-round2/REPORT.html)：当前判断、三份独立模拟审稿、20项意见处置及恢复证据的最小路径；[可编辑源](review/2026-10-24-round2/REPORT.md)。
- [第一轮提纲自审报告](review/2026-10-24-self-audit/REPORT.html)：理解修正、完整实验层次、新CPU分析与Weak Accept补强判断；[可编辑源](review/2026-10-24-self-audit/REPORT.md)。
- [最小补强验证方案](review/2026-10-24-self-audit/VALIDATION_PLAN.html)：第一轮114引用规格，尚未执行；A组受影响GU暂停，B组54引用可优先推进，当前分支以第二轮报告为准。
- [LaTeX 环境与验证说明](latex/ENVIRONMENT.md)：实际工具链、Overleaf模板来源、构建命令与验证结果。
- [本地模板入口](latex/main.tex)：ACM匿名双栏环境自检；当前内容不作为第一版论文正文。

已有云端稿件的同步副本位于 [report/paper/overleaf](../report/paper/overleaf/main.tex)，来源和哈希见 [同步清单](../output/paper-review-20261024/sync-manifest.json)。本轮模板验证与未来新稿在独立的 `latex/` 项目准备，避免把环境自检混进已有云端稿件。

写作门槛通过后，按提纲中“主张—证据批次—图表—反例—范围”的对应关系准备第一稿。当前实验状态和科学决定仍由 `self/research/` 对应记录维护；写作文件不替代实验台账。

在仓库根目录重建提纲和环境说明的HTML：

```powershell
./paper_writing/tools/render-docs.ps1
```

只重建提纲：

```powershell
./paper_writing/tools/render-docs.ps1 -SourcePaths outline/OUTLINE.md
```

渲染脚本使用本机PowerShell 7内置的Markdown转换器，不增加Node/Python包。LaTeX构建命令及输出位置见环境说明。
