import argparse

def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_pc", type=str, help="path to point_cloud.hdf5", default="../point_cloud.hdf5")
    parser.add_argument("--path", type=str, help="path to scene.annotated.ply", default="/datasets/released/scannet/public/v2/scans_extra/annotated")
    parser.add_argument("--glove", type=str, help="path to glove", default="/localhome/yetesam/Desktop/glove/glove.6B.300d.txt")
    parser.add_argument("--qa_path",type=str,help="path to the folder containg questions and answers", default="/project/3dlg-hcvc/3dvqa/dataset_may18/sampled/")
    parser.add_argument("--splits", type=str, help= "path to the txt file for val/train/test splits", default ="/project/3dlg-hcvc/3dvqa/splits")
    parser.add_argument("--checkpoint_path", type=str, help="path to save the checkpoint", default = "checkpoint.tar")
    parser.add_argument("--do_val", type=bool , help="do the validation", default = True)
    parser.add_argument("--do_test", type=bool, help="do the test", default = True)
    parser.add_argument("--fused_attention", type=bool, help="use 3d fused attention if true", default = True)
    parser.add_argument("--lr", type=float, help="learning rate", default = 0.001)
    parser.add_argument("--step_size", type=int, help="step size for scheduler", default = 2)
    parser.add_argument("--gamma", type=float, help="gamma for scheduler", default = 0.5)
    parser.add_argument("--epochs", type=int, help="maximum number of epochs", default = 30)
    parser.add_argument("--embedding_dim", type=int, help="embedding dimention of the lstm", default = 300)
    parser.add_argument("--hidden_dim", type=int, help="hidden dimention of the lstm", default = 300)
    parser.add_argument("--3dscene_path", type=str, help="path to 3d scenes of scannet", default="/home/yetesam/Desktop/Pointnet2.ScanNet/scripts/votenet/scannet/scannet_train_detection_data")
    parser.add_argument("--ply_path" , type=str , help="path the to point clouds", default="/datasets/released/scannet/public/v2/scans")
    args = parser.parse_args()
    return args
