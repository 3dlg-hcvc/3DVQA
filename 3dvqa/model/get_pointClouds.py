import h5py
import numpy as np
import os
import argparse
import sys
from config import config
from utils import train_val_lists
import numpy as np


def random_sampling(pc, num_sample, return_choices=False):
    replace = (pc.shape[0]<num_sample)
    choices = np.random.choice(pc.shape[0], num_sample, replace=replace)
    if return_choices:
        return pc[choices], choices
    else:
        return pc[choices]

def preprocess_point_cloud(point_cloud):
    Number_of_points_to_sample = 40000
    point_cloud = point_cloud[:, 0:6]
    point_cloud = random_sampling(point_cloud, Number_of_points_to_sample)
    pc = np.expand_dims(point_cloud.astype(np.float32), 0)
    return pc


def get_pcs(the_scene):
    args = config()
    mesh_vertices = np.load(os.path.join(
        args.scene_path,
        str(the_scene) + "_vert.npy")
        )
    point_cloud = mesh_vertices[:, 0:6]
    pc = preprocess_point_cloud(point_cloud[:, 0:6])
    inputs = {"point_clouds": pc}
    return inputs


def get_pc_dict(scenes):
    args = config() 
    pcs = {}
    for i in scenes:
        pcs[i] = get_pcs(i)
    if not os.path.exists(args.point_cloud_hdf5):
        f = h5py.File(args.point_cloud_hdf5, "w")
        for k, v in pcs.items():
            print(k)

            if k not in f:
                f.create_dataset(k, data=np.array(v["point_clouds"], dtype=np.int8))


if __name__ == "__main__":
    args = config()
    train, val, test = train_val_lists(args)
    print(len(train))
    get_pc_dict(train + val + test)
