"""RR maximum coverage, corrected IMM, and conservative OPIM-C adapters."""

from __future__ import annotations

import heapq
import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from .contracts import (
    ApproximationCertificate,
    ScoreArtifact,
    SelectionArtifact,
)
from .rr_core import DirectedGraph, RRBundle, sample_rr_bundle


class SampleBudgetExceeded(RuntimeError):
    """Raised when a theory-derived RR request exceeds the registered guard."""


def _validate_budget(candidate_count: int, budget: int) -> int:
    budget = int(budget)
    if not 1 <= budget <= int(candidate_count):
        raise ValueError("budget must be in [1, candidate_count]")
    return budget


def _log_binomial(n: int, k: int) -> float:
    n = int(n)
    k = int(k)
    if not 0 <= k <= n:
        raise ValueError("invalid binomial arguments")
    k = min(k, n - k)
    return float(
        math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    )


def _spawn_seeds(seed: int, count: int) -> List[int]:
    sequence = np.random.SeedSequence(int(seed))
    return [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in sequence.spawn(int(count))
    ]


def maximum_coverage_greedy(
    bundle: RRBundle,
    budget: int,
    *,
    algorithm: str = "rr_maximum_coverage_greedy",
) -> SelectionArtifact:
    """Deterministic greedy maximum coverage with node-id tie breaking."""

    budget = _validate_budget(bundle.candidate_count, budget)
    inverse = bundle.inverted_index()
    gains = bundle.incidence_counts().astype(np.int64, copy=True)
    versions = np.zeros(bundle.candidate_count, dtype=np.int64)
    selected_mask = np.zeros(bundle.candidate_count, dtype=np.bool_)
    covered = np.zeros(bundle.rr_count, dtype=np.bool_)
    heap: List[Tuple[int, int, int, int]] = []
    for local_id, node in enumerate(bundle.candidate_nodes.tolist()):
        heapq.heappush(
            heap,
            (-int(gains[local_id]), int(node), int(local_id), 0),
        )

    selected: List[int] = []
    accepted: List[float] = []
    coverage_trace: List[int] = []
    while len(selected) < budget:
        while heap:
            negative_gain, node, local_id, version = heapq.heappop(heap)
            if selected_mask[local_id]:
                continue
            if version != int(versions[local_id]):
                continue
            if -negative_gain != int(gains[local_id]):
                continue
            break
        else:
            raise RuntimeError("maximum coverage heap exhausted before budget")

        accepted_gain = int(gains[local_id])
        selected_mask[local_id] = True
        selected.append(int(node))
        accepted.append(float(accepted_gain))
        newly_covered = [
            int(rr_index)
            for rr_index in inverse[local_id].tolist()
            if not covered[int(rr_index)]
        ]
        for rr_index in newly_covered:
            covered[rr_index] = True
            for other_local in bundle.local_row(rr_index).tolist():
                other_local = int(other_local)
                if selected_mask[other_local]:
                    continue
                gains[other_local] -= 1
                versions[other_local] += 1
                heapq.heappush(
                    heap,
                    (
                        -int(gains[other_local]),
                        int(bundle.candidate_nodes[other_local]),
                        other_local,
                        int(versions[other_local]),
                    ),
                )
        coverage_trace.append(int(covered.sum()))

    return SelectionArtifact(
        algorithm=algorithm,
        selected_nodes=np.asarray(selected, dtype=np.int64),
        accepted_gains=np.asarray(accepted, dtype=np.float64),
        budget=budget,
        source_rr_count=bundle.rr_count,
        metadata={
            "tie_break": "gain_desc_node_id_asc",
            "covered_rr_count": int(covered.sum()),
            "coverage_fraction": float(covered.mean()),
            "coverage_trace": coverage_trace,
            "estimated_spread": (
                float(bundle.num_nodes) * float(covered.mean())
            ),
        },
    )


