import torch.nn as nn
from torch.nn.utils.weight_norm import weight_norm
"""
This is the source we used for this code:
https://github.com/BierOne/bottom-up-attention-vqa/tree/44ac1d747b3dabb620e77dbafd1feece4d1c478b
"""

class FCNet(nn.Module):
    def __init__(self, dims, dropout=0.0, norm=True):
        super(FCNet, self).__init__()
        self.num_layers = len(dims) -1
        self.drop = dropout
        self.norm = norm
        self.main = nn.Sequential(*self._init_layers(dims))

    def _init_layers(self, dims):
        layers = []
        for i in range(self.num_layers):
            in_dim = dims[i]
            out_dim = dims[i + 1]
            if self.norm:
                layers.append(weight_norm(nn.Linear(in_dim, out_dim), dim=None))
            else:
                layers.append(nn.Linear(in_dim, out_dim))
            layers.append(nn.ReLU())
        return layers

    def forward(self, x):
        return self.main(x)
