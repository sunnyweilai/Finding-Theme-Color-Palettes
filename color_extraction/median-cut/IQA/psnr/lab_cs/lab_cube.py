# -*- coding: UTF-8 -*-
from statistics import mean


class LAB_Cube_2(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.L = [l[0] for l in colors]
        self.A = [a[1] for a in colors]
        self.B = [b[2] for b in colors]
        added_L = (max(self.L) - min(self.L))*1.5
        self.size = (added_L,
                     max(self.A) - min(self.A),
                     max(self.B) - min(self.B))
        self.range = max(self.size)
        self.channel = self.size.index(self.range)

    def __lt__(self, other):
        return self.range < other.range

    def average(self):
        l = int(mean(self.L))
        a = int(mean(self.A))
        b = int(mean(self.B))
        return l, a, b

    def split(self):
        middle = int(len(self.colors) / 2)
        colors = sorted(self.colors, key=lambda c: c[self.channel])
        return LAB_Cube_2(colors[:middle]), LAB_Cube_2(colors[middle:])

class LAB_Cube_1(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.L = [l[0] for l in colors]
        self.A = [a[1] for a in colors]
        self.B = [b[2] for b in colors]

        added_L = (max(self.L) - min(self.L))
        self.size = (added_L,
                     max(self.A) - min(self.A),
                     max(self.B) - min(self.B))
        self.range = max(self.size)
        self.channel = self.size.index(self.range)

    def __lt__(self, other):
        return self.range < other.range

    def average(self):
        l = int(mean(self.L))
        a = int(mean(self.A))
        b = int(mean(self.B))
        return l, a, b

    def split(self):
        middle = int(len(self.colors) / 2)
        colors = sorted(self.colors, key=lambda c: c[self.channel])
        return LAB_Cube_1(colors[:middle]), LAB_Cube_1(colors[middle:])