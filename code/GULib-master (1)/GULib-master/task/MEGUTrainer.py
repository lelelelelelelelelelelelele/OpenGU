import torch.nn.functional as F
import time
import torch
import copy
import numpy as np
from tqdm import tqdm
from task import BaseTrainer
from config import root_path
from sklearn.metrics import f1_score, accuracy_score,recall_score

class MEGUTrainer(BaseTrainer):
    def __init__(self, args, logger, model, data):
        super().__init__(args, logger, model, data)

    