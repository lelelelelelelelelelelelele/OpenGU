# from dataset.original_dataset import original_dataset
# from parameter_parser import parameter_parser
# from utils.logger import create_logger

# args = parameter_parser()
# logger = create_logger(args)


# original_data = original_dataset(args,logger)
# data,dataset = original_data.load_data()
import torch.nn.functional as F
import torch
a = torch.tensor([[0.5],[0.4],[0.5]])
b = torch.tensor([[0.3],[0.7],[0.5]])
a = torch.log(a)
b
print(a,b)
loss = F.kl_div(a,b)
print(loss)