# 服务器执行手册（Phase B 全量重跑）

> 创建: 2026-05-04 · 目标: 在租用 GPU 服务器上跑完 Phase B（B.0 → B.4）
> 本地分支: `nips-prep` @ `20264ec`
> NeurIPS 截稿: 2026-05-07（剩 3 天）

---

## 0. 你有两条路把代码送上去（任选其一）

### 路 A：git pull（推荐）

前提：服务器已经 clone 过仓库 `https://github.com/lelelelelelelelelelelelele/OpenGU.git`，并且 checkout 到 `nips-prep` 分支。

如果服务器是**全新机器**：
```bash
cd ~                # 或者你想放代码的地方
git clone https://github.com/lelelelelelelelelelelelele/OpenGU.git
cd OpenGU
git checkout nips-prep
```

> **autodl / 境内 GPU 服务器 GitHub 慢或超时？** 三种加速方案按顺序试：
>
> 1. **autodl 学术加速**（首选）：clone 之前先 `source /etc/network_turbo` 启用代理；clone 完后 `unset http_proxy https_proxy` 关掉，避免实验阶段下数据集走代理
> 2. **ghproxy 镜像**：`git clone https://ghproxy.com/https://github.com/lelelelelelelelelelelelele/OpenGU.git OpenGU`
> 3. **shallow clone**（只拿最新 commit，省 history）：在原命令加 `--depth 1 -b nips-prep`
>
> 全失败就走下面的"路 B"。

如果服务器**已经有旧版**：
```bash
cd ~/OpenGU         # 你之前 clone 的位置
git fetch origin
git pull origin nips-prep
git log --oneline -3
# 应看到顶部是: 20264ec chore: relax numpy pin + document server install path
```

> ⚠ 本地 working tree 当前是干净的（git status 无输出），所以服务器 pull 下来就是最新。如果你之后又改了东西，**记得先在本地 commit + push**，不然服务器 pull 不到。

### 路 B：直接上传压缩包（git pull 失败时的兜底）

本地（PowerShell）：
```powershell
cd H:\project\OpenGU
# 排除 cache / data / log，避免几十 GB 上传
Compress-Archive -Path GULib-master,requirements.txt -DestinationPath OpenGU_nips-prep.zip -Force
# 上传（替换 user@host:path 为你的服务器）
scp OpenGU_nips-prep.zip user@host:~/
```

服务器：
```bash
cd ~ && unzip -q OpenGU_nips-prep.zip -d OpenGU
cd OpenGU
```

> 注意：路 B 上传的代码不是 git repo，`experiments/run.py` 里取 `git_sha` 会写 `"unknown"`——可接受但不便于回溯。优先选路 A。

---

## 1. 环境准备（首次部署，~10-20 分钟）

服务器栈：**Ubuntu 22.04 + Python 3.10 + PyTorch 2.1.2 + CUDA 11.8**（你租的实例预装的）。

> 如果租的镜像已经预装了 torch 2.1.2+cu118，**直接跳到第 1.2 步**装 PyG。先跑 1.0 自检确认。

### 1.0 先确认预装情况（10 秒）

```bash
python -c "import torch; print(torch.__version__, 'cuda:', torch.cuda.is_available(), torch.version.cuda)"
```

期望输出 `2.1.2+cu118 cuda: True 11.8`（或类似）。如果已经满足就跳到 **1.2**。

### 1.1 如果需要从零装 torch

```bash
conda create -n gnn python=3.10 -y
conda activate gnn

pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 \
    --index-url https://download.pytorch.org/whl/cu118
```

### 1.2 装 PyG 的 C++ wheels（必须匹配 torch 2.1.2 + cu118）

```bash
pip install torch_scatter==2.1.2 torch_sparse==0.6.18 \
    -f https://data.pyg.org/whl/torch-2.1.2+cu118.html
```

### 1.3 装其余依赖

```bash
cd ~/OpenGU
pip install -r requirements.txt
```

> torch / torch_scatter / torch_sparse 已装，pip 会跳过它们；只补装 numpy / pyg / scipy / ogb / pyyaml 等纯 Python 包。

### 环境自检（30 秒）

```bash
cd ~/OpenGU/GULib-master
python -c "
import torch, torch_geometric, torch_scatter, torch_sparse, yaml, ogb
print('torch:', torch.__version__, 'cuda:', torch.cuda.is_available())
print('PyG:', torch_geometric.__version__)
print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')
"
```

期望输出包含 `cuda: True` 和你租的卡型号。**如果 cuda False，停下来排查驱动**——后续都跑不动。

---

## 2. ⚠ 清理 bug 污染的旧 cache（首次 Phase B 跑之前必做一次）

> 背景：Phase A.1/A.3/A.4 修了 MIA AUC=0 和 IM seed 不确定性两个 bug，但本地 `results/cache/` 和 `results/selection_cache/` 里仍存着 bug 修复**之前**生成的 stale 条目。如果不清，B.0/B.1 会被静默命中、读到 mia_auc=0 和 Jaccard=0.13 的废数据。

服务器 `cd ~/OpenGU/GULib-master` 然后任选：

**方案 A（推荐）：直接清空两个目录**
```bash
rm -rf results/cache/*.json
rm -rf results/selection_cache/*.json
```
代价：第一次跑 IM/Hybrid 选择会额外花 ~500s（仅一次，之后命中新 cache）。

**方案 B（更保险）：先备份再清**
```bash
mv results/cache results/cache.preB.bak
mv results/selection_cache results/selection_cache.preB.bak
mkdir -p results/cache results/selection_cache
```
跑完 Phase B 验证无误后再 `rm -rf *.bak`。

