# -*- coding: utf8 -*-
"""
Using Octree algorithm to to extract color themes (1-20) from the "sky" image in RGB color space
---- reference:
---- 1. "八叉树颜色量化" written by TwinklingStar,http://www.twinklingstar.cn/2013/491/octree-quantization/
---- 2. "octree_color_quantizer" written by delimitry, https://github.com/delimitry/octree_color_quantizer
"""

from rgb_color import RGB_Color

class OctreeNode(object):
    """
    octree node class for quantization

    """

    def __init__(self,level, parent):
        """
        initialize new octree node

        :param level:
        :param parent:
        """
        self.color = RGB_Color(0,0,0)
        self.pixel_count = 0
        self.palette_index = 0
        self.children = [None for _ in xrange(8)]
        # add node to current level
        if level < OctreeQuantizer.MAX_DEPTH - 1:
            parent.add_level_node(level, self)

    def is_leaf(self):
        """
        check if the node is leaf
        :return:
        """
        return self.pixel_count > 0

    def get_leaf_nodes(self):
        """
        get all leaf nodes
        :return:
        """
        leaf_nodes = []
        for i in xrange(8):
            node = self.children[i]
            if node:
                if node.is_leaf():
                    leaf_nodes.append(node)
                else:
                    leaf_nodes.extend(node.get_leaf_nodes())
        return leaf_nodes

    def get_nodes_pixel_count(self):
        """
        get a sum of pixel count for node and its children

        :return:

        """
        sum_count = self.pixel_count
        for i in xrange(8):
            node = self.children[i]
            if node:
                sum_count += node.pixel_count
        return sum_count

    def add_color(self, color, level, parent):
        """
        Add `color` to the tree
        """
        if level >= OctreeQuantizer.MAX_DEPTH:
            self.color.red += color.red
            self.color.green += color.green
            self.color.blue += color.blue
            self.pixel_count += 1
            return
        index = self.get_color_index_for_level(color, level)
        if not self.children[index]:
            self.children[index] = OctreeNode(level, parent)
        self.children[index].add_color(color, level + 1, parent)

    def get_palette_index(self, color, level):
        """
        Get palette index for 'color'
        uses 'level' to go deeper if the node is not a leaf
        :param color:
        :param level:
        :return:
        """
        if self.is_leaf():
            return self.palette_index
        index = self.get_color_index_for_level(color, level)
        if self.children[index]:
            return self.children[index].get_palette_index(color, level+1)
        else:
            # get palette index for the first found child node
            for i in xrange(8):
                if self.children[i]:
                    return self.children[i].get_palette_index(color, level+1)

    def remove_leaves(self):
        """
        add all children pixels count and color channels to parent node
        :return: the number of removed leaves
        """
        result = 0
        for i in xrange(8):
            node = self.children[i]
            if node:
                self.color.red += node.color.red
                self.color.green += node.color.green
                self.color.blue += node.color.blue
                self.pixel_count += node.pixel_count
                result += 1
        return result - 1

    def get_color_index_for_level(self,color,level):
        """
        get index for next 'level'
        :param color:
        :param level:
        :return:

        """
        index = 0
        mask = 0x80 >> level
        if color.red & mask:
            index |= 4
        if color.green & mask:
            index |= 2
        if color.blue & mask:
            index |= 1
        return index

    def get_color(self):
        """
        Get average color
        :return:
        """
        return RGB_Color(
            self.color.red / self.pixel_count,
            self.color.green / self.pixel_count,
            self.color.blue / self.pixel_count)


class OctreeQuantizer(object):
    """
    Octree quantizer class for image quantization
    use MAX_DEPTH to limit a number of levels
    """

    MAX_DEPTH = 8

    def __init__(self):
        """
        init octree quantizer
        """
        self.levels = {i: [] for i in xrange(OctreeQuantizer.MAX_DEPTH)}
        self.root = OctreeNode(0, self)

    def get_leaves(self):
        """
        get all leaves
        :return:

        """
        return [node for node in self.root.get_leaf_nodes()]

    def add_level_node(self, level, node):
        """
        add 'node' to the nodes at 'level'
        :param level:
        :param node:
        :return:
        """
        self.levels[level].append(node)

    def add_color(self,color):
        """
        add 'color' to the Octree
        :param color:
        :return:
        """
    #  passes self value as 'parent' to save nodes to levels dict
        self.root.add_color(color, 0, self)

    def make_palette(self, color_count):
        """
        make color palette with 'color_count' colors maximum
        :param color_count:
        :return:
        """
        palette = []
        palette_index = 0
        leaf_count = len(self.get_leaves())
        """
        reduce nodes
        up to 8 colors can be reduced and the least number of colors should be 248
        """
        for level in xrange(OctreeQuantizer.MAX_DEPTH - 1, -1, -1):
            if self.levels[level]:
                for node in self.levels[level]:
                    leaf_count -= node.remove_leaves()
                    if leaf_count <= color_count:
                        break
                if leaf_count <= color_count:
                    break
                self.levels[level] = []
        # build palette
        for node in self.get_leaves():
            if palette_index >= color_count:
                break
            if node.is_leaf():
                palette.append(node.get_color())
            node.palette_index = palette_index
            palette_index += 1
        return palette

    def get_palette_index(self,color):
        """
        get palette index for 'color'
        :param color:
        :return:
        """
        return self.root.get_palette_index(color, 0)

