import torch
import pickle
import os
import numpy as np
import config
import torch.nn as nn
from torch_geometric.data import Data
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from config import root_path
from torch_geometric.transforms import SIGN
from config import root_path,unlearning_path,split_ratio,unlearning_edge_path
from utils.utils import filter_edge_index_2
from torch_geometric.utils import negative_sampling
def process_data(logger,data,args):
    if args["downstream_task"]=="graph":
        data.train_mask = torch.zeros(len(data))
        data.test_mask = torch.zeros(len(data))
        data.train_mask[:int(len(data)*0.8)] = True
        data.test_mask[int(len(data)*0.8):] = True
        data.train_indices =data.train_mask.nonzero(as_tuple=True)[0].tolist()
        data.test_indices = data.test_mask.nonzero(as_tuple=True)[0].tolist()
        
        return data
    #     data = graph_cls_process(args,data)
    #     return data
    if args["unlearning_methods"] == "CEU":
        data = ceu_process(args,data)
        return data

    if args['is_transductive']:
        if args['is_balanced']:
            filename = root_path + '/data/processed/transductive/' + args['dataset_name'] +split_ratio+ '_balanced.pkl'
            if is_data_exists(filename):
                with open(filename, 'rb') as file:
                    data = pickle.load(file)
            else:
                data = transductive_split_node_balanced(logger,args,data,train_ratio=args["train_ratio"], val_ratio=args["val_ratio"], test_ratio=args["test_ratio"])
                save_data(logger, data, filename)
        else:
            filename = root_path + '/data/processed/transductive/' + args['dataset_name'] + split_ratio + '.pkl'
            if is_data_exists(filename):
                with open(filename, 'rb') as file:
                    data = pickle.load(file)
            else:
                data = transductive_split_node(logger,args,data,train_ratio=args["train_ratio"], val_ratio=args["val_ratio"], test_ratio=args["test_ratio"])
                save_data(logger, data, filename)
            
    else:
        if args['is_balanced']:
            filename = root_path + '/data/processed/inductive/' + args['dataset_name'] + split_ratio + '_balanced.pkl'
            if is_data_exists(filename):
                with open(filename, 'rb') as file:
                    data = pickle.load(file)
            else:
                data = inductive_split_node_balanced(logger,args,data,train_ratio=args["train_ratio"], val_ratio=args["val_ratio"], test_ratio=args["test_ratio"])
                save_data(logger, data, filename)
        else:
            filename = root_path + '/data/processed/inductive/' + args['dataset_name'] + split_ratio +'.pkl'
            if is_data_exists(filename):
                with open(filename, 'rb') as file:
                    data = pickle.load(file)
            else:
                data = inductive_split_node(logger,args,data,train_ratio=args["train_ratio"], val_ratio=args["val_ratio"], test_ratio=args["test_ratio"])
                save_data(logger, data, filename)
    if args["unlearn_task"]=="node":
        train_nodes = np.array(data.train_indices)
        for i in range(args["num_runs"]):
            shuffle_num = torch.randperm(train_nodes.size)
            unlearning_nodes = train_nodes[shuffle_num][:args["num_unlearned_nodes"]]
            path_un = unlearning_path + "_" + str(i) + ".txt"
            if not os.path.isfile(path_un):
                np.savetxt(path_un, unlearning_nodes, fmt="%d")
    elif args["unlearn_task"]=="edge":
        train_edges = np.array(data.train_edge_index)
        num_unlearned_edges = int(train_edges.shape[1] * args["unlearn_ratio"])
        for i in range(args["num_runs"]):
            path_un_edge = unlearning_edge_path + "_" + str(i) + ".txt"
            if args["poison"]:
                if not os.path.isfile(path_un_edge):
                    unlearning_edges = negative_sampling(
                        edge_index=data.edge_index, num_nodes=data.num_nodes,
                        num_neg_samples=num_unlearned_edges,force_undirected=True
                    )
                    data.edge_index = torch.cat([data.edge_index, unlearning_edges], dim=1)
                    data.train_edge_index = torch.cat([data.train_edge_index, unlearning_edges], dim=1)
                    np.savetxt(path_un_edge, unlearning_edges.T, fmt="%d")
                else:
                    unlearning_edges = np.loadtxt(path_un_edge).T
                    data.edge_index = torch.cat([data.edge_index, torch.tensor(unlearning_edges,dtype=torch.int)], dim=1)
                    data.train_edge_index = torch.cat([data.train_edge_index, torch.tensor(unlearning_edges,dtype=torch.int)], dim=1)
            else:
                shuffle_num = torch.randperm(train_edges.shape[1])
                unlearning_edges = train_edges[:, shuffle_num][:, :num_unlearned_edges]
            
                if not os.path.isfile(path_un_edge):
                    np.savetxt(path_un_edge, unlearning_edges.T, fmt="%d")
                
    return data

