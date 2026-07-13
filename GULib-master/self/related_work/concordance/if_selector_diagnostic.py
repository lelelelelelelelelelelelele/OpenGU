"""
IF-style selector diagnostic on a trained base model.

This script is selector-only: it trains/loads the canonical base model via the
AttackPipeline train_only path, computes several IF/TracIn scoring variants on
the same candidate pool, and compares their top-k overlap. It does not run any
graph-unlearning method.

Outputs:
    self/related_work/concordance/data/
    ifdiag_{dataset}_{base_model}_r{ratio}_seed{seed}_{recipe_hash12}.json

Canonical Cora reproduction command:
    E:/conda_package/envs/gnn/python.exe \
      self/related_work/concordance/if_selector_diagnostic.py \
      --dataset_name cora --base_model GCN --unlearn_ratio 0.05 \
      --seed 2024 --num_epochs 100 --batch_size 64 \
      --lissa_iter 100 --lissa_scale 25.0 --lissa_damp 0.01 \
      --hutch_probes 32 --hutch_seed 1729

The default recipe-hashed path prevents different configurations from sharing
one filename. Existing files are never replaced unless --overwrite is passed,
and --overwrite is accepted only when the stored recipe hash matches exactly.
"""
import argparse
import hashlib
import json
import os
import random
import shlex
import sys
import tempfile
import time
from pathlib import Path

# Keep this diagnostic on CPU. The local Windows GPU stack is not compatible
# with the pinned torch build used by this project.
os.environ["CUDA_VISIBLE_DEVICES"] = ""

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DIAGNOSTIC_SCHEMA_VERSION = "if-selector-diagnostic-result/2.0.0"
ALGORITHM_VERSION = "if-selector-diagnostic/2.0.0"


def build_parser():
    p = argparse.ArgumentParser(
        description=(
            "CPU-only selector diagnostic; trains/loads a base model but does "
            "not run graph unlearning."
        )
    )
    p.add_argument("--dataset_name", default="cora")
    p.add_argument("--base_model", default="GCN")
    p.add_argument("--unlearn_ratio", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=2024)
    p.add_argument("--num_epochs", type=int, default=100)
    p.add_argument("--batch_size", type=int, default=64)
    p.add_argument("--lissa_iter", type=int, default=100)
    p.add_argument("--lissa_scale", type=float, default=25.0)
    p.add_argument("--lissa_damp", type=float, default=0.01)
    p.add_argument("--hutch_probes", type=int, default=32)
    p.add_argument("--hutch_seed", type=int, default=1729)
    p.add_argument(
        "--output_path",
        type=Path,
        default=None,
        help=(
            "Optional output path. Relative paths are resolved from the repo "
            "root; by default the filename includes the stable recipe hash."
        ),
    )
    p.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Replace an existing output only if its stored recipe hash is an "
            "exact match; a different or unverifiable recipe is always refused."
        ),
    )
    return p


def parse_local(argv=None):
    return build_parser().parse_args(argv)


def _sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def _script_fingerprint():
    # Normalize line endings so a Windows checkout and a Linux checkout of the
    # same source have the same implementation fingerprint.
    source = Path(__file__).read_text(encoding="utf-8").replace("\r\n", "\n")
    return _sha256_bytes(source.encode("utf-8"))


def _topology_sidecar(local):
    path = DATA / (
        f"{local.dataset_name}_{local.base_model}_"
        f"r{local.unlearn_ratio}_seed{local.seed}.json"
    )
    if not path.exists():
        return None
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": _sha256_bytes(path.read_bytes()),
        "imported_selectors": ["degree", "pagerank", "im"],
        "selection_rule": "take first k nodes from each available selection",
    }


