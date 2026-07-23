"""Local exact and contract tests for the modern IM benchmark package."""

import json
import math
from pathlib import Path

import numpy as np
import pytest

from experiments.im_score_benchmark.aggregate import aggregate_documents
from experiments.im_score_benchmark.baselines import degree_score
from experiments.im_score_benchmark.benchmark import run_selector_benchmark
from experiments.im_score_benchmark.evaluate_spread import evaluate_selections
from experiments.im_score_benchmark.exact_tiny import (
    exact_greedy_selection,
    exact_k_semivalue_scores,
    exact_optimal_selection,
    exact_shapley_scores,
    exact_singleton_scores,
    exact_spread,
)
from experiments.im_score_benchmark.legacy_adapters import legacy_celf_selection
from experiments.im_score_benchmark.local_smoke import run_local_smoke
from experiments.im_score_benchmark.render_report import (
    render_html,
    render_markdown,
)
from experiments.im_score_benchmark.run_arxiv import _parser as arxiv_parser
from experiments.im_score_benchmark.run_planetoid import main as planetoid_main
from experiments.im_score_benchmark.runner_common import (
    EXECUTION_TOKEN,
    assert_execution_authorized,
)
from experiments.im_score_benchmark.rr_core import (
    DirectedGraph,
    RRBundle,
    _sample_reverse_reachable,
    sample_rr_bundle,
)
from experiments.im_score_benchmark.score_reducers import (
    build_score_bundle,
    rr_k_semivalue,
    rr_shapley,
    rr_sni,
)
from experiments.im_score_benchmark.selectors import (
    SampleBudgetExceeded,
    corrected_imm_select,
    maximum_coverage_greedy,
    opimc_select,
    select_top_k_score,
)


def _chain_graph():
    return DirectedGraph.from_edges(3, [(0, 1), (1, 2)])


def _chain_exact_rr_bundle():
    return RRBundle.from_rr_sets(
        num_nodes=3,
        candidate_nodes=[0, 1, 2],
        rr_sets=[[0], [0, 1], [0, 1, 2]],
        roots=[0, 1, 2],
        propagation_probability=1.0,
        rr_seed=0,
    )


def test_directed_graph_deduplicates_without_symmetrizing():
    graph = DirectedGraph.from_edges(3, [(0, 1), (0, 1), (1, 0)])
    assert graph.edges == ((0, 1), (1, 0))
    assert graph.in_neighbors[0] == (1,)
    assert graph.in_neighbors[1] == (0,)
    assert graph.out_neighbors[2] == ()


def test_reverse_reachable_respects_direction():
    graph = _chain_graph()
    rng = np.random.default_rng(1)
    assert _sample_reverse_reachable(graph, 2, 1.0, rng) == (0, 1, 2)
    assert _sample_reverse_reachable(graph, 0, 1.0, rng) == (0,)


def test_exact_spread_chain():
    graph = _chain_graph()
    assert exact_spread(graph, [0], 1.0) == pytest.approx(3.0)
    assert exact_spread(graph, [1], 1.0) == pytest.approx(2.0)
    assert exact_spread(graph, [2], 1.0) == pytest.approx(1.0)
    assert exact_spread(graph, [0], 0.0) == pytest.approx(1.0)


def test_rr_sni_matches_exact_singletons_on_complete_root_enumeration():
    graph = _chain_graph()
    artifact = rr_sni(_chain_exact_rr_bundle())
    expected = exact_singleton_scores(graph, [0, 1, 2], 1.0)
    np.testing.assert_allclose(artifact.scores, expected, atol=1e-12)
    assert artifact.ranking.tolist() == [0, 1, 2]


def test_rr_shapley_matches_exact_candidate_game():
    graph = _chain_graph()
    artifact = rr_shapley(_chain_exact_rr_bundle())
    expected = exact_shapley_scores(graph, [0, 1, 2], 1.0)
    np.testing.assert_allclose(artifact.scores, expected, atol=1e-12)
    assert artifact.scores.sum() == pytest.approx(3.0)


@pytest.mark.parametrize("budget", [1, 2, 3])
def test_rr_k_semivalue_matches_exact_candidate_game(budget):
    graph = _chain_graph()
    artifact = rr_k_semivalue(_chain_exact_rr_bundle(), budget)
    expected = exact_k_semivalue_scores(
        graph,
        [0, 1, 2],
        budget,
        1.0,
    )
    np.testing.assert_allclose(artifact.scores, expected, atol=1e-12)
    if budget == 1:
        np.testing.assert_allclose(
            artifact.scores,
            rr_sni(_chain_exact_rr_bundle()).scores,
            atol=1e-12,
        )


def test_build_score_bundle_and_top_k_are_typed_and_stable():
    bundle = _chain_exact_rr_bundle()
    artifacts = build_score_bundle(bundle, budgets=[2, 1, 2])
    assert sorted(artifacts) == [
        "rr_ksemivalue_k1",
        "rr_ksemivalue_k2",
        "rr_shapley",
        "rr_sni",
    ]
    selection = select_top_k_score(artifacts["rr_sni"], 2)
    assert selection.selected_nodes.tolist() == [0, 1]
    assert selection.metadata["selection_semantics"] == "static_score_top_k"
    json.dumps(selection.to_dict(), allow_nan=False)


