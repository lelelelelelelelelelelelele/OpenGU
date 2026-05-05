# 服务器执行手册 v4 — Phase B 双机执行

> v4 重写: 2026-05-06。原 v3 740 行散在 §5 / §5A / §0.9，本版按"先看什么 → 跑什么 → 出问题怎么办"线性整理。
> NeurIPS 截稿: 2026-05-07。

---

## 0. TL;DR — 我现在该跳到哪节

| 我现在的状态 | 跳到 |
|---|---|
| 第一次进这个 runbook | §1 + §2 + §3 |
| 刚 ssh 进任意一台 | §2 |
| 要烟测一下环境 | §3.1 (B.0) |
| 4090 实例上要启 cora 大跑 | §3.5 (机器 A) |
| 80GB 实例上要启 arxiv 大跑 | §3.3 → §3.4 (机器 B) |
| 全新 H800/H20，没有镜像 | §4 (fresh-clone) → 然后 §3 |
| nohup 跑了几秒就 fail / 5 cell 全挂 | §5.1 ⭐ |
| OOM / cache 错 / 各种红字 | §5 |
| 两机都跑完，要回收数据 | §6 |

---

## 1. 阶段总览

### 1.1 Phase 表

| Phase | 内容 | 哪台 | 估时 | yaml |
|---|---|---|---|---|
| **B.0** | sanity 烟测：cora + GIF + random + seed42 | 任意 | ~20s | `sanity_one_cell.yaml` |
| **B.1** | arxiv 5 GU method × random × seed42（feasibility baseline） | B | ~75-120 min | `phase_b_arxiv_feasibility.yaml` |
| **B.2** | arxiv 3 method × 4 strategy × 3 seed = 36 cell（核心数据） | B | ~25-30h | `phase_b_arxiv.yaml` |
| **B.3** | cora_GCN 5 method × 6 strategy × 5 seed = 150 cell | A | ~3-5h | `phase_b_cora_gcn.yaml` |
| **B.4** | cora_GAT 同上 = 150 cell | A | ~3-5h | `phase_b_cora_gat.yaml` |
| Prewarm（可选） | 跨 cell 共享 IF/IM 选择，B.2 前跑节省 alpha-sweep | B | ~50-100 min | — |

### 1.2 时长 & 显存参考（看这张表决定"是否合理"）

每 cell 平均成本，按 strategy/数据集分类：

| dataset | strategy | 时长（H800 80GB） | 时长（4090 24GB） | peak mem | 备注 |
|---|---|---|---|---|---|
| cora | 任意 | <1 min | <1 min | <4 GB | cora 全套都不挑卡 |
| arxiv | random | ~10 min | ~10 min | ~8 GB | selection 0.002s，瓶颈在 GU+retrain |
| arxiv | im (CELF) | ~3 min | ~3 min | ~8 GB | yaml 必须带 `candidate_fraction=0.1, mc_rounds=50` |
| arxiv | **tracin** | **~50-90 min** | ~81 min（已测） | **~68 GB** | **24GB 卡 OOM**；候选 = 全 train ~90K，逐节点 backward |
| arxiv | hybrid | ~50-90 min（首次） | ~81 min（首次） | ~68 GB | IF + IM 共用 ScoreCache，第二次同 (dataset, model, seed, ratio) 几秒回 |
| arxiv | retrain（collateral） | ~30s | ~22 GB peak | — | 24GB 卡边缘 OOM，必须走 80GB |

⚠ **TracIn 1.5h 是正常的**。`tracin_strategy.py:_compute_tracin_scores` 里候选数 = `train_mask` ≈ 90K，每个节点一次 backward retain_graph。Forward-once 优化（commit `6b7285b`）只把时间砍半（~3h → ~1.5h），mem 没变。要再压：yaml 加 `candidate_fraction=0.1` 限流（10× 加速，但改语义，论文要写）。

### 1.3 双机分工 & 数据合并

