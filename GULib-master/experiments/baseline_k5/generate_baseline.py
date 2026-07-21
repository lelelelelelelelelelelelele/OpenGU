"""
generate_baseline.py - Pre-generate K=5 random baseline metrics for unlearning methods.

This script should be run BEFORE `eval_relative.py`. It runs a bare-bones 
evaluation using the `random` strategy for a tiny number of nodes (default K=5)
to extract the inherent F1 shift protecting the unlearning method.

Usage:
    python experiments/baseline_k5/generate_baseline.py \
        --dataset_name cora \
        --base_model GCN \
        --unlearning_methods GraphEraser \
        --random_seed 2024 \
        --baseline_k 5
"""
import os
import sys
import json
import numpy as np
import torch
import random
import subprocess
from pathlib import Path
from datetime import datetime

# Extract custom args BEFORE parameter_parser (which rejects unknown args)
_baseline_k = 5
_output_root = None
_raw_args = list(sys.argv[1:])
_filtered_argv = []
_i = 0
while _i < len(_raw_args):
    _arg = _raw_args[_i]
    if _arg == '--baseline_k':
        if _i + 1 < len(_raw_args):
            _baseline_k = int(_raw_args[_i + 1])
            _i += 2
            continue
        _i += 1
        continue
    elif _arg.startswith('--baseline_k='):
        _baseline_k = int(_arg.split('=', 1)[1])
    elif _arg == '--output_root':
        if _i + 1 < len(_raw_args):
            _output_root = _raw_args[_i + 1]
            _i += 2
            continue
        raise SystemExit('--output_root requires a path')
    elif _arg.startswith('--output_root='):
        _output_root = _arg.split('=', 1)[1]
    else:
        _filtered_argv.append(_arg)
    _i += 1
sys.argv = [sys.argv[0]] + _filtered_argv

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from parameter_parser import parameter_parser
from attack.pipeline_adapter import AttackPipeline
from attack.attack_strategies import RandomStrategy
from experiments.baseline_k5.baseline_contract import (
    SCHEMA,
    SCHEMA_VERSION,
    default_result_root,
    expected_config,
    load_valid_record,
    measure_method_perf_before,
    validate_run_result,
)


REPO_ROOT = Path(base_dir)
DEFAULT_OUTPUT_ROOT = default_result_root(REPO_ROOT)


def _git_provenance():
    def run(*args):
        return subprocess.check_output(
            ['git', '-C', str(REPO_ROOT), *args], text=True, encoding='utf-8'
        ).strip()

    try:
        sha = run('rev-parse', 'HEAD')
        dirty = bool(run('status', '--porcelain'))
    except (OSError, subprocess.SubprocessError):
        sha, dirty = None, None
    return {'git_sha': sha, 'git_dirty': dirty}


def _write_json_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f'.tmp-{os.getpid()}')
    temporary.write_text(json.dumps(value, indent=2), encoding='utf-8')
    os.replace(str(temporary), str(path))


def generate_baseline(args: dict, k: int, output_root: Path):
    dataset = args.get('dataset_name', 'cora')
    model = args.get('base_model', 'GCN')
    method = args.get('unlearning_methods', 'GraphEraser')
    seed = int(args.get('random_seed', 2024))
    
    # k5_random is canonical.  Pre-v2 evidence lives in the tracked
    # k5_random_OLD_20260227 archive, so it cannot be mistaken for a resume hit.
    cache_dir = Path(output_root) / method / dataset / model
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"baseline_seed{seed}_k{k}.json"
    expected = expected_config(
        dataset=dataset, model=model, method=method, seed=seed, k=k
    )
    
    print(f"\n==================================================")
    print(f"[Generate Baseline] Method: {method} | Dataset: {dataset} | Model: {model}")
    print(f"                    Seed: {seed} | K: {k}")
    print(f"==================================================")
    
    if cache_file.exists():
        try:
            load_valid_record(cache_file, expected)
        except Exception as exc:
            raise RuntimeError(
                f"Existing output is not a compatible v2 artifact: {cache_file}: {exc}. "
                "Move it aside explicitly; it will not be overwritten."
            ) from exc
        print(f"[INFO] Compatible v2 artifact exists; resuming: {cache_file}")
        return cache_file
        
    print(f"[*] Initializing pipeline...")
    
    # 1. Lock seeds
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        
    # 2. Setup
    before_pipeline = AttackPipeline(dict(args))
    method_perf_before, before_source = measure_method_perf_before(
        before_pipeline, method
    )
    print(
        f"[*] Method-specific before F1: {method_perf_before:.4f} "
        f"(source={before_source})"
    )

    # Use a fresh pipeline for the actual random-unlearning run.  The
    # train-only measurement above can replace ``self.model`` with a shard
    # wrapper or trained target; reusing it would contaminate random-init
    # restoration in the unlearning path.
    pipeline = AttackPipeline(args)
    strategy = RandomStrategy(args)

    # CRITICAL: Sync proportion_unlearned_nodes with actual k / num_nodes.
    # GNNDelete's delete_node() computes df_size = int(num_nodes * proportion_unlearned_nodes)
    # and asserts df_mask_node.sum() == df_size.  If proportion_unlearned_nodes stays at the
    # parameter_parser default (0.1), the assertion fails (5 != 270), the exception is caught
    # silently by pipeline_adapter, and a garbage f1_after is returned.
    # Also sync unlearn_ratio so _inject_unlearn_nodes writes the correct file path.
    num_nodes = pipeline.data.num_nodes
    ratio_for_k = k / num_nodes
    args['proportion_unlearned_nodes'] = ratio_for_k
    args['unlearn_ratio'] = ratio_for_k
    print(f"[*] Synced proportion_unlearned_nodes = {ratio_for_k:.6f} (k={k}, num_nodes={num_nodes})")
    
    # 3. Execution
    print(f"[*] Executing random unlearning to extract inherent F1 metric...")
    result_dict = pipeline.run_with_strategy(strategy, k)
    
    # 4. Collection
    f1_after = validate_run_result(result_dict, k)
    f1_before = result_dict.get("f1_before")
    f1_drop = result_dict.get("f1_drop")
    if f1_drop is None and f1_before is not None and f1_after is not None:
        f1_drop = f1_before - f1_after
    
    data = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "f1_after": f1_after,
        "f1_before": f1_before,
        "f1_drop": f1_drop,
        "method_perf_before": method_perf_before,
        "method_noise_drop": (
            method_perf_before - f1_after
            if method_perf_before is not None and f1_after is not None
            else None
        ),
        "config": {
            "dataset_name": dataset,
            "base_model": model,
            "unlearning_methods": method,
            "seed": seed,
            "k": k,
            "strategy": "random",
            "before_metric": "method_train_only_f1",
            "before_metric_source": before_source,
            "output_root": str(Path(output_root).resolve()),
            **_git_provenance(),
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # 5. Saving. Failed runs never reach this point.
    _write_json_atomic(cache_file, data)
        
    print(f"[*] Completed! F1 After: {f1_after:.4f}")
    print(f"[*] Baseline saved to: {cache_file}")
    return cache_file


def main():
    args = parameter_parser()
    
    # We enforce ratio=0 internally during generation of the base model 
    # to avoid conflict, but since AttackPipeline only triggers the 'k'
    # we pass to 'run_with_strategy(strategy, k)', standard args are fine.
    
    output_root = (
        Path(_output_root).expanduser().resolve()
        if _output_root
        else DEFAULT_OUTPUT_ROOT
    )
    generate_baseline(args, _baseline_k, output_root)


if __name__ == '__main__':
    main()
