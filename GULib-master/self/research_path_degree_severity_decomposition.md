---
tags:
  - 自己的研究
  - research-path
  - degree
  - decomposition
  - gu-safety
created: 2026-06-15
origin: 与学长讨论 + 2026-06-15 status survey 验证
---

> Status: active research path (proposed second-order contribution)
> Role: 把"degree 攻击严重性最高"翻成有原理的分解 + GU 安全指数（弱版），再抬成"识别正确攻击 target（$\mathcal{U}$ 近似误差）+ U-aware selector"的 **paper 核心正向贡献**（强版 §7）。
> Use this when: 推进 paper reframe 的 mechanism / §5.2 之后的二级结论 / rebuttal 加分项。
> See also: `report/paper/overleaf/sec/5_results.tex` §5.2 (`sec:results-alignment`), `dashboard/METRICS_CATALOG.md` (gap 定义), `limitations.md` L8 (gap 污染同根因), `idea_cross_arch_consensus.md`, 记忆 `paper-contribution-falsified`

# 研究路径：degree 最严重 → 重要性×脆弱性分解 → GU 安全性指标

## 0. 一句话

"degree 攻击严重性最高"不是"degree 这个攻击聪明"，而是攻击伤害能拆成
**(节点重要性) + (GU 方法脆弱性)** 两个轴，degree 同时把两轴顶满。
用 `retrain − unlearn` 的 **gap** 把第二个轴单独量化出来，得到一个方法级
**unlearning 安全指数**。

**两个版本（§7 是关键）**：
- **弱版**（§1-§6）：misalignment 假说 + 相关性证据，定位 = F1 drop 的二级结论。能成立但单薄。
- **强版**（§7）：把 gap 抬成**正式攻击 target**（= $\mathcal{U}$ 的近似误差），证 degree 只是它的廉价代理、IF/IM 瞄错了 object，并试一个 **U-aware selector**。这是把整篇 paper 从"degree 很水"翻成"我们识别了正确的攻击目标"的**核心正向贡献**。

## 1. 出发点（与学长讨论的结论）

- **结论**：在我们的矩阵里，**degree 选点造成的攻击严重性最高**（survey 已核：
  全局 paired 均值 `degree +1.85 > pagerank +1.53 > im +1.19 > hybrid +0.21 > tracin −0.31`；
  cora/GCN 上逐方法 `degree ≥ im ≥ tracin`）。
- **切入点**：不要把这当"我们的高级 selector 输了"的尴尬，而是从
  **GNN 本身特性**解释——把效果拆成 **node 本身的重要性** 和 **GU 方法的脆弱性**。

## 2. 形式化：加法分解（用现成的 gap 列）

记被删集合 $S$、unlearning 方法 $M$：

$$
\underbrace{F_1^{\text{before}} - F_1^{\text{unlearn}}(S,M)}_{\text{总攻击伤害 } D}
=
\underbrace{\big[F_1^{\text{before}} - F_1^{\text{retrain}}(S)\big]}_{(\mathrm{I})\ \text{节点重要性，与方法无关}}
+
\underbrace{\big[F_1^{\text{retrain}}(S) - F_1^{\text{unlearn}}(S,M)\big]}_{(\mathrm{II})\ =\ \texttt{gap}\ \text{列，方法脆弱性}}
$$

- **(Ⅰ) 节点重要性轴**：连"完美 unlearner = 精确 retrain"都躲不掉的合法损失，**只依赖删哪些点**，与 $M$ 无关。degree 高 → (Ⅰ) 大。
- **(Ⅱ) 方法脆弱性轴**：近似 unlearning 相对精确 retrain 多坏的部分 = 仓库里的 `gap` 列（`perf_retrain − perf_unlearn`，正值=unlearn 比 retrain 更差=过度遗忘/失真）。依赖 $(S,M)$。

