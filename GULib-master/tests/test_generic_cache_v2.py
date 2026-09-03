"""Real generic consumer execution, using disposable CPU graph/model inputs."""
import copy
import logging
import os
from pathlib import Path
import runpy
import sys

import numpy as np
import pytest
import torch
from torch_geometric.data import Data

from attack.attack_manager import AttackManager
from attack.pipeline_adapter import AttackPipeline
from attack.attack_strategies.tracin_strategy import TracInStrategy
from attack.attack_strategies.im_strategy import IMStrategy
from cache_v2 import CacheIndex
from cache_v2.store import ArtifactIntegrityError


class CpuModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = torch.nn.Linear(3, 2)

    def forward(self, x, edge_index=None):
        return self.linear(x)


class CpuPipeline(AttackPipeline):
    """Use production pipeline orchestration with a tiny retraining method.

    Only data/model provisioning and method-side deletion are injected. The
    public pipeline selection/unlearning methods execute unchanged on CPU.
    This is integration evidence, never a formal research experiment.
    """
    calls = 0

    def __init__(self, args):
        self.args = args
        torch.manual_seed(42)
        self.model = CpuModel()
        self.data = Data(x=torch.randn(8, 3), y=torch.arange(8) % 2,
            edge_index=torch.tensor([[0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
                                     [1, 0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5]]),
            train_mask=torch.tensor([1, 1, 1, 1, 1, 1, 0, 0], dtype=torch.bool),
            val_mask=torch.tensor([0, 0, 0, 0, 0, 0, 1, 0], dtype=torch.bool),
            test_mask=torch.tensor([0, 0, 0, 0, 0, 0, 0, 1], dtype=torch.bool))
        self.logger = logging.getLogger("aagu025-cpu")
        self.initial = copy.deepcopy(self.model.state_dict())
        self.manager = self

    def get_method(self):
        return self

    def _inject_unlearn_nodes(self, nodes, run_id):
        self.deleted = nodes

    def _restore_random_init(self):
        self.model.load_state_dict(self.initial)

    def _ensure_base_model_trained(self):
        self._train(self.data.train_mask)

    def _train(self, mask):
        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.1)
        for _ in range(2):
            optimizer.zero_grad()
            loss = torch.nn.functional.cross_entropy(self.model(self.data.x)[mask], self.data.y[mask])
            loss.backward()
            optimizer.step()

    def run_exp(self):
        type(self).calls += 1
        self._train(self.data.train_mask)
        before = self._evaluate_model()
        keep = self.data.train_mask.clone()
        keep[self.deleted] = False
        self._restore_random_init()
        self._train(keep)
        self.poison_f1 = [before]
        self.average_f1 = [self._evaluate_model()]
        self.average_auc = [None]
        self.avg_unlearning_time = [0.01]

    def _evaluate_model(self):
        return float((self.model(self.data.x).argmax(1) == self.data.y).float().mean())


def manager(root, *, enabled=True, **overrides):
    args = dict(dataset_name="cora", base_model="GCN", unlearning_methods="GIF",
                random_seed=42, seed=42, mc_rounds=3, im_parallel_mc=False,
                cache_v2_store_root=str(root), device=torch.device("cpu"))
    args.update(overrides)
    return AttackManager(args, CpuPipeline(args), use_cache=enabled)


@pytest.fixture
def deny_legacy_access(tmp_path, monkeypatch):
    """Audit actual file access/mkdir calls, including reads, not just references."""
    monkeypatch.chdir(tmp_path)
    denied = [(tmp_path / "results" / name).resolve()
              for name in ("cache", "selection_cache", "score_cache")]
    state = {"active": True, "violations": []}

    def audit(event, args):
        if not state["active"] or event not in ("open", "os.mkdir", "os.listdir", "os.scandir", "os.remove", "os.rename"):
            return
        if not args or not isinstance(args[0], (str, bytes, os.PathLike)):
            return
        path = Path(os.fsdecode(args[0])).absolute()
        for root in denied:
            if path == root or root in path.parents:
                state["violations"].append((event, str(path)))
                raise AssertionError("Legacy cache access: " + str(path))

    sys.addaudithook(audit)
    yield state
    state["active"] = False
    assert state["violations"] == []
    assert all(not root.exists() for root in denied)