def test_maximum_coverage_matches_exact_greedy_on_chain():
    graph = _chain_graph()
    selection = maximum_coverage_greedy(_chain_exact_rr_bundle(), 2)
    exact_nodes, _ = exact_greedy_selection(graph, [0, 1, 2], 2, 1.0)
    assert selection.selected_nodes.tolist() == list(exact_nodes)
    assert selection.accepted_gains.tolist() == [3.0, 0.0]


def test_exact_optimal_selection_uses_lexicographic_tie_break():
    graph = _chain_graph()
    selected, spread = exact_optimal_selection(graph, [0, 1, 2], 2, 1.0)
    assert selected == (0, 1)
    assert spread == pytest.approx(3.0)


def test_rr_sampling_is_deterministic_and_candidate_restricted():
    graph = _chain_graph()
    first = sample_rr_bundle(
        graph,
        candidate_nodes=[0, 2],
        rr_count=32,
        propagation_probability=0.3,
        rr_seed=2024,
    )
    second = sample_rr_bundle(
        graph,
        candidate_nodes=[0, 2],
        rr_count=32,
        propagation_probability=0.3,
        rr_seed=2024,
    )
    np.testing.assert_array_equal(first.roots, second.roots)
    np.testing.assert_array_equal(first.offsets, second.offsets)
    np.testing.assert_array_equal(
        first.candidate_local_ids,
        second.candidate_local_ids,
    )
    assert set(first.candidate_nodes.tolist()) == {0, 2}


def test_corrected_imm_uses_independent_final_batch_and_selects_hub():
    graph = DirectedGraph.from_edges(
        6,
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
    )
    result = corrected_imm_select(
        graph,
        candidate_nodes=list(range(6)),
        budget=1,
        propagation_probability=1.0,
        selector_seed=42,
        epsilon=0.5,
        delta=0.2,
        max_rr_sets=20_000,
    )
    assert result.selected_nodes.tolist() == [0]
    assert result.certificate.kind == "imm_workaround1_independent_final_rr"
    assert result.certificate.details["fixed_final_batch"] is True
    assert result.metadata["pilot_rr_total"] > 0
    assert result.source_rr_count > 0
    assert result.certificate.target_ratio > 0.0


def test_corrected_imm_fails_closed_on_sample_guard():
    graph = _chain_graph()
    with pytest.raises(SampleBudgetExceeded):
        corrected_imm_select(
            graph,
            candidate_nodes=[0, 1, 2],
            budget=1,
            propagation_probability=0.1,
            selector_seed=1,
            epsilon=0.1,
            delta=0.01,
            max_rr_sets=1,
        )


def test_opimc_has_independent_conservative_certificate():
    graph = DirectedGraph.from_edges(
        6,
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
    )
    result = opimc_select(
        graph,
        candidate_nodes=list(range(6)),
        budget=1,
        propagation_probability=1.0,
        selector_seed=7,
        epsilon=0.5,
        delta=0.2,
        initial_rr_count=64,
        max_rr_sets=256,
    )
    assert result.selected_nodes.tolist() == [0]
    assert result.certificate.kind.startswith("opimc_conservative")
    assert result.certificate.paper_equivalent is False
    assert result.metadata["selection_rr_count"] == result.metadata[
        "validation_rr_count"
    ]
    assert result.source_rr_count == 2 * result.metadata["selection_rr_count"]
    assert 0.0 <= result.certificate.ratio_lower_bound <= 1.0
    selected_spread = exact_spread(
        graph,
        result.selected_nodes.tolist(),
        1.0,
    )
    _, optimum_spread = exact_optimal_selection(
        graph,
        list(range(6)),
        1,
        1.0,
    )
    assert result.certificate.lower_bound <= selected_spread
    assert result.certificate.upper_bound >= optimum_spread


def test_local_smoke_is_dataset_free_and_serializable():
    result = run_local_smoke()
    assert result["ssh_used"] is False
    assert result["formal_dataset_used"] is False
    assert result["gu_cell_used"] is False
    assert result["corrected_imm"]["selected_nodes"][0] == 0
    assert result["opimc"]["selected_nodes"][0] == 0
    assert result["exact"]["imm_spread"] == pytest.approx(
        result["exact"]["optimum_spread"]
    )
    assert result["exact"]["opimc_spread"] == pytest.approx(
        result["exact"]["optimum_spread"]
    )
    json.dumps(result, allow_nan=False)


def test_score_artifact_arrays_are_read_only():
    artifact = rr_sni(_chain_exact_rr_bundle())
    with pytest.raises(ValueError):
        artifact.scores[0] = math.nan


def test_degree_score_matches_source_axis_and_stable_ties():
    graph = DirectedGraph.from_edges(4, [(0, 2), (1, 2), (1, 3)])
    artifact = degree_score(graph, [3, 2, 1, 0])
    assert artifact.source_rr_count == 0
    assert artifact.semantics == "degree_out"
    assert artifact.ranking.tolist() == [1, 0, 2, 3]
    np.testing.assert_array_equal(artifact.scores, [0.0, 0.0, 2.0, 1.0])


