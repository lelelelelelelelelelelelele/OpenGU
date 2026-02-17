# Round0 阶段性报告（基于当前已有结果）

- 生成时间：2026-02-17 13:04:29
- 评估范围：不新增运行，只分析现有 `results/step0_validation/cross_dataset_results.json` 与日志产物

## 1) 覆盖度与完整性

- 目标组合数：`3 datasets × 10 methods × 7 ratios = 210`
- `cross_dataset_results.json` 实际记录：`210`（缺失 `0`）
- 状态分布：
  - `SKIP`: 193
  - `X`: 16
  - `TIMEOUT`: 1
- 可用覆盖率（`OK/SKIP` 视为可用）：`193 / 210 = 91.9%`

## 2) 分数据集健康度

- `cora`: 70 条（`SKIP=69, X=1`）
- `citeseer`: 70 条（`SKIP=69, X=1`）
- `pubmed`: 70 条（`SKIP=55, X=14, TIMEOUT=1`）

结论：主要风险集中在 `pubmed`。

## 3) 分方法稳定性

- 全覆盖稳定（`21/21` 可用）：`GraphEraser, GIF, GUIDE, MEGU, D2DGN, IDEA, GraphRevoker`
- 部分失败：
  - `SGU`: `20/21`（`pubmed@0.5` 失败）
  - `GUKD`: `14/21`（`pubmed` 全比例失败）
  - `GNNDelete`: `12/21`（`pubmed` 全比例失败，且 `cora/citeseer@0.5` 失败）

## 4) 当前失败清单（17项）

- `cora / GNNDelete / 0.5` → `MIA_LENGTH_MISMATCH`
- `citeseer / GNNDelete / 0.5` → `MIA_LENGTH_MISMATCH`
- `pubmed / GNNDelete / 0.005` → `TIMEOUT`
- `pubmed / GNNDelete / 0.01` → `OSError`
- `pubmed / GNNDelete / 0.02` → `OSError`
- `pubmed / GNNDelete / 0.05` → `OSError`
- `pubmed / GNNDelete / 0.1` → `OSError`
- `pubmed / GNNDelete / 0.2` → `OSError`
- `pubmed / GNNDelete / 0.5` → `OSError`
- `pubmed / SGU / 0.5` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.005` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.01` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.02` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.05` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.1` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.2` → `RETURN_CODE_NONZERO`
- `pubmed / GUKD / 0.5` → `RETURN_CODE_NONZERO`

## 5) 日志产物现状

- `results/step0_validation/cross_logs/cora`: 11
- `results/step0_validation/cross_logs/citeseer`: 70
- `results/step0_validation/cross_logs/pubmed`: 70
- 历史补充目录：
  - `results/step0_validation/round1_logs`: 15
  - `results/step0_validation/round2_logs`: 64
  - `results/step0_validation/ratio05_logs`: 9

说明：`cora` 的大量 `SKIP` 来自严格 OK 的历史日志复用（脚本搜索了上述补充目录）。

## 6) 结论：是否需要“完整分析”？

结论分两层：

1. 是否足以支撑“后续实验启动”：
- **足够**（可用覆盖率 91.9%，且有 7 个方法全覆盖稳定），可以进入下一阶段实验设计/攻击验证。

2. 是否足以支撑“完整分析与最终结论”：
- **暂不足够**。原因：
  - 仍有 17 个失败点，且集中在 `pubmed` 的关键方法（`GNNDelete/GUKD/SGU`）。
  - 当前结果主要是运行健康度验证，不等同于完整论文级分析。
  - 若按你当前研究目标（强调 `Unlearn vs Retrain-after-deletion` 的 attribution / approximation gap），还缺少系统化的 retrain 对照结果。

## 7) 建议（阶段决策）

- 推荐策略：**先不做完整分析**，先进入后续实验，但以 7 个稳定方法为主线推进；并将失败方法作为并行修复分支处理。
- 触发“完整分析”的门槛建议：
  - 失败组合降到接近 0（至少补齐 `pubmed` 上的 `GNNDelete/GUKD/SGU`）。
  - 补齐 retrain-after-deletion 对照，并可计算 approximation gap。
