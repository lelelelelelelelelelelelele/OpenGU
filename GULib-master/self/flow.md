# Flow：功能模块与测试设计

> **v2 增量补丁**：eval 指标、归因框架、指标命名等章节已有升级，见 [`plan_flow_v2_delta.md`](plan_flow_v2_delta.md)。本文件内容保持不变，增量变更记录于该文件。

本文档定义每个需要新增的函数、其输入输出规格、以及对应的测试方案。

---

## 1. 总体调用流程

```
attack_main.py / main.py
  │
  ├── 1. 加载数据 & 预训练模型
  │
  ├── 2. AttackManager.get_strategy(strategy_name)
  │       └── 返回 BaseStrategy 子类实例
  │
  ├── 3. strategy.select_nodes(data, model, k)
  │       │
  │       ├── [Random]  → random_select()
  │       ├── [Degree]  → compute_degree() → topk
  │       ├── [PageRank]→ compute_pagerank() → topk
  │       ├── [TracIn]  → compute_tracin_scores() → topk
  │       ├── [IM]      → compute_im_celf() → greedy topk
  │       └── [Hybrid]  → compute_tracin_scores()
  │                       + compute_im_celf()
  │                       → fuse_scores() → topk
  │
  ├── 4. 执行遗忘: unlearning_method.run_exp(unlearn_nodes=selected)
  │
  └── 5. 评估: attack_eval.evaluate(model_before, model_after, data)
```

---

## 2. 指标计算函数（底层）

这些是被策略函数调用的底层计算模块。

### 2.1 `compute_degree(edge_index, num_nodes) -> Tensor`

**文件**: `attack/attack_strategies/degree_strategy.py`

```python
def compute_degree(edge_index: Tensor, num_nodes: int) -> Tensor:
    """
    计算每个节点的度数。

    Args:
        edge_index: [2, E] 边索引
        num_nodes: 节点总数

    Returns:
        degree: [N] 每个节点的度数
    """
```

**测试**:
- 输入一个已知的小图（如 5 节点三角形 + 孤立点），验证度数是否正确
- 验证有向图 vs 无向图的处理
- 边界: 空图、单节点图

---

### 2.2 `compute_pagerank(edge_index, num_nodes, damping=0.85, max_iter=100) -> Tensor`

**文件**: `attack/attack_strategies/pagerank_strategy.py`

```python
def compute_pagerank(
    edge_index: Tensor,
    num_nodes: int,
    damping: float = 0.85,
    max_iter: int = 100,
    tol: float = 1e-6
) -> Tensor:
    """
    计算 PageRank 值。

    Args:
        edge_index: [2, E] 边索引
        num_nodes: 节点总数
        damping: 阻尼系数
        max_iter: 最大迭代次数
        tol: 收敛阈值

    Returns:
        pagerank: [N] 每个节点的 PageRank 值
    """
```

**测试**:
- 用 networkx 的 `nx.pagerank()` 作为 ground truth 对比，误差 < 1e-4
- 验证所有 PageRank 值之和 ≈ 1.0
- 验证星型图中心节点 PageRank 最高
- 性能: Cora (2708 节点) 上执行时间 < 1s

---

### 2.3 `compute_tracin_scores(model, data, train_mask, checkpoint_paths=None) -> Tensor`

**文件**: `attack/attack_strategies/tracin_strategy.py`

```python
def compute_tracin_scores(
    model: torch.nn.Module,
    data: Data,
    train_mask: Tensor,
    test_mask: Tensor,
    checkpoint_paths: Optional[List[str]] = None
) -> Tensor:
    """
    计算每个训练节点的 TracIn self-influence score。

    TracIn(z_i) = sum_t η_t * <∇L(z_i, θ_t), ∇L(z_i, θ_t)>

    简化版（单 checkpoint）:
    TracIn(z_i) ≈ ||∇L(z_i, θ)||^2

    Args:
        model: 已训练的 GNN 模型
        data: PyG Data 对象
        train_mask: 训练节点 mask
        test_mask: 测试节点 mask
        checkpoint_paths: 模型 checkpoint 路径列表（可选，None 则用当前参数）

    Returns:
        scores: [N_train] 每个训练节点的 TracIn 得分
    """
```

**内部辅助函数**:

