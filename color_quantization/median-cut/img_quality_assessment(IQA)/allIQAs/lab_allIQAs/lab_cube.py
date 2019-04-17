# -*- coding: UTF-8 -*-
"""Build 2 different L*a*b* color cubes to achieve the median-cut algorithm
---- reference: "颜色量化中位切割法" written by perry0528
---- https: // blog.csdn.net / perry0528 / article / details / 83048388
"""

"""
Human eyes are most sensitive to luma information which represents brightness in an image,
therefore I built the 2nd color cube with this consideration to compare with the 1st one.
"""
from statistics import mean

# ---- build the original median-cut color cube
class LAB_Cube_1(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.L = [l[0] for l in colors]
        self.A = [a[1] for a in colors]
        self.B = [b[2] for b in colors]

        self.size = (max(self.L) - min(self.L),
                     max(self.A) - min(self.A),
                     max(self.B) - min(self.B))
        self.range = max(self.size)
        self.channel = self.size.index(self.range)

    def __lt__(self, other):
        return self.range < other.range

    # ---- get the mean L*a*b* color of the cube
    def average(self):
        l = int(mean(self.L))
        a = int(mean(self.A))
        b = int(mean(self.B))
        return l, a, b

    # ---- split the cube into 2 subcubes from the middle of the channel with the maximum range
    def split(self):
        middle = int(len(self.colors) / 2)
        colors = sorted(self.colors, key=lambda c: c[self.channel])
        return LAB_Cube_1(colors[:middle]), LAB_Cube_1(colors[middle:])

# ---- build the new median-cut L*a*b* color cube
class LAB_Cube_2(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.L = [l[0] for l in colors]
        self.A = [a[1] for a in colors]
        self.B = [b[2] for b in colors]

        # ---- increase the range of the L* channel in order to increase the cube-split from the  L* channel
        added_L = (max(self.L) - min(self.L))*1.5
        self.size = (added_L,
                     max(self.A) - min(self.A),
                     max(self.B) - min(self.B))
        self.range = max(self.size)
        self.channel = self.size.index(self.range)

    def __lt__(self, other):
        return self.range < other.range

    # ---- get the mean L*a*b* color of the cube
    def average(self):
        l = int(mean(self.L))
        a = int(mean(self.A))
        b = int(mean(self.B))
        return l, a, b

    # ---- split the cube into 2 subcubes from the middle of the channel with the maximum range
    def split(self):
        middle = int(len(self.colors) / 2)
        colors = sorted(self.colors, key=lambda c: c[self.channel])
        return LAB_Cube_2(colors[:middle]), LAB_Cube_2(colors[middle:])

