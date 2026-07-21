import hashlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch

from experiments.bc_target_v2.core import (
    checkpoint_view_indices,
    deterministic_random_scores,
    hutchinson_parameter_change_scores,
    remove_selected_nodes,
    weighted_checkpoint_scores,
)
from experiments.bc_target_v2.benchmark_selection import (
    CUBLAS_WORKSPACE_CONFIG,
    _build_cell_record,
    _command,
    _run,
    build_parser as build_benchmark_parser,
)
from experiments.bc_target_v2.recipe import SCORE_NAMES, build_recipe
from experiments.bc_target_v2.dataset_source import (
    DatasetSourceError,
    canonical_data_root,
    resolve_planetoid_public_source,
    validate_public_split,
)
from experiments.bc_target_v2.render_markdown import render_document
from experiments.bc_target_v2.run_downstream import build_parser as build_downstream_parser
from experiments.bc_target_v2.run_matrix import build_parser as build_matrix_parser
from experiments.bc_target_v2.run_selection import build_parser as build_selection_parser
from experiments.bc_target_v2.run_selection import _resolve_device
from experiments.bc_target_v2.syncmate_recipe import (
    cell_artifact_paths,
    load_recipe_config,
    preflight_recipe,
)


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _write_planetoid_source(repository_root, dataset="Cora"):
    root = canonical_data_root(repository_root)
    storage = dataset.lower()
    raw = root / storage / "raw"
    processed = root / storage / "processed"
    raw.mkdir(parents=True)
    processed.mkdir(parents=True)
    for suffix in ("x", "tx", "allx", "y", "ty", "ally", "graph", "test.index"):
        (raw / "ind.{0}.{1}".format(storage, suffix)).write_bytes(
            (dataset + suffix).encode("utf-8")
        )
    (processed / "data.pt").write_bytes(b"processed")
    return root


def test_checkpoint_views_and_weighted_scores():
    views = checkpoint_view_indices(6)
    assert views["single"] == (5,)
    assert views["cp3"] == (0, 3, 5)
    assert views["cp_all"] == (0, 1, 2, 3, 4, 5)
    vectors = [torch.tensor([float(index), 1.0]) for index in range(6)]
    weights = [1.0] * 6
    assert weighted_checkpoint_scores(
        vectors, weights, views["cp3"]
    ).tolist() == [8.0, 3.0]


def test_hutchinson_projection_and_random_scores_are_deterministic():
    candidates = torch.tensor([[1.0, 0.0], [0.0, 2.0]])
    inverse_probes = torch.tensor([[1.0, 1.0], [1.0, -1.0]])
    scores = hutchinson_parameter_change_scores(
        candidates, inverse_probes
    )
    assert scores.tolist() == pytest.approx([1.0, 2.0])
    assert torch.equal(
        deterministic_random_scores(5, 42),
        deterministic_random_scores(5, 42),
    )
    assert not torch.equal(
        deterministic_random_scores(5, 42),
        deterministic_random_scores(5, 43),
    )


def test_remove_selected_nodes_updates_mask_and_incident_edges():
    edge_index = torch.tensor(
        [[0, 1, 1, 2, 2, 3], [1, 0, 2, 1, 3, 2]], dtype=torch.long
    )
    train_mask = torch.tensor([True, True, True, False])
    clean_edges, clean_mask = remove_selected_nodes(
        edge_index, train_mask, [1]
    )
    assert clean_mask.tolist() == [True, False, True, False]
    assert clean_edges.tolist() == [[2, 3], [3, 2]]


def test_bc_recipe_contains_complete_score_family():
    recipe = build_recipe(
        source_fingerprint=_sha("source"),
        data_identity={
            "dataset": "Cora",
            "edge_index_hash": _sha("edges"),
            "features_hash": _sha("features"),
            "labels_hash": _sha("labels"),
            "split_hash": _sha("split"),
        },
        candidate_ids_hash=_sha("candidates"),
        target_ids_hash=_sha("targets"),
        selector_model={
            "final_state_hash": _sha("state"),
            "parameter_schema_hash": _sha("parameters"),
        },
        training={"epochs": 200, "optimizer": "ADAM"},
        checkpoints=(
            {"global_step": 1, "state_hash": _sha("s1"), "weight": 0.01},
            {"global_step": 50, "state_hash": _sha("s50"), "weight": 0.01},
            {"global_step": 200, "state_hash": _sha("s200"), "weight": 0.0025},
        ),
        checkpoint_views={
            "single": (2,),
            "cp3": (0, 1, 2),
            "cp_all": (0, 1, 2),
        },
        graph_intervention={
            "operation": "remove_candidate_incident_edges",
            "per_candidate_exact_retrain": False,
        },
        hessian={"method": "LiSSA", "hutch_probes": 32},
        loss={"type": "cross_entropy", "target_set": "validation_mask"},
        parameter_scope="all_trainable",
        seed_bundle={"python_numpy_torch": 2024},
        numerics={"torch_dtype": "torch.float32"},
    )
    assert tuple(recipe.fields["score_names"]) == SCORE_NAMES
    assert len(SCORE_NAMES) == 17
    assert "b_param_lissa" not in SCORE_NAMES
    assert recipe.fields["candidate_set"]["ranking_reusable_across_budgets"]


