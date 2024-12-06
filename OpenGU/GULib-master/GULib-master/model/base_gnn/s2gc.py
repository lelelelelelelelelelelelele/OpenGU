import torch
import yaml
from torch_geometric.nn import SGConv
from typing import Union
import torch.nn.functional as F

from model.base_gnn.Convs import S2GConv
from model.base_gnn.abstract_model import abstract_model,RandomizedClassifier
from torch_geometric.typing import Adj, OptTensor, OptPairTensor
from torch import Tensor
from config import root_path
from parameter_parser import parameter_parser

class S2GCNet(abstract_model):
    def __init__(self, args,in_channels, out_channels, num_layers=3):
        super(S2GCNet, self).__init__()
        self.args = args
        self.config = self.load_config()
        self.num_layers = num_layers
        self.convs = torch.nn.ModuleList()
        hidden_channels = 64
        if self.args["unlearning_methods"] == "SGU" or self.args["unlearning_methods"] =="GNNDelete":
            # self.convs.append(SGConv(in_channels, 64, K=3, bias=False))
            self.convs.append(torch.nn.Linear(in_channels, 64, bias=False))
            self.convs.append(torch.nn.Linear(64,out_channels,bias=False))
        elif self.args["unlearning_methods"] == "GraphRevoker":
            self.convs.append(S2GConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(S2GConv(hidden_channels, hidden_channels, cached=False))
            self.convs.append(S2GConv(hidden_channels, hidden_channels))
            self.cls = RandomizedClassifier(hidden_channels, out_channels)
        else:
            self.convs.append(S2GConv(in_channels, hidden_channels, K=self.num_layers, bias=False))
            self.convs.append(torch.nn.Linear(hidden_channels, out_channels, bias=False))

    def forward(self, x, edge_index = None,adjs=None,edge_weight=None,return_feature=False):
        if self.args["unlearning_methods"] == "GraphRevoker":
            x = self.convs[0](x,edge_index)
            feat = self.convs[-1](x, edge_index)
            x = self.cls(feat)
            if return_feature:
                return x, feat
            return x
        elif edge_index is None:
                x = self.convs[0](x)
                x = self.convs[1](x)
        else:
            x = self.convs[0](x,edge_index)
            x = self.convs[1](x)

        return x

    def get_softlabel(self,x):
        x = self.convs[0](x)
        x = self.convs[1](x)

        return F.softmax(x,dim=1)
    def emb2softlable(self,x):
        x = self.convs[1](x)

        return F.softmax(x,dim=1)


    def get_embedding(self,x):
        emb = self.convs[0](x)
        return emb

    def reset_parameters(self):
        for i in range(2):
            self.convs[i].reset_parameters()

    def inference(self, x_all, subgraph_loader, device):
        # Compute representations of nodes layer by layer, using *all*
        # available edges. This leads to faster computation in contrast to
        # immediately computing the final representations of each batch.
        for i in range(self.num_layers):
            xs = []

            for batch_size, n_id, adj in subgraph_loader:
                edge_index, _, size = adj.to(device)
                x = x_all[n_id].to(device)
                x_target = x[:size[1]]
                x = self.convs[i]((x, x_target), edge_index)
                if i != self.num_layers - 1:
                    x = F.relu(x)
                xs.append(x.cpu())

            x_all = torch.cat(xs, dim=0)

        return x_all



    def GIF_inference(self, x_all, subgraph_loader, edge_weight, device):
        for i in range(self.num_layers):
            xs = []

            for batch_size, n_id, adj in subgraph_loader:
                edge_index, e_id, size = adj.to(device)
                x = x_all[n_id].to(device)
                x_target = x[:size[1]]
                x = self.convs_batch[i]((x, x_target), edge_index, edge_weight=edge_weight[e_id])

                xs.append(x.cpu())

            x_all = torch.cat(xs, dim=0)

        return x_all
    
    # def forward_once(self, data, edge_weight):
    #     x, edge_index = data.x, data.edge_index
    #     x = self.convs_batch[0](x, edge_index, edge_weight)
    #     x = F.dropout(x, p=0.5, training=self.training)
    #     x = self.convs_batch[1](x, edge_index, edge_weight)

    #     return F.log_softmax(x, dim=-1)

    # def forward_once_unlearn(self, data, edge_weight):
    #     x, edge_index = data.x_unlearn, data.edge_index_unlearn
    #     x = self.convs_batch[0](x, edge_index, edge_weight)
    #     x = F.dropout(x, p=0.5, training=self.training)
    #     x = self.convs_batch[1](x, edge_index, edge_weight)

    #     return F.log_softmax(x, dim=-1)
    
    def reason_once(self,data):
        x, edge_index = data.x, data.edge_index
        x = self.convs[0](x,edge_index)
        x = self.convs[1](x)

        return  x
    
    def reason_once_unlearn(self,data):
        x, edge_index = data.x_unlearn, data.edge_index_unlearn
        x = self.convs[0](x,edge_index)
        x = self.convs[1](x)

        return  x
    
    
# class S2GConvBatch(S2GConv):
#     def __init__(self, in_channels: int, out_channels: int, K: int = 1,
#                  cached: bool = False, add_self_loops: bool = True, 
#                  bias: bool = True, **kwargs):
#         super(S2GConvBatch, self).__init__(in_channels, out_channels,
#                                           cached=cached, add_self_loops=add_self_loops,
#                                           bias=bias)

#     def forward(self, x: Union[Tensor, OptPairTensor], edge_index: Adj,
#                 edge_weight: OptTensor = None) -> Tensor:

#         out = self.propagate(edge_index, x=x, edge_weight=edge_weight, size=None)
#         out = self.lin(out)

#         return out