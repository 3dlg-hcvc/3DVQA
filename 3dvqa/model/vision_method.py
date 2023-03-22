import argparse
import h5py
import torch
import numpy as np
from tqdm import tqdm
import torch.optim as optim
from config import config

from utils import train_val_lists
from votenet_with_color.scannet.scannet_detection_dataset import DC
from votenet_with_color.models.votenet import VoteNet

class Pretrained:
    def __init__(self, checkpoint_path):
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.net = VoteNet(
            num_proposal=256,
            input_feature_dim=3,
            num_clrs=3,
            vote_factor=1,
            sampling="seed_fps",
            num_class=DC.num_class,
            num_heading_bin=DC.num_heading_bin,
            num_size_cluster=DC.num_size_cluster,
            mean_size_arr=DC.mean_size_arr,
        ).to(device)

        # Load checkpoint
        optimizer = optim.Adam(self.net.parameters(), lr=0.001)
        checkpoint = torch.load(checkpoint_path)
        self.net.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        self.net.eval()
    
    def inferemce(self, scene):
        with torch.no_grad():
            end_points = self.net(scene)

        return end_points


if __name__ == "__main__":

    args = config()


    train, val, test = train_val_lists(args)
    votenet = True
    pointnet = True

    if votenet:
        votenet_dict = {}
        model = Pretrained(args.checkpoint_color_votenet)
        
        with h5py.File(args.votenet_hdf5) as f:
            with h5py.File(args.point_cloud_hdf5, "r") as h5py_file:
                for i in tqdm(train + val + test):
                    pc = torch.from_numpy(np.array(h5py_file[i][:], dtype=np.float32))
                    endpoint = model.inferemce(pc.cuda())
                    votenet_dict[i] = (
                        endpoint["vqa_in"]
                        .view(endpoint["vqa_in"].shape[0], endpoint["vqa_in"].shape[2], -1)
                        .squeeze()
                        .cpu()
                    )

            for k, v in votenet_dict.items():
                if k not in f:
                    f.create_dataset(k, data=np.array(v, dtype=np.int8))

    if pointnet:
        model_path = os.path.join(args.folder, "model.pth")  
        Pointnet = importlib.import_module("pointnet2_semseg") 
        model = Pointnet.get_model(num_classes=20, is_msg=True, input_channels=3, use_xyz=True, bn=True).cuda() 
        model.load_state_dict(torch.load(model_path))  
        model.eval() 
        pointnet_dict = {}
        with h5py.File(args.pointnet_hdf5,'w') as f:
            for i in train+val+test:
                with h5py.File(args.point_cloud_hdf5, 'r') as ff:
                    point_out = ff[i][:]
                    pc = torch.from_numpy(point_out).float()
                    with torch.no_grad():
                        output , xyz, feat= model(torch.cat([pc[:,:,0:3].cuda(), pc[:,:,3:6].cuda()], dim=2))
                        x = torch.transpose(feat[-1].view(1024,16,-1),0,2)[0]
                        pointnet_dict[i]=torch.transpose(x,0,1).cpu()
                        
            for k,v in pointnet_dict.items():
                if k not in f:
                    f.create_dataset(k, data=np.array(v, dtype=np.int8))
