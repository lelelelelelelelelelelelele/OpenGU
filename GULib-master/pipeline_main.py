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
from utils.dataset_utils import process_data,save_data
from attack.Attack_methods.GraphEraser_MIA import GraphEraser_Attack
from attack.Attack_methods.GUIDE_MIA import GUIDE_MIA
from unlearning_manager import UnlearningManager
from pipeline.Shard_based_pipeline import Shard_based_pipeline
from pipeline.IF_based_pipeline import IF_based_pipeline
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
    args["num_unlearned_nodes"] = int(data.num_nodes * args["proportion_unlearned_nodes"])
    # assert args["num_unlearned_nodes"] == int(data.num_nodes * args["proportion_unlearned_nodes"]), (
    #     "Mismatch detected: 'num_unlearned_nodes' (value: {}) is not equal to the calculated value based on 'proportion_unlearned_nodes' (value: {})."
    #     .format(args["num_unlearned_nodes"], int(data.num_nodes * args["proportion_unlearned_nodes"])))


    data = process_data(logger,data,args)

    #model
    model_zoo = model_zoo(args,data)
    model = model_zoo.model
    if args["base_model"] not in ["GST","Projector"]:
        logger.log_model_info(model)   

    args["partition_method"] = "fast"
    method = Shard_based_pipeline(args,logger,model_zoo)
    method.run_exp()


