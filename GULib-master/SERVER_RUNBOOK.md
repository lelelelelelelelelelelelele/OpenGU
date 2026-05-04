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

5 cells（5 method × random × seed=42）。完成后人工对照 `self/dashboard/EXPERIMENT_DASHBOARD.md §5.3.2.1` 的 11 项 metric 闸：

- F1_clean / F1_unlearn / F1_retrain 在 `[0.55, 0.85]` 范围
- mia_auc 非 0、非 1
- gap、collateral、hop_decay 4 桶都有数

**fail 不要进 B.2**——B.2 是 12+ GPU-h，跑废了租金最痛。fail → `attack.json` + `_meta.json` 粘给我。

✅ 通过 → 进 B.2

### B.2 · arxiv 主矩阵（~12-30 GPU-h）💰 最贵

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
| `mia_auc: 0.000` 在 B.0 输出里 | bug 没修干净或缓存污染 | `rm -rf results/cache/*.json results/selection_cache/*.json`，再 `--force` 重跑 |
| `ImportError: torch_scatter` | wheel mismatch | 用 `-f https://data.pyg.org/whl/torch-2.1.2+cu118.html` 重装 |
| B.1 metric 闸不过 | 真 bug 或数据问题 | **停下**，把 `attack.json` + `_meta.json` 发我 |
| SSH 断了 nohup 任务停了 | 没用 nohup | 必须用 §2 B.2 那种 `nohup ... &` 写法 |
| tmux 找不到会话 | 实例重启 | 实例如果停过电，所有 tmux 会话都没了；重 `tmux new -s phaseB` |
| 磁盘满 | results/runs 涨太快 | `du -sh results/*` 看哪个大；arxiv 结果可能 10+GB |
| autodl 实例显示"运行中"但 ssh 不上 | 网络抽风 | 控制台"重启实例"，**注意会杀掉所有 tmux 会话** |

---

## 5. 一键脚本（懒人复制）

**B.0 + B.1 一键串行**（首次跑这个，~1.5h）：
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