**为什么 degree 赢（核心论点）**：高度数节点的**结构杠杆**是 (Ⅰ)(Ⅱ) 的**共同潜变量**——
删它既让 retrain 也掉得多（Ⅰ），又让近似算子的线性化/外推崩得狠（Ⅱ）。
degree 是这个潜变量最便宜的估计；TracIn/IM 估的是**别的**潜变量
（test-loss 影响 / IC 传播），与结构杠杆只弱相关 → 输。
→ 与 §5.2 objective-misalignment **同源且更进一步**：§5.2 说"selector 没对齐结构"，
这里进一步说"**结构杠杆同时驱动合法损失和近似失真**，所以对齐结构的 degree 通吃"。

## 3. "用插值判断 GU 安全性" → 落成一个指标

把 strategy 按**选中节点平均度数 $\bar d$** 从 random（≈图均值）插值到 degree（最高），
对每个方法回归 $(\mathrm{II})$ 对 $\bar d$：
$$
\texttt{gap}_M(\bar d) \approx \alpha_M + \beta_M\,\bar d
$$
- $\beta_M \approx 0$：**安全**——无论删哪些点近似都忠实（worst-case 选点也不崩）。
- $\beta_M$ 大：**不安全**——删关键点 gap 暴涨。

$\beta_M$（或更简单：`gap@degree − gap@random`）= **方法级 unlearning 安全/鲁棒指数**。
$\bar d$ 在 FIG-5 / §5.2 已经算好，**几乎零新数据**。
天然是 F1 drop 的**二级结论**（量级小、更本质），正对应"当时结论没 f1 drop 明显"。

## 4. 现有数据验证（2026-06-15，cora/GCN/r0.05）

| 验证项 | 结果 | 结论 |
|---|---|---|
| (Ⅱ) gap 是否也 degree 最高 | `degree +0.0285 ≈ im +0.0259 ≈ pagerank +0.0231 > random +0.0127 > tracin +0.0086`（按 strategy 均值）| ✅ 轴B 也被结构型 selector 顶高，tracin 垫底 |
| GNNDelete 的 gap 是否单调干净 | `degree +0.150 > im +0.131 > random +0.089 > tracin +0.063` | ✅ **比它噪的 F1 paired（±7 不显著）更稳**，gap 是更好的二级证据 |
| shard/MEGU 是否 β≈0 | GraphEraser/GraphRevoker/MEGU gap 均 ≈0 或负 | ✅ "安全"端锚点成立（物理隔离/忠实近似）|
| GIF/IDEA gap 是否可信 | `GIF|degree=IDEA|degree=-0.0022`，四 strategy **逐位相同** | 🔴 **被 L8 污染**（同 hop-decay 指纹），IF-family 的 gap 不可用，需修 L8 重跑 |

## 5. 三个必须接住的坑

1. **gap 的 L8 污染（IF-family）**：GIF/IDEA 的 `perf_unlearn ≈ 原模型`，所以它俩的 gap 逐位相同、近零，是**假的**。
   **代码已经修好**：写回逻辑在 `gif.py:802-810` / `idea.py:489-497`，已提交为 `d674f62`（在 HEAD，
   与所谓"未合并分支 `949d0f8`"逐字相同——**不需要合任何分支**）。
   **数据仍坏的根因是 stale `.pyc`**：那次 run 的 `git_sha=78872fc` 已含 `d674f62`，但 autodl 容器加载了
   旧 `__pycache__` 字节码，所以 bug 照旧。→ 修复动作不是改代码，而是
   **清 `.pyc`（`find . -name '*.pyc' -delete` + 删 `__pycache__`）+ `scripts/redo_collateral_if_family.py` 重跑 GIF/IDEA collateral**（环境可重建、服务器有原件）。
   非-IF（GNNDelete/GraphEraser/GraphRevoker/MEGU）的 gap 干净可用。
2. **避免循环论证**：degree 既是 selector 又被当"重要性"代理 → 会变成同义反复。
   **操作上用 (Ⅰ)=`F1_before − F1_retrain`（与 selector 无关）当重要性的客观度量**，
   再证"degree 选点最大化 (Ⅰ)"，循环就破了。
3. **轴B 的理论依据按家族分**（不能一刀切）：
   - **IF 系（GIF/CGU…）**：$U$ 是 Newton/influence step，误差 ∝ 删除方向上的 Hessian 曲率
     + 高阶 Taylor 余项；删高杠杆点 → 大参数扰动 → 线性化失效 → gap 涨。
   - **Learning 系（GNNDelete/MEGU）**：mask/learned operator 在"删除分布"上训练，
     高度数删除是**尾部事件**，学到的算子外推差 → gap 涨。
   - **Shard 系（GraphEraser/Revoker）**：物理重训分片，$\text{unlearn}\approx\text{retrain}$ → gap≈0（结构性安全）。

