from PIL import Image
from skimage import color
from lab_cube import LAB_Cube_2
import skimage
import numpy as np
import scipy.misc




# implement median-cut
def median_cut(img, num):
    ori_arr = np.array(img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)
    rows, cols, channel = ori_arr_lab.shape
    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple,color))
    cubes = [LAB_Cube_2(colors)]

    while len(cubes) < num:
        cubes.sort()
        cubes += cubes.pop().split()

    LUT = {}
    for c in cubes:
        c.average()
        average = c.average()
        for color in c.colors:
            LUT[color] = average

    quant_arr = ori_arr_lab
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color

    # rescale float to [0,1]
    rescale_quant = (quant_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant

