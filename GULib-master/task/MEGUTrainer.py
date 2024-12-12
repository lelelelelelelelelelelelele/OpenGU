import torch.nn.functional as F
import time
import torch
import copy
import numpy as np
from tqdm import tqdm
from task import BaseTrainer
from config import root_path
from sklearn.metrics import f1_score, accuracy_score,recall_score,roc_auc_score
from torch_geometric.transforms import SIGN
from utils.utils import sparse_mx_to_torch_sparse_tensor,normalize_adj,propagate,criterionKD,calc_f1
from torch_geometric.utils import negative_sampling
from torch_geometric.nn import CorrectAndSmooth
class GATE(torch.nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.lr = torch.nn.Linear(dim, dim)

    def forward(self, x):
        t = x.clone()
        return self.lr(t)

class MEGUTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    def megu_unlearning(self,temp_node,neighbor_khop):
        self.temp_node = temp_node
        self.neighbor_khop = neighbor_khop
        operator = GATE(self.data.num_classes).to(self.device)
        optimizer = torch.optim.SGD(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        self.data = self.data.cuda()
            

        with torch.no_grad():
            self.model.eval()
            if self.args["base_model"] == "SIGN":
                preds = self.model(self.data.xs)
            else:
                preds = self.model(self.data.x,self.data.edge_index)
                preds_edge = preds
            if self.args['dataset_name'] == 'ppi':
                preds = torch.sigmoid(preds).ge(0.5)
                preds = preds.type_as(self.data.y)
            else:           
                preds = torch.argmax(preds, axis=1).type_as(self.data.y)
            
        if self.args["base_model"] == "SIGN":
            self.data.x = self.data.x_unlearn
            self.data.edge_index = self.data.edge_index_unlearn
            self.data = SIGN(self.args["GNN_layer"])(self.data)
            self.data.xs = [self.data.x] + [self.data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
            self.data.xs = torch.stack(self.data.xs).to('cuda')
            self.data.xs = self.data.xs.transpose(0,1)

        start_time = time.time()
        for epoch in tqdm(range(self.args["unlearning_epochs"]),desc="Unlearning"):
            self.model.train()
            operator.train()
            optimizer.zero_grad()
            if self.args["base_model"] == "SIGN":
                out_ori =  self.model(self.data.xs)
            else:
                out_ori = self.model(self.data.x_unlearn, self.data.edge_index_unlearn)
            out = operator(out_ori)
            # if self.args["downstream_task"]=="node":
            if self.args['dataset_name'] == 'ppi':
                loss_u = criterionKD(out_ori[self.temp_node], out[self.temp_node]) - F.binary_cross_entropy_with_logits(out[self.temp_node], preds[self.temp_node])
                loss_r = criterionKD(out[self.neighbor_khop], out_ori[self.neighbor_khop]) + F.binary_cross_entropy_with_logits(out_ori[self.neighbor_khop], preds[self.neighbor_khop])
            else:
                loss_u = criterionKD(out_ori[self.temp_node], out[self.temp_node]) - F.cross_entropy(out[self.temp_node], preds[self.temp_node])
                loss_r = criterionKD(out[self.neighbor_khop], out_ori[self.neighbor_khop]) + F.cross_entropy(out_ori[self.neighbor_khop], preds[self.neighbor_khop])
            # elif self.args["downstream_task"]=="edge":
            #     neg_edge_index = negative_sampling(
            #         edge_index=self.data.edge_index_unlearn,num_nodes=self.data.num_nodes,
            #         num_neg_samples=self.data.edge_index_unlearn.size(1)
            #     )
            #     mask = np.isin(self.data.edge_index_unlearn.cpu().numpy(), self.data.edge_index.cpu().numpy()).astype(np.uint8)
            #     neg_edge_label = torch.zeros(neg_edge_index.size(1), dtype=torch.float32)
            #     pos_edge_label = torch.ones(neg_edge_index.size(1),dtype=torch.float32)
            #     edge_labels = torch.cat((pos_edge_label,neg_edge_label),dim=-1)
            #     edge_logits = self.decode(z=out, pos_edge_index=self.data.edge_index_unlearn,neg_edge_index=neg_edge_index)
                
            #     if self.args['dataset_name'] == 'ppi':
            #         loss_u = criterionKD(out_ori[self.temp_node], out[self.temp_node]) - F.binary_cross_entropy_with_logits(edge_logits, edge_preds[mask])
            #         loss_r = criterionKD(out[self.neighbor_khop], out_ori[self.neighbor_khop]) + F.binary_cross_entropy_with_logits(out_ori[self.neighbor_khop], preds[self.neighbor_khop])
            loss = self.args['kappa'] * loss_u + loss_r

            loss.backward()
            optimizer.step()

        unlearn_time = time.time() - start_time
        self.model.eval()
        if self.args["base_model"] == "SIGN":
            test_out =  self.model(self.data.xs)
        else:
            test_out = self.model(self.data.x_unlearn, self.data.edge_index_unlearn)
        if self.args['dataset_name'] == 'ppi':
            out = torch.sigmoid(test_out)
        else:
            out = self.correct_and_smooth(F.softmax(test_out, dim=-1), preds)
        if self.args["downstream_task"]=="node":
            y_hat = out.cpu().detach().numpy()
            y = self.data.y.cpu()
            if self.args['dataset_name'] == 'ppi':
                test_f1 = calc_f1(y, y_hat, self.data.test_mask, multilabel=True)
            else:
                test_f1 = calc_f1(y, y_hat, self.data.test_mask)
        elif self.args["downstream_task"]=="edge":
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
            test_f1 = roc_auc_score(edge_labels.cpu(), edge_pred.cpu())

        return unlearn_time, test_f1
    
    
    def correct_and_smooth(self, y_soft, preds):
        pos = CorrectAndSmooth(num_correction_layers=80, correction_alpha=self.args['alpha1'],
                               num_smoothing_layers=80, smoothing_alpha=self.args['alpha2'],
                               autoscale=False, scale=1.)

        y_soft = pos.correct(y_soft, preds[self.data.train_mask], self.data.train_mask,
                                  self.data.edge_index_unlearn)
        y_soft = pos.smooth(y_soft, preds[self.data.train_mask], self.data.train_mask,
                                 self.data.edge_index_unlearn)
        
        return y_soft
