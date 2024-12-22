import torch
import time
import torch.nn.functional as F
import numpy as np
import random
import copy
import os
from torch_geometric.utils import negative_sampling
from torch_geometric.transforms import RandomLinkSplit
from sklearn.metrics import f1_score, accuracy_score, recall_score
from tqdm import tqdm
from torch_geometric.utils import negative_sampling
from torch_geometric.data import Data
from utils.utils import get_link_labels
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score


class EdgePredictor:
    """
    EdgePredictor class for training and evaluating edge prediction models.

    This class provides a framework for training Graph Neural Network (GNN) models to perform 
    edge prediction tasks. It manages data preparation, model training, evaluation, and 
    model persistence. The class supports different loss functions and can handle node, edge, 
    and graph-level downstream tasks.

    Class Attributes:
        args (dict): Configuration parameters, including model type, dataset specifications, 
                     training hyperparameters, unlearning settings, and other relevant settings.

        data (dict): A dictionary containing datasets for training, validation, and testing.
                     Expected keys include 'train_set', 'valid_set', 'test_set', and 'edges'.

        device (torch.device): The computation device (CPU or GPU) on which the model 
                               and data are loaded for training.

        model_zoo (object): An object that contains the GNN model to be trained and its configuration.

        model (torch.nn.Module): The neural network model that will be trained for edge prediction.

        model_name (str): The name of the base model being used (e.g., "SIGN").

        logger (logging.Logger): Logger object used to log training progress, metrics, 
                                 and other important information.

        alpha (float): Weighting factor used in the loss function to balance between 
                       different components of the loss.
    """
    def __init__(self, args, data, model_zoo, logger):
        """
        Initializes the EdgePredictor with the provided configuration, logger, model zoo, data, and alpha.

        Args:
            args (dict): Configuration parameters, including model type, dataset specifications, 
                        training hyperparameters, unlearning settings, and other relevant settings.
                        
            logger (logging.Logger): Logger object used to log training progress, metrics, 
                                     and other important information.
                        
            model_zoo (object): An object that contains the GNN model to be trained and its configuration.
                        
            data (dict): A dictionary containing datasets for training, validation, and testing.
                         Expected keys include 'train_set', 'valid_set', 'test_set', and 'edges'.
                        
            alpha (float, optional): Weighting factor for balancing different loss components. 
                                     Defaults to 0.5.
        """
        self.args = args
        self.data = data
        self.data = self.split_edge(self.data)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_zoo = model_zoo
        self.model = model_zoo.model
        self.model_name = self.args['base_model']
        self.logger = logger

    def train_model(self, retrain=False):
        """
        Trains the edge prediction model.

        This method initiates the training process. It prepares the data, sets the model to training 
        mode, and iterates through epochs to optimize the model parameters based on the specified 
        loss function. Periodically evaluates the model on the validation set and logs the performance.

        Args:
            retrain (bool, optional): Whether to retrain the model from scratch. Defaults to False.

        Returns:
            None
        """
        self.data = self.split_edge(self.data)
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        # self.train_data=self.train_data.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr,
                                          weight_decay=self.model_zoo.model.config.decay)
        time_sum = 0
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            start_time = time.time()
            self.model.train()

            self.optimizer.zero_grad()
            if self.model_name == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.train_edge_index)

            neg_edge_index = negative_sampling(
                edge_index=self.data.train_edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.train_edge_label_index.size(1)
            )
            neg_edge_label = torch.zeros(neg_edge_index.size(1), dtype=torch.float32)
            pos_edge_label = torch.ones(self.data.train_edge_index.size(1),dtype=torch.float32)
            # edge_logits = self.decode(z=out, edge_index=self.data.train_edge_label_index)
            edge_logits = self.decode(z=out, pos_edge_index=self.data.train_edge_index,neg_edge_index=neg_edge_index)
            
            edge_labels = torch.cat((pos_edge_label,neg_edge_label),dim=-1)
            edge_labels = edge_labels.to(self.device)
            # edge_labels = edge_labels.to(self.device)
            loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels)
            # loss = self.get_loss(out)
            loss.backward()
            self.optimizer.step()
            self.best_valid_acc = 0
            time_sum += time.time() - start_time
            # print(loss.item())
            if (epoch + 1) % self.args["test_freq"] == 0:
                F1_score = self.evaluate_model()
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, F1_score, loss))
        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))

    # def get_loss(self, out, reduction="none"):
    #     # neg_edge_index = negative_sampling(
    #     #         edge_index=self.data.train_edge_index,num_nodes=self.data.num_nodes,
    #     #         num_neg_samples=self.data.train_edge_label_index.size(1)
    #     #     )
    #     edge_logits = self.decode(z=out, edge_index=self.data.train_edge_label_index)
    #     edge_labels = self.data.train_edge_label
    #     loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels, reduction=reduction)
    #     return loss

    @torch.no_grad()
    def evaluate_model(self):
        """
        Evaluates the model's performance on the validation set.

        This method computes the F1 score based on the model's predictions and the true labels 
        of the validation set. It performs a forward pass through the model, applies a sigmoid 
        activation to the logits, and calculates the F1 score.

        Returns:
            float: The F1 score of the model on the validation set.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)

        if self.args["base_model"] == "SIGN":
            out = self.model(self.data.xs)
        else:
            out = self.model(self.data.x, self.data.val_edge_index)
        edge_label_index = self.data.val_edge_label_index
        edge_pred_logits = self.decode_val(z=out, edge_label_index=edge_label_index)
        edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        # edge_pred = torch.argmax(edge_pred_logits)
        edge_labels = self.data.val_edge_label
        F1_score = f1_score(edge_labels.cpu(), edge_pred.cpu())
        # Acc_score = accuracy_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        # Recall_score = recall_score(y_true=edge_labels.cpu(),y_pred=edge_pred.cpu())
        return F1_score

    @torch.no_grad()
    def eval_unlearning(self, features, unlearning_nodes, edge_mask=None):
        """
        Evaluates the model's performance on unlearning tasks.

        This method assesses how well the model has unlearned specific nodes by comparing 
        the predicted labels with the true labels for those nodes. It computes F1 score, 
        accuracy, and recall.

        Args:
            features (torch.Tensor): Feature representations of the nodes.
                
            unlearning_nodes (list or torch.Tensor): Indices of the nodes to be unlearned.
                
            edge_mask (torch.Tensor, optional): Mask for edges, if applicable. Defaults to None.

        Returns:
            tuple: A tuple containing the F1 score, accuracy, and recall for the unlearned nodes.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = F.softmax(self.model(features[unlearning_nodes].cuda()),dim = 1).cpu()
        else:
            y_pred = F.softmax(self.model(self.data.x, self.data.edge_index),dim = 1).cpu()
            y_pred = y_pred[unlearning_nodes]
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        F1_score = f1_score(y[unlearning_nodes], y_pred, average="micro")
        Acc_score = accuracy_score(y_true=y[unlearning_nodes], y_pred=y_pred)
        Recall_score = recall_score(y_true=y[unlearning_nodes], y_pred=y_pred, average="micro")
        return F1_score, Acc_score, Recall_score

    def split_edge(self, data):
        """
        Splits the edge data into training, validation, and testing sets.

        This method uses the `RandomLinkSplit` function to divide the edges into training, 
        validation, and testing subsets. It assigns the split edges and their labels back 
        to the data object.

        Args:
            data (torch_geometric.data.Data): The original graph data containing all edges.

        Returns:
            torch_geometric.data.Data: The updated data object with split edges.
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

    # def decode(self, z, edge_index):
    #     # edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
    #     return (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

    def decode_val(self, z, edge_label_index):
        """
        Decodes the model's output logits for validation edge prediction.

        This method computes the dot product between node embeddings for each edge in 
        the validation set to obtain logits for edge existence.

        Args:
            z (torch.Tensor): Node embeddings from the model.
                
            edge_label_index (torch.Tensor): Indices of the edges in the validation set.

        Returns:
            torch.Tensor: Logits for the validation edges.
        """
        # print(z.shape)
        return (z[edge_label_index[0]] * z[edge_label_index[1]]).sum(dim=-1)

    def get_edge_labels(self, pos_edge_index, neg_edge_index):
        """
        Generates labels for positive and negative edges.

        This method creates a label tensor where positive edges are labeled as 1 and 
        negative edges are labeled as 0.

        Args:
            pos_edge_index (torch.Tensor): Indices of the positive (existing) edges.
                
            neg_edge_index (torch.Tensor): Indices of the negative (non-existing) edges.

        Returns:
            torch.Tensor: A tensor of edge labels.
        """
        num_edges = pos_edge_index.size(1) + neg_edge_index.size(1)
        edge_labels = torch.zeros(num_edges, dtype=torch.float32, device=self.device)  # float32 or float
        edge_labels[:pos_edge_index.size(1)] = 1
        return edge_labels

    def save_model(self, save_path, model_dict=None):
        """
        Saves the model's state or a specific model dictionary to the specified file path.

        This method saves the current state of the model or an optional custom model dictionary 
        to a file. If the directory does not exist, it is created. The model is saved using 
        PyTorch's `torch.save` method.

        Args:
            save_path (str): The path to the file where the model will be saved.
                
            model_dict (dict, optional): A specific model dictionary to save. If None, the model's 
                                         current state is saved. Defaults to None.

        Returns:
            None
        """
        with open(save_path, mode='w') as file:
            if model_dict is not None:
                self.logger.info('saving best model {}'.format(save_path))
                torch.save(model_dict, save_path)
            else:
                self.logger.info('saving model {}'.format(save_path))
                torch.save(self.model.state_dict(), save_path)

    def load_model(self, save_path):
        """
        Loads the model's state from the specified file path.

        This method loads the model's state dictionary from a file using PyTorch's `torch.load` 
        and applies it to the model.

        Args:
            save_path (str): The path to the file from which the model will be loaded.

        Returns:
            None
        """
        # self.logger.info('loading model {}'.format(save_path))
        device = torch.device('cpu')
        self.model.load_state_dict(torch.load(save_path, map_location=device))

    def posterior_other(self):
        """
        Computes the model's posteriors for node-level tasks.

        This method performs a forward pass through the model to compute the posteriors for node 
        classification tasks. It applies log-softmax to the output based on the test mask.

        Returns:
            torch.Tensor: The log-softmax of the posteriors for the test set nodes.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SIGN":
            posteriors = F.log_softmax(self.model(self.data.xs))
        else:
            posteriors = F.log_softmax(self.model(self.data.x, self.data.edge_index))
        for _, mask in self.data('test_mask'):
            posteriors = F.log_softmax(posteriors[mask.cpu()], dim=-1)

        return posteriors.detach()

    @torch.no_grad()
    def evaluate_Del_model(self):
        """
        Evaluates the model's performance after unlearning.

        This method assesses the model's performance by computing the F1 score, accuracy, 
        and recall on the validation set after the unlearning process.

        Returns:
            tuple: A tuple containing the F1 score, accuracy, and recall of the model.
        """
        # self.data = self.split_edge(self.data)
        self.model.eval()
        self.model = self.model.to(self.device)
        # self.data = self.data.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = self.model(self.data.features_pre).cpu()
        else:
            y_pred = self.model(self.data.x, self.data.val_edge_index).cpu()
        edge_label_index = self.data.val_edge_label_index
        edge_pred_logits = self.decode_val(z=y_pred, edge_label_index=edge_label_index.cpu())
        edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        # edge_pred = torch.argmax(edge_pred_logits)
        edge_labels = self.data.val_edge_label
        F1_score = f1_score(edge_labels.cpu(), edge_pred.cpu())
        Acc_score = accuracy_score(y_true=edge_labels.cpu(), y_pred=edge_pred.cpu())
        Recall_score = recall_score(y_true=edge_labels.cpu(), y_pred=edge_pred.cpu())
        return F1_score, Acc_score, Recall_score

    # def train_SGU_model(self, retrain=False):
    #     self.model.train()
    #     self.model.reset_parameters()
    #     self.model = self.model.to(self.device)
    #     self.data = self.data.to(self.device)
    #     self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr,
    #                                       weight_decay=self.model_zoo.model.config.decay)
    #     start_time = time.time()
    #     best_acc = 0
    #     best_w = 0
    #     for epoch in range(self.args['num_epochs']):
    #         self.model.train()
    #         self.optimizer.zero_grad()
    #         neg_edge_index = negative_sampling(
    #             edge_index=self.data.train_edge_index, num_nodes=self.data.num_nodes,
    #             num_neg_samples=self.data.train_edge_label_index.size(1)
    #         )
    #         if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args[
    #             "base_model"] == "SIGN":
    #             out = self.model(self.data.pre_features[self.data.train_indices])
    #         else:
    #             out = self.model(self.data.x, self.data.train_edge_index)
    #         edge_logits = self.decode(z=out, edge_index=self.data.train_edge_label_index)
    #         edge_labels = self.get_edge_labels(self.data.train_edge_label_index, neg_edge_index)
    #         # edge_labels = edge_labels.to(self.device)
    #         loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels)
    #         loss.backward()
    #         self.optimizer.step()

    #         if (epoch + 1) % self.args["test_freq"] == 0:
    #             F1_score, Accuracy, Recall = self.evaluate_SGU_model(self.data.pre_features[self.data.test_indices])
    #             self.logger.info(
    #                 'epoch: {}  F1_score = {}  Accuracy = {}  Recall = {}'.format(epoch, F1_score, Accuracy, Recall))
    #             if Accuracy > best_acc:
    #                 best_acc = Accuracy
    #                 best_w = copy.deepcopy(self.model.state_dict())

    #     self.logger.info("best:{}".format(best_acc))

    def GIF_evaluate_unlearn_F1(self, new_parameters):
        """
        Evaluates the F1 score after applying Graph Influence Function (GIF) based unlearning.

        This method updates the model's parameters with `new_parameters`, which are typically generated by 
        the Graph Influence Function unlearning process. It performs a forward pass using the updated 
        model to obtain edge predictions, and then calculates the F1 score by comparing the predicted 
        edge labels against the true labels.

        Args:
            new_parameters (list of torch.Tensor or torch.Tensor): 
                New model parameters to replace the current ones. 

        Returns:
            float: The F1 score of the model after applying the unlearning process.
        """
        idx = 0
        for p in self.model.parameters():
            p.data = new_parameters[idx]
            idx = idx + 1

        out = self.model.reason_once_unlearn(self.data)

        neg_edge_index = negative_sampling(
            edge_index=self.data.edge_index, num_nodes=self.data.num_nodes,
            num_neg_samples=self.data.edge_index.size(1)
        )
        edge_label = self.get_edge_labels(self.data.edge_index, neg_edge_index)
        edge_index = torch.cat([self.data.edge_index, neg_edge_index], dim=-1)
        edge_logits = self.decode(out, edge_index=edge_index).cpu()
        edge_pred = torch.where(edge_logits > 0.5, torch.tensor(1), torch.tensor(0))
        F1_score = f1_score(edge_label.cpu(), edge_pred.cpu())
        return F1_score

    @torch.no_grad()
    def evaluate_SGU_model(self, test_features):
        """
        Evaluates the model's performance after applying the SGU method.

        This method computes the F1 score, accuracy, and recall based on the model's predictions 
        and the true labels of the validation set.

        Args:
            test_features (torch.Tensor): Feature representations of the test nodes.

        Returns:
            tuple: A tuple containing the F1 score, accuracy, and recall of the model.
        """
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            y_pred = F.softmax(self.model(test_features,return_all_emb = True)[-1],dim=1).cpu()
        else:
            y_pred = F.softmax(self.model(self.data.x, self.data.edge_index,return_all_emb = True)[-1],dim=1).cpu()
        edge_label_index = self.data.val_edge_label_index
        edge_pred_logits = self.decode_val(z=y_pred, edge_label_index=edge_label_index.cpu())
        edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        # edge_pred = torch.argmax(edge_pred_logits)
        edge_labels = self.data.val_edge_label
        F1_score = f1_score(edge_labels.cpu(), edge_pred.cpu())
        Acc_score = accuracy_score(y_true=edge_labels.cpu(), y_pred=edge_pred.cpu())
        Recall_score = recall_score(y_true=edge_labels.cpu(), y_pred=edge_pred.cpu())
        return F1_score, Acc_score, Recall_score

    def train_GUIDE_model(self):
        """
        Trains the GNN model using the GUIDE (Guided Inductive Graph Unlearning) unlearning method.

        This method handles the training loop, including loss computation, 
        backpropagation, optimizer steps, and periodic logging of the training loss.
        
        Returns:
            None
        """
        self.data = self.split_edge(self.data)
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            self.model.train()

            self.optimizer.zero_grad()
            if self.model_name == "SIGN":
                out = self.model(self.data.xs)
            else:
                out = self.model(self.data.x, self.data.train_edge_index)

            edge_logits = self.decode(z=out, edge_index=self.data.train_edge_label_index)
            edge_labels = self.data.train_edge_label
            # edge_labels = edge_labels.to(self.device)
            loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels)
            loss.backward()
            self.optimizer.step()
            self.logger.info('Epoch: {:03d} | Loss: {:.4f}'.format(epoch + 1, loss))

    def train_UTU_model(self):
        """
        Trains the model using the UTU (Unlink to Unlearn) method.

        This method manages the training process, including data preparation, 
        loss computation, backpropagation, optimizer steps, evaluation on the validation set, 
        and saving the best model checkpoints based on validation loss improvements.

        Returns:
            None
        """
        self.data = self.data.to(self.device)
        self.trainer_log = {
            'unlearning_model': self.args["unlearning_model"],
            'dataset': self.args["dataset"],
            'log': []}
        self.logit_all_pair = None
        self.df_pos_edge = []
        start_time = time.time()
        best_valid_loss = 1000000
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model_zoo.model.config.lr,
                                          weight_decay=self.model_zoo.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="Training", unit="epoch"):
            self.model.train()
            self.model.reset_parameters()
            neg_edge_index = negative_sampling(
                edge_index=self.data.train_pos_edge_index,
                num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.dtrain_mask.sum())
            z = self.model(self.data.x, self.data.train_pos_edge_index)
            logits = self.decode(z, self.data.train_pos_edge_index, neg_edge_index)
            label = get_link_labels(self.data.train_pos_edge_index, neg_edge_index)
            loss = F.binary_cross_entropy_with_logits(logits, label)
            loss.backward()
            # torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
            self.optimizer.step()
            self.optimizer.zero_grad()
            if (epoch + 1) % self.args["test_freq"] == 0:
                valid_loss, dt_auc, dt_aup, df_auc, df_aup, df_logit, logit_all_pair, valid_log = self.UTU_eval(
                    self.model, self.data, 'val')

                train_log = {
                    'epoch': epoch,
                    'train_loss': loss.item()
                }
                log = {**train_log, **valid_log}
                for log in [train_log, valid_log]:
                    msg = [f'{i}: {j:>4d}' if isinstance(j, int) else f'{i}: {j:.4f}' for i, j in log.items()]
                    tqdm.write(' | '.join(msg))

                self.trainer_log['log'].append(train_log)
                self.trainer_log['log'].append(valid_log)

                if valid_loss < best_valid_loss:
                    best_valid_loss = valid_loss
                    best_epoch = epoch

                    print(f'Save best checkpoint at epoch {epoch:04d}. Valid loss = {valid_loss:.4f}')
                    ckpt = {
                        'model_state': self.model.state_dict(),
                        'optimizer_state': self.optimizer.state_dict(),
                    }
                    torch.save(ckpt, os.path.join(self.args["checkpoint_dir"], 'model_best.pt'))
                    torch.save(z, os.path.join(self.args["checkpoint_dir"], 'node_embeddings.pt'))

        self.trainer_log['training_time'] = time.time() - start_time
        ckpt = {
            'model_state': self.model.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
        }
        torch.save(ckpt, os.path.join(self.args["checkpoint_dir"], 'model_final.pt'))

        print(
            f'Training finished. Best checkpoint at epoch = {best_epoch:04d}, best valid loss = {best_valid_loss:.4f}')

        self.trainer_log['best_epoch'] = best_epoch
        self.trainer_log['best_valid_loss'] = best_valid_loss

    @torch.no_grad()
    def UTU_eval(self, model, data, stage='val', pred_all=False):
        """
        Evaluates the model's performance after applying the Unlink to Unlearn (UTU) method.

        This method assesses the model's performance by computing various metrics such as 
        loss, AUC, and average precision on both destructive (DT) and defensive (DF) sets.

        Args:
            model (torch.nn.Module): The trained model to be evaluated.
                
            data (torch_geometric.data.Data): The dataset containing edge information.
                
            stage (str, optional): The evaluation stage, either 'val' or 'test'. Defaults to 'val'.
                
            pred_all (bool, optional): Whether to predict logits for all node pairs. Defaults to False.

        Returns:
            tuple: A tuple containing loss, DT AUC, DT AUP, DF AUC, DF AUP, DF logits, all pair logits, and log dictionary.
        """
        model.eval()
        pos_edge_index = data[f'{stage}_pos_edge_index']
        neg_edge_index = data[f'{stage}_neg_edge_index']

        if hasattr(data, 'dtrain_mask'):
            mask = data.dtrain_mask
        else:
            mask = data.dr_mask
        z = model(data.x, data.train_pos_edge_index[:, mask])
        logits = self.decode(z, pos_edge_index, neg_edge_index).sigmoid()
        label = get_link_labels(pos_edge_index, neg_edge_index)

        # DT AUC AUP
        loss = F.binary_cross_entropy_with_logits(logits, label).cpu().item()
        dt_auc = roc_auc_score(label.cpu(), logits.cpu())
        dt_aup = average_precision_score(label.cpu(), logits.cpu())

        # DF AUC AUP
        if self.args["unlearning_model"] in ['original']:
            df_logit = []
        else:
            # df_logit = model.decode(z, data.train_pos_edge_index[:, data.df_mask]).sigmoid().tolist()
            df_logit = self.decode(z, data.directed_df_edge_index).sigmoid().tolist()

        if len(df_logit) > 0:
            df_auc = []
            df_aup = []

            # Sample pos samples
            if len(self.df_pos_edge) == 0:
                for i in range(5):
                    mask = torch.zeros(data.train_pos_edge_index[:, data.dr_mask].shape[1], dtype=torch.bool)
                    idx = torch.randperm(data.train_pos_edge_index[:, data.dr_mask].shape[1])[:len(df_logit)]
                    mask[idx] = True
                    self.df_pos_edge.append(mask)

            # Use cached pos samples
            for mask in self.df_pos_edge:
                pos_logit = self.decode(z, data.train_pos_edge_index[:, data.dr_mask][:, mask]).sigmoid().tolist()

                logit = df_logit + pos_logit
                label = [0] * len(df_logit) + [1] * len(pos_logit)
                df_auc.append(roc_auc_score(label, logit))
                df_aup.append(average_precision_score(label, logit))

            df_auc = np.mean(df_auc)
            df_aup = np.mean(df_aup)

        else:
            df_auc = np.nan
            df_aup = np.nan

        # Logits for all node pairs
        # if pred_all and stage == 'test':
        #     logit_all_pair = (z @ z.t()).cpu()
        # else:
        #     logit_all_pair = None

        log = {
            f'{stage}_loss': loss,
            f'{stage}_dt_auc': dt_auc,
            f'{stage}_dt_aup': dt_aup,
            f'{stage}_df_auc': df_auc,
            f'{stage}_df_aup': df_aup,
            f'{stage}_df_logit_mean': np.mean(df_logit) if len(df_logit) > 0 else np.nan,
            f'{stage}_df_logit_std': np.std(df_logit) if len(df_logit) > 0 else np.nan
        }

        return loss, dt_auc, dt_aup, df_auc, df_aup, df_logit, None, log
    
    def decode(self, z, pos_edge_index, neg_edge_index=None):
        """
        Decodes the edge logits from node embeddings.

        This method computes the dot product between node embeddings for each edge to obtain 
        logits indicating the existence of edges. It can handle both positive and negative edges.

        Args:
            z (torch.Tensor): Node embeddings from the model.
                
            pos_edge_index (torch.Tensor): Indices of the positive (existing) edges.
                
            neg_edge_index (torch.Tensor, optional): Indices of the negative (non-existing) edges.
                                                    Defaults to None.

        Returns:
            torch.Tensor: Logits for the specified edges.
        """
        if neg_edge_index is not None:
            edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        else:
            edge_index = pos_edge_index
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        return logits

