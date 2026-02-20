"""
Quick script to get graph_fingerprint for each seed.
"""
import sys
sys.path.insert(0, ".")

import hashlib
import numpy as np

DATASET_NAME = "cora"
BASE_MODEL = "GCN"

def get_fingerprint(seed):
    from dataset.original_dataset import original_dataset
    import logging

    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("data")

    # Minimal args - what original_dataset needs
    args = {
        "dataset_name": DATASET_NAME,
        "base_model": BASE_MODEL,
        "is_transductive": True,
        "is_balanced": False,
        "train_ratio": 0.8,
        "val_ratio": 0.0,
        "test_ratio": 0.2,
        "seed": seed,
        "proportion_unlearned_nodes": 0.1,
        "downstream_task": "node",  # Required by process_data but we won't call it
    }

    dataset = original_dataset(args, logger)
    data, _ = dataset.load_data()

    # Get edge_index and train_mask (before process_data modifies them)
    edge_index = data.edge_index.detach().cpu().numpy().astype(np.int64, copy=False)

    # Get train_mask if available, otherwise use all nodes
    if hasattr(data, "train_mask") and data.train_mask is not None:
        train_mask = data.train_mask
        if train_mask.dim() > 1:
            train_mask = train_mask.squeeze(-1)
        candidates = train_mask.nonzero(as_tuple=False).squeeze(-1).cpu().numpy()
    else:
        candidates = np.arange(data.num_nodes, dtype=np.int64)

    digest = hashlib.sha256()
    digest.update(np.int64(data.num_nodes).tobytes())
    digest.update(edge_index.tobytes())
    digest.update(candidates.tobytes())
    return digest.hexdigest()[:32]

for seed in [42, 212, 722, 1337]:
    fp = get_fingerprint(seed)
    print(f"seed={seed}: {fp}")
