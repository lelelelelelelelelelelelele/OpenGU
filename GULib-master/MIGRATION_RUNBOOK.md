# 数据回收手册 v1 — Phase B 双机产物拉回 + 分析

> v1: 2026-05-07。配套 `SERVER_RUNBOOK.md` v4。
> 场景：机 A（4090）跑 B.3 + B.4（cora），机 B（H800/A100）跑 B.2（arxiv-T1/T2/T3）。
> 小数据集（cora）先到，大数据集（arxiv）很久之后到。本手册描述**两段式**回收 + 分析。
> NeurIPS 截稿：2026-05-07。

---

## 0. TL;DR — 我现在该跳到哪节

| 我现在的状态 | 跳到 |
|---|---|
| 第一次进这个 runbook | §1 + §2 |
| **cora 已 ship 回本地，发现 GIF/IDEA collateral 失真，要 server 侧 redo** | **§0.5（IF-family fix 重跑工作流）** |
| 机 A 喊"cora 跑完了"（先到） | §2 → §3（出货检查 → 第一波回收） |
| cora 落本地了，想先看图但 arxiv 还没到 | §4（中场分析，仅 cora） |
| 机 B 喊"arxiv 跑完了"（后到，可能只 T1 / T1+T2 / 全 T1+T2+T3） | §2 → §5（出货检查 → 第二波回收） |
| 两机都到了 | §6（合并分析 + 出图） |
| scp 卡死 / tar 错 / 缺文件 | §7（故障） |
| 要 deadline 砍刀方案（机 B 没跑完先停） | §7.4 |
| 想要一键脚本 | 附录 A |

**核心原则**：
1. **本地只做分析，不跑代码**——所有 `gate_runs.py` / `experiments/run.py` / `inspect_run.py` / `eval_collateral.py` 在服务器侧跑完。本地分析读 json + meta，写 CSV / 图。要补跑回服务器，按 `SERVER_RUNBOOK.md` 走。
2. **按机器分目录**——`results/runs/4090/` 放机 A 数据（cora），`results/runs/h20/` 放机 B 数据（arxiv）。**两台机的产物物理隔离**，永远不会混源。已建好两个空目录 + README，untar 时直接落进对应位置。
3. **predictions.npz 不传**——2026-05-07 grep 确认：本仓库**没有任何分析代码读 npz 内容**（plot 脚本 / aggregator 全只读 json）。npz 只被 `experiments/run.py` / `gate_runs.py` / `inspect_run.py` 用作 4 件齐的存在性 check，那三个本地都不跑。**服务器侧 gate PASS 之后，本地完全跳过 npz**——cora ~省 0.5 GB，arxiv ~省 6-10 GB。
4. **先到先分析**——cora 落地立即跑 §4 出 cora-only 草图，避免 arxiv 卡 deadline 时全图缺。
5. **服务器侧产物是金本位**——本地是只读视图。万一本地损坏（tar 解错 / 误删），删掉对应 `results/runs/{机器}/` 子树重 scp 即可。

---

## 0.5 IF-family fix 重跑工作流（适用：commit `d674f62` 落到服务器之后，cora 已 ship 但 GIF/IDEA collateral 失真）

> 触发条件：cora ship 回本地、`scripts/aggregate_phase_b.py` 跑完发现 `GIF.perf_unlearn ≡ IDEA.perf_unlearn` bit-identical（30/30 GCN，20/30 GAT），证实 IF-family collateral 走了 stale baseline。修复 commit `d674f62 fix(IF-family): write params_esti back to target_model in approxi()` 已合入 `release/phase-b-fixes`。
>
> 影响范围：**仅 collateral 端**——`collateral.json.{perf_unlearn, gap, hop_decay, pred_shift}` + `predictions.npz.logits_unlearned` 失真，`attack.json.{f1_after, mia_auc, selected_nodes}` 全可信，**不需要重跑 demo_attack**。
>
> 受影响方法：**仅 GIF + IDEA**。MEGU/GNNDelete 用 in-place 写回，shard 系（GraphEraser/GraphRevoker）路径独立——经验证 0 bit-collision，**不受影响**。

### 0.5.1 服务器侧 4 步重跑（4090，约 2-3h）

```bash
ssh <4090-host>
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master
tmux attach -t phaseB || tmux new -s phaseB

# 步骤 1：拉 fix + redo 脚本
git fetch origin
git checkout release/phase-b-fixes
git pull --ff-only origin release/phase-b-fixes
# 验证 fix 在
git log --oneline -3
# 应看到（顺序可能不同）：
#   68c8eb4 feat(redo): scripts/cleanup_if_family_collateral.py
#   025c2dc feat(phase-b): cora migration tooling
#   d674f62 fix(IF-family): write params_esti back to target_model in approxi()

# 步骤 2：dry-run 看要删哪些（240 文件 = 120 cell × {collateral.json, predictions.npz}）
python scripts/cleanup_if_family_collateral.py --dry_run
# 期望末尾：
#   cells seen (dir exists)       : 120 / 120
#   files deleted                 : 240    （服务器上 npz 都在，所以 240）

# 步骤 3：实删 + 跑 canonical runner（demo_attack hit ResultCache，eval_collateral 用 patched approxi 重写）
python scripts/cleanup_if_family_collateral.py
python experiments/run.py experiments/configs/phase_b_cora_gcn.yaml
python experiments/run.py experiments/configs/phase_b_cora_gat.yaml

# run.py 行为：
#   - 60 个 incomplete cell（GIF/IDEA × 6 strat × 5 seed）→ 重跑
#   - 120 个 complete cell（GNNDelete/MEGU/GraphEraser/GraphRevoker × …）→ skip
#   - 每 cell：demo_attack ~10s（cache hit）+ eval_collateral ~30-90s

# 步骤 4：gate + 验收 spot-check
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml

# spot-check fix 真生效（修前 GIF≡IDEA bit-identical，修后应不同）
python -c "
import json
g = json.load(open('results/runs/cora_GCN_r0.05/GIF_random/seed42/collateral.json'))['results'][0]
i = json.load(open('results/runs/cora_GCN_r0.05/IDEA_random/seed42/collateral.json'))['results'][0]
print(f'GIF  perf_unlearn={g[\"perf_unlearn\"]}')
print(f'IDEA perf_unlearn={i[\"perf_unlearn\"]}')
print(f'BUG STILL PRESENT' if abs(g['perf_unlearn']-i['perf_unlearn']) < 1e-9 else 'FIX WORKS')
"
# 期望输出末行：FIX WORKS
```

