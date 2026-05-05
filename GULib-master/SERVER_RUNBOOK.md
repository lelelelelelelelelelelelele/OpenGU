# 服务器执行手册 v2 — Phase B 执行

> 创建: 2026-05-04 · 更新: 2026-05-05
> NeurIPS 截稿: 2026-05-07（剩 2 天）
> 状态：env + clone ✅ 已完成 → 现在跑 Phase B

---

## ✅ 已完成（简略）

| 项 | 状态 |
|---|---|
| 代码 | `~/OpenGU/GULib-master` @ `nips-prep` |
| Python / torch | 3.10 / 2.1.2+cu118 |
| PyG / scatter / sparse | 2.6.1 / 2.1.2 / 0.6.18 |
| GPU | NVIDIA RTX 4090, cuda True |
| 缓存清理 | 全新 clone，无污染数据，**跳过** |

> 重新部署的话见 §A 附录。

---

## 0. 常用指令速查 ⭐

### 0.1 ssh 进来后三连

```bash
source /etc/network_turbo                 # 学术加速（每次都要，pip/git 走它快 5-10x）
cd ~/OpenGU/GULib-master                  # 项目根
tmux attach -t phaseB || tmux new -s phaseB   # 进或建 tmux
```

### 0.2 同步代码（每次本地 push 后）

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

```bash
# 在 tmux 里跑的前台任务：直接按 Ctrl+C 一次（一两秒不响应再按一次）
# 卡死在 numba/CUDA 不响应：Ctrl+\ 发 SIGQUIT 强退

# 后台 nohup 任务（B.2 用的那种）
ps -ef | grep -E "run\.py|prewarm" | grep -v grep   # 找 PID
kill <PID>                                # SIGTERM 优雅退
kill -9 <PID>                             # 不响应再来 SIGKILL

# 一键全杀（项目所有 python 进程，谨慎用）
pkill -f "experiments/run.py"
pkill -f "prewarm_selection_cache"

# 看 GPU 还在不在跑
nvidia-smi                                # 关心 GPU 利用率 + 进程 PID
watch -n 2 nvidia-smi                     # 每 2 秒刷新
```

### 0.5 清缓存（污染或 key 变更后）

```bash
# 只清 selection_cache（大多数情况这就够了）
find results/selection_cache -name '*.json' -delete

# 全清（B.0 sanity 出 mia_auc=0 时用）
find results/cache results/selection_cache -name '*.json' -delete

# 不要碰：results/runs/（实验输出）、data/processed/（数据集 split）
```

### 0.6 监控正在跑的任务

```bash
tail -f logs/phase_b_arxiv.log                              # 实时日志
ls results/runs/ogbn-arxiv_*/*/seed*/attack.json | wc -l    # 进度计数
grep -c "SelectionCache.*HIT" logs/phase_b_arxiv.log        # 看 cache 命中数
df -h ~                                                      # 看磁盘还剩多少
du -sh results/                                              # 看实验产出多大
```

---

## 1. tmux 工作流（每次 ssh 后第一件事）⭐

### 1.1 初次创建会话

```bash
# autodl 镜像没预装 tmux，第一次先装一下（root 默认，无需 sudo）
which tmux || apt update && apt install -y tmux

source /etc/network_turbo                  # 学术加速（每次 ssh 都要）
tmux new -s phaseB
# 进 tmux 后底栏出现绿条 [phaseB] 表示成功
```

> apt 卡的话备选：`screen -S phaseB`（多数镜像预装），detach 是 `Ctrl-a d`，重连 `screen -r phaseB`。

### 1.2 关键操作

| 动作 | 按键 | 说明 |
|---|---|---|
| **挂后台**（detach） | `Ctrl-b` 然后 `d` | VSCode 里先点一下 terminal 确保焦点 |
| 关 SSH / 关电脑 | — | 服务器上 tmux 继续跑 |
| **重新进会话** | `tmux attach -t phaseB` | 下次 ssh 进去后跑这个 |
| 列出所有会话 | `tmux ls` | |
| 在会话里开新 window | `Ctrl-b` 然后 `c` | 想并行跑监控时用 |
| 切 window | `Ctrl-b` 然后 `n` (下一个) / `p` (上一个) | |
| 关掉某个 window | `exit` 或 `Ctrl-d` | |

### 1.3 VSCode 用户特殊提示

VSCode 的 `Ctrl-B` 默认是侧边栏切换，会拦截 tmux prefix。**先用鼠标点一下 terminal**确保焦点在 terminal 再按 Ctrl-b。

不想这样就改 prefix（在服务器一次性配置）：
```bash
cat > ~/.tmux.conf <<'EOF'
set -g prefix C-a
unbind C-b
bind C-a send-prefix
EOF
tmux kill-server && tmux new -s phaseB
```
之后所有 `Ctrl-b` 改成 `Ctrl-a`。

---

## 2. Phase B 五步检查点（按顺序，B.1 后停一下）

