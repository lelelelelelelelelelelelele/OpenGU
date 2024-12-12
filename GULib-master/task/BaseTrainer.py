import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy
from tqdm import trange, tqdm
from torch_geometric.data import DataLoader
from torch_geometric.utils import negative_sampling
from torch_geometric.loader import GraphSAINTRandomWalkSampler
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score
from config import root_path
from torch_geometric.data import Data
from torch_geometric.transforms import RandomLinkSplit
class BaseTrainer:
    def __init__(self,args,logger,model, data):
        self.args = args
        self.logger = logger
        self.model = model
        self.data = data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def train(self,save=False):
        if self.args["downstream_task"] == 'node':
            return self.train_node(save)
        else:
            return self.train_edge(save)

    def train_node(self,save=False):
        if self.args["use_batch"]:
            return self.train_node_minibatch(save)
        else:
            return self.train_node_fullbatch(save)


    def train_edge(self,save=False):
        print(self.data)
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr,
                                          weight_decay=self.model.config.decay)
        time_sum = 0
        best_f1 = 0
        best_w = 0
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            start_time = time.time()
            self.model.train()

            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.train_edge_index)

            neg_edge_index = negative_sampling(
                edge_index=self.data.train_edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.train_edge_index.size(1)
            )
            neg_edge_label = torch.zeros(neg_edge_index.size(1), dtype=torch.float32)
            pos_edge_label = torch.ones(self.data.train_edge_index.size(1),dtype=torch.float32)

            edge_logits = self.decode(z=out, pos_edge_index=self.data.train_edge_index,neg_edge_index=neg_edge_index)
            edge_labels = torch.cat((pos_edge_label,neg_edge_label),dim=-1)
            edge_labels = edge_labels.to(self.device)
            loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels)
            # loss = self.get_loss(out)
            loss.backward()
            self.optimizer.step()
            self.best_valid_acc = 0
            time_sum += time.time() - start_time
            # print(loss.item())
            if (epoch + 1) % self.args["test_freq"] == 0:
                F1_score = self.evaluate_edge_model()
                if F1_score > best_f1:
                    best_f1 = F1_score
                    if save:
                        best_w = copy.deepcopy(self.model.state_dict())
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, F1_score, loss))
        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))
        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_f1,avg_training_time

    def split_edge(self, data):
        # print(type(data.adj))
        temp = Data(x=data.x, y=data.y, edge_index=data.edge_index)
        train_data, val_data, test_data = RandomLinkSplit(num_val=0.2, num_test=0.1, is_undirected=True,
                                                          add_negative_train_samples=True)(temp)

        data.train_edge_index = train_data.edge_index
        data.test_edge_index = test_data.edge_index
        data.val_edge_index = val_data.edge_index

        data.train_edge_label = train_data.edge_label
        data.test_edge_label = test_data.edge_label
        data.val_edge_label = val_data.edge_label

        data.train_edge_label_index = train_data.edge_label_index
        data.test_edge_label_index = test_data.edge_label_index
        data.val_edge_label_index = val_data.edge_label_index
        # print(train_data.edge_label.shape)

        return data
    
    @torch.no_grad()
    def evaluate_edge_model(self):

        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)

        if self.args["base_model"] == "SIGN":
            out = self.model(self.data.xs)
        else:
            out = self.model(self.data.x, self.data.test_edge_index)
        neg_edge_index = negative_sampling(
                edge_index=self.data.test_edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.test_edge_index.size(1)
            )
        edge_pred_logits = self.decode(z=out, pos_edge_index=self.data.test_edge_index,neg_edge_index=neg_edge_index)
        edge_pred_logits = torch.sigmoid(edge_pred_logits)
        edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        
        # edge_pred = torch.argmax(edge_pred_logits)
        pos_edge_labels = torch.ones(self.data.test_edge_index.size(1),dtype=torch.float32)
        neg_edge_labels = torch.zeros(neg_edge_index.size(1),dtype=torch.float32)
        edge_labels = torch.cat((pos_edge_labels,neg_edge_labels))
        F1_score = f1_score(edge_labels.cpu(), edge_pred.cpu())
        # Acc_score = accuracy_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        # Recall_score = recall_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        return F1_score

    def decode(self, z, pos_edge_index,neg_edge_index):
        edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
        return (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

    def decode_val(self, z, edge_label_index):
        # print(z.shape)
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def get_edge_labels(self, pos_edge_index, neg_edge_index):
        num_edge = pos_edge_index.size(1) + neg_edge_index.size(1)
        edge_labels = torch.zeros(num_edge, dtype=torch.float32, device=self.device)  # float32 or float
        edge_labels[:pos_edge_index.size(1)] = 1
        return edge_labels

    def train_node_minibatch(self,save=False):
        pass

    def train_node_fullbatch(self,save=False):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="BaseTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.edge_index)
            loss = F.cross_entropy(out[self.data.train_mask], self.data.y[self.data.train_mask]).to(self.device)
            loss.backward()
            self.optimizer.step()
            time_sum += time.time() - start_time

            #test#
            if (epoch + 1) % self.args["test_freq"] == 0:
                f1 = self.test_node_fullbatch()
                if f1 > best_f1:
                    best_f1 = f1
                    if save:
                        best_w = copy.deepcopy(self.model.state_dict())
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, f1, loss))

        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))
        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_f1,avg_training_time

    @torch.no_grad()
    def test_node_fullbatch(self):
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SIGN":
            y_pred = self.model(self.data.xs).cpu()
        else:
            y_pred = self.model(self.data.x, self.data.edge_index).cpu()
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        f1 = f1_score(y[self.data.test_mask.cpu()], y_pred[self.data.test_mask.cpu()], average="micro")
        return f1

    def posterior(self):
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["unlearning_methods"] == "GraphRevoker":
            posteriors = self.model(self.data.x, self.data.edge_index)
            return F.log_softmax(posteriors[self.data.test_mask, :]).detach()
        else:
            if self.args["base_model"] == "SIGN":
                posteriors = F.log_softmax(self.model(self.data.xs))
            else:
                posteriors = F.log_softmax(self.model(self.data.x,self.data.edge_index))
            for _, mask in self.data('test_mask'):
                posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

        return posteriors.detach()

    def save_model(self, save_path,model_dict=None):
        with open(save_path,mode='w') as file:
            if model_dict is not None:
                self.logger.info('saving best model {}'.format(save_path))
                torch.save(model_dict, save_path)
            else:
                self.logger.info('saving model {}'.format(save_path))
                torch.save(self.model.state_dict(), save_path)

    def load_model(self, save_path):
        self.model.load_state_dict(torch.load(save_path, map_location=self.device))