### 0.5.2 重新 ship + 重跑本地分析

服务器侧 redo 跑完后，**完全跟 §3 一样 ship**——脚本只 tar `*.json` + `_meta.json`，新 collateral 自动包进去，老 npz 一起重写：

```bash
# 服务器侧
bash scripts/ship_results.sh cora     # 出 cora_results_<timestamp>.tar.gz

# 本地：MIGRATION_RUNBOOK §3.3-§3.4 老路子，但要先清理旧版本（避免新老混落）
cd H:\project\OpenGU\GULib-master
Remove-Item -Recurse -Force results\runs\4090\cora_GCN_r0.05
Remove-Item -Recurse -Force results\runs\4090\cora_GAT_r0.05

scp <user>@<4090-host>:~/autodl-fs/OpenGU/GULib-master/cora_results_*.tar.gz .
tar xzf cora_results_*.tar.gz -C results/runs/4090 --strip-components=2

# 重跑分析（产物自动覆盖）
H:/conda_package/envs/gnn/python.exe scripts/aggregate_phase_b.py 4090
H:/conda_package/envs/gnn/python.exe scripts/plot_phase_b_cora.py
H:/conda_package/envs/gnn/python.exe scripts/build_paper_table1.py
```

### 0.5.3 验收：fig5 retrain gap 应该有变化

修前的 fig5（`results/paper_figures/fig5_retrain_gap.pdf`）：GIF/IDEA 的 gap 几乎是 0（被 stale baseline mask 掉），GNNDelete 是 outlier ~10-16%。

修后预期：GIF/IDEA 的 gap 不再贴 0（小但非零），但 GNNDelete 仍然是显著最高的——**paper 主结论"GNNDelete 是最不像 retrain 的方法"不变**。

如果修后 GIF/IDEA 仍 0：fix 没生效，回 §0.5.1 步骤 4 的 spot-check 重新查。

### 0.5.4 备选路径（不推荐除非赶时间）

`scripts/redo_collateral_if_family.py` 是另一条路：直接调 `eval_collateral.py --output_dir`，绕过 `experiments/run.py` 的 demo_attack 步骤。省 30-40 min（每 cell 少一次 demo_attack subprocess 启动），但偏离 canonical pipeline，`_meta.json` 需脚本自己 refresh `git_sha`。**默认走 §0.5.1 的 cleanup + run.py 主路**。

---

## 1. 数据流总览

### 1.1 两段式时间线

```
T0  机 A 启动 B.3+B.4 cora 串行（~7-12h）
T0  机 B 启动 B.2 arxiv 链（T1 ~7-8h；可选 T2/T3 各 ~7-8h）
                              │
T1  ┌─机 A 跑完─→ §3 第一波回收（cora）
    │            ├─ ssh 进 A：tar
    │            ├─ scp 拉回本地
    │            └─ 解包 + 校验
    │
    ├─→ §4 中场分析（仅 cora）
    │     ├─ 抽查 mia_auc 分布合理性
    │     ├─ 出 cora-only 表 / 图（可发 paper draft）
    │     └─ 标记 arxiv 占位行为 TBD
    │
T2  └─机 B 跑完（或到 deadline kill）─→ §5 第二波回收（arxiv）
                  │
                  └─→ §6 合并分析（全量）
                        ├─ untar arxiv 到 results/runs/h20/
                        ├─ 全表/全图重出
                        └─ paper §4 / Table 1 / abstract refresh
```

### 1.2 产物路径速查

**服务器侧**（两机都是 autodl 部署，路径一致）：

| Phase | 服务器路径（机器内） |
|---|---|
| B.3 cora_GCN（机 A=4090） | `~/autodl-fs/OpenGU/GULib-master/results/runs/cora_GCN_r0.05/` |
| B.4 cora_GAT（机 A=4090） | `~/autodl-fs/OpenGU/GULib-master/results/runs/cora_GAT_r0.05/` |
| B.2 arxiv（机 B=h20，T1/T2/T3 都在同一目录） | `~/autodl-fs/OpenGU/GULib-master/results/runs/ogbn-arxiv_GCN_r0.05/` |

**本地落点**（按机器分层）：

```
results/runs/
  4090/                                # 机 A 数据（cora）
    cora_GCN_r0.05/{method}_{strategy}/seed{N}/{attack,collateral,_meta}.json
    cora_GAT_r0.05/{method}_{strategy}/seed{N}/{attack,collateral,_meta}.json
  h20/                                 # 机 B 数据（arxiv）
    ogbn-arxiv_GCN_r0.05/{method}_{strategy}/seed{N}/{attack,collateral,_meta}.json
```

每个 cell 服务器侧有 4 件，但**只有前 3 件需要传回本地**：

