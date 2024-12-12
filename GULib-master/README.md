## 数据集：

Cora Citeseer PubMed Ogbn-arvix

## 模型：

GraphEraser，GNNDelete，CGU，SGU

## SGU：

特征预处理

训练模型（如果有训练好的就直接读取）

- **影响力传播：**

​		选取10%unlearning nodes（有则读取，否则从train set里面随机选取）

​		计算特征相似度和节点标签相似度（求和）

​		寻找激活节点

- 遗忘学习阶段：

```python
self.NodeClassfier.SGU_unlearning(self.original_softlabels,
                                           self.original_w,
                                           self.unlearning_nodes,
                                           self.activated_nodes,
                                           self.pos_pair,
                                           self.neg_pair,
                                           self.features,
                                           self.prototype_embedding)
```

​		遗忘：

​			**unlearning nodes**：打乱标签，交叉熵损失（将遗忘节点的标签打乱，不是随机赋类别）

```python
loss_pU = F.cross_entropy(softlabels_U, random_class.to(self.device))
```

​			**activated nodes**：对比学习，正样本（属于同类别但是不属于unlearning nodes和activated nodes）每个节点对应5个，求取平均，负样本（一半比重选择自己，另一半选择同类别属于unlearning nodes和activated nodes当中的节点），每个节点对应10个，求取平均，平均->加快运算速度

```python
loss_hE = -torch.log(pos_scores / neg_scores).sum()
```

​		维持：

​			**activated nodes**：KL散度减小训练前后软标签变化，维持准确

```python
loss_pE = F.kl_div(torch.log(softlabels_E + smooth_factor),original_softlabels[activated_nodes] + smooth_factor, reduction='batchmean')
```

​		 	**权重参数W：**用MSE损失规范

```python
for i in range(len(original_w)):
	delta_w = (w_U[i] - original_w[i])
	loss_w += torch.norm(delta_w)
creterion_MSE = torch.nn.MSELoss(reduction="mean")
```

​			