def test_default_real_entry_cold_hot_and_shared_store(tmp_path, deny_legacy_access, record_property):
    # No cache flag/root override: prove the actual default relative root.
    from attack import cache_identity
    previous = cache_identity.DEFAULT_STORE_ROOT
    cache_identity.DEFAULT_STORE_ROOT = "./results/cache_v2"
    try:
        args = dict(dataset_name="cora", base_model="GCN", unlearning_methods="GIF")
        first = AttackManager(args, CpuPipeline(args))
        assert first.get_strategy("im")._score_cache is not None
        assert first.get_strategy("tracin")._score_cache is not None
        start = CpuPipeline.calls
        cold = first.run_attack("degree", 2)
        assert cold.result_cache_hit is False
        assert cold.selection_cache_hit is False
        second = AttackManager(args, CpuPipeline(args))
        warm = second.run_attack("degree", 2)
        assert warm.result_cache_hit is True
        assert warm.result_cache_key == cold.result_cache_key
        assert warm.selection_artifact_id == cold.selection_artifact_id
        assert CpuPipeline.calls == start + 1
        assert second.cache.root == second.selection_cache.root == second.get_strategy("im")._score_cache.root
        assert second.cache.root == (tmp_path / "results/cache_v2").resolve()
        record_property("cold_selection_artifact", cold.selection_artifact_id)
        record_property("cold_result_artifact", cold.result_artifact_id)
        record_property("warm_result_artifact", warm.result_artifact_id)
        record_property("result_recipe_hash", warm.result_recipe_hash)
        record_property("result_content_hash", warm.result_content_hash)
        record_property("compute_calls_cold_plus_hot", CpuPipeline.calls - start)
        record_property("legacy_access_violations", len(deny_legacy_access["violations"]))
    finally:
        cache_identity.DEFAULT_STORE_ROOT = previous


def test_selection_hit_with_distinct_target_evaluation(tmp_path):
    root = tmp_path / "v2"
    cold = manager(root).run_attack("degree", 2)
    warm_selection = manager(root, num_epochs=7).run_attack("degree", 2)
    assert warm_selection.selection_cache_hit is True
    assert warm_selection.result_cache_hit is False
    assert warm_selection.selection_artifact_id == cold.selection_artifact_id
    assert warm_selection.result_cache_key != cold.result_cache_key


def test_shard_consumer_reuses_canonical_trained_selection(tmp_path):
    root = tmp_path / "v2"
    canonical = manager(root).run_attack("tracin", 2)
    shard = manager(root, unlearning_methods="GraphEraser").run_attack("tracin", 2)
    assert shard.selection_cache_hit is True
    assert shard.selection_artifact_id == canonical.selection_artifact_id
    assert shard.result_cache_hit is False


def test_collateral_consumer_exact_read_only_selection(tmp_path):
    from eval_collateral import load_generic_selection
    m = manager(tmp_path / "v2")
    assert load_generic_selection(m, "degree", 2)[0] is None
    result = m.run_attack("degree", 2)
    before = {p: p.read_bytes() for p in (tmp_path / "v2").rglob("*") if p.is_file()}
    selection, provenance = load_generic_selection(m, "degree", 2)
    assert selection.artifact_id == result.selection_artifact_id
    assert provenance["authoritative"] is True
    assert {p: p.read_bytes() for p in before} == before
    m.data.x[0, 0] += 1
    assert load_generic_selection(m, "degree", 2)[0] is None


