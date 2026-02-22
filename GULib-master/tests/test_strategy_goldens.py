"""Golden-fixture tests for attack strategy node selection semantics."""

import json
import random
from pathlib import Path
from typing import Optional

import numpy as np
import pytest
import torch
from torch_geometric.data import Data

import attack.attack_strategies.im_strategy as im_strategy_module
from attack.attack_manager import AttackManager
from attack.attack_strategies import (
    DegreeStrategy,
    HybridStrategy,
    IMStrategy,
    PageRankStrategy,
    RandomStrategy,
    TracInStrategy,
)
from attack.selection_cache import SelectionCache


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "strategies"


STRATEGY_MAP = {
    "random": RandomStrategy,
    "degree": DegreeStrategy,
    "pagerank": PageRankStrategy,
    "im": IMStrategy,
    "tracin": TracInStrategy,
    "hybrid": HybridStrategy,
}


@pytest.fixture(autouse=True)
def _pin_im_backend_to_python(monkeypatch):
    # Keep golden fixtures deterministic across environments with/without numba.
    monkeypatch.setattr(im_strategy_module, "HAS_NUMBA", False)


def _set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def _load_fixture(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _build_data(graph_payload: dict) -> Data:
    payload = dict(graph_payload)
    num_nodes = int(payload["num_nodes"])
    x = torch.tensor(payload["x"], dtype=torch.float)
    edge_index = torch.tensor(payload["edge_index"], dtype=torch.long)
    y = torch.tensor(payload["y"], dtype=torch.long)

    data_kwargs = {
        "num_nodes": num_nodes,
        "x": x,
        "edge_index": edge_index,
        "y": y,
    }
    if "train_mask" in payload:
        data_kwargs["train_mask"] = torch.tensor(payload["train_mask"], dtype=torch.bool)

    return Data(**data_kwargs)


class _LinearModel(torch.nn.Module):
    def __init__(self, in_features: int, out_features: int):
        super().__init__()
        self.lin = torch.nn.Linear(in_features, out_features)

    def forward(self, x, edge_index=None):
        return self.lin(x)


def _build_model(model_payload: Optional[dict]):
    if model_payload is None:
        return None

    model = _LinearModel(
        int(model_payload["in_features"]),
        int(model_payload["out_features"]),
    )
    with torch.no_grad():
        model.lin.weight.copy_(torch.tensor(model_payload["weight"], dtype=torch.float))
        model.lin.bias.copy_(torch.tensor(model_payload["bias"], dtype=torch.float))
    return model


def _run_fixture_strategy(spec: dict) -> torch.Tensor:
    strategy_name = spec["strategy"]
    strategy_cls = STRATEGY_MAP[strategy_name]
    strategy = strategy_cls(spec.get("args", {}))

    data = _build_data(spec["graph"])
    model = _build_model(spec.get("model"))

    seed = spec.get("seed")
    if seed is not None:
        _set_seed(int(seed))

    if "k" in spec:
        return strategy.select_nodes(data, model, int(spec["k"]))
    return strategy.select_nodes_by_ratio(data, model, float(spec["ratio"]))


def _fixture_paths():
    return sorted(FIXTURE_DIR.glob("*.json"))


@pytest.mark.parametrize("fixture_path", _fixture_paths(), ids=lambda p: p.stem)
def test_strategy_matches_golden_fixture(fixture_path):
    spec = _load_fixture(fixture_path)
    result = _run_fixture_strategy(spec)
    expected = torch.tensor(spec["expected_selected_nodes"], dtype=torch.long)

    assert result.dtype == torch.long
    assert result.tolist() == expected.tolist()
    assert len(result.unique()) == len(result)

    graph = spec["graph"]
    assert (result >= 0).all()
    assert (result < int(graph["num_nodes"])).all()

    if spec.get("assert_subset_of_train_mask"):
        train_mask = torch.tensor(graph["train_mask"], dtype=torch.bool)
        candidates = set(train_mask.nonzero(as_tuple=False).squeeze(-1).tolist())
        assert set(result.tolist()).issubset(candidates)


class _FakePipeline:
    def __init__(self, data: Data, model: Optional[torch.nn.Module]):
        self.data = data
        self.model = model

    def run_with_strategy(self, strategy, k: int):
        selected_nodes = strategy.select_nodes(self.data, self.model, k)
        return {
            "selected_nodes": selected_nodes,
            "f1_before": 0.91,
            "f1_after": 0.81,
            "unlearn_time": 0.05,
            "selection_time": 0.02,
            "mia_auc": 0.61,
        }

    def run_with_selected_nodes(self, strategy_name: str, selected_nodes: torch.Tensor, selection_time: float):
        return {
            "selected_nodes": selected_nodes,
            "f1_before": 0.91,
            "f1_after": 0.81,
            "unlearn_time": 0.05,
            "selection_time": selection_time,
            "mia_auc": 0.61,
        }


def _base_args():
    return {
        "dataset_name": "golden_graph",
        "base_model": "DummyLinear",
        "unlearning_methods": "DummyMethod",
        "unlearn_ratio": 0.2,
        "seed": 17,
        "random_seed": 17,
        "cuda": -1,
        "is_transductive": True,
        "is_balanced": False,
        "train_ratio": 0.8,
        "val_ratio": 0.0,
        "test_ratio": 0.2,
        "propagation_prob": 0.2,
        "mc_rounds": 30,
        "alpha": 0.6,
        "fusion_method": "rank",
        "device": "cpu",
    }


def _fixture_by_name(name: str) -> dict:
    return _load_fixture(FIXTURE_DIR / f"{name}.json")


def test_attack_manager_tracin_matches_direct_and_cache_roundtrip(tmp_path):
    spec = _fixture_by_name("tracin_masked_noncontiguous_k3")
    data = _build_data(spec["graph"])
    model = _build_model(spec["model"])
    k = int(spec["k"])

    manager = AttackManager(
        args=_base_args(),
        pipeline=_FakePipeline(data, model),
        cache_dir=str(tmp_path / "cache"),
        use_cache=True,
    )
    # Isolate this test from shared selection cache directory side effects.
    manager.selection_cache = None

    expected = manager.get_strategy("tracin").select_nodes(data, model, k).tolist()
    first = manager.run_attack("tracin", k=k, use_cache=True)
    second = manager.run_attack("tracin", k=k, use_cache=True)

    assert first.selected_nodes.tolist() == expected
    assert second.selected_nodes.tolist() == expected
    assert second.selected_nodes.tolist() == first.selected_nodes.tolist()

    train_mask = data.train_mask
    candidates = set(train_mask.nonzero(as_tuple=False).squeeze(-1).tolist())
    assert set(first.selected_nodes.tolist()).issubset(candidates)


def test_attack_manager_random_matches_direct_and_cache_roundtrip(tmp_path):
    spec = _fixture_by_name("random_basic_k3")
    data = _build_data(spec["graph"])
    k = int(spec["k"])
    seed = int(spec["seed"])

    manager = AttackManager(
        args=_base_args(),
        pipeline=_FakePipeline(data, model=None),
        cache_dir=str(tmp_path / "cache"),
        use_cache=True,
    )
    manager.selection_cache = None

    _set_seed(seed)
    expected = manager.get_strategy("random").select_nodes(data, None, k).tolist()

    _set_seed(seed)
    first = manager.run_attack("random", k=k, use_cache=True)
    second = manager.run_attack("random", k=k, use_cache=True)

    assert first.selected_nodes.tolist() == expected
    assert second.selected_nodes.tolist() == expected
    assert second.selected_nodes.tolist() == first.selected_nodes.tolist()


def test_attack_manager_im_reuses_larger_selection_cache_for_smaller_k(tmp_path):
    spec = _fixture_by_name("im_basic_k3")
    data = _build_data(spec["graph"])
    model = _build_model(spec.get("model"))
    large_k = int(spec["k"])
    small_k = large_k - 1

    manager = AttackManager(
        args=_base_args(),
        pipeline=_FakePipeline(data, model),
        cache_dir=str(tmp_path / "cache"),
        use_cache=True,
    )
    manager.selection_cache = SelectionCache(str(tmp_path / "selection_cache"))

    first = manager.run_attack("im", k=large_k, use_cache=True)
    second = manager.run_attack("im", k=small_k, use_cache=True)

    assert first.selection_cache_hit is False
    assert second.selection_cache_hit is True
    assert second.selected_nodes.tolist() == first.selected_nodes.tolist()[:small_k]
