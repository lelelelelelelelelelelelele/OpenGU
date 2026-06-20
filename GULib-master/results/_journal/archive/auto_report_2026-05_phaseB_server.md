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

### [2026-05-06 21:00] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.6s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:00:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0129 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:03:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0132 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:03:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0121 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.7s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:03:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0124 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:03:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0138 |    0.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.7s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:04:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0130 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.3s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:04:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0139 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:04:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.64% |    0.0126 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:05:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0123 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:05:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.85% |    0.0138 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=MISS, selection=0.0630s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:05:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.86% |    0.0134 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.3s, cache=MISS, selection=0.0424s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:05:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0140 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.6s, cache=MISS, selection=0.0478s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:06:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.64% |    0.0128 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.4s, cache=MISS, selection=0.0504s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:06:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0125 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=MISS, selection=0.0376s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:06:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 1.06% |    0.0140 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=4.2s, cache=MISS, selection=2.6732s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:07:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.96% |    0.0219 |    0.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.3s, cache=MISS, selection=2.6966s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:07:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0220 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.3s, cache=MISS, selection=2.6928s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:07:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.86% |    0.0213 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=4.1s, cache=MISS, selection=2.5781s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:08:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.62% |    0.0238 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=4.7s, cache=MISS, selection=3.0086s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:08:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0219 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=3.6s, cache=MISS, selection=2.2911s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:08:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0144 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.2s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001238s, speedup=1850.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:08:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0146 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001091s, speedup=2099.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:09:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0132 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.1s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000661s, speedup=3465.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:09:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0133 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000729s, speedup=3142.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:09:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0154 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.1s, cache=MISS, selection=0.5315s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:10:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.9s, cache=MISS, selection=0.0446s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:10:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.0s, cache=MISS, selection=0.0716s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:10:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0157 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.9s, cache=MISS, selection=0.0508s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:11:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0168 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:11] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=2.1s, cache=MISS, selection=0.0671s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:11:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0168 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.1550 (f1_before=0.8672, f1_after=0.7122, time=3.3s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.000802s, speedup=0.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:11:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.56% |    0.3538 |   16.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.1531 (f1_before=0.8653, f1_after=0.7122, time=2.3s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.000608s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:12:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.51% |    0.3152 |    7.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0221 (f1_before=0.8672, f1_after=0.8450, time=2.5s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.000725s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:12:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.80% |    0.2685 |   18.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.0923 (f1_before=0.8653, f1_after=0.7731, time=2.3s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.001126s, speedup=0.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:12:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.57% |    0.3236 |   21.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0996 (f1_before=0.8616, f1_after=0.7620, time=1.9s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.000789s, speedup=0.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:13:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 9.57% |    0.2991 |   14.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = 0.1328 (f1_before=0.8672, f1_after=0.7343, time=2.0s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:13:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 16.03% |    0.3543 |   20.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = 0.2214 (f1_before=0.8653, f1_after=0.6439, time=2.1s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:13:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 22.22% |    0.3711 |   22.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = 0.1974 (f1_before=0.8672, f1_after=0.6697, time=1.9s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:13:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 14.07% |    0.4244 |   18.22% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = 0.1494 (f1_before=0.8653, f1_after=0.7159, time=1.8s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:14:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 9.68% |    0.3637 |   15.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.1218 (f1_before=0.8616, f1_after=0.7399, time=1.9s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:14:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 24.79% |    0.3632 |   27.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.0683 (f1_before=0.8672, f1_after=0.7989, time=2.1s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.000699s, speedup=90.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:14:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 15.74% |    0.3743 |   18.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.2362 (f1_before=0.8653, f1_after=0.6292, time=1.9s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.000688s, speedup=61.73x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:15:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 17.99% |    0.4756 |   21.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = 0.2085 (f1_before=0.8672, f1_after=0.6587, time=1.8s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.000664s, speedup=72.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:15:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 12.98% |    0.4601 |   19.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = 0.1550 (f1_before=0.8653, f1_after=0.7103, time=2.0s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.001363s, speedup=36.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:15:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 7.74% |    0.3897 |   13.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = 0.1144 (f1_before=0.8616, f1_after=0.7472, time=2.6s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.003823s, speedup=9.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:16:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 15.14% |    0.4024 |   19.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0443 (f1_before=0.8672, f1_after=0.8229, time=2.0s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.003558s, speedup=751.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:16:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 9.15% |    0.2229 |   12.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.1015 (f1_before=0.8653, f1_after=0.7638, time=1.8s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.000672s, speedup=4014.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:16:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 5.77% |    0.2078 |   12.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0572 (f1_before=0.8672, f1_after=0.8100, time=1.8s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.001115s, speedup=2414.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:17:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 4.47% |    0.1884 |    7.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0461 (f1_before=0.8653, f1_after=0.8192, time=1.9s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.000718s, speedup=3591.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:17:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 5.05% |    0.2207 |   12.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0424 (f1_before=0.8616, f1_after=0.8192, time=2.0s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.001157s, speedup=2600.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:17:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 12.50% |    0.2320 |   18.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.0849 (f1_before=0.8672, f1_after=0.7823, time=1.9s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001009s, speedup=2271.75x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:17:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 13.03% |    0.3968 |   19.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.1808 (f1_before=0.8653, f1_after=0.6845, time=1.6s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001205s, speedup=1900.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:18:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 7.26% |    0.3931 |   10.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1771 (f1_before=0.8672, f1_after=0.6900, time=1.9s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000663s, speedup=3455.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:18:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 15.50% |    0.3922 |   19.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1255 (f1_before=0.8653, f1_after=0.7399, time=1.9s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000696s, speedup=3290.92x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:18:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 20.51% |    0.5352 |   28.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.1144 (f1_before=0.8616, f1_after=0.7472, time=1.8s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000692s, speedup=3310.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:19:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 19.74% |    0.4201 |   27.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1033 (f1_before=0.8672, f1_after=0.7638, time=2.0s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.001019s, speedup=521.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:19:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.47% |    0.2701 |   20.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.0646 (f1_before=0.8653, f1_after=0.8007, time=1.8s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.001037s, speedup=42.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:19:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 8.99% |    0.3422 |   11.42% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.0756 (f1_before=0.8672, f1_after=0.7915, time=2.3s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.001106s, speedup=64.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:19:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 13.92% |    0.2328 |   19.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:20] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.1033 (f1_before=0.8653, f1_after=0.7620, time=2.0s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.001519s, speedup=33.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:20:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 5.62% |    0.2427 |    8.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:20] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.0775 (f1_before=0.8616, f1_after=0.7841, time=2.1s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.003775s, speedup=17.77x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:20:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 10.15% |    0.2111 |   12.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:20] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.5s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.002531s, speedup=0.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:20:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0184 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:21] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.4s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.003427s, speedup=0.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:21:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.85% |    0.0169 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:21] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.6s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.003477s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:21:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.51% |    0.0121 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:21] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.6s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.000623s, speedup=0.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:21:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0156 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:22] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.4s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.001710s, speedup=0.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:22:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0209 |    1.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:22] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.3s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:22:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.21% |    0.0193 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:22] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.6s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:22:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.22% |    0.0170 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:22] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.4s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:23:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.43% |    0.0129 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:23] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:23:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.85% |    0.0177 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:23] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.6s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:23:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.22% |    0.0206 |    1.51% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:23] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.6s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.000730s, speedup=86.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:23:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0195 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:24] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.001075s, speedup=39.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:24:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0172 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:24] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.6s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.000945s, speedup=50.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:24:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.21% |    0.0133 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:24] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.5s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.000689s, speedup=73.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:24:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.43% |    0.0179 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:24] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.4s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.001944s, speedup=19.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:25:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.43% |    0.0208 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.4s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.000770s, speedup=3472.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:25:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.30% |    0.0234 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=1.5s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.003942s, speedup=683.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:25:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0228 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.5s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.002114s, speedup=1273.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:25:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.07% |    0.0198 |    0.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.6s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.003050s, speedup=845.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:26:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.30% |    0.0200 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.5s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.003422s, speedup=879.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:26:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0228 |    0.73% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.5s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000608s, speedup=3768.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:26:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.43% |    0.0208 |    1.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.4s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000728s, speedup=3148.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:27:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0185 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.4s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001073s, speedup=2134.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:27:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.05% |    0.0139 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.5s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000729s, speedup=3144.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:27:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0182 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.4s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000702s, speedup=3261.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:27:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0220 |    1.51% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.5s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.000590s, speedup=900.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:28:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0207 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.6s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.000748s, speedup=59.58x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:28:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0177 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.001117s, speedup=64.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:28:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0155 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.4s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.014140s, speedup=3.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:29:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0176 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:29] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.3s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.000554s, speedup=121.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:29:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.21% |    0.0206 |    1.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:29] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.2s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.000879s, speedup=0.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:29:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0129 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:29] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.000684s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:29:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0132 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:30] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.1s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.001161s, speedup=0.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:30:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0121 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:30] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.2s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.000413s, speedup=0.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:30:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0124 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:30] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.4s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.003464s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:30:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0138 |    0.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:30] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.3s, cache=MISS, selection=0.0010s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:31:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0130 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:31] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.6s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:31:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0139 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:31] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:31:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.64% |    0.0126 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:31] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:31:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0123 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:32] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=1.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:32:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.85% |    0.0138 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:32] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.3s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.000836s, speedup=75.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:32:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.86% |    0.0134 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:32] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.1s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.000632s, speedup=67.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:32:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0140 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:32] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.7s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.000701s, speedup=68.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:33:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.64% |    0.0128 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:33] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.2s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.001473s, speedup=34.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:33:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0125 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:33] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.2s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.000824s, speedup=45.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:33:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 1.06% |    0.0140 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:33] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.000672s, speedup=3977.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:33:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.96% |    0.0219 |    0.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:34] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.1s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.000818s, speedup=3298.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:34:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0220 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:34] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.000723s, speedup=3722.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:34:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.86% |    0.0213 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:34] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.000815s, speedup=3161.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:34:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.62% |    0.0238 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:34] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.3s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.000595s, speedup=5059.81x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:34:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0219 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:35] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001034s, speedup=2214.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:35:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0144 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:35] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.4s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.004067s, speedup=563.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:35:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0146 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:35] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003783s, speedup=605.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:35:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0132 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003608s, speedup=635.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:36:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0133 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003022s, speedup=758.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:36:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0154 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.000778s, speedup=683.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:36:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.6s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.000616s, speedup=72.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:37:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.5s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.000655s, speedup=109.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:37:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0157 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.000674s, speedup=75.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:37:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0168 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.3s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.000633s, speedup=106.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:37:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0168 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:38] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=31.6s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.000675s, speedup=0.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:39:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.81% |    0.2810 |   29.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:40] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=34.1s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.000730s, speedup=0.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:41:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.13% |    0.1858 |   17.20% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:41] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=32.9s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.002754s, speedup=0.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:42:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.74% |    0.2412 |   25.70% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:43] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=33.1s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.000823s, speedup=0.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:44:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.52% |    0.2606 |   26.29% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:45] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=34.4s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.000682s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:46:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.49% |    0.2352 |   22.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:47] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=43.5s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:48:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 11.81% |    0.2648 |   27.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=34.2s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:50:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 3.07% |    0.1951 |   18.27% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:50] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=35.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:51:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.23% |    0.2375 |   25.56% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:52] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=33.1s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:53:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.51% |    0.2619 |   26.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:54] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=31.5s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:55:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.74% |    0.2464 |   23.52% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=36.7s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.004030s, speedup=15.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:57:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 12.04% |    0.2700 |   28.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:57] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=35.5s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.000746s, speedup=56.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 21:58:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 2.13% |    0.1965 |   18.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 21:59] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=34.5s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.000693s, speedup=69.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:00:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -2.45% |    0.2394 |   25.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:01] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=35.9s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.003082s, speedup=16.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:02:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.51% |    0.2624 |   26.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:03] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=32.0s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.000751s, speedup=50.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:04:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.23% |    0.2448 |   23.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:04] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=34.3s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.000911s, speedup=2935.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:05:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 17.59% |    0.3110 |   32.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=33.8s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.004210s, speedup=640.55x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:07:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 3.07% |    0.1855 |   16.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:08] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=34.5s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.000787s, speedup=3419.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:09:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.74% |    0.2363 |   24.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:10] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=36.0s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.000794s, speedup=3245.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:11:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.05% |    0.2422 |   23.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:12] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=34.1s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.002854s, speedup=1054.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:13:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.70% |    0.2190 |   20.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:13] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=33.7s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000669s, speedup=3423.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:14:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 9.72% |    0.2615 |   26.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:15] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=32.8s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000740s, speedup=3096.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:16:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.89% |    0.1959 |   18.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:17] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=32.6s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001028s, speedup=2228.54x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:18:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.98% |    0.2475 |   25.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=34.9s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000664s, speedup=3451.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:19:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.2699 |   27.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=34.9s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000959s, speedup=2389.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:21:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -3.92% |    0.2407 |   22.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:22] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=41.0s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.000950s, speedup=559.75x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:23:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 15.97% |    0.3172 |   32.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:24] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=34.6s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.000669s, speedup=66.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:25:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.36% |    0.1839 |   16.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:26] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=36.0s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.001024s, speedup=69.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:27:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.2437 |   25.32% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:27] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=32.1s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.000700s, speedup=72.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:28:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -4.80% |    0.2406 |   23.42% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 22:29] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=33.1s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.000634s, speedup=105.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 22:30:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.98% |    0.2390 |   22.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=2.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:03:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.0285 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.5s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:03:55] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0270 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=2.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:04:15] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.50% |    0.0304 |    3.06% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=2.2s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:04:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.85% |    0.0283 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.4s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:04:54] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.30% |    0.0260 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:05:14] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.43% |    0.0254 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.3s, cache=MISS, selection=0.0010s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:05:36] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.63% |    0.0252 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7601, time=2.4s, cache=MISS, selection=0.0015s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:05:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.28% |    0.0284 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.3s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:06:23] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.00% |    0.0279 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=2.3s, cache=MISS, selection=0.0009s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:06:46] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0281 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=2.3s, cache=MISS, selection=0.0376s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:07:05] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.43% |    0.0275 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=2.2s, cache=MISS, selection=0.0370s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:07:25] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.21% |    0.0260 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7878, time=2.3s, cache=MISS, selection=0.0367s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:07:45] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -2.38% |    0.0295 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7841, time=2.3s, cache=MISS, selection=0.0379s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:08:05] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0294 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=2.1s, cache=MISS, selection=0.0370s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:08:25] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.65% |    0.0265 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=7.4s, cache=MISS, selection=4.0304s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:08:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0279 |    1.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=7.0s, cache=MISS, selection=3.4496s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:09:16] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.29% |    0.0338 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=8.0s, cache=MISS, selection=3.4869s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:09:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.39% |    0.0306 |    2.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=7.2s, cache=MISS, selection=3.3704s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:10:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.86% |    0.0294 |    1.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=7.4s, cache=MISS, selection=3.8873s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:10:34] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.08% |    0.0295 |    2.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=4.8s, cache=MISS, selection=1.5652s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:11:02] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.43% |    0.0271 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:11] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004891s, speedup=320.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:11:25] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.21% |    0.0281 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:11] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7878, time=2.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004775s, speedup=327.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:11:47] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0304 |    2.53% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:11] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000995s, speedup=1573.55x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:12:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0280 |    1.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:12] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000801s, speedup=1953.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:12:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0258 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:12] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=5.0s, cache=MISS, selection=0.0416s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:12:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.30% |    0.0270 |    1.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:13] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=3.4s, cache=MISS, selection=0.0418s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:13:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.42% |    0.0316 |    3.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:13] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7970, time=4.0s, cache=MISS, selection=0.0419s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:13:34] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.42% |    0.0272 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:13] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=3.2s, cache=MISS, selection=0.0420s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:13:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.0272 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:14] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=3.2s, cache=MISS, selection=0.0365s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:14:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0247 |    2.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.1218 (f1_before=0.8782, f1_after=0.7565, time=2.7s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.000620s, speedup=0.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:14:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 17.93% |    0.3159 |   20.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.1218 (f1_before=0.8690, f1_after=0.7472, time=2.8s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.000836s, speedup=0.27x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:14:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.56% |    0.3089 |   15.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.1716 (f1_before=0.8598, f1_after=0.6882, time=2.7s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.000641s, speedup=0.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:15:13] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.39% |    0.2389 |   17.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1679 (f1_before=0.8616, f1_after=0.6937, time=2.9s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.005966s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:15:39] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 8.32% |    0.1728 |   11.47% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0609 (f1_before=0.8727, f1_after=0.8118, time=2.9s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.002538s, speedup=0.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:16:02] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.32% |    0.2944 |   22.35% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = 0.1753 (f1_before=0.8782, f1_after=0.7030, time=3.4s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:16:26] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 21.43% |    0.3037 |   27.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = 0.1199 (f1_before=0.8727, f1_after=0.7528, time=2.8s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:16:48] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 15.20% |    0.2655 |   22.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = 0.1882 (f1_before=0.8598, f1_after=0.6716, time=2.8s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:17:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 14.26% |    0.2073 |   19.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = 0.1089 (f1_before=0.8672, f1_after=0.7583, time=2.6s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:17:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 13.59% |    0.3696 |   17.88% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = 0.1384 (f1_before=0.8635, f1_after=0.7251, time=2.8s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:17:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 31.65% |    0.3672 |   34.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:17] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = 0.1402 (f1_before=0.8708, f1_after=0.7306, time=2.7s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.000759s, speedup=49.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:18:10] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 15.48% |    0.2951 |   18.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = 0.1125 (f1_before=0.8672, f1_after=0.7546, time=2.8s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.000575s, speedup=64.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:18:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 11.99% |    0.2337 |   15.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:18] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = 0.1605 (f1_before=0.8635, f1_after=0.7030, time=2.7s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.000777s, speedup=47.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:18:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 10.99% |    0.2115 |   19.05% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = 0.1587 (f1_before=0.8616, f1_after=0.7030, time=3.0s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.000679s, speedup=55.77x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:19:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 17.20% |    0.3933 |   21.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = 0.1218 (f1_before=0.8690, f1_after=0.7472, time=2.8s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.000771s, speedup=47.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:19:33] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 24.57% |    0.2734 |   26.00% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:19] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.1181 (f1_before=0.8782, f1_after=0.7601, time=2.7s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.000816s, speedup=4941.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:19:55] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 14.69% |    0.2318 |   19.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:20] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.1513 (f1_before=0.8672, f1_after=0.7159, time=2.8s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.000709s, speedup=4868.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:20:15] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 8.39% |    0.2189 |   13.51% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:20] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.1587 (f1_before=0.8672, f1_after=0.7085, time=2.9s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.004912s, speedup=709.81x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:20:40] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.98% |    0.1565 |   11.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:20] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.1605 (f1_before=0.8708, f1_after=0.7103, time=3.2s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.003864s, speedup=872.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:21:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 10.65% |    0.1889 |   16.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:21] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0701 (f1_before=0.8727, f1_after=0.8026, time=3.3s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.004463s, speedup=870.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:21:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.14% |    0.1819 |   15.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:21] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1310 (f1_before=0.8782, f1_after=0.7472, time=4.5s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004425s, speedup=353.71x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:21:57] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.13% |    0.2338 |   17.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:22] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.1107 (f1_before=0.8690, f1_after=0.7583, time=3.1s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000713s, speedup=2194.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:22:19] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.44% |    0.2904 |   20.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:22] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1753 (f1_before=0.8672, f1_after=0.6919, time=3.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000730s, speedup=2145.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:22:41] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 12.95% |    0.2565 |   20.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:22] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1236 (f1_before=0.8616, f1_after=0.7380, time=2.9s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000706s, speedup=2216.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:23:02] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 16.17% |    0.2442 |   23.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.0996 (f1_before=0.8653, f1_after=0.7657, time=2.9s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000633s, speedup=2471.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:23:22] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 11.78% |    0.2738 |   19.73% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1292 (f1_before=0.8782, f1_after=0.7491, time=3.2s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.001037s, speedup=40.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:23:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 20.95% |    0.3114 |   22.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.1070 (f1_before=0.8672, f1_after=0.7601, time=3.6s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.001042s, speedup=40.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:24:06] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 9.64% |    0.2943 |   15.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:24] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.1328 (f1_before=0.8598, f1_after=0.7269, time=2.3s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.002091s, speedup=20.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:24:26] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 6.16% |    0.2021 |   13.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:24] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.1661 (f1_before=0.8690, f1_after=0.7030, time=3.1s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.001698s, speedup=24.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:24:47] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 6.70% |    0.2028 |   10.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:24] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GAT, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.0756 (f1_before=0.8708, f1_after=0.7952, time=3.1s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.000959s, speedup=38.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:25:08] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 9.32% |    0.1717 |   15.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GNNDelete_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=2.3s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.000626s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:25:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.50% |    0.0754 |    4.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=2.3s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.004661s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:25:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0969 |    4.42% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.2s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.002903s, speedup=0.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:26:16] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.08% |    0.0546 |    3.35% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.2s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.004006s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:26:39] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.61% |    0.0584 |    4.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=2.2s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.001171s, speedup=0.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:26:58] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.29% |    0.0522 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.2s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:27:17] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 1.27% |    0.0795 |    4.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=2.3s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:27:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.86% |    0.0951 |    4.52% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:27] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.3s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:27:56] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0594 |    3.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=2.3s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:28:17] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 2.14% |    0.0618 |    4.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:28:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.21% |    0.0504 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:28] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=2.3s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.000785s, speedup=47.89x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:28:57] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.29% |    0.0816 |    3.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:29] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=2.2s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.000652s, speedup=56.79x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:29:16] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.1010 |    4.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:29] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=2.4s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.000670s, speedup=54.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:29:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.65% |    0.0562 |    3.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:29] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.3s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.001161s, speedup=32.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:29:55] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 2.56% |    0.0600 |    4.76% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:30] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.2s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.001125s, speedup=32.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:30:15] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.64% |    0.0511 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:30] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8690, time=2.3s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.005230s, speedup=770.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:30:39] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0799 |    3.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:30] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=2.1s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.004484s, speedup=769.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:31:04] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.0916 |    3.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:31] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=2.3s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.004843s, speedup=719.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:31:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.40% |    0.0605 |    3.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:31] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.2s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.004039s, speedup=834.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:31:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.52% |    0.0625 |    4.47% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:31] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=2.2s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.000780s, speedup=4986.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:32:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.87% |    0.0607 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:32] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000658s, speedup=2377.71x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:32:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.22% |    0.0781 |    3.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:32] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=2.1s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.002154s, speedup=726.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:32:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0931 |    3.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:33] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000723s, speedup=2164.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:33:13] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.30% |    0.0582 |    3.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:33] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=2.1s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000804s, speedup=1945.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:33:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 2.78% |    0.0601 |    4.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:33] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004716s, speedup=331.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:33:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 2.33% |    0.0519 |    3.06% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=2.2s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.000831s, speedup=50.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:34:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0772 |    3.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=2.2s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.001823s, speedup=22.91x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:34:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.0886 |    3.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.0s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.001164s, speedup=35.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:34:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0541 |    3.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=2.3s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.000625s, speedup=67.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:35:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0573 |    3.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GAT, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=2.2s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.003795s, speedup=9.63x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:35:33] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0516 |    2.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/MEGU_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:35] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.3s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.004858s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:35:56] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0288 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.004250s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:36:20] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0270 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=2.3s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.004839s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:36:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.72% |    0.0281 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:36] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.3s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.008600s, speedup=0.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:37:03] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0283 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=2.1s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.000863s, speedup=0.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:37:23] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0258 |    1.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7823, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:37:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.86% |    0.0264 |    2.53% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=2.2s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:38:03] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.42% |    0.0251 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.1s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:38:23] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.28% |    0.0284 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:38:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.22% |    0.0291 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=2.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:39:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.51% |    0.0263 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7860, time=2.2s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.000619s, speedup=60.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:39:21] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.21% |    0.0271 |    2.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.2s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.000647s, speedup=57.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:39:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0262 |    2.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7768, time=2.2s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.000661s, speedup=55.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:40:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -2.38% |    0.0295 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7970, time=1.9s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.001897s, speedup=19.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:40:21] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.22% |    0.0297 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=2.3s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.004224s, speedup=8.75x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:40:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.65% |    0.0266 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=2.3s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.004039s, speedup=997.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:41:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0280 |    1.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.3s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.002809s, speedup=1228.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:41:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.17% |    0.0324 |    2.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=2.2s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.000735s, speedup=4742.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:41:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.16% |    0.0316 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=2.3s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.000798s, speedup=4223.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:42:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.20% |    0.0299 |    1.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=2.4s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.000664s, speedup=5858.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:42:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.08% |    0.0295 |    2.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000646s, speedup=2421.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:42:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.43% |    0.0285 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000707s, speedup=2214.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:43:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0275 |    2.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000657s, speedup=2382.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:43:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0275 |    1.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=2.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000601s, speedup=2603.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:43:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0294 |    1.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.8s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000658s, speedup=2378.57x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:44:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.21% |    0.0249 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.4s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.000619s, speedup=67.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:44:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0270 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=2.2s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.000748s, speedup=55.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:44:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.63% |    0.0321 |    3.01% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:45] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=2.9s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.001385s, speedup=30.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:45:13] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0280 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:45] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=2.5s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.004638s, speedup=9.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:45:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.0270 |    2.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:45] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=2.4s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.003746s, speedup=9.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:46:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0247 |    1.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:46] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=48.5s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.004545s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:48:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 21.87% |    0.3265 |   37.51% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=46.7s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.000667s, speedup=0.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:50:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.51% |    0.2409 |   25.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:51] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=48.3s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.003280s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:53:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.33% |    0.3053 |   27.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:54] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=47.7s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.000660s, speedup=0.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:55:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.60% |    0.2473 |   26.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:57] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=61.7s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.004122s, speedup=0.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-06 23:58:46] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -6.17% |    0.2808 |   28.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-06 23:59] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=48.7s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:01:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 15.06% |    0.3197 |   35.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:02] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=47.1s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:03:33] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 10.02% |    0.2750 |   28.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:04] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=47.0s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:05:58] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -5.67% |    0.2726 |   26.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=52.5s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:08:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.82% |    0.2581 |   27.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:09] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=49.9s, cache=MISS, selection=0.0014s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:11:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 1.29% |    0.2962 |   28.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:11] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=48.8s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.004991s, speedup=7.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:13:25] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 9.39% |    0.3029 |   33.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:14] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=47.7s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.000803s, speedup=46.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:15:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 12.75% |    0.2645 |   27.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:16] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=50.7s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.003319s, speedup=11.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:18:21] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.30% |    0.2847 |   26.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:19] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=52.8s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.000794s, speedup=47.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:20:55] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.82% |    0.2584 |   27.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:21] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=53.9s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.005153s, speedup=7.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:23:24] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 8.21% |    0.3173 |   31.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:24] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=45.9s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.001114s, speedup=3618.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:25:44] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 10.54% |    0.3329 |   34.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:26] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=48.1s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.002119s, speedup=1628.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:28:08] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.50% |    0.2347 |   24.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:29] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=48.1s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.000636s, speedup=5479.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:30:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.64% |    0.2858 |   23.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:31] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=57.8s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.002343s, speedup=1438.54x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:33:15] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.52% |    0.2645 |   28.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:34] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=48.5s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.000649s, speedup=5987.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:35:41] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -7.63% |    0.2867 |   28.52% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:36] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=50.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.003473s, speedup=450.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:38:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 5.33% |    0.2913 |   32.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:39] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=48.5s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000676s, speedup=2315.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:40:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 4.68% |    0.2518 |   28.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:41] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=49.0s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.001127s, speedup=1388.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:42:58] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.3140 |   31.39% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:43] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=47.7s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.001039s, speedup=1506.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:45:21] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.56% |    0.2672 |   27.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:46] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=49.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.003211s, speedup=487.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:47:44] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.76% |    0.2865 |   27.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:48] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=48.2s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.001406s, speedup=29.58x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:50:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 13.79% |    0.3558 |   39.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:51] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=54.9s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.001196s, speedup=34.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:52:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.25% |    0.2187 |   21.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:53] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=47.5s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.002768s, speedup=15.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:55:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -4.43% |    0.3033 |   25.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=52.8s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.029271s, speedup=1.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 00:57:40] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.26% |    0.2578 |   25.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 00:58] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=47.0s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.001610s, speedup=22.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 01:00:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -2.52% |    0.3152 |   27.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphEraser_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:29] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6328, time=45.8s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.002326s, speedup=0.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:31:30] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.38% |    0.3086 |   40.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:32] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6310, time=43.9s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.001547s, speedup=0.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:33:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.08% |    0.3806 |   44.56% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:34] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6273, time=42.8s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.007851s, speedup=0.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:35:51] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -19.20% |    0.2858 |   34.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:36] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6476, time=47.7s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.074471s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:38:08] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.61% |    0.2804 |   33.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:38] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6384, time=43.4s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.001271s, speedup=0.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:40:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.46% |    0.3799 |   44.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:41] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.6033, time=46.7s, cache=MISS, selection=0.0013s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:42:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -9.24% |    0.2855 |   32.94% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:43] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.6310, time=42.6s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:44:40] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 11.96% |    0.2820 |   38.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:45] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.6070, time=46.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:46:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -15.04% |    0.2396 |   26.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:47] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.6292, time=43.7s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:49:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -10.94% |    0.2909 |   31.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:49] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.6347, time=44.3s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:51:20] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 3.10% |    0.3463 |   39.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:52] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.6107, time=44.2s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.005407s, speedup=6.95x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:53:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -15.48% |    0.3550 |   39.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:54] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.6107, time=43.4s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.001199s, speedup=30.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:55:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -13.46% |    0.3404 |   43.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:56] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.6310, time=48.5s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.003610s, speedup=10.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 02:58:03] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -19.49% |    0.2834 |   32.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 02:58] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.6384, time=46.4s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.028519s, speedup=1.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:00:14] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -6.56% |    0.2828 |   34.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:01] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.6218, time=45.5s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.034407s, speedup=1.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:02:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -2.05% |    0.3067 |   32.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:03] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6328, time=44.4s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.021524s, speedup=187.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:04:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -12.77% |    0.2936 |   30.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:05] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6568, time=48.1s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.076403s, speedup=45.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:07:00] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.19% |    0.3192 |   44.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:07] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6089, time=46.9s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.037621s, speedup=92.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:09:11] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 8.94% |    0.2050 |   20.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:10] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6236, time=44.3s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.067033s, speedup=50.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:11:24] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -9.02% |    0.3237 |   36.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:12] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6439, time=42.1s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.032407s, speedup=119.95x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:13:34] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 16.18% |    0.3478 |   43.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:14] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6255, time=46.0s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.021375s, speedup=73.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:15:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -7.75% |    0.3205 |   30.27% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:16] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6218, time=49.9s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004063s, speedup=385.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:18:12] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 9.52% |    0.3104 |   40.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:19] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6347, time=43.7s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000710s, speedup=2205.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:20:20] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -9.45% |    0.2491 |   25.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:21] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6218, time=46.9s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.003546s, speedup=441.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:22:34] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -17.02% |    0.3209 |   37.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:23] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6107, time=44.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000709s, speedup=2208.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:24:48] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 13.96% |    0.3790 |   48.25% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:25] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.6033, time=48.5s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.046017s, speedup=0.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:27:10] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -4.03% |    0.3448 |   37.51% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:28] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.6218, time=45.4s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.008588s, speedup=4.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:29:19] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.59% |    0.2835 |   37.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:30] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.6181, time=43.9s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.181247s, speedup=0.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:31:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 3.03% |    0.2708 |   30.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:32] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.6162, time=44.3s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.011375s, speedup=3.69x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:33:40] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -13.18% |    0.2870 |   36.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:34] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GAT, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.6494, time=46.2s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.062220s, speedup=0.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:35:56] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 21.43% |    0.3625 |   50.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GraphRevoker_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:40] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7251, time=30.6s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.303218s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:41:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -4.41% |    0.3148 |   31.00% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:42] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=28.3s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.012952s, speedup=0.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:43:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.09% |    0.2586 |   27.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:43] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=29.1s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.091068s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:44:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.58% |    0.2545 |   27.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:45] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7140, time=30.2s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.020795s, speedup=0.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:46:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -15.60% |    0.3095 |   31.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:47] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=32.8s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.098959s, speedup=0.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:47:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.98% |    0.2380 |   23.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:48] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=29.7s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:49:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 7.53% |    0.2543 |   27.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:49] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7288, time=28.1s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:50:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.31% |    0.2927 |   28.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:51] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=30.2s, cache=MISS, selection=0.0011s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:52:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -7.33% |    0.2682 |   29.06% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:52] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=28.7s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:53:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.88% |    0.2129 |   23.57% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:54] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7122, time=29.5s, cache=MISS, selection=0.0015s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:55:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.95% |    0.2885 |   28.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:55] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=34.0s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.233109s, speedup=0.27x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:56:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 4.97% |    0.2453 |   25.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:57] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=30.3s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.065638s, speedup=0.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:58:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -6.65% |    0.2572 |   29.01% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 03:59] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=29.7s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.110343s, speedup=0.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 03:59:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 1.27% |    0.2316 |   26.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:00] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7085, time=28.4s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.009291s, speedup=5.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:01:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -2.45% |    0.1983 |   20.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:01] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=28.0s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.022972s, speedup=1.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:02:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 5.83% |    0.2517 |   24.05% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:03] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7066, time=32.9s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.017679s, speedup=151.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:04:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.54% |    0.2853 |   27.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:04] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7288, time=31.6s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.018867s, speedup=142.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:05:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -10.68% |    0.2407 |   21.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:06] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=34.3s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.017015s, speedup=158.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:07:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -7.49% |    0.2501 |   27.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:08] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=29.5s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.017119s, speedup=150.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:08:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 2.05% |    0.2078 |   20.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:09] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=29.1s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.014187s, speedup=212.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:10:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.44% |    0.2505 |   21.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:11] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7085, time=31.0s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.069716s, speedup=32.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:11:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 2.61% |    0.3959 |   40.57% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:12] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=32.1s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000915s, speedup=2503.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:13:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.30% |    0.2536 |   24.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:14] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=32.0s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000714s, speedup=3210.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:15:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 8.44% |    0.2433 |   26.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:15] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=29.5s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001083s, speedup=2116.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:16:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -12.33% |    0.2362 |   26.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:17] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=28.5s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000658s, speedup=3480.44x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:18:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 9.52% |    0.2741 |   29.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:18] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=29.2s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.013396s, speedup=39.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:19:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.60% |    0.2951 |   29.54% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:20] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7251, time=28.8s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.015184s, speedup=2.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:20:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -3.00% |    0.2303 |   22.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:21] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=31.9s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.039644s, speedup=1.81x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:22:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.2460 |   27.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:23] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=31.3s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.233855s, speedup=0.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:24:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -6.77% |    0.2191 |   22.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 04:24] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=30.8s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.127966s, speedup=0.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 04:25:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -10.14% |    0.2490 |   25.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphRevoker_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.6s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:29:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0129 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:29:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0132 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:29:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0121 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.7s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:30:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0124 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:30:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0138 |    0.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.7s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:30:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0130 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:30] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.3s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:31:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0139 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:31] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:31:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.64% |    0.0126 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:31] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:31:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0123 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:31] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:31:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.85% |    0.0138 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:31] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=MISS, selection=0.0630s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:32:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.86% |    0.0134 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.3s, cache=MISS, selection=0.0424s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:32:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0140 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.6s, cache=MISS, selection=0.0478s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:32:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.64% |    0.0128 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.4s, cache=MISS, selection=0.0504s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:32:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0125 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:32] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=MISS, selection=0.0376s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:33:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 1.06% |    0.0140 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:33] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=4.2s, cache=MISS, selection=2.6732s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:33:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.96% |    0.0219 |    0.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:33] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.3s, cache=MISS, selection=2.6966s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:33:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0220 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:33] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.3s, cache=MISS, selection=2.6928s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:33:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.86% |    0.0213 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:33] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=4.1s, cache=MISS, selection=2.5781s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:34:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.62% |    0.0238 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:34] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=4.7s, cache=MISS, selection=3.0086s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:34:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0219 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:34] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=3.6s, cache=MISS, selection=2.2911s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:34:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0144 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:34] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.2s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001238s, speedup=1850.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:34:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0146 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:35] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001091s, speedup=2100.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:35:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0132 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:35] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.1s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000661s, speedup=3466.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:35:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0133 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:35] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.000729s, speedup=3142.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:35:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0154 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:35] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.1s, cache=MISS, selection=0.5315s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:36:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:36] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.9s, cache=MISS, selection=0.0446s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:36:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:36] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=2.0s, cache=MISS, selection=0.0716s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:36:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0157 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:36] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.9s, cache=MISS, selection=0.0508s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:36:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0168 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:36] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=2.1s, cache=MISS, selection=0.0671s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:37:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0168 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.2s, cache=HIT(key=c0e65b3d8774b78403053bc8be0e89bf), selection=0.0004s, reuse=0.000879s, speedup=0.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:37:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0129 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=7bd08402807cd6b744566aeaf8671260), selection=0.0002s, reuse=0.000684s, speedup=0.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:37:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0132 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:37] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.1s, cache=HIT(key=b9c784384df55bcf3b975633b3a804b8), selection=0.0002s, reuse=0.001161s, speedup=0.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:37:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0121 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.2s, cache=HIT(key=89b2e6cd18c5a01fa8998ce1339cf225), selection=0.0003s, reuse=0.000413s, speedup=0.73x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:38:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0124 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.4s, cache=HIT(key=37495ba8a4a39dda875482de2fd6cdd3), selection=0.0002s, reuse=0.003464s, speedup=0.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:38:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0138 |    0.78% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.3s, cache=MISS, selection=0.0010s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:38:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0130 |    1.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:38] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.6s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:38:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0139 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.2s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:39:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.64% |    0.0126 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:39:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0123 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=1.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:39:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.85% |    0.0138 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:39] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.3s, cache=HIT(key=979f1cc6142145f2310a1470ed6feba1), selection=0.0630s, reuse=0.000836s, speedup=75.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:39:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.86% |    0.0134 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.1s, cache=HIT(key=611939773c06d4e1976fa14d296c6b56), selection=0.0424s, reuse=0.000632s, speedup=67.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:40:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0140 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.7s, cache=HIT(key=482d233daed38911833601290a3b4303), selection=0.0478s, reuse=0.000701s, speedup=68.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:40:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.64% |    0.0128 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.2s, cache=HIT(key=f73d032dd486d55e36bf5a94bddddb90), selection=0.0504s, reuse=0.001473s, speedup=34.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:40:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0125 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:40] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.2s, cache=HIT(key=f7002a81216e6cc21ebe0ba3e3b6f699), selection=0.0376s, reuse=0.000824s, speedup=45.63x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:41:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 1.06% |    0.0140 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=40207dd070ab43430b9966347f93cdf2), selection=2.6732s, reuse=0.000672s, speedup=3977.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:41:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.96% |    0.0219 |    0.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.1s, cache=HIT(key=b1f1d57c3e4c99a115d60fcd65a561b5), selection=2.6966s, reuse=0.000818s, speedup=3296.58x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:41:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0220 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=HIT(key=1ee87f3a6d32badd59174a75cd21988f), selection=2.6928s, reuse=0.000723s, speedup=3724.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:41:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.86% |    0.0213 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=753e6961cee71bcef6ba5aa2559e0c10), selection=2.5781s, reuse=0.000815s, speedup=3163.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:42:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.62% |    0.0238 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.3s, cache=HIT(key=6f413781ea495438b169fc76a21216bb), selection=3.0086s, reuse=0.000595s, speedup=5056.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:42:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0219 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.001034s, speedup=2215.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:42:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0144 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.4s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.004067s, speedup=563.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:42:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0146 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003783s, speedup=605.63x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:43:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0132 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003608s, speedup=635.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:43:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0133 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.3s, cache=HIT(key=8120ecc3978a7a64c402f5e473b60ae4), selection=2.2911s, reuse=0.003022s, speedup=758.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:43:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.06% |    0.0154 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:43] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=d6bd19b117fb770a833d5a13598702c3), selection=0.5315s, reuse=0.000778s, speedup=683.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:43:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.6s, cache=HIT(key=1d07c4e39192b462f835cb5b4c503adc), selection=0.0446s, reuse=0.000616s, speedup=72.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:44:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.5s, cache=HIT(key=da959eb92bf52967c797a899c77af391), selection=0.0716s, reuse=0.000655s, speedup=109.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:44:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0157 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=d313c6f6b4874fa033217f238c3316a5), selection=0.0508s, reuse=0.000674s, speedup=75.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:44:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0168 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:44] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.3s, cache=HIT(key=80856bf5cb3605d8db49fad1399ffce8), selection=0.0671s, reuse=0.000633s, speedup=106.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:45:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0168 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:45] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=2.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:45:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0281 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:45] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.5s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:45:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0269 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:45] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=2.3s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:45:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.28% |    0.0293 |    2.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:46] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=2.2s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:46:19] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.0287 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:46] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.4s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:46:37] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0256 |    1.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:46] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:46:54] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.22% |    0.0259 |    1.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.3s, cache=MISS, selection=0.0010s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:47:14] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.21% |    0.0271 |    2.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7601, time=2.4s, cache=MISS, selection=0.0015s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:47:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.50% |    0.0286 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.3s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:47:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.21% |    0.0279 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:47] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=2.3s, cache=MISS, selection=0.0009s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:48:08] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0281 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:48] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=2.3s, cache=MISS, selection=0.0376s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:48:26] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.43% |    0.0292 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:48] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=2.2s, cache=MISS, selection=0.0370s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:48:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.21% |    0.0260 |    2.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:48] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7878, time=2.3s, cache=MISS, selection=0.0367s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:49:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.50% |    0.0294 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7841, time=2.3s, cache=MISS, selection=0.0379s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:49:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.00% |    0.0274 |    2.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=2.1s, cache=MISS, selection=0.0370s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:49:38] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.65% |    0.0258 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:49] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=7.4s, cache=MISS, selection=4.0304s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:49:56] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0294 |    1.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:50] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=7.0s, cache=MISS, selection=3.4496s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:50:13] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.61% |    0.0329 |    2.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:50] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=8.0s, cache=MISS, selection=3.4869s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:50:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.16% |    0.0316 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:50] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=7.2s, cache=MISS, selection=3.3704s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:50:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.98% |    0.0299 |    2.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=7.4s, cache=MISS, selection=3.8873s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:51:14] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.08% |    0.0295 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=4.8s, cache=MISS, selection=1.5652s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:51:32] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.43% |    0.0271 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004891s, speedup=320.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:51:49] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.42% |    0.0285 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:51] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7878, time=2.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.004775s, speedup=327.79x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:52:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0295 |    1.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000995s, speedup=1573.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:52:23] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.65% |    0.0283 |    1.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000801s, speedup=1954.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:52:41] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.21% |    0.0249 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7804, time=5.0s, cache=MISS, selection=0.0416s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:52:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0279 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=3.4s, cache=MISS, selection=0.0418s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:53:17] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.63% |    0.0321 |    3.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7970, time=4.0s, cache=MISS, selection=0.0419s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:53:34] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.42% |    0.0296 |    2.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=3.2s, cache=MISS, selection=0.0420s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:53:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.30% |    0.0290 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GAT, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=3.2s, cache=MISS, selection=0.0365s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:54:10] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0247 |    2.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/GIF_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:54] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.3s, cache=HIT(key=b6b6f43ac298af42a65aafe7c31a96b1), selection=0.0002s, reuse=0.004858s, speedup=0.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:54:29] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0279 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:54] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=HIT(key=f181796ac08a25e0102d20de727f981f), selection=0.0002s, reuse=0.004250s, speedup=0.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:54:47] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0270 |    2.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:54] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=2.3s, cache=HIT(key=bd755edc36ee4bac9ae3e6845d8804ab), selection=0.0002s, reuse=0.004839s, speedup=0.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:55:06] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.28% |    0.0287 |    2.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:55] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.3s, cache=HIT(key=581a09ae37a4eeb2f2a0be75ee433849), selection=0.0003s, reuse=0.008600s, speedup=0.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:55:26] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.85% |    0.0297 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:55] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=2.1s, cache=HIT(key=36014e0d1e0c5d7c829bea7a8c607b96), selection=0.0002s, reuse=0.000863s, speedup=0.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:55:46] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0254 |    1.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:55] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7823, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:56:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.43% |    0.0253 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:56] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=2.2s, cache=MISS, selection=0.0006s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:56:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.43% |    0.0288 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:56] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.1s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:56:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -0.85% |    0.0273 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:56] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.7786, time=2.3s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:57:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | 0.21% |    0.0293 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['degree'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - degree: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=2.2s, cache=MISS, selection=0.0005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:57:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| degree   | -1.08% |    0.0282 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_degree/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7860, time=2.2s, cache=HIT(key=176cebffe4617a33bb71f6f23148b125), selection=0.0376s, reuse=0.000619s, speedup=60.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:57:36] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | 0.43% |    0.0272 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.2s, cache=HIT(key=dd5ec72bf0830e7e400d928dfda320af), selection=0.0370s, reuse=0.000647s, speedup=57.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:57:53] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.43% |    0.0270 |    2.53% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7768, time=2.2s, cache=HIT(key=782302cbb08333caa37529a6731e6c2a), selection=0.0367s, reuse=0.000661s, speedup=55.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:58:10] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -1.71% |    0.0269 |    2.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.7970, time=1.9s, cache=HIT(key=05ba9c36f139f7a5fa9e15ca7ebc26d8), selection=0.0379s, reuse=0.001897s, speedup=19.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:58:27] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.22% |    0.0278 |    2.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['pagerank'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - pagerank: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=2.3s, cache=HIT(key=6b33a6ed3749f6cebd81963a30a177de), selection=0.0370s, reuse=0.004224s, speedup=8.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:58:43] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| pagerank | -0.86% |    0.0269 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_pagerank/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=2.3s, cache=HIT(key=de33487b3b2ec1fb97016a2cf85849b0), selection=4.0304s, reuse=0.004039s, speedup=997.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:59:01] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0295 |    1.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:59] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=2.3s, cache=HIT(key=872e0a1cd3d5ed6f45017171b0c2f705), selection=3.4496s, reuse=0.002809s, speedup=1228.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:59:18] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.61% |    0.0328 |    2.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:59] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=2.2s, cache=HIT(key=2458618d4cd0c8d1c95024e65fa3d288), selection=3.4869s, reuse=0.000735s, speedup=4744.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:59:35] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.16% |    0.0315 |    2.19% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:59] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=2.3s, cache=HIT(key=e8aa9284c03d06635cc8c9e0fa08b7da), selection=3.3704s, reuse=0.000798s, speedup=4223.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 06:59:52] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.75% |    0.0293 |    2.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 06:59] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=2.4s, cache=HIT(key=23c1590633c8891ebb25223cf63e3155), selection=3.8873s, reuse=0.000664s, speedup=5854.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:00:09] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.86% |    0.0294 |    2.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:00] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000646s, speedup=2422.91x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:00:28] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.43% |    0.0277 |    2.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:00] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000707s, speedup=2213.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:00:48] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.21% |    0.0281 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:00] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=2.2s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000657s, speedup=2382.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:01:10] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0293 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=2.3s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000601s, speedup=2604.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:01:31] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.65% |    0.0288 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.8s, cache=HIT(key=f8720fb27f50dfbcdbdcbb4d32f8d65d), selection=1.5652s, reuse=0.000658s, speedup=2378.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:01:50] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.21% |    0.0249 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=2.4s, cache=HIT(key=eef316a98651cf9343bd641ad8ced68b), selection=0.0416s, reuse=0.000619s, speedup=67.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:02:07] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.0257 |    1.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=2.2s, cache=HIT(key=961c74aa8a2367874e24e20f43b4ece0), selection=0.0418s, reuse=0.000748s, speedup=55.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:02:24] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.63% |    0.0311 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=2.9s, cache=HIT(key=2b9a401bc161acccc3c33ae2af90ca26), selection=0.0419s, reuse=0.001385s, speedup=30.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:02:42] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.85% |    0.0297 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=2.5s, cache=HIT(key=cfd4cc3a1bad69f5e855245c774e4e01), selection=0.0420s, reuse=0.004638s, speedup=9.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:02:59] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.65% |    0.0274 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:03] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GAT, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=2.4s, cache=HIT(key=8f3b01734e237321463cc2eb2baf31e3), selection=0.0365s, reuse=0.003746s, speedup=9.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:03:16] eval_collateral.py
- 任务：dataset=cora, model=GAT, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0247 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/IDEA_hybrid/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:29] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=34.4s, cache=MISS, selection=0.0007s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:30:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.34% |    0.2635 |   27.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:31] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=33.0s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:32:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.43% |    0.1910 |   17.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:33] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=26.8s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:34:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.70% |    0.2416 |   25.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:34] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=29.4s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:35:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -5.72% |    0.2432 |   23.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 07:36] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=33.5s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 07:37:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.23% |    0.2425 |   23.73% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 08:53] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1037.4s, cache=MISS, selection=43.0121s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 09:25:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 7.18% |    0.2567 |   25.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 09:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1321.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=43.0121s, reuse=0.001786s, speedup=24089.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 10:31:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -2.46% |    0.2438 |   24.29% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 10:56] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1447.6s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=43.0121s, reuse=0.001268s, speedup=33917.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:03] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=9083.1s, cache=MISS, selection=3731.1005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:04:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -7.14% |    0.2490 |   23.64% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:04] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:07] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=26.7s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.001671s, speedup=0.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:08:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.48% |    0.2376 |   23.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:09] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=56.2s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.025700s, speedup=0.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:09] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=54.0s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000905s, speedup=0.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:11:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -4.55% |    0.2271 |   21.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:11:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -4.55% |    0.2267 |   21.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:11] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=56.2s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.025700s, speedup=0.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:12] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7306, time=27.1s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.001209s, speedup=0.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:13] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=42.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000825s, speedup=4520326.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:13:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.53% |    0.2914 |   30.96% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:14] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=42.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.007300s, speedup=511099.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:15] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=51.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000817s, speedup=4569159.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:15:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -3.87% |    0.2531 |   27.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:16] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=42.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000825s, speedup=4522546.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:17] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=46.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000620s, speedup=6016674.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:17:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 5.94% |    0.2125 |   23.22% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:17] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=51.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000817s, speedup=4566830.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:18] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:18] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=46.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000620s, speedup=6017904.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:18] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:18] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:19] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:19] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:19] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:19] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:20] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:20] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.2s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000580s, speedup=1.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:20:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0108 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:20] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.1s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000711s, speedup=0.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:20] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:20:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0120 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:20] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.2s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.003148s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:20] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:20:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0107 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.2s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.002172s, speedup=0.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:21:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0105 |    0.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.2s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.002172s, speedup=0.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.2s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.003107s, speedup=0.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:21:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0105 |    0.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:21:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0130 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.2s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.003107s, speedup=0.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.1s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000631s, speedup=5914349.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:21:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0130 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:21:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.08% |    0.0116 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.1s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000631s, speedup=5912996.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000615s, speedup=6070352.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:22:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.08% |    0.0116 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:22:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0124 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000615s, speedup=6066830.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000788s, speedup=4732195.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:22:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0124 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:22:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000788s, speedup=4734899.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001061s, speedup=3517502.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:22:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001061s, speedup=3516588.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:22:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    0.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:22:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    0.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000673s, speedup=5541561.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000673s, speedup=5543982.91x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:22:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0135 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:23:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0135 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=4.1s, cache=MISS, selection=2.5018s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=4.1s, cache=MISS, selection=2.5018s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:23:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0154 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:23:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0154 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=3.5s, cache=MISS, selection=1.9848s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=3.4s, cache=MISS, selection=2.0432s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:23:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0153 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:23:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0153 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=4.6s, cache=MISS, selection=2.9054s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:23] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=4.0s, cache=MISS, selection=2.4321s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:23:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.07% |    0.0147 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:23:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.07% |    0.0147 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.8s, cache=MISS, selection=2.9480s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=4.7s, cache=MISS, selection=2.8454s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:24:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0143 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:24:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0143 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=4.6s, cache=MISS, selection=2.8518s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=4.4s, cache=MISS, selection=2.7331s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:24:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0152 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:24:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0152 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:24] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.2s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000625s, speedup=1.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:24] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.2s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000281s, speedup=2.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:24:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0108 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:24:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0108 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.2s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000604s, speedup=0.57x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.2s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000300s, speedup=1.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:25:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0120 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:25:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0120 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.1s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000691s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000724s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:25:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0107 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:25:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0107 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.008601s, speedup=0.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:25] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000646s, speedup=0.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:25:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0105 |    0.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:25:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0105 |    0.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.6s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.003587s, speedup=0.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.7s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.001036s, speedup=0.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:26:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0130 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:26:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.64% |    0.0130 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.002945s, speedup=1266847.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.4s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000498s, speedup=7494908.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:26:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.08% |    0.0116 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:26:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.08% |    0.0116 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.4s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000884s, speedup=4219296.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000632s, speedup=5903194.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:26:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0124 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:26:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0124 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000691s, speedup=5396334.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=2.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000282s, speedup=13239737.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:27:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:27:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.1s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000654s, speedup=5707282.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.1s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000654s, speedup=5705046.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:27:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    0.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:27:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.21% |    0.0107 |    0.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.007304s, speedup=510816.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.8s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000272s, speedup=13739569.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:27:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0135 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:27:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0135 |    0.93% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.1s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.001018s, speedup=2458.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000348s, speedup=7182.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:28:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0154 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:28:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0154 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.4s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.001209s, speedup=1690.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.1s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000300s, speedup=6806.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:28:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0153 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:28:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0153 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.001318s, speedup=1845.63x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000902s, speedup=2696.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:28:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.07% |    0.0147 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:28:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.07% |    0.0147 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.001807s, speedup=1574.91x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:28] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=2.1s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000294s, speedup=9671.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:28:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0143 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:28:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0143 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:29] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.001093s, speedup=2500.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:29] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000315s, speedup=8684.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:29:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0152 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:29:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.85% |    0.0152 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.0185 (f1_before=0.8672, f1_after=0.8487, time=1.7s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.001359s, speedup=0.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.0185 (f1_before=0.8672, f1_after=0.8487, time=2.0s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000315s, speedup=2.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:29:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.19% |    0.1898 |    6.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:29:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.19% |    0.1898 |    6.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.0517 (f1_before=0.8653, f1_after=0.8137, time=1.7s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000357s, speedup=0.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.0517 (f1_before=0.8653, f1_after=0.8137, time=1.9s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000679s, speedup=0.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:29:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.78% |    0.2027 |    8.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:29:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 7.07% |    0.2131 |   13.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0535 (f1_before=0.8672, f1_after=0.8137, time=2.1s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000388s, speedup=0.58x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:29] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0535 (f1_before=0.8672, f1_after=0.8137, time=2.2s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000685s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:30:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.91% |    0.1308 |    5.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:30:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.91% |    0.1308 |    5.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:30] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.0277 (f1_before=0.8653, f1_after=0.8376, time=2.5s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000827s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:30] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.0277 (f1_before=0.8653, f1_after=0.8376, time=2.6s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000353s, speedup=0.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:30:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.60% |    0.1477 |    8.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:30:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.60% |    0.1477 |    8.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:30] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0609 (f1_before=0.8616, f1_after=0.8007, time=2.1s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.003625s, speedup=0.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:30] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0609 (f1_before=0.8616, f1_after=0.8007, time=2.3s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.000406s, speedup=0.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:30:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.45% |    0.1364 |    7.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:30:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.45% |    0.1364 |    7.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1642 (f1_before=0.8672, f1_after=0.7030, time=2.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001948s, speedup=1915702.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1642 (f1_before=0.8672, f1_after=0.7030, time=2.1s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.003753s, speedup=994115.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:31:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 17.66% |    0.3454 |   20.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:31:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 17.66% |    0.3454 |   20.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.1882 (f1_before=0.8653, f1_after=0.6771, time=2.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000997s, speedup=3742077.86x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.1882 (f1_before=0.8653, f1_after=0.6771, time=2.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.003695s, speedup=1009701.89x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:31:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 20.38% |    0.4843 |   22.70% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:31:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.23% |    0.3236 |   18.09% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1513 (f1_before=0.8672, f1_after=0.7159, time=3.8s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000832s, speedup=4486631.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:31] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1531 (f1_before=0.8672, f1_after=0.7140, time=2.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001324s, speedup=2817675.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:31:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.50% |    0.4701 |   19.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:31:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.50% |    0.4701 |   19.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1052 (f1_before=0.8653, f1_after=0.7601, time=1.8s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001284s, speedup=2905024.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1052 (f1_before=0.8653, f1_after=0.7601, time=1.8s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001284s, speedup=2905841.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:32:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 24.68% |    0.3316 |   26.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:32:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 24.68% |    0.3316 |   26.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.1070 (f1_before=0.8616, f1_after=0.7546, time=1.8s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.014041s, speedup=265734.49x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.1070 (f1_before=0.8616, f1_after=0.7546, time=1.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000279s, speedup=13386971.44x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:32:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 15.09% |    0.4820 |   19.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:32:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 15.09% |    0.4820 |   19.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0369 (f1_before=0.8672, f1_after=0.8303, time=3.0s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000324s, speedup=7727.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:32] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0369 (f1_before=0.8672, f1_after=0.8303, time=3.1s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000717s, speedup=3488.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:32:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 2.77% |    0.1466 |    5.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:32:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 2.77% |    0.1466 |    5.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0221 (f1_before=0.8653, f1_after=0.8432, time=2.6s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000640s, speedup=3191.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0221 (f1_before=0.8653, f1_after=0.8432, time=3.6s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000762s, speedup=2682.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:33:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.50% |    0.1566 |    4.52% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0830 (f1_before=0.8672, f1_after=0.7841, time=2.6s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000958s, speedup=2537.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0221 (f1_before=0.8672, f1_after=0.8450, time=2.9s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000444s, speedup=5481.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:33:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 10.15% |    0.2599 |   15.57% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:33:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 4.23% |    0.1324 |    7.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0535 (f1_before=0.8653, f1_after=0.8118, time=2.5s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000616s, speedup=4622.24x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:33] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0535 (f1_before=0.8653, f1_after=0.8118, time=3.6s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000687s, speedup=4143.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:33:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.71% |    0.1336 |    6.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:34:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.71% |    0.1336 |    6.99% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:34] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0351 (f1_before=0.8616, f1_after=0.8266, time=2.2s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000641s, speedup=4263.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:34] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0351 (f1_before=0.8616, f1_after=0.8266, time=2.0s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000576s, speedup=4748.71x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:34:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 6.62% |    0.1278 |    9.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:34:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 6.62% |    0.1278 |    9.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.5s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000690s, speedup=0.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.5s, cache=HIT(key=e47ddf5fd2054c009114e7c2cab0b5c3), selection=0.0007s, reuse=0.000690s, speedup=1.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:34:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0196 |    1.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:34:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0196 |    1.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.5s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.014215s, speedup=0.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:34] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.5s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.014215s, speedup=0.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:34:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.86% |    0.0164 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:34:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.86% |    0.0164 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.5s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000691s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.6s, cache=HIT(key=ee087c816816de54fbd6554197d26471), selection=0.0002s, reuse=0.000333s, speedup=0.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:35:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0109 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:35:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.00% |    0.0109 |    0.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.7s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000764s, speedup=0.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.6s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000678s, speedup=0.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:35:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.0134 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:35:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.21% |    0.0134 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.5s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.003732s, speedup=0.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:35] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.6s, cache=HIT(key=d28c88645b4b41d80563b944da990368), selection=0.0003s, reuse=0.001824s, speedup=0.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:35:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0227 |    1.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:35:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0227 |    1.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.002680s, speedup=1392044.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000826s, speedup=4519020.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:36:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0183 |    1.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:36:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0183 |    1.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000626s, speedup=5959394.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=1.6s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.002744s, speedup=1359750.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:36:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0156 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:36:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0156 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000707s, speedup=5276254.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:36] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000321s, speedup=11635219.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:36:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0111 |    0.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:36:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0111 |    0.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000981s, speedup=3803005.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000938s, speedup=3975957.73x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:37:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.85% |    0.0154 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:37:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.85% |    0.0154 |    1.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000284s, speedup=13128665.79x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000631s, speedup=5912115.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:37:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0196 |    1.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:37:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0196 |    1.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.5s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000744s, speedup=3364.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.5s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000359s, speedup=6976.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:37:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0190 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:37:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.21% |    0.0190 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8579, time=1.5s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000697s, speedup=2930.85x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:37] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8579, time=1.5s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000640s, speedup=3192.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.4s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000654s, speedup=3716.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.4s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000273s, speedup=8901.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:38:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0161 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:38:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0161 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.4s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000883s, speedup=3222.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8542, time=1.4s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000328s, speedup=8673.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:38:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.0162 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:38:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.0162 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.6s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000895s, speedup=3052.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 11:38] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.6s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000303s, speedup=9019.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 11:38:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.86% |    0.0186 |    0.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 11:38:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.86% |    0.0186 |    0.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:37] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.0516 (f1_before=0.8653, f1_after=0.8137, time=1.9s, cache=HIT(key=0a90ea6605db0c5dddcecf57cf33678b), selection=0.0003s, reuse=0.000679s, speedup=0.44x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:38:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 2.78% |    0.2027 |    8.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:38] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.0277 (f1_before=0.8653, f1_after=0.8376, time=2.6s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.000353s, speedup=0.85x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:38:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.60% |    0.1477 |    8.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:38] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=9083.1s, cache=MISS, selection=3731.1005s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:39:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.88% |    0.1921 |   18.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:40] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=25.3s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001467s, speedup=2542545.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:40:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -4.73% |    0.2453 |   23.64% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:41] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=27.5s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.006058s, speedup=412.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:42:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 9.58% |    0.2765 |   28.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:43] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=25.7s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.020632s, speedup=99.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:43:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.67% |    0.1917 |   17.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:44] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=25.2s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.000959s, speedup=2536.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:45:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.23% |    0.2360 |   25.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:46] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=35.2s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.005013s, speedup=567.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:47:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.47% |    0.2400 |   22.56% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:47] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=28.7s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.001075s, speedup=2542.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:48:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.47% |    0.2317 |   21.91% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:49] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=21.9s, cache=HIT(key=81977582a5610cdbf2efe00b25a2884f), selection=0.0003s, reuse=0.013595s, speedup=0.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:49:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.42% |    0.2630 |   26.34% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:50] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=23.5s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.001226s, speedup=3042256.92x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:51:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -15.23% |    0.2680 |   25.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:51] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=51.0s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000817s, speedup=4566830.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:52:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.30% |    0.2545 |   30.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:52] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=46.2s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.000620s, speedup=6017904.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:53:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -4.51% |    0.2771 |   29.60% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:53] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=25.7s, cache=HIT(key=f69fa4c93733fcb6f946cb205d32301b), selection=2.5018s, reuse=0.000658s, speedup=3800.55x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:54:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 9.86% |    0.2702 |   24.20% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:55] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=25.6s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.000708s, speedup=2885.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:56:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.16% |    0.2711 |   28.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:56] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=25.4s, cache=HIT(key=63e11ab8b40e8799c621d10c3a954ecd), selection=2.4321s, reuse=0.003973s, speedup=612.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:57:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.2463 |   25.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:57] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=24.4s, cache=HIT(key=cd07a9b13ae587e2b546f135686bd853), selection=2.8454s, reuse=0.000674s, speedup=4218.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:58:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.83% |    0.2103 |   23.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 14:59] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=24.5s, cache=HIT(key=3127b2225ef78fbff976a29c43929c10), selection=2.7331s, reuse=0.000601s, speedup=4550.77x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 14:59:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.38% |    0.2613 |   26.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/GraphRevoker_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:00] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.7s, cache=HIT(key=5f739bf9163454950a4a07260ff8660e), selection=3731.1005s, reuse=0.002680s, speedup=1392201.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:00:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0183 |    1.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:00] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (21 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8579, time=1.4s, cache=HIT(key=17ee8f5c2b8d4222d3c406a2883e55e0), selection=2.0432s, reuse=0.004096s, speedup=498.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:00:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.22% |    0.0191 |    1.40% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.01/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:00] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=1.5s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:01:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.96% |    0.0152 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:01] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=1.3s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:01:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0160 |    1.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:01] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.6s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:01:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0146 |    1.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:01] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.2s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:02:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0145 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=2.3s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:02:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0153 |    1.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=7.0s, cache=MISS, selection=2.5835s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:02:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0163 |    0.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:02] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001115s, speedup=2317.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:03:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0163 |    1.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000578s, speedup=4468.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:03:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0156 |    1.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000801s, speedup=3224.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:03:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.43% |    0.0156 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:03] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000782s, speedup=3302.63x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:03:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.85% |    0.0164 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=4.2s, cache=MISS, selection=2.5095s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:04:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.53% |    0.0264 |    1.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=3.9s, cache=MISS, selection=2.2379s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:04:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.85% |    0.0259 |    1.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:04] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=4.3s, cache=MISS, selection=2.4653s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:05:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.74% |    0.0251 |    1.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=4.1s, cache=MISS, selection=2.3261s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:05:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.52% |    0.0274 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:05] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=4.8s, cache=MISS, selection=2.7588s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:05:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0260 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:05] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.1162 (f1_before=0.8672, f1_after=0.7509, time=2.0s, cache=HIT(key=9d38579f288c417f82d21e8182ea65ca), selection=0.0004s, reuse=0.003407s, speedup=0.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:06:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 12.53% |    0.3464 |   17.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:06] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.0904 (f1_before=0.8653, f1_after=0.7749, time=1.9s, cache=HIT(key=58063834b34c8ef2fa2b2f0276c5da20), selection=0.0004s, reuse=0.004966s, speedup=0.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:06:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.66% |    0.3541 |   13.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:06] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.0978 (f1_before=0.8672, f1_after=0.7694, time=1.9s, cache=HIT(key=981b1c52e186b16189fdf270bfc0ab5a), selection=0.0002s, reuse=0.001113s, speedup=0.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:06:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 11.88% |    0.3786 |   18.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:06] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1292 (f1_before=0.8653, f1_after=0.7362, time=1.8s, cache=HIT(key=0a99b5ed4c5e95151750eaa484708672), selection=0.0003s, reuse=0.000691s, speedup=0.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:07:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 18.67% |    0.3934 |   27.54% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0461 (f1_before=0.8616, f1_after=0.8155, time=1.9s, cache=HIT(key=fedae5d010111de0b778a6c58f2f79d6), selection=0.0003s, reuse=0.000986s, speedup=0.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:07:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.85% |    0.3395 |   16.26% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1937 (f1_before=0.8672, f1_after=0.6734, time=2.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001003s, speedup=2576.91x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:07:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 13.01% |    0.3814 |   19.49% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:07] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.1882 (f1_before=0.8653, f1_after=0.6771, time=2.6s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000737s, speedup=3504.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:08:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 10.85% |    0.3605 |   15.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1734 (f1_before=0.8672, f1_after=0.6937, time=1.8s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000749s, speedup=3447.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:08:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 9.68% |    0.3644 |   13.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1568 (f1_before=0.8653, f1_after=0.7085, time=2.5s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000741s, speedup=3487.58x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:08:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 9.89% |    0.4088 |   15.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.1218 (f1_before=0.8616, f1_after=0.7399, time=1.6s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000681s, speedup=3794.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:08:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 20.43% |    0.3822 |   28.56% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:09] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0683 (f1_before=0.8672, f1_after=0.7989, time=2.9s, cache=HIT(key=924e6c8bbb3190ee333d1dc89951ab95), selection=2.5095s, reuse=0.001263s, speedup=1987.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:09:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 9.05% |    0.3044 |   14.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:09] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0664 (f1_before=0.8653, f1_after=0.7989, time=2.1s, cache=HIT(key=ed8b5cda8509acfbe9aeecb90f9a73ff), selection=2.2379s, reuse=0.001029s, speedup=2174.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:09:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 6.14% |    0.2511 |   10.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:09] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0775 (f1_before=0.8672, f1_after=0.7897, time=2.1s, cache=HIT(key=794bf964e39e86c0425585102c9e1467), selection=2.4653s, reuse=0.001530s, speedup=1611.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:10:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.77% |    0.1952 |    5.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0738 (f1_before=0.8653, f1_after=0.7915, time=2.7s, cache=HIT(key=9e373fc4407c38dfa0b8fa7c27e40588), selection=2.3261s, reuse=0.000971s, speedup=2394.81x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:10:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 4.21% |    0.2018 |   10.00% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0904 (f1_before=0.8616, f1_after=0.7712, time=3.1s, cache=HIT(key=5bf71c8559d6765943abb63ee9f7c591), selection=2.7588s, reuse=0.005217s, speedup=528.85x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:10:52] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 12.10% |    0.2191 |   15.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:11] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=43.2s, cache=HIT(key=9d38579f288c417f82d21e8182ea65ca), selection=0.0004s, reuse=0.003751s, speedup=0.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:12:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 12.96% |    0.2885 |   29.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:13] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=33.8s, cache=HIT(key=58063834b34c8ef2fa2b2f0276c5da20), selection=0.0004s, reuse=0.000792s, speedup=0.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:14:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.65% |    0.1924 |   19.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:15] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=35.1s, cache=HIT(key=981b1c52e186b16189fdf270bfc0ab5a), selection=0.0002s, reuse=0.000739s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:16:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.25% |    0.2424 |   26.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:17] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=33.6s, cache=HIT(key=0a99b5ed4c5e95151750eaa484708672), selection=0.0003s, reuse=0.000748s, speedup=0.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:18:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.01% |    0.2595 |   26.05% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=32.4s, cache=HIT(key=fedae5d010111de0b778a6c58f2f79d6), selection=0.0003s, reuse=0.000875s, speedup=0.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:19:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.74% |    0.2424 |   22.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=33.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001430s, speedup=1806.89x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:21:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 10.42% |    0.2676 |   27.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:22] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=31.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000696s, speedup=3712.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:23:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 1.18% |    0.1957 |   17.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:23] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=34.3s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000769s, speedup=3358.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:24:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.23% |    0.2527 |   26.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:25] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=36.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000890s, speedup=2901.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:26:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.2771 |   28.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:27] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=35.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001083s, speedup=2386.24x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:28:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.72% |    0.2473 |   23.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:29] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=32.3s, cache=HIT(key=924e6c8bbb3190ee333d1dc89951ab95), selection=2.5095s, reuse=0.000903s, speedup=2778.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:30:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 18.06% |    0.3078 |   31.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:30] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=36.3s, cache=HIT(key=ed8b5cda8509acfbe9aeecb90f9a73ff), selection=2.2379s, reuse=0.001097s, speedup=2039.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:31:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.89% |    0.1784 |   16.56% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:32] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=34.1s, cache=HIT(key=794bf964e39e86c0425585102c9e1467), selection=2.4653s, reuse=0.000745s, speedup=3308.88x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:33:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.72% |    0.2489 |   23.49% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:34] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=34.3s, cache=HIT(key=9e373fc4407c38dfa0b8fa7c27e40588), selection=2.3261s, reuse=0.000825s, speedup=2820.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:35:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -4.04% |    0.2330 |   22.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:36] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=36.0s, cache=HIT(key=5bf71c8559d6765943abb63ee9f7c591), selection=2.7588s, reuse=0.004383s, speedup=629.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:37:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.94% |    0.2194 |   19.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:37] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=30.7s, cache=HIT(key=9d38579f288c417f82d21e8182ea65ca), selection=0.0004s, reuse=0.000701s, speedup=0.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:38:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.83% |    0.3269 |   32.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:39] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7140, time=31.0s, cache=HIT(key=58063834b34c8ef2fa2b2f0276c5da20), selection=0.0004s, reuse=0.001420s, speedup=0.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:40:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 3.07% |    0.2712 |   28.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:40] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7140, time=31.2s, cache=HIT(key=981b1c52e186b16189fdf270bfc0ab5a), selection=0.0002s, reuse=0.000851s, speedup=0.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:41:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.61% |    0.2385 |   25.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:42] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=30.3s, cache=HIT(key=0a99b5ed4c5e95151750eaa484708672), selection=0.0003s, reuse=0.000510s, speedup=0.49x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 15:43] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=29.8s, cache=HIT(key=fedae5d010111de0b778a6c58f2f79d6), selection=0.0003s, reuse=0.000679s, speedup=0.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:44:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.97% |    0.2597 |   27.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:45] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=29.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000829s, speedup=3114.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:46:10] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.32% |    0.3334 |   32.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:46] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=31.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.002429s, speedup=1063.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:47:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -3.37% |    0.2585 |   25.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:48] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=29.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000686s, speedup=3765.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:49:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.85% |    0.2536 |   25.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:49] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=30.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000831s, speedup=3108.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:50:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -4.89% |    0.2280 |   24.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:51] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=31.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.003495s, speedup=739.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:52:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 8.93% |    0.3228 |   32.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:52] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=30.1s, cache=HIT(key=924e6c8bbb3190ee333d1dc89951ab95), selection=2.5095s, reuse=0.000983s, speedup=2553.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:53:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.98% |    0.2570 |   23.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:54] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7288, time=28.7s, cache=HIT(key=ed8b5cda8509acfbe9aeecb90f9a73ff), selection=2.2379s, reuse=0.000917s, speedup=2440.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:55:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.48% |    0.2384 |   24.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:55] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=31.3s, cache=HIT(key=794bf964e39e86c0425585102c9e1467), selection=2.4653s, reuse=0.004043s, speedup=609.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:56:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 5.00% |    0.2978 |   29.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:57] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7085, time=40.3s, cache=HIT(key=9e373fc4407c38dfa0b8fa7c27e40588), selection=2.3261s, reuse=0.001130s, speedup=2058.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 15:58:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -4.13% |    0.2302 |   22.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 15:59] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=42.2s, cache=HIT(key=5bf71c8559d6765943abb63ee9f7c591), selection=2.7588s, reuse=0.001124s, speedup=2453.60x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:01:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -9.44% |    0.2624 |   29.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/GraphRevoker_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.4s, cache=HIT(key=9d38579f288c417f82d21e8182ea65ca), selection=0.0004s, reuse=0.002927s, speedup=0.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:01:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.96% |    0.0152 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.4s, cache=HIT(key=58063834b34c8ef2fa2b2f0276c5da20), selection=0.0004s, reuse=0.002680s, speedup=0.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:01:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.64% |    0.0160 |    1.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:01] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=981b1c52e186b16189fdf270bfc0ab5a), selection=0.0002s, reuse=0.000786s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:02:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0146 |    1.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.2s, cache=HIT(key=0a99b5ed4c5e95151750eaa484708672), selection=0.0003s, reuse=0.000673s, speedup=0.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:02:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.86% |    0.0145 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=HIT(key=fedae5d010111de0b778a6c58f2f79d6), selection=0.0003s, reuse=0.000634s, speedup=0.49x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:02:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.43% |    0.0153 |    1.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:02] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000994s, speedup=2599.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:02:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0163 |    0.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:03] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000708s, speedup=3648.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:03:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0163 |    1.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:03] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.3s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001217s, speedup=2122.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:03:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.64% |    0.0156 |    1.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:03] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.3s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000852s, speedup=3033.57x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:03:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.43% |    0.0156 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:03] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.0s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000844s, speedup=3060.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:04:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.85% |    0.0164 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:04] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.4s, cache=HIT(key=924e6c8bbb3190ee333d1dc89951ab95), selection=2.5095s, reuse=0.000731s, speedup=3432.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:04:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.53% |    0.0264 |    1.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:04] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=ed8b5cda8509acfbe9aeecb90f9a73ff), selection=2.2379s, reuse=0.001154s, speedup=1939.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:04:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.85% |    0.0259 |    1.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:04] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.3s, cache=HIT(key=794bf964e39e86c0425585102c9e1467), selection=2.4653s, reuse=0.000675s, speedup=3652.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:04:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.74% |    0.0251 |    1.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:05] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.1s, cache=HIT(key=9e373fc4407c38dfa0b8fa7c27e40588), selection=2.3261s, reuse=0.000629s, speedup=3697.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:05:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.52% |    0.0274 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:05] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.2s, cache=HIT(key=5bf71c8559d6765943abb63ee9f7c591), selection=2.7588s, reuse=0.003119s, speedup=884.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:05:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.43% |    0.0260 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=9d38579f288c417f82d21e8182ea65ca), selection=0.0004s, reuse=0.003669s, speedup=0.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:05:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.65% |    0.0221 |    1.49% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.4s, cache=HIT(key=58063834b34c8ef2fa2b2f0276c5da20), selection=0.0004s, reuse=0.003504s, speedup=0.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:06:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0192 |    1.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=981b1c52e186b16189fdf270bfc0ab5a), selection=0.0002s, reuse=0.003485s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:06:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.73% |    0.0145 |    1.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.5s, cache=HIT(key=0a99b5ed4c5e95151750eaa484708672), selection=0.0003s, reuse=0.001215s, speedup=0.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:06:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0190 |    1.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:07] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.4s, cache=HIT(key=fedae5d010111de0b778a6c58f2f79d6), selection=0.0003s, reuse=0.000737s, speedup=0.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:07:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.22% |    0.0221 |    1.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:07] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=2.1s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000795s, speedup=3251.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:07:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0229 |    1.49% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:07] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.5s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000469s, speedup=5511.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:08:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0210 |    1.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:08] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000847s, speedup=3050.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:08:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0157 |    1.18% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:08] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.5s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.001528s, speedup=1691.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:08:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.65% |    0.0206 |    1.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:08] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.4s, cache=HIT(key=98b37d4ca306865f7947cb56fa842642), selection=2.5835s, reuse=0.000803s, speedup=3217.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:08:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.22% |    0.0239 |    1.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:09] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.4s, cache=HIT(key=924e6c8bbb3190ee333d1dc89951ab95), selection=2.5095s, reuse=0.000482s, speedup=5205.44x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:09:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.85% |    0.0271 |    1.03% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:09] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.7s, cache=HIT(key=ed8b5cda8509acfbe9aeecb90f9a73ff), selection=2.2379s, reuse=0.000970s, speedup=2307.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:09:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.10% |    0.0253 |    1.13% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:09] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.4s, cache=HIT(key=794bf964e39e86c0425585102c9e1467), selection=2.4653s, reuse=0.000931s, speedup=2647.27x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:09:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.30% |    0.0245 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:10] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.3s, cache=HIT(key=9e373fc4407c38dfa0b8fa7c27e40588), selection=2.3261s, reuse=0.000672s, speedup=3462.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:10:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.86% |    0.0227 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 16:10] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.1
- 配置：unlearn_ratio=0.1 (216 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.4s, cache=HIT(key=5bf71c8559d6765943abb63ee9f7c591), selection=2.7588s, reuse=0.000647s, speedup=4266.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 16:10:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.1
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.08% |    0.0246 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.1/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:06] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:06:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.53% |    0.0206 |    1.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.3s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:07:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.85% |    0.0192 |    1.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.1s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:07:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.07% |    0.0200 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=1.2s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:07:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.08% |    0.0169 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:07] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.4s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:08:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.22% |    0.0192 |    1.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=7.4s, cache=MISS, selection=1.9343s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:08:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.30% |    0.0202 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.1s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.001612s, speedup=1199.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:08:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0197 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.7s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000651s, speedup=2969.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:09:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.29% |    0.0201 |    1.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.1s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.001159s, speedup=1668.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:09:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.29% |    0.0195 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.1s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000714s, speedup=2709.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:09:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0200 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=4.5s, cache=MISS, selection=2.3880s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:09:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -7.32% |    0.0305 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=2.7s, cache=MISS, selection=1.2172s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:10:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.16% |    0.0309 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=3.9s, cache=MISS, selection=2.2985s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:10:38] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.32% |    0.0291 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:10] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=3.7s, cache=MISS, selection=2.1128s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:11:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.58% |    0.0325 |    1.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:11] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=4.1s, cache=MISS, selection=2.4745s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:11:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.56% |    0.0297 |    1.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.1458 (f1_before=0.8672, f1_after=0.7214, time=1.7s, cache=HIT(key=6d9d442b17df64065c30f3166d2cbf6e), selection=0.0002s, reuse=0.000809s, speedup=0.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:11:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 13.51% |    0.4554 |   18.23% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.2011 (f1_before=0.8653, f1_after=0.6642, time=1.9s, cache=HIT(key=4ac5a54de5ad706f40c3b8e9a959f4f4), selection=0.0003s, reuse=0.001310s, speedup=0.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:12:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 5.42% |    0.4149 |   10.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.2399 (f1_before=0.8672, f1_after=0.6273, time=1.9s, cache=HIT(key=f7fa5e9ff678bbb25a7b3b10a586cf14), selection=0.0003s, reuse=0.000835s, speedup=0.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:12:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 25.70% |    0.4037 |   29.20% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1863 (f1_before=0.8653, f1_after=0.6790, time=2.1s, cache=HIT(key=fec1b58e648a1d725ecdb271610a9025), selection=0.0003s, reuse=0.000830s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:12:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 13.70% |    0.3595 |   22.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.0720 (f1_before=0.8616, f1_after=0.7897, time=1.9s, cache=HIT(key=eaf054688d6fa7c3b938ce01a437472a), selection=0.0003s, reuse=0.000757s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:12:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 12.69% |    0.3312 |   17.95% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.1402 (f1_before=0.8672, f1_after=0.7269, time=2.7s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000739s, speedup=2617.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:13:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.38% |    0.4502 |   19.39% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = 0.0775 (f1_before=0.8653, f1_after=0.7878, time=2.0s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000852s, speedup=2269.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:13:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 12.26% |    0.4510 |   19.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:13] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = 0.1273 (f1_before=0.8672, f1_after=0.7399, time=1.9s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000767s, speedup=2523.53x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:13:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 15.88% |    0.3790 |   22.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = 0.1439 (f1_before=0.8653, f1_after=0.7214, time=1.8s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000730s, speedup=2649.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:14:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 20.86% |    0.4054 |   29.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = 0.1162 (f1_before=0.8616, f1_after=0.7454, time=2.0s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000762s, speedup=2536.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:14:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 15.27% |    0.3834 |   19.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:14] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.1476 (f1_before=0.8672, f1_after=0.7196, time=2.3s, cache=HIT(key=ded8c70a4eeaadd5d8d6f0b7522da7f1), selection=2.3880s, reuse=0.001913s, speedup=1248.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:14:54] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 6.32% |    0.2235 |   11.89% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0572 (f1_before=0.8653, f1_after=0.8081, time=2.3s, cache=HIT(key=aa418e5cf08e8a96b23b12ff01efc0f9), selection=1.2172s, reuse=0.001239s, speedup=982.77x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:15:15] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 4.03% |    0.1952 |   12.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.1144 (f1_before=0.8672, f1_after=0.7528, time=1.6s, cache=HIT(key=76677e0ec904c5e68579e65e65514f21), selection=2.2985s, reuse=0.004902s, speedup=468.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:15:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 3.39% |    0.1972 |    9.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:15] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.1015 (f1_before=0.8653, f1_after=0.7638, time=3.3s, cache=HIT(key=4bce9005a220ab503fecd5589ed005ae), selection=2.1128s, reuse=0.005098s, speedup=414.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:16:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.05% |    0.2059 |   11.54% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:16] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.1162 (f1_before=0.8616, f1_after=0.7454, time=2.8s, cache=HIT(key=650995eb5983b200515bfa16025d427d), selection=2.4745s, reuse=0.003684s, speedup=671.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:16:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 8.26% |    0.1762 |   11.14% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:17] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=36.7s, cache=HIT(key=6d9d442b17df64065c30f3166d2cbf6e), selection=0.0002s, reuse=0.001155s, speedup=0.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:18:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 15.28% |    0.2940 |   30.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=31.2s, cache=HIT(key=4ac5a54de5ad706f40c3b8e9a959f4f4), selection=0.0003s, reuse=0.000750s, speedup=0.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:19:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.42% |    0.1980 |   18.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=32.6s, cache=HIT(key=f7fa5e9ff678bbb25a7b3b10a586cf14), selection=0.0003s, reuse=0.000774s, speedup=0.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:21:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.47% |    0.2494 |   25.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:22] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=36.3s, cache=HIT(key=fec1b58e648a1d725ecdb271610a9025), selection=0.0003s, reuse=0.000741s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:23:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.78% |    0.2606 |   26.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:24] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=35.8s, cache=HIT(key=eaf054688d6fa7c3b938ce01a437472a), selection=0.0003s, reuse=0.000747s, speedup=0.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:25:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.72% |    0.2410 |   22.27% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:26] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=34.2s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.004541s, speedup=425.95x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:27:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 14.58% |    0.2951 |   31.74% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:27] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=35.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000660s, speedup=2932.11x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:28:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.24% |    0.2027 |   17.20% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:29] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=34.0s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000672s, speedup=2880.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:30:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.98% |    0.2588 |   27.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:31] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=42.2s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.003221s, speedup=600.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:32:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.51% |    0.2664 |   27.47% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:33] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=33.3s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000738s, speedup=2619.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:34:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.47% |    0.2602 |   24.06% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:35] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8007, time=32.5s, cache=HIT(key=ded8c70a4eeaadd5d8d6f0b7522da7f1), selection=2.3880s, reuse=0.000776s, speedup=3076.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:36:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 15.51% |    0.3244 |   32.37% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:36] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=35.1s, cache=HIT(key=aa418e5cf08e8a96b23b12ff01efc0f9), selection=1.2172s, reuse=0.000750s, speedup=1623.89x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:38:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 3.07% |    0.1887 |   17.25% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:38] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8007, time=38.4s, cache=HIT(key=76677e0ec904c5e68579e65e65514f21), selection=2.2985s, reuse=0.000760s, speedup=3023.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:40:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 6.37% |    0.2833 |   26.02% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:40] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7934, time=37.9s, cache=HIT(key=4bce9005a220ab503fecd5589ed005ae), selection=2.1128s, reuse=0.000714s, speedup=2960.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:41:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.27% |    0.2277 |   20.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:42] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=32.2s, cache=HIT(key=650995eb5983b200515bfa16025d427d), selection=2.4745s, reuse=0.000762s, speedup=3247.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:43:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -2.70% |    0.2343 |   20.54% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:44] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7085, time=28.9s, cache=HIT(key=6d9d442b17df64065c30f3166d2cbf6e), selection=0.0002s, reuse=0.000791s, speedup=0.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:45:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.03% |    0.2875 |   30.01% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:46] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7232, time=36.0s, cache=HIT(key=4ac5a54de5ad706f40c3b8e9a959f4f4), selection=0.0003s, reuse=0.003536s, speedup=0.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:47:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 10.56% |    0.3568 |   35.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:47] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=29.8s, cache=HIT(key=f7fa5e9ff678bbb25a7b3b10a586cf14), selection=0.0003s, reuse=0.000821s, speedup=0.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:48:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.40% |    0.2625 |   25.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:49] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=29.4s, cache=HIT(key=fec1b58e648a1d725ecdb271610a9025), selection=0.0003s, reuse=0.000742s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 17:50] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7159, time=28.5s, cache=HIT(key=eaf054688d6fa7c3b938ce01a437472a), selection=0.0003s, reuse=0.000790s, speedup=0.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:51:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 4.00% |    0.4071 |   42.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:52] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7103, time=29.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.001225s, speedup=1578.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:53:03] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -6.93% |    0.2821 |   32.20% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:53] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7196, time=31.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000848s, speedup=2280.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:54:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.28% |    0.2973 |   28.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:55] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=29.2s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000803s, speedup=2409.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:56:08] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -2.56% |    0.2765 |   29.08% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:56] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7362, time=29.3s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.002451s, speedup=789.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:57:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 5.18% |    0.2246 |   25.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:58] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.7269, time=29.8s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000777s, speedup=2487.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 17:59:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.97% |    0.2860 |   29.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 17:59] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7491, time=31.4s, cache=HIT(key=ded8c70a4eeaadd5d8d6f0b7522da7f1), selection=2.3880s, reuse=0.000803s, speedup=2975.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:00:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.72% |    0.2988 |   24.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:01] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7214, time=32.7s, cache=HIT(key=aa418e5cf08e8a96b23b12ff01efc0f9), selection=1.2172s, reuse=0.004300s, speedup=283.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:02:28] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.00% |    0.2879 |   26.43% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:03] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7288, time=30.0s, cache=HIT(key=76677e0ec904c5e68579e65e65514f21), selection=2.2985s, reuse=0.000743s, speedup=3094.84x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:03:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.19% |    0.2277 |   22.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:04] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=28.0s, cache=HIT(key=4bce9005a220ab503fecd5589ed005ae), selection=2.1128s, reuse=0.000950s, speedup=2224.34x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:05:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.2431 |   25.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:06] demo_attack.py - GraphRevoker 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphRevoker, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7177, time=33.8s, cache=HIT(key=650995eb5983b200515bfa16025d427d), selection=2.4745s, reuse=0.003740s, speedup=661.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:07:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphRevoker, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.94% |    0.2312 |   23.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/GraphRevoker_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.4s, cache=HIT(key=6d9d442b17df64065c30f3166d2cbf6e), selection=0.0002s, reuse=0.000701s, speedup=0.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:07:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -3.53% |    0.0206 |    1.10% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.3s, cache=HIT(key=4ac5a54de5ad706f40c3b8e9a959f4f4), selection=0.0003s, reuse=0.000798s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:07:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.85% |    0.0192 |    1.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.4s, cache=HIT(key=f7fa5e9ff678bbb25a7b3b10a586cf14), selection=0.0003s, reuse=0.000779s, speedup=0.42x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:07:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.07% |    0.0200 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.7s, cache=HIT(key=fec1b58e648a1d725ecdb271610a9025), selection=0.0003s, reuse=0.000766s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:08:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.08% |    0.0169 |    0.63% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.2s, cache=HIT(key=eaf054688d6fa7c3b938ce01a437472a), selection=0.0003s, reuse=0.000692s, speedup=0.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:08:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.22% |    0.0192 |    1.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.1s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000717s, speedup=2697.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:08:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.30% |    0.0202 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.3s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000726s, speedup=2662.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:09:11] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.86% |    0.0197 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.6s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000845s, speedup=2287.97x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:09:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.29% |    0.0201 |    1.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=2.1s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000771s, speedup=2508.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:09:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.29% |    0.0195 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.3s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000835s, speedup=2317.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:10:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.64% |    0.0200 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=ded8c70a4eeaadd5d8d6f0b7522da7f1), selection=2.3880s, reuse=0.000762s, speedup=3131.96x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:10:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -7.32% |    0.0305 |    1.15% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.2s, cache=HIT(key=aa418e5cf08e8a96b23b12ff01efc0f9), selection=1.2172s, reuse=0.004163s, speedup=292.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:10:46] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.16% |    0.0309 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=HIT(key=76677e0ec904c5e68579e65e65514f21), selection=2.2985s, reuse=0.003519s, speedup=653.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:11:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.32% |    0.0291 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:11] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.3s, cache=HIT(key=4bce9005a220ab503fecd5589ed005ae), selection=2.1128s, reuse=0.004776s, speedup=442.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:11:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.58% |    0.0325 |    1.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:11] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=1.3s, cache=HIT(key=650995eb5983b200515bfa16025d427d), selection=2.4745s, reuse=0.001205s, speedup=2053.98x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:11:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.56% |    0.0297 |    1.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:11] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.4s, cache=HIT(key=6d9d442b17df64065c30f3166d2cbf6e), selection=0.0002s, reuse=0.000747s, speedup=0.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:12:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -2.19% |    0.0264 |    1.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:12] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.5s, cache=HIT(key=4ac5a54de5ad706f40c3b8e9a959f4f4), selection=0.0003s, reuse=0.000798s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:12:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.31% |    0.0225 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:12] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.5s, cache=HIT(key=f7fa5e9ff678bbb25a7b3b10a586cf14), selection=0.0003s, reuse=0.000872s, speedup=0.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:12:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.21% |    0.0196 |    1.38% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:12] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.6s, cache=HIT(key=fec1b58e648a1d725ecdb271610a9025), selection=0.0003s, reuse=0.000771s, speedup=0.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:12:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -1.08% |    0.0220 |    1.44% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['random'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.4s, cache=HIT(key=eaf054688d6fa7c3b938ce01a437472a), selection=0.0003s, reuse=0.001086s, speedup=0.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:13:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0253 |    1.85% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000813s, speedup=2379.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:13:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.43% |    0.0248 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8413, time=1.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000802s, speedup=2411.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:13:48] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.00% |    0.0243 |    1.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_im/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.4s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.001149s, speedup=1683.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:14:06] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.29% |    0.0198 |    1.27% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_im/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:14] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.4s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000756s, speedup=2557.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:14:23] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -1.30% |    0.0240 |    1.90% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_im/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:14] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['im'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.5s, cache=HIT(key=cc325476cc84b8e021041ff4878373c2), selection=1.9343s, reuse=0.000719s, speedup=2690.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:14:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | -0.22% |    0.0267 |    1.96% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_im/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:14] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=2.0s, cache=HIT(key=ded8c70a4eeaadd5d8d6f0b7522da7f1), selection=2.3880s, reuse=0.000821s, speedup=2908.25x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:15:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -6.12% |    0.0301 |    1.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:15] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=1.5s, cache=HIT(key=aa418e5cf08e8a96b23b12ff01efc0f9), selection=1.2172s, reuse=0.001333s, speedup=913.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:15:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.43% |    0.0293 |    1.27% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:15] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8469, time=1.5s, cache=HIT(key=76677e0ec904c5e68579e65e65514f21), selection=2.2985s, reuse=0.002875s, speedup=799.57x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:15:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.84% |    0.0277 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:15] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.5s, cache=HIT(key=4bce9005a220ab503fecd5589ed005ae), selection=2.1128s, reuse=0.002974s, speedup=710.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:16:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -5.64% |    0.0258 |    0.98% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:16] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['tracin'], ratio=0.2
- 配置：unlearn_ratio=0.2 (433 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=HIT(key=650995eb5983b200515bfa16025d427d), selection=2.4745s, reuse=0.003311s, speedup=747.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:16:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.2
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -3.77% |    0.0253 |    1.04% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.2/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=2.0s, cache=MISS, selection=0.1799s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:21:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:21] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=3.1s, cache=MISS, selection=0.0697s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:22:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.9s, cache=MISS, selection=0.0602s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:22:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.7s, cache=MISS, selection=0.1979s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:22:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:22] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.5s, cache=MISS, selection=0.0600s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:22:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1384 (f1_before=0.8672, f1_after=0.7288, time=2.1s, cache=HIT(key=e152c45f7f2613c698a4a78b878b8767), selection=0.1799s, reuse=0.001081s, speedup=166.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:23:17] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 18.38% |    0.4779 |   22.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.2048 (f1_before=0.8653, f1_after=0.6605, time=2.1s, cache=HIT(key=e281ab5a57d9747d054fbf65699281f0), selection=0.0697s, reuse=0.001677s, speedup=41.57x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:23:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.13% |    0.3843 |   15.01% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:23] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.1421 (f1_before=0.8672, f1_after=0.7251, time=2.8s, cache=HIT(key=973a9b5bb97a7c2976894619f1385559), selection=0.0602s, reuse=0.001182s, speedup=50.95x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:23:57] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.21% |    0.1930 |   15.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:24] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.1974 (f1_before=0.8653, f1_after=0.6679, time=1.9s, cache=HIT(key=f4a427e7a28ee7f2994b0c79e43e48a6), selection=0.1979s, reuse=0.001889s, speedup=104.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:24:16] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 10.78% |    0.2538 |   14.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:24] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.1125 (f1_before=0.8616, f1_after=0.7491, time=1.9s, cache=HIT(key=f19b118e386e18defc2cfd68e5360af2), selection=0.0600s, reuse=0.000621s, speedup=96.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:24:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 7.73% |    0.2010 |   10.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:24] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.5s, cache=HIT(key=e152c45f7f2613c698a4a78b878b8767), selection=0.1799s, reuse=0.000707s, speedup=254.33x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:24] demo_attack.py - GIF 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6818, time=31.1s, cache=MISS, selection=0.0021s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:24:55] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0206 |    1.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=e281ab5a57d9747d054fbf65699281f0), selection=0.0697s, reuse=0.000724s, speedup=96.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:25:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0177 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.4s, cache=HIT(key=973a9b5bb97a7c2976894619f1385559), selection=0.0602s, reuse=0.000592s, speedup=101.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:25:32] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.21% |    0.0126 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:25] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.5s, cache=HIT(key=f4a427e7a28ee7f2994b0c79e43e48a6), selection=0.1979s, reuse=0.004815s, speedup=41.09x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:25:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0181 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:26] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.6s, cache=HIT(key=f19b118e386e18defc2cfd68e5360af2), selection=0.0600s, reuse=0.003376s, speedup=17.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:26:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0217 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=1.3s, cache=HIT(key=e152c45f7f2613c698a4a78b878b8767), selection=0.1799s, reuse=0.003823s, speedup=47.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:26:33] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.08% |    0.0129 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:26:38] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.25% |    0.0383 |    4.82% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:26] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.3s, cache=HIT(key=e281ab5a57d9747d054fbf65699281f0), selection=0.0697s, reuse=0.002515s, speedup=27.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:26:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.21% |    0.0134 |    1.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.4s, cache=HIT(key=973a9b5bb97a7c2976894619f1385559), selection=0.0602s, reuse=0.000735s, speedup=82.01x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:27:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:27] demo_attack.py - GIF 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.6786, time=31.1s, cache=HIT(key=c20b2c24de53ecb82242fdee3d0be954), selection=5110.1408s, reuse=0.001136s, speedup=4499996.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.3s, cache=HIT(key=f4a427e7a28ee7f2994b0c79e43e48a6), selection=0.1979s, reuse=0.000721s, speedup=274.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:27:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:27] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=1.2s, cache=HIT(key=f19b118e386e18defc2cfd68e5360af2), selection=0.0600s, reuse=0.000694s, speedup=86.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:27:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:28] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=32.9s, cache=HIT(key=e152c45f7f2613c698a4a78b878b8767), selection=0.1799s, reuse=0.000675s, speedup=266.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:28:43] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.14% |    0.0422 |    4.99% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:29] demo_attack.py - GIF 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - im: F1 Drop = NA (f1_before=NA, f1_after=0.6783, time=31.0s, cache=HIT(key=ce8117dc5bf55cbad0eceba989b3e5e2), selection=1722.0304s, reuse=0.001730s, speedup=995550.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:29:34] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 15.97% |    0.3172 |   32.75% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:30] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=35.9s, cache=HIT(key=e281ab5a57d9747d054fbf65699281f0), selection=0.0697s, reuse=0.000766s, speedup=90.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:30:47] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GIF, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 0.35% |    0.0417 |    5.14% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GIF_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:31:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.36% |    0.1839 |   16.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:32] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=37.5s, cache=HIT(key=973a9b5bb97a7c2976894619f1385559), selection=0.0602s, reuse=0.000847s, speedup=71.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:33:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.74% |    0.2530 |   27.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:33] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=34.1s, cache=HIT(key=f4a427e7a28ee7f2994b0c79e43e48a6), selection=0.1979s, reuse=0.001080s, speedup=183.28x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:35:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -4.80% |    0.2406 |   23.42% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:35] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=33.8s, cache=HIT(key=f19b118e386e18defc2cfd68e5360af2), selection=0.0600s, reuse=0.001166s, speedup=51.46x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:36:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.98% |    0.2390 |   22.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.7s, cache=MISS, selection=0.0466s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:37:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.25/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.6s, cache=MISS, selection=0.0447s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:37:31] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.25/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.6s, cache=MISS, selection=0.0464s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:37:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.25/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:37] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=1.7s, cache=MISS, selection=0.0471s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:38:07] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.25/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:38] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.6s, cache=MISS, selection=0.0437s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:38:25] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.25/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:38] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.1494 (f1_before=0.8672, f1_after=0.7177, time=1.9s, cache=HIT(key=bd145390297fc10ce7469a55c3a79395), selection=0.0466s, reuse=0.001545s, speedup=30.15x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:38:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 18.38% |    0.4779 |   22.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.25/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:38] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.1993 (f1_before=0.8653, f1_after=0.6661, time=1.9s, cache=HIT(key=21e12b819911413d9cbcd128590d5dbd), selection=0.0447s, reuse=0.001245s, speedup=35.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:39:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 14.07% |    0.3895 |   16.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.25/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:39] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.1476 (f1_before=0.8672, f1_after=0.7196, time=1.7s, cache=HIT(key=c92e8e9b9b19fdbcc8156fd0a5ba414b), selection=0.0464s, reuse=0.002107s, speedup=22.00x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:39:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.21% |    0.1930 |   15.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.25/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:39] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.1458 (f1_before=0.8653, f1_after=0.7196, time=1.9s, cache=HIT(key=a373bc3416f7e309019d2176c5d2b3ae), selection=0.0471s, reuse=0.001202s, speedup=39.21x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:39:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 10.78% |    0.2538 |   14.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.25/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:39] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.1181 (f1_before=0.8616, f1_after=0.7435, time=1.8s, cache=HIT(key=ca2a5e12f3a93b645c5f2e4a1973d73f), selection=0.0437s, reuse=0.001976s, speedup=22.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:40:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 7.73% |    0.2010 |   10.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.25/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:40] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.3s, cache=HIT(key=bd145390297fc10ce7469a55c3a79395), selection=0.0466s, reuse=0.000882s, speedup=52.83x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:40:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0206 |    1.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.25/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:40] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=21e12b819911413d9cbcd128590d5dbd), selection=0.0447s, reuse=0.004231s, speedup=10.56x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:40:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0177 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.25/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:40] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.6s, cache=HIT(key=c92e8e9b9b19fdbcc8156fd0a5ba414b), selection=0.0464s, reuse=0.003826s, speedup=12.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:40:58] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.21% |    0.0126 |    0.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.25/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:41] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=1.6s, cache=HIT(key=a373bc3416f7e309019d2176c5d2b3ae), selection=0.0471s, reuse=0.003591s, speedup=13.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:41:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0181 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.25/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:41] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.4s, cache=HIT(key=ca2a5e12f3a93b645c5f2e4a1973d73f), selection=0.0437s, reuse=0.002108s, speedup=20.71x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:41:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0217 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.25/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:41] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.1s, cache=HIT(key=bd145390297fc10ce7469a55c3a79395), selection=0.0466s, reuse=0.000643s, speedup=72.43x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:41:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0146 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.25/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.0s, cache=HIT(key=21e12b819911413d9cbcd128590d5dbd), selection=0.0447s, reuse=0.000682s, speedup=65.51x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:42:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0154 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.25/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.2s, cache=HIT(key=c92e8e9b9b19fdbcc8156fd0a5ba414b), selection=0.0464s, reuse=0.000830s, speedup=55.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:42:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.25/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.2s, cache=HIT(key=a373bc3416f7e309019d2176c5d2b3ae), selection=0.0471s, reuse=0.000683s, speedup=69.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:42:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.25/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:42] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8007, time=1.2s, cache=HIT(key=ca2a5e12f3a93b645c5f2e4a1973d73f), selection=0.0437s, reuse=0.000752s, speedup=58.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:43:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.25/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:43] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=35.5s, cache=HIT(key=bd145390297fc10ce7469a55c3a79395), selection=0.0466s, reuse=0.000657s, speedup=70.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:44:53] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 15.28% |    0.3047 |   31.00% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.25/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:45] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=39.0s, cache=HIT(key=21e12b819911413d9cbcd128590d5dbd), selection=0.0447s, reuse=0.000794s, speedup=56.27x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:47:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.36% |    0.1839 |   16.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.25/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:47] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=35.5s, cache=HIT(key=c92e8e9b9b19fdbcc8156fd0a5ba414b), selection=0.0464s, reuse=0.000847s, speedup=54.73x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:48:49] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.74% |    0.2530 |   27.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.25/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:49] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=35.7s, cache=HIT(key=a373bc3416f7e309019d2176c5d2b3ae), selection=0.0471s, reuse=0.000690s, speedup=68.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:50:35] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -6.31% |    0.2510 |   24.05% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.25/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:51] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=38.0s, cache=HIT(key=ca2a5e12f3a93b645c5f2e4a1973d73f), selection=0.0437s, reuse=0.003311s, speedup=13.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:52:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.74% |    0.2470 |   23.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.25/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.7s, cache=MISS, selection=0.0460s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:52:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.75/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:52] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=3.0s, cache=MISS, selection=0.0450s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:53:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0163 |    1.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.75/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.7s, cache=MISS, selection=0.0440s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:53:24] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.75/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.8s, cache=MISS, selection=0.0250s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:53:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0188 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.75/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:53] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.7s, cache=MISS, selection=0.0488s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:54:00] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha0.75/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:54] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.0830 (f1_before=0.8672, f1_after=0.7841, time=2.1s, cache=HIT(key=cec403c6c192d44d482a20e989ed8ff5), selection=0.0460s, reuse=0.001479s, speedup=31.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:54:18] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 18.38% |    0.4779 |   22.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.75/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:54] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.1015 (f1_before=0.8653, f1_after=0.7638, time=2.8s, cache=HIT(key=0f5ebfe24927b7e75ffc8433e8a08f4e), selection=0.0450s, reuse=0.000991s, speedup=45.38x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:54:39] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 14.07% |    0.3895 |   16.33% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.75/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:54] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=MISS, selection=0.0003s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:54] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.0904 (f1_before=0.8672, f1_after=0.7768, time=3.4s, cache=HIT(key=26ea006ee7e7c06bffe64b7aeb5de379), selection=0.0440s, reuse=0.001142s, speedup=38.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:54:56] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.71% |    0.0408 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:54:59] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.21% |    0.1930 |   15.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.75/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:55] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.1s, cache=MISS, selection=0.0008s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:55] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.0886 (f1_before=0.8653, f1_after=0.7768, time=2.0s, cache=HIT(key=a3f2d4376849cd8527907b4d29d4d1c3), selection=0.0250s, reuse=0.001327s, speedup=18.82x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:55:13] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.44% |    0.0350 |    2.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:55:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 10.78% |    0.2538 |   14.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.75/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:55] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.2s, cache=MISS, selection=0.0002s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:55] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.0849 (f1_before=0.8616, f1_after=0.7768, time=2.9s, cache=HIT(key=44e115d6d008a144c62b475c0f10e15f), selection=0.0488s, reuse=0.003431s, speedup=14.23x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:55:33] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0382 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:55] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=1.3s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:55:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.10% |    0.2373 |   13.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha0.75/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:55] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.5s, cache=HIT(key=cec403c6c192d44d482a20e989ed8ff5), selection=0.0460s, reuse=0.003897s, speedup=11.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:55:56] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0373 |    3.30% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:56:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0197 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.75/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:56] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=1.3s, cache=MISS, selection=0.0004s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:56] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.4s, cache=HIT(key=0f5ebfe24927b7e75ffc8433e8a08f4e), selection=0.0450s, reuse=0.003422s, speedup=13.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:56:16] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.86% |    0.0438 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:56:26] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0177 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.75/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:56] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:56] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8450, time=1.5s, cache=HIT(key=26ea006ee7e7c06bffe64b7aeb5de379), selection=0.0440s, reuse=0.001723s, speedup=25.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:56] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:56:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.21% |    0.0180 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.75/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:56] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.4s, cache=HIT(key=a3f2d4376849cd8527907b4d29d4d1c3), selection=0.0250s, reuse=0.000619s, speedup=40.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:56] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:57:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0181 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.75/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:57] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=HIT(key=44e115d6d008a144c62b475c0f10e15f), selection=0.0488s, reuse=0.001393s, speedup=35.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:57] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:57:20] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0217 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha0.75/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:57] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.2s, cache=HIT(key=cec403c6c192d44d482a20e989ed8ff5), selection=0.0460s, reuse=0.000793s, speedup=57.93x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:57:37] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0146 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.75/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:57] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.4s, cache=HIT(key=0f5ebfe24927b7e75ffc8433e8a08f4e), selection=0.0450s, reuse=0.000781s, speedup=57.55x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:57] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=3.9s, cache=MISS, selection=2.2827s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:57:56] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0154 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.75/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:57:57] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.22% |    0.0454 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=1.0s, cache=HIT(key=26ea006ee7e7c06bffe64b7aeb5de379), selection=0.0440s, reuse=0.001983s, speedup=22.18x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:58] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8081, time=4.2s, cache=MISS, selection=2.6487s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:58:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.75/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:58:17] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.33% |    0.0447 |    2.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=a3f2d4376849cd8527907b4d29d4d1c3), selection=0.0250s, reuse=0.000737s, speedup=33.87x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:58] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=4.0s, cache=MISS, selection=2.4384s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:58:30] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.75/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 18:58:37] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0449 |    2.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:58] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8063, time=1.3s, cache=HIT(key=44e115d6d008a144c62b475c0f10e15f), selection=0.0488s, reuse=0.000732s, speedup=66.70x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:58:47] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha0.75/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:58] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=4.0s, cache=MISS, selection=2.5635s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:58:57] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.0367 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:59] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GIN, method=GIF, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=4.2s, cache=MISS, selection=2.5898s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:59:18] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0604 |    3.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GIF_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:59] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.1421 (f1_before=0.8432, f1_after=0.7011, time=1.8s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.000664s, speedup=0.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 18:59] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8100, time=34.2s, cache=HIT(key=cec403c6c192d44d482a20e989ed8ff5), selection=0.0460s, reuse=0.000777s, speedup=59.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:59:37] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 17.32% |    0.4038 |   21.28% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 18:59] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = 0.1015 (f1_before=0.8450, f1_after=0.7435, time=1.8s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000684s, speedup=1.17x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 18:59:57] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 18.30% |    0.3362 |   25.70% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:00] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = 0.1605 (f1_before=0.8413, f1_after=0.6808, time=1.7s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000612s, speedup=0.40x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:00:17] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 20.00% |    0.3236 |   26.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:00] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = 0.1494 (f1_before=0.8524, f1_after=0.7030, time=2.3s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.003484s, speedup=0.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:00:36] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 11.11% |    0.2743 |   27.79% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.75/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:00:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 21.18% |    0.3682 |   27.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:00] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = 0.1144 (f1_before=0.8413, f1_after=0.7269, time=3.2s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.003299s, speedup=0.13x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:01:02] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 12.42% |    0.3684 |   16.76% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:01] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=37.1s, cache=HIT(key=0f5ebfe24927b7e75ffc8433e8a08f4e), selection=0.0450s, reuse=0.003256s, speedup=13.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:01] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:02] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:02:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 2.36% |    0.1839 |   16.81% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.75/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:02] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.0941 (f1_before=0.8432, f1_after=0.7491, time=1.7s, cache=HIT(key=aec7f452202222c09d5ecbe3aeb284ab), selection=2.2827s, reuse=0.011015s, speedup=207.24x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:02] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.3976 (f1_before=0.6997, f1_after=0.3021, time=29.2s, cache=HIT(key=1229ed5eb9c1930bc80a4b860c8f841d), selection=0.0021s, reuse=0.001747s, speedup=1.22x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:02:43] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 4.20% |    0.2643 |   12.68% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:02] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = 0.0904 (f1_before=0.8450, f1_after=0.7546, time=2.6s, cache=HIT(key=51dbfff55b791c903c7e6aa99b66706d), selection=2.6487s, reuse=0.000727s, speedup=3641.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:03:04] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 11.52% |    0.2686 |   15.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:03] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=36.9s, cache=HIT(key=26ea006ee7e7c06bffe64b7aeb5de379), selection=0.0440s, reuse=0.000411s, speedup=107.05x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0867 (f1_before=0.8413, f1_after=0.7546, time=4.9s, cache=HIT(key=6929688e7cd8ddbd6d6c759551a21d66), selection=2.4384s, reuse=0.000676s, speedup=3608.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = 0.0867 (f1_before=0.8413, f1_after=0.7546, time=4.9s, cache=HIT(key=6929688e7cd8ddbd6d6c759551a21d66), selection=2.4384s, reuse=0.000676s, speedup=3607.10x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:03:26] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 15.62% |    0.3248 |   20.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:03:31] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 15.62% |    0.3248 |   20.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0720 (f1_before=0.8524, f1_after=0.7804, time=1.8s, cache=HIT(key=06076e24df54945eb347fc7f8974a31d), selection=2.5635s, reuse=0.000728s, speedup=3523.03x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = 0.0720 (f1_before=0.8524, f1_after=0.7804, time=1.8s, cache=HIT(key=06076e24df54945eb347fc7f8974a31d), selection=2.5635s, reuse=0.000728s, speedup=3521.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:03:44] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.49% |    0.2502 |   11.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:03:47] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 7.49% |    0.2502 |   11.61% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0775 (f1_before=0.8413, f1_after=0.7638, time=1.6s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000679s, speedup=3816.74x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:03] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GIN, method=GNNDelete, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = 0.0775 (f1_before=0.8413, f1_after=0.7638, time=1.6s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000679s, speedup=3814.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:04:04] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 12.72% |    0.2993 |   14.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:04:06] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 12.72% |    0.2993 |   14.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GNNDelete_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.5s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.000737s, speedup=0.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.5s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.000737s, speedup=0.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:04:19] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.74% |    0.2388 |   24.59% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.75/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:04:21] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.22% |    0.0405 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:04:22] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.22% |    0.0405 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.5s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000532s, speedup=1.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=1.6s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.001699s, speedup=0.47x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:04:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.73% |    0.0442 |    3.35% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:04:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.73% |    0.0442 |    3.35% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:04] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - random: F1 Drop = 0.3976 (f1_before=0.6997, f1_after=0.3021, time=29.2s, cache=HIT(key=1229ed5eb9c1930bc80a4b860c8f841d), selection=0.0021s, reuse=0.001747s, speedup=1.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.7s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000789s, speedup=0.31x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:04] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=1.9s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000706s, speedup=0.35x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:05:00] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0362 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:05:00] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0362 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:05] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=39.8s, cache=HIT(key=a3f2d4376849cd8527907b4d29d4d1c3), selection=0.0250s, reuse=0.000711s, speedup=35.12x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.5s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.001378s, speedup=0.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8303, time=1.5s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.000447s, speedup=0.81x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:05:19] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.66% |    0.0336 |    2.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:05:19] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.66% |    0.0336 |    2.92% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.5s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.022052s, speedup=0.02x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.5s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.000972s, speedup=0.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:05:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.87% |    0.0390 |    2.53% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:05:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.87% |    0.0390 |    2.53% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:05] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.7s, cache=HIT(key=aec7f452202222c09d5ecbe3aeb284ab), selection=2.2827s, reuse=0.003593s, speedup=635.37x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:06:03] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.88% |    0.0521 |    3.69% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:06:09] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 46.23% |    0.5288 |   53.72% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GNNDelete_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8432, time=1.5s, cache=HIT(key=51dbfff55b791c903c7e6aa99b66706d), selection=2.6487s, reuse=0.003473s, speedup=762.61x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:06:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.01% |    0.2503 |   25.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.75/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:06:23] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 2.14% |    0.0501 |    3.16% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.5s, cache=HIT(key=6929688e7cd8ddbd6d6c759551a21d66), selection=2.4384s, reuse=0.000745s, speedup=3272.75x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:06:40] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.66% |    0.0449 |    3.11% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:06] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, strategies=['tracin'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = 0.3160 (f1_before=0.7001, f1_after=0.3841, time=30.0s, cache=HIT(key=c20b2c24de53ecb82242fdee3d0be954), selection=5110.1408s, reuse=0.003593s, speedup=1422072.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8376, time=1.8s, cache=HIT(key=06076e24df54945eb347fc7f8974a31d), selection=2.5635s, reuse=0.000814s, speedup=3147.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:06] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:06] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8266, time=35.5s, cache=HIT(key=44e115d6d008a144c62b475c0f10e15f), selection=0.0488s, reuse=0.003673s, speedup=13.30x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:07:00] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.32% |    0.0373 |    2.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:07] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.6s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000716s, speedup=3617.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:07] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GIN, method=MEGU, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.6s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000716s, speedup=3617.04x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:07:18] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.44% |    0.0609 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:07:18] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.44% |    0.0609 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/MEGU_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.000702s, speedup=0.39x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.2s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.000290s, speedup=0.94x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:07:36] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.71% |    0.0408 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:07:36] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.71% |    0.0408 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.4s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000700s, speedup=1.14x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:07] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8173, time=1.4s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000267s, speedup=2.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:07:55] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.44% |    0.0349 |    2.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:07:55] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.44% |    0.0349 |    2.77% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.3s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000842s, speedup=0.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8137, time=1.4s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000258s, speedup=0.95x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:08:09] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.23% |    0.2408 |   22.50% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha0.75/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:12] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0382 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:13] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.43% |    0.0382 |    2.72% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:13] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 56.25% |    0.5770 |   62.12% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GNNDelete_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=2.0s, cache=MISS, selection=0.0451s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=1.1s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.000677s, speedup=0.54x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8044, time=1.1s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.000313s, speedup=1.16x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:08:27] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0158 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha1.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:28] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0373 |    3.30% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:30] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | -0.87% |    0.0373 |    3.30% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.7s, cache=MISS, selection=0.0452s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=1.1s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.000648s, speedup=0.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.7952, time=1.1s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.000648s, speedup=0.62x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:08:44] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0220 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha1.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:46] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.86% |    0.0438 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:08:47] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 0.86% |    0.0438 |    2.67% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:08] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, strategies=['im'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - im: F1 Drop = 0.3853 (f1_before=0.6999, f1_after=0.3146, time=31.3s, cache=HIT(key=ce8117dc5bf55cbad0eceba989b3e5e2), selection=1722.0304s, reuse=0.001051s, speedup=1638176.20x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8487, time=1.7s, cache=MISS, selection=0.0438s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:08] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.1s, cache=HIT(key=aec7f452202222c09d5ecbe3aeb284ab), selection=2.2827s, reuse=0.000698s, speedup=3272.19x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:09:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0118 |    1.07% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha1.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:09:04] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.22% |    0.0455 |    3.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=2.0s, cache=MISS, selection=0.0452s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8229, time=1.1s, cache=HIT(key=51dbfff55b791c903c7e6aa99b66706d), selection=2.6487s, reuse=0.000780s, speedup=3396.41x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:09:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -1.29% |    0.0188 |    1.17% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha1.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:09:22] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -1.33% |    0.0447 |    2.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=1.1s, cache=HIT(key=6929688e7cd8ddbd6d6c759551a21d66), selection=2.4384s, reuse=0.000679s, speedup=3591.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - GIF 攻击实验
- 任务：dataset=cora, model=GCN, method=GIF, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.9s, cache=MISS, selection=0.0488s)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:09:41] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0450 |    2.82% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:09:41] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GIF, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GIF_hybrid_alpha1.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8118, time=1.9s, cache=HIT(key=06076e24df54945eb347fc7f8974a31d), selection=2.5635s, reuse=0.000737s, speedup=3477.45x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = 0.0443 (f1_before=0.8672, f1_after=0.8229, time=2.4s, cache=HIT(key=a87eb16ca0dd7f8969d160e0bf9f6f71), selection=0.0451s, reuse=0.000970s, speedup=46.49x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:09] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:09:59] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | -0.65% |    0.0367 |    2.48% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:10:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 8.68% |    0.2732 |   13.80% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha1.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=1.5s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000723s, speedup=3583.78x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:10] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GIN, method=IDEA, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7989, time=1.5s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.000282s, speedup=9197.66x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = 0.0812 (f1_before=0.8653, f1_after=0.7841, time=2.3s, cache=HIT(key=51b3244a2fe1c31764542eaf35d19784), selection=0.0452s, reuse=0.000687s, speedup=65.80x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:10:16] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0605 |    3.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:10:18] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 0.00% |    0.0605 |    3.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/IDEA_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:10:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 3.22% |    0.2386 |    4.62% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha1.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:10:22] eval_collateral.py
- 任务：dataset=ogbn-arxiv, model=GCN, method=GNNDelete, ratio=0.01
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| im       | 72.22% |    0.5529 |   75.52% |
- 日志路径：`/autodl-fs/data/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.01/GNNDelete_im/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:10] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = 0.0554 (f1_before=0.8672, f1_after=0.8118, time=5.3s, cache=HIT(key=0c6a671fab01782bba8d0512ab6729f5), selection=0.0438s, reuse=0.003752s, speedup=11.68x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:10:50] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 12.21% |    0.1930 |   15.84% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha1.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:11] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = 0.0590 (f1_before=0.8653, f1_after=0.8063, time=5.4s, cache=HIT(key=ed310c0ece58355d68af9a2beafe5d2b), selection=0.0452s, reuse=0.004312s, speedup=10.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:11:43] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 10.78% |    0.2538 |   14.24% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha1.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:11] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=90.2s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.004058s, speedup=0.07x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:11] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8358, time=89.9s, cache=HIT(key=0aaf5eefcccb19db4b2c63c71b0e42e0), selection=0.0003s, reuse=0.003364s, speedup=0.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:12] demo_attack.py - GNNDelete 攻击实验
- 任务：dataset=cora, model=GCN, method=GNNDelete, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = 0.0572 (f1_before=0.8616, f1_after=0.8044, time=2.0s, cache=HIT(key=399342b2c0055bef355b248eb1621bde), selection=0.0488s, reuse=0.000652s, speedup=74.89x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:12:12] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GNNDelete, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 11.16% |    0.2251 |   12.39% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GNNDelete_hybrid_alpha1.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:12] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8561, time=1.6s, cache=HIT(key=a87eb16ca0dd7f8969d160e0bf9f6f71), selection=0.0451s, reuse=0.000645s, speedup=69.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:12:29] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0206 |    1.55% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha1.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:12] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=4.8s, cache=HIT(key=51b3244a2fe1c31764542eaf35d19784), selection=0.0452s, reuse=0.000932s, speedup=48.52x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:13:13] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.22% |    0.0177 |    1.12% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha1.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:13] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=80.2s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000738s, speedup=1.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8506, time=1.4s, cache=HIT(key=0c6a671fab01782bba8d0512ab6729f5), selection=0.0438s, reuse=0.000721s, speedup=60.72x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:13:44] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 19.15% |    0.3422 |   34.21% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GraphEraser_random/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:13:45] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.21% |    0.0180 |    1.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha1.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:13] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8026, time=80.2s, cache=HIT(key=8e6ffac5e4fc564c1cced6361092d944), selection=0.0008s, reuse=0.000738s, speedup=1.08x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:13] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.1s, cache=HIT(key=ed310c0ece58355d68af9a2beafe5d2b), selection=0.0452s, reuse=0.001819s, speedup=24.85x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:14:02] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.43% |    0.0181 |    1.41% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha1.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:14] demo_attack.py - MEGU 攻击实验
- 任务：dataset=cora, model=GCN, method=MEGU, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=1.5s, cache=HIT(key=399342b2c0055bef355b248eb1621bde), selection=0.0488s, reuse=0.005632s, speedup=8.67x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:14:22] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=MEGU, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.00% |    0.0228 |    0.73% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/MEGU_hybrid_alpha1.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:14] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=1.5s, cache=HIT(key=a87eb16ca0dd7f8969d160e0bf9f6f71), selection=0.0451s, reuse=0.000719s, speedup=62.76x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:14:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0146 |    0.97% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha1.00/seed42/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:14] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.3s, cache=HIT(key=51b3244a2fe1c31764542eaf35d19784), selection=0.0452s, reuse=0.000688s, speedup=65.78x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:15:01] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.64% |    0.0154 |    1.31% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha1.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:15:02] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 6.22% |    0.1975 |   20.46% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GraphEraser_random/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:15] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8210, time=1.4s, cache=HIT(key=0c6a671fab01782bba8d0512ab6729f5), selection=0.0438s, reuse=0.000665s, speedup=65.90x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:15] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8524, time=39.9s, cache=HIT(key=092436af0e50e28b4003614615ac353b), selection=0.0002s, reuse=0.000775s, speedup=0.32x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:15:21] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.86% |    0.0213 |    0.83% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha1.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:15] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=1.2s, cache=HIT(key=ed310c0ece58355d68af9a2beafe5d2b), selection=0.0452s, reuse=0.004245s, speedup=10.65x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:15:42] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -0.43% |    0.0121 |    0.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha1.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:15] demo_attack.py - IDEA 攻击实验
- 任务：dataset=cora, model=GCN, method=IDEA, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8192, time=1.4s, cache=HIT(key=399342b2c0055bef355b248eb1621bde), selection=0.0488s, reuse=0.004297s, speedup=11.36x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:16:04] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=IDEA, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 1.06% |    0.0140 |    0.87% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/IDEA_hybrid_alpha1.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:17] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8395, time=79.4s, cache=HIT(key=9c42112ef358156333e825b2ee44bd19), selection=0.0004s, reuse=0.006212s, speedup=0.06x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=102.7s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.000680s, speedup=0.64x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=106.7s, cache=HIT(key=51b3244a2fe1c31764542eaf35d19784), selection=0.0452s, reuse=0.000763s, speedup=59.26x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=42
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:18] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['random'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.8321, time=102.7s, cache=HIT(key=8d477db63190d3fe623440b6321ea04f), selection=0.0004s, reuse=0.000680s, speedup=0.59x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:19] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:19] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:19:40] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 3.07% |    0.2054 |   19.58% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha1.00/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:19:53] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| random   | 1.27% |    0.1966 |   20.36% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GraphEraser_random/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=722
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8284, time=38.9s, cache=HIT(key=0c6a671fab01782bba8d0512ab6729f5), selection=0.0438s, reuse=0.000724s, speedup=60.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:20] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['im'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:21] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7860, time=42.0s, cache=HIT(key=51dbfff55b791c903c7e6aa99b66706d), selection=2.6487s, reuse=0.009792s, speedup=270.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:21] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=212
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.7860, time=42.0s, cache=HIT(key=51dbfff55b791c903c7e6aa99b66706d), selection=2.6487s, reuse=0.009792s, speedup=270.50x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:21:51] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.74% |    0.2530 |   27.45% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha1.00/seed722/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:23] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=1337
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8155, time=78.8s, cache=HIT(key=ed310c0ece58355d68af9a2beafe5d2b), selection=0.0452s, reuse=0.001675s, speedup=26.99x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:23:25] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 1.91% |    0.1871 |   19.29% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GraphEraser_tracin/seed212/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:25:05] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | -4.80% |    0.2450 |   23.42% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha1.00/seed1337/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:25] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=65.5s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.001005s, speedup=2576.48x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:25] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GIN, method=GraphEraser, strategies=['tracin'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - tracin: F1 Drop = NA (f1_before=NA, f1_after=0.8339, time=65.5s, cache=HIT(key=20c35a90d1931cf8f179369a28e0850b), selection=2.5898s, reuse=0.001005s, speedup=2576.92x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。

### [2026-05-07 19:26] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=cora, model=GCN, method=GraphEraser, strategies=['hybrid'], ratio=0.05
- 配置：unlearn_ratio=0.05 (108 nodes), seed=2024
- 执行结果：
  - hybrid: F1 Drop = NA (f1_before=NA, f1_after=0.8247, time=52.6s, cache=HIT(key=399342b2c0055bef355b248eb1621bde), selection=0.0488s, reuse=0.000657s, speedup=74.29x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
### [2026-05-07 19:26:53] eval_collateral.py
- 任务：dataset=cora, model=GIN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| tracin   | 2.53% |    0.2043 |   20.65% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GIN_r0.05/GraphEraser_tracin/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。

### [2026-05-07 19:27:14] eval_collateral.py
- 任务：dataset=cora, model=GCN, method=GraphEraser, ratio=0.05
- 策略结果：
| Strategy | Gap% | MeanShift | Flipped% |
|----------|------|-----------|----------|
| hybrid   | 0.74% |    0.2470 |   23.66% |
- 日志路径：`/root/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/GraphEraser_hybrid_alpha1.00/seed2024/collateral.json`
- 执行结果：OK
- 异常与定位：无
- 下一步建议：检查该方法在其他比例或数据集的趋势。


### [2026-05-07 19:33] demo_attack.py - GraphEraser 攻击实验
- 任务：dataset=ogbn-arxiv, model=GCN, method=GraphEraser, strategies=['random'], ratio=0.01
- 配置：unlearn_ratio=0.01 (1354 nodes), seed=42
- 执行结果：
  - random: F1 Drop = NA (f1_before=NA, f1_after=0.6603, time=1356.0s, cache=HIT(key=1229ed5eb9c1930bc80a4b860c8f841d), selection=0.0021s, reuse=0.003058s, speedup=0.69x)
- 异常与定位：无
- 下一步建议：检查 cache 是否正确写入，继续其他策略或数据集。
