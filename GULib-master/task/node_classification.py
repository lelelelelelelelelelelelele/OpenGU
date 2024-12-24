import logging
import os
import random
import time
import copy
import torch
import numpy as np
import torch.nn.functional as F
from sklearn.metrics import f1_score, accuracy_score,recall_score
from torch_geometric.data import NeighborSampler
from torch_geometric.nn.conv.gcn_conv import gcn_norm
from torch_geometric.utils import negative_sampling
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report
from torch_geometric.loader import NeighborLoader
from attack.Attack_methods.GNNDelete_MIA import member_infer_attack
from model.base_gnn.ceu_model import CEU_GNN
from utils import  utils
from torch.autograd import grad
import config
import torch_geometric.transforms as T
from tqdm import tqdm
from utils.utils import get_loss_fct, trange, Reverse_CE
from config import root_path


class NodeClassifier:
    """
    NodeClassifier class for training and evaluating Graph Neural Network (GNN) models on node classification tasks.

    The `NodeClassifier` class provides functionalities to train GNN models, evaluate their performance, and perform
    selective graph unlearning operations. It supports both standard training and specialized unlearning procedures
    tailored for specific scenarios such as edge-level unlearning. The class utilizes various evaluation metrics
    like F1 score, accuracy, and recall to assess model performance.

    Class Attributes:
        args (dict): Configuration parameters, including model type, dataset specifications, training hyperparameters, 
                    unlearning settings, and other relevant settings.

        data (torch_geometric.data.Data): The dataset containing node features, edge indices, and labels for training,
                                         validation, and testing.

        model_zoo (Any): Object that provides access to different GNN models and their configurations.

        logger (logging.Logger): Logger object used to log training progress, metrics, and other important information.

        model (torch.nn.Module): The GNN model that will be trained and evaluated.

        model_name (str): Name of the base model being used (e.g., "SIGN", "SGC").

        device (torch.device): The computation device (CPU or GPU) on which the model and data are loaded.
    """
    def __init__(self,args,data,model_zoo,logger):
        """
        Initializes the NodeClassifier with the given configuration, data, model zoo, and logger.

        Sets up the training environment by assigning the model, dataset, and logger. Determines the computation device
        (CPU or GPU) based on availability.

        Args:
            args (dict): Configuration parameters, including model type, dataset specifications, training hyperparameters,
                        unlearning settings, and other relevant settings.

            data (torch_geometric.data.Data): The dataset containing node features, edge indices, and labels for training,
                                             validation, and testing.

            model_zoo (Any): Object that provides access to different GNN models and their configurations.

            logger (logging.Logger): Logger object used to log training progress, metrics, and other important information.
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.args = args
        self.data = data
        self.model_zoo = model_zoo
        self.model = model_zoo.model
        self.logger = logger
        self.model_name = self.args['base_model']

    def train_model(self,retrain=False):
        """
        Trains the GNN model based on the specified dataset.

        Delegates the training process to the appropriate method (`train_fullbatch`) depending on the dataset type.

        Args:
            retrain (bool, optional): Flag indicating whether to retrain the model. Defaults to `False`.

        Returns:
            None
        """
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr, weight_decay=self.model_zoo.model.config.decay)
        time_sum = 0
        # for epoch in range(self.args['num_epochs']):
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x,self.data.edge_index)
            # print(out.shape,self.data.train_mask.shape,self.data.y.shape)
            loss = F.cross_entropy(out[self.data.train_mask],self.data.y[self.data.train_mask])
            
            
            loss.backward()
            self.optimizer.step()
            self.best_valid_acc = 0
            time_sum += time.time() - start_time

            if (epoch+1) % self.args["test_freq"] == 0:
                # if self.args["unlearning_methods"] == 'GNNDelete':
                    # self.GNNDelete_eval(epoch,retrain)
                
                F1_score = self.evaluate_model()
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, F1_score, loss))

                
        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))

    @torch.no_grad()
    def evaluate_model(self):
        """
        Evaluates the GNN model's performance on the test dataset.

        Sets the model to evaluation mode and moves it to the designated device. Depending on the base model type,
        computes predictions using either pre-processed features (`self.data.xs`) or the original node features
        and edge indices. Calculates the F1 score based on the model's predictions and the true labels on the test mask.

        Returns:
            float: The micro-averaged F1 score on the test dataset.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SIGN":
            y_pred = self.model(self.data.xs).cpu()
        else:
            y_pred = self.model(self.data.x,self.data.edge_index).cpu()
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        F1_score = f1_score(y[self.data.test_mask.cpu()], y_pred[self.data.test_mask.cpu()], average="micro")
        
        # Acc_score = accuracy_score(y_true=y[self.data.test_mask.cpu()], y_pred=y_pred[self.data.test_mask.cpu()])
        # Recall_score = recall_score(y_true=y[self.data.test_mask.cpu()], y_pred=y_pred[self.data.test_mask.cpu()],average="micro")
        return F1_score


    def train_SGU_model(self,retrain=False):
        """
        Trains the GNN model for node classification tasks.

        Resets the model's parameters, initializes the optimizer, and iterates through the training epochs.
        It evaluates the model's performance at regular intervals and saves the model state with the best accuracy.

        Args:
            retrain (bool, optional): Flag indicating whether to retrain the model. Defaults to `False`.

        Returns:
            None
        """
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr, weight_decay=self.model_zoo.model.config.decay)
        start_time = time.time()
        best_acc = 0
        best_w = 0
        for epoch in range(self.args['num_epochs']):
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
                out = self.model(self.data.pre_features[self.data.train_indices])
                loss = F.cross_entropy(out, self.data.y[self.data.train_indices])
            else:
                out = self.model(self.data.x,self.data.edge_index)
                loss = F.cross_entropy(out[self.data.train_indices], self.data.y[self.data.train_indices])

            self.logger.info("epoch:{} loss:{}".format(epoch,loss))
            loss.backward()
            self.optimizer.step()

            if (epoch+1) % self.args["test_freq"] == 0:
                F1_score, Accuracy, Recall = self.evaluate_SGU_model(self.data.pre_features[self.data.test_indices])
                self.logger.info(
                    'epoch: {}  F1_score = {}  Accuracy = {}  Recall = {}'.format(epoch, F1_score, Accuracy, Recall))
                if Accuracy > best_acc :
                    best_acc = Accuracy
                    best_w = copy.deepcopy(self.model.state_dict())
        if self.args["unlearn_task"] == "edge":
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + \
                         self.args["base_model"] + self.args["proportion_unlearned_edges"]
        else:
            model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + \
                         self.args["base_model"]
        self.save_model(model_path,best_w)
        self.logger.info("best:{}".format(best_acc))


    @torch.no_grad()
    def evaluate_SGU_model(self,test_features):
        """
        Evaluates the GNN model's performance.

        Computes the F1 score, accuracy, and recall for the unlearned nodes to assess the effectiveness of the unlearning process.

        Args:
            test_features (torch.Tensor): The input features for the test nodes targeted.

        Returns:
            tuple: A tuple containing evaluation metrics:
                - F1_score (float): The micro-averaged F1 score on the unlearned test nodes.

                - Acc_score (float): The accuracy on the unlearned test nodes.

                - Recall_score (float): The micro-averaged recall on the unlearned test nodes.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = self.model.get_softlabel(test_features).cpu()
        else:
            y_pred = self.model.get_softlabel(self.data.x,self.data.edge_index).cpu()
            y_pred = y_pred[self.data.test_indices]
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        F1_score = f1_score(y[self.data.test_indices], y_pred, average="micro")
        Acc_score = accuracy_score(y_true=y[self.data.test_indices], y_pred=y_pred)
        Recall_score = recall_score(y_true=y[self.data.test_indices], y_pred=y_pred, average="micro")
        return F1_score, Acc_score, Recall_score



    def SGU_unlearning_edge(self,
                        original_softlabels,
                        original_w,
                        unlearning_nodes,
                        activated_nodes,
                        pos_pair,
                        neg_pair,
                        original_feaures,
                        prototype_embedding,
                        unlearning_edge_index):
        """
        Performs SGU unlearning method on edge-level tasks.

        Targets specific edges and their activated components for unlearning. Adjusts the model's parameters to forget the influence
        of the targeted edges while preserving the model's performance on other parts of the graph. The unlearning process
        involves minimizing various loss components to ensure effective forgetting and model integrity.

        Args:
            original_softlabels (torch.Tensor): The original soft labels before unlearning.

            original_w (list): The original model parameters before unlearning.

            unlearning_nodes (list or torch.Tensor): Indices of nodes targeted for unlearning.

            activated_nodes (list or torch.Tensor): Indices of neighboring nodes activated for unlearning.

            pos_pair (dict): Dictionary containing positive pairs for activated nodes.

            neg_pair (dict): Dictionary containing negative pairs for activated nodes.

            original_feaures (torch.Tensor): Original input features for the nodes.

            prototype_embedding (torch.Tensor): Prototype embeddings for the classes.

            unlearning_edge_index (torch.Tensor): Edge indices targeted for unlearning.

        Returns:
            None
        """
        self.tau = 0.5
        self.para1 = 0.8
        self.para2 = 0.001
        self.para3 = 100
        self.para4 = 0.01
        self.para5 = 15
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr,
                                          weight_decay=self.model_zoo.model.config.decay)
        best = 0
        prototype_embedding = prototype_embedding.cuda()


        for epoch in range(self.args['unlearning_epochs']):
            if (epoch+1) % self.args["test_freq"] == 0:
                F1_score,Accuracy,Recall = self.evaluate_SGU_model(original_feaures[self.data.test_indices])
                self.logger.info('epoch: {}  F1_score = {}  Accuracy = {}  Recall = {}'.format(epoch, F1_score,Accuracy,Recall))
            self.model.train()
            self.optimizer.zero_grad()
            z = self.model(original_feaures)
            logits = self.model.decode(z, unlearning_edge_index)
            label = torch.zeros(unlearning_edge_index.size(1)).to(self.device)
            loss_U_edge = F.binary_cross_entropy_with_logits(logits, label)
            softlabels_E = F.softmax(self.model(original_feaures[activated_nodes]),dim=1)
            embedding_E = self.model.get_embedding(original_feaures[activated_nodes])
            embedding_U = self.model.get_embedding(original_feaures[unlearning_nodes])

            w_U = []
            loss_w = 0
            for param_tensor in self.model.parameters():
                param_clone = param_tensor
                w_U.append(param_tensor)
            for i in range(len(original_w)):
                delta_w = (w_U[i] - original_w[i])
                loss_w += torch.norm(delta_w)
            creterion_MSE = torch.nn.MSELoss(reduction="mean")
            smooth_factor = 1e-9

            loss_pE = F.kl_div(torch.log(softlabels_E + smooth_factor),original_softlabels[activated_nodes] + smooth_factor, reduction='batchmean')
            pos_tensors = [torch.tensor(pos_pair[node]) for node in activated_nodes]
            positive_tensors = torch.stack([F.normalize(pos_tensor, p=2, dim=0) for pos_tensor in pos_tensors], dim=0).cuda()
            pos_scores = torch.exp(torch.einsum('ij,ij->i', F.normalize(embedding_E, p=2, dim=1),
                                                positive_tensors )/ self.tau)
            neg_scores = torch.zeros_like(pos_scores)
            for i, node in enumerate(activated_nodes):
                neg_tensors = [torch.tensor(neg_emb) for neg_emb in neg_pair[node]]
                negtive_tensors = torch.stack([F.normalize(neg_tensor, p=2, dim=0) for neg_tensor in neg_tensors], dim=0).cuda()
                neg_scores[i] = torch.exp(torch.einsum('d,nd->n', F.normalize(embedding_E[i], p=2, dim=0),
                                 negtive_tensors) / self.tau).sum()
            loss_hE = -torch.log(pos_scores / neg_scores).sum()


            embedding_E_proto = prototype_embedding[self.data.y[activated_nodes].cuda()]


            loss_proto = creterion_MSE(embedding_E,embedding_E_proto)

            loss = self.para1 * loss_w +  self.para2 * loss_hE + self.para3 * loss_pE + self.para4 * loss_U_edge  + self.para5 * loss_proto

            # loss = loss_pE + loss_proto + loss_pU

            self.logger.info("loss_w: {}  loss_hE: {} loss_pE: {} loss_pU: {} loss_proto:{}".format(self.para1*loss_w,
                                                                                                    self.para2 * loss_hE,
                                                                                                    self.para3 * loss_pE,
                                                                                                    self.para4 * loss_U_edge,
                                                                                                    self.para5 * loss_proto))
            self.logger.info("epoch:{} loss:{}".format(epoch, loss))
            loss.backward()
            self.optimizer.step()

            if F1_score > best and epoch > 40:
                best = F1_score
                F1_score,Accuracy,Recall = self.eval_unlearning(original_feaures,unlearning_nodes)
                self.logger.info('Unlearning: F1_score = {}  Accuracy = {}  Recall = {}'.format(F1_score,Accuracy,Recall))
        F1_score, Accuracy, Recall = self.eval_unlearning(original_feaures,unlearning_nodes)
        self.logger.info("para1:{}   para2:{}   para3:{}   para4:{}   para5:{}".format(self.para1,
                                                                                       self.para2,
                                                                                       self.para3,
                                                                                       self.para4,
                                                                                       self.para5))
        self.logger.info('Unlearning: F1_score = {}  Accuracy = {}  Recall = {}  best: {}'.format(F1_score, Accuracy, Recall,best))






    @torch.no_grad()
    def eval_unlearning(self,features,unlearning_nodes,edge_mask=None):
        """
        Evaluates the GNN model's performance on unlearned nodes after SGU.

        Computes the F1 score, accuracy, and recall for the unlearned nodes to assess the effectiveness of the unlearning process.

        Args:
            features (torch.Tensor): The input features for the nodes.

            unlearning_nodes (list or torch.Tensor): Indices of nodes targeted for unlearning.

            edge_mask (torch.Tensor, optional): Mask to filter specific edges during evaluation. Defaults to `None`.

        Returns:
            tuple:

                - F1_score (float): The micro-averaged F1 score on the unlearned nodes.

                - Acc_score (float): The accuracy on the unlearned nodes.

                - Recall_score (float): The micro-averaged recall on the unlearned nodes.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = self.model.get_softlabel(features[unlearning_nodes].cuda()).cpu()
        else:
            y_pred = self.model.get_softlabel(self.data.x,self.data.edge_index).cpu()
            y_pred = y_pred[unlearning_nodes]
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        F1_score = f1_score(y[unlearning_nodes], y_pred, average="micro")
        Acc_score = accuracy_score(y_true=y[unlearning_nodes], y_pred=y_pred)
        Recall_score = recall_score(y_true=y[unlearning_nodes], y_pred=y_pred,average="micro")
        return F1_score,Acc_score,Recall_score


    def GIF_evaluate_unlearn_F1(self, new_parameters):
        """
        Evaluates the GNN model's F1 score after applying GIF unlearning method.

        Applies the new parameters to the model, performs a forward pass, and computes the F1 score on the test dataset.

        Args:
            new_parameters (list): A list of new model parameters obtained after the GIF unlearning process.

        Returns:
            float: The F1 score on the test dataset after unlearning.
        """
        idx = 0
        for p in self.model.parameters():
            p.data = new_parameters[idx]
            idx = idx + 1

        out = self.model.reason_once_unlearn(self.data)

        test_f1 = f1_score(
            self.data.y[self.data['test_mask']].cpu().numpy(),
            out[self.data['test_mask']].argmax(axis=1).cpu().numpy(),
            average="micro"
        )
        return test_f1

    def train_GUIDE_model(self):
        """
        Trains the GNN models in preparation for applying the GUIDE (Guided Inductive Graph Unlearning) unlearning method.

        Iterates through the specified number of training epochs, performing forward and backward passes.
        Depending on the base model type, computes the cross-entropy loss using either pre-processed features (`self.data.xs`)
        or the original node features and edge indices. Logs the loss at each epoch to monitor training progress.

        Returns:
            None
        """
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            self.model.train()
            labels = self.data.y

            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out = self.model(self.data.xs)[self.data.train_mask]
                loss = F.cross_entropy(out, labels[self.data.train_mask[:labels.size(0)]])

            else:
                out = self.model(self.data.x,self.data.edge_index)[self.data.train_mask]
                loss = F.cross_entropy(out, labels[self.data.train_mask[:labels.size(0)]])
            self.logger.info('Epoch: {:03d} | Loss: {:.4f}'.format(epoch + 1, loss))

            loss.backward()
            self.optimizer.step()


    def CEU_train(self,data,eval=True, verbose=True,return_epoch=False):
        """
        Trains the model for node-level task.

        This method trains the model on the provided training dataset, evaluates it on the validation set, and saves
        the best-performing model based on validation loss. It supports early stopping to prevent overfitting.

        Args:
            data (dict): A dictionary containing training, validation, and test datasets along with edge information.

            eval (bool, optional): Flag indicating whether to perform evaluation after training. Defaults to `True`.

            verbose (bool, optional): Flag indicating whether to print training progress. Defaults to `True`.

            return_epoch (bool, optional): Flag indicating whether to return the number of training epochs completed. Defaults to `False`.

        Returns:
            torch.nn.Module: The trained GNN model.

            int, optional: The number of training epochs completed if `return_epoch` is `True`.
        """
        if verbose:
            t0 = time.time()
            print(f'Start to train a {self.args["model_name"]} model...')

        model = self.model_zoo.model.to(self.device)
        train_loader = DataLoader(data['train_set'], batch_size=self.args["train_batch"], shuffle=True)
        valid_loader = DataLoader(data['valid_set'], batch_size=self.args["test_batch"])
        edge_index = torch.tensor(data['edges'], device=self.device).t()
        num_epochs = self.args['num_epochs']
        lr = self.args["unlearn_lr"]
        l2 = self.args["l2"]
        patience = self.args["patience"]

        optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=l2)

        best_valid_loss = 999999.
        best_epoch = 0
        trail_count = 0

        for e in range(1, num_epochs + 1):

            train_losses = []

            model.train()
            iterator = tqdm(train_loader, f'  Epoch {e}') if verbose else train_loader
            for nodes, labels in iterator:
                model.zero_grad()

                nodes = nodes.to(self.device)
                labels = labels.to(self.device)

                y_hat = model(nodes, edge_index)
                loss = model.loss(y_hat, labels)
                loss.backward()
                optimizer.step()

                train_losses.append(loss.cpu().item())

            train_loss = np.mean(train_losses)

            valid_losses = []

            model.eval()
            with torch.no_grad():
                for nodes, labels in valid_loader:
                    nodes = nodes.to(self.device)
                    labels = labels.to(self.device)

                    y_hat = model(nodes, edge_index)
                    loss = model.loss(y_hat, labels)

                    valid_losses.append(loss.cpu().item())

            valid_loss = np.mean(valid_losses)

            if verbose:
                print(f'  Epoch {e}, training loss: {train_loss:.4f}, validation loss: {valid_loss:.4f}.')

            if self.args["early_stop"]:
                if valid_loss < best_valid_loss:
                    best_valid_loss = valid_loss
                    trail_count = 0
                    best_epoch = e
                    path = os.path.join('./data/CEU/checkpoint', 'tmp')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    torch.save(model.state_dict(), path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
                else:
                    trail_count += 1
                    if trail_count > patience:
                        if verbose:
                            print(
                                f'  Early Stop, the best Epoch is {best_epoch}, validation loss: {best_valid_loss:.4f}.')
                        break
            else:
                path = os.path.join('./data/CEU/checkpoint','tmp')
                if not os.path.exists(path):
                    os.makedirs(path)
                torch.save(model.state_dict(),path+f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt')
        path = os.path.join('./data/CEU/checkpoint', 'tmp')
        model.load_state_dict(torch.load(path + f'/{self.args["base_model"]}_{self.args["dataset_name"]}_{self.args["cuda"]}_best.pt'))

        if eval:
            self.CEU_evaluate()

        # os.remove(os.path.join('./checkpoint', 'tmp', f'{args.model}_{args.data}_{args.gpu}_best.pt'))

        if verbose:
            print(f'{self.args["base_model"]} model training finished. Duration:', int(time.time() - t0))

        if return_epoch:
            return model, num_epochs
        else:
            return model

    @torch.no_grad()
    def CEU_test(self,model, test_loader, edge_index):
        """
        Tests the GNN model's performance on the test dataset.

        This method evaluates the trained model by computing the classification report and average test loss on the test dataset.

        Args:
            model (torch.nn.Module): The trained GNN model to be evaluated.

            test_loader (torch.utils.data.DataLoader): DataLoader for the test dataset.

            edge_index (torch.Tensor): Tensor containing edge indices of the graph.

        Returns:
            tuple:

                - dict: Classification report containing precision, recall, F1-score, and support for each class.

                - float: The average test loss over the test dataset.
        """
        y_preds = []
        y_trues = []
        test_loss = []
        model.eval()
        with torch.no_grad():
            for nodes, labels in test_loader:
                nodes, labels = nodes.to(self.device), labels.to(self.device)
                y_hat = model(nodes, edge_index)
                test_loss.append(model.loss(y_hat, labels).cpu().item())
                y_pred = torch.argmax(y_hat, dim=1)
                y_preds.extend(y_pred.cpu().tolist())
                y_trues.extend(labels.cpu().tolist())
        # del model
        # torch.cuda.empty_cache()
        res = classification_report(y_trues, y_preds, digits=4, output_dict=True)
        return res, np.mean(test_loss)

    @torch.no_grad()
    def CEU_evaluate(self):
        """
        Evaluates the GNN model's performance on the test dataset.

        This method computes and prints the classification report for the test dataset, providing detailed metrics
        such as precision, recall, F1-score, and support for each class.

        Returns:
            None
        """
        test_loader = DataLoader(self.data['test_set'], batch_size=self.args['test_batch'], shuffle=False)
        edge_index = torch.tensor(self.data['edges'], device=self.device).t()
        y_preds = []
        y_true = []

        self.model.eval()
        with torch.no_grad():
            for nodes, labels in test_loader:
                nodes = nodes.to(self.device)
                labels = labels.to(self.device)

                y_hat = self.model(nodes, edge_index)
                y_pred = torch.argmax(y_hat, dim=1)

                y_preds.extend(y_pred.cpu().tolist())
                y_true.extend(labels.cpu().tolist())

        results = classification_report(y_true, y_preds, digits=4)
        print('  Result:')
        print(results)




    def GNNDelete_train(self,logger, avg_time,run,model, data, optimizer, args, logits_ori=None, attack_model_all=None, attack_model_sub=None):
        """
        Trains the GNN model using the GNNDelete unlearning method.

        This method performs the unlearning process by removing specified edges and assessing the model's performance.
        It conducts membership inference attacks before unlearning to establish baseline attack metrics, and logs
        the training progress and evaluation results.

        Args:
            logger (logging.Logger): Logger object for logging training progress and metrics.

            avg_time (dict): Dictionary to store the average training time per run.

            run (int): The current run index or identifier.

            model (torch.nn.Module): The GNN model to be trained and unlearned.

            data (torch_geometric.data.Data): The dataset containing node features, edge indices, and other relevant information.

            optimizer (torch.optim.Optimizer): The optimizer used for updating the model's parameters during training.

            args (dict): Configuration parameters, including unlearning settings, dataset specifications, and other relevant settings.

            logits_ori (torch.Tensor, optional): The original logits from the model before any unlearning or attack processes.
                                                Defaults to `None`.

            attack_model_all (Any, optional): The attack model used for evaluating membership inference attacks on all data.
                                            Defaults to `None`.

            attack_model_sub (Any, optional): The attack model used for evaluating membership inference attacks on a subset of data.
                                            Defaults to `None`.

        Returns:
            None
        """
        self.trainer_log = {
            'unlearning_model': self.args["unlearning_model"],
            'dataset': self.args["dataset_name"],
            'log': []}
        model = model.to('cuda')
        data = data.to('cuda')

        best_metric = 0

        # MI Attack before unlearning
        if attack_model_all is not None:
            mi_logit_all_before, mi_sucrate_all_before = member_infer_attack(model, attack_model_all, data)
            self.trainer_log['mi_logit_all_before'] = mi_logit_all_before
            self.trainer_log['mi_sucrate_all_before'] = mi_sucrate_all_before
        if attack_model_sub is not None:
            mi_logit_sub_before, mi_sucrate_sub_before = member_infer_attack(model, attack_model_sub, data)
            self.trainer_log['mi_logit_sub_before'] = mi_logit_sub_before
            self.trainer_log['mi_sucrate_sub_before'] = mi_sucrate_sub_before

        # All node paris in S_Df without Df
        ## S_Df 1 hop all pair mask
        # sdf1_all_pair_mask = torch.zeros(data.num_nodes, data.num_nodes, dtype=torch.bool)
        # idx = torch.combinations(torch.arange(data.num_nodes)[data.sdf_node_1hop_mask], with_replacement=True).t()
        # sdf1_all_pair_mask[idx[0], idx[1]] = True
        # sdf1_all_pair_mask[idx[1], idx[0]] = True

        # assert sdf1_all_pair_mask.sum().cpu() == data.sdf_node_1hop_mask.sum().cpu() * data.sdf_node_1hop_mask.sum().cpu()

        # ## Remove Df itself
        # sdf1_all_pair_mask[data.train_pos_edge_index[:, data.df_mask][0], data.train_pos_edge_index[:, data.df_mask][1]] = False
        # sdf1_all_pair_mask[data.train_pos_edge_index[:, data.df_mask][1], data.train_pos_edge_index[:, data.df_mask][0]] = False

        # ## S_Df 2 hop all pair mask
        # sdf2_all_pair_mask = torch.zeros(data.num_nodes, data.num_nodes, dtype=torch.bool)
        # idx = torch.combinations(torch.arange(data.num_nodes)[data.sdf_node_2hop_mask], with_replacement=True).t()
        # sdf2_all_pair_mask[idx[0], idx[1]] = True
        # sdf2_all_pair_mask[idx[1], idx[0]] = True

        # assert sdf2_all_pair_mask.sum().cpu() == data.sdf_node_2hop_mask.sum().cpu() * data.sdf_node_2hop_mask.sum().cpu()

        # ## Remove Df itself
        # sdf2_all_pair_mask[data.train_pos_edge_index[:, data.df_mask][0], data.train_pos_edge_index[:, data.df_mask][1]] = False
        # sdf2_all_pair_mask[data.train_pos_edge_index[:, data.df_mask][1], data.train_pos_edge_index[:, data.df_mask][0]] = False

        # ## Lower triangular mask
        # idx = torch.tril_indices(data.num_nodes, data.num_nodes, -1)
        # lower_mask = torch.zeros(data.num_nodes, data.num_nodes, dtype=torch.bool)
        # lower_mask[idx[0], idx[1]] = True

        # ## The final mask is the intersection
        # sdf1_all_pair_without_df_mask = sdf1_all_pair_mask & lower_mask
        # sdf2_all_pair_without_df_mask = sdf2_all_pair_mask & lower_mask

        non_df_node_mask = torch.ones(data.x.shape[0], dtype=torch.bool, device=data.x.device)
        non_df_node_mask[data.directed_df_edge_index.flatten().unique()] = False

        data.sdf_node_1hop_mask_non_df_mask = data.sdf_node_1hop_mask & non_df_node_mask
        data.sdf_node_2hop_mask_non_df_mask = data.sdf_node_2hop_mask & non_df_node_mask

        # Original node embeddings
        with torch.no_grad():
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
                z1_ori, z2_ori = model.get_original_embeddings(data.features_pre,return_all_emb=True)
            else:
                z1_ori, z2_ori = model.get_original_embeddings(data.x, data.edge_index[:, data.dr_mask],
                                                           return_all_emb=True)

        loss_fct = get_loss_fct(self.args["loss_fct"])

        neg_edge = neg_edge_index = negative_sampling(
            edge_index=data.edge_index,
            num_nodes=data.num_nodes,
            num_neg_samples=data.df_mask.sum())
        epoch_time = 0

        for epoch in trange(self.args["unlearning_epochs"], desc='Unlerning'):
            model.train()

            start_time = time.time()
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
                z1, z2 = model(data.features_pre, return_all_emb=True)
            else:    
                z1, z2 = model(data.x, data.edge_index[:, data.sdf_mask], return_all_emb=True)
            # print('current deletion weight', model.deletion1.deletion_weight.sum(), model.deletion2.deletion_weight.sum())
            # print('aaaaaa', z[data.sdf_node_2hop_mask].sum())

            # Randomness
            pos_edge = data.edge_index[:, data.df_mask]
            # neg_edge = torch.randperm(data.num_nodes)[:pos_edge.view(-1).shape[0]].view(2, -1)

            embed1 = torch.cat([z1[pos_edge[0]], z1[pos_edge[1]]], dim=0)
            embed1_ori = torch.cat([z1_ori[neg_edge[0]], z1_ori[neg_edge[1]]], dim=0)

            embed2 = torch.cat([z2[pos_edge[0]], z2[pos_edge[1]]], dim=0)
            embed2_ori = torch.cat([z2_ori[neg_edge[0]], z2_ori[neg_edge[1]]], dim=0)

            loss_r1 = loss_fct(embed1, embed1_ori)
            loss_r2 = loss_fct(embed2, embed2_ori)

            # Local causality
            loss_l1 = loss_fct(z1[data.sdf_node_1hop_mask_non_df_mask], z1_ori[data.sdf_node_1hop_mask_non_df_mask])
            loss_l2 = loss_fct(z2[data.sdf_node_2hop_mask_non_df_mask], z2_ori[data.sdf_node_2hop_mask_non_df_mask])

            # Total loss
            '''both_all, both_layerwise, only2_layerwise, only2_all, only1'''
            loss_l = loss_l1 + loss_l2
            loss_r = loss_r1 + loss_r2

            loss1 = self.args["alpha"] * loss_r1 + (1 - self.args["alpha"]) * loss_l1
            loss1.backward(retain_graph=True)
            optimizer[0].step()
            optimizer[0].zero_grad()

            loss2 = self.args["alpha"] * loss_r2 + (1 - self.args["alpha"]) * loss_l2
            loss2.backward(retain_graph=True)
            optimizer[1].step()
            optimizer[1].zero_grad()

            loss = loss1 + loss2

            end_time = time.time()
            epoch_time += end_time - start_time

            step_log = {
                'Epoch': epoch,
                'train_loss': loss.item(),
                'loss_r': loss_r.item(),
                'loss_l': loss_l.item(),
                'train_time': epoch_time/self.args["unlearning_epochs"]
            }
            msg = [f'{i}: {j:>4d}' if isinstance(j, int) else f'{i}: {j:.4f}' for i, j in step_log.items()]
            tqdm.write(' | '.join(msg))
            logger.info("time:{}".format(epoch_time/50))
            if (epoch + 1) % self.args["test_freq"] == 0:
                valid_loss, dt_acc,recall, dt_f1, valid_log = self.eval(model, data, 'val')
                valid_log['epoch'] = epoch

                train_log = {
                    'epoch': epoch,
                    'train_loss': loss.item(),
                    'loss_r': loss_r.item(),
                    'loss_l': loss_l.item(),
                    'train_time': epoch_time/self.args["unlearning_epochs"],
                }

                for log in [train_log, valid_log]:
                    msg = [f'{i}: {j:>4d}' if isinstance(j, int) else f'{i}: {j:.4f}' for i, j in log.items()]
                    tqdm.write(' | '.join(msg))
                    self.trainer_log['log'].append(log)

                if dt_acc + dt_f1 > best_metric:
                    best_metric = dt_acc + dt_f1
                    best_epoch = epoch

                    print(f'Save best checkpoint at epoch {epoch:04d}. Valid loss = {valid_loss:.4f}')
                    ckpt = {
                        'model_state': model.state_dict(),
                        # 'optimizer_state': [optimizer[0].state_dict(), optimizer[1].state_dict()],
                    }
                    torch.save(ckpt, os.path.join(self.args["checkpoint_dir"],'model_best.pt'))
        avg_time[run] = epoch_time/self.args["unlearning_epochs"]  
        # Save
        ckpt = {
            'model_state': {k: v.to('cpu') for k, v in model.state_dict().items()},
            # 'optimizer_state': [optimizer[0].state_dict(), optimizer[1].state_dict()],
        }
        torch.save(ckpt, os.path.join(self.args["checkpoint_dir"], 'model_final.pt'))

    @torch.no_grad()
    def GNNDelete_test(self, model, data, model_retrain=None, attack_model_all=None, attack_model_sub=None, ckpt='best'):
        """
        Tests the GNN models on the test dataset.
        
        This method loads a specified checkpoint, evaluates the model's performance on the test dataset,
        conducts membership inference attacks if provided, logs the results, and returns evaluation metrics.
        
        Args:
            model (torch.nn.Module): The GNN model to be evaluated.
        
            data (torch_geometric.data.Data): The dataset containing node features, edge indices, and labels.
        
            model_retrain (torch.nn.Module, optional): The retrained model after unlearning. Defaults to `None`.
        
            attack_model_all (Any, optional): The attack model for evaluating membership inference attacks on all data.
        
            attack_model_sub (Any, optional): The attack model for evaluating membership inference attacks on a subset of data.
        
            ckpt (str, optional): The checkpoint to load for evaluation. Use `'best'` to load the best-performing model. Defaults to `'best'`.
        
        Returns:
            tuple:
                - float: The cross-entropy loss on the test dataset.
        
                - float: The accuracy on the test dataset.
        
                - float: The recall on the test dataset.
        
                - float: The F1 score on the test dataset.
        
                - dict: A dictionary containing additional test metrics.
        """
        if ckpt == 'best':  # Load best ckpt
            ckpt = torch.load(os.path.join(self.args["checkpoint_dir"], 'model_best.pt'))
            model.load_state_dict(ckpt['model_state'])

        if 'ogbl' in self.args["dataset_name"]:
            pred_all = False
        else:
            pred_all = True
        loss, dt_acc, recall,dt_f1, test_log = self.eval(model, data, 'test', pred_all)

        self.trainer_log['dt_loss'] = loss
        self.trainer_log['dt_acc'] = dt_acc
        self.trainer_log['dt_f1'] = dt_f1
        # self.trainer_log['df_logit'] = df_logit
        # self.logit_all_pair = logit_all_pair
        # self.trainer_log['df_auc'] = df_auc
        # self.trainer_log['df_aup'] = df_aup

        if model_retrain is not None:  # Deletion
            self.trainer_log['ve'] = self.verification_error(model, model_retrain).cpu().item()
            # self.trainer_log['dr_kld'] = output_kldiv(model, model_retrain, data=data).cpu().item()

        # MI Attack after unlearning
        if attack_model_all is not None:
            mi_logit_all_after, mi_sucrate_all_after = member_infer_attack(model, attack_model_all, data)
            self.trainer_log['mi_logit_all_after'] = mi_logit_all_after
            self.trainer_log['mi_sucrate_all_after'] = mi_sucrate_all_after
        if attack_model_sub is not None:
            mi_logit_sub_after, mi_sucrate_sub_after = member_infer_attack(model, attack_model_sub, data)
            self.trainer_log['mi_logit_sub_after'] = mi_logit_sub_after
            self.trainer_log['mi_sucrate_sub_after'] = mi_sucrate_sub_after

            self.trainer_log['mi_ratio_all'] = np.mean([i[1] / j[1] for i, j in
                                                        zip(self.trainer_log['mi_logit_all_after'],
                                                            self.trainer_log['mi_logit_all_before'])])
            self.trainer_log['mi_ratio_sub'] = np.mean([i[1] / j[1] for i, j in
                                                        zip(self.trainer_log['mi_logit_sub_after'],
                                                            self.trainer_log['mi_logit_sub_before'])])
            print(self.trainer_log['mi_ratio_all'], self.trainer_log['mi_ratio_sub'],
                  self.trainer_log['mi_sucrate_all_after'], self.trainer_log['mi_sucrate_sub_after'])
            print(self.trainer_log['df_auc'], self.trainer_log['df_aup'])
        self.logger.info("loss:{}  ,dt_acc:{} ,recall:{}  ,dt_f1:{}  ,test_log:{}  ".format(loss, dt_acc, recall, dt_f1, test_log))
        return loss, dt_acc, recall, dt_f1, test_log

    @torch.no_grad()
    def GNNDelete_eval(self,epoch,retrain):
        """
        Evaluates the GNN model's performance on the validation dataset and saves the best model based on validation accuracy.
        
        This method computes the evaluation metrics (e.g., accuracy, F1 score, etc.) on the validation set, updates and saves the model if it
        achieves better validation accuracy than previous epochs, and logs the evaluation results.
        
        Args:
            epoch (int): The current training epoch.
        
            retrain (bool): Flag indicating whether the evaluation is after retraining. Determines the checkpoint save path.
        
        Returns:
            None
        """
        valid_loss, dt_acc, recall, dt_f1, valid_log = self.eval(self.model, self.data, 'val')
        if dt_acc > self.best_valid_acc:
            best_valid_acc = dt_acc
            best_epoch = epoch

            self.logger.info(f'Save best checkpoint at epoch {epoch:04d}. Valid Acc = {dt_acc:.4f} ')
            ckpt = {
                'model_state': self.model.state_dict(),
                'optimizer_state': self.optimizer.state_dict(),
            }
            if retrain == False:
                original_path = os.path.join(self.args["checkpoint_dir"], self.args["dataset_name"], self.args["gnn"],
                                             'original',
                                             '-'.join([str(i) for i in [self.args["df"], self.args["df_size"],
                                                                        self.args["random_seed"]]]))
                os.makedirs(original_path, exist_ok=True)
                torch.save(ckpt, original_path + '/model_best.pt')
            else:
                retrain_path = os.path.join(self.args["checkpoint_dir"], self.args["dataset_name"], self.args["gnn"],
                                            'retrain',
                                            '-'.join([str(i) for i in [self.args["df"], self.args["df_size"],
                                                                       self.args["random_seed"]]]))
                os.makedirs(retrain_path, exist_ok=True)
                torch.save(ckpt, retrain_path + '/model_best.pt')
        # self.logger.info(
        #     'epoch: {}  valid_loss = {} dt_acc = {} dt_f1 = {} valid_log = {}'.format(epoch, valid_loss, dt_acc, dt_f1,
        #                                                                               valid_log))
        self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, dt_f1, valid_loss))


    
    
    @torch.no_grad()
    def evaluate_Del_model(self):
        """
        Evaluates the GNN model's performance on the test dataset after deletion.
        
        Computes the F1 score, accuracy, and recall on the test dataset to assess the model's performance post-deletion.
        
        Returns:
            tuple:
        
                - float: The micro-averaged F1 score on the test dataset.
        
                - float: The accuracy on the test dataset.
        
                - float: The micro-averaged recall on the test dataset.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = self.model(self.data.features_pre).cpu()
        else:
            y_pred = self.model(self.data.x,self.data.edge_index).cpu()
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        F1_score = f1_score(y[self.data.test_mask.cpu()], y_pred[self.data.test_mask.cpu()], average="micro")
        Acc_score = accuracy_score(y_true=y[self.data.test_mask.cpu()], y_pred=y_pred[self.data.test_mask.cpu()])
        Recall_score = recall_score(y_true=y[self.data.test_mask.cpu()], y_pred=y_pred[self.data.test_mask.cpu()],average="micro")
        return F1_score,Acc_score,Recall_score



    @torch.no_grad()
    def eval(self, model, data, stage='val', pred_all=False):
        """
        Evaluates the GNN model's performance on a specified dataset stage.
        
        This method computes the loss, accuracy, recall, and F1 score for the given stage ('val' or 'test').
        It can optionally compute predictions for all node pairs based on the `pred_all` flag.
        
        Args:
            model (torch.nn.Module): The GNN model to be evaluated.
        
            data (torch_geometric.data.Data): The dataset containing node features, edge indices, and labels.
        
            stage (str, optional): The dataset stage to evaluate ('val' or 'test'). Defaults to `'val'`.
        
            pred_all (bool, optional): Flag indicating whether to compute predictions for all node pairs. Defaults to `False`.
        
        Returns:
            tuple:
        
                - float: The cross-entropy loss for the specified stage.
        
                - float: The accuracy on the specified stage.
        
                - float: The recall on the specified stage.
        
                - float: The F1 score on the specified stage.
        
                - dict: A dictionary containing additional evaluation metrics.
        """
        model.eval()

        if self.device == 'cpu':
            model = model.to('cpu')

        # if hasattr(data, 'dtrain_mask'):
        #     mask = data.dtrain_mask
        # else:
        #     mask = data.dr_mask
        #z = F.log_softmax(model(data.x, data.edge_index), dim=1)

        # DT AUC AUP
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            z = self.model(self.data.features_pre)
        else:
            z = self.model(self.data.x, self.data.edge_index)
        loss = F.cross_entropy(z[data.val_mask], data.y[data.val_mask]).cpu().item()
        pred = torch.argmax(z[data.val_mask], dim=1).cpu()
        true_lable = data.y[data.val_mask]
        dt_acc = accuracy_score(data.y[data.val_mask].cpu(), pred)
        recall = recall_score(data.y[data.val_mask].cpu(), pred,average='micro')
        dt_f1 = f1_score(data.y[data.val_mask].cpu(), pred, average='micro')

        # DF AUC AUP
        # if self.args.unlearning_model in ['original', 'original_node']:
        #     df_logit = []
        # else:
        #     df_logit = model.decode(z, data.directed_df_edge_index).sigmoid().tolist()

        # if len(df_logit) > 0:
        #     df_auc = []
        #     df_aup = []

        #     # Sample pos samples
        #     if len(self.df_pos_edge) == 0:
        #         for i in range(500):
        #             mask = torch.zeros(data.train_pos_edge_index[:, data.dr_mask].shape[1], dtype=torch.bool)
        #             idx = torch.randperm(data.train_pos_edge_index[:, data.dr_mask].shape[1])[:len(df_logit)]
        #             mask[idx] = True
        #             self.df_pos_edge.append(mask)

        #     # Use cached pos samples
        #     for mask in self.df_pos_edge:
        #         pos_logit = model.decode(z, data.train_pos_edge_index[:, data.dr_mask][:, mask]).sigmoid().tolist()

        #         logit = df_logit + pos_logit
        #         label = [0] * len(df_logit) +  [1] * len(df_logit)
        #         df_auc.append(roc_auc_score(label, logit))
        #         df_aup.append(average_precision_score(label, logit))

        #     df_auc = np.mean(df_auc)
        #     df_aup = np.mean(df_aup)

        # else:
        #     df_auc = np.nan
        #     df_aup = np.nan

        # Logits for all node pairs
        # if pred_all:
        #     logit_all_pair = (z @ z.t()).cpu()
        # else:
        #     logit_all_pair = None

        log = {
            f'{stage}_loss': loss,
            f'{stage}_dt_acc': dt_acc,
            f'{stage}_dt_f1': dt_f1,
        }

        if self.device == 'cpu':
            model = model.to(self.device)

        return loss, dt_acc,recall, dt_f1, log

    @torch.no_grad()
    def prediction_info(self):
        """
        Retrieves the model's predictions and true labels for the test dataset.
        
        This method computes the model's output on the test dataset and returns both the predicted labels and the true labels.
        
        Returns:
            tuple:
        
                - torch.Tensor: The predicted labels for the test dataset.
        
                - torch.Tensor: The true labels for the test dataset.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        y_pred = self.model(self.data.x, self.data.edge_index).cpu()
        y = self.data.y.cpu()
        return y_pred[self.data.test_mask.cpu()], y[self.data.test_mask.cpu()]



    def posterior(self,return_features=False):
        """
        Generates the posterior probabilities from the GNN model.
        
        This method performs inference to obtain the log-softmaxed output probabilities from the model.
        It supports returning either the predictions or both predictions and intermediate features based on the `return_features` flag.
        
        Args:
            return_features (bool, optional): Flag indicating whether to return intermediate features alongside predictions. Defaults to `False`.
        
        Returns:
            torch.Tensor or tuple:
        
                - torch.Tensor: The posterior probabilities for the test dataset.
        
                - torch.Tensor, optional: The intermediate features if `return_features` is `True`.
        """
        self.logger.debug("generating posteriors")
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self.model.eval()

        # self._gen_test_loader()
        # if self.model_name in ['GCN',"SGC","S2GC"] and self.args["unlearning_methods"] == "GIF":
        #     posteriors = self.model.GIF_inference(self.data.x, self.test_loader, self.edge_weight, self.device)
        # elif self.model_name in ["SIGN"] and self.args["unlearning_methods"] == "GIF":
        #     posteriors = self.model.GIF_inference(self.data)
        
        if self.args["unlearning_methods"] == "GraphRevoker":
            z, f = self._inference()

            if return_features:
                return z[self.data_full.test_mask, :], f[self.data_full.test_mask, :]
            return z[self.data_full.test_mask, :]
        posteriors = self.model.inference(self.data.x, self.test_loader, self.device)
        for _, mask in self.data('test_mask'):
            posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

        return posteriors.detach()
    
    @torch.no_grad()
    def _inference(self, no_test_edges=False):
        """
        Performs inference to obtain the model's output and intermediate features.
        
        This internal method computes the log-softmaxed outputs and retrieves intermediate features from the model.
        
        Args:
            no_test_edges (bool, optional): Flag indicating whether to exclude test edges during inference. Defaults to `False`.
        
        Returns:
            tuple:
        
                - torch.Tensor: The log-softmaxed output probabilities.
        
                - torch.Tensor: The intermediate features extracted from the model.
        """
        assert not self.data is None and not self.data_full is None

        self.model.eval()
        self.model = self.model.to(self.device)
        self.data_full = self.data.to(self.device) if no_test_edges else self.data_full.to(self.device)

        z, feat = self.model(self.data_full.x, self.data_full.edge_index, return_feature=True)

        return F.log_softmax(z,dim=1), feat

    def posterior_other(self):
        """
        Generates the posterior probabilities from the GNN model using alternative methods.
        
        This method computes the log-softmaxed output probabilities based on the unlearning method specified.
        
        Returns:
            torch.Tensor: The posterior probabilities for the test dataset.
        """
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

    def generate_embeddings(self):
        """
        Generates embeddings for all nodes in the dataset using the GNN model.
        
        This method performs inference on the entire dataset to obtain the embeddings from the model.
        
        Returns:
            torch.Tensor: The generated embeddings for all nodes in the dataset.
        """
        self.model.eval()
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self._gen_test_loader()

        if self.model_name == 'GCN':
            logits = self.model.inference(self.data.x, self.test_loader, self.edge_weight, self.device)
        else:
            logits = self.model.inference(self.data.x, self.test_loader, self.device)
        return logits
    

    def prepare_data(self, input_data):
        """
        Prepares the dataset for training and evaluation.
        
        This method clones the input data, sets up training and full datasets by adjusting edge indices,
        and generates data loaders based on configuration flags.
        
        Args:
            input_data (torch_geometric.data.Data): The original dataset to be prepared.
        
        Returns:
            None
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
        # self.data_full = to_sparse(data_full)
        
        if self.args['is_use_train_batch']:
            self.gen_train_loader()
        if self.args['is_use_test_batch']:
            self.gen_test_loader()

    def gen_train_loader(self):
        """
        Generates the training data loader using NeighborLoader.
        
        This method creates a NeighborLoader for the training dataset with specified neighbor sizes and batch configurations.
        
        Returns:
            None
        """
        assert not self.data is None

        #self.logger.info("generate train loader")
        self.train_loader = NeighborLoader(self.data, input_nodes=self.data.train_mask,
                                           num_neighbors=[15, 10], batch_size=self.args['batch_size'], 
                                           shuffle=True, num_workers=0, drop_last=True)
        #self.logger.info("generate train loader finish")

    def gen_test_loader(self):
        """
        Generates the test data loader using NeighborLoader.
        
        This method creates a NeighborLoader for the full dataset with specified neighbor sizes and batch configurations.
        
        Returns:
            None
        """
        assert not self.data_full is None

        self.test_loader = NeighborLoader(self.data_full, input_nodes=None,
                                          num_neighbors=[15, 10], batch_size=self.args['test_batch_size'], 
                                          shuffle=False, num_workers=0)


    # def _gen_test_loader(self):
    #     test_indices = np.nonzero(self.data.test_mask.cpu().numpy())[0]

    #     if not self.args['use_test_neighbors']:
    #         edge_index = utils.filter_edge_index(self.data.edge_index, test_indices, reindex=False)
    #     else:
    #         edge_index = self.data.edge_index

    #     if edge_index.shape[1] == 0:
    #         edge_index = torch.tensor([[1, 3], [3, 1]])

    #     self.test_loader = NeighborSampler(
    #         edge_index, node_idx=None,
    #         sizes=[-1], num_nodes=self.data.num_nodes,
    #         # sizes=[5], num_nodes=self.data.num_nodes,
    #         batch_size=self.args['test_batch_size'], shuffle=False,
    #         num_workers=0)
    #     # self.test_loader = NeighborSampler(
    #     #     edge_index, node_idx=None,
    #     #     sizes=[-1], num_nodes=self.data.num_nodes,
    #     #     # sizes=[5], num_nodes=self.data.num_nodes,
    #     #     batch_size=self.args['test_batch_size'], shuffle=False,
    #     #     num_workers=0)

    #     if self.model_name == 'GCN':
    #         _, self.edge_weight = gcn_norm(self.data.edge_index, edge_weight=None, num_nodes=self.data.x.shape[0],
    #                                        add_self_loops=False)
    # def _gen_train_loader(self):
    #     self.logger.info("generate train loader")
    #     train_indices = np.nonzero(self.data.train_mask.cpu().numpy())[0]
    #     edge_index = utils.filter_edge_index(self.data.edge_index, train_indices, reindex=False)
    #     if edge_index.shape[1] == 0:
    #         edge_index = torch.tensor([[1, 2], [2, 1]])

    #     self.train_loader = NeighborSampler(
    #         edge_index, node_idx=self.data.train_mask,
    #         sizes=[5, 5], num_nodes=self.data.num_nodes,
    #         batch_size=self.args['batch_size'], shuffle=True,
    #         num_workers=0)

    #     if self.model_name in ['GCN','SGC','S2GC']:
    #         _, self.edge_weight = gcn_norm(self.data.edge_index, edge_weight=None, num_nodes=self.data.x.shape[0],
    #                                        add_self_loops=False)

    #         if self.args["GIF_method"] in ["GIF", "IF"]:
    #             _, self.edge_weight_unlearn = gcn_norm(
    #                 self.data.edge_index_unlearn,
    #                 edge_weight=None,
    #                 num_nodes=self.data.x.shape[0],
    #                 add_self_loops=False)

    #     self.logger.info("generate train loader finish")

    @torch.no_grad()
    def verification_error(self,model1, model2):
        """
        Computes the L2 distance between approximate model and re-trained model to measure verification error.
        
        This method calculates the sum of L2 norms of the differences between corresponding parameters of two models,
        providing a quantitative measure of how much the models differ.
        
        Args:
            model1 (torch.nn.Module): The first GNN model.
        
            model2 (torch.nn.Module): The second GNN model to compare against the first.
        
        Returns:
            float: The total L2 distance between the two models' parameters.
        """
        '''l'''

        model1 = model1.to('cpu')
        model2 = model2.to('cpu')

        modules1 = {n: p for n, p in model1.named_parameters()}
        modules2 = {n: p for n, p in model2.named_parameters()}

        all_names = set(modules1.keys()) & set(modules2.keys())

        print(all_names)

        diff = torch.tensor(0.0).float()
        for n in all_names:
            diff += torch.norm(modules1[n] - modules2[n])

        return diff

    def save_model(self, save_path,model_dict=None):
        """
        Saves the GNN model's state dictionary to a specified path.
        
        This method writes the model's state dictionary to the provided `save_path`. If a `model_dict` is provided,
        it saves that dictionary instead.
        
        Args:
            save_path (str): The file path where the model's state dictionary will be saved.
        
            model_dict (dict, optional): A dictionary of model parameters to save. If `None`, the current model's state dictionary is saved.
        
        Returns:
            None
        """
        with open(save_path,mode='w') as file:
            if model_dict is not None:
                self.logger.info('saving best model {}'.format(save_path))
                torch.save(model_dict, save_path)
            else:
                self.logger.info('saving model {}'.format(save_path))
                torch.save(self.model.state_dict(), save_path)

    def load_model(self, save_path):
        """
        Loads the GNN model's state dictionary from a specified path.
        
        This method reads the model's state dictionary from the provided `save_path` and updates the model accordingly.
        
        Args:
            save_path (str): The file path from where the model's state dictionary will be loaded.
        
        Returns:
            None
        """
        # self.logger.info('loading model {}'.format(save_path))
        device = torch.device('cpu')
        self.model.load_state_dict(torch.load(save_path, map_location=device))



