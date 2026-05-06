from __future__ import annotations

import torch

from model.base_gnn.gcn import GCNNet
from model.base_gnn.deletion import GCNDelete


def _args(num_layers: int = 3, hidden: int = 16, hidden_dim: int | None = None) -> dict:
    if hidden_dim is None:
        hidden_dim = hidden
    return {
        "dataset_name": "ogbn-arxiv",
        "downstream_task": "node",
        "base_model": "GCN",
        "gcn_num_layers": num_layers,
        "gcn_hidden": hidden,
        "hidden_dim": hidden_dim,
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


def test_gcn_delete_uses_gcn_hidden_for_first_deletion_layer():
    args = _args(num_layers=3, hidden=256, hidden_dim=64)
    delete_model = GCNDelete(
        args,
        in_channels=8,
        out_channels=args["out_dim"],
        mask_1hop=torch.zeros(10, dtype=torch.bool),
        mask_2hop=torch.zeros(10, dtype=torch.bool),
        num_nodes=10,
    )

    assert delete_model.convs[0].out_channels == 256
    assert delete_model.deletion1.deletion_weight.shape == (256, 256)

    edge_index = torch.tensor(
        [[0, 1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9]],
        dtype=torch.long,
    )
    out = delete_model(torch.randn(10, 8), edge_index)
    assert out.shape == (10, args["out_dim"])
