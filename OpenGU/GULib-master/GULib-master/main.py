import os
import random
# import optuna
import numpy as np
import torch

from model.model_zoo import model_zoo
from dataset.original_dataset import original_dataset
from parameter_parser import parameter_parser
from unlearning.unlearning_methods.CEU.ceu import ceu
from utils.logger import create_logger
from task.node_classification import NodeClassifier
from unlearning.unlearning_methods.GNNDelete.gnndelete import gnndelete
from utils.dataset_utils import process_data,save_data
from attack.Attack_methods.GraphEraser_MIA import GraphEraser_Attack
from attack.Attack_methods.GUIDE_MIA import GUIDE_MIA
from unlearning.unlearning_methods.GraphEraser.grapheraser import grapheraser
from unlearning.unlearning_methods.GUIDE.guide import guide
from unlearning.unlearning_methods.GIF.gif import gif
from unlearning.unlearning_methods.CGU.cgu import cgu
from unlearning.unlearning_methods.GST.gst_based import gst
from unlearning.unlearning_methods.Projector.projector import projector
from unlearning_manager import UnlearningManager
from config import unlearning_path
import sys 
import os
import copy


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

# def objective(trial):
#     para1 = trial.suggest_float('para1', 0.5, 1.5)
#     para2 = trial.suggest_float('para2', 0.0001, 0.01)
#     para3 = trial.suggest_int('para3', 20, 500)
#     para4 = trial.suggest_int('para4', 5, 50)
#     para5 = trial.suggest_int('para5', 2, 50)
#     args["para1"] = para1
#     args["para2"] = para2
#     args["para3"] = para3
#     args["para4"] = para4
#     args["para5"] = para5
#     model_zoo_copy = copy.deepcopy(model_zoo)
#     SGU_instance = SGU(args,logger,model_zoo_copy)
#     # SGU_instance.run = np.random.randint(0,5) 
#     SGU_instance.run_exp()
#     return SGU_instance.best 

#     # return 10*abs(SGU_instance.final_auc-0.5)

# def run_optuna(args,logger):
#     study = optuna.create_study(direction='maximize')
#     study.optimize(objective, n_trials=100)
#     best_params = study.best_params
#     logger.info("最佳超参数：{}".format(best_params) )
#     args["para1"] = best_params["para1"]
#     args["para2"] = best_params["para2"]
#     args["para3"] = best_params["para3"]
#     args["para4"] = best_params["para4"]
#     args["para5"] = best_params["para5"]
#     args["parameter_task"] = "normal"
#     model_zoo_copy = copy.deepcopy(model_zoo)
#     SGU_instance = SGU(args,logger,model_zoo_copy)
#     SGU_instance.run_exp()
#     logger.info("最佳超参数：{}".format(best_params) )


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    sys.path.append(base_dir)

    args = parameter_parser()
    
    logger = create_logger(args)
    seed_everything(2024)

    torch.cuda.set_device(args['cuda'])
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args["cuda"])
 
    #dataset
    original_data = original_dataset(args,logger)
    data,dataset = original_data.load_data()
    # 使用 assert 直接检查 args 中的参数
    assert args["num_unlearned_nodes"] == int(data.num_nodes * args["proportion_unlearned_nodes"]), (
        "Mismatch detected: 'num_unlearned_nodes' (value: {}) is not equal to the calculated value based on 'proportion_unlearned_nodes' (value: {})."
        .format(args["num_unlearned_nodes"], int(data.num_nodes * args["proportion_nodes"])))


    data = process_data(logger,data,args)

    #model
    model_zoo = model_zoo(args,data)
    model = model_zoo.model
    if args["base_model"] not in ["GST","Projector"]:
        logger.log_model_info(model)   
    

    manager = UnlearningManager(args, original_data, data, logger, model_zoo, dataset)
    manager.run()
 