def build_recipe(local):
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "implementation": {
            "script": Path(__file__).resolve().relative_to(REPO).as_posix(),
            "script_sha256": _script_fingerprint(),
        },
        "dataset": local.dataset_name,
        "base_model": local.base_model,
        "unlearn_ratio": local.unlearn_ratio,
        "training": {
            "pipeline": "AttackPipeline.train_only",
            "seed": local.seed,
            "num_epochs": local.num_epochs,
            "batch_size": local.batch_size,
            "device": "cpu",
        },
        "candidate_set": {
            "mask": "train_mask",
            "k_rule": "max(floor(num_candidates * unlearn_ratio), 1)",
        },
        "evaluation_set": {
            "primary_mask": "test_mask",
            "fallback_mask": "logical_not(train_mask)",
            "use": "mechanism diagnostic only; not a deployable attack query set",
        },
        "loss": {
            "function": "cross_entropy",
            "train_reduction": "mean",
            "evaluation_reduction": "mean",
            "candidate_pool_reduction": "sum",
            "per_candidate_reduction": "single",
        },
        "inverse_hessian": {
            "solver": "LiSSA",
            "iterations": local.lissa_iter,
            "scale": local.lissa_scale,
            "damp": local.lissa_damp,
            "parameter_change_norm_estimator": "shared Rademacher Hutchinson probes",
            "hutch_probes": local.hutch_probes,
            "hutch_seed": local.hutch_seed,
        },
        "score_set": [
            "grad_norm",
            "deployed_cross_tracin",
            "eval_proper_tracin",
            "eval_if_gif",
            "model_hinv_norm_hutch",
        ],
        "topology_sidecar": _topology_sidecar(local),
    }


def canonical_recipe_json(recipe):
    return json.dumps(recipe, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def recipe_hash(recipe):
    return _sha256_bytes(canonical_recipe_json(recipe).encode("utf-8"))


def resolve_output_path(local, digest):
    if local.output_path is not None:
        path = local.output_path
        return path.resolve() if path.is_absolute() else (REPO / path).resolve()
    return DATA / (
        f"ifdiag_{local.dataset_name}_{local.base_model}_"
        f"r{local.unlearn_ratio}_seed{local.seed}_{digest[:12]}.json"
    )


def canonical_reproduction_command(local):
    command = [
        "E:/conda_package/envs/gnn/python.exe",
        "self/related_work/concordance/if_selector_diagnostic.py",
        "--dataset_name", local.dataset_name,
        "--base_model", local.base_model,
        "--unlearn_ratio", str(local.unlearn_ratio),
        "--seed", str(local.seed),
        "--num_epochs", str(local.num_epochs),
        "--batch_size", str(local.batch_size),
        "--lissa_iter", str(local.lissa_iter),
        "--lissa_scale", str(local.lissa_scale),
        "--lissa_damp", str(local.lissa_damp),
        "--hutch_probes", str(local.hutch_probes),
        "--hutch_seed", str(local.hutch_seed),
    ]
    if local.output_path is not None:
        command.extend(["--output_path", local.output_path.as_posix()])
    return shlex.join(command)


def validate_output_target(path, expected_recipe_hash, overwrite):
    if not path.exists():
        return
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"refusing to replace unreadable existing output: {path}"
        ) from exc
    existing_hash = existing.get("recipe_hash")
    if existing_hash != expected_recipe_hash:
        observed = existing_hash or "missing (legacy/unverifiable output)"
        raise RuntimeError(
            "refusing to replace output with a different or unverifiable recipe: "
            f"{path}; expected={expected_recipe_hash}, observed={observed}"
        )
    if not overwrite:
        raise FileExistsError(
            f"output already exists for this exact recipe: {path}; "
            "pass --overwrite to replace it explicitly"
        )


