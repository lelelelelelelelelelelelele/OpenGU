import copy
import math
import os
import pickle
import numpy as np
import torch
import torch.nn.functional as F
from ogb.linkproppred import PygLinkPropPredDataset
from sklearn.metrics import roc_auc_score
from torch_geometric import seed_everything
from torch_geometric.datasets import CitationFull, Coauthor, Flickr
import torch_geometric.transforms as T
from torch_geometric.utils import to_networkx
from torch_geometric.utils import train_test_split_edges, k_hop_subgraph, negative_sampling, to_undirected, is_undirected, to_networkx
from tqdm import tqdm
from model.base_gnn.Convs import S2GConv,SGConv,GCNConv
from task.node_classification import NodeClassifier
from utils.dataset_utils import load_saved_data
from utils.utils import negative_sampling_kg, plot_auc
from utils.utils import to_directed
from config import root_path,unlearning_path
from config import BLUE_COLOR,RESET_COLOR
from task import get_trainer
from task.edge_prediction import EdgePredictor

class gnndelete:
    def __init__(self,args,logger,model_zoo,dataset):
        self.args= args
        self.model_zoo = model_zoo
        self.data = self.model_zoo.data
        # self.data.train_mask = self.data.val_mask = self.data.test_mask = None
        self.logger = logger
        self.dataset = dataset
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        num_runs = self.args["num_runs"]
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_time = np.zeros(num_runs)
        self.run = 0
        

        # seed_everything(self.args['random_seed'])
        # self.prepare_dataset()
        # if self.args["base_model"] == "SGC":
        #     propagation = SGConv(self.data.num_features,self.data.num_classes,K=3,bias=False)
        #     features_pre = propagation.forward_SGU(self.data.x,self.data.edge_index)
        #     self.data.features_pre = features_pre.cuda()
        # elif self.args["base_model"] == "S2GC":
        #     propagation = S2GConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
        #     features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
        #     self.data.features_pre = features_pre.cuda()
        # elif self.args["base_model"] == "SIGN":
        #     self.data.xs = torch.tensor([x.detach().numpy() for x in self.data.xs]).cuda()
        #     self.data.xs = self.data.xs.transpose(0,1)
        #     self.data.features_pre = self.data.xs
        # for self.run in range(10):
        #     self.train_node(self.data)
        #     self.delete_node()

        # self.logger.info("average_f1:{}±{}".format(np.mean(self.average_f1),np.std(self.average_f1)))
        # self.logger.info("average_auc:{}±{}".format(np.mean(self.average_auc),np.std(self.average_auc)))
        # self.logger.info("avg_time:{}±{}".format(np.mean(self.avg_time),np.std(self.avg_time)))
        
    def run_exp(self):
        if self.args["base_model"] == "SGC":
            propagation = SGConv(self.data.num_features,self.data.num_classes,K=3,bias=False)
            features_pre = propagation.forward_SGU(self.data.x,self.data.edge_index)
            self.data.features_pre = features_pre.cuda()
        elif self.args["base_model"] == "S2GC":
            propagation = S2GConv(self.data.num_features, self.data.num_classes, K=3, bias=False)
            features_pre = propagation.forward_SGU(self.data.x, self.data.edge_index)
            self.data.features_pre = features_pre.cuda()
        elif self.args["base_model"] == "SIGN":
            # self.data.xs = torch.tensor([x.detach().numpy() for x in self.data.xs]).cuda()
            # self.data.xs = self.data.xs.transpose(0,1)
            self.data.features_pre = self.data.xs
        for self.run in range(self.args["num_runs"]):
            self.args["unlearn_trainer"] = "GNNDeleteTrainer"
            self.train_node(self.data,retrain=True)
            # self.args["unlearn_trainer"] = "GNNDeleteTrainer"
            self.delete_node()

        self.logger.info(
            "{}Performance Metrics:\n"
            " - Average F1 Score: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average Training Time: {:.4f} ± {:.4f} seconds\n".format(
                BLUE_COLOR,
                np.mean(self.average_f1), np.std(self.average_f1),
                np.mean(self.average_auc), np.std(self.average_auc),
                np.mean(self.avg_time), np.std(self.avg_time),
                RESET_COLOR
            )
        )

    def prepare_dataset(self):
        df_size = [i / 100 for i in range(10)] + [i / 10 for i in range(10)] + [i for i in range(10)]  # Df_size in percentage
        seeds = [42, 21, 13, 87, 100]
        self.graph = to_networkx(self.data)

        # Get two hop degree for all nodes
        node_to_neighbors = {}
        for n in tqdm(self.graph.nodes(), desc='Two hop neighbors'):
            neighbor_1 = set(self.graph.neighbors(n))
            neighbor_2 = sum([list(self.graph.neighbors(i)) for i in neighbor_1], [])
            neighbor_2 = set(neighbor_2)
            neighbor = neighbor_1 | neighbor_2

            node_to_neighbors[n] = neighbor

        two_hop_degree = []
        row, col = self.data.edge_index
        mask = row < col
        row, col = row[mask], col[mask]
        for r, c in tqdm(zip(row, col), total=len(row)):
            neighbor_row = node_to_neighbors[r.item()]
            neighbor_col = node_to_neighbors[c.item()]
            neighbor = neighbor_row | neighbor_col

            num = len(neighbor)

            two_hop_degree.append(num)

        two_hop_degree = torch.tensor(two_hop_degree)

        for s in seeds:
            seed_everything(s)

            # D
            data = self.data
            if self.args["dataset_name"] == 'ogbl':
                data = self.train_test_split_edges_no_neg_adj_mask(data, test_ratio=0.1, two_hop_degree=two_hop_degree)
            else:
                data = self.train_test_split_edges_no_neg_adj_mask(data, test_ratio=0.2)
            print(s, data)

            with open(root_path + "/data/GNNDelete/" + self.args["dataset_name"]+ "/" + f'd_{s}.pkl', 'wb') as f:
                pickle.dump((self.dataset, data), f)

            _, local_edges, _, mask = k_hop_subgraph(
                data.test_pos_edge_index.flatten().unique(),
                2,
                data.train_pos_edge_index,
                num_nodes=self.dataset[0].num_nodes)
            distant_edges = data.train_pos_edge_index[:, ~mask]
            print('Number of edges. Local: ', local_edges.shape[1], 'Distant:', distant_edges.shape[1])

            in_mask = mask
            out_mask = ~mask

            # df_in_mask = torch.zeros_like(mask)
            # df_out_mask = torch.zeros_like(mask)

            # df_in_all_idx = in_mask.nonzero().squeeze()
            # df_out_all_idx = out_mask.nonzero().squeeze()
            # df_in_selected_idx = df_in_all_idx[torch.randperm(df_in_all_idx.shape[0])[:df_size]]
            # df_out_selected_idx = df_out_all_idx[torch.randperm(df_out_all_idx.shape[0])[:df_size]]

            # df_in_mask[df_in_selected_idx] = True
            # df_out_mask[df_out_selected_idx] = True

            # assert (in_mask & out_mask).sum() == 0
            # assert (df_in_mask & df_out_mask).sum() == 0

            # local_edges = set()
            # for i in range(data.test_pos_edge_index.shape[1]):
            #     edge = data.test_pos_edge_index[:, i].tolist()
            #     subgraph = get_enclosing_subgraph(graph, edge)
            #     local_edges = local_edges | set(subgraph[2])

            # distant_edges = graph.edges() - local_edges

            # print('aaaaaaa', len(local_edges), len(distant_edges))
            # local_edges = torch.tensor(sorted(list([i for i in local_edges if i[0] < i[1]])))
            # distant_edges = torch.tensor(sorted(list([i for i in distant_edges if i[0] < i[1]])))

            # df_in = torch.randperm(local_edges.shape[1])[:df_size]
            # df_out = torch.randperm(distant_edges.shape[1])[:df_size]

            # df_in = local_edges[:, df_in]
            # df_out = distant_edges[:, df_out]

            # df_in_mask = torch.zeros(data.train_pos_edge_index.shape[1], dtype=torch.bool)
            # df_out_mask = torch.zeros(data.train_pos_edge_index.shape[1], dtype=torch.bool)

            # for row in df_in:
            #     i = (data.train_pos_edge_index.T == row).all(axis=1).nonzero()
            #     df_in_mask[i] = True

            # for row in df_out:
            #     i = (data.train_pos_edge_index.T == row).all(axis=1).nonzero()
            #     df_out_mask[i] = True

            save_path = os.path.join("./data/GNNDelete", self.args["dataset_name"])
            os.makedirs(save_path, exist_ok=True)
            torch.save(
                {'out': out_mask, 'in': in_mask},
                os.path.join(save_path, f'df_{s}.pt')
            )

    def train_test_split_edges_no_neg_adj_mask(self,data, val_ratio: float = 0.2, test_ratio: float = 0.2,
                                               two_hop_degree=None, kg=False):
        '''Avoid adding neg_adj_mask'''
        num_nodes = data.num_nodes
        row, col = data.edge_index
        edge_attr = data.edge_attr

        if not kg:
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
        train_mask = torch.zeros(num_nodes, dtype=torch.bool)
        train_mask[r] = train_mask[c] = True
        data.train_mask = train_mask

        data.train_pos_edge_index = torch.stack([r, c], dim=0)
        if edge_attr is not None:
            out = to_undirected(data.train_pos_edge_index, edge_attr[n_v + n_t:])
            data.train_pos_edge_index, data.train_pos_edge_attr = out
        else:
            data.train_pos_edge_index = data.train_pos_edge_index
            # data.train_pos_edge_index = to_undirected(data.train_pos_edge_index)

        assert not is_undirected(data.train_pos_edge_index)

        # Test
        r, c = row[:n_t], col[:n_t]
        test_mask = torch.zeros(num_nodes, dtype=torch.bool)
        test_mask[r] = test_mask[c] = True
        data.test_mask = test_mask
        data.test_pos_edge_index = torch.stack([r, c], dim=0)
        neg_edge_index = negative_sampling(
            edge_index=data.test_pos_edge_index,
            num_nodes=data.num_nodes,
            num_neg_samples=data.test_pos_edge_index.shape[1])

        data.test_neg_edge_index = neg_edge_index

        # Valid
        r, c = row[n_t:n_t + n_v], col[n_t:n_t + n_v]
        val_mask = torch.zeros(num_nodes, dtype=torch.bool)
        val_mask[r] = val_mask[c] = True
        data.val_mask = val_mask
        data.val_pos_edge_index = torch.stack([r, c], dim=0)

        neg_edge_index = negative_sampling(
            edge_index=data.val_pos_edge_index,
            num_nodes=data.num_nodes,
            num_neg_samples=data.val_pos_edge_index.shape[1])

        data.val_neg_edge_index = neg_edge_index

        return data

    def train_node(self,data = None,retrain=False):
        self.args["checkpoint_dir"] = root_path + '/data/GNNDelete/checkpoint_node'
        data = data.to(self.device)
        self.args['in_dim'] = data.x.shape[1]
        self.args['out_dim'] = self.dataset.num_classes
        self.args['unlearning_model'] = 'original'
        model = self.model_zoo.get_model(num_nodes=data.num_nodes).to(self.device)
        self.model_zoo.model = model
        #9.20
        # if self.args["downstream_task"]=="node":
        #     self.NodeClassifier = NodeClassifier(self.args, data, self.model_zoo, self.logger)
        # elif self.args["downstream_task"]=="edge":
        #     self.NodeClassifier = EdgePredictor(self.args, data, self.model_zoo, self.logger)
        self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)

        # if retrain:
        #     self.NodeClassifier.train_model(retrain=retrain)
        # else:
        #     self.NodeClassifier.train_model()
        
        if os.path.exists(os.path.join(root_path + "/data/model/node_level/",self.args["dataset_name"],self.args["base_model"])):
            model_ckpt = torch.load(os.path.join(root_path + "/data/model/node_level/",self.args["dataset_name"],self.args["base_model"]),
                                    map_location=self.device)
            # model.load_state_dict(model_ckpt['model_state'], strict=False)
            self.target_model.model.load_state_dict(model_ckpt, strict=False)
            self.target_model.model.to(self.device)
            
        else:
            self.target_model.train(save=True)
        
        # self.logger.info("original:{}".format(F1))
        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args["base_model"] == "SIGN":
            self.original_softlabels = F.softmax(self.target_model.model(self.data.features_pre), dim=1)
        else:
            self.original_softlabels = F.softmax(self.target_model.model(self.data.x, self.data.edge_index), dim=1)
        self.args["unlearning_model"] = 'gnndelete_nodeemb'





    def delete_node(self):
        # data_num = "13"
        # self.data = load_saved_data(self.logger,"data/GNNDelete/cora/" + "d_" + data_num + ".pkl")[1]
        self.args["checkpoint_dir"] = root_path + '/data/GNNDelete/checkpoint_node'
        original_path = os.path.join(self.args["checkpoint_dir"],self.args["dataset_name"],self.args["base_model"],'original',
                                                          '-'.join([str(i) for i in [self.args["df"], self.args["df_size"], self.args["random_seed"]]]))
        # if 'gnndelete' in self.args["unlearning_model"]:
        #     self.args["checkpoint_dir"] = os.path.join("data/GNNDelete/",
        #         self.args["checkpoint_dir"], self.args["dataset_name"], self.args["gnn"],
        #         f'{self.args["unlearning_model"]}-node_deletion',
        #         '-'.join([str(i) for i in [self.args["loss_fct"], self.args["loss_type"],
        #                                    self.args["alpha"], self.args["neg_sample_random"]]]),
        #         '-'.join([str(i) for i in [self.args["df"], self.args["df_size"], self.args["random_seed"]]])
        #     )
        # else:
        #     self.args["checkpoint_dir"] = os.path.join("data/GNNDelete/",
        #         self.args["checkpoint_dir"], self.args["dataset_name"], self.args["gnn"],
        #         f'{self.args["unlearning_model"]}-node_deletion',
        #         '-'.join([str(i) for i in [self.args["df"], self.args["df_size"], self.args["random_seed"]]])
        #     )

        os.makedirs(self.args["checkpoint_dir"], exist_ok=True)

        # Df and Dr
        # if self.args["df_size"] >= 100:  # df_size is number of nodes/edges to be deleted
            # df_size = int(self.args["df_size"])
        # else:  # df_size is the ratio
            # df_size = int(self.args["df_size"] / 100 * self.data["train_pos_edge_index"].shape[1])
        ############ set the number
        df_size = int(self.data.num_node * self.args["proportion_unlearned_nodes"])




        # print(f'Original size: {self.data["num_node"]:,}')
        # print(f'Df size: {df_size:,}')
        # print("data: {}".format(self.data))
        # Delete nodes

        #修改为从train——set里面找删除节点
        # shuffle_num = torch.randperm(len(self.data.train_indices))[:df_size]
        # df_nodes = np.array(self.data.train_indices)[shuffle_num]
        # np.savetxt("./data/SGU/unlearning_nodes.txt", df_nodes, fmt="%d")
        path_un = unlearning_path + "_" + str(self.run) + ".txt"
        df_nodes = np.loadtxt(path_un, dtype=int)
        self.unlearning_nodes = df_nodes
        df_nodes_set = set(df_nodes)
        all_exist = df_nodes_set.issubset(self.data.train_indices)
        global_node_mask = torch.ones(self.data.num_nodes, dtype=torch.bool)
        global_node_mask[df_nodes] = False

        dr_mask_node = global_node_mask
        df_mask_node = ~global_node_mask
        assert df_mask_node.sum() == df_size

        # Delete edges associated with deleted nodes from training set
        res = [torch.eq(self.data.edge_index, aelem).logical_or_(torch.eq(self.data.edge_index, aelem)) for aelem in df_nodes]
        # res = []
        # for aelem in df_nodes:
        #     comparison = torch.eq(self.data.edge_index, aelem)
        #     logical_or = torch.logical_or(comparison[0], comparison[1])
        #     res.append(logical_or)
        df_mask_edge = torch.any(torch.stack(res, dim=0), dim=0)
        df_mask_edge = df_mask_edge.sum(0).bool()
        dr_mask_edge = ~df_mask_edge

        df_edge = self.data.edge_index[:, df_mask_edge]
        self.data.directed_df_edge_index = to_directed(df_edge)

        # self.logger.info('Deleting the following nodes:{}'.format(df_nodes) )

        _, two_hop_edge, _, two_hop_mask = k_hop_subgraph(
            self.data.edge_index[:, df_mask_edge].flatten().unique(),
            2,
            self.data.edge_index,
            num_nodes=self.data.num_node)

        # Nodes in S_Df
        _, one_hop_edge, _, one_hop_mask = k_hop_subgraph(
            self.data.edge_index[:, df_mask_edge].flatten().unique(),
            1,
            self.data.edge_index,
            num_nodes=self.data.num_nodes)
        sdf_node_1hop = torch.zeros(self.data.num_nodes, dtype=torch.bool)
        sdf_node_2hop = torch.zeros(self.data.num_nodes, dtype=torch.bool)

        sdf_node_1hop[one_hop_edge.flatten().unique()] = True
        sdf_node_2hop[two_hop_edge.flatten().unique()] = True

        assert sdf_node_1hop.sum() == len(one_hop_edge.flatten().unique())
        assert sdf_node_2hop.sum() == len(two_hop_edge.flatten().unique())

        self.data.sdf_node_1hop_mask = sdf_node_1hop
        self.data.sdf_node_2hop_mask = sdf_node_2hop

        print(is_undirected(self.data.edge_index))

        two_hop_mask = two_hop_mask.bool()
        df_mask_edge = df_mask_edge.bool()
        dr_mask_edge = ~df_mask_edge

        # print('Undirected dataset:', self.data)evaluate_Del_model
        # print(is_undirected(train_pos_edge_index), train_pos_edge_index.shape, two_hop_mask.shape, df_mask.shape, two_hop_mask.shape)

        self.data.sdf_mask = two_hop_mask
        self.data.df_mask = df_mask_edge
        self.data.dr_mask = dr_mask_edge
        self.data.dtrain_mask = dr_mask_edge



        self.target_model.model = self.model_zoo.get_model(sdf_node_1hop, sdf_node_2hop, num_nodes=self.data.num_node)

        if self.args["unlearning_model"] != 'retrain':  # Start from trained GNN model
            if os.path.exists(os.path.join(original_path, 'pred_proba.pt')):
                logits_ori = torch.load(os.path.join(original_path, 'pred_proba.pt'))
                if logits_ori is not None:
                    logits_ori = logits_ori.to(self.device)
            else:
                logits_ori = None

            model_ckpt = torch.load(os.path.join(root_path + "/data/model/node_level/" ,self.args["dataset_name"], self.args["base_model"]), map_location=self.device)
            # model.load_state_dict(model_ckpt['model_state'], strict=False)
            self.target_model.model.load_state_dict(model_ckpt, strict=False)

        else:  # Initialize a new GNN model
            retrain = None
            logits_ori = None
        self.target_model.model.to(self.device)


        if 'gnndelete' in self.args["unlearning_model"] and 'nodeemb' in self.args["unlearning_model"]:
            parameters_to_optimize = [
                {'params': [p for n, p in self.target_model.model.named_parameters() if 'del' in n], 'weight_decay': 0.0}
            ]
            print('parameters_to_optimize', [n for n, p in self.target_model.model.named_parameters() if 'del' in n])
            if 'layerwise' in self.args["loss_type"]:
                optimizer1 = torch.optim.Adam(self.target_model.model.deletion1.parameters(), lr=self.args["unlearn_lr"])
                optimizer2 = torch.optim.Adam(self.target_model.model.deletion2.parameters(), lr=self.args["unlearn_lr"])
                optimizer = [optimizer1, optimizer2]
            else:
                optimizer = torch.optim.Adam(parameters_to_optimize, lr=self.args["unlearn_lr"])

        else:
            if 'gnndelete' in self.args["unlearning_model"]:
                parameters_to_optimize = [
                    {'params': [p for n, p in self.target_model.model.named_parameters() if 'del' in n], 'weight_decay': 0.0}
                ]
                print('parameters_to_optimize', [n for n, p in self.target_model.model.named_parameters() if 'del' in n])

            else:
                parameters_to_optimize = [
                    {'params': [p for n, p in self.target_model.model.named_parameters()], 'weight_decay': 0.0}
                ]
                print('parameters_to_optimize', [n for n, p in self.target_model.model.named_parameters()])

            optimizer = torch.optim.Adam(parameters_to_optimize, lr=self.args["unlearn_lr"])  # , weight_decay=args.weight_decay)

        # MI attack model
        attack_model_all = None
        # attack_model_all = MLPAttacker(args)
        # attack_ckpt = torch.load(os.path.join(attack_path_all, 'attack_model_best.pt'))
        # attack_model_all.load_state_dict(attack_ckpt['model_state'])
        # attack_model_all = attack_model_all.to(device)

        attack_model_sub = None
        # attack_model_sub = MLPAttacker(args)
        # attack_ckpt = torch.load(os.path.join(attack_path_sub, 'attack_model_best.pt'))
        # attack_model_sub.load_state_dict(attack_ckpt['model_state'])
        # attack_model_sub = attack_model_sub.to(device)

        #Train
        self.model_zoo.model = self.target_model.model
        self.args["unlearn_trainer"] = "GNNDeleteTrainer"
        self.target_model = get_trainer(self.args, self.logger,self.model_zoo.model, self.data)
        # self.NodeClassifier_Del.GNNDelete_train(self.logger,self.avg_time,self.run,self.NodeClassifier.model, self.data, optimizer, self.args, logits_ori, attack_model_all, attack_model_sub)
        self.target_model.train_node_fullbatch_del(self.avg_time, self.run, optimizer,logits_ori, attack_model_all, attack_model_sub)
        

        #Test
        # if self.args["unlearning_model"] != 'retrain':
        #     retrain_path = os.path.join(self.args["checkpoint_dir"],self.args["dataset_name"],self.args["gnn"],'retrain',
        #                                                   '-'.join([str(i) for i in [self.args["df"], self.args["df_size"], self.args["random_seed"]]]))
        #     retrain_ckpt = torch.load(os.path.join(retrain_path, 'model_best.pt'), map_location=self.device)
        #     retrain_args = copy.deepcopy(self.args)
        #     original_model = self.args["unlearning_model"]
        #     self.args["unlearning_model"] = 'retrain'
        #     retrain = self.model_zoo.get_model(num_nodes=self.data.num_nodes)
        #     self.args["unlearning_model"] =original_model
        #     retrain.load_state_dict(retrain_ckpt['model_state'])
        #     retrain = retrain.to(self.device)
        #     retrain.eval()


        # else:
        #     retrain = None

        # self.NodeClassifier_Del.GNNDelete_test(self.data, model_retrain=None, attack_model_all=attack_model_all,
        #              attack_model_sub=attack_model_sub)
        self.target_model.test_node_fullbatch_del(model_retrain=None, attack_model_all=attack_model_all,attack_model_sub=attack_model_sub)
        self.target_model.model.to(self.device)
        loss, dt_acc, recall, dt_f1, log = self.target_model.eval_node_fullbatch_del( 'test')
        self.logger.info(
            "Loss: {:.4f} | Accuracy: {:.4f} | Recall: {:.4f} | F1 Score: {:.4f}".format(
                loss, dt_acc, recall, dt_f1
            )
        )
        self.average_f1[self.run] = dt_acc
        # F1_score, Accuracy, Recall = self.NodeClassifier_Del.eval_unlearning(self.data.features_pre, self.unlearning_nodes)
        # self.logger.info(
            # 'Original Model Unlearning : F1_score = {}  Accuracy = {}  Recall = {}'.format(F1_score, Accuracy, Recall))

        ###MIA

        self.mia_num = df_size
        original_softlabels_member = self.original_softlabels[df_nodes]
        original_softlabels_non = self.original_softlabels[self.data.test_indices[:self.mia_num]]

        if self.args["base_model"] == "SGC" or self.args["base_model"] == "S2GC" or self.args[
            "base_model"] == "SIGN":
            unlearning_softlabels_member = self.target_model.model.get_softlabel(self.data.features_pre[df_nodes])
            unlearning_softlabels_non = self.target_model.model.get_softlabel(
                self.data.features_pre[self.data.test_indices[:self.mia_num]])
        else:
            unlearning_softlabels_member = F.softmax(self.target_model.model(self.data.x, self.data.edge_index)[
                df_nodes],dim = 1)
            unlearning_softlabels_non = F.softmax(self.target_model.model(
                self.data.x, self.data.edge_index)[self.data.test_indices[:self.mia_num]],dim=1)

        mia_test_y = torch.cat((torch.ones(self.mia_num), torch.zeros(self.mia_num)))
        posterior1 = torch.cat((original_softlabels_member, original_softlabels_non), 0).cpu().detach()
        posterior2 = torch.cat((unlearning_softlabels_member, unlearning_softlabels_non), 0).cpu().detach()
        posterior = np.array([np.linalg.norm(posterior1[i] - posterior2[i]) for i in range(len(posterior1))])
        # self.logger.info("posterior:{}".format(posterior))
        auc = roc_auc_score(mia_test_y, posterior.reshape(-1, 1))
        # self.logger.info("auc:{}".format(auc))
        self.average_auc[self.run] = auc
        plot_auc(mia_test_y, posterior.reshape(-1, 1))
