"""Deterministic CPU primitives for the C-target approximation experiment."""

from __future__ import annotations

import contextlib
import hashlib
import json
import math
import random
import time
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple, Union

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import kendalltau, spearmanr
from torch import Tensor, nn
from torch_geometric.nn import GCNConv


class GateGCN(nn.Module):
    """Small two-layer GCN used only by the isolated local gate."""

    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        dropout: float,
    ) -> None:
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)
        self.dropout = float(dropout)

    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def tensor_hash(tensor: Tensor) -> str:
    value = tensor.detach().cpu().contiguous()
    header = json.dumps(
        {"dtype": str(value.dtype), "shape": list(value.shape)},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(header + value.numpy().tobytes(order="C"))


def ids_hash(ids: Union[Sequence[int], Tensor]) -> str:
    value = torch.as_tensor(ids, dtype=torch.int64).detach().cpu().contiguous()
    return tensor_hash(value)


def state_hash(state: Mapping[str, Tensor]) -> str:
    digest = hashlib.sha256()
    for name in sorted(state):
        name_bytes = name.encode("utf-8")
        value_bytes = bytes.fromhex(tensor_hash(state[name]))
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(value_bytes).to_bytes(8, "big"))
        digest.update(value_bytes)
    return digest.hexdigest()


def source_fingerprint(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        name_bytes = path.name.encode("utf-8")
        source_bytes = (
            path.read_text(encoding="utf-8")
            .replace("\r\n", "\n")
            .encode("utf-8")
        )
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(source_bytes).to_bytes(8, "big"))
        digest.update(source_bytes)
    return digest.hexdigest()


def flatten(items: Sequence[Tensor]) -> Tensor:
    return torch.cat([item.reshape(-1) for item in items])


