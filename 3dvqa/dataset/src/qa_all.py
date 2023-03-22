import json
import csv
import argparse
import random
import os
import time
from scene_graph_clean import scene_graph
from question_generator_clean import qa_connect
from shutil import copyfile
import numpy as np

random.seed(10)
np.random.seed(42)

def json_reader(arg):
    with open(arg) as f:
        data = json.load(f)
    return data


def qa_write(
    file, arg, QA, the_zero, the_one, no, yes_count, medium, no_med_count, QA_int_comp
):
    outfile = open(arg.qa + str(file) + ".tsv", "wt")
    tsv_writer = csv.writer(outfile, delimiter="\t")

    correction = {
        "doorframes": "door frames",
        "door frame": "door frame",
        "loofa": "lofa",
        "loofas": "lofa",
        "dustpans": "dustpan",
        "swiffers": "swiffer",
        "tupperwares": "tupperware",
        "sanitzer": "sanitizer",
        "sanitzers": "sanitizers",
        "quadcopters": "quadcopter",
        "roombas": "roomba",
        "coatrack": "coat rack",
        "carseats": "car seats",
        "carseat": "car seat",
        "coatracks": "coat racks",
        "hatracks": "hat racks",
        "hatrack": "hat rack",
        "dumbell": "dumbbell",
        "dumbells": "dumbbells",
        "stepstool": "step stool",
        "stepstools": "steps tools",
        "bycicle": "bicycle",
        "bycicles": "bicycles",
    }

    for i in QA:
        for j in correction:
            if j in i[0].split(" "):
                i[0] = i[0].replace(j, correction[j])
        tsv_writer.writerow(i)
        
    zero_choice = random.sample(the_zero, min(len(the_one), len(the_zero), arg.const))
    for i in zero_choice:
        for j in correction:
            if j in i[0].split(" "):
                i[0] = i[0].replace(j, correction[j])
        tsv_writer.writerow(i)
        
    one_choice = random.sample(the_one, min(len(the_one), len(the_zero), arg.const))
    for i in one_choice:
        for j in correction:
            if j in i[0].split(" "):
                i[0] = i[0].replace(j, correction[j])
        tsv_writer.writerow(i)
        
    no_choice = random.sample(no, min(int(1.5 * yes_count), len(no)))
    for i in no_choice:
        for j in correction:
            if j in i[0].split(" "):
                i[0] = i[0].replace(j, correction[j])
        tsv_writer.writerow(i)
        
    medium_choice = random.sample(medium, int(min(len(medium), no_med_count)))
    for i in medium_choice:
        for j in correction:
            if j in i[0].split(" "):
                i[0] = i[0].replace(j, correction[j])
        tsv_writer.writerow(i)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--files",
        nargs="+",
        help="scene nums to generate questions",
        default=[1, 2, 3, 4],
    )
    parser.add_argument(
        "--filename", type=str, help="scene nums to generate questions", default="0"
    )
    parser.add_argument(
        "--data",
        type=str,
        help="path to json file",
        default="./info/scene_graph_info.json",
    )
    parser.add_argument(
        "--path",
        type=str,
        help="path to scene.annotated.ply",
        default="/datasets/released/scannet/public/v2/scans_extra/annotated",
    )
    parser.add_argument(
        "--qaj",
        type=str,
        help="path for json qa file to write in",
        default="./QA-allscene_json/",
    )
    parser.add_argument(
        "--sg",
        type=str,
        help="path to the folder for saving atr.tsv and scene_graph.tsv",
        default="./scene-graph/",
    )
    parser.add_argument(
        "--obb", type=str, help="path to the folder of obbs", default="../obbs/"
    )
    parser.add_argument(
        "--synonyms",
        type=str,
        help="path to the synonyms json file",
        default="./aliases.json",
    )
    parser.add_argument(
        "--thresholds",
        type=str,
        help="path to the synonyms json file for thresholds",
        default="./info/thresholds.json",
    )
    parser.add_argument(
        "--path_to_color_txt_files",
        type=str,
        help="path to xtc txt files",
        default="./",
    )

    args = parser.parse_args()

    data = json_reader(args.data)
    theDict = data["theDict"]
    category_list = data["category_list"]

    data = json_reader(args.thresholds)
    height_thresholds = data["height_thresholds"]
    vol_thresholds = data["volume_thresholds"]
    width_thresholds = data["width_thresholds"]

    if not os.path.exists(args.sg):
        os.makedirs(args.sg)

    if not os.path.exists(args.qaj):
        os.makedirs(args.qaj)

    files = os.listdir(args.path)
    start = time.time()
    
    for file in args.files:
        the_zero = []
        the_one = []
        yes_count = []
        medium = []
        no_med_count = []
        obj = {}
        path_to_annotation = os.path.join(args.path, str(file), str(file) + ".annotated.ply")
        
        with open(args.synonyms, "r") as f:
            synonyms = json.load(f)

        with open(os.path.join(args.obb, file, file + ".semseg.json"), "r") as f:
            obbs = json.load(f)
        
        if file.endswith("_00") and os.path.exists(path_to_annotation):
            directions = {}
            
            print("creating questions for {}".format(file))
    
            scene_graph(
                args.path_to_color_txt_files,
                path_to_annotation,
                theDict,
                category_list,
                height_thresholds,
                width_thresholds,
                vol_thresholds,
                obbs,
                args.filename,
                directions,
            )
            copyfile("./atr" + args.filename + ".tsv", args.sg + str(file) + "-atr.tsv")
            copyfile(
                "./Scene_Graph" + args.filename + ".tsv",
                args.sg + str(file) + "-scenegraph.tsv",
            )
            Q = qa_connect(obbs, file, synonyms, args.filename)

            with open(os.path.join(args.qaj, str(file) + ".json"), "w") as outfile:
                json.dump(Q, outfile)
