from utils import load_question
import json
import os

def accuracy(args, where_dict, question, answer, prediction, sceneID):
    acc = 0
    for i in range(len(prediction)):
        if answer[i] == prediction[i]:
            acc += 1
        elif sceneID[i] in where_dict:
            if question[i] in where_dict[sceneID[i]]:
                if prediction[i] in where_dict[sceneID[i]][question[i]]:
                    acc += 1
    return acc / len(prediction)


def where_acc_corrector(args, allscene):
    repeat_dic = {}
    for i in allscene:
        repeat_dic[i] = {}
        with open(os.path.join(args.qa_path , str(i) + ".json"), "r") as f:
            data = json.load(f)
            for j in data:
                if data[j]["question_type"] == "location":
                    repeat_dic[i][j] = data[j]["answer"]
    return repeat_dic
