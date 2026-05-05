# 服务器执行手册 v3 — 双机 Phase B 执行

> 创建: 2026-05-04 · 大改: 2026-05-05（双机版）
> NeurIPS 截稿: 2026-05-07（剩 2 天）

---

## 🗂 Phase → 章节索引（找命令直接跳这里）

| Phase | 内容 | 跑哪台 | 章节 | 估时 |
|---|---|---|---|---|
| **B.0** | cora/GIF/random sanity（最小 cell 烟测，4 件齐 + gate） | 任意 | **§B.0** ⭐ | ~20s |
| **B.1** | arxiv 5 GU method × random × seed42（feasibility / 5-method random baseline） | 机器 B | §5.3 (有镜像) / §5A.4 (fresh clone) | ~75-120 min |
| **B.2** | arxiv 3 method × 4 strategy × 3 seed 全矩阵（核心数据） | 机器 B | §5.6 / §5A.7 | ~22-40h |
| **B.3** | cora_GCN 5 method × 6 strategy × 5 seed | 机器 A | §4.1 | ~3-5h |
| **B.4** | cora_GAT 同上 | 机器 A | §4.3 | ~3-5h |
| 装环境 | 全新 H20/H800 fresh clone | 任意 | §A 附录 / §5A.2 | ~10-15 min |
| 调试 | nohup 全 fail / 找不到 traceback | — | **§0.9** ⭐ | — |
| 故障速查 | 错信息 → 处理 | — | §7 | — |

> "B.0 ⭐" 是新提到的顶层节，下面就是；以前埋在 §5A.3，user 反馈太难找。

---

## ✅ 已完成（环境层）

| 项 | 状态 |
|---|---|
| 代码 | `~/autodl-fs/OpenGU/GULib-master` @ `nips-prep` |
| Python / torch | 3.10 / 2.1.2+cu118 |
| PyG / scatter / sparse | 2.6.1 / 2.1.2 / 0.6.18 |
| 当前 GPU | RTX 4090 24GB（用于 cora 部分；arxiv 太小）|

---

## 0. 常用指令速查 ⭐

### 0.1 ssh 进来后三连

```bash
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master
tmux attach -t phaseB || tmux new -s phaseB
unset http_proxy && unset https_proxy

```

### 0.2 同步代码

```bash
git pull --ff-only && git log --oneline -5
```

### 0.3 tmux 速记

| 操作 | 按键 / 命令 |
|---|---|
| **挂后台**（detach） | `Ctrl-b` 然后 `d` |
| 重新进会话 | `tmux attach -t phaseB` |
| 列所有会话 | `tmux ls` |
| 在会话里开新窗格（监控用） | `Ctrl-b` 然后 `c`；切换 `Ctrl-b n` / `p` |
| 关当前窗格 | `exit` 或 `Ctrl-d` |
| 杀整个会话 | `tmux kill-session -t phaseB` |

> VSCode 用户：先**鼠标点一下 terminal** 再按 `Ctrl-b`，否则被 VSCode 侧边栏拦截。

### 0.4 紧急停止跑飞的任务

