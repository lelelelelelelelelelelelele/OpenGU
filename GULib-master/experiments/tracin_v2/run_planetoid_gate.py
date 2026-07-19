"""Run an isolated Planetoid gate for the UNSTABLE TracIn V2 scorer.

This script does not call the attack runner and does not read or write any
Legacy Result/Selection/Score cache.  Its JSON output is a diagnostic gate
report, not a formal Cache V2 ScoreArtifact.
"""

from __future__ import annotations

import argparse
import copy
import contextlib
import hashlib
import json
import os
import platform
import random
import socket
import tempfile
import time
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np
import torch
import torch.nn.functional as F
import torch_geometric
from scipy.stats import kendalltau, spearmanr
from torch import Tensor, nn
from torch_geometric.datasets import Planetoid
from torch_geometric.nn import GATConv, GCNConv
from torch_geometric.transforms import NormalizeFeatures

from experiments.tracin_v2.core import (
    deployed_cross_gradient_scores,
    stable_topk,
    tracin_cp_eval_scores,
    tracin_cp_self_scores,
)
from experiments.tracin_v2.recipe import build_unstable_recipe


class GateGCN(nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int, dropout: float):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)
        self.dropout = float(dropout)

    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        x = self.conv1(x, edge_index).relu()
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


class GateGAT(nn.Module):
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        dropout: float,
        heads: int,
    ):
        super().__init__()
        self.conv1 = GATConv(
            in_channels,
            hidden_channels,
            heads=heads,
            dropout=dropout,
        )
        self.conv2 = GATConv(
            hidden_channels * heads,
            out_channels,
            heads=1,
            concat=False,
            dropout=dropout,
        )
        self.dropout = float(dropout)

    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = F.elu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


PLANETOID_NAMES = {
    "cora": "Cora",
    "citeseer": "CiteSeer",
    "pubmed": "PubMed",
}


def canonical_dataset_name(value: str) -> str:
    try:
        return PLANETOID_NAMES[value.strip().lower()]
    except KeyError as exc:
        raise argparse.ArgumentTypeError(
            "dataset must be one of: Cora, CiteSeer, PubMed"
        ) from exc


