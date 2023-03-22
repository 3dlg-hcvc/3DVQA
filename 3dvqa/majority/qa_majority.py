import json
import csv
import sys 
import os
sys.path.insert(0,'..') 
from model.config import config
args = config()

val_set = []
train_set = [] 
test_set = [] 
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

with open(os.path.join(args.splits,'scannetv1_test.txt'),'r') as f:
    for file in f:
        file = file.replace('\n','') 
        if file.endswith('_00'): 
            test_set.append(file)

path_to_qa_folder = args.qa_path


qa = {}
for file in train_set:
    with open(os.path.join(path_to_qa_folder, str(file) + '.json') , 'r') as js:
        jout = json.load(js) 
        for i in jout:
            if i not in qa: qa[i]={}
            if jout[i]["question_type"] == "location":
                if jout[i]['answer'][0] in qa[i]: qa[i][jout[i]['answer'][0]] += 1
                else: qa[i][jout[i]['answer'][0]] = 1
            else: 
               if jout[i]['answer'] in qa[i]: qa[i][jout[i]['answer']] +=1
               else: qa[i][jout[i]['answer']] = 1 



mca = {}

for i in qa:
    mm = 0
    an = ""
    for j in qa[i]:
        if qa[i][j] > mm:
            mm = qa[i][j]
            an = j
    mca[i] = (an,mm)


#tsv_val = open('majority_qtype_val_result.tsv', 'w')
#tsv_writer = csv.writer(tsv_val, delimiter='\t')


all_q = 0
corrects = 0
for file in val_set:
    with open(os.path.join(path_to_qa_folder, str(file) + '.json') , 'r') as js:
        jout = json.load(js)
        for i in jout:
            all_q += 1
            if jout[i]['question_type'] == "location":
                if i in mca and mca[i][0] in jout[i]['answer']:
                    corrects += 1
            else:
                if i in mca and mca[i][0] == jout[i]['answer']:
                    corrects += 1
            #if i in mca: tsv_writer.writerow([file , i , jout[i]['answer'], mca[i][0]])
            #else: tsv_writer.writerow([file , i , jout[i]['answer'], "N/A"])

print("validation majority accuracy: ", corrects/all_q)
print("total questions in val: ", all_q)





#tsv_test = open('random_majority_qtype_test_result.tsv', 'w')
#tsv_writer_test = csv.writer(tsv_test, delimiter='\t')
all_q = 0 
corrects = 0
for file in test_set:
    with open(os.path.join(path_to_qa_folder, str(file) + '.json') , 'r') as js:
        jout = json.load(js)
        for i in jout: 
            all_q += 1
            if i in mca and jout[i]['question_type'] == "location": 
                if mca[i][0] in jout[i]['answer']: 
                    corrects += 1  
            else: 
                if i in mca and mca[i][0] == jout[i]['answer']:
                    corrects += 1
            
                #if i in mca: tsv_writer_test.writerow([file , i , jout[i]['answer'], mca[i][0]]) 
                #else: tsv_writer.writerow([file , i , jout[i]['answer'], "N/A"])

print("test majority accuracy: ", corrects/all_q) 
print("total questions in val: ", all_q)  



