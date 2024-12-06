import logging
import os
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import torch
import pickle
import torch_geometric.transforms as T
import networkx as nx
from ogb.linkproppred import PygLinkPropPredDataset
from ogb.nodeproppred import PygNodePropPredDataset
from torch_geometric.datasets import Planetoid, Coauthor, Flickr, Amazon, CitationFull,PPI,Reddit
from utils.dataset_utils import is_data_exists, load_saved_data, save_data
from torch_geometric.transforms import SIGN
from config import root_path,split_ratio
from dataset.ppi_data import ppi_data


class original_dataset:
    def __init__(self,args,logger):
        self.args = args
        self.dataset_name = self.args['dataset_name']
        self.num_features = {
            "cora": 1433,
            "pubmed": 500,
            "citeseer": 3703,
            "CS": 6805,
            "Physics": 8415,
            'flickr': 500,
            "ppi": 50,
            "Computers": 767,
            "Photo": 745,
            "ogbn-arxiv":128,
            "DBLP":334,
            "ogbn-products":100
        }
        self.base_model = self.args['base_model']
        self.logger = logger


    def load_data(self):
        """ get the original data and split according to inductive or transductive
        """
        if self.args["is_transductive"]:
            if self.args['is_balanced']:
                data_filename = './data/processed/transductive/'+self.args['dataset_name']+ split_ratio +'_balanced.pkl'
                dataset_filename = './data/processed/transductive/'+self.args['dataset_name'] +  split_ratio +"dataset" +'_balanced.pkl'
            else:
                data_filename = './data/processed/transductive/'+self.args['dataset_name']+ split_ratio +'.pkl'
                dataset_filename = './data/processed/transductive/'+self.args['dataset_name'] +  split_ratio +"dataset" +'.pkl'
        else:
            if self.args['is_balanced']:
                data_filename = './data/processed/inductive/'+self.args['dataset_name']+ split_ratio +'_balanced.pkl'
                dataset_filename = './data/processed/inductive/'+self.args['dataset_name'] +  split_ratio +"dataset" +'_balanced.pkl'
            else:
                data_filename = './data/processed/inductive/' + self.args['dataset_name'] +  split_ratio +'.pkl'
                dataset_filename = './data/processed/inductive/' + self.args['dataset_name'] +  split_ratio +"dataset" + '.pkl'
        if is_data_exists(data_filename) and is_data_exists(dataset_filename):
            self.logger.info("Data already saved! "+ data_filename)
            data = load_saved_data(self.logger,data_filename)
            dataset = load_saved_data(self.logger, dataset_filename)
            return data, dataset

        if self.dataset_name in ["cora", "pubmed", "citeseer"]:
            dataset = Planetoid(root_path + '/data/raw', self.dataset_name, transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.dataset_name in ["CS", "Physics"]:
            dataset = Coauthor(root_path + '/data/raw', self.dataset_name, pre_transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.dataset_name == 'flickr':
            dataset = Flickr(root_path + '/data/raw/flickr' ,self.dataset_name, pre_transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.args["dataset_name"] == 'Reddit':
            dataset = Reddit(root_path + '/data/raw/Reddit')
            data = dataset._data
        elif self.args["dataset_name"] == "ppi":
            train_datasets = PPI(root='./data/raw/ppi', split='train')
            val_datasets = PPI(root='./data/raw/ppi', split='val')
            test_datasets = PPI(root='./data/raw/ppi', split='test')
            all_data = []
            for train_dataset in train_datasets:
                all_data.append(train_dataset)
            for val_dataset in val_datasets:
                all_data.append(val_dataset)
            for test_dataset in test_datasets:
                all_data.append(test_dataset)
            ppi_ = ppi_data(all_data)
            ppi_.train_y = torch.cat([data.y for data in all_data[:20]], dim=0)
            ppi_.test_y = torch.cat([data.y for data in all_data[22:24]], dim=0)
            return ppi_,ppi_
        elif self.dataset_name in ['Computers','Photo']:
            dataset = Amazon(root_path + '/data/raw', self.dataset_name, transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.dataset_name in ['DBLP']:
            dataset = CitationFull(root_path + '/data/raw', self.args["dataset_name"], transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.args["dataset_name"] == 'obgl' and self.args["unlearning_methods"] == "CEU":
            dataset = PygLinkPropPredDataset(root_path + '/data/raw')
            data = dataset._data
        elif self.args["dataset_name"] in ['ogbn-arxiv', 'ogbn-products']:
            dataset = PygNodePropPredDataset(name=self.dataset_name, root = root_path + '/data/raw')
            ogb_data = dataset[0]
            ogb_data = T.ToUndirected()(ogb_data)
            split_idx = dataset.get_idx_split()


            mask = torch.zeros(ogb_data.x.size(0))
            mask[split_idx['train']] = 1
            ogb_data.train_mask = mask.to(torch.bool)
            ogb_data.train_indices = split_idx['train']

            mask = torch.zeros(ogb_data.x.size(0))
            mask[split_idx['valid']] = 1
            ogb_data.val_mask = mask.to(torch.bool)
            ogb_data.val_indices = split_idx['valid']

            mask = torch.zeros(ogb_data.x.size(0))
            mask[split_idx['test']] = 1
            ogb_data.test_mask = mask.to(torch.bool)
            ogb_data.test_indices = split_idx['test']

            ogb_data.y = ogb_data.y.flatten()
            data = ogb_data

        else:
            raise Exception('unsupported dataset')

        # data = SIGN(self.args["GNN_layer"])(data)
        # data.xs = [data.x] + [data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
        data.adj = self.edge2graph(data.edge_index)
        data.name = self.dataset_name
        data.num_classes = dataset.num_classes
        data.num_node = data.x.size(0)
        data.num_features = self.num_features[data.name]
        data.base_model = self.base_model
        data.num_edge = data.edge_index.size(1)
        # save_data(self.logger, data, data_filename)
        save_data(self.logger, dataset, dataset_filename)


        return data,dataset

    def edge2graph(self,edge_index):
        # 创建一个空的无向图
        G = nx.Graph()

        # 将边添加到图中
        G.add_edges_from(edge_index.t().tolist())

        # 获取图的邻接矩阵
        adj_matrix = nx.adjacency_matrix(G)


        return adj_matrix


