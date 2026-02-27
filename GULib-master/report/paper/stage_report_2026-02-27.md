# OpenGU 项目阶段报告（截至 2026-02-27）

## 1. 报告范围

本报告面向“整个项目阶段进展”，覆盖以下证据源：

- `scripts/evaluation/exp_status_checker.py`（进度核查逻辑）
- `self/generalization_experiment_checklist.md`（实验清单与阶段结论）
- `results/experiments/auto_discovered.json`（自动发现 runs 汇总，2026-02-27 11:10 更新）
- `results/paper_figures/`（论文图表产出）
- `report/paper/sections/`（论文草稿与统计表）

## 2. 全局进度总览（实验执行）

依据 `exp_status_checker.py` 扫描结果（质量过滤开启，5-seed 口径）：

- 总发现 runs：`950`
- 阶段覆盖：`7/7` 阶段达到 `100%`

分阶段统计（来自 `results/experiments/auto_discovered.json`）：

| 阶段 | 已发现 runs |
|---|---:|
| mg0 | 90 |
| mg1 | 90 |
| mg2 | 90 |
| mg3_citeseer | 40 |
| mg3_gat | 40 |
| ratio_sensitivity | 240 |
| p2_ext_GAT + p2_ext_GCN + p2_ext_GIN | 360 |
| **总计** | **950** |

## 3. 评估与图表产出状态

### 3.1 评估结果资产

- `results/relative/`：已生成大量非空结果（当前扫描到 `341` 个非空 JSON）。
- `results/collateral/`：已生成 `1880` 条结果记录（含多方法/多配置）。
- `exp_status_checker` 覆盖表中，主配置 `Rel/Col` seed 覆盖均满足 `5/5`。

### 3.2 论文图表资产

`results/paper_figures/` 已产出 5 张主图（含 PDF+PNG）：

- `FIG-1_Generalization`
- `FIG-2_Scaling`
- `FIG-3_Spectrum`
- `FIG-4_Significance`
- `FIG-5_Collateral`

最新写入时间集中在 `2026-02-27 11:01`，说明图表批次已完成一次统一导出。

### 3.3 论文文本资产

`report/paper/sections/` 中已具备关键草稿：

- `abstract.md`（摘要草稿）
- `paper_analysis.md`（主分析与叙事骨架）
- `cross_seed_tables.md`（跨 seed 统计表）

## 4. 当前阶段结论（基于已有文档汇总）

依据 `self/generalization_experiment_checklist.md` 与论文草稿，当前叙事主线已形成：

- 存在跨方法族的脆弱性差异（Learning-based / IF-based / Shard-based）。
- Ratio 敏感性、多 seed 稳定性与跨模型/跨数据集材料已具备主体证据。
- Relative 指标、Collateral 指标与显著性图表均已有对应产物与写作入口。

## 5. 从 `paper_analysis.md` 可并入的深度要点

1. **GNNDelete 高脆弱 + 高 collateral 已有强证据**
   - ratio=`0.01` 下已观察到显著性能与近似误差放大（`gap_pct` 可达 20%+，并伴随较高 `fraction_flipped`）。
   - 对应 `paper_analysis.md` 的 C1/C2 与 §5.2 叙事，可直接并入阶段汇报正文。

2. **“方法族差异”叙事已成型**
   - Learning-based（GNNDelete）显著脆弱、IF-based（GIF）相对稳健、Shard-based（GraphEraser）存在保护效应。
   - 可直接复用 `paper_analysis.md` 的 H1/H2/H3 对照逻辑，形成“机制-证据”闭环。

3. **Relative 指标必要性已被理论化**
   - `paper_analysis.md` 与 `visualization_plan.md` 都支持：`k=5 random baseline` 能剥离方法自身偏移，避免误读 GraphEraser 的“天然增益”。

4. **IM v4 工程收益可作为方法贡献点**
   - `18.9s vs 653s`（约 `34.6x`）且 spread 损失约 `1.3%`，可作为“可落地攻击框架”的工程证据。

## 6. 已识别问题与审稿风险（合并版）

1. **MIA 证据仍不完整**
   - `paper_analysis.md` 明确标注 `[待补充]`：需要补 `attack/MIA_attack.py` 的系统结果。

2. **外推范围仍偏窄**
   - 主要集中在 `cora/citeseer`，对更大图与更多场景的可迁移性证据不足。

3. **部分机制解释仍需最小验证实验**
   - 例如 GNNDelete 的 DEC/NI 分解、GIF 在更复杂模型上的边界验证，目前在文稿中仍属待补。

4. **环境可复现性小问题**
   - 本地直接运行 `exp_status_checker.py` 依赖 `numpy`，新环境下“一键复查”仍可能阻塞。

## 7. 下一阶段建议（按优先级）

1. 先补齐 `MIA` 最小闭环（至少覆盖 `GNNDelete + GIF`、`im_v4 + random` 对照）。
2. 将 `paper_analysis.md` 的 H1–H3 对照表裁剪进阶段报告主文，统一“结论口径”。
3. 对 `results/paper_figures` 与 `report/paper/sections` 做一次图号/字段/caption 一致性检查。
4. 固化评估依赖（至少补充 `numpy`）以保证状态脚本可直接运行。

## 8. ECCV 关联与补实验方向

1. **CV 关联定位**：将当前工作定位为“图结构视觉系统中的 unlearning 安全审计框架”，场景可对接 scene graph / skeleton / point cloud。
2. **当前缺口**：缺少 CV 数据集定量结果与可视化案例，ECCV 证据链尚不闭环。
3. **最小补充包**：优先补 `1` 个 scene-graph 类数据集，至少跑 `GNNDelete + GIF` 与 `random/tracin/im_v4`，并补 `MIA + qualitative`。
4. **时间预估**：若要对齐 ECCV 口径，建议按 `2-3` 周准备一个最小 CV proof-of-concept 批次。

---

报告生成时间：2026-02-27  
报告位置：`report/paper/stage_report_2026-02-27.md`
