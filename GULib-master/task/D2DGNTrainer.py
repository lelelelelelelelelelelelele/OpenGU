from task.BaseTrainer import BaseTrainer
import torch
from tqdm import tqdm
import time
import torch.nn.functional as F
from config import root_path
import copy
import os
from torch_geometric.utils import negative_sampling
class D2DGNTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data,alpha=0.5):
        super().__init__(args, logger, model, data)
        self.alpha = alpha

    def d2dgn_train(self,preserver_knowledge,destroyer_knowledge,loss_fn,save=False):
        if self.args["downstream_task"] == 'node':
            return self.d2dgn_train_node(preserver_knowledge,destroyer_knowledge,loss_fn,save)
        else:
            return self.d2dgn_train_edge(preserver_knowledge,destroyer_knowledge,loss_fn,save)
        
    def d2dgn_train_node(self,preserver_knowledge,destroyer_knowledge,loss_fn,save=False):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        self.alpha = torch.tensor(self.alpha,dtype=torch.float,device=self.device)
        for epoch in tqdm(range(self.args['num_epochs']), desc="D2DGNTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if loss_fn== "KL":
                if self.args["base_model"] == "SIGN":
                    out = self.model(self.data.xs)
                else:
                    
                    out = self.model(self.data.x, self.data.edge_index)
                out = F.log_softmax(out,dim=-1)
                # print(out[self.data.keep_mask].shape)
                loss1 = F.kl_div(out[self.data.keep_mask],preserver_knowledge[self.data.keep_mask],reduction='batchmean')
                loss2 = F.kl_div(out[self.data.unlearn_mask],destroyer_knowledge[self.data.unlearn_mask],reduction='batchmean')
            elif loss_fn == "MSE":
                if self.args["base_model"] == "SIGN":
                    out = self.model(self.data.xs,return_all_emb=True)
                else:
                    out = self.model(self.data.x, self.data.edge_index,return_all_emb=True)

                loss_func = torch.nn.MSELoss(reduction="sum")
                loss1 = 0
                loss2 = 0
                for conv_out,know in zip(out,preserver_knowledge):
                    # conv_out=F.softmax(conv_out,dim=-1)
                    
                    loss1 += loss_func(conv_out[self.data.keep_mask],know[self.data.keep_mask])
                for conv_out,know in zip(out,destroyer_knowledge):
                    # conv_out=F.softmax(conv_out,dim=-1)
                    loss2 += loss_func(conv_out[self.data.unlearn_mask],know[self.data.unlearn_mask])
            
            loss = loss1 * self.alpha + loss2 * (1 - self.alpha)
            # print(loss)
            loss.backward(retain_graph=True)
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
        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_f1,avg_training_time
    

    def d2dgn_train_edge(self,preserver_knowledge,destroyer_knowledge,loss_fn,save=False):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr/10, weight_decay=self.model.config.decay)
        self.alpha = torch.tensor(self.alpha,dtype=torch.float,device=self.device)
        neg_edge_index = negative_sampling(
                edge_index=self.data.train_edge_index,num_nodes=self.data.num_nodes,
                num_neg_samples=self.data.train_edge_index.size(1)
            )
        if loss_fn == "KL":
            logits_preserver = self.decode(preserver_knowledge,self.data.keep_edge_index,neg_edge_index)
            logits_preserver = torch.sigmoid(logits_preserver)
            logits_preserver = torch.clamp(logits_preserver, min=1e-5, max=1-1e-5)
            logits_preserver = torch.stack([logits_preserver,1-logits_preserver],dim=1)

            logits_destroyer = self.decode(destroyer_knowledge,self.data.unlearn_edge_index,neg_edge_index)
            logits_destroyer = torch.sigmoid(logits_destroyer)
            logits_destroyer = torch.clamp(logits_destroyer, min=1e-5, max=1-1e-5)
            logits_destroyer = torch.stack([logits_destroyer,1-logits_destroyer],dim=1)
        else:
            logits_preserver = []
            logits_destroyer = []
            for i,know in enumerate(preserver_knowledge):
                logits_preserver.append(self.decode(know,self.data.keep_edge_index,neg_edge_index))
            for i,know in enumerate(destroyer_knowledge):
                logits_destroyer.append(self.decode(know,self.data.unlearn_edge_index,neg_edge_index)) 
        for epoch in tqdm(range(self.args['num_epochs']), desc="D2DGNTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if loss_fn== "KL":
                if self.args["base_model"] == "SIGN":
                    out = self.model(self.data.xs)
                else:
                    
                    out = self.model(self.data.x, self.data.train_edge_index)

                logits_keep = self.decode(out,self.data.keep_edge_index,neg_edge_index)
                logits_keep = torch.sigmoid(logits_keep)
                logits_keep = torch.clamp(logits_keep, min=1e-5, max=1-1e-5)
                logits_keep = torch.log(torch.stack([logits_keep,1-logits_keep],dim=1))
                # print(logits_keep)

                logits_unlearn = self.decode(out,self.data.unlearn_edge_index,neg_edge_index)
                logits_unlearn = torch.sigmoid(logits_unlearn)
                logits_unlearn = torch.clamp(logits_unlearn, min=1e-5, max=1-1e-5)
                logits_unlearn = torch.log(torch.stack([logits_unlearn,1-logits_unlearn],dim=1))
                
                loss1 = F.kl_div(logits_keep,logits_preserver,reduction="batchmean")
                loss2 = F.kl_div(logits_unlearn,logits_destroyer,reduction="batchmean")
            elif loss_fn == "MSE":
                if self.args["base_model"] == "SIGN":
                    out = self.model(self.data.xs,return_all_emb=True)
                else:
                    out = self.model(self.data.x, self.data.edge_index,return_all_emb=True)

                loss_func = torch.nn.MSELoss(reduction="sum")
                loss1 = 0
                loss2 = 0
                for conv_out,logit_preserver in zip(out,logits_preserver):
                    logit_keep = self.decode(conv_out,self.data.keep_edge_index,neg_edge_index)
                    loss1 += loss_func(logit_keep,logit_preserver)
                for conv_out,logit_destroyer in zip(out,logits_destroyer):
                    logit_unlearn = self.decode(conv_out,self.data.unlearn_edge_index,neg_edge_index)
                    loss2 += loss_func(logit_unlearn,logit_destroyer)
            # print(loss1,loss2)
            loss = loss1 * self.alpha + loss2 * (1 - self.alpha)
            
            loss.backward(retain_graph=True)
            self.optimizer.step()
            time_sum += time.time() - start_time


            
            #test#
            if (epoch + 1) % self.args["test_freq"] == 0:
                f1 = self.evaluate_edge_model()
                if f1 > best_f1:
                    best_f1 = f1
                    if save:
                        best_w = copy.deepcopy(self.model.state_dict())
                
                self.logger.info('Epoch: {:03d} | F1 Score: {:.4f} | Loss: {:.4f}'.format(epoch + 1, f1, loss))

        avg_training_time = time_sum / self.args['num_epochs']
        self.logger.info("Average training time per epoch: {:.4f}s".format(avg_training_time))
        model_path = root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"] + "/" + self.args["base_model"]
        os.makedirs(root_path + "/data/model/" + self.args["unlearn_task"] + "_level/" + self.args["dataset_name"], exist_ok=True)
        self.save_model(model_path,best_w)
        return best_f1,avg_training_time
    
        
