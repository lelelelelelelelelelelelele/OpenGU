"""Experiment-owned max-k Selection planning over formal Cache V2 Artifacts."""

from __future__ import annotations

import operator
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Sequence, Tuple, Union

from cache_v2 import ProducerVersion
from cache_v2.errors import ContractValidationError
from cache_v2.selection_materializer import (
    SelectionArtifactRequest,
    build_selection_recipe,
    resolve_covering_selection_artifact,
    store_selection_artifact,
)
from cache_v2.store import StoreResult
from experiments.selection_inputs import DatasetSelectionInputs
from experiments.selection_producer import UpstreamProducerCalledError


MAXK_SELECTION_PLAN_SCHEMA = "opengu.maxk_selection_plan"
MAXK_SELECTION_PLAN_VERSION = 1


def normalize_budgets(
    budgets: Sequence[int], candidate_count: int
) -> Tuple[int, ...]:
    """Validate, deduplicate, and return budgets from largest to smallest."""

    if isinstance(candidate_count, bool) or candidate_count <= 0:
        raise ContractValidationError("candidate_count must be positive")
    normalized = []
    for position, value in enumerate(budgets):
        if isinstance(value, bool):
            raise ContractValidationError(
                "budget at position {0} must be an integer".format(position)
            )
        try:
            budget = operator.index(value)
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "budget at position {0} must be an integer".format(position)
            )
        if budget <= 0 or budget > candidate_count:
            raise ContractValidationError(
                "budget at position {0} is outside [1, candidate_count]".format(
                    position
                )
            )
        normalized.append(int(budget))
    if not normalized:
        raise ContractValidationError("at least one Selection budget is required")
    return tuple(sorted(set(normalized), reverse=True))


def _validate_selected_nodes(
    values: Sequence[int], *, k: int, candidates: Sequence[int]
) -> Tuple[int, ...]:
    nodes = []
    for position, value in enumerate(values):
        if isinstance(value, bool):
            raise ContractValidationError(
                "selected node at position {0} must be an integer".format(position)
            )
        try:
            nodes.append(int(operator.index(value)))
        except (TypeError, ValueError, OverflowError):
            raise ContractValidationError(
                "selected node at position {0} must be an integer".format(position)
            )
    result = tuple(nodes)
    if len(result) != k:
        raise ContractValidationError("producer selected-node count does not match max k")
    if len(result) != len(set(result)):
        raise ContractValidationError("producer selected nodes contain duplicates")
    candidate_set = set(int(node) for node in candidates)
    outside = [node for node in result if node not in candidate_set]
    if outside:
        raise ContractValidationError(
            "producer selected nodes outside candidate set: {0}".format(outside)
        )
    return result


def _budget_views(
    budgets_desc: Sequence[int],
    *,
    request_max_k: int,
    artifact_k: int,
    selected_nodes: Sequence[int],
    cache_hit: bool,
) -> Mapping[str, Mapping[str, Any]]:
    views: Dict[str, Mapping[str, Any]] = {}
    for budget in budgets_desc:
        prefix_reuse = int(budget) < int(artifact_k)
        if cache_hit:
            outcome = "cache_hit_prefix_reuse" if prefix_reuse else "cache_hit"
            reuse_kind = "cache_artifact_prefix" if prefix_reuse else "none"
        else:
            outcome = (
                "same_run_prefix_reuse"
                if int(budget) < int(request_max_k)
                else "cache_miss_saved"
            )
            reuse_kind = (
                "same_run_prefix" if int(budget) < int(request_max_k) else "none"
            )
        views[str(int(budget))] = {
            "requested_k": int(budget),
            "request_max_k": int(request_max_k),
            "artifact_k": int(artifact_k),
            "cache_outcome": outcome,
            "prefix_reuse": bool(prefix_reuse or int(budget) < int(request_max_k)),
            "reuse_kind": reuse_kind,
            "selected_nodes": [int(node) for node in selected_nodes[: int(budget)]],
        }
    return views


@dataclass(frozen=True)
class MaterializedBudgetSelection:
    strategy: str
    budgets_descending: Tuple[int, ...]
    request_max_k: int
    artifact_k: int
    artifact_recipe_hash: str
    cache_hit: bool
    producer_called: bool
    lookup_policy: str
    result: StoreResult
    views: Mapping[str, Mapping[str, Any]]

    def to_manifest(self, store_root: Union[str, Path]) -> Mapping[str, Any]:
        root = Path(store_root).expanduser().resolve(strict=False)
        return {
            "schema": MAXK_SELECTION_PLAN_SCHEMA,
            "version": MAXK_SELECTION_PLAN_VERSION,
            "strategy": self.strategy,
            "requested_budgets_descending": list(self.budgets_descending),
            "request_max_k": self.request_max_k,
            "artifact_k": self.artifact_k,
            "cache": {
                "root": str(root),
                "hit": self.cache_hit,
                "outcome": "hit" if self.cache_hit else "miss_saved",
                "producer_called": self.producer_called,
                "lookup_policy": self.lookup_policy,
            },
            "artifact": {
                "artifact_id": self.result.artifact_id,
                "recipe_hash": self.artifact_recipe_hash,
                "content_hash": self.result.content_hash,
                "semantic_path": self.result.semantic_path,
                "source_score_artifact_id": self.result.payload.source_score_artifact_id,
            },
            "views": {key: dict(value) for key, value in self.views.items()},
        }