def write_json_atomic(path, result, overwrite=False):
    expected_hash = result["recipe_hash"]
    validate_output_target(path, expected_hash, overwrite)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        # Re-check immediately before replacement to fail closed if another
        # process created or changed the destination while this run computed.
        validate_output_target(path, expected_hash, overwrite)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def load_runtime(local):
    framework_argv = [
        sys.argv[0],
        "--dataset_name", local.dataset_name,
        "--base_model", local.base_model,
        "--unlearning_methods", "GIF",
        "--unlearn_ratio", str(local.unlearn_ratio),
        "--proportion_unlearned_nodes", str(local.unlearn_ratio),
        "--random_seed", str(local.seed),
        "--cuda", "-1",
        "--num_epochs", str(local.num_epochs),
        "--batch_size", str(local.batch_size),
    ]
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    original_argv = sys.argv
    sys.argv = framework_argv
    try:
        import numpy as np
        import torch
        import torch.nn.functional as F
        from parameter_parser import parameter_parser
        from attack.pipeline_adapter import AttackPipeline
        framework_args = parameter_parser()
    finally:
        sys.argv = original_argv
    torch.cuda.is_available = lambda: False
    return np, torch, F, framework_args, AttackPipeline


def seed_everything(seed, np, torch):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def flatten_tensors(items, torch):
    return torch.cat([x.reshape(-1) for x in items])


def unflatten_like(flat, refs):
    out = []
    offset = 0
    for ref in refs:
        n = ref.numel()
        out.append(flat[offset:offset + n].view_as(ref))
        offset += n
    return out


def jaccard(a, b):
    if not a or not b:
        return None
    aa = set(int(x) for x in a)
    bb = set(int(x) for x in b)
    return round(len(aa & bb) / len(aa | bb), 4) if (aa | bb) else None


def top_nodes(scores, cand_ids, k, torch, largest=True):
    idx = torch.topk(scores, k, largest=largest).indices.tolist()
    return [int(cand_ids[i]) for i in idx]


def matrix(selections):
    names = list(selections)
    return {
        a: {b: jaccard(selections[a], selections[b]) for b in names}
        for a in names
    }


