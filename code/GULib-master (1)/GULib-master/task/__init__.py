from task.BaseTrainer import BaseTrainer
from task.GUIDETrainer import GUIDETrainer
from task.GNNDeleteTrainer import GNNDeleteTrainer
from task.GIFTrainer import GIFTrainer
from task.SGUTrainer import SGUTrainer
from task.GSTTrainer import GSTTrainer
from task.MEGUTrainer import MEGUTrainer
from task.GUKDTrainer import GUKDTrainer
from task.D2DGNTrainer import D2DGNTrainer
from task.IDEATrainer import IDEATrainer
trainer_mapping = {
    'BaseTrainer': BaseTrainer,
    'GUIDETrainer': GUIDETrainer,
    'GNNDeleteTrainer': GNNDeleteTrainer,
    'GIFTrainer': GIFTrainer,
    'SGUTrainer': SGUTrainer,
    'GSTTrainer': GSTTrainer,
    'MEGUTrainer': MEGUTrainer,
    'GUKDTrainer':GUKDTrainer,
    'D2DGNTrainer':D2DGNTrainer,
    'IDEATrainer':IDEATrainer,
}


def get_trainer(args, logger, model, data):
    return trainer_mapping[args["unlearn_trainer"]](args, logger, model, data)
    
