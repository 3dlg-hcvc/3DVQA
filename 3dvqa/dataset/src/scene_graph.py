import json
import numpy as np
from plyfile import PlyData, PlyElement
import csv
import torch
import os
from config import config
from constant import constant

args = config()


class sceneGraph:
    def __init__(
        self,
        color_path,
        path_to_ply,
        theDict,
        category_list,
        height_thresholds,
        width_thresholds,
        vol_thresholds,
        obbs,
        filename,
        data_dir,
        classes,
    ):
        self.classes = classes
        self.direction = False
        self.dirs = data_dir
        self.path_to_ply = path_to_ply
        self.filename = filename
        self.theDict = theDict
        self.category_list = category_list
        self.height_thresholds = height_thresholds
        self.vol_thresholds = vol_thresholds
        self.width_thresholds = width_thresholds
        self.obbs = obbs
        obb = {}
        for i in obbs["segGroups"]:
            obb[i["objectId"] + 1] = i["obb"]
        self.obb = obb

    def hsl_value(self, inColor):
        lightness = (
            max(inColor[0] / 255, inColor[1] / 255, inColor[2] / 255)
            + min(inColor[0] / 255, inColor[1] / 255, inColor[2] / 255)
        ) / 2
        if 0 <= lightness and lightness < 0.25:
            light_range = 1
        elif 0.25 <= lightness and lightness < 0.5:
            light_range = 2
        elif 0.5 <= lightness and lightness < 0.75:
            light_range = 3
        else:
            light_range = 4
        return lightness

    def number_point_inside(self, obbi, consi, obbj, consj, xyz):
        # print(xyz)
        points_i = []
        points_j = []
        ver = []
        x, y, z = obbj["centroid"]
        a, b, c = obbj["axesLengths"]
        a = a + a * consj[0]
        b = b + b * consj[1]
        c = c + c * consj[2]
        rot = np.array(obbj["normalizedAxes"]).reshape(3, 3).transpose()
        points_pre_j = [
            rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
        ]

        cent_after = (np.array(points_pre_j[0]) + np.array(points_pre_j[-1])) / 2
        points_j += [
            i - cent_after + np.array([x, y, z])
            for i in [
                rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
            ]
        ]
        # points_j = sorted(points_j, key = lambda x: int(x[-1]))

        x, y, z = obbi["centroid"]
        a, b, c = obbi["axesLengths"]
        a = a + a * consi[0]
        b = b + b * consi[1]
        c = c + c * consi[2]
        rot = np.array(obbi["normalizedAxes"]).reshape(3, 3).transpose()
        points_pre_i = [
            rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
        ]

        cent_after = (np.array(points_pre_i[0]) + np.array(points_pre_i[-1])) / 2
        points_i += [
            i - cent_after + np.array([x, y, z])
            for i in [
                rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
            ]
        ]
        # points_i = sorted(points_i, key = lambda x: int(x[-1]))
        # print(points_j)
        # print("---")
        # print(points_i)
        maxx = max(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[0],
        )

        minx = min(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[0],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[0],
        )

        maxy = max(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[1],
        )

        miny = min(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[1],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[1],
        )

        maxz = max(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[2],
        )

        minz = min(
            np.linalg.inv(rot).dot(np.array(points_i[0]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[1]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[2]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[3]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[4]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[5]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[6]))[2],
            np.linalg.inv(rot).dot(np.array(points_i[7]))[2],
        )

        if xyz == "xy":
            # print(maxx,minx,maxy,miny)
            # print("----------------------------")
            j_rot = [
                (
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[1],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[1],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[2]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[2]))[1],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[1],
                ),
            ]
            # print(j_rot)

            n_points = 0
            for k in j_rot:
                if k[0] > minx and k[0] < maxx and k[1] > miny and k[1] < maxy:
                    n_points += 1
                    ver.append(k)
            # print(n_points)
            # print("--------------------------------")
            return n_points, ver
        if xyz == "xz":
            points_j = sorted(points_j, key=lambda x: int(x[1]))
            j_rot = [
                (
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[4]))[0],
                    np.linalg.inv(rot).dot(np.array(points_j[4]))[2],
                ),
            ]
            n_points = 0
            for k in j_rot:
                if k[0] > minx and k[0] < maxx and k[1] > minz and k[1] < maxz:
                    n_points += 1
                    ver.append(k)
            return n_points, ver
        if xyz == "yz":
            # print(points_j)
            points_j = sorted(points_j, key=lambda x: int(x[0]))
            j_rot = [
                (
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[1],
                    np.linalg.inv(rot).dot(np.array(points_j[0]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[1],
                    np.linalg.inv(rot).dot(np.array(points_j[1]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[1],
                    np.linalg.inv(rot).dot(np.array(points_j[3]))[2],
                ),
                (
                    np.linalg.inv(rot).dot(np.array(points_j[4]))[1],
                    np.linalg.inv(rot).dot(np.array(points_j[4]))[2],
                ),
            ]
            # print(j_rot)
            # print(minx,maxx,minz,maxz)
            n_points = 0
            for k in j_rot:
                if k[0] > miny and k[0] < maxy and k[1] > minz and k[1] < maxz:
                    n_points += 1
                    ver.append(k)
            return n_points, ver

    def get_xy_maxz(self, obb):
        points = []
        # print(obb)
        x, y, z = obb["centroid"]
        a, b, c = obb["axesLengths"]
        rot = np.array(obb["normalizedAxes"]).reshape(3, 3).transpose()
        points_pre = [
            rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
        ]

        cent_after = (np.array(points_pre[0]) + np.array(points_pre[-1])) / 2
        points += [
            i - cent_after + np.array([x, y, z])
            for i in [
                rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
            ]
        ]

        # points_sorted = sorted(points, key = lambda x: int(x[-1]))
        return (
            (
                (points[0][0], points[0][1]),
                (points[1][0], points[1][1]),
                (points[2][0], points[2][1]),
                (points[3][0], points[3][1]),
            ),
            obb["max"][2],
        )

    def xyz_expand(self, obb, cons):
        points = []
        x, y, z = obb["centroid"]
        a, b, c = obb["axesLengths"]
        rot = np.array(obb["normalizedAxes"]).reshape(3, 3).transpose()
        a = a + a * cons[0]
        b = b + b * cons[1]
        c = c + c * cons[2]
        points_pre = [
            rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
        ]

        cent_after = (np.array(points_pre[0]) + np.array(points_pre[-1])) / 2
        points += [
            i - cent_after + np.array([x, y, z])
            for i in [
                rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
            ]
        ]
        # points = sorted(points, key = lambda x: int(x[2]))
        return points

    def xyz_expand_2(self, obb, cons):
        points = []
        x, y, z = obb["centroid"]
        a, b, c = obb["axesLengths"]
        rot = np.array(obb["normalizedAxes"]).reshape(3, 3).transpose()
        a = a + a * cons[0]
        b = b + b * cons[1]
        c = c + c * cons[2]
        points_pre = [
            rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
            rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
        ]

        cent_after = (np.array(points_pre[0]) + np.array(points_pre[-1])) / 2
        points += [
            i - cent_after + np.array([x, y, z])
            for i in [
                rot.dot(np.array([x - a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z - c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y - b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x - a / 2, y + b / 2, z + c / 2])).tolist(),
                rot.dot(np.array([x + a / 2, y + b / 2, z + c / 2])).tolist(),
            ]
        ]
        # points = sorted(points, key = lambda x: int(x[2]))
        return (
            (points[0][0], points[0][1]),
            (points[1][0], points[1][1]),
            (points[2][0], points[2][1]),
            (points[3][0], points[3][1]),
        )

    def obb_intersection_helper(self, xy1, xy2):
        if isinstance(xy2, dict):
            xy2, _ = self.get_xy_maxz(xy2)

        if isinstance(xy1, dict):
            xy1, _ = self.get_xy_maxz(xy1)

        longest = 0
        od = 0
        for i in [1, 2, 3]:
            l = (xy1[0][0] - xy1[i][0]) ** 2 + (xy1[0][1] - xy1[i][1]) ** 2
            if l > longest:
                longest = l
                od = i
        xy1 = np.array(xy1)
        xy2 = np.array(xy2)
        az = [1, 2, 3]
        az.remove(od)
        lines = []
        for j in [0, od]:
            for i in az:
                l2 = np.sum((xy1[j] - xy1[i]) ** 2)

                if (
                    (
                        np.sum((xy2[0] - xy1[j]) * (xy1[i] - xy1[j])) / l2 > 1
                        or np.sum((xy2[0] - xy1[j]) * (xy1[i] - xy1[j])) / l2 < 0
                    )
                    and (
                        np.sum((xy2[1] - xy1[j]) * (xy1[i] - xy1[j])) / l2 > 1
                        or np.sum((xy2[1] - xy1[j]) * (xy1[i] - xy1[j])) / l2 < 0
                    )
                    and (
                        np.sum((xy2[2] - xy1[j]) * (xy1[i] - xy1[j])) / l2 > 1
                        or np.sum((xy2[2] - xy1[j]) * (xy1[i] - xy1[j])) / l2 < 0
                    )
                    and (
                        np.sum((xy2[3] - xy1[j]) * (xy1[i] - xy1[j])) / l2 > 1
                        or np.sum((xy2[3] - xy1[j]) * (xy1[i] - xy1[j])) / l2 < 0
                    )
                ):
                    x0 = xy1[j] + (
                        np.sum((xy2[0] - xy1[j]) * (xy1[i] - xy1[j])) / l2
                    ) * (xy1[i] - xy1[j])
                    x1 = xy1[j] + (
                        np.sum((xy2[1] - xy1[j]) * (xy1[i] - xy1[j])) / l2
                    ) * (xy1[i] - xy1[j])
                    x2 = xy1[j] + (
                        np.sum((xy2[2] - xy1[j]) * (xy1[i] - xy1[j])) / l2
                    ) * (xy1[i] - xy1[j])
                    x3 = xy1[j] + (
                        np.sum((xy2[3] - xy1[j]) * (xy1[i] - xy1[j])) / l2
                    ) * (xy1[i] - xy1[j])
                    if max(
                        np.sum(x0 - x1) ** 2,
                        np.sum(x0 - x2) ** 2,
                        np.sum(x0 - x3) ** 2,
                        np.sum(x1 - x2) ** 2,
                        np.sum(x1 - x3) ** 2,
                        np.sum(x2 - x3) ** 2,
                    ) < max(
                        np.sum(x0 - xy1[i]) ** 2,
                        np.sum(x0 - xy1[j]) ** 2,
                        np.sum(x1 - xy1[i]) ** 2,
                        np.sum(x1 - xy1[j]) ** 2,
                        np.sum(x2 - xy1[i]) ** 2,
                        np.sum(x2 - xy1[j]) ** 2,
                        np.sum(x3 - xy1[i]) ** 2,
                        np.sum(x3 - xy1[j]) ** 2,
                    ):
                        return False
        return True

    def obb_intersection(self, xy1, xy2):
        if self.obb_intersection_helper(xy1, xy2) or self.obb_intersection_helper(
            xy2, xy1
        ):
            return True
        else:
            return False

    def intersection(self, maxx1, minx1, maxy1, miny1, maxx2, minx2, maxy2, miny2):
        xmax = min(maxx1, maxx2)
        xmin = max(minx1, minx2)
        ymax = min(maxy1, maxy2)
        ymin = max(miny1, miny2)
        if xmax < xmin or ymax < ymin:
            return False
        else:
            return True

    def color_trained(self, incolor):
        model = color_model(len(self.classes))
        model.load_state_dict(
            torch.load(args.color_ckp, map_location=torch.device("cpu"))
        )
        model.eval()
        with torch.no_grad():
            score = model(torch.FloatTensor(incolor))
            predictions = self.classes[torch.argmax(score)]
        return predictions

    def color_lookup_table(self):
        rgb_cube_path = args.satfaces
        main_survey_path = args.mainsurvey
        main_color_names_map = {}
        main_color_names = constant.main_color_names
        for i in main_color_names:
            main_color_names_map[i] = i
            if main_color_names[i] != None:
                for j in main_color_names[i]:
                    main_color_names_map[j] = i
        color_look_up = {}
        with open(rgb_cube_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            l = line.split("]")
            ll = l[0][1:].split(",")
            rgb = (int(ll[0]), int(ll[1]), int(ll[2]))
            color_name = str(l[1][0:-1])
            color_name = " ".join(color_name.split())
            if color_name in main_color_names_map:
                color_look_up[rgb] = main_color_names_map[color_name]
            else:
                print(main_color_names_map)
                print(color_name)
                hi
        rgb_cube = dict(color_look_up)

        with open(main_survey_path, "r") as f:
            lines = f.readlines()
        first = lines[4:152404]
        second = lines[152407:3560442]
        for i in first:
            c = (i.split(",")[-2][1:-1]).split("/")
            c1 = c[0]
            c2 = c[1]
            if c1 == "gray":
                c1 = "grey"
            if c2 not in main_color_names_map:
                main_color_names_map[c2] = c1
        for j in second:
            sp = j.split(",")
            col = sp[-1][1:-4]
            if sp[-2].isnumeric() and sp[-3].isnumeric() and sp[-4].isnumeric():
                rgb = (int(sp[-4]), int(sp[-3]), int(sp[-2]))
                if col in main_color_names_map:
                    color_look_up[rgb] = main_color_names_map[col]
        return color_look_up, rgb_cube

    def colorMap(self, inColor, table, rgb_cube):
        if (inColor[0], inColor[1], inColor[2]) in table:
            return table[(inColor[0], inColor[1], inColor[2])]
        for i in [
            1,
            -1,
            2,
            -2,
            3,
            -3,
            4,
            -4,
            5,
            -5,
            6,
            -6,
            7,
            -7,
            8,
            -8,
            9,
            -9,
            10,
            -10,
            11,
            -11,
            12,
            -12,
        ]:
            if (inColor[0], inColor[1], inColor[2] + i) in table:
                return table[(inColor[0], inColor[1], inColor[2] + i)]
            if (inColor[0] + i / 2, inColor[1], inColor[2]) in table:
                return table[(inColor[0] + i / 2, inColor[1], inColor[2])]
            if (inColor[0], inColor[1] + i / 4, inColor[2]) in table:
                return table[(inColor[0], inColor[1] + i / 4, inColor[2])]
            if (inColor[0] + i / 2, inColor[1], inColor[2] + i) in table:
                return table[(inColor[0] + i / 2, inColor[1], inColor[2] + i)]
            if (inColor[0], inColor[1] + i / 4, inColor[2] + i) in table:
                return table[(inColor[0], inColor[1] + i / 4, inColor[2] + i)]
            if (inColor[0] + i / 2, inColor[1] + i / 4, inColor[2]) in table:
                return table[(inColor[0] + i / 2, inColor[1] + i / 4, inColor[2])]
            if (inColor[0] + i / 2, inColor[1] + i / 4, inColor[2] + i) in table:
                return table[(inColor[0] + i / 2, inColor[1] + i / 4, inColor[2] + i)]
        dict = constant.rgb_dict
        min_dis = 100000000
        for i in dict:
            dis = (
                (((dict[i][0] - int(inColor[0])) * 0.299) ** 2)
                + (((dict[i][1] - int(inColor[1])) * 0.587) ** 2)
                + (((dict[i][2] - int(inColor[2])) * 0.114) ** 2)
            )
            if min_dis > dis:
                min_dis = dis
                theColor = i
        return theColor

    def points_color_light(self):
        lut, rgb_cube = self.color_lookup_table()
        with open(self.path_to_ply, "rb") as f:
            ids = []
            colors_dict = {}
            light_dict = {}
            objectID_type = {}
            category_type = {}
            plydata = PlyData.read(f)
            for i in range(len(plydata["vertex"]["objectId"])):
                if plydata["vertex"]["objectId"][i] not in ids:
                    ids.append(plydata["vertex"]["objectId"][i])
                    colors_dict[plydata["vertex"]["objectId"][i]] = {}
                    light_dict[plydata["vertex"]["objectId"][i]] = {}
                    objectID_type[plydata["vertex"]["objectId"][i]] = plydata["vertex"][
                        "NYU40"
                    ][i]
                    category_type[plydata["vertex"]["objectId"][i]] = plydata["vertex"][
                        "categoryId"
                    ][i]
                else:
                    color_vec = [
                        plydata["vertex"]["red"][i],
                        plydata["vertex"]["green"][i],
                        plydata["vertex"]["blue"][i],
                    ]
                    color_ins = self.colorMap(color_vec, lut, rgb_cube)
                    light_ins = self.hsl_value(color_vec)
                    if (
                        color_ins == "red"
                        or color_ins == "crimson"
                        or color_ins == "dark red"
                        or color_ins == "indian red"
                        or color_ins == "maroon"
                    ):
                        color_ins = "red"
                    if (
                        color_ins == "blue"
                        or color_ins == "aqua"
                        or color_ins == "MediumBlue"
                        or color_ins == "navy"
                        or color_ins == "RoyalBlue"
                        or color_ins == "DodgerBlue"
                        or color_ins == "LightBlue"
                        or color_ins == "SkyBlue"
                        or color_ins == "cyan"
                    ):
                        color_ins = "blue"
                    if (
                        color_ins == "green"
                        or color_ins == "olive"
                        or color_ins == "lime"
                        or color_ins == "dark green"
                        or color_ins == "SpringGreen"
                        or color_ins == "LightGreen"
                    ):
                        color_ins = "green"
                    if color_ins == "gray" or color_ins == "silver":
                        color_ins = "gray"
                    if (
                        color_ins == "pink"
                        or color_ins == "HotPink"
                        or color_ins == "DeepPink"
                    ):
                        color_ins = "pink"
                    if (
                        color_ins == "purple"
                        or color_ins == "violet"
                        or color_ins == "DarkViolet"
                        or color_ins == "Indigo"
                    ):
                        color_ins = "purple"
                    if (
                        color_ins == "brown"
                        or color_ins == "SaddleBrown"
                        or color_ins == "Tan"
                        or color_ins == "Chocolate"
                        or color_ins == "Sienna"
                        or color_ins == "RosyBrown"
                        or color_ins == "DarkGoldenrod"
                    ):
                        color_ins = "brown"
                    if (
                        color_ins == "yellow"
                        or color_ins == "Gold"
                        or color_ins == "Khaki"
                    ):
                        color_ins = "yellow"
                    if (
                        color_ins == "orange"
                        or color_ins == "DarkOrange"
                        or color_ins == "Tomato"
                        or color_ins == "Coral"
                    ):
                        color_ins = "orange"
                    if (
                        color_ins == "cream1"
                        or color_ins == "cream2"
                        or color_ins == "cream3"
                    ):
                        color_ins = "cream"
                    if (
                        color_ins == "white"
                        or color_ins == "snow"
                        or color_ins == "Ghost white"
                        or color_ins == "white smoke"
                    ):
                        color_ins = "white"
                    if color_ins == "black":
                        color_ins = "black"
                    if color_ins not in colors_dict[plydata["vertex"]["objectId"][i]]:
                        colors_dict[plydata["vertex"]["objectId"][i]][color_ins] = 1
                    else:
                        colors_dict[plydata["vertex"]["objectId"][i]][color_ins] += 1
                    if light_ins not in light_dict[plydata["vertex"]["objectId"][i]]:
                        light_dict[plydata["vertex"]["objectId"][i]][light_ins] = 1
                    else:
                        light_dict[plydata["vertex"]["objectId"][i]][light_ins] += 1
        return colors_dict, light_dict, category_type, objectID_type

    def points_position(self):
        with open(self.path_to_ply, "rb") as f:
            plydata = PlyData.read(f)
            ids = []
            position = {}
            objectID_type = {}
            for i in range(len(plydata["vertex"]["objectId"])):
                if plydata["vertex"]["objectId"][i] not in ids:
                    ids.append(plydata["vertex"]["objectId"][i])
                    position[plydata["vertex"]["objectId"][i]] = {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "n": 1,
                        "maxx": plydata["vertex"]["x"][i],
                        "maxy": plydata["vertex"]["y"][i],
                        "maxz": plydata["vertex"]["z"][i],
                        "minx": plydata["vertex"]["x"][i],
                        "miny": plydata["vertex"]["y"][i],
                        "minz": plydata["vertex"]["z"][i],
                    }
                    objectID_type[plydata["vertex"]["objectId"][i]] = plydata["vertex"][
                        "NYU40"
                    ][i]
                else:
                    position[plydata["vertex"]["objectId"][i]]["n"] += 1
                    if (
                        position[plydata["vertex"]["objectId"][i]]["maxx"]
                        < plydata["vertex"]["x"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["maxx"] = plydata[
                            "vertex"
                        ]["x"][i]
                    if (
                        position[plydata["vertex"]["objectId"][i]]["maxy"]
                        < plydata["vertex"]["y"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["maxy"] = plydata[
                            "vertex"
                        ]["y"][i]
                    if (
                        position[plydata["vertex"]["objectId"][i]]["maxz"]
                        < plydata["vertex"]["z"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["maxz"] = plydata[
                            "vertex"
                        ]["z"][i]
                    if (
                        position[plydata["vertex"]["objectId"][i]]["minx"]
                        > plydata["vertex"]["x"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["minx"] = plydata[
                            "vertex"
                        ]["x"][i]
                    if (
                        position[plydata["vertex"]["objectId"][i]]["miny"]
                        > plydata["vertex"]["y"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["miny"] = plydata[
                            "vertex"
                        ]["y"][i]
                    if (
                        position[plydata["vertex"]["objectId"][i]]["minz"]
                        > plydata["vertex"]["z"][i]
                    ):
                        position[plydata["vertex"]["objectId"][i]]["minz"] = plydata[
                            "vertex"
                        ]["z"][i]
        return position

    def find_dominant_color(self, d):
        max_each = {}
        for i in d:
            mm = 0
            for j in d[i]:
                if d[i][j] > mm:
                    mm = d[i][j]
                    dominant = j
            mmm = 0
            for j in d[i]:
                if d[i][j] > mmm and j != dominant:
                    mmm = d[i][j]
                    dominant2 = j
            # print(i,dominant,mm,dominant2,mmm)
            if dominant == "black":
                if dominant2 != "grey" and mmm + mmm // 100 > mm // 3:
                    dominant = dominant2
                if dominant2 == "grey" and mmm + mm // 100 > 2 * mm // 3:
                    dominant = dominant2
            if dominant == "grey":
                if dominant2 != "black" and mmm + mm // 100 > mm // 3:
                    dominant = dominant2
            max_each[i] = dominant
        # print(max_each)
        return max_each

    def find_dominant_light(self, d):
        max_each = {}
        for i in d:
            mm = 0
            nn = 0
            for j in d[i]:
                mm += j * d[i][j]
                nn += d[i][j]
            max_each[i] = mm / nn
        return max_each

    def find_atributes(
        self,
        position,
        color_dict,
        light_dict,
        category_type,
        objectID_type,
        max_color,
        max_light,
    ):
        fine_dict = {}
        for i in self.obb:
            if (
                i != 0
                and i in category_type
                and str(category_type[i]) in self.category_list
            ):
                if (
                    (self.obb[i]["axesLengths"][0])
                    * (self.obb[i]["axesLengths"][1])
                    * (self.obb[i]["axesLengths"][2])
                    < self.vol_thresholds[self.category_list[str(category_type[i])]][
                        "lowerbound"
                    ]
                ):
                    object_size = "small"
                elif (
                    (self.obb[i]["axesLengths"][0])
                    * (self.obb[i]["axesLengths"][1])
                    * (self.obb[i]["axesLengths"][2])
                    > self.vol_thresholds[self.category_list[str(category_type[i])]][
                        "upperbound"
                    ]
                ):
                    object_size = "large"
                else:
                    object_size = "medium"
                if (self.obb[i]["axesLengths"][2]) < self.height_thresholds[
                    self.category_list[str(category_type[i])]
                ]["lowerbound"]:
                    height = "short"
                elif (self.obb[i]["axesLengths"][2]) > self.height_thresholds[
                    self.category_list[str(category_type[i])]
                ]["upperbound"]:
                    height = "tall"
                else:
                    height = "medium"

                ### width
                if (
                    min(self.obb[i]["axesLengths"][0], self.obb[i]["axesLengths"][1])
                    < self.width_thresholds[self.category_list[str(category_type[i])]][
                        "lowerbound"
                    ]
                ):
                    width = "thin"
                elif (
                    min(self.obb[i]["axesLengths"][0], self.obb[i]["axesLengths"][1])
                    > self.width_thresholds[self.category_list[str(category_type[i])]][
                        "upperbound"
                    ]
                ):
                    width = "wide"
                else:
                    width = "medium"

                fine_dict[i] = {
                    "category": self.category_list[str(category_type[i])],
                    "object_group": self.theDict[str(objectID_type[i])],
                    "x": round((position[i]["maxx"] + position[i]["minx"]) / 2, 2),
                    "y": round((position[i]["maxy"] + position[i]["miny"]) / 2, 2),
                    "z": round((position[i]["minz"] + position[i]["maxz"]) / 2, 2),
                    "maxx": position[i]["maxx"],
                    "maxy": position[i]["maxy"],
                    "maxz": position[i]["maxz"],
                    "minx": position[i]["minx"],
                    "miny": position[i]["miny"],
                    "minz": position[i]["minz"],
                    "color": max_color[i],
                    "lightness": max_light[i],
                    "height": height,
                    "object_volume": object_size,
                    "width": width,
                }

        outfile = open("./atr" + self.filename + ".tsv", "wt")
        tsv_writer_atr = csv.writer(outfile, delimiter="\t")
        # tsv_writer_atr.writerow(['objectID', 'category', 'object_group', 'x','y','z','maxx','maxy','maxz','minx','miny','minz','color','lightness','height','object_volume'])
        for i in fine_dict:
            tsv_writer_atr.writerow([i] + list(fine_dict[i].values()))
        return fine_dict

    def create_scene_graph(self, scene):
        Scene_Graph = []
        out_file = open("./Scene_Graph" + self.filename + ".tsv", "wt")
        tsv_writer = csv.writer(out_file, delimiter="\t")
        for i in scene:
            if self.direction:
                idir = self.dirs[str(i - 1)]
                if idir["orientation"] != []:
                    x1 = idir["orientation"][0][0]
                    y1 = idir["orientation"][0][1]
                    x2 = idir["orientation"][1][0]
                    y2 = idir["orientation"][1][1]
                    difx = x2 - x1
                    dify = y2 - y1
                    if abs(dify) < abs(difx):
                        if difx > 0:
                            yl = y1 + 10
                            xl = x1
                        else:
                            yl = y1 - 10
                            xl = x1
                    else:
                        if dify > 0:
                            xl = x1 - 10
                            yl = y1
                        else:
                            xl = x1 + 10
                            yl = y1
                    dl = (xl - x1) * (y2 - y1) - (yl - y1) * (x2 - x1)

                icenter = idir["centroid"]
            for j in scene:

                # if i == 12 and j ==3:
                # print(self.number_point_inside(self.obb[j],[0,0.05,0.05],self.obb[i],[0,0,0],'yz'))
                # print(self.number_point_inside(self.obb[j],[0,0.05,0.05],self.obb[i],[0,0,0],'xz'))
                # print(scene[i]['minz'] ,scene[j]['minz'])
                if (
                    j != i
                    and self.direction
                    and icenter[2] - jdir["centroid"][2] < 0.5
                    and idir["orientation"] != []
                    and scene[j]["category"] != "floor"
                    and scene[j]["category"] != "ceiling"
                ):
                    jdir = self.dirs[str(j - 1)]
                    corner, _ = self.get_xy_maxz(self.obb[j])
                    jcenter = jdir["centroid"]
                    x = jcenter[0]
                    y = jcenter[1]
                    if (icenter[0] - x) ** 2 + (icenter[1] - y) ** 2 < (
                        max(idir["axesLengths"][0], idir["axesLengths"][1]) ** 2
                        + max(jdir["axesLengths"][0], jdir["axesLengths"][1]) ** 2
                    ) / 2 + 0.1:

                        d = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
                        dc0 = (corner[0][0] - x1) * (y2 - y1) - (corner[0][1] - y1) * (
                            x2 - x1
                        )
                        dc1 = (corner[1][0] - x1) * (y2 - y1) - (corner[1][1] - y1) * (
                            x2 - x1
                        )
                        dc2 = (corner[2][0] - x1) * (y2 - y1) - (corner[2][1] - y1) * (
                            x2 - x1
                        )
                        dc3 = (corner[3][0] - x1) * (y2 - y1) - (corner[3][1] - y1) * (
                            x2 - x1
                        )
                        if (
                            d * dl > 0
                            and dc0 * dl > 0
                            and dc1 * dl > 0
                            and dc2 * dl > 0
                            and dc3 * dl > 0
                        ):
                            if abs(dify) < abs(difx):
                                # if self.number_point_inside(self.obb[i],[10,0,0],self.obb[j],[0,0,0],'xy')[0] < 2:
                                if (
                                    self.obb_intersection(
                                        self.xyz_expand_2(self.obb[i], [10, 0, 0]),
                                        self.obb[j],
                                    )
                                    == False
                                ):
                                    Scene_Graph.append((i, j, "on the left"))
                                    tsv_writer.writerow([i, j, "on the left"])
                        if (
                            d * dl < 0
                            and dc0 * dl < 0
                            and dc1 * dl < 0
                            and dc2 * dl < 0
                            and dc3 * dl < 0
                        ):
                            if abs(dify) > abs(difx):
                                # if self.number_point_inside(self.obb[i],[0,10,0],self.obb[j],[0,0,0],'xy')[0] < 2:
                                if (
                                    self.obb_intersection(
                                        self.xyz_expand_2(self.obb[i], [0, 10, 0]),
                                        self.obb[j],
                                    )
                                    == False
                                ):
                                    Scene_Graph.append((i, j, "on the right"))
                                    tsv_writer.writerow([i, j, "on the right"])
                        if abs(dify) < abs(difx):
                            # if self.number_point_inside(self.obb[i],[1,0,0],self.obb[j],[0,0,0],'xy')[0] > 0:
                            if (
                                self.obb_intersection(
                                    self.xyz_expand_2(self.obb[i], [1, 0, 0]),
                                    self.obb[j],
                                )
                                == True
                            ):
                                if (x - x1) ** 2 + (y - y1) ** 2 < (x - x2) ** 2 + (
                                    y - y2
                                ) ** 2:
                                    if (
                                        dc0 * dl > 0
                                        or dc1 * dl > 0
                                        or dc2 * dl > 0
                                        or dc3 * dl > 0
                                    ) and (
                                        dc0 * dl < 0
                                        or dc1 * dl < 0
                                        or dc2 * dl < 0
                                        or dc3 * dl < 0
                                    ):
                                        Scene_Graph.append((i, j, "behind"))
                                        tsv_writer.writerow([i, j, "behind"])
                                if (x - x1) ** 2 + (y - y1) ** 2 > (x - x2) ** 2 + (
                                    y - y2
                                ) ** 2:

                                    if (
                                        dc0 * dl > 0
                                        or dc1 * dl > 0
                                        or dc2 * dl > 0
                                        or dc3 * dl > 0
                                    ) and (
                                        dc0 * dl < 0
                                        or dc1 * dl < 0
                                        or dc2 * dl < 0
                                        or dc3 * dl < 0
                                    ):
                                        Scene_Graph.append((i, j, "in front of"))
                                        tsv_writer.writerow([i, j, "in front of"])
                        elif abs(dify) > abs(difx):
                            # if self.number_point_inside(self.obb[i],[0,1,0],self.obb[j],[0,0,0],'xy')[0] > 0:
                            if (
                                self.obb_intersection(
                                    self.xyz_expand_2(self.obb[i], [0, 1, 0]),
                                    self.obb[j],
                                )
                                == True
                            ):
                                if (x - x1) ** 2 + (y - y1) ** 2 < (x - x2) ** 2 + (
                                    y - y2
                                ) ** 2:

                                    if (
                                        dc0 * dl > 0
                                        or dc1 * dl > 0
                                        or dc2 * dl > 0
                                        or dc3 * dl > 0
                                    ) and (
                                        dc0 * dl < 0
                                        or dc1 * dl < 0
                                        or dc2 * dl < 0
                                        or dc3 * dl < 0
                                    ):
                                        Scene_Graph.append((i, j, "behind"))
                                        tsv_writer.writerow([i, j, "behind"])
                                if (x - x1) ** 2 + (y - y1) ** 2 > (x - x2) ** 2 + (
                                    y - y2
                                ) ** 2:

                                    if (
                                        dc0 * dl > 0
                                        or dc1 * dl > 0
                                        or dc2 * dl > 0
                                        or dc3 * dl > 0
                                    ) and (
                                        dc0 * dl < 0
                                        or dc1 * dl < 0
                                        or dc2 * dl < 0
                                        or dc3 * dl < 0
                                    ):
                                        Scene_Graph.append((i, j, "in front of"))
                                        tsv_writer.writerow([i, j, "in front of"])

                if j != i:
                    ### nodes with same color_list
                    if scene[i]["color"] == scene[j]["color"]:
                        Scene_Graph.append((i, j, "same color"))
                        tsv_writer.writerow([i, j, "same color"])
                    ### lighter/darker
                    if scene[i]["lightness"] > scene[j]["lightness"] + 0.5:
                        Scene_Graph.append((i, j, "lighter"))
                        tsv_writer.writerow([i, j, "lighter"])
                    elif scene[i]["lightness"] < scene[j]["lightness"] - 0.5:
                        Scene_Graph.append((i, j, "darker"))
                        tsv_writer.writerow([i, j, "darker"])
                    ### nodes with same category
                    if scene[i]["category"] == scene[j]["category"]:
                        Scene_Graph.append((i, j, "same category"))
                        tsv_writer.writerow([i, j, "same category"])
                    ### nodes with same object group
                    # if scene[i]["object_group"] == scene[j]["object_group"]:
                    #    Scene_Graph.append((i,j,"same object group"))
                    #    tsv_writer.writerow([i,j,"same object group"])
                    ### nodes with the same size
                    if (
                        abs(
                            abs(
                                self.obb[i]["axesLengths"][0]
                                * self.obb[i]["axesLengths"][1]
                                * self.obb[i]["axesLengths"][2]
                            )
                            - abs(
                                self.obb[j]["axesLengths"][0]
                                * self.obb[j]["axesLengths"][1]
                                * self.obb[j]["axesLengths"][2]
                            )
                        )
                        < 0.1
                        * min(
                            abs(
                                self.obb[i]["axesLengths"][0]
                                * self.obb[i]["axesLengths"][1]
                                * self.obb[i]["axesLengths"][2]
                            ),
                            abs(
                                self.obb[j]["axesLengths"][0]
                                * self.obb[j]["axesLengths"][1]
                                * self.obb[j]["axesLengths"][2]
                            ),
                        )
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "same valume"))
                        tsv_writer.writerow([i, j, "same volume"])
                    ### smaller/larger
                    if (
                        abs(
                            self.obb[i]["axesLengths"][0]
                            * self.obb[i]["axesLengths"][1]
                            * self.obb[i]["axesLengths"][2]
                        )
                        > 2
                        * abs(
                            self.obb[j]["axesLengths"][0]
                            * self.obb[j]["axesLengths"][1]
                            * self.obb[j]["axesLengths"][2]
                        )
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "larger"))
                        tsv_writer.writerow([i, j, "larger"])
                    if (
                        abs(
                            self.obb[i]["axesLengths"][0]
                            * self.obb[i]["axesLengths"][1]
                            * self.obb[i]["axesLengths"][2]
                        )
                        < 0.5
                        * abs(
                            self.obb[j]["axesLengths"][0]
                            * self.obb[j]["axesLengths"][1]
                            * self.obb[j]["axesLengths"][2]
                        )
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "smaller"))
                        tsv_writer.writerow([i, j, "smaller"])
                    ### nodes with the same height
                    if (
                        abs(
                            self.obb[i]["axesLengths"][2]
                            - self.obb[j]["axesLengths"][2]
                        )
                        < 0.1
                        * min(
                            self.obb[i]["axesLengths"][2], self.obb[j]["axesLengths"][2]
                        )
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "same height"))
                        tsv_writer.writerow([i, j, "same height"])
                    ### longer/shorter
                    if (
                        self.obb[i]["axesLengths"][2]
                        > 2 * self.obb[j]["axesLengths"][2]
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "taller"))
                        tsv_writer.writerow([i, j, "taller"])
                    if (
                        self.obb[i]["axesLengths"][2]
                        < 0.5 * self.obb[j]["axesLengths"][2]
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "shorter"))  ### on/under/above
                        tsv_writer.writerow([i, j, "shorter"])

                    ### same width/wider/skinnier
                    if (
                        abs(
                            min(
                                abs(self.obb[i]["axesLengths"][0]),
                                abs(self.obb[i]["axesLengths"][1]),
                            )
                            - min(
                                abs(self.obb[j]["axesLengths"][0]),
                                abs(self.obb[j]["axesLengths"][1]),
                            )
                        )
                        < 0.1
                        * min(
                            min(
                                abs(self.obb[i]["axesLengths"][0]),
                                abs(self.obb[i]["axesLengths"][1]),
                            ),
                            min(
                                abs(self.obb[j]["axesLengths"][0]),
                                abs(self.obb[j]["axesLengths"][1]),
                            ),
                        )
                        and scene[j]["category"] != "wall"
                        and scene[j]["category"] != "floor"
                        and scene[i]["category"] != "wall"
                        and scene[i]["category"] != "floor"
                        and scene[i]["object_group"] != "ceiling"
                        and scene[j]["object_group"] != "ceiling"
                    ):
                        Scene_Graph.append((i, j, "same width"))
                        tsv_writer.writerow([i, j, "same width"])

                    if scene[j]["object_group"] not in [
                        "wall",
                        "floor",
                        "ceiling",
                    ] and scene[i]["object_group"] not in ["wall", "floor", "ceiling"]:
                        if min(
                            abs(self.obb[i]["axesLengths"][0]),
                            abs(self.obb[i]["axesLengths"][1]),
                        ) > 2 * min(
                            abs(self.obb[j]["axesLengths"][0]),
                            abs(self.obb[j]["axesLengths"][1]),
                        ):
                            Scene_Graph.append((i, j, "wider"))
                            tsv_writer.writerow([i, j, "wider"])

                        elif min(
                            abs(self.obb[i]["axesLengths"][0]),
                            abs(self.obb[i]["axesLengths"][1]),
                        ) < 0.5 * min(
                            abs(self.obb[j]["axesLengths"][0]),
                            abs(self.obb[j]["axesLengths"][1]),
                        ):
                            Scene_Graph.append((i, j, "skinnier"))
                            tsv_writer.writerow([i, j, "skinnier"])

                    ### under/above/on/supporting
                    # if abs(scene[i]['minx'])> abs(scene[j]['minx']) and abs(scene[i]['maxx']) < abs(scene[j]['maxx']) and abs(scene[i]['miny'])> abs(scene[j]['miny']) and abs(scene[i]['maxy']) < abs(scene[j]['maxy']) and scene[j]['object_group']!='floor' and scene[i]['object_group']!='floor' and scene[j]['object_group']!='wall' and scene[i]['object_group']!='wall' and scene[i]['object_group']!='ceiling' and scene[j]['object_group']!='ceiling' :

                    # if (abs(scene[i]['minx']) + 0.05> abs(scene[j]['minx']) and abs(scene[i]['maxx'])-0.05 < abs(scene[j]['maxx']) and abs(scene[i]['miny'])+0.05> abs(scene[j]['miny']) and abs(scene[i]['maxy'])-0.05 < abs(scene[j]['maxy'])) or (abs(scene[j]['minx']) + 0.05> abs(scene[i]['minx']) and abs(scene[j]['maxx'])-0.05 < abs(scene[i]['maxx']) and abs(scene[j]['miny'])+0.05> abs(scene[i]['miny']) and abs(scene[j]['maxy'])-0.05 < abs(scene[i]['maxy'])) and(scene[j]['object_group']!='floor' and scene[i]['object_group']!='floor' and scene[j]['object_group']!='wall' and scene[i]['object_group']!='wall'):
                    xyz_exi_nt = self.xyz_expand(self.obb[i], [0.5, 0.5, 0])
                    xyz_exi = self.xyz_expand(self.obb[i], [0.1, 0.1, 0])
                    xyz_exj = self.xyz_expand(self.obb[j], [0.1, 0.1, 0])
                    obbi_xy = [
                        (xyz_exi[0][0], xyz_exi[0][1]),
                        (xyz_exi[1][0], xyz_exi[1][1]),
                        (xyz_exi[2][0], xyz_exi[2][1]),
                        (xyz_exi[3][0], xyz_exi[3][1]),
                    ]

                    obbj_xy = [
                        (xyz_exj[0][0], xyz_exj[0][1]),
                        (xyz_exj[1][0], xyz_exj[1][1]),
                        (xyz_exj[2][0], xyz_exj[2][1]),
                        (xyz_exj[3][0], xyz_exj[3][1]),
                    ]

                    obbi_xz = [
                        (xyz_exi[0][0], xyz_exi[0][2]),
                        (xyz_exi[1][0], xyz_exi[1][2]),
                        (xyz_exi[2][0], xyz_exi[2][2]),
                        (xyz_exi[3][0], xyz_exi[3][2]),
                    ]

                    obbj_xz = [
                        (xyz_exj[0][0], xyz_exj[0][2]),
                        (xyz_exj[1][0], xyz_exj[1][2]),
                        (xyz_exj[2][0], xyz_exj[2][2]),
                        (xyz_exj[3][0], xyz_exj[3][2]),
                    ]

                    obbi_yz = [
                        (xyz_exi[0][1], xyz_exi[0][2]),
                        (xyz_exi[1][1], xyz_exi[1][2]),
                        (xyz_exi[2][1], xyz_exi[2][2]),
                        (xyz_exi[3][1], xyz_exi[3][2]),
                    ]

                    obbj_yz = [
                        (xyz_exj[0][1], xyz_exj[0][2]),
                        (xyz_exj[1][1], xyz_exj[1][2]),
                        (xyz_exj[2][1], xyz_exj[2][2]),
                        (xyz_exj[3][1], xyz_exj[3][2]),
                    ]

                    # if (self.obb_intersection_helper(obbi_xy,self.obb[j]) != self.obb_intersection_helper(self.obb[j],obbi_xy)) or (self.obb_intersection_helper(self.obb[i],obbj_xy) != self.obb_intersection_helper(obbj_xy,self.obb[i])): #get xy
                    if (
                        self.number_point_inside(
                            self.obb[i], [0.05, 0.05, 0], self.obb[j], [0, 0, 0], "xy"
                        )[0]
                        == 4
                        or self.number_point_inside(
                            self.obb[j], [0.05, 0.05, 0], self.obb[i], [0, 0, 0], "xy"
                        )[0]
                        == 4
                    ):

                        # print(i,j)
                        # print(scene[i]['category'], scene[j]['category'])
                        # print(self.obb[j])
                        # print("-------------------------")
                        # print(self.obb[i])
                        # print(self.obb[i]['centroid'][2] , self.obb[j]['centroid'][2])
                        # print(scene[i]['maxz'], scene[i]['minz'],scene[j]['maxz'],scene[j]['minz'])
                        # if (i == 11 and j ==4):
                        #    hi
                        ### light on the ceiling

                        if (
                            self.obb[i]["centroid"][2] < self.obb[j]["centroid"][2]
                            and scene[j]["object_group"] == "ceiling"
                            and (
                                (scene[j]["minz"] - scene[i]["maxz"]) < 0.05
                                and (scene[j]["minz"] - scene[i]["minz"]) > 0.2
                            )
                        ):
                            Scene_Graph.append((i, j, "on_vertical"))
                            tsv_writer.writerow([i, j, "on_vertical"])
                            Scene_Graph.append((j, i, "supporting_vertical"))
                            tsv_writer.writerow([i, j, "supporting_vertical"])

                        #### should I use minz maxz from obbs ??????
                        elif (
                            self.obb[i]["centroid"][2] < self.obb[j]["centroid"][2]
                            and (scene[j]["minz"] - scene[i]["maxz"]) >= 0.05
                            and scene[j]["object_group"] != "ceiling"
                            and scene[j]["object_group"] != "floor"
                        ):
                            Scene_Graph.append((i, j, "under"))
                            tsv_writer.writerow([i, j, "under"])
                            Scene_Graph.append((j, i, "above"))
                            tsv_writer.writerow([j, i, "above"])

                        elif (
                            (self.obb[i]["centroid"][2] < self.obb[j]["centroid"][2])
                            and (scene[j]["minz"] - scene[i]["maxz"]) < 0.05
                            and (scene[j]["minz"] - scene[i]["minz"]) > 0.2
                            and scene[j]["object_group"] != "ceiling"
                            and scene[j]["object_group"] != "floor"
                        ):
                            Scene_Graph.append((i, j, "supporting"))
                            tsv_writer.writerow([i, j, "supporting"])
                            Scene_Graph.append((j, i, "on"))
                            tsv_writer.writerow([j, i, "on"])
                        ### paiting on wall
                    # elif abs(scene[i]['minx'])+0.05 > abs(scene[j]['minx']) and  abs(scene[i]['maxx'])-0.05 < abs(scene[j]['maxx']) and abs(scene[i]['minz']) > abs(scene[j]['minz']) and abs(scene[i]['maxz']) < abs(scene[j]['maxz']):
                    ##elif (self.obb_intersection_helper(obbi_xz,obbj_xz) != self.obb_intersection_helper(obbj_xz,obbi_xz)) or (self.obb_intersection_helper(obbi_xz,obbj_xz) != self.obb_intersection_helper(obbj_xz,obbi_xz)):  #xz plane
                    elif (
                        self.number_point_inside(
                            self.obb[j], [0.05, 0, 0.05], self.obb[i], [0, 0, 0], "xz"
                        )[0]
                        == 4
                        and abs(self.obb[i]["centroid"][1] - self.obb[j]["centroid"][1])
                        < 0.15
                        and scene[j]["object_group"] == "wall"
                        and scene[i]["minz"] > scene[j]["minz"] + 0.1
                    ):

                        Scene_Graph.append((i, j, "on_horizontal"))
                        tsv_writer.writerow([i, j, "on_horizontal"])
                        Scene_Graph.append((j, i, "supporting_horizontal"))
                        tsv_writer.writerow([j, i, "supporting_horizontal"])
                    # elif abs(scene[i]['miny'])+0.05 > abs(scene[j]['miny']) and abs(scene[i]['maxy'])-0.05 < abs(scene[j]['maxy']) and abs(scene[i]['minz'])> abs(scene[j]['minz']) and abs(scene[i]['maxz']) < abs(scene[j]['maxz']):
                    # elif (self.obb_intersection_helper(obbi_yz,obbj_yz) != self.obb_intersection_helper(obbi_yz,obbi_yz)) or (self.obb_intersection_helper(obbi_yz,obbj_yz) != self.obb_intersection_helper(obbj_yz,obbi_yz)):#get yz
                    elif (
                        self.number_point_inside(
                            self.obb[j], [0, 0.05, 0.05], self.obb[i], [0, 0, 0], "yz"
                        )
                        == 4
                        and abs(self.obb[i]["centroid"][0] - self.obb[j]["centroid"][0])
                        < 0.15
                        and scene[j]["object_group"] == "wall"
                        and scene[i]["minz"] > scene[j]["minz"] + 0.1
                    ):

                        Scene_Graph.append((i, j, "on_horizontal"))
                        tsv_writer.writerow([i, j, "on_horizontal"])
                        Scene_Graph.append((j, i, "supporting_horizontal"))
                        tsv_writer.writerow([j, i, "supporting_horizontal"])

                    ### next to

                    elif (
                        scene[i]["object_group"] not in ["floor", "ceiling"]
                        and scene[j]["object_group"] not in ["floor", "ceiling"]
                        and (
                            self.number_point_inside(
                                self.obb[i],
                                [0.25, 0.25, 0],
                                self.obb[j],
                                [0.25, 0.25, 0],
                                "xy",
                            )[0]
                            > 0
                            or self.number_point_inside(
                                self.obb[j],
                                [0.25, 0.25, 0],
                                self.obb[i],
                                [0.25, 0.25, 0],
                                "xy",
                            )[0]
                            > 0
                        )
                    ):
                        # elif scene[i]['object_group'] not in ["wall","floor","ceiling"] and scene[j]['object_group'] not in ["wall","floor","ceiling"] and
                        if (
                            scene[i]["minz"] > scene[j]["minz"]
                            and scene[i]["minz"] < scene[j]["maxz"]
                        ) or (
                            scene[j]["minz"] > scene[i]["minz"]
                            and scene[j]["minz"] < scene[i]["maxz"]
                        ):
                            Scene_Graph.append((i, j, "next to"))
                            tsv_writer.writerow([i, j, "next to"])
                            # print(i,j,"next to")
                            # print(i,category_list[str(category_type[i])],j,category_list[str(category_type[j])],"next to")

        # print(scene[11])
        # print(scene[1])
        for i in scene:
            if (
                scene[i]["object_group"] != "floor"
                and scene[i]["object_group"] != "wall"
                and scene[i]["object_group"] != "ceiling"
            ):

                maxx = scene[i]["maxx"] + (scene[i]["maxx"] - scene[i]["minx"]) * 0.25
                minx = scene[i]["minx"] - (scene[i]["maxx"] - scene[i]["minx"]) * 0.25
                maxy = scene[i]["maxy"] + (scene[i]["maxy"] - scene[i]["miny"]) * 0.25
                miny = scene[i]["miny"] - (scene[i]["maxy"] - scene[i]["miny"]) * 0.25
                xres = (scene[i]["maxx"] - scene[i]["minx"]) * 0.005 * 0
                yres = (scene[i]["maxy"] - scene[i]["miny"]) * 0.005 * 0
                xx = (scene[i]["maxx"] - scene[i]["minx"]) * 0.1
                yy = (scene[i]["maxy"] - scene[i]["miny"]) * 0.1

                for j in scene:
                    if (
                        self.intersection(
                            maxx,
                            scene[i]["maxx"] + xres,
                            scene[i]["maxy"] - yy,
                            scene[i]["miny"] + yy,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        and j != i
                        and (
                            (
                                scene[i]["minz"] > scene[j]["minz"]
                                and scene[i]["minz"] < scene[j]["maxz"]
                            )
                            or (
                                scene[j]["minz"] > scene[i]["minz"]
                                and scene[j]["minz"] < scene[i]["maxz"]
                            )
                        )
                        and scene[j]["object_group"] != "floor"
                        and scene[j]["object_group"] != "ceiling"
                        and self.intersection(
                            scene[i]["minx"],
                            minx,
                            scene[i]["maxy"] - yy,
                            scene[i]["miny"] + yy,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                        and self.intersection(
                            scene[i]["maxx"] - xx,
                            scene[i]["minx"] + xx,
                            scene[i]["miny"],
                            miny,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                        and self.intersection(
                            scene[i]["maxx"] - xx,
                            scene[i]["minx"] + xx,
                            maxy,
                            scene[i]["maxy"],
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                    ):

                        for k in scene:

                            if (
                                self.intersection(
                                    scene[i]["minx"] - xres,
                                    minx,
                                    scene[i]["maxy"] - yy,
                                    scene[i]["miny"] + yy,
                                    scene[k]["maxx"],
                                    scene[k]["minx"],
                                    scene[k]["maxy"],
                                    scene[k]["miny"],
                                )
                                and k != i
                                and k != j
                                and (
                                    (
                                        scene[i]["minz"] > scene[k]["minz"]
                                        and scene[i]["minz"] < scene[k]["maxz"]
                                    )
                                    or (
                                        scene[k]["minz"] > scene[i]["minz"]
                                        and scene[k]["minz"] < scene[i]["maxz"]
                                    )
                                )
                                and scene[k]["object_group"] != "floor"
                                and scene[k]["object_group"] != "ceiling"
                                and self.intersection(
                                    maxx,
                                    scene[i]["maxx"],
                                    scene[i]["maxy"] - yy,
                                    scene[i]["miny"] + yy,
                                    scene[k]["maxx"],
                                    scene[k]["minx"],
                                    scene[k]["maxy"],
                                    scene[k]["miny"],
                                )
                                == False
                                and self.intersection(
                                    scene[i]["maxx"] - xx,
                                    scene[i]["minx"] + xx,
                                    scene[i]["miny"],
                                    miny,
                                    scene[k]["maxx"],
                                    scene[k]["minx"],
                                    scene[k]["maxy"],
                                    scene[k]["miny"],
                                )
                                == False
                                and self.intersection(
                                    scene[i]["maxx"] - xx,
                                    scene[i]["minx"] + xx,
                                    maxy,
                                    scene[i]["maxy"],
                                    scene[k]["maxx"],
                                    scene[k]["minx"],
                                    scene[k]["maxy"],
                                    scene[k]["miny"],
                                )
                                == False
                            ):

                                Scene_Graph.append((i, j, k, "between_x"))
                                tsv_writer.writerow([i, j, k, "between_x"])
                                # print([i['label'],str(j['label']) + " and " + str(k['label']),"1.between"])

                    if (
                        self.intersection(
                            scene[i]["maxx"] - xx,
                            scene[i]["minx"] + xx,
                            maxy,
                            scene[i]["maxy"] + yres,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        and j != i
                        and (
                            (
                                scene[i]["minz"] > scene[j]["minz"]
                                and scene[i]["minz"] < scene[j]["maxz"]
                            )
                            or (
                                scene[j]["minz"] > scene[i]["minz"]
                                and scene[j]["minz"] < scene[i]["maxz"]
                            )
                        )
                        and scene[j]["object_group"] != "floor"
                        and scene[j]["object_group"] != "ceiling"
                        and self.intersection(
                            scene[i]["maxx"] - xx,
                            scene[i]["minx"] + xx,
                            scene[i]["miny"],
                            miny,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                        and self.intersection(
                            scene[i]["minx"],
                            minx,
                            scene[i]["maxy"] - yy,
                            scene[i]["miny"] + yy,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                        and self.intersection(
                            maxx,
                            scene[i]["maxx"],
                            scene[i]["maxy"] - yy,
                            scene[i]["miny"] + yy,
                            scene[j]["maxx"],
                            scene[j]["minx"],
                            scene[j]["maxy"],
                            scene[j]["miny"],
                        )
                        == False
                    ):
                        # if i == 11: print(j)
                        for kk in scene:
                            if (
                                self.intersection(
                                    scene[i]["maxx"] - xx,
                                    scene[i]["minx"] + xx,
                                    scene[i]["miny"] - yres,
                                    miny,
                                    scene[kk]["maxx"],
                                    scene[kk]["minx"],
                                    scene[kk]["maxy"],
                                    scene[kk]["miny"],
                                )
                                and kk != i
                                and kk != j
                                and (
                                    (
                                        scene[i]["minz"] > scene[kk]["minz"]
                                        and scene[i]["minz"] < scene[kk]["maxz"]
                                    )
                                    or (
                                        scene[kk]["minz"] > scene[i]["minz"]
                                        and scene[kk]["minz"] < scene[i]["maxz"]
                                    )
                                )
                                and scene[kk]["object_group"] != "floor"
                                and scene[kk]["object_group"] != "ceiling"
                                and self.intersection(
                                    scene[i]["maxx"] - xx,
                                    scene[i]["minx"] + xx,
                                    maxy,
                                    scene[i]["maxy"],
                                    scene[kk]["maxx"],
                                    scene[kk]["minx"],
                                    scene[kk]["maxy"],
                                    scene[kk]["miny"],
                                )
                                == False
                                and self.intersection(
                                    scene[i]["minx"],
                                    minx,
                                    scene[i]["maxy"] - yy,
                                    scene[i]["miny"] + yy,
                                    scene[kk]["maxx"],
                                    scene[kk]["minx"],
                                    scene[kk]["maxy"],
                                    scene[kk]["miny"],
                                )
                                == False
                                and self.intersection(
                                    maxx,
                                    scene[i]["maxx"],
                                    scene[i]["maxy"] - yy,
                                    scene[i]["miny"] + yy,
                                    scene[kk]["maxx"],
                                    scene[kk]["minx"],
                                    scene[kk]["maxy"],
                                    scene[kk]["miny"],
                                )
                                == False
                            ):

                                Scene_Graph.append((i, j, kk, "between_y"))
                                tsv_writer.writerow([i, j, kk, "between_y"])

                                # print([i['label'],str(j['label']) + " and " + str(kk['label']),"2.between"])

        """


        for i in scene:
            dict_i = {'xl':[] , 'xr':[] , 'yu' :[] , 'yd' :[]}
            if scene[i]['category'] != 'floor' and scene[i]['category'] != 'wall' and scene[i]['category']!='ceiling':
                for j in scene:
                    Flag = True
                    if j != i and (i,j,"on") not in Scene_Graph and (i,j,"under") not in Scene_Graph and (i,j,"above") not in Scene_Graph and (i,j,"supporting") not in Scene_Graph :
                        #if self.obb_intersection_helper(self.obb[i],self.obb[j]) != self.obb_intersection_helper(self.obb[j],self.obb[i]): pass
                        if self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 4 or self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 4 : pass
                        elif self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 1 and self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 1: pass
                        #elif self.obb_intersection_helper(self.obb[i],self.obb[j]) and self.number_point_inside(self.obb[i],self.obb[j])[0] == 0 and self.number_point_inside(self.obb[j],self.obb[i])[0] == 0: pass 
                        elif self.obb_intersection(self.obb[i],self.obb[j]) and self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 0 and self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 0: pass

                        elif self.obb_intersection(self.obb[i],self.obb[j]) == False and self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 0 and self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 0:
                            xyz_xi = self.xyz_expand(self.obb[i],[0.5,0,0])
                            obbi_x = ((xyz_xi[0][0],xyz_xi[0][1]) , (xyz_xi[1][0],xyz_xi[1][1]) , (xyz_xi[2][0],xyz_xi[2][1]) , (xyz_xi[3][0],xyz_xi[3][1]))
                            xyz_yi = self.xyz_expand(self.obb[i],[0,0.5,0])
                            obbi_y = ((xyz_yi[0][0],xyz_yi[0][1]) , (xyz_yi[1][0],xyz_yi[1][1]) , (xyz_yi[2][0],xyz_yi[2][1]) , (xyz_yi[3][0],xyz_yi[3][1]))
                            if self.obb_intersection(obbi_x,self.obb[j]) and self.obb_intersection(obbi_y,self.obb[j]) == False:                        
                                rot = np.array(self.obb[i]['normalizedAxes']).reshape(3,3).transpose()
                                c_i = np.linalg.inv(rot).dot(np.array(self.obb[i]['centroid']))
                                c_j = np.linalg.inv(rot).dot(np.array(self.obb[j]['centroid']))
                                if c_j[0] > c_i[0]: dict_i['xr'].append(j)
                                elif c_j[0] < c_i[0]: dict_i['xl'].append(j)
                            elif self.obb_intersection(obbi_y,self.obb[j]) and self.obb_intersection(obbi_x,self.obb[j]) == False:
                                rot = np.array(self.obb[i]['normalizedAxes']).reshape(3,3).transpose()
                                c_i = np.linalg.inv(rot).dot(np.array(self.obb[i]['centroid']))
                                c_j = np.linalg.inv(rot).dot(np.array(self.obb[j]['centroid']))
                                if c_j[1] > c_i[1]: dict_i['yu'].append(j)
                                elif c_j[1] < c_i[1]: dict_i['yd'].append(j)

                        elif self.obb_intersection_helper(self.obb[i],self.obb[j]) and ((self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 2 and self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 0) or (self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 0 and self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 2)):

                            if self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] == 2:
                                if (self.obb[i]['centroid'][0],self.obb[i]['centroid'][1]) != map(lambda x: x/2.0, tuple(map(operator.add, self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[1][0], self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[1][1]))): Flag = False
                            if self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] == 2:
                                          
                                if (self.obb[j]['centroid'][0],self.obb[j]['centroid'][1]) != map(lambda x: x/2.0, tuple(map(operator.add, self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[1][0], self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[1][1]))): Flag = False
                                  
                        elif self.obb_intersection_helper(self.obb[i],self.obb[j]) and self.number_point_inside(self.obb[i],[0,0,0],self.obb[j],[0,0,0],'xy')[0] != self.number_point_inside(self.obb[j],[0,0,0],self.obb[i],[0,0,0],'xy')[0] and Flag:
                            rot = np.array(self.obb[i]['normalizedAxes']).reshape(3,3).transpose()
                            c_i = np.linalg.inv(rot).dot(np.array(self.obb[i]['centroid']))
                            c_j = np.linalg.inv(rot).dot(np.array(self.obb[j]['centroid']))
                            deg = math.degrees(math.atan((c_j[1]-c_i[1]) / (c_j[0] - c_i[0])))
                            if  deg < 45 or deg >315 : dict_i['xr'].append(j)
                            elif deg > 45 and deg< 135 : dict_i['yu'].append(j)
                            elif deg > 135 and deg < 225: dict_i['xl'].append(j) 
                            elif deg > 225 and deg < 315: dict_i['yd'].append(j) 
                            

            for t_xl in dict_i['xl']:
                for t_xr in dict_i['xr']:
                    Scene_Graph.append((str(i),str(t_xl) + " and " + str(t_xr),"between"))
                    tsv_writer.writerow([scene[i]['category'],str(scene[t_xl]['category']) + " and " + str(scene[t_xr]['category']),"between"])

            for t_yu in dict_i['yu']:
                for t_yd in dict_i['yd']:
                    Scene_Graph.append((str(i),str(t_yu) + " and " + str(t_yd),"between"))
                    tsv_writer.writerow([scene[i]['category'],str(scene[t_yu]['category']) + " and " + str(scene[t_yd]['category']),"between"])
"""


"""
        for i in scene:
            if scene[i]['category'] != 'floor' and scene[i]['category'] != 'wall' and scene[i]['category']!='ceiling':
                xyz_xi = self.xyz_expand(self.obb[i],[0.5,0,0])
                obbi_x = ((xyz_xi[0][0],xyz_xi[0][1]) , (xyz_xi[1][0],xyz_xi[1][1]) , (xyz_xi[2][0],xyz_xi[2][1]) , (xyz_xi[3][0],xyz_xi[3][1]))
                xyz_yi = self.xyz_expand(self.obb[i],[0,0.5,0]) 
                obbi_y = ((xyz_yi[0][0],xyz_yi[0][1]) , (xyz_yi[1][0],xyz_yi[1][1]) , (xyz_yi[2][0],xyz_yi[2][1]) , (xyz_yi[3][0],xyz_yi[3][1]))
                for j in scene:
                    xyz_j = self.xyz_expand(self.obb[j],[-0.2,-0.2,0]) 
                    
                    obbj_xy = ((xyz_j[0][0],xyz_j[0][1]) , (xyz_j[1][0],xyz_j[1][1]) , (xyz_j[2][0],xyz_j[2][1]) , (xyz_j[3][0],xyz_j[3][1]))
                    if self.obb_intersection(obbi_x,obbj_xy) and self.obb_intersection_helper(obbi_x,obbj_xy) == self.obb_intersection_helper(obbj_xy,obbi_x) and self.obb_intersection(obbi_y,obbj_xy) == False and j != i and (scene[j]["minz"] < scene[i]["maxz"] and scene[j]["maxz"] > scene[i]["minz"]  ) and scene[j]['category'] !='floor' and scene[j]['category'] !='ceiling': 

                        for k in scene:
                            xyz_k = self.xyz_expand(self.obb[k],[-0.2,-0.2,0])
                            obbk_xy = ((xyz_k[0][0],xyz_k[0][1]) , (xyz_k[1][0],xyz_k[1][1]) , (xyz_k[2][0],xyz_k[2][1]) , (xyz_k[3][0],xyz_k[3][1]))
                            if ((self.obb[k]['centroid'][0] - self.obb[j]['centroid'][0])**2 + (self.obb[k]['centroid'][1] - self.obb[j]['centroid'][1])**2) > ((self.obb[k]['centroid'][0] - self.obb[i]['centroid'][0])**2 + (self.obb[k]['centroid'][1] - self.obb[i]['centroid'][1])**2) and self.obb_intersection(obbi_x,obbk_xy) and self.obb_intersection_helper(obbi_x,obbk_xy) == self.obb_intersection_helper(obbk_xy,obbi_x) and self.obb_intersection(obbi_y,obbk_xy) == False and  k != i and k != j  and (scene[k]["minz"] < scene[i]["maxz"] and scene[k]["maxz"] > scene[i]["minz"] ) and str(scene[k]['category'])!='floor' and str(scene[k]['category'])!='ceiling' :

                                Scene_Graph.append((str(i),str(j) + " and " + str(k),"between"))
                                tsv_writer.writerow([scene[i]['category'],str(scene[j]['category']) + " and " + str(scene[k]['category']),"1.between"])
         
                    if self.obb_intersection(obbi_y,obbj_xy) and self.obb_intersection_helper(obbi_y,obbj_xy) == self.obb_intersection_helper(obbj_xy,obbi_y) and self.obb_intersection(obbi_x,obbj_xy) == False and j != i and (scene[j]["minz"] < scene[i]["maxz"] and scene[j]["maxz"] > scene[i]["minz"]  ) and scene[j]['category'] !='floor' and scene[j]['category'] !='ceiling':           

                        for kk in scene:
                            xyz_kk = self.xyz_expand(self.obb[kk],[-0.2,-0.2,0])
                            obbkk_xy = ((xyz_kk[0][0],xyz_kk[0][1]) , (xyz_kk[1][0],xyz_kk[1][1]) , (xyz_kk[2][0],xyz_kk[2][1]) , (xyz_kk[3][0],xyz_kk[3][1]))
                            if ((self.obb[kk]['centroid'][0] - self.obb[j]['centroid'][0])**2 + (self.obb[kk]['centroid'][1] -self.obb[j]['centroid'][1])**2) > ((self.obb[kk]['centroid'][0] - self.obb[i]['centroid'][0])**2 + (self.obb[kk]['centroid'][1] - self.obb[i]['centroid'][1])**2) and self.obb_intersection(obbi_y,obbkk_xy) and self.obb_intersection_helper(obbi_y,obbkk_xy) == self.obb_intersection_helper(obbkk_xy,obbi_y) and self.obb_intersection(obbi_x,obbj_xy) == False and kk!=i and kk!=j and (scene[kk]["minz"] < scene[i]["maxz"] and scene[kk]["maxz"] > scene[i]["minz"] ) and scene[kk]['category']!='floor' and scene[kk]['category']!='ceiling':

                                Scene_Graph.append((str(i),str(j) + " and " + str(kk),"between"))
                                tsv_writer.writerow([i,scene[i]['category'],j,kk,str(scene[j]['category']) + " and " + str(scene[kk]['category']),"2.between"])
                                if scene[i]['category'] == 'bench' and str(scene[j]['category']) == 'wall' and str(scene[kk]['category']) == 'chair':
                                    print(scene[i]['maxx'],scene[i]['minx'],scene[i]['maxy'],scene[i]['miny'],scene[kk]['maxx'],scene[kk]['minx'],scene[kk]['maxy'],scene[kk]['miny'])        

"""


def scene_graph(
    path_to_ply,
    theDict,
    category_list,
    height_thresholds,
    width_thresholds,
    vol_thresholds,
    obbs,
    filename,
    dr,
):
    classes = []
    graph_class = sceneGraph(
        path_to_ply,
        theDict,
        category_list,
        height_thresholds,
        width_thresholds,
        vol_thresholds,
        obbs,
        filename,
        dr,
        classes,
    )
    (
        color_dict,
        light_dict,
        category_type,
        objectID_type,
    ) = graph_class.points_color_light()
    max_color = graph_class.find_dominant_color(color_dict)
    max_light = graph_class.find_dominant_light(light_dict)
    position = graph_class.points_position()
    scene = graph_class.find_atributes(
        position,
        color_dict,
        light_dict,
        category_type,
        objectID_type,
        max_color,
        max_light,
    )
    graph_class.create_scene_graph(scene)


if __name__ == "__main__":
    path_to_ply = "/datasets/released/scannet/public/v2/scans_extra/annotated/scene0358_00/scene0358_00.annotated.ply"
    with open("./scene_graph_info.json") as f:
        data = json.load(f)
        theDict = data["theDict"]
        category_list = data["category_list"]
        height_thresholds = data["height_thresholds"]
        width_thresholds = data["width_thresholds"]
        vol_thresholds = data["vol_thresholds"]
    scene_graph(
        path_to_ply,
        theDict,
        category_list,
        height_thresholds,
        width_thresholds,
        vol_thresholds,
        "scene0358_00",
    )

