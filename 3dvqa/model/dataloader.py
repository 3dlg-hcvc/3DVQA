import torch
import h5py
from constant import constant
from config import config

class MyDataLoader(torch.utils.data.Dataset):
    def __init__(
        self,
        im_out,
        max_len,
        complete_list,
        ModelID,
        QuestionList,
        Correct_Answer,
        embeddings_dict,
        method,
        mode,
    ):
        self.max_len = max_len
        self.im_out = im_out
        self.ModelID = ModelID
        self.QuestionList = QuestionList
        self.Correct_Answer = Correct_Answer
        self.embeddings_dict = embeddings_dict
        self.size = len(Correct_Answer)
        self.method = method
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

        if self.method == "pointnet" or self.method == "votenet" or self.method == "pointnet_only" or self.method == "votenet_only" :

            if self.method == "votenet" or self.method == "votenet_only":
                with h5py.File(args.votenet_hdf5, "r") as f:
                    point_out = f[model_idx][:]
                    point_out = torch.from_numpy(point_out).float()

            elif self.method == "pointnet" or self.method == "pointnet_only":
                with h5py.File(args.pointnet_hdf5, "r") as f:
                    point_out = f[model_idx][:]
                    point_out = torch.from_numpy(point_out).float()

            return (
                self.QuestionList[index],
                self.Correct_Answer[index],
                Question1.cuda(),
                point_out.cuda(),
                self.indxs[index].cuda(),
                self.ModelID[index],
            )

        if self.method == "2dvqa" or self.method == "2dvqa_only":
            return (
                self.QuestionList[index],
                self.Correct_Answer[index],
                Question1.cuda(),
                self.im_out[self.ModelID[index]].cuda(),
                self.indxs[index].cuda(),
                self.ModelID[index],
            )

        if self.method == "lstm":
            return (
                self.QuestionList[index],
                self.Correct_Answer[index],
                Question1.cuda(),
                torch.tensor([]).cuda(),
                self.indxs[index].cuda(),
                self.ModelID[index],
            )

    def __len__(self):
        return self.size
