"""Produce 17 white-box selections from the exact OpenGU GNNDelete target."""

from __future__ import annotations

import argparse
import json
import os
import platform
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np
import torch
import torch_geometric

from experiments.processed_provider import (
    ProcessedArtifactError,
)
from experiments.target_direct_v1 import (
    DEFAULT_SPLIT_CONTRACT,
    target_direct_split_contract,
)
from experiments.target_direct_v1.recipe import (
    ALGORITHM_VERSION,
    APPROVED_BUDGET_RATIOS,
    SCORE_BUDGET_SEMANTICS,
    SCORE_NAMES,
)
from experiments.target_direct_v1.split_profile import stage_profile, verify_profile
from utils.target_checkpoint import (
    capture_state,
    data_identity,
    load_target_checkpoint,
    save_target_checkpoint,
    state_hash,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def _int_list(value: str) -> Tuple[int, ...]:
    result = tuple(int(item.strip()) for item in value.split(",") if item.strip())
    if not result or any(item <= 0 for item in result):
        raise argparse.ArgumentTypeError("expected positive comma-separated integers")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset", choices=("Cora", "CiteSeer", "PubMed"), required=True
    )
    parser.add_argument("--processed-root", type=Path, required=True)
    parser.add_argument(
        "--processed-profile",
        default=None,
    )
    parser.add_argument(
        "--train-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.train_ratio
    )
    parser.add_argument(
        "--val-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.val_ratio
    )
    parser.add_argument(
        "--test-ratio", type=float, default=DEFAULT_SPLIT_CONTRACT.test_ratio
    )
    parser.add_argument(
        "--split-seed", type=int, default=DEFAULT_SPLIT_CONTRACT.split_seed
    )
    parser.add_argument("--materialize-split-on-miss", action="store_true")
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--selection-cache-root", type=Path, required=True)
    parser.add_argument("--checkpoint-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--ratio", type=float, required=True)
    parser.add_argument("--cuda", type=int, default=0)
    parser.add_argument("--num-threads", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument(
        "--checkpoint-epochs",
        type=_int_list,
        default=(1, 10, 25, 50, 75, 100),
    )
    parser.add_argument("--gcn-num-layers", type=int, default=2)
    parser.add_argument("--gcn-hidden", type=int, default=64)
    parser.add_argument(
        "--parameter-scope",
        choices=("last_layer", "all_trainable"),
        default="last_layer",
    )
    parser.add_argument("--affected-hops", type=int, default=2)
    parser.add_argument("--lissa-iterations", type=int, default=20)
    parser.add_argument("--lissa-scale", type=float, default=25.0)
    parser.add_argument("--lissa-damp", type=float, default=0.01)
    parser.add_argument("--hutch-probes", type=int, default=32)
    parser.add_argument("--hutch-seed", type=int, default=1729)
    parser.add_argument("--reuse-checkpoint", action="store_true")
    parser.add_argument("--fail-if-score-producer-called", action="store_true")
    parser.add_argument("--fail-if-producer-called", action="store_true")
    parser.add_argument("--overwrite-output", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--experiment-git-sha", default=None)
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    try:
        args.split_contract = target_direct_split_contract(
            {
                "processed_profile": args.processed_profile,
                "split": {
                    "train_ratio": args.train_ratio,
                    "val_ratio": args.val_ratio,
                    "test_ratio": args.test_ratio,
                    "split_seed": args.split_seed,
                },
            },
            require_explicit=True,
        )
        args.processed_profile = args.split_contract.processed_profile
    except ProcessedArtifactError as exc:
        raise ValueError(str(exc)) from exc
    if args.seed < 0 or args.num_threads <= 0 or args.epochs <= 0:
        raise ValueError("seed, thread count, and epochs must be positive")
    if not any(
        abs(float(args.ratio) - approved) < 1e-12
        for approved in APPROVED_BUDGET_RATIOS
    ):
        raise ValueError(
            "formal ratio must be one of {0}".format(
                list(APPROVED_BUDGET_RATIOS)
            )
        )
    if args.checkpoint_epochs[-1] != args.epochs:
        raise ValueError("final checkpoint epoch must equal epochs")
    if len(args.checkpoint_epochs) < 3:
        raise ValueError("at least three checkpoints are required")
    if tuple(sorted(set(args.checkpoint_epochs))) != tuple(args.checkpoint_epochs):
        raise ValueError("checkpoint epochs must be unique and increasing")
    if args.gcn_num_layers != 2:
        raise ValueError("target_direct_v1 currently freezes a two-layer OpenGU GCN")
    if args.gcn_hidden <= 0:
        raise ValueError("gcn_hidden must be positive")
    for path, label in (
        (args.processed_root, "processed_root"),
        (args.runtime_root, "runtime_root"),
        (args.cache_root, "cache_root"),
        (args.selection_cache_root, "selection_cache_root"),
    ):
        if not Path(path).expanduser().is_absolute():
            raise ValueError("{0} must be absolute".format(label))
    cache_root = Path(args.cache_root).expanduser().resolve()
    selection_cache_root = Path(args.selection_cache_root).expanduser().resolve()
    if cache_root != selection_cache_root:
        raise ValueError(
            "cache_root and selection_cache_root must resolve to the same canonical Cache V2 root"
        )


def _git_provenance(expected_sha: str | None, allow_dirty: bool) -> Dict[str, Any]:
    def run(*arguments: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(REPO_ROOT), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout.strip()

    head = run("rev-parse", "HEAD").lower()
    status = run("status", "--short")
    if expected_sha is not None and head != str(expected_sha).lower():
        raise RuntimeError(
            "experiment Git HEAD mismatch: observed {0}, expected {1}".format(
                head, expected_sha
            )
        )
    if status and not allow_dirty:
        raise RuntimeError("formal target-direct selection requires a clean worktree")
    return {
        "head": head,
        "expected_head": expected_sha,
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "worktree_dirty": bool(status),
        "status_short": status.splitlines() if status else [],
    }


def _seed_everything(seed: int, num_threads: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(num_threads)
    os.environ["PYTHONHASHSEED"] = str(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _synchronize(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def _gpu_peaks(device: torch.device) -> Dict[str, Any]:
    if device.type != "cuda":
        return {
            "available": False,
            "device": str(device),
            "peak_allocated_bytes": None,
            "peak_reserved_bytes": None,
        }
    _synchronize(device)
    return {
        "available": True,
        "device": str(device),
        "device_name": torch.cuda.get_device_name(device),
        "peak_allocated_bytes": int(torch.cuda.max_memory_allocated(device)),
        "peak_reserved_bytes": int(torch.cuda.max_memory_reserved(device)),
    }


def _atomic_json(path: Path, value: Mapping[str, Any], overwrite: bool) -> None:
    target = Path(path).expanduser().resolve()
    if target.exists() and not overwrite:
        raise FileExistsError("output already exists: {0}".format(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp-{0}".format(os.getpid()))
    try:
        temporary.write_text(
            json.dumps(
                value,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
                allow_nan=False,
            )
            + "\n",
            encoding="utf-8",
        )
        os.replace(str(temporary), str(target))
    finally:
        if temporary.exists():
            temporary.unlink()


def _parameter_argv(args: argparse.Namespace, expected_k: int) -> Sequence[str]:
    contract = args.split_contract
    return [
        str(Path(__file__).resolve()),
        "--root_path",
        str(REPO_ROOT),
        "--runtime_root",
        str(args.runtime_root.expanduser().resolve()),
        "--processed_root",
        str(args.processed_root.expanduser().resolve()),
        "--processed_profile",
        contract.processed_profile,
        "--dataset_name",
        args.dataset.lower(),
        "--base_model",
        "GCN",
        "--unlearning_methods",
        "GNNDelete",
        "--train_ratio",
        str(contract.train_ratio),
        "--val_ratio",
        str(contract.val_ratio),
        "--test_ratio",
        str(contract.test_ratio),
        "--split_seed",
        str(contract.split_seed),
        "--unlearn_ratio",
        str(args.ratio),
        "--proportion_unlearned_nodes",
        str(args.ratio),
        "--formal_expected_k",
        str(expected_k),
        "--formal_fail_closed",
        "--num_epochs",
        str(args.epochs),
        "--num_threads",
        str(args.num_threads),
        "--random_seed",
        str(args.seed),
        "--cuda",
        str(args.cuda),
        "--gcn_num_layers",
        str(args.gcn_num_layers),
        "--gcn_hidden",
        str(args.gcn_hidden),
    ]


def _prepare_target(
    args: argparse.Namespace,
    *,
    candidate_count: int,
    expected_k: int,
    expected_data_identity: Mapping[str, Any],
) -> Tuple[Any, Any, Sequence[Mapping[str, Any]], Dict[str, Any], Dict[str, Any]]:
    sys.argv = list(_parameter_argv(args, expected_k))
    from parameter_parser import parameter_parser
    from attack.pipeline_adapter import AttackPipeline

    runtime_args = parameter_parser()
    runtime_args["split_contract"] = args.split_contract.to_manifest()
    runtime_args["seed"] = int(args.seed)
    runtime_args["target_direct_checkpoint_epochs"] = tuple(
        int(value) for value in args.checkpoint_epochs
    )
    pipeline = AttackPipeline(runtime_args)
    observed_identity = data_identity(pipeline.data)
    if observed_identity != dict(expected_data_identity):
        raise RuntimeError(
            "OpenGU runtime data differs from verified target-direct profile"
        )

    checkpoint_path = args.checkpoint_path.expanduser().resolve()
    training_started = time.perf_counter()
    if args.reuse_checkpoint:
        checkpoint = load_target_checkpoint(
            checkpoint_path,
            expected_metadata={
                "dataset_name": args.dataset.lower(),
                "base_model": "GCN",
                "seed": int(args.seed),
                "processed_profile": args.split_contract.processed_profile,
                "split_contract": args.split_contract.to_manifest(),
                "num_epochs": int(args.epochs),
                "gcn_num_layers": int(args.gcn_num_layers),
                "gcn_hidden": int(args.gcn_hidden),
            },
            map_location="cpu",
        )
        if checkpoint["metadata"].get("data_identity") != observed_identity:
            raise RuntimeError("reused target checkpoint data identity mismatch")
        pipeline.method.determine_target_model()
        model = pipeline.method.target_model.model
        model.load_state_dict(checkpoint["state_dict"], strict=True)
        checkpoints = checkpoint["checkpoints"]
        training_observation = {
            "mode": "reused_checkpoint",
            "seconds": time.perf_counter() - training_started,
        }
        checkpoint_manifest = {
            "path": checkpoint["path"],
            "file_sha256": checkpoint["file_sha256"],
            "state_hash": checkpoint["state_hash"],
            "checkpoint_count": len(checkpoints),
            "metadata": dict(checkpoint["metadata"]),
        }
    else:
        pipeline.args["train_only"] = True
        pipeline.args["num_runs"] = 1
        pipeline.method.run_exp()
        model = pipeline._get_trained_model()
        checkpoints = tuple(
            getattr(pipeline.method.target_model, "target_direct_checkpoints", ())
        )
        final_state = capture_state(model)
        metadata = {
            "dataset_name": args.dataset.lower(),
            "base_model": "GCN",
            "seed": int(args.seed),
            "processed_profile": args.split_contract.processed_profile,
            "split_contract": args.split_contract.to_manifest(),
            "num_epochs": int(args.epochs),
            "gcn_num_layers": int(args.gcn_num_layers),
            "gcn_hidden": int(args.gcn_hidden),
            "data_identity": observed_identity,
            "candidate_identity": {
                "denominator": "train_candidate_count",
                "candidate_count": int(candidate_count),
                "deletion_budget_conditioned": False,
            },
        }
        checkpoint_manifest = save_target_checkpoint(
            checkpoint_path,
            state_dict=final_state,
            metadata=metadata,
            checkpoints=checkpoints,
            overwrite=args.overwrite_output,
        )
        training_observation = {
            "mode": "cold_training",
            "seconds": time.perf_counter() - training_started,
            "test_f1_observed_after_training": float(
                pipeline.method.poison_f1[0]
            ),
        }
    model = model.to(pipeline.device)
    model.load_state_dict(checkpoints[-1]["state"], strict=True)
    if state_hash(model.state_dict()) != checkpoint_manifest["state_hash"]:
        raise RuntimeError("prepared model differs from target checkpoint")
    return (
        pipeline,
        model,
        checkpoints,
        checkpoint_manifest,
        training_observation,
    )


def run(args: argparse.Namespace) -> Dict[str, Any]:
    _validate_args(args)
    run_started = time.perf_counter()
    git_provenance = _git_provenance(
        args.experiment_git_sha, args.allow_dirty
    )
    profile_loader = (
        stage_profile if args.materialize_split_on_miss else verify_profile
    )
    profile = profile_loader(
        repository_root=REPO_ROOT,
        processed_root=args.processed_root,
        dataset=args.dataset,
        contract=args.split_contract,
    )
    candidate_count = int(profile["inputs"].candidate_count)
    expected_k = max(1, int(candidate_count * float(args.ratio)))
    _seed_everything(args.seed, args.num_threads)
    if not torch.cuda.is_available():
        raise RuntimeError("target-direct formal selection requires CUDA")
    torch.cuda.set_device(args.cuda)
    device = torch.device("cuda", args.cuda)
    torch.cuda.reset_peak_memory_stats(device)

    pipeline, model, checkpoints, target_checkpoint, training_observation = (
        _prepare_target(
            args,
            candidate_count=candidate_count,
            expected_k=expected_k,
            expected_data_identity=data_identity(profile["data"]),
        )
    )
    data = pipeline.data.to(device)
    candidate_ids = torch.where(data.train_mask)[0].sort().values
    target_ids = torch.where(data.val_mask)[0].sort().values
    if int(candidate_ids.numel()) != candidate_count:
        raise RuntimeError("candidate count changed after target preparation")
    if int(target_ids.numel()) <= 0:
        raise RuntimeError("validation target set is empty")
    from experiments.target_direct_v1.method_cache import resolve_methods
    from experiments.target_direct_v1.methods import parameter_defaults
    selectors = []
    for name in SCORE_NAMES:
        defaults = parameter_defaults(name)
        parameters = {}
        if 'parameter_scope' in defaults:
            parameters['parameter_scope'] = args.parameter_scope
        if 'lissa' in defaults:
            parameters['lissa'] = {'iterations': args.lissa_iterations,
                'scale': args.lissa_scale, 'damp': args.lissa_damp}
        if 'affected_hops' in defaults:
            parameters['affected_hops'] = args.affected_hops
        if 'hutchinson' in defaults:
            parameters['hutchinson'] = {'probes': args.hutch_probes, 'seed': args.hutch_seed}
        if name == 'random':
            parameters['seed'] = int(args.seed) + 100003
        selectors.append({'method': name, 'parameters': parameters,
            'budget': {'mode': 'ratio', 'value': float(args.ratio), 'k': expected_k,
                'denominator': 'train_candidate_count', 'rounding': 'floor_with_minimum_one'}})
    model_config = getattr(model, 'config', None)
    training_gpu_peaks = _gpu_peaks(device)
    torch.cuda.reset_peak_memory_stats(device)
    started = time.perf_counter()
    results = resolve_methods(store_root=args.cache_root.resolve(), data=data,
        dataset_name=args.dataset.lower(), model=model, checkpoints=checkpoints,
        model_config={'architecture': 'OpenGU.GCNNet', 'layers': args.gcn_num_layers,
                      'hidden_channels': args.gcn_hidden, 'dropout': 0.5},
        training={'epochs': args.epochs, 'optimizer': 'Adam',
                  'lr': float(model_config.lr), 'weight_decay': float(model_config.decay),
                  'scheduler': 'none', 'seed': args.seed}, selectors=selectors,
        fail_if_score_called=args.fail_if_score_producer_called or args.fail_if_producer_called,
        fail_if_selection_called=args.fail_if_producer_called)
    score_gpu_peaks = _gpu_peaks(device)
    return {
        'schema': 'target_direct_v1.selection_summary', 'version': 3,
        'status': {'state': 'success', 'failure': None}, 'algorithm_version': ALGORITHM_VERSION,
        'dataset': args.dataset, 'model': 'OpenGU.GCNNet', 'seed': int(args.seed),
        'processed_profile': args.split_contract.processed_profile,
        'split_contract': args.split_contract.to_manifest(),
        'candidate_count': candidate_count, 'target_count': int(target_ids.numel()),
        'budget': {'requested_ratio': float(args.ratio), 'denominator': 'train_candidate_count',
            'denominator_count': candidate_count, 'rounding': 'floor_with_minimum_one', 'expected_k': expected_k},
        'budget_projection': {'score_semantics': SCORE_BUDGET_SEMANTICS,
            'supported_ratios': list(APPROVED_BUDGET_RATIOS), 'budget_conditioned_strategies': [],
            'method_scores_shared_across_ratios': True, 'selection_artifact_ratio_conditioned': True},
        'target_objective': 'validation_mask_mean_cross_entropy', 'parameter_scope': args.parameter_scope,
        'dataset_profile': profile['manifest'], 'git_provenance': git_provenance,
        'target_checkpoint': target_checkpoint, 'training_observation': training_observation,
        'method_scores': {name: value['score'] for name, value in results.items()},
        'selection_artifacts': {name: value['selection'] for name, value in results.items()},
        'selection_cache': {'root': str(args.selection_cache_root.resolve()), 'method_count': len(results),
            'hit_count': sum(value['selection']['cache']['hit'] for value in results.values()),
            'method_timings': {name: {'status': 'success', 'cache_hit': item['selection']['cache']['hit'],
                'selection_projection_cache_hit': item['selection']['cache']['hit'],
                'cold_selection_projection_seconds': None if item['selection']['cache']['hit'] else item['selection_seconds'],
                'score_access_seconds': item['score']['access_seconds']} for name, item in results.items()}},
        'gpu_memory': {'training_and_checkpoint': training_gpu_peaks, 'method_scores': score_gpu_peaks,
            'process_peak_allocated_bytes': max(training_gpu_peaks['peak_allocated_bytes'], score_gpu_peaks['peak_allocated_bytes']),
            'process_peak_reserved_bytes': max(training_gpu_peaks['peak_reserved_bytes'], score_gpu_peaks['peak_reserved_bytes'])},
        'runtime': {'total_seconds': time.perf_counter() - run_started,
                    'score_and_selection_access_seconds': time.perf_counter() - started},
        'environment': {'python': platform.python_version(), 'torch': torch.__version__,
            'torch_geometric': torch_geometric.__version__, 'cuda': torch.version.cuda, 'device': str(device)},
    }


def main(argv: Sequence[str] | None = None) -> int:
    parsed = build_parser().parse_args(argv)
    started = time.perf_counter()
    try:
        summary = run(parsed)
    except Exception as exc:
        failure_gpu = {
            "available": bool(torch.cuda.is_available()),
            "device": None,
            "peak_allocated_bytes": None,
            "peak_reserved_bytes": None,
        }
        if torch.cuda.is_available():
            try:
                failure_device = torch.device("cuda", parsed.cuda)
                failure_gpu = _gpu_peaks(failure_device)
            except Exception:
                pass
        failure = {
            "schema": "target_direct_v1.selection_summary",
            "version": 3,
            "status": {
                "state": "failed",
                "failure": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            },
            "dataset": parsed.dataset,
            "seed": int(parsed.seed),
            "processed_profile": parsed.processed_profile,
            "split_contract": {
                "processed_profile": parsed.processed_profile,
                "train_ratio": float(parsed.train_ratio),
                "val_ratio": float(parsed.val_ratio),
                "test_ratio": float(parsed.test_ratio),
                "split_seed": int(parsed.split_seed),
            },
            "parameter_scope": parsed.parameter_scope,
            "budget": {
                "requested_ratio": float(parsed.ratio),
                "denominator": "train_candidate_count",
                "rounding": "floor_with_minimum_one",
            },
            "gpu_memory": failure_gpu,
            "runtime": {"total_seconds": time.perf_counter() - started},
        }
        _atomic_json(parsed.output, failure, parsed.overwrite_output)
        raise
    _atomic_json(parsed.output, summary, parsed.overwrite_output)
    print(
        json.dumps(
            {
                "output": str(parsed.output.expanduser().resolve()),
                "status": "success",
                "method_score_hits": sum(item["hit"] for item in summary["method_scores"].values()),
                "expected_k": summary["budget"]["expected_k"],
                "target_checkpoint_state_hash": summary["target_checkpoint"][
                    "state_hash"
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