每步前都先确认：
- 在 `~/OpenGU/GULib-master`
- 在 tmux `phaseB` 会话里（底栏看到 `[phaseB]`）

### B.0 · Sanity（~20 秒）

```bash
cd ~/OpenGU/GULib-master
python experiments/run.py experiments/configs/sanity_one_cell.yaml --force
```

**通过判据**：
- 退出码 0
- 屏幕看到 `wrote results/runs/cora_GCN_r0.05/GIF_random/seed42/attack.json`（4 个文件）
- ⚠ `mia_auc` 字段是 **非 0 的小数**（应在 0.3–0.6 区间），不是 `0.000`

✅ 通过 → 进 B.1
❌ `mia_auc: 0.000` 或其他错 → **停下问我**

### B.1 · arxiv 可行性闸（~1.5 GPU-h）⚠ 关键检查点

```bash
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml
```

**v3 矩阵（2026-05-05 起）**：5 cells = 5 method × **random** × seed=42。**仅测 GU 管线稳定性**（base train → unlearn → retrain → MIA 在 169K 节点图上不挂）。策略可行性（tracin OOM 风险、IM MC 时间）独立测试，见下面 §B.1.5。

> v2 (commit 81733b2) 把 tracin/im 也塞进来 × 5 method 是设计错误——selection 与 GU method 解耦（cross-method SelectionCache），tracin × 5 method 里有 4 个 cell 重复劳动。已在 commit 6b7285b 回滚。

> 已跑过的 5 个 random cell 仍然有效，runner 的 skip-if-exists 会跳过；首次跑大约 1.5h。

完成后人工对照 `self/dashboard/EXPERIMENT_DASHBOARD.md §5.3.2.1` 的 11 项 metric 闸：

- F1_clean / F1_unlearn / F1_retrain 在 `[0.55, 0.85]` 范围
- mia_auc 非 0、非 1
- gap、collateral、hop_decay 4 桶都有数

**fail 不要进 B.2**——B.2 是 12+ GPU-h，跑废了租金最痛。fail → `attack.json` + `_meta.json` 粘给我。

✅ 通过 → 进 B.1.5（分卡）或直接 B.2（单卡）

### B.1.5 · 分卡省钱：prewarm selection cache（可选，推荐）⭐ 新

**适用场景**：B.1 通过、想跑 B.2，但 tracin 在 arxiv 上需要 ~150min/cell × 9 cell ≈ 22h 大卡。把 selection（贵卡需求）和 GU+retrain+MIA（4090 就够）拆到两台机器。

**省的钱**：A100 80GB × 6h（仅 selection）+ 4090 × 11h（仅 GU）≈ $20 vs A100 全程 ≈ $42。

#### 先决条件：清空旧 selection cache

旧 cache 文件可能用了老的 key 方案（IM 在 2026-05-05 commit `af1c8ba` 前 key 含训练 seed），保留它们不会出错但占空间且容易混淆。**Phase B 开始前清一次**：

```bash
cd ~/OpenGU/GULib-master
ls results/selection_cache/*.json 2>/dev/null | wc -l    # 看有多少
find results/selection_cache -name '*.json' -delete       # 只删 json，保 CLAUDE.md
ls results/selection_cache/                               # 验证只剩 CLAUDE.md
```

> ⚠ **不要**碰 `results/runs/`（B.1a 的 5 个 random cell 在里面）和 `data/processed/`（数据集 split 缓存，重生不必要）。

#### Stage 1: 在 A100 80GB 上算 selection（~6h）

```bash
# 探针先确认 tracin 不会 OOM（~2 min）
python scripts/feasibility_selection_only.py \
    --dataset_name ogbn-arxiv --base_model GCN \
    --gcn_num_layers 3 --gcn_hidden 256 \
    --candidate_subset_size 1000 --strategies tracin

# 看输出 [extrapolation] 行的 mem_full(GB)：
#   <22 → 4090 也够，跳过分卡，直接走 B.2 单卡
#   22–44 → 租 A6000 48GB
#   >44   → 租 A100 80GB ⭐ 当前估计就在这一档

# 全量 prewarm（10 个独立 selection 计算，~6h）
nohup python scripts/prewarm_selection_cache.py \
    experiments/configs/phase_b_arxiv.yaml \
    > logs/prewarm.log 2>&1 &
echo $! > logs/prewarm.pid
tail -f logs/prewarm.log     # 监控

# 完成后打包（~5 MB tarball）
tar czf selection_cache.tar.gz results/selection_cache/
ls -lh selection_cache.tar.gz
```

#### Stage 2: scp 到 4090

```bash
# 在本地 PowerShell 中转
scp a100-host:~/OpenGU/GULib-master/selection_cache.tar.gz .
scp selection_cache.tar.gz 4090-host:~/OpenGU/GULib-master/

# 或两台之间直传（autodl 实例间同区域）
# 在 4090 上：scp a100-host:~/.../selection_cache.tar.gz .
```

