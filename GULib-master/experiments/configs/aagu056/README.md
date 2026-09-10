# AAGU-056 · arxiv RR-1024 运行准备

## 固定条件

入口仍为 `experiments/run.py`。`rr_1024.yaml` 引用057已核验的
`datasets/ogbn-arxiv.yaml`：项目随机70/10/20、split seed 2024，非OGB官方划分。
169343节点、2315598条边、train-mask候选118540；预算5%，实际K=5927。
Selector为im_rr_greedy，RR=1024，传播概率0.1，IM seed=11。
只有1个Selector cell，无模型训练、GU、Retrain或evaluation。

## 静态运行注册

- recipe：`opengu-aagu056-rr1024-v1`
- experiment_id：`aagu056-arxiv-rr1024-budget05`
- run_id：`aagu056-rr1024-v1`
- timeout_seconds：21600（6小时），由Core控制实验子进程。
- 结果根：`results/runs/aagu056-arxiv-rr1024-budget05/aagu056-rr1024-v1`
- 回传合同由现有recipe生成：run.json和唯一cell的selection.json。
- 首轮job id建议：`aagu056-rr1024-v1`；提交前确认所有队列状态均未占用此ID。

验证命令（不运行Selector）：

```powershell
E:/conda_package/envs/gnn/python.exe experiments/run.py experiments/configs/aagu056/rr_1024.yaml --dry_run
```

接受并落地后，先核对本地main、origin/main、SSH活跃main为同一完整SHA，tracked tree干净，
再执行现有Core runner-preflight。提交时绑定当时三方一致的完整SHA；候选SHA不是落地SHA。
正式启动命令由Core dispatch提供，不能直接启动另一个launcher，也不提前写inbox。

## 资源方案

2026-09-11 SSH探测：容器memory.max=128849018880字节（120 GiB），
cpu.max=1600000/100000（16核配额），GPU为RTX4090 24 GiB。
当前普通链按设备文件使用cuda并将图搬到GPU，但RR采样与贪心本身运行在CPU。
不修改共享设备文件，不声称整个进程零显存占用。

本轮只允许一个实验job。启动前inbox/running必须为空，且053和其他实验进程均未占用资源；
容器memory.current必须低于8 GiB，留下至少112 GiB容器余量；GPU空闲显存至少4 GiB。
宿主机free输出不能替代容器限额。

- 硬限制：现有容器120 GiB，由内核执行；这是整个容器的共享上限，不是本job独占RSS限额。
- 软停止阈值：容器memory.current达到96 GiB。执行者需每5秒检查并记录，触发时停止本job的
  已核实实验子进程，保留Core失败记录及日志，不自动重试。它是运行操作要求，当前Core没有
  per-job内存限额字段，也没有已启用的memory.high保护，不能宣称此软阈值已经自动执行。
- 无持续资源监控的执行者时不得启动；不要影响同机其他进程，不调整共享cgroup限额。
- 记录进程RSS采样最大值时必须标为采样值；cgroup memory.peak是共享容器历史高水位，
  不能作为本job峰值RSS。拿不到可靠的本job峰值就标未记录，不伪造测量。

## 运行前与运行后

使用057资产的真实读取核验，确认manifest/graph/split身份及候选数量；按同一producer身份只读
查询Selection缓存，精确HIT或覆盖K的HIT均复用，不清缓存。启动前再次确认独立结果根不存在。
缓存MISS才计算；报告明确区分读取时间与冷计算时间。

完成后沿用Core scoped collect与SHA验证，检查Selection长度5927、唯一性、候选范围和身份，
读取现有selection_seconds。数据、模型与Cache payload留在SSH。
先核验1024，再记录4096预测并决定扩档；本次没有注册或启动4096/16384。

本文件为运行方案，实时准备证据与验收决定归canonical
`.workblock/items/AAGU-056/WORKITEM.md`。运行准备不代表正式计时已执行。
