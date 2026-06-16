# 自动实验汇报（追加）

该文件由实验脚本自动追加写入，用于记录每个任务的执行结果与下一步动作。

---

_Reset 2026-05-06：清理 Phase B Blocker-1/2 污染数据后重置。前面历史在 git log + `results/_archive_20260506/` 里：_

```bash
# 历史日志（10000+ 行 pre-reset 内容）
git log -p results/_journal/auto_report.md

# 老实验产物（54 MB，已 .gitignore）
ls results/_archive_20260506/
```

---

### [2026-05-06 03:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8819, time=0.9s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8875, time=2.6s, cache=MISS, selection=1.9685s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-06 04:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random', 'tracin', 'hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8819, time=1.0s, cache=MISS, selection=0.0000s)
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8875, time=4.3s, cache=MISS, selection=3.2664s)
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8948, time=1.0s, cache=MISS, selection=0.1809s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-06 22:51] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7638, time=50.5s, cache=MISS, selection=0.0055s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:53:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -6.56% |    0.2496 |   26.92% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_random\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:03] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=40.3s, cache=MISS, selection=0.0033s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:04:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -9.27% |    0.2783 |   31.68% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_degree\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:05] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7712, time=41.3s, cache=MISS, selection=0.0401s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:06:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -12.22% |    0.2328 |   23.86% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_pagerank\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:07] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7897, time=47.0s, cache=HIT(key=df722027ea8b323817cc8cfd12810ec9), selection=2.1047s, reuse=0.001000s, speedup=2105.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:08:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -7.21% |    0.2470 |   25.41% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_tracin\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:09] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=48.5s, cache=MISS, selection=1.1599s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:11:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -3.55% |    0.2045 |   20.17% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_im\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:12] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7712, time=46.7s, cache=HIT(key=b5df0a23dea5473658f95b50ba6d4f3e), selection=1.2024s, reuse=0.000000s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:13:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.65% |    0.2225 |   22.01% |
- 日志路径：`H:\project\OpenGU\GULib-master\results\runs\cora_GCN_r0.05\GraphRevoker_hybrid\seed42\collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


---

### [2026-05-07 05:00] 决策 · MIGRATION_RUNBOOK §3-§4 一气贯通

**任务**：从 4090 服务器拉回 cora_ship_20260507_0442.tar.gz，全自动跑 §3 解包 → §4 中场分析 → §6 全图（cora-only），不等 arxiv。

**执行**：
1. §3.4 解包：`tar xzf ... -C results/runs/4090 --strip-components=2` → 360 cell（180 GCN + 180 GAT）三件齐
2. §3.5 来源核验：1 hostname + 2 git_sha (300+60) + 时间窗 7.5h → 干净
3. 写 `scripts/aggregate_phase_b.py`（runbook 附录 A.3 升级版：吞 collateral.json 的 perf_before/perf_unlearn/perf_retrain/gap/hop_decay，导 33-列 CSV）→ `results/_phase_b_aggregate.csv` (360 rows × 33 cols, zero nulls)
4. 写 `scripts/plot_phase_b_cora.py` 替代 stale `plot_paper_figures.py`：5 张图 → `results/paper_figures/`
   - fig1 F1-drop · fig2 MIA-AUC · fig3 paired-Δ · fig4 hop-decay · fig5 retrain-gap
5. 写 `scripts/build_paper_table1.py` → Markdown + LaTeX → `results/_paper_table1_cora.{md,tex}`

**核心发现（cora-only，paper draft 可填）**：
- **GNNDelete 是最易攻击的方法**：GCN max F1-drop 23.6% (degree, seed 1337)；mean 11.8%；retrain gap 9–17% — 唯一 gap 显著非零的方法
- **GraphRevoker MIA 最弱**：所有 strategy AUC 0.77-0.89，degree/random 都直接 0.83+ — 攻击不需要选点，default leakage 已经溢
- **MEGU-tracin 单点 MIA spike**：AUC 0.86 (GCN) / 0.77 (GAT) vs 同方法其他 strategy 0.30-0.50 — tracin 选到 MIA 边界节点了，可能是 paper 里的 "strategic selection breaks otherwise-robust unlearners" 的最强证据
- **shard 系负 F1-drop**：GraphEraser/GraphRevoker -5% 到 -15%，已被 k=5 noise floor cover (memory `feedback_shard_baselines.md`)
- **Phase B paired Δ vs random**：GIF/IDEA/MEGU 上策略普遍 ≥0（中位数 0.01-0.03 偏正），GNNDelete 高度不稳定（spread ±0.10）

**异常 · 待写入 limitations.md**：
- **GIF ≡ IDEA 在 collateral.json 的 perf_unlearn / perf_retrain 完全 bit-identical**（cora_GCN 30/30 cell，cora_GAT 20/30 cell，GIF/IDEA 与 MEGU 也部分匹配 9/30）
  - `f1_after` (attack.json) 仍各自不同 → **F1-drop 指标不受影响，可信**
  - `gap` (retrain gap, perf_unlearn − perf_retrain) **失真**：fig5 / Table 1 retrain gap 部分需打 caveat
  - 推测：`eval_collateral.py` 的 retrain pipeline 在 GIF/IDEA 上命中了相同 baseline cache（IF-based 方法共享 retrained baseline checkpoint 的可能性），或 collateral 用的是 transductive eval 路径而非攻击侧的 inductive 路径
  - **paper §5 candidate**：retrain-gap 指标需独立验证，否则只用 F1-drop + MIA-AUC 作主指标

**下一步**：
- arxiv 还未到位，等 H800 ship 进 `results/runs/h20/`，重跑 `aggregate_phase_b.py` → 全表/全图刷新
- limitations.md 写一条 "L6: collateral retrain gap 在 IF-family 方法间存在 cache collision 嫌疑"，触发 follow-up：跟 `attack/pipeline_adapter.py::run_retrain` 看是否复用了 GIF baseline checkpoint
- paper Table 1 cora 行 / Figure 1-3 cora 部分可立即填进 `report/paper/overleaf/sec/`，arxiv 列保留 `\textcolor{gray}{TBD}`

---

### [2026-05-07 06:00] BUG · IF-family approxi() 不写回 params_esti — **已确认 + 已修**

**根因（代码 trace 锁死）**：
- `unlearning/unlearning_methods/IDEA/idea.py::approxi()` 算完 `params_esti = model_params + params_change`，调 `evaluate_unlearn_F1(params_esti)` 算 F1 直接 return
- `unlearning/unlearning_methods/GIF/gif.py::approxi()` 同模式
- **整个流程都没把 `params_esti` 写回 `self.target_model.model.parameters()`**
- `pipeline_adapter.py::_get_trained_model()` 返回 `method.target_model.model` —— 对 IF-family 来说就是 originally-trained 权重，不是 unlearn 后的

**经验证**：
- ✅ MEGU 不受影响：`MEGUTrainer.py:102` `optimizer = torch.optim.SGD(self.model.parameters(), ...)` 走真梯度 in-place
- ✅ GNNDelete 不受影响：`gnndelete.py:825 load_state_dict + 487/838 optimizer on deletion module.parameters()` 真改权重
- ✅ Shard 系（GraphEraser/GraphRevoker）路径完全不同（`method.model_zoo.model`），且 perf_unlearn 跨方法 0 bit-collision
- ✅ MEGU 与 GIF/IDEA 有 9/30 collision = F1 lattice 巧合（cora test=542 节点，离散 F1 概率撞）

**Empirical 证据**：
- cora_GCN 30/30, cora_GAT 20/30 cell `GIF.perf_unlearn ≡ IDEA.perf_unlearn` 全精度 bit-identical
- 同 cell `attack.json.f1_after`（GIF=0.8395, IDEA=0.8266）≠ `collateral.json.perf_unlearn`（两者都=0.8653）—— 印证 attack 走的是另一条评估路径，collateral 拿到 stale baseline

**受影响指标**：
| 指标 | 状态 | 范围 |
|---|---|---|
| `attack.json.{f1_after, f1_drop, mia_auc, selected_nodes}` | ✅ 真 | 全方法 |
| `predictions.npz.{logits_before, logits_retrained}` | ✅ 真 | 全方法 |
| `predictions.npz.logits_unlearned` | ❌ 假 | GIF + IDEA |
| `collateral.json.{perf_unlearn, gap, hop_decay, pred_shift}` | ❌ 假 | GIF + IDEA |

**修复 (commit on `bug/perf-unlearn-collateral-collision` branch)**：
- `idea.py::approxi()` return 前加 `with torch.no_grad(): trainable_params = ...; for p, new_p in zip(...): p.data.copy_(new_p.detach().to(p.device))`
- `gif.py::approxi()` 同
- 验证：`scripts/verify_if_writeback_patch.py`（unit-test，stub model + 模拟写回 + 比对 model.parameters()）—— ALL CHECKS PASSED

**重跑范围**：
- ✅ 不需要重跑 `demo_attack.py`（attack.json 全可信）—— 360 cell 都不动
- ⚠ 需要重跑 `eval_collateral.py`，**仅限 GIF + IDEA**：
  - cora_GCN: 2 method × 6 strategy × 5 seed = 60 cell
  - cora_GAT: 60 cell
  - **共 120 cell**（不是 180、不是 360）
- arxiv（机 B 还在跑）：fix 部署到机 B 后，B.2 后续直接出正确版本，0 重跑

**对 paper 的影响**：
- **Table 1 主指标 F1-drop / MIA-AUC**：完全不受影响 ✓ paper 第一稿可以照填
- **fig5 retrain gap**：GNNDelete (uniquely high gap ~10-16%) 仍然正确，paper 主结论"GNNDelete 是 outlier" 不变；GIF/IDEA gap 修后会从 ~0 变成真 gap，预计仍小（因为 IF 方法本来就接近 retrain）
- **fig4 hop-decay**：GIF/IDEA 部分修后会变；但 paper 主线没依赖这张图

**下一步**：
- 把 fix 推到 4090 + h800 服务器
- 4090 跑 GIF + IDEA collateral（120 cell × ~30s ≈ 1h）
- 重新 ship + 重跑 `aggregate_phase_b.py` + `plot_phase_b_cora.py` + `build_paper_table1.py`
- arxiv 那边 H800 修复 fix 后 carry-on