```
{cell}/{method}_{strategy}/seed{N}/
  attack.json       # ~10-50 KB ✅ 必传 —— F1 drop / mia_auc / selected_nodes
  collateral.json   # ~10-50 KB ✅ 必传 —— retrain gap / hop_decay / perf_before
  _meta.json        # ~5 KB     ✅ 必传 —— config + git_sha + timestamp + hostname
  predictions.npz   # ~1-200 MB ❌ 不传 —— 没有分析代码读它
```

### 1.3 期望 cell 计数（落地后用 Get-ChildItem 校验）

| 本地路径 | 期望数 | 备注 |
|---|---|---|
| `results\runs\4090\cora_GCN_r0.05\*\seed*\attack.json` | 180 | 6 method × 6 strategy × 5 seed |
| `results\runs\4090\cora_GAT_r0.05\*\seed*\attack.json` | 180 | 同上 |
| `results\runs\h20\ogbn-arxiv_GCN_r0.05\*\seed42\attack.json` | 12 | T1 = 3 method × 4 strategy × seed42 |
| `results\runs\h20\ogbn-arxiv_GCN_r0.05\*\seed212\attack.json` | 12 | T2 加跑后才有 |
| `results\runs\h20\ogbn-arxiv_GCN_r0.05\*\seed722\attack.json` | 12 | T3 加跑后才有 |
| `results\runs\h20\ogbn-arxiv_GCN_r0.05\*\seed*\attack.json` | 12-36 | 看 T2/T3 是否 deadline 富余跑了 |

---

## 2. 服务器侧出货前检查（每台都做一次）

> 目的：在本地浪费带宽 scp 之前，先在服务器上确认数据没烂，省掉"拉回来才发现 5 个 cell mia_auc=0"的尴尬。
> 这一步对两台机都做，只是 yaml 不同。

### 2.1 ssh 进去 + 计数 + gate

```bash
# 任选一台机
ssh <host>
source /etc/network_turbo
cd ~/autodl-fs/OpenGU/GULib-master
tmux attach -t phaseB || tmux new -s phaseB

# 1) 数 cell（机 A）
ls results/runs/cora_GCN_r0.05/*/seed*/attack.json | wc -l   # → 180
ls results/runs/cora_GAT_r0.05/*/seed*/attack.json | wc -l   # → 180

# 1') 数 cell（机 B）
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed*/attack.json | wc -l   # → 12 / 24 / 36

# 2) gate（机 A）
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml

# 2') gate（机 B）—— 跑了哪个 tier 就 gate 哪个
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T1_seed42.yaml --f1-min 0.55 --f1-max 0.85
# T2/T3 跑了再加：
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T2_seed212.yaml --f1-min 0.55 --f1-max 0.85
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T3_seed722.yaml --f1-min 0.55 --f1-max 0.85
```

`gate exit 0` = 通过，可以打包。`exit 1` = 有 cell 烂，**先在服务器侧重跑/补**而不是直接 scp（详见 SERVER_RUNBOOK §5）。

### 2.2 4 件齐校验（gate 之外的 belt-and-suspenders）

> 服务器侧 cell **完整定义还是 4 件**（含 npz）——npz 缺意味着 `eval_collateral` 当时 OOM 或 disk full 中断了，这种 cell 就是坏的，不要打包。"npz 不传到本地"是出货后的优化，不影响服务器侧的完整性判定。

```bash
# 任意一个 cell 应有 4 件：
ls -la results/runs/cora_GAT_r0.05/GIF_random/seed42/
# 期望 4 行（attack.json / collateral.json / predictions.npz / _meta.json）

# 全量统计：缺 npz 的 cell（npz 是最容易因 OOM 或 disk full 缺的）
for f in attack.json collateral.json predictions.npz _meta.json; do
    n=$(ls results/runs/cora_GAT_r0.05/*/seed*/$f 2>/dev/null | wc -l)
    echo "  $f: $n / 180"
done
```

少哪个文件就回 SERVER_RUNBOOK §5 / §A.1 的 redo_collateral.sh 补，**不要带病出货**。

### 2.3 磁盘空间预估

服务器侧原始（含 npz，下面 du 看到的）：

```bash
du -sh results/runs/cora_*_r0.05/      # 单 cora 矩阵 ~2-5 GB
du -sh results/runs/ogbn-arxiv_*_r0.05/   # arxiv 单 tier ~3-8 GB，全 T1+T2+T3 ~20 GB
df -h ~                                  # 自由空间 > tar 大小？不够换路径
```

**实际 tar 大小**（跳 npz 后小一个量级）：
- cora 整套 tar.gz：~100-300 MB
- arxiv 整套 tar.gz：~50-200 MB
- gzip 在 json 上压缩比 2-5×，`tar czf` 直接用

服务器侧 du 跟 tar 大小是两码事，看 du 不要被吓到。

---

## 3. 第一波回收：cora（机 A 先到）

### 3.1 出货前最后一道（机 A 内）

```bash
ssh <4090-host>
cd ~/autodl-fs/OpenGU/GULib-master

# 必须 PASS 才打包
python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml && \
python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml && \
echo "BOTH GATES PASS — ok to tar"
```

### 3.2 打包（机 A 内）—— **只 tar json + meta，不 tar npz**

```bash
# 用 find 只挑 json/meta 三件，npz 自动排除
TS=$(date +%Y%m%d_%H%M)
find results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05 \
     -type f \( -name '*.json' -o -name '_meta.json' \) \
     | tar czf cora_results_${TS}.tar.gz -T -

# A.5 / A.5-2 / A.6 / A.3 也跑了的话，find 路径加进来：
# find results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05 \
#      results/runs/cora_GCN_r0.01 results/runs/cora_GCN_r0.10 results/runs/cora_GCN_r0.20 \
#      results/runs/cora_GIN_r0.05 \
#      results/runs/citeseer_GCN_r0.05 results/runs/citeseer_GCN_r0.20 \
#      -type f \( -name '*.json' -o -name '_meta.json' \) \
#      | tar czf cora_results_${TS}.tar.gz -T -

ls -lh cora_results_*.tar.gz       # 期望 ~50-300 MB
md5sum cora_results_*.tar.gz | tee /tmp/cora.md5
```

