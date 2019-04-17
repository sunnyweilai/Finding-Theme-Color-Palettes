#-*- coding: utf-8 -*-
"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR
----- method: SSIM / version 1.0 (skimage library) / http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
----- method: gmsd ("sporco" library) / reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index / https://arxiv.org/pdf/1308.3052.pdf
----- method: VIF / version 1.0 (VIF function written by Alex Izvorski) / https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""
from PIL import Image
from lab_cube import LAB_Cube_1
import numpy as np
from lab_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list
from pandas.core.frame import DataFrame
from skimage import color
import skimage

import scipy.misc


# ---- implement median-cut
def median_cut(img, num):

    # ---- convert the RGB array of the original image into L*a*b* color space
    ori_arr = np.array(img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)
    rows, cols, channel = ori_arr_lab.shape

    # ---- obtain all L*a*b* color information of the original image
    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple,color))
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

    # ---- rescale quantized array into [0,1]
    rescale_quant_arr = (quant_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant_arr




def main() :
    # ---- open the reference image
    rgb_img = Image.open('../../../../img/img01.jpg')
    n_colors_list = range(1, 21)

    testimg_list = []
    for i in n_colors_list:
        result = median_cut(rgb_img, i)
        testimg_list.append(result)

    # ---- rescale the reference image into [0,1]
    rgb_raster = np.array(rgb_img)
    lab_raster = skimage.color.rgb2lab(rgb_raster)
    rescale_lab_raster = (lab_raster + [0, 128, 128]) / [100, 255, 255]

    # ---- compute 4 IQAs
    PSNR_score_list, L_PSNR_score_list = psnr_list(rescale_lab_raster,testimg_list)
    SSIM_score_list, L_SSIM_score_list = ssim_list(rescale_lab_raster,testimg_list)
    VIF_score_list  = vif_list(rescale_lab_raster,testimg_list)
    GMSD_score_list = gmsd_list(rescale_lab_raster,testimg_list)

    # ----- build the framework and save csv
    score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
    score_table = DataFrame(score_dic)
    score_table.to_csv('#1lab_results/01score_table.csv')

    # ----  build L* and lab framework
    l_score_dic = {"PSNR": PSNR_score_list, "L_PSNR": L_PSNR_score_list, "SSIM": SSIM_score_list,"L_SSIM": L_SSIM_score_list}
    l_score_table = DataFrame(l_score_dic)
    l_score_table.to_csv('#1lab_results/L_compare_10/01_L_score.csv')




if __name__ == "__main__":
    main()


