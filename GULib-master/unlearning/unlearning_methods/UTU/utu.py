import copy
import os
import math
import torch
import numpy as np
from config import root_path
from torch_geometric.utils import to_undirected, is_undirected
from torch_geometric.utils import k_hop_subgraph, is_undirected, to_undirected, negative_sampling, subgraph
from task.edge_prediction import EdgePredictor
from utils.utils import split_forget_retain
from task.UtUTrainer import UtUTrainer
from config import BLUE_COLOR,RESET_COLOR
import time
class utu:
    def __init__(self, args, logger, model_zoo):
        self.args = args
        self.logger = logger
        self.model_zoo = model_zoo
        self.data = model_zoo.data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        num_runs = self.args["num_runs"]
        self.poison_f1 = np.zeros(self.args["num_runs"])
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_training_time = np.zeros(num_runs)

    def run_exp(self):
        for self.run in range(self.args["num_runs"]):
            self.train_gnn()
            self.delete_gnn()
        self.logger.info(
            "{}Performance Metrics:\n"
            " - Poison F1 Score: {:.4f} ± {:.4f}\n"
            " - Unlearn F1 Score: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
                BLUE_COLOR,
                np.mean(self.poison_f1), np.std(self.poison_f1),
                np.mean(self.average_f1), np.std(self.average_f1),
                np.mean(self.average_auc), np.std(self.average_auc),
                np.mean(self.avg_training_time), np.std(self.avg_training_time),
                RESET_COLOR
                )
            )
    def train_gnn(self):
        self.args["checkpoint_dir"] = root_path + '/data/UTU/checkpoint_node'
        self.args["checkpoint_dir"] = os.path.join(self.args["checkpoint_dir"], self.args["dataset_name"], self.args["base_model"], 'original',
                                           str(self.args["random_seed"]))
        os.makedirs(self.args["checkpoint_dir"], exist_ok=True)
        self.args['in_dim'] = self.data.x.shape[1]
        self.args['out_dim'] = self.data.num_classes
        self.args['unlearning_model'] = 'original'
        self.data = self.train_test_split_edges_no_neg_adj_mask(self.data)
        self.data.dtrain_mask = torch.ones(self.data.train_pos_edge_index.shape[1], dtype=torch.bool)
        train_pos_edge_index = to_undirected(self.data.train_pos_edge_index)
        self.data.train_pos_edge_index = train_pos_edge_index
        self.data.dtrain_mask = torch.ones(self.data.train_pos_edge_index.shape[1], dtype=torch.bool)
        self.EdgePredictor = EdgePredictor(self.args, self.data, self.model_zoo, self.logger)
        self.EdgePredictor.train_UTU_model()
        if self.args["poison"] and self.args["unlearn_task"]=="edge":
            self.poison_f1[self.run] = self.EdgePredictor.evaluate_model()

    def delete_gnn(self):
        self.args["checkpoint_dir"] = root_path + '/data/UTU/checkpoint_node'
        original_path = os.path.join(self.args["checkpoint_dir"], self.args["dataset_name"], self.args["base_model"], 'original', str(self.args["random_seed"]))
        attack_path_all = os.path.join(self.args["checkpoint_dir"], self.args["dataset_name"],self.args["base_model"], 'member_infer_all',
                                       str(self.args["random_seed"]))
        self.attack_dir = attack_path_all
        if not os.path.exists(attack_path_all):
            os.makedirs(attack_path_all, exist_ok=True)
        shadow_path_all = os.path.join(self.args["checkpoint_dir"],self.args["dataset_name"], self.args["base_model"], 'shadow_all', str(self.args["random_seed"]))
        self.shadow_dir = shadow_path_all
        if not os.path.exists(shadow_path_all):
            os.makedirs(shadow_path_all, exist_ok=True)
        self.args['unlearning_model'] = 'gnndelete'
        self.args["checkpoint_dir"] = os.path.join(
            self.args["checkpoint_dir"], self.args["dataset_name"], self.args["base_model"], 'unlearn',str(self.args["random_seed"]))
        os.makedirs(self.args["checkpoint_dir"], exist_ok=True)

        subset = 'in'
        self.data = split_forget_retain(self.data, self.args["df_size"], subset)
        self.args["unlearning_model"]="utu_del"
        self.EdgePredictor.model = self.model_zoo.get_model(self.data.sdf_node_1hop_mask, self.data.sdf_node_2hop_mask, num_nodes=self.data.num_nodes)
        if self.args["unlearning_model"] != 'retrain':  # Start from trained GNN model
            if os.path.exists(os.path.join(original_path, 'pred_proba.pt')):
                logits_ori = torch.load(os.path.join(original_path,
                                                     'pred_proba.pt'))  # logits_ori: tensor.shape([num_nodes, num_nodes]), represent probability of edge existence between any two nodes
                if logits_ori is not None:
                    logits_ori = logits_ori.to(self.device)
            else:
                logits_ori = None

            model_ckpt = torch.load(os.path.join(original_path, 'model_best.pt'), map_location=self.device)
            self.EdgePredictor.model.load_state_dict(model_ckpt['model_state'], strict=False)

        else:  # Initialize a new GNN model
            retrain = None
            logits_ori = None
        self.args["unlearning_model"] = "utu"
        if 'gnndelete' in self.args["unlearning_model"]:
            parameters_to_optimize = [
                {'params': [p for n, p in self.EdgePredictor.model.named_parameters() if 'del' in n], 'weight_decay': self.args["opt_decay"]}
            ]
            print('parameters_to_optimize', [n for n, p in self.EdgePredictor.model.named_parameters() if 'del' in n])
            if 'layerwise' in self.args["loss_type"]:
                optimizer1 = torch.optim.Adam(self.EdgePredictor.model.deletion1.parameters(), lr=self.args["unlearn_lr"])
                optimizer2 = torch.optim.Adam(self.EdgePredictor.model.deletion2.parameters(), lr=self.args["unlearn_lr"])
                optimizer = [optimizer1, optimizer2]
            else:
                optimizer = torch.optim.Adam(parameters_to_optimize, lr=self.args["unlearn_lr"])
        else:
            parameters_to_optimize = [
                {'params': [p for n, p in self.EdgePredictor.model.named_parameters()], 'weight_decay': self.args["opt_decay"]}
            ]
            print('parameters_to_optimize', [n for n, p in self.EdgePredictor.model.named_parameters()])
            optimizer = torch.optim.Adam(parameters_to_optimize, lr=self.args["unlearn_lr"])

        attack_model_all = None
        attack_model_sub = None

        trainer = UtUTrainer(self.args)
        start_time = time.time()
        trainer.train(self.EdgePredictor.model, self.data, optimizer, self.args, logits_ori, attack_model_all, attack_model_sub)
        self.avg_training_time[self.run] = time.time()-start_time
        if self.args["unlearning_model"] != 'retrain':
            retrain_path = os.path.join(
                'checkpoint', self.args["dataset"], self.args["base_model"], 'retrain',
                'model_best.pt')
            if os.path.exists(retrain_path):
                retrain_ckpt = torch.load(retrain_path, map_location=self.device)
                retrain_args = copy.deepcopy(self.args)
                retrain_args.unlearning_model = 'retrain'
                retrain = self.model_zoo.get_model(retrain_args, num_nodes=self.data.num_nodes, num_edge_type=self.args["num_edge_type"])
                retrain.load_state_dict(retrain_ckpt['model_state'])
                retrain = retrain.to(self.device)
                retrain.eval()
            else:
                retrain = None
        else:
            retrain = None

        test_results = trainer.test(self.EdgePredictor.model, self.data, model_retrain=retrain, attack_model_all=attack_model_all,
                                    attack_model_sub=attack_model_sub)

        self.average_f1[self.run] = test_results[1]
    def train_test_split_edges_no_neg_adj_mask(self, data, val_ratio: float = 0.05, test_ratio: float = 0.05,
                                               two_hop_degree=None):
        '''Avoid adding neg_adj_mask'''

        num_nodes = data.num_nodes
        row, col = data.edge_index
        edge_attr = data.edge_attr

        # Return upper triangular portion.
        mask = row < col
        row, col = row[mask], col[mask]

        if edge_attr is not None:
            edge_attr = edge_attr[mask]

        n_v = int(math.floor(val_ratio * row.size(0)))
        n_t = int(math.floor(test_ratio * row.size(0)))

        if two_hop_degree is not None:  # Use low degree edges for test sets
            low_degree_mask = two_hop_degree < 50

            low = low_degree_mask.nonzero().squeeze()
            high = (~low_degree_mask).nonzero().squeeze()

            low = low[torch.randperm(low.size(0))]
            high = high[torch.randperm(high.size(0))]

            perm = torch.cat([low, high])

        else:
            perm = torch.randperm(row.size(0))

        row = row[perm]
        col = col[perm]

        # Train
        r, c = row[n_v + n_t:], col[n_v + n_t:]
        data.train_pos_edge_index = torch.stack([r, c], dim=0)
        if edge_attr is not None:
            data.train_pos_edge_index, data.train_pos_edge_attr = None
        else:
            data.train_pos_edge_index = data.train_pos_edge_index

        assert not is_undirected(data.train_pos_edge_index)

        # Test
        r, c = row[:n_t], col[:n_t]
        data.test_pos_edge_index = torch.stack([r, c], dim=0)
        neg_edge_index = negative_sampling(
            edge_index=data.test_pos_edge_index,
            num_nodes=data.num_nodes,
            num_neg_samples=data.test_pos_edge_index.shape[1])

        data.test_neg_edge_index = neg_edge_index

        # Valid
        r, c = row[n_t:n_t + n_v], col[n_t:n_t + n_v]
        data.val_pos_edge_index = torch.stack([r, c], dim=0)

        neg_edge_index = negative_sampling(
            edge_index=data.val_pos_edge_index,
            num_nodes=data.num_nodes,
            num_neg_samples=data.val_pos_edge_index.shape[1])

        data.val_neg_edge_index = neg_edge_index

        return data

