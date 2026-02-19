"""
Evaluation module for adversarial attacks on GNN unlearning.

Implements the attribution framework from update.md:
- Drop_retrain = Perf_before - Perf_retrain  (inherent loss from deletion)
- Gap = Perf_retrain - Perf_unlearn           (extra loss from approximate unlearning)

All functions are pure (no dependency on config.py) and operate on
torch models + PyG Data objects.
"""

from typing import List

import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score, roc_auc_score
from scipy import stats


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _predict(model, data):
    """Forward pass returning logits. Handles both f(x) and f(x, edge_index) signatures."""
    # Move model to data's device (keep everything on CUDA if data is on CUDA)
    device = data.x.device
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        if hasattr(model, 'forward') and 'edge_index' in model.forward.__code__.co_varnames:
            logits = model(data.x, data.edge_index)
        else:
            logits = model(data.x)
    return logits


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def evaluate_f1_drop(model_before, model_after, data, test_mask):
    """
    Compute F1 (micro) before and after unlearning on test nodes.

    Returns:
        dict with keys: f1_before, f1_after, f1_drop, f1_drop_pct
    """
    y_true = data.y.cpu().numpy()
    mask = test_mask.cpu()

    logits_before = _predict(model_before, data).cpu().numpy()
    logits_after = _predict(model_after, data).cpu().numpy()

    pred_before = logits_before.argmax(axis=1)
    pred_after = logits_after.argmax(axis=1)

    f1_before = float(f1_score(y_true[mask], pred_before[mask], average="micro"))
    f1_after = float(f1_score(y_true[mask], pred_after[mask], average="micro"))

    f1_drop = f1_before - f1_after
    f1_drop_pct = (f1_drop / f1_before * 100) if f1_before > 0 else 0.0

    return {
        "f1_before": f1_before,
        "f1_after": f1_after,
        "f1_drop": f1_drop,
        "f1_drop_pct": f1_drop_pct,
    }


def evaluate_mia_auc(model, data, member_mask, non_member_mask):
    """
    Confidence-based Membership Inference Attack AUC.

    Uses max softmax probability as the attack signal.
    Returns 0.5 if either member or non-member set is empty.
    """
    if member_mask.sum().item() == 0 or non_member_mask.sum().item() == 0:
        return 0.5

    logits = _predict(model, data)
    probs = F.softmax(logits, dim=1)
    confidence = probs.max(dim=1).values.cpu().numpy()

    member_idx = member_mask.cpu().nonzero(as_tuple=False).squeeze(-1).numpy()
    non_member_idx = non_member_mask.cpu().nonzero(as_tuple=False).squeeze(-1).numpy()

    labels = [1] * len(member_idx) + [0] * len(non_member_idx)
    scores = list(confidence[member_idx]) + list(confidence[non_member_idx])

    return float(roc_auc_score(labels, scores))


def evaluate_retrain_gap(model_before, model_unlearned, model_retrained, data, test_mask):
    """
    Attribution framework: decompose total performance drop.

    - Drop_retrain = Perf_before - Perf_retrain  (inherent loss from deletion)
    - Gap = Perf_retrain - Perf_unlearn           (extra loss from approximate unlearning)
    - Total = Drop_retrain + Gap = Perf_before - Perf_unlearn

    Returns:
        dict with keys: perf_before, perf_retrain, perf_unlearn,
                        drop_retrain, gap, gap_pct
    """
    y_true = data.y.cpu().numpy()
    mask = test_mask.cpu()

    pred_before = _predict(model_before, data).cpu().numpy().argmax(axis=1)
    pred_retrained = _predict(model_retrained, data).cpu().numpy().argmax(axis=1)
    pred_unlearned = _predict(model_unlearned, data).cpu().numpy().argmax(axis=1)

    perf_before = float(f1_score(y_true[mask], pred_before[mask], average="micro"))
    perf_retrain = float(f1_score(y_true[mask], pred_retrained[mask], average="micro"))
    perf_unlearn = float(f1_score(y_true[mask], pred_unlearned[mask], average="micro"))

    drop_retrain = perf_before - perf_retrain
    gap = perf_retrain - perf_unlearn
    gap_pct = (gap / perf_retrain * 100) if perf_retrain > 0 else 0.0

    return {
        "perf_before": perf_before,
        "perf_retrain": perf_retrain,
        "perf_unlearn": perf_unlearn,
        "drop_retrain": drop_retrain,
        "gap": gap,
        "gap_pct": gap_pct,
    }


def evaluate_collateral_damage(model_unlearned, model_retrained, data, retain_mask):
    """
    Measure prediction disturbance on retained nodes (inspired by UtU's Δp).

    Compares model_unlearned vs model_retrained on the retain set.
    Both models share the same deletion set; the difference isolates
    the approximation error's collateral effect on retained nodes.

    Args:
        model_unlearned: Model after approximate unlearning.
        model_retrained: Model after exact retrain-from-scratch.
        data: PyG Data object.
        retain_mask: Boolean mask for retained nodes.

    Returns:
        dict with keys: mean_pred_shift, max_pred_shift, fraction_flipped
    """
    logits_retrained = _predict(model_retrained, data)
    logits_unlearned = _predict(model_unlearned, data)

    probs_retrained = F.softmax(logits_retrained, dim=1)
    probs_unlearned = F.softmax(logits_unlearned, dim=1)

    mask = retain_mask.cpu()

    # Prediction probability shift on retained nodes
    shift = (probs_unlearned - probs_retrained).abs().cpu()
    # Per-node shift = max across classes (L-inf per node)
    node_shift = shift[mask].max(dim=1).values

    # Fraction of retained nodes whose predicted class changed
    pred_retrained = logits_retrained.argmax(dim=1).cpu()
    pred_unlearned = logits_unlearned.argmax(dim=1).cpu()
    flipped = (pred_retrained[mask] != pred_unlearned[mask]).float()

    return {
        "mean_pred_shift": float(node_shift.mean().item()) if node_shift.numel() > 0 else 0.0,
        "max_pred_shift": float(node_shift.max().item()) if node_shift.numel() > 0 else 0.0,
        "fraction_flipped": float(flipped.mean().item()) if flipped.numel() > 0 else 0.0,
    }


def compute_gap_statistics(gaps):
    """
    Statistical analysis of Gap values across multiple seeds.

    Args:
        gaps: List of Gap values from repeated experiments.

    Returns:
        dict with keys: mean, std, ci_lower, ci_upper, p_value, reject_h0
    """
    if len(gaps) < 2:
        val = float(gaps[0])
        return {
            "mean": val,
            "std": 0.0,
            "ci_lower": val,
            "ci_upper": val,
            "p_value": 1.0,
            "reject_h0": False,
        }

    import math
    n = len(gaps)
    mean = float(sum(gaps) / n)
    std = float((sum((g - mean) ** 2 for g in gaps) / (n - 1)) ** 0.5)

    se = std / math.sqrt(n)
    ci_lower = mean - 1.96 * se
    ci_upper = mean + 1.96 * se

    t_stat, p_value = stats.ttest_1samp(gaps, 0)
    p_value = float(p_value)

    return {
        "mean": mean,
        "std": std,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": p_value,
        "reject_h0": p_value < 0.05,
    }
