"""Erase Then Rectify, adapted from the MIT-licensed GULib benchmark.

Reference: idea-iitd/Unlearning_Benchmark, commit
9c95ac387b528967cc1c3aebbd20ce78bcf418c8, ETRTrainer.py and etr_utils.py.
See LICENSE.benchmark. Node task only; no optimizer steps or implicit retraining.
"""
import copy
import time

import numpy as np
import torch
from torch_geometric.data import Data
from torch_geometric.utils import k_hop_subgraph


def training_graph(data):
    """Benchmark ETR computes edit gradients on train-to-train edges."""
    graph = data.clone()
    keep = data.train_mask[data.edge_index[0]] & data.train_mask[data.edge_index[1]]
    graph.edge_index = data.edge_index[:, keep].clone()
    return graph


def influence_nodes(nodes, edges):
    edges = edges.detach().cpu().numpy()
    influenced = np.asarray(nodes, dtype=np.int64)
    for _ in range(2):
        influenced = np.unique(np.append(influenced, edges[1, np.isin(edges[0], influenced)]))
    return np.setdiff1d(influenced, nodes)


def seed_subgraph(nodes, graph):
    """Preserve benchmark's connected-seed population and exact PyG mapping.

    Empty seeds fail explicitly instead of substituting an unrelated node.
    Original global IDs remain attached for diagnostics and parity checks.
    """
    nodes = np.asarray(nodes, dtype=np.int64)
    edges = graph.edge_index.detach().cpu().numpy()
    connected = nodes[np.isin(nodes, edges)]
    if not len(connected):
        raise ValueError('ETR requires a nonempty connected seed population in each edit subgraph')
    seeds = torch.tensor(connected, dtype=torch.long, device=graph.x.device)
    subset, edge_index, mapping, _ = k_hop_subgraph(
        seeds, 2, graph.edge_index, relabel_nodes=True, num_nodes=graph.num_nodes)
    return Data(x=graph.x[subset], edge_index=edge_index, y=graph.y[subset],
                mapping=mapping, seed_nodes=seeds, global_nodes=subset)


def edit_subgraphs(data, nodes):
    from experiments.node_deletion import retained_graph
    # Validate the request against the original supervised population.
    retained_graph(data, nodes)
    train = training_graph(data)
    retained = retained_graph(train, nodes)
    influenced = influence_nodes(nodes, train.edge_index)
    return train, seed_subgraph(nodes, train), seed_subgraph(influenced, train), \
        seed_subgraph(influenced, retained), influenced


def gradient_information(model, graph, *, seed_loss):
    # Compare data gradients without independently sampled Dropout masks.
    # eval() preserves autograd; training of the original model is unaffected.
    model.eval()
    model.zero_grad(set_to_none=True)
    output = model(graph.x, graph.edge_index)
    indices = graph.mapping if seed_loss else graph.train_mask
    # reshape handles a single seed without turning the target into a scalar.
    loss = torch.nn.functional.cross_entropy(
        output[indices], graph.y[indices].reshape(-1).long(), label_smoothing=0.1)
    loss.backward()
    gradients = {name: torch.zeros_like(p) if p.grad is None else p.grad.detach().clone()
                 for name, p in model.named_parameters()}
    if not all(torch.isfinite(g).all() for g in gradients.values()):
        raise ValueError('ETR produced non-finite edit gradients')
    # Promote before the first square: nonzero float32 gradients may square to zero.
    return gradients, {name: grad.to(torch.float64).pow(2) for name, grad in gradients.items()}


def erase(model, all_importance, forgotten_importance, influenced_importance, ratio):
    with torch.no_grad():
        for name, parameter in model.named_parameters():
            # Keep every Erase intermediate wide, including products before division.
            original = all_importance[name].to(torch.float64)
            forgotten = forgotten_importance[name].to(torch.float64)
            influenced = influenced_importance[name].to(torch.float64)
            if not all(torch.isfinite(value).all() and (value >= 0).all()
                       for value in (original, forgotten, influenced)):
                raise ValueError('ETR importance must be finite and nonnegative: ' + name)
            b1 = torch.min(torch.nan_to_num(original / forgotten, nan=1.0), torch.ones_like(original))
            b2 = torch.min(torch.nan_to_num(original.pow(2) / (forgotten * influenced), nan=1.0),
                           torch.ones_like(original))
            q1, q2 = torch.quantile(b1, ratio), torch.quantile(b2, ratio)
            if not torch.isfinite(q1) or not torch.isfinite(q2):
                raise ValueError('ETR erase quantile is non-finite: ' + name)
            if q1 <= 0 or q2 <= 0:
                raise ValueError('ETR erase quantile is zero; parameter edit is undefined: ' + name)
            loc1 = b1 <= q1
            loc2 = b2 <= q2
            loc2[loc1] = False
            parameter[loc1] = parameter[loc1].mul(b1[loc1] / q1).to(parameter.dtype)
            parameter[loc2] = parameter[loc2].mul(b2[loc2] / q2).to(parameter.dtype)


def rectify(model, grad_all, grad_forget, grad_influenced, grad_after,
            coefficient, num_forget, num_influenced, num_train):
    remaining = num_train - num_forget
    with torch.no_grad():
        for name, parameter in model.named_parameters():
            parameter.sub_(coefficient * (
                grad_all[name] * num_train / remaining - grad_forget[name] * num_forget / remaining
                - grad_influenced[name] * num_influenced / remaining
                + grad_after[name] * num_influenced / remaining))


def run_etr(model, data, nodes, *, erase_ratio, coefficient, trace=None):
    """Edit a copy; optional trace exposes actual stage states to verification."""
    started = time.perf_counter()
    train, forgotten, influenced, after, influence = edit_subgraphs(data, nodes)
    edited = copy.deepcopy(model)
    g_all, i_all = gradient_information(edited, train, seed_loss=False)
    g_f, i_f = gradient_information(edited, forgotten, seed_loss=True)
    g_k, i_k = gradient_information(edited, influenced, seed_loss=True)
    erase(edited, i_all, i_f, i_k, erase_ratio)
    if trace is not None:
        trace('erase', edited)
    g_u, _ = gradient_information(edited, after, seed_loss=True)
    rectify(edited, g_all, g_f, g_k, g_u, coefficient,
            len(nodes), len(influence), int(train.train_mask.sum()))
    if not all(torch.isfinite(p).all() for p in edited.parameters()):
        raise ValueError('ETR produced non-finite edited parameters')
    if trace is not None:
        trace('rectify', edited)
    edited.eval()
    return edited, time.perf_counter() - started