def test_independent_evaluator_uses_common_random_rr_samples():
    graph = DirectedGraph.from_edges(
        5,
        [(0, 1), (0, 2), (0, 3), (0, 4)],
    )
    result = evaluate_selections(
        graph,
        selections={"degree": [0], "same": [0], "leaf": [1]},
        degree_key="degree",
        propagation_probability=1.0,
        evaluator_seed=7,
        min_rr_sets=64,
        batch_rr_sets=64,
        max_rr_sets=64,
        target_half_width_probability=0.0,
    )
    assert result["sample_count"] == 64
    assert result["methods"]["same"]["paired_difference_probability"] == 0.0
    assert result["methods"]["leaf"]["spread_ratio_vs_degree"] < 1.0


def test_dataset_agnostic_benchmark_aggregate_and_render():
    graph = DirectedGraph.from_edges(
        6,
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
    )
    document = run_selector_benchmark(
        graph,
        dataset_name="dataset-free-fixture",
        candidate_nodes=list(range(6)),
        budgets=[1, 2],
        selector_seed=42,
        propagation_probability=1.0,
        methods=["degree", "rr_sni", "rr_shapley", "rr_ksemivalue"],
        score_rr_count=64,
        evaluator_min_rr_sets=64,
        evaluator_batch_rr_sets=64,
        evaluator_max_rr_sets=128,
        evaluator_half_width=0.05,
        source_manifest={
            "run_kind": "dataset_free_local_only",
            "ssh_used": False,
            "formal_dataset_used": False,
            "gu_cell_used": False,
        },
    )
    assert document["schema"] == "im_score_benchmark.selector_benchmark"
    assert sorted(document["budgets"]) == ["1", "2"]
    assert document["shared_rr_bundle"]["rr_count"] == 64
    rr_timing = document["budgets"]["1"]["methods"]["rr_sni"]["telemetry"]
    assert rr_timing["wall_seconds"] >= rr_timing["online_wall_seconds"]
    assert rr_timing["shared_precompute_wall_seconds"] > 0.0
    aggregate = aggregate_documents([document])
    assert len(aggregate["rows"]) == 8
    assert set(aggregate["method_summary"]) == {
        "degree",
        "rr_ksemivalue",
        "rr_shapley",
        "rr_sni",
    }
    markdown = render_markdown(aggregate)
    html = render_html(markdown, aggregate)
    assert "dataset-free-fixture" in markdown
    assert "IM 成熟算法 Selector 结果报告" in html
    json.dumps(aggregate, ensure_ascii=False, allow_nan=False)


@pytest.mark.parametrize(
    "algorithm,batch_size",
    [("im_celf_strict", 1), ("im_batch_celf_current", 2)],
)
def test_legacy_celf_adapters_run_without_cache(algorithm, batch_size):
    graph = DirectedGraph.from_edges(3, [(0, 1), (0, 2)])
    selection = legacy_celf_selection(
        graph,
        candidate_nodes=[0, 1, 2],
        budget=1,
        propagation_probability=1.0,
        selector_seed=42,
        mc_rounds=2,
        batch_size=batch_size,
        algorithm=algorithm,
    )
    assert selection.selected_nodes.tolist() == [0]
    assert selection.source_rr_count == 0
    assert selection.metadata["batch_size"] == batch_size


def test_execution_guard_is_preflight_by_default_and_token_gated():
    provenance = assert_execution_authorized(
        execute=False,
        approval_token="",
        formal=False,
    )
    assert len(provenance["sha"]) == 40
    with pytest.raises(RuntimeError, match=EXECUTION_TOKEN):
        assert_execution_authorized(
            execute=True,
            approval_token="wrong-token",
            formal=False,
        )


def test_registered_matrix_is_disabled_and_counts_are_consistent():
    plan_path = (
        Path(__file__).resolve().parents[1]
        / "experiments"
        / "im_score_benchmark"
        / "registered_plan.json"
    )
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    assert plan["formal_execution_authorized"] is False
    small = plan["small"]
    large = plan["large"]
    assert small["profile"] == "opengu_canonical_processed_transductive_80_20"
    assert small["budget_ratios"] == [0.01, 0.05]
    assert "im_batch_celf_current" not in small["methods"]
    assert "im_celf_strict" not in small["methods"]
    assert small["registered_rows"] == (
        len(small["datasets"])
        * len(small["selector_seeds"])
        * len(small["budget_ratios"])
        * len(small["methods"])
    )
    assert large["budget_ratios"] == [0.01, 0.05]
    assert large["registered_rows"] == (
        len(large["selector_seeds"])
        * len(large["budget_ratios"])
        * len(large["methods"])
    )


def test_formal_budget_defaults_and_public_diagnostic_boundary():
    assert arxiv_parser().parse_args([]).budget_ratios == "0.01,0.05"
    with pytest.raises(RuntimeError, match="diagnostic-only"):
        planetoid_main(["--dataset", "Cora", "--formal"])
