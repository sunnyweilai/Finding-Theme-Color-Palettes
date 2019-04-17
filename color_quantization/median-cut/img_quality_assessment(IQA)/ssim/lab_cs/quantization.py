# -*- coding: UTF-8 -*-
"""
Using median-cut algorithm to extract color themes (1-20) from the "sky" image in L*a*b* color space
---- reference:  "color quantization"
---- https://www.cs.tau.ac.il/~dcor/Graphics/cg-slides/color_q.pdf
"""
from lab_cube import LAB_Cube_1
import skimage
import numpy as np


# ---- implement median-cut
def median_cut(img, num):
    # ---- convert the RGB array of the original image into L*a*b* color space
    ori_arr = np.array(img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)
    rows, cols, channel = ori_arr_lab.shape

    # ---- obtain all L*a*b* color information of the original image
    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple, color))
    cubes = [LAB_Cube_1(colors)]

    # ---- split the color cube into "num" small color cubes
    # ---- reference: "颜色量化中位切割法" written by perry0528
    # ---- https: // blog.csdn.net / perry0528 / article / details / 83048388
    while len(cubes) < num:
        cubes.sort()
        cubes += cubes.pop().split()

    # ---- get the mean L*a*b* color of each cube and the color palette
    LUT = {}
    for c in cubes:
        c.average()
        average = c.average()
        for color in c.colors:
            LUT[color] = average

    # ---- using color palette to get the quantized image array and save it
    quant_arr = ori_arr_lab
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color

    # rescale float to [0,1]
    rescale_quant = (quant_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant

