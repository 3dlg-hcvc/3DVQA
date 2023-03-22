from plyfile import PlyData, PlyElement
from config import config
from constant import constant


def color_load_data():
    args = config()
    classes = []
    rgb_cube_path = args.satfaces
    main_survey_path = args.mainsurvey
    main_color_names_map = {}
    main_color_names = constant.main_color_names
    for i in main_color_names:
        main_color_names_map[i] = i
        classes.append(i)
        if main_color_names[i] != None:
            for j in main_color_names[i]:
                main_color_names_map[j] = i

    with open(rgb_cube_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        l = line.split("]")
        ll = l[0][1:].split(",")
        rgb = (int(ll[0]), int(ll[1]), int(ll[2]))
        color_name = str(l[1][0:-1])
        color_name = " ".join(color_name.split())
        RGBs.append(rgb)
        labels.append(main_color_names_map[color_name])

        if color_name in main_color_names_map:
            color_look_up[rgb] = main_color_names_map[color_name]

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
        # if c2 not in color_names:
        #    color_names.append(c2)
        if c2 not in main_color_names_map:
            main_color_names_map[c2] = c1

    unidentified_names = 0
    for j in second:
        bg = 0
        sp = j.split(",")
        col = sp[-1][1:-4]
        if sp[-2].isnumeric() and sp[-3].isnumeric() and sp[-4].isnumeric():
            rgb = (int(sp[-4]), int(sp[-3]), int(sp[-2]))
            if col in main_color_names_map:

                RGBs.append(rgb)
                labels.append(main_color_names_map[col])
            else:

                for lol in col.split():
                    if lol in main_color_names_map:
                        tn = lol
                        bg += 1

                if bg == 1:
                    RGBs.append(rgb)
                    labels.append(main_color_names_map[tn])
                else:
                    unidentified_names += 1
            if col in main_color_names_map:
                color_look_up[rgb] = main_color_names_map[col]

    hist = {}
    for i in classes:
        hist[i] = 0
    for i in labels:
        hist[i] += 1
    max_s = 0
    for i in hist:
        if max_s < hist[i]:
            max_s = hist[i]
    for i in hist:
        hist[i] = max_s / hist[i]

    weights = []
    for i in hist:
        weights.append(hist[i])

    return classes, RGBs, labels, weights


if __name__ == "__main__":
    max_s = 0
    q_all = 0

    classes, RGBs, labels, w = color_load_data()

    hist = {i: 0 for i in classes}

    for i in labels:
        hist[i] += 1

    for i in hist:
        q_all += hist[i]
        if max_s < hist[i]:
            max_s = hist[i]

    perc = dict(hist)
    for i in hist:
        hist[i] = max_s / hist[i]

    for i in perc:
        perc[i] = perc[i] / q_all

    weights = []
    for i in hist:
        weights.append(hist[i])