def materialize_budget_selection(
    *,
    store_root: Union[str, Path],
    dataset: DatasetSelectionInputs,
    strategy: str,
    selector_seed: int,
    budgets: Sequence[int],
    producer_version: ProducerVersion,
    algorithm_version: str,
    parameters: Mapping[str, Any],
    source_score_artifact_id: str,
    producer: Callable[[int], Sequence[int]],
    fail_if_producer_called: bool = False,
) -> MaterializedBudgetSelection:
    """Resolve one max-k request and fan its ordered prefix out to all budgets."""

    if not isinstance(dataset, DatasetSelectionInputs):
        raise ContractValidationError("dataset must be DatasetSelectionInputs")
    if not callable(producer):
        raise ContractValidationError("producer must be callable")
    selector_parameters = dict(parameters)
    if selector_parameters.get("prefix_stable") is not True:
        raise ContractValidationError("max-k reuse requires prefix_stable=true")
    budgets_desc = normalize_budgets(budgets, dataset.candidate_count)
    request_max_k = budgets_desc[0]
    recipe = build_selection_recipe(
        dataset_fingerprint=dataset.dataset_fingerprint,
        graph_fingerprint=dataset.graph_fingerprint,
        candidate_set_hash=dataset.candidate_set_hash,
        num_nodes=dataset.num_nodes,
        candidate_count=dataset.candidate_count,
        node_id_space=dataset.node_id_space,
        strategy=strategy,
        seed=int(selector_seed),
        k=request_max_k,
        producer_version=producer_version,
        algorithm_version=algorithm_version,
        parameters=selector_parameters,
        source_score_artifact_id=source_score_artifact_id,
    )
    request = SelectionArtifactRequest.from_recipe(recipe, producer_version)
    resolution = resolve_covering_selection_artifact(store_root, request)
    if resolution.hit and resolution.result is not None:
        result = resolution.result
        artifact_k = int(resolution.source_k)
        selected = tuple(result.payload.selected_nodes_ordered)
        if len(selected) != artifact_k or artifact_k < request_max_k:
            raise ContractValidationError("covering Selection Artifact has invalid length")
        if resolution.source_recipe_hash is None:
            raise ContractValidationError(
                "covering Selection resolution has no source Recipe hash"
            )
        return MaterializedBudgetSelection(
            strategy=str(strategy),
            budgets_descending=budgets_desc,
            request_max_k=request_max_k,
            artifact_k=artifact_k,
            artifact_recipe_hash=str(resolution.source_recipe_hash),
            cache_hit=True,
            producer_called=False,
            lookup_policy=resolution.lookup_policy,
            result=result,
            views=_budget_views(
                budgets_desc,
                request_max_k=request_max_k,
                artifact_k=artifact_k,
                selected_nodes=selected,
                cache_hit=True,
            ),
        )

    if fail_if_producer_called:
        raise UpstreamProducerCalledError(
            "max-k Selection producer fail-if-called sentinel reached for {0} k={1}".format(
                strategy, request_max_k
            )
        )
    started = time.perf_counter()
    selected = _validate_selected_nodes(
        producer(request_max_k),
        k=request_max_k,
        candidates=dataset.candidate_nodes,
    )
    elapsed = time.perf_counter() - started
    result = store_selection_artifact(
        store_root,
        request,
        selected_nodes=selected,
        compute_seconds=elapsed,
    )
    return MaterializedBudgetSelection(
        strategy=str(strategy),
        budgets_descending=budgets_desc,
        request_max_k=request_max_k,
        artifact_k=request_max_k,
        artifact_recipe_hash=recipe.recipe_hash,
        cache_hit=False,
        producer_called=True,
        lookup_policy=resolution.lookup_policy,
        result=result,
        views=_budget_views(
            budgets_desc,
            request_max_k=request_max_k,
            artifact_k=request_max_k,
            selected_nodes=selected,
            cache_hit=False,
        ),
    )


__all__ = [
    "MAXK_SELECTION_PLAN_SCHEMA",
    "MAXK_SELECTION_PLAN_VERSION",
    "MaterializedBudgetSelection",
    "materialize_budget_selection",
    "normalize_budgets",
]
