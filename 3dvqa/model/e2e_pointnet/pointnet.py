'''This part of code comes from pytorch
implementation of pointnet++ repo: https://github.com/daveredrum/Pointnet2.ScanNet
'''

import torch
import torch.nn as nn
import sys
sys.path.insert(0,"/localhome/yetesam/Desktop/Pointnet2.ScanNet/pointnet2")
import torch.nn.functional as F
from pointnet2_modules import PointnetFPModule, PointnetSAModule
from torch.utils.data import DataLoader

class PointNet3dvqa(nn.Module):
    def _break_up_pc(self, pc):
        xyz = pc[..., :3].contiguous()
        features = pc[..., 3:].transpose(1, 2).contiguous() if pc.size(-1) > 3 else None
        return xyz, features

    def __init__(self):
        super(PointNet3dvqa, self).__init__()
        self.SA_modules = nn.ModuleList()
        self.SA_modules.append(
            PointnetSAModule(
                npoint=1024,
                radius=0.1,
                nsample=32,
                mlp=[3, 32, 32, 64],
                use_xyz=True,
            )
        )
        self.SA_modules.append(
            PointnetSAModule(
                npoint=256,
                radius=0.2,
                nsample=32,
                mlp=[64,64, 64, 128],
                use_xyz=False,
            )
        )
        self.SA_modules.append(
            PointnetSAModule(
                npoint=64,
                radius=0.4,
                nsample=32,
                mlp=[128, 128, 128, 256],
                use_xyz=False,
            )
        )
        self.SA_modules.append(
            PointnetSAModule(
                npoint=16,
                radius=0.8,
                nsample=32,
                mlp=[256,256, 256, 512],
                use_xyz=False,
            )
        )

        self.FP_modules = nn.ModuleList()
        self.FP_modules.append(PointnetFPModule(mlp=[256 + 128, 256, 256]))
        self.FP_modules.append(PointnetFPModule(mlp=[512 + 256, 256, 256]))

        self.fc_lyaer = nn.Sequential(
            nn.Conv1d(256,128, kernel_size=5,padding=2, bias=False),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(5,padding=2),
            nn.BatchNorm1d(128),
            nn.Conv1d(128, 30, kernel_size=3,padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(3,padding=1),
            nn.BatchNorm1d(30),
            nn.Conv1d(30,10,kernel_size=3,padding=1),
            nn.ReLU(inplace=True)
        )

    def forward(self, pointcloud):
        r"""
            Forward pass of the network
            Parameters
            ----------
            pointcloud: Variable(torch.cuda.FloatTensor)
                (B, N, 3 + input_channels) tensor
                Point cloud to run predicts on
                Each point in the point-cloud MUST
                be formated as (x, y, z, features...)
        """
        pointcloud = pointcloud.squeeze()
        xyz, features = self._break_up_pc(pointcloud)

        l_xyz, l_features = [xyz], [features]
        for i in range(len(self.SA_modules)):
            li_xyz, li_features = self.SA_modules[i](l_xyz[i], l_features[i])
            l_xyz.append(li_xyz)
            l_features.append(li_features)
        r_xyz = l_xyz
        r_feature = l_features
        for i in range(-1, -(len(self.FP_modules) + 1), -1):
            l_features[i - 1] = self.FP_modules[i](
                l_xyz[i - 1], l_xyz[i], l_features[i - 1], l_features[i]
            )
        return r_feature
