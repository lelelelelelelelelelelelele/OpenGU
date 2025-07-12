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
from unlearning.unlearning_methods.SGU import sgu
from unlearning.unlearning_methods.Projector.projector import projector
from unlearning_manager import UnlearningManager
from config import unlearning_path
import sys 
import os
# import copy
# import optuna


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
    data = process_data(logger,data,args)
    
    #model
    model_zoo = model_zoo(args,data)
    model = model_zoo.model
    if args["base_model"] not in ["GST","Projector"]:
        logger.log_model_info(model)   
    
    
    manager = UnlearningManager(args, original_data, data, logger, model_zoo, dataset)
    GU_method = manager.get_method()
    if args["cal_mem"] is True:
        args["num_runs"] = 1
        GU_method.run_exp_mem()
    else:
        GU_method.run_exp()
 

