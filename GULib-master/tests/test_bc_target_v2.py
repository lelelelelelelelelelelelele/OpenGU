import hashlib
import sys

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
    _build_cell_record,
    _command,
)
from experiments.bc_target_v2.recipe import SCORE_NAMES, build_recipe
from experiments.bc_target_v2.render_markdown import render_document
from experiments.bc_target_v2.run_downstream import build_parser as build_downstream_parser
from experiments.bc_target_v2.run_matrix import build_parser as build_matrix_parser
from experiments.bc_target_v2.run_selection import build_parser as build_selection_parser


def _sha(label):
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


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


def test_selection_device_defaults_to_auto():
    parser = build_selection_parser()
    assert parser.parse_args([]).device == "auto"
    assert parser.parse_args(["--device", "cpu"]).device == "cpu"


def test_benchmark_cell_requires_17_cold_misses_and_warm_hits(tmp_path):
    def summary(hit):
        return {
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
        warm=True,
    )
    assert "--fail-if-producer-called" in command
    assert command[0] == sys.executable