前台 tmux 任务：`Ctrl+C` → 不响应再 `Ctrl+\`。

后台 nohup：

```bash
ps -ef | grep -E "run\.py|prewarm" | grep -v grep
kill <PID>
kill -9 <PID>
```

按命令模式批杀：

```bash
pkill -f "experiments/run.py"
pkill -f "prewarm_selection_cache"
```

GPU 状态：

```bash
nvidia-smi
watch -n 2 nvidia-smi
```

### 0.5 清缓存

只清 selection_cache（大多数情况这就够了）：

```bash
find results/selection_cache -name '*.json' -delete
```

全清（B.0 sanity 出 `mia_auc=0` 时用）：

```bash
find results/cache results/selection_cache -name '*.json' -delete
```

> 不要碰：`results/runs/`（实验输出）、`data/processed/`（数据集 split）。

### 0.6 看一个 cell 卡哪了

各阶段 CPU/GPU 占用 + 已知瓶颈位置：见 `self/attack_flow.md`。判别"卡死还是慢"必看。

### 0.7 监控正在跑的任务

```bash
tail -f logs/phase_b_arxiv.log
ls results/runs/ogbn-arxiv_*/*/seed*/attack.json | wc -l
grep -c "SelectionCache.*HIT" logs/phase_b_arxiv.log
df -h ~
du -sh results/
```

依次：实时日志 / 进度计数 / cache 命中数 / 磁盘剩余 / 实验产出占用。

### 0.8 一键诊断 + gate

```bash
bash scripts/diag_b1.sh                              # 当前 cell 输出列表 + log 错误尾
python scripts/gate_runs.py <yaml> [--f1-min N --f1-max M]   # 自动 pass/fail
```

### 0.9 前台单 cell 调试（nohup 全失败时第一件事）

`run.py` 用 `subprocess.run` 跑 demo_attack / eval_collateral，stdout/stderr 透传到父进程。但 nohup 把父进程 stdout/stderr 写文件时若子进程 import 阶段就 segfault / argparse error / `os._exit()`，错误可能被 buffer 吞掉看不全。**整 yaml 5/5 `failed_attack` + `elapsed: <30s` = 子进程根本没启动到 GPU 阶段**——这时跳过 nohup，前台跑一个 cell 看真实 traceback。

```bash
# A. 用 run.py 的 --limit 1，路径与 B.1 完全一致（含 collateral）
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml --limit 1

# B. 或者直接调 demo_attack（最薄一层，便于把 args 一一对照 yaml）
python demo_attack.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --unlearning_methods GIF --strategies random \
    --unlearn_ratio 0.05 --seed 42 \
    --num_epochs 200 --batch_size 256 --cuda 0 \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --save_path /tmp/test_attack.json
```

A 优先（暴露的 bug 跟 nohup 路径完全一致）；A 起不来就退到 B（绕开 run.py 包装）。

修好之后再回到 nohup 全跑——别在前台跑 5 cell 把人锁住，shell 一断又要重来。

---

## 1. 双机执行计划（核心架构）⭐

**两台机器并行**，各跑各的数据集，互不冲突（不同 dataset → 不同 cache key、不同 results 目录）。

### 1.1 分工

| 机器 | GPU | 显存 | 角色 | 跑的内容 | 估时 |
|---|---|---|---|---|---|
| **机器 A** | RTX 4090 | 24 GB | cora 数据集 | B.3 cora_GCN + B.4 cora_GAT（300 cell）| ~6-10h |
| **机器 B** | H800 / A100 80G | 80 GB | arxiv 数据集 | B.1 collateral 补 + B.1.5 prewarm + B.2（36 cell）| ~25h |

> 机器 A 是当前实例（4090，已经跑过 B.1 attack）。机器 B 用**保存镜像**克隆系统盘到新实例（不重装环境）。

### 1.2 为什么必须两机

arxiv 上：
- TracIn G-matrix peak ~68 GB → **24GB 卡 OOM**
- collateral retrain peak ~22 GB → **24GB 卡边缘 OOM**

cora 上：
- 全套都 < 4GB → 4090 完全够，且每 cell <1 min 用 H800 浪费

### 1.3 数据合并

各自写不同子目录，不冲突：
- 机器 A 写 `results/runs/cora_GCN_r0.05/`、`cora_GAT_r0.05/`
- 机器 B 写 `results/runs/ogbn-arxiv_GCN_r0.05/`

跑完两边各 `tar` 一份 scp 回本地合并。

---

## 2. 进度快照（2026-05-05 23:00 更新）

### B.0 sanity ✅

```
cora/GCN/GIF/random/seed42 — 20s 跑完
attack.json + collateral.json + predictions.npz + _meta.json 四件齐
mia_auc=0.592, f1_before=0.884
```

### B.1 attack 部分 ✅（5/5 cell 都有 attack.json）

```
results/runs/ogbn-arxiv_GCN_r0.05/
  GIF_random/seed42/attack.json          (140K, 16:18)
  GNNDelete_random/seed42/attack.json    (140K, 16:19)
  IDEA_random/seed42/attack.json         (140K, 16:20)
  GraphEraser_random/seed42/attack.json  (140K, 16:51)
  MEGU_random/seed42/attack.json         (140K, 03:06，旧但有效)
