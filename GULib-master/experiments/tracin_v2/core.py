"""Pure scoring primitives for the UNSTABLE TracIn V2 gates."""

from __future__ import annotations

from numbers import Integral
from typing import Iterable, Sequence, Tuple

import torch
from torch import Tensor


def _validate_trajectory(
    candidate_gradients: Sequence[Tensor],
    target_gradients: Sequence[Tensor],
    checkpoint_weights: Sequence[float],
) -> Tuple[int, torch.dtype, torch.device]:
    if not candidate_gradients:
        raise ValueError("at least one checkpoint is required")
    if not (
        len(candidate_gradients)
        == len(target_gradients)
        == len(checkpoint_weights)
    ):
        raise ValueError(
            "candidate gradients, target gradients, and weights must have "
            "the same checkpoint count"
        )

    first = candidate_gradients[0]
    if first.ndim != 2:
        raise ValueError("candidate gradients must have shape [N, P]")
    num_candidates, num_parameters = first.shape
    if num_candidates <= 0 or num_parameters <= 0:
        raise ValueError("candidate gradient matrices must be non-empty")

    for index, (matrix, target, weight) in enumerate(
        zip(candidate_gradients, target_gradients, checkpoint_weights)
    ):
        if matrix.ndim != 2 or tuple(matrix.shape) != (
            num_candidates,
            num_parameters,
        ):
            raise ValueError(
                "checkpoint {0} candidate gradients have inconsistent shape".format(
                    index
                )
            )
        if target.ndim != 1 or target.numel() != num_parameters:
            raise ValueError(
                "checkpoint {0} target gradient must have shape [P]".format(index)
            )
        if matrix.dtype != first.dtype or target.dtype != first.dtype:
            raise ValueError("all gradients must share one dtype")
        if matrix.device != first.device or target.device != first.device:
            raise ValueError("all gradients must share one device")
        if not torch.isfinite(matrix).all() or not torch.isfinite(target).all():
            raise ValueError("gradient inputs must be finite")
        if isinstance(weight, bool):
            raise ValueError("checkpoint weights must be non-negative finite scalars")
        weight_tensor = torch.as_tensor(weight, dtype=first.dtype, device=first.device)
        if (
            weight_tensor.ndim != 0
            or not torch.isfinite(weight_tensor)
            or weight_tensor.item() < 0
        ):
            raise ValueError("checkpoint weights must be non-negative finite scalars")

    return num_candidates, first.dtype, first.device


def tracin_cp_eval_scores(
    candidate_gradients: Sequence[Tensor],
    target_gradients: Sequence[Tensor],
    checkpoint_weights: Sequence[float],
) -> Tensor:
    """Compute sum_c w_c <g_v(theta_c), g_E(theta_c)> for every candidate."""

    num_candidates, dtype, device = _validate_trajectory(
        candidate_gradients, target_gradients, checkpoint_weights
    )
    scores = torch.zeros(num_candidates, dtype=dtype, device=device)
    for matrix, target, weight in zip(
        candidate_gradients, target_gradients, checkpoint_weights
    ):
        scores = scores + torch.as_tensor(
            weight, dtype=dtype, device=device
        ) * matrix.mv(target)
    if not torch.isfinite(scores).all():
        raise ValueError("TracInCP eval scores must be finite")
    return scores


def tracin_cp_self_scores(
    candidate_gradients: Sequence[Tensor], checkpoint_weights: Sequence[float]
) -> Tensor:
    """Compute sum_c w_c ||g_v(theta_c)||^2 for every candidate."""

    zero_targets = [
        torch.zeros(matrix.shape[1], dtype=matrix.dtype, device=matrix.device)
        for matrix in candidate_gradients
    ]
    num_candidates, dtype, device = _validate_trajectory(
        candidate_gradients, zero_targets, checkpoint_weights
    )
    scores = torch.zeros(num_candidates, dtype=dtype, device=device)
    for matrix, weight in zip(candidate_gradients, checkpoint_weights):
        scores = scores + torch.as_tensor(
            weight, dtype=dtype, device=device
        ) * matrix.square().sum(dim=1)
    if not torch.isfinite(scores).all():
        raise ValueError("TracInCP self scores must be finite")
    return scores


def deployed_cross_gradient_scores(candidate_gradients: Tensor) -> Tensor:
    """Replay the legacy final-point score -g_v dot sum_j g_j."""

    if candidate_gradients.ndim != 2 or candidate_gradients.numel() == 0:
        raise ValueError("candidate gradients must be a non-empty [N, P] matrix")
    if not torch.isfinite(candidate_gradients).all():
        raise ValueError("candidate gradients must be finite")
    return -candidate_gradients.mv(candidate_gradients.sum(dim=0))


def stable_topk(candidate_ids: Iterable[int], scores: Tensor, k: int) -> Tuple[int, ...]:
    """Rank by score descending, then node ID ascending."""

    raw_ids = tuple(candidate_ids)
    if any(isinstance(node_id, bool) or not isinstance(node_id, Integral) for node_id in raw_ids):
        raise ValueError("candidate IDs must be integer values, not coerced strings/floats/bools")
    ids = tuple(int(node_id) for node_id in raw_ids)
    if scores.ndim != 1 or scores.numel() != len(ids):
        raise ValueError("scores must have one value for each candidate ID")
    if len(set(ids)) != len(ids):
        raise ValueError("candidate IDs must be unique")
    if isinstance(k, bool) or not isinstance(k, int) or not 0 < k <= len(ids):
        raise ValueError("k must be an integer in [1, number of candidates]")
    if not torch.isfinite(scores).all():
        raise ValueError("scores must be finite")

    order = sorted(
        range(len(ids)), key=lambda index: (-float(scores[index].item()), ids[index])
    )
    return tuple(ids[index] for index in order[:k])