## 6. 待办（找理论依据 + 完善，用户主导）

- [ ] (Ⅰ) 重要性轴的理论锚：图谱/中心性杠杆、normalized adj $D^{-1/2}AD^{-1/2}$ 扰动、structural redundancy（连到 §5.1 fingerprint 的 "structural-redundancy amplification"）。
- [ ] (Ⅱ) 脆弱性轴的理论锚：IF unlearning 的 influence/Newton 余项界；learned-operator 的分布外推。
- [ ] 修 L8 重跑 → 把 4 个 hop 列 + 干净 gap 灌进 `_phase_b_aggregate.csv`（顺带解 survey 的 H1/H2）。
- [ ] 算 $\beta_M$（gap-vs-$\bar d$ 斜率）做一张"安全指数"小表/小图，作为 §5.2 之后的 §5.x 二级结论。
- [ ] 决定叙事位置：当前 paper 的二级小节 vs follow-up（与 `idea_cross_arch_consensus.md` 一起可凑一篇"unlearning 安全性诊断"follow-up）。

**强版（§7）专属待办：**
- [ ] **IF 系 leverage 分数 $L(v)$ 探针**（cora/GIF，复用 TracIn HVP）：算 $L$，验 `gap ∝ L`、`TracIn/IM 分数 ⊥ L`、`degree ∝ L`。环境后 ~1-2 天。
- [ ] **U-aware selector**：按 $L$ 选点 vs degree（cora 先），看 §7.5 哪种结局。
- [ ] **scale × 机制双用实验**：arxiv 全矩阵**含 degree** + ≥3 seed，验"IM−degree 差随 k 增大"（PROGRESS P2）。
- [ ] Learning 系（GNNDelete）的 OOD leverage 度量设计（最难，可后置）。

## 7. 强版：从 proxy 到 target —— U-aware selector（这条路线的核心 contribution）

> 2026-06-16 加。弱版（§1-§6）能成立但单薄、且坐实了"degree 很水"的担忧。强版的目的：让
> **IF/IM 从"失败的方法"变成"揭示机制的探针 + 通往正确方法的垫脚石"，degree 从"赢家"变成
> "被我们识别出来的廉价代理"，paper 的 hero 变成"正确的攻击目标"本身**。

### 7.1 攻击的正确 target = $\mathcal{U}$ 的近似误差（不是 degree）

由 §2 分解，攻击者真正"利用近似"的杠杆是第二项 gap：
$$
S^\star=\arg\max_S\ \mathrm{Gap}(S,M)=\arg\max_S\big[F_1^{\text{retrain}}(S)-F_1^{\text{unlearn}}(S,M)\big]
$$
即 **unlearning 算子 $\mathcal{U}$ 对删除集 $S$ 的近似误差**。这是"对 $\mathcal{U}$ 误差的 influence"，
与 TracIn（对 test loss 的 influence）、IM（IC 传播覆盖）是**三个不同的 object**。
→ **贡献是识别这个 target，degree 只是它的免费拓扑代理。** 这一句把 paper 从"用 degree"翻成"找到正确目标函数"。

### 7.2 IF/IM 为什么瞄不准（misalignment 的精确版）

- **TracIn** 按 $\partial L_{\text{test}}/\partial\theta\cdot\partial\theta/\partial v$ 在**原模型**上排序 → 测"对精度的贡献"，
  不是"对 $\mathcal{U}$ 线性化误差的贡献"。**可证伪预言**：TracIn 选点 $\bar d\approx$ random、gap≈0（§4 已见 $\bar d{=}3.9\approx$random、tracin gap 垫底）。
- **IM** 按 IC-spread $\sigma(\{v\})$（拓扑覆盖）。**小 k** 时 $\sigma(\{v\})\propto$ degree（所以 IM≈degree）；CELF submodular 精修只在**大 k** 才与 degree 分离。
- 两者都**没碰** $\nabla^2 L$（曲率）或 $\mathcal{U}$ 的具体近似结构 → 系统性失配，不是调参问题。

