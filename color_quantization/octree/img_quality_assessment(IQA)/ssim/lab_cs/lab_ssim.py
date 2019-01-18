"""
image quality assessment (IQA) of the quantized images and the original image in  L*a*b* color space
----- method: SSIM
----- version 1.0 (skimage library)
----- http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
"""

from __future__ import division
from PIL import Image
import numpy as np
import skimage
from lab_color import LAB_Color
from lab_quantizer import OctreeQuantizer
import math
import csv
from skimage.measure import compare_ssim


#  ---- insert all colors of image into octree
def quantize_color(image, num):
    ori_arr = np.array(image)

    # ---- convert to L*a*b* colorspace
    lab_arr = skimage.color.rgb2lab(ori_arr)
    ori_arr_lab = lab_arr.astype(int)
    width, height = image.size

    # ---- get all colors of the original image
    colors = ()
    for color in ori_arr_lab:
        colors += tuple(map(tuple, color))

    # ---- add colors to octree
    octree = OctreeQuantizer()
    colors_length = len(colors)
    for i in xrange(colors_length):
        octree.add_color(LAB_Color(colors[i]))

    # ---- get the lab color palette of the original image
    palette_object = octree.make_palette(num)

    # ---- get the quantized image
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

    # ---- rescale float to [0,1]
    rescale_quant = (final_lab_arr + [0, 128, 128]) / [100, 255, 255]

    return rescale_quant


def main():
    original_img = Image.open('../../../../img/sky.jpg')

    testimg_list = []
    for n_colors in range(1, 21):
        lab_array = quantize_color(original_img, n_colors)
        testimg_list.append(lab_array)

    # ---- get lab original array
    ori_arr = np.array(original_img)
    ori_arr_lab = skimage.color.rgb2lab(ori_arr)

    # ---- rescale original raster
    rescale_ori = (ori_arr_lab + [0, 128, 128]) / [100, 255, 255]

    # ---- compare MSSIM
    score_list = []
    for i in testimg_list:
        score = compare_ssim(rescale_ori, i, multichannel=True)
        score_list.append(score)

    # ----- save ssim score to csv file
    csvfile = "ssim_lab.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in score_list:
            writer.writerow([val])

if __name__ == "__main__":
    main()