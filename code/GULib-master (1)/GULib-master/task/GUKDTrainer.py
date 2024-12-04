from task.BaseTrainer import BaseTrainer
from sklearn.metrics import f1_score
import torch
from tqdm import trange, tqdm
import time
import torch.nn.functional as F
from config import root_path
import copy
import os
from torch_geometric.utils import negative_sampling
class GUKDTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    def gukd_train(self,z_t,save=False):
        if self.args["downstream_task"] == 'node':
            return self.gukd_train_node(z_t,save)
        else:
            return self.gukd_train_edge(z_t,save)
    def gukd_train_node(self,z_t,save):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        logits_t = F.log_softmax(z_t[self.data.test_mask]).to(self.device)
        for epoch in tqdm(range(self.args['num_epochs']), desc="GUKD_Training", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.edge_index)
            logits_s = F.log_softmax(out[self.data.test_mask],dim=-1)
            loss = F.mse_loss(logits_s, logits_t)
            loss.backward(retain_graph=True)
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

    def gukd_train_edge(self,z_t,save):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        z_t = z_t.to(self.device)
        # print(self.data.test_edge_index.shape)
        neg_edge_index = negative_sampling(
                edge_index=self.data.train_edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.train_edge_index.size(1)
            )
        logits_t = self.decode(z_t,self.data.test_edge_index,neg_edge_index).to(self.device)
        for epoch in tqdm(range(self.args['num_epochs']), desc="GUKD_Training", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.test_edge_index)
            
            logits_s = self.decode(out,self.data.test_edge_index,neg_edge_index)
            loss = F.mse_loss(logits_s, logits_t)
            loss.backward(retain_graph=True)
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