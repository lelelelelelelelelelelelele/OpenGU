import json
import torch
from torch import nn
from torch.nn import functional as F
class LabelEntropyLoss(nn.Module):
    def __init__(self, labels, n_classes):
        super(LabelEntropyLoss, self).__init__()
        self.one_hot = F.embedding(input=labels, weight=torch.eye(n_classes).to(labels.device))
        self.one_hot = nn.Parameter(self.one_hot, requires_grad=False)

    def forward(self, partition):
        shard_samples = partition.T @ self.one_hot + 1e-5 # Avoid division by zero
        shard_dists = (shard_samples) / torch.sum(shard_samples, dim=1, keepdim=True)
        shard_entropy = torch.sum(torch.mean(-shard_dists * torch.log(shard_dists), dim=1))

        return shard_entropy
labels=torch.tensor([0,0,1,1])
loss=LabelEntropyLoss(labels,2)
balanced=torch.tensor([[1.,0.],[0.,1.],[1.,0.],[0.,1.]])
segregated=torch.tensor([[1.,0.],[1.,0.],[0.,1.],[0.,1.]])
print(json.dumps(dict(balanced=float(loss(balanced)),segregated=float(loss(segregated)))))