```python
def _compute_node_gradient(model, data, node_idx) -> Tensor:
    """
    计算单个节点 loss 对模型参数的梯度，展平为一维向量。

    Returns:
        grad: [P] P 为模型参数总数
    """

def _compute_gradient_dot_product(grad_a, grad_b) -> float:
    """两个梯度向量的点积。"""
```

**测试**:
- 验证梯度维度 = 模型参数总数
- 验证 self-influence score 非负（因为是梯度范数的平方）
- 对比: 在 Cora+GCN 上，高 TracIn 节点是否与高 degree 节点有相关性（预期：有一定相关但不完全重合）
- 验证多 checkpoint 累加 vs 单 checkpoint 的结果差异
- 性能: Cora 上全节点计算时间 < 60s（单 GPU）

---

### 2.4 `compute_im_celf(edge_index, num_nodes, k, mc_rounds=100) -> List[int]`

**文件**: `attack/attack_strategies/im_strategy.py`

```python
def compute_im_celf(
    edge_index: Tensor,
    num_nodes: int,
    k: int,
    propagation_prob: float = 0.1,
    mc_rounds: int = 100
) -> Tuple[List[int], Tensor]:
    """
    CELF 加速的贪心 Influence Maximization。

    使用 Independent Cascade (IC) 模型模拟传播。

    Args:
        edge_index: [2, E] 边索引
        num_nodes: 节点总数
        k: 选择节点数
        propagation_prob: 传播概率
        mc_rounds: Monte Carlo 模拟轮数

    Returns:
        selected_nodes: 选中的 k 个节点 ID 列表
        marginal_gains: 每个节点被选中时的边际增益
    """
```

**内部辅助函数**:

```python
def _simulate_spread(edge_index, seed_set, prob, num_nodes) -> float:
    """
    单次 Independent Cascade 模拟。

    Args:
        seed_set: 种子节点集合
        prob: 传播概率

    Returns:
        spread: 被影响的节点数量
    """

def _estimate_spread(edge_index, seed_set, prob, num_nodes, mc_rounds) -> float:
    """多次 MC 模拟取平均。"""
```

**测试**:
- 星型图: 中心节点必须第一个被选中
- 验证 CELF 优化: 结果与朴素贪心一致，但函数调用次数更少
- 验证选出 k 个节点且无重复
- 性能: Cora 上 k=50, mc_rounds=100 时间 < 120s

---

### 2.5 `fuse_scores(if_scores, im_scores, method, alpha=0.5) -> Tensor`

**文件**: `attack/attack_strategies/hybrid_strategy.py`

```python
def fuse_scores(
    if_scores: Tensor,
    im_scores: Tensor,
    method: str = "rank",
    alpha: float = 0.5
) -> Tensor:
    """
    融合 IF 和 IM 两个维度的得分。

    Args:
        if_scores: [N] IF 维度得分
        im_scores: [N] IM 维度得分
        method: "linear" | "rank"
            - linear: alpha * norm(IF) + (1-alpha) * norm(IM)
            - rank: alpha * rank(IF) + (1-alpha) * rank(IM)
        alpha: 权重系数

    Returns:
        fused: [N] 融合后的得分
    """
```

**内部辅助函数**:

```python
def _min_max_normalize(scores: Tensor) -> Tensor:
    """Min-max 归一化到 [0, 1]。"""

def _rank_normalize(scores: Tensor) -> Tensor:
    """转为排名百分比 [0, 1]，最高分 = 1.0。"""
```

**测试**:
- 当 alpha=1.0 时，结果排序应与 IF 排序一致
- 当 alpha=0.0 时，结果排序应与 IM 排序一致
- rank-based fusion 对 score 乘以常数后排序不变
- linear fusion 对 score 乘以常数后排序可能改变（验证 rank 方法的鲁棒性优势）
- 输入含 NaN/Inf 时的异常处理

---

## 3. 节点选择策略函数（上层）

每个策略类继承 `BaseStrategy`，核心方法是 `select_nodes()`。

### 3.1 `BaseStrategy` 抽象基类

**文件**: `attack/attack_strategies/base_strategy.py`

