# Config Inventory 仪表盘 — 验收报告

> **FROZEN HISTORICAL SNAPSHOT（2026-06-30）**：本报告保留当日 F4 验收事实，不再代表当前 GraphRevoker 状态。2026-07-20 起，dashboard 明确区分 `local usable`、`accepted remote / archive pending` 与 `rerun`；GraphRevoker 当前边界见 [`docs/graphrevoker_e4_ACCEPTANCE_REPORT.md`](../../docs/graphrevoker_e4_ACCEPTANCE_REPORT.md)。

> 验收对象：[`config_inventory.html`](config_inventory.html)（coverage-heatmap）+ 生成器 [`scripts/dashboard/gen_config_inventory.py`](../../scripts/dashboard/gen_config_inventory.py) + 数据 [`config_inventory.csv`](config_inventory.csv)
> 对应任务：WORKPLAN **F4**（"exp 看板改进：`config_inventory` 仍不够清晰，迭代成『一眼看懂跑了啥 / 缺啥』"）
> 验收日期：2026-06-30 · 验收人：Claude (Opus 4.8)
> **结论：通过（conditional）** —— 功能与数据真实性全部达标；遗留 2 项「done 口径」问题（F-1 / F-2）待用户拍板，改一处 CSV/生成器即可。

---

## 1. 验收标准

| # | 标准 | 来源 |
|---|---|---|
| C1 | 渲染正常、离线自包含（无外部依赖） | 看板要能直接 `file://` 打开 |
| C2 | 页内数字内部一致，且与数据文件 (`config_inventory.csv`) 一致 | 看板可信前提 |
| C3 | 数字**与真实数据源对得上**（cora ← `_phase_b_aggregate.csv`；arxiv ← `results/runs/` 磁盘扫描） | 监控盘的核心：得说真话 |
| C4 | 「一眼看懂跑了啥 / 缺啥」——分类清晰、缺口可见（F4 目标） | F4 验收点 |
| C5 | **可回填**：跑完一批后，能低成本刷新进度，不引入漂移 | 用户明确诉求 |

---

## 2. 功能验收（C1 / C2 / C4 / C5）

| 项 | 方法 | 结果 |
|---|---|---|
| 渲染 | Chrome `file://` 全页截图 | ✅ summary + 6 分类 block + 全 tile 正常 |
| 自包含 (C1) | grep `http(s)://` / `cdn` / `<link` / `<script src` | ✅ **0** 外部资源 |
| JS 合法 | `node --check`（抽出 `<script>`） | ✅ 通过 |
| 内部一致 (C2) | 求和嵌入 `CONFIGS` 数组 | ✅ **29 configs / 467 done / 1214 total**，与 CSV 完全一致 |
| 派生而非硬编码 | 审阅 JS | ✅ overall% / track / dataset / category / status / block 全部由 `CONFIGS` 页内计算（旧稿/原版是 3 处硬编码，已消除） |
| 分类可读 (C4) | 视觉 | ✅ 每分类独立 block；A3 渲染为 GAT/GCN × 4-α 网格；tile 红→黄→绿 + fill 编码完成度 |
| 缺口可见 (C4) | 视觉 + filter | ✅ "仅看红 / 隐藏已完成 / csv·disk" 三类过滤；红 tile 一眼定位未跑 |
| 可回填 (C5) | 改 CSV `done` → 重生 → 核对 | ✅ 实测：把 `phase_b_arxiv_T2_seed212` done `0→18` 重生 → 全盘 `485/1214`、该 config not-started→done、status `19/2/8`；`git checkout` 还原 → 回到 `467`。**一处 CSV 编辑，全盘联动** |

功能验收：**全绿**。

---

## 3. 数据真实性验收（C3）—— 与真实源逐项对账

数据源：`results/_phase_b_aggregate.csv`（460 行，cora 主源）+ `results/runs/ogbn-arxiv_GCN_r0.01/`（arxiv 磁盘）。