def test_markdown_renderer_keeps_tables_and_heading_anchors(tmp_path):
    source = tmp_path / "report.md"
    output = tmp_path / "report.html"
    source.write_text(
        "---\ntitle: smoke\n---\n# Report\n## Main result\n"
        "| Method | Score |\n|---|---:|\n| GIF | 0.9 |\n",
        encoding="utf-8",
    )
    render_document(
        source,
        output,
        "Report",
        "ACCEPTED",
        "LOCAL TEST",
    )
    rendered = output.read_text(encoding="utf-8")
    assert 'id="main-result"' in rendered
    assert "<table>" in rendered
    assert "GIF" in rendered
    assert "title: smoke" not in rendered


def test_budget_cli_normalizes_duplicates_and_order():
    value = "14,3,7,3"
    assert build_selection_parser().parse_args(["--budgets", value]).budgets == (
        14,
        7,
        3,
    )
    assert build_downstream_parser().parse_args(
        ["--selection-summary", "selection.json", "--budgets", value]
    ).budgets == (14, 7, 3)
    assert build_matrix_parser().parse_args(["--budgets", value]).budgets == (
        14,
        7,
        3,
    )


def test_default_budget_order_is_max_first():
    assert build_selection_parser().parse_args([]).budgets == (14, 7, 3)
    assert build_matrix_parser().parse_args([]).budgets == (14, 7, 3)


def test_benchmark_requires_explicit_experiment_git_sha():
    parser = build_benchmark_parser()
    args = parser.parse_args(["--experiment-git-sha", "a" * 40])
    assert args.experiment_git_sha == "a" * 40
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_planetoid_source_is_repo_relative_fingerprinted_and_fail_closed(tmp_path):
    repository_root = tmp_path / "repo"
    root = _write_planetoid_source(repository_root)
    source = resolve_planetoid_public_source(
        root, repository_root=repository_root, dataset="Cora"
    )
    manifest = source.to_manifest()
    assert manifest["canonical_root_match"] is True
    assert manifest["resolved_root"] == str(root.resolve())
    assert Path(manifest["dataset_dir"]).parts[-3:] == ("data", "raw", "cora")
    assert len(manifest["raw_files"]) == 8
    assert len(manifest["source_fingerprint"]) == 64
    assert manifest["automatic_download_allowed"] is False
    assert manifest["runtime_processing_allowed"] is False

    external_root = _write_planetoid_source(tmp_path / "external-repo")
    with pytest.raises(DatasetSourceError, match="non-canonical"):
        resolve_planetoid_public_source(
            external_root, repository_root=repository_root, dataset="Cora"
        )


def test_planetoid_source_requires_existing_processed_cache(tmp_path):
    repository_root = tmp_path / "repo"
    root = _write_planetoid_source(repository_root)
    (root / "cora" / "processed" / "data.pt").unlink()
    with pytest.raises(DatasetSourceError, match="processed/data.pt"):
        resolve_planetoid_public_source(
            root, repository_root=repository_root, dataset="Cora"
        )


def test_public_split_validator_rejects_opengu_80_20_split():
    public = SimpleNamespace(
        num_nodes=2708,
        edge_index=torch.empty((2, 10556), dtype=torch.long),
        train_mask=torch.cat((torch.ones(140), torch.zeros(2568))),
        val_mask=torch.cat((torch.ones(500), torch.zeros(2208))),
        test_mask=torch.cat((torch.ones(1000), torch.zeros(1708))),
    )
    assert validate_public_split(public, "Cora")["train_count"] == 140
    public.train_mask = torch.cat((torch.ones(2166), torch.zeros(542)))
    public.val_mask = torch.zeros(2708)
    public.test_mask = torch.cat((torch.ones(542), torch.zeros(2166)))
    with pytest.raises(DatasetSourceError, match="frozen public split"):
        validate_public_split(public, "Cora")


def test_selection_device_defaults_to_auto():
    parser = build_selection_parser()
    assert parser.parse_args([]).device == "auto"
    assert parser.parse_args(["--device", "cpu"]).device == "cpu"


def test_cuda_device_resolution_has_an_explicit_index(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "current_device", lambda: 0)
    assert str(_resolve_device("cuda")) == "cuda:0"