```python
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, args: dict):
        self.args = args

    @abstractmethod
    def select_nodes(
        self,
        data: Data,
        model: torch.nn.Module,
        k: int
    ) -> Tensor:
        """
        选择 k 个节点用于遗忘。

        Args:
            data: PyG Data 对象（含 edge_index, x, y, masks）
            model: 已训练的 GNN 模型（部分策略不使用）
            k: 选择节点数

        Returns:
            node_indices: [k] 选中的节点索引
        """
        pass

    def select_nodes_by_ratio(
        self,
        data: Data,
        model: torch.nn.Module,
        ratio: float
    ) -> Tensor:
        """按比例选择节点。ratio ∈ (0, 1)。"""
        k = int(data.num_nodes * ratio)
        return self.select_nodes(data, model, k)
```

---

### 3.2 各策略实现

| 策略类 | `select_nodes()` 实现逻辑 |
|--------|--------------------------|
| `RandomStrategy` | `torch.randperm(N)[:k]` |
| `DegreeStrategy` | `compute_degree()` → `torch.topk()` |
| `PageRankStrategy` | `compute_pagerank()` → `torch.topk()` |
| `TracInStrategy` | `compute_tracin_scores()` → `torch.topk()` |
| `IMStrategy` | `compute_im_celf()` → 返回贪心选中列表 |
| `HybridStrategy` | `compute_tracin_scores()` + `compute_im_celf()` → `fuse_scores()` → `torch.topk()` |

---

### 3.3 策略层测试矩阵

对每个策略统一测试以下内容:

| 测试项 | 说明 | 验证方法 |
|--------|------|---------|
| 输出形状 | 返回恰好 k 个节点 | `assert len(result) == k` |
| 无重复 | 选出的节点无重复 | `assert len(set(result)) == k` |
| 有效索引 | 所有索引 ∈ [0, N) | `assert (result >= 0).all() and (result < N).all()` |
| 确定性 | 固定 seed 后结果一致（Random 除外） | 两次调用结果相同 |
| ratio 接口 | `select_nodes_by_ratio` 与手动算 k 结果一致 | 对比两种调用方式 |
| Cora 端到端 | 在 Cora 上跑通，不报错 | 加载真实数据测试 |

---

## 4. 攻击调度：AttackManager

**文件**: `attack/attack_manager.py`

```python
class AttackManager:
    strategy_map = {
        "random": RandomStrategy,
        "degree": DegreeStrategy,
        "pagerank": PageRankStrategy,
        "tracin": TracInStrategy,
        "im": IMStrategy,
        "hybrid": HybridStrategy,
    }

    def __init__(self, args: dict):
        self.args = args

    def get_strategy(self, strategy_name: str) -> BaseStrategy:
        """
        根据名称返回策略实例。

        Args:
            strategy_name: 策略名称（key in strategy_map）

        Returns:
            strategy: BaseStrategy 子类实例

        Raises:
            ValueError: 未知策略名称
        """
```

**测试**:
- 所有已注册策略名称都能正确实例化
- 未知名称抛出 `ValueError`
- 返回对象是 `BaseStrategy` 子类

---

## 5. 攻击评估函数

**文件**: `attack/attack_eval.py`

### 5.1 `evaluate_f1_drop(model_before, model_after, data, test_mask) -> dict`

```python
def evaluate_f1_drop(
    model_before: torch.nn.Module,
    model_after: torch.nn.Module,
    data: Data,
    test_mask: Tensor
) -> dict:
    """
    评估遗忘前后模型在测试集上的 F1 变化。

    Returns:
        {
            "f1_before": float,
            "f1_after": float,
            "f1_drop": float,          # before - after
            "f1_drop_pct": float,       # (before - after) / before * 100
        }
    """
```

**测试**:
- 同一个模型作为 before 和 after → drop = 0
- 随机初始化模型作为 after → drop 显著为正
- 验证 F1 计算与 sklearn 一致

### 5.2 `evaluate_mia_auc(model, data, member_mask, non_member_mask) -> float`

```python
def evaluate_mia_auc(
    model: torch.nn.Module,
    data: Data,
    member_mask: Tensor,
    non_member_mask: Tensor
) -> float:
    """
    简易 MIA 评估：用模型输出 confidence 做 membership 判断。

    Returns:
        auc: MIA AUC score (0.5 = 无信息泄露)
    """
```

**测试**:
- 随机模型 → AUC ≈ 0.5
- member 和 non_member 大小不同时仍能正确计算

### 5.3 `evaluate_retrain_gap(model_before, model_unlearned, model_retrained, data, test_mask) -> dict`

> **已实现**: `attack/attack_eval.py:92`