> **不要 tar 整个 `results/`**。其他子目录：
> - `baseline/` 已在本地 git 跟踪
> - `cache/` / `selection_cache/` / `score_cache/` 是 hash-named，跨机不命中（IF cache key 含 model fingerprint），白浪费 GB
> - `runs/*/predictions.npz` 没人读（§1.2 已论证），跳过

### 3.3 scp 拉回本地（PowerShell）

```powershell
cd H:\project\OpenGU\GULib-master

# 拉 tar
scp <user>@<4090-host>:~/autodl-fs/OpenGU/GULib-master/cora_results_*.tar.gz .

# 比对 md5（防 scp 中途坏）
scp <user>@<4090-host>:/tmp/cora.md5 .
Get-FileHash cora_results_*.tar.gz -Algorithm MD5
Get-Content cora.md5
# 两个 hash 一致 → 安全
```

> **scp 网络抽风时**：autodl 内网带宽 ~50 MB/s 起步，cora 主矩阵 tar ~2-5 GB 大约 1-3 分钟。如果 scp 卡死，看 §7.1。

### 3.4 解包到本地 `results/runs/4090/`

tar 内是 `results/runs/cora_*_r0.05/...` 相对路径。用 `--strip-components=2 -C results/runs/4090` 把 `results/runs/` 两层去掉，直接落进机器目录：

```powershell
cd H:\project\OpenGU\GULib-master
tar xzf cora_results_*.tar.gz -C results/runs/4090 --strip-components=2

# 计数（每张 cora 矩阵期望 180）
(Get-ChildItem results\runs\4090\cora_GCN_r0.05 -Recurse -Filter attack.json).Count
(Get-ChildItem results\runs\4090\cora_GAT_r0.05 -Recurse -Filter attack.json).Count
```

> 不在本地跑 gate——服务器侧 §3.1 已 gate 过，本地只做分析。

### 3.5 来源核验（可选）

随机抽几个 cell 看 `_meta.json` 的 `hostname` / `git_sha` 是否一致，确认都是同一次 B.3+B.4 跑出来的：

```powershell
H:/conda_package/envs/gnn/python.exe -c "
import json, pathlib, collections
shas = collections.Counter()
hosts = collections.Counter()
for p in pathlib.Path('results/runs/4090').rglob('_meta.json'):
    d = json.loads(p.read_text())
    shas[d.get('git_sha','?')[:7]] += 1
    hosts[d.get('hostname','?')] += 1
print('shas:', shas.most_common(3))
print('hosts:', hosts.most_common(3))
"
```

理想：1-2 个 git_sha + 1 个 hostname（cora 跑了 B.3 + B.4 两次，中间可能 git pull，2 个 sha 正常）。> 3 个 sha 或多个 hostname → 数据来源混乱，回 §3.5 上面那段决定要不要重抓。

---

## 4. 中场分析（仅 cora，B.2 还没回来）

> 时机：cora 已落地 + gate PASS，但 B.2 arxiv 还在机 B 上跑（可能还要 4-12h）。
> 目的：把 paper Table 1 的 cora 行 / Figure 1-3 的 cora 部分先草出来，arxiv 列留 TBD 占位。论文 deadline 紧，这一步**不要等 arxiv**。

### 4.1 快速摸盘（看 5 分钟内能否定主结论）

```powershell
# 跨 cell 看 mia_auc 分布是否合理（别全是 0.5 或 0.99）
H:/conda_package/envs/gnn/python.exe -c "
import json, pathlib, statistics
ps = list(pathlib.Path('results/runs/4090/cora_GCN_r0.05').glob('*/seed*/attack.json'))
aucs = []
for p in ps:
    d = json.loads(p.read_text())
    for s, r in d.get('results', {}).items():
        if r.get('mia_auc') is not None:
            aucs.append(r['mia_auc'])
print(f'cora_GCN: n={len(aucs)}, median={statistics.median(aucs):.3f}, range=[{min(aucs):.3f}, {max(aucs):.3f}]')
"
```

预期 mia_auc median ~0.55-0.75，range 在 (0.001, 0.999) 内。极端值集中 → §7.2 cache 污染怀疑。

### 4.2 出 cora-only 草图

⚠ `scripts/evaluation/final_data_aggregator.py` 是 **pre-Phase-B 版本**，跑会 exit 2 拒绝（设了 guard，需 `ALLOW_LEGACY_AGGREGATOR=1` 强跑也只输出空 CSV）。**Phase B port 还没写**，所以中场分析走临时 ad-hoc Python：

```powershell
# 临时 aggregator：walk results/runs/4090/ 拼 DataFrame
H:/conda_package/envs/gnn/python.exe -c "
import json, pathlib, pandas as pd
rows = []
for p in pathlib.Path('results/runs/4090').glob('cora_*_r0.05/*/seed*/attack.json'):
    machine = p.parts[-5]         # 4090
    cell = p.parts[-4]            # cora_GCN_r0.05
    method, strategy = p.parts[-3].rsplit('_', 1)
    seed = int(p.parts[-2].removeprefix('seed'))
    d = json.loads(p.read_text())
    for s, r in d.get('results', {}).items():
        rows.append(dict(machine=machine, cell=cell, method=method, strategy=s, seed=seed,
                         f1_after=r.get('f1_after'), mia_auc=r.get('mia_auc')))
df = pd.DataFrame(rows)
df.to_csv('results/_phase_b_cora_interim.csv', index=False)
print(df.groupby(['cell','method','strategy'])['f1_after'].agg(['mean','std']).round(3))
"
```