| 机器 | GPU | 角色 | 跑 |
|---|---|---|---|
| **A** | RTX 4090 24GB | cora workload | B.0 + B.3 + B.4（300 cell） |
| **B** | H800 / H20 / A100 ≥80GB | arxiv workload | B.0 + B.1 + B.2（41 cell） |

不冲突：各自写 `results/runs/{dataset}_*` 不同子目录。跑完 §6 各 tar 一份 scp 回本地合并。

**显存红线**（违反则不能跑该 cell）：
- arxiv tracin / hybrid → ≥80GB
- arxiv collateral retrain → ≥40GB（24GB 边缘 OOM）
- arxiv random / im → ≥16GB（24GB 也行）
- cora 全套 → 任意

---

## 2. 每次 ssh 都做的三步

```bash
# 1) 进实例
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master   # 或 ~/OpenGU/GULib-master 看部署位置

# 2) 进会话（Ctrl-b d 是 detach；Ctrl+C 之后会话还在）
tmux attach -t phaseB || tmux new -s phaseB

# 3) 同步 + 检查
unset http_proxy https_proxy
git pull --ff-only && git log --oneline -3
```

> **VSCode 用户**：`Ctrl-b` 被侧边栏拦截。先鼠标点 terminal 再按；或一次性把 prefix 改成 `Ctrl-a`：
> ```bash
> printf 'set -g prefix C-a\nunbind C-b\nbind C-a send-prefix\nset -g history-limit 50000\n' > ~/.tmux.conf
> tmux kill-server && tmux new -s phaseB
> ```

---

## 3. Phase 执行流程（按顺序）

> 全部 phase 都遵循同一个回路：**`yaml → run.py → gate_runs.py`**。
> `run.py` 吃 yaml 展开 (method, strategy, seed) 矩阵，每 cell 跑 `demo_attack` + `eval_collateral`，写四件 (`attack.json`, `collateral.json`, `predictions.npz`, `_meta.json`) 到 `results/runs/{cell}/seed{N}/`。
> `gate_runs.py` 自动 PASS/FAIL：4 件齐 + `mia_auc∈(0.001, 0.999)` + `f1_before∈[min,max]` + `gap` 是有限数。

### 3.1 B.0 — 烟测（任意机，~20s，每次大跑前必跑）

```bash
python experiments/run.py experiments/configs/sanity_one_cell.yaml 2>&1 | tee /tmp/b0.log
ls -la results/runs/cora_GCN_r0.05/GIF_random/seed42/   # 4 件齐？
python scripts/gate_runs.py experiments/configs/sanity_one_cell.yaml --f1-min 0.7
```

`gate exit 0` = 通过。FAIL → §5.1，**不要继续上 B.1+**。

> 关于 `gate_runs.py`：node task 下 `attack.json[results][strategy].f1_before` 恒为 `None`（`pipeline_adapter.py:285` 只 edge task 才填），gate 已绕开这个字段。别自己 inline `python -c` 读 `f1_before`。

### 3.2 现在跑到哪了 — 实时计数

```bash
# B.0
ls results/runs/cora_GCN_r0.05/GIF_random/seed42/_meta.json 2>/dev/null && echo B.0 done

# B.1（期望 5）
ls results/runs/ogbn-arxiv_GCN_r0.05/*_random/seed42/attack.json     2>/dev/null | wc -l
ls results/runs/ogbn-arxiv_GCN_r0.05/*_random/seed42/collateral.json 2>/dev/null | wc -l

# B.2（期望 36 = 3 method × 4 strategy × 3 seed）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json | wc -l

# B.3 / B.4（各期望 150）
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l
```

### 3.3 B.1 — arxiv random baseline（机 B，~75-120 min）

只 5 cell，random only。验三件：(a) refactor 后端到端通；(b) GU 方法在 169K 节点 arxiv 上不崩；(c) gate 的 f1 范围设对了。

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml \
    > logs/phase_b1_arxiv_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b1_arxiv.pid
echo "PID: $(cat logs/phase_b1_arxiv.pid)"

