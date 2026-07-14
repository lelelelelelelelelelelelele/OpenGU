# 自动汇报规则

> v1/v2 已于 2026-07-14 退役。以下模板仅用于解释 archive；新运行只写 V3 事件。

- `report_style_version = v1`
- 历史文件：`results/_journal/archive/auto_report_*.md`
- 写入策略：仅追加（append-only），不回写历史记录。

## 固定段落模板（必须）

```md
### [YYYY-MM-DD HH:MM:SS] <script>
- 任务：dataset=<dataset>, model=<model>, method=<method>, ratio=<ratio>
- 日志路径：`<log_file>`
- 执行结果：<status> | f1_before=<f1_before> | f1_after=<f1_after> | auc=<auc> | unlearn_time=<unlearn_time> | wall_time=<time_s>s
- 异常与定位：<error_type>: <error_msg> 或 无
- 下一步建议：<one actionable sentence>
```

## 状态字典

- `OK`：任务执行并产出有效指标。
- `SKIP`：仅在命中“严格 OK 日志”时允许跳过。
- `WARN`：任务结束但结果不完整或可疑。
- `X`：任务失败（返回码异常或运行错误）。
- `TIMEOUT`：超时中断。

## 历史默认下一步建议（已废弃）

- `OK`：检查该方法在其他比例或数据集的趋势。
- `SKIP`：继续执行下一个未完成配置。
- `TIMEOUT`：提高超时阈值或先降低比例后再重试。
- `WARN`/`X`：打开日志定位根因并重跑该配置。

## 字段格式规则

- 数值精度：`f1_before/f1_after/auc/unlearn_time` 保留 4 位小数。
- `wall_time` 保留 2 位小数并追加 `s`。
- 空值统一显示为 `NA`。
- 非数值（如不可计算）统一显示为 `NaN`。
- `异常与定位`：
  - 有 `error_type`：`<error_type>: <error_msg>`
  - 无异常：`无`

## 兼容性说明

- 该规范只约束 `v1` 之后新增条目。
- 历史条目不追改，允许与 `v1` 存在轻微格式差异。

---

## v2 扩展：决策条目（2026-02-17 起生效）

- `report_style_version = v2`
- 历史文件仍位于 `results/_journal/archive/auto_report_*.md`

### 会话分隔符

历史写法是在旧 auto_report.md 追加：

```
---
## Session YYYY-MM-DD-N
```

N 为当天第几次会话（从 1 开始）。

### 决策条目模板

```md
### [YYYY-MM-DD HH:MM] DECISION — <短标题>
- 背景：<触发原因>
- 选项：A: <...> / B: <...> [/ C: <...>]
- 选择：<选项> — <理由>
- 影响：<文件/参数/计划变更>
- 关联 Step：<Step N 或 N/A>
```

### 决策状态

- `DECIDED`：已确定并执行。
- `REVISED`：修正了先前的决策（必须引用原决策时间戳）。
- `DEFERRED`：暂时搁置，记录原因。

### 何时写决策条目

以下情况必须记录：
- 方案选择（如选 Phase 1 而非 Phase 2）
- 参数/指标变更（如从 accuracy 改为只看 F1）
- 计划调整（如跳过某个 Step 或改变优先级）
- 发现导致的策略转向（如发现 Random baseline 弱 → 调整攻击目标）

可选记录：
- 代码设计决策（如选择继承哪个基类）
- 环境/工具链变更

## 示例条目（人工验收）

```md
### [2026-02-16 18:00:00] run_cross_dataset_resume.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.5
- 日志路径：`results/step0_validation/cross_logs/cora/GIF_GCN_cora_r0.5.log`
- 执行结果：OK | f1_before=0.8838 | f1_after=0.8137 | auc=0.5087 | unlearn_time=0.3281 | wall_time=10.73s
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-02-16 18:01:00] run_cross_dataset_resume.py
- 任务：dataset=pubmed, model=GCN, method=IDEA, ratio=0.5
- 日志路径：`results/step0_validation/cross_logs/pubmed/IDEA_GCN_pubmed_r0.5.log`
- 执行结果：X | f1_before=NA | f1_after=NA | auc=NA | unlearn_time=NA | wall_time=1200.00s
- 异常与定位：TIMEOUT: Timeout after 1200s
- 下一步建议：提高超时阈值或先降低比例后再重试。
```

