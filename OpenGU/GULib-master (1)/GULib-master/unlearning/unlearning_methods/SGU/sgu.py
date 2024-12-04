import random
import heapq
import numpy
import torch
import copy
import numpy as np
from numba import njit, prange, jit
import os
import torch.nn.functional as F
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from lightgbm import LGBMClassifier
from sklearn.metrics import f1_score, accuracy_score,recall_score,roc_auc_score
from torch_geometric.nn.conv.gcn_conv import gcn_norm
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.utils import to_undirected
import time
from task.node_classification import NodeClassifier
from utils import utils
from utils.utils import aug_normalized_adjacency, cal_distance
from sklearn.utils import shuffle
from torch_geometric.transforms import SIGN
from config import root_path,unlearning_path
from model.base_gnn.Convs import S2GConv,SGConv,GCNConv
from config import BLUE_COLOR,RESET_COLOR
from tqdm import tqdm
from task import get_trainer
from task.edge_prediction import EdgePredictor

class sgu():
    def __init__(self,args,logger,model_zoo):
        self.args = args
        self.logger = logger
        self.model_zoo = model_zoo
        self.data = model_zoo.data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.alpha = 1
        self.Budget = int(self.data.num_nodes *self.args["Budget"])
        self.num_node = self.data.num_node
        self.timecount = {}
        num_runs = self.args["num_runs"]
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_activating_time = np.zeros(num_runs)
        self.avg_sampling_time = np.zeros(num_runs)
        self.avg_training_time = np.zeros(num_runs)
        self.run = 0
        self.best = 0
        self.final_auc = 0


    def run_exp(self):
        if self.args["parameter_task"] == "optuna":
            self.node_unlearning()
        else:
            for self.run in range(self.args["num_runs"]):
                if self.args["unlearn_task"] == "node" or self.args["unlearn_task"] == "feature":
                    self.node_unlearning()
                elif self.args["unlearn_task"] == "edge":
                    self.edge_unlearning()
            self.logger.info(
            "{}Performance Metrics:\n"
            " - Average F1 Score: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average Activating Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Sampling Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
                BLUE_COLOR,
                np.mean(self.average_f1), np.std(self.average_f1),
                np.mean(self.average_auc), np.std(self.average_auc),
                np.mean(self.avg_activating_time), np.std(self.avg_activating_time),
                np.mean(self.avg_sampling_time), np.std(self.avg_sampling_time),
                np.mean(self.avg_training_time), np.std(self.avg_training_time),
                RESET_COLOR
                )
            )


    def node_unlearning(self):
        self.logger.info("unlearning node number:{}".format(self.args["num_unlearned_nodes"]))
        # train
        if self.args["parameter_task"] == "optuna":
            self.features = self.preprocess_feature()
        else:
            if self.run == 0:
                self.features = self.preprocess_feature()
        # self.target_model.data.pre_features = self.features.clone().detach().float()
        # 9.20
        # if self.args["downstream_task"]=="node":
        #     self.target_model = NodeClassifier(self.args, self.data, self.model_zoo, self.logger)
        # elif self.args["downstream_task"]=="edge":
        #     self.target_model = EdgePredictor(self.args, self.data, self.model_zoo, self.logger)
        self.args["unlearn_trainer"] = 'SGUTrainer'
        self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)
        self.target_model.data.pre_features = self.features


        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + \
                         self.args["base_model"]
        if os.path.exists(model_path):
            print(f"File {model_path} already exists.")
            self.target_model.load_model(model_path)
        else:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            with open(model_path, 'w'):
                print(f"File {model_path} created successfully.")
                self.target_model.train()
                self.target_model.load_model(model_path)
                # self.target_model.save_model(model_path)

        # select unlearning dataset
        # train_nodes = np.array(self.data.train_indices)
        # shuffle_num = torch.randperm(train_nodes.size)
        # self.unlearning_nodes = train_nodes[shuffle_num][:self.args["num_unlearned_nodes"]]
        path_un = unlearning_path + "_" + str(self.run) + ".txt"
        self.unlearning_nodes = np.loadtxt(path_un, dtype=int)
        # F1_score, Accuracy, Recall = self.target_model.eval_unlearning(self.features, self.unlearning_nodes)
        # self.logger.info(
        #     'Original Model Unlearning : F1_score = {}  Accuracy = {}  Recall = {}'.format(F1_score, Accuracy, Recall))
        self.unlearning_num = self.unlearning_nodes.size
        self.unlearning_mask = torch.zeros(self.num_node, dtype=torch.bool)
        self.unlearning_mask[self.unlearning_nodes] = True

        # compute influence_score
        start_time = time.time()
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            # self.softlabels = self.target_model.model.get_softlabel(self.features.cuda()).cpu().detach().numpy()
            # get frozen model param
            self.original_emb = self.target_model.model.get_embedding(self.features).clone().detach().float()
            self.original_softlabels = self.target_model.model.get_softlabel(self.features).clone().detach().float()
        else:
            # self.softlabels = self.target_model.model.get_softlabel(self.data.x,self.data.edge_index).cpu().detach().numpy()
            # get frozen model param
            self.data = self.data.to(self.device)
            self.original_emb = self.target_model.model.get_embedding(self.data.x,self.data.edge_index).clone().detach().float()
            self.original_softlabels = self.target_model.model.get_softlabel(self.data.x,self.data.edge_index).clone().detach().float()

        self.feature_similarity = self.cal_similarity(self.features, self.unlearning_nodes, True).cuda()
        # print("feature_similarity ready!")
        self.label_similarity = self.cal_similarity(self.original_softlabels, self.unlearning_nodes, False).cuda()
        # print("label_similarity ready!")
        self.influence_score = (self.feature_similarity + self.alpha * self.label_similarity).clone().detach()
        # print("influence_score ready!")
        del self.feature_similarity
        del self.label_similarity
        # self.logger.info("influence_score: {}".format(self.influence_score))

        # select edit datasets
        # self.activated_nodes = np.loadtxt("./data/SGU/activated_nodes.txt",dtype=int)
        self.activated_nodes = self.activate_nodes()
        self.avg_activating_time[self.run] = time.time()-start_time
        # print("activated_nodes ready!")
        del self.influence_score
        self.activated_mask = torch.zeros(self.num_node, dtype=torch.bool)
        self.activated_mask[self.activated_nodes] = True
        # np.savetxt(root_path + "/data/SGU/activated_nodes.txt", self.activated_nodes, fmt="%d")

        parameter_list = []
        for param_tensor in self.target_model.model.parameters():
            param_clone = param_tensor.clone().detach().float()
            parameter_list.append(param_clone)
        self.original_w = parameter_list
        # print("parameter_list ready!")

        # get prototype embedding
        self.prototype_embedding = self.get_prototype()
        # pred = self.target_model.model.emb2softlable(self.prototype_embedding.to(self.device)).cpu().detach().numpy()
        # pred = np.argmax(pred, axis=1)
        # self.logger.info("proto_acc:{}".format(accuracy_score(y_true=np.arange(0, self.data.num_classes), y_pred=pred)))

        # contrastive learning sampling
        activated_label = np.argmax(self.original_softlabels[self.activated_nodes].cpu().numpy(), axis=1)
        start_time = time.time()
        self.pos_pair = self.pos_sampling(self.activated_nodes, activated_label, self.unlearning_nodes)
        self.neg_pair = self.neg_sampling(self.activated_nodes, activated_label, self.unlearning_nodes)
        self.avg_sampling_time[self.run] = time.time()-start_time
        # delete node
        # self.delete_node()
        # self.features_unlearning = self.preprocess_feature(self.edge_mask)
        # self.features_unlearning = None
        # unlearning process
        # self.mia_attack()
        # self.best = self.target_model.SGU_unlearning(self.original_softlabels,
        #                                    self.original_w,
        #                                    self.unlearning_nodes,
        #                                    self.activated_nodes,
        #                                    self.pos_pair,
        #                                    self.neg_pair,
        #                                    self.features,
        #                                    self.prototype_embedding,
        #                                    self.avg_training_time,
        #                                    self.average_f1,
        #                                    self.run)
        self.best = self.SGU_unlearning()
        # F1_score, Accuracy, Recall = self.target_model.eval_unlearning(self.features, self.unlearning_nodes)
        # self.logger.info(
        #     'Original Model Unlearning : F1_score = {}  Accuracy = {}  Recall = {}'.format(F1_score, Accuracy, Recall))
        # retrain
        # self.retrain(self.unlearning_nodes, self.edge_mask)
        # mia attack test
        self.target_model.load_model(root_path + "/data/model/node_level/"+self.args["dataset_name"]+ "/" + self.args["base_model"]+"_unlearning_best.pt")
        self.final_auc = self.mia_attack()
        self.logger.info("Budget: {}".format(self.Budget))

        


    def preprocess_feature(self,edge_mask=None):
        start_time = time.time()
        if self.args["base_model"] == "SGC":
            propagation = SGConv(self.data.num_features,self.data.num_classes,K=3,bias=False)
            features_pre = propagation.forward_SGU(self.data.x,self.data.edge_index)
            return features_pre.cuda()
        elif self.args["base_model"] == "S2GC":
            propagation = S2GConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            return features_pre.cuda()
        elif self.args["base_model"] == "SIGN":
            return self.data.xs
        elif self.args["base_model"] == "GCN":
            propagation = propagation = SGConv(self.data.num_features,self.data.num_classes,K=3,bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            return features_pre.cuda()
        elif self.args["base_model"] == "GAT":
            propagation = propagation = SGConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            return features_pre.cuda()
        elif self.args["base_model"] == "SAGE":
            propagation = propagation = SGConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            return features_pre.cuda()
        elif self.args["base_model"] == "GIN":
            propagation = propagation = SGConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            return features_pre.cuda()
        timesum = time.time()-start_time
        self.timecount["process_feaure_time"] = timesum

            # adj = aug_normalized_adjacency(self.data.adj)
            # adj_matrix = torch.FloatTensor(adj.todense()).cuda()
            # adj_matrix_last = torch.FloatTensor(adj.todense()).cuda()
            # for i in range(self.args["GNN_layer"]):
            #     adj_matrix_last = torch.mm(adj_matrix_last,adj_matrix).cuda()
            # features = self.data.x.cuda()
            # features_last = np.array(torch.mm(adj_matrix_last,features).cpu())
            # adj_matrix_last = np.array(adj_matrix_last.cpu())

    def cal_similarity(self,vectors,unleaning_nodes,isfeature):
        # vectors = torch.FloatTensor(vectors)
        # similarity_matrix = np.zeros((self.num_node,self.num_node))
        # # similarity_matrix = torch.FloatTensor(self.num_node,self.num_node)
        # for i in range(self.num_node-1):
        #     for j in range(i+1,self.num_node):
        #         similarity_matrix[i][j] = cal_distance(vectors[i,:],vectors[j,:])
        #         similarity_matrix[j][i] = similarity_matrix[i][j]
        if self.args["base_model"] == "SIGN" and isfeature:
            vectors = self.target_model.model.get_features(vectors)

        if isinstance(vectors, np.ndarray):
            vectors = torch.FloatTensor(vectors)
        unlearning_vector = vectors[unleaning_nodes,:]
        unlearning_vector = F.normalize(unlearning_vector, p=2, dim=1).clone().detach().float()
        vectors = F.normalize(vectors, p=2, dim=1).clone().detach().float()
        # similarity_matrix = torch.matmul(unlearning_vector, vectors.T)
        # similarity_matrix = torch.sum(torch.matmul(unlearning_vector, vectors.T),dim=0)
        similarity_matrix = self.compute_similarity_in_chunks(unlearning_vector, vectors, 10000)

        return similarity_matrix
    
    def compute_similarity_in_chunks(self,unlearning_vector, vectors, chunk_size):
        num_vectors = vectors.size(0)
        similarity_matrix = torch.zeros(num_vectors, device=unlearning_vector.device)

        # Iterate through the vectors in chunks
        for start in range(0, num_vectors, chunk_size):
            end = min(start + chunk_size, num_vectors)
            chunk = vectors[start:end]
            
            # Compute the chunk of the similarity matrix
            similarity_chunk = torch.matmul(unlearning_vector, chunk.T)
            
            # Sum the results along the dimension
            similarity_chunk_sum = torch.sum(similarity_chunk, dim=0)
            
            # Store the results in the corresponding part of the similarity matrix
            similarity_matrix[start:end] = similarity_chunk_sum

        return similarity_matrix

    def activate_nodes(self):
        activated_node  = list()
        total_influence = torch.zeros(self.num_node)
        self.influence_score[self.unlearning_nodes] = 0
        # influence_mask = torch.zeros(self.num_node,dtype=torch.bool)
        # influence_mask[self.data.train_indices] = True
        # influence_mask[self.unlearning_nodes] = False
        # for i in range(self.args["num_unlearned_nodes"]):
        #     self.influence_score[i, ~influence_mask] = 0
        #     node_influence_score = self.influence_score[i,:]
        #     #compute the influence by all the unlearning node
        #     total_influence+= node_influence_score.cpu()

        max_score,max_node,count = 0, 0, 0
        # topk_val,activated_node = torch.topk(total_influence,self.Budget)
        topk_val,activated_node = torch.topk(self.influence_score,self.Budget)
        return np.array(activated_node.cpu(),dtype=int)

    def pos_sampling(self, activated_nodes,activated_labels,unlearning_nodes):
        # pos_pair = {}
        # count = 0
        # number = 0
        # for node in activated_nodes:
        #     number = 0
        #     pos_pair[node] = []
        #     labels = self.data.y[self.data.train_mask].cpu().numpy()
        #     indice = np.where(labels == activated_labels[count])
        #     np.random.shuffle(indice[0])
        #     count += 1
        #     if indice == None:
        #         pos_pair[node].append(numpy.zeros_like(self.original_emb[0]))
        #     for index in indice[0]:
        #         if index not in unlearning_nodes and index not in activated_nodes:
        #             pos_pair[node].append(self.original_emb[index].cpu().numpy())
        #             number += 1
        #             if number >= 5:
        #                 break
        #     if pos_pair[node] == []:
        #         pos_pair[node].append(numpy.zeros_like(self.original_emb[0].cpu()))
        #     pos_pair[node] = np.mean(pos_pair[node],axis=0)
        pos_pair = {}
        labels = self.data.y[self.data.train_mask].cpu().numpy()  # 提前将labels转为numpy数组
        unlearning_set = set(unlearning_nodes)  # 转为集合加速查找
        activated_set = set(activated_nodes)  # 转为集合加速查找

        for count, node in enumerate(activated_nodes):
            # if count % 10000 == 0:
                # print("count!{}".format(count))
            pos_pair[node] = []
            indice = np.where(labels == activated_labels[count])[0]  # 获取索引并直接使用数组
            np.random.shuffle(indice)  # 打乱索引
            number = 0
            embeddings = []
            for index in indice:
                if index not in unlearning_set and index not in activated_set:
                    embeddings.append(self.original_emb[index].cpu().numpy())
                    number += 1
                    if number >= 5:
                        break

            if not embeddings:
                pos_pair[node].append(np.zeros_like(self.original_emb[0].cpu()))
            else:
                pos_pair[node] = np.mean(embeddings, axis=0)
        pos_pair = {k: np.array(v) for k, v in pos_pair.items()}
            


        return pos_pair

    def neg_sampling(self, activated_nodes, activated_labels, unlearning_nodes):
        # neg_pair = {}
        # count = 0
        # for node in activated_nodes:
        #     number = 1
        #     neg_pair[node] = []
        #     for i in range(5):
        #         neg_pair[node].append(self.original_emb[node].cpu().numpy())
        #     count = 5
        #     labels = self.data.y[activated_nodes].cpu().numpy()
        #     indice = np.where(labels == activated_labels[count])
        #     np.random.shuffle(indice[0])
        #     if indice == None:
        #         continue
        #     for index in indice[0]:
        #         if index not in unlearning_nodes:
        #             neg_pair[node].append(self.original_emb[index].cpu().numpy())
        #             number += 1
        #             if number >= 10:
        #                 break
        #     neg_pair[node] = np.mean(neg_pair[node],axis=0)
        neg_pair = {}
        labels = self.data.y[activated_nodes].cpu().numpy()  # 提前将labels转为numpy数组
        unlearning_set = set(unlearning_nodes)  # 转为集合加速查找

        for count, node in enumerate(activated_nodes):
            # if count % 10000 == 0:
            #     print("count!{}".format(count))
            neg_pair[node] = []
            embeddings = []

            # 添加当前节点的embedding 5次
            current_emb = self.original_emb[node].cpu().numpy()
            embeddings.extend([current_emb] * 5)

            # 获取符合条件的节点索引
            indice = np.where(labels == activated_labels[count])[0]
            np.random.shuffle(indice)  # 打乱索引

            number = 5
            for index in indice:
                if index not in unlearning_set:
                    embeddings.append(self.original_emb[index].cpu().numpy())
                    number += 1
                    if number >= 10:
                        break

            # 计算均值
            neg_pair[node] = np.mean(embeddings, axis=0)
            
        return neg_pair
    #5个自身向量，5个负样本

    def delete_node(self):
        self.edge_mask = torch.ones(self.data.edge_index.shape[1], dtype=torch.bool)
        for node in self.unlearning_nodes:
            self.edge_mask[self.data.edge_index[0] == node] = False
            self.edge_mask[self.data.edge_index[1] == node] = False

    def retrain(self, unlearning_nodes, edge_mask):
        self.target_model.data.edge_index = self.target_model.data.edge_index[:,edge_mask]
        self.target_model.train()
        edge_mask = True
        # F1 = self.target_model.eval_unlearning(unlearning_nodes,edge_mask)
        # self.logger.info('unlearning F1_score : {}'.format(F1))

    def mia_attack(self):

        self.mia_num = self.unlearning_num
        original_softlabels_member = self.original_softlabels[self.unlearning_nodes]
        original_softlabels_non = self.original_softlabels[self.data.test_indices[:self.mia_num]]
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args[
            "base_model"] == "SIGN":
            unlearning_softlabels_member = self.target_model.model.get_softlabel(self.features[self.unlearning_nodes])
            unlearning_softlabels_non = self.target_model.model.get_softlabel(
                self.features[self.data.test_indices[:self.mia_num]])
        else:
            unlearning_softlabels_member = self.target_model.model.get_softlabel(self.data.x,self.data.edge_index)[self.unlearning_nodes]
            unlearning_softlabels_non = self.target_model.model.get_softlabel(
                self.data.x,self.data.edge_index)[self.data.test_indices[:self.mia_num]]

        mia_test_y = torch.cat((torch.ones(self.mia_num), torch.zeros(self.mia_num)))
        posterior1 = torch.cat((original_softlabels_member, original_softlabels_non), 0).cpu().detach()
        posterior2 = torch.cat((unlearning_softlabels_member, unlearning_softlabels_non), 0).cpu().detach()
        posterior = np.array([np.linalg.norm(posterior1[i]-posterior2[i]) for i in range(len(posterior1))])
        # self.logger.info("posterior:{}".format(posterior))
        auc = roc_auc_score(mia_test_y, posterior.reshape(-1, 1))
        self.average_auc[self.run] = auc
        # self.logger.info("auc:{}".format(auc))
        # self.plot_auc(mia_test_y, posterior.reshape(-1, 1))
        return auc

    def SGU_unlearning(self):
        self.target_model.model.train()
        self.avg_training_time[self.run] = 0
        self.lam = 1
        self.tau = 0.5
        self.para1 = self.args["para1"]
        self.para2 = self.args["para2"]
        self.para3 = self.args["para3"]
        self.para4 = self.args["para4"]
        self.para5 = self.args["para5"]
        self.target_model.model = self.target_model.model.to(self.device)
        self.target_model.data = self.target_model.data.to(self.device)
        prototype_embedding = self.prototype_embedding.to(self.device)
        self.target_model.optimizer = torch.optim.Adam(self.target_model.model.parameters(), lr=self.target_model.model.config.lr,
                                          weight_decay=self.target_model.model.config.decay)

        indices = torch.randperm(self.data.y[self.unlearning_nodes].size(0))

        # 使用这些索引重新排列原始张量
        random_class = self.data.y[self.unlearning_nodes][indices]
        random_emb_proto = prototype_embedding[random_class]
        average_probs = torch.ones(self.data.num_classes) / self.data.num_classes
        stacked_probs = average_probs.repeat(self.args["num_unlearned_nodes"], 1).detach()
        best = 0
        best_w = 0
        F1_score = 0
        F1_score,Accuracy,Recall = self.target_model.test_node_fullbatch(self.features[self.data.test_indices])
        self.logger.info("Original F1 Score: {:.4f} ".format(F1_score) )
        for epoch in tqdm(range(self.args['unlearning_epochs']), desc="Unlearning", unit="epoch"):
            self.target_model.model.train()
            self.target_model.optimizer.zero_grad()


            ###get emb softlabel###
            # softlabels_U = F.softmax(self.model(features[unlearning_nodes]),dim=1)
            # # softlabels_U = self.model.get_softlabel(features[unlearning_nodes])
            # softlabels_E = F.softmax(self.model(features_unlearning[activated_nodes]),dim=1)
            # embedding_E = self.model.get_embedding(features_unlearning[activated_nodes])
            # embedding_U = self.model.get_embedding(features[unlearning_nodes])

            ## 3.25 19-16
            # softlabels_U = F.softmax(self.model(features[unlearning_nodes]),dim=1)
            start_time = time.time()
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args[
                "base_model"] == "SIGN":
                softlabels_U = self.target_model.model.get_softlabel(self.features[self.unlearning_nodes])
                softlabels_E = F.softmax(self.target_model.model(self.features[self.activated_nodes]),dim=1)
                embedding_E = self.target_model.model.get_embedding(self.features[self.activated_nodes])
                embedding_U = self.target_model.model.get_embedding(self.features[self.unlearning_nodes])
            else:
                softlabels_U = self.target_model.model.get_softlabel(self.data.x,self.data.edge_index)[self.unlearning_nodes]
                softlabels_E = self.target_model.model.get_softlabel(self.data.x,self.data.edge_index)[self.activated_nodes]
                embedding_E = self.target_model.model.get_embedding(self.data.x,self.data.edge_index)[self.activated_nodes]
                embedding_U = self.target_model.model.get_embedding(self.data.x,self.data.edge_index)[self.unlearning_nodes]
            w_U = []
            ### cal loss###
            loss_w = 0
            for param_tensor in self.target_model.model.parameters():
                param_clone = param_tensor
                w_U.append(param_tensor)
            for i in range(len(self.original_w)):
                delta_w = (w_U[i] - self.original_w[i])
                loss_w += torch.norm(delta_w)
            creterion_MSE = torch.nn.MSELoss(reduction="mean")
            # loss_pE = creterion_MSE(softlabels_E,original_softlabels[activated_nodes])
            smooth_factor = 1e-9
            loss_pE = F.kl_div(torch.log(softlabels_E + smooth_factor),self.original_softlabels[self.activated_nodes] + smooth_factor, reduction='batchmean')
            pos_tensors = [torch.tensor(self.pos_pair[node]) for node in self.activated_nodes]
            positive_tensors = torch.stack([F.normalize(pos_tensor, p=2, dim=0) for pos_tensor in pos_tensors], dim=0).cuda()
            pos_scores = torch.exp(torch.einsum('ij,ij->i', F.normalize(embedding_E, p=2, dim=1),
                                                positive_tensors )/ self.tau)
            neg_scores = torch.zeros_like(pos_scores)

            ####6/1#########
            neg_tensors = [torch.tensor(self.neg_pair[node]) for node in self.activated_nodes]
            negtive_tensors = torch.stack([F.normalize(negtive_tensor, p=2, dim=0) for negtive_tensor in neg_tensors],
                                           dim=0).cuda()
            neg_scores = torch.exp(torch.einsum('ij,ij->i', F.normalize(embedding_E, p=2, dim=1),
                                                negtive_tensors) / self.tau)

            ################
            # for i, node in enumerate(activated_nodes):
            #     # neg_tensors = F.normalize(torch.tensor(neg_pair[node][0]), p=2, dim=0).cuda()
            #     # tmp_emb = F.normalize(embedding_E[i], p=2, dim=0)
            #     # neg_scores = 10 * torch.dot(neg_tensors,tmp_emb)
            #
            #     neg_tensors = [torch.tensor(neg_emb) for neg_emb in neg_pair[node]]
            #     negtive_tensors = torch.stack([F.normalize(neg_tensor, p=2, dim=0) for neg_tensor in neg_tensors], dim=0).cuda()
            #     neg_scores[i] = torch.exp(torch.einsum('d,nd->n', F.normalize(embedding_E[i], p=2, dim=0),
            #                      negtive_tensors) / self.tau).sum()
            loss_hE = -torch.log(pos_scores /50*neg_scores).sum()
             


            embedding_E_proto = prototype_embedding[self.data.y[self.activated_nodes]]
            loss_proto = creterion_MSE(embedding_E,embedding_E_proto)
            # loss_proto = F.kl_div(torch.log(embedding_E),embedding_E_proto, reduction='batchmean')
            # for node in activated_nodes:
            #     emb = embedding_E[node]
            #     pos_num = torch.exp(torch.mul(F.normalize(emb, p=2, dim=0),F.normalize(torch.from_numpy(pos_pair[node]).to(self.device), p=2, dim=0)).sum()/self.tau)
            #     neg_num = 0
            #     for neg_emb in neg_pair[node]:
            #         neg_num += torch.exp(torch.mul(F.normalize(emb, p=2, dim=0),F.normalize(torch.from_numpy(neg_emb).to(self.device), p=2, dim=0)).sum()/self.tau)
            #     loss_hE += -torch.log(pos_num/neg_num)

            #尝试用随机标签的方式遗忘
            loss_pU = F.cross_entropy(softlabels_U, random_class.to(self.device))

            #尝试用平均概率的方式遗忘
            # loss_pU = F.kl_div(torch.log(softlabels_U+smooth_factor),stacked_probs.to(self.device), reduction='batchmean')
            loss_emb_U = creterion_MSE(embedding_U, random_emb_proto)
            # loss_emb_U = 0
            # onehot = F.one_hot(self.data.y[unlearning_nodes]).detach()

            loss = ( self.para1 * loss_w +  self.para3 * loss_pE ) + (self.para2 * loss_hE +  self.para4 * (loss_pU+ loss_emb_U)  + self.para5 * loss_proto)
            # loss = self.lam * ( self.para3 * loss_pE ) + (self.para2 * loss_hE +  self.para4 * (loss_pU+ loss_emb_U)  )
            # loss = self.lam * (self.para1 * loss_w + self.para3 * loss_pE + self.para5 * loss_proto) + (
            #             self.para2 * loss_hE + self.para4 * (loss_pU + loss_emb_U))

            # self.logger.info("loss_w: {}  loss_hE: {} loss_pE: {} loss_pU: {} ".format(self.para1*loss_w,
            #                                                                                         self.para2 * loss_hE,
            #                                                                                         self.para3 * loss_pE,
            #                                                                                         self.para4* (loss_pU+ loss_emb_U)))
            loss.backward()
            if (epoch+1) % self.args["test_freq"] == 0:
                F1_score,Accuracy,Recall = self.target_model.test_node_fullbatch(self.features[self.data.test_indices])
                self.logger.info("Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}".format(epoch, F1_score, loss) )
            
            self.target_model.optimizer.step()
            self.avg_training_time[self.run] += (time.time() - start_time)/self.args["unlearning_epochs"]

            ##test##
            # if (epoch+1) % self.args["test_freq"] == 0:
            #     F1_score,Accuracy,Recall = self.evaluate_SGU_model(features[self.data.test_indices])
            #     self.logger.info('epoch: {}  F1_score = {}  Accuracy = {}  Recall = {}'.format(epoch, F1_score,Accuracy,Recall))
            if F1_score > best and epoch > 30:
                best = F1_score
                best_w = copy.deepcopy(self.target_model.model.state_dict())
                # F1_score,Accuracy,Recall = self.target_model.eval_unlearning(self.features,self.unlearning_nodes)
                # self.logger.info('Unlearning: F1_score = {}  Accuracy = {}  Recall = {}'.format(F1_score,Accuracy,Recall))
        # F1_score, Accuracy, Recall = self.target_model.eval_unlearning(self.features,self.unlearning_nodes)
        self.logger.info("Parameters - para1: {:.4f} | para2: {:.4f} | para3: {:.4f} | para4: {:.4f} | para5: {:.4f}".format(self.para1, self.para2, self.para3, self.para4, self.para5))

        self.logger.info('Best Unlearning: F1_score: {:.4f}'.format(best))
        self.average_f1[self.run] = best
        
        save_path = root_path + "/data/model/node_level/"+self.args["dataset_name"]+ "/" + self.args["base_model"]+"_unlearning_best.pt"
        with open(save_path,'w') as file:
            self.target_model.save_model(save_path,best_w)

        return best

    def get_prototype(self):
        train_indices = torch.tensor(self.data.train_indices,requires_grad=False)
        prototype_mask = torch.ones_like(train_indices, dtype=torch.bool)
        u_nodes = torch.from_numpy(self.unlearning_nodes)
        a_nodes = torch.from_numpy(self.activated_nodes)
        prototype_mask[torch.isin(train_indices, torch.cat((u_nodes,a_nodes)))] = False
        prototype_indices = train_indices[prototype_mask]
        tmp_emb = self.original_emb[prototype_indices]
        tmp_y = self.data.y[prototype_indices].cpu()
        unique_labels = np.unique(tmp_y)
        # 初始化一个数组用于存储每个类别的平均嵌入向量
        class2embeddings = torch.zeros((self.data.num_classes, tmp_emb.shape[1]),requires_grad=False)


        # 遍历每个类别
        for label in unique_labels:
            # 获取属于当前类别的样本索引
            indices = np.where(tmp_y == label)[0]
            # 获取属于当前类别的嵌入向量
            class_emb = tmp_emb[indices]
            # 计算当前类别的平均嵌入向量
            class_avg_emb = torch.mean(class_emb, dim=0)
            class2embeddings[label.item()] = class_avg_emb

        return class2embeddings

    def plot_auc(self,y_true,y_score):
        y_true = y_true
        y_score = y_score

        # 计算ROC曲线上的点
        fpr, tpr, thresholds = roc_curve(y_true, y_score)

        # 计算AUC
        roc_auc = auc(fpr, tpr)

        # 绘制ROC曲线
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.5f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.show()



    def edge_unlearning(self):
        #add heterophilous_edges

        self.adj = self.data.adj
        self.adj_sp = self.adj.tocoo()
        self.adj_torch = utils.sparse_mx_to_torch_sparse_tensor(self.adj_sp)
        self.adj_norm_sp = utils.aug_normalized_adjacency(self.adj)
        self.adj_norm_torch = utils.sparse_mx_to_torch_sparse_tensor(self.adj_norm_sp)
        degree_torch = torch.sparse.sum(self.adj_torch, dim=0).values()
        self.deg = np.array(degree_torch)

        #find the initailly activated nodes
        # rand = torch.randint(high=self.data.edge_index.size(1),size=(self.args["num_unlearned_edges"],))
        # remove_edge = self.data.edge_index[:,rand]
        if os.path.exists(root_path + "/data/SGU/unlearning_edge.pt"):
            remove_edge = torch.load(root_path+ "/data/SGU/unlearning_edge.pt")
            updated_edge_index = torch.hstack([self.data.edge_index, remove_edge])
        else:
            remove_edge,updated_edge_index = self.generate_heterophilous_edges(self.data.edge_index,self.data.num_node,self.args["proportion_unlearned_edges_num"])
            torch.save(remove_edge,root_path + "/data/SGU/unlearning_edge.pt")

        self.data.edge_index = updated_edge_index
        self.unlearning_nodes = np.union1d(remove_edge[0],remove_edge[1])
        self.logger.info("add edges:{}".format(remove_edge.size(1)))



        #cal the influence score
        self.node_cnt_sum = torch.zeros(self.data.num_nodes,requires_grad=False)
        self.adj_lil = self.adj_sp.tolil()
        self.adj_norm_lil = self.adj_norm_sp.tolil()
        self.node_degree = torch.sparse.sum(self.adj_torch.to(self.device), [0]).to_dense().cpu().numpy()
        node_cnt = np.array(self.adj_norm_lil[self.unlearning_nodes].tocsr().max(axis=0).todense()).flatten()
        self.degree_heap = []
        for i in self.unlearning_nodes:
            node_cnt[i] = 1
            heapq.heappush(self.degree_heap, (self.node_degree[i], i))

        self.__prep_cnt_sum(self.node_cnt_sum, node_cnt, self.adj_norm_sp.row, self.adj_norm_sp.col,
                            self.adj_norm_sp.data)

        self.activated_nodes = torch.topk(self.node_cnt_sum, self.Budget)[1].numpy()

        self.features = self.preprocess_feature()
        # self.target_model = NodeClassifier(self.args, self.data, self.model_zoo, self.logger)
        self.target_model = get_trainer(self.args,self.logger,self.model,self.data)
        self.target_model.data.pre_features = self.features
        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + \
                         self.args["base_model"] + self.args["proportion_unlearned_edges"]
        if os.path.exists(model_path):
            print(f"File {model_path} already exists.")
            self.target_model.load_model(model_path)
        else:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            with open(model_path, 'w'):
                print(f"File {model_path} created successfully.")
                self.target_model.train()

        ##############train################

        self.softlabels = self.target_model.model.get_softlabel(self.features.cuda()).cpu().detach().numpy()

        # get frozen model param
        self.original_emb = self.target_model.model.get_embedding(self.features).clone().detach().float()
        self.original_softlabels = self.target_model.model.get_softlabel(
            self.features).clone().detach().float()
        parameter_list = []
        for param_tensor in self.target_model.model.parameters():
            param_clone = param_tensor.clone().detach().float()
            parameter_list.append(param_clone)
        self.original_w = parameter_list

        # get prototype embedding
        self.prototype_embedding = self.get_prototype()
        pred = self.target_model.model.emb2softlable(
            self.prototype_embedding.to(self.device)).cpu().detach().numpy()
        pred = np.argmax(pred, axis=1)
        self.logger.info(
            "proto_acc:{}".format(accuracy_score(y_true=np.arange(0, self.data.num_classes), y_pred=pred)))

        # contrastive learning sampling
        activated_label = np.argmax(self.original_softlabels[self.activated_nodes].cpu().numpy(), axis=1)
        self.pos_pair = self.pos_sampling(self.activated_nodes, activated_label, self.unlearning_nodes)
        self.neg_pair = self.neg_sampling(self.activated_nodes, activated_label, self.unlearning_nodes)



        self.target_model.SGU_unlearning_edge(self.original_softlabels,
                                                self.original_w,
                                                self.unlearning_nodes,
                                                self.activated_nodes,
                                                self.pos_pair,
                                                self.neg_pair,
                                                self.features,
                                                self.prototype_embedding,
                                                remove_edge)











    def __prep_cnt_sum(self,node_cnt_sum, K_arr, row, col, data):
        non_zero_indices = np.where(K_arr > 0)[0]

        # 广播non_zero_indices到row数组的形状，然后比较是否相等
        # 这样会自动对每个元素进行比较，而不需要显式的循环
        mask = np.isin(row, non_zero_indices)

        tx_values = np.where(mask)[0]

        for tx in prange(tx_values[0]):
            if node_cnt_sum[col[tx]] < K_arr[row[tx]] * data[tx]:
                node_cnt_sum[col[tx]] = K_arr[row[tx]] * data[tx]

    def generate_heterophilous_edges(self,edge_index, node_num, proportion):
        """
        生成异配性的边并更新edge_index。

        参数:
        edge_index (np.array): 形状为 (2, E) 的数组，其中E是边的数量，每一列代表一对节点索引。
        node_num (int): 图中节点的总数。
        proportion (float): 需要生成的异配性边的比例，相对于全连接图的边数量。

        返回:
        np.array: 更新后的edge_index，包含新的异配性边。
        """

        # 计算全连接图的边数量
        full_connected_edges = node_num * (node_num - 1) // 2

        # 根据比例计算需要生成的异配性边的数量
        num_heterophilous_edges = int(full_connected_edges * proportion)

        heterophilous_edges = []
        for _ in range(num_heterophilous_edges):
            # 随机选择两个不同类别的节点
            node1 = np.random.choice(node_num)
            while True:
                node2 = np.random.choice(node_num)
                if self.data.y[node1] != self.data.y[node2] and node1 != node2:
                    break
            heterophilous_edges.append((node1, node2))

        # 将新的异配性边添加到现有的edge_index中
        heterophilous_edges_array = torch.tensor(heterophilous_edges,requires_grad=False).T
        heterophilous_edges_array = to_undirected(heterophilous_edges_array)
        updated_edge_index = torch.hstack([edge_index, heterophilous_edges_array])

        return heterophilous_edges_array, updated_edge_index


    def print_time(self):
        for key,value in self.timecount.items():
            if key == "training_time":
                value = value/self.args["unlearning_epochs"]
            self.logger.info("{} : {}s".format(key,value))

        

    