def select_top_k_score(
    artifact: ScoreArtifact,
    budget: int,
    *,
    algorithm: Optional[str] = None,
) -> SelectionArtifact:
    """Materialize a stable top-k selection from a static full score."""

    budget = _validate_budget(artifact.candidate_nodes.size, budget)
    selected = artifact.ranking[:budget]
    score_by_node = {
        int(node): float(score)
        for node, score in zip(
            artifact.candidate_nodes.tolist(),
            artifact.scores.tolist(),
        )
    }
    gains = np.asarray(
        [score_by_node[int(node)] for node in selected.tolist()],
        dtype=np.float64,
    )
    return SelectionArtifact(
        algorithm=algorithm or artifact.semantics,
        selected_nodes=selected,
        accepted_gains=gains,
        budget=budget,
        source_rr_count=artifact.source_rr_count,
        metadata={
            "selection_semantics": "static_score_top_k",
            "source_score_semantics": artifact.semantics,
            "source_score_budget": artifact.budget,
            "tie_break": "score_desc_node_id_asc",
        },
    )


def _imm_lambdas(
    *,
    num_nodes: int,
    candidate_count: int,
    budget: int,
    epsilon: float,
    delta: float,
) -> Tuple[float, float, float]:
    epsilon_prime = math.sqrt(2.0) * float(epsilon)
    log_comb = _log_binomial(candidate_count, budget)
    log_failure = math.log(2.0 / float(delta))
    ladder_count = max(1.0, math.log2(max(2, int(num_nodes))))
    lambda_prime = (
        (2.0 + (2.0 / 3.0) * epsilon_prime)
        * (
            log_comb
            + log_failure
            + math.log(max(1.0, ladder_count))
        )
        * float(num_nodes)
        / (epsilon_prime ** 2)
    )
    alpha = math.sqrt(log_failure)
    beta = math.sqrt((1.0 - 1.0 / math.e) * (log_comb + log_failure))
    lambda_star = (
        2.0
        * float(num_nodes)
        * (((1.0 - 1.0 / math.e) * alpha + beta) ** 2)
        / (float(epsilon) ** 2)
    )
    return epsilon_prime, lambda_prime, lambda_star


def corrected_imm_select(
    graph: DirectedGraph,
    *,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
    selector_seed: int,
    epsilon: float = 0.1,
    delta: float = 0.01,
    root_nodes: Optional[Sequence[int]] = None,
    max_rr_sets: Optional[int] = None,
) -> SelectionArtifact:
    """IMM-style sampling with Chen workaround 1.

    Pilot RR samples determine the final fixed theta.  The final selection is
    computed from a newly generated independent RR batch of exactly theta
    samples, so the stopping-time sample is never reused for NodeSelection.
    """

    candidates = np.asarray(candidate_nodes, dtype=np.int64).reshape(-1)
    if candidates.size != np.unique(candidates).size:
        raise ValueError("candidate_nodes must be unique")
    budget = _validate_budget(candidates.size, budget)
    epsilon = float(epsilon)
    delta = float(delta)
    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must be in (0, 1)")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must be in (0, 1)")

    epsilon_prime, lambda_prime, lambda_star = _imm_lambdas(
        num_nodes=graph.num_nodes,
        candidate_count=int(candidates.size),
        budget=budget,
        epsilon=epsilon,
        delta=delta,
    )
    ladder_steps = max(1, int(math.ceil(math.log2(max(2, graph.num_nodes)))))
    seeds = _spawn_seeds(selector_seed, ladder_steps + 1)
    lower_bound = 1.0
    pilot_rr_total = 0
    pilot_observations: List[Dict[str, float]] = []
    for step in range(1, ladder_steps + 1):
        x_value = float(graph.num_nodes) / float(2 ** step)
        requested = max(1, int(math.ceil(lambda_prime / x_value)))
        if max_rr_sets is not None and requested > int(max_rr_sets):
            raise SampleBudgetExceeded(
                "IMM pilot requires {0} RR sets, above guard {1}".format(
                    requested,
                    int(max_rr_sets),
                )
            )
        pilot_bundle = sample_rr_bundle(
            graph,
            candidate_nodes=candidates,
            rr_count=requested,
            propagation_probability=propagation_probability,
            rr_seed=seeds[step - 1],
            root_nodes=root_nodes,
            metadata={"phase": "imm_pilot", "step": step},
        )
        pilot_selection = maximum_coverage_greedy(
            pilot_bundle,
            budget,
            algorithm="corrected_imm_pilot",
        )
        coverage_fraction = float(
            pilot_selection.metadata["coverage_fraction"]
        )
        estimated_spread = float(graph.num_nodes) * coverage_fraction
        pilot_rr_total += requested
        pilot_observations.append(
            {
                "step": float(step),
                "x": x_value,
                "rr_count": float(requested),
                "estimated_spread": estimated_spread,
            }
        )
        if estimated_spread >= (1.0 + epsilon_prime) * x_value:
            lower_bound = estimated_spread / (1.0 + epsilon_prime)
            break

    final_rr_count = max(1, int(math.ceil(lambda_star / lower_bound)))
    if max_rr_sets is not None and final_rr_count > int(max_rr_sets):
        raise SampleBudgetExceeded(
            "IMM final batch requires {0} RR sets, above guard {1}".format(
                final_rr_count,
                int(max_rr_sets),
            )
        )
    final_bundle = sample_rr_bundle(
        graph,
        candidate_nodes=candidates,
        rr_count=final_rr_count,
        propagation_probability=propagation_probability,
        rr_seed=seeds[-1],
        root_nodes=root_nodes,
        metadata={"phase": "imm_final_independent"},
    )
    base = maximum_coverage_greedy(
        final_bundle,
        budget,
        algorithm="corrected_imm",
    )
    target_ratio = max(0.0, 1.0 - 1.0 / math.e - epsilon)
    certificate = ApproximationCertificate(
        kind="imm_workaround1_independent_final_rr",
        lower_bound=target_ratio,
        upper_bound=1.0,
        ratio_lower_bound=target_ratio,
        target_ratio=target_ratio,
        failure_probability=delta,
        met_target=True,
        paper_equivalent=False,
        details={
            "bound_units": "relative_to_candidate_restricted_optimum",
            "candidate_restricted_adaptation": True,
            "fixed_final_batch": True,
            "final_batch_independent_of_pilot": True,
            "implementation_acceptance": "local_exact_tiny_only",
        },
    )
    return SelectionArtifact(
        algorithm=base.algorithm,
        selected_nodes=base.selected_nodes,
        accepted_gains=base.accepted_gains,
        budget=base.budget,
        source_rr_count=base.source_rr_count,
        certificate=certificate,
        metadata={
            **dict(base.metadata),
            "epsilon": epsilon,
            "delta": delta,
            "lower_bound_estimate": lower_bound,
            "lambda_prime": lambda_prime,
            "lambda_star": lambda_star,
            "pilot_rr_total": pilot_rr_total,
            "pilot_observations": pilot_observations,
            "pilot_seed_count": ladder_steps,
            "final_rr_seed": seeds[-1],
            "candidate_fraction": 1.0,
        },
    )