```python
def evaluate_retrain_gap(
    model_before: torch.nn.Module,
    model_unlearned: torch.nn.Module,
    model_retrained: torch.nn.Module,
    data: Data,
    test_mask: Tensor
) -> dict:
    """
    Attribution framework: decompose total performance drop.

    - Drop_retrain = Perf_before - Perf_retrain  (inherent loss from deletion)
    - Gap = Perf_retrain - Perf_unlearn           (extra loss from approximate unlearning)

    Returns:
        {
            "perf_before": float,
            "perf_retrain": float,
            "perf_unlearn": float,
            "drop_retrain": float,     # perf_before - perf_retrain
            "gap": float,              # perf_retrain - perf_unlearn
            "gap_pct": float,
        }
    """
```

**测试**:
- 同一模型 → gap = 0
- 验证归因分解: drop_retrain + gap = perf_before - perf_unlearn

### 5.4 `evaluate_collateral_damage(model_unlearned, model_retrained, data, retain_mask) -> dict`

> **已实现**: `attack/attack_eval.py:129`

```python
def evaluate_collateral_damage(
    model_unlearned: torch.nn.Module,
    model_retrained: torch.nn.Module,
    data: Data,
    retain_mask: Tensor
) -> dict:
    """
    Measure prediction disturbance on retained nodes (inspired by UtU's Δp).

    Compares model_unlearned vs model_retrained on the retain set.
    Both models share the same deletion set; the difference isolates
    the approximation error's collateral effect on retained nodes.

    Returns:
        {
            "mean_pred_shift": float,
            "max_pred_shift": float,
            "fraction_flipped": float,
        }
    """
```

**测试**:
- 同一模型 → mean_pred_shift = 0, fraction_flipped = 0
- 随机模型 vs 训练模型 → shift > 0

---

## 6. 端到端测试流程

以下是对完整攻击流程的集成测试。

### 测试 1: Random 策略 × GIF × Cora

```
目的: 验证整个 pipeline 能跑通
步骤:
  1. 加载 Cora, 训练 GCN
  2. AttackManager.get_strategy("random")
  3. strategy.select_nodes(data, model, k=50)
  4. 运行 GIF unlearning (移除选中节点)
  5. evaluate_f1_drop()
预期: F1 有一定下降，pipeline 无报错
```

### 测试 2: 所有策略 × GIF × Cora

```
目的: 对比不同策略的攻击效果
步骤:
  对 [random, degree, pagerank, tracin, im, hybrid] 分别:
    1. select_nodes(k=50)
    2. GIF unlearning
    3. evaluate_f1_drop()
预期: tracin / hybrid 的 F1 drop > degree / pagerank > random
```

### 测试 3: Hybrid 策略 × 多遗忘方法 × Cora

```
目的: 验证攻击跨遗忘方法的泛化性
步骤:
  对 [GIF, GST, GNNDelete, MEGU] 分别:
    1. hybrid.select_nodes(k=50)
    2. 运行对应遗忘方法
    3. evaluate_f1_drop()
预期: IF-based 方法 (GIF, GST) F1 drop 大于 Learning-based；Shard-based (GraphEraser) 攻击效果较弱
```

### 测试 4: Unlearn ratio 敏感性

```
目的: 分析遗忘比例对攻击效果的影响
步骤:
  对 ratio ∈ [0.01, 0.05, 0.10, 0.20]:
    1. hybrid.select_nodes_by_ratio(ratio)
    2. GIF unlearning
    3. evaluate_f1_drop()
预期: ratio 越大 F1 drop 越大，但边际递减
```

### 测试 5: Retrain 对照

> **已实现**: `eval_collateral.py` + `tests/test_collateral.py` (17 测试)

```
目的: 证明攻击利用了近似误差
步骤:
  1. hybrid.select_nodes(k=50) → D_unlearn
  2. GIF unlearning → model_unlearned
  3. 从头训练 GCN（去掉 D_unlearn）→ model_retrained  (via AttackPipeline.run_retrain())
  4. evaluate_retrain_gap(model_before, model_unlearned, model_retrained, data, test_mask)
  5. evaluate_collateral_damage(model_unlearned, model_retrained, data, retain_mask)
预期: model_unlearned 的 F1 显著低于 model_retrained (gap > 0)
```

---

## 7. 函数依赖关系图

