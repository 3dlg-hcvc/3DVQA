import torch
import torch.nn as nn
from language import language
from vision import vision_pointnet
import torch.nn.functional as F
from utils import PreTrainedResNet
from config import config
from torch.nn.utils.weight_norm import weight_norm
from fc import FCNet
torch.manual_seed(0)

class vqamodel(nn.Module):
    def __init__(self, output_size, embedding_dim, hidden_dim, method):
        super(vqamodel, self).__init__()
        args = config()
        self.use_attention = args.fused_attention
        self.use_attention_bc = False
        self.method = method

        if method == "votenet" :
            c2 = 4444
            self.v_proj = FCNet([4144, embedding_dim], 0.2)
            self.q_proj = FCNet([embedding_dim, embedding_dim], 0.2)
            self.drop = nn.Dropout(0.2)
            self.linear = weight_norm(nn.Linear(embedding_dim, 1), dim=None)
            if not self.use_attention:
                self.visual_adj = nn.Linear(256 , 1)

        if method == "2dvqa" :
            self.v_proj = FCNet([16, embedding_dim], 0.2)
            self.q_proj = FCNet([embedding_dim, embedding_dim], 0.2)
            self.drop = nn.Dropout(0.2)
            self.linear = weight_norm(nn.Linear(embedding_dim, 1), dim=None)
            self.res = PreTrainedResNet(embedding_dim, True)
            if self.use_attention:
                c2 = embedding_dim + 16
            else:
                c2 = embedding_dim * 2

        if method == "pointnet":
            if self.use_attention:
                c2 = embedding_dim + 16
            else:
                c2 = embedding_dim*2
            self.vis = vision_pointnet(embedding_dim)
            #self.wot = nn.Conv1d(16, 1, kernel_size=1)
            self.wot = nn.Linear(16, 1)
            self.v_proj = FCNet([16, embedding_dim], 0.2)
            self.q_proj = FCNet([embedding_dim, embedding_dim], 0.2)
            self.drop = nn.Dropout(0.2)
            self.linear = weight_norm(nn.Linear(embedding_dim, 1), dim=None)

        if method == "lstm" :
            c2 = embedding_dim

        if method == "votenet_only":
            c2 = 4144
            self.visual_adj = nn.Linear(256 , 1)

        if method == "2dvqa_only":
            self.res = PreTrainedResNet(embedding_dim, True)
            c2 = embedding_dim

        if method == "pointnet_only":
            self.vis = vision_pointnet(embedding_dim)
            self.visadjust = nn.Linear(16, 1)
            c2 = 300

        self.lang = language(embedding_dim,embedding_dim)
        self.combined = nn.Sequential(
        nn.Linear(c2, int(output_size/2)),
        nn.ReLU(inplace=True),
        nn.Dropout(0.7),
        nn.Linear(int(output_size/2),output_size)
         )



    def forward(self, Q, object_vec):
        q_reps , _ = self.lang(Q)

        if self.method == "votenet":         # object_vec size = BS*256*4144
            if self.use_attention == True:
                object_vec = object_vec.view(object_vec.shape[0], object_vec.shape[1], -1)
                v_proj = self.v_proj(object_vec)            # BS*256*300
                q_proj = self.q_proj(q_reps).unsqueeze(1)       # BS*1*300
                logits = self.linear(self.drop(v_proj * q_proj))
                att = nn.functional.softmax(logits, 1)          # BS*256*1
                v_emb = (att * object_vec).sum(1)
                reps = torch.cat((q_reps, v_emb.float()) ,1)
            else:
                #v1 = v1.view(v1.shape[0], v1.shape[1], -1)
                v1 = object_vec.view(object_vec.shape[0], -1, object_vec.shape[1])
                v1 = self.visual_adj(v1)
                v1 = v1.view(v1.shape[0],-1)
                reps = torch.cat((q_reps, v1.squeeze().float()) , 1)


        elif self.method == "votenet_only":
            v1 = object_vec.view(object_vec.shape[0], -1, object_vec.shape[1])  
            v1 = self.visual_adj(v1)
            v1 = v1.view(v1.shape[0],-1)
            reps = v1.squeeze()


        elif self.method == "pointnet":
            v1 = self.vis(object_vec)
            if self.use_attention == True:
                v_proj = self.v_proj(v1)
                q_proj = self.q_proj(q_reps).unsqueeze(1) #BS*1*300
                logits = self.linear(self.drop(v_proj * q_proj))
                att = nn.functional.softmax(logits, 1)          
                v_emb = (att * v1).sum(1)
                reps = torch.cat((q_reps, v_emb.float()),1)
            else:
                reps = torch.cat((q_reps, F.relu(self.wot(v1).squeeze())),1)


        elif self.method == "pointnet_only":
            v1 = self.vis(object_vec)
            v1 = self.visadjust(v1)
            reps = v1.squeeze()


        elif self.method == "2dvqa":
            v1, feat = self.res(object_vec)
            if self.use_attention == True:
                v_proj = self.v_proj(feat)           # 16*256*300
                q_proj = self.q_proj(q_reps).unsqueeze(1)         # 16*1*300
                logits = self.linear(self.drop(v_proj * q_proj))
                att = nn.functional.softmax(logits, 1)
                v_emb = (att * feat).sum(1)
                reps = torch.cat((q_reps, v_emb.float()), 1)
            else:
                reps = torch.cat((q_reps, v1.squeeze()),1).cuda()



        elif self.method == "2dvqa_only":
            v1, feat = self.res(object_vec)
            reps = v1


        elif self.method == "lstm":
            reps = q_reps


        if self.use_attention_bc == True:
            reps_adj = self.repsajust(reps)
            att_weight = torch.tanh(self.attention(att_in))
            if self.method == "lstm":
                att_weight=att_weight.permute(1,0,2)
            att_weight = torch.bmm(att_weight, reps_adj.unsqueeze(2))
            att_weight = F.softmax(att_weight, dim=1)
            output_f = torch.bmm(att_weight.permute(0,2,1),att_in)
            score_fc = self.combined(torch.cat((output_f.squeeze(),reps.squeeze()) , 1))

        else: score_fc = self.combined(reps)

        return(score_fc)