class BasicDataset(Dataset):

    def __init__(self, nodes, labels):
        self.nodes = nodes
        self.labels = labels

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, idx):
        return self.nodes[idx], self.labels[idx]

    def remove(self, node):
        index = self.nodes.index(node)
        del self.nodes[index]
        del self.labels[index]



def ceu_process(args,data):
    nodes = list(range(len(data.x)))
    edges = [(e[0],e[1]) for e in data.edge_index.t().tolist()]
    features = data.x.numpy()
    num_features = data.x.size(1)
    labels = data.y.tolist()
    num_nodes = data.num_nodes
    if not args['feature']:
        features = initialize_features(data, num_nodes, args['emb_dim'],args)
        num_features = args['emb_dim']
    train_set_path = os.path.join('./data/CEU', args["dataset_name"], 'train_set.pt')
    valid_set_path = os.path.join('./data/CEU', args["dataset_name"], 'valid_set.pt')
    test_set_path = os.path.join('./data/CEU', args["dataset_name"], 'test_set.pt')
    if os.path.exists(train_set_path) and os.path.exists(valid_set_path) and os.path.exists(test_set_path):
        train_set = torch.load(os.path.join('./data/CEU', args["dataset_name"], 'train_set.pt'))
        valid_set = torch.load(os.path.join('./data/CEU', args["dataset_name"], 'valid_set.pt'))
        test_set = torch.load(os.path.join('./data/CEU', args["dataset_name"], 'test_set.pt'))
    else:
        nodes_train, nodes_test, labels_train, labels_test = train_test_split(nodes, labels, test_size=0.2)
        nodes_train, nodes_valid, labels_train, labels_valid = train_test_split(
            nodes_train, labels_train, test_size=0.2)
        train_set = BasicDataset(nodes_train, labels_train)
        valid_set = BasicDataset(nodes_valid, labels_valid)
        test_set = BasicDataset(nodes_test, labels_test)
        torch.save(train_set, train_set_path)
        torch.save(valid_set, valid_set_path)
        torch.save(test_set, test_set_path)
        
    data = {
        'nodes': nodes,
        'edges': edges,
        'features': features,
        'labels': labels,
        'num_nodes': len(nodes),
        'num_edges': len(edges),
        'num_classes': np.max(labels) + 1,
        'num_features': num_features,
        # 'node2idx': node2idx,
        # 'label2idx': label2idx,
        'train_set': train_set,
        'valid_set': valid_set,
        'test_set': test_set,
    }
    return data


def initialize_features(dataset, num_nodes, emb_dim,args):
    if emb_dim == 32:
        features_path = os.path.join('./data/CEU', args["dataset_name"], 'features.pt')
    else:
        features_path = os.path.join('./data/CEU', args["dataset_name"], f'features_{emb_dim}.pt')
    if os.path.exists(features_path):
        features = torch.load(features_path)
    else:
        features = torch.zeros(num_nodes, emb_dim)
        nn.init.xavier_normal_(features)
        torch.save(features, features_path)
    return features.numpy()



