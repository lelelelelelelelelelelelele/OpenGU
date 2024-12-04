import os
import random
import numpy as np
import torch

from model.model_zoo import model_zoo
from dataset.original_dataset import original_dataset
from parameter_parser import parameter_parser
from utils.logger import create_logger
from utils.dataset_utils import process_data,save_data
from unlearning_manager import UnlearningManager
from config import unlearning_path
import sys 
import os
import copy
from task.edge_prediction import EdgePredictor

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
    # if args["downstream_task"]=="node":
    data = process_data(logger,data,args)
    #model
    MODEL_ZOO = model_zoo(args,data)
    model = MODEL_ZOO.model
    logger.info(model)
    args["num_unlearned_nodes"] = int(data.num_nodes * args["proportion_unlearned_nodes"])
    # edgepredictor = EdgePredictor(args,data,MODEL_ZOO,logger)
    # edgepredictor.train_model()
    manager = UnlearningManager(args, original_data, data, logger, MODEL_ZOO, dataset)
    manager.run()
# D:/Anaconda3-2022/envs/GUL/python.exe d:/Desktop/图神经网络/GULib/test_edge_main.py   
# /home/ai2/anaconda3/envs/GULib/bin/python /home/ai2/GULib/test_edge_main.py
# --partition_method=lpa --num_runs=2 --unlearn_task=node --downstream_task=node --unlearning_method=GraphEraser


# --is_balanced=False



