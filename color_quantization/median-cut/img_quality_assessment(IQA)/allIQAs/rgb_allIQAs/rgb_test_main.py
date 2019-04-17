#-*- coding: utf-8 -*-
"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR
----- method: SSIM / version 1.0 (skimage library) / http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
----- method: gmsd ("sporco" library) / reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index / https://arxiv.org/pdf/1308.3052.pdf
----- method: VIF / version 1.0 (VIF function written by Alex Izvorski) / https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""
import numpy as np
from skimage import color,data
from PIL import Image
import csv
import math
import sporco.metric
from skimage import color
from rgb_cube import Cube
from rgb_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list
from pandas.core.frame import DataFrame
import scipy.misc

import os.path



def open_pics(path_pics):
    files =os.listdir(path_pics)
    files.sort()
    pic_list = []
    for file in files:
        if file.endswith('jpg'):
            new_path = path_pics + '/' + str(file)
            pic_list.append((int(str(file)[:2]),new_path))
    return pic_list



# ---- implement median-cut algorithm
def median_cut(img, num):
    ori_arr = np.array(img)
    rows, cols, channel = ori_arr.shape

    # ---- get the RGB color array of the original image
    colors = []
    for count, color in img.getcolors(img.width * img.height):
        colors += [color]
    # print(colors)
    cubes = [Cube(colors)]
    # print((cubes))

    # ---- split the color cube into "num" small color cubes
    # ---- reference: "颜色量化中位切割法" written by perry0528
    # ---- https: // blog.csdn.net / perry0528 / article / details / 83048388
    while len(cubes) < num:
        cubes.sort()
        cubes += cubes.pop().split()

    # ---- get the mean RGB color of each cube and the color palette
    LUT = {}
    for c in cubes:
        # print(type(c))
        average = c.average()
        for color in c.colors:
            LUT[color] = average

    # ---- using color palette to get the quantized image array and save it
    quant_arr = ori_arr
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color

    # ---- rescale quantized array into [0,1]
    rescale_quant_arr = quant_arr / 255.0

    return rescale_quant_arr

def main() :
    path_pics = '../../../../img/test_image'
    pic_list = open_pics(path_pics)
    for pic_nam,pic_path in pic_list:

        # ---- open the reference image
        rgb_img = Image.open(pic_path)
        n_colors_list = range(1, 21)

        testimg_list = []
        for i in n_colors_list:
            result = median_cut(rgb_img, i)
            testimg_list.append(result)

        # ---- rescale the reference image into [0,1]
        rgb_raster = np.array(rgb_img)
        rescale_rgb_raster = rgb_raster / 255.0

        # ---- compute 4 IQAs
        PSNR_score_list = psnr_list(rescale_rgb_raster,testimg_list)
        SSIM_score_list = ssim_list(rescale_rgb_raster,testimg_list)
        VIF_score_list  = vif_list(rescale_rgb_raster,testimg_list)
        GMSD_score_list = gmsd_list(rescale_rgb_raster,testimg_list)

        # ----- build the framework and save csv
        score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
        score_table = DataFrame(score_dic)
        score_table.to_csv('rgb_results/rgb_50/%02dscore_table.csv' % pic_nam)




if __name__ == "__main__":
    main()