---

## v3：机器事件、历史 baseline 与有限状态视图（2026-07-14 起）

- 4090 active checkout 的旧 live `auto_report.md` 整体、逐字节归档为 `archive/auto_report_2026-05-06_to_2026-07-10_active4090.md`；不清洗、不截断、不把旧记录回填成 V3 事件。
- 新机器事件写入 `auto_report.events.jsonl`：一行一个 JSON 对象，`schema_version=3`，只追加。
- `auto_report_baseline.json` 只整理旧日志里仍需保留的事实、失效边界和来源校验，不宣称这些 cell 是当前 V3 完成态。
- 人看当前进度使用可重建的 `auto_report.md` / `auto_report.html`；这两个文件是有上限的派生视图，不是审计原件，可以从 JSONL + baseline 重建。

### 身份与阶段

- `cell_id`：由 dataset/model/method/strategy/ratio/seed/k 等矩阵坐标稳定生成；不随时间或重试改变。
- `run_id`：一次真实执行尝试的 ID；runner 通过环境变量传给 attack/collateral 子进程，因此同一次分阶段执行共享一个 `run_id`。
- runner 同时传播规范化 identity envelope；子进程的 identity 与 `cell_id` 不一致时拒绝追加，不能只靠外部传入的 `cell_id` 掩盖坐标差异。
- `config_fingerprint` 与 `git_sha` 必须独立记录；cell 坐标相同不代表配置或代码相同。
- 阶段：`selection` / `attack` / `collateral` / `run`。
- 状态：`started` / `completed` / `failed` / `skipped` / `retrying`。
- 允许阶段性终点：selection-only、attack-only、collateral、complete、failed；不能因为 collateral 尚未执行就伪报 complete。

### Cache 语义

每个 Cache observation 必须说明：

- `type`：`selection`、`result`、`score`、`artifact` 或 `run_artifact`；禁止只写泛化的 `cache=HIT`。
- `outcome`：`hit` / `miss` / `bypass` / `unknown`。
- `recipe` / `recipe_hash`：已知多少写多少；Legacy cache key 只能作为 Legacy recipe 字段，不能伪装成 Cache V2 Recipe hash。
- `artifact`：已知的 path / Artifact ID / content hash；Legacy 来源必须标 `authoritative=false`。
- `hit_source` 与 `lookup_policy`：HIT 必填来源，说明是 SelectionCache、ResultCache、完整 run artifacts 还是 exact resolver。
- `write_outcome`：`saved` / `reused` / `not_written` / `unknown`。

ResultCache 整体命中时，历史 `AttackResult` 内保存的 `selection_cache_hit` 只是原始运行事实，不能在本次运行中再次表达成 selection HIT。

### 何时追加

| 场景 | 是否追加 |
|---|---|
| 真实 compute/retry 开始 | 是：`started` / `retrying` |
| 阶段首次到达 terminal state | 是：`completed` / `failed` / `skipped` |
| 错误、return code、retry_of/attempt 变化 | 是 |
| dry-run | 否 |
| 同一 run/stage/state 的重复 producer 回报 | 否：按稳定 dedup key 抑制 |
| 未变化的完整 cell 被反复 skip / Cache hit | 只记录一次；Artifact/Recipe/config 改变后才新增 |
| standalone producer 的 selection/result 阶段完全由相同 Cache 复用满足 | 只记录一次语义 Cache reuse；runner 管理的真实 retry 仍逐 attempt 保留阶段事件 |
| 内部逐文件 Cache probe、固定“下一步建议”、重复 HIT 文本 | 否 |

追加前必须重新校验现有 JSONL、重算 event/dedup identity；发现坏行、被篡改事件或 identity/cell 不一致时 fail-closed，原文件保持不变。追加与 Markdown/HTML 视图刷新在同一锁内串行化。

主 `demo_attack.py`、`eval_collateral.py`、`experiments/run.py` 只使用 V3 事件。旧 `append_report_entry` / `append_attack_result` / `append_collateral_entry` 已废弃：不传显式 `report_path` 会拒绝写入，避免覆盖新的 `auto_report.md`；显式 fixture/export 路径仍可用于兼容测试，且不再自动生成“下一步建议”。兼容 reader 仍解析 v1 实验条目、v2 session/decision 和 v3 JSONL，读取不触发历史迁移。
