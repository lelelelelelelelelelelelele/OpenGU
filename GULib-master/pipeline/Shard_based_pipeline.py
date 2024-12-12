import numpy as np
import networkx as nx
import time
import torch
import random
from utils import dataset_utils
from utils import utils
from utils.dataset_utils import *

# from pipeline.Shard_based_components.Partition.graph_partition import GraphPartition
# from pipeline.Shard_based_components.Aggregation.aggregator import Aggregator
# from pipeline.Shard_based_components.Aggregation.aggregator_guide import Aggregator_GUIDE
# from pipeline.Shard_based_components.Partition.kernel_vector import PyramidMatchVector
from task import get_trainer
from memory_profiler import profile
BLUE_COLOR = "\033[34m"
RESET_COLOR = "\033[0m"

class Shard_based_pipeline:
    def __init__(self,args,logger,model_zoo):
        self.args = args
        self.logger = logger
        self.data = model_zoo.data
        self.model_zoo = model_zoo
        self.run = 0
        self.num_shards = self.args["num_shards"]
        self.poison_f1 = np.zeros(self.args["num_runs"])
        self.average_f1 = np.zeros(self.args["num_runs"])
        self.average_auc = np.zeros(self.args["num_runs"])
        self.average_acc = np.zeros(self.args["num_runs"])
        self.avg_partition_time = np.zeros(self.args["num_runs"])
        self.avg_training_time = np.zeros(self.args["num_runs"])
        self.avg_unlearning_time = np.zeros(self.args["num_runs"])
        pass
    
    @profile
    def run_exp_mem(self):
        for self.run in range(self.args["num_runs"]):
            seed_everything(2024 + self.run)
            self.exp_partition()
            self.exp_train()
            self.exp_unlearn()
            
            
    def run_exp(self):
        for self.run in range(self.args["num_runs"]):
            
            self.exp_partition()
            self.exp_train()
            self.exp_unlearn()
            
            
                # 输出带有红色文字的日志
        self.logger.info(
            "{}Performance Metrics:\n"
            " - Poison F1 Score: {:.4f} ± {:.4f}\n"
            " - Unlearn F1 Score: {:.4f} ± {:.4f}\n"
            " - Unlearn Acc for Graph Cls: {:.4f} ± {:.4f}\n"
            " - Average AUC Score: {:.4f} ± {:.4f}\n"
            " - Average Partition Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Training Time: {:.4f} ± {:.4f} seconds\n"
            " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
                BLUE_COLOR,
                np.mean(self.poison_f1), np.std(self.poison_f1),
                np.mean(self.average_f1), np.std(self.average_f1),
                np.mean(self.average_acc), np.std(self.average_auc),
                np.mean(self.average_auc), np.std(self.average_auc),
                np.mean(self.avg_partition_time), np.std(self.avg_partition_time),
                np.mean(self.avg_training_time), np.std(self.avg_training_time),
                np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
                RESET_COLOR
            )
        )
        self.logger.info(self.avg_partition_time)
        self.logger.info(self.avg_unlearning_time)
            
    def exp_partition(self):
        """
        Basic Data Partition -> *num_shard* shards
        
        Applied for GraphEraser, GraphEevoker
        
        GUIDE with different method.
        """
        self.args["exp"] = "partition"
        self.gen_train_graph()
        self.graph_partition()
        self.generate_shard_data()
        pass
    
    def exp_train(self):
        """
        Basic Unlearn Training
        
        Get original model
        """
        self.args["exp"] = "unlearning"
        self.load_data()
        self.determine_target_model()
        self.train_shard_model()
        self.aggregate_shard_model()
        
        pass
    def exp_unlearn(self):
        """
        Evaluate Unlearning and Attack_Unlearning
        """
        self.args["exp"] = "attack_unlearning"
        self.generate_requests()
        self.unlearn()
        self.attack_unlearning()
            
            
    def gen_train_graph(self):
        pass

    def graph_partition(self):
        pass
        
    def generate_shard_data(self):
        pass
            
    def load_data(self):
        pass
        
    def determine_target_model(self):
        pass

    def train_shard_model(self):
        pass
    
    def aggregate_shard_model(self):
        pass
    
    def generate_requests(self):
        pass
    
    def unlearn(self):
        pass
    
    def attack_unlearning(self):
        pass
    
    
def seed_everything(seed_value):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    os.environ['PYTHONHASHSEED'] = str(seed_value)

    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True