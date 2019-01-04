from __future__ import division
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
import math
import csv





#  insert all colors of image into octree
def quantize_color(image, num):
    ori_arr = np.array(image)

    # convert to L*a*b* colorspace
    lab_arr = skimage.color.rgb2lab(ori_arr)
    ori_arr_lab = lab_arr.astype(int)
    width, height = image.size


    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple, color))


    # add colors to octree
    octree = OctreeQuantizer()
    colors_length = len(colors)
    for i in xrange(colors_length):
        octree.add_color(LAB_Color(colors[i]))


    # 256 colors for "num" bits per pixel output image
    palette_object = octree.make_palette(num)

    # get the quantized image
    quantized_arr = np.ones((width,height,3))
    for j in xrange(colors_length):
        index = octree.get_palette_index(LAB_Color(colors[j]))
        color = palette_object[index]
        h = (j+1) % width - 1
        if h == -1:
            h = width -1
        v = int(math.ceil((j+1) / width )) - 1

        quantized_arr[h,v] = [color.L, color.A, color.B]

    final_lab_arr = quantized_arr.transpose((1,0,2))

    # rescale float to [0,1]
    rescale_quant = (final_lab_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant

# PSNR method
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    # 16 bits per pixel in lab color space
    PIXEL_MAX = 1
    return 10 * math.log10((PIXEL_MAX)**2 / mse)

def main():
    original_img = Image.open('../../../../img/sky.jpg')

    testimg_list = []
    for n_colors in range(1, 21):
        lab_array = quantize_color(original_img, n_colors)
        testimg_list.append(lab_array)

    # get lab original array
    ori_arr = np.array(original_img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)

    # rescale original raster
    rescale_ori = (ori_arr_lab + [0, 128, 128]) / [100, 255, 255]

    # compare PSNR
    score_list = []
    for i in testimg_list:
        score = psnr(rescale_ori, i)
        score_list.append(score)

    # save PSNR score to csv file
    csvfile = "psnr_lab.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in score_list:
            writer.writerow([val])

if __name__ == "__main__":
    main()