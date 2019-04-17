# -*- coding: UTF-8 -*-
"""
Using median-cut algorithm to extract color themes (1-20) from the "sky" image in L*a*b* color space
---- reference:  "color quantization"
---- https://www.cs.tau.ac.il/~dcor/Graphics/cg-slides/color_q.pdf
"""
from PIL import Image
from skimage import color
from lab_cube import LAB_Cube_2
import numpy as np
import skimage
import pandas as pd
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
# get the run time
import datetime

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

    # ---- using color palette to get the quantized image array and save it
    quant_arr = ori_arr_lab
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color

    new_rgb_raster = skimage.color.lab2rgb(quant_arr) * 255
    image = Image.fromarray(new_rgb_raster.astype(np.uint8))
    image.save("img/img10/lab_cs/quantized_img_#2/img_quantized%02d.png" % num)

    # ---- extract palette using pandas
    LUT_df = pd.DataFrame.from_dict(LUT, orient = 'index',columns = ['L','A','B'])
    lab_palette = LUT_df.drop_duplicates(subset=['L','A','B']).values

    # ---- transform to 3d array to do the color space conversion
    lab_array = np.asarray([lab_palette])
    new_lab_palette = lab_array.astype(float)
    back2rgb_palette = skimage.color.lab2rgb(new_lab_palette)

    # ---- transform back to 2d array in order to do the palette visualization
    rgb_palette = []
    for rgb in back2rgb_palette[0]:
        rgb_palette.append(rgb)

    # ----- visualize color them palette
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img10/lab_cs/quantized_palette_#2/img_palette%02d.png' % num)


# start timer
start = datetime.datetime.now()
# ---- obtain color themes
def main() :
    # open the reference image
    original_img = Image.open('../img/img10.jpg')
    for n_colors in range(10,21):
        median_cut(original_img, n_colors)

if __name__ == "__main__":
    main()
# end timer
end = datetime.datetime.now()
print (end-start)

