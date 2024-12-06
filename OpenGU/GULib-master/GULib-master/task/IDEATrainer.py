import torch
import numpy as np
from task.BaseTrainer import BaseTrainer
import time
from sklearn.metrics import f1_score
import torch.nn.functional as F
from tqdm import tqdm
from torch.autograd import grad
from torch_geometric.loader import NeighborSampler
from torch_geometric.nn.conv.gcn_conv import gcn_norm
class IDEATrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)
        self.target_model_name = self.args["base_model"]
        self.attack_preparations = {}
        self.loss_all = None
    
    
    def evaluate(self, run):
        self.logger.info('model evaluation')

        start_time = time.time()
        posterior = self.posterior()
        test_f1 = f1_score(
            self.data.y[self.data['test_mask']].cpu().numpy(), 
            posterior.argmax(axis=1).cpu().numpy(), 
            average="micro"
        )

        evaluate_time = time.time() - start_time
        self.logger.info("Evaluation cost %s seconds." % evaluate_time)

        self.logger.info("Final Test F1: %s" % (test_f1,))
        return test_f1
    
    
    
    def idea_train(self,unlearn_info=None):
        self.logger.info("training model")
        self.model.train()
        self.model.reset_parameters()
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self.data.y = self.data.y.squeeze().to(self.device)
        self._gen_train_loader()

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)

        for epoch in tqdm(range(int(self.args['num_epochs']))):

            optimizer.zero_grad()
            if self.target_model_name in ['GCN','SGC']:
                out = self.model.forward_once(self.data, self.edge_weight)

            else:
                out = self.model.forward_once(self.data)
            
            loss = F.nll_loss(out[self.data.train_mask], self.data.y[self.data.train_mask])
            loss.backward()
            optimizer.step()

        grad_all, grad1, grad2 = None, None, None

        if self.target_model_name in ['GCN','SGC']:
            out1 = self.model.forward_once(self.data, self.edge_weight)
            out2 = self.model.forward_once_unlearn(self.data, self.edge_weight_unlearn)

        else:
            out1 = self.model.forward_once(self.data)
            out2 = self.model.forward_once_unlearn(self.data)
        
        if self.args["unlearn_task"] == "edge":
            mask1 = np.array([False] * out1.shape[0])
            mask1[unlearn_info[2]] = True
            mask2 = mask1
        if self.args["unlearn_task"] == "node":
            mask1 = np.array([False] * out1.shape[0])
            mask1[unlearn_info[0]] = True
            mask1[unlearn_info[2]] = True
            mask2 = np.array([False] * out2.shape[0])
            mask2[unlearn_info[2]] = True
        if self.args["unlearn_task"] == "feature" or 'partial_feature':
            mask1 = np.array([False] * out1.shape[0])
            mask1[unlearn_info[1]] = True
            mask1[unlearn_info[2]] = True
            mask2 = mask1

        loss = F.nll_loss(out1[self.data.train_mask], self.data.y[self.data.train_mask], reduction='sum')
        loss1 = F.nll_loss(out1[mask1], self.data.y[mask1], reduction='sum')
        loss2 = F.nll_loss(out2[mask2], self.data.y[mask2], reduction='sum')
        model_params = [p for p in self.model.parameters() if p.requires_grad]
        grad_all = grad(loss, model_params, retain_graph=True, create_graph=True)
        grad1 = grad(loss1, model_params, retain_graph=True, create_graph=True)
        grad2 = grad(loss2, model_params, retain_graph=True, create_graph=True)

        self.loss_all = loss

        return (grad_all, grad1, grad2)
    
    def train_model_continue(self, unlearn_info=None):
        self.logger.info("training model continue")
        self.model.train()
        self._gen_train_loader()

        optimizer = torch.optim.Adam(self.model.parameters(), lr=(self.model.config.lr / 1e2), weight_decay=self.model.config.decay) 
        training_mask = self.data.train_mask.clone()
        if unlearn_info[0] is not np.array([]):
            training_mask[unlearn_info[0]] = False

        for epoch in tqdm(range(int(self.args['num_epochs'] * 0.1))):
            optimizer.zero_grad()
            if self.target_model_name in ['GCN','SGC']:
                out = self.model.forward_once_unlearn(self.data, self.edge_weight_unlearn)

            else:
                out = self.model.forward_once_unlearn(self.data)

            loss = F.nll_loss(out[training_mask], self.data.y[training_mask])
            loss.backward()
            optimizer.step()

    def evaluate_unlearn_F1(self, new_parameters=None):

        if new_parameters is not None:
            idx = 0
            for p in self.model.parameters():
                p.data = new_parameters[idx]
                idx = idx + 1

        self.model.eval()

        if self.target_model_name in ['GCN','SGC']:
            out = self.model.forward_once_unlearn(self.data, self.edge_weight_unlearn)
        else:
            out = self.model.forward_once_unlearn(self.data)
        self.attack_preparations["predicted_prob"] = 0

        self.attack_preparations["unlearned_feature_pre"] = 0

        test_f1 = f1_score(
            self.data.y[self.data['test_mask']].cpu().numpy(), 
            out[self.data['test_mask']].argmax(axis=1).cpu().numpy(), 
            average="micro"
        )
        return test_f1
    
    @torch.no_grad()
    def evaluate_model(self):
        self.model.eval()
        self.model, self.data = self.model.to(self.device), self.data.to(self.device)
        self._gen_test_loader()

        if self.target_model_name in ['GCN','SGC']:
            out = self.model(self.data.x, self.test_loader, self.edge_weight, self.device)
        else:
            out = self.model(self.data.x, self.test_loader, self.device)

        y_true = self.data.y.cpu().unsqueeze(-1)
        y_pred = out.argmax(dim=-1, keepdim=True)

        results = []
        for mask in [self.data.train_mask, self.data.test_mask]:
            results += [int(y_pred[mask].eq(y_true[mask]).sum()) / int(mask.sum())]

        return results
    

    
    def eval_hessian(self, loss_grad, model):
        cnt = 0
        for g in loss_grad:
            g_vector = g.contiguous().view(-1) if cnt == 0 else torch.cat([g_vector, g.contiguous().view(-1)])
            cnt = 1
        l = g_vector.size(0)
        hessian = torch.zeros(l, l).to(loss_grad[0].device)
        for idx in range(l):
            grad2rd = torch.autograd.grad(g_vector[idx], model.parameters(), create_graph=True)
            cnt = 0
            for g in grad2rd:
                g2 = g.contiguous().view(-1) if cnt == 0 else torch.cat([g2, g.contiguous().view(-1)])
                cnt = 1
            hessian[idx] = g2
        return hessian
    
    def _gen_train_loader(self):
        self.logger.info("generate train loader")
        train_indices = np.nonzero(self.data.train_mask.cpu().numpy())[0]
        edge_index = self.filter_edge_index(self.data.edge_index, train_indices, reindex=False)
        if edge_index.shape[1] == 0:
            edge_index = torch.tensor([[1, 2], [2, 1]])

        self.train_loader = NeighborSampler(
            edge_index, node_idx=self.data.train_mask,
            sizes=[5, 5], num_nodes=self.data.num_nodes,
            batch_size=self.args['batch_size'], shuffle=True,
            num_workers=0)
        if self.target_model_name in ['GCN','SGC']:
            _, self.edge_weight = gcn_norm(
                self.data.edge_index, 
                edge_weight=None, 
                num_nodes=self.data.x.shape[0],
                add_self_loops=False)

            _, self.edge_weight_unlearn = gcn_norm(
                self.data.edge_index_unlearn, 
                edge_weight=None, 
                num_nodes=self.data.x.shape[0],
                add_self_loops=False)

        self.logger.info("generate train loader finish")
        
    def filter_edge_index(self,edge_index, node_indices, reindex=True):
        assert np.all(np.diff(node_indices) >= 0), 'node_indices must be sorted'
        if isinstance(edge_index, torch.Tensor):
            edge_index = edge_index.cpu()

        node_index = np.isin(edge_index, node_indices)
        col_index = np.nonzero(np.logical_and(node_index[0], node_index[1]))[0]
        edge_index = edge_index[:, col_index]

        if reindex:
            return np.searchsorted(node_indices, edge_index)
        else:
            return edge_index