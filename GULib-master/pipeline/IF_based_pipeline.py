import numpy as np
from task import get_trainer
BLUE_COLOR = "\033[34m"
RESET_COLOR = "\033[0m"
class IF_based_pipeline:
    """
    这是一个最基础的IF_based_Pipeline，需要实现其中的所有函数。
    如果您不想从头实现，请从IF方法的派生类中继承，而不是继承此类。
    """
    def __init__(self,args,logger,model_zoo):
        self.args = args
        self.logger = logger
        self.data = model_zoo.data
        self.model_zoo = model_zoo
        self.num_runs = self.args["num_runs"]
        self.run = 0
        self.num_shards = self.args["num_shards"]
        self.poison_f1 = np.zeros(self.args["num_runs"])
        self.average_f1 = np.zeros(self.args["num_runs"])
        self.average_auc = np.zeros(self.args["num_runs"])
        self.avg_partition_time = np.zeros(self.args["num_runs"])
        self.avg_training_time = np.zeros(self.args["num_runs"])
        self.avg_unlearning_time = np.zeros(self.args["num_runs"])
        # self.training_time = np.zeros(self.num_runs)
        self.deleted_nodes = np.array([])
        self.feature_nodes = np.array([])
        self.influence_nodes = np.array([])
        self.deleted_edges = np.array([])
        self.influence_edges = np.array([])
        self.num_feats = self.data.num_features
    
    def run_exp(self):
        for self.run in range(self.args['num_runs']):
            self.target_model_name = self.args['base_model']
            self.determine_target_model()
            self.train_original_model(self.run)
            self.unlearning_request()
            self.unlearn()
            
            
            if self.args["unlearn_task"]=="node" and self.args["downstream_task"]=="node":
                self.mia_attack()
            # elif self.args["unlearn_task"]=="edge":
            #     self.mia_attack_edge()
                
        
        self.logger.info(
        "{}Performance Metrics:\n"
        " - Poison F1 Score: {:.4f} ± {:.4f}\n"
        " - Unlearn F1 Score: {:.4f} ± {:.4f}\n"
        " - Average AUC Score: {:.4f} ± {:.4f}\n"
        " - Average Training Time: {:.4f} ± {:.4f}\n"
        " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
            BLUE_COLOR,
            np.mean(self.poison_f1), np.std(self.poison_f1),
            np.mean(self.average_f1), np.std(self.average_f1),
            np.mean(self.average_auc), np.std(self.average_auc),
            np.mean(self.avg_training_time), np.std(self.avg_training_time),
            np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
            RESET_COLOR
            )
        )
        pass
    
    def unlearning_request(self):
        pass
    
    def determine_target_model(self):
        # self.args["unlearn_trainer"] = trainer
        # self.target_model = get_trainer(self.args,self.logger,self.model_zoo.model,self.data)
        pass
    def train_original_model(self,run):
        pass
    
    def approxi(self,result_tuple):
        pass
    
    def mia_attack(self):
        pass
    
    def get_if_grad(self,run):
        pass

    def mia_attack_edge(self):
        pass
    
    def unlearn(self):
        pass
    