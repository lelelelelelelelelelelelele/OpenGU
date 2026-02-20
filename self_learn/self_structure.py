import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
# from torch_geometric.nn import GCNConv, GATConv
import numpy as np
from matplotlib import pyplot as plt
from torch_geometric.nn.conv import MessagePassing

import torch.nn as nn
from torch_scatter import scatter_softmax
# 1. 超参数
# seed = 42
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# torch.manual_seed(seed)
# np.random.seed(seed)

# # 2. 载入 Cora
# dataset = Planetoid(root='./data', name='Cora')
# data = dataset[0].to(device)

# ------------------
# original norm func:
# node = data.num_nodes
# norm = torch.zeros(node)
# for row1,col1 in zip(row,col):
#     norm[row1] += 1
#     norm[col1] += 1
# norm = norm//2
# A = torch.zeros((node, node), device=device)
# for row1,col1 in zip(row,col):
#     A[row1][col1] = 1 / (norm[row1] * norm[col1]) ** 0.5
# return A (duplicate)
def add_self_loop(edge, node):
    loop = torch.arange(node, device=edge.device)
    return torch.stack([torch.cat([edge[0], loop]), torch.cat([edge[1], loop])])

def norm(node, edge_index, device="cuda"):
    row, col = edge_index
    d = torch.zeros(node, device=device)
    d.scatter_add_(0, torch.cat([row, col]),torch.full((row.size(0)*2,), 0.5, device=device, dtype=d.dtype))
    # d.scatter_add_(0, col, torch.ones_like(col, device=device)//2)
    # print(d)
    d+=1
    w = 1/(d[row]*d[col])**0.5
    A = torch.zeros((node, node), device=device)
    A[row, col] = w
    A = A + torch.eye(node, device=device)/d  # 加上单位矩阵
    return A
# is_sym = torch.allclose(A, A.T)
# print("is_symmetric:", is_sym)
class GCNconv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Linear(in_channels, out_channels)

    def forward(self, x, edge_matrix, edge_index):
        # role: fuse the adjacency matrix and node features
        re = edge_matrix @ x # x=point embedding (n*f_in)
        return self.conv(re)

# advanced: use propagate and message to calculate weight on edge size instead of on graph size (n*n -> E)
class self_GCN(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super().__init__()
        self.conv1 = GCNconv(in_channels, hidden_channels)
        self.conv2 = GCNconv(hidden_channels, out_channels)
        self.dropout_ratio = 0.4

    def forward(self, x, edge_matrix, edge_index):
        x = self.conv1(x, edge_matrix, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout_ratio, training=self.training)
        x = self.conv2(x, edge_matrix, edge_index)
        return x
    
class GATconv(MessagePassing):
    def __init__(self, input_dim, output_dim, k_head):
        super().__init__()
        self.linear = nn.Linear(input_dim, k_head * output_dim)
        self.k_head = k_head
        self.att = nn.Parameter(torch.zeros(size=(1, k_head, output_dim * 2)))
    def forward(self, x, edge_index):
        re = self.linear(x)
        edge_index = add_self_loop(edge_index, x.size(0))
        # row, col = edge_index
        # x_i = re[row]  # (E, k_head * fout)
        # x_j = re[col]
        # re = re.view(-1, self.k_head, re.size(-1) // self.k_head)
        # print("re.shape after view:", re.shape)
        return self.propagate(edge_index = edge_index, size=(x.size(0), x.size(0)), x= re)
    def message(self, x_i, x_j, edge_index): # （E, k_head, fout）
        x_i = x_i.view(-1, self.k_head, x_i.size(-1) // self.k_head)
        x_j = x_j.view(-1, self.k_head, x_j.size(-1) // self.k_head)
        a = torch.cat([x_i, x_j], dim=-1) #(E, k, 2*fout) ``
        a = (a * self.att).sum(-1) #(E, k_head)
        a = F.leaky_relu(a, negative_slope=0.2)  # (E, k_head)
        # print("a:", a.shape)
        # print("edge:", edge_index.shape)
        # a = F.softmax(a, dim = row)
        a = scatter_softmax(a, index=edge_index[0], dim=0)
        a = F.dropout(a, p=0.5, training=self.training)  # 再 dropout

        out = F.elu(x_j * a.unsqueeze(-1))  # (E, k_head, fout) a:(E, k_head)
        return out.view(out.size(0), -1)

class self_GAT(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, k_head):
        super().__init__()
        self.k_head = k_head
        self.conv1 = GATconv(input_dim, hidden_dim, k_head)
        self.conv2 = GATconv(k_head*hidden_dim, output_dim, 1)
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        # x(n, k_head, hidden_dim)
        # concat
        x = x.view(x.size(0), -1)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        return x.squeeze(1)