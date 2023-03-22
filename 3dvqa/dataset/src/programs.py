class functional_program:
    def __init__(self, qtype, attr1, obj1, rel, attr2, obj2, qsubj=None):
        super().__init__()

        self.heights = []
        self.volumes = []
        self.qtype = qtype
        self.qsubj = qsubj
        self.attr1 = attr1
        self.obj1 = obj1
        self.rel = rel
        self.attr2 = attr2
        self.obj2 = obj2

        self.colors = [
            "white",
            "black",
            "red",
            "blue",
            "green",
            "yellow",
            "grey",
            "purple",
            "brown",
            "orange",
            "cream",
            "beige",
            "pink",
        ]

        for i in ("small", "large", "medium"):
            self.volumes.append(i + " size")

        for i in ("short", "tall", "medium"):
            self.heights.append(i + " height")

        self.final_str = ""

        if self.obj1:
            self.final_str += "<select>:{} - ".format(self.obj1)
            self.flag = 0
            self.cmp1 = self.flag

        if self.attr1:
            if self.attr1 in self.colors:
                self.final_str += "<filter color>:{} [{}] - ".format(
                    self.attr1, self.flag
                )
            elif self.attr1 in self.heights:
                self.final_str += "<filter height>:{} [{}] - ".format(
                    self.attr1, self.flag
                )
            elif self.attr1 in self.volumes:
                self.final_str += "<filter volume>:{} [{}] - ".format(
                    self.attr1, self.flag
                )

            self.flag += 1
            self.cmp1 = self.flag

        if self.rel:
            self.final_str += "<relate>:{} [{}] - ".format(self.rel, self.flag)
            self.flag += 1

        if self.obj2:
            self.final_str += "<select>:{} - ".format(self.obj2)
            self.flag += 1
            self.cmp2 = self.flag

        if self.attr2:
            if self.attr2 in self.colors:
                self.final_str += "<filter color>:{} [{}] - ".format(
                    self.attr2, self.flag
                )
            elif self.attr2 in self.heights:
                self.final_str += "<filter height>:{} [{}] - ".format(
                    self.attr2, self.flag
                )
            elif self.attr2 in self.volumes:
                self.final_str += "<filter volume>:{} [{}] - ".format(
                    self.attr2, self.flag
                )

            self.flag += 1
            self.cmp2 = self.flag

    def __call__(self):

        if self.qtype == "counting":
            self.final_str += "<count> [{}]".format(self.flag)

        elif self.qtype == "query_attribute":
            self.final_str += "<measure {}> [{}]".format(self.qsubj, self.flag)

        elif self.qtype == "location":
            self.final_str += "<get {}> [{}]".format(self.qtype, self.flag)

        elif self.qtype == "existence":
            self.final_str += "<existence> [{}]".format(self.flag)

        elif self.qtype == "compare_integer":
            self.final_str += "<compare_integer> [{}], [{}]".format(
                self.cmp1, self.cmp2
            )

        elif self.qtype == "compare_attribute":
            self.final_str += "<compare_attribute> [{}], [{}] ".format(
                self.cmp1, self.cmp2
            )

        return self.final_str