@pytest.mark.parametrize("change", ["features", "labels", "graph", "candidates", "split", "model", "seed"])
def test_identity_changes_reject_old_result(tmp_path, change, record_property):
    root = tmp_path / "v2"
    first = manager(root)
    cold = first.run_attack("degree", 2)
    next_manager = manager(root, seed=43, random_seed=43) if change == "seed" else manager(root)
    if change == "features":
        next_manager.data.x[0, 0] += 1
    elif change == "labels":
        next_manager.data.y[0] = 1 - next_manager.data.y[0]
    elif change == "graph":
        next_manager.data.edge_index[0, 0] = 4
    elif change == "candidates":
        next_manager.data.train_mask[0] = False
    elif change == "split":
        next_manager.data.val_mask, next_manager.data.test_mask = next_manager.data.test_mask, next_manager.data.val_mask
    elif change == "model":
        args = next_manager.args
        pipeline = CpuPipeline(args)
        with torch.no_grad():
            pipeline.model.linear.weight.add_(1)
        next_manager = AttackManager(args, pipeline)
    changed = next_manager.run_attack("degree", 2)
    assert changed.result_cache_hit is False
    assert changed.result_cache_key != cold.result_cache_key
    record_property("old_artifact", cold.result_cache_key)
    record_property("new_artifact", changed.result_cache_key)


@pytest.mark.parametrize("global_cache,score_cache", [(False, True), (False, False), (True, False), (True, True)])
def test_switch_semantics_all_consumers(tmp_path, global_cache, score_cache, record_property):
    root = tmp_path / "v2"
    m = manager(root, enabled=global_cache, enable_score_cache=score_cache)
    m.run_attack("hybrid", 2)
    record_property("global_cache", global_cache)
    record_property("score_cache", score_cache)
    if not global_cache:
        assert not root.exists()
        return
    assert list((root / "evaluation").rglob("payload.json")) or (root / "index.sqlite").exists()
    index = CacheIndex(root / "index.sqlite")
    import sqlite3
    with sqlite3.connect(str(index.database_path)) as conn:
        types = {row[0] for row in conn.execute("select artifact_type from artifacts")}
    assert "selection" in types and "evaluation" in types
    assert ("score" in types) == score_cache
    record_property("artifact_types", ",".join(sorted(types)))


def test_per_call_cache_override(tmp_path):
    root = tmp_path / "v2"
    m = manager(root)
    m.run_attack("im", 2, use_cache=False)
    assert not root.exists()
    m.run_attack("im", 2, use_cache=True)
    assert (root / "index.sqlite").is_file()


def test_tracin_exact_weight_and_data_identity(tmp_path):
    m = manager(tmp_path / "v2")
    strategy = m.get_strategy("tracin")
    nodes = torch.arange(6)
    before = strategy.compute_scores(m.model, m.data, nodes)
    original = strategy._compute_tracin_scores
    strategy._compute_tracin_scores = lambda *a: pytest.fail("warm Score called producer")
    torch.testing.assert_close(before, strategy.compute_scores(m.model, m.data, nodes))
    with torch.no_grad():
        m.model.linear.weight[0, 0] += 0.01
    identity = strategy._build_cache_config(m.model, m.data, nodes)
    assert strategy._score_cache.get(identity)[0] is None
    strategy._compute_tracin_scores = original
    strategy.compute_scores(m.model, m.data, nodes)
    m.data.x[0, 0] += 1
    assert strategy._score_cache.get(strategy._build_cache_config(m.model, m.data, nodes))[0] is None


def test_corrupt_artifact_fails_before_producer(tmp_path):
    m = manager(tmp_path / "v2")
    cold = m.run_attack("degree", 2)
    Path(cold.selection_cache_source).write_bytes(b"corrupt disposable fixture")
    calls = CpuPipeline.calls
    with pytest.raises(ArtifactIntegrityError):
        manager(tmp_path / "v2").run_attack("degree", 2)
    assert CpuPipeline.calls == calls


