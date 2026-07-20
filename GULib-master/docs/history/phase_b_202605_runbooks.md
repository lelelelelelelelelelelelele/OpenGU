# 2026-05 Phase B Runbook 退休记录

> Retired: 2026-07-20
> Scope: historical pointer only; not an execution guide.

以下文件服务于 2026-05-07 截稿期的双机 Phase B 执行，包含已过时的分支名、deadline 顺序、成本估计、GraphRevoker feasibility 状态和 cache 假设。2026-07-20 已从活动树删除：

- `SERVER_RUNBOOK.md`
- `ARXIV_RUNBOOK.md`
- `MIGRATION_RUNBOOK.md`
- `experiments/configs/SANITY_GRAPHREVOKER.md`

当前替代入口：

| 需要 | 当前来源 |
|---|---|
| 当前任务、正式 lane、远端状态 | `self/dashboard/WORKPLAN.md` |
| runner / yaml / dry-run / gate | `文档规划/10_实验矩阵/15_实验运行入口与脚本.md` |
| 4090 小图运行与回收 | `文档规划/10_实验矩阵/16_4090小数据集运行与回收.md` |
| CPU/GPU 估时 | `文档规划/10_实验矩阵/17_CPU-GPU估时与资源分工.md` |
| SSH / AutoDL | `文档规划/10_实验矩阵/18_AutoDL_4090连接与加速.md` |
| 修复结论、测试、失效数据 | `文档规划/10_实验矩阵/13_重跑与缓存修复Runbook.md` |
| OpenGU cache/result 修复 | `scripts/syncmate/OPENGU_CACHE_REPAIR_RUNBOOK.md` |
| GraphRevoker 当前边界 | `docs/graphrevoker_e4_ACCEPTANCE_REPORT.md` |

旧文件全文不复制到新文档；需要历史溯源时使用 Git：

```powershell
git log -- SERVER_RUNBOOK.md ARXIV_RUNBOOK.md MIGRATION_RUNBOOK.md experiments/configs/SANITY_GRAPHREVOKER.md
git show 2f0d22a:GULib-master/SERVER_RUNBOOK.md
```

dated reports 与 `VALIDATION_LOG.md` 中对旧文件名的引用保持历史原貌，不代表这些文件仍是当前入口。
