import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)

""" This is our language encoder consisting of
    one LSTM. Input Q is a list of question's
    word embeddings """


class language(nn.Module):
    def __init__(self, embedding_dim, hidden_dim):
        super(language, self).__init__()
        self.use_attention = True
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.attention = nn.Linear(embedding_dim, embedding_dim)
        self.contex = nn.Linear(embedding_dim, 1)
        self.language = nn.Sequential(
            nn.Linear(embedding_dim, embedding_dim),
            nn.ReLU(inplace=True),
            nn.Dropout(0.8),
        )

    def forward(self, Q):
        att_in = torch.tensor([]).cuda()
        hidden = (
            torch.zeros(1, Q.shape[0], self.hidden_dim).cuda(),
            torch.zeros(1, Q.shape[0], self.hidden_dim).cuda(),
        )
        for w in range(Q.shape[1]):
            words = Q[:, w, :].unsqueeze(1)
            out, hidden = self.lstm(words, hidden)
            att_in = torch.cat((att_in, hidden[0]), 0)

        if self.use_attention == True:
            att_in = att_in.permute(1, 0, 2)
            att_weight = torch.tanh(self.attention(att_in))
            att_weight = F.softmax(self.contex(att_weight), dim=1)
            att_out = torch.bmm(att_weight.permute(0, 2, 1), att_in)
            final = self.language(att_out.squeeze())

        else:
            final = self.language(out)

        return final.squeeze(), att_in
