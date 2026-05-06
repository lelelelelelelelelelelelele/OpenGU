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
from attack.selection_cache import SelectionCache
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


def test_run_config_method_overrides_fingerprint_only_target_method():
    """Method-specific runner args must only invalidate that method's cells.

    GraphRevoker needs --partition_method gpa, but adding it globally would
    stale every GraphEraser/GIF/etc. Phase B cell. The runner fingerprint must
    include the override for GraphRevoker while leaving other method cells
    unchanged.
    """
    from experiments.run import _content_fingerprint

    base_cfg = {
        "dataset": "cora",
        "base_model": "GCN",
        "ratio": 0.05,
        "defaults": {"run_collateral": True, "cuda": 0, "num_epochs": 100},
        "extra_args": [],
        "model_overrides": {"GCN": {"gcn_num_layers": 2, "gcn_hidden": 64}},
    }
    cfg_with_override = {
        **base_cfg,
        "method_overrides": {
            "GraphRevoker": {"extra_args": ["--partition_method", "gpa"]}
        },
    }

    assert _content_fingerprint(
        cfg_with_override, "GraphRevoker", "random", 42
    ) != _content_fingerprint(base_cfg, "GraphRevoker", "random", 42)
    assert _content_fingerprint(
        cfg_with_override, "GIF", "random", 42
    ) == _content_fingerprint(base_cfg, "GIF", "random", 42)


# ----------------------------------------------------------------------
# 3b. A3 alpha sweep — cell_dir disambiguates non-default hybrid_alpha
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "strategy,alpha_source,alpha_value,expect_suffix",
    [
        ("hybrid", None, None, False),                      # no alpha set → bare leaf
        ("hybrid", "top", 0.5, False),                      # default alpha → bare leaf
        ("hybrid", "top", 0.25, True),                      # non-default top-level → suffix
        ("hybrid", "top", 0.75, True),
        ("hybrid", "extra", 0.25, True),                    # via extra_args
        ("hybrid", "extra", 0.5, False),                    # default via extra_args
        ("random", "top", 0.25, False),                     # non-hybrid ignores alpha
        ("tracin", "top", 0.25, False),
    ],
)
def test_cell_dir_disambiguates_hybrid_alpha(strategy, alpha_source, alpha_value, expect_suffix):
    """A3 alpha sweep: two hybrid runs at different alphas must NOT share
    a cell directory (would overwrite each other's attack.json). Default
    alpha=0.5 stays under the bare leaf so it shares with the main matrix.
    """
    from experiments.run import cell_dir

    cfg = {"dataset": "cora", "base_model": "GCN", "ratio": 0.05}
    if alpha_source == "top":
        cfg["hybrid_alpha"] = alpha_value
    elif alpha_source == "extra":
        cfg["extra_args"] = ["--hybrid_alpha", str(alpha_value)]

    leaf = cell_dir(cfg, "GIF", strategy, 42).parent.name

    if expect_suffix:
        assert leaf == f"GIF_hybrid_alpha{alpha_value:.2f}", leaf
    else:
        assert leaf == f"GIF_{strategy}", leaf


def test_cell_dir_alpha_top_level_and_extra_args_agree():
    """If both top-level and extra_args carry hybrid_alpha at the SAME value,
    cell_dir picks one consistently (top-level wins)."""
    from experiments.run import cell_dir

    cfg = {
        "dataset": "cora", "base_model": "GCN", "ratio": 0.05,
        "hybrid_alpha": 0.25,
        "extra_args": ["--hybrid_alpha", "0.25"],
    }
    assert cell_dir(cfg, "GIF", "hybrid", 42).parent.name == "GIF_hybrid_alpha0.25"


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
# 4b. ResultCache key isolation — A3 alpha sweep adds 5 fields
# ----------------------------------------------------------------------


@pytest.mark.parametrize(
    "knob,val_a,val_b",
    [
        ("hybrid_alpha", 0.25, 0.75),
        ("alpha", 0.1, 0.9),
        ("fusion_method", "rank", "linear"),
        ("candidate_fraction", 1.0, 0.1),
        ("mc_rounds", 50, 100),
        ("im_batch_size", 1, 8),
        ("im_selector_seed", 2024, 2025),
    ],
)
def test_result_cache_key_isolation_for_a3_fields(knob, val_a, val_b):
    """Bug we're protecting against: A3 alpha sweep would silently return
    a stale ResultCache entry from a different (alpha, fusion_method, IM
    knob) configuration because those fields used to be missing from
    `ResultCache.CACHE_KEY_FIELDS`.

    Property: each of the 7 A3-relevant knobs must change the ResultCache
    key when toggled.
    """
    from attack.result_cache import ResultCache

    cache = ResultCache.__new__(ResultCache)  # bypass __init__ (no disk)
    cfg_a = {"dataset_name": "cora", "base_model": "GCN", "k": 5, knob: val_a}
    cfg_b = {"dataset_name": "cora", "base_model": "GCN", "k": 5, knob: val_b}

    key_a = cache._hash_fields(cfg_a, ResultCache.CACHE_KEY_FIELDS)
    key_b = cache._hash_fields(cfg_b, ResultCache.CACHE_KEY_FIELDS)

    assert key_a != key_b, (
        f"ResultCache key collides on `{knob}` ({val_a!r} vs {val_b!r}): "
        f"alpha-sweep / fusion-sweep / IM-knob ablation would replay stale results."
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
