import argparse

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--satfaces", type=float, help="path to satfaces.txt file", default = "./satfaces.txt")
    parser.add_argument("--mainsurvey", type=float, help="path to mainsurvey_sqldump.txt file", default = "./mainsurvey_sqldump.txt")
    parser.add_argument("--files", nargs="+", help="scene nums to generate questions", default=[1,2,3,4]) 
    parser.add_argument("--filename", type=str, help="scene nums to generate questions", default='0')
    parser.add_argument("--data",type=str,help="path to json file", default="./scene_graph_info.json") 
    parser.add_argument("--qa",type=str,help="path to qa file to write in", default="./QA-allscene/")
    parser.add_argument("--path", type=str, help="path to scene.annotated.ply", default="/datasets/released/scannet/public/v2/scans_extra/annotated") 
    parser.add_argument("--qaj",type=str,help="path for json qa file to write in", default="./QA-allscene_json/")
    parser.add_argument("--qaj_sampled",type=str,help="path for json qa file to write in", default="./QA-allscene_json_sampled/")
    parser.add_argument("--const", type=int, help="number of zeroes, ones, comparisons" ,default=1000) 
    parser.add_argument("--sg", type = str, help = "path to the folder for saving atr.tsv and scene_graph.tsv", default = "./scene-graph/") 
    parser.add_argument("--obb", type = str, help = "path to the folder of obbs" , default = "../obbs/") 
    parser.add_argument("--synonyms", type=str, help="path to the synonyms json file", default="./aliases.json")
    parser.add_argument("--thresholds", type=str, help="path to the synonyms json file for thresholds", default="./thresholds.json") 
    parser.add_argument("--path_to_color_txt_files", type=str, help="path to xtc txt files", default="./")
    parser.add_argument("--color_ckp", type=str, help="path to checkpoints of trained model for predicting color", default=".color_checkpoint_2.pth")
    args = parser.parse_args()
    return args
