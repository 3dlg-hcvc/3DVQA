from question import questions
import csv
import random
import time
import json
import argparse
from constant import constant
from config import config

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument(
    "--data",
    type=str,
    help="path to json file",
    default="./info/scene_graph_info.json",
)
parser.add_argument(
    "--synonyms",
    type=str,
    help="path to the synonyms json file",
    default="./aliases.json",
)

args = parser.parse_args()
    
def atr_reader(filename):
    unique_obj = []
    unique_atr = []
    atr_for_each_object = {}
    category_repeat = {}
    atr_obj_repeat = {}

    with open("atr" + filename + ".tsv", "r") as ttsvin:
        atr_out = csv.reader(ttsvin, delimiter="\t")
        for i in atr_out:
            if i[1] not in atr_for_each_object:
                atr_for_each_object[i[1]] = []
            if i[12] not in atr_for_each_object[i[1]]:
                atr_for_each_object[i[1]].append(i[12])
            if i[14] not in atr_for_each_object[i[1]] and i[14] != "medium":
                atr_for_each_object[i[1]].append(i[14])
            if i[15] not in atr_for_each_object[i[1]] and i[15] != "medium":
                atr_for_each_object[i[1]].append(i[15])

            if i[1] not in category_repeat:
                category_repeat[i[1]] = 1
            else:
                category_repeat[i[1]] += 1
            if (i[12], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[12], i[1])] = 1
            else:
                atr_obj_repeat[(i[12], i[1])] += 1
            if (i[14], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[14], i[1])] = 1
            else:
                atr_obj_repeat[(i[14], i[1])] += 1
            if (i[15], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[15], i[1])] = 1
            else:
                atr_obj_repeat[(i[15], i[1])] += 1
            if (i[14], i[12], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[14], i[12], i[1])] = 1
            else:
                atr_obj_repeat[(i[14], i[12], i[1])] += 1
            if (i[15], i[12], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[15], i[12], i[1])] = 1
            else:
                atr_obj_repeat[(i[15], i[12], i[1])] += 1
            if (i[15], i[14], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[15], i[14], i[1])] = 1
            else:
                atr_obj_repeat[(i[15], i[14], i[1])] += 1
            if (i[15], i[14], i[12], i[1]) not in atr_obj_repeat:
                atr_obj_repeat[(i[15], i[14], i[12], i[1])] = 1
            else:
                atr_obj_repeat[(i[15], i[14], i[12], i[1])] += 1
            if (
                i[1] not in unique_obj
                and i[1] != "0"
                and i[1] != "floor"
                and i[1] != "ceiling"
                and i[1] != "object"
            ):
                unique_obj.append(i[1])
            if i[12] not in unique_atr:
                unique_atr.append(i[12])
            if i[14] not in unique_atr and i[14] != "medium":
                unique_atr.append(i[14])
            if i[15] not in unique_atr and i[15] != "medium":
                unique_atr.append(i[15])
    return unique_obj, unique_atr, category_repeat, atr_obj_repeat, atr_for_each_object


def initialization():
    args = config()
    relation_than = constant.relation_than
    relation_with_the = constant.relation_with_the
    relation_which_is = constant.relation_which_is
    atr = constant.atr
    color = constant.color
    with open(args.data) as f:
        data = json.load(f)
        category_list = data["category_list"]
        category_list_name = [category_list[i] for i in category_list]

    with open(args.synonyms, 'r') as f:
        data = json.load(f)
    syns = []
    for i in data:
        if i not in syns:
            syns.append(i)
        for j in data[i]:
            if j not in syns:
                syns.append(j)
    syns_unq = []
    for i in syns:
        if i not in category_list_name:
            syns_unq.append(i)

    syns_spc = constant.syns_spc 

    specials = constant.specials
    plural = {}
    for i in category_list_name:
        if i in specials:
            plural[i] = specials[i]
        else:
            plural[i] = i + "s"
    for i in syns_unq:
        if i in syns_spc:
            plural[i] = syns_spc[i]
        else:
            plural[i] = i + "s"
    return (
        relation_than,
        relation_with_the,
        relation_which_is,
        atr,
        color,
        category_list_name,
        plural,
        atr,
    )


def qa_connect(obbs, file, synonyms, filename):
    (
        relation_than,
        relation_with_the,
        relation_which_is,
        atr,
        color,
        category_list_name,
        plural,
        atr,
    ) = initialization()
    (
        unique_obj,
        unique_atr,
        repeat_obj,
        repeat_atr_obj,
        atr_for_each_object,
    ) = atr_reader(filename)
    rnd_obj = random.choices(category_list_name, k=len(unique_obj) // 5)
    rnd_atr = random.choices(atr, k=1)
    object2 = [None] + list(unique_obj)
    object1 = list(unique_obj)
    attribute1 = [None] + list(unique_atr)
    atr_for_each_object_add_rnd = dict(atr_for_each_object)
    
    for j in rnd_obj:
        if j not in object1 and j != "0" and j != "ceiling" and j != "floor":
            object1.append(j)
            atr_for_each_object_add_rnd[j] = random.choices(atr, k=1)
            
    temp = random.choices(object1, k=len(object1) // 10)
    for j in temp:
        at = random.choices(atr, k=1)[0]
        if at not in atr_for_each_object_add_rnd[j]:
            atr_for_each_object_add_rnd[j].append(at)

    if rnd_atr not in attribute1:
        attribute1.append(rnd_atr[0])
    
    Q = {}
    for obj1 in object1:
        for atr1 in atr_for_each_object_add_rnd[obj1] + [None]:
            for obj2 in object2:
                if obj2 != None:
                    for atr2 in atr_for_each_object[obj2] + [None]:

                        qclass = questions(
                            Q,
                            obj1,
                            atr1,
                            obj2,
                            atr2,
                            repeat_obj,
                            repeat_atr_obj,
                            plural,
                            file,
                            filename,
                            obbs,
                            synonyms,
                        )
                        Q = qclass.generate()
                else:
                    qclass = questions(
                        Q,
                        obj1,
                        atr1,
                        obj2,
                        None,
                        repeat_obj,
                        repeat_atr_obj,
                        plural,
                        file,
                        filename,
                        obbs,
                        synonyms,
                    )
                    Q = qclass.generate()
    return Q
