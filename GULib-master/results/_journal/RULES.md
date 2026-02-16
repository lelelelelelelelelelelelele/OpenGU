# 自动汇报规则（LLM v1）

- `report_style_version = v1`
- 生效文件：`results/_journal/auto_report.md`
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

## 默认下一步建议（无显式 `next_step` 时）

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
- 生效文件不变：`results/_journal/auto_report.md`

### 会话分隔符

每次新会话开始时，在 auto_report.md 追加：

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