```
hybrid_strategy.select_nodes()
  ├── tracin_strategy.compute_tracin_scores()
  │     ├── _compute_node_gradient()
  │     └── _compute_gradient_dot_product()
  ├── im_strategy.compute_im_celf()
  │     ├── _simulate_spread()
  │     └── _estimate_spread()
  └── fuse_scores()
        ├── _min_max_normalize()
        └── _rank_normalize()

attack_eval.evaluate_f1_drop()
  └── sklearn.metrics.f1_score()

attack_eval.evaluate_mia_auc()
  └── sklearn.metrics.roc_auc_score()

attack_eval.evaluate_retrain_gap()
  └── sklearn.metrics.f1_score()

attack_eval.evaluate_collateral_damage()
  └── torch.nn.functional.softmax()

AttackManager.get_strategy()
  └── strategy_map[name](args)

AttackPipeline.run_retrain()
  ├── model_zoo()           # 重新初始化模型
  ├── method.run_exp()      # train_only 模式
  ├── _get_trained_model()  # 提取模型
  └── _evaluate_model()     # F1 评估

eval_collateral.py
  ├── ResultCache.get()
  ├── pipeline._inject_unlearn_nodes()
  ├── pipeline.run_retrain()
  ├── evaluate_retrain_gap()
  └── evaluate_collateral_damage()
```

---

## 8. 开发顺序（含 Git 存档 & 测试验收）

每个 Step 严格遵循：**编码 → 单元测试 → 验收条件 → git 存档** 的流程。
只有验收条件全部通过，才能 commit 并进入下一步。

---

### Step 0: OpenGU 基础设施验证（地基测试）

**目的**: 在构建攻击模块之前，验证 OpenGU 框架中各 GU 方法、模型、数据集的可用性。
明确哪些方法能正常运行，哪些有 bug 或不兼容，避免后续实验时踩坑。

**无新建代码文件**，仅新建测试脚本和日志。

#### 0.1 测试矩阵

分两轮测试：先广度扫描（快速排除坏方法），再深度验证（确认重点方法在不同条件下稳定）。

**第一轮：广度扫描（1 模型 × 1 数据集 × 默认参数）**

目标：快速判断 15 个方法哪些能跑通。

| 方法 | 模型 | 数据集 | unlearn_nodes | 预期 |
|------|------|--------|---------------|------|
| GraphEraser | GCN | Cora | 270 (默认) | 跑通 |
| GIF | GCN | Cora | 270 | 跑通 |
| GST | GCN | Cora | 270 | 跑通 |
| GNNDelete | GCN | Cora | 270 | 跑通 |
| CEU | GCN | Cora | 270 | 跑通 |
| CGU | GCN | Cora | 270 | 跑通 |
| SGU | GCN | Cora | 270 | 跑通 |
| MEGU | GCN | Cora | 270 | 跑通 |
| UTU | GCN | Cora | 270 | 跑通 |
| GUKD | GCN | Cora | 270 | 跑通 |
| D2DGN | GCN | Cora | 270 | 跑通 |
| IDEA | GCN | Cora | 270 | 跑通 |
| Projector | GCN | Cora | 270 | 跑通 |
| GraphRevoker | GCN | Cora | 270 | 跑通 |

命令模板：
```bash
python main.py --cuda 0 --dataset_name cora --base_model GCN \
  --unlearning_methods {METHOD} --unlearn_task node --downstream_task node \
  --num_epochs 100 --num_runs 1
```

**第一轮输出**: 将每个方法标记为 ✅ 可用 / ❌ 报错 / ⚠️ 跑通但结果异常

**第二轮：深度验证（仅对第一轮 ✅ 的方法）**

对通过第一轮的方法，测试模型/数据集/遗忘量的组合：

| 维度 | 取值 |
|------|------|
| 模型 | GCN, GAT |
| 数据集 | Cora, Citeseer |
| 遗忘节点数 | 10, 100, 1000 |

即每个 ✅ 方法最多 2×2×3 = **12 组**实验。

命令模板：
```bash
python main.py --cuda 0 --dataset_name {DATASET} --base_model {MODEL} \
  --unlearning_methods {METHOD} --unlearn_task node --downstream_task node \
  --num_unlearned_nodes {N} --num_epochs 100 --num_runs 1
```

#### 0.2 记录指标

每组实验记录以下信息：

