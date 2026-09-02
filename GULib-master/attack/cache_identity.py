"""Experiment-owned identities for the generic consumers of Cache V2."""
from __future__ import annotations

import hashlib
import random
from contextlib import contextmanager
from pathlib import Path
import numpy as np
import torch
from cache_v2 import ProducerVersion, canonical_sha256
from experiments.selection_inputs import graph_fingerprint, candidate_fingerprint, dataset_fingerprint
from experiments.selection_producer import validate_store_root, legacy_cache_roots

DEFAULT_STORE_ROOT = "./results/cache_v2"


def store_root(args):
    return resolve_store_root(args.get("cache_v2_store_root") or DEFAULT_STORE_ROOT)


def resolve_store_root(value):
    root = Path(value).absolute().resolve()
    repo = Path(__file__).resolve().parents[1]
    forbidden = legacy_cache_roots(repo / "results") + legacy_cache_roots(Path.cwd() / "results")
    return validate_store_root(root, forbidden)


def producer_version(kind, paths):
    digest = hashlib.sha256()
    root = Path(__file__).resolve().parents[1]
    for relative in sorted(set(paths)):
        digest.update(relative.encode() + b"\0" + (root / relative).read_bytes())
    return ProducerVersion(semantic_version="generic-" + kind + "-v1", source_fingerprint=digest.hexdigest())


def strategy_version(name):
    names = [name] + (["tracin", "im"] if name == "hybrid" else [])
    return producer_version("selection", ["attack/cache_identity.py", "attack/attack_manager.py",
        "attack/attack_strategies/base_strategy.py"] +
        ["attack/attack_strategies/" + item + "_strategy.py" for item in names])


def model_fingerprint(model):
    digest = hashlib.sha256()
    for name, tensor in sorted(model.state_dict().items()):
        tensor = tensor.detach().cpu().contiguous()
        digest.update(name.encode() + str(tensor.dtype).encode())
        digest.update(np.asarray(tensor.shape, dtype="<i8").tobytes())
        digest.update(tensor.numpy().tobytes())
    return digest.hexdigest()


def split_fingerprint(data):
    fields = {}
    for name in ("train_mask", "val_mask", "test_mask", "train_indices", "val_indices", "test_indices"):
        value = getattr(data, name, None)
        fields[name] = None if value is None else torch.as_tensor(value).cpu().tolist()
    return canonical_sha256(fields)


def score_identity(edge_index, num_nodes, candidates):
    nodes = torch.as_tensor(candidates).cpu().tolist()
    return {"graph_fingerprint": graph_fingerprint(edge_index, num_nodes),
            "candidate_set_hash": candidate_fingerprint(nodes, num_nodes),
            "candidate_order_hash": canonical_sha256(nodes),
            "candidate_nodes": nodes, "num_nodes": int(num_nodes)}


TARGET_PARAMETER_NAMES = frozenset("""
base_model unlearning_methods unlearn_trainer downstream_task unlearn_task
is_transductive is_balanced use_batch poison process noise_ratio sparsity_ratio
train_ratio val_ratio test_ratio split_seed num_epochs test_freq batch_size
opt_lr opt_decay std alpha optimizer lam eps compare_gnorm num_unlearned_nodes
proportion_unlearned_nodes resolved_unlearn_k proportion_unlearned_edges
proportion_unlearned_edges_num unlearn_ratio unlearn_lr GUIDE_methods
GUIDE_repair_methods num_shards partition_method opt_num_epochs ratio_deleted_edges
aggregator shard_size_delta terminate_delta is_prune is_partition is_constrained
is_train_target_model is_gen_embedding num_opt_samples test_batch_size
use_test_neighbors repartition random_seed seed hidden_dim gcn_num_layers
gcn_hidden in_dim out_dim unlearning_model df df_idx df_size neg_sample_random
loss_fct loss_type loss train_batch test_batch l2 early_stop patience feature
feature_update emb_dim max_degree damping hidden approx depth GIF_method GIF_exp
is_split iteration scale damp GNN_layer unlearning_epochs Budget lr dropout
weight_decay target_checkpoint_sha256 target_checkpoint_state_hash
para1 para2 para3 para4 para5 folds J Q L remove_guo retrain GST_delta
hop_neighbors dropout_times use_cross_entropy use_adapt_gcs x_iters y_iters
require_linear_span regen_model parallel_unlearning train_mode train_sep
XdegNorm add_self_loops wd featNorm GPR balance_train Y_binary noise_mode
removal_mode delta fix_random_seed compare_retrain compare_guo kappa alpha1
alpha2 is_use_train_batch is_use_test_batch unlearn_feature_partial_ratio
gaussian_mean gaussian_std l c c1 lambda_edge_unlearn gamma_2 trials axis_num
prop_algo prop_step r decay RW rmax ppr weight_mode optuna del_only
num_batch_removes no_retrain edge_idx_start num_removes run_update_detection_auc
M lambda exp parameter_task dataset formal_expected_k formal_fail_closed
""".split())


def target_parameters(args):
    return {key: args[key] for key in sorted(TARGET_PARAMETER_NAMES) if key in args}


@contextmanager
def seeded_execution(seed):
    """Each producer starts from its declared seed, independent of cache hits."""
    python_state, numpy_state = random.getstate(), np.random.get_state()
    try:
        with torch.random.fork_rng():
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            yield
    finally:
        random.setstate(python_state)
        np.random.set_state(numpy_state)
