import json
import csv
import os
import sys
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

with open(os.path.join(args.splits, 'scannetv1_test.txt'),'r') as f:
    for file in f:
        file = file.replace('\n','') 
        if file.endswith('_00'): 
            test_set.append(file)

path_to_qa_folder = args.qa_path

af={"location":{},"yes/no":{},"query_attribute":{}, "counting":{}}

for file in train_set:
    with open(path_to_qa_folder + str(file) + '.json' , 'r') as js:
        jout = json.load(js) 
        for i in jout:
            if jout[i]["question_type"] == "location":
                    if jout[i]['answer'][0] in af["location"]: af["location"][jout[i]['answer'][0]] += 1
                    else: af["location"][jout[i]['answer'][0]] = 1
            else: 
               if jout[i]['answer'] in af[jout[i]["question_type"]]: af[jout[i]["question_type"]][jout[i]['answer']] +=1
               else: af[jout[i]["question_type"]][jout[i]['answer']] = 1 


mca = {"location":("",0), "yes/no":("",0), "query_attribute":("",0), "counting":("",0)}

for i in af:
    mm = 0
    an = ""
    for j in af[i]:
        if af[i][j] > mm:
            mm = af[i][j]
            an = j
    mca[i] = (an,mm)


#tsv_val = open('majority_qtype_val_result.tsv', 'w')
#tsv_writer = csv.writer(tsv_val, delimiter='\t')

all_q = 0
corrects = 0
for file in val_set:
    with open(path_to_qa_folder + str(file) + '.json' , 'r') as js:
        jout = json.load(js)
        for i in jout:
            all_q += 1
            if jout[i]['question_type'] == "location":
                if mca["location"][0] in jout[i]['answer']:
                    corrects += 1
            else:
                if mca[jout[i]['question_type']][0] == jout[i]['answer']:
                    corrects += 1
            #tsv_writer.writerow([file , i , jout[i]['answer'], mca[jout[i]['question_type']][0]])

print(mca)
print("validation majority qtype accuracy: ", corrects/all_q)
print("total questions in val: ", all_q)





#tsv_test = open('random_majority_qtype_test_result.tsv', 'w')
#tsv_writer_test = csv.writer(tsv_test, delimiter='\t')

all_q = 0 
corrects = 0
for file in test_set:
    with open(os.path.join(path_to_qa_folder, str(file) + '.json'), 'r') as js:
        jout = json.load(js)
        for i in jout: 
            all_q += 1
            if jout[i]['question_type'] == "location": 
                if mca["location"][0] in jout[i]['answer']: 
                    corrects += 1  
                    
            else: 
                if mca[jout[i]['question_type']][0] == jout[i]['answer']:
                    corrects += 1
            
            #tsv_writer_test.writerow([file , i , jout[i]['answer'], mca[jout[i]['question_type']][0]]) 

print("test majority qtype accuracy: ", corrects/all_q) 
print("total questions in val: ", all_q)  





mm = 0
for i in mca:
    if mca[i][1] > mm:
        mm = mca[i][1]
        j = mca[i][0]
print(j)

#tsv_val = open('majority_val_result.tsv', 'w')
#tsv_writer = csv.writer(tsv_val, delimiter='\t')


all_q = 0
corrects = 0
for file in val_set:
    with open(path_to_qa_folder + str(file) + '.json' , 'r') as js:
        jout = json.load(js)
        for i in jout:
            all_q += 1
            if str(jout[i]["answer"]) == str(j):
                corrects += 1

            #tsv_writer.writerow([file , i , jout[i]['answer'], j])
print("validation majority _ answer to all val questions is the most common answer in all the questions of train:", corrects/all_q)




#tsv_test = open('random_majority_test_result.tsv', 'w')
#tsv_writer_test = csv.writer(tsv_test, delimiter='\t')


all_q = 0
corrects = 0
for file in test_set:
    with open(os.path.join(path_to_qa_folder + str(file) + '.json'), 'r') as js:
        jout = json.load(js)
        for i in jout:
            all_q += 1
            if str(jout[i]["answer"]) == str(j):
                corrects += 1
            #tsv_writer_test.writerow([file , i , jout[i]['answer'], j])
print("test majority _ answer to all val questions is the most common answer in all the questions of train:", corrects/all_q)
