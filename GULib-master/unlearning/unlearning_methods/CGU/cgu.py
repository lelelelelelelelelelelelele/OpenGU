from __future__ import print_function
import argparse
import math
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from matplotlib import pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, auc
from torchvision import datasets, transforms
import argparse
import os
from sklearn.linear_model import LogisticRegression
import pickle
# Below is for graph learning part
from torch_geometric.nn.conv import MessagePassing
from typing import Optional

from torch import Tensor
from torch_geometric.nn.dense.linear import Linear
from torch_geometric.typing import Adj, OptTensor
from torch_geometric.utils import degree

from torch_scatter import scatter_add
from torch_sparse import SparseTensor, fill_diag, matmul, mul
from torch_sparse import sum as sparsesum

from torch_geometric.typing import Adj, OptTensor, PairTensor
from torch_geometric.utils import add_remaining_self_loops
from torch_geometric.utils.num_nodes import maybe_num_nodes

from torch_geometric.datasets import Planetoid, Coauthor, Amazon, CitationFull
from ogb.nodeproppred import PygNodePropPredDataset
import torch_geometric.transforms as T
import os.path as osp

from torch.nn import init
from utils.utils import *

from sklearn import preprocessing
from numpy.linalg import norm
from config import root_path,unlearning_path
from config import BLUE_COLOR,RESET_COLOR


def plot_auc( y_true, y_score):
    y_true = y_true
    y_score = y_score

    # 计算ROC曲线上的点
    fpr, tpr, thresholds = roc_curve(y_true, y_score)

    # 计算AUC
    roc_auc = auc(fpr, tpr)

    # 绘制ROC曲线
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()

