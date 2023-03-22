import csv
import random
from answer import answers
from programs import functional_program 
from constant import constant
class questions:
    def __init__(self, Q, obj1, atr1, obj2, atr2, repeat_obj, repeat_atrobj, plural, file, filename, obbs, synonyms):
        obb = {}
        for i in obbs["segGroups"]:
            obb[str(i["objectId"]+1)] = i["obb"] 
        self.obb = obb
        self.obj1 = obj1
        self.synonyms = synonyms
        self.atr1 = atr1
        self.a1 = atr1
        self.a2 = atr2
        self.obj2 = obj2
        self.atr2 = atr2
        self.repeat_obj = repeat_obj
        self.repeat_atrobj = repeat_atrobj
        self.Q = Q
        self.plural = plural
        self.file = file
        self.filename = filename
        self.object1 = obj1
        self.object2 = obj2
    def generate(self):  
        relation_than = constant.relation_than
        relation_with_the = constant.relation_with_the
        relation_which_is = constant.relation_which_is
        question = {"answer":"","answer_OBB":None,"question_type":"", "sub_question_type":None, "object1": self.obj1 , "attribute1":self.atr1, "relation": None, "object2":self.obj2 , "attribute2":self.atr2, "program":"", "extra_information":[]}
        if self.atr1 != None: self.atr1 = self.atr1 + " "
        if self.atr2 != None: self.atr2 = self.atr2 + " "
        if self.atr1 == None: self.atr1 =""
        if self.atr2 == None: self.atr2 =""
        if self.obj2 == None:
            ### counting 
            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1
            question["question_type"] = "counting"
            question["relation"] = None 
            f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
            question["program"] = f_p.__call__()
            ans = answers("counting",self.object1, self.a1, self.object2, self.a2, None,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
            question["answer"] = ans[0]
            ans_obb = []
            #for ii in ans[1]:
            #    ans_obb.append(self.obb[ii])
            question["answer_OBB"] = ans[1]
            
            if str(question["answer"])[0:5] != "error":  self.Q[random.choice(["how many "+ self.atr1 + self.plural[self.obj1] +" are there ?" , "what is the number of "+ self.atr1 + self.plural[self.obj1] +" ?"])] = dict(question)
            ### existence/yesno

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1
            question["question_type"] = "yes/no"
            question["sub_question_type"] = "existence"

            f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
            question["program"] = f_p.__call__()
            
            ans = answers("existence",self.object1, self.a1, self.object2, self.a2, None,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
            question["answer"] = ans[0]
            ans_obb = [] 
            #for ii in ans[1]:
            #    ans_obb.append(self.obb[ii])
            question["answer_OBB"] = ans[1]
            
 
            if question["answer"][0:5] != "error": self.Q["is there any "+self.atr1 + self.obj1 +" ?"] = dict(question)
            question["sub_question_type"] = None
            ### location

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1
            question["question_type"] = "location"
 
            f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
            question["program"] = f_p.__call__()
                       #### double check if that's the list of all possible answers
            ans = answers("location", self.object1, self.a1, self.object2, self.a2, None,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)

            question["answer"] = ans[0]
            ans_obb = []
            #for ii in ans[1]:
            #    ans_obb.append(self.obb[ii])
            question["answer_OBB"] = ans[1]
            if self.object1 in self.repeat_obj and self.repeat_obj[self.object1] == 1: question["extra_information"] = [self.atr1]
            if question["answer"][0:5] != "error": self.Q[random.choice(["where is the " + self.atr1 + self.obj1+ random.choice([""," located"," placed"])+" ?", "what is the location of the "+self.atr1 + self.obj1+" ?"])] = dict(question) 
            ### query_atr

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1
            question["question_type"] = "query_attribute"

            for i in ["color","height","size"]:
                if self.a1 == None or (self.a1 in ["short", "tall"] and i != "height") or (self.a1 in ["large","small"] and i != "size") or (self.a1 not in ["short", "tall","large","small","light","dark",None] and i!= "color"): 
                    ### answers doesn't work that way:
                   
                    ans = answers("query_"+i, self.object1, self.a1, self.object2, self.a2, None,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                   
                    question["answer"] = ans[0]
                    ans_obb = []
                    #for ii in ans[1]:
                    #    ans_obb.append(self.obb[ii])
                    question["answer_OBB"] = ans[1]
 
                    f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,i)
                    question["program"] = f_p.__call__()
                    if question["answer"][0:5] != "error": self.Q["what is the "+ i + " of the " + self.atr1 + self.obj1 +" ?"] = dict(question)
            
        else: 
            ### compare_integer/yesno

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2

            question["question_type"] = "yes/no"
            question["extra_information"] = []
            question["sub_question_type"] = "compare_integer"
            comp = random.choice(["more ", "larger number of ", "fewer ", "less ","equal number of ", "same number of "])

            f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
            question["program"] = f_p.__call__()
            
            full_ans  = answers("compare_integer",self.object1, self.a1, self.object2, self.a2, None,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
            #ans_obb1 = []
            
            #for ii in full_ans[1]:
            #    ans_obb1.append(self.obb[ii])
            #ans_obb2 = []
            #for ii in full_ans[2]:
            #    ans_obb2.append(self.obb[ii])
            question["answer_OBB"] = [full_ans[1], full_ans[2]]

            ans = full_ans[0] 
            if comp in ["fewer ", "less "]: 
                if ans == "less" : question["answer"] = "yes"
                elif ans=="more" or ans=="equal": question["answer"]  = "no"
                else: question["answer"] = ans
                if question["answer"][0:5] != "error": self.Q ["are there " + comp + self.atr1 + self.plural[self.obj1] +" than the "+ self.atr2  + self.plural[self.obj2] + " ? "] = dict(question)
            if comp in ["more ", "larger number of "]:
                if ans == "more" : question["answer"] = "yes"
                elif ans == "less" or ans=="equal": question["answer"] = "no"
                else: question["answer"] = ans 
                if question["answer"][0:5] != "error": self.Q ["are there " + comp + self.atr1 + self.plural[self.obj1] +" than the "+ self.atr2  + self.plural[self.obj2] + " ? "] = dict(question)
            if comp in ["equal number of ", "same number of "]:
                if ans == "equal" : question["answer"] = "yes"
                elif ans == "less" or ans=="more": question["answer"] = "no"  
                else: question["answer"] = ans     
                if question["answer"][0:5] != "error": self.Q ["are there " + comp + self.atr1 + self.plural[self.obj1] +" and "+ self.atr2  + self.plural[self.obj2] + " ? "] = dict(question)
            ### compare_atr/yesno

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2

            question["sub_question_type"] = "check_relation"

            if self.object1 in self.repeat_obj and self.repeat_obj[self.object1] == 1: question["extra_information"] = [self.atr1]
            
            if self.object2 in self.repeat_obj and self.repeat_obj[self.object2] == 1: question["extra_information"] = [self.atr2]
            for i  in relation_than :
                question["relation"] = i

                f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("compare_attribute",self.object1, self.a1, self.object2, self.a2,i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                #ans_obb = []
                #for ii in ans[1] + ans[2]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = [ans[1],ans[2]]

                if question["answer"][0:5] != "error": self.Q["is the " + self.atr1 + self.obj1 + " " + i + " than the "+ self.atr2 + self.obj2 + " ? "] = dict(question)
            for i in relation_with_the:
                if i != "same color" or (self.a1 in ["short", "tall","large","small",None] and self.a2 in ["short", "tall","large","small",None]):
                    if i!= "same category" or (self.obj1 == "thing"): 
                        question["relation"] = i

                        f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                        question["program"] = f_p.__call__()
                        ans = answers("compare_attribute",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1] + ans[2]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = [ans[1] + ans[2]]
                        if question["answer"][0:5] != "error": self.Q["does the "+ self.atr1 + self.object1 + " has the " + i + " as the "+ self.atr2 + self.object2 + " ? "] = dict(question)
            for i in relation_which_is:
                question["relation"] = i

                f_p = functional_program("existence", self.a1, self.object1, question["relation"], self.a2, self.object2,None)
                question["program"] = f_p.__call__()
                ans = answers("compare_attribute",self.object1, self.a1, self.object2, self.a2, i ,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                ans_obb = []
                #for ii in ans[1] + ans[2]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = [ans[1] + ans[2]]
                #question['sub_question_type'] = 'existence'
                if question["answer"][0:5] != "error" and (self.obj1!='wall' or i=='next to') and (self.obj2!='wall' or i=='next to' or i=='on') and ((self.obj2!='door' and self.obj1!='door') or i=='next to'): self.Q["is the "+ self.atr1 + self.obj1 + " " + i + " the " +  self.atr2 + self.obj2 + " ?"] = dict(question)
            ### existence/yesno

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2
            question["sub_question_type"] = "existence"

            if self.object2 in self.repeat_obj and self.repeat_obj[self.object2] == 1: question["extra_information"] = [self.atr2]
            for i in relation_than :
                question["relation"] = i

                f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("existence",self.object1, self.a1, self.object2, self.a2, i, self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0] 
                #ans_obb = []
                #for ii in ans[1]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = ans[1]
                if question["answer"][0:5] != "error": self.Q["is there any "+ self.atr1 + self.obj1 + " which is " + i +  " than the " + self.atr2 + self.obj2 + " ? "] = dict(question)
            for i in relation_with_the:
                if i != "same color" or (self.a1 in ["short", "tall","large","small",None] and self.a2 in ["short", "tall","large","small",None]):
                    if i!= "same category" or (self.obj1 == "thing"): 
                        question["relation"] = i

                        f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                        question["program"] = f_p.__call__()
                        ans = answers("existence",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = ans[1]
                        if question["answer"][0:5] != "error": self.Q["is there any "+ self.atr1 + self.obj1 + " with the " + i + " as the "+self.atr2 +self.obj2 + " ? "] = dict(question)
            for i in relation_which_is:
                question["relation"] = i

                f_p = functional_program(question["sub_question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("existence",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                #ans_obb = []
                #for ii in ans[1]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = ans[1]
                if question["answer"][0:5] != "error" and (i=='next to' or (self.obj1!='door' and self.obj2!='door' and self.obj1!='floor' and self.obj2!='floor' and self.obj1!='wall' and self.obj2!='wall' ) or (i=='on' and self.obj2!='wall' )): self.Q["is there any "+ self.atr1 + self.obj1 +" "+ i + " the " +  self.atr2 + self.obj2 + " ?"] = dict(question)
            ### counting

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2

            question["sub_question_type"] = None
            question["question_type"] = "counting"
            for i  in relation_than : 
                question["relation"] = i

                f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("counting",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                #ans_obb = []
                #for ii in ans[1]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = ans[1]
                if str(question["answer"])[0:5] != "error": self.Q[random.choice(["how many "+ self.atr1 + self.plural[self.obj1] +" are there which are "+i+" than the "+ self.atr2 + self.obj2 +" ?" , "what is the number of "+ self.atr1 + self.plural[self.obj1] +" which are " + i + " than the "+self.atr2 + self.obj2  +" ?"])] = dict(question)
            for i in relation_with_the:
                if i != "same color" or (self.a1 in ["short", "tall","large","small",None] and self.a2 in ["short", "tall","large","small",None]):
                    if i!= "same category" or (self.obj1 == "thing"): 
                        question["relation"] = i

                        f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                        question["program"] = f_p.__call__()
                        ans = answers("counting",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = ans[1]
                        if str(question["answer"])[0:5] != "error": self.Q[random.choice(["how many "+ self.atr1 + self.plural[self.obj1] +" are there with the "+i+" as the "+ self.atr2 + self.obj2 +" ?" , "what is the number of "+ self.atr1 + self.plural[self.obj1] +" with the " + i + " as the "+self.atr2 + self.obj2  +" ?"])] = dict(question)
            for i in relation_which_is:
                question["relation"] = i

                f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("counting",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                #ans_obb = []
                #for ii in ans[1]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = ans[1]
                if str(question["answer"])[0:5] != "error" and (i=='next to' or (self.obj1!='door' and self.obj2!='door' and self.obj1!='floor' and self.obj2!='floor' and self.obj1!='wall' and self.obj2!='wall' ) or (i=='on' and self.obj2!='wall' )): self.Q[random.choice(["how many "+ self.atr1 + self.plural[self.obj1] +" are there which are "+i+" the "+ self.atr2 + self.obj2 +" ?" , "what is the number of "+ self.atr1 + self.plural[self.obj1] +" which are " + i + " the "+self.atr2 + self.obj2  +" ?"])] = dict(question)
            ### where

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2

            question["question_type"] = "location"
            question["extra_information"] = []
            if self.object1 in self.repeat_obj and self.repeat_obj[self.object1] == 1: question["extra_information"] = [self.a1]
            flag = False
            if self.object1 in self.synonyms:
                for sn in self.synonyms[self.object1]:
                    if "where is the " + self.atr1 + sn + " ?" in self.Q : 
                        flag = True
                        break
            elif "where is the " + self.atr1 + self.obj1 + " ?" in self.Q: flag=True 
            if flag: question["extra_information"] + [self.obj2, self.a2]
            elif self.repeat_obj[self.object2] == 1: question["extra_information"].append(self.a2)
            for i  in relation_than :
                question["relation"] = i

                f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                question["program"] = f_p.__call__()
                ans = answers("location",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                question["answer"] = ans[0]
                #ans_obb = []
                #for ii in ans[1]:
                #    ans_obb.append(self.obb[ii])
                question["answer_OBB"] = ans[1]
                if question["answer"][0:5] != "error": self.Q[random.choice(["where is the " + self.atr1 + self.obj1 + " which is " + i +" than the "+  self.atr2 + self.obj2 +random.choice([""," placed"," located"])+ " ?", "what is the location of the "+ self.atr1 + self.obj1 +" which is " + i +" than the "+  self.atr2 + self.obj2 + " ?"])] = dict(question)
            for i in relation_with_the:
                if i != "same color" or (self.a1 in ["short", "tall","large","small",None] and self.a2 in ["short", "tall","large","small",None]):
                    if i!= "same category" or (self.obj1 == "thing"): 
                        question["relation"] = i

                        f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,None)
                        question["program"] = f_p.__call__()
                        ans = answers("location",self.object1, self.a1, self.object2, self.a2, i,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = ans[1]
                        if question["answer"][0:5] != "error": self.Q[random.choice(["where is the " + self.atr1 + self.obj1 +  " with the " + i + " as the " + self.atr2 +self.obj2 +random.choice([""," placed"," located"])+ " ?","waht is the location of the "+ self.atr1 + self.obj1 +  " with the " + i + " as the " + self.atr2 +self.obj2+ " ?"])] = dict(question)
            
            ### query_attribute

            if self.object1 in self.synonyms:
                self.obj1 = random.choice(self.synonyms[self.object1])
                question["object1"] = self.obj1

            if self.object2 in self.synonyms:
                self.obj2 = random.choice(self.synonyms[self.object2])
                question["object2"] = self.obj2

            question["question_type"] = "query_attribute"
            question["extra_information"] = []
            for i in ["color","height","size"]:
                if self.object1 in self.repeat_obj and self.repeat_obj[self.object1] == 1: question["extra_information"] = [self.a1]
                if self.a1 == None or (self.a1 not in ["short", "tall"] and i == "height") or (self.a1 not in ["large","small"] and i == "size") or (self.a1 in ["short", "tall","large","small",None] and i== "color"):

                    flag = False
                    if self.object1 in self.synonyms:
                        for sn in self.synonyms[self.object1]:
                            if "what is the "+ i + " of the "+ self.atr1 + sn + " ?" in self.Q: 
                                flag = True
                                break
                    elif "what is the "+ i + " of the "+ self.atr1 + self.object1 + " ?" in self.Q: flag = True

                    if flag: question["extra_information"] + [self.obj2, self.atr2]
                    elif self.object2 in self.repeat_obj and self.repeat_obj[self.object2] == 1: question["extra_information"].append(self.a2)
                    for j  in relation_than :
                        question["relation"] = j

                        f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,i)
                        question["program"] = f_p.__call__()
                       
                        ans  = answers("query_"+i, self.object1, self.a1, self.object2, self.a2, j,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = ans[1]
                        if question["answer"][0:5] != "error": self.Q["what is the "+i+" of the " + self.atr1 + self.obj1 + " which is " + j +" than the "+  self.atr2 + self.obj2 + " ? "] = dict(question)
                    for j in relation_with_the:
                        if j != "same color" or (self.a1 in ["short", "tall","large","small",None] and self.a2 in ["short", "tall","large","small",None]):
                            if j!= "same category" or (self.obj1 == "thing"): 
                                question["relation"] = j

                                f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,i)
                                question["program"] = f_p.__call__()
                                ans = answers("query_"+i, self.object1, self.a1, self.object2, self.a2, j,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                                question["answer"] = ans[0]
                                #ans_obb = []
                                #for ii in ans[1]:
                                #    ans_obb.append(self.obb[ii])
                                question["answer_OBB"] = ans[1]
                                if question["answer"][0:5] != "error": self.Q["what is the "+i +" of the " + self.atr1 + self.obj1 +  " with the " + j + " as the " + self.atr2 +self.obj2 + " ?"] = dict(question)
                    for j in relation_which_is:
                        question["relation"] = j

                        f_p = functional_program(question["question_type"], self.a1, self.obj1, question["relation"], self.a2, self.obj2,i)
                        question["program"] = f_p.__call__()
                        ans = answers("query_"+i, self.object1, self.a1, self.object2, self.a2, j,self.repeat_obj,self.repeat_atrobj,self.file,self.filename,self.synonyms,self.plural)
                        question["answer"] = ans[0]
                        #ans_obb = []
                        #for ii in ans[1]:
                        #    ans_obb.append(self.obb[ii])
                        question["answer_OBB"] = ans[1]
                        if question["answer"][0:5] != "error" and (i=='next to' or (self.obj1!='door' and self.obj2!='door' and self.obj1!='floor' and self.obj2!='floor' and self.obj1!='wall' and self.obj2!='wall' ) or (i=='on' and self.obj2!='wall' )): self.Q["what is the "+ i +" of the " + self.atr1 + self.obj1 + " which is " + j + " the "+ self.atr2 +self.obj2 + " ?"] = dict(question)
       
        return self.Q                  

 