def build_model(
    architecture: str,
    in_channels: int,
    hidden_channels: int,
    out_channels: int,
    dropout: float,
    gat_heads: int,
) -> nn.Module:
    if architecture == "gcn":
        return GateGCN(in_channels, hidden_channels, out_channels, dropout)
    if architecture == "gat":
        return GateGAT(
            in_channels,
            hidden_channels,
            out_channels,
            dropout,
            gat_heads,
        )
    raise ValueError("unsupported architecture: {0}".format(architecture))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dataset", type=canonical_dataset_name, default="Cora")
    parser.add_argument("--model", choices=("gcn", "gat"), default="gcn")
    parser.add_argument("--seed", type=int, default=2024)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--checkpoint-epochs", default="1,5,10,20,30")
    parser.add_argument("--hidden-channels", type=int, default=16)
    parser.add_argument("--gat-heads", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--optimizer", choices=("sgd", "adam"), default="sgd")
    parser.add_argument("--lr", type=float, default=None)
    parser.add_argument("--weight-decay", type=float, default=5e-4)
    parser.add_argument("--lr-milestones", default="50,80")
    parser.add_argument("--lr-gamma", type=float, default=0.5)
    parser.add_argument(
        "--target-profile",
        choices=("attack_safe_holdout", "diagnostic_test_labels"),
        default="attack_safe_holdout",
    )
    parser.add_argument("--parameter-scope", choices=("all_trainable", "last_layer"), default="all_trainable")
    parser.add_argument("--candidate-limit", type=int, default=0)
    parser.add_argument(
        "--topk",
        type=int,
        default=0,
        help="exact selection budget; 0 uses --topk-ratio",
    )
    parser.add_argument("--topk-ratio", type=float, default=0.05)
    parser.add_argument("--lissa-iter", type=int, default=20)
    parser.add_argument("--lissa-scale", type=float, default=25.0)
    parser.add_argument("--lissa-damp", type=float, default=0.01)
    parser.add_argument("--num-threads", type=int, default=1)
    return parser


def parse_ints(value: str) -> Tuple[int, ...]:
    if not value.strip():
        return tuple()
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


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


def ids_hash(ids: Tensor) -> str:
    return tensor_hash(ids.detach().cpu().to(torch.int64).contiguous())


def source_fingerprint(paths: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.as_posix()):
        name_bytes = path.name.encode("utf-8")
        source_bytes = path.read_text(encoding="utf-8").replace("\r\n", "\n").encode("utf-8")
        digest.update(len(name_bytes).to_bytes(8, "big"))
        digest.update(name_bytes)
        digest.update(len(source_bytes).to_bytes(8, "big"))
        digest.update(source_bytes)
    return digest.hexdigest()


def flatten(items: Sequence[Tensor]) -> Tensor:
    return torch.cat([item.reshape(-1) for item in items])


def model_parameters(model: nn.Module, scope: str) -> List[nn.Parameter]:
    if scope == "last_layer":
        return [parameter for parameter in model.conv2.parameters() if parameter.requires_grad]
    return [parameter for parameter in model.parameters() if parameter.requires_grad]


def parameter_schema_hash(model: nn.Module, scope: str) -> str:
    entries = []
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        if scope == "last_layer" and not name.startswith("conv2."):
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


def seed_everything(seed: int, num_threads: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(num_threads)
    torch.use_deterministic_algorithms(True)


def train_trajectory(
    model: nn.Module,
    data,
    checkpoint_epochs: Sequence[int],
    epochs: int,
    optimizer_name: str,
    lr: float,
    weight_decay: float,
    milestones: Sequence[int],
    gamma: float,
) -> Tuple[List[Dict[str, object]], Dict[str, float]]:
    if optimizer_name == "sgd":
        optimizer = torch.optim.SGD(model.parameters(), lr=lr, weight_decay=weight_decay)
    else:
        optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(
        optimizer, milestones=list(milestones), gamma=gamma
    )
    wanted = set(checkpoint_epochs)
    checkpoints: List[Dict[str, object]] = []

    def record(epoch: int, update_lr: float) -> None:
        state = capture_state(model)
        checkpoints.append(
            {
                "epoch": int(epoch),
                "global_step": int(epoch),
                "update_lr": float(update_lr),
                "state_hash": state_hash(state),
                "state": state,
            }
        )

    last_loss = float("nan")
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(data.x, data.edge_index)
        loss = F.cross_entropy(logits[data.train_mask], data.y[data.train_mask])
        loss.backward()
        update_lr = float(optimizer.param_groups[0]["lr"])
        optimizer.step()
        scheduler.step()
        last_loss = float(loss.item())
        if epoch in wanted:
            record(epoch, update_lr)

    if tuple(item["epoch"] for item in checkpoints) != tuple(checkpoint_epochs):
        raise RuntimeError("checkpoint capture did not match the requested ordered schedule")
    return checkpoints, {"final_train_loss": last_loss}


def checkpoint_gradients(
    model: nn.Module,
    data,
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
        target_loss = F.cross_entropy(target_logits[target_ids], data.y[target_ids], reduction="mean")
        target_gradient = flatten(torch.autograd.grad(target_loss, params)).detach()

        candidate_logits = model(data.x, data.edge_index)
        rows: List[Tensor] = []
        for index, node_id in enumerate(candidate_ids.tolist()):
            loss = F.cross_entropy(
                candidate_logits[node_id : node_id + 1],
                data.y[node_id : node_id + 1],
                reduction="mean",
            )
            gradient = torch.autograd.grad(
                loss, params, retain_graph=index < candidate_ids.numel() - 1
            )
            rows.append(flatten(gradient).detach())
        return torch.stack(rows), target_gradient


def lissa_eval_reference(
    model: nn.Module,
    data,
    state: Mapping[str, Tensor],
    candidate_ids: Tensor,
    hessian_train_ids: Tensor,
    target_ids: Tensor,
    parameter_scope: str,
    iterations: int,
    scale: float,
    damp: float,
) -> Tensor:
    with preserve_model_state_and_mode(model):
        model.load_state_dict(state)
        model.eval()
        params = model_parameters(model, parameter_scope)
        train_logits = model(data.x, data.edge_index)
        train_loss = F.cross_entropy(
            train_logits[hessian_train_ids], data.y[hessian_train_ids], reduction="mean"
        )
        train_gradient = torch.autograd.grad(train_loss, params, create_graph=True)

        target_logits = model(data.x, data.edge_index)
        target_loss = F.cross_entropy(
            target_logits[target_ids], data.y[target_ids], reduction="mean"
        )
        target_gradient = [
            value.detach() for value in torch.autograd.grad(target_loss, params)
        ]
        estimate = [value.clone() for value in target_gradient]
        for _ in range(iterations):
            dot = sum((left * right).sum() for left, right in zip(train_gradient, estimate))
            hvp = torch.autograd.grad(dot, params, retain_graph=True)
            estimate = [
                value + (1.0 - damp) * old - curvature.detach() / scale
                for value, old, curvature in zip(target_gradient, estimate, hvp)
            ]
        inverse_target = flatten([value / scale for value in estimate]).detach()
        final_matrix, _ = checkpoint_gradients(
            model, data, state, candidate_ids, target_ids, parameter_scope
        )
        return final_matrix.mv(inverse_target)


def reject_legacy_output_path(output: Path, repo: Path) -> None:
    resolved = output.expanduser().resolve()
    legacy_roots = (
        repo / "results" / "cache",
        repo / "results" / "selection_cache",
        repo / "results" / "score_cache",
    )
    for root in legacy_roots:
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        raise ValueError("gate output must not be written under a Legacy cache root")


def accuracy(model: nn.Module, data, mask: Tensor) -> float:
    model.eval()
    with torch.no_grad():
        prediction = model(data.x, data.edge_index).argmax(dim=-1)
    return float((prediction[mask] == data.y[mask]).float().mean().item())


def jaccard(left: Iterable[int], right: Iterable[int]) -> float:
    a, b = set(left), set(right)
    return float(len(a & b) / len(a | b)) if (a | b) else 1.0


def pair_metrics(scores: Mapping[str, Tensor], selections: Mapping[str, Tuple[int, ...]]) -> Dict[str, object]:
    output: Dict[str, object] = {}
    names = list(scores)
    for left_index, left in enumerate(names):
        for right in names[left_index + 1 :]:
            spearman = spearmanr(scores[left].numpy(), scores[right].numpy()).statistic
            kendall = kendalltau(scores[left].numpy(), scores[right].numpy()).statistic
            output["{0}__{1}".format(left, right)] = {
                "spearman": None if np.isnan(spearman) else float(spearman),
                "kendall": None if np.isnan(kendall) else float(kendall),
                "jaccard_at_k": jaccard(selections[left], selections[right]),
                "ordered_topk_equal": selections[left] == selections[right],
            }
    return output


def atomic_write_json(path: Path, payload: Mapping[str, object], overwrite: bool) -> None:
    path = path.expanduser().resolve()
    if path.exists() and not overwrite:
        raise FileExistsError("refusing to overwrite existing gate report: {0}".format(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(prefix=".{0}.".format(path.name), suffix=".tmp", dir=str(path.parent))
    temp_path = Path(temp_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    checkpoint_epochs = parse_ints(args.checkpoint_epochs)
    milestones = parse_ints(args.lr_milestones)
    if not checkpoint_epochs or tuple(sorted(set(checkpoint_epochs))) != checkpoint_epochs:
        raise ValueError("checkpoint epochs must be unique and ascending")
    if checkpoint_epochs[0] <= 0 or checkpoint_epochs[-1] > args.epochs:
        raise ValueError("post-epoch checkpoints must fall inside [1, epochs]")
    if args.epochs not in checkpoint_epochs:
        raise ValueError("the final epoch must be included in checkpoint epochs")
    if not 0.0 < args.topk_ratio <= 1.0:
        raise ValueError("topk ratio must be in (0, 1]")
    if args.topk < 0:
        raise ValueError("topk must be non-negative")
    if args.hidden_channels <= 0:
        raise ValueError("hidden channels must be positive")
    if args.gat_heads <= 0:
        raise ValueError("GAT heads must be positive")
    if args.lissa_iter < 0:
        raise ValueError("LiSSA iterations must be non-negative")
    if args.lissa_scale <= 0 or not 0.0 <= args.lissa_damp < 1.0:
        raise ValueError("LiSSA scale must be positive and damp must be in [0, 1)")

    repo = Path(__file__).resolve().parents[2]
    reject_legacy_output_path(args.output, repo)

    seed_everything(args.seed, args.num_threads)
    device = torch.device("cpu")
    dataset = Planetoid(
        root=str(args.data_root.expanduser().resolve()),
        name=args.dataset,
        transform=NormalizeFeatures(),
    )
    data = dataset[0].to(device)
    candidate_ids = data.train_mask.nonzero(as_tuple=False).view(-1)
    hessian_train_ids = candidate_ids.clone()
    if args.candidate_limit > 0:
        candidate_ids = candidate_ids[: args.candidate_limit]
    target_mask = data.val_mask if args.target_profile == "attack_safe_holdout" else data.test_mask
    target_ids = target_mask.nonzero(as_tuple=False).view(-1)
    if set(candidate_ids.tolist()) & set(target_ids.tolist()):
        raise RuntimeError("candidate T and target E must be disjoint")

    lr = args.lr if args.lr is not None else (0.1 if args.optimizer == "sgd" else 0.01)
    model = build_model(
        args.model,
        dataset.num_features,
        args.hidden_channels,
        dataset.num_classes,
        args.dropout,
        args.gat_heads,
    ).to(device)
    started = time.time()
    checkpoints, train_summary = train_trajectory(
        model,
        data,
        checkpoint_epochs,
        args.epochs,
        args.optimizer,
        lr,
        args.weight_decay,
        milestones,
        args.lr_gamma,
    )

    candidate_trajectory: List[Tensor] = []
    target_trajectory: List[Tensor] = []
    for item in checkpoints:
        matrix, target_gradient = checkpoint_gradients(
            model,
            data,
            item["state"],
            candidate_ids,
            target_ids,
            args.parameter_scope,
        )
        candidate_trajectory.append(matrix)
        target_trajectory.append(target_gradient)

    checkpoint_weights = [float(item["update_lr"]) for item in checkpoints]
    final_matrix = candidate_trajectory[-1]
    scores: Dict[str, Tensor] = {
        "deployed_cross_final": deployed_cross_gradient_scores(final_matrix),
        "single_final_eval": final_matrix.mv(target_trajectory[-1]),
        "tracin_cp_lr": tracin_cp_eval_scores(
            candidate_trajectory, target_trajectory, checkpoint_weights
        ),
        "tracin_cp_uniform": tracin_cp_eval_scores(
            candidate_trajectory, target_trajectory, [1.0] * len(checkpoints)
        ),
        "tracin_cp_self": tracin_cp_self_scores(
            candidate_trajectory, checkpoint_weights
        ),
    }
    if args.lissa_iter > 0:
        scores["eval_if_reference"] = lissa_eval_reference(
            model,
            data,
            checkpoints[-1]["state"],
            candidate_ids,
            hessian_train_ids,
            target_ids,
            args.parameter_scope,
            args.lissa_iter,
            args.lissa_scale,
            args.lissa_damp,
        )

    k = args.topk if args.topk > 0 else max(int(candidate_ids.numel() * args.topk_ratio), 1)
    if k > candidate_ids.numel():
        raise ValueError("topk cannot exceed the candidate count")
    selections = {
        name: stable_topk(candidate_ids.tolist(), value, k)
        for name, value in scores.items()
    }

    source_hash = source_fingerprint(
        [Path(__file__).resolve(), repo / "experiments" / "tracin_v2" / "core.py", repo / "experiments" / "tracin_v2" / "recipe.py"]
    )
    numerics = {
        "python": platform.python_version(),
        "torch": torch.__version__,
        "torch_geometric": torch_geometric.__version__,
        "numpy": np.__version__,
        "scipy": __import__("scipy").__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "byteorder": sys.byteorder,
        "torch_build_hash": sha256_bytes(torch.__config__.show().encode("utf-8")),
        "execution_backend": "cpu",
        "dtype": "float32",
        "num_threads": args.num_threads,
        "deterministic_algorithms": True,
    }
    numerics_hash = sha256_bytes(
        json.dumps(numerics, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    checkpoint_manifest = [
        {
            "epoch": int(item["epoch"]),
            "global_step": int(item["global_step"]),
            "state_hash": str(item["state_hash"]),
            "weight": float(item["update_lr"]),
        }
        for item in checkpoints
    ]
    model.load_state_dict(checkpoints[-1]["state"])
    recipe = build_unstable_recipe(
        source_fingerprint=source_hash,
        data_identity={
            "dataset_adapter": "torch_geometric.datasets.Planetoid",
            "dataset_name": args.dataset,
            "split_policy": "public",
            "transform_policy": "NormalizeFeatures",
            "edge_index_hash": tensor_hash(data.edge_index),
            "features_hash": tensor_hash(data.x),
            "labels_hash": tensor_hash(data.y),
            "split_hash": sha256_bytes(
                bytes.fromhex(tensor_hash(data.train_mask))
                + bytes.fromhex(tensor_hash(data.val_mask))
                + bytes.fromhex(tensor_hash(data.test_mask))
            ),
        },
        candidate_ids_hash=ids_hash(candidate_ids),
        target_ids_hash=ids_hash(target_ids),
        target_profile=args.target_profile,
        label_source=(
            "validation_true_labels"
            if args.target_profile == "attack_safe_holdout"
                else "test_true_labels_diagnostic_only"
        ),
        diagnostic_only=args.target_profile == "diagnostic_test_labels",
        selector_model={
            "architecture": "two_layer_{0}".format(args.model),
            "hidden_channels": args.hidden_channels,
            "gat_heads": args.gat_heads if args.model == "gat" else None,
            "dropout": args.dropout,
            "final_state_hash": state_hash(checkpoints[-1]["state"]),
            "gradient_model_mode": "eval",
            "parameter_schema_hash": parameter_schema_hash(model, args.parameter_scope),
            "training_batch_policy": "full_batch_one_optimizer_step_per_epoch",
        },
        checkpoints=checkpoint_manifest,
        weight_policy=(
            "paper_lr"
            if args.optimizer == "sgd"
            else "adam_lr_weighted_gradient_heuristic"
        ),
        optimizer={
            "family": args.optimizer,
            "initial_lr": lr,
            "weight_decay": args.weight_decay,
            "lr_milestones": list(milestones),
            "lr_gamma": args.lr_gamma,
            "state_policy": "provenance_only_not_score_input",
        },
        loss={
            "family": "cross_entropy",
            "candidate_reduction": "single",
            "target_reduction": "mean",
            "training_reduction": "mean",
            "class_weights": None,
            "ignore_index": -100,
        },
        parameter_scope=args.parameter_scope,
        seed_bundle={"train": args.seed, "data": args.seed, "query": args.seed},
        numerics_profile_hash=numerics_hash,
    )

    result = {
        "gate_schema_version": "tracin-v2-gate-report-v2",
        "stability": "unstable",
        "formal_score_artifact": False,
        "legacy_cache_access": False,
        "default_runner_registered": False,
        "diagnostic_only": args.target_profile == "diagnostic_test_labels",
        "recipe_hash": recipe.recipe_hash,
        "recipe": recipe.to_dict(),
        "provenance": {
            "hostname": socket.gethostname(),
            "numerics": numerics,
            "source_fingerprint": source_hash,
        },
        "dataset": {
            "name": args.dataset,
            "num_nodes": int(data.num_nodes),
            "num_edges": int(data.num_edges),
            "num_candidates": int(candidate_ids.numel()),
            "num_targets": int(target_ids.numel()),
            "target_profile": args.target_profile,
        },
        "training": {
            "model": args.model,
            "hidden_channels": args.hidden_channels,
            "gat_heads": args.gat_heads if args.model == "gat" else None,
            "optimizer": args.optimizer,
            "epochs": args.epochs,
            "checkpoint_manifest": checkpoint_manifest,
            **train_summary,
            "test_accuracy": accuracy(model, data, data.test_mask),
        },
        "scoring": {
            "primary_score": "tracin_cp_lr",
            "score_identity": {
                name: (
                    {"recipe_hash": recipe.recipe_hash, "formal_artifact": False}
                    if name == "tracin_cp_lr"
                    else {"recipe_hash": None, "reference_only": True}
                )
                for name in scores
            },
            "parameter_scope": args.parameter_scope,
            "k": k,
            "selection_budget_policy": (
                "exact" if args.topk > 0 else "floor_candidate_ratio_with_minimum_one"
            ),
            "topk_ratio": None if args.topk > 0 else args.topk_ratio,
            "lissa": {
                "iterations": args.lissa_iter,
                "scale": args.lissa_scale,
                "damp": args.lissa_damp,
                "solver": "deterministic_full_batch_neumann_recursion",
                "hessian_loss": "full_train_mask_mean_cross_entropy_without_optimizer_regularizer",
                "hessian_train_ids_hash": ids_hash(hessian_train_ids),
            },
            "candidate_ids": candidate_ids.tolist(),
            "scores": {name: value.tolist() for name, value in scores.items()},
            "selections": {name: list(value) for name, value in selections.items()},
            "pair_metrics": pair_metrics(scores, selections),
            "finite": {name: bool(torch.isfinite(value).all()) for name, value in scores.items()},
        },
        "historical_overlap_comparable": False,
        "compute_seconds": time.time() - started,
    }
    atomic_write_json(args.output, result, args.overwrite)
    print(
        json.dumps(
            {
                "output": str(args.output.expanduser().resolve()),
                "recipe_hash": recipe.recipe_hash,
                "dataset": args.dataset,
                "model": args.model,
                "optimizer": args.optimizer,
                "target_profile": args.target_profile,
                "test_accuracy": result["training"]["test_accuracy"],
                "compute_seconds": result["compute_seconds"],
                "key_metrics": {
                    key: value
                    for key, value in result["scoring"]["pair_metrics"].items()
                    if key
                    in {
                        "single_final_eval__tracin_cp_lr",
                        "tracin_cp_lr__eval_if_reference",
                        "deployed_cross_final__tracin_cp_lr",
                    }
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
