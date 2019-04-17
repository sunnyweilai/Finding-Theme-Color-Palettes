# -*- coding: utf8 -*-
"""
Using Octree algorithm to to extract color themes (1-20) from the "sky" image in L*a*b* color space
---- reference:
---- 1. "八叉树颜色量化" written by TwinklingStar,http://www.twinklingstar.cn/2013/491/octree-quantization/
---- 2. "octree_color_quantizer" written by delimitry, https://github.com/delimitry/octree_color_quantizer
"""
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
# get the run time
import datetime

#  ---- insert all colors of image into octree
def quantize_color(image, num):
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
    lab_palette = []
    for i in palette_object:
         L = i.L
         A = i.A
         B = i.B
         lab = [L, A , B]
         lab_palette.append(lab)

    # ---- transform to 3d array to do the color space conversion
    lab_array = np.asarray([lab_palette])
    new_lab_palette = lab_array.astype(float)
    back2rgb_palette = skimage.color.lab2rgb(new_lab_palette)

    # ---- transform back to 2d array in order to do the palette visualization
    rgb_palette = []
    for rgb in back2rgb_palette[0]:
        rgb_palette.append(rgb)
    # print(rgb_palette)

    # ---- visualize color theme palette
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img01/lab_cs/quantized_palette/img_palette%02d.png' % num)

    # ----- get the quantized image
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
    quantized_image.save('img/img01/lab_cs/quantized_img/img%02d.png' % num)

# start timer
start = datetime.datetime.now()
def main():
    original_img = Image.open('../img/img01.jpg')
    for i in range(1, 21):
        quantize_color(original_img, i)

if __name__ == "__main__":
    main()

# end timer
end = datetime.datetime.now()
print (end-start)