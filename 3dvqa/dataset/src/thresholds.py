import json
import math
import os
import csv
from plyfile import PlyData, PlyElement
import numpy as np
from config import config
object_dist_height = {}
object_dist_volume = {}
object_dist_width = {}
num_scenes = 0
args = config()
for file in os.listdir(args.obb):
    if file.endswith('_00') and os.path.exists(args.path+str(file) +"/" + str(file) + ".annotated.ply") :
        with open(args.obb+str(file) +"/" + str(file) + ".semseg.json","r") as f:
            obbs = json.load(f)
#            print(plydata)
            for i in obbs["segGroups"]:          
                    if i["label"] in object_dist_height:
                        object_dist_height[i["label"]].append(i["obb"]["axesLengths"][2])
                    else:
                        
                        object_dist_height[i["label"]] = [i["obb"]["axesLengths"][2]]
                    ### width
                    if i["label"] in object_dist_width:
                        object_dist_width[i["label"]].append(min(i["obb"]["axesLengths"][0],i["obb"]["axesLengths"][1])) 
                    else:
                        object_dist_width[i["label"]] = [min(i["obb"]["axesLengths"][0],i["obb"]["axesLengths"][1])]
              
                    if i["label"] in object_dist_volume:
                        object_dist_volume[i["label"]].append(i["obb"]["axesLengths"][0]*i["obb"]["axesLengths"][1]*i["obb"]["axesLengths"][2])
                    else:
                        object_dist_volume[i["label"]] = [i["obb"]["axesLengths"][0]*i["obb"]["axesLengths"][1]*i["obb"]["axesLengths"][2]]
              

#print(object_dist_height["table"])
#print(object_dist_width["table"])
#print(object_dist_volume["table"])
#hi

volume_thresholds = {}
for i in object_dist_volume:
    volume_thresholds[i] = {}
    mean_volume = np.mean(object_dist_volume[i])
    sd_volume = math.sqrt(np.var(object_dist_volume[i]))
    volume_thresholds[i]["upperbound"] = mean_volume + sd_volume
    volume_thresholds[i]["lowerbound"] = mean_volume - sd_volume


height_thresholds = {}
for i in object_dist_height:
    height_thresholds[i] = {}
    mean_height = np.mean(object_dist_height[i])
    sd_height = math.sqrt(np.var(object_dist_height[i]))
    height_thresholds[i]["upperbound"] = mean_height + sd_height
    height_thresholds[i]["lowerbound"] = mean_height - sd_height


width_thresholds = {}
for i in object_dist_width:
    width_thresholds[i] = {}
    mean_width = np.mean(object_dist_width[i])
    sd_width = math.sqrt(np.var(object_dist_width[i]))
    width_thresholds[i]["upperbound"] = mean_width + sd_width
    width_thresholds[i]["lowerbound"] = mean_width - sd_width



with open("thresholds.json" , "w") as outfile:
    json.dump({"height_thresholds":height_thresholds , "width_thresholds":width_thresholds , "volume_thresholds":volume_thresholds},outfile)


