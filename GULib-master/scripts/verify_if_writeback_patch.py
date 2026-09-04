"""Verify real IF-family write-back on fixed CPU tensors, without experiments."""
from __future__ import annotations

import copy
import hashlib
from pathlib import Path
import sys

import torch
import torch.nn as nn

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class TrainerStub:
    """Record evaluation parameters without writing them into the model."""
    def __init__(self):
        self.model = nn.Linear(2, 2)
        with torch.no_grad():
            self.model.weight.copy_(torch.eye(2))
            self.model.bias.zero_()
        self.model.bias.requires_grad_(False)
        self.evaluated_params = None

    def eval_unlearn(self, params):
        self.evaluated_params = [p.detach().clone() for p in params]
        return 0.5

    def evaluate_unlearn_F1(self, params, edge_weight_unlearn=None):
        return self.eval_unlearn(params)


def check_model_writeback(label, pipeline_class):
    """Call production approxi and the production model/metric consumers.

    Only fixed CPU fixtures are used. The comparison model is not a retraining
    result. No constructor, trainer, dataset loader, cache or runner is invoked.
    """
    from attack.attack_eval import evaluate_collateral_damage
    from attack.pipeline_adapter import AttackPipeline
    from torch_geometric.data import Data

    method = pipeline_class.__new__(pipeline_class)
    method.target_model = TrainerStub()
    method.args = {
        "iteration": 1, "damp": 0.0, "scale": 2.0,
        "dataset_name": "Cora", "GIF_method": "GIF",
        "gaussian_std": 0.0, "gaussian_mean": 0.25,
    }
    method.edge_weight_unlearn = None
    # Isolate write-back from the expensive Hessian calculation.
    method.hvps = lambda gradients, params, estimate: [torch.zeros_like(p) for p in params]
    before = copy.deepcopy(method.target_model.model)
    zero = (torch.zeros(2, 2),)
    direction = (torch.tensor([[-4.0, 4.0], [4.0, -4.0]]),)
    method.approxi((zero, direction, zero))

    trainer = method.target_model
    assert trainer.evaluated_params is not None, "updated parameters were not evaluated"
    expected = trainer.evaluated_params[0]
    assert not torch.equal(expected, before.weight), "fixture must produce a nonzero update"
    assert torch.equal(trainer.model.weight, expected), "write-back missing: model retains stale weights"
    assert torch.equal(trainer.model.bias, before.bias), "frozen parameter changed"

    consumer = AttackPipeline.__new__(AttackPipeline)
    consumer.method = method
    consumer.args = {"unlearning_methods": label}
    model = consumer._get_trained_model()
    assert model is trainer.model, "collateral consumer extracted a different model"

    reference = copy.deepcopy(before)
    with torch.no_grad():
        reference.weight.copy_(expected)
    data = Data(
        x=torch.tensor([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]]),
        edge_index=torch.tensor([[0, 1, 1, 2], [1, 0, 2, 1]]),
    )
    retain = torch.tensor([False, True, True])
    stale = evaluate_collateral_damage(before, reference, data, retain, [0], max_hop=2)
    observed = evaluate_collateral_damage(model, reference, data, retain, [0], max_hop=2)
    assert stale["fraction_flipped"] == 1.0, "fixture must distinguish stale predictions"
    assert observed["fraction_flipped"] == 0.0, "collateral still sees stale predictions"
    assert observed["mean_pred_shift"] == 0.0, "collateral sees different update parameters"
    for hop in (1, 2):
        assert observed["hop_decay"][f"{hop}_hop_count"] == 1
        assert stale["hop_decay"][f"{hop}_hop_flip_rate"] == 1.0
        assert observed["hop_decay"][f"{hop}_hop_flip_rate"] == 0.0
    return observed


def verify_loaded_writeback(label, pipeline_class, relative_path):
    expected_path = (REPO_ROOT / relative_path).resolve()
    loaded_path = Path(pipeline_class.approxi.__code__.co_filename).resolve()
    print(f"  loaded {label} source: {loaded_path}")
    if loaded_path != expected_path:
        print(f"  [FAIL] expected active-checkout source: {expected_path}")
        return False
    try:
        check_model_writeback(label, pipeline_class)
    except AssertionError as error:
        print(f"  [FAIL] {label}: {error}")
        return False
    digest = hashlib.sha256(expected_path.read_bytes()).hexdigest()
    print(f"  [OK] {label} actual approxi -> model -> collateral/hop fixture; source_sha256={digest}")
    return True


def main():
    # Direct execution supplies the intentional minimal CLI context needed by
    # config.py when importing the actual methods; this script has no options.
    from unlearning.unlearning_methods.GIF.gif import gif
    from unlearning.unlearning_methods.IDEA.idea import idea

    print("Fixed CPU software fixtures only; no experiment or retraining run.")
    outcomes = [
        verify_loaded_writeback("GIF", gif, "unlearning/unlearning_methods/GIF/gif.py"),
        verify_loaded_writeback("IDEA", idea, "unlearning/unlearning_methods/IDEA/idea.py"),
    ]
    if all(outcomes):
        print("\nALL CHECKS PASSED")
        return 0
    print("\nSOME CHECKS FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