> 注意：**不要**清 `results/runs/`、`results/experiments/`、`results/evaluation/`——那些是历史结果。

---

## 3. Phase B 五步检查点（按顺序，停下来看 B.1 再放 B.2）

每步前都先确认在 `~/OpenGU/GULib-master` 下，且 `gnn` env 激活。

### B.0 · Sanity（~20 秒）

```bash
python experiments/run.py experiments/configs/sanity_one_cell.yaml --force
```

通过判据：
- 命令 0 退出码
- 屏幕看到 `wrote results/runs/.../seed*/attack.json`（4 个文件齐全）
- 没有 `mia_auc: 0.0` 这种异常（Phase A 已修，应是非零数）

✅ 通过 → 进 B.1。失败 → 检查 env / cache，**不要往后跑**。

---

### B.1 · arxiv 可行性闸（~1.5 GPU-h）⚠ 关键检查点

```bash
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml
```

5 cells × random × 1 seed。完成后**人工对照** `self/dashboard/EXPERIMENT_DASHBOARD.md` 的 `§5.3.2.1` 11 项 metric 闸：
- F1_clean / F1_unlearn / F1_retrain 在合理范围
- mia_auc 非 0、非 1
- gap、collateral、hop_decay 4 桶都有数

**这步 fail 了不要进 B.2**——B.2 是 12+ GPU-h，跑废了租金最痛。fail 的话先记下来问我。

✅ 通过 → 进 B.2。

---

### B.2 · arxiv 主矩阵（~12-30 GPU-h）💰 最贵的一步

```bash
nohup python experiments/run.py experiments/configs/phase_b_arxiv.yaml \
    > logs/phase_b_arxiv.log 2>&1 &
echo $! > logs/phase_b_arxiv.pid
```

36 cells = 3 method × 4 strategy × 3 seed。**用 nohup + 后台**，断开 SSH 不会中断。

监控：
```bash
tail -f logs/phase_b_arxiv.log
# 或看进度
ls results/runs/ogbn-arxiv_*/*/seed*/attack.json | wc -l
# 期望最终 36
```

✅ 完成 → 进 B.3/B.4（cora 矩阵）。

---

### B.3 / B.4 · cora 全矩阵（各 ~75-90 min，可与 B.2 并行）

如果服务器有**第二张卡**，开两个新 ssh tab 并行跑：

```bash
# tab 1：cora/GCN，cuda 1
CUDA_VISIBLE_DEVICES=1 nohup python experiments/run.py \
    experiments/configs/phase_b_cora_gcn.yaml \
    > logs/phase_b_cora_gcn.log 2>&1 &

# tab 2：cora/GAT，cuda 2（如果有第三张）
CUDA_VISIBLE_DEVICES=2 nohup python experiments/run.py \
    experiments/configs/phase_b_cora_gat.yaml \
    > logs/phase_b_cora_gat.log 2>&1 &
```

只有 1 张卡就**等 B.2 跑完再跑 B.3，再跑 B.4**，串行：
```bash
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml
```

每个矩阵 150 cells，完成后看：
```bash
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l    # 期望 150
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l    # 期望 150
```

---

## 4. 数据回收（跑完之后把结果带回本地）

服务器：
```bash
cd ~/OpenGU/GULib-master
tar czf phase_b_results.tar.gz results/runs/
ls -lh phase_b_results.tar.gz
```

本地（PowerShell）：
```powershell
scp user@host:~/OpenGU/GULib-master/phase_b_results.tar.gz H:\project\OpenGU\GULib-master\
cd H:\project\OpenGU\GULib-master
tar xzf phase_b_results.tar.gz
```

回到本地后告诉我 "phase B 数据回来了"，我跑 Phase C（重画 FIG-4b、hop-decay 曲线、abstract refresh）。

---

## 5. 故障速查

| 现象 | 原因 | 处理 |
|------|------|------|
| `cuda: False` 在自检里 | 驱动 / cu118 mismatch | `nvidia-smi` 看驱动；不行换 torch+cu 版本对齐 |
| `ImportError: torch_scatter` | wheel 没匹配 torch 2.1.2+cu118 | 用 `-f https://data.pyg.org/whl/torch-2.1.2+cu118.html` 重装 |
| `mia_auc: 0.0` 在 B.0 输出里 | 没清 cache | 回到第 2 节清 cache，再 `--force` 跑 B.0 |
| B.1 某项 metric 闸不过 | 真 bug 或数据问题 | **停下**，把 `attack.json` + `_meta.json` 发我 |
| 服务器 SSH 断了 | nohup 没用 | 用 `tmux` 或确保用了第 3 节 B.2 的 nohup 写法 |
| 磁盘满 | results/runs 涨得快 | `du -sh results/*` 看哪个大；arxiv 可能要 10+GB |

---

## 6. Quick reference（懒人复制）

```bash
# 一键自检 + B.0 + B.1（首次部署后跑这个）
cd ~/OpenGU/GULib-master && \
conda activate gnn && \
python -c "import torch; assert torch.cuda.is_available()" && \
rm -rf results/cache/*.json results/selection_cache/*.json && \
python experiments/run.py experiments/configs/sanity_one_cell.yaml --force && \
python experiments/run.py experiments/configs/phase_b_arxiv_feasibility.yaml && \
echo "B.0 + B.1 完成，停下来人工看 11 项 metric 闸再决定要不要进 B.2"
```
