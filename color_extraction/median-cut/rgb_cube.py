# -*- coding: UTF-8 -*-
from statistics import mean


class Cube(object):
    def __init__(self, colors):
        self.colors = colors or []
        self.red = [r[0] for r in colors]
        self.green = [g[1] for g in colors]
        self.blue = [b[2] for b in colors]
        self.size = (max(self.red) - min(self.red),
                     max(self.green) - min(self.green),
                     max(self.blue) - min(self.blue))
        self.range = max(self.size)
        self.channel = self.size.index(self.range)

    def __lt__(self, other):
        return self.range < other.range

    def average(self):
        r = int(mean(self.red))
        g = int(mean(self.green))
        b = int(mean(self.blue))
        return r, g, b

    def split(self):
        middle = int(len(self.colors) / 2)
        colors = sorted(self.colors, key=lambda c: c[self.channel])
        return Cube(colors[:middle]), Cube(colors[middle:])


# ---------------------
# 作者：perry0528
# 来源：CSDN
# 原文：https: // blog.csdn.net / perry0528 / article / details / 83048388
# 版权声明：本文为博主原创文章，转载请附上博文链接！