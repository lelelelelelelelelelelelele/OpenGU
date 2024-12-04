import logging
import torch

torch.cuda.empty_cache()

from sklearn.metrics import f1_score
import numpy as np

from unlearning.unlearning_methods.GraphEraser.aggregation.optimal_aggregator import OptimalAggregator
from dataset.original_dataset import original_dataset
from utils.dataset_utils import *

class Aggregator:
    def __init__(self, run, target_model, data, shard_data, args,logger,affected_shard=None):
        self.logger = logger
        self.args = args

        self.data_store = original_dataset(self.args,logger)

        self.run = run
        self.target_model =target_model
        self.data = data
        self.shard_data = shard_data
        self.affected_shard = affected_shard
        self.num_shards = args['num_shards']

    def generate_posterior(self, suffix=""):
        self.true_label = self.shard_data[0].y[self.shard_data[0]['test_mask']].detach().cpu().numpy()
        self.posteriors = {}

        for shard in range(self.args['num_shards']):
            self.target_model.data = self.shard_data[shard]
            if self.affected_shard is not None and shard in self.affected_shard:
                load_target_model(self.logger,self.args,self.run, self.target_model, shard, "_unlearned")
            else:
                load_target_model(self.logger, self.args, self.run, self.target_model, shard, "")
            # if self.args['base_model'] == 'SAGE':
            #     self.posteriors[shard] = self.target_model.posterior()
            # else:
            #9.20
            # self.posteriors[shard] = self.target_model.posterior_other()
            self.posteriors[shard] = self.target_model.posterior()
        self.logger.info("Saving posteriors.")
        save_posteriors(self.logger,self.args,self.posteriors, self.run, suffix)

    def aggregate(self,data):
        if self.args['aggregator'] == 'mean':
            aggregate_f1_score = self._mean_aggregator(data)
        elif self.args['aggregator'] == 'optimal':
            aggregate_f1_score = self._optimal_aggregator(data)
        elif self.args['aggregator'] == 'majority':
            aggregate_f1_score = self._majority_aggregator(data)
        else:
            raise Exception("unsupported aggregator.")

        return aggregate_f1_score

    def _mean_aggregator(self,data):
        posterior = self.posteriors[0]
        for shard in range(1, self.num_shards):
            posterior += self.posteriors[shard]

        posterior = posterior / self.num_shards
        return f1_score(self.true_label, posterior.argmax(axis=1).cpu().numpy(), average="micro")

    def _majority_aggregator(self,data):
        pred_labels = []
        for shard in range(self.num_shards):
            pred_labels.append(self.posteriors[shard].argmax(axis=1).cpu().numpy())

        pred_labels = np.stack(pred_labels)
        pred_label = np.argmax(
            np.apply_along_axis(np.bincount, axis=0, arr=pred_labels, minlength=self.posteriors[0].shape[1]), axis=0)

        return f1_score(self.true_label, pred_label, average="micro")

    def _optimal_aggregator(self,original_data):
        optimal = OptimalAggregator(self.run, self.target_model, self.data, self.args,self.logger)
        optimal.generate_train_data(original_data)
        weight_para = optimal.optimization()
        save_optimal_weight(self.logger,self.args, weight_para, run=self.run)

        posterior = self.posteriors[0] * weight_para[0]
        for shard in range(1, self.num_shards):
            posterior += self.posteriors[shard] * weight_para[shard]

        return f1_score(self.true_label, posterior.argmax(axis=1).cpu().numpy(), average="micro")