```

attack 阶段（selection + unlearn + MIA）**全员通过**，5 个 method 在 169K 节点 arxiv 上都能跑完。

### B.1 collateral 部分 ⚠（2/5，3 个 OOM 待 H800 上解决）

```
GraphEraser_random/seed42/collateral.json  (1K, 17:51 — 完整)
MEGU_random/seed42/collateral.json         (1K, 03:07 — 旧但有效)
GIF_random/seed42                          ❌ 缺（OOM during retrain）
GNNDelete_random/seed42                    ❌ 缺（OOM during retrain）
IDEA_random/seed42                         ❌ 缺（OOM during retrain）
```

OOM 错：`Tried to allocate 1.81 GiB on 23.52 GiB total`。retrain peak ~22 GB，4090 24GB 边缘失败。**待机器 B（H800 80GB）切换后 5 min 补完**，详见 §5.3。

### B.1.5 探针 ✅（arxiv tracin 显存外推）

```bash
python scripts/feasibility_selection_only.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --candidate_subset_size 1000 --strategies tracin
```

输出：

```
[init] num_nodes=169343  edges=2315598  train=135474  device=cuda
[probe] subset=1000, ratio=0.0074, k=500
tracin   0   36.07s   5931.7 MB peak   top-5: [29875, 110788, 108125, 128381, 106199]
```

**真实显存外推**（修正 probe 脚本里的线性外推 bug 后）：
- per-grad 内存：~440 KB
- forward 计算图常驻：~7-8 GB
- 全量 N=135474：**~68 GB peak** → A100/H800 80GB 够用，**留 ~12 GB 缓冲**
- 全量时间：**~81 min/cell** on 4090（H800 上估 ~50 min）

> 探针脚本输出了 "OOM 785 GB" 的吓人数字，但那是把固定 forward 开销错误线性外推得到的。实际是 ~68 GB。

### B.2 + B.3 + B.4 ⏳ 待启

需要先切到 H800 + 补 collateral，详见 §4 / §5。

---

## 3. tmux 工作流（每次 ssh 后第一件事）

### 3.1 初次创建会话

```bash
which tmux || apt update && apt install -y tmux
source /etc/network_turbo
tmux new -s phaseB
```

> apt 卡的话备选 `screen -S phaseB`，detach 是 `Ctrl-a d`。

### 3.2 VSCode 用户特殊提示

VSCode 的 `Ctrl-B` 默认是侧边栏切换，会拦截 tmux prefix。**先用鼠标点一下 terminal** 再按 Ctrl-b。或者一次性配置改 prefix：

```bash
cat > ~/.tmux.conf <<'EOF'
set -g prefix C-a
unbind C-b
bind C-a send-prefix
EOF
tmux kill-server && tmux new -s phaseB
```

### 3.3 history 调大（避免 OOM 时翻不到 traceback）

```bash
echo 'set -g history-limit 50000' >> ~/.tmux.conf
tmux source-file ~/.tmux.conf
```

---

## B.0 烟测（任意 GPU，~20s，每次大跑前先做）⭐

cora/GCN/GIF/random/seed=42 的最小 cell。验三件事：
1. attack pipeline 端到端通（base train → unlearn → MIA → 4 件输出齐）
2. 当前环境的 PyG / cuda / dataloader 没崩
3. ScoreCache / SelectionCache / ResultCache 三个 cache 的写盘正常

**~20s on cora, ~¥0**。任何 refactor 改完 / 装新机器 / 换 GPU 都先跑这一步，再决定上 B.1 / B.2。

```bash
# 跑 B.0
python experiments/run.py experiments/configs/sanity_one_cell.yaml 2>&1 | tee /tmp/b0.log
ls -la results/runs/cora_GCN_r0.05/GIF_random/seed42/

