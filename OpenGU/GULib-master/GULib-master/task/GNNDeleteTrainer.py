import torch.nn.functional as F
import torch
import os
import time
import numpy as np
import copy
from task.BaseTrainer import BaseTrainer
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score,recall_score
from attack.Attack_methods.GNNDelete_MIA import member_infer_attack
from torch_geometric.utils import negative_sampling
from utils.utils import get_loss_fct, trange, Reverse_CE
from config import root_path

class GNNDeleteTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    def train_node_fullbatch(self,save=False):
        time_sum = 0
        best_f1 = 0
        best_w = 0
        self.model.train()
        self.model.reset_parameters()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.model.config.lr, weight_decay=self.model.config.decay)
        for epoch in tqdm(range(self.args['num_epochs']), desc="BaseTraining", unit="epoch"):
            start_time = time.time()
            self.model.train()
            self.optimizer.zero_grad()
            if self.args["base_model"] == "SIGN" or self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" :
                out = self.model(self.data.features_pre)
            else:
                out = self.model(self.data.x, self.data.edge_index)
            loss = F.cross_entropy(out[self.data.train_mask], self.data.y[self.data.train_mask]).to(self.device)
            loss.backward()
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
    

    @torch.no_grad()
    def test_node_fullbatch(self):
        self.model.eval()
        self.model = self.model.to(self.device)
        self.data = self.data.to(self.device)
        if self.args["base_model"] == "SIGN" or self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" :
            y_pred = self.model(self.data.features_pre).cpu()
        else:
            y_pred = self.model(self.data.x, self.data.edge_index).cpu()
        y = self.data.y.cpu()
        y_pred = np.argmax(y_pred, axis=1)
        f1 = f1_score(y[self.data.test_mask.cpu()], y_pred[self.data.test_mask.cpu()], average="micro")
        return f1


    def train_node_fullbatch_del(self, avg_time, run, optimizer, logits_ori=None, attack_model_all=None, attack_model_sub=None):
        self.trainer_log = {
            'unlearning_model': self.args["unlearning_model"],
            'dataset': self.args["dataset_name"],
            'log': []}
        self.model = self.model.to('cuda')
        self.data = self.data.to('cuda')

        best_metric = 0
        
        # MI Attack before unlearning
        if attack_model_all is not None:
            mi_logit_all_before, mi_sucrate_all_before = member_infer_attack(self.model, attack_model_all, self.data)
            self.trainer_log['mi_logit_all_before'] = mi_logit_all_before
            self.trainer_log['mi_sucrate_all_before'] = mi_sucrate_all_before
        if attack_model_sub is not None:
            mi_logit_sub_before, mi_sucrate_sub_before = member_infer_attack(self.model, attack_model_sub, self.data)
            self.trainer_log['mi_logit_sub_before'] = mi_logit_sub_before
            self.trainer_log['mi_sucrate_sub_before'] = mi_sucrate_sub_before

        non_df_node_mask = torch.ones(self.data.x.shape[0], dtype=torch.bool, device=self.data.x.device)
        non_df_node_mask[self.data.directed_df_edge_index.flatten().unique()] = False

        self.data.sdf_node_1hop_mask_non_df_mask = self.data.sdf_node_1hop_mask & non_df_node_mask
        self.data.sdf_node_2hop_mask_non_df_mask = self.data.sdf_node_2hop_mask & non_df_node_mask

        # Original node embeddings
        with torch.no_grad():
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
                z1_ori, z2_ori = self.model.get_original_embeddings(self.data.features_pre,return_all_emb=True)
            else:
                z1_ori, z2_ori = self.model.get_original_embeddings(self.data.x, self.data.edge_index[:, self.data.dr_mask],
                                                           return_all_emb=True)

        loss_fct = get_loss_fct(self.args["loss_fct"])

        neg_edge = neg_edge_index = negative_sampling(
            edge_index=self.data.edge_index,
            num_nodes=self.data.num_nodes,
            num_neg_samples=self.data.df_mask.sum())
        epoch_time = 0

        for epoch in trange(self.args["unlearning_epochs"], desc='Unlerning'):
            self.model.train()

            start_time = time.time()
            if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
                z1, z2 = self.model(self.data.features_pre, return_all_emb=True)
            else:    
                z1, z2 = self.model(self.data.x, self.data.edge_index[:, self.data.sdf_mask], return_all_emb=True)

            # Randomness
            pos_edge = self.data.edge_index[:, self.data.df_mask]


            embed1 = torch.cat([z1[pos_edge[0]], z1[pos_edge[1]]], dim=0)
            embed1_ori = torch.cat([z1_ori[neg_edge[0]], z1_ori[neg_edge[1]]], dim=0)

            embed2 = torch.cat([z2[pos_edge[0]], z2[pos_edge[1]]], dim=0)
            embed2_ori = torch.cat([z2_ori[neg_edge[0]], z2_ori[neg_edge[1]]], dim=0)

            loss_r1 = loss_fct(embed1, embed1_ori)
            loss_r2 = loss_fct(embed2, embed2_ori)

            # Local causality
            loss_l1 = loss_fct(z1[self.data.sdf_node_1hop_mask_non_df_mask], z1_ori[self.data.sdf_node_1hop_mask_non_df_mask])
            loss_l2 = loss_fct(z2[self.data.sdf_node_2hop_mask_non_df_mask], z2_ori[self.data.sdf_node_2hop_mask_non_df_mask])

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
            self.logger.info("time:{}".format(epoch_time/self.args["num_epochs"]))
            if (epoch + 1) % self.args["test_freq"] == 0:
                valid_loss, dt_acc,recall, dt_f1, valid_log = self.eval_node_fullbatch_del('val')
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
                        'model_state': self.model.state_dict(),
                        # 'optimizer_state': [optimizer[0].state_dict(), optimizer[1].state_dict()],
                    }
                    torch.save(ckpt, os.path.join(self.args["checkpoint_dir"],'model_best.pt'))
        avg_time[run] = epoch_time/self.args["unlearning_epochs"]  
        # Save
        ckpt = {
            'model_state': {k: v.to('cpu') for k, v in self.model.state_dict().items()},
            # 'optimizer_state': [optimizer[0].state_dict(), optimizer[1].state_dict()],
        }
        torch.save(ckpt, os.path.join(self.args["checkpoint_dir"], 'model_final.pt'))

    @torch.no_grad()
    def test_node_fullbatch_del(self, model_retrain=None, attack_model_all=None, attack_model_sub=None, ckpt='best'):

        if ckpt == 'best':  # Load best ckpt
            ckpt = torch.load(os.path.join(self.args["checkpoint_dir"], 'model_best.pt'))
            self.model.load_state_dict(ckpt['model_state'])

        if 'ogbl' in self.args["dataset_name"]:
            pred_all = False
        else:
            pred_all = True
        loss, dt_acc, recall,dt_f1, test_log = self.eval_node_fullbatch_del('test', pred_all)

        self.trainer_log['dt_loss'] = loss
        self.trainer_log['dt_acc'] = dt_acc
        self.trainer_log['dt_f1'] = dt_f1
        # self.trainer_log['df_logit'] = df_logit
        # self.logit_all_pair = logit_all_pair
        # self.trainer_log['df_auc'] = df_auc
        # self.trainer_log['df_aup'] = df_aup

        if model_retrain is not None:  # Deletion
            self.trainer_log['ve'] = self.verification_error(self.model, model_retrain).cpu().item()
            # self.trainer_log['dr_kld'] = output_kldiv(model, model_retrain, self.data=self.data).cpu().item()

        # MI Attack after unlearning
        if attack_model_all is not None:
            mi_logit_all_after, mi_sucrate_all_after = member_infer_attack(self.model, attack_model_all, self.data)
            self.trainer_log['mi_logit_all_after'] = mi_logit_all_after
            self.trainer_log['mi_sucrate_all_after'] = mi_sucrate_all_after
        if attack_model_sub is not None:
            mi_logit_sub_after, mi_sucrate_sub_after = member_infer_attack(self.model, attack_model_sub, self.data)
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
    def eval_node_fullbatch_del(self,stage='val', pred_all=False):
        self.model.eval()

        # DT AUC AUP
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            z = self.model(self.data.features_pre)
        else:
            z = self.model(self.data.x, self.data.edge_index)
        loss = F.cross_entropy(z[self.data.test_mask], self.data.y[self.data.test_mask]).cpu().item()
        pred = torch.argmax(z[self.data.test_mask], dim=1).cpu()
        true_lable = self.data.y[self.data.test_mask]
        dt_acc = accuracy_score(self.data.y[self.data.test_mask].cpu(), pred)
        recall = recall_score(self.data.y[self.data.test_mask].cpu(), pred,average='micro')
        dt_f1 = f1_score(self.data.y[self.data.test_mask].cpu(), pred, average='micro')

        # DF AUC AUP
        # if self.args.unlearning_model in ['original', 'original_node']:
        #     df_logit = []
        # else:
        #     df_logit = self.model.decode(z, self.data.directed_df_edge_index).sigmoid().tolist()

        # if len(df_logit) > 0:
        #     df_auc = []
        #     df_aup = []

        #     # Sample pos samples
        #     if len(self.df_pos_edge) == 0:
        #         for i in range(500):
        #             mask = torch.zeros(self.data.train_pos_edge_index[:, self.data.dr_mask].shape[1], dtype=torch.bool)
        #             idx = torch.randperm(self.data.train_pos_edge_index[:, self.data.dr_mask].shape[1])[:len(df_logit)]
        #             mask[idx] = True
        #             self.df_pos_edge.append(mask)

        #     # Use cached pos samples
        #     for mask in self.df_pos_edge:
        #         pos_logit = self.model.decode(z, self.data.train_pos_edge_index[:, self.data.dr_mask][:, mask]).sigmoid().tolist()

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
            self.model = self.model.to(self.device)

        return loss, dt_acc,recall, dt_f1, log