class cgu():
    def __init__(self,logger,args,model_zoo):
        self.logger = logger
        self.run = 0
        self.args = args
        self.model_zoo = model_zoo
        self.data = self.model_zoo.data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        num_runs = self.args["num_runs"]
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_training_time = np.zeros(num_runs)
        assert self.args["base_model"] == 'SGC'

    def run_exp(self):
        self.CGU_Unlearning(self.args)
        self.logger.info(
        "{}Performance Metrics:\n"
        " - Average F1 Score: {:.4f} ± {:.4f}\n"
        " - Average AUC Score: {:.4f} ± {:.4f}\n"
        " - Average Unlearning Time: {:.4f} ± {:.4f} seconds\n".format(
            BLUE_COLOR,
            np.mean(self.average_f1), np.std(self.average_f1),
            np.mean(self.average_auc), np.std(self.average_auc),
            np.mean(self.avg_training_time), np.std(self.avg_training_time),
            RESET_COLOR
            )
        )


    def CGU_Unlearning(self,args):

        self.logger.info('='*10 + 'Loading data' + '='*10)
        self.logger.info('Dataset:{}'.format( self.args["dataset_name"]))

        self.data = self.data.to(device)
        self.args["num_unlearned_nodes"] = int(self.data.num_nodes * self.args["unlearn_ratio"])
        self.nonmember_id = self.data.test_indices[:self.args["num_unlearned_nodes"]]
        # save the degree of each node for later use
        row = self.data.edge_index[0]
        deg = degree(row)

        
        # process features
        if self.args["featNorm"]:
            X = preprocess_data(self.data.x).to(device)
        else:
            X = self.data.x.to(device)
        # save a copy of X for removal
        X_scaled_copy_guo = X.clone().detach().float()

        # process labels
        if self.args["train_mode"] == 'binary':
            if '+' in self.args["Y_binary"]:
                # two classes are specified
                class1 = int(self.args["Y_binary"].split('+')[0])
                class2 = int(self.args["Y_binary"].split('+')[1])
                Y = self.data.y.clone().detach().float()
                Y[self.data.y == class1] = 1
                Y[self.data.y == class2] = -1
                interested_data_mask = (self.data.y == class1) + (self.data.y == class2)
                train_mask = self.data.train_mask * interested_data_mask
                val_mask = self.data.val_mask * interested_data_mask
                test_mask = self.data.test_mask * interested_data_mask
                self.data.Y = Y
            else:
                # one vs rest
                class1 = int(self.args["Y_binary"])
                Y = self.data.y.clone().detach().float()
                Y[self.data.y == class1] = 1
                Y[self.data.y != class1] = -1
                train_mask = self.data.train_mask
                val_mask = self.data.val_mask
                test_mask = self.data.test_mask
            y_train, y_val, y_test = Y[train_mask].to(device), Y[val_mask].to(device), Y[test_mask].to(device)
            self.data.Y = Y.to(device)
        else:
            # multiclass classification
            train_mask = self.data.train_mask
            val_mask = self.data.val_mask
            test_mask = self.data.test_mask
            y_train = F.one_hot(self.data.y[self.data.train_mask]) * 2 - 1
            y_train = y_train.float().to(device)
            y_val = self.data.y[self.data.val_mask].to(device)
            y_test = self.data.y[self.data.test_mask].to(device)
            self.data.Y = (F.one_hot(self.data.y)* 2 - 1)
            self.data.Y = self.data.Y.float().to(device)


        assert self.args["noise_mode"] == 'data'

        if self.args["compare_gnorm"]:
            # if we want to compare the residual gradient norm of three cases, we should not add noise
            # and make budget very large
            b_std = 0
        else:
            if self.args["noise_mode"] == 'data':
                b_std = self.args["std"]
            elif self.args["noise_mode"] == 'worst':
                b_std = self.args["std"]  # change to worst case sigma
            else:
                raise("Error: Not supported noise model.")

        #############
        # initial training with graph
        self.logger.info('='*10 + 'Training on full dataset with graph' + '='*10)
        start = time.time()
        Propagation = MyGraphConv(K=self.args["GNN_layer"], add_self_loops=self.args["add_self_loops"],
                                  alpha=self.args["alpha"], XdegNorm=self.args["XdegNorm"], GPR=self.args["GPR"]).to(device)

        if self.args["GNN_layer"] > 0:
            X = Propagation(X, self.data.edge_index)

        X = X.float()
        X_train = X[train_mask].to(device)
        X_val = X[val_mask].to(device)
        X_test = X[test_mask].to(device)

        self.logger.info("Train node:{}, Val node:{}, Test node:{}, Edges:{}, Feature dim:{}".format(X_train.shape[0], X_val.shape[0],
                                                                                          X_test.shape[0],
                                                                                          self.data.edge_index.shape[1],
                                                                                          X_train.shape[1]))
        ############
        # train removal-enabled linear model
        self.logger.info("With graph, train mode:{}, optimizer:{}".format( self.args["train_mode"], self.args["optimizer"]))

        # reserved for future extension
        weight = None
        # in our case weight should always be None
        assert weight is None
        # record the optimal gradient norm wrt the whole training set
        opt_grad_norm = 0

        if self.args["train_mode"] == 'ovr':
            b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
            if self.args["train_sep"]:
                # train K binary LR models separately
                w = torch.zeros(b.size()).float().to(device)
                for k in range(y_train.size(1)):
                    if weight is None:
                        w[:, k] = lr_optimize(X_train, y_train[:, k], self.args["lam"], b=b[:, k], num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                    else:
                        w[:, k] = lr_optimize(X_train[weight[:, k].gt(0)], y_train[:, k][weight[:, k].gt(0)], self.args["lam"],
                                              b=b[:, k], num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
            else:
                # train K binary LR models jointly
                w = ovr_lr_optimize(X_train, y_train, self.args["lam"], weight, b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                    opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
            # record the opt_grad_norm
            for k in range(y_train.size(1)):
                opt_grad_norm += lr_grad(w[:, k], X_train, y_train[:, k], self.args["lam"]).norm().cpu()
        else:
            b = b_std * torch.randn(X_train.size(1)).float().to(device)
            w = lr_optimize(X_train, y_train, self.args["lam"], weight, b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                    opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
            opt_grad_norm = lr_grad(w, X_train, y_train, self.args["lam"]).norm().cpu()

        self.logger.info('Time elapsed: %.6fs' % (time.time() - start))
        if self.args["train_mode"] == 'ovr':
            self.logger.info('Val accuracy = %.4f F1 = %.4f Recall = %.4f' % ovr_lr_eval(w, X_val, y_val))
            self.logger.info('Test accuracy = %.4f F1 = %.4f Recall = %.4f' % ovr_lr_eval(w, X_test, y_test))
        else:
            self.logger.info('Val accuracy = %.4f' % lr_eval(w, X_val, y_val))
            self.logger.info('Test accuracy = %.4f' % lr_eval(w, X_test, y_test))

        ###########
        if self.args["unlearn_task"] == 'node' or self.args["unlearn_task"] == 'feature':
            if self.args["compare_guo"]:
                # initial training without graph
                self.logger.info('='*10 + 'Training on full dataset without graph' + '='*10)
                start = time.time()

                # only the data preparation part is different
                X_train = X_scaled_copy_guo[train_mask].to(device)
                X_val = X_scaled_copy_guo[val_mask].to(device)
                X_test = X_scaled_copy_guo[test_mask].to(device)

                self.logger.info("Train node:{}, Val node:{}, Test node:{}, Feature dim:{}".format(X_train.shape[0], X_val.shape[0],
                                                                                        X_test.shape[0], X_train.shape[1]))
                ######
                # train removal-enabled linear model without graph
                self.logger.info("Without graph, train mode:", self.args["train_mode"], ", optimizer:", self.args["optimizer"])
                weight = None
                # in our case weight should always be None
                assert weight is None
                opt_grad_norm_guo = 0

                if self.args["train_mode"] == 'ovr':
                    b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
                    if self.args["train_sep"]:
                        # train K binary LR models separately
                        w_guo = torch.zeros(b.size()).float().to(device)
                        for k in range(y_train.size(1)):
                            if weight is None:
                                w_guo[:, k] = lr_optimize(X_train, y_train[:, k], self.args["lam"], b=b[:, k], num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])

                            else:
                                w_guo[:, k] = lr_optimize(X_train[weight[:, k].gt(0)], y_train[:, k][weight[:, k].gt(0)], self.args["lam"],
                                              b=b[:, k], num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                    else:
                        # train K binary LR models jointly
                        w_guo = ovr_lr_optimize(X_train, y_train, self.args["lam"], weight, b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                    opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                    # record the opt_grad_norm
                    for k in range(y_train.size(1)):
                        opt_grad_norm_guo += lr_grad(w_guo[:, k], X_train, y_train[:, k],self.args["lam"]).norm().cpu()
                else:
                    b = b_std * torch.randn(X_train.size(1)).float().to(device)
                    w_guo = lr_optimize(X_train, y_train,self.args["lam"], b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"], opt_choice=self.args["optimizer"],
                                        lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                    opt_grad_norm_guo = lr_grad(w_guo, X_train, y_train, self.args["lam"]).norm().cpu()

                self.logger.info('Time elapsed: %.2fs' % (time.time() - start))
                if self.args["train_mode"] == 'ovr':
                    self.logger.info('Val accuracy = %.4f F1 = %.4f Recall = %.4f' % ovr_lr_eval(w_guo, X_val, y_val))
                    self.logger.info('Test accuracy = %.4f F1 = %.4f Recall = %.4f' % ovr_lr_eval(w_guo, X_test, y_test))
                else:
                    self.logger.info('Val accuracy = %.4f' % lr_eval(w_guo, X_val, y_val))
                    self.logger.info('Test accuracy = %.4f' % lr_eval(w_guo, X_test, y_test))


        ###########
        # budget for removal
        c_val = get_c(self.args["delta"])
        # if we need to compute the norms, we should not retrain at all
        if self.args["compare_gnorm"]:
            budget = 1e5
        else:
            if self.args["train_mode"] == 'ovr':
                budget = get_budget(b_std, self.args["eps"], c_val) * y_train.size(1)
            else:
                budget = get_budget(b_std, self.args["eps"], c_val)
        gamma = 1/4  # pre-computed for -logsigmoid loss
        self.logger.info('Budget:{}'.format(budget) )

        ##########
        # our removal
        # all norm here is NOT accumulated, need to use np.cumsum in plots
        grad_norm_approx = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()
        removal_times = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # record the time of each removal
        acc_removal = torch.zeros((3, self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # record the acc after removal, 0 for val, 1 for test
        grad_norm_worst = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # worst case norm bound
        grad_norm_real = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # true norm
        # graph retrain
        removal_times_graph_retrain = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()
        acc_graph_retrain = torch.zeros((2, self.args["num_unlearned_nodes"], self.args["num_runs"])).float()
        if  self.args["unlearn_task"] == 'node' or self.args["unlearn_task"] == 'feature':
            # guo removal
            grad_norm_approx_guo = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()
            removal_times_guo = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # record the time of each removal
            acc_guo = torch.zeros((2, self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # first row for val acc, second row for test acc
            grad_norm_real_guo = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # true norm
            # guo retrain
            removal_times_guo_retrain = torch.zeros((self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # record the time of each removal
            acc_guo_retrain = torch.zeros((2, self.args["num_unlearned_nodes"], self.args["num_runs"])).float()  # first row for val acc, second row for test acc

        if  self.args["unlearn_task"] == 'node' or self.args["unlearn_task"] == 'feature':
            for trail_iter in range(self.args["num_runs"]):
                self.logger.info('*'*10 + str(trail_iter) + '*'*10)
                if self.args["fix_random_seed"]:
                    # fix the random seed for perm
                    np.random.seed(trail_iter)
                train_id = torch.arange(self.data.x.shape[0])[train_mask.cpu()]
                # perm = torch.from_numpy(np.random.permutation(train_id.shape[0]))
                # perm = list(perm)
                #############
                # removal_queue = train_id[perm]
                path_un = unlearning_path + "_" + str(trail_iter) + ".txt"
                removal_queue = np.loadtxt(path_un,dtype=int)
                removal_queue_tensor = torch.from_numpy(removal_queue)

                # 找出train_id中存在但removal_queue_tensor中不存在的元素
                unique_elements = train_id.tolist()  # 将train_id转换为列表
                removal_queue_list = removal_queue_tensor.tolist()  # 将removal_queue_tensor转换为列表
                additional_elements = [item for item in unique_elements if item not in removal_queue_list]

                # 将找到的额外元素添加到removal_queue_tensor中
                updated_removal_queue_tensor = torch.cat((removal_queue_tensor, torch.tensor(additional_elements)))

                # 如果需要将结果转换回NumPy数组
                updated_removal_queue = updated_removal_queue_tensor.numpy()
                removal_queue = updated_removal_queue
                # self.member_id = removal_queue[:args.num_removes]
                self.member_id = removal_queue[:self.args["num_unlearned_nodes"]]


                #############

                edge_mask = torch.ones(self.data.edge_index.shape[1], dtype=torch.bool)

                X_scaled_copy = X_scaled_copy_guo.clone().detach().float()
                w_approx = w.clone().detach()  # copy the parameters to modify
                X_old = X.clone().detach().to(device)

                num_retrain = 0
                grad_norm_approx_sum = 0
                # start the removal process
                self.logger.info('='*10 + 'Testing our removal' + '='*10)
                for i in tqdm(range(self.args["num_unlearned_nodes"]-1)):
                        
                    # First, replace removal features with 0 vector
                    X_scaled_copy[removal_queue[i]] = 0
                    if self.args["unlearn_task"] == 'node':
                        # Then remove the correpsonding edges
                        edge_mask[self.data.edge_index[0] == removal_queue[i]] = False
                        edge_mask[self.data.edge_index[1] == removal_queue[i]] = False
                        # make sure we do not remove self-loops
                        self_loop_idx = torch.logical_and(self.data.edge_index[0] == removal_queue[i],
                                                          self.data.edge_index[1] == removal_queue[i]).nonzero().squeeze(-1)
                        if self_loop_idx.size(0) > 0:
                            edge_mask[self_loop_idx] = True

                    start = time.time()
                    # Get propagated features
                    if self.args["GNN_layer"] > 0:
                        X_new = Propagation(X_scaled_copy, self.data.edge_index[:, edge_mask]).to(device)
                    else:
                        X_new = X_scaled_copy.to(device)

                    X_val_new = X_new[val_mask]
                    X_test_new = X_new[test_mask]
                    X_unlearning_new = X_new[removal_queue]
                    y_unlearning = self.data.y[removal_queue].to(device)

                    # note that the removed data point should still not be used in computing K or H
                    # removal_queue[(i+1):] are the remaining training idx
                    K = get_K_matrix(X_new[removal_queue[(i+1):]]).to(device)
                    spec_norm = sqrt_spectral_norm(K)

                    if self.args["train_mode"] == 'ovr':
                        # removal from all one-vs-rest models
                        X_rem = X_new[removal_queue[(i+1):]]
                        for k in range(y_train.size(1)):
                            y_rem = self.data.Y[removal_queue[(i+1):], k]
                            H_inv = lr_hessian_inv(w_approx[:, k], X_rem, y_rem, self.args["lam"])
                            # grad_i is the difference
                            grad_old = lr_grad(w_approx[:, k], X_old[removal_queue[i:]], self.data.Y[removal_queue[(i):], k],  self.args["lam"])
                            grad_new = lr_grad(w_approx[:, k], X_rem, y_rem,  self.args["lam"])
                            grad_i = grad_old - grad_new
                            Delta = H_inv.mv(grad_i)
                            Delta_p = X_rem.mv(Delta)
                            # update w here. If beta exceed the budget, w_approx will be retrained
                            w_approx[:, k] += Delta
                            # data dependent norm
                            grad_norm_approx[i, trail_iter] += (Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                            if self.args["compare_gnorm"]:
                                grad_norm_real[i, trail_iter] += lr_grad(w_approx[:, k], X_rem, y_rem,  self.args["lam"]).norm().cpu()
                                if self.args["unlearn_task"] == 'node':
                                    grad_norm_worst[i, trail_iter] += get_worst_Gbound_node( self.args["lam"], X_rem.shape[0],
                                                                                            self.args["GNN_layer"],
                                                                                            deg[removal_queue[i]]).cpu()
                                elif self.args["unlearn_task"] == 'feature':
                                    grad_norm_worst[i, trail_iter] += get_worst_Gbound_feature( self.args["lam"], X_rem.shape[0],
                                                                                               deg[removal_queue[i]]).cpu()
                        # decide after all classes
                        if grad_norm_approx_sum + grad_norm_approx[i, trail_iter] > budget:
                            # retrain the model
                            grad_norm_approx_sum = 0
                            b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
                            w_approx = ovr_lr_optimize(X_rem, self.data.Y[removal_queue[(i+1):]], self.args["lam"], weight, b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                       opt_choice=self.args["optimizer"],lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            num_retrain += 1
                        else:
                            grad_norm_approx_sum += grad_norm_approx[i, trail_iter]
                        # record acc each round
                        acc_removal[0, i, trail_iter] = ovr_lr_eval(w_approx, X_val_new, y_val)[1]
                        acc_removal[1, i, trail_iter] = ovr_lr_eval(w_approx, X_test_new, y_test)[1]
                        acc_removal[2, i, trail_iter] = ovr_lr_eval(w_approx, X_unlearning_new, y_unlearning)[1]
                    else:
                        # removal from a single binary logistic regression model
                        X_rem = X_new[removal_queue[(i+1):]]
                        y_rem = self.data.Y[removal_queue[(i+1):]]
                        H_inv = lr_hessian_inv(w_approx, X_rem, y_rem, self.args["lam"])
                        # grad_i should be the difference
                        grad_old = lr_grad(w_approx, X_old[removal_queue[i:]], Y[removal_queue[i:]], self.args["lam"])
                        grad_new = lr_grad(w_approx, X_rem, y_rem, self.args["lam"])
                        grad_i = grad_old - grad_new
                        Delta = H_inv.mv(grad_i)
                        Delta_p = X_rem.mv(Delta)
                        w_approx += Delta
                        grad_norm_approx[i, trail_iter] += (Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                        if self.args["compare_gnorm"]:
                            grad_norm_real[i, trail_iter] += lr_grad(w_approx, X_rem, y_rem, self.args["lam"]).norm().cpu()
                            if self.args["unlearn_task"] == 'node':
                                grad_norm_worst[i, trail_iter] += get_worst_Gbound_node(self.args["lam"], X_rem.shape[0],
                                                                                        self.args["GNN_layer"],
                                                                                        deg[removal_queue[i]]).cpu()
                            elif self.args["unlearn_task"] == 'feature':
                                grad_norm_worst[i, trail_iter] += get_worst_Gbound_feature(self.args["lam"], X_rem.shape[0],
                                                                                           deg[removal_queue[i]]).cpu()

                        if grad_norm_approx_sum + grad_norm_approx[i, trail_iter] > budget:
                            # retrain the model
                            grad_norm_approx_sum = 0
                            b = b_std * torch.randn(X_train.size(1)).float().to(device)
                            w_approx = lr_optimize(X_rem, y_rem, self.args["lam"], b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                   opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            num_retrain += 1
                        else:
                            grad_norm_approx_sum += grad_norm_approx[i, trail_iter]
                        # record acc each round
                        acc_removal[0, i, trail_iter] = lr_eval(w_approx, X_val_new, y_val)
                        acc_removal[1, i, trail_iter] = lr_eval(w_approx, X_test_new, y_test)


                    removal_times[i, trail_iter] = time.time() - start
                    # Remember to replace X_old with X_new
                    X_old = X_new.clone().detach()
                    unlearning_acc = ovr_lr_eval(w_approx, X_scaled_copy_guo[self.member_id], self.data.y[self.member_id])
                    if i % self.args["disp"] == 0:
                        self.logger.info("unlearning_acc:{}".format(unlearning_acc))
                        self.logger.info('Iteration %d: time = %.6fs, number of retrain = %d' % (i+1, removal_times[i, trail_iter], num_retrain))
                        self.logger.info('Val acc = %.4f, Test acc = %.4f Unlearning acc = %.4f' % (acc_removal[0, i, trail_iter], acc_removal[1, i, trail_iter],acc_removal[2, i, trail_iter]))
                #######
                    if i == self.args["num_unlearned_nodes"]-2:
                        self.average_f1[trail_iter] = acc_removal[1, i, trail_iter]
                        softlabel_original0 = F.softmax(X_scaled_copy_guo[self.nonmember_id].mm(w),dim = 1)
                        softlabel_original1 = F.softmax(X_scaled_copy_guo[self.member_id].mm(w),dim = 1)
                        softlabel_new0 = F.softmax(X_scaled_copy_guo[self.nonmember_id].mm(w_approx),dim = 1)
                        softlabel_new1 = F.softmax(X_scaled_copy_guo[self.member_id].mm(w_approx),dim = 1)
                        mia_test_y = torch.cat((torch.ones(self.args["num_unlearned_nodes"]), torch.zeros(self.args["num_unlearned_nodes"])))
                        posterior1 = torch.cat((softlabel_original1, softlabel_original0), 0).cpu().detach()
                        posterior2 = torch.cat((softlabel_new1, softlabel_new0), 0).cpu().detach()
                        posterior = np.array([np.linalg.norm(posterior1[i] - posterior2[i]) for i in range(len(posterior1))])
                        
                        auc = roc_auc_score(mia_test_y, posterior.reshape(-1, 1))
                        self.logger.info('auc:{}'.format(auc))
                        self.average_auc[trail_iter] = auc
                        plot_auc(mia_test_y, posterior.reshape(-1, 1))
                        average = removal_times[:, trail_iter].mean()
                        self.avg_training_time[trail_iter] = average

                        self.logger.info('removal_time:{}'.format(average))
                # retrain each round with graph
                if self.args["compare_retrain"]:
                    X_scaled_copy = X_scaled_copy_guo.clone().detach()
                    edge_mask = torch.ones(self.data.edge_index.shape[1], dtype=torch.bool)
                    # start the removal process
                    self.logger.info('=' * 10 + 'Testing with graph retrain' + '=' * 10)
                    for i in tqdm(range(self.args["num_unlearned_nodes"])):
                        # First, replace removal features with 0 vector
                        X_scaled_copy[removal_queue[i]] = 0
                        # Then remove the correpsonding edges
                        if self.args["unlearn_task"] == 'node':
                            edge_mask[self.data.edge_index[0] == removal_queue[i]] = False
                            edge_mask[self.data.edge_index[1] == removal_queue[i]] = False
                            # make sure we do not remove self-loops
                            self_loop_idx = torch.logical_and(self.data.edge_index[0] == removal_queue[i],
                                                              self.data.edge_index[1] == removal_queue[
                                                                  i]).nonzero().squeeze(-1)
                            if self_loop_idx.size(0) > 0:
                                edge_mask[self_loop_idx] = True

                        start = time.time()
                        # Get propagated features
                        if self.args["GNN_layer"] > 0:
                            X_new = Propagation(X_scaled_copy, self.data.edge_index[:, edge_mask]).to(device)
                        else:
                            X_new = X_scaled_copy.to(device)

                        X_val_new = X_new[val_mask]
                        X_test_new = X_new[test_mask]

                        if self.args["train_mode"] == 'ovr':
                            # removal from all one-vs-rest models
                            X_rem = X_new[removal_queue[(i + 1):]]
                            y_rem =  self.data.Y[removal_queue[(i + 1):]]
                            # retrain the model
                            # we do not need to add noise if we are retraining every time
                            # b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
                            w_graph_retrain = ovr_lr_optimize(X_rem, y_rem, self.args["lam"], weight, b=None,
                                                              num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])


                            acc_graph_retrain[0, i, trail_iter] = ovr_lr_eval(w_graph_retrain, X_val_new, y_val)
                            acc_graph_retrain[1, i, trail_iter] = ovr_lr_eval(w_graph_retrain, X_test_new,
                                                                              y_test)
                        else:
                            # removal from a single binary logistic regression model
                            X_rem = X_new[removal_queue[(i + 1):]]
                            y_rem =  Y[removal_queue[(i + 1):]]
                            # retrain the model
                            # b = b_std * torch.randn(X_train.size(1)).float().to(device)
                            w_graph_retrain = lr_optimize(X_rem, y_rem, self.args["lam"], b=None,
                                                              num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            acc_graph_retrain[0, i, trail_iter] = lr_eval(w_graph_retrain, X_val_new, y_val)
                            acc_graph_retrain[1, i, trail_iter] = lr_eval(w_graph_retrain, X_test_new, y_test)

                        removal_times_graph_retrain[i, trail_iter] = time.time() - start
                        if i % self.args["disp"] == 0:
                            self.logger.info('Iteration %d, time = %.6fs, val acc = %.4f, test acc = %.4f' % (
                            i + 1, removal_times_graph_retrain[i, trail_iter],
                            acc_graph_retrain[0, i, trail_iter], acc_graph_retrain[1, i, trail_iter]))

                #######
                # guo removal
                if self.args["compare_guo"] and self.args["unlearn_task"] != 'edge':
                    w_approx_guo = w_guo.clone().detach()  # copy the parameters to modify
                    num_retrain = 0
                    grad_norm_approx_sum_guo = 0
                    # prepare the train/val/test sets
                    X_train = X_scaled_copy_guo[train_mask].to(device)
                    X_train_perm = X_scaled_copy_guo[removal_queue]
                    y_train_perm =  Y[removal_queue]
                    K = get_K_matrix(X_train_perm).to(device)
                    X_val = X_scaled_copy_guo[val_mask].to(device)
                    X_test = X_scaled_copy_guo[test_mask].to(device)
                    # start the removal process
                    self.logger.info('=' * 10 + 'Testing Guo et al. removal' + '=' * 10)
                    for i in tqdm(range(self.args["num_unlearned_nodes"])):
                        start = time.time()
                        if self.args["train_mode"] == 'ovr':
                            # removal from all one-vs-rest models
                            X_rem = X_train_perm[(i + 1):]
                            # update matrix K
                            K -= torch.outer(X_train_perm[i], X_train_perm[i])
                            spec_norm = sqrt_spectral_norm(K)
                            for k in range(y_train_perm.size(1)):
                                y_rem = y_train_perm[(i + 1):, k]
                                H_inv = lr_hessian_inv(w_approx_guo[:, k], X_rem, y_rem, self.args["lam"])
                                # grad_i is the difference
                                grad_i = lr_grad(w_approx_guo[:, k], X_train_perm[i].unsqueeze(0),
                                                 y_train_perm[i, k].unsqueeze(0), self.args["lam"])
                                Delta = H_inv.mv(grad_i)
                                Delta_p = X_rem.mv(Delta)
                                # update w here. If beta exceed the budget, w_approx_guo will be retrained
                                w_approx_guo[:, k] += Delta
                                grad_norm_approx_guo[i, trail_iter] += (
                                            Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                                if self.args["compare_gnorm"]:
                                    grad_norm_real_guo[i, trail_iter] += lr_grad(w_approx_guo[:, k], X_rem,
                                                                                 y_rem, self.args["lam"]).norm().cpu()
                            # decide after all classes
                            if grad_norm_approx_sum_guo + grad_norm_approx_guo[i, trail_iter] > budget:
                                # retrain the model
                                grad_norm_approx_sum_guo = 0
                                b = b_std * torch.randn(X_train_perm.size(1), y_train_perm.size(1)).float().to(
                                    device)
                                w_approx_guo = ovr_lr_optimize(X_rem, y_train_perm[(i + 1):], self.args["lam"], weight,
                                                               b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                                num_retrain += 1
                            else:
                                grad_norm_approx_sum_guo += grad_norm_approx_guo[i, trail_iter]
                            # record the acc each round
                            acc_guo[0, i, trail_iter] = ovr_lr_eval(w_approx_guo, X_val, y_val)
                            acc_guo[1, i, trail_iter] = ovr_lr_eval(w_approx_guo, X_test, y_test)
                        else:
                            # removal from a single binary logistic regression model
                            X_rem = X_train_perm[(i + 1):]
                            y_rem = y_train_perm[(i + 1):]
                            H_inv = lr_hessian_inv(w_approx_guo, X_rem, y_rem, self.args["lam"])
                            grad_i = lr_grad(w_approx_guo, X_train_perm[i].unsqueeze(0),
                                             y_train_perm[i].unsqueeze(0), self.args["lam"])
                            K -= torch.outer(X_train_perm[i], X_train_perm[i])
                            spec_norm = sqrt_spectral_norm(K)
                            Delta = H_inv.mv(grad_i)
                            Delta_p = X_rem.mv(Delta)
                            w_approx_guo += Delta
                            grad_norm_approx_guo[i, trail_iter] += (
                                        Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                            if self.args["compare_gnorm"]:
                                grad_norm_real_guo[i, trail_iter] += lr_grad(w_approx_guo, X_rem, y_rem,
                                                                             self.args["lam"]).norm().cpu()
                            if grad_norm_approx_sum_guo + grad_norm_approx_guo[i, trail_iter] > budget:
                                # retrain the model
                                grad_norm_approx_sum_guo = 0
                                b = b_std * torch.randn(X_train_perm.size(1)).float().to(device)
                                w_approx_guo = lr_optimize(X_rem, y_rem, self.args["lam"], b=b,
                                                           num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                                num_retrain += 1
                            else:
                                grad_norm_approx_sum_guo += grad_norm_approx_guo[i, trail_iter]
                            # record the acc each round
                            acc_guo[0, i, trail_iter] = lr_eval(w_approx_guo, X_val, y_val)
                            acc_guo[1, i, trail_iter] = lr_eval(w_approx_guo, X_test, y_test)

                        removal_times_guo[i, trail_iter] = time.time() - start
                        if i % self.args["disp"] == 0:
                            self.logger.info('Iteration %d: time = %.6fs, number of retrain = %d' % (
                            i + 1, removal_times_guo[i, trail_iter], num_retrain))
                            self.logger.info('Val acc = %.4f, Test acc = %.4f' % (
                            acc_guo[0, i, trail_iter], acc_guo[1, i, trail_iter]))

                #######
                # retrain each round without graph
                if self.args["unlearn_task"] != 'edge' and self.args["compare_retrain"] and self.args["compare_guo"]:
                    X_train = X_scaled_copy_guo[train_mask].to(device)
                    X_train_perm = X_train[perm]
                    y_train_perm = y_train[perm]
                    X_val = X_scaled_copy_guo[val_mask].to(device)
                    X_test = X_scaled_copy_guo[test_mask].to(device)

                    # start the removal process
                    self.logger.info('=' * 10 + 'Testing without graph retrain' + '=' * 10)
                    for i in tqdm(range(self.args["num_unlearned_nodes"])):
                        start = time.time()
                        if self.args["train_mode"] == 'ovr':
                            # removal from all one-vs-rest models
                            X_rem = X_train_perm[(i + 1):]
                            y_rem = y_train_perm[(i + 1):]
                            # retrain the model
                            # b = b_std * torch.randn(X_train_perm.size(1), y_train_perm.size(1)).float().to(device)
                            w_guo_retrain = ovr_lr_optimize(X_rem, y_rem, self.args["lam"], weight, b=None,
                                                            num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            acc_guo_retrain[0, i, trail_iter] = ovr_lr_eval(w_guo_retrain, X_val, y_val)
                            acc_guo_retrain[1, i, trail_iter] = ovr_lr_eval(w_guo_retrain, X_test, y_test)
                        else:
                            # removal from a single binary logistic regression model
                            X_rem = X_train_perm[(i + 1):]
                            y_rem = y_train_perm[(i + 1):]
                            # retrain the model
                            # b = b_std * torch.randn(X_train_perm.size(1)).float().to(device)
                            w_guo_retrain = lr_optimize(X_rem, y_rem, self.args["lam"],  b=None,
                                                            num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            acc_guo_retrain[0, i, trail_iter] = lr_eval(w_guo_retrain, X_val, y_val)
                            acc_guo_retrain[1, i, trail_iter] = lr_eval(w_guo_retrain, X_test, y_test)

                        removal_times_guo_retrain[i, trail_iter] = time.time() - start
                        if i % self.args["disp"] == 0:
                            self.logger.info('Iteration %d, time = %.6fs, val acc = %.4f, test acc = %.4f' % (
                            i + 1, removal_times_guo_retrain[i, trail_iter], acc_guo_retrain[0, i, trail_iter],
                            acc_guo_retrain[1, i, trail_iter]))

        else:
            for trail_iter in range(self.args["num_runs"]):
                self.logger.info('*' * 10, trail_iter, '*' * 10)
                if self.args["fix_random_seed"]:
                    np.random.seed(trail_iter)
                # get a random permutation for edge indices for each trail
                perm = torch.from_numpy(np.random.permutation(self.data.edge_index.shape[1]))
                # Note that all edges are used in training, so we just need to decide the order to remove edges
                # the number of training samples will always be m
                edge_mask = torch.ones(self.data.edge_index.shape[1], dtype=torch.bool)

                X_scaled_copy = X_scaled_copy_guo.clone().detach().float()
                w_approx = w.clone().detach()  # copy the parameters to modify
                X_old = X.clone().detach().to(device)

                num_retrain = 0
                grad_norm_approx_sum = 0
                perm_idx = 0
                # start the removal process
                self.logger.info('=' * 10 + 'Testing our edge removal' + '=' * 10)
                for i in tqdm(range(self.args["num_unlearned_nodes"])):
                    # First, check if this is a self-loop or an edge already deleted
                    while (self.data.edge_index[0, perm[perm_idx]] == self.data.edge_index[1, perm[perm_idx]]) or (
                    not edge_mask[perm[perm_idx]]):
                        perm_idx += 1
                    edge_mask[perm[perm_idx]] = False
                    source_idx = self.data.edge_index[0, perm[perm_idx]]
                    dst_idx = self.data.edge_index[1, perm[perm_idx]]
                    # find the other undirected edge
                    rev_edge_idx = torch.logical_and(self.data.edge_index[0] == dst_idx,
                                                     self.data.edge_index[1] == source_idx).nonzero().squeeze(-1)
                    if rev_edge_idx.size(0) > 0:
                        edge_mask[rev_edge_idx] = False

                    perm_idx += 1
                    start = time.time()
                    # Get propagated features
                    if self.args["GNN_layer"] > 0:
                        X_new = Propagation(X_scaled_copy, self.data.edge_index[:, edge_mask]).to(device)
                    else:
                        X_new = X_scaled_copy.to(device)

                    X_val_new = X_new[val_mask]
                    X_test_new = X_new[test_mask]

                    K = get_K_matrix(X_new[train_mask]).to(device)
                    spec_norm = sqrt_spectral_norm(K)

                    if self.args["train_mode"] == 'ovr':
                        # removal from all one-vs-rest models
                        X_rem = X_new[train_mask]
                        for k in range(y_train.size(1)):
                            assert weight is None
                            y_rem = y_train[:, k]
                            H_inv = lr_hessian_inv(w_approx[:, k], X_rem, y_rem, self.args["lam"])
                            # grad_i is the difference
                            grad_old = lr_grad(w_approx[:, k], X_old[train_mask], y_rem, self.args["lam"])
                            grad_new = lr_grad(w_approx[:, k], X_rem, y_rem, self.args["lam"])
                            grad_i = grad_old - grad_new
                            Delta = H_inv.mv(grad_i)
                            Delta_p = X_rem.mv(Delta)
                            # update w here. If beta exceed the budget, w_approx will be retrained
                            w_approx[:, k] += Delta
                            grad_norm_approx[i, trail_iter] += (Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                            if self.args["compare_gnorm"]:
                                grad_norm_real[i, trail_iter] += lr_grad(w_approx[:, k], X_rem, y_rem,
                                                                         self.args["lam"]).norm().cpu()
                                grad_norm_worst[i, trail_iter] += get_worst_Gbound_edge(self.args["lam"], X_rem.shape[0],
                                                                                        self.args["GNN_layer"])
                        # decide after all classes
                        if grad_norm_approx_sum + grad_norm_approx[i, trail_iter] > budget:
                            # retrain the model
                            grad_norm_approx_sum = 0
                            b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
                            w_approx = ovr_lr_optimize(X_rem, y_train, self.args["lam"], weight, b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            num_retrain += 1
                        else:
                            grad_norm_approx_sum += grad_norm_approx[i, trail_iter]
                        # record acc each round
                        acc_removal[0, i, trail_iter] = ovr_lr_eval(w_approx, X_val_new, y_val)
                        acc_removal[1, i, trail_iter] = ovr_lr_eval(w_approx, X_test_new, y_test)
                    else:
                        # removal from a single binary logistic regression model
                        X_rem = X_new[train_mask]
                        y_rem = y_train
                        H_inv = lr_hessian_inv(w_approx, X_rem, y_rem, self.args["lam"])
                        # grad_i should be the difference
                        grad_old = lr_grad(w_approx, X_old[train_mask], y_train, self.args["lam"])
                        grad_new = lr_grad(w_approx, X_rem, y_rem, self.args["lam"])
                        grad_i = grad_old - grad_new
                        Delta = H_inv.mv(grad_i)
                        Delta_p = X_rem.mv(Delta)
                        w_approx += Delta
                        grad_norm_approx[i, trail_iter] += (Delta.norm() * Delta_p.norm() * spec_norm * gamma).cpu()
                        if self.args["compare_gnorm"]:
                            grad_norm_real[i, trail_iter] += lr_grad(w_approx, X_rem, y_rem, self.args["lam"]).norm().cpu()
                            grad_norm_worst[i, trail_iter] += get_worst_Gbound_edge(self.args["lam"], X_rem.shape[0],
                                                                                    self.args["GNN_layer"])
                        if grad_norm_approx_sum + grad_norm_approx[i, trail_iter] > budget:
                            # retrain the model
                            grad_norm_approx_sum = 0
                            b = b_std * torch.randn(X_train.size(1)).float().to(device)
                            w_approx = lr_optimize(X_rem, y_rem,self.args["lam"], b=b, num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            num_retrain += 1
                        else:
                            grad_norm_approx_sum += grad_norm_approx[i, trail_iter]
                        # record acc each round
                        acc_removal[0, i, trail_iter] = lr_eval(w_approx, X_val_new, y_val)
                        acc_removal[1, i, trail_iter] = lr_eval(w_approx, X_test_new, y_test)

                    removal_times[i, trail_iter] = time.time() - start
                    # Remember to replace X_old with X_new
                    X_old = X_new.clone().detach()
                    if i % self.args["disp"] == 0:
                        self.logger.info('Iteration %d: time = %.6fs, number of retrain = %d' % (
                        i + 1, removal_times[i, trail_iter], num_retrain))
                        self.logger.info('Val acc = %.4f, Test acc = %.4f' % (
                        acc_removal[0, i, trail_iter], acc_removal[1, i, trail_iter]))
                #######
                # retrain each round with graph
                if self.args["compare_retrain"]:
                    edge_mask = torch.ones(self.data.edge_index.shape[1], dtype=torch.bool)
                    perm_idx = 0
                    # start the removal process
                    self.logger.info('=' * 10 + 'Testing with graph retrain' + '=' * 10)
                    for i in tqdm(range(self.args["num_unlearned_nodes"])):
                        # First, check if this is a self-loop or an edge already deleted
                        while (self.data.edge_index[0, perm[perm_idx]] == self.data.edge_index[1, perm[perm_idx]]) or (
                        not edge_mask[perm[perm_idx]]):
                            perm_idx += 1
                        edge_mask[perm[perm_idx]] = False
                        source_idx = self.data.edge_index[0, perm[perm_idx]]
                        dst_idx = self.data.edge_index[1, perm[perm_idx]]
                        # find the other undirected edge
                        rev_edge_idx = torch.logical_and(self.data.edge_index[0] == dst_idx,
                                                         self.data.edge_index[1] == source_idx).nonzero().squeeze(-1)
                        if rev_edge_idx.size(0) > 0:
                            edge_mask[rev_edge_idx] = False

                        perm_idx += 1
                        start = time.time()
                        # Get propagated features
                        if self.args["GNN_layer"] > 0:
                            X_new = Propagation(X_scaled_copy, self.data.edge_index[:, edge_mask]).to(device)
                        else:
                            X_new = X_scaled_copy.to(device)

                        X_val_new = X_new[val_mask]
                        X_test_new = X_new[test_mask]

                        if self.args["train_mode"] == 'ovr':
                            # removal from all one-vs-rest models
                            X_rem = X_new[train_mask]
                            # retrain the model
                            # we do not need to add noise if we are retraining every time
                            # b = b_std * torch.randn(X_train.size(1), y_train.size(1)).float().to(device)
                            w_graph_retrain = ovr_lr_optimize(X_rem, y_train, self.args["lam"], weight, b=None,
                                                              num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            acc_graph_retrain[0, i, trail_iter] = ovr_lr_eval(w_graph_retrain, X_val_new, y_val)
                            acc_graph_retrain[1, i, trail_iter] = ovr_lr_eval(w_graph_retrain, X_test_new,
                                                                              y_test)
                        else:
                            # removal from a single binary logistic regression model
                            X_rem = X_new[train_mask]
                            # retrain the model
                            # b = b_std * torch.randn(X_train.size(1)).float().to(device)
                            w_graph_retrain = lr_optimize(X_rem, y_train, self.args["lam"], b=None,
                                                              num_steps=self.args["num_epochs"], verbose=self.args["verbose"],
                                                              opt_choice=self.args["optimizer"], lr=self.args["opt_lr"], wd=self.args["opt_decay"])
                            acc_graph_retrain[0, i, trail_iter] = lr_eval(w_graph_retrain, X_val_new, y_val)
                            acc_graph_retrain[1, i, trail_iter] = lr_eval(w_graph_retrain, X_test_new, y_test)

                        removal_times_graph_retrain[i, trail_iter] = time.time() - start
                        if i % self.args["disp"] == 0:
                            self.logger.info('Iteration %d, time = %.6fs, val acc = %.4f, test acc = %.4f' % (
                            i + 1, removal_times_graph_retrain[i, trail_iter],
                            acc_graph_retrain[0, i, trail_iter], acc_graph_retrain[1, i, trail_iter]))


        # softlabel_original0 = F.softmax(X_scaled_copy_guo[self.nonmember_id].mm(w),dim = 1)
        # softlabel_original1 = F.softmax(X_scaled_copy_guo[self.member_id].mm(w),dim = 1)
        # softlabel_new0 = F.softmax(X_scaled_copy_guo[self.nonmember_id].mm(w_approx),dim = 1)
        # softlabel_new1 = F.softmax(X_scaled_copy_guo[self.member_id].mm(w_approx),dim = 1)
        # mia_test_y = torch.cat((torch.ones(args.num_removes), torch.zeros(args.num_removes)))
        # posterior1 = torch.cat((softlabel_original1, softlabel_original0), 0).cpu().detach()
        # posterior2 = torch.cat((softlabel_new1, softlabel_new0), 0).cpu().detach()
        # posterior = np.array([np.linalg.norm(posterior1[i] - posterior2[i]) for i in range(len(posterior1))])
        
        # auc = roc_auc_score(mia_test_y, posterior.reshape(-1, 1))
        # self.logger.info(auc)
        # plot_auc(mia_test_y, posterior.reshape(-1, 1))
        # average = removal_times[:, 0].mean()

        # self.logger.info(average)

        # save all results
        # if not osp.exists(args.result_dir):
        #     os.makedirs(args.result_dir)
        # save_path = '%s/%s_std_%.0e_lam_%.0e_nr_%d_K_%d_opt_%s_mode_%s_eps_%.1f_delta_%.0e' % (args.result_dir,
        #              args.dataset, b_std, args.lam, args.num_removes, args.prop_step, args.optimizer, args.removal_mode, args.eps, args.delta)


        # if  args.removal_mode == 'node' or args.removal_mode == 'feature':
        #     if args.train_mode == 'binary':
        #         save_path += '_bin_%s' % args.Y_binary
        #     if args.GPR:
        #         save_path += '_gpr'
        #     if args.compare_gnorm:
        #         save_path += '_gnorm'
        #     if args.compare_retrain:
        #         save_path += '_retrain'
        #     if args.compare_guo:
        #         save_path += '_withguo'

        #     save_path += '.pth'
        #     torch.save({'grad_norm_approx': grad_norm_approx, 'removal_times': removal_times, 'acc_removal': acc_removal,
        #                 'grad_norm_worst': grad_norm_worst, 'grad_norm_real': grad_norm_real,
        #                 'removal_times_graph_retrain': removal_times_graph_retrain, 'acc_graph_retrain': acc_graph_retrain,
        #                 'grad_norm_approx_guo': grad_norm_approx_guo, 'removal_times_guo': removal_times_guo, 'acc_guo': acc_guo,
        #                 'removal_times_guo_retrain': removal_times_guo_retrain, 'acc_guo_retrain': acc_guo_retrain,
        #                 'grad_norm_real_guo': grad_norm_real_guo}, save_path)
        # else:
        #     if args.train_mode == 'binary':
        #         save_path += '_bin_%s' % args.Y_binary
        #     if args.GPR:
        #         save_path += '_gpr'
        #     if args.compare_gnorm:
        #         save_path += '_gnorm'
        #     if args.compare_retrain:
        #         save_path += '_retrain'
        #     save_path += '.pth'

        #     torch.save({'grad_norm_approx': grad_norm_approx, 'removal_times': removal_times, 'acc_removal': acc_removal,
        #                 'grad_norm_worst': grad_norm_worst, 'grad_norm_real': grad_norm_real,
        #                 'removal_times_graph_retrain': removal_times_graph_retrain,
        #                 'acc_graph_retrain': acc_graph_retrain}, save_path)
