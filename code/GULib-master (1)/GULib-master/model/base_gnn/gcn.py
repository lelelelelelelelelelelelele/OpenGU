import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from model.base_gnn.abstract_model import abstract_model,RandomizedClassifier
from torch_geometric.typing import Adj, OptTensor, OptPairTensor
from torch import Tensor
import yaml
from typing import Union
from config import root_path
from parameter_parser import parameter_parser

class GCNNet(abstract_model):
    def __init__(self,args,in_channels, out_channels, num_layers=2):
        super(GCNNet,self).__init__()
        self.args = args
        self.config = self.load_config()
        self.num_layers = num_layers
        hidden_channels = 64
        self.convs = torch.nn.ModuleList()

        if self.args["unlearning_methods"] == "SGU":
            self.convs.append(GCNConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(GCNConv(hidden_channels, hidden_channels, cached=False))
            self.convs.append(GCNConv(hidden_channels, out_channels))
        elif self.args["unlearning_methods"] == "GraphRevoker":
            self.convs.append(GCNConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(GCNConv(hidden_channels, hidden_channels, cached=False))
            self.convs.append(GCNConv(hidden_channels, hidden_channels))
            self.cls = RandomizedClassifier(hidden_channels, out_channels)
        else :
            self.convs.append(GCNConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(GCNConv(hidden_channels, hidden_channels, cached=False))
            self.convs.append(GCNConv(hidden_channels, out_channels))


    def forward(self, x, edge_index,return_all_emb=False,adjs=None,edge_weight=None,return_feature=False): 
        x_list = []
        for i in range(self.num_layers - 1):
            x_list.append(self.convs[i](x, edge_index))
            x = F.relu(self.convs[i](x, edge_index))
            x = F.dropout(x, training=self.training)
        x_list.append(self.convs[-1](x, edge_index))

        if self.args["unlearning_methods"] == "GraphRevoker":
            feat = self.convs[-1](x, edge_index)
            x = self.cls(feat)
            if return_feature:
                return x, feat
            return x
        else:
            x = self.convs[-1](x, edge_index)
            if return_all_emb:
                return x_list
        
            return x

    def get_softlabel(self,x,edge_index=None):
        for i in range(self.num_layers - 1):
            x = F.relu(self.convs[i](x, edge_index))
            x = F.dropout(x)

        x = self.convs[-1](x, edge_index)

        return F.softmax(x, dim=1)

    def emb2softlable(self,x,edge_index=None):
        x = self.convs[-1](x,edge_index)

        return F.softmax(x,dim=1)


    def get_embedding(self,x,edge_index=None):
        emb = F.relu(self.convs[0](x, edge_index))
        return emb




    def reset_parameters(self):
        for i in range(self.num_layers):
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



    def reason(self,x,edge_index):
        for i in range(self.num_layers):
            xs = []
            x = self.convs[i](x,edge_index)
            if i != self.num_layers - 1:
                x = F.relu(x)
            xs.append(x.cpu())
        x_all = torch.cat(xs, dim=0)
        return x_all
            

    #GNNDelete
    def decode(self, z, pos_edge_index, neg_edge_index=None):
        if neg_edge_index is not None:
            edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
            # Z1 = z[edge_index[0]]
            # Z2 = z[edge_index[1]]
            # SUM = Z1*Z2
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        else:
            edge_index = pos_edge_index
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        return logits
    
    def reason_once(self,data):
        x, edge_index = data.x, data.edge_index
        for i in range(self.num_layers):
            x = self.convs[i](x,edge_index)
            if i != self.num_layers - 1:
                x = F.relu(x)
                x = F.dropout(x, training=self.training)

        return  x
    
    def reason_once_unlearn(self,data):
        x, edge_index = data.x_unlearn, data.edge_index_unlearn
        for i in range(self.num_layers):
            x = self.convs[i](x,edge_index)
            if i != self.num_layers - 1:
                x = F.relu(x)
                x = F.dropout(x, training=self.training)

        return  x


    def forward_once(self, data, edge_weight):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.convs[0](x, edge_index, edge_weight))
        x = F.dropout(x, training=self.training)
        x = self.convs[1](x, edge_index, edge_weight)

        return F.log_softmax(x, dim=-1)

    def forward_once_unlearn(self, data, edge_weight):
        x, edge_index = data.x_unlearn, data.edge_index_unlearn
        x = F.relu(self.convs[0](x, edge_index, edge_weight))
        x = F.dropout(x, training=self.training)
        x = self.convs[1](x, edge_index, edge_weight)

        return F.log_softmax(x, dim=-1)
    #GIF
    # def forward_once(self, data, edge_weight):
    #     x, edge_index = data.x, data.edge_index
    #     x = F.relu(self.convs_batch[0](x, edge_index, edge_weight))
    #     x = F.dropout(x, training=self.training)
    #     x = self.convs_batch[1](x, edge_index, edge_weight)

    #     return F.log_softmax(x, dim=-1)
    


    # def forward_once_unlearn(self, data, edge_weight):
    #     x, edge_index = data.x_unlearn, data.edge_index_unlearn
    #     x = F.relu(self.convs_batch[0](x, edge_index, edge_weight))
    #     x = F.dropout(x, training=self.training)
    #     x = self.convs_batch[1](x, edge_index, edge_weight)

    #     return F.log_softmax(x, dim=-1)

    # def GIF_inference(self, x_all, subgraph_loader, edge_weight, device):
    #     for i in range(self.num_layers):
    #         xs = []

    #         for batch_size, n_id, adj in subgraph_loader:
    #             edge_index, e_id, size = adj.to(device)
    #             x = x_all[n_id].to(device)
    #             x_target = x[:size[1]]
    #             x = self.convs_batch[i]((x, x_target), edge_index, edge_weight=edge_weight[e_id])

    #             if i != self.num_layers - 1:
    #                 x = F.relu(x)
    #             xs.append(x.cpu())

    #         x_all = torch.cat(xs, dim=0)

    #     return x_all
    


    # def load_config(self):
    #     f = open(root_path + '/model/properties/gcn' +'.yaml','r')
    #     config_str = f.read()
    #     config = yaml.load(config_str,Loader=yaml.FullLoader)
    #     self.lr = config['lr']
    #     self.decay = config['decay']
    #     return config

# class GCNConvBatch(GCNConv):
#     def __init__(self, in_channels: int, out_channels: int,
#                  improved: bool = False, cached: bool = False,
#                  add_self_loops: bool = True, bias: bool = True,
#                  **kwargs):
#         super(GCNConvBatch, self).__init__(in_channels, out_channels,
#                                            improved=improved, cached=cached, add_self_loops=add_self_loops,
#                                            bias=bias)

#     def forward(self, x: Union[Tensor, OptPairTensor], edge_index: Adj,
#                 edge_weight: OptTensor = None) -> Tensor:

#         out = self.propagate(edge_index, x=x, edge_weight=edge_weight, size=None)
#         #out = torch.matmul(out, self.weight)
#         out = self.lin(out)

#         return out

