# Work Plan Agent Guide

- 本目录是实验过程权威，Block生命周期不决定实验进度。
- 实验执行、重跑或分析先读取目标 experiments/AAGU-NNN.json，再按 RUNBOOK.md；不Claim一个纯实验Block。
- 只读取目标实验明确引用的Block，不扫描全体WorkItems，不改写其状态、graph或Claim。
- 所有状态声明绑定证据和范围。原始结果、科学解释与用户接受分开维护。
- 更新当前记录、追加history后重建；HTML/SVG禁止手改。参数只在正式YAML拥有，不复制参数树。
- README.md拥有字段与维护命令；MIGRATION.md解释旧混合记录的剩余交接边界。
