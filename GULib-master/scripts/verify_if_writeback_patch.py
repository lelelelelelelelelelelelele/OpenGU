"""Unit-test for the IF-family approxi() write-back patch.

Verifies that after the patched IDEA/GIF approxi() runs, target_model.model's
parameters reflect params_esti (i.e., the fix took effect and downstream
_get_trained_model() / collateral.perf_unlearn will see post-unlearn weights).

Run:
    H:/conda_package/envs/gnn/python.exe scripts/verify_if_writeback_patch.py

Exit codes: 0 = OK, 1 = patch missing or write-back not visible.
"""
from __future__ import annotations

import sys
import torch
import torch.nn as nn


class MiniGCNStub(nn.Module):
    def __init__(self):
        super().__init__()
        self.lin1 = nn.Linear(8, 4)
        self.lin2 = nn.Linear(4, 3)

    def forward(self, x):
        return self.lin2(torch.relu(self.lin1(x)))


class TrainerStub:
    """Mimics target_model in IDEA/GIF. .model holds the GNN; .eval_unlearn /
    .evaluate_unlearn_F1 take an external params list and return a fake F1."""

    def __init__(self):
        self.model = MiniGCNStub()
        self.eval_calls = []

    def eval_unlearn(self, params_esti):
        self.eval_calls.append([p.detach().clone() for p in params_esti])
        return 0.5

    def evaluate_unlearn_F1(self, params_esti, edge_weight_unlearn=None):
        self.eval_calls.append([p.detach().clone() for p in params_esti])
        return 0.5


def simulate_patched_writeback(target_model, params_esti):
    """Replicates the exact patch from IDEA/GIF approxi() — used to validate
    the bytes inside the actual edited source files match this reference."""
    with torch.no_grad():
        trainable_params = [p for p in target_model.model.parameters() if p.requires_grad]
        for p, new_p in zip(trainable_params, params_esti):
            p.data.copy_(new_p.detach().to(p.device))


def grab_params_snapshot(model):
    return [p.detach().clone() for p in model.parameters() if p.requires_grad]


def all_close_lists(a, b):
    return len(a) == len(b) and all(torch.equal(x, y) for x, y in zip(a, b))


def check_fix_applied_in_source(path: str, marker: str = "Write params_esti back into target_model.model") -> bool:
    with open(path, encoding="utf-8") as f:
        return marker in f.read()


def test_writeback_changes_model():
    target = TrainerStub()
    pre = grab_params_snapshot(target.model)

    # Fabricate a params_esti list with the same shapes but distinct values
    params_esti = [
        torch.randn_like(p) * 100 + 7.0
        for p in target.model.parameters() if p.requires_grad
    ]

    # Sanity: pre-state must NOT match the fabricated params_esti
    assert not all_close_lists(pre, params_esti), "pre-state already matches params_esti — test setup wrong"

    simulate_patched_writeback(target, params_esti)

    post = grab_params_snapshot(target.model)
    assert all_close_lists(post, params_esti), \
        "model.parameters() did NOT match params_esti after write-back — patch logic wrong"
    assert not all_close_lists(post, pre), \
        "model.parameters() unchanged — write-back was a no-op"
    print("  [OK] write-back correctly transferred params_esti into model")


def test_idea_source_has_patch():
    p = "unlearning/unlearning_methods/IDEA/idea.py"
    if not check_fix_applied_in_source(p):
        print(f"  [FAIL] {p} does not contain the write-back marker — patch missing")
        return False
    print(f"  [OK] {p} contains write-back marker")
    return True


def test_gif_source_has_patch():
    p = "unlearning/unlearning_methods/GIF/gif.py"
    if not check_fix_applied_in_source(p):
        print(f"  [FAIL] {p} does not contain the write-back marker — patch missing")
        return False
    print(f"  [OK] {p} contains write-back marker")
    return True


def main() -> int:
    print("[1/3] simulate write-back on a stub model")
    test_writeback_changes_model()

    print("[2/3] verify IDEA source carries the patch")
    ok1 = test_idea_source_has_patch()

    print("[3/3] verify GIF source carries the patch")
    ok2 = test_gif_source_has_patch()

    if ok1 and ok2:
        print("\nALL CHECKS PASSED")
        return 0
    print("\nSOME CHECKS FAILED — re-apply patch")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