### 7.3 三族可证伪预言（机制不是叙事）

| family | $\mathcal{U}$ 误差由什么驱动 | 预言 | 数据 |
|---|---|---|---|
| Shard（Eraser/Revoker）| 重训分片 → $\mathcal{U}$ 近似精确 → 误差≈0 | **对任何选点免疫** | ✅ 已验（robust，§4）|
| IF（GIF/IDEA）| Newton step 的曲率 + 高阶余项 → 删高杠杆点误差大 | gap ∝ 删除集 Hessian-leverage | 待算（需 L8-clean）|
| Learning（GNNDelete/MEGU）| learned mask 对"删除分布"的外推 → 高度数=尾部 | gap ∝ 删除的 OOD 程度 | ◐ GNNDelete gap 已见 degree 单调（§4）|

Shard 免疫这条**已印证机制的一半**（是预言，不是巧合）——这是"叙事 vs 机制"的关键区别。

### 7.4 决定性一招：leverage 分数 + U-aware selector

- **IF 系** $L(v)\approx$ self-influence / Hessian-leverage 代理（如 $\|\nabla_\theta L(v)\|^2_{H^{-1}}$ 或 influence 算子对角），
  **用现有 TracIn 的 HVP 基建可算，不需全 retrain**。
- **Learning 系** $L(v)\approx$ 删除在 mask network 训练分布下的 OOD 度（最难一块；候选：删除集在 mask net 上的梯度范数 / 重构误差）。
- **Shard 系**：免疫，无需 selector。
- selector：对 $L(v)$ 跑 greedy/CELF 或 topk。
- **实验**：U-aware（按 $L$ 选）能否打过 degree？cora 先做，再 arxiv。

### 7.5 两种结局都能发（这一步是上保险，不是赌）

- U-aware **>** degree → **正向新方法 + 机制坐实**；IF/IM=垫脚石，degree=被超越的代理。**硬 paper。**
- U-aware **≈** degree → "**degree 是对 GU 最优攻击的免费、黑盒、近最优代理**"——廉价逼近昂贵最优的干净结果。**照样发。**

### 7.6 与 scale 轴合流（一个实验两用）

机制预言：**小 k（cora）leverage≈degree → degree 近最优；大 k（arxiv）最优集需多样性/submodular → IM 或 U-aware 拉开 degree。**
即 **IM−degree 的差应随 k 增大**。arxiv pilot（GNNDelete IM **+18pp**、degree **没跑**）是第一个信号 →
**arxiv 全矩阵 + degree 同时是 scale 实验和机制检验**（见 PROGRESS P2 / 5 轴 paper）。

### 7.7 风险 / 诚实

- $L(v)$ 是 **family-specific**，不是单一通用分数（IF 可算、learning 难、shard 不需要）。
- GNNDelete 的 OOD 度量是最难的一块，可能要单独设计。
- 需要 **L8-clean 的 gap**（IF 系 gap 现被污染，§5 坑1）——这是前置。
- U-aware **可能打不过 degree**（但按 §7.5 那也是一个干净结果）。

### 7.8 工作量

- IF 系 $L(v)$ 探针（cora，复用 TracIn HVP + 已有 gap）：环境重建后 **~1-2 天分析**。
- 完整（含 learning OOD 度量 + arxiv 检验）：更多，属重投实质。

---

## 8. 一句话评估

**路径成立、且用现有数据已部分验证**。它把"degree 通吃"从尴尬翻成原理（结构杠杆=共同驱动），
gap 把方法脆弱性单独量化（GNNDelete 上甚至比 F1 更稳），并给出一个零新数据的安全指数。
**强版（§7）进一步把 gap 抬成正式攻击 target + U-aware selector**，是这篇 paper 不水的核心：
IF/IM 成探针、degree 成被识别的代理、"正确的攻击目标"成 hero。
硬前提：先修 L8（覆盖 IF-family gap）+ 重建环境。弱版可先作 §5.2 后二级结论；强版是重投的核心 contribution。
