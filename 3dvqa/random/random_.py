import csv
import random
import json
import os
import sys
sys.path.insert(0,'..')
from model.config import config
random.seed(0)
val_set = []
train_set = []
test_set = []
args = config()
with open(os.path.join(args.splits, 'scannetv1_val.txt'),'r') as f:
    for file in f:
        file = file.replace('\n','')
        if file.endswith('_00'):
            val_set.append(file)

with open(os.path.join(args.splits, 'scannetv1_train.txt'),'r') as f:
    for file in f:
        file = file.replace('\n','')
        if file.endswith('_00'):
            train_set.append(file)

with open(os.path.join(args.splits, 'scannetv1_test.txt'),'r') as f:
    for file in f:
        file = file.replace('\n','')
        if file.endswith('_00'):
            test_set.append(file)

path_to_qa_folder = args.qa_path

all_answers = []
for file in train_set:
    with open(os.path.join(path_to_qa_folder , str(file) + '.json') , 'r') as js:
        jout = json.load(js)
        for i in jout:
            if jout[i]['question_type'] == "location":
                if jout[i]["answer"][0] not in all_answers: all_answers.append(jout[i]["answer"][0])
            else:
                if jout[i]['answer'] not in all_answers:
                    all_answers.append(jout[i]['answer'])

#tsv_val = open('random_val_result.tsv', 'w')
#tsv_writer = csv.writer(tsv_val, delimiter='\t')

all_q = 0
corrects = 0
for file in val_set:
    with open(path_to_qa_folder + str(file) + '.json' , 'r') as js:
        jout = json.load(js)     
        for i in jout:
            all_q += 1
            rand = random.sample(all_answers,1)
            if jout[i]['question_type'] == "location":
                if rand[0] in jout[i]['answer']:
                    corrects += 1
            else:
                if rand[0] == jout[i]['answer']:
                    corrects += 1
            #tsv_writer.writerow([file , i , jout[i]['answer'], rand[0]])
print("validation accuracy: ", corrects/all_q)
print("length of all answers: ", len(all_answers))
print("total questions in val: ", all_q)

#tsv_test = open('random_test_result.tsv', 'w')
#tsv_writer_test = csv.writer(tsv_test, delimiter='\t')



all_q = 0
corrects = 0
for file in test_set:
    with open(os.path.join(path_to_qa_folder , str(file) + '.json') , 'r') as js:
        jout = json.load(js)
        for i in jout:
            all_q += 1
            rand = random.sample(all_answers,1)
            if jout[i]['question_type'] == "location":
                if rand[0] in list(jout[i]['answer']):
                    corrects += 1
            else:
                if rand[0] == jout[i]['answer']:
                    corrects += 1
            #tsv_writer_test.writerow([file , i , jout[i]['answer'], rand[0]])

print("test accuracy: ", corrects/all_q)
print("length of all answers: ", len(all_answers))
print("total questions in test: ", all_q)