| 字段 | 说明 |
|------|------|
| method | 遗忘方法名 |
| model | GNN backbone |
| dataset | 数据集 |
| num_unlearned | 遗忘节点数 |
| status | ✅ / ❌ / ⚠️ |
| error_msg | 如果报错，记录错误信息 |
| f1_before | 遗忘前 F1 |
| f1_after | 遗忘后 F1 |
| time_s | 总耗时（秒）|
| mem_mb | 显存占用（如可获取）|
| notes | 备注（如：1000 节点时 OOM）|

#### 0.3 输出文件

```
results/step0_validation/
  ├── round1_scan.md          # 第一轮广度扫描汇总表
  ├── round2_detail.md        # 第二轮深度验证汇总表
  ├── round1_logs/            # 第一轮每个方法的运行日志
  │   ├── GIF_GCN_cora.log
  │   ├── GST_GCN_cora.log
  │   └── ...
  ├── round2_logs/            # 第二轮详细日志
  │   ├── GIF_GCN_cora_10.log
  │   ├── GIF_GCN_cora_100.log
  │   └── ...
  └── method_compatibility.json   # 机器可读的兼容性矩阵
```

`method_compatibility.json` 格式：
```json
{
  "GIF": {
    "status": "✅",
    "compatible_models": ["GCN", "GAT"],
    "compatible_datasets": ["cora", "citeseer"],
    "max_unlearn_nodes_tested": 1000,
    "known_issues": [],
    "notes": "stable across all configurations"
  },
  "CEU": {
    "status": "⚠️",
    "compatible_models": ["GCN"],
    "compatible_datasets": ["cora"],
    "max_unlearn_nodes_tested": 100,
    "known_issues": ["OOM at 1000 nodes on citeseer"],
    "notes": "hessian computation is memory-intensive"
  }
}
```

#### 0.4 验收条件

- [x] 第一轮：15 个方法全部测试完毕，生成 round1_scan.md
- [x] 至少 5 个方法标记为 ✅（如果少于 5 个，说明框架有系统性问题，需先修复）  → 11/15 通过
- [ ] 重点方法 GIF, GST 必须 ✅（这两个是后续攻击的主要目标）  → GIF ✅, GST ❌ (forward() API 不兼容，可修复)
- [x] 第二轮：所有 ✅ 方法 × 5 unlearn_ratio 完成，生成 round2_detail.md  (注：发现 num_unlearned_nodes 被覆盖，改用 unlearn_ratio 测试)
- [x] 识别出各方法的遗忘量上限（多少节点会 OOM 或数值不稳定）  → 见 method_compatibility.json
- [x] 生成 method_compatibility.json
- [x] 确认后续实验的安全参数范围（哪些 method × model × dataset × N 的组合是可靠的）  → 见 round2_detail.md

#### 0.5 Git 存档

```
git checkout -b feat/attack-strategies
mkdir -p results/step0_validation/round1_logs results/step0_validation/round2_logs
git add results/step0_validation/
git commit -m "step-0: OpenGU framework validation, 15 methods × compatibility matrix"
```

#### 0.6 Step 0 的结论如何影响后续

| Step 0 发现 | 对后续的影响 |
|------------|------------|
| GIF/GST 全 ✅ | 后续正常执行 |
| 某方法 ❌ | 从实验矩阵中移除该方法 |
| 某方法在 1000 节点 OOM | 该方法的 unlearn_ratio 实验设上限 |
| 某 model+method 不兼容 | 跨模型实验时避开该组合 |
| Citeseer 上多方法异常 | 考虑换用 PubMed 或 Physics |

### Git 规范

- 分支: `feat/attack-strategies`（从 main 拉出）
- Commit message 格式: `step-{N}: {简要描述}`
- 每个 step 对应一个 commit（如有 bugfix 则追加 `fix(step-{N}): ...`）
- Tag: 关键里程碑打 tag（如 `v0.1-baseline`, `v0.2-core`）

---

### Step 1: 骨架 + Random 策略

**新建文件**:
- `attack/attack_strategies/__init__.py`
- `attack/attack_strategies/base_strategy.py`
- `attack/attack_strategies/random_strategy.py`
- `tests/test_strategies.py`（测试文件）

**单元测试**:
```python
# tests/test_strategies.py
def test_random_output_shape():
    """返回恰好 k 个节点"""
def test_random_no_duplicates():
    """无重复节点"""
def test_random_valid_indices():
    """所有索引 ∈ [0, N)"""
def test_random_ratio_interface():
    """select_nodes_by_ratio 与手动算 k 一致"""
```

