import torch
import torch.nn as nn
import torch.optim as optim
torch.manual_seed(1)
import os
import sys
import importlib
from config import config
sys.path.insert(1,"/home/yetesam/Desktop/Pointnet2.ScanNet")
import torch.utils.data
import timeit
import random
from dataloader import MyDataLoader
from combineLanguageVision import vqamodel
from utils import embedding, train_val_lists, load_question, imvqa
from metric import accuracy, where_acc_corrector
torch.manual_seed(0)
random.seed(0)

if __name__ == "__main__":
    args = config()
    embeddings_dict = embedding(args.glove)
    train, val, test = train_val_lists(args)
    ModelID1_test, Correct_Answers_test, QuestionList_test = load_question(args.qa_path, test)
    ModelID1, Correct_Answers, QuestionList = load_question(args.qa_path, train)
    where_dict = where_acc_corrector(args, train+val+test)

    # get the number of words in the longest question
    max_len = 0
    for i in QuestionList:
        if len(i.split()) > max_len:
            max_len = len(i.split())

    # list of all possible answers (answers in the train set)
    complete_list = []
    for an in Correct_Answers:
        if str(an) not in complete_list:
            if str(an) !="" and str(an) != " ":
                complete_list.append(str(an))
    complete_list.append("")

    im_dict = {}
    Correct_Answer_length = len(complete_list)
    method = args.method
    
    # do to memory constraints we use bs=128 for 2dvqa
    if method == "2dvqa" or method == "2dvqa_only":
        im_dict = imvqa(args.im_path, train+val+test)
        BS = 128

    elif method == "pointnet" or method == "pointnet_only": 
        BS = 1024*4

    else:
        BS = 256
        

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vqa_model = vqamodel(Correct_Answer_length, args.embedding_dim, args.hidden_dim, method)
    vqa_model = vqa_model.to(device)
    checkpoint = torch.load(args.checkpoint_path , map_location=torch.device('cpu') )
    vqa_model.load_state_dict(checkpoint["model_state_dict"])
    vqa_model.eval() 
    lenMID1_test = len(ModelID1_test)


    kwargs = {'num_workers': 0} if torch.cuda.is_available() else {}

    test_loader = torch.utils.data.DataLoader(
                  MyDataLoader(
                  im_dict, max_len, complete_list, ModelID1_test, QuestionList_test, Correct_Answers_test , embeddings_dict, method, mode='test'
                  ),
                  batch_size=BS, shuffle=False, **kwargs
                  )

    start = timeit.default_timer()
    steps_test = 0
    if True:
        Epoch_acc_test = 0
        vqa_model.eval()
        with torch.no_grad():
            for batch_idx_test, (question, answer, x_test1, x_test2, inx_test, scene_ID) in enumerate(test_loader):
                steps_test += 1
                tag_score_test = vqa_model(x_test1, x_test2)
                predictions = tuple([complete_list[x] for x in torch.argmax(tag_score_test,1)])
                acc_test = accuracy(args, where_dict, question, answer, predictions, scene_ID)
                if float((BS*steps_test)/lenMID1_test)*100 > 100:
                    percent = 100
                else:
                    percent = float((BS*steps_test)/lenMID1_test)*100
                print("test:",int(percent),"%    ", "accuracy: ", acc_test)
                Epoch_acc_test = Epoch_acc_test + acc_test*len(question)

        print("test Accuracy: ", Epoch_acc_test,"/",lenMID1_test," = ", Epoch_acc_test/lenMID1_test )




    stop = timeit.default_timer()
    print("time: ", stop-start)
