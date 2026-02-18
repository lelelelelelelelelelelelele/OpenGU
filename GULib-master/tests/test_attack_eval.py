"""Unit tests for attack/attack_eval.py evaluation module."""

import torch
import torch.nn as nn
from torch_geometric.data import Data
from sklearn.metrics import f1_score

from attack.attack_eval import (
    evaluate_f1_drop,
    evaluate_mia_auc,
    evaluate_retrain_gap,
    evaluate_collateral_damage,
    compute_gap_statistics,
)


# ---------------------------------------------------------------------------
# Helpers (same style as test_im_hybrid.py)
# ---------------------------------------------------------------------------

def _make_dummy_data(num_nodes=100, num_features=16, num_classes=7):
    x = torch.randn(num_nodes, num_features)
    edge_index = torch.randint(0, num_nodes, (2, 300))
    y = torch.randint(0, num_classes, (num_nodes,))
    test_mask = torch.zeros(num_nodes, dtype=torch.bool)
    test_mask[80:] = True
    return Data(x=x, edge_index=edge_index, y=y, test_mask=test_mask)


def _make_dummy_model(num_features=16, num_classes=7):
    class DummyGNN(nn.Module):
        def __init__(self, in_ch, out_ch):
            super().__init__()
            self.lin = nn.Linear(in_ch, out_ch)

        def forward(self, x, edge_index=None):
            return self.lin(x)

    return DummyGNN(num_features, num_classes)


def _make_trained_model(data, num_features=16, num_classes=7, steps=200):
    """Train a model briefly so it has non-trivial accuracy."""
    model = _make_dummy_model(num_features, num_classes)
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    for _ in range(steps):
        model.train()
        out = model(data.x)
        loss = nn.functional.cross_entropy(out, data.y)
        opt.zero_grad()
        loss.backward()
        opt.step()
    return model


# ===========================================================================
# TestEvaluateF1Drop
# ===========================================================================

