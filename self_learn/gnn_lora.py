import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
# from torch_geometric.nn import GCNConv, GATConv
from self_structure import norm,self_GCN, self_GAT
import numpy as np
from matplotlib import pyplot as plt
import torch.nn as nn
# 1. 超参数
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
lr = 0.01

weight_decay = 5e-4
hidden = 4
dropout = 0.5
epochs = 200
seed = 42

torch.manual_seed(seed)
np.random.seed(seed)

# 2. 载入 Cora
dataset = Planetoid(root='./data', name='Cora')
data = dataset[0].to(device)

node = data.num_nodes
edge = data.edge_index

# print("edge_index:", edge.shape)

# A = norm(node, edge, device=device)
def feng():
    from torch_geometric.nn import GATConv, GCNConv

    class GAT(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = GATConv(dataset.num_features, 8, heads=8, dropout=0.6)
            self.conv2 = GATConv(64, dataset.num_classes, heads=1, dropout=0.6)

        def forward(self, x, edge_index):
            x = F.dropout(x, p=0.6, training=self.training)
            x = F.elu(self.conv1(x, edge_index))
            x = F.dropout(x, p=0.6, training=self.training)
            x = self.conv2(x, edge_index)
            return x
    # 3. 定义 2-layer GCN
    class GCN(torch.nn.Module):
        def __init__(self, in_channels, hidden_channels, out_channels):
            super().__init__()
            self.conv1 = GCNConv(in_channels, hidden_channels)
            self.conv2 = GCNConv(hidden_channels, out_channels)

        def forward(self, x, edge_index):
            x = self.conv1(x, edge_index)
            x = F.relu(x)
            x = F.dropout(x, p=dropout, training=self.training)
            x = self.conv2(x, edge_index)
            return x

# model = GCN(dataset.num_features, hidden, dataset.num_classes).to(device)
# model = self_GCN(dataset.num_features, hidden, dataset.num_classes).to(device)
model = self_GAT(dataset.num_features, hidden, dataset.num_classes, k_head=8).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
# decreasing lr
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.1)
# lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10)

# 4. 训练与评估
def train():
    model.train()
    optimizer.zero_grad()
    out = model(data.x, edge)
    loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()
    return loss.item()

@torch.no_grad()
def test():
    model.eval()
    logits = model(data.x, edge)
    masks = ['train_mask', 'val_mask', 'test_mask']
    accs = []
    # val_loss = F.cross_entropy(logits[data.val_mask], data.y[data.val_mask])
    lr_scheduler.step()
    for mask in masks:
        pred = logits[getattr(data, mask)].argmax(1)
        true = data.y[getattr(data, mask)]
        acc = (pred == true).float().mean().item()
        accs.append(acc)
    return accs

def visualization(epochs, loss, train_acc, test_acc, step=20):
    # epochs = np.arange(1, epoch +2, step)
    # print(epochs)
    plt.plot(epochs, train_acc, label='Train Accuracy')
    plt.plot(epochs, test_acc, label='Test Accuracy')
    plt.plot(epochs, loss, label='Train Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Training and Test Accuracy')
    plt.legend()
    plt.show()
train_losses = []
train_accs = []
test_accs = []
epoch_ = []
best_val_acc = best_test_acc = 0
for epoch in range(0, epochs+1):
    loss = train()
    train_acc, val_acc, test_acc = test()
    
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_test_acc = test_acc
    if epoch % 20 == 0 or epoch == epochs or val_acc == best_val_acc:
        print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, '
              f'Train: {train_acc:.4f}, Val: {val_acc:.4f}, '
              f'Test: {test_acc:.4f}')
        train_losses.append(loss)
        train_accs.append(train_acc)
        test_accs.append(test_acc)
        epoch_.append(epoch)

print(f'Best Test Accuracy: {best_test_acc * 100:.2f}%')
# visualization
visualization(epoch_, train_losses, train_accs, test_accs)