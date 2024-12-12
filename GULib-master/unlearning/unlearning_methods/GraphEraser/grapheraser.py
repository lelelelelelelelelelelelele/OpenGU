import numpy as np
import networkx as nx
import time
import torch

import config
from task.node_classification import NodeClassifier
from unlearning.unlearning_methods.GraphEraser.aggregation.aggregator import Aggregator
from utils.dataset_utils import *
import config
from utils.utils import *
from torch_geometric.data import Data
from unlearning.unlearning_methods.GraphEraser.partition.graph_partition import GraphPartition
from utils import utils, dataset_utils
from dataset.original_dataset import *
from attack.Attack_methods.GraphEraser_MIA import GraphEraser_Attack
from task.edge_prediction import EdgePredictor
from task import get_trainer
BLUE_COLOR = "\033[34m"
RESET_COLOR = "\033[0m"

class grapheraser:
    def __init__(self,args,original_data,logger,model_zoo):
        self.args = args
        self.args["unlearn_trainer"] = 'BaseTrainer'
        self.original_data = original_data
        self.data = model_zoo.data
        self.model_zoo = model_zoo
        self.logger = logger
        self.partition_method = self.args['partition_method']
        self.num_shards = self.args['num_shards']
        self.target_model_name = self.args['base_model']
        # 假设 num_runs 是一个整数，表示运行的次数
        num_runs = self.args["num_runs"]
        self.run = 0
        # 初始化数组的大小为 num_runs
        self.average_f1 = np.zeros(num_runs)
        self.average_auc = np.zeros(num_runs)
        self.avg_partition_time = np.zeros(num_runs)
        self.avg_training_time = np.zeros(num_runs)
        self.avg_unlearning_time = np.zeros(num_runs)

    

    def run_exp(self):
        self.args["exp"] = "partition"
        self.train_test_split()
        self.gen_train_graph()
        self.graph_partition()
        self.generate_shard_data()
        self.args["exp"] = "unlearning"
        self.shard_data = dataset_utils.load_shard_data(self.logger)
        self.train_data = dataset_utils.load_saved_data(self.logger, config.train_data_file)
        self.unlearned_shard_data = self.shard_data
        self.logger.info(self.shard_data)
        self.target_model = get_trainer(self.args, self.logger, self.model_zoo.model,self.data)
        self.run_exp_train()


        self.args["exp"] = "attack_unlearning"
        for self.run in range(self.args["num_runs"]):
            self.train_test_split()
            self.model_zoo.data = self.data
            GraphEraser_Attack(self.args, self.logger, self.original_data, self.model_zoo,self.avg_unlearning_time,self.average_f1,self.average_auc,self.run)




        # 输出带有红色文字的日志
        self.logger.info(
            "{}Performance Metrics:\n"
            " - Average F1 Score: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average Partition Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Training Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
                BLUE_COLOR,
                np.mean(self.average_f1), np.std(self.average_f1),
                np.mean(self.average_auc), np.std(self.average_auc),
                np.mean(self.avg_partition_time), np.std(self.avg_partition_time),
                np.mean(self.avg_training_time), np.std(self.avg_training_time),
                np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
                np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
                RESET_COLOR
            )
        )


    


    def train_test_split(self):
        if not self.args['is_split']:
            self.logger.info('splitting train/test data')
            self.data.train_indices, self.data.test_indices = train_test_split(np.arange((self.data.num_node)),train_size = 0.6,test_size=self.args['test_ratio'], random_state=100)
            save_train_test_split(self.logger,self.args,self.data.train_indices, self.data.test_indices)

            self.data.train_mask = torch.from_numpy(np.isin(np.arange(self.data.num_node), self.data.train_indices))
            self.data.test_mask = torch.from_numpy(np.isin(np.arange(self.data.num_node), self.data.test_indices))
            print(self.data.train_indices.size, self.data.test_indices.size)
        else:
            self.data = load_train_test_split(self.logger)
            # self.data.train_indices, self.data.test_indices

            self.data.train_mask = torch.from_numpy(np.isin(np.arange(self.data.num_node), self.data.train_indices))
            self.data.test_mask = torch.from_numpy(np.isin(np.arange(self.data.num_node), self.data.test_indices))



    def gen_train_graph(self):
        edge_index = self.data.edge_index.numpy()

        test_edge_indices = np.logical_or(np.isin(edge_index[0], self.data.test_indices),
                                        np.isin(edge_index[1], self.data.test_indices))
        train_edge_indices = np.logical_not(test_edge_indices)
        edge_index_train = edge_index[:, train_edge_indices]

        self.train_graph = nx.Graph()
        self.train_graph.add_nodes_from(self.data.train_indices)

        # use largest connected graph as train graph
        if self.args['is_prune']:
            self._prune_train_set()

        # reconstruct a networkx train graph
        for u, v in np.transpose(edge_index_train):
            self.train_graph.add_edge(u, v)

        self.logger.info("After edge deletion. train graph  #.Nodes: %f, #.Edges: %f" % (
            self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))
        self.logger.info("After edge deletion. train data  #.Nodes: %f, #.Edges: %f" % (
            self.data.num_node, self.data.num_edges))
        save_train_data(self.logger, self.data, config.train_data_file)
        save_train_graph(self.logger, self.train_graph, config.train_graph_file)

    # def gen_train_graph_del_edge(self):
    #     edge_index = self.data.edge_index.numpy()
    #     self.train_graph = nx.Graph()
    #     self.train_graph.add_nodes_from(self.data.train_indices)
    #     #for edge-level task 10/14
    #     if self.args["unlearn_task"] == "edge" :
    #         train_edge_indices = np.logical_and(np.isin(edge_index[0], self.data.train_indices),
    #                                 np.isin(edge_index[1], self.data.train_indices))

    #     # 过滤出满足 edge_index[0] < edge_index[1] 的边，构成单向边
    #     directed_train_edges = np.logical_and(train_edge_indices, edge_index[0] < edge_index[1])

    #     # 获取这些单向边的索引
    #     train_edges = np.where(directed_train_edges)[0]

    #     # 计算需要删除的边的数量 (5%)
    #     num_edges_to_remove = int(len(train_edges) * 0.05)

    #     # 随机选择 5% 的单向边
    #     edges_to_remove = np.random.choice(train_edges, size=num_edges_to_remove, replace=False)

    #     # 找到与这些单向边对应的反向边
    #     reverse_edges_to_remove = np.where(
    #         (edge_index[0][None, :] == edge_index[1][edges_to_remove][:, None]) &
    #         (edge_index[1][None, :] == edge_index[0][edges_to_remove][:, None])
    #     )[1]

    #     # 合并正向边和反向边的索引
    #     all_edges_to_remove = np.concatenate([edges_to_remove, reverse_edges_to_remove])

    #     # 创建掩码，初始为 train_edge_indices，表示只对 train 边进行操作
    #     mask = train_edge_indices.copy()

    #     # 将选中的边对标记为 False，表示要删除
    #     mask[all_edges_to_remove] = False

    #     # 应用掩码保留剩下的边
    #     edge_index_train = edge_index[:, mask]


    #     # reconstruct a networkx train graph
    #     for u, v in np.transpose(edge_index_train):
    #         self.train_graph.add_edge(u, v)

    #     self.logger.info("After edge deletion. train graph  #.Nodes: %f, #.Edges: %f" % (
    #         self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))
    #     self.logger.info("After edge deletion. train data  #.Nodes: %f, #.Edges: %f" % (
    #         self.data.num_node, self.data.num_edges))
    #     save_train_data(self.logger,self.data,config.train_data_file)
    #     save_train_graph(self.logger,self.train_graph,config.train_graph_file)

    # def gen_train_graph_del_feature(self):
    #     edge_index = self.data.edge_index.numpy()

    #     test_edge_indices = np.logical_or(np.isin(edge_index[0], self.data.test_indices),
    #                                     np.isin(edge_index[1], self.data.test_indices))
    #     train_edge_indices = np.logical_not(test_edge_indices)
    #     edge_index_train = edge_index[:, train_edge_indices]

    #     self.train_graph = nx.Graph()
    #     self.train_graph.add_nodes_from(self.data.train_indices)
    #     #for feature-level task 10/14
    
    #     if self.args["unlearn_task"] == "feature" and self.args["exp"] == "attack_unlearning":
    #         path_un = config.unlearning_path + "_" + str(self.run) + ".txt"
    #         if os.path.exists(path_un):
    #             with open(path_un) as file:
    #                 node_unlearning_indices = [int(line.rstrip()) for line in file]
    #         self.data.x[node_unlearning_indices] = torch.zeros_like(self.data.x[node_unlearning_indices])
    #     # reconstruct a networkx train graph
    #     for u, v in np.transpose(edge_index_train):
    #         self.train_graph.add_edge(u, v)

    #     self.logger.info("After edge deletion. train graph  #.Nodes: %f, #.Edges: %f" % (
    #         self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))
    #     self.logger.info("After edge deletion. train data  #.Nodes: %f, #.Edges: %f" % (
    #         self.data.num_node, self.data.num_edges))
    #     save_train_data(self.logger,self.data,config.train_data_file)
    #     save_train_graph(self.logger,self.train_graph,config.train_graph_file)

    # def gen_train_graph_del_edge(self):
    #     edge_index = self.data.edge_index.numpy()
    #     self.train_graph = nx.Graph()
    #     self.train_graph.add_nodes_from(self.data.train_indices)
    #     #for edge-level task 10/14
    #     if self.args["unlearn_task"] == "edge" :
    #         train_edge_indices = np.logical_and(np.isin(edge_index[0], self.data.train_indices),
    #                                 np.isin(edge_index[1], self.data.train_indices))

    #     # 过滤出满足 edge_index[0] < edge_index[1] 的边，构成单向边
    #     directed_train_edges = np.logical_and(train_edge_indices, edge_index[0] < edge_index[1])

    #     # 获取这些单向边的索引
    #     train_edges = np.where(directed_train_edges)[0]

    #     # 计算需要删除的边的数量 (5%)
    #     num_edges_to_remove = int(len(train_edges) * 0.05)

    #     # 随机选择 5% 的单向边
    #     edges_to_remove = np.random.choice(train_edges, size=num_edges_to_remove, replace=False)

    #     # 找到与这些单向边对应的反向边
    #     reverse_edges_to_remove = np.where(
    #         (edge_index[0][None, :] == edge_index[1][edges_to_remove][:, None]) &
    #         (edge_index[1][None, :] == edge_index[0][edges_to_remove][:, None])
    #     )[1]

    #     # 合并正向边和反向边的索引
    #     all_edges_to_remove = np.concatenate([edges_to_remove, reverse_edges_to_remove])

    #     # 创建掩码，初始为 train_edge_indices，表示只对 train 边进行操作
    #     mask = train_edge_indices.copy()

    #     # 将选中的边对标记为 False，表示要删除
    #     mask[all_edges_to_remove] = False

    #     # 应用掩码保留剩下的边
    #     edge_index_train = edge_index[:, mask]


    #     # reconstruct a networkx train graph
    #     for u, v in np.transpose(edge_index_train):
    #         self.train_graph.add_edge(u, v)

    #     self.logger.info("After edge deletion. train graph  #.Nodes: %f, #.Edges: %f" % (
    #         self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))
    #     self.logger.info("After edge deletion. train data  #.Nodes: %f, #.Edges: %f" % (
    #         self.data.num_node, self.data.num_edges))
    #     save_train_data(self.logger,self.data,config.train_data_file)
    #     save_train_graph(self.logger,self.train_graph,config.train_graph_file)

    # def gen_train_graph_del_feature(self):
    #     edge_index = self.data.edge_index.numpy()

    #     test_edge_indices = np.logical_or(np.isin(edge_index[0], self.data.test_indices),
    #                                     np.isin(edge_index[1], self.data.test_indices))
    #     train_edge_indices = np.logical_not(test_edge_indices)
    #     edge_index_train = edge_index[:, train_edge_indices]

    #     self.train_graph = nx.Graph()
    #     self.train_graph.add_nodes_from(self.data.train_indices)
    #     #for feature-level task 10/14
    
    #     if self.args["unlearn_task"] == "feature" and self.args["exp"] == "attack_unlearning":
    #         path_un = config.unlearning_path + "_" + str(self.run) + ".txt"
    #         if os.path.exists(path_un):
    #             with open(path_un) as file:
    #                 node_unlearning_indices = [int(line.rstrip()) for line in file]
    #         self.data.x[node_unlearning_indices] = torch.zeros_like(self.data.x[node_unlearning_indices])
    #     # reconstruct a networkx train graph
    #     for u, v in np.transpose(edge_index_train):
    #         self.train_graph.add_edge(u, v)

    #     self.logger.info("After edge deletion. train graph  #.Nodes: %f, #.Edges: %f" % (
    #         self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))
    #     self.logger.info("After edge deletion. train data  #.Nodes: %f, #.Edges: %f" % (
    #         self.data.num_node, self.data.num_edges))
    #     save_train_data(self.logger,self.data,config.train_data_file)
    #     save_train_graph(self.logger,self.train_graph,config.train_graph_file)

    def graph_partition(self):

        if self.args['is_partition']:
            self.logger.info('graph partitioning')

            start_time = time.time()
            partition = GraphPartition(self.logger, self.args,self.train_graph, self.data)
            self.community_to_node = partition.graph_partition()
            partition_time = time.time() - start_time
            self.logger.info("Partition cost %s seconds." % partition_time)
            self.avg_partition_time[self.run]  = partition_time

            save_community_data(self.logger, self.community_to_node, config.community_path)
        else:
            self.community_to_node = load_community_data(self.logger, config.community_path)

        self.logger.info(partition)

    def generate_shard_data(self):
        self.shard_path = config.shard_file
        # self.logger.info('generating shard data')

        self.shard_data = {}
        for shard in range(self.args['num_shards']):
            train_shard_indices = list(self.community_to_node[shard])
            shard_indices = np.union1d(train_shard_indices, self.data.test_indices)

            x = self.data.x[shard_indices]
            y = self.data.y[shard_indices]
            edge_index = utils.filter_edge_index_1(self.data, shard_indices)

            data = Data(x=x, edge_index=torch.from_numpy(edge_index), y=y)
            if self.args["base_model"] == "SIGN":
                data = SIGN(self.args["GNN_layer"])(data)
                data.xs = [data.x] + [data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
                # data.xs = torch.tensor([x.detach().numpy() for x in data.xs]).cuda()
                data.xs = torch.stack(data.xs).cuda()
                data.xs = data.xs.transpose(0, 1)

            data.train_mask = torch.from_numpy(np.isin(shard_indices, train_shard_indices))
            data.test_mask = torch.from_numpy(np.isin(shard_indices, self.data.test_indices))
            # utils.get_inductive_edge(data)
            # utils.get_inductive_edge(data)

            self.shard_data[shard] = data
            self.logger.info(data)
        save_shard_data(self.logger,self.shard_data,self.shard_path)

    def run_exp_train(self):
        self.train_target_models(self.run)
        aggregate_f1_score = self.aggregate(self.run)
        self.average_f1[self.run] = aggregate_f1_score

        self.train_target_models(self.run)
        aggregate_f1_score = self.aggregate(self.run)
        self.average_f1[self.run] = aggregate_f1_score

    

    def _ratio_delete_edges(self, edge_index):
        edge_index = edge_index.numpy()

        unique_indices = np.where(edge_index[0] < edge_index[1])[0]
        unique_indices_not = np.where(edge_index[0] > edge_index[1])[0]
        remain_indices = np.random.choice(unique_indices,
                                           int(unique_indices.shape[0] * (1.0 - self.args['ratio_deleted_edges'])),
                                           replace=False)

        remain_encode = edge_index[0, remain_indices] * edge_index.shape[1] * 2 + edge_index[1, remain_indices]
        unique_encode_not = edge_index[1, unique_indices_not] * edge_index.shape[1] * 2 + edge_index[0, unique_indices_not]
        sort_indices = np.argsort(unique_encode_not)
        remain_indices_not = unique_indices_not[sort_indices[np.searchsorted(unique_encode_not, remain_encode, sorter=sort_indices)]]
        remain_indices = np.union1d(remain_indices, remain_indices_not)

        # self.data.edge_index = torch.from_numpy(edge_index[:, remain_indices])
        return torch.from_numpy(edge_index[:, remain_indices])

    def _prune_train_set(self):
        # extract the the maximum connected component
        self.logger.debug("Before Prune...  #. of Nodes: %f, #. of Edges: %f" % (
            self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))

        self.train_graph = max(connected_component_subgraphs(self.train_graph), key=len)

        self.logger.debug("After Prune... #. of Nodes: %f, #. of Edges: %f" % (
            self.train_graph.number_of_nodes(), self.train_graph.number_of_edges()))

    def train_target_models(self, run):
        if self.args['is_train_target_model']:
            self.logger.info('training target models')

            self.time = {}
            for shard in range(self.args['num_shards']):
                self.time[shard] = self._train_model(run, shard)
                self.avg_training_time[self.run] += self.time[shard]
            self.avg_training_time[self.run] = self.avg_training_time[self.run]/ self.args['num_shards']/self.args["num_epochs"]

    def _train_model(self, run, shard):
        self.logger.info('training target models, run %s, shard %s' % (run, shard))

        start_time = time.time()
        self.target_model.data = self.unlearned_shard_data[shard]
        # if self.args["base_model"] == "SIGN":
        #     self.target_model.data = SIGN(self.args["GNN_layer"])(self.target_model.data)
        #     self.target_model.data.xs = [self.target_model.data.x] + [self.target_model.data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
        #     self.target_model.data.xs = torch.tensor([x.detach().numpy() for x in self.target_model.data.xs]).cuda()
        #     self.target_model.data.xs = self.target_model.data.xs.transpose(0, 1)

        #9.20self.target_model.train_model()
        self.target_model.train()


        #nodeClassifier = NodeClassifier(self.args, self.target_model.data, self.model_zoo, self.logger)
        train_time = time.time() - start_time
        save_target_model(self.logger,self.args,run, self.target_model, shard)

        return train_time

    def aggregate(self, run):
        self.logger.info('aggregating submodels')

        # posteriors, true_label = self.generate_posterior()
        aggregator = Aggregator(run, self.target_model, self.train_data, self.unlearned_shard_data, self.args,self.logger)
        aggregator.generate_posterior()
        self.aggregate_f1_score = aggregator.aggregate(self.data)

        self.logger.info("Final Test F1: %s" % (self.aggregate_f1_score,))
        return self.aggregate_f1_score