class TestEvaluateF1Drop:
    def test_same_model_zero_drop(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        result = evaluate_f1_drop(model, model, data, data.test_mask)
        assert result["f1_drop"] == 0.0
        assert result["f1_drop_pct"] == 0.0

    def test_positive_drop(self):
        data = _make_dummy_data()
        trained = _make_trained_model(data)
        random_model = _make_dummy_model()
        result = evaluate_f1_drop(trained, random_model, data, data.test_mask)
        # Trained model should generally outperform random init
        assert result["f1_drop"] >= 0.0

    def test_matches_sklearn(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        result = evaluate_f1_drop(model, model, data, data.test_mask)
        # Manually compute
        model.eval()
        with torch.no_grad():
            logits = model(data.x).cpu().numpy()
        preds = logits.argmax(axis=1)
        mask = data.test_mask.cpu()
        expected = f1_score(data.y.cpu().numpy()[mask], preds[mask], average="micro")
        assert abs(result["f1_before"] - expected) < 1e-6

    def test_return_keys(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        result = evaluate_f1_drop(model, model, data, data.test_mask)
        assert set(result.keys()) == {"f1_before", "f1_after", "f1_drop", "f1_drop_pct"}


# ===========================================================================
# TestEvaluateMiaAuc
# ===========================================================================

class TestEvaluateMiaAuc:
    def test_random_model_near_half(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        member_mask = torch.zeros(100, dtype=torch.bool)
        member_mask[:50] = True
        non_member_mask = ~member_mask
        auc = evaluate_mia_auc(model, data, member_mask, non_member_mask)
        assert 0.0 <= auc <= 1.0

    def test_empty_member_returns_half(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        empty = torch.zeros(100, dtype=torch.bool)
        non_empty = torch.ones(100, dtype=torch.bool)
        assert evaluate_mia_auc(model, data, empty, non_empty) == 0.5

    def test_empty_non_member_returns_half(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        non_empty = torch.ones(100, dtype=torch.bool)
        empty = torch.zeros(100, dtype=torch.bool)
        assert evaluate_mia_auc(model, data, non_empty, empty) == 0.5

    def test_return_type(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        member_mask = torch.zeros(100, dtype=torch.bool)
        member_mask[:50] = True
        auc = evaluate_mia_auc(model, data, member_mask, ~member_mask)
        assert isinstance(auc, float)


# ===========================================================================
# TestEvaluateRetrainGap
# ===========================================================================

class TestEvaluateRetrainGap:
    def test_same_model_zero_gap(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        result = evaluate_retrain_gap(model, model, model, data, data.test_mask)
        assert result["gap"] == 0.0
        assert result["drop_retrain"] == 0.0

    def test_return_keys(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        result = evaluate_retrain_gap(model, model, model, data, data.test_mask)
        expected_keys = {"perf_before", "perf_retrain", "perf_unlearn",
                         "drop_retrain", "gap", "gap_pct"}
        assert set(result.keys()) == expected_keys

    def test_gap_decomposition(self):
        """drop_retrain + gap should equal perf_before - perf_unlearn."""
        data = _make_dummy_data()
        m1 = _make_dummy_model()
        m2 = _make_dummy_model()
        m3 = _make_dummy_model()
        result = evaluate_retrain_gap(m1, m2, m3, data, data.test_mask)
        total = result["drop_retrain"] + result["gap"]
        expected = result["perf_before"] - result["perf_unlearn"]
        assert abs(total - expected) < 1e-6


# ===========================================================================
# TestEvaluateCollateralDamage
# ===========================================================================

class TestEvaluateCollateralDamage:
    def test_same_model_zero_shift(self):
        """Same model as both unlearned and retrained → zero shift."""
        data = _make_dummy_data()
        model = _make_dummy_model()
        retain_mask = torch.ones(100, dtype=torch.bool)
        result = evaluate_collateral_damage(
            model_unlearned=model, model_retrained=model,
            data=data, retain_mask=retain_mask,
        )
        assert abs(result["mean_pred_shift"]) < 1e-6
        assert result["fraction_flipped"] == 0.0

    def test_return_keys(self):
        data = _make_dummy_data()
        model = _make_dummy_model()
        retain_mask = torch.ones(100, dtype=torch.bool)
        result = evaluate_collateral_damage(
            model_unlearned=model, model_retrained=model,
            data=data, retain_mask=retain_mask,
        )
        assert set(result.keys()) == {"mean_pred_shift", "max_pred_shift", "fraction_flipped"}

    def test_different_model_positive_shift(self):
        """Different unlearned vs retrained models → positive shift."""
        data = _make_dummy_data()
        model_unlearned = _make_dummy_model()
        model_retrained = _make_dummy_model()
        retain_mask = torch.ones(100, dtype=torch.bool)
        result = evaluate_collateral_damage(
            model_unlearned=model_unlearned, model_retrained=model_retrained,
            data=data, retain_mask=retain_mask,
        )
        assert result["mean_pred_shift"] > 0.0


# ===========================================================================
# TestComputeGapStatistics
# ===========================================================================

class TestComputeGapStatistics:
    def test_all_positive_gaps(self):
        gaps = [0.05, 0.08, 0.06, 0.07, 0.09, 0.06, 0.08, 0.07, 0.10, 0.06]
        result = compute_gap_statistics(gaps)
        assert result["mean"] > 0
        assert result["reject_h0"] is True

    def test_zero_gaps(self):
        gaps = [0.0, 0.0, 0.0, 0.0, 0.0]
        result = compute_gap_statistics(gaps)
        assert result["mean"] == 0.0
        assert result["reject_h0"] is False

    def test_single_value(self):
        result = compute_gap_statistics([0.05])
        assert result["mean"] == 0.05
        assert result["std"] == 0.0
        assert result["p_value"] == 1.0
        assert result["reject_h0"] is False

    def test_return_keys(self):
        result = compute_gap_statistics([0.1, 0.2, 0.3])
        expected_keys = {"mean", "std", "ci_lower", "ci_upper", "p_value", "reject_h0"}
        assert set(result.keys()) == expected_keys