def main(argv=None):
    local = parse_local(argv)
    recipe = build_recipe(local)
    digest = recipe_hash(recipe)
    out_path = resolve_output_path(local, digest)
    # Refuse a known collision before paying the model-training cost. The same
    # validation is repeated atomically at write time.
    validate_output_target(out_path, digest, local.overwrite)

    np, torch, F, args, AttackPipeline = load_runtime(local)
    seed_everything(local.seed, np, torch)
    for key, value in {
        "dataset_name": local.dataset_name,
        "base_model": local.base_model,
        "unlearning_methods": "GIF",
        "unlearn_ratio": local.unlearn_ratio,
        "random_seed": local.seed,
        "seed": local.seed,
        "cuda": -1,
        "num_epochs": local.num_epochs,
        "batch_size": local.batch_size,
    }.items():
        args[key] = value

    pipe = AttackPipeline(args)
    print("[ifdiag] training base model (train_only; no unlearning)...")
    t0 = time.time()
    pipe._ensure_base_model_trained()
    model = pipe.model
    model.eval()
    data = pipe.data
    dev = torch.device("cpu")
    data = data.to(dev)
    model = model.to(dev)
    f1 = pipe._evaluate_model(model)
    print(f"[ifdiag] base model ready in {time.time() - t0:.1f}s test_F1={f1:.4f}")

    train_mask = data.train_mask
    if train_mask.dim() > 1:
        train_mask = train_mask.squeeze(-1)
    eval_mask = getattr(data, "test_mask", None)
    if eval_mask is None:
        eval_mask = ~train_mask
    if eval_mask.dim() > 1:
        eval_mask = eval_mask.squeeze(-1)

    candidates = train_mask.nonzero(as_tuple=False).view(-1)
    cand_ids = [int(x) for x in candidates.tolist()]
    k = max(int(len(cand_ids) * local.unlearn_ratio), 1)
    print(f"[ifdiag] candidates={len(cand_ids)} k={k}")

    params = [p for p in model.parameters() if p.requires_grad]
    num_params = sum(p.numel() for p in params)
    print(f"[ifdiag] trainable_params={num_params}")

    def fwd():
        try:
            return model(data.x, data.edge_index)
        except TypeError:
            return model(data.x)

    out_train = fwd()
    train_loss = F.cross_entropy(out_train[train_mask], data.y[train_mask], reduction="mean")
    grad_train = torch.autograd.grad(train_loss, params, create_graph=True)

    out_eval = fwd()
    eval_loss = F.cross_entropy(out_eval[eval_mask], data.y[eval_mask], reduction="mean")
    grad_eval = [g.detach() for g in torch.autograd.grad(eval_loss, params)]
    grad_eval_flat = flatten_tensors(grad_eval, torch)

    out_cand = fwd()
    cand_loss_sum = F.cross_entropy(out_cand[candidates], data.y[candidates], reduction="sum")
    grad_cand_sum = [g.detach() for g in torch.autograd.grad(cand_loss_sum, params)]
    grad_cand_sum_flat = flatten_tensors(grad_cand_sum, torch)
    print(
        "[ifdiag] vector norms "
        f"grad_eval={grad_eval_flat.norm().item():.4g} "
        f"grad_cand_sum={grad_cand_sum_flat.norm().item():.4g}"
    )

    def hvp(vec):
        dot = sum((g * v).sum() for g, v in zip(grad_train, vec))
        return [h.detach() for h in torch.autograd.grad(dot, params, retain_graph=True)]

    def lissa_inverse(vec):
        estimate = [v.detach().clone() for v in vec]
        for _ in range(local.lissa_iter):
            hv = hvp(estimate)
            estimate = [
                v + (1.0 - local.lissa_damp) * e - h / local.lissa_scale
                for v, e, h in zip(vec, estimate, hv)
            ]
        return [e / local.lissa_scale for e in estimate]

    print("[ifdiag] solving H^-1 grad_eval...")
    inv_eval = lissa_inverse(grad_eval)
    inv_eval_flat = flatten_tensors(inv_eval, torch)
    print(f"[ifdiag] ||H^-1 grad_eval||={inv_eval_flat.norm().item():.4g}")

    print(f"[ifdiag] solving H^-1 Hutchinson probes n={local.hutch_probes}...")
    rng = torch.Generator(device="cpu")
    rng.manual_seed(local.hutch_seed)
    inv_probe_flats = []
    ref_flat = flatten_tensors([p.detach() for p in params], torch)
    for probe_idx in range(local.hutch_probes):
        # Rademacher probe in parameter space. Shared inverse solves allow an
        # efficient Hutchinson estimate of ||H^-1 g_v|| for every candidate:
        # ||H^-1 g||^2 = E_z [(H^-1 z)^T g]^2 for symmetric H.
        probe_flat = torch.randint(
            0, 2, ref_flat.shape, generator=rng, dtype=torch.float32
        ) * 2.0 - 1.0
        probe = unflatten_like(probe_flat, params)
        inv_probe = lissa_inverse(probe)
        inv_probe_flats.append(flatten_tensors(inv_probe, torch))
        print(f"[ifdiag] probe {probe_idx + 1}/{local.hutch_probes} done")
    inv_probe_mat = torch.stack(inv_probe_flats) if inv_probe_flats else torch.empty(0, num_params)

    out_nodes = fwd()
    n = len(cand_ids)
    scores = {
        "grad_norm": torch.empty(n),
        "deployed_cross_tracin": torch.empty(n),
        "eval_proper_tracin": torch.empty(n),
        "eval_if_gif": torch.empty(n),
        "model_hinv_norm_hutch": torch.empty(n),
    }

    for idx, node in enumerate(cand_ids):
        loss_v = F.cross_entropy(out_nodes[node:node + 1], data.y[node:node + 1])
        grad_v = torch.autograd.grad(loss_v, params, retain_graph=(idx < n - 1))
        grad_v_flat = flatten_tensors(grad_v, torch).detach()

        scores["grad_norm"][idx] = grad_v_flat.norm()
        scores["deployed_cross_tracin"][idx] = -torch.dot(grad_cand_sum_flat, grad_v_flat)
        scores["eval_proper_tracin"][idx] = torch.dot(grad_eval_flat, grad_v_flat)
        scores["eval_if_gif"][idx] = torch.dot(inv_eval_flat, grad_v_flat)
        if local.hutch_probes > 0:
            proj = inv_probe_mat @ grad_v_flat
            scores["model_hinv_norm_hutch"][idx] = torch.sqrt(torch.mean(proj * proj).clamp_min(0.0))
        else:
            scores["model_hinv_norm_hutch"][idx] = float("nan")

        if (idx + 1) % 250 == 0 or idx + 1 == n:
            print(f"[ifdiag] scored {idx + 1}/{n}")

    selections = {
        name: top_nodes(value, cand_ids, k, torch)
        for name, value in scores.items()
    }

    topo_path = DATA / (
        f"{local.dataset_name}_{local.base_model}_"
        f"r{local.unlearn_ratio}_seed{local.seed}.json"
    )
    if topo_path.exists():
        topo = json.loads(topo_path.read_text(encoding="utf-8"))
        for name in ("degree", "pagerank", "im"):
            if name in topo.get("selections", {}):
                selections[name] = [int(x) for x in topo["selections"][name][:k]]

    score_stats = {}
    for name, value in scores.items():
        finite = value[torch.isfinite(value)]
        score_stats[name] = {
            "min": round(float(finite.min().item()), 6) if finite.numel() else None,
            "max": round(float(finite.max().item()), 6) if finite.numel() else None,
            "mean": round(float(finite.mean().item()), 6) if finite.numel() else None,
            "std": round(float(finite.std(unbiased=False).item()), 6) if finite.numel() else None,
        }

    result = {
        "diagnostic_schema_version": DIAGNOSTIC_SCHEMA_VERSION,
        "algorithm_version": ALGORITHM_VERSION,
        "recipe_hash": digest,
        "recipe": recipe,
        "reproduction_command": canonical_reproduction_command(local),
        "dataset": local.dataset_name,
        "base_model": local.base_model,
        "ratio": local.unlearn_ratio,
        "seed": local.seed,
        "k": k,
        "num_candidates": len(cand_ids),
        "test_f1": round(float(f1), 6),
        "config": {
            "num_epochs": local.num_epochs,
            "batch_size": local.batch_size,
            "lissa_iter": local.lissa_iter,
            "lissa_scale": local.lissa_scale,
            "lissa_damp": local.lissa_damp,
            "hutch_probes": local.hutch_probes,
            "hutch_seed": local.hutch_seed,
        },
        "score_definitions": {
            "grad_norm": "||grad loss_v||; Hessian-free model-state proxy",
            "model_hinv_norm_hutch": "Hutchinson estimate of ||H_train^-1 grad loss_v||",
            "eval_proper_tracin": "<grad L_eval, grad loss_v>; Hessian-free eval-impact TracIn",
            "eval_if_gif": "<H_train^-1 grad L_eval, grad loss_v>; eval-impact IF/GIF",
            "deployed_cross_tracin": "-<sum_candidate grad loss_j, grad loss_v>; legacy training-residual alignment",
        },
        "score_stats": score_stats,
        "selections": selections,
        "jaccard": matrix(selections),
    }

    write_json_atomic(out_path, result, overwrite=local.overwrite)
    print(f"[ifdiag] wrote {out_path}")
    print(json.dumps({
        "dataset": result["dataset"],
        "base_model": result["base_model"],
        "k": result["k"],
        "key_jaccard": {
            "model_hinv_vs_grad_norm": result["jaccard"]["model_hinv_norm_hutch"]["grad_norm"],
            "model_hinv_vs_eval_if": result["jaccard"]["model_hinv_norm_hutch"]["eval_if_gif"],
            "eval_proper_vs_eval_if": result["jaccard"]["eval_proper_tracin"]["eval_if_gif"],
            "deployed_cross_vs_eval_if": result["jaccard"]["deployed_cross_tracin"]["eval_if_gif"],
            "model_hinv_vs_degree": result["jaccard"]["model_hinv_norm_hutch"].get("degree"),
            "model_hinv_vs_im": result["jaccard"]["model_hinv_norm_hutch"].get("im"),
        },
    }, indent=2))


if __name__ == "__main__":
    main()