def inductive_split_node(logger,args,data, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    """
    create three graph:
    train: data.x[data.train_mask] data.train_edge_index
    val: the same
    test: the same

    :param logger:
    :param args:
    :param data:
    :param train_ratio:
    :param val_ratio:
    :param test_ratio:
    :return:
    """

    num_nodes = data.num_nodes
    indices = torch.randperm(num_nodes)
    edge_index = data.edge_index

    train_mask = indices[:int(train_ratio * num_nodes)]
    val_mask = indices[int(train_ratio * num_nodes):int((train_ratio + val_ratio) * num_nodes)]
    test_mask = indices[int((train_ratio + val_ratio) * num_nodes):]

    # 创建训练、验证和测试集的掩码
    data.train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    data.train_mask[train_mask] = 1
    data.val_mask[val_mask] = 1
    data.test_mask[test_mask] = 1

    data.train_indices =data.train_mask.nonzero(as_tuple=True)[0].tolist()
    data.test_indices = data.test_mask.nonzero(as_tuple=True)[0].tolist()
    data.val_indices = data.val_mask.nonzero(as_tuple=True)[0].tolist()

    train_mask = data.train_mask
    val_mask = data.val_mask
    test_mask = data.test_mask

    # 获取 edge_index 的起点和终点
    src, dst = edge_index[0], edge_index[1]

    # 训练集的边：起点和终点都在训练集中
    train_edges_mask = train_mask[src] & train_mask[dst]

    # 验证集的边：起点和终点都在验证集中
    val_edges_mask = val_mask[src] & val_mask[dst]

    # 测试集的边：起点和终点都在测试集中
    test_edges_mask = test_mask[src] & test_mask[dst]

    # 合并三个掩码，生成最终的 edge_index
    final_edges_mask = train_edges_mask | val_edges_mask | test_edges_mask

    # 根据合并后的 mask 筛选出最终的 edge_index
    final_edge_index = edge_index[:, final_edges_mask]

    # 将结果保存回 data 对象中
    data.edge_index = final_edge_index

    train_edge_index = data.edge_index.clone()
    val_edge_index = data.edge_index.clone()
    test_edge_index = data.edge_index.clone()

    train_new_index = 0
    val_new_index = 0
    test_new_index = 0
    train_dict = {}
    val_dict = {}
    test_dict = {}
    for node in range(num_nodes):
        if data.train_mask[node]:
            train_dict[node] = train_new_index
            train_new_index += 1
        elif data.val_mask[node]:
            val_dict[node] = val_new_index
            val_new_index += 1
        elif data.test_mask[node]:
            test_dict[node] = test_new_index
            test_new_index += 1



    # 删除连接训练、验证和测试集之间的边
    train_edge_mask = data.train_mask[train_edge_index[0]] & data.train_mask[train_edge_index[1]]
    data.train_edge_index = train_edge_index[:, train_edge_mask]
    for edge in range(data.train_edge_index.size(1)):
        data.train_edge_index[0][edge] = train_dict[data.train_edge_index[0][edge].item()]
        data.train_edge_index[1][edge] = train_dict[data.train_edge_index[1][edge].item()]
    # 删除连接验证集之外的边
    val_edge_mask = data.val_mask[val_edge_index[0]] & data.val_mask[val_edge_index[1]]
    data.val_edge_index = val_edge_index[:, val_edge_mask]
    for edge in range(data.val_edge_index.size(1)):
        data.val_edge_index[0][edge] = val_dict[data.val_edge_index[0][edge].item()]
        data.val_edge_index[1][edge] = val_dict[data.val_edge_index[1][edge].item()]

        # 删除连接测试集之外的边
    test_edge_mask = data.test_mask[test_edge_index[0]] & data.test_mask[test_edge_index[1]]
    data.test_edge_index = test_edge_index[:, test_edge_mask]
    for edge in range(data.test_edge_index.size(1)):
        data.test_edge_index[0][edge] = test_dict[data.test_edge_index[0][edge].item()]
        data.test_edge_index[1][edge] = test_dict[data.test_edge_index[1][edge].item()]

    test_neg_edge_index = negative_sampling(
            edge_index=data.test_edge_index,num_nodes=data.num_nodes,
            num_neg_samples=data.test_edge_index.size(1)
        )
    pos_edge_labels = torch.ones(data.test_edge_index.size(1),dtype=torch.float32)
    neg_edge_labels = torch.zeros(test_neg_edge_index.size(1),dtype=torch.float32)
    test_edge_labels = torch.cat((pos_edge_labels,neg_edge_labels))
    data.test_neg_edge_index = test_neg_edge_index
    data.edge_labels = test_edge_labels
    # save_train_test_split(logger,args,data.train_indices,data.test_indices)

    return data

def inductive_split_node_balanced(logger,args,data, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    """
    create three graph:
    train: data.x[data.train_mask] data.train_edge_index
    val: the same
    test: the same

    :param logger:
    :param args:
    :param data:
    :param train_ratio:
    :param val_ratio:
    :param test_ratio:
    :return:
    """

    num_nodes = data.num_nodes
    labels = data.y  # 假设节点的类别标签保存在 data.y 中
    num_classes = labels.max().item() + 1
    edge_index = data.edge_index

    train_indices = []
    val_indices = []
    test_indices = []

    for i in range(num_classes):
        class_indices = (labels == i).nonzero(as_tuple=True)[0]  # 获取每个类别的节点索引
        class_indices = class_indices[torch.randperm(class_indices.size(0))]  # 随机打乱

        num_train = int(train_ratio * len(class_indices))
        num_val = int(val_ratio * len(class_indices))

        train_indices.append(class_indices[:num_train])
        val_indices.append(class_indices[num_train:num_train + num_val])
        test_indices.append(class_indices[num_train + num_val:])

    train_indices = torch.cat(train_indices)
    val_indices = torch.cat(val_indices)
    test_indices = torch.cat(test_indices)

    data.train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    data.train_mask[train_indices] = 1
    data.val_mask[val_indices] = 1
    data.test_mask[test_indices] = 1

    data.train_indices =data.train_mask.nonzero(as_tuple=True)[0].tolist()
    data.test_indices = data.test_mask.nonzero(as_tuple=True)[0].tolist()
    data.val_indices = data.val_mask.nonzero(as_tuple=True)[0].tolist()

    train_mask = data.train_mask
    val_mask = data.val_mask
    test_mask = data.test_mask

    # 获取 edge_index 的起点和终点
    src, dst = edge_index[0], edge_index[1]

    # 训练集的边：起点和终点都在训练集中
    train_edges_mask = train_mask[src] & train_mask[dst]

    # 验证集的边：起点和终点都在验证集中
    val_edges_mask = val_mask[src] & val_mask[dst]

    # 测试集的边：起点和终点都在测试集中
    test_edges_mask = test_mask[src] & test_mask[dst]

    # 合并三个掩码，生成最终的 edge_index
    final_edges_mask = train_edges_mask | val_edges_mask | test_edges_mask

    # 根据合并后的 mask 筛选出最终的 edge_index
    final_edge_index = edge_index[:, final_edges_mask]

    # 将结果保存回 data 对象中
    data.edge_index = final_edge_index

    train_edge_index = data.edge_index.clone()
    val_edge_index = data.edge_index.clone()
    test_edge_index = data.edge_index.clone()

    train_new_index = 0
    val_new_index = 0
    test_new_index = 0
    train_dict = {}
    val_dict = {}
    test_dict = {}
    for node in range(num_nodes):
        if data.train_mask[node]:
            train_dict[node] = train_new_index
            train_new_index += 1
        elif data.val_mask[node]:
            val_dict[node] = val_new_index
            val_new_index += 1
        elif data.test_mask[node]:
            test_dict[node] = test_new_index
            test_new_index += 1



    # 删除连接训练、验证和测试集之间的边
    train_edge_mask = data.train_mask[train_edge_index[0]] & data.train_mask[train_edge_index[1]]
    data.train_edge_index = train_edge_index[:, train_edge_mask]
    for edge in range(data.train_edge_index.size(1)):
        data.train_edge_index[0][edge] = train_dict[data.train_edge_index[0][edge].item()]
        data.train_edge_index[1][edge] = train_dict[data.train_edge_index[1][edge].item()]
    # 删除连接验证集之外的边
    val_edge_mask = data.val_mask[val_edge_index[0]] & data.val_mask[val_edge_index[1]]
    data.val_edge_index = val_edge_index[:, val_edge_mask]
    for edge in range(data.val_edge_index.size(1)):
        data.val_edge_index[0][edge] = val_dict[data.val_edge_index[0][edge].item()]
        data.val_edge_index[1][edge] = val_dict[data.val_edge_index[1][edge].item()]

        # 删除连接测试集之外的边
    test_edge_mask = data.test_mask[test_edge_index[0]] & data.test_mask[test_edge_index[1]]
    data.test_edge_index = test_edge_index[:, test_edge_mask]
    for edge in range(data.test_edge_index.size(1)):
        data.test_edge_index[0][edge] = test_dict[data.test_edge_index[0][edge].item()]
        data.test_edge_index[1][edge] = test_dict[data.test_edge_index[1][edge].item()]

    # save_train_test_split(logger,args,data.train_indices,data.test_indices)

    return data

def transductive_split_node(logger,args,data, train_ratio=0.8, val_ratio=0, test_ratio=0.2):
    
    num_nodes = data.num_nodes
    indices = torch.randperm(num_nodes)

    train_mask = indices[:int(train_ratio * num_nodes)]
    val_mask = indices[int(train_ratio * num_nodes):int((train_ratio + val_ratio) * num_nodes)]
    test_mask = indices[int((train_ratio + val_ratio) * num_nodes):]

    # 创建训练、验证和测试集的掩码
    data.train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    data.train_mask[train_mask] = 1
    data.val_mask[val_mask] = 1
    data.test_mask[test_mask] = 1

    data.train_indices = data.train_mask.nonzero(as_tuple=True)[0].tolist()
    data.test_indices = data.test_mask.nonzero(as_tuple=True)[0].tolist()
    data.val_indices = data.val_mask.nonzero(as_tuple=True)[0].tolist()

    num_edges = data.edge_index.size(1)
    num_train_edges = int(train_ratio * num_edges)
    num_val_edges = int(val_ratio * num_edges)
    num_test_edges = int(test_ratio * num_edges)
    
    # shuffle_num = torch.randperm(num_edges)
    # data.train_edge_index = data.edge_index[:, shuffle_num[:num_train_edges]]
    # data.val_edge_index = data.edge_index[:, shuffle_num[num_train_edges:num_train_edges + num_val_edges]]
    # data.test_edge_index = data.edge_index[:, shuffle_num[num_train_edges + num_val_edges:]]
    
    # 获取 edge_index 的起点和终点
    src, dst = data.edge_index[0], data.edge_index[1]
    # 训练集的边：起点和终点都在训练集中
    train_edges_mask = data.train_mask[src] & data.train_mask[dst]
    # 验证集的边：起点和终点都在验证集中
    val_edges_mask = data.val_mask[src] & data.val_mask[dst]
    # 测试集的边：起点和终点都在测试集中
    test_edges_mask = data.test_mask[src] & data.test_mask[dst]
    # 根据掩码筛选出训练、验证和测试集的 edge_index
    data.train_edge_index = data.edge_index[:, train_edges_mask]
    data.val_edge_index = data.edge_index[:, val_edges_mask]
    data.test_edge_index = data.edge_index[:, test_edges_mask]

    # test_neg_edge_index = negative_sampling(
    #         edge_index=data.test_edge_index,num_nodes=data.num_nodes,
    #         num_neg_samples=data.test_edge_index.size(1)
    #     )
    # pos_edge_labels = torch.ones(data.test_edge_index.size(1),dtype=torch.float32)
    # neg_edge_labels = torch.zeros(test_neg_edge_index.size(1),dtype=torch.float32)
    # test_edge_labels = torch.cat((pos_edge_labels,neg_edge_labels))
    # data.test_neg_edge_index = test_neg_edge_index
    # data.test_edge_labels = test_edge_labels
    # save_train_test_split(logger,args, data.train_indices, data.test_indices)
    return data

def transductive_split_edge(logger,args,data, train_ratio=0.8, val_ratio=0, test_ratio=0.2):
    num_nodes = data.num_nodes
    num_edges = data.edge_index.size(1)
    data.train_mask = torch.ones(num_nodes, dtype=torch.bool)
    data.val_mask = torch.ones(num_nodes, dtype=torch.bool)
    data.test_mask = torch.ones(num_nodes, dtype=torch.bool)
    
    data.train_indices = data.train_mask.nonzero(as_tuple=True)[0].tolist()
    data.test_indices = data.test_mask.nonzero(as_tuple=True)[0].tolist()
    data.val_indices = data.val_mask.nonzero(as_tuple=True)[0].tolist()
    
    num_train_edges = int(train_ratio * num_edges)
    num_val_edges = int(val_ratio * num_edges)
    num_test_edges = int(test_ratio * num_edges)
    
    shuffle_num = torch.randperm(num_edges)
    data.train_edge_index = data.edge_index[:, shuffle_num[:num_train_edges]]
    data.val_edge_index = data.edge_index[:, shuffle_num[num_train_edges:num_train_edges + num_val_edges]]
    data.test_edge_index = data.edge_index[:, shuffle_num[num_train_edges + num_val_edges:]]
    
    return data

def transductive_split_node_balanced(logger, args, data, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    num_nodes = data.num_nodes
    labels = data.y  # 假设节点的类别标签保存在 data.y 中
    num_classes = labels.max().item() + 1

    train_indices = []
    val_indices = []
    test_indices = []

    for i in range(num_classes):
        class_indices = (labels == i).nonzero(as_tuple=True)[0]  # 获取每个类别的节点索引
        class_indices = class_indices[torch.randperm(class_indices.size(0))]  # 随机打乱

        num_train = int(train_ratio * len(class_indices))
        num_val = int(val_ratio * len(class_indices))

        train_indices.append(class_indices[:num_train])
        val_indices.append(class_indices[num_train:num_train + num_val])
        test_indices.append(class_indices[num_train + num_val:])

    # 合并每个类别的索引
    train_indices = torch.cat(train_indices)
    val_indices = torch.cat(val_indices)
    test_indices = torch.cat(test_indices)

    # 创建训练、验证和测试集的掩码
    data.train_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.val_mask = torch.zeros(num_nodes, dtype=torch.bool)
    data.test_mask = torch.zeros(num_nodes, dtype=torch.bool)

    data.train_mask[train_indices] = True
    data.val_mask[val_indices] = True
    data.test_mask[test_indices] = True

    data.train_indices = train_indices.tolist()
    data.val_indices = val_indices.tolist()
    data.test_indices = test_indices.tolist()

    data.train_edge_index = data.edge_index.clone()
    data.val_edge_index = data.edge_index.clone()
    data.test_edge_index = data.edge_index.clone()
    # save_train_test_split(logger, args, data.train_indices, data.test_indices)

    return data


def c2n_to_n2c(args, community_to_node):
    node_list = []
    for i in range(args['num_shards']):
        node_list.extend(list(community_to_node.values())[i])
    node_to_community = {}

    for comm, nodes in dict(community_to_node).items():
        for node in nodes:
            # Map node id back to original graph
            # node_to_community[node_list[node]] = comm
            node_to_community[node] = comm

    return node_to_community





def save_train_test_split(logger,args,train_indices, test_indices):
    train_test_split_file = config.train_test_split_file
    os.makedirs(os.path.dirname(train_test_split_file), exist_ok=True)
    logger.info("save_train_test_split:{}".format(train_test_split_file) )
    pickle.dump((train_indices, test_indices), open(train_test_split_file, 'wb'))

def save_data(logger,data, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    logger.info("save_data {}".format(filename))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def save_train_data(logger,data,filename):
    logger.info("save_train_data {}".format(filename))
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def save_train_graph(logger,gragh_data,filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(gragh_data, file)

def save_unlearned_data(logger,data, suffix):
    logger.info('saving unlearned data {}'.format('_'.join((config.unlearned_file, suffix))))
    pickle.dump(data, open('_'.join((config.unlearned_file, suffix)), 'wb'))


def load_unlearned_data(logger, suffix):
    file_path = '_'.join((config.unlearned_file, suffix))
    logger.info('loading unlearned data from %s' % file_path)
    return pickle.load(open(file_path, 'rb'))

def save_community_data(logger,community_to_node,filename, suffix=''):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    logger.info('save_community_data {}'.format(filename + suffix))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pickle.dump(community_to_node, open(filename + suffix, 'wb'))

def save_shard_data(logger,shard_data, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pickle.dump(shard_data, open(filename, 'wb'))

def load_shard_data(logger):
    logger.info("load_shard_data {}".format(config.shard_file))
    return pickle.load(open(config.shard_file, 'rb'))


def load_train_graph(logger):
    logger.info("load_train_graph {}".format(config.train_graph_file))
    return pickle.load(open(config.train_graph_file, 'rb'))

def save_embeddings(embeddings,filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pickle.dump(embeddings, open(filename, 'wb'))

def load_community_data(logger,filename = config.load_community_data,suffix=''):
    # logger.info("load_community_data {}".format(filename+suffix))
    return pickle.load(open(filename + suffix, 'rb'))

def load_saved_data(logger,filename = config.train_data_file):
    logger.info('load_saved_data {}'.format(filename))
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data

def load_embeddings(logger,filename):
    logger.info('load_embeddings {}'.format(filename))
    with open(filename, 'rb') as file:
        embeddings = pickle.load(file)
    return embeddings

def load_train_test_split(logger, filename = config.train_test_split_file):
    logger.info("load_train_test_split {}".format(filename))
    return  pickle.load(open(filename, 'rb'))

def is_data_exists(filename):
    return os.path.exists(filename)

def _extract_embedding_method(partition_method):
    return partition_method.split('_')[0]

def save_target_model(logger,args,run, model, shard, suffix=''):
    
    if not os.path.exists(config.MODEL_PATH + args['dataset_name']):
        os.mkdir(config.MODEL_PATH + args['dataset_name'])
    if args["exp"] in ["node_edge_unlearning", "attack_unlearning"]:
        model_path = '_'.join((config.target_model_file, str(shard), str(run), str(args['num_unlearned_nodes']))) + suffix
        model.save_model(model_path)
        logger.info("save_target_model {}".format(model_path))
    else:
        model.save_model(config.target_model_file + '_' + str(shard) + '_' + str(run))
        logger.info("save_target_model {}".format(config.target_model_file + '_' + str(shard) + '_' + str(run)))
        # model.save_model(self.target_model_file + '_' + str(shard))

def load_target_model(logger,args, run, model, shard, suffix=''):
    if args["exp"] == "node_edge_unlearning":
        model.load_model(
            '_'.join((config.target_model_file, str(shard), str(run), str(args['num_unlearned_nodes']))))
        # logger.info("load_target_model {}".format('_'.join((config.target_model_file, str(shard), str(run), str(args['num_unlearned_nodes'])))))
    elif args["exp"] == "attack_unlearning":
        if(suffix == ''):
            model_path = '_'.join((config.target_model_file, str(shard), str(run)))
        else:
            model_path = '_'.join((config.target_model_file, str(shard), str(run), str(args['num_unlearned_nodes']))) + suffix
        device = torch.device('cpu')
        model.load_model(model_path)
        model.device=device
        # logger.info("load_target_model {}".format(model_path))
    else:
        # model.load_model(self.target_model_file + '_' + str(shard) + '_' + str(run))
        model.load_model(config.target_model_file + '_' + str(shard) + '_' + str(run))
        # logger.info("load_target_model {}".format(config.target_model_file + '_' + str(shard) + '_' + str(0)))

def save_posteriors(logger,args, posteriors, run, suffix=''):
    posteriors_path = config.ANALYSIS_PATH + 'posteriors/' + args['dataset_name'] + '/' + config.target_model_name
    os.makedirs(os.path.dirname(posteriors_path), exist_ok=True)
    logger.info("save_posteriors {}".format(posteriors_path))
    torch.save(posteriors, posteriors_path + '_' + str(run) + suffix)

def save_optimal_weight(logger,args,weight,run):
    optimal_weight_path = config.ANALYSIS_PATH + 'optimal/' + args['dataset_name'] + '/' + config.optimal_weight_name
    os.makedirs(os.path.dirname(optimal_weight_path), exist_ok=True)
    torch.save(weight, optimal_weight_path + '_' + str(run))


def build_shard_data(data_full, train_shard_indices, val_indices=None, test_indices=None):
    # Avoid computing val/test indices for multiple times when building multiple shards
    val_indices = torch.nonzero(data_full.val_mask).squeeze(1).numpy() if val_indices is None else val_indices
    test_indices = torch.nonzero(data_full.test_mask).squeeze(1).numpy() if test_indices is None else test_indices

    shard_indices = np.union1d(np.union1d(train_shard_indices, val_indices), 
                               test_indices)
    x = data_full.x[shard_indices]
    y = data_full.y[shard_indices]
    edge_index, edge_index_train = filter_edge_index_2(data_full, shard_indices)

    data = Data(x=x, edge_index=torch.from_numpy(edge_index), y=y)
    data.train_mask = torch.from_numpy(np.isin(shard_indices, train_shard_indices))
    data.val_mask = torch.from_numpy(np.isin(shard_indices, val_indices))
    data.test_mask = torch.from_numpy(np.isin(shard_indices, test_indices))
    data.edge_index_train = torch.from_numpy(edge_index_train)

    return data

def graph_cls_process(graph_data,train_ratio=0.7,val_ratio=0.1,test_ratio=0.2):
        # 初始化大图的属性
        all_x = []             # 节点特征
        all_edge_index = []    # 边索引
        all_y = []             # 节点标签
        all_graph_id = []      # 每个节点所属的图ID标签，用于标识节点来源

        node_offset = 0        # 用于跟踪节点索引偏移量

        # 遍历数据集中的每个图
        
        for i, data in enumerate(graph_data):
            # print(data)
            # 收集节点特征和标签
            all_x.append(data.x)
            all_y.append(data.y)
            
            # 调整边索引以适应全局大图
            edge_index = data.edge_index + node_offset
            all_edge_index.append(edge_index)
            
            # 将每个节点的图ID记录下来
            all_graph_id.append(torch.full((data.num_nodes,), i, dtype=torch.long))
            
            # 更新节点偏移量
            node_offset += data.num_nodes

        # 将所有节点特征、边索引和标签进行拼接
        big_x = torch.cat(all_x, dim=0)
        big_edge_index = torch.cat(all_edge_index, dim=1)
        big_y = torch.cat(all_y, dim=0)
        big_graph_id = torch.cat(all_graph_id, dim=0)

        # 构建大图的 Data 对象
        big_graph = Data(x=big_x, edge_index=big_edge_index, y=big_y, graph_id=big_graph_id)
        data = big_graph
        graph_ids = torch.unique(data.graph_id)
        num_train_ids = int(len(graph_ids) * train_ratio)
        shuffle_num = torch.randperm(len(graph_ids))
        train_ids = graph_ids[shuffle_num][:num_train_ids]
        val_ids = graph_ids[shuffle_num][num_train_ids:num_train_ids + int(len(graph_ids) * val_ratio)]
        test_ids = graph_ids[shuffle_num][num_train_ids + int(len(graph_ids) * val_ratio):]
        
        train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
        val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
        test_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
        
        train_label_mask = torch.zeros(data.y.size(), dtype=torch.bool)
        val_label_mask = torch.zeros(data.y.size(), dtype=torch.bool)
        test_label_mask = torch.zeros(data.y.size(), dtype=torch.bool)
        
        train_indices = []
        val_indices = []
        test_indices = []
        
        for gid in train_ids:
            mask = data.graph_id == gid
            indice = mask.nonzero(as_tuple=True)[0]
            train_indices.append(indice)
            train_mask[mask] = True
            train_label_mask[gid] = True
        for gid in val_ids:
            mask = data.graph_id == gid
            indice = mask.nonzero(as_tuple=True)[0]
            val_indices.append(indice)
            val_mask[mask] = True
            val_label_mask[gid] = True
        for gid in test_ids:
            mask = data.graph_id == gid
            indice = mask.nonzero(as_tuple=True)[0]
            test_indices.append(indice)
            test_mask[mask] = True
            test_label_mask[gid] = True
            
        data.train_ids = train_ids
        data.val_ids = val_ids
        data.test_ids = test_ids
        data.train_mask = train_mask
        data.val_mask = val_mask
        data.test_mask = test_mask
        data.train_indices = train_indices
        data.val_indices = val_indices
        data.test_indices = test_indices
        data.train_label_mask = train_label_mask
        data.val_label_mask = val_label_mask
        data.test_label_mask = test_label_mask
        
        return data
        

