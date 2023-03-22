import csv
import random
from constant import constant

class find_answer:
    def __init__(
        self,
        obj1,
        atr1,
        obj2,
        atr2,
        relation,
        repeat_obj,
        repeat_atr_obj,
        file,
        filename,
        synonyms,
        plural,
    ):
        self.plural = plural
        self.l1 = self.object_finder_category(obj1, atr1, filename)
        self.l2 = self.object_relation_finder_category(obj2, atr2, relation, filename)
        self.relation = relation
        self.between = True
        self.filename = filename
        self.obj2 = obj2
        self.atr2 = atr2
        self.obj1 = obj1
        self.atr1 = atr1
        self.repeat_obj = repeat_obj
        self.repeat_atr_obj = repeat_atr_obj
        self.synonyms = synonyms
        self.opdict = constant.oposite_dict  
    def object_finder_category(self,obj, atr,filename):
        l1 = []

        with open("atr" + filename + ".tsv", "r") as ttsvin:
            # with open("atr.tsv", "r") as ttsvin:
            atr_out = csv.reader(ttsvin, delimiter="\t")
            if atr == None and obj != "thing":
                for i in atr_out:
                    if i[1] == obj:
                        l1.append(i[0])
            elif atr != None and obj != "thing":
                for i in atr_out:
                    if i[1] == obj and (atr in i):
                        l1.append(i[0])
            if atr != None and obj == "thing":
                for i in atr_out:
                    if atr in i:
                        l1.append(i[0])
        return l1

    def object_relation_finder_category(self, obj, atr, relation, filename):

        list3 = []
        l1 = self.object_finder_category(obj, atr, filename)
        if relation == None or obj == None:
            return list3
        elif len(l1) == 1:
            with open("Scene_Graph" + filename + ".tsv", "r") as tsvin:
                ID = csv.reader(tsvin, delimiter="\t")
                for i in ID:
                    if i[1] == l1[0] and i[2] == relation:
                        list3.append(i[0])
            return list3
        else:
            return "ambigious_question"

    def get_all_attributes(self, obj_id, filename):

        with open("atr" + filename + ".tsv", "r") as ttsvin:
            atr_out = csv.reader(ttsvin, delimiter="\t")
            for i in atr_out:
                if i[0] == obj_id:
                    return i

    def counting(self, filename):
        id_list = []
        if self.relation == None:
            return len(self.l1), self.l1
        elif self.l2 != "ambigious_question":
            count = 0
            if self.l1 == self.object_finder_category(self.obj2, self.atr2, filename):
                return "error: same objects", []
            for i in self.l1:
                if i in self.l2:
                    id_list.append(i)
                # count+=1
            return len(id_list), id_list
        else:
            return "error: ambigious_question", []

    def query_atr(self, query, filename):
        if query == "color":
            pos = 12
        if query == "height":
            pos = 14
        if query == "size":
            pos = 15
        if len(self.l1) == 0:
            return "error: no such an object", []
        if self.relation == None:
            list1 = self.l1
        elif self.l2 != "ambigious_question":
            list1 = []
            if self.l1 == self.object_finder_category(self.obj2, self.atr2, filename):
                return "error: same_objects", []
            for i in self.l1:
                if i in self.l2:
                    list1.append(i)
        else:
            return "error: ambigious_question", []
        if len(list1) == 1:
            return self.get_all_attributes(list1[0], filename)[pos], list1
        else:
            return "error : no such such an object/or more than one", []

    def location(self, filename):
        anss = []
        list1 = []
        ans = ""
        if len(self.l1) == 0:
            return "error: no such an object", []
        else:
            if self.relation == None:
                list1 = self.l1
            else:
                if self.l2 == "ambigious_question":
                    return "error: ambigious_question", []
                list1 = []
                if self.l1 == self.object_finder_category(
                    self.obj2, self.atr2, filename
                ):
                    return "error: same_objects", []
                for i in self.l1:
                    if i in self.l2:
                        list1.append(i)
            if len(list1) == 1:
                with open("Scene_Graph" + filename + ".tsv", "r") as tsvin:
                    # with open ("Scene_Graph.tsv" , 'r') as tsvin:
                    ID = csv.reader(tsvin, delimiter="\t")
                    for i in ID:
                        ans = ""
                        if str(i[0]) == str(list1[0]) and (
                            str(i[2]) == "on"
                            or str(i[2]) == "under"
                            or str(i[2]) == "above"
                            or str(i[2]) == "supporting"
                            or str(i[2]) == "next to"
                            or str(i[2])
                            in [
                                "on_vertical",
                                "supporting_vertical",
                                "on_horizontal",
                                "supporting_horizontal",
                            ]
                        ):
                            atr_l = self.get_all_attributes(i[1], filename)
                            if str(i[2]) in [
                                "supporting_vertical",
                                "supporting_horizontal",
                            ]:
                                i[2] = "supporting"
                            if str(i[2]) in ["on_vertical", "on_horizontal"]:
                                i[2] = "on"

                            if self.repeat_obj[atr_l[1]] == 1:
                                ans = str(i[2]) + " the " + atr_l[1]
                            elif self.repeat_atr_obj[(atr_l[12], atr_l[1])] == 1:
                                ans = str(i[2]) + " the " + atr_l[12] + " " + atr_l[1]
                            elif (
                                self.repeat_atr_obj[(atr_l[14], atr_l[1])] == 1
                                and atr_l[14] != "medium"
                            ):
                                ans = str(i[2]) + " the " + atr_l[14] + " " + atr_l[1]
                            elif (
                                self.repeat_atr_obj[(atr_l[15], atr_l[1])] == 1
                                and atr_l[15] != "medium"
                            ):
                                ans = str(i[2]) + " the " + atr_l[15] + " " + atr_l[1]
                            elif (
                                self.repeat_atr_obj[(atr_l[14], atr_l[12], atr_l[1])]
                                == 1
                                and atr_l[14] != "medium"
                            ):
                                ans = (
                                    str(i[2])
                                    + " the "
                                    + atr_l[14]
                                    + " "
                                    + atr_l[12]
                                    + " "
                                    + atr_l[1]
                                )
                            elif (
                                self.repeat_atr_obj[(atr_l[15], atr_l[12], atr_l[1])]
                                == 1
                                and atr_l[15] != "medium"
                            ):
                                ans = (
                                    str(i[2])
                                    + " the "
                                    + atr_l[15]
                                    + " "
                                    + atr_l[12]
                                    + " "
                                    + atr_l[1]
                                )
                            elif (
                                self.repeat_atr_obj[(atr_l[15], atr_l[14], atr_l[1])]
                                == 1
                                and atr_l[15] != "medium"
                                and atr_l[14] != "medium"
                            ):
                                ans = (
                                    str(i[2])
                                    + " the "
                                    + atr_l[15]
                                    + " "
                                    + atr_l[14]
                                    + " "
                                    + atr_l[1]
                                )
                            elif (
                                self.repeat_atr_obj[
                                    (atr_l[15], atr_l[14], atr_l[12], atr_l[1])
                                ]
                                == 1
                                and atr_l[15] != "medium"
                                and atr_l[14] != "medium"
                            ):
                                ans = (
                                    str(i[2])
                                    + " the "
                                    + atr_l[15]
                                    + " "
                                    + atr_l[14]
                                    + " "
                                    + atr_l[12]
                                    + " "
                                    + atr_l[1]
                                )
                        elif self.between:

                            ans12 = []
                            if (
                                len(i) == 4
                                and str(i[0]) == str(list1[0])
                                and (
                                    str(i[3]) == "between_x" or str(i[3]) == "between_y"
                                )
                            ):
                                atr_l1 = self.get_all_attributes(i[1], filename)
                                atr_l2 = self.get_all_attributes(i[2], filename)

                                if (
                                    atr_l1[1] == atr_l2[1]
                                    and self.repeat_obj[atr_l1[1]] == 2
                                ):
                                    ans = "between " + self.plural[atr_l1[1]]
                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[12] == atr_l2[12]
                                    and self.repeat_atr_obj[(atr_l1[12], atr_l1[1])]
                                    == 2
                                ):
                                    ans = (
                                        "between "
                                        + atr_l1[12]
                                        + " "
                                        + self.plural[atr_l1[1]]
                                    )
                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[14] == atr_l2[14]
                                    and self.repeat_atr_obj[(atr_l1[14], atr_l1[1])]
                                    == 2
                                ):
                                    if atr_l1[14] != "medium":
                                        ans = (
                                            "between "
                                            + atr_l1[14]
                                            + " "
                                            + self.plural[atr_l1[1]]
                                        )

                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[15] == atr_l2[15]
                                    and self.repeat_atr_obj[(atr_l1[15], atr_l1[1])]
                                    == 2
                                ):
                                    if atr_l1[15] != "medium":
                                        ans = (
                                            "between "
                                            + atr_l1[15]
                                            + " "
                                            + self.plural[atr_l1[1]]
                                        )

                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[12] == atr_l2[12]
                                    and atr_l1[14] == atr_l2[14]
                                    and self.repeat_atr_obj[
                                        (atr_l1[14], atr_l1[12], atr_l1[1])
                                    ]
                                    == 2
                                    and atr_l1[14] != "medium"
                                ):
                                    ans = (
                                        "between "
                                        + atr_l1[14]
                                        + " "
                                        + atr_l1[12]
                                        + " "
                                        + self.plural[atr_l1[1]]
                                    )

                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[12] == atr_l2[12]
                                    and atr_l1[15] == atr_l2[15]
                                    and self.repeat_atr_obj[
                                        (atr_l1[15], atr_l1[12], atr_l1[1])
                                    ]
                                    == 2
                                    and atr_l1[15] != "medium"
                                ):
                                    ans = (
                                        "between "
                                        + atr_l1[15]
                                        + " "
                                        + atr_l1[12]
                                        + " "
                                        + self.plural[atr_l1[1]]
                                    )

                                elif (
                                    atr_l1[1] == atr_l2[1]
                                    and atr_l1[12] == atr_l2[12]
                                    and atr_l1[14] == atr_l2[14]
                                    and atr_l1[15] == atr_l2[15]
                                    and self.repeat_atr_obj[
                                        (atr_l1[15], atr_l1[14], atr_l1[12], atr_l1[1])
                                    ]
                                    == 2
                                    and atr_l1[14] != "medium"
                                    and atr_l1[15] != "medium"
                                ):
                                    ans = (
                                        "between "
                                        + atr_l1[15]
                                        + " "
                                        + atr_l1[14]
                                        + " "
                                        + atr_l1[12]
                                        + " "
                                        + self.plural[atr_l1[1]]
                                    )

                                else:
                                    for j in [i[1], i[2]]:
                                        ans1 = ""
                                        atr_l = self.get_all_attributes(j, filename)
                                        if self.repeat_obj[atr_l[1]] == 1:
                                            ans1 = atr_l[1]
                                        elif (
                                            self.repeat_atr_obj[(atr_l[12], atr_l[1])]
                                            == 1
                                        ):
                                            ans1 = atr_l[12] + " " + atr_l[1]
                                        elif (
                                            self.repeat_atr_obj[(atr_l[14], atr_l[1])]
                                            == 1
                                            and atr_l[14] != "medium"
                                        ):
                                            ans1 = atr_l[14] + " " + atr_l[1]
                                        elif (
                                            self.repeat_atr_obj[(atr_l[15], atr_l[1])]
                                            == 1
                                            and atr_l[15] != "medium"
                                        ):
                                            ans1 = atr_l[15] + " " + atr_l[1]
                                        elif (
                                            self.repeat_atr_obj[
                                                (atr_l[14], atr_l[12], atr_l[1])
                                            ]
                                            == 1
                                            and atr_l[14] != "medium"
                                        ):
                                            ans1 = (
                                                atr_l[14]
                                                + " "
                                                + atr_l[12]
                                                + " "
                                                + atr_l[1]
                                            )
                                        elif (
                                            self.repeat_atr_obj[
                                                (atr_l[15], atr_l[12], atr_l[1])
                                            ]
                                            == 1
                                            and atr_l[15] != "medium"
                                        ):
                                            ans1 = (
                                                atr_l[15]
                                                + " "
                                                + atr_l[12]
                                                + " "
                                                + atr_l[1]
                                            )
                                        elif (
                                            self.repeat_atr_obj[
                                                (atr_l[15], atr_l[14], atr_l[1])
                                            ]
                                            == 1
                                            and atr_l[15] != "medium"
                                            and atr_l[14] != "medium"
                                        ):
                                            ans1 = (
                                                atr_l[15]
                                                + " "
                                                + atr_l[14]
                                                + " "
                                                + atr_l[1]
                                            )
                                        elif (
                                            self.repeat_atr_obj[
                                                (
                                                    atr_l[15],
                                                    atr_l[14],
                                                    atr_l[12],
                                                    atr_l[1],
                                                )
                                            ]
                                            == 1
                                            and atr_l[15] != "medium"
                                            and atr_l[14] != "medium"
                                        ):
                                            ans1 = (
                                                atr_l[15]
                                                + " "
                                                + atr_l[14]
                                                + " "
                                                + atr_l[12]
                                                + " "
                                                + atr_l[1]
                                            )

                                        ans12.append(ans1)

                                    if ans12[0] != ans12[1]:
                                        if ans12[0] != "" and ans12[1] != "":
                                            ans = random.choice(
                                                [
                                                    "between the "
                                                    + ans12[0]
                                                    + " and "
                                                    + ans12[1],
                                                    "between the "
                                                    + ans12[1]
                                                    + " and "
                                                    + ans12[0],
                                                ]
                                            )

                        if ans not in anss and ans != "":
                            anss.append(ans)
                            if atr_l[1] in self.synonyms:
                                for sn in self.synonyms[atr_l[1]]:
                                    if ans.replace(atr_l[1], sn) not in anss:
                                        anss.append(ans.replace(atr_l[1], sn))
                                if len(i) == 4:
                                    xx = self.get_all_attributes(i[1], filename)
                                    if xx[1] in self.synonyms:
                                        for sn in self.synonyms[xx[1]]:
                                            if ans.replace(xx[1], sn) not in anss:
                                                anss.append(ans.replace(xx[1], sn))
                                    if (
                                        atr_l[1] in self.synonyms
                                        and xx[1] in self.synonyms
                                    ):
                                        for sn1 in self.synonyms[xx[1]]:
                                            for sn2 in self.synonyms[atr_l[1]]:
                                                if (
                                                    ans.replace(xx[1], sn1).replace(
                                                        atr_l[1], sn2
                                                    )
                                                    not in anss
                                                ):
                                                    anss.append(
                                                        ans.replace(xx[1], sn1).replace(
                                                            atr_l[1], sn2
                                                        )
                                                    )

            else:
                return "error : no such such an object/or more than one", []
            if len(anss) == 0:
                return "error : cannot address base on a unique object", []
            return anss, list1

    def existance(self, filename):
        if self.relation == None:
            list1 = self.l1
        else:
            if self.l2 == "ambigious_question":
                return "error: ambigious_question", []
            list1 = []
            if self.l1 == self.object_finder_category(self.obj2, self.atr2, filename):
                return "error: same_object", []
            for i in self.l1:
                if i in self.l2:  list1.append(i)
        if len(list1) > 0: return "yes", list1
        elif self.relation in constant.er_relations:
            for j in self.opdict[self.relation]:
                ll2 = self.object_relation_finder_category(
                    self.obj2, self.atr2, j, filename
                )
                for i in self.l1:
                    if i in ll2:
                        return "no", []
            return "error: not clear", []
        else:
            return "no", []

    def integer_comparison(self, filename):
        list2 = self.object_finder_category(self.obj2, self.atr2, filename)
        if list2 == self.l1:
            return "error: same objects", [], []
        if len(self.l1) > len(list2):
            return "more", self.l1, list2
        elif len(self.l1) == len(list2):
            return "equal", self.l1, list2
        else:
            return "less", self.l1, list2

    def compare_atr(self, filename):

        list2 = self.object_finder_category(self.obj2, self.atr2, filename)
        if self.l1 == list2:
            return "error: same objects", [], []
        if len(self.l1) == 1 and len(list2) == 1:
            if self.l1[0] != list2[0]:
                with open("Scene_Graph" + filename + ".tsv", "r") as tsvin:
                    ID = csv.reader(tsvin, delimiter="\t")
                    for i in ID:
                        if i[0] == self.l1[0] and i[1] == list2[0] and i[2]==self.relation: return "yes",self.l1,list2
            else: return "error: two same things", [], []
        else: return "error: not two specific objects",[], []
        if self.relation in self.er_relations:
            for j in self.opdict[self.relation]:
                with open("Scene_Graph" + filename + ".tsv", "r") as tsvin:
                    ID = csv.reader(tsvin, delimiter="\t")
                    for i in ID:
                        if i[0] == self.l1[0] and i[1] == list2[0] and i[2] == j:
                            return "no", self.l1, list2
            return "error: not clear", [], []
        else:
            return "no", self.l1, list2


def answers(
    wh_cat,
    obj1,
    atr1,
    obj2,
    atr2,
    relation,
    repeat_obj,
    repeat_atr_obj,
    file,
    filename,
    synm,
    plu,
):
    ans = find_answer(
        obj1,
        atr1,
        obj2,
        atr2,
        relation,
        repeat_obj,
        repeat_atr_obj,
        file,
        filename,
        synm,
        plu,
    )
    if wh_cat == "counting":
        return ans.counting(filename)
    if wh_cat == "query_color":
        return ans.query_atr("color", filename)
    if wh_cat == "query_height":
        return ans.query_atr("height", filename)
    if wh_cat == "query_size":
        return ans.query_atr("size", filename)
    if wh_cat == "location":
        return ans.location(filename)
    if wh_cat == "existence":
        return ans.existance(filename)
    if wh_cat == "compare_integer":
        return ans.integer_comparison(filename)
    if wh_cat == "compare_attribute":
        return ans.compare_atr(filename)

