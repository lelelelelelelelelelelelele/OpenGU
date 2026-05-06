import copy
import logging

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader
from unlearning.unlearning_methods.GraphRevoker.lib_aggregator.opt_dataset import OptDataset
from torch_geometric.data import Data
import torch_geometric.transforms as T
from utils import dataset_utils,utils



class OptimalAggregator:
    def __init__(self, run, target_model, data, args,logger):
        self.logger = logger
        self.args = args

        self.run = run
        self.target_model = target_model
        self.data = data
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.num_shards = args['num_shards']

    def _generate_train_data(self):
        data = dataset_utils.load_train_test_split(self.logger)
        # train_indices,_= load_train_test_split(self.logger)
        
        train_indices = data.train_indices
        train_indices = np.array(train_indices)

        com2node = dataset_utils.load_community_data(self.logger)
        node2com = {}
        
        for com, indices in com2node.items():
            for node in indices:
                node2com[node] = com
        node2com = np.array(list(node2com.values()), dtype=np.int64)
        
        # sample a set of nodes from train_indices
        if self.args["num_opt_samples"] == 1000:
            selected_indices = np.random.choice(np.arange(len(train_indices)), size=1000, replace=False)
        elif self.args["num_opt_samples"] == 10000:
            selected_indices = np.random.choice(np.arange(len(train_indices)), size=int(len(train_indices) * 0.1), replace=False)
        elif self.args["num_opt_samples"] == 1:
            selected_indices = np.random.choice(np.arange(len(train_indices)), size=int(len(train_indices)), replace=False)

        train_indices = train_indices[selected_indices]
        # Defensive: node2com (loaded from the partition snapshot) and
        # train_indices (loaded from the train/test split) can fall out of
        # alignment when run_retrain shrinks the train set after unlearning.
        # node2com is unused by OptimalAggregator (only ContrastiveAggregator
        # consumes self.node2com), so a length mismatch should not fail this
        # path. Mask out-of-range indices to a safe sentinel; downstream code
        # that genuinely needs node2com (contrastive_aggregator) will still
        # raise visibly if it walks past the array.
        if len(selected_indices) and selected_indices.max() >= len(node2com):
            safe_idx = np.clip(selected_indices, 0, len(node2com) - 1)
            self.node2com = node2com[safe_idx]
        else:
            self.node2com = node2com[selected_indices]

        train_indices = np.sort(train_indices)
        self.logger.info("Using %s samples for optimization" % (int(train_indices.shape[0])))

        x = self.data.x[train_indices]
        y = self.data.y[train_indices]
        edge_index = utils.filter_edge_index(self.data.edge_index, train_indices)

        train_data = Data(x=x, edge_index=torch.from_numpy(edge_index), y=y)
        train_data.train_mask = torch.zeros(train_indices.shape[0], dtype=torch.bool)
        train_data.test_mask = torch.ones(train_indices.shape[0], dtype=torch.bool)
        self.true_labels = y

        self.posteriors = {}
        
        return train_data

    def generate_train_data(self):
        train_data= self._generate_train_data()

        # Save original target_model.data to restore after the loop. We need
        # to point .data at train_data because GraphRevokerTrainer._inference
        # reads self.data.x / self.data.edge_index (NOT self.data_full like
        # NodeClassifier._inference does — that asymmetry between the two
        # trainers is what made this bug latent until 2026-05-05).
        original_data = getattr(self.target_model, 'data', None)
        for shard in range(self.num_shards):
            self.target_model.data = train_data
            self.target_model.data_full = train_data  # set both for safety
            if self.args['is_use_test_batch']:
                self.target_model.gen_test_loader()
            dataset_utils.load_target_model(self.logger,self.args,self.run, self.target_model, shard)

            self.posteriors[shard] = self.target_model._inference()[0].to(self.device)

        # Restore original data so subsequent code paths (e.g. unlearn-time
        # aggregator re-runs) see what they expect.
        if original_data is not None:
            self.target_model.data = original_data
            #self.posteriors[shard] = self.target_model.posterior().to(self.device)
        

    def optimization(self):
        weight_para = nn.Parameter(torch.full((self.num_shards,), fill_value=1.0 / self.num_shards), requires_grad=True)
        optimizer = optim.Adam([weight_para], lr=self.args['opt_lr'])
        scheduler = MultiStepLR(optimizer, milestones=[5000, 10000], gamma=0.05)

        train_dset = OptDataset(self.posteriors, self.true_labels)
        train_loader = DataLoader(train_dset, batch_size=64, shuffle=True, num_workers=0)

        min_loss = 1e9
        for epoch in range(self.args['opt_num_epochs']):
            loss_all = 0.0

            for posteriors, labels in train_loader:
                labels = labels.to(self.device)

                optimizer.zero_grad()
                loss = self._loss_fn(posteriors, labels, weight_para)
                loss.backward()
                loss_all += loss

                optimizer.step()
                with torch.no_grad():
                    weight_para[:] = torch.clamp(weight_para, min=0.0)

            scheduler.step()

            if loss_all < min_loss:
                ret_weight_para = copy.deepcopy(weight_para)
                min_loss = loss_all

            self.logger.info('epoch: %s, loss: %s' % (epoch, loss_all))

        return ret_weight_para / torch.sum(ret_weight_para)
        #return torch.softmax(ret_weight_para, 0)

    def _loss_fn(self, posteriors, labels, weight_para):
        aggregate_posteriors = torch.zeros_like(posteriors[0])
        for shard in range(self.num_shards):
            aggregate_posteriors += weight_para[shard] * posteriors[shard]

        aggregate_posteriors = F.softmax(aggregate_posteriors, dim=1)
        loss_1 = F.cross_entropy(aggregate_posteriors, labels)
        loss_2 = torch.sqrt(torch.sum(weight_para ** 2))

        return loss_1 + loss_2