**验收条件**:
- [x] 4 个单元测试全部通过
- [x] RandomStrategy 能在 Cora 数据上调用不报错（手动验证）

**Git 存档**:
```
git add attack/attack_strategies/ tests/test_strategies.py
git commit -m "step-1: base strategy ABC + random strategy with unit tests"
```

---

### Step 2: Degree + PageRank 策略

**新建文件**:
- `attack/attack_strategies/degree_strategy.py`
- `attack/attack_strategies/pagerank_strategy.py`

**单元测试**:
```python
def test_degree_known_graph():
    """5 节点三角形+孤立点，验证度数=[2,2,2,1,0]"""
def test_degree_topk_order():
    """top-k 按度数降序"""
def test_pagerank_star_graph():
    """星型图中心节点 PageRank 最高"""
def test_pagerank_sum_to_one():
    """所有 PR 值之和 ≈ 1.0"""
def test_pagerank_vs_networkx():
    """与 nx.pagerank() 结果误差 < 1e-4"""
```

**验收条件**:
- [x] 5 个单元测试全部通过
- [x] Cora 上 degree top-50 和 pagerank top-50 有交集但不完全重合（sanity check）
- [x] 三策略(random/degree/pagerank)的选点结果可以写出到 txt，格式与原 pipeline 兼容

**Git 存档**:
```
git commit -m "step-2: degree + pagerank strategies with validation against networkx"
```

---

### Step 3: AttackManager 调度器

**修改文件**:
- `attack/attack_manager.py`（填充现有空文件）
- `attack/__init__.py`（添加导出）

**单元测试**:
```python
def test_manager_all_strategies():
    """所有注册名称都能实例化"""
def test_manager_unknown_raises():
    """未知名称抛出 ValueError"""
def test_manager_returns_base_strategy():
    """返回对象 isinstance(BaseStrategy)"""
```

**验收条件**:
- [x] 3 个单元测试通过
- [x] 能通过字符串参数选择策略并生成选点文件

**Git 存档**:
```
git commit -m "step-3: attack manager with strategy dispatch"
git tag v0.1-baseline
```

**里程碑**: v0.1-baseline — 三个 baseline 策略 + 调度器就绪

---

### Step 4: TracIn 策略（核心）

**新建文件**:
- `attack/attack_strategies/tracin_strategy.py`

**单元测试**:
```python
def test_node_gradient_shape():
    """梯度维度 = 模型参数总数"""
def test_tracin_score_non_negative():
    """self-influence score >= 0（梯度范数平方）"""
def test_tracin_deterministic():
    """固定 seed 后两次计算结果一致"""
def test_tracin_topk_differs_from_random():
    """TracIn top-50 与 random 50 的重合率 < 50%"""
```

**验收条件**:
- [x] 4 个单元测试通过
- [x] Cora+GCN 上全节点 TracIn 计算完成，无 OOM
- [x] **关键验证**: TracIn top-50 送入 GIF unlearning 后 F1 drop > Random top-50 的 F1 drop
- [x] 计算耗时记录到 `results/` (作为 efficiency baseline)

**Git 存档**:
```
git commit -m "step-4: tracin pseudo-IF strategy, validated F1 drop > random on cora+GIF"
```

---

### Step 5: Influence Maximization 策略

**新建文件**:
- `attack/attack_strategies/im_strategy.py`

**单元测试**:
```python
def test_im_star_graph():
    """星型图 k=1 时必选中心节点"""
def test_im_no_duplicate():
    """CELF 选出 k 个不重复节点"""
def test_im_celf_equals_naive():
    """小图上 CELF 结果与朴素贪心一致"""
def test_im_spread_monotone():
    """seed set 越大，spread 单调递增"""
```

**验收条件**:
- [x] 4 个单元测试通过
- [x] Cora 上 k=50, mc_rounds=100 跑通，耗时 < 120s
- [x] IM top-50 的 F1 drop 与 degree/pagerank 对比（记录数据）

**Git 存档**:
```
git commit -m "step-5: influence maximization (CELF) strategy"
```

---

### Step 6: Hybrid 融合策略

**新建文件**:
- `attack/attack_strategies/hybrid_strategy.py`