#### Stage 3: 在 4090 上跑 GU（~11h，全 cache hit）

```bash
cd ~/OpenGU/GULib-master
git pull                                    # 确保代码同步
tar xzf selection_cache.tar.gz              # 解压 cache
ls results/selection_cache/*.json | wc -l   # 看到 ~10 个文件就对

# 跑 B.2 主矩阵 — selection 全部 HIT，只跑 GU + retrain + MIA
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv.log 2>&1 &
echo $! > logs/phase_b_arxiv.pid

# 监控（应该看到大量 "[SelectionCache] HIT"，每个 selection 复用时间 < 1ms）
grep -c "SelectionCache.*HIT" logs/phase_b_arxiv.log
```

✅ 进度满 36 cell → 进 B.3/B.4

---

### B.2 · arxiv 主矩阵（~12-30 GPU-h）💰 最贵（如不分卡）

**用 nohup 跑后台，断 SSH 不影响**：

```bash
mkdir -p logs
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv.log 2>&1 &
echo $! > logs/phase_b_arxiv.pid
```

36 cells = 3 method × 4 strategy × 3 seed。

**监控**（在 tmux 别的 window 里）：
```bash
tail -f logs/phase_b_arxiv.log              # 实时日志
ls results/runs/ogbn-arxiv_*/*/seed*/attack.json | wc -l    # 进度，最终 36
```

✅ 完成 → 进 B.3 / B.4

### B.3 / B.4 · cora 全矩阵（各 ~75–90 min）

**单卡**情况，B.2 跑完后串行：
```bash
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml
```

**双卡**情况（autodl 双卡实例），跟 B.2 并行：
```bash
# 新开一个 tmux window: Ctrl-b c
CUDA_VISIBLE_DEVICES=1 nohup python experiments/run.py \
    experiments/configs/phase_b_cora_gcn.yaml > logs/cora_gcn.log 2>&1 &
```

每个矩阵 150 cells，验证：
```bash
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l    # 期望 150
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l    # 期望 150
```

---

## 3. 数据回收（跑完之后）

服务器：
```bash
cd ~/OpenGU/GULib-master
tar czf phase_b_results.tar.gz results/runs/
ls -lh phase_b_results.tar.gz       # 看大小，估计几十 MB ~ 几百 MB
```

本地（PowerShell）：
```powershell
scp user@host:~/OpenGU/GULib-master/phase_b_results.tar.gz H:\project\OpenGU\GULib-master\
cd H:\project\OpenGU\GULib-master
tar xzf phase_b_results.tar.gz
```

回到本地告诉我 "phase B 数据回来了"，我跑 Phase C（重画 figure、Table 1 数字填入、abstract refresh）。

---

## 4. 故障速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `mia_auc: 0.000` 在 B.0 输出里 | bug 没修干净或缓存污染 | `find results/cache results/selection_cache -name '*.json' -delete`，再 `--force` 重跑 |
| 4090 跑 B.2 没看到 `[SelectionCache] HIT` | selection_cache.tar.gz 没解压或解压到错地方 | 在 GULib-master 根目录跑 `tar xzf selection_cache.tar.gz`，再 `ls results/selection_cache/*.json` 应有 ~10 个文件 |
| `ImportError: torch_scatter` | wheel mismatch | 用 `-f https://data.pyg.org/whl/torch-2.1.2+cu118.html` 重装 |
| B.1 metric 闸不过 | 真 bug 或数据问题 | **停下**，把 `attack.json` + `_meta.json` 发我 |
| SSH 断了 nohup 任务停了 | 没用 nohup | 必须用 §2 B.2 那种 `nohup ... &` 写法 |
| tmux 找不到会话 | 实例重启 | 实例如果停过电，所有 tmux 会话都没了；重 `tmux new -s phaseB` |
| 磁盘满 | results/runs 涨太快 | `du -sh results/*` 看哪个大；arxiv 结果可能 10+GB |
| autodl 实例显示"运行中"但 ssh 不上 | 网络抽风 | 控制台"重启实例"，**注意会杀掉所有 tmux 会话** |

---

## 5. 一键脚本（懒人复制）

**B.0 + B.1 一键串行**（首次跑这个，~5h）：
```bash
cd ~/OpenGU/GULib-master && \
python experiments/run.py experiments/configs/sanity_one_cell.yaml --force && \
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml && \
echo "B.0 + B.1 完成，停下来人工看 11 项 metric 闸"
```

**B.2 后台启动 + PID 记录**：
```bash
mkdir -p logs && \
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv.log 2>&1 & \
echo $! > logs/phase_b_arxiv.pid && \
echo "PID: $(cat logs/phase_b_arxiv.pid)，tail -f logs/phase_b_arxiv.log 监控"
```

---

## A. 附录：首次部署（已完成，仅供参考）

部署一台**新**服务器从零到现在状态的步骤。你这次已经走完了，重新部署或换机器再用。

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
cd ~/OpenGU
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