# 15s 后看是不是真起来了（不是 import 阶段秒挂）
sleep 15
ps -p $(cat logs/phase_b1_arxiv.pid) -o pid,etime,cmd
tail -30 logs/phase_b1_arxiv_*.log
nvidia-smi | head -12

# Ctrl-b d  detach 出 tmux
```

**或者交互式跑（前台 + tee，能盯着看）**：

```bash
mkdir -p logs
LOG=logs/phase_b1_arxiv_$(date +%Y%m%d_%H%M).log

# tmux 会话里前台跑，stdout 同时进 terminal 和 logfile
python -u experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml 2>&1 | tee "$LOG"

# 中途要走：Ctrl-b d  detach（任务继续跑），回来 tmux attach -t phaseB
# 真要停：tmux 里 Ctrl+C
```

`-u` 关 Python 输出 buffering，否则 tee 看不到实时进度。

> **nohup vs 交互式没本质区别**——cell-level checkpoint 在 `results/runs/`、ScoreCache / SelectionCache 在 autodl-fs 持久盘，tmux 死或实例重启都最多丢当前 mid-flight 那一个 cell，重 ssh + attach + 重跑同 yaml 自动跳过已完成的。**真正的风险是账户欠费实例被销毁**，这个 nohup 也救不了。任选。

跑完后：

```bash
bash scripts/diag_b1.sh   # 当前 cell 输出 + log 错误尾
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml --f1-min 0.55 --f1-max 0.85
```

> **如果 B.1 是从 4090 镜像继承过来的**（已有 5/5 attack 但 collateral 缺）：跳过上面 nohup，跑 §A.1 的 `redo_collateral.sh` 单补 collateral，~5 min 完事。
>
> **如果是 fresh-clone**（机器 B 上之前没跑过 attack）：上面 nohup 全跑，attack + collateral 一起出。两条路径**不要混用**——pre-refactor 的 attack 数据跟新代码混会污染。

### 3.4 B.2 — arxiv 全矩阵（机 B，~25-30h）

**前置**：B.0 PASS + B.1 PASS（5/5 attack + 5/5 collateral + gate exit 0）。

可选 prewarm（见 §3.6）：如果要做 hybrid alpha-sweep 或同 (method, strategy) 跨 seed 复用 selection，先跑 prewarm 把 IF/IM 算好缓存，B.2 里 9 个 hybrid cell 后续 alpha 秒回。**仅跑 1 套 alpha 不需要 prewarm**。

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/phase_b_arxiv.pid
# Ctrl-b d
```

**或者交互式（tmux 前台 + tee）**：

```bash
mkdir -p logs
LOG=logs/phase_b_arxiv_$(date +%Y%m%d_%H%M).log
python -u experiments/run.py experiments/configs/phase_b_arxiv.yaml 2>&1 | tee "$LOG"
# 中途要走：Ctrl-b d
```

B.2 ~25h，但 cell-level checkpoint + ScoreCache 都在 autodl-fs 持久盘，tmux 或实例真挂了也最多丢 1 个 mid-flight cell，重跑同 yaml 自动跳过完成的。任选。

预算（H800 80GB，36 cell）：
- 9 random × 10 min = 1.5h
- 9 im × 3 min = 0.5h
- 9 tracin × 50 min = 7.5h（首次填 ScoreCache，同一 (dataset,model,seed,ratio) 第二次秒回）
- 9 hybrid × 50 min = 7.5h（命中 IF/IM cache 则 < 1 min）
- 加 GU+retrain+MIA per cell ~20 min × 36 = 12h
- **total ~25-30h**，¥6-13/h × 25h ≈ **¥150-325**

监控：

```bash
tail -f logs/phase_b_arxiv_*.log
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json | wc -l   # 渐增 → 36
grep -c "ScoreCache.*HIT\|SelectionCache.*HIT" logs/phase_b_arxiv_*.log
nvidia-smi
```

跑完 gate：

```bash
python scripts/gate_runs.py experiments/configs/phase_b_arxiv.yaml --f1-min 0.55 --f1-max 0.85
```