这个 CSV 至少能让你看 method×strategy 的 F1/MIA 分布。完整 Table 1 / Figure 出图还是等 §6 全量到位再做。

### 4.3 paper 草稿处理

把 paper（`report/paper/overleaf/sec/`）里的 **arxiv 列**先标 `\textcolor{gray}{TBD (B.2 pending)}`，cora 列填上 §4.2 看到的均值。Section 5 就可以开始往下写了。

---

## 5. 第二波回收：arxiv（机 B 后到）

### 5.1 等什么算"到"？三种合法状态

| 落盘状态 | 含义 | 合法 yaml gate |
|---|---|---|
| 只有 seed42（12 cell） | T1 完成，T2/T3 没跑或被 deadline kill | `phase_b_arxiv_T1_seed42.yaml` |
| seed42 + seed212（24 cell） | T1+T2 完成，T3 没跑 | T1 + T2 各 gate |
| seed42+212+722（36 cell） | 完整 n=3 | 三个都 gate |

**不要等"应该有 36"才打包**——deadline 到了就以当时的状态出货。paper §4 写法：T1 only → n=1 报点估计 + cora n=5 做误差棒；T1+T2 → n=2 报 spread；T1+T2+T3 → n=3 完整 errorbar。

⚠ **IM cell 可能缺**。SERVER_RUNBOOK §1.2 修正后实测：arxiv IM CELF 默认参数 4-10h（不是原标的 3 min），T1 7-8h 预算下 IM 列可能根本没跑完。**缺 IM 也是合法状态**——出货时 IM cell 文件夹空就空，paper §A.x 写 "IM omitted on arxiv: full CELF intractable at k=O(10³); see [limitations]"。后续优化方向（batch=100 加速 ~20×）见 SERVER_RUNBOOK §1.2 ⚠ 段，留作 deadline 后处理。

### 5.2 出货前检查（机 B 内）

```bash
ssh <h800-host>
cd ~/autodl-fs/OpenGU/GULib-master

# 看现状
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed42/attack.json  | wc -l   # 期望 12
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed212/attack.json | wc -l   # 0 / 12
ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed722/attack.json | wc -l   # 0 / 12

# 跑哪个 tier gate 哪个
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T1_seed42.yaml --f1-min 0.55 --f1-max 0.85
# 有 T2 才跑：
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T2_seed212.yaml --f1-min 0.55 --f1-max 0.85
# 有 T3 才跑：
python scripts/gate_runs.py experiments/configs/phase_b_arxiv_T3_seed722.yaml --f1-min 0.55 --f1-max 0.85
```

**部分 tier FAIL 怎么办**：把 FAIL tier 从这次 tar 里排除，本地分析时只用 PASS 的 tier。SERVER_RUNBOOK §5 决定要不要回服务器补；deadline 紧时直接接受 n=1 / n=2。

### 5.3 打包（机 B 内）—— 同样只 tar json + meta

```bash
# arxiv 跳过 npz（~6-10 GB → ~50-200 MB）
TS=$(date +%Y%m%d_%H%M)
find results/runs/ogbn-arxiv_GCN_r0.05 \
     -type f \( -name '*.json' -o -name '_meta.json' \) \
     | tar czf arxiv_results_${TS}.tar.gz -T -

ls -lh arxiv_results_*.tar.gz       # 期望 ~30-200 MB
md5sum arxiv_results_*.tar.gz | tee /tmp/arxiv.md5
```

### 5.4 scp 拉回本地

```powershell
cd H:\project\OpenGU\GULib-master
scp <user>@<h800-host>:~/autodl-fs/OpenGU/GULib-master/arxiv_results_*.tar.gz .
scp <user>@<h800-host>:/tmp/arxiv.md5 .

Get-FileHash arxiv_results_*.tar.gz -Algorithm MD5
Get-Content arxiv.md5
```

### 5.5 解包到 `results/runs/h20/`

```powershell
cd H:\project\OpenGU\GULib-master
tar xzf arxiv_results_*.tar.gz -C results/runs/h20 --strip-components=2

# 计数（看 tier 落了哪些；T1=12 / T1+T2=24 / 全=36）
(Get-ChildItem results\runs\h20\ogbn-arxiv_GCN_r0.05 -Recurse -Filter attack.json).Count
```

不跑本地 gate——服务器侧 §5.2 已 gate 过。如果服务器侧某 tier FAIL 了被排除在 tar 外，本地直接看缺数；要复 gate 回服务器。

### 5.6 真要 npz 怎么办

`predictions.npz` 当前没分析消费者，但万一未来 hop_decay / collateral 二次诊断要从原始 logits 重算（不信 `collateral.json` 里的 hop_decay 字段、想自己复现）：

```bash
# 服务器侧单独打 npz 包（~6-10 GB）
tar cf arxiv_npz_$(date +%Y%m%d_%H%M).tar \
    $(find results/runs/ogbn-arxiv_GCN_r0.05 -name 'predictions.npz' -print)
```

scp 拉回，解到 `results/runs/h20/`（同样 `--strip-components=2`），与已有 json 自动对齐（同 cell 路径）。**默认不做这一步**——deadline 前 paper 不需要。

---

## 6. 全量分析（cora + arxiv 都到位）

