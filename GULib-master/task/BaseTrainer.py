import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy
from tqdm import trange, tqdm
# from torch_geometric.data import DataLoader
from torch_geometric.loader import DataLoader
from torch_geometric.utils import negative_sampling
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score
from config import root_path
from torch_geometric.data import Data
from torch_geometric.transforms import RandomLinkSplit
from torch_geometric.loader import NeighborSampler
from torch_geometric.loader import NeighborLoader
from torch_geometric.loader import GraphSAINTNodeSampler
from torch_geometric.loader import ClusterData, ClusterLoader
from torch_geometric.utils import k_hop_subgraph, to_scipy_sparse_matrix
from utils.utils import sparse_mx_to_torch_sparse_tensor,normalize_adj
class BaseTrainer:
    """
    A base trainer class for training models on various tasks (node, edge, or graph level).

    This class provides a foundational framework for training different types of models 
    on graph-based datasets. It manages essential components such as configuration 
    parameters, logging, model setup, and data handling. Subclasses should extend 
    this class to implement specific training and evaluation routines tailored to their 
    respective tasks.

    Class Attributes:
        args (dict): Configuration parameters for training, including model type, 
                     dataset specifications, and training hyperparameters.

        logger (logging.Logger): Logger object for logging training progress, metrics, 
                                 and other relevant information.

        model (torch.nn.Module): The neural network model to be trained.

        data (torch_geometric.data.Data): The dataset containing graph information, 
                                         including features, labels, and edge indices, 
                                         used for training and evaluation.

        device (torch.device): The computation device (CPU or GPU) on which the model 
                               and data are loaded for training.
    """
    def __init__(self,args,logger,model, data):
        """
        Initializes the BaseTrainer with the provided configuration, logger, model, and data.

        Args:
            args (dict): Configuration parameters, including model type, dataset specifications, 
                        training hyperparameters, and other relevant settings.

            logger (logging.Logger): Logger object used to log training progress, metrics, 
                                     and other important information.

            model (torch.nn.Module): The neural network model that will be trained.

            data (torch_geometric.data.Data): The dataset containing graph information, 
                                             including features, labels, and edge indices, 
                                             used for training and evaluation.
        """
        self.args = args
        self.logger = logger
        self.model = model
        self.data = data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def train(self,save=False,model_path=None):
        """
        Trains the model based on the specified downstream task (node, edge, or graph).

        This method selects the appropriate training routine based on the task type 
        defined in the configuration parameters. It can optionally save the best model 
        weights to the specified path.

        Args:
            save (bool, optional): Whether to save the best model weights during training.
                                   Defaults to False.

            model_path (str, optional): The path where the best model weights will be saved.
                                        If None, a default path based on configuration parameters
                                        will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best F1 score achieved during training and 
                   the average training time per epoch.
        """
        if self.args["downstream_task"] == 'node':
            return self.train_node(save,model_path)
        elif self.args["downstream_task"] == 'edge':
            return self.train_edge(save,model_path)
        elif self.args["downstream_task"]=="graph":
            self.train_loader = DataLoader(self.data[0], batch_size=64, shuffle=False)
            self.test_loader = DataLoader(self.data[1], batch_size=64, shuffle=False)
            # self.train_loader = self.gen_loader(mode="train",batch_size=64)
            # self.test_loader = self.gen_loader(mode="test",batch_size=64)
            return self.train_graph(save,model_path)

    def evaluate(self):
        """
        Evaluates the model based on the specified downstream task (node, edge, or graph).

        This method selects the appropriate evaluation routine based on the task type 
        defined in the configuration parameters.

        Returns:
            float: The evaluation result of the model, such as F1 score, accuracy, etc., 
                   depending on the task.
        """
        if self.args["downstream_task"] == 'node':
            return self.test_node_fullbatch()
        elif self.args["downstream_task"] == 'edge':
            return self.evaluate_edge_model()
        elif self.args["downstream_task"]=="graph":
            return self.evaluate_graph_model()

    def train_node(self,save=False,model_path=None):
        """
        Trains the model for node-level tasks.

        Depending on the configuration, this method either performs mini-batch training 
        or full-batch training for node classification tasks.

        Args:
            save (bool, optional): Whether to save the best model weights during training.
                                   Defaults to False.

            model_path (str, optional): The path where the best model weights will be saved.
                                        If None, a default path based on configuration parameters
                                        will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best F1 score achieved during training and 
                   the average training time per epoch.
        """
        if self.args["use_batch"]:
            return self.train_node_minibatch(save,model_path)
        else:
            return self.train_node_fullbatch(save,model_path)


    def train_edge(self,save=False,model_path=None):
        """
        Trains the model for edge-level tasks.

        This method handles the training loop for edge classification tasks, including 
        loss computation, backpropagation, optimizer steps, evaluation, and model saving.

        Args:
            save (bool, optional): Whether to save the best model weights during training.
                                   Defaults to False.

            model_path (str, optional): The path where the best model weights will be saved.
                                        If None, a default path based on configuration parameters
                                        will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best F1 score achieved during training and 
                   the average training time per epoch.
        """
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        # print("train_data",self.data)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr,
                                          weight_decay=self.model.config.decay)
        time_sum = 0
        best_f1 = 0
        best_w = 0
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training Edge", unit="epoch"):
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
            # edge_logits = torch.sigmoid(edge_logits)
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
        if not model_path:
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_f1,avg_training_time

    # def get_edge_loss(self,out,edge_index,reduction):
    #     neg_edge_index = negative_sampling(
    #             edge_index=edge_index,num_nodes=out.shape[0],
    #             num_neg_samples=edge_index.size(1)
    #         )
    #     neg_edge_label = torch.zeros(neg_edge_index.size(1), dtype=torch.float32)
    #     pos_edge_label = torch.ones(edge_index.size(1),dtype=torch.float32)
    #     edge_logits = self.decode(z=out, pos_edge_index=edge_index,neg_edge_index=neg_edge_index)
    #     edge_labels = torch.cat((pos_edge_label,neg_edge_label),dim=-1)
    #     edge_labels = edge_labels.to(self.device)
    #     loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels,reduction=reduction)
    #     return loss
        
    def split_edge(self, data):
        """
        Splits the edges of the graph into training, validation, and test sets.

        This method uses the `RandomLinkSplit` utility to randomly split the edges while 
        maintaining the graph's undirected property and adding negative samples to the training set.

        Args:
            data (torch_geometric.data.Data): The original graph data containing all edges.

        Returns:
            torch_geometric.data.Data: The updated graph data with `train_edge_index`, 
                                        `val_edge_index`, `test_edge_index`, and their 
                                        corresponding labels and label indices.
        """
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
    
    def train_graph(self,save=False,model_path=None):
        """
        Trains the model for graph-level tasks.

        This method handles the training loop for graph classification tasks, including 
        loss computation, backpropagation, optimizer steps, evaluation, and model saving.

        Args:
            save (bool, optional): Whether to save the best model weights during training.
                                   Defaults to False.

            model_path (str, optional): The path where the best model weights will be saved.
                                        If None, a default path based on configuration parameters
                                        will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best accuracy achieved during training and 
                   the average training time per epoch.
        """
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr,
                                          weight_decay=self.model.config.decay)
        time_sum = 0
        best_acc = 0
        best_w = 0
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            start_time = time.time()
            for graph_data in self.train_loader:
                graph_data = graph_data.to(self.device)
                self.optimizer.zero_grad()

                if self.args["base_model"] == "SIGN":
                    logits,feat = self.model(graph_data.xs,return_feature=True)
                else:
                    logits,feat = self.model(graph_data.x, graph_data.edge_index,return_feature=True,batch = graph_data.batch)
                # mask  = torch.ones_like(graph_data.y).bool()
                
                loss = F.cross_entropy(logits,graph_data.y)

                loss.backward()
                self.optimizer.step()
            self.best_valid_acc = 0
            time_sum += time.time() - start_time

            if (epoch + 1) % self.args["test_freq"] == 0:
                acc = self.evaluate_graph_model()
                if acc > best_acc:
                    best_acc = acc
                    if save:
                        best_w = copy.deepcopy(self.model.state_dict())
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, best_acc, loss))
        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))
        if not model_path:
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_acc,avg_training_time
    
    @torch.no_grad()
    def evaluate_edge_model(self):
        """
        Evaluates the model on edge-level tasks using the ROC AUC score.

        This method performs edge prediction by computing logits for both positive and 
        negative edges, applying a sigmoid activation, and then calculating the 
        ROC AUC score based on the predicted and true labels.

        Returns:
            float: The ROC AUC score of the model on edge-level tasks.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        # self.data.edge_index = torch.tensor(self.data.edge_index,dtype=torch.long)
        self.data = self.data.to(self.device)

        if self.args["base_model"] == "SIGN":
            out = self.model(self.data.xs)
        else:
            out = self.model(self.data.x, self.data.train_edge_index)
        neg_edge_index = negative_sampling(
            edge_index=self.data.edge_index,num_nodes=self.data.num_nodes,
            num_neg_samples=self.data.test_edge_index.size(1)
        )
        # print(out.shape,self.data.test_edge_index,neg_edge_index)
        edge_pred_logits = self.decode(z=out, pos_edge_index=self.data.test_edge_index,neg_edge_index=neg_edge_index).sigmoid()
        
        # edge_pred_logits = torch.sigmoid(edge_pred_logits*2-1)
        # edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        edge_pred = edge_pred_logits.cpu()
        # edge_pred = torch.argmax(edge_pred_logits)
        # edge_labels = self.data.test_edge_labels
        pos_edge_labels = torch.ones(self.data.test_edge_index.size(1),dtype=torch.float32)
        neg_edge_labels = torch.zeros(neg_edge_index.size(1),dtype=torch.float32)
        edge_labels = torch.cat((pos_edge_labels,neg_edge_labels))
        AUC_score = roc_auc_score(edge_labels.cpu(), edge_pred.cpu())
        # Acc_score = accuracy_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        # Recall_score = recall_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        return AUC_score

    def decode(self, z, pos_edge_index, neg_edge_index=None):
        """
        Decodes the edge logits based on node embeddings.

        This method computes the logits for given edges by taking the dot product 
        of the corresponding node embeddings. It can handle both positive and 
        negative edges if provided.

        Args:
            z (torch.Tensor): The node embeddings.
            pos_edge_index (torch.LongTensor): The indices of positive edges.
            neg_edge_index (torch.LongTensor, optional): The indices of negative edges.
                                                     Defaults to None.

        Returns:
            torch.Tensor: The computed logits for the edges.
        """
        if neg_edge_index is not None:
            edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        else:
            edge_index = pos_edge_index
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        return logits

    def decode_val(self, z, edge_label_index):
        """
        Decodes the logits for validation edges.

        This method computes the logits for validation edges by taking the dot product 
        of the corresponding node embeddings.

        Args:
            z (torch.Tensor): The node embeddings.
            edge_label_index (torch.LongTensor): The indices of edges for validation.

        Returns:
            torch.Tensor: The computed logits for the validation edges.
        """
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def get_edge_labels(self, pos_edge_index, neg_edge_index):
        """
        Generates edge labels for positive and negative edges.

        This method creates a label tensor where positive edges are labeled as 1 and 
        negative edges are labeled as 0.

        Args:
            pos_edge_index (torch.LongTensor): The indices of positive edges.
            neg_edge_index (torch.LongTensor): The indices of negative edges.

        Returns:
            torch.Tensor: A tensor containing labels for the edges.
        """
        num_edges = pos_edge_index.size(1) + neg_edge_index.size(1)
        edge_labels = torch.zeros(num_edges, dtype=torch.float32, device=self.device)  # float32 or float
        edge_labels[:pos_edge_index.size(1)] = 1
        return edge_labels

    def train_node_minibatch(self,save=False,model_path=None):
        """
        Trains the model for node-level tasks using mini-batch training.

        This method handles the training loop for node classification tasks using 
        mini-batch data loaders. It includes loss computation, backpropagation, 
        optimizer steps, evaluation, and model saving.

        Args:
            save (bool, optional): Whether to save the best model weights during training.
                                   Defaults to False.

            model_path (str, optional): The path where the best model weights will be saved.
                                        If None, a default path based on configuration parameters
                                        will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best F1 score achieved during training and 
                   the average training time per epoch.
        """
        time_sum  = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data.num_nodes = self.data.x.size(0)
        self.data = self.data.to('cpu')
        if self.args["base_model"] == "SAINT":
            self.loader = GraphSAINTNodeSampler(self.data,batch_size=256)
        elif self.args["base_model"] == "Cluster_GCN":
            cluster_data = ClusterData(self.data, num_parts=50)  
            cluster_data.data.num_edges = self.data.edge_index.size(1)
            self.loader = ClusterLoader(cluster_data, batch_size=5, shuffle=False)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="BaseTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            for data in self.loader:
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
        # time_sum = 0
        # best_f1 = 0
        # best_w = 0
        # self.model.train()
        # self.model.reset_parameters()
        # self.model = self.model.to(self.device)
        # self.data = self.data.to(self.device)

        # # 构建 NeighborLoader
        # edge_index = self.data.edge_index
        # train_mask = self.data.train_mask
        # batch_size = 2048  # minibatch大小
        # sizes = [10, 10]  # 每层采样的邻居数

        # # 使用 NeighborLoader 构建数据加载器
        # loader = NeighborLoader(
        #     self.data,
        #     num_neighbors=sizes,
        #     batch_size=batch_size,
        #     shuffle=True,
        #     input_nodes=self.data.train_mask,  # 只从训练节点开始采样
        # )

        # self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        
        # for epoch in tqdm(range(self.args['num_epochs']), desc="BaseTraining", unit="epoch"):
        #     start_time = time.time()
        #     self.model.train()
        #     self.optimizer.zero_grad()

        #     # 遍历 NeighborLoader 生成的 mini-batch
        #     for batch in loader:
        #         # batch = batch.to(self.device)
        #         # batch: 当前batch，包含了子图的数据
        #         # batch.x, batch.edge_index, batch.y 是该子图中的节点特征、边和标签
        #         if self.args["base_model"] == "SIGN":
        #             out = self.model(batch.xs)  # SIGN模型
        #         else:
        #             out = self.model(batch.x, batch.edge_index)  # 其他模型

        #         # 计算损失：仅使用训练集的mask部分进行计算
        #         loss = F.cross_entropy(out[batch.train_mask], batch.y[batch.train_mask])
        #         loss.backward()
        #         self.optimizer.step()

        #     time_sum += time.time() - start_time

        #     # 在指定的频率下进行测试
        #     if (epoch + 1) % self.args["test_freq"] == 0:
        #         f1 = self.test_node_minibatch()  # 使用适当的测试方法
        #         if f1 > best_f1:
        #             best_f1 = f1
        #             if save:
        #                 best_w = copy.deepcopy(self.model.state_dict())
        #         self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, f1, loss))

        # avg_training_time = time_sum / self.args['num_epochs']
        # self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))
        
        # if not model_path:
        #     model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"]  +"/"+self.args["downstream_task"]+"/" + self.args["base_model"]
        
        # os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        # self.save_model(model_path, best_w)
        
        # return best_f1, avg_training_time
    def train_node_fullbatch(self,save=False,model_path=None):
        """
        Trains the model for node-level tasks using full-batch training.

        This method performs full-batch training for node classification tasks, where the entire dataset 
        is used at once for each forward pass. It includes loss computation, backpropagation, 
        optimizer steps, evaluation, and model saving.

        Args:
            save (bool, optional): Whether to save the best model weights during training. Defaults to False.
            model_path (str, optional): The path where the best model weights will be saved. 
                                        If None, a default path based on configuration parameters will be used. Defaults to None.

        Returns:
            tuple: A tuple containing the best F1 score achieved during training and 
                   the average training time per epoch.
        """
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        # if self.args['dataset_name'] == "ogbn-products":
        #     self.model.adj = self.sparse_mx_to_torch_sparse_tensor(normalize_adj(to_scipy_sparse_matrix(self.data.edge_index,num_nodes=self.data.num_nodes))).cuda()
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
        if not model_path:
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"]  +"/"+self.args["downstream_task"]+"/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        
        return best_f1,avg_training_time

    @torch.no_grad()
    def test_node_fullbatch(self):
        """
        Evaluates the model for node-level tasks using full-batch testing.

        This method performs evaluation on the test set using the entire dataset at once. 
        It computes the F1 score based on the model's predictions and compares them against the true labels.

        Returns:
            float: The F1 score on the test set.
        """
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
    
    @torch.no_grad
    def test_node_minibatch(self):
        """
        Evaluates the model for node-level tasks using mini-batch testing.

        This method performs evaluation on the test set using mini-batches of data. 
        It computes the F1 score based on the model's predictions and compares them against the true labels.

        Returns:
            float: The F1 score on the test set using mini-batch evaluation.
        """
        self.model.eval()  # 设置模型为评估模式
        all_preds = []  # 用于存储所有预测值
        all_labels = []  # 用于存储所有真实标签

        for data in self.loader:
            data = data.to(self.device)
            out = self.model(data.x, data.edge_index)  # 前向传播
            pred = out.argmax(dim=1)  # 获取预测类别
            # 仅选择测试集上的预测和标签
            all_preds.append(pred[data.test_mask].cpu())
            all_labels.append(data.y[data.test_mask].cpu())

        # 将分批次预测和真实标签拼接
        all_preds = torch.cat(all_preds, dim=0).numpy()
        all_labels = torch.cat(all_labels, dim=0).numpy()

        # 计算 F1-score (支持多分类，average 可选 'micro', 'macro', 'weighted')
        f1 = f1_score(all_labels, all_preds, average='micro')

        return f1
        
    @torch.no_grad()
    def evaluate_graph_model(self):
        """
        Evaluates the graph model's performance on node-level tasks.

        This method computes the overall accuracy of the model on the test set, 
        using the model's predictions and comparing them against the true labels.

        Returns:
            float: The accuracy score on the test set.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        # self.data = self.data.to(self.device)
        
        preds = []
        labels = []
        for graph_data in self.test_loader:
            graph = graph_data.to(self.device)
            if self.args["base_model"] == "SIGN":
                logits,feat = self.model(graph.xs,return_feature=True)
            else:
                logits,feat = self.model(graph.x, graph.edge_index,return_feature=True,batch = graph.batch)
            # loss = F.cross_entropy(logits,graph_data.y)
            # print(logits,feat)
            pred = logits.argmax(dim=1)
            preds.append(pred)
            labels.append(graph.y)

        preds = torch.concat(preds,dim=0).cpu()
        labels = torch.concat(labels,dim=0).cpu()
        acc = accuracy_score(labels,preds)
        return acc


    def posterior(self):
        """
        Computes the model's posteriors for node-level tasks.

        This method performs a forward pass through the model to compute the posteriors for node classification tasks.
        It applies softmax to the output, optionally using different model configurations, such as GraphRevoker or SIGN.
        The result is computed based on the test mask and returned.

        Returns:
            Tensor: The log-softmax of the posteriors for the test set nodes.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["unlearning_methods"] == "GraphRevoker":
            posteriors = self.model(self.data.x, self.data.edge_index)
            return F.log_softmax(posteriors[self.data.test_mask, :]).detach()
        else:
            if self.args["base_model"] == "SIGN":
                posteriors = self.model(self.data.xs)
            else:
                posteriors = self.model(self.data.x,self.data.edge_index)
            for _, mask in self.data('test_mask'):
                posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

        return posteriors.detach()

    def save_model(self, save_path,model_dict=None):
        """
        Saves the model's state or a specific model dictionary to the specified file path.

        This method saves the current state of the model or an optional custom model dictionary to a file. 
        If the directory does not exist, it is created. The model is saved using PyTorch's `torch.save` method.

        Args:
            save_path (str): The path to the file where the model will be saved.
            model_dict (dict, optional): A specific model dictionary to save. If None, the model's current state is saved. Defaults to None.
        """
        folder_path = os.path.dirname(save_path)

        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(save_path,mode='w') as file:
            if model_dict is not None:
                self.logger.info('saving best model {}'.format(save_path))
                torch.save(model_dict, save_path)
            else:
                self.logger.info('saving model {}'.format(save_path))
                torch.save(self.model.state_dict(), save_path)

    def load_model(self, save_path):
        """
        Loads the model's state from the specified file path.

        This method loads the model's state dictionary from a file using PyTorch's `torch.load` and applies it to the model.

        Args:
            save_path (str): The path to the file from which the model will be loaded.
        """
        self.model.load_state_dict(torch.load(save_path, map_location=self.device))
        
        
    def prepare_data(self, input_data):
        """
        Prepares the data for training and evaluation.

        This method clones the input data and modifies it for training and evaluation. It specifically sets the edge index
        to the training edge index and removes the training edge index from the data to prevent it from being used during inference.

        Args:
            input_data (Data): The input data object containing graph data and edge indices.
        """
        data_full = input_data.clone()
        data = input_data.clone()
        
        data.edge_index = data.edge_index_train
        
        data.edge_index_train = None
        data_full.edge_index_train = None

        # to_sparse = T.ToSparseTensor()
        # self.data = to_sparse(data)
        self.data.edge_index = input_data.edge_index_train
        self.data.edge_index_train = None
        self.data_full = data_full
        
    def posterior_con(self,return_features=False,mia=False):
        """
        Computes the model's posteriors for node-level tasks with optional feature return.

        This method computes the posteriors for node classification tasks using either full-batch or mini-batch processing. 
        It also includes an option to return the features from the model, depending on the `return_features` parameter.

        Args:
            return_features (bool, optional): Whether to return the features along with the posteriors. Defaults to False.
            mia (bool, optional): Whether to apply the MIA (Model Inversion Attack) method. Defaults to False.

        Returns:
            Tensor: The log-softmax of the posteriors for the test set nodes.
            (Optional) Tensor: The features from the model, if `return_features` is True.
        """
        # self.logger.debug("generating posteriors")
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self.model.eval()
        if mia:
            if self.args["base_model"] == "SIGN":
                posteriors = F.log_softmax(self.model(self.data.xs))
            else:
                posteriors = F.log_softmax(self.model(self.data.x,self.data.edge_index))
            for _, mask in self.data('test_mask'):
                posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

            return posteriors.detach()
        else:
            z, f = self._inference()

        if return_features:
        #     return z[self.data_full.test_mask], f[self.data_full.test_mask]
        # return z[self.data_full.test_mask, :]
            return z[self.data.test_mask], f[self.data.test_mask]
        return z[self.data.test_mask, :]
    
    @torch.no_grad()
    def _inference(self, no_test_edges=False):
        """
        Performs inference on the model without gradient tracking.

        This method runs a forward pass through the model to get the posteriors and features for the input data, 
        and applies softmax to the results. It performs inference for both training and testing data.

        Args:
            no_test_edges (bool, optional): Whether to exclude test edges in the data. Defaults to False.

        Returns:
            tuple: A tuple containing the log-softmax of the posteriors and the features from the model.
        """
        # assert not self.data is None and not self.data_full is None

        self.model.eval()
        self.model = self.model.to(self.device)
        # self.data_full = self.data.to(self.device) if no_test_edges else self.data_full.to(self.device)
        self.data = self.data.to(self.device) 
        
        # z, feat = self.model(self.data_full.x, self.data_full.edge_index, return_feature=True)
        z, feat = self.model(self.data.x, self.data.edge_index, return_feature=True)

        return F.log_softmax(z,dim=1), feat
    
    def gen_loader(self,mode="train",batch_size=1,shuffle=True):
        """
        Generates a data loader for a specified mode (train, validation, or test).

        This method generates mini-batches of graph data for training, validation, or testing. 
        The data is filtered according to the specified mode, and a DataLoader is returned to handle batching and shuffling.

        Args:
            mode (str, optional): The mode for generating the loader, can be "train", "val", or "test". Defaults to "train".
            batch_size (int, optional): The batch size for the DataLoader. Defaults to 1.
            shuffle (bool, optional): Whether to shuffle the data. Defaults to True.

        Returns:
            DataLoader: A PyTorch DataLoader that can be used to iterate over the graph data in mini-batches.
        """
        data_list = []
        if mode == "train":
            for gid in self.data.train_ids:
                mask = self.data.graph_id == gid
                sub_x = self.data.x[mask]
                sub_edge_index = self.data.edge_index[:,(self.data.edge_index[0] >= mask.nonzero().min()) & (self.data.edge_index[1] <= mask.nonzero().max())]- mask.nonzero().min()
                sub_y = self.data.y[gid]
                data_list.append(Data(x=sub_x, edge_index=sub_edge_index, y=sub_y))
        elif mode == "val":
            for gid in self.data.val_ids:
                mask = self.data.graph_id == gid
                sub_x = self.data.x[mask]
                sub_edge_index = self.data.edge_index[:,(self.data.edge_index[0] >= mask.nonzero().min()) & (self.data.edge_index[1] <= mask.nonzero().max())]- mask.nonzero().min()
                sub_y = self.data.y[gid]
                data_list.append(Data(x=sub_x, edge_index=sub_edge_index, y=sub_y))
                
        elif mode == "test":
            for gid in self.data.test_ids:
                mask = self.data.graph_id == gid
                sub_x = self.data.x[mask]
                sub_edge_index = self.data.edge_index[:,(self.data.edge_index[0] >= mask.nonzero().min()) & (self.data.edge_index[1] <= mask.nonzero().max())]- mask.nonzero().min()
                sub_y = self.data.y[gid]
                data_list.append(Data(x=sub_x, edge_index=sub_edge_index, y=sub_y))
                
        return DataLoader(data_list,batch_size=batch_size,shuffle=shuffle)
    
    def forward_graph_once(self,data):
        """
        Performs a forward pass through the model for a single graph.

        This method performs a forward pass through the model for the given data, which is expected to be a graph. 
        It computes the logits (model predictions) for the graph and returns them.

        Args:
            data (Data): The graph data to pass through the model.

        Returns:
            Tensor: The logits for the graph after a forward pass through the model.
        """
        loader = self.gen_loader(mode="train",batch_size=data.y.size(),shuffle=False)
        logits = []
        for graph_data in loader:
            logit = self.model(graph_data.x,graph_data.edge_index,batch=graph_data.batch)
            logits.append(logit)
        logits = torch.concat(logits,dim=0)
        return logits
    
    def posterior_edge(self):
        """
        Computes the model's posteriors for edge-level tasks.

        This method computes the posteriors for edge classification tasks, using the model to predict edge labels for the 
        positive and negative test edges. The posteriors are then passed through a sigmoid activation to return probabilities.

        Returns:
            Tensor: The posteriors for the test set edges, passed through a sigmoid activation.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)

        neg_edge_index = negative_sampling(
            edge_index=self.data.test_edge_index,num_nodes=self.data.num_nodes,
            num_neg_samples=self.data.test_edge_index.size(1)
        )
        if self.args["unlearning_methods"] == "GraphRevoker":
            posteriors = self.model(self.data.x, self.data.test_edge_index)
            return self.decode(posteriors,pos_edge_index=self.data.test_edge_index,neg_edge_index=neg_edge_index).detach()
        else:
            if self.args["base_model"] == "SIGN":
                posteriors = self.model(self.data.xs)
            else:
                posteriors = self.model(self.data.x,self.data.test_edge_index)
            posteriors = self.decode(posteriors,pos_edge_index=self.data.test_edge_index,neg_edge_index=neg_edge_index).sigmoid()
            # print(posteriors)
        return posteriors.detach()
