"""
Model-based selector concordance (TracIn vs real GIF/IF) on a PROPERLY TRAINED
base GCN.

The user authorised training a base model FOR THIS CONCORDANCE STUDY (it is
independent of the GU attack matrix). We:
  1. Build AttackPipeline and call _ensure_base_model_trained() — the pipeline's
     train_only path: trains the canonical base GCN, NO unlearning.
  2. On that SAME trained model, compute:
       - TracIn cross-influence ranking (the user's actual strategy), cache OFF
         so it is bit-on-this-model.
       - GIF/IF ranking via s = H^{-1} grad(L_test) (LiSSA, GIF's HVP) then
         infl(v) = <s, grad(loss_v)>.
       - TracIn self-influence ||grad(loss_v)|| for reference.
  3. Jaccard@k vs degree / IM / pagerank (topology sets from the *_GCN_*.json).

Answers the validity question: does the cheap Hessian-free TracIn pick the same
nodes as the real Hessian-based GIF?  High overlap ⇒ TracIn is a faithful IF
surrogate; low ⇒ they diverge.

Output: self/related_work/concordance/data/modelbased_{dataset}.json
Usage:  python .../concordance_model_based.py --dataset_name cora
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import sys
import json
import time
import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def parse_local():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--dataset_name", default="cora")
    p.add_argument("--base_model", default="GCN")
    p.add_argument("--unlearn_ratio", type=float, default=0.05)
    p.add_argument("--seed", type=int, default=2024)
    p.add_argument("--lissa_iter", type=int, default=100)
    p.add_argument("--lissa_scale", type=float, default=25.0)
    p.add_argument("--lissa_damp", type=float, default=0.01)
    a, _ = p.parse_known_args()
    return a


LOCAL = parse_local()
sys.argv = [sys.argv[0], "--dataset_name", LOCAL.dataset_name, "--base_model", LOCAL.base_model,
            "--unlearning_methods", "GIF", "--unlearn_ratio", str(LOCAL.unlearn_ratio),
            "--proportion_unlearned_nodes", str(LOCAL.unlearn_ratio),
            "--random_seed", str(LOCAL.seed), "--cuda", "-1",
            "--num_epochs", "100", "--batch_size", "64"]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import numpy as np
import torch
# Local sm_120 GPU is incompatible with this torch build; CUDA_VISIBLE_DEVICES=''
# does not stop torch.cuda.is_available() returning True here, so the training
# path tries to launch kernels on the dead GPU. Force CPU everywhere.
torch.cuda.is_available = lambda: False
import torch.nn.functional as F
from parameter_parser import parameter_parser
from attack.pipeline_adapter import AttackPipeline
from attack.attack_strategies import TracInStrategy


def jac(A, B):
    A, B = set(int(x) for x in A), set(int(x) for x in B)
    return round(len(A & B) / len(A | B), 3) if (A | B) else None


def main():
    args = parameter_parser()
    for k, v in {"dataset_name": LOCAL.dataset_name, "base_model": LOCAL.base_model,
                 "unlearning_methods": "GIF", "unlearn_ratio": LOCAL.unlearn_ratio,
                 "random_seed": LOCAL.seed, "seed": LOCAL.seed, "cuda": -1,
                 "num_epochs": 100}.items():
        args[k] = v

    pipe = AttackPipeline(args)
    print("[mb] training base model (train_only; NO unlearning)...")
    t0 = time.time()
    pipe._ensure_base_model_trained()
    model = pipe.model
    model.eval()
    data = pipe.data
    dev = torch.device("cpu")
    data = data.to(dev)
    model = model.to(dev)
    f1 = pipe._evaluate_model(model)
    print(f"[mb] base model trained in {time.time()-t0:.1f}s  test_F1={f1:.3f}")

    tm = data.train_mask
    if tm.dim() > 1:
        tm = tm.squeeze(-1)
    test_m = getattr(data, "test_mask", None)
    if test_m is None:
        test_m = ~tm
    if test_m.dim() > 1:
        test_m = test_m.squeeze(-1)
    cand = tm.nonzero(as_tuple=False).view(-1)
    cand_ids = [int(x) for x in cand.tolist()]
    k = max(int(len(cand_ids) * LOCAL.unlearn_ratio), 1)
    print(f"[mb] candidates={len(cand_ids)} k={k}")

    # --- TracIn (user's strategy, same model, cache OFF) ---
    ts = TracInStrategy({**args, "enable_score_cache": False})
    tracin_scores = ts._compute_tracin_scores(model, data, cand.to(dev))
    tracin_top = [cand_ids[i] for i in torch.topk(tracin_scores, k).indices.tolist()]

    # --- GIF/IF: s = H^{-1} grad(L_test) via LiSSA, then <s, grad(loss_v)> ---
    params = [p for p in model.parameters() if p.requires_grad]

    def fwd():
        try:
            return model(data.x, data.edge_index)
        except TypeError:
            return model(data.x)

    out_t = fwd()
    L_test = F.cross_entropy(out_t[test_m], data.y[test_m], reduction="mean")
    v = [g.detach() for g in torch.autograd.grad(L_test, params)]
    out_h = fwd()
    L_train = F.cross_entropy(out_h[tm], data.y[tm], reduction="mean")
    grad_train = torch.autograd.grad(L_train, params, create_graph=True)

    def hvp(vec):
        dot = sum((g * w).sum() for g, w in zip(grad_train, vec))
        return [h.detach() for h in torch.autograd.grad(dot, params, retain_graph=True)]

    h = [vi.clone() for vi in v]
    for _ in range(LOCAL.lissa_iter):
        hv = hvp(h)
        h = [vi + (1 - LOCAL.lissa_damp) * hi - hvi / LOCAL.lissa_scale
             for vi, hi, hvi in zip(v, h, hv)]
    s_flat = torch.cat([(hi / LOCAL.lissa_scale).reshape(-1) for hi in h])
    print(f"[mb] LiSSA done; ||s||={s_flat.norm().item():.3g} (finite={torch.isfinite(s_flat).all().item()})")

    out_g = fwd()
    n = len(cand_ids)
    gif_scores = torch.empty(n)
    tracin_self = torch.empty(n)
    for idx, node in enumerate(cand_ids):
        lv = F.cross_entropy(out_g[node:node + 1], data.y[node:node + 1])
        gv = torch.autograd.grad(lv, params, retain_graph=(idx < n - 1))
        gflat = torch.cat([g.reshape(-1) for g in gv])
        gif_scores[idx] = torch.dot(s_flat, gflat).item()
        tracin_self[idx] = gflat.norm().item()
    gif_top = [cand_ids[i] for i in torch.topk(gif_scores, k).indices.tolist()]
    tself_top = [cand_ids[i] for i in torch.topk(tracin_self, k).indices.tolist()]

    # --- topology reference sets ---
    topo = json.loads((DATA / f"{LOCAL.dataset_name}_{LOCAL.base_model}_r{LOCAL.unlearn_ratio}_seed{LOCAL.seed}.json").read_text(encoding="utf-8"))
    deg = topo["selections"]["degree"][:k]
    im = topo["selections"]["im"][:k]
    pr = topo["selections"]["pagerank"][:k]

    res = {
        "dataset": LOCAL.dataset_name, "base_model": LOCAL.base_model, "k": k,
        "test_f1": round(float(f1), 4),
        "lissa": {"iter": LOCAL.lissa_iter, "scale": LOCAL.lissa_scale, "damp": LOCAL.lissa_damp,
                  "s_norm": round(float(s_flat.norm().item()), 4)},
        "jaccard": {
            "gif_tracin": jac(gif_top, tracin_top),          # <-- the validity number
            "gif_tracinself": jac(gif_top, tself_top),
            "gif_degree": jac(gif_top, deg),
            "gif_im": jac(gif_top, im),
            "tracin_degree": jac(tracin_top, deg),
            "tracin_im": jac(tracin_top, im),
            "tracin_pagerank": jac(tracin_top, pr),
        },
        "note": "GIF (s=H^-1 grad L_test, LiSSA) vs TracIn (cross-influence) on the SAME trained base GCN. degree/im/pagerank are topology.",
    }
    (DATA / f"modelbased_{LOCAL.dataset_name}.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
