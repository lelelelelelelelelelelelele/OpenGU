from __future__ import annotations

import torch

from model.base_gnn.gcn import GCNNet
from model.base_gnn.deletion import GCNDelete


def _args(num_layers: int = 3, hidden: int = 16) -> dict:
    return {
        "dataset_name": "ogbn-arxiv",
        "downstream_task": "node",
        "base_model": "GCN",
        "gcn_num_layers": num_layers,
        "gcn_hidden": hidden,
        "hidden_dim": hidden,
        "out_dim": 5,
    }


def test_gcn_delete_matches_configured_gcn_depth_for_arxiv():
    args = _args(num_layers=3, hidden=16)

    original = GCNNet(args, in_channels=8, out_channels=args["out_dim"])
    delete_model = GCNDelete(
        args,
        in_channels=8,
        out_channels=args["out_dim"],
        mask_1hop=torch.zeros(10, dtype=torch.bool),
        mask_2hop=torch.zeros(10, dtype=torch.bool),
        num_nodes=10,
    )

    assert len(original.convs) == 3
    assert len(delete_model.convs) == 3

    incompatible = delete_model.load_state_dict(original.state_dict(), strict=False)
    assert all(key.startswith("deletion") for key in incompatible.missing_keys)
    assert incompatible.unexpected_keys == []
