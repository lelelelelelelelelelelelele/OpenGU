import numpy as np
import logging

from unlearning.unlearning_methods.GraphRevoker.lib_partition.partition import Partition
# from lib_utils import utils

from torch import nn, optim
import torch.nn.functional as F
import torch
from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import to_dense_adj
import torch_geometric.transforms as T
from tqdm import tqdm

class DistMatchLoss(nn.Module):
    def __init__(self, labels, n_classes, n_shards):
        super(DistMatchLoss, self).__init__()
        
        self.one_hot = F.embedding(input=labels, weight=torch.eye(n_classes).to(labels.device))
        self.target_dist = torch.sum(self.one_hot, dim=0)
        self.target_dist = self.target_dist / torch.sum(self.target_dist)
        self.target_dist = torch.repeat_interleave(self.target_dist.unsqueeze(0), n_shards, 0)

        self.one_hot = nn.Parameter(self.one_hot, requires_grad=False)
        self.target_dist = nn.Parameter(self.target_dist, requires_grad=False)
        self.kl_div = nn.KLDivLoss(reduction='sum')

    def forward(self, partition):
        shard_samples = partition.T @ self.one_hot
        shard_dists = shard_samples / torch.sum(shard_samples, dim=1, keepdim=True)

        return self.kl_div(torch.log(shard_dists), self.target_dist)

class LabelEntropyLoss(nn.Module):
    def __init__(self, labels, n_classes):
        super(LabelEntropyLoss, self).__init__()
        self.one_hot = F.embedding(input=labels, weight=torch.eye(n_classes).to(labels.device))
        self.one_hot = nn.Parameter(self.one_hot, requires_grad=False)

    def forward(self, partition):
        shard_samples = partition.T @ self.one_hot + 1e-5 # Avoid division by zero
        shard_dists = (shard_samples) / torch.sum(shard_samples, dim=1, keepdim=True)
        shard_entropy = torch.sum(torch.mean(-shard_dists * torch.log(shard_dists), dim=1))

        return shard_entropy

class Partitioner(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_shards):
        super(Partitioner, self).__init__()

        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(in_dim, hidden_dim))
        self.convs.append(SAGEConv(hidden_dim, hidden_dim))
        self.cls = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Dropout(0.0),
            nn.GELU(),
            nn.Linear(hidden_dim, num_shards),
        )
    
    def forward(self, x, edge_index):
        for i, layer in enumerate(self.convs):
            x = layer(x, edge_index)
            if i + 1 < len(self.convs):
                x = F.gelu(x)
        x = F.gelu(x)
        x = self.cls(x)
        x = F.softmax(x / 1, dim=1) # Cora & Citeseer
        return x

class PartitionGPA(Partition):
    def __init__(self, args, graph, dataset,logger,model_zoo):
        super(PartitionGPA, self).__init__(args, graph, dataset)
        self.logger = logger
        self.model_zoo = model_zoo
        import cupy as cp
        cp.cuda.Device(self.args['cuda']).use()
        self.load_embeddings()

    def load_embeddings(self):
        from unlearning.unlearning_methods.GraphRevoker.lib_partition.node_embedding import NodeEmbedding
        node_embedding = NodeEmbedding(self.args, self.logger,self.graph, self.dataset,self.model_zoo)

        self.node_to_embedding = node_embedding.encoder(256, 2)
    
    def partition(self):
        nodes = torch.nonzero(self.dataset.train_mask).flatten()
        embeddings = torch.as_tensor(np.array([self.node_to_embedding[int(n)] for n in nodes]))
        assignment, _ = partition_embeddings(self.dataset, embeddings, self.args, self.logger)
        return {shard: nodes[assignment.cpu() == shard].cpu().numpy()
                for shard in range(self.num_shards)}