def test_real_demo_cli_cold_hot(tmp_path, monkeypatch, deny_legacy_access):
    import attack.attack_manager as module
    monkeypatch.setenv("OPENGU_AUTOREPORT_EVENT_PATH", str(tmp_path / "events.jsonl"))
    monkeypatch.setenv("OPENGU_AUTOREPORT_STATUS_MD_PATH", str(tmp_path / "status.md"))
    monkeypatch.setenv("OPENGU_AUTOREPORT_STATUS_HTML_PATH", str(tmp_path / "status.html"))
    monkeypatch.setattr(module, "AttackPipeline", CpuPipeline)
    script = Path(module.__file__).resolve().parents[1] / "demo_attack.py"
    for name in ("cold", "hot"):
        monkeypatch.setattr(sys, "argv", [str(script), "--strategies", "degree", "--k", "2",
            "--base_model", "GCN", "--unlearning_methods", "GIF", "--cuda", "-1",
            "--cache_v2_store_root", str(tmp_path / "v2"), "--save_path", str(tmp_path / (name + ".json"))])
        runpy.run_path(str(script), run_name="__main__")
    import json
    cold = json.loads((tmp_path / "cold.json").read_text())["results"]["degree"]
    hot = json.loads((tmp_path / "hot.json").read_text())["results"]["degree"]
    assert cold["result_cache_hit"] is False and hot["result_cache_hit"] is True
    assert cold["result_cache_key"] == hot["result_cache_key"]
    events = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text().splitlines()]
    selection_event = next(event for event in events if event["stage"] == "selection")
    assert selection_event["cache"][0]["outcome"] == "miss"
    result_observations = [observation for event in events for observation in event["cache"]
                           if observation["type"] == "result"]
    assert {o["outcome"] for o in result_observations} == {"hit", "miss"}
    assert all(o["authoritative"] for o in result_observations)


def test_formal_artifact_consumer_runs_real_pipeline(tmp_path):
    from cache_v2.runtime import load_selection_artifact
    root = tmp_path / "v2"
    source = manager(root).run_attack("degree", 2)
    target = manager(root)
    loaded = load_selection_artifact(root, source.selection_artifact_id,
        num_nodes=8, candidate_nodes=list(range(6)), expected_selector="degree", expected_k=2)
    before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    result = target.run_attack_with_selected_nodes("degree", loaded.selected_nodes,
        selection_provenance=loaded.provenance(root))
    assert result.selection_artifact_id == source.selection_artifact_id
    assert result.selection_authoritative is True
    assert {p: p.read_bytes() for p in root.rglob("*") if p.is_file()} == before


def test_changed_score_content_is_quarantined_not_overwritten(tmp_path):
    from cache_v2.store import ArtifactConflictError
    m = manager(tmp_path / "v2")
    strategy = m.get_strategy("im")
    nodes = list(range(6))
    scores = strategy.compute_initial_marginal_gains(m.data.edge_index, 8, nodes)
    identity = strategy._build_cache_config(m.data.edge_index, 8, nodes)
    cached = strategy._score_cache.get(identity)[0]
    original = Path(cached.source).read_bytes()
    with pytest.raises(ArtifactConflictError):
        strategy._score_cache.save(np.asarray(nodes), scores.numpy() + 1, identity)
    assert Path(cached.source).read_bytes() == original


def test_random_production_is_independent_of_prior_rng_and_cache(tmp_path):
    first = manager(tmp_path / "first")
    first_nodes, _ = first.produce_selection("random", 2)
    torch.rand(100)
    second = manager(tmp_path / "second")
    torch.rand(11)
    second_nodes, _ = second.produce_selection("random", 2)
    assert torch.equal(first_nodes, second_nodes)
    bypass = manager(tmp_path / "none", enabled=False).run_attack("random", 2)
    cold = manager(tmp_path / "v2").run_attack("random", 2)
    warm = manager(tmp_path / "v2").run_attack("random", 2)
    assert torch.equal(bypass.selected_nodes, cold.selected_nodes)
    assert torch.equal(cold.selected_nodes, warm.selected_nodes)
    assert bypass.f1_after == cold.f1_after == warm.f1_after