def seed_everything(seed: int, num_threads: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(num_threads)
    torch.use_deterministic_algorithms(True)


def model_parameters(model: nn.Module, scope: str) -> List[nn.Parameter]:
    if scope == "last_layer":
        if hasattr(model, "conv2"):
            module = model.conv2
        elif hasattr(model, "convs") and len(model.convs) > 0:
            module = model.convs[-1]
        else:
            raise ValueError("model has no recognized final GNN layer")
        return [
            parameter
            for parameter in module.parameters()
            if parameter.requires_grad
        ]
    if scope != "all_trainable":
        raise ValueError("parameter scope must be all_trainable or last_layer")
    return [parameter for parameter in model.parameters() if parameter.requires_grad]


def parameter_schema_hash(model: nn.Module, scope: str) -> str:
    last_layer_prefixes = ("conv2.",)
    if hasattr(model, "convs") and len(model.convs) > 0:
        last_layer_prefixes = (
            "convs.{0}.".format(len(model.convs) - 1),
        )
    entries = []
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        if scope == "last_layer" and not name.startswith(last_layer_prefixes):
            continue
        entries.append(
            {
                "name": name,
                "shape": list(parameter.shape),
                "dtype": str(parameter.dtype),
            }
        )
    return sha256_bytes(
        json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )


def capture_state(model: nn.Module) -> Dict[str, Tensor]:
    return {
        name: value.detach().cpu().clone()
        for name, value in model.state_dict().items()
    }


@contextlib.contextmanager
def preserve_model_state_and_mode(model: nn.Module):
    original_state = capture_state(model)
    was_training = model.training
    try:
        yield
    finally:
        model.load_state_dict(original_state)
        model.train(was_training)


def train_trajectory(
    model: nn.Module,
    data,
    *,
    checkpoint_epochs: Sequence[int],
    epochs: int,
    lr: float,
    weight_decay: float,
    milestones: Sequence[int],
    gamma: float,
    optimizer_name: str = "sgd",
) -> Tuple[List[Dict[str, object]], Dict[str, float]]:
    normalized_optimizer = optimizer_name.strip().lower()
    if normalized_optimizer == "sgd":
        optimizer = torch.optim.SGD(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )
    elif normalized_optimizer == "adam":
        optimizer = torch.optim.Adam(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )
    else:
        raise ValueError("optimizer_name must be sgd or adam")
    scheduler = torch.optim.lr_scheduler.MultiStepLR(
        optimizer, milestones=list(milestones), gamma=gamma
    )
    wanted = set(int(epoch) for epoch in checkpoint_epochs)
    checkpoints: List[Dict[str, object]] = []
    started = time.perf_counter()
    last_loss = float("nan")

    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(data.x, data.edge_index)
        loss = F.cross_entropy(
            logits[data.train_mask], data.y[data.train_mask], reduction="mean"
        )
        loss.backward()
        update_lr = float(optimizer.param_groups[0]["lr"])
        optimizer.step()
        scheduler.step()
        last_loss = float(loss.item())
        if epoch in wanted:
            state = capture_state(model)
            checkpoints.append(
                {
                    "epoch": int(epoch),
                    "global_step": int(epoch),
                    "update_lr": update_lr,
                    "state_hash": state_hash(state),
                    "state": state,
                }
            )

    observed = tuple(int(item["epoch"]) for item in checkpoints)
    expected = tuple(int(epoch) for epoch in checkpoint_epochs)
    if observed != expected:
        raise RuntimeError(
            "checkpoint capture mismatch: expected {0}, observed {1}".format(
                expected, observed
            )
        )
    return checkpoints, {
        "training_seconds": time.perf_counter() - started,
        "final_train_loss": last_loss,
        "optimizer": normalized_optimizer,
    }


def checkpoint_point_gradients(
    model: nn.Module,
    data,
    *,
    state: Mapping[str, Tensor],
    candidate_ids: Tensor,
    target_ids: Tensor,
    parameter_scope: str,
) -> Tuple[Tensor, Tensor]:
    with preserve_model_state_and_mode(model):
        model.load_state_dict(state)
        model.eval()
        params = model_parameters(model, parameter_scope)

        target_logits = model(data.x, data.edge_index)
        target_loss = F.cross_entropy(
            target_logits[target_ids], data.y[target_ids], reduction="mean"
        )
        target_gradient = flatten(
            torch.autograd.grad(target_loss, params)
        ).detach()

        candidate_logits = model(data.x, data.edge_index)
        rows: List[Tensor] = []
        raw_ids = candidate_ids.detach().cpu().tolist()
        for index, node_id in enumerate(raw_ids):
            loss = F.cross_entropy(
                candidate_logits[node_id : node_id + 1],
                data.y[node_id : node_id + 1],
                reduction="mean",
            )
            gradient = torch.autograd.grad(
                loss,
                params,
                retain_graph=index < len(raw_ids) - 1,
            )
            rows.append(flatten(gradient).detach())
        matrix = torch.stack(rows)
        if not torch.isfinite(matrix).all() or not torch.isfinite(
            target_gradient
        ).all():
            raise ValueError("point or target gradients contain non-finite values")
        return matrix, target_gradient


def inverse_hessian_target(
    model: nn.Module,
    data,
    *,
    state: Mapping[str, Tensor],
    hessian_train_ids: Tensor,
    target_ids: Tensor,
    parameter_scope: str,
    iterations: int,
    scale: float,
    damp: float,
) -> Tuple[Tensor, Tensor, Dict[str, float]]:
    if iterations <= 0 or scale <= 0 or not 0 <= damp < 1:
        raise ValueError("invalid LiSSA parameters")
    started = time.perf_counter()
    with preserve_model_state_and_mode(model):
        model.load_state_dict(state)
        model.eval()
        params = model_parameters(model, parameter_scope)

        train_logits = model(data.x, data.edge_index)
        train_loss = F.cross_entropy(
            train_logits[hessian_train_ids],
            data.y[hessian_train_ids],
            reduction="mean",
        )
        train_gradient = torch.autograd.grad(
            train_loss, params, create_graph=True
        )

        target_logits = model(data.x, data.edge_index)
        target_loss = F.cross_entropy(
            target_logits[target_ids], data.y[target_ids], reduction="mean"
        )
        target_gradient_parts = [
            value.detach()
            for value in torch.autograd.grad(target_loss, params)
        ]
        estimate = [value.clone() for value in target_gradient_parts]

        for _ in range(iterations):
            product = sum(
                (gradient * vector).sum()
                for gradient, vector in zip(train_gradient, estimate)
            )
            hvp = torch.autograd.grad(product, params, retain_graph=True)
            estimate = [
                source
                + (1.0 - damp) * previous
                - curvature.detach() / scale
                for source, previous, curvature in zip(
                    target_gradient_parts, estimate, hvp
                )
            ]

        target_gradient = flatten(target_gradient_parts).detach()
        inverse_target = flatten(
            [value.detach() / scale for value in estimate]
        )
        if not torch.isfinite(inverse_target).all():
            raise ValueError("LiSSA inverse target contains non-finite values")
        return target_gradient, inverse_target, {
            "ihvp_seconds": time.perf_counter() - started,
            "target_gradient_norm": float(target_gradient.norm().item()),
            "inverse_target_norm": float(inverse_target.norm().item()),
        }


def build_undirected_adjacency(edge_index: Tensor, num_nodes: int) -> List[Set[int]]:
    adjacency = [set() for _ in range(int(num_nodes))]
    source = edge_index[0].detach().cpu().tolist()
    target = edge_index[1].detach().cpu().tolist()
    for left, right in zip(source, target):
        if left == right:
            continue
        adjacency[int(left)].add(int(right))
        adjacency[int(right)].add(int(left))
    return adjacency


def affected_nodes(
    adjacency: Sequence[Set[int]], node_id: int, hops: int
) -> Tuple[int, ...]:
    if hops < 0:
        raise ValueError("affected hops must be non-negative")
    visited = {int(node_id)}
    frontier = {int(node_id)}
    for _ in range(hops):
        next_frontier = set()
        for current in frontier:
            next_frontier.update(adjacency[current])
        next_frontier.difference_update(visited)
        if not next_frontier:
            break
        visited.update(next_frontier)
        frontier = next_frontier
    return tuple(sorted(visited))


def remove_incident_edges(edge_index: Tensor, node_id: int) -> Tensor:
    keep = (edge_index[0] != int(node_id)) & (edge_index[1] != int(node_id))
    return edge_index[:, keep]


def graph_source_scores(
    model: nn.Module,
    data,
    *,
    state: Mapping[str, Tensor],
    candidate_ids: Tensor,
    source_ids: Tensor,
    parameter_scope: str,
    affected_hops: int,
    target_gradient: Tensor,
    inverse_target: Tensor,
) -> Tuple[Dict[str, Tensor], Dict[str, object]]:
    started = time.perf_counter()
    with preserve_model_state_and_mode(model):
        model.load_state_dict(state)
        model.eval()
        params = model_parameters(model, parameter_scope)
        adjacency = build_undirected_adjacency(
            data.edge_index, int(data.num_nodes)
        )
        original_logits = model(data.x, data.edge_index)
        candidate_list = [int(value) for value in candidate_ids.cpu().tolist()]
        source_list = [int(value) for value in source_ids.cpu().tolist()]
        source_set = set(source_list)

        gt_simple: List[float] = []
        gt_full: List[float] = []
        p_simple: List[float] = []
        p_graph: List[float] = []
        affected_sizes: List[int] = []

        for position, node_id in enumerate(candidate_list):
            affected = affected_nodes(adjacency, node_id, affected_hops)
            affected_source = tuple(
                value for value in affected if value in source_set
            )
            source_neighbors = tuple(
                value for value in affected_source if value != node_id
            )
            affected_source_tensor = torch.as_tensor(
                affected_source, dtype=torch.long, device=data.y.device
            )
            loss1 = F.cross_entropy(
                original_logits[affected_source_tensor],
                data.y[affected_source_tensor],
                reduction="sum",
            )
            grad1 = flatten(
                torch.autograd.grad(
                    loss1,
                    params,
                    retain_graph=position < len(candidate_list) - 1,
                )
            ).detach()

            if source_neighbors:
                deleted_edge_index = remove_incident_edges(
                    data.edge_index, node_id
                )
                deleted_logits = model(data.x, deleted_edge_index)
                neighbor_tensor = torch.as_tensor(
                    source_neighbors, dtype=torch.long, device=data.y.device
                )
                loss2 = F.cross_entropy(
                    deleted_logits[neighbor_tensor],
                    data.y[neighbor_tensor],
                    reduction="sum",
                )
                grad2 = flatten(torch.autograd.grad(loss2, params)).detach()
            else:
                grad2 = torch.zeros_like(grad1)

            full_source = grad1 - grad2
            gt_simple.append(float(torch.dot(grad1, inverse_target).item()))
            gt_full.append(float(torch.dot(full_source, inverse_target).item()))
            p_simple.append(float(torch.dot(grad1, target_gradient).item()))
            p_graph.append(float(torch.dot(full_source, target_gradient).item()))
            affected_sizes.append(len(affected))

    scores = {
        "gt_simple": torch.tensor(gt_simple, dtype=torch.float64),
        "gt_full": torch.tensor(gt_full, dtype=torch.float64),
        "p_simple": torch.tensor(p_simple, dtype=torch.float64),
        "p_graph": torch.tensor(p_graph, dtype=torch.float64),
    }
    if any(not torch.isfinite(value).all() for value in scores.values()):
        raise ValueError("graph source scores contain non-finite values")
    return scores, {
        "graph_source_seconds": time.perf_counter() - started,
        "affected_hops": int(affected_hops),
        "affected_sizes": affected_sizes,
        "affected_size_min": min(affected_sizes),
        "affected_size_max": max(affected_sizes),
        "affected_size_mean": float(np.mean(affected_sizes)),
    }


def tracin_cp_eval_scores(
    candidate_gradients: Sequence[Tensor],
    target_gradients: Sequence[Tensor],
    checkpoint_weights: Sequence[float],
) -> Tensor:
    if not candidate_gradients or not (
        len(candidate_gradients)
        == len(target_gradients)
        == len(checkpoint_weights)
    ):
        raise ValueError("trajectory inputs must have equal non-zero length")
    first = candidate_gradients[0]
    if first.ndim != 2:
        raise ValueError("candidate gradients must be matrices")
    scores = torch.zeros(
        first.shape[0], dtype=first.dtype, device=first.device
    )
    for matrix, target, weight in zip(
        candidate_gradients, target_gradients, checkpoint_weights
    ):
        if (
            matrix.shape != first.shape
            or target.ndim != 1
            or target.shape[0] != first.shape[1]
            or not math.isfinite(float(weight))
            or float(weight) < 0
        ):
            raise ValueError("invalid checkpoint gradient or weight")
        scores = scores + float(weight) * matrix.mv(target)
    if not torch.isfinite(scores).all():
        raise ValueError("TracInCP scores contain non-finite values")
    return scores


def deployed_cross_gradient_scores(candidate_gradients: Tensor) -> Tensor:
    if candidate_gradients.ndim != 2:
        raise ValueError("candidate gradients must be a matrix")
    return -candidate_gradients.mv(candidate_gradients.sum(dim=0))


def stable_ranking(candidate_ids: Iterable[int], scores: Tensor) -> Tuple[int, ...]:
    ids = tuple(int(value) for value in candidate_ids)
    if len(set(ids)) != len(ids):
        raise ValueError("candidate ids must be unique")
    if scores.ndim != 1 or scores.numel() != len(ids):
        raise ValueError("scores must align with candidate ids")
    if not torch.isfinite(scores).all():
        raise ValueError("scores must be finite")
    order = sorted(
        range(len(ids)),
        key=lambda index: (-float(scores[index].item()), ids[index]),
    )
    return tuple(ids[index] for index in order)


def _finite_or_none(value: float) -> Optional[float]:
    return float(value) if math.isfinite(float(value)) else None


def pair_metrics(
    reference_scores: Sequence[float],
    candidate_scores: Sequence[float],
    reference_ranking: Sequence[int],
    candidate_ranking: Sequence[int],
    k: int,
) -> Dict[str, Union[float, int, None]]:
    ref = np.asarray(reference_scores, dtype=np.float64)
    cand = np.asarray(candidate_scores, dtype=np.float64)
    if ref.shape != cand.shape or ref.ndim != 1:
        raise ValueError("metric score arrays must be aligned vectors")
    ref_top = set(int(value) for value in reference_ranking[:k])
    cand_top = set(int(value) for value in candidate_ranking[:k])
    intersection = len(ref_top & cand_top)
    union = len(ref_top | cand_top)
    spearman = spearmanr(ref, cand).statistic
    kendall = kendalltau(ref, cand).statistic
    return {
        "k": int(k),
        "intersection": int(intersection),
        "union": int(union),
        "jaccard": float(intersection / union) if union else 1.0,
        "common_fraction": float(intersection / k) if k else 1.0,
        "spearman": _finite_or_none(spearman),
        "kendall": _finite_or_none(kendall),
        "sign_agreement": float(np.mean(np.signbit(ref) == np.signbit(cand))),
    }