def partition_embeddings(dataset, embeddings, parameters, logger):
    """Existing GPA objective and postprocessing over correctly relabelled train nodes."""
    from torch_geometric.utils import subgraph
    nodes = dataset.train_mask.nonzero().flatten()
    if len(nodes) < parameters['num_shards']:
        raise ValueError('fewer training nodes than GPA shards')
    edge_index, _ = subgraph(nodes, dataset.edge_index, relabel_nodes=True,
                            num_nodes=dataset.num_nodes)
    if edge_index.shape[1] == 0:
        raise ValueError('GPA partition requires nonempty training edges')
    x = embeddings.to(dataset.x.device)
    if len(x) != len(nodes):
        raise ValueError('GPA embeddings do not match ordered training nodes')
    y = dataset.y[nodes]
    n_classes = int(dataset.y.max()) + 1
    data = Data(x=x, edge_index=edge_index, y=y)
    data.n_id = torch.arange(data.num_nodes, device=x.device)
    loader = NeighborLoader(data, num_neighbors=[-1, -1], input_nodes=None,
        batch_size=parameters.get('gpa_batch_size', 512), shuffle=True)
    model = Partitioner(x.shape[1], parameters.get('gpa_hidden_channels', 256), parameters['num_shards']).to(x.device)
    optimizer = optim.AdamW(model.parameters(), lr=parameters.get('gpa_lr', 1e-3),
                           weight_decay=parameters.get('gpa_weight_decay', 1e-5))
    model.train()
    for epoch in range(parameters.get('gpa_epochs', 10)):
        for batch in loader:
            optimizer.zero_grad()
            adj = to_dense_adj(batch.edge_index, max_num_nodes=batch.num_nodes)[0]
            output = model(batch.x, batch.edge_index)
            cut = ncut_loss(output, adj)
            semantic = LabelEntropyLoss(y[batch.n_id], n_classes)(output)
            balance = eff_norm(output, adj, batch.edge_index.shape[1])
            loss = cut + semantic * 1e-3 + balance * .001
            if not torch.isfinite(loss):
                raise ValueError('GPA objective is nonfinite')
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), .5)
            optimizer.step()
        logger.info('GPA epoch %s', epoch)
    model.eval()
    with torch.no_grad():
        results = torch.argsort(model(data.x, data.edge_index), dim=1, descending=True)[:, :1].cpu().numpy()
    counts = [0] * parameters['num_shards']
    assignment = torch.empty(len(nodes), dtype=torch.long, device=x.device)
    for node in sorted(range(len(nodes)), key=lambda i: results[i][0]):
        label = int(results[node][0])
        if counts[label] >= len(nodes) / parameters['num_shards'] + len(nodes) * parameters['shard_size_delta']:
            label = int(np.argmin(counts))
        assignment[node] = label
        counts[label] += 1
    if min(counts) == 0:
        raise ValueError('GPA partition produced an empty shard')
    return assignment, model


def balance_loss(y, n):
    g = y.shape[1]
    return torch.sum((torch.sum(y, dim=0) - n / g) ** 2) / g

def ncut_loss(Y, A):
    D = torch.sum(A, dim=1)
    Gamma = torch.mm(Y.t(), D.unsqueeze(1).float())
    loss = torch.sum(torch.mm(torch.div(Y.float(), Gamma.t()), (1 - Y).t().float()) * A.float())
    #loss = torch.sum(torch.mm(Y.float(), (1 - Y).t().float()) * A.float())

    return loss

def eff_norm(Y, A, edge_cnt):
    shard_num_nodes = torch.sum(Y, dim=0)
    y = Y.unsqueeze(2) # (N, S, 1)
    shard_edges = torch.einsum('nsc,msc->snm', y, y) # For each shard, (N, 1) matmul (1, N)
    # filter invalid edges, then sum up
    shard_num_edges = torch.sum((A.unsqueeze(0) * shard_edges).view(y.shape[1], -1),  
                                 dim=1)

    return torch.sum(((shard_num_nodes / Y.shape[0]) * (shard_num_nodes / Y.shape[0]) * (shard_num_edges / edge_cnt)) ** (1/3))