def test_benchmark_cell_requires_17_cold_misses_and_warm_hits(tmp_path):
    dataset_source = {
        "schema": "bc_target_v2.planetoid_public_source",
        "version": 1,
        "profile": "planetoid_public_fixed_split",
        "dataset": "Cora",
        "storage_name": "cora",
        "split_policy": "public",
        "resolved_root": "/repo/data/raw",
        "resolved_dataset_dir": "/repo/data/raw/cora",
        "raw_dir": "/repo/data/raw/cora/raw",
        "processed_data_path": "/repo/data/raw/cora/processed/data.pt",
        "source_fingerprint": _sha("dataset-source"),
    }

    def summary(hit):
        return {
            "dataset_source": dataset_source,
            "split_observation": {"train_count": 140},
            "git_provenance": {"head": "a" * 40},
            "cache": {"hit": hit, "artifact_id": "score_fixture"},
            "selection_cache": {
                "miss_saved_count": 0 if hit else 17,
                "hit_count": 17 if hit else 0,
                "method_timings": {
                    name: {
                        "seconds": 0.001,
                        "cache_hit": hit,
                    }
                    for name in SCORE_NAMES
                },
            },
            "runtime": {
                "score_bundle_cold_total_seconds": None if hit else 2.0,
                "score_bundle_warm_read_seconds": 0.01 if hit else None,
                "total_seconds": 3.0,
            },
            "gpu_memory": {
                "process_peak_allocated_bytes": 1024 if not hit else 512,
                "process_peak_reserved_bytes": 2048 if not hit else 1024,
            },
            "environment": {"device": "cuda"},
        }

    record = _build_cell_record(
        dataset="Cora",
        seed=42,
        cold_path=tmp_path / "cold.json",
        warm_path=tmp_path / "warm.json",
        cold=summary(False),
        warm=summary(True),
    )
    assert record["status"] == "success"
    assert len(record["methods"]) == 17
    assert record["score_bundle_cold_total_seconds"] == 2.0
    assert record["score_bundle_warm_read_seconds"] == 0.01


def test_benchmark_warm_command_enables_producer_sentinel(tmp_path):
    command = _command(
        dataset="Cora",
        seed=42,
        data_root=tmp_path / "data",
        cache_root=tmp_path / "cache",
        output=tmp_path / "warm.json",
        budgets="14,7,3",
        device="cpu",
        experiment_git_sha="a" * 40,
        warm=True,
    )
    assert "--fail-if-producer-called" in command
    assert command[0] == sys.executable


def test_benchmark_subprocess_sets_deterministic_cublas_workspace(monkeypatch):
    observed = {}

    class Completed:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(command, **kwargs):
        observed.update(kwargs["env"])
        return Completed()

    monkeypatch.setattr("experiments.bc_target_v2.benchmark_selection.subprocess.run", fake_run)
    result = _run((sys.executable, "-c", "pass"), 1.0)
    assert result["returncode"] == 0
    assert observed["CUBLAS_WORKSPACE_CONFIG"] == CUBLAS_WORKSPACE_CONFIG


def test_syncmate_small_selection_configs_are_three_bounded_stages():
    root = Path(__file__).resolve().parents[1]
    config_dir = root / "experiments" / "configs"
    mvp = load_recipe_config(
        config_dir / "syncmate_small_selection_mvp_v1.yaml",
        repository_root=root,
    )
    dataset_gate = load_recipe_config(
        config_dir / "syncmate_small_selection_dataset_gate_v1.yaml",
        repository_root=root,
    )
    full = load_recipe_config(
        config_dir / "syncmate_small_selection_full_v1.yaml",
        repository_root=root,
    )

    assert (mvp["datasets"], mvp["seeds"], mvp["resume"]) == (("Cora",), (42,), False)
    assert dataset_gate["datasets"] == ("Cora", "CiteSeer", "PubMed")
    assert dataset_gate["seeds"] == (42,)
    assert dataset_gate["required_prior_cells"] == ("cora_seed42",)
    assert full["seeds"] == (42, 212, 2024)
    assert full["required_prior_cells"] == (
        "cora_seed42",
        "citeseer_seed42",
        "pubmed_seed42",
    )
    assert len(cell_artifact_paths(mvp)) == 3
    assert len(cell_artifact_paths(dataset_gate)) == 9
    assert len(cell_artifact_paths(full)) == 27


def test_syncmate_small_selection_preflight_blocks_non_4090(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    config = root / "experiments" / "configs" / "syncmate_small_selection_mvp_v1.yaml"
    monkeypatch.setattr(
        "experiments.bc_target_v2.syncmate_recipe._git_state",
        lambda _root: {"head": "a" * 40, "branch": "test", "status_short": []},
    )
    monkeypatch.setattr(
        "experiments.bc_target_v2.syncmate_recipe.resolve_planetoid_public_source",
        lambda *_args, **_kwargs: SimpleNamespace(to_manifest=lambda: {"canonical_root_match": True}),
    )
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(torch.cuda, "device_count", lambda: 1)
    monkeypatch.setattr(torch.cuda, "current_device", lambda: 0)
    monkeypatch.setattr(torch.cuda, "get_device_name", lambda _index: "NVIDIA GeForce RTX 5070")

    result = preflight_recipe(config)

    assert result["ready"] is False
    assert any("required device" in error for error in result["errors"])
