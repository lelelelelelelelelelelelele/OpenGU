from task.BaseTrainer import BaseTrainer
from sklearn.metrics import f1_score,roc_auc_score
import torch.nn.functional as F
from torch_geometric.utils import negative_sampling
import torch
class GIFTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)
        

    
    def eval_unlearn(self, new_parameters):
        idx = 0
        for p in self.model.parameters():
            p.data = new_parameters[idx]
            idx = idx + 1

        out = self.model.reason_once_unlearn(self.data)
        if self.args["downstream_task"]=="node":
            test_f1 = f1_score(
                self.data.y[self.data['test_mask']].cpu().numpy(),
                out[self.data['test_mask']].argmax(axis=1).cpu().numpy(),
                average="micro"
            )
        elif self.args["downstream_task"]=="edge":
            test_f1 = self.eval_unlearn_edge(out)
        elif self.args["downstream_task"]=="graph":
            test_f1 = self.evaluate_graph_model()
        return test_f1
    
    def eval_unlearn_edge(self,out):
        neg_edge_index = negative_sampling(
            edge_index=self.data.test_edge_index,num_nodes=self.data.num_nodes,
            num_neg_samples=self.data.test_edge_index.size(1)
        )
        # print(out.shape,self.data.test_edge_index,neg_edge_index)
        edge_pred_logits = self.decode(z=out, pos_edge_index=self.data.test_edge_index,neg_edge_index=neg_edge_index).sigmoid()
        # print(edge_pred_logits)
        # edge_pred_logits = torch.sigmoid(edge_pred_logits)
        # edge_pred_logits = edge_pred_logits.cpu()
        edge_pred = torch.where(edge_pred_logits > 0.5, torch.tensor(1), torch.tensor(0))
        edge_pred = edge_pred_logits.cpu()
        # edge_pred = torch.argmax(edge_pred_logits)
        # edge_labels = self.data.test_edge_labels
        pos_edge_labels = torch.ones(self.data.test_edge_index.size(1),dtype=torch.float32)
        neg_edge_labels = torch.zeros(neg_edge_index.size(1),dtype=torch.float32)
        edge_labels = torch.cat((pos_edge_labels,neg_edge_labels))
        AUC_score = roc_auc_score(edge_labels.detach().cpu(), edge_pred.detach().cpu())
        return AUC_score
    
    def get_loss(self, out, reduction="none"):
        neg_edge_index = negative_sampling(
                edge_index=self.data.edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.edge_index.size(1)
            )
        neg_edge_label = torch.zeros(neg_edge_index.size(1), dtype=torch.float32)
        pos_edge_label = torch.ones(self.data.edge_index.size(1),dtype=torch.float32)
        edge_logits = self.decode(z=out, pos_edge_index=self.data.edge_index,neg_edge_index=neg_edge_index)
        edge_labels = torch.cat((pos_edge_label,neg_edge_label),dim=-1)
        edge_labels = edge_labels.to(self.device)
        loss = F.binary_cross_entropy_with_logits(edge_logits, edge_labels, reduction=reduction)
        return loss
