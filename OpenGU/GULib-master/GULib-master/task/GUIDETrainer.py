import torch.nn.functional as F
import torch
import numpy as np
from task.BaseTrainer import BaseTrainer
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

class GUIDETrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)
    

    def train_node_fullbatch(self,save=False):
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



    @torch.no_grad()
    def prediction_info(self):
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        y_pred = self.model(self.data.x, self.data.edge_index).cpu()
        y = self.data.y.cpu()
        return y_pred[self.data.test_mask.cpu()], y[self.data.test_mask.cpu()]