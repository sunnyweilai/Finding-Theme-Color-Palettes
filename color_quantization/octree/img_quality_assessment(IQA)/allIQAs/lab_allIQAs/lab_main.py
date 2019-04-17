#-*- coding: utf-8 -*-
"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR
----- method: SSIM / version 1.0 (skimage library) / http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
----- method: gmsd ("sporco" library) / reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index / https://arxiv.org/pdf/1308.3052.pdf
----- method: VIF / version 1.0 (VIF function written by Alex Izvorski) / https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""

from __future__ import division
from PIL import Image
from skimage import color

import numpy as np
import skimage
from lab_color import LAB_Color
from lab_quantizer import OctreeQuantizer
import math
from lab_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list
from pandas.core.frame import DataFrame

#  ---- insert all colors of image into octree
def octree_quantize(image, num):
    ori_arr = np.array(image)

    # ---- convert to L*a*b* colorspace
    lab_arr = skimage.color.rgb2lab(ori_arr)
    ori_arr_lab = lab_arr.astype(int)
    width, height = image.size

    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple, color))

    # ---- add colors to octree
    octree = OctreeQuantizer()
    colors_length = len(colors)
    for i in xrange(colors_length):
        octree.add_color(LAB_Color(colors[i]))

    # ---- get the color palette of the original image
    palette_object = octree.make_palette(num)


    # ----- get the quantized image
    quantized_arr = np.ones((width, height, 3))
    for j in xrange(colors_length):
        index = octree.get_palette_index(LAB_Color(colors[j]))
        color = palette_object[index]
        h = (j + 1) % width - 1
        if h == -1:
            h = width - 1
        v = int(math.ceil((j + 1) / width)) - 1

        quantized_arr[h, v] = [color.L, color.A, color.B]

    new_quantized_arr = quantized_arr.transpose((1, 0, 2))

    rescale_quantized_arr = (new_quantized_arr + [0, 128, 128]) / [100, 255, 255]



    return rescale_quantized_arr



def main():
    # ---- open the reference image
    rgb_img = Image.open('../../../../img/img01.jpg')
    n_colors_list = range(1, 21)

    testimg_list = []
    for i in n_colors_list:
        result = octree_quantize(rgb_img, i)
        testimg_list.append(result)

    # ---- rescale the reference image into [0,1]
    rgb_raster = np.array(rgb_img)
    lab_raster = skimage.color.rgb2lab(rgb_raster)
    rescale_lab_raster = (lab_raster + [0, 128, 128]) / [100, 255, 255]

    # ---- compute 4 IQAs
    PSNR_score_list, L_PSNR_score_list = psnr_list(rescale_lab_raster, testimg_list)
    SSIM_score_list, L_SSIM_score_list = ssim_list(rescale_lab_raster, testimg_list)
    VIF_score_list = vif_list(rescale_lab_raster, testimg_list)
    GMSD_score_list = gmsd_list(rescale_lab_raster, testimg_list)

    # ----- build the framework and save csv
    score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
    score_table = DataFrame(score_dic)
    score_table.to_csv('lab_results/01score_table.csv')

    # ----  build L* and lab framework
    l_score_dic = {"PSNR": PSNR_score_list, "L_PSNR": L_PSNR_score_list, "SSIM": SSIM_score_list,
                   "L_SSIM": L_SSIM_score_list}
    l_score_table = DataFrame(l_score_dic)
    l_score_table.to_csv('lab_results/L_compare_10/01_L_score.csv')

if __name__ == '__main__':
    main()