def _opim_conservative_certificate(
    selection_bundle: RRBundle,
    validation_bundle: RRBundle,
    selection: SelectionArtifact,
    *,
    candidate_count: int,
    budget: int,
    per_round_delta: float,
    overall_delta: float,
    target_ratio: float,
    round_index: int,
) -> ApproximationCertificate:
    theta_one = float(selection_bundle.rr_count)
    theta_two = float(validation_bundle.rr_count)
    log_comb = _log_binomial(candidate_count, budget)
    alpha = 1.0 if budget == 1 else 1.0 - (1.0 - 1.0 / budget) ** budget
    selected = selection.selected_nodes.tolist()
    fraction_one = selection_bundle.coverage_count(selected) / theta_one
    fraction_two = validation_bundle.coverage_count(selected) / theta_two
    upper_radius = math.sqrt(
        (log_comb + math.log(2.0 / per_round_delta)) / (2.0 * theta_one)
    )
    lower_radius = math.sqrt(
        math.log(2.0 / per_round_delta) / (2.0 * theta_two)
    )
    lower_fraction = max(0.0, fraction_two - lower_radius)
    upper_fraction = min(1.0, fraction_one / alpha + upper_radius)
    bounds_crossed = upper_fraction < lower_fraction
    upper_fraction = max(lower_fraction, upper_fraction)
    lower_bound = float(selection_bundle.num_nodes) * lower_fraction
    upper_bound = float(selection_bundle.num_nodes) * upper_fraction
    ratio = 0.0 if upper_bound <= 0.0 else lower_bound / upper_bound
    return ApproximationCertificate(
        kind="opimc_conservative_independent_rr_hoeffding_v1",
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        ratio_lower_bound=min(1.0, max(0.0, ratio)),
        target_ratio=target_ratio,
        failure_probability=overall_delta,
        met_target=ratio >= target_ratio,
        paper_equivalent=False,
        details={
            "round_index": int(round_index),
            "overall_failure_probability": overall_delta,
            "per_round_failure_probability": per_round_delta,
            "selection_coverage_fraction": fraction_one,
            "validation_coverage_fraction": fraction_two,
            "uniform_upper_radius": upper_radius,
            "validation_lower_radius": lower_radius,
            "finite_k_greedy_alpha": alpha,
            "bounds_crossed_before_clamp": bounds_crossed,
            "candidate_restricted_adaptation": True,
            "paper_bound_status": "conservative_not_paper_equivalent",
        },
    )


