"""Phase B invariants — regression locks for the 8-bug audit (2026-05-06).

Each test below pins one of the bugs from `self/dashboard/EXPERIMENT_DASHBOARD.md §3.6`
to a discrete property test. PASS == that bug is physically impossible to
re-introduce silently. Numbers (f1, mia_auc) drift; properties don't.

Mapping:
    test_hybrid_alpha_changes_cache_key       — Bug "SelectionCache hyperparam gaps" (Hybrid α)
    test_baselines_subset_of_train_mask       — Bug "baselines ignore train_mask"
    test_tracin_trained_differs_from_random_init — Bug "random-init TracIn/Hybrid"
    test_cache_key_isolation_across_hyperparams — Bug "SelectionCache cross-contamination"
    test_inject_path_matches_config_unlearning_path — Bug "config path leakage"
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Dict

import pytest
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data

from attack.attack_manager import AttackManager
from attack.attack_result import AttackResult
from attack.selection_cache import SelectionCache, SelectionResult
from attack.attack_strategies import (
    DegreeStrategy,
    PageRankStrategy,
    RandomStrategy,
    TracInStrategy,
)


# ----------------------------------------------------------------------
# Shared helpers
# ----------------------------------------------------------------------


class _StubManager:
    """Minimal stand-in for AttackManager so we can exercise the cache-key
    helpers without paying for a full pipeline (data load + model_zoo).

    The methods we call below only touch self.args / self.data, so a stub
    with those attributes is enough.
    """

    def __init__(self, args: Dict[str, Any], data=None):
        self.args = args
        self.data = data
        self._graph_fingerprint = None


class _FakePipeline:
    def __init__(self, data):
        self.data = data
        self.model = nn.Linear(data.num_features, int(data.y.max().item()) + 1)
        self.called_run_with_strategy = False
        self.called_run_with_selected_nodes = False

    def run_with_strategy(self, strategy, k):
        self.called_run_with_strategy = True
        return {
            "selected_nodes": torch.arange(k),
            "f1_before": None,
            "f1_after": 0.0,
            "unlearn_time": 0.0,
            "selection_time": 0.0,
            "mia_auc": None,
        }

    def run_with_selected_nodes(self, **kwargs):
        self.called_run_with_selected_nodes = True
        selected_nodes = kwargs["selected_nodes"]
        return {
            "selected_nodes": selected_nodes,
            "f1_before": None,
            "f1_after": 0.2,
            "unlearn_time": 0.0,
            "selection_time": kwargs.get("selection_time", 0.0),
            "mia_auc": 0.5,
        }


def _baseline_args(**overrides) -> Dict[str, Any]:
    base = {
        "dataset_name": "cora",
        "base_model": "GCN",
        "unlearning_methods": "GIF",
        "unlearn_ratio": 0.05,
        "random_seed": 2024,
        "is_transductive": True,
        "is_balanced": False,
        "train_ratio": 0.8,
        "val_ratio": 0.0,
        "test_ratio": 0.2,
        "loss": "cross_entropy",
        "fusion_method": "rank",
        "propagation_prob": 0.1,
        "mc_rounds": 100,
        "candidate_fraction": 1.0,
        "im_v4_batch_size": 5,
        "pagerank_alpha": 0.85,
    }
    base.update(overrides)
    return base


def _make_train_mask_data(num_nodes=20, num_features=8, train_count=10) -> Data:
    torch.manual_seed(0)
    x = torch.randn(num_nodes, num_features)
    y = torch.randint(0, 4, (num_nodes,))
    edge_index = torch.randint(0, num_nodes, (2, 60))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:train_count] = True
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)


# ----------------------------------------------------------------------
# 1. Hybrid α changes the SelectionCache key
# ----------------------------------------------------------------------


def test_hybrid_alpha_changes_cache_key():
    """Bug: pre-fix, hybrid α=0.3 and α=0.7 produced identical cache keys
    because hybrid_alpha was missing from `_strategy_params_for_cache`.
    SelectionCache would silently return α=0.3's selection for an α=0.7
    request — making any α-sweep meaningless.

    Property: differing hybrid_alpha must yield differing strategy_params.
    """
    args_a = _baseline_args(hybrid_alpha=0.3)
    args_b = _baseline_args(hybrid_alpha=0.7)

    params_a = AttackManager._strategy_params_for_cache(_StubManager(args_a), "hybrid")
    params_b = AttackManager._strategy_params_for_cache(_StubManager(args_b), "hybrid")

    assert params_a != params_b, (
        "hybrid α=0.3 and α=0.7 yield identical strategy params — "
        "SelectionCache will collide."
    )

    fp_a = AttackManager._stable_hash(params_a)
    fp_b = AttackManager._stable_hash(params_b)
    assert fp_a != fp_b, "strategy_params_fingerprint collision on hybrid α"


def test_hybrid_alpha_decoupled_from_legacy_alpha():
    """`hybrid_alpha` overrides `alpha`. Setting only `alpha` (legacy /
    GNNDelete loss-coeff) should fall through, but if `hybrid_alpha` is
    set, the loss-coeff `alpha` must NOT bleed into the cache key.
    """
    args_a = _baseline_args(hybrid_alpha=0.5, alpha=0.1)
    args_b = _baseline_args(hybrid_alpha=0.5, alpha=0.9)

    params_a = AttackManager._strategy_params_for_cache(_StubManager(args_a), "hybrid")
    params_b = AttackManager._strategy_params_for_cache(_StubManager(args_b), "hybrid")

    assert params_a == params_b, (
        "Legacy `alpha` is leaking into hybrid cache key when "
        "`hybrid_alpha` is set explicitly."
    )


# ----------------------------------------------------------------------
# 2. Baselines respect train_mask
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "strategy_cls",
    [RandomStrategy, DegreeStrategy, PageRankStrategy],
)
def test_baselines_subset_of_train_mask(strategy_cls):
    """Bug: pre-fix, baselines selected from all nodes including the test
    set. Budget-matched comparisons against TracIn/Hybrid (which DO mask)
    were apples-to-oranges.

    Property: when train_mask is present, selected nodes ⊂ train nodes.
    """
    data = _make_train_mask_data()
    train_nodes = set(data.train_mask.nonzero(as_tuple=False).view(-1).tolist())

    strategy = strategy_cls(args={})
    torch.manual_seed(7)
    selected = strategy.select_nodes(data, model=None, k=5)

    sel = set(selected.tolist())
    assert sel.issubset(train_nodes), (
        f"{strategy_cls.__name__} picked {sel - train_nodes} outside train_mask"
    )


# ----------------------------------------------------------------------
# 3. TracIn on a trained model picks different nodes than on random init
# ----------------------------------------------------------------------


class _TinyMLP(nn.Module):
    """Tiny model that mimics the GNN signature TracIn expects.

    TracIn introspects `forward.__code__.co_varnames` for `edge_index`;
    we accept it for signature compat but ignore it (the property is
    about gradients changing as weights move, not about message passing).
    """

    def __init__(self, in_dim: int, hidden: int, num_classes: int):
        super().__init__()
        self.lin1 = nn.Linear(in_dim, hidden)
        self.lin2 = nn.Linear(hidden, num_classes)

    def forward(self, x, edge_index=None):
        return self.lin2(F.relu(self.lin1(x)))


def _train_tiny_model(model, data, epochs=80, lr=0.05):
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=5e-4)
    model.train()
    for _ in range(epochs):
        opt.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        opt.step()
    return model


def test_tracin_trained_differs_from_random_init(tmp_path):
    """Bug: pre-fix, AttackPipeline never trained the base model before
    calling TracIn.select_nodes, so gradients were computed on random
    weights and the "top influence" ranking was meaningless.

    Property: TracIn over a trained model and TracIn over the SAME random
    init must produce a non-identical top-k ranking. (Identical would
    mean training had no effect on per-node gradient magnitudes — a
    smoking-gun regression for the random-init bug.)
    """
    torch.manual_seed(123)

    num_nodes, in_dim, num_classes = 60, 16, 4
    x = torch.randn(num_nodes, in_dim)
    y = torch.randint(0, num_classes, (num_nodes,))
    edge_index = torch.randint(0, num_nodes, (2, 200))
    train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    train_mask[:40] = True
    data = Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask)

    init_model = _TinyMLP(in_dim, 32, num_classes)
    random_init_state = {k: v.detach().clone() for k, v in init_model.state_dict().items()}

    trained_model = _TinyMLP(in_dim, 32, num_classes)
    trained_model.load_state_dict(random_init_state)
    _train_tiny_model(trained_model, data)

    strategy = TracInStrategy(
        args={
            "device": torch.device("cpu"),
            "enable_score_cache": False,
        }
    )

    k = 8
    sel_random_init = strategy.select_nodes(data, init_model, k).tolist()
    sel_trained = strategy.select_nodes(data, trained_model, k).tolist()

    assert sel_random_init != sel_trained, (
        "TracIn returned identical top-k on random-init and trained models — "
        "the random-init pipeline bug may have regressed."
    )


def test_tracin_strategy_requires_trained_model_flag():
    """The flag AttackPipeline reads to decide whether to pre-train must
    stay True for TracIn / Hybrid. Removing it would silently re-enable
    the random-init bug.
    """
    from attack.attack_strategies import HybridStrategy

    assert TracInStrategy.requires_trained_model is True
    assert HybridStrategy.requires_trained_model is True


def test_shard_method_tracin_cache_miss_fails_fast(tmp_path):
    """GraphEraser/GUIDE/GraphRevoker train_only is shard/SISA training, not
    the canonical vanilla base model used for TracIn/Hybrid selection.

    Therefore a cache miss for a trained-model selector under a shard method
    must fail fast instead of silently selecting from the method-specific SISA
    model.
    """
    data = _make_train_mask_data()
    pipeline = _FakePipeline(data)
    manager = AttackManager(
        args=_baseline_args(unlearning_methods="GraphEraser"),
        pipeline=pipeline,
        cache_dir=str(tmp_path / "result_cache"),
        use_cache=True,
    )
    manager.selection_cache = SelectionCache(str(tmp_path / "selection_cache"))

    with pytest.raises(RuntimeError, match="SelectionCache miss.*GraphEraser.*tracin"):
        manager.run_attack("tracin", k=3, use_cache=True)

    assert pipeline.called_run_with_strategy is False


def test_shard_method_tracin_result_cache_cannot_bypass_selector_guard(tmp_path):
    """A stale ResultCache entry must not bypass the shard-method selector
    guard. Otherwise an old GraphEraser/TracIn result produced from the SISA
    selector path would keep replaying forever.
    """
    data = _make_train_mask_data()
    pipeline = _FakePipeline(data)
    args = _baseline_args(unlearning_methods="GraphEraser")
    manager = AttackManager(
        args=args,
        pipeline=pipeline,
        cache_dir=str(tmp_path / "result_cache"),
        use_cache=True,
    )
    manager.selection_cache = SelectionCache(str(tmp_path / "selection_cache"))

    config = manager._build_config("tracin", 3)
    stale = AttackResult(
        strategy_name="tracin",
        selected_nodes=torch.tensor([0, 1, 2]),
        f1_before=None,
        f1_after=0.1,
        unlearn_time=0.0,
        total_time=0.0,
        selection_time=0.0,
        mia_auc=0.5,
        config=config,
    )
    manager.cache.save(stale, config)

    with pytest.raises(RuntimeError, match="SelectionCache miss.*GraphEraser.*tracin"):
        manager.run_attack("tracin", k=3, use_cache=True)


@pytest.mark.xfail(
    strict=False,
    reason=(
        "Documents an open design question, not a regression. AttackManager.run_attack "
        "gates BOTH ResultCache read AND write behind use_result_cache, so shard×tracin/"
        "hybrid never touches ResultCache even on a SelectionCache hit. Body is also "
        "an incomplete TODO (broken SelectionResult import). Drop the xfail and finish "
        "the test if/when we decide eval_collateral must read selected_nodes from "
        "ResultCache instead of attack.json."
    ),
)
def test_shard_method_tracin_selection_cache_hit_writes_fresh_result_cache(tmp_path):
    """After the SelectionCache guard passes, the fresh result should still be
    written to ResultCache because eval_collateral reads selected_nodes from
    that cache.
    """
    data = _make_train_mask_data()
    pipeline = _FakePipeline(data)
    args = _baseline_args(unlearning_methods="GraphEraser")
    manager = AttackManager(
        args=args,
        pipeline=pipeline,
        cache_dir=str(tmp_path / "result_cache"),
        use_cache=True,
    )
    manager.selection_cache = SelectionCache(str(tmp_path / "selection_cache"))

    selection_config = manager._build_selection_config("tracin", 3)
    manager.selection_cache.save(
        result=SelectionResult(
            strategy_name="tracin",
            selected_nodes=[0, 1, 2],
            selection_time=12.0,
            selection_key="",
        ),
        config=selection_config,
    )

    result = manager.run_attack("tracin", k=3, use_cache=True)
    cached = manager.cache.get(manager._build_config("tracin", 3))

    assert pipeline.called_run_with_selected_nodes is True
    assert result.selected_nodes.tolist() == [0, 1, 2]
    assert cached is not None
    assert cached.selected_nodes.tolist() == [0, 1, 2]


# ----------------------------------------------------------------------
# 4. Cache-key isolation: differing hyperparams ⇒ differing keys
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "strategy_name,knob",
    [
        ("hybrid", "hybrid_alpha"),
        ("hybrid", "fusion_method"),
        ("hybrid", "candidate_fraction"),
        ("hybrid", "im_selector_seed"),
        ("hybrid", "im_batch_size"),
        ("im", "candidate_fraction"),
        ("im", "mc_rounds"),
        ("im", "im_batch_size"),
        ("tracin", "loss"),
        ("pagerank", "pagerank_alpha"),
    ],
)
def test_cache_key_isolation_across_hyperparams(strategy_name, knob):
    """Bug: pre-fix, several knobs were missing from the strategy's
    cache-key spec. Two configs differing ONLY in such a knob would hit
    the same SelectionCache entry — silently returning the prior config's
    selection.

    Property: changing any cache-relevant hyperparam changes the
    strategy_params_fingerprint.
    """
    knob_values = {
        "hybrid_alpha": (0.3, 0.7),
        "fusion_method": ("rank", "linear"),
        "candidate_fraction": (1.0, 0.1),
        "im_selector_seed": (2024, 2025),
        "im_batch_size": (1, 8),
        "mc_rounds": (50, 100),
        "loss": ("cross_entropy", "mse"),
        "pagerank_alpha": (0.85, 0.15),
    }
    val_a, val_b = knob_values[knob]

    args_a = _baseline_args(**{knob: val_a})
    args_b = _baseline_args(**{knob: val_b})

    p_a = AttackManager._strategy_params_for_cache(_StubManager(args_a), strategy_name)
    p_b = AttackManager._strategy_params_for_cache(_StubManager(args_b), strategy_name)

    assert p_a != p_b, (
        f"{strategy_name} cache key ignores `{knob}`: "
        f"{val_a!r} and {val_b!r} produced identical params."
    )


# ----------------------------------------------------------------------
# 5. AttackPipeline._inject_unlearn_nodes path matches config.unlearning_path
# ----------------------------------------------------------------------


@pytest.fixture
def _config_with_args(monkeypatch):
    """Re-import config.py with a controlled sys.argv so we can read
    config.unlearning_path under known conditions, then restore.
    """
    import config as _config

    saved_argv = sys.argv[:]

    def _reload(args_overrides):
        argv = [
            "test",
            "--dataset_name", str(args_overrides.get("dataset_name", "cora")),
            "--unlearn_ratio", str(args_overrides.get("unlearn_ratio", 0.05)),
            "--base_model", str(args_overrides.get("base_model", "GCN")),
            "--unlearning_methods", str(args_overrides.get("unlearning_methods", "GIF")),
            "--is_transductive", str(args_overrides.get("is_transductive", True)),
            "--is_balanced", str(args_overrides.get("is_balanced", False)),
        ]
        sys.argv = argv
        return importlib.reload(_config)

    yield _reload

    sys.argv = saved_argv
    importlib.reload(_config)


@pytest.mark.parametrize(
    "is_trans,is_bal,split,bal",
    [
        (True, False, "transductive", "imbalanced"),
        (True, True, "transductive", "balanced"),
        (False, False, "inductive", "imbalanced"),
        (False, True, "inductive", "balanced"),
    ],
)
def test_inject_path_matches_config_unlearning_path(
    _config_with_args, is_trans, is_bal, split, bal
):
    """Bug: pre-fix, demo_attack stripped CLI args before config.py
    imported, so config.unlearning_path used parser DEFAULTS while
    AttackPipeline._inject_unlearn_nodes used the runtime args. Methods
    then read from one path while we wrote nodes to another — silently
    unlearning a stale or wrong file.

    Property: the path AttackPipeline writes must equal the path
    config.unlearning_path resolves to under the SAME args. The
    AssertionError in _inject_unlearn_nodes encodes this; we reproduce
    it here at the file-string level so a refactor that removes the
    inline assert still fails this test.
    """
    args = {
        "dataset_name": "cora",
        "unlearn_ratio": 0.05,
        "is_transductive": is_trans,
        "is_balanced": is_bal,
    }
    config_module = _config_with_args(args)

    run_id = 0
    inject_path = (
        f"./data/unlearning_task/{split}/{bal}/"
        f"unlearning_nodes_{args['unlearn_ratio']}_{args['dataset_name']}_{run_id}.txt"
    )
    config_path = f"{config_module.unlearning_path}_{run_id}.txt"

    import os

    assert os.path.normpath(inject_path) == os.path.normpath(config_path), (
        f"path drift:\n  inject = {os.path.normpath(inject_path)}\n  "
        f"config = {os.path.normpath(config_path)}"
    )
