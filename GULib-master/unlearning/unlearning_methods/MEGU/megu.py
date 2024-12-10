import torch
import torch.nn as nn
import numpy as np
import time
import torch.nn.functional as F
from tqdm import tqdm
from torch_geometric.nn import CorrectAndSmooth
from task.node_classification import NodeClassifier
from torch_geometric.utils import k_hop_subgraph, to_scipy_sparse_matrix
from utils.utils import sparse_mx_to_torch_sparse_tensor,normalize_adj,propagate,criterionKD,calc_f1
from config import BLUE_COLOR,RESET_COLOR
from config import unlearning_path
from sklearn.metrics import roc_auc_score
from task import get_trainer
from torch_geometric.transforms import SIGN

class GATE(torch.nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.lr = torch.nn.Linear(dim, dim)

    def forward(self, x):
        t = x.clone()
        return self.lr(t)



class megu:
    def __init__(self,args,logger,model_zoo):
        self.args = args
        self.logger = logger
        self.model_zoo = model_zoo
        self.data = self.model_zoo.data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_feats = self.data.num_features
        self.num_layers = self.args["GNN_layer"]
        self.args["unlearn_trainer"] = 'MEGUTrainer'
        num_runs = self.args["num_runs"]
        self.run = 0
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_unlearning_time = np.zeros(num_runs)
        self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)

    def run_exp(self):
        self.train_indices,self.test_indices = self.data.train_indices,self.data.test_indices
        self.train_mask,self.test_mask= self.data.train_mask,self.data.test_mask
        self.unlearning_request()
        self.adj = sparse_mx_to_torch_sparse_tensor(normalize_adj(to_scipy_sparse_matrix(self.data.edge_index)))
        self.neighbor_khop = self.neighbor_select(self.data.x)
        for self.run in range(self.args["num_runs"]):
            run_training_time, _ = self._train_model(self.run)
            mem_labels_o,non_labels_o = self.get_softlabels()
            self.avg_unlearning_time[self.run], self.average_f1[self.run] = self.megu_training()
            mem_labels,non_labels = self.get_softlabels()
            self.average_auc[self.run] = self.mia_attack(mem_labels_o,non_labels_o,mem_labels,non_labels)
        
        self.logger.info(
        "{}Performance Metrics:\n"
        " - Average F1 Score: {:.4f} ± {:.4f}\n"
        " - Average AUC Score: {:.4f} ± {:.4f}\n"
        " - Average Unlearning Time: {:.4f} ± {:.4f} seconds\n".format(
            BLUE_COLOR,
            np.mean(self.average_f1), np.std(self.average_f1),
            np.mean(self.average_auc), np.std(self.average_auc),
            np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
            RESET_COLOR
            )
        )

    def get_softlabels(self):
        if self.args["base_model"] == "SIGN":
            out = self.target_model.model(self.data.xs)
        else:
            out = self.target_model.model(self.data.x,self.data.edge_index)
        mem_labels = F.softmax(out,dim = 1)[self.unlearing_nodes]
        non_labels = F.softmax(out,dim = 1)[self.data.test_indices[:self.args["num_unlearned_nodes"]]]
        return mem_labels,non_labels

    def _train_model(self, run):
        # self.logger.info('training target models, run %s' % run)

        start_time = time.time()
        self.target_model.data = self.data
        res = self.target_model.train()
        train_time = time.time() - start_time

        # self.data_store.save_target_model(run, self.target_model)
        # self.logger.info(f"Model training time: {train_time:.4f}")

        return train_time, res
        
    def unlearning_request(self):
        # self.logger.debug("Train data  #.Nodes: %f, #.Edges: %f" % (
        #     self.data.num_nodes, self.data.num_edges))

        self.data.x_unlearn = self.data.x.clone()
        self.data.edge_index_unlearn = self.data.edge_index.clone()
        edge_index = self.data.edge_index.numpy()
        unique_indices = np.where(edge_index[0] < edge_index[1])[0]

        if self.args["unlearn_task"] == 'node':
            # unique_nodes = np.random.choice(len(self.train_indices),
            #                                 int(len(self.train_indices) * self.args['unlearn_ratio']),
            #                                 replace=False)
            path_un = unlearning_path + "_" + str(self.run) + ".txt"
            unique_nodes = np.loadtxt(path_un, dtype=int)
            self.unlearing_nodes = unique_nodes
            self.data.edge_index_unlearn = self.update_edge_index_unlearn(unique_nodes)

        if self.args["unlearn_task"] == 'edge':
            remove_indices = np.random.choice(
                unique_indices,
                int(unique_indices.shape[0] * self.args['unlearn_ratio']),
                replace=False)
            remove_edges = edge_index[:, remove_indices]
            unique_nodes = np.unique(remove_edges)

            self.data.edge_index_unlearn = self.update_edge_index_unlearn(unique_nodes, remove_indices)

        if self.args["unlearn_task"] == 'feature':
            unique_nodes = np.random.choice(len(self.train_indices),
                                            int(len(self.train_indices) * self.args['unlearn_ratio']),
                                            replace=False)
            self.data.x_unlearn[unique_nodes] = 0.

        self.temp_node = unique_nodes





    def neighbor_select(self, features):
        temp_features = features.clone()
        pfeatures = propagate(temp_features, self.num_layers, self.adj)
        reverse_feature = self.reverse_features(temp_features)
        re_pfeatures = propagate(reverse_feature, self.num_layers, self.adj)

        cos = nn.CosineSimilarity()
        sim = cos(pfeatures, re_pfeatures)
        
        alpha = 0.1
        gamma = 0.1
        max_val = 0.
        while True:
            influence_nodes_with_unlearning_nodes = torch.nonzero(sim <= alpha).flatten().cpu()
            if len(influence_nodes_with_unlearning_nodes.view(-1)) > 0:
                temp_max = torch.max(sim[influence_nodes_with_unlearning_nodes])
            else:
                alpha = alpha + gamma
                continue

            if temp_max == max_val:
                break

            max_val = temp_max
            alpha = alpha + gamma

        # influence_nodes_with_unlearning_nodes = torch.nonzero(sim < 0.5).squeeze().cpu()
        neighborkhop, _, _, two_hop_mask = k_hop_subgraph(
            torch.tensor(self.temp_node,dtype=torch.long),
            self.num_layers,
            self.data.edge_index,
            num_nodes=self.data.num_nodes)

        neighborkhop = neighborkhop[~np.isin(neighborkhop.cpu(), self.temp_node)]
        neighbor_nodes = []
        for idx in influence_nodes_with_unlearning_nodes:
            if idx in neighborkhop and idx not in self.temp_node:
                neighbor_nodes.append(idx.item())
        
        neighbor_nodes_mask = torch.from_numpy(np.isin(np.arange(self.data.num_nodes), neighbor_nodes))

        return neighbor_nodes_mask


    def megu_training(self):
        operator = GATE(self.data.num_classes).to(self.device)

        optimizer = torch.optim.SGD(self.target_model.model.parameters(), lr=self.target_model.model.config.lr, weight_decay=self.target_model.model.config.decay)

            

        with torch.no_grad():
            self.target_model.model.eval()
            if self.args["base_model"] == "SIGN":
                preds = self.target_model.model(self.data.xs)
            else:
                preds = self.target_model.model(self.data.x,self.data.edge_index)
            # preds = self.target_model.model(self.data.x, self.data.edge_index)
            if self.args['dataset_name'] == 'ppi':
                preds = torch.sigmoid(preds).ge(0.5)
                preds = preds.type_as(self.data.y)
            else:           
                preds = torch.argmax(preds, axis=1).type_as(self.data.y)
            
        if self.args["base_model"] == "SIGN":
            self.data.x = self.data.x_unlearn
            self.data.edge_index = self.data.edge_index_unlearn
            self.data = SIGN(self.args["GNN_layer"])(self.data)
            self.data.xs = [self.data.x] + [self.data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
            self.data.xs = torch.stack(self.data.xs).to('cuda')
            self.data.xs = self.data.xs.transpose(0,1)

        start_time = time.time()
        for epoch in tqdm(range(self.args["unlearning_epochs"]),desc="Unlearning"):
            self.target_model.model.train()
            operator.train()
            optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out_ori =  self.target_model.model(self.data.xs)
            else:
                out_ori = self.target_model.model(self.data.x_unlearn, self.data.edge_index_unlearn)
            out = operator(out_ori)

            if self.args['dataset_name'] == 'ppi':
                loss_u = criterionKD(out_ori[self.temp_node], out[self.temp_node]) - F.binary_cross_entropy_with_logits(out[self.temp_node], preds[self.temp_node])
                loss_r = criterionKD(out[self.neighbor_khop], out_ori[self.neighbor_khop]) + F.binary_cross_entropy_with_logits(out_ori[self.neighbor_khop], preds[self.neighbor_khop])
            else:
                loss_u = criterionKD(out_ori[self.temp_node], out[self.temp_node]) - F.cross_entropy(out[self.temp_node], preds[self.temp_node])
                loss_r = criterionKD(out[self.neighbor_khop], out_ori[self.neighbor_khop]) + F.cross_entropy(out_ori[self.neighbor_khop], preds[self.neighbor_khop])

            loss = self.args['kappa'] * loss_u + loss_r

            loss.backward()
            optimizer.step()

        unlearn_time = time.time() - start_time
        self.target_model.model.eval()
        if self.args["base_model"] == "SIGN":
            test_out =  self.target_model.model(self.data.xs)
        else:
            test_out = self.target_model.model(self.data.x_unlearn, self.data.edge_index_unlearn)
        if self.args['dataset_name'] == 'ppi':
            out = torch.sigmoid(test_out)
        else:
            out = self.correct_and_smooth(F.softmax(test_out, dim=-1), preds)

        y_hat = out.cpu().detach().numpy()
        y = self.data.y.cpu()
        if self.args['dataset_name'] == 'ppi':
            test_f1 = calc_f1(y, y_hat, self.data.test_mask, multilabel=True)
        else:
            test_f1 = calc_f1(y, y_hat, self.data.test_mask)


        return unlearn_time, test_f1


    def update_edge_index_unlearn(self, delete_nodes, delete_edge_index=None):
        edge_index = self.data.edge_index.numpy()

        unique_indices = np.where(edge_index[0] < edge_index[1])[0]
        unique_indices_not = np.where(edge_index[0] > edge_index[1])[0]

        if self.args["unlearn_task"] == 'edge':
            remain_indices = np.setdiff1d(unique_indices, delete_edge_index)
        else:
            unique_edge_index = edge_index[:, unique_indices]
            delete_edge_indices = np.logical_or(np.isin(unique_edge_index[0], delete_nodes),
                                                np.isin(unique_edge_index[1], delete_nodes))
            remain_indices = np.logical_not(delete_edge_indices)
            remain_indices = np.where(remain_indices == True)

        remain_encode = edge_index[0, remain_indices] * edge_index.shape[1] * 2 + edge_index[1, remain_indices]
        unique_encode_not = edge_index[1, unique_indices_not] * edge_index.shape[1] * 2 + edge_index[
            0, unique_indices_not]
        sort_indices = np.argsort(unique_encode_not)
        remain_indices_not = unique_indices_not[
            sort_indices[np.searchsorted(unique_encode_not, remain_encode, sorter=sort_indices)]]
        remain_indices = np.union1d(remain_indices, remain_indices_not)

        return torch.from_numpy(edge_index[:, remain_indices])
    
    def reverse_features(self, features):
        reverse_features = features.clone()
        for idx in self.temp_node:
            reverse_features[idx] = 1 - reverse_features[idx]

        return reverse_features

    def correct_and_smooth(self, y_soft, preds):
        pos = CorrectAndSmooth(num_correction_layers=80, correction_alpha=self.args['alpha1'],
                               num_smoothing_layers=80, smoothing_alpha=self.args['alpha2'],
                               autoscale=False, scale=1.)

        y_soft = pos.correct(y_soft, preds[self.data.train_mask], self.data.train_mask,
                                  self.data.edge_index_unlearn)
        y_soft = pos.smooth(y_soft, preds[self.data.train_mask], self.data.train_mask,
                                 self.data.edge_index_unlearn)
        
        return y_soft
    
    def mia_attack(self,mem_labels_o,non_labels_o,mem_labels,non_labels):
        mia_test_y = torch.cat((torch.ones(self.args["num_unlearned_nodes"]), torch.zeros(self.args["num_unlearned_nodes"])))
        posterior1 = torch.cat((mem_labels_o, non_labels_o), 0).cpu().detach()
        posterior2 = torch.cat((mem_labels, non_labels), 0).cpu().detach()
        posterior = np.array([np.linalg.norm(posterior1[i]-posterior2[i]) for i in range(len(posterior1))])
        # self.logger.info("posterior:{}".format(posterior))
        auc = roc_auc_score(mia_test_y, posterior.reshape(-1, 1))
        self.average_auc[self.run] = auc
        # self.logger.info("auc:{}".format(auc))
        # self.plot_auc(mia_test_y, posterior.reshape(-1, 1))
        return auc