# gate（自动 PASS/FAIL，exit 0 = 通过）
python scripts/gate_runs.py experiments/configs/sanity_one_cell.yaml --f1-min 0.7
```

`gate_runs.py` 检查（脚本 docstring 是真源）：
- 4 件齐：`attack.json` / `collateral.json` / `predictions.npz` / `_meta.json`
- `attack.json[results][strategy].mia_auc` ∈ `(0.001, 0.999)`
- `collateral.json[results][0].perf_before` ∈ `[--f1-min, --f1-max]`（base train 真 F1，跨 node/edge 任务都填）
- `collateral.json[results][0].gap` 是有限数；`hop_decay` 是 dict

> `attack.json[results][strategy].f1_before` **node task 下恒为 None**（`pipeline_adapter.py:285` 的 `poison_f1` 只 edge task 路径填）。`gate_runs.py` 已经改成不依赖这个字段——别自己写 inline `python -c` 去读 `f1_before`，会被这个坑掉。
>
> `gap = perf_retrain - perf_unlearn`，cora 小图上 unlearn ≈ retrain 时四位小数会 round 到 0.0；`is_finite_number(0.0)=True`，照样过 gate。

**FAIL 处理**：gate 会列每条失败原因。先看 §0.9 前台单 cell 调试拿真 traceback，再决定改代码还是清缓存（§0.5）。**FAIL 不要继续上 B.1 / B.2**——保证 ~¥0 失败比 ~¥100 失败强。

---

## 4. 机器 A（4090）— cora workload

当前实例已在跑/即将跑。

### 4.1 启 B.3 cora_GCN（150 cell, ~3-5h）

```bash
cd ~/autodl-fs/OpenGU/GULib-master
git pull --ff-only

# nohup 后台
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml \
    > logs/phase_b_cora_gcn_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b_cora_gcn.pid

# detach 出 tmux
# Ctrl-b d
```

### 4.2 监控

```bash
tail -f logs/phase_b_cora_gcn_*.log
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l    # 期望 150
ls results/runs/cora_GCN_r0.05/*/seed*/collateral.json | wc -l # 期望 150
```

### 4.3 跑完后 launch B.4 cora_GAT

```bash
nohup python experiments/run.py experiments/configs/phase_b_cora_gat.yaml \
    > logs/phase_b_cora_gat_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b_cora_gat.pid
```

### 4.4 跑完后 gate

```bash
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
```

期望 150/150 PASS 各自一份。

### 4.5 数据打包

```bash
tar czf cora_results.tar.gz results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05
```

---

## 5. 机器 B（H800 80GB）— arxiv workload

### 5.1 镜像保存与切换（**必做**，省去重装环境）

**当前 4090 实例**上：

```
autodl 控制台 → 实例 → 更多操作 → 保存镜像
镜像名建议: gnn-pytorch-2.1-cu118-2026-05-05
```

保存耗时 10-30 min，~¥0.3-0.5/天存储费。期间可以正常跑 B.3。

**创建 H800 新实例**：

```
autodl 控制台 → 创建实例 → 选 H800 80G
镜像选: 我的镜像 → 选刚保存的
GPU 数量: 1
计费: 按量
```

> 不选 PRO 6000：那是 Blackwell sm_100，PyTorch 2.1+cu118 不支持。
> 不选 vGPU/A6000：48GB 显存不够 tracin 的 ~68 GB 需求。

### 5.2 H800 上首次连进去验证

```bash
ssh ...new-h800-instance
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master

# 验证 GPU + env 都齐
nvidia-smi                                  # 看到 H800 + 80GB
python -c "import torch; print(torch.__version__, torch.cuda.is_available()); torch.zeros(1).cuda()"
                                            # 应输出 'True' + 无 'no kernel image' 错
git pull --ff-only && git log --oneline -3
tmux new -s phaseB
```

### 5.3 补 B.1 三个 OOM 的 collateral（~5 min）

cat 一个补数脚本进去（系统盘转过来后是不存在的，因为本地写过没 commit）：

```bash
cat > scripts/redo_collateral.sh << 'EOF'
#!/bin/bash
EXTRA="--num_epochs 200 --batch_size 256 --gcn_num_layers 3 --gcn_hidden 256"
for method in GIF GNNDelete IDEA GraphEraser MEGU; do
    out="results/runs/ogbn-arxiv_GCN_r0.05/${method}_random/seed42"
    if [ -f "$out/collateral.json" ] && [ "$(du -k "$out/collateral.json" | cut -f1)" -gt 0 ]; then
        echo "[skip] $method"
        continue
    fi
    echo "[run] $method"
    python eval_collateral.py \
        --dataset_name ogbn-arxiv --base_model GCN \
        --unlearning_methods $method --strategies random \
        --unlearn_ratio 0.05 --random_seed 42 \
        --cuda 0 --save_predictions \
        --output_dir "$out" \
        $EXTRA 2>&1 | tee -a /tmp/redo_collateral.log