> 前置：§3 + §5 解包完成（`results/runs/4090/` 和 `results/runs/h20/` 都有数据）。
> 本地不跑 gate；服务器侧已 gate 过。

### 6.1 全量 ad-hoc aggregator（Phase B port 没写之前的临时方案）

```powershell
H:/conda_package/envs/gnn/python.exe -c "
import json, pathlib, pandas as pd
rows = []
# walk 两台机的 results/runs/{4090,h20}/{cell}/...
for p in pathlib.Path('results/runs').glob('*/*/*/seed*/attack.json'):
    machine = p.parts[-5]                # 4090 or h20
    cell = p.parts[-4]                   # cora_GCN_r0.05 / ogbn-arxiv_GCN_r0.05 ...
    method_strategy = p.parts[-3]
    seed = int(p.parts[-2].removeprefix('seed'))
    # 拆 method_strategy：strategy 名固定一个单词，method 可能含下划线
    method, _, strategy_full = method_strategy.rpartition('_')
    d = json.loads(p.read_text())
    for s, r in (d.get('results') or {}).items():
        row = dict(machine=machine, cell=cell, method=method, strategy=s,
                   strategy_full=strategy_full, seed=seed,
                   f1_after=r.get('f1_after'),
                   mia_auc=r.get('mia_auc'),
                   selected_n=len(r.get('selected_nodes') or []))
        cp = p.parent / 'collateral.json'
        if cp.exists():
            try:
                cres = (json.loads(cp.read_text()).get('results') or [{}])[0]
                row.update(perf_before=cres.get('perf_before'), gap=cres.get('gap'))
            except Exception as e:
                row['collateral_err'] = str(e)
        rows.append(row)
df = pd.DataFrame(rows)
df.to_csv('results/_phase_b_full_interim.csv', index=False)
print('rows:', len(df), '| machines:', df.machine.unique().tolist())
print(df.groupby(['machine','cell','method','strategy_full'])['mia_auc']
        .agg(['count','mean','std']).round(3).head(60))
"
```

输出 `results/_phase_b_full_interim.csv`——paper Table 1 的原料，`machine` 列让 cora/arxiv 来源可追溯。

### 6.2 出图（plot_paper_figures.py）

```powershell
# 主图（5 张 PDF/PNG → results/paper_figures/）
H:/conda_package/envs/gnn/python.exe scripts/plot_paper_figures.py
# 补充图
H:/conda_package/envs/gnn/python.exe scripts/plot_supp_figures.py
```

> ⚠ `plot_paper_figures.py` 内部如果还指向 `results/relative/` 等已废弃路径就会空跑——出空图时跑 `Get-Content scripts/plot_paper_figures.py | Select-String "results/"` 看它读哪。
> 必要时在 §6.1 的 CSV 上手写 matplotlib 临时出图；deadline 紧的话**不依赖** plot 脚本，直接 paper 里贴 §6.1 的均值/方差表也合规。

### 6.3 paper 三件套刷新（内容由 report-writing skill 处理）

按优先级：

1. **Table 1**（每 (dataset, method) × (strategy) 的 F1 drop / MIA AUC）—— 直接读 §6.1 CSV
2. **Figure: hop-decay**（cora vs arxiv 衰减曲线）—— 用 npz 里 logits 算
3. **Abstract / Section 5 数字**—— 把 §4.3 留的 TBD 全替换

详见 `report/paper/overleaf/sec/` 各 .tex 文件。这步用 `/skill report-writing` 或 `/review`。

---

## 7. 故障处理

### 7.1 scp 卡死 / 速度慢

```bash
# 1) 看是不是 autodl 内部限速：换 -P 22022（如果实例开了 ssh 代理转发）
scp -P 22022 ...

# 2) 走 rsync（断点续传）—— autodl 容器多数装了 rsync
rsync -avzP --partial \
    <user>@<host>:~/autodl-fs/OpenGU/GULib-master/cora_results_*.tar.gz \
    H:/project/OpenGU/GULib-master/

# 3) 大文件拆 tar：split + 多次 scp
# 服务器侧
split -b 500M arxiv_results.tar arxiv_results.tar.part-
# 本地拼回
cmd /c "copy /b arxiv_results.tar.part-* arxiv_results.tar"
```

### 7.2 本地 untar 后文件数不对

```powershell
# 看哪台机缺多少
H:/conda_package/envs/gnn/python.exe -c "
import pathlib
for machine in ['4090', 'h20']:
    base = pathlib.Path(f'results/runs/{machine}')
    if not base.exists(): continue
    for f in ['attack.json', 'collateral.json', '_meta.json']:
        n = len(list(base.glob(f'*/*/seed*/{f}')))
        print(f'{machine}/{f}: {n}')
"
```

如果某文件计数不对：
- mia_auc 异常 / 字段缺失 → 服务器侧那个 cell 当时就坏；回 SERVER_RUNBOOK §5 重跑该 cell 后**只 scp 那一个 cell** 覆盖
- tar 损坏 → 整 tar 重传（先看 md5）

### 7.3 来源审计（cell git_sha 不一致）

每台机理论上一个 commit、一个 hostname。多个 sha 不致命但要心里有数：

```powershell
H:/conda_package/envs/gnn/python.exe -c "
import json, pathlib, collections
for machine in ['4090', 'h20']:
    base = pathlib.Path(f'results/runs/{machine}')
    if not base.exists(): continue
    shas = collections.Counter()
    hosts = collections.Counter()
    for p in base.rglob('_meta.json'):
        try:
            d = json.loads(p.read_text())
            shas[d.get('git_sha','?')[:7]] += 1
            hosts[d.get('hostname','?')] += 1
        except Exception:
            shas['parse_error'] += 1
    print(f'{machine}: shas={shas.most_common(3)} hosts={hosts.most_common(3)}')
"
```

