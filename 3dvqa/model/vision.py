import torch
import torch.nn as nn
import torch.nn.functional as F

class vision_pointnet(nn.Module):
    def __init__(self, embedding_dim):
        super(vision_pointnet, self).__init__()
        self.layer = nn.Linear(512, embedding_dim)
        self.conv1 = nn.Conv1d(1024, 300, 5, padding=2)
        self.norm1 = nn.BatchNorm1d(300)

    def forward(self, object_vec):
        x = self.conv1(F.relu(object_vec))
        x = self.norm1(x)
        return x
