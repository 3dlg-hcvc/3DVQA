import numpy as np
import json
import torch
import torch.nn as nn
import os
from torchvision import transforms
import cv2
import torchvision.models as models
from torch.hub import load_state_dict_from_url
from typing import Type, Any, Callable, Union, List, Dict, Optional, cast
from torch import Tensor
from collections import OrderedDict
from torchvision.models.resnet import *
from torchvision.models.resnet import BasicBlock, Bottleneck
from torchvision.models.resnet import model_urls


def load_question(path, sets):
    ModelID1 = []
    Answers = []
    Question_list = []
    for fi in sets:
        with open(os.path.join(path , fi + '.json'),'r') as f:
            data = json.load(f)
            for i in data:
                ModelID1.append(fi)
                Question_list.append(i)
                if data[i]["question_type"] == "location":
                    Answers.append(data[i]["answer"][0])
                else:
                    Answers.append(str(data[i]['answer']))
    return ModelID1, Answers, Question_list


def embedding(path):
    with open(path, 'r') as f:
        embeddings_dict = {}
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = torch.Tensor(vector)
    return embeddings_dict


def train_val_lists(args):
    val = []
    train = []
    test = []

    with open(os.path.join(args.splits , "scannetv1_val.txt"), 'r') as files:
        for file in files:
            file = file.replace('\n','')
            if file.endswith('_00') and os.path.exists(args.qa_path + '/' + file +'.json'):
                val.append(file)
    with open(os.path.join(args.splits , "scannetv1_train.txt") , 'r') as files:
        for file in files:
            file = file.replace('\n','')
            if file.endswith('_00') and os.path.exists(args.qa_path + '/' + file +'.json'):
                train.append(file)
    with open(os.path.join(args.splits + "/scannetv1_test.txt"), 'r') as files:
        for file in files:
            file = file.replace('\n','')
            if file.endswith('_00') and os.path.exists(args.qa_path + '/' + file +'.json'):
                test.append(file)
    return train,val,test



class PreTrainedResNet(nn.Module):
    def __init__(self, num_classes, feature_extracting):

        super(PreTrainedResNet, self).__init__()

        self.resnet50 = models.resnet50(pretrained=True)
        if feature_extracting:
            for param in self.resnet50.parameters():
                param.requires_grad = False
        num_feats = self.resnet50.fc.in_features
        self.resnet50.fc = nn.Linear(num_feats, num_classes)
        self.model = new_resnet('resnet50','layer4',Bottleneck, [3, 4, 6, 3],True,True)
        self.model = self.model.to('cuda:0')
    def forward(self, x):
        feat =  self.model(x)
        return self.resnet50(x), feat.view(feat.shape[0],feat.shape[1],-1)


def imvqa(path, tvs):
    im_dict = {}
    from PIL import Image
    trans = transforms.ToTensor()
    for i in tvs:
        if i not in im_dict:
            name = i + ".color.png"
            image = cv2.imread(os.path.join(path , i , name))
            image = cv2.resize(image,(128,128))
            image = trans(image)
            im_dict[i] = image
    return im_dict


class IntResNet(ResNet):
    def __init__(self,output_layer,*args):
        self.output_layer = output_layer
        super().__init__(*args)

        self._layers = []
        for l in list(self._modules.keys()):
            self._layers.append(l)
            if l == output_layer:
                break
        self.layers = OrderedDict(zip(self._layers,[getattr(self,l) for l in self._layers]))

    def _forward_impl(self, x):
        for l in self._layers:
            x = self.layers[l](x)

        return x

    def forward(self, x):
        return self._forward_impl(x)

def new_resnet(
    arch: str,
    outlayer: str,
    block: Type[Union[BasicBlock, Bottleneck]],
    layers: List[int],
    pretrained: bool,
    progress: bool,
    **kwargs: Any
) -> IntResNet:

    model_urls = {
        'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
        'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
        'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
        'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
        'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
        'resnext50_32x4d': 'https://download.pytorch.org/models/resnext50_32x4d-7cdf4587.pth',
        'resnext101_32x8d': 'https://download.pytorch.org/models/resnext101_32x8d-8ba56ff5.pth',
        'wide_resnet50_2': 'https://download.pytorch.org/models/wide_resnet50_2-95faca4d.pth',
        'wide_resnet101_2': 'https://download.pytorch.org/models/wide_resnet101_2-32ee1156.pth',
    }

    model = IntResNet(outlayer, block, layers, **kwargs)
    if pretrained:
        state_dict = load_state_dict_from_url(model_urls[arch],
                                              progress=progress, )
        model.load_state_dict(state_dict)
    return model
