import os
import time
import json
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import trange, tqdm
from ogb.graphproppred import Evaluator
from torch_geometric.data import DataLoader
from torch_geometric.utils import negative_sampling
from torch_geometric.loader import GraphSAINTRandomWalkSampler
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score
from utils.utils import member_infer_attack,get_link_labels
from task.BaseTrainer import BaseTrainer
class UtUTrainer:
    def __init__(self,args):
        self.args = args
        self.trainer_log = {
            'unlearning_model': args["unlearning_model"],
            'dataset': args["dataset_name"],
            'log': []}
        self.logit_all_pair = None
        self.df_pos_edge = []
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # def freeze_unused_mask(self, model, edge_to_delete, subgraph, h):
    #     gradient_mask = torch.zeros_like(delete_model.operator)
    #
    #     edges = subgraph[h]
    #     for s, t in edges:
    #         if s < t:
    #             gradient_mask[s, t] = 1
    #     gradient_mask = gradient_mask.to(device)
    #     model.operator.register_hook(lambda grad: grad.mul_(gradient_mask))

    def train(self, model, data, optimizer, args, logits_ori=None, attack_model_all=None, attack_model_sub=None):
        if 'ogbl' in args["dataset_name"]:
            return self.train_fullbatch(model, data, optimizer, args, logits_ori, attack_model_all, attack_model_sub)

        else:
            return self.train_fullbatch(model, data, optimizer, args, logits_ori, attack_model_all, attack_model_sub)

    def train_fullbatch(self, model, data, optimizer, args, logits_ori=None, attack_model_all=None,
                        attack_model_sub=None):
        model = model.to(self.device)
        data = data.to(self.device)

        best_metric = 0
        loss_fct = nn.MSELoss()

        # MI Attack before unlearning
        if attack_model_all is not None:
            mi_logit_all_before, mi_sucrate_all_before = member_infer_attack(model, attack_model_all, data)
            self.trainer_log['mi_logit_all_before'] = mi_logit_all_before
            self.trainer_log['mi_sucrate_all_before'] = mi_sucrate_all_before
        if attack_model_sub is not None:
            mi_logit_sub_before, mi_sucrate_sub_before = member_infer_attack(model, attack_model_sub, data)
            self.trainer_log['mi_logit_sub_before'] = mi_logit_sub_before
            self.trainer_log['mi_sucrate_sub_before'] = mi_sucrate_sub_before
        z = model(data.x, data.train_pos_edge_index[:, data.dr_mask])
        # Save
        ckpt = {
            'model_state': model.state_dict(),
            'optimizer_state': optimizer.state_dict(),
        }
        torch.save(ckpt, os.path.join(self.args["checkpoint_dir"], 'model_best.pt'))
        torch.save(z, os.path.join(self.args["checkpoint_dir"], 'node_embeddings.pt'))
        self.trainer_log['best_metric'] = best_metric

    def train_minibatch(self, model, data, optimizer, args, logits_ori=None, attack_model_all=None,
                        attack_model_sub=None):
        start_time = time.time()
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

        # Save models and node embeddings
        print('Saving final checkpoint')
        ckpt = {
            'model_state': model.state_dict(),
            'optimizer_state': optimizer.state_dict(),
        }
        torch.save(ckpt, os.path.join(args["checkpoint_dir"], 'model_best.pt'))
        # torch.save(z, os.path.join(args.checkpoint_dir, 'node_embeddings.pt'))
        self.trainer_log['best_metric'] = best_metric

    @torch.no_grad()
    def test(self, model, data, model_retrain=None, attack_model_all=None, attack_model_sub=None, ckpt='best'):

        if ckpt == 'best' and self.args["unlearning_model"] != 'simple':  # Load best ckpt
            ckpt = torch.load(os.path.join(self.args["checkpoint_dir"], 'model_best.pt'), map_location=self.device)
            model.load_state_dict(ckpt['model_state'])

        if 'ogbl' in self.args["dataset"]:
            pred_all = False
        else:
            pred_all = True
        loss, dt_auc, dt_aup, df_auc, df_aup, df_logit, logit_all_pair, test_log = self.eval(model, data, 'test',
                                                                                             pred_all)

        self.trainer_log['dt_loss'] = loss
        self.trainer_log['dt_auc'] = dt_auc
        self.trainer_log['dt_aup'] = dt_aup
        # self.trainer_log['df_logit'] = df_logit
        self.logit_all_pair = logit_all_pair
        self.trainer_log['df_auc'] = df_auc
        self.trainer_log['df_aup'] = df_aup
        self.trainer_log['auc_sum'] = dt_auc + df_auc
        self.trainer_log['aup_sum'] = dt_aup + df_aup
        self.trainer_log['auc_gap'] = abs(dt_auc - df_auc)
        self.trainer_log['aup_gap'] = abs(dt_aup - df_aup)

        # if model_retrain is not None:    # Deletion
        #     self.trainer_log['ve'] = verification_error(model, model_retrain).cpu().item()
        # self.trainer_log['dr_kld'] = output_kldiv(model, model_retrain, data=data).cpu().item()

        # MI Attack after unlearning
        if attack_model_all is not None:
            mi_logit_all_after, mi_sucrate_all_after = member_infer_attack(model, attack_model_all, data)
            self.trainer_log['mi_logit_all_after'] = mi_logit_all_after
            self.trainer_log['mi_sucrate_all_after'] = mi_sucrate_all_after
            self.trainer_log['mi_ratio_all'] = np.mean([i[1] / j[1] for i, j in
                                                        zip(self.trainer_log['mi_logit_all_after'],
                                                            self.trainer_log['mi_logit_all_before'])])
            test_log['mi_sucrate'], test_log['mi_ratio'] = mi_sucrate_all_after, self.trainer_log['mi_ratio_all']
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
        return loss, dt_auc, dt_aup, df_auc, df_aup, df_logit, logit_all_pair, test_log

    def eval(self, model, data, stage='val', pred_all=False):
        model.eval()
        pos_edge_index = data[f'{stage}_pos_edge_index']
        neg_edge_index = data[f'{stage}_neg_edge_index']

        if self.args["eval_on_cpu"]:
            model = model.to('cpu')

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

        if self.args["eval_on_cpu"]:
            model = model.to(self.device)

        return loss, dt_auc, dt_aup, df_auc, df_aup, df_logit, None, log
    
    def decode(self, z, pos_edge_index, neg_edge_index=None):
        if neg_edge_index is not None:
            edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        else:
            edge_index = pos_edge_index
            logits = (z[edge_index[0]] * z[edge_index[1]]).sum(dim=-1)

        return logits