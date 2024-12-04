import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv
from model.base_gnn.abstract_model import abstract_model,RandomizedClassifier
from parameter_parser import parameter_parser

class SAGENet(abstract_model):
    def __init__(self,args,in_channels, out_channels, num_layers=2):
        super(SAGENet,self).__init__()
        self.args = args
        self.config = self.load_config()
        self.num_layers = num_layers
        self.convs = torch.nn.ModuleList()
        hidden_channels = 64
        if self.args["unlearning_methods"] == "GraphRevoker":
            self.convs.append(SAGEConv(in_channels, hidden_channels))
            for _ in range(num_layers - 2):
                self.convs.append(SAGEConv(hidden_channels, hidden_channels, cached=False))
            self.convs.append(SAGEConv(hidden_channels, hidden_channels))
            self.cls = RandomizedClassifier(hidden_channels, out_channels)
        else:
            self.convs.append(SAGEConv(in_channels, hidden_channels))
            self.convs.append(SAGEConv(hidden_channels, out_channels))

    def forward(self, x, edge_index,return_all_emb=False,adjs=None,edge_weight=None,return_feature=False):
        if self.args["unlearning_methods"] == "GraphRevoker":
            feat = self.convs[-1](x, edge_index)
            x = self.cls(feat)
            if return_feature:
                return x, feat
            return x
        elif adjs is None:
            x_list = []
            for i in range(self.num_layers - 1):
                x_list.append(self.convs[i](x, edge_index))
                x = F.relu(self.convs[i](x, edge_index))
                x = F.dropout(x, p=0.5, training=self.training)

            x_list.append(self.convs[-1](x, edge_index))
            x = self.convs[-1](x, edge_index)

            if return_all_emb:
                return x_list
            #F.log_softmax(x, dim=-1)
            return x
        else:
            for i, (edge_index_, e_id, size) in enumerate(adjs):
                x_target = x[:size[1]]  # Target nodes are always placed first.
                x = self.convs[i]((x, x_target), edge_index_)

                if i != self.num_layers - 1:
                    x = F.relu(x)
                    x = F.dropout(x, p=0.5, training=self.training)

            return F.log_softmax(x, dim=1)
        
    def get_softlabel(self,x,edge_index=None):
        for i in range(self.num_layers - 1):
            x = F.relu(self.convs[i](x, edge_index))
            x = F.dropout(x, p=0.5, training=self.training)

        x = self.convs[-1](x, edge_index)

        return F.softmax(x, dim=1)

    def emb2softlable(self,x,edge_index=None):
        x = self.convs[1](x,edge_index)

        return F.softmax(x,dim=1)


    def get_embedding(self,x,edge_index=None):
        emb = self.convs[0](x,edge_index)
        emb = F.relu(emb)
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

    #lack of code in GIF
    # def forward_once(self, data):
    #     x = F.dropout(data.x, p=0.5, training=self.training)
    #     x = F.relu(self.convs[0](x, data.edge_index))
    #     x = F.dropout(x, p=0.5, training=self.training)
    #     x = self.convs[1](x, data.edge_index)

    #     return F.log_softmax(x, dim=1)

    # def forward_once_unlearn(self, data):
    #     x = F.dropout(data.x_unlearn, p=0.5, training=self.training)
    #     x = F.relu(self.convs[0](x, data.edge_index_unlearn))
    #     x = F.dropout(x, p=0.5, training=self.training)
    #     x = self.convs[1](x, data.edge_index_unlearn)

    #     return F.log_softmax(x, dim=1)
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