### 3.5 B.3 + B.4 — cora（机 A，串行 ~6-10h）

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs

# 串行：GCN 完了直接接 GAT
nohup bash -c '
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml && \
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
' > logs/cora_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/cora_full.pid
# Ctrl-b d
```

**或者交互式（tmux 前台 + tee）**：

```bash
mkdir -p logs
LOG=logs/cora_full_$(date +%Y%m%d_%H%M).log
{ python -u experiments/run.py experiments/configs/phase_b_cora_gcn.yaml && \
  python -u experiments/run.py experiments/configs/phase_b_cora_gat.yaml && \
  python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
  python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml; } 2>&1 | tee "$LOG"
# Ctrl-b d 中途 detach
```

cora 全跑 ~6-10h，想盯实时输出选这条；checkpoint 同样在持久盘，断了重跑跳过已完成。

监控：

```bash
tail -f logs/cora_full_*.log
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l   # → 150
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l   # → 150
```

### 3.6 Prewarm — 何时跑（可选，机 B）

`scripts/prewarm_selection_cache.py` 把跨 cell 共享的 selection 提前算到 `results/selection_cache/` 和 `results/score_cache/`。

**何时值得跑**：
- 计划做 hybrid alpha-sweep（5+ alpha 值同一 (dataset, model, seed, ratio)）→ 跑一次 prewarm，sweep 阶段每 alpha < 1 min
- 跨 strategy / 跨 method 但同 IF 输入 → 第一次填，后续 cell 命中

**何时不跑**：B.2 yaml 的 36 cell 各 (method, strategy, seed) 不同，prewarm 帮不上多少（除非 IF cache key 复用）。直接 §3.4 nohup 让 run.py 自己 lazy 算。

如果要跑：

```bash
python scripts/prewarm_selection_cache.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --strategies tracin,im --seeds 42,123,2024 \
    --unlearn_ratio 0.05
# 之后再跑 §3.4 的 B.2 全矩阵，hybrid cell 会命中
```

ScoreCache key 故意不含 model_fingerprint（`tracin_strategy.py:115-133` 的 docstring 写了 why：跨进程 cuDNN 1e-5 权重漂移会让 fingerprint 失效，丢命中率 → 改用 (dataset, model, seed, ratio) 静态 key）。

---

## 4. 全新机器初始化

### 4.1 优先：从镜像复用（~10 min）

老实例上：autodl 控制台 → 实例 → 更多操作 → 保存镜像（~10-30 min，~¥0.3-0.5/天存储）。

新实例：创建实例 → 选 H800 80G → 镜像 → 我的镜像。

⚠ **GPU 选型**：
- ✅ H800 80GB / A100 80GB（sm_90，cu118 PyTorch 2.1.2 OK）
- ✅ H20 96GB（cu118 不一定认 sm_90，必要时 cu121；算力 ~H800 1/3，B.2 拉到 ~38-40h）
- ❌ PRO 6000（Blackwell sm_100，cu118 不支持）
- ❌ vGPU / A6000 48GB（tracin 68GB peak 不够）

### 4.2 备用：fresh-clone（无镜像或代码大改）

```bash
ssh ...new-instance
source /etc/network_turbo
cd ~

git clone -b nips-prep https://github.com/lelelelelelelelelelelelele/OpenGU.git
cd OpenGU/GULib-master

# autodl PyTorch 镜像默认 2.1.2+cu118，先验
python -c "import torch; print(torch.__version__, 'cuda:', torch.cuda.is_available())"
# 期望: 2.1.2+cu118 cuda: True

# 装 PyG 扩展
pip install torch_scatter==2.1.2 torch_sparse==0.6.18 \
    -f https://data.pyg.org/whl/torch-2.1.2+cu118.html
pip install -r requirements.txt

