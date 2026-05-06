# Evaluation Tools

> **2026-05-06**: 移除了 `gen_md_report.py` (v1)、`sync_random_data.py`、
> `stat_analyzer_v2.py`、`full_results_audit.py`、`HOWTO_REPAIR_CORRUPTED_RESULTS.md`，
> 并对 `final_data_aggregator.py` 与 `exp_status_checker.py` 加了 STALE 守卫
> （读 `results/relative/`、`results/collateral/`、`results/experiments/`，三者
> 自 2026-05-05 起被 .gitignore 为 bug-polluted）。Phase B 用 `experiments/run.py`
> + `scripts/gate_runs.py` 的组合替代 Step0/Step1 流程。

## 仍在用

| 模块 | 用途 |
|---|---|
| `scripts.evaluation.reporting.writer` | `demo_attack.py` / `eval_collateral.py` 跑完后自动追加 `results/_journal/auto_report.md`（参 CLAUDE.md research-journal 节） |
| `scripts.evaluation.metrics.*` | 测试间复用的指标计算（`tests/test_attack_charts.py` 在用） |
| `scripts.evaluation.plotting.*` | Step0 老图复用（`tests/test_step0_extractor.py`） |
| `gen_md_report_v2.py` | 读 `results/evaluation/stats/final_paper_stats.csv` 出论文表格到 `report/paper/sections/cross_seed_tables.md`（CLAUDE.md 引用） |

## 守卫态（带 STALE header，运行会拒绝）

| 模块 | 现状 |
|---|---|
| `final_data_aggregator.py` | 读 3 个 gitignored 旧目录；Phase B 用之前必须重写为 walk `results/runs/{cell}/{method}_{strategy}/seed{N}/` |
| `exp_status_checker.py` | 同上；想看 Phase B 进度直接 `python scripts/gate_runs.py results/runs/<cell>` |

强制跑（仅在还有 legacy 数据的机器上）：`ALLOW_LEGACY_AGGREGATOR=1` / `ALLOW_LEGACY_PLOT=1`。

## CLI 入口（仍存活，但所指向的 Step0 流程已是 pre-Phase-B 历史）

```bash
H:/conda_package/envs/gnn/python.exe -m scripts.evaluation --help
```

`extract / plot / report / all` 子命令本身是好的，但默认输入路径
（`results/step0_validation/...`）是 Step0 的，现在没人在跑 Step0。
保留是为了 `tests/test_step0_extractor.py` 的回归保护。