done
EOF
bash scripts/redo_collateral.sh
```

H800 80GB 上单 cell retrain ~30s × 3 = ~2 min 完事。

### 5.4 验证 + gate B.1

```bash
bash scripts/diag_b1.sh
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml \
    --f1-min 0.55 --f1-max 0.85
```

期望：5/5 attack + 5/5 collateral + 5/5 predictions，gate exit 0。

### 5.5 探针验 H800 真实显存（~5 min，可选但建议）

```bash
python scripts/feasibility_selection_only.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --candidate_subset_size 1000 --strategies tracin
```

看 peak_mem(MB)：在 4090 上 ~5.9 GB，H800 上数字应类似（机器无关）。外推 mem_full ~68 GB，<80 GB 的 H800 容量 → ✅ 安全。

### 5.6 launch B.2（~22-25h）

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b_arxiv.pid
echo "PID: $(cat logs/phase_b_arxiv.pid)"

# Ctrl-b d detach 出 tmux
```

36 cell = 3 method × 4 strategy × 3 seed。预计：
- 9 random cell × ~10 min = 1.5h
- 9 im cell × ~3 min = 0.5h
- 9 tracin cell × ~50 min = 7.5h
- 9 hybrid cell × ~50 min = 7.5h
- 加 GU+retrain+MIA per cell ~20 min × 36 = 12h
- **总计 ~25-30h on H800 80GB**，¥6-13/h × 25h ≈ **¥150-325**

### 5.7 监控（detach 后或新窗格）

```bash
tail -f logs/phase_b_arxiv_*.log
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json | wc -l    # 期望 36
grep -c "SelectionCache.*HIT" logs/phase_b_arxiv_*.log                # 看 cache 命中
nvidia-smi                                                              # GPU 状态
```

### 5.8 跑完后 gate

```bash
python scripts/gate_runs.py experiments/configs/phase_b_arxiv.yaml --f1-min 0.55 --f1-max 0.85
```

### 5.9 数据打包

```bash
tar czf arxiv_results.tar.gz results/runs/ogbn-arxiv_GCN_r0.05
```

---

## 5A. 机器 B 替代路径 — H20 异区 fresh-clone（无镜像可用）

### 5A.1 何时走这条

当 §5.1 的"镜像复用"方案不可用时：
- H20 等机器在 autodl 不同区，autodl-fs 不互通，没法从 4090 把 B.1 attack 数据搬过来
- 或者代码大重构后，4090 上的旧 B.1 attack 数据已 stale（pre-refactor），不能与新代码混用

H20 显存 96GB > 80GB（H800），TracIn G-matrix 68GB peak 仍宽松；算力约 H800 的 1/3，B.2 总耗预估从 H800 ~25h 拉到 H20 ~38-40h。

### 5A.2 装环境（~10-15 min on H20）

```bash
source /etc/network_turbo
cd ~
git clone -b nips-prep https://github.com/lelelelelelelelelelelelele/OpenGU.git
cd OpenGU
pip install torch_scatter==2.1.2 torch_sparse==0.6.18 \
    -f https://data.pyg.org/whl/torch-2.1.2+cu118.html
pip install -r requirements.txt

cd GULib-master
python -c "
import torch, torch_geometric, ogb, yaml
print('torch:', torch.__version__, '| cuda:', torch.cuda.is_available())
print('GPU:', torch.cuda.get_device_name(0), '| capability:', torch.cuda.get_device_capability(0))
torch.zeros(1).cuda(); print('cuda alloc ok')
"

which tmux || apt update && apt install -y tmux
tmux new -s phaseB
```

> 默认 autodl PyTorch 镜像若不是 `2.1.x+cu118` 而是 `2.3.x+cu121`，把 torch_scatter / torch_sparse 的 wheel URL 换成 `https://data.pyg.org/whl/torch-2.3.0+cu121.html`。

### 5A.3 B.0 烟测

→ 见顶层 **§B.0 烟测**（任意 GPU 通用，跟 H20 无关，提到顶层方便查）。

跑通 B.0（gate exit 0）才往下走 §5A.4。FAIL 不继续。

