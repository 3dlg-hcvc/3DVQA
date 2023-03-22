import torch
import h5py
from constant import constant
from config import config

class MyDataLoader(torch.utils.data.Dataset):
    def __init__(
        self,
        max_len,
        complete_list,
        ModelID,
        QuestionList,
        Correct_Answer,
        embeddings_dict,
    ):
        self.max_len = max_len
        self.ModelID = ModelID
        self.QuestionList = QuestionList
        self.Correct_Answer = Correct_Answer
        self.embeddings_dict = embeddings_dict
        self.size = len(Correct_Answer)
        indxs = torch.tensor([])
        for j in range(len(Correct_Answer)):
            i = Correct_Answer[j]
            if i in complete_list:
                indx = complete_list.index(i)
            else:
                indx = complete_list.index("")
            indx = torch.tensor(indx, dtype=torch.float32)
            indxs = torch.cat((indxs, indx.unsqueeze(0)), 0)
        self.indxs = indxs

    def __getitem__(self, index):
        args = config()
        correction = constant.correction
        model_idx = self.ModelID[index]
        question = self.QuestionList[index]
        for cor in correction:
            if cor in question.split(" "):
                question = question.replace(cor, correction[cor])
        Question1 = torch.tensor([])
        for j in question.split()[:-1]:
            Question1 = torch.cat((Question1, self.embeddings_dict[j].view(1, 300)), 0)
        while Question1.shape[0] < self.max_len:
            Question1 = torch.cat((Question1, torch.zeros(1, 300)), 0)

        with h5py.File(args.path_pc,'r') as f:
            point_out = f[self.ModelID[index]][:]
            point_out = torch.from_numpy(point_out).float()
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        return self.QuestionList[index], self.Correct_Answer[index], Question1.to(device), point_out.to(device), self.indxs[index].to(device), self.ModelID[index]

    def __len__(self):
        return self.size
