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
from utils import embedding, train_val_lists, load_question
from metric import accuracy, where_acc_corrector
torch.manual_seed(0)
random.seed(0)

def get_plys(path,li):
    files = os.listdir(path)
    init = True
    themax = 0
    ply_dict = {}
    for file in li:
        if file.endswith('_00') and os.path.exists(os.path.join(path , file , file+'_vh_clean_2.ply')):
            with open(os.path.join(path , file , file+'_vh_clean_2.ply'),'rb') as f:
                plydata = PlyData.read(f)
                print(file)
                xyz_color = np.asarray([[plydata['vertex']['x'],plydata['vertex']['y'],plydata['vertex']['z'],plydata['vertex']['red'], plydata['vertex']['green'], plydata['vertex']['blue']]], dtype=np.float32)
                xyz_color = np.transpose(xyz_color)
            ply_dict[file] = torch.from_numpy(xyz_color)
            if xyz_color.shape[0] > themax :
                themax = xyz_color.shape[0]
    return ply_dict , themax

if __name__ == "__main__":

    args = config()

    embeddings_dict = embedding(args.glove)
    train, val, test = train_val_lists(args)
    test = test[0:3]
    train = train[0:3]
    val = val[0:3]
    ModelID1_val, Correct_Answers_val, QuestionList_val = load_question(args.qa_path, val)
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



    Correct_Answer_length = len(complete_list)
    BS = 64

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    vqa_model = vqamodel(Correct_Answer_length, args.embedding_dim, args.hidden_dim, method = "pointnet")
    vqa_model = vqa_model.to(device)

    loss_function = nn.CrossEntropyLoss().cuda()
    vqa_optimizer = optim.Adam(vqa_model.parameters(), args.lr)
    scheduler = torch.optim.lr_scheduler.StepLR(vqa_optimizer, args.step_size, args.gamma)


    lenMID1 = len(ModelID1)
    lenMID1_val = len(ModelID1_val)
    lenMID1_test = len(ModelID1_test)

    kwargs = {'num_workers': 0} if torch.cuda.is_available() else {}

    train_loader = torch.utils.data.DataLoader(
                   MyDataLoader(max_len, complete_list, ModelID1, QuestionList, Correct_Answers, embeddings_dict),
                   batch_size= BS, shuffle=True, **kwargs
                   )


    val_loader = torch.utils.data.DataLoader(
                 MyDataLoader(max_len, complete_list, ModelID1_val, QuestionList_val, Correct_Answers_val , embeddings_dict),
                 batch_size= BS, shuffle=False, **kwargs
                 )

    test_loader = torch.utils.data.DataLoader(
                  MyDataLoader(max_len, complete_list, ModelID1_test, QuestionList_test, Correct_Answers_test , embeddings_dict),
                  batch_size= BS, shuffle=False, **kwargs
                  )


    start = timeit.default_timer()
    acc_val = 0
    acc_mem = 0
    for epoch in range(args.epochs):
        steps_train = 0
        steps_test = 0
        steps_val = 0
        loss_val = 0
        Epoch_acc = 0
        Epoch_acc_val = 0
        print(epoch+1,"/", args.epochs)

        for batch_idx, (question, answer, x_train1, x_train2, inx, scene_ID) in enumerate(train_loader):
            vqa_model.train()
            vqa_model.zero_grad()
            vqa_optimizer.zero_grad()
            steps_train += 1
            tag_score = vqa_model(x_train1, x_train2)
            loss = loss_function(tag_score, inx.long())
            predictions = tuple([complete_list[x] for x in torch.argmax(tag_score,1)])
            acc = accuracy(args, where_dict, question, answer, predictions, scene_ID)

            if float((BS*steps_train)/lenMID1)*100 > 100:
                percent = 100
            else:
                percent = float((BS*steps_train)/lenMID1)*100

            print("train:", int(percent), "%   ", "epoch: ", epoch, "accuracy: ", acc, "loss: ", loss)
            Epoch_acc = Epoch_acc + acc*len(question)
            loss.backward()
            vqa_optimizer.step()

        scheduler.step()


        if args.do_val:
            acc_val_last_epoch = acc_mem
            vqa_model.eval()
            with torch.no_grad():
                for batch_idx_val, (question, answer, x_val1, x_val2, inx_val, scene_ID) in enumerate(val_loader):
                    steps_val += 1
                    tag_score_val = vqa_model(x_val1, x_val2)

                    loss_val = loss_function(tag_score_val, inx_val.long().cuda())
                    tag_score_val_f = tag_score_val

                    predictions = tuple([complete_list[x] for x in torch.argmax(tag_score_val,1)])
                    acc_val = accuracy(args, where_dict, question, answer, predictions, scene_ID)
                    if float((BS*steps_val)/lenMID1_val)*100 > 100:
                        percent = 100
                    else:
                        percent = float((BS*steps_val)/lenMID1_val)*100
                    print("val:",int(percent),"%    ","epoch: ", epoch, "accuracy: ", acc_val,"loss: ",loss_val)


                    Epoch_acc_val = Epoch_acc_val + acc_val*len(question)
            vqa_model.train()



        acc_mem = Epoch_acc_val/lenMID1_val
        print("Train Accuracy: ", Epoch_acc,"/",lenMID1," = ", Epoch_acc/lenMID1 )

        print("Validation Accuracy: ", Epoch_acc_val,"/",lenMID1_val," = ", Epoch_acc_val/lenMID1_val )

        torch.save({
    			'epoch': epoch,
    			'model_state_dict': vqa_model.state_dict(),
    			'optimizer_state_dict': vqa_optimizer.state_dict(),
    			'loss': loss,
                'tag_score': tag_score
    			}, args.checkpoint_path)

        if Epoch_acc_val/lenMID1_val - acc_val_last_epoch < 0.0001 and epoch > 9 :
            break
    steps_test = 0
    if args.do_test:
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
                print("test:",int(percent),"%    ","epoch: ", epoch, "accuracy: ", acc_test)
                Epoch_acc_test = Epoch_acc_test + acc_test*len(question)

        print("test Accuracy: ", Epoch_acc_test,"/",lenMID1_test," = ", Epoch_acc_test/lenMID1_test )


    stop = timeit.default_timer()
    print("time: ", stop-start)
