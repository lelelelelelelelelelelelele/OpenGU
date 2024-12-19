import torch.nn.functional as F
import torch
import time
import numpy as np
import copy
import os
from task.BaseTrainer import BaseTrainer
from config import root_path
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from torch_geometric.loader import GraphSAINTNodeSampler
class GUIDETrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)
    

    def train_node_fullbatch(self,save=False,model_path =False):
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            self.model.train()
            labels = self.data.y

            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
                loss = F.cross_entropy(out[self.data.train_mask], labels[self.data.train_mask[:labels.size(0)]])
            else:
                out = self.model(self.data.x,self.data.edge_index)
                loss = F.cross_entropy(out[self.data.train_mask], labels[self.data.train_mask[:labels.size(0)]])
            loss.backward()
            self.optimizer.step()

            if (epoch + 1) % self.args["test_freq"] == 0:
                y_pred,y = out[self.data.test_mask.cpu()],self.data.y[self.data.test_mask[:labels.size(0)].cpu()]
                y_pred = y_pred.detach().cpu().numpy()              
                y = y.detach().cpu().numpy()
                f1macro = f1_score(y, np.argmax(y_pred, axis=1), average='macro')
                
                self.logger.info('Epoch: {:03d} | Loss: {:.4f} | F1: {:.4f}'.format(epoch + 1, loss, f1macro))

    def train_node_minibatch(self,save=False,model_path=None):
        time_sum  = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data.num_nodes = self.data.x.size(0)
        self.data = self.data.to('cpu')
        padding = torch.full((self.data.num_nodes - self.data.y.size(0),), -1, dtype=self.data.y.dtype)  # 创建填充张量
        self.data.y = torch.cat([self.data.y, padding], dim=0) 
        loader = GraphSAINTNodeSampler(self.data,batch_size=256,num_steps = 10)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="BaseTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            for data in loader:
                data = data.to(self.device)
                out = self.model(data.x, data.edge_index)  # 其他模型
                loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
                loss.backward()
                self.optimizer.step()
            time_sum += time.time() - start_time
            
            if (epoch + 1) % self.args["test_freq"] == 0:
                f1 = self.test_node_minibatch()  # 使用适当的测试方法
                if f1 > best_f1:
                    best_f1 = f1
                    if save:
                        best_w = copy.deepcopy(self.model.state_dict())
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, f1, loss))
                
                avg_training_time = time_sum / self.args['num_epochs']
        if not model_path:
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"]  +"/"+self.args["downstream_task"]+"/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)        
        return best_f1,avg_training_time

    # @torch.no_grad
    def test_node_minibatch(self):
        self.model.eval()  # 设置模型为评估模式
        loader = GraphSAINTNodeSampler(self.data, batch_size=256)  # 创建测试阶段的采样器
        all_preds = []  # 用于存储所有预测值
        all_labels = []  # 用于存储所有真实标签

        for data in loader:
            data = data.to(self.device)
            out = self.model(data.x, data.edge_index)  # 前向传播
            pred = out.argmax(dim=1)  # 获取预测类别
            # 仅选择测试集上的预测和标签
            all_preds.append(pred[data.test_mask].cpu())
            all_labels.append(data.y[data.test_mask].cpu())

        # 将分批次预测和真实标签拼接
        all_preds = torch.cat(all_preds, dim=0).detach().cpu().numpy()
        all_labels = torch.cat(all_labels, dim=0).detach().cpu().numpy()

        # 计算 F1-score (支持多分类，average 可选 'micro', 'macro', 'weighted')
        f1 = f1_score(all_labels, all_preds, average='micro')

        return f1
    
    @torch.no_grad()
    def prediction_info(self):
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        y_pred = self.model(self.data.x, self.data.edge_index).cpu()
        y = self.data.y.cpu()
        return y_pred[self.data.test_mask.cpu()], y[self.data.test_mask.cpu()]