**单元测试**:
```python
def test_fuse_alpha_one():
    """alpha=1.0 → 排序与 IF 一致"""
def test_fuse_alpha_zero():
    """alpha=0.0 → 排序与 IM 一致"""
def test_rank_fusion_scale_invariant():
    """rank-based 对 score*100 排序不变"""
def test_linear_fusion_scale_sensitive():
    """linear 对 score*100 排序可能变（对比 rank 优势）"""
def test_fuse_nan_handling():
    """含 NaN 输入不崩溃"""
```

**验收条件**:
- [x] 5 个单元测试通过
- [x] **核心验证**: Cora+GCN+GIF 上 Hybrid F1 drop ≥ max(TracIn alone, IM alone)
- [x] Linear vs Rank-based 结果对比记录

**Git 存档**:
```
git commit -m "step-6: hybrid IF-IM fusion strategy with linear and rank-based modes"
git tag v0.2-core
```

**里程碑**: v0.2-core — 全部 6 个策略就绪

---

### Step 7: 评估模块

**新建文件**:
- `attack/attack_eval.py`

**单元测试**:
```python
def test_f1_drop_same_model():
    """同一模型 → drop=0"""
def test_f1_drop_matches_sklearn():
    """F1 计算与 sklearn.metrics.f1_score 一致"""
def test_mia_auc_random_model():
    """随机模型 → AUC ≈ 0.5 (±0.1)"""
def test_retrain_gap_same_model():
    """同一模型 → gap=0"""
```

**验收条件**:
- [x] 4 个单元测试通过
- [x] 完整 pipeline 跑通: 策略选点 → 遗忘 → 评估 → JSON 写入 results/

**Git 存档**:
```
git commit -m "step-7: attack evaluation module (f1_drop, mia_auc, retrain_gap)"
```

---

### Step 8: 端到端实验（Phase 1-2）

**无新建文件**，纯实验运行。

**实验矩阵**:
```
6 策略 × GIF × Cora × GCN = 6 组实验
6 策略 × GST × Cora × GCN = 6 组实验（可选）
```

**验收条件**:
- [x] 所有 6 个策略在 GIF+Cora 上都能跑通
- [x] 结果 JSON 全部写入 `results/`
- [x] 生成策略对比表，确认排序符合预期: hybrid ≥ tracin > im ≥ pagerank ≥ degree > random
- [x] 如果排序不符合预期，记录异常并分析原因

**Git 存档**:
```
git commit -m "step-8: phase 1-2 experiments, 6 strategies × GIF × cora"
git tag v0.3-experiments
```

**里程碑**: v0.3-experiments — 核心实验完成，可以开始写论文初稿

---

### Step 9: 扩展实验（Phase 3-4）

**验收条件**:
- [x] 跨遗忘方法: hybrid × [GIF, GNNDelete, GraphEraser, IDEA, MEGU] (缺 GST)
- [x] 跨数据集: hybrid × GIF × [Cora, Citeseer] (缺 PubMed, Physics)
- [x] 跨模型: hybrid × GIF × [GCN, GAT] (缺 GIN, SAGE)
- [ ] Unlearn ratio 敏感性: [1%, 5%, 10%, 20%] 四组结果
- [x] Retrain 对照: Phase A+ 有 retrain gap 结果
- [x] GraphEraser 抗攻击对照
- [x] MIA AUC 评估

> 2026-02-22 更新: MG-0 ~ MG-3 完成 (5 seeds × 6 strategies)

**Git 存档**:
```
git commit -m "step-9: phase 3-4 generalization experiments"
git tag v1.0-complete
```

---

### 总览: Git 存档检查点

| Step | Commit | Tag | 里程碑 |
|------|--------|-----|--------|
| 1 | `step-1: base + random` | | |
| 2 | `step-2: degree + pagerank` | | |
| 3 | `step-3: attack manager` | `v0.1-baseline` | Baseline 就绪 |
| 4 | `step-4: tracin` | | |
| 5 | `step-5: im (CELF)` | | |
| 6 | `step-6: hybrid fusion` | `v0.2-core` | 核心方法就绪 |
| 7 | `step-7: eval module` | | |
| 8 | `step-8: phase 1-2 exp` | `v0.3-experiments` | 核心实验完成 |
| 9 | `step-9: phase 3-4 exp` | `v1.0-complete` | 全部实验完成 |
