import numpy as np
BLUE_COLOR = "\033[34m"
RESET_COLOR = "\033[0m"
class Learning_based_pipeline:
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
        self.avg_training_time = np.zeros(self.args["num_runs"])
        self.avg_unlearning_time = np.zeros(self.args["num_runs"])
        self.avg_sampling_time = np.zeros(self.args["num_runs"])
        
    def run_exp(self):
        for self.run in range(self.args['num_runs']):
            self.determine_target_model()
            self.train_original_model()
            self.unlearning_request()
            self.unlearn()
            if self.args["downstream_task"] == "node" and self.args["unlearn_task"]=="node":
                self.mia_attack()
            elif self.args["unlearn_task"]=="edge":
                self.mia_attack_edge()
        self.logger.info(
        "{}Performance Metrics:\n"
        " - Poison F1 Score: {:.4f} ± {:.4f}\n"
        " - Unlearn F1 Score: {:.4f} ± {:.4f}\n"
        " - Average AUC Score: {:.4f} ± {:.4f}\n"
        " - Average Training Time: {:.4f} ± {:.4f}\n"
        " - Average Sampling Time: {:.4f} ± {:.4f} seconds\n"
        " - Average Unlearning Time: {:.4f} ± {:.4f} seconds{}".format(
            BLUE_COLOR,
            np.mean(self.poison_f1), np.std(self.poison_f1),
            np.mean(self.average_f1), np.std(self.average_f1),
            np.mean(self.average_auc), np.std(self.average_auc),
            np.mean(self.avg_training_time), np.std(self.avg_training_time),
            np.mean(self.avg_sampling_time), np.std(self.avg_sampling_time),
            np.mean(self.avg_unlearning_time), np.std(self.avg_unlearning_time),
            RESET_COLOR
            )
        )
            
    def determine_target_model(self):
        pass
            
    def train_original_model(self):
        pass
            
    def unlearning_request(self):
        pass
    
    def unlearn(self):
        pass
    
    def mia_attack(self):
        pass
    
    def mia_attack_edge(self):
        pass