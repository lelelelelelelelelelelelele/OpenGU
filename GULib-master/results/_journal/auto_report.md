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
