# Cache/Results 审计与清理明细（迁移归档）

来源：`CRITICAL_BUG_REPORT_20260227.md` 的历史审计明细（2026-02-27）。

## 1) 审计工具：Ultimate Audit V3 (`final_boss_cleanup.py`)

为彻底根除僵尸数据，审计脚本包含以下机制：
- 递归扫描 JSON 任意嵌套（如 `results -> method -> results -> strategy`）。
- 双重策略：
  - 单项删除（Purge）：对 `cache/`, `baseline/`, `experiments/` 下单次运行记录执行物理删除，触发后续 `--repair` 补齐。
  - 汇总标记（Mark）：对 `step0_validation/` / `evaluation/` 汇总表打失效标记（`is_corrupted`, `corruption_note`）。
- 判定阈值：`abs(a - b) < 1e-12` 视为零变动。

## 2) 审计处理结果（历史记录）

基于对 `results/` 目录 1900+ JSON 的扫描：

### A. 物理删除项（Leaf Results，85+）
- Collateral：GIF (76), GraphEraser (5), IDEA/MEGU (9) 等。
- Relative：GNNDelete 在 Citeseer 的全 seed 坏数据 (5)。
- Result Cache：16 个失效 MD5 缓存 JSON。
- 单项补全：`mg0_completion` 下 2 个坏 JSON（由加载路径缺陷产生）。

### B. 失效标记项（Summary Tables）
- `results/evaluation/step0/all_metrics_detailed.json`
- `results/step0_validation/all_metrics_detailed.json`
- `results/step0_validation/cross_dataset_results.json`
- `results/step0_validation/round2_results.json`

该文件仅作为历史归档，不再参与主报告叙事。
