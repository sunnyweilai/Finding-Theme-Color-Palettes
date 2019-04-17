# -*- coding: utf8 -*-
"""
Using Octree algorithm to to extract color themes (1-20) from the "sky" image in RGB color space
---- reference:
---- 1. "八叉树颜色量化" written by TwinklingStar,http://www.twinklingstar.cn/2013/491/octree-quantization/
---- 2. "octree_color_quantizer" written by delimitry, https://github.com/delimitry/octree_color_quantizer
"""
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from rgb_color import RGB_Color
from rgb_quantizer import OctreeQuantizer
# get the run time
import datetime

#  ---- insert all colors of image into octree
def quantize_color(path,num):
    image = Image.open(path)
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
    out_image.save('img/img08/rgb_cs/quantized_img/img%02d.png' % num)

    # ---- get the RGB color palette array
    rgb_palette = []
    for color in palette_object:
        R = color.red / 255.0
        G = color.green / 255.0
        B = color.blue / 255.0
        rgb = [R,G,B]
        rgb_palette.append(rgb)

    # ---- visualize color them palette
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img08/rgb_cs/quantized_palette/img_palette%02d.png' % num)

# start timer
start = datetime.datetime.now()
def main():
    for i in [20]:
        quantize_color('../img/img08.jpg',i)

if __name__ == '__main__':
    main()

# end timer
end = datetime.datetime.now()
print (end-start)