| 看板配置 | 看板 done/total | 源核对 | 判定 |
|---|---|---|---|
| `phase_b_cora_gat` | 180/180 | aggregate `cell=cora_GAT_r0.05` = 180 行，纯 6 strategy（无 alpha 行） | ✅ 真 |
| `phase_b_cora_gcn` | 180/180 | aggregate `cell=cora_GCN_r0.05` = **190 行** = 180 主矩阵 + 10 `hybrid_alpha0.00`（实为 A3，见 F-1） | ✅ 主矩阵部分准确（10 行另属 A3，看板已正确未计入本 config） |
| `A5_ratio_0.01` | 90/90 | aggregate `cell=cora_GCN_r0.01` = 90 行，**含 1 行 `failed=True`**（GraphRevoker/random/seed42, f1=0.583） | ⚠ 见 F-2 |
| **A3（全 8 config）** | **0/200** | aggregate 含 **10 个** A3 α=0.00 GCN 结果（`strategy=hybrid_alpha0.00`，GIF+GNNDelete × 5 seed） | ⚠ 见 F-1 |
| `phase_b_arxiv_T1_seed42` | 6/18 | disk = 6（GIF/GNNDelete × random/im/tracin, seed42） | ✅ 真 |
| `phase_b_arxiv_im_only_r01` | 2/9 | disk = 2（GIF_im / GNNDelete_im, seed42；与 T1 重叠） | ✅（per-config 口径） |
| `phase_b_arxiv_tracin_smoke` | 1/1 | disk = 1（GIF_tracin, seed42；与 T1 重叠） | ✅（per-config 口径） |
| `phase_b_arxiv` / `T2` / `T3` / `im_only`(r0.05) / `feasibility` / `hybrid_smoke` | 0/… | disk 无对应结果 | ✅ 真 |
| `sanity`（4 config） | 8/14 | aggregate `cora_GCN_r0.05` 子集 + r0.10 缺 | ✅ 一致 |

**arxiv 重叠口径说明**：磁盘只有 **6 个** distinct arxiv 结果 cell，但看板跨 config 计 **9**（im×1、tracin×1 被 `T1` 与 `im_only_r01`/`tracin_smoke` 重复计）。这与看板自述「config 互相重叠、1214 为上界」一致——**分子与分母同口径**（都含重叠），比值诚实；但「distinct cells done」< 467，应知悉。

数据真实性：**headline 全部对得上源**，无虚报。两项口径问题如下。

---

## 4. 发现与建议（需用户拍板）

### F-1 ★ A3 并非真 0/200

`_phase_b_aggregate.csv` 里实际存在 **10 个 A3 α=0.00 (cora_GCN) 结果**：`strategy=hybrid_alpha0.00`，method ∈ {GIF, GNNDelete}，seed 全 5 个，各带真实 `f1_after` 等指标。看板却报 A3 = 0/200、`A3_cora_GCN_alpha0.00` = 0/25。

- **两种解读**：
  - *alias 视角*（看板现状）：α=0.00 ≈ tracin，复用主矩阵 → 不单独计 → A3 = 0。
  - *字面结果视角*：这 10 行是 distinct 已产出 cell → `A3_cora_GCN_alpha0.00` = **10/25 partial**，A3 = **10/200**。
- **影响**："缺啥" 判断会偏——A3 并非完全未跑（α=0.00 GCN 的 GIF/GNNDelete 已有数）。
- **建议（推荐 a）**：
  - **(a)** 把 `A3_cora_GCN_alpha0.00` 的 `done` 改为 10（CSV 一处），A3 → 10/200、该 tile 变黄；并在 dedup 注里点明「其余 α-endpoint 仍按 alias 复用、未单独计」。最贴合 F4「看懂跑了啥」目标。
  - (b) 维持 0，但加脚注明示「aggregate 存在 α=0.00 alias 结果，按复用未单独计入」。

### F-2 A5_ratio_0.01 的 90/90 含 1 个失败 cell

