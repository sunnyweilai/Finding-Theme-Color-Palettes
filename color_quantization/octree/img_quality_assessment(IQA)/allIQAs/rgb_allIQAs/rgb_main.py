#-*- coding: utf-8 -*-
"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR
----- method: SSIM / version 1.0 (skimage library) / http://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
----- method: gmsd ("sporco" library) / reference:Gradient Magnitude Similarity Deviation: An Highly Efficient Perceptual Image Quality Index / https://arxiv.org/pdf/1308.3052.pdf
----- method: VIF / version 1.0 (VIF function written by Alex Izvorski) / https://github.com/aizvorski/video-quality/blob/master/vifp.py
"""
from PIL import Image
import numpy as np
from rgb_color import RGB_Color
from rgb_quantizer import OctreeQuantizer
from rgb_4IQAs import psnr_list,ssim_list,gmsd_list,vif_list
from pandas.core.frame import DataFrame



#  ---- insert all colors of image into octree
def octree_quantize(image,num):

    pixels = image.load()
    width, height = image.size

    octree = OctreeQuantizer()

    # ---- add colors to octree
    for j in xrange(height):
        for i in xrange(width):
            octree.add_color(RGB_Color(*pixels[i, j]))

    # ---- 256 colors for "num" bits per pixel output image
    palette_object= octree.make_palette(num)

    # ---- save output image
    out_image = Image.new('RGB', (width, height))
    out_pixels = out_image.load()
    for j in xrange(height):
        for i in xrange(width):
            index = octree.get_palette_index(RGB_Color(*pixels[i, j]))
            color = palette_object[index]
            out_pixels[i, j] = (color.red, color.green, color.blue)

    quantized_raster = np.array(out_image)
    rescale_quantized_raster = quantized_raster / 255.0

    return rescale_quantized_raster



def main():
    # ---- open the reference image
    rgb_img = Image.open('../../../../img/img10.jpg')
    n_colors_list = range(1, 21)

    testimg_list = []
    for i in n_colors_list:
        result = octree_quantize(rgb_img, i)
        testimg_list.append(result)

    # ---- rescale the reference image into [0,1]
    rgb_raster = np.array(rgb_img)
    rescale_rgb_raster = rgb_raster / 255.0

    # ---- compute 4 IQAs
    PSNR_score_list = psnr_list(rescale_rgb_raster, testimg_list)
    SSIM_score_list = ssim_list(rescale_rgb_raster, testimg_list)
    VIF_score_list = vif_list(rescale_rgb_raster, testimg_list)
    GMSD_score_list = gmsd_list(rescale_rgb_raster, testimg_list)

    # ----- build the framework and save csv
    score_dic = {"PSNR": PSNR_score_list, "SSIM": SSIM_score_list, "VIF": VIF_score_list, "GMSD": GMSD_score_list}
    score_table = DataFrame(score_dic)
    score_table.to_csv('rgb_results/10score_table.csv')

if __name__ == '__main__':
    main()