### 5A.4 B.1 nohup launch（~75-120 min on H20，5 cell）

`phase_b_arxiv_feasibility.yaml` = 5 GU method × random × seed=42，在 arxiv 上的 random baseline。**注意：本路径下不存在"补 collateral"概念**——所有 5 个 cell 都从零跑（attack + collateral 一并出）。

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml \
    > logs/phase_b1_arxiv_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b1_arxiv.pid
echo "PID: $(cat logs/phase_b1_arxiv.pid)"

sleep 15
ps -p $(cat logs/phase_b1_arxiv.pid) -o pid,etime,cmd
tail -30 logs/phase_b1_arxiv_*.log
nvidia-smi | head -12

# Ctrl-b d  detach
```

### 5A.5 监控 + gate B.1

```bash
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/attack.json | wc -l       # 渐增 → 5
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/collateral.json | wc -l   # 渐增 → 5
tail -50 logs/phase_b1_arxiv_*.log

# 5/5 都有后过 gate
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml \
    --f1-min 0.55 --f1-max 0.85
```

`exit 0` = 通过 → 接 §5.6 launch B.2，或者跑 hybrid alpha sweep（用新加的 ScoreCache infra，见 `attack/score_cache.py` 和 `scripts/sweep_hybrid_alpha.py`）。

### 5A.6 红线

| 现象 | 含义 | 处理 |
|---|---|---|
| B.0 ImportError / `no kernel image` | env 没装对 / cu118 wheel 不认 H20 sm_90 | 贴 traceback；wheel 切到 cu121 版（见 §5A.2 备注） |
| B.0 `mia_auc=0.0` 或 `=1.0` | 老 bug 复发或 cache 污染 | 清缓存：`find results/cache results/selection_cache results/score_cache -name '*.json' -delete -o -name '*.npz' -delete`，再跑 |
| B.0 `f1_before < 0.5` | refactor 改坏了 cora 训练路径 | 贴 b0.log 全文 |
| B.1 OOM on H20 96GB | 不该发生 | 查 hidden=256 / num_layers=3 是否被覆盖；贴 traceback |
| B.1 全 5 cell `mia_auc` 同值 | dispatcher / cache key bug | 跑 `python scripts/diag_mia_dup.py` |
| `git pull --ff-only` 在重新 ssh 后报 conflict | 4090 / 本地推了新代码，H20 上之前手动 patch 过 | `git stash` 后再 pull，再决定 stash drop / pop |

### 5A.7 之后接什么

- **B.2（36 cell, ~38-40h on H20）**：见 §5.6
- **Hybrid alpha sweep**：见 `scripts/sweep_hybrid_alpha.py`，第一次跑 arxiv 时建 IF/IM ScoreCache（~50-100 min），之后每个 alpha 秒回
- **B.4 cora_GAT**：H20 不该跑 cora（屠龙刀杀鸡），让 4090 跑（§4.3）

---

## 6. 数据回收（两机都跑完之后）

机器 A 上：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
tar czf cora_results.tar.gz results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05
ls -lh cora_results.tar.gz
```