def opimc_select(
    graph: DirectedGraph,
    *,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
    selector_seed: int,
    epsilon: float = 0.1,
    delta: float = 0.01,
    initial_rr_count: int = 256,
    max_rr_sets: int = 1_048_576,
    root_nodes: Optional[Sequence[int]] = None,
) -> SelectionArtifact:
    """Anytime dual-sample RR selection with a conservative certificate.

    The selection and validation RR batches are independent.  The current
    certificate uses a union-Hoeffding upper bound and is intentionally marked
    as not paper-equivalent to the tighter OPIM-C bound.
    """

    candidates = np.asarray(candidate_nodes, dtype=np.int64).reshape(-1)
    if candidates.size != np.unique(candidates).size:
        raise ValueError("candidate_nodes must be unique")
    budget = _validate_budget(candidates.size, budget)
    epsilon = float(epsilon)
    delta = float(delta)
    initial_rr_count = int(initial_rr_count)
    max_rr_sets = int(max_rr_sets)
    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must be in (0, 1)")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must be in (0, 1)")
    if initial_rr_count <= 0 or max_rr_sets < initial_rr_count:
        raise ValueError("invalid OPIM-C RR schedule")

    max_rounds = 1 + int(
        math.ceil(math.log(max_rr_sets / float(initial_rr_count), 2.0))
    )
    per_round_delta = delta / float(max_rounds)
    seeds = _spawn_seeds(selector_seed, max_rounds * 2)
    target_ratio = max(0.0, 1.0 - 1.0 / math.e - epsilon)
    rr_count = initial_rr_count
    total_generated = 0
    latest: Optional[SelectionArtifact] = None
    for round_index in range(max_rounds):
        rr_count = min(rr_count, max_rr_sets)
        selection_bundle = sample_rr_bundle(
            graph,
            candidate_nodes=candidates,
            rr_count=rr_count,
            propagation_probability=propagation_probability,
            rr_seed=seeds[2 * round_index],
            root_nodes=root_nodes,
            metadata={"phase": "opimc_selection", "round": round_index},
        )
        validation_bundle = sample_rr_bundle(
            graph,
            candidate_nodes=candidates,
            rr_count=rr_count,
            propagation_probability=propagation_probability,
            rr_seed=seeds[2 * round_index + 1],
            root_nodes=root_nodes,
            metadata={"phase": "opimc_validation", "round": round_index},
        )
        total_generated += 2 * rr_count
        base = maximum_coverage_greedy(
            selection_bundle,
            budget,
            algorithm="opimc_conservative",
        )
        certificate = _opim_conservative_certificate(
            selection_bundle,
            validation_bundle,
            base,
            candidate_count=int(candidates.size),
            budget=budget,
            per_round_delta=per_round_delta,
            overall_delta=delta,
            target_ratio=target_ratio,
            round_index=round_index,
        )
        latest = SelectionArtifact(
            algorithm=base.algorithm,
            selected_nodes=base.selected_nodes,
            accepted_gains=base.accepted_gains,
            budget=base.budget,
            source_rr_count=2 * rr_count,
            certificate=certificate,
            metadata={
                **dict(base.metadata),
                "epsilon": epsilon,
                "delta": delta,
                "round_delta": per_round_delta,
                "round_index": round_index,
                "selection_rr_count": rr_count,
                "validation_rr_count": rr_count,
                "total_generated_rr_count": total_generated,
                "candidate_fraction": 1.0,
            },
        )
        if certificate.met_target or rr_count >= max_rr_sets:
            return latest
        rr_count *= 2
    if latest is None:
        raise RuntimeError("OPIM-C schedule produced no selection")
    return latest
