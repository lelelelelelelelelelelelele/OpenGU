"""CPU scoring primitives for the current target-direct selector lane."""

from __future__ import annotations

import math
import time
from typing import Any, Dict, List, Mapping, Sequence, Tuple

import torch
import torch.nn.functional as F
from torch import Tensor

from experiments.c_target_v1.core import (
    GateGCN,
    capture_state,
    flatten,
    model_parameters,
    preserve_model_state_and_mode,
    seed_everything,
    state_hash,
    train_trajectory,
)
from experiments.c_target_v1.core import graph_source_scores


def checkpoint_view_indices(checkpoint_count: int) -> Dict[str, Tuple[int, ...]]:
    if checkpoint_count < 3:
        raise ValueError("at least three checkpoints are required")
    return {
        "single": (checkpoint_count - 1,),
        "cp3": (0, checkpoint_count // 2, checkpoint_count - 1),
        "cp_all": tuple(range(checkpoint_count)),
    }


def weighted_checkpoint_scores(
    score_vectors: Sequence[Tensor],
    weights: Sequence[float],
    indices: Sequence[int],
) -> Tensor:
    if not score_vectors or len(score_vectors) != len(weights):
        raise ValueError("score vectors and weights must be aligned")
    first = score_vectors[0]
    if first.ndim != 1:
        raise ValueError("checkpoint scores must be vectors")
    result = torch.zeros_like(first)
    for index in indices:
        if index < 0 or index >= len(score_vectors):
            raise ValueError("checkpoint index is out of range")
        current = score_vectors[index]
        weight = float(weights[index])
        if current.shape != first.shape or not math.isfinite(weight) or weight < 0:
            raise ValueError("invalid checkpoint score or weight")
        result = result + weight * current
    if not torch.isfinite(result).all():
        raise ValueError("weighted checkpoint scores contain non-finite values")
    return result


def _unflatten_vector(vector: Tensor, parameters: Sequence[Tensor]) -> List[Tensor]:
    if vector.ndim != 1:
        raise ValueError("inverse-Hessian source must be a vector")
    parts: List[Tensor] = []
    offset = 0
    for parameter in parameters:
        size = parameter.numel()
        parts.append(
            vector[offset : offset + size]
            .to(device=parameter.device, dtype=parameter.dtype)
            .reshape_as(parameter)
        )
        offset += size
    if offset != vector.numel():
        raise ValueError("inverse-Hessian vector does not match parameter schema")
    return parts


def inverse_hessian_vectors(
    model: GateGCN,
    data,
    *,
    state: Mapping[str, Tensor],
    hessian_train_ids: Tensor,
    parameter_scope: str,
    vectors: Tensor,
    iterations: int,
    scale: float,
    damp: float,
) -> Tuple[Tensor, Dict[str, float]]:
    """Apply the same LiSSA approximation to multiple parameter-space vectors."""

    if vectors.ndim != 2 or vectors.shape[0] == 0:
        raise ValueError("vectors must be a non-empty matrix")
    if iterations <= 0 or scale <= 0 or not 0 <= damp < 1:
        raise ValueError("invalid LiSSA parameters")
    started = time.perf_counter()
    rows: List[Tensor] = []
    with preserve_model_state_and_mode(model):
        model.load_state_dict(state)
        model.eval()
        params = model_parameters(model, parameter_scope)
        expected_width = sum(parameter.numel() for parameter in params)
        if vectors.shape[1] != expected_width:
            raise ValueError("vector matrix does not match parameter schema")

        train_logits = model(data.x, data.edge_index)
        train_loss = F.cross_entropy(
            train_logits[hessian_train_ids],
            data.y[hessian_train_ids],
            reduction="mean",
        )
        train_gradient = torch.autograd.grad(
            train_loss, params, create_graph=True
        )

        for row in vectors:
            source = [part.detach() for part in _unflatten_vector(row, params)]
            estimate = [part.clone() for part in source]
            for _ in range(iterations):
                product = sum(
                    (gradient * vector).sum()
                    for gradient, vector in zip(train_gradient, estimate)
                )
                hvp = torch.autograd.grad(product, params, retain_graph=True)
                estimate = [
                    original
                    + (1.0 - damp) * previous
                    - curvature.detach() / scale
                    for original, previous, curvature in zip(
                        source, estimate, hvp
                    )
                ]
            rows.append(
                flatten([part.detach() / scale for part in estimate]).cpu()
            )
    matrix = torch.stack(rows)
    if not torch.isfinite(matrix).all():
        raise ValueError("inverse-Hessian matrix contains non-finite values")
    return matrix, {
        "vector_count": int(vectors.shape[0]),
        "seconds": time.perf_counter() - started,
        "output_norm_mean": float(matrix.norm(dim=1).mean().item()),
        "output_norm_max": float(matrix.norm(dim=1).max().item()),
    }


def hutchinson_parameter_change_scores(
    candidate_gradients: Tensor, inverse_probes: Tensor
) -> Tensor:
    if (
        candidate_gradients.ndim != 2
        or inverse_probes.ndim != 2
        or candidate_gradients.shape[1] != inverse_probes.shape[1]
        or inverse_probes.shape[0] == 0
    ):
        raise ValueError("candidate gradients and inverse probes are invalid")
    projections = candidate_gradients.mm(inverse_probes.t())
    scores = projections.square().mean(dim=1).clamp_min(0).sqrt()
    if not torch.isfinite(scores).all():
        raise ValueError("Hutchinson parameter-change scores are non-finite")
    return scores


def degree_scores(
    edge_index: Tensor, candidate_ids: Tensor, num_nodes: int
) -> Tensor:
    degree = torch.bincount(edge_index[0], minlength=int(num_nodes))
    return degree[candidate_ids].to(dtype=torch.float64)


def deterministic_random_scores(candidate_count: int, seed: int) -> Tensor:
    if candidate_count <= 0:
        raise ValueError("candidate_count must be positive")
    generator = torch.Generator(device="cpu")
    generator.manual_seed(int(seed))
    return torch.rand(candidate_count, generator=generator, dtype=torch.float64)


def remove_selected_nodes(
    edge_index: Tensor,
    train_mask: Tensor,
    selected_nodes: Sequence[int],
) -> Tuple[Tensor, Tensor]:
    selected = tuple(int(value) for value in selected_nodes)
    if len(set(selected)) != len(selected):
        raise ValueError("selected node ids must be unique")
    clean_train_mask = train_mask.clone()
    if selected:
        selected_tensor = torch.as_tensor(
            selected, dtype=torch.long, device=train_mask.device
        )
        if selected_tensor.min().item() < 0 or selected_tensor.max().item() >= train_mask.numel():
            raise ValueError("selected node id is out of range")
        if not bool(train_mask[selected_tensor].all().item()):
            raise ValueError("every selected node must belong to train_mask")
        clean_train_mask[selected_tensor] = False
        membership = torch.zeros(
            train_mask.numel(), dtype=torch.bool, device=edge_index.device
        )
        membership[selected_tensor.to(edge_index.device)] = True
        keep = ~membership[edge_index[0]] & ~membership[edge_index[1]]
        clean_edge_index = edge_index[:, keep]
    else:
        clean_edge_index = edge_index.clone()
    return clean_edge_index, clean_train_mask


def evaluate_model(model: GateGCN, data) -> Dict[str, float]:
    model.eval()
    with torch.no_grad():
        logits = model(data.x, data.edge_index)
    metrics: Dict[str, float] = {}
    for name, mask in (
        ("train", data.train_mask),
        ("validation", data.val_mask),
        ("test", data.test_mask),
    ):
        loss = F.cross_entropy(
            logits[mask], data.y[mask], reduction="mean"
        )
        accuracy = (
            logits[mask].argmax(dim=-1) == data.y[mask]
        ).float().mean()
        metrics["{0}_loss".format(name)] = float(loss.item())
        metrics["{0}_accuracy".format(name)] = float(accuracy.item())
    return metrics


def train_model_once(
    data,
    *,
    in_channels: int,
    hidden_channels: int,
    out_channels: int,
    dropout: float,
    seed: int,
    num_threads: int,
    epochs: int,
    lr: float,
    weight_decay: float,
    milestones: Sequence[int],
    gamma: float,
    optimizer_name: str,
) -> Tuple[GateGCN, Dict[str, object]]:
    seed_everything(seed, num_threads)
    model = GateGCN(
        int(in_channels),
        int(hidden_channels),
        int(out_channels),
        float(dropout),
    )
    checkpoints, observation = train_trajectory(
        model,
        data,
        checkpoint_epochs=(int(epochs),),
        epochs=int(epochs),
        lr=float(lr),
        weight_decay=float(weight_decay),
        milestones=tuple(int(value) for value in milestones),
        gamma=float(gamma),
        optimizer_name=optimizer_name,
    )
    final_state = checkpoints[-1]["state"]
    model.load_state_dict(final_state)
    return model, {
        "state_hash": state_hash(final_state),
        "training": observation,
        "metrics": evaluate_model(model, data),
    }


def state_copy(model: GateGCN) -> Dict[str, Tensor]:
    return capture_state(model)


def checkpoint_graph_scores(
    model: GateGCN,
    data,
    *,
    checkpoints,
    candidate_ids: Tensor,
    source_ids: Tensor,
    target_gradients,
    parameter_scope: str,
    affected_hops: int,
    final_inverse_target: Tensor,
) -> Dict[str, Any]:
    """Evaluate point and graph sources over one checkpoint trajectory."""

    simple_vectors = []
    graph_vectors = []
    observations = []
    final_index = len(checkpoints) - 1
    final_scores = None
    final_observation = None
    for index, item in enumerate(checkpoints):
        target = target_gradients[index]
        inverse = final_inverse_target if index == final_index else target
        scores, observation = graph_source_scores(
            model,
            data,
            state=item["state"],
            candidate_ids=candidate_ids,
            source_ids=source_ids,
            parameter_scope=parameter_scope,
            affected_hops=affected_hops,
            target_gradient=target,
            inverse_target=inverse,
        )
        simple_vectors.append(scores["p_simple"].to(torch.float64))
        graph_vectors.append(scores["p_graph"].to(torch.float64))
        observations.append(
            {
                "global_step": int(item["global_step"]),
                "seconds": float(observation["graph_source_seconds"]),
                "affected_size_min": int(observation["affected_size_min"]),
                "affected_size_mean": float(observation["affected_size_mean"]),
                "affected_size_max": int(observation["affected_size_max"]),
            }
        )
        if index == final_index:
            final_scores = scores
            final_observation = observation
    if final_scores is None or final_observation is None:
        raise RuntimeError("final graph source scores were not produced")
    return {
        "simple_vectors": simple_vectors,
        "graph_vectors": graph_vectors,
        "final_scores": final_scores,
        "final_observation": final_observation,
        "checkpoint_observations": observations,
    }
