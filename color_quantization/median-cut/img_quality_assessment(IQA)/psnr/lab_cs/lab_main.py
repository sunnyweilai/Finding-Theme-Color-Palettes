# -*- coding: UTF-8 -*-
"""
image quality assessment (img_quality_assessment(img_quality_assessment(IQA))) of the quantized images and the original image in L*a*b* color space
----- method: PSNR

"""

from PIL import Image
from skimage import color
from lab_cube import LAB_Cube_2 # I also imported LAB_Cube_2 to get the PSNR result of the 2nd color cube
import skimage
import numpy as np
import csv
import math


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
    cubes = [LAB_Cube_2(colors)]

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
    # ---- using color palette to get the quantized image array
    quant_arr = ori_arr_lab
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color

    # ---- rescale float to [0,1]
    rescale_quant = (quant_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant


# ---- PSNR method
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    # ---- 16 bits per pixel in lab color space
    PIXEL_MAX = 1
    return 10 * math.log10((PIXEL_MAX)**2 / mse)

# ----- obtain color themes
def main() :
    # ---- open the reference image
    original_img = Image.open('../../../../img/sky.jpg')

    testimg_list = []
    for n_colors in range(1, 21):
        lab_array = median_cut(original_img, n_colors)
        testimg_list.append(lab_array)

    # ---- get lab original array
    ori_arr = np.array(original_img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)

    # ---- rescale original raster
    rescale_ori = (ori_arr_lab + [0, 128, 128]) / [100, 255, 255]

    # ---- compare PSNR
    score_list = []
    for i in testimg_list:
        score = psnr(rescale_ori[:,:,0], i[:,:,0])
        score_list.append(score)

    # ---- save PSNR score to csv file
    csvfile = "added_L_psnr_lab_L.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in score_list:
            writer.writerow([val])


if __name__ == "__main__":
    main()

