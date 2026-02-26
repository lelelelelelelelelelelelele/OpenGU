# Results 目录指导说明（含架构）

## 1. 目录目标

`results/` 用于存放实验输出、缓存、验证产物与研究日志。  
这里是“产物层”，不是核心代码层。

## 2. 当前架构（2026-02-27 快照）

```text
results/
├─ experiments/            # 泛化实验主结果
│  ├─ _archive/            # 已归档的旧批次（保留可追溯性）
│  ├─ mg0_completion/
│  ├─ mg1_citeseer/
│  ├─ mg2_gat/
│  ├─ mg3_citeseer/
│  ├─ mg3_gat/
│  ├─ p2_ext_gif_GAT/
│  ├─ p2_ext_gif_GCN/
│  ├─ p2_ext_gif_GIN/
│  ├─ im_v4_compare/
│  ├─ im_v4_probe/
│  └─ ratio_sensitivity/
├─ relative/               # 相对评估结果（相对 random baseline 的 F1 drop）
│  └─ {Method}/{Dataset}/{Model}/relative_seed{seed}_{timestamp}.json
├─ baseline/               # baseline 实验结果
├─ cache/                  # ResultCache（哈希键命名，按配置缓存结果）
├─ selection_cache/        # SelectionCache（选点缓存，跨方法复用）
├─ collateral/             # collateral damage 评估结果
├─ step0_validation/       # step0 历史只读结果
├─ evaluation/             # 统一评估产物（由 scripts/evaluation 生成）
│  ├─ step0/               # Step0 输出（日志、JSON、图表、报告）
│  ├─ attack/              # 攻击图表输入/输出
│  └─ stats/               # 聚合统计 CSV（final_paper_stats.csv 等）
├─ _journal/               # 自动研究日志（append-only）
└─ _deprecated_tracin_bug/ # 历史问题留档（已废弃）


## 3. 代码与产物边界

- `results/` 只存放数据与产物。
- Step0 评估工具代码已迁移到 `scripts/evaluation/`。
- 统一入口：`python -m scripts.evaluation --help`

## 4. 命名与数据模型

- 实验目录：`results/experiments/<group>/phase_a/<timestamp>_seed<seed>/`
- 单方法结果：`<Method>_<dataset>_<model>_r<ratio>_s<seed>.json`
- 批次汇总：`_summary.json`
- 错误日志：`*_error.log`
- 对比表：`_comparison_table.txt`

## 5. cache 与 selection_cache 的边界

- `results/cache/`
  - 由 `attack/result_cache.py` 维护。
  - 可删除（只影响速度，不影响可重跑性）。
  - 默认 key 包含：数据集、模型、方法、ratio、k、seed、strategy 等。
- `results/selection_cache/`
  - 由 `attack/selection_cache.py` 维护。
  - 主要复用 `random/pagerank/im` 选点结果。
  - 建议保留；丢失后可用 `scripts/tools/extract_selection_cache.py` 从历史结果重建。

## 6. 历史整理动作

### 2026-02-22

- 已将 `mg1_citeseer` 的旧重复批次归档到 `results/experiments/_archive/mg1_citeseer/phase_a/`
- 当前 `mg1_citeseer/phase_a` 仅保留每个 seed 的最新完整批次（5 个 seed）
- 已将历史目录归档到：
  - `results/experiments/_archive/phase_a/`
  - `results/experiments/_archive/tracin_fix_phase_a/`
  - `results/experiments/_archive/phase_a_v2_tracin_fix/`

### 2026-02-27

- 新增 `results/relative/` 目录，存放相对评估结果（由 `eval_relative.py` 生成）
- 新增 `results/evaluation/stats/final_paper_stats.csv`（由 `final_data_aggregator.py` 聚合生成）
- 新增 experiments 子组：`p2_ext_gif_*`, `im_v4_*`, `ratio_sensitivity`

## 7. 维护规则（建议长期执行）

- 保持写入路径稳定，不要改动 `results/cache` 与 `results/selection_cache` 目录名。
- 对同一实验组同一 seed 的重复批次：
  - 保留最新且 `completed==total_experiments` 的目录。
  - 旧目录移动到 `results/experiments/_archive/...`，不要直接删除。
- `_archive/phase_a*` 与 `_archive/tracin_fix_phase_a` 属历史对照数据，优先”冻结”而非重排。
- 报告类目录（`_journal`）保持 append-only。checkpoint_report 已移至 `report/progress/`。
- `results/step0_validation` 视为历史冻结目录，不再写入新运行结果。
- 新 Step0 产物写入 `results/evaluation/step0`，攻击图产物写入 `results/evaluation/attack`。
- 聚合统计 CSV 写入 `results/evaluation/stats/`（由 `scripts/evaluation/final_data_aggregator.py` 生成）。
- 相对评估结果写入 `results/relative/{Method}/{Dataset}/{Model}/`（由 `eval_relative.py` 生成）。

## 8. 常用检查命令

```powershell
# 查看 experiments 下每组 seed 重复情况
@'
from pathlib import Path
import re
root = Path("results/experiments")
for g in sorted([p for p in root.iterdir() if p.is_dir()]):
    runs = [d for d in g.rglob("*") if d.is_dir() and re.search(r"seed\d+$", d.name)]
    if not runs:
        continue
    by = {}
    for d in runs:
        s = re.search(r"seed(\d+)$", d.name).group(1)
        by[s] = by.get(s, 0) + 1
    dup = sum(v > 1 for v in by.values())
    print(g.name, "runs=", len(runs), "dup_seed_groups=", dup)
'@ | python -

# 统计 cache 与 selection_cache 文件数
(Get-ChildItem results/cache -File *.json).Count
(Get-ChildItem results/selection_cache -File *.json).Count
```

## 9. 数据流水线（实验结果 → 论文表格）

| 阶段 | 工具 | 输入 | 输出 |
|------|------|------|------|
| 1. 原始实验 | `main.py` | CLI 参数 | `experiments/{group}/phase_a/` (JSON per seed) |
| 2. 相对评估 | `eval_relative.py` | experiments JSON + random baseline | `relative/{Method}/{Dataset}/{Model}/` |
| 3. 附带损伤 | `eval_collateral.py` | experiments JSON + retrain 结果 | `collateral/{Method}/{Dataset}/{Model}/` |
| 4. 聚合统计 | `scripts/evaluation/final_data_aggregator.py` | relative/ + collateral/ + experiments/ | `evaluation/stats/final_paper_stats.csv` |
| 5. 生成表格 | `scripts/evaluation/gen_md_report_v2.py` | final_paper_stats.csv | `report/paper/sections/cross_seed_tables.md` |

## 10. 当前数据量快照（2026-02-27）

- `results/experiments`: 341 files, ~31 MB
- `results/step0_validation`: 271 files, ~7.9 MB
- `results/cache`: 1148 json, ~12 MB
- `results/selection_cache`: 297 json, ~2.2 MB
- `results/relative`: 162 files, ~674 KB
- `results/collateral`: 266 files, ~1.1 MB
- `results/evaluation/stats`: 9 files, ~49 KB

说明：当前 cache/selection_cache 文件均可解析，未发现坏文件。