该 config 90 行里有 1 行 `failed=True`（GraphRevoker / random / seed42，f1=0.583）。看板 `done` 口径是「文件/行存在」，非「成功」。该失败 cell 即已知的 **GraphRevoker 退化**问题（perf_before 落在 0.50–0.58，见 `project_graphrevoker_dispatcher_history` / WORKPLAN E4「修+重跑」）。

- **建议**：不改 `done` 数（90 仍是已产出 cell 数，口径自洽），但在脚注/tile detail 披露「含 1 个已知 GraphRevoker 失败 cell」。彻底解决随 E4「修聚合器 + 整 method 重跑」一并刷新。

> F-1 / F-2 都不影响 **cora 主矩阵 360 cell** 与 **arxiv pilot** 的真实性，是「done 的定义」问题，非虚报。

---

## 5. 结论

- **功能（C1/C2/C4/C5）**：通过，全绿。看板达成 F4「一眼看懂跑了啥 / 缺啥」，且 CSV→重生的回填闭环实测可用。
- **数据真实性（C3）**：通过；headline 数字全部与 `_phase_b_aggregate.csv` / 磁盘对得上，无虚报；遗留 F-1（A3 口径）/ F-2（失败 cell 披露）两项待定。
- **F4 验收：通过（conditional）** —— 待用户对 F-1/F-2 口径拍板后，改一处 CSV + 重生即收尾。

**复核命令**（任何人可复跑本验收的关键对账）：
```bash
# cora 源行数（cora_GAT_r0.05=180 / cora_GCN_r0.05=190 / cora_GCN_r0.01=90）
python -c "import csv,collections;print(collections.Counter(r['cell'] for r in csv.DictReader(open('results/_phase_b_aggregate.csv',encoding='utf-8-sig'))))"
# arxiv 磁盘 distinct 结果 cell（=6）
find results/runs/ogbn-arxiv_GCN_r0.01 -name attack.json | wc -l
# 看板内部一致（=29 / 467 / 1214）
python scripts/dashboard/gen_config_inventory.py   # 重生后看控制台汇总
```
---

## 6. 2026-06-30 correction: done vs usable vs rerun

User decision applied:

- **F-1 resolved**: `A3_cora_GCN_alpha0.00` now counts the 10 real `hybrid_alpha0.00` aggregate rows (GIF + GNNDelete x 5 seeds). A3 is therefore `10/200` produced instead of visually `0/200`.
- **F-2 resolved**: `A5_ratio_0.01` stays `90/90` produced, but the dashboard now warns that GraphRevoker contributes 15 cells pending E4 rerun and includes 1 failed `GraphRevoker/random/seed42` cell.
- **GraphRevoker repair surfaced**: `phase_b_cora_gcn` and `phase_b_cora_gat` now show `180/180 produced`, `150/180 usable`, and `30 rerun pending`, instead of a misleading all-green `180/180`.
- **Execution order adjusted**: the dashboard block order now follows the practical work sequence: Cora main matrix -> A5 -> arxiv remote queue -> A3 -> A6 -> sanity.

Regression lock: `tests/test_config_inventory_dashboard.py`.

---

## 7. 2026-07-01 story layer + IF-concordance refresh

Advisor-reporting layer added:

- Every experiment group now has a story block: Question / Setup / Why / Current read / Next decision.
- Story text is defined in `scripts/dashboard/gen_config_inventory.py` as generator metadata, not in `config_inventory.csv`.
- IF-concordance is now part of the rerun semantics: deployed TracIn/Hybrid rows are produced artifacts but not clean usable evidence until refreshed with proper-TracIn.

Updated clean counts:

- Cora main matrices: `180/180 produced`, `100/180 usable`, `80 rerun`.
- A5 r0.01: `90/90 produced`, `50/90 usable`, `40 rerun`.
- arxiv T1 seed42: `6/18 produced`, `4/18 usable`, `2 rerun`.
- arxiv TracIn smoke: `1/1 produced`, `0/1 usable`, `1 rerun`.
- Overall: `477/1214 produced`, `274/1214 usable`, `203 rerun`.

Regression lock remains `tests/test_config_inventory_dashboard.py`.
