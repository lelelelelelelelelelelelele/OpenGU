# Results 目录指导说明（含架构）

## 1. 目录目标

`results/` 用于存放实验输出、缓存、验证产物与研究日志。  
这里是“产物层”，不是核心代码层。

## 2. 当前架构（2026-02-22 快照）

```text
results/
├─ experiments/            # 泛化实验主结果（mg0/mg1/mg2/mg3）
│  ├─ _archive/            # 已归档的旧批次（保留可追溯性）
│  ├─ mg0_completion/
│  ├─ mg1_citeseer/
│  ├─ mg2_gat/
│  ├─ mg3_citeseer/
│  └─ mg3_gat/
├─ cache/                  # ResultCache（哈希键命名，按配置缓存结果）
├─ selection_cache/        # SelectionCache（选点缓存，跨方法复用）
├─ collateral/             # collateral damage 评估结果
├─ step0_validation/       # step0 历史只读结果
├─ evaluation/             # 统一评估产物（由 scripts/evaluation 生成）
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

## 6. 今日整理动作（已执行）

- 已将 `mg1_citeseer` 的旧重复批次归档到：
  - `results/experiments/_archive/mg1_citeseer/phase_a/`
- 当前 `mg1_citeseer/phase_a` 仅保留每个 seed 的最新完整批次（5 个 seed）。
- 已将历史目录归档到：
  - `results/experiments/_archive/phase_a/`
  - `results/experiments/_archive/tracin_fix_phase_a/`
  - `results/experiments/_archive/phase_a_v2_tracin_fix/`

## 7. 维护规则（建议长期执行）

- 保持写入路径稳定，不要改动 `results/cache` 与 `results/selection_cache` 目录名。
- 对同一实验组同一 seed 的重复批次：
  - 保留最新且 `completed==total_experiments` 的目录。
  - 旧目录移动到 `results/experiments/_archive/...`，不要直接删除。
- `_archive/phase_a*` 与 `_archive/tracin_fix_phase_a` 属历史对照数据，优先”冻结”而非重排。
- 报告类目录（`_journal`）保持 append-only。checkpoint_report 已移至 `report/progress/`。
- `results/step0_validation` 视为历史冻结目录，不再写入新运行结果。
- 新 Step0 产物写入 `results/evaluation/step0`，攻击图产物写入 `results/evaluation/attack`。

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

## 9. 当前数据量快照（2026-02-22）

- `results/experiments`: 198 files, ~12.93 MB
- `results/step0_validation`: 278 files, ~7.42 MB
- `results/cache`: 483 json, ~3.48 MB
- `results/selection_cache`: 84 json, ~0.18 MB
- `report/progress/2026-02-19_checkpoint`: 7 files, ~0.54 MB (已迁移)

说明：当前 cache/selection_cache 文件均可解析，未发现坏文件。
