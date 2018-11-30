# -*- coding: UTF-8 -*-
from PIL import Image
from skimage import color

import numpy as np
import skimage
import pandas as pd
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from lab_color import LAB_Color
from lab_quantizer import OctreeQuantizer


# implement median-cut
def median_cut(img, num):
    ori_arr = np.array(img)
    ori_arr_lab = np.array(skimage.color.rgb2lab(ori_arr),dtype=int)


    width, height = img.size

    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple, color))
    print(colors[1])

    # add colors to octree
    octree = OctreeQuantizer()
    for i in xrange(len(colors)):
        octree.add_color(LAB_Color(colors[i]))
    #
    #
    print(octree)

    # # 256 colors for "num" bits per pixel output image
    # palette_object = octree.make_palette(num)
    #
    # # save output image
    # out_image = Image.new('LAB', (width, height))
    # out_pixels = out_image.load()
    # for j in xrange(height * width):
    #     index = octree.get_palette_index(LAB_Color(*colors[i]))
    #     color = palette_object[index]
    #     out_pixels[i, j] = (color.L, color.A, color.B)
    # out_image.save('img/sky/lab_cs/quantized_img/img%02d.png' % num)
    # rows, cols, channel = ori_arr_lab.shape
    # colors = ()
    # for color in ori_arr_lab:
    #     colors += tuple(map(tuple,color))
    # cubes = [LAB_Cube_2(colors)]
    #
    # while len(cubes) < num:
    #     cubes.sort()
    #     cubes += cubes.pop().split()
    #
    # LUT = {}
    # for c in cubes:
    #     c.average()
    #     average = c.average()
    #     for color in c.colors:
    #         LUT[color] = average
    # quant_arr = ori_arr_lab
    # for i in range(rows):
    #     for j in range(cols):
    #         index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
    #         new_color = LUT[index]
    #         quant_arr[i, j] = new_color
    #
    # new_rgb_raster = skimage.color.lab2rgb(quant_arr) * 255
    # image = Image.fromarray(new_rgb_raster.astype(np.uint8))
    # image.save("img/sky/lab_cs/added_L_quantized_img/img_quantized%02d.png" % num)





# obtain color themes
def main() :
    # open the reference image
    original_img = Image.open('../img/sky.jpg')
    for n_colors in [5]:
        median_cut(original_img, n_colors)

if __name__ == "__main__":
    main()



# ---------------------
# 作者：perry0528
# 来源：CSDN
# 原文：https://blog.csdn.net/perry0528/article/details/83048388
# 版权声明：本文为博主原创文章，转载请附上博文链接！