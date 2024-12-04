import torch.nn.functional as F
import time
import torch
import copy
import numpy as np
from tqdm import tqdm
from task import BaseTrainer
from config import root_path
from sklearn.metrics import f1_score, accuracy_score,recall_score

class SGUTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    def train_node_fullbatch(self,save = False, retrain=False):
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        start_time = time.time()
        best_acc = 0
        best_w = 0
        for epoch in tqdm(range(self.args['num_epochs'])):
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
                F1_score, Accuracy, Recall = self.test_node_fullbatch(self.data.pre_features[self.data.test_indices])
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
    def test_node_fullbatch(self,test_features):
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