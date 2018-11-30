# -*- coding: UTF-8 -*-
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




#  insert all colors of image into octree
def quantize_color(image, num):
    ori_arr = np.array(image)
    print(ori_arr)
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
    # print(palette_object)

    # save output image
    # out_image = Image.new('RGB', (width, height))
    # out_arr = np.reshape(np.array(out_image),(width,height))
    # out_pixels = out_image.load()
    quantized_arr = np.ones((width,height,3))

    for j in xrange(colors_length):
        index = octree.get_palette_index(LAB_Color(colors[j]))
        color = palette_object[index]
        h = (j+1) % width - 1
        if h == -1:
            h = width -1
        v = int(math.ceil((j+1) / width )) - 1

        quantized_arr[h,v] = [color.L, color.A, color.B]

    new_rgb_arr = skimage.color.lab2rgb(quantized_arr) * 255
    f_rgb_arr = new_rgb_arr.transpose((1,0,2))
    quantized_image = Image.fromarray(f_rgb_arr.astype(np.uint8))
    quantized_image.save('img/sky/lab_cs/quantized_img/img%02d.png' % num)

def main():
    original_img = Image.open('../img/sky.jpg')
    quantize_color(original_img, 5)

if __name__ == "__main__":
    main()