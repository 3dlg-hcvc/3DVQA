import torch
import torch.nn as nn
from language import language
import torch.nn.functional as F
from pointnet import PointNet3dvqa
from torch.nn.utils.weight_norm import weight_norm
from fc import FCNet
from config import config

class vqamodel(nn.Module):
    def __init__(self, output_size, embedding_dim, hidden_dim, method):
        super(vqamodel,self).__init__()
        args = config()
        self.v_proj = FCNet([16, embedding_dim], 0.2)
        self.q_proj = FCNet([embedding_dim, embedding_dim], 0.2)
        self.drop = nn.Dropout(0.2)
        self.linear = weight_norm(nn.Linear(embedding_dim, 1), dim=None)
        self.use_attention = args.fused_attention
        self.pp = PointNet3dvqa()
        self.lang = language(embedding_dim, hidden_dim)
        if self.use_attention: d = 16
        else: d = 0
        self.combined = nn.Sequential(
        nn.Linear(embedding_dim+d, int(output_size/2)),
        nn.ReLU(inplace=True),
        nn.Dropout(0.7),
        nn.Linear(int(output_size/2),output_size)
                )

    def forward(self, Q, pc):
        feat = self.pp(pc)
        object_vec = feat[4]
        q_reps, _ = self.lang(Q)
        q_reps = q_reps.squeeze()
        reps = q_reps
        if self.use_attention == True:
            v_proj = self.v_proj(object_vec)
            q_proj = self.q_proj(q_reps).unsqueeze(1)
            logits = self.linear(self.drop(v_proj * q_proj))
            att = nn.functional.softmax(logits, 1)
            v_emb = (att * object_vec).sum(1)
            reps = torch.cat((q_reps, v_emb.float()),1)


        score_fc = self.combined(reps)
        return(score_fc)