# 自检
python -c "
import torch, torch_geometric, torch_scatter, torch_sparse, ogb, yaml
print('torch:', torch.__version__, '| cuda:', torch.cuda.is_available())
print('GPU:', torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
torch.zeros(1).cuda(); print('alloc ok')
"

which tmux || apt update && apt install -y tmux
tmux new -s phaseB
```

> torch 不是 2.1.2+cu118 → wheel URL 切到对应版本（如 `torch-2.3.0+cu121.html`）。
> GitHub 慢 → `git clone --depth 1` 或加 `https://ghproxy.com/` 前缀。

### 4.3 完了 → §3.1 跑 B.0 验证

B.0 PASS 才往下跑 B.1+。FAIL 不继续。

---

## 5. 故障处理

### 5.1 nohup 全 5 cell 几秒就挂 ⭐

**症状**：log 里 `failed_attack: 5/5` + 各 cell `elapsed: <30s`，attack.json 一个都没出。

**含义**：子进程在 import / argparse / 早期 segfault 阶段挂了，nohup buffer 把 traceback 吞了。

**回滚流程**：

```bash
# 1) kill 跑飞的
ps -ef | grep -E "run\.py" | grep -v grep
kill <PID>; pkill -f "experiments/run.py"

# 2) 前台跑一个 cell 拿真 traceback（路径与 nohup 一致）
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml --limit 1

# 3) 还看不出 → 直接调 demo_attack（最薄，对照 yaml 看 args）
python demo_attack.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --unlearning_methods GIF --strategies random \
    --unlearn_ratio 0.05 --seed 42 \
    --num_epochs 200 --batch_size 256 --cuda 0 \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --save_path /tmp/test_attack.json

# 4) 修好之后回 nohup（别在前台跑全 5 cell，shell 一断又重来）
```

### 5.2 OOM / GPU 错

| 症状 | 处理 |
|---|---|
| `CUDA out of memory` 在 retrain 阶段 | 24GB 卡跑 arxiv collateral，必出。切 80GB 卡或 `--gcn_hidden 128` 降配（会改 baseline，论文一致性要管） |
| `CUDA out of memory` 在 tracin selection | <80GB 卡跑 tracin。切 H800/A100 80GB，或 yaml 加 `candidate_fraction=0.1` 限流 |
| `no kernel image is available` | GPU 架构 PyTorch 不支持（Blackwell sm_100 + cu118）。换 H800/A100，或 PyTorch 2.4+cu124 |
| `ImportError: torch_scatter` | wheel mismatch，按 §4.2 装回去 |

### 5.3 Cache 污染 / mia_auc 异常

```bash
# mia_auc=0.0 或 =1.0 → cache 污染或老 bug
find results/cache results/selection_cache results/score_cache \
    \( -name '*.json' -o -name '*.npz' \) -delete

# 别碰：results/runs/（实验输出）、data/processed/（dataset split）
```

### 5.4 速查

| 现象 | 处理 |
|---|---|
| 4090 跑 B.2 没看到 `[SelectionCache] HIT` | cache 没解压或路径错。根目录 `tar xzf selection_cache.tar.gz` |
| B.1 全 5 cell `mia_auc` 同值 | dispatcher / cache key bug。`python scripts/diag_mia_dup.py` |
| `git pull --ff-only` 报 conflict | 远端推了新代码本地有 patch。`git stash && git pull && git stash pop` |
| SSH 断了 | tmux 会话 + 进程不受影响（tmux 守在服务器端），重 ssh + `tmux attach -t phaseB` 接着看 |
| tmux 找不到会话（实例真重启过） | 所有会话清零，但 cell-level checkpoint 在 `results/runs/`、cache 在 autodl-fs 持久盘。`tmux new -s phaseB` 重起，重跑同 yaml 自动跳过完成的 cell |
| autodl 实例显示运行中但 ssh 不上 | 网络抽风。等几分钟或控制台"重启实例"——重启会杀 tmux + 进程，但持久盘数据还在，按上一行处理 |
| 磁盘满 | `du -sh results/*`；arxiv 单 cell ~140K × 36 + npz 大头，总 ~10GB |
| 翻不到 OOM 日志 | tmux 默认 history 2000 行。`set -g history-limit 50000` 或 `tee /tmp/log.txt` |

紧急停止任务：

```bash
ps -ef | grep -E "run\.py|prewarm" | grep -v grep
kill <PID>             # 优雅
kill -9 <PID>          # 不响应再这样
pkill -f "experiments/run.py"
```

---

## 6. 数据回收（两机都跑完之后）

机器 A：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
tar czf cora_results.tar.gz results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05
ls -lh cora_results.tar.gz
```

机器 B：

```bash
cd ~/autodl-fs/OpenGU/GULib-master
tar czf arxiv_results.tar.gz results/runs/ogbn-arxiv_GCN_r0.05
ls -lh arxiv_results.tar.gz
```

本地 PowerShell：

```powershell
scp 4090-host:~/autodl-fs/OpenGU/GULib-master/cora_results.tar.gz H:\project\OpenGU\GULib-master\
scp h800-host:~/autodl-fs/OpenGU/GULib-master/arxiv_results.tar.gz H:\project\OpenGU\GULib-master\
cd H:\project\OpenGU\GULib-master
tar xzf cora_results.tar.gz
tar xzf arxiv_results.tar.gz
```

通知 "phase B 数据回来了" → 进 Phase C（figure / Table 1 / abstract refresh）。

---

## 附录 A — 一次性脚本

### A.1 redo_collateral.sh（B.1 缺 collateral 时单补）

```bash
cat > scripts/redo_collateral.sh << 'EOF'
#!/bin/bash
EXTRA="--num_epochs 200 --batch_size 256 --gcn_num_layers 3 --gcn_hidden 256"
for method in GIF GNNDelete IDEA GraphEraser MEGU; do
    out="results/runs/ogbn-arxiv_GCN_r0.05/${method}_random/seed42"
    if [ -f "$out/collateral.json" ] && [ "$(du -k "$out/collateral.json" | cut -f1)" -gt 0 ]; then
        echo "[skip] $method"; continue
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
chmod +x scripts/redo_collateral.sh
bash scripts/redo_collateral.sh
```

H800 上 5 cell 共 ~2-5 min。

### A.2 显存外推探针

```bash
python scripts/feasibility_selection_only.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --candidate_subset_size 1000 --strategies tracin
```

输出 peak_mem(MB)。subset=1000 时 ~5.9 GB，外推全量 N=135474 → ~68 GB peak（**注意：脚本默认线性外推会输出 "OOM 785 GB" 之类吓人数字，那是 forward 固定开销被错误线性外推；真值 ~68 GB**）。

### A.3 机器 B 一键串：B.1 补 + 探针 + B.2

```bash
cd ~/autodl-fs/OpenGU/GULib-master && git pull --ff-only && mkdir -p logs
nohup bash -c '
bash scripts/redo_collateral.sh && \
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_feasibility.yaml --f1-min 0.55 --f1-max 0.85 && \
python experiments/run.py experiments/configs/phase_b_arxiv.yaml
' > logs/h800_full_$(date +%Y%m%d_%H%M).log 2>&1 &
echo $! > logs/h800_full.pid
```

### A.4 监控命令汇总

```bash
# 实时日志
tail -f logs/<name>.log

# cache 命中率
grep -cE "ScoreCache.*HIT|SelectionCache.*HIT|ResultCache.*HIT" logs/<name>.log

# 进度计数
ls results/runs/<dataset>_<model>_r<ratio>/*/seed*/attack.json | wc -l

# 资源
nvidia-smi
watch -n 2 nvidia-smi
df -h ~
du -sh results/
```

---

## 附录 B — 各 cell 内部时序

调试卡死位置必看 `self/attack_flow.md`。每 cell 大致：
1. base train（CPU+GPU 满，~1-3 min on arxiv）
2. selection（strategy 决定，详见 §1.2 表）
3. unlearn（GU 方法决定，~1-15 min）
4. retrain from scratch（peak mem 在这，~30s on H800 / OOM on 4090 for arxiv）
5. MIA（CPU bound，~6 min × 2 rounds for GraphEraser；GPU idle）
6. 写 4 件 + collateral.json
