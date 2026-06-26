"""
GIF / influence-function as a per-node SCORER (feasibility comparison).

Implements the efficient influence form (Koh-Liang; same HVP machinery GIF's
approxi/hvps uses): solve s = H^{-1} grad(L_test) once via a LiSSA iteration,
then score every candidate by infl(v) = <s, grad(loss_v)>. Ranks candidates,
takes top-k, and measures Jaccard set-overlap vs TracIn-self / degree / IM.

NO TRAINING. We load the only trained cora model on disk — the GNNDelete
3-layer checkpoint (data/GNNDelete/checkpoint_node/model_best.pt) — into a plain
3-layer GCN (conv weights only; deletion operators ignored) and compute
influence on it (forward + autograd only). This is a *feasibility* comparison on
an available trained cora GCN, NOT the canonical 2-layer base model; treat the
numbers as directional. The clean run belongs on a freshly trained base GCN
(AutoDL / un-gated train).

Output: self/related_work/concordance/data/gif_cora.json
"""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import sys
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
CKPT = REPO / "data" / "GNNDelete" / "checkpoint_node" / "model_best.pt"

sys.argv = [sys.argv[0], "--dataset_name", "cora", "--base_model", "GCN",
            "--unlearning_methods", "GIF", "--unlearn_ratio", "0.05",
            "--random_seed", "2024", "--cuda", "-1", "--num_epochs", "1", "--batch_size", "64"]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from parameter_parser import parameter_parser
from attack.pipeline_adapter import AttackPipeline


class PlainGCN(torch.nn.Module):
    """3-layer GCN matching the GNNDelete cora checkpoint conv shapes."""
    def __init__(self, in_dim, hid, out_dim):
        super().__init__()
        self.convs = torch.nn.ModuleList([
            GCNConv(in_dim, hid), GCNConv(hid, hid), GCNConv(hid, out_dim)
        ])

    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            if i < len(self.convs) - 1:
                x = F.relu(x)
        return x


def jaccard_topk(a_scores, b_set, k, largest=True):
    a_top = set(int(i) for i in torch.topk(a_scores, k, largest=largest).indices.tolist())
    B = set(int(x) for x in b_set)
    return len(a_top & B) / len(a_top | B) if (a_top | B) else float("nan")


def main():
    args = parameter_parser()
    for kk, vv in {"dataset_name": "cora", "base_model": "GCN", "unlearning_methods": "GIF",
                   "unlearn_ratio": 0.05, "random_seed": 2024, "seed": 2024, "cuda": -1}.items():
        args[kk] = vv

    pipe = AttackPipeline(args)          # data only; no training
    data = pipe.data
    dev = torch.device("cpu")
    x = data.x.to(dev).float()
    ei = data.edge_index.to(dev)
    y = data.y.to(dev)
    tm = data.train_mask
    if tm.dim() > 1:
        tm = tm.squeeze(-1)
    test_m = getattr(data, "test_mask", None)
    if test_m is None:
        test_m = ~tm
    if test_m.dim() > 1:
        test_m = test_m.squeeze(-1)

    in_dim = x.shape[1]
    out_dim = int(y.max().item()) + 1
    model = PlainGCN(in_dim, 64, out_dim).to(dev)

    sd = torch.load(CKPT, map_location="cpu")
    if isinstance(sd, dict) and "model_state" in sd:
        sd = sd["model_state"]
    load_sd = {k: v for k, v in sd.items() if k.startswith("convs.")}
    missing, unexpected = model.load_state_dict(load_sd, strict=False)
    model.eval()

    with torch.no_grad():
        logits = model(x, ei)
        pred = logits.argmax(1)
        train_acc = (pred[tm] == y[tm]).float().mean().item()
        test_acc = (pred[test_m] == y[test_m]).float().mean().item()
    print(f"[gif] loaded conv weights (missing={list(missing)[:3]}...). "
          f"train_acc={train_acc:.3f} test_acc={test_acc:.3f}")

    params = [p for p in model.parameters() if p.requires_grad]
    cand = tm.nonzero(as_tuple=False).view(-1).tolist()
    k = max(int(len(cand) * 0.05), 1)
    print(f"[gif] candidates={len(cand)} k={k}")

    # v = grad(L_test) ; H from L_train (create_graph for HVP)
    out = model(x, ei)
    L_test = F.cross_entropy(out[test_m], y[test_m], reduction="mean")
    v = torch.autograd.grad(L_test, params, retain_graph=True, create_graph=False)
    v = [g.detach() for g in v]

    out2 = model(x, ei)
    L_train = F.cross_entropy(out2[tm], y[tm], reduction="mean")
    grad_train = torch.autograd.grad(L_train, params, create_graph=True)

    def hvp(vec):
        dot = sum((g * w).sum() for g, w in zip(grad_train, vec))
        return [h.detach() for h in torch.autograd.grad(dot, params, retain_graph=True)]

    # LiSSA: s ~= H^{-1} v
    damp, scale, iters = 0.01, 25.0, 100
    h = [vi.clone() for vi in v]
    for _ in range(iters):
        hv = hvp(h)
        h = [vi + (1 - damp) * hi - hvi / scale for vi, hi, hvi in zip(v, h, hv)]
    s = [hi / scale for hi in h]
    s_flat = torch.cat([t.reshape(-1) for t in s])

    # per-candidate grad on a single shared forward
    out3 = model(x, ei)
    n = len(cand)
    gif_scores = torch.empty(n)
    tracin_self = torch.empty(n)
    for idx, node in enumerate(cand):
        loss_v = F.cross_entropy(out3[node:node + 1], y[node:node + 1])
        gv = torch.autograd.grad(loss_v, params, retain_graph=(idx < n - 1))
        gflat = torch.cat([g.reshape(-1) for g in gv])
        gif_scores[idx] = torch.dot(s_flat, gflat).item()
        tracin_self[idx] = gflat.norm().item()

    # reference sets (topology) from the cora selection JSON, remapped to candidate-index space
    cora = json.loads((DATA / "cora_GCN_r0.05_seed2024.json").read_text(encoding="utf-8"))
    cand_pos = {int(nd): i for i, nd in enumerate(cand)}
    def to_pos(nodes):
        return [cand_pos[n] for n in nodes if n in cand_pos]
    deg_set = set(to_pos(cora["selections"]["degree"][:k]))
    im_set = set(to_pos(cora["selections"]["im"][:k]))

    gif_top = set(torch.topk(gif_scores, k, largest=True).indices.tolist())
    tracin_top = set(torch.topk(tracin_self, k, largest=True).indices.tolist())

    def jac(A, B):
        return round(len(A & B) / len(A | B), 3) if (A | B) else None

    res = {
        "model_note": (f"GNNDelete 3-layer cora checkpoint loaded as plain GCN "
                       f"(train_acc={train_acc:.2f}, test_acc={test_acc:.2f}); "
                       f"feasibility only, NOT the canonical 2-layer base model"),
        "k": k,
        "gif_tracin": jac(gif_top, tracin_top),
        "gif_degree": jac(gif_top, deg_set),
        "gif_im": jac(gif_top, im_set),
        "tracin_degree_samemodel": jac(tracin_top, deg_set),
        "note": ("Efficient IF scorer: s=H^{-1} grad(L_test) via 100-step LiSSA "
                 "(damp=0.01, scale=25), infl(v)=<s, grad(loss_v)>. GIF vs TracIn-self "
                 "computed on the SAME loaded model (clean internal validity check); "
                 "degree/IM are topology (model-independent). Directional — see model_note."),
    }
    (DATA / "gif_cora.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