机器 B 上：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
tar czf arxiv_results.tar.gz results/runs/ogbn-arxiv_GCN_r0.05
ls -lh arxiv_results.tar.gz
```

本地 PowerShell 拉两个 tarball：

```powershell
scp 4090-host:~/autodl-fs/OpenGU/GULib-master/cora_results.tar.gz H:\project\OpenGU\GULib-master\
scp h800-host:~/autodl-fs/OpenGU/GULib-master/arxiv_results.tar.gz H:\project\OpenGU\GULib-master\
cd H:\project\OpenGU\GULib-master
tar xzf cora_results.tar.gz
tar xzf arxiv_results.tar.gz
```

通知我"phase B 数据回来了" → Phase C（重画 figure、Table 1 数字、abstract refresh）。

---

## 7. 故障速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `mia_auc: 0.000` 在 B.0 输出里 | bug 没修干净或缓存污染 | `find results/cache results/selection_cache -name '*.json' -delete`，再 `--force` 重跑 |
| nohup 里 `failed_attack: N` + `elapsed: <30s`（全部 cell 立刻挂） | 子进程 import / argparse / 早期 segfault；nohup buffer 吞了 traceback | 跳到 §0.9 前台单 cell 跑，让 traceback 直出 terminal |
| `Error during unlearning: CUDA out of memory` | retrain 显存不够（24GB 卡上 arxiv） | 切到 H800 80GB；或 `--gcn_hidden 128` 降配 |
| `no kernel image is available for execution on the device` | GPU 架构 PyTorch 不支持（如 Blackwell + cu118） | 换 H800/A100 (sm_90)，或装 PyTorch 2.4+cu124 |
| `ImportError: torch_scatter` | wheel mismatch | `pip install torch_scatter==2.1.2 -f https://data.pyg.org/whl/torch-2.1.2+cu118.html` |
| 4090 跑 B.2 没看到 `[SelectionCache] HIT` | cache 不在或解压到错地方 | 在 GULib-master 根目录 `tar xzf selection_cache.tar.gz` |
| B.1 gate FAIL | 看具体哪 cell 哪条没过，按 OOM 处理或贴给我 | `python scripts/gate_runs.py xxx.yaml` 输出会列原因 |
| SSH 断了任务停了 | 没用 nohup | 必须用 §5.6 那种 `nohup ... &` 写法 |
| tmux 找不到会话 | 实例重启 | autodl 实例如果停过电，所有 tmux 会话都没了；重 `tmux new -s phaseB` |
| 磁盘满 | results/runs 涨太快 | `du -sh results/*` 看哪个大；arxiv 结果可能 10+GB |
| 翻不到 OOM 日志 | tmux 默认 history 2000 行 | §3.3 调到 50000；或后台用 `tee /tmp/log.txt` |
| autodl 实例显示"运行中"但 ssh 不上 | 网络抽风 | 控制台"重启实例"，**注意会杀掉所有 tmux 会话** |

---

## 8. 一键脚本（懒人复制）

### 8.1 机器 A：cora 全跑（B.3 + B.4 串行，~6-10h）

```bash
cd ~/autodl-fs/OpenGU/GULib-master && \
mkdir -p logs && \
nohup bash -c '
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml && \
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
' > logs/cora_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/cora_full.pid
```

### 8.2 机器 B：B.1 补 + 探针 + B.2 一键串

```bash
cd ~/autodl-fs/OpenGU/GULib-master && \
git pull --ff-only && \
mkdir -p logs && \
nohup bash -c '
bash scripts/redo_collateral.sh && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv.yaml
' > logs/h800_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/h800_full.pid
```

---

## A. 附录：首次部署（已完成，仅供参考）

部署一台**新**服务器从零到现在状态的步骤。镜像方案下不再需要，但万一镜像丢了用得上。

### A.1 拿代码

```bash
source /etc/network_turbo
cd ~
git clone https://github.com/lelelelelelelelelelelelele/OpenGU.git
cd OpenGU
git checkout nips-prep
unset http_proxy https_proxy
```

GitHub 慢的 fallback：用 `https://ghproxy.com/` 前缀，或加 `--depth 1 -b nips-prep` shallow clone。

### A.2 验环境

autodl 的 PyTorch / 2.1.2 / 3.10 / cu118 镜像默认装好了 torch + torchvision。先跑：

```bash
python -c "import torch; print(torch.__version__, 'cuda:', torch.cuda.is_available())"
```

如果是 `2.1.2+cu118 cuda: True` 就跳到 A.3。否则按 A.4 从零装。

### A.3 装 PyG + 项目依赖

```bash
pip install torch_scatter==2.1.2 torch_sparse==0.6.18 \
    -f https://data.pyg.org/whl/torch-2.1.2+cu118.html
cd ~/OpenGU/GULib-master
pip install -r requirements.txt
```

### A.4 从零装 torch（只有 A.2 失败才用）

```bash
conda create -n gnn python=3.10 -y
conda activate gnn
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 \
    --index-url https://download.pytorch.org/whl/cu118
# 然后 A.3
```

### A.5 完整自检

```bash
cd ~/OpenGU/GULib-master
python -c "
import torch, torch_geometric, torch_scatter, torch_sparse, yaml, ogb
print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())
print('PyG:', torch_geometric.__version__)
print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')
"
```

期望全过且 `cuda: True`。
