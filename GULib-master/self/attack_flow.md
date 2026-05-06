# Attack Flow 时序与硬件占用

> 一个 cell 跑完 attack + collateral 经历的所有阶段，以及每段在哪个硬件上工作。
> 用途：调试卡死位置、估算 B.2 总耗时、决定 GPU 配置。
>
> 图例：🔥 = GPU 高利用（>70%）｜ 🐌 = CPU 主导，GPU 闲置｜ ⚠ = 已知瓶颈

## 一个 cell 完整 flow（按时序）

```
[demo_attack.py 一个 cell]
      │
      ├─ ① 数据加载（一次性，cell 间复用）         CPU       <1 min
      │
      ├─ ② Base model train (200 epoch GCN)        GPU 🔥    ~38 s
      │
      ├─ ③ Selection ─────────────────────┐
      │     ├─ random / degree              CPU       <1 s
      │     ├─ pagerank                     CPU       ~10 s
      │     ├─ IM (CELF + numba)            CPU 🐌    ⚠ 卡过 10h+ (默认参数)
      │     │                                          fix: candidate_fraction=0.1, mc_rounds=50
      │     │                                          → ~3 min（B.1.5 prewarm 后 cache hit）
      │     ├─ tracin                       GPU 🔥    ⚠ G-matrix 40GB OOM on 24GB
      │     │                                          ~150 min on A100 80GB
      │     └─ hybrid                       GPU+CPU   tracin + IM 之和
      │
      ├─ ④ Inject selected nodes            CPU       <1 s（写文件）
      │
      ├─ ⑤ Unlearn ─────────────────────┐
      │     ├─ GIF (Hessian-vector)         GPU 🔥    ~1 min
      │     ├─ GNNDelete (mask network)     GPU 🔥    ~2 min
      │     ├─ MEGU / IDEA                  GPU 🔥    ~1-3 min
      │     └─ GraphEraser ─────┐
      │           ├─ partition (LPA)        CPU 🐌    ⚠ 10 min/iter，早停 1-2 iter ≈ 10 min
      │           └─ shard model train      GPU 🔥    ~1 min
      │
      ├─ ⑥ F1 measurement                   GPU       <1 s（一次 forward）
      │
      └─ ⑦ Update-Detection AUC (legacy: MIA AUC)
            ├─ positive samples loop        CPU 🐌    ⚠ 6 min（100 iter × 3.6s）
            │                                          GPU < 5%
            └─ negative samples loop        CPU 🐌    ⚠ 6 min（100 iter × 3.6s）
                                                      → update-detection 总 ~12 min

[eval_collateral.py 一个 cell]
      │
      ├─ ⑧ Retrain from scratch (200 epoch) GPU 🔥💥 ⚠ OOM on 24GB（实际峰值 ~22 GB）
      │                                                必须 ≥40 GB（A6000 48GB / A100 40GB+）
      │
      ├─ ⑨ Generate retrained predictions   GPU       <1 s
      │
      └─ ⑩ Compute gap / pred_shift / hop   CPU       <1 s（numpy diff）
```

## 单 cell 耗时估算（arxiv 3-layer GCN/256 hidden）

| Cell 类型 | 总耗 | 分解 |
|---|---|---|
| `random` cell | ~12 min | base train 0.5 + unlearn 1-3 + F1 0 + MIA 12 |
| `random` + GraphEraser | ~30 min | + LPA 10 + shard train 1 |
| `tracin` cell | ~165 min | + selection 150 |
| `tracin` + GraphEraser | ~180 min | + LPA 10 |
| `eval_collateral` 单独 | ~1 min | retrain 0.5 + compute 0.5 |

## A100 80GB 全程跑 B.2 的"忙闲"剖面

按一个 GraphEraser tracin cell ~180 min 拆解：

| 阶段 | 耗时 | GPU 利用率 | 说明 |
|---|---|---|---|
| ② base train | ~30 s | 90%+ 🔥 | 划算 |
| ③ selection (tracin) | ~150 min | 80%+ 🔥 | 划算 |
| ⑤b GraphEraser LPA | ~10 min | <5% 🐌 | **空转** |
| ⑤b shard train | ~1 min | 70%+ 🔥 | 划算 |
| ⑦ Update-detection × 2 (legacy: MIA) | ~12 min | <5% 🐌 | **空转**，CPU 10 核满 |
| ⑧ retrain | ~30 s | 90%+ 🔥 | 划算 |

**约 12-15% 时间 GPU 空转**（update-detection + LPA），按 B.2 总 ~22h 估算 ~$8 浪费在闲置上。
拆分到便宜机器的工程成本 > 节省，**接受浪费换稳定**。

## 已经撞到的瓶颈一览（cross-link 到 limitations.md）

| 瓶颈 | 位置 | 处置 | 文档 |
|---|---|---|---|
| IM CELF 卡 10h+ | ③ IM | yaml 加 `candidate_fraction=0.1, mc_rounds=50` | L3 |
| LPA 单 iter 10min | ⑤b GraphEraser | terminate_delta 早停救场 | L1 |
| Update-detection CPU-bound（legacy: MIA） | ⑦ | 接受，租 ≥8 核实例 | L5 |
| TracIn G-matrix 40GB | ③ tracin | 升级到 A100 80GB | L2 |
| Retrain 22GB peak | ⑧ collateral | 升级到 A100 80GB / A6000 48GB | （隐含 in L2） |
