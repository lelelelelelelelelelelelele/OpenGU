"""Single-model measurements computed entirely from persisted predictions."""
from __future__ import annotations

import numpy as np
import torch


def method_metrics(payload):
    """Fixed single-label test protocol shared by every method, including Retrain."""
    from sklearn.metrics import roc_auc_score
    a = payload.arrays
    mask = a['test_mask']
    logits = torch.tensor(a['logits'][mask], dtype=torch.float64)
    labels = np.asarray(a['y'][mask], dtype=np.int64)
    probabilities = torch.softmax(logits, dim=1).numpy()
    accuracy = float(np.mean(probabilities.argmax(axis=1) == labels))
    auc = None
    classes = logits.shape[1]
    auc_status = 'missing_test_classes'
    if classes > 1 and np.array_equal(np.unique(labels), np.arange(classes)):
        auc = float(roc_auc_score(labels, probabilities[:, 1]) if classes == 2 else
                    roc_auc_score(labels, probabilities, multi_class='ovr', average='macro',
                                  labels=np.arange(classes)))
        auc_status = 'computed'
    return {'f1': accuracy, 'accuracy': accuracy,
            'cross_entropy': float(torch.nn.functional.cross_entropy(logits, torch.tensor(labels))),
            'classification_auc': auc,
            'classification_auc_status': auc_status}


def update_detection(payload):
    """Existing posterior-change detection protocol; not a generic MIA score."""
    from sklearn.metrics import roc_auc_score
    a = payload.arrays
    if 'logits_before' not in a:
        return {'update_detection_auc': None, 'update_detection_auc_status': 'missing_original_predictions'}
    members = a['selected_nodes']
    nonmembers = np.flatnonzero(a['test_mask'])
    n = min(len(members), len(nonmembers))
    if n < 2:
        return {'update_detection_auc': None, 'update_detection_auc_status': 'insufficient_samples'}
    rows = np.concatenate((members[:n], nonmembers[:n]))
    before = torch.softmax(torch.tensor(a['logits_before']), dim=1).numpy()
    after = torch.softmax(torch.tensor(a['logits']), dim=1).numpy()
    change = np.linalg.norm(before[rows] - after[rows], axis=1)
    return {'update_detection_auc': float(roc_auc_score(np.r_[np.ones(n), np.zeros(n)], change)),
            'update_detection_auc_status': 'computed'}


def evaluate_method(reference, payload):
    """A rebuildable metrics receipt, separate from model computation identity."""
    from cache_v2 import canonical_sha256
    from experiments.implementation_identity import implementation_fingerprint
    import sklearn
    identity = {'output': reference, 'protocol': 'single-label-test-micro-f1-ovr-macro-auc-v1',
                'metric_libraries': {'sklearn': sklearn.__version__, 'torch': torch.__version__, 'numpy': np.__version__},
                'implementation': implementation_fingerprint(method_metrics, update_detection)}
    return {'evaluation_receipt_id': 'evalr_' + canonical_sha256(identity)[:32],
            'identity': identity, 'metrics': {**method_metrics(payload), **update_detection(payload)}}
