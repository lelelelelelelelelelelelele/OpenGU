import logging
import os
from scipy.sparse import coo_matrix
from os import path as osp
from typing import Dict, List, Optional, Tuple,Callable
from scipy.sparse import csr_matrix
import torch
import pickle
import torch_geometric.transforms as T
import networkx as nx
import torch_geometric
from torch_geometric.datasets import MNISTSuperpixels,ShapeNet
from ogb.linkproppred import PygLinkPropPredDataset
from ogb.nodeproppred import PygNodePropPredDataset
from ogb.graphproppred import PygGraphPropPredDataset
from torch_geometric.datasets import Planetoid, Coauthor, Flickr, Amazon, CitationFull,PPI,Reddit,TUDataset
from utils.dataset_utils import is_data_exists, load_saved_data, save_data
from torch_geometric.transforms import SIGN
from config import root_path,split_ratio
from torch_geometric.io import fs
from dataset.ppi_data import ppi_data
from torch_geometric.datasets import Actor
from torch_geometric.datasets import Amazon
from torch_geometric.datasets import HeterophilousGraphDataset
from torch_geometric.data import Data, InMemoryDataset
from torch_geometric.utils import k_hop_subgraph, to_scipy_sparse_matrix
from utils.utils import sparse_mx_to_torch_sparse_tensor,normalize_adj
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
            "ogbn-products":100,
            'Squirrel': 2089,
            'Chameleon': 2325,
            'Actor': 931,
            'Minesweeper':7,
            'Tolokers': 10,
            'Roman-empire': 300,
            'Amazon-ratings': 300,
            'Questions':301,
            'MUTAG':7,
            'COX2':38,
            "BZR":56,
            "AIDS":42,
            "DD":89,
            "PROTEINS":4,
            "ENZYMES":21,
            "PTC_MR":9,
            "NCI1":37,
            "DHFR": 56,
            "MNISTSuperpixels":1
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
            self.args["num_unlearned_nodes"] = int(data.num_nodes * self.args["proportion_unlearned_nodes"])
            return data, dataset

        if self.dataset_name in ["cora", "pubmed", "citeseer"]:
            dataset = Planetoid(root_path + '/data/raw', self.dataset_name, transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.dataset_name in ["Tolokers", "Roman-empire", "Amazon-ratings", "Questions", "Minesweeper"]:
            dataset =  HeterophilousGraphDataset(root=root_path + '/data/raw', name=self.dataset_name)
            data = dataset._data
        elif self.dataset_name in ["Chameleon", "Squirrel"]:
            dataset =  WikiPages(root=root_path + '/data/raw', name=self.dataset_name)
            data = dataset._data
        elif self.dataset_name in ["CS", "Physics"]:
            dataset = Coauthor(root_path + '/data/raw', self.dataset_name, pre_transform=T.NormalizeFeatures())
            data = dataset._data
        elif self.dataset_name == 'flickr':
            dataset = Flickr(root_path + '/data/raw/flickr' ,self.dataset_name, pre_transform=T.NormalizeFeatures())
            data = dataset._data
            data.num_classes = 7
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
        elif self.dataset_name in ['Actor']:
            dataset = Actor(root= root_path + '/data/raw')
            data = dataset._data
        elif self.dataset_name == 'AmazonRatings':
            dataset = Amazon(root=root_path + '/data/raw', name='Ratings')
            data = dataset[0]
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
        elif self.args["dataset_name"] in ["ogbg-molhiv","ogbg-molpcba","ogbg-ppa"]:
            dataset = PygGraphPropPredDataset(name=self.dataset_name, root = root_path + '/data/raw')
            data = dataset._data
            data = dataset
            return data,dataset
        elif self.args["dataset_name"] == "MNISTSuperpixels":
            data = MNISTSuperpixels(name=self.dataset_name, root = root_path + '/data/raw')
            data = dataset._data
            return data,dataset
        elif self.args["dataset_name"] == "ShapeNet":
            data = ShapeNet(name=self.dataset_name, root = root_path + '/data/raw')
            data = dataset._data
            return data,dataset
            
        elif self.args["dataset_name"] in ["AIDS","BZR","COX2","DD","MUTAG","PROTEINS","PTC_MR","ENZYMES","NCI1","DHFR","IMDB-BINARY","IMDB-MULTI","COLLAB"]:
            dataset = TUDataset(root=root_path + '/data/raw',name=self.args["dataset_name"],use_node_attr=True,use_edge_attr=True)
            
            # # 初始化大图的属性
            # all_x = []             # 节点特征
            # all_edge_index = []    # 边索引
            # all_y = []             # 节点标签
            # all_graph_id = []      # 每个节点所属的图ID标签，用于标识节点来源

            # node_offset = 0        # 用于跟踪节点索引偏移量

            # # 遍历数据集中的每个图
            # for i, data in enumerate(dataset):
            #     # 收集节点特征和标签
            #     all_x.append(data.x)
            #     all_y.append(data.y)
                
            #     # 调整边索引以适应全局大图
            #     edge_index = data.edge_index + node_offset
            #     all_edge_index.append(edge_index)
                
            #     # 将每个节点的图ID记录下来
            #     all_graph_id.append(torch.full((data.num_nodes,), i, dtype=torch.long))
                
            #     # 更新节点偏移量
            #     node_offset += data.num_nodes

            # # 将所有节点特征、边索引和标签进行拼接
            # big_x = torch.cat(all_x, dim=0)
            # big_edge_index = torch.cat(all_edge_index, dim=1)
            # big_y = torch.cat(all_y, dim=0)
            # big_graph_id = torch.cat(all_graph_id, dim=0)

            # # 构建大图的 Data 对象
            # big_graph = Data(x=big_x, edge_index=big_edge_index, y=big_y, graph_id=big_graph_id)
            # data = big_graph
            data = dataset
            return data,dataset
        else:
            raise Exception('unsupported dataset')

        # data = SIGN(self.args["GNN_layer"])(data)
        # data.xs = [data.x] + [data[f'x{i}'] for i in range(1, self.args["GNN_layer"] + 1)]
        # data.adj = self.edge2graph(data.edge_index)
        data = T.ToUndirected()(data)
        data.name = self.dataset_name
        if not hasattr(data, 'num_classes'):
            data.num_classes = dataset.num_classes
        data.num_nodes = data.x.size(0)
        data.num_features = self.num_features[data.name]
        data.num_edges = data.edge_index.size(1)
        data.x = data.x.to(torch.float32)
        self.args["num_unlearned_nodes"] = int(data.num_nodes * self.args["proportion_unlearned_nodes"])
        # save_data(self.logger, data, data_filename)
        if self.args['dataset_name'] == "ogbn-products":
            adj = to_scipy_sparse_matrix(data.edge_index,num_nodes=data.num_nodes)
            adj = normalize_adj(adj)
            data.adj = sparse_mx_to_torch_sparse_tensor(adj).cuda()
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


class WikiPages(InMemoryDataset):
    url = "https://data.dgl.ai/dataset"

    def __init__(
        self,
        root: str,
        name: str,
        transform: Optional[Callable] = None,
        pre_transform: Optional[Callable] = None,
        force_reload: bool = False,
    ) -> None:
        self.name = name # [chameleon, squirrel]

        super().__init__(root, transform, pre_transform,
                         force_reload=force_reload)
        self.load(self.processed_paths[0])

    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, self.name, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, self.name, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        return ["out1_graph_edges.txt", "out1_node_feature_label.txt"]

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'

    def download(self) -> None:
        fs.cp(f"{self.url}/{self.name.lower()}.zip", self.raw_dir, extract=True)

    def process(self) -> None:
        edge_index_path = osp.join(self.raw_dir, "out1_graph_edges.txt")
        data_list = []
        with open(edge_index_path, 'r') as file:
            # Skip the header
            next(file)
            for line in file:
                data_list.append([int(number) for number in line.split()])
        edge_index = torch.tensor(data_list).long().T

        node_feature_label_path = osp.join(self.raw_dir, "out1_node_feature_label.txt")
        node_feature_list = []
        node_label_list = []
        with open(node_feature_label_path, 'r') as file:
            # Skip the header
            next(file)
            for line in file:
                node_id, feature, label = line.strip().split('\t')
                node_feature_list.append([int(num) for num in feature.split(',')])
                node_label_list.append(int(label))
        x = torch.tensor(node_feature_list)
        y = torch.tensor(node_label_list)
        data = Data(x=x, edge_index=edge_index, y=y)
        
        
        data = data if self.pre_transform is None else self.pre_transform(data)
        self.save([data], self.processed_paths[0])

    def __repr__(self) -> str:
        return f'{self.name}()'