### 7.4 deadline 砍刀方案（机 B 没跑完，但必须出货）

1. 在机 B 上 `kill $(cat logs/h800_*.pid)` 停止 run.py（已落盘 cell 都不损）
2. 立刻 §5.2 → §5.5 拉当时的状态
3. paper §4 文案匹配现状：
   - 只 T1（n=1）→ "single-seed point estimate; cora (n=5) provides statistical anchor"
   - T1+T2（n=2）→ "two-seed mean ± half-range; full n=5 left to camera-ready"
   - 全 36 → 正常 n=3 errorbar

### 7.5 速查

| 现象 | 处理 |
|---|---|
| scp 中途断 | rsync `--partial` 续传（§7.1） |
| tar 解压报 "Unexpected EOF" | tar 文件不全；md5 比对 → 不一致就重传 |
| 本地 tar 命令找不到（PowerShell） | Win10+ 自带 bsdtar，直接 `tar` 命令；老系统装 7-Zip 用 `7z x` |
| 本地 disk full | tar 在远端，本地解时分两步：先 `Move-Item *.tar D:\`，到大盘解，再 `Move-Item D:\results\runs\* H:\...\results\runs\{机器}\` |
| 临时 aggregator 报 cell 名解析错 | strategy 名带下划线（如 `tracin_xfrom_GCN`，A.7 的 cross-arch 后缀，或 `hybrid_alpha0.25`）—— §6.1 的脚本要扩 |
| 解出来的目录多了一层 `results/runs/` | 忘加 `--strip-components=2`；删掉 `results/runs/{机器}/results/`，重 `tar xzf ... -C results/runs/{机器} --strip-components=2` |

---

## 附录 A — 一键脚本

### A.1 服务器侧出货脚本（`scripts/ship_results.sh`，自建）

```bash
cat > scripts/ship_results.sh << 'EOF'
#!/bin/bash
# 用法: bash scripts/ship_results.sh cora     # 机 A (4090)
#       bash scripts/ship_results.sh arxiv    # 机 B (h20)
# 行为：gate -> 只 tar json/_meta（跳过 npz） -> md5
set -e
cd ~/autodl-fs/OpenGU/GULib-master
TS=$(date +%Y%m%d_%H%M)

case "$1" in
  cora)
    echo "[gate] cora_GCN..."
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gcn.yaml
    echo "[gate] cora_GAT..."
    python scripts/gate_runs.py experiments/configs/phase_b_cora_gat.yaml
    OUT=cora_results_${TS}.tar.gz
    DIRS="results/runs/cora_GCN_r0.05 results/runs/cora_GAT_r0.05"
    # A.5 / A.6 / 其他可选目录如果存在就一并打
    for d in results/runs/cora_GCN_r0.0[12] results/runs/cora_GCN_r0.1[0] \
             results/runs/cora_GCN_r0.20 results/runs/cora_GIN_r0.05 \
             results/runs/citeseer_GCN_r0.0[5] results/runs/citeseer_GCN_r0.20; do
      [ -d "$d" ] && DIRS="$DIRS $d"
    done
    find $DIRS -type f \( -name '*.json' -o -name '_meta.json' \) \
        | tar czf "$OUT" -T -
    ;;
  arxiv)
    for tier in T1_seed42 T2_seed212 T3_seed722; do
      yaml="experiments/configs/phase_b_arxiv_${tier}.yaml"
      [ -f "$yaml" ] || continue
      seed=$(echo $tier | sed 's/.*seed//')
      [ "$(ls results/runs/ogbn-arxiv_GCN_r0.05/*/seed${seed}/attack.json 2>/dev/null | wc -l)" -gt 0 ] || continue
      echo "[gate] $tier..."
      python scripts/gate_runs.py "$yaml" --f1-min 0.55 --f1-max 0.85 \
          || echo "  ↑ FAIL but proceeding (deadline mode)"
    done
    OUT=arxiv_results_${TS}.tar.gz
    find results/runs/ogbn-arxiv_GCN_r0.05 \
         -type f \( -name '*.json' -o -name '_meta.json' \) \
         | tar czf "$OUT" -T -
    ;;
  *)
    echo "usage: $0 {cora|arxiv}"; exit 2 ;;
esac

ls -lh "$OUT"
md5sum "$OUT" > "${OUT}.md5"
cat "${OUT}.md5"
echo "[done] tar at $(pwd)/$OUT"
EOF
chmod +x scripts/ship_results.sh
```

跑：

```bash
bash scripts/ship_results.sh cora     # 机 A (4090)
bash scripts/ship_results.sh arxiv    # 机 B (h20)
```

### A.2 本地一键拉 + 校验（`scripts/pull_results.ps1`，自建）

```powershell
# scripts/pull_results.ps1
param(
  [Parameter(Mandatory)] [ValidateSet('cora','arxiv')] $What,
  [Parameter(Mandatory)] $RemoteHost,
  $User = 'root'
)
Set-Location H:\project\OpenGU\GULib-master

$pattern = if ($What -eq 'cora') { 'cora_results_*.tar.gz' } else { 'arxiv_results_*.tar.gz' }
$machine = if ($What -eq 'cora') { '4090' } else { 'h20' }
$remote  = "${User}@${RemoteHost}:~/autodl-fs/OpenGU/GULib-master/${pattern}"

# 拉 tar + md5
scp $remote .
scp "${User}@${RemoteHost}:~/autodl-fs/OpenGU/GULib-master/${pattern}.md5" .

