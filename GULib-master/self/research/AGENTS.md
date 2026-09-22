# Work Plan Agent Guide

- 本目录是实验过程权威，Block生命周期不决定实验进度。
- 实验执行、重跑或分析先读取目标 experiments/AAGU-NNN.json，再按 RUNBOOK.md；不Claim一个纯实验Block。
- 只读取目标实验明确引用的Block，不扫描全体WorkItems，不改写其状态、graph或Claim。
- 所有状态声明绑定证据和范围。原始结果、科学解释与用户接受分开维护。
- 更新当前记录、追加history后重建；HTML/SVG禁止手改。参数只在正式YAML拥有，不复制参数树。
- README.md拥有字段与维护命令；MIGRATION.md解释旧混合记录的剩余交接边界。

- experiments/ 是持续维护、Git 忽略的状态目录；更新运行进度不得 commit，不要求三端为状态变动同步。不要删除状态文件或把它当作可再生缓存。
- analysis/decision 只在 Git 跟踪的 analyses/AAGU-NNN.json 维护；运行前同时读取对应已保存分析（如有），但不得用历史分析恢复或猜测当前状态。
- 完成分析后才显式提交对应分析记录和报告，绑定原运行 SHA；进度/草稿留在忽略目录。提交不等于科学接受，下次正式运行前重新同步三端，活跃任务不切换 SSH checkout。
