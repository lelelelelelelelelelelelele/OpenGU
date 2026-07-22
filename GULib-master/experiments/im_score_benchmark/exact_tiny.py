"""Exact live-edge references for tiny directed IC graphs."""

from __future__ import annotations

import itertools
import math
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple

import numpy as np

from .rr_core import DirectedGraph


def iter_live_edge_worlds(
    graph: DirectedGraph,
    propagation_probability: float,
) -> Iterator[Tuple[Tuple[Tuple[int, int], ...], float]]:
    """Enumerate every live-edge world and its probability."""

    probability = float(propagation_probability)
    if not 0.0 <= probability <= 1.0:
        raise ValueError("propagation probability must be in [0, 1]")
    edge_count = graph.edge_count
    if edge_count > 20:
        raise ValueError("exact live-edge enumeration is limited to 20 edges")
    for mask in range(1 << edge_count):
        live: List[Tuple[int, int]] = []
        live_count = 0
        for edge_index, edge in enumerate(graph.edges):
            if mask & (1 << edge_index):
                live.append(edge)
                live_count += 1
        dead_count = edge_count - live_count
        world_probability = (
            (probability ** live_count)
            * ((1.0 - probability) ** dead_count)
        )
        if world_probability > 0.0:
            yield tuple(live), float(world_probability)


def _reachable_count(
    num_nodes: int,
    live_edges: Iterable[Tuple[int, int]],
    seeds: Sequence[int],
) -> int:
    outgoing: List[List[int]] = [[] for _ in range(int(num_nodes))]
    for src, dst in live_edges:
        outgoing[int(src)].append(int(dst))
    reached = {int(node) for node in seeds}
    frontier = sorted(reached)
    head = 0
    while head < len(frontier):
        node = frontier[head]
        head += 1
        for neighbor in outgoing[node]:
            if neighbor not in reached:
                reached.add(neighbor)
                frontier.append(neighbor)
    return len(reached)


def exact_spread(
    graph: DirectedGraph,
    seeds: Sequence[int],
    propagation_probability: float,
) -> float:
    """Compute exact expected spread by enumerating live-edge worlds."""

    seed_tuple = tuple(sorted({int(node) for node in seeds}))
    if any(node < 0 or node >= graph.num_nodes for node in seed_tuple):
        raise ValueError("seed is outside [0, num_nodes)")
    total = 0.0
    for live_edges, world_probability in iter_live_edge_worlds(
        graph,
        propagation_probability,
    ):
        total += world_probability * _reachable_count(
            graph.num_nodes,
            live_edges,
            seed_tuple,
        )
    return float(total)


def exact_singleton_scores(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
    propagation_probability: float,
) -> np.ndarray:
    return np.asarray(
        [
            exact_spread(graph, [int(node)], propagation_probability)
            for node in candidate_nodes
        ],
        dtype=np.float64,
    )


def exact_shapley_scores(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
    propagation_probability: float,
) -> np.ndarray:
    """Exact Shapley values for the spread cooperative game on candidates."""

    candidates = tuple(int(node) for node in candidate_nodes)
    if len(candidates) != len(set(candidates)) or not candidates:
        raise ValueError("candidate_nodes must be non-empty and unique")
    count = len(candidates)
    factorial = math.factorial
    scores = np.zeros(count, dtype=np.float64)
    value_cache: Dict[Tuple[int, ...], float] = {}

    def value(coalition: Sequence[int]) -> float:
        key = tuple(sorted(int(node) for node in coalition))
        if key not in value_cache:
            value_cache[key] = exact_spread(
                graph,
                key,
                propagation_probability,
            )
        return value_cache[key]

    for index, node in enumerate(candidates):
        others = tuple(value for value in candidates if value != node)
        for size in range(len(others) + 1):
            weight = (
                factorial(size)
                * factorial(count - size - 1)
                / float(factorial(count))
            )
            for coalition in itertools.combinations(others, size):
                scores[index] += weight * (
                    value(coalition + (node,)) - value(coalition)
                )
    return scores


def exact_k_semivalue_scores(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
) -> np.ndarray:
    """Exact mean marginal over coalitions of size budget-1."""

    candidates = tuple(int(node) for node in candidate_nodes)
    budget = int(budget)
    if len(candidates) != len(set(candidates)) or not candidates:
        raise ValueError("candidate_nodes must be non-empty and unique")
    if not 1 <= budget <= len(candidates):
        raise ValueError("budget must be in [1, candidate_count]")
    scores = np.zeros(len(candidates), dtype=np.float64)
    for index, node in enumerate(candidates):
        others = tuple(value for value in candidates if value != node)
        coalitions = list(itertools.combinations(others, budget - 1))
        scores[index] = float(
            np.mean(
                [
                    exact_spread(
                        graph,
                        coalition + (node,),
                        propagation_probability,
                    )
                    - exact_spread(
                        graph,
                        coalition,
                        propagation_probability,
                    )
                    for coalition in coalitions
                ]
            )
        )
    return scores


def exact_greedy_selection(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
) -> Tuple[Tuple[int, ...], Tuple[float, ...]]:
    """Exact spread greedy with node-id tie breaking."""

    candidates = tuple(sorted({int(node) for node in candidate_nodes}))
    budget = int(budget)
    if not 1 <= budget <= len(candidates):
        raise ValueError("budget must be in [1, candidate_count]")
    selected: List[int] = []
    gains: List[float] = []
    current = exact_spread(graph, selected, propagation_probability)
    for _ in range(budget):
        best_node = None
        best_gain = -math.inf
        best_spread = None
        for node in candidates:
            if node in selected:
                continue
            spread = exact_spread(
                graph,
                selected + [node],
                propagation_probability,
            )
            gain = spread - current
            if (
                gain > best_gain + 1e-12
                or (
                    abs(gain - best_gain) <= 1e-12
                    and (best_node is None or node < best_node)
                )
            ):
                best_node = node
                best_gain = gain
                best_spread = spread
        if best_node is None or best_spread is None:
            raise RuntimeError("exact greedy failed to select a node")
        selected.append(best_node)
        gains.append(float(best_gain))
        current = float(best_spread)
    return tuple(selected), tuple(gains)


def exact_optimal_selection(
    graph: DirectedGraph,
    candidate_nodes: Sequence[int],
    budget: int,
    propagation_probability: float,
) -> Tuple[Tuple[int, ...], float]:
    """Enumerate every size-k candidate set and return the exact optimum."""

    candidates = tuple(sorted({int(node) for node in candidate_nodes}))
    budget = int(budget)
    if not 1 <= budget <= len(candidates):
        raise ValueError("budget must be in [1, candidate_count]")
    best_set = None
    best_spread = -math.inf
    for selection in itertools.combinations(candidates, budget):
        spread = exact_spread(graph, selection, propagation_probability)
        if (
            spread > best_spread + 1e-12
            or (
                abs(spread - best_spread) <= 1e-12
                and (best_set is None or selection < best_set)
            )
        ):
            best_set = selection
            best_spread = spread
    if best_set is None:
        raise RuntimeError("exact optimum enumeration produced no selection")
    return tuple(best_set), float(best_spread)