# 比对
$tar = (Get-ChildItem $pattern | Sort-Object LastWriteTime -Desc | Select-Object -First 1).Name
$localMd5  = (Get-FileHash $tar -Algorithm MD5).Hash.ToLower()
$remoteMd5 = (Get-Content "${tar}.md5").Split(' ')[0].ToLower()
if ($localMd5 -ne $remoteMd5) {
  Write-Error "MD5 mismatch! local=$localMd5 remote=$remoteMd5"
  exit 1
}
Write-Host "MD5 OK: $localMd5"

# 解包到 results/runs/{machine}/，--strip-components=2 去掉 tar 内的 results/runs/ 两层
New-Item -ItemType Directory -Force -Path "results/runs/${machine}" | Out-Null
tar xzf $tar -C "results/runs/${machine}" --strip-components=2

# 计数
$n = (Get-ChildItem "results/runs/${machine}" -Recurse -Filter attack.json).Count
Write-Host "[done] $What landed at results/runs/${machine}/  ($n attack.json)"
```

跑：

```powershell
.\scripts\pull_results.ps1 -What cora  -RemoteHost 4090-host
.\scripts\pull_results.ps1 -What arxiv -RemoteHost h20-host
```

### A.3 中场+全量临时 aggregator（`scripts/aggregate_phase_b.py`，自建）

```python
# scripts/aggregate_phase_b.py
"""Phase B interim aggregator. Walks results/runs/{machine}/{cell}/{method}_{strategy}/seed*/
and dumps a flat CSV. Replaces the broken pre-Phase-B final_data_aggregator until
a proper Phase B port is written.

Layout after migration:
    results/runs/4090/cora_*_r0.05/...
    results/runs/h20/ogbn-arxiv_*_r0.05/...
"""
import json, pathlib, pandas as pd, sys

# 可选过滤：限定机器（4090 / h20）
MACHINES = sys.argv[1:] or ['4090', 'h20']
STRATS = ['random', 'degree', 'pagerank', 'tracin', 'im', 'hybrid']

def split_method_strategy(name):
    for s in sorted(STRATS, key=len, reverse=True):
        if name.endswith(f'_{s}'):
            return name[:-(len(s)+1)], s
        # alpha-sweep / xfer 后缀也吃下：tracin_xfrom_GCN, hybrid_alpha0.25, ...
        for suffix in ['_xfrom_', '_alpha']:
            if f'_{s}{suffix}' in name + '_':
                head, _, tail = name.partition(f'_{s}')
                return head, s + tail
    method, _, strategy = name.rpartition('_')
    return method, strategy

rows = []
for machine in MACHINES:
    base = pathlib.Path('results/runs') / machine
    if not base.exists():
        print(f'[skip] {base} (not found)')
        continue
    for p in base.glob('*/*/seed*/attack.json'):
        cell = p.parts[-4]                 # cora_GCN_r0.05 / ogbn-arxiv_GCN_r0.05 ...
        method, strategy_full = split_method_strategy(p.parts[-3])
        seed = int(p.parts[-2].removeprefix('seed'))
        d = json.loads(p.read_text())
        for s, r in (d.get('results') or {}).items():
            row = dict(machine=machine, cell=cell, method=method, strategy=s,
                       strategy_full=strategy_full, seed=seed,
                       f1_after=r.get('f1_after'),
                       mia_auc=r.get('mia_auc'),
                       selected_n=len(r.get('selected_nodes') or []))
            cp = p.parent / 'collateral.json'
            if cp.exists():
                try:
                    cres = (json.loads(cp.read_text()).get('results') or [{}])[0]
                    row.update(perf_before=cres.get('perf_before'),
                               gap=cres.get('gap'))
                except Exception as e:
                    row['collateral_err'] = str(e)
            rows.append(row)

df = pd.DataFrame(rows)
out = pathlib.Path('results/_phase_b_aggregate.csv')
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f'wrote {out} ({len(df)} rows; machines={df.machine.unique().tolist() if len(df) else []})')
if len(df):
    print(df.groupby(['machine','cell','method','strategy_full'])['mia_auc']
            .agg(['count','mean','std']).round(3).head(60))
```

跑：

```powershell
# 全量
H:/conda_package/envs/gnn/python.exe scripts/aggregate_phase_b.py
# 只 cora（中场）
H:/conda_package/envs/gnn/python.exe scripts/aggregate_phase_b.py 4090
# 只 arxiv
H:/conda_package/envs/gnn/python.exe scripts/aggregate_phase_b.py h20
```

---

## 附录 B — 路径速查

| 角色 | 路径 |
|---|---|
| 服务器源（A=4090 / B=h20 共用 schema） | `~/autodl-fs/OpenGU/GULib-master/results/runs/{cell}/...` |
| 本地落点（机 A） | `H:\project\OpenGU\GULib-master\results\runs\4090\{cell}\...` |
| 本地落点（机 B） | `H:\project\OpenGU\GULib-master\results\runs\h20\{cell}\...` |
| 本地 conda Python | `H:/conda_package/envs/gnn/python.exe` |
| 临时 CSV | `results/_phase_b_aggregate.csv`（aggregator 输出） |
| 论文图 | `results/paper_figures/`（plot_paper_figures.py 输出） |
| 论文章节 | `report/paper/overleaf/sec/` |
| 一次性归档（pre-migration） | `results/_archive_20260507_pre_migration/` |
| 主 runbook（执行侧） | `SERVER_RUNBOOK.md` |
| 这份手册（回收侧） | `MIGRATION_RUNBOOK.md` |

字段语义、metric 定义在 `self/dashboard/METRIC_FIELD_SEMANTICS.md` 和 `self/dashboard/METRICS_CATALOG.md`，分析时不确定 `f1_before` / `perf_before` / `gap` 是哪个语义看那两份。
