#-*- coding: utf-8 -*-
"""
Using median-cut algorithm to extract color themes (1-20) from the "sky" image in RGB color space
---- reference:  "color quantization"
---- https://www.cs.tau.ac.il/~dcor/Graphics/cg-slides/color_q.pdf
"""
from PIL import Image
from rgb_cube import Cube
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
# get the run time
import datetime

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
    image = Image.fromarray(quant_arr.astype(np.uint8))
    image.save("img/img10/rgb_cs/quantized_img/img_quantized%02d.png" % num)

    # ----extract palette using pandas
    LUT_df = pd.DataFrame.from_dict(LUT, orient = 'index',columns = ['R','G','B'])
    palette = LUT_df.drop_duplicates(subset=['R','G','B']).values

    # ----visualize color theme palette
    rgb_palette = palette / 255.0
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    plt.savefig('img/img10/rgb_cs/quantized_palette/img_palette%02d.png' % num)

# start timer
start = datetime.datetime.now()

# ---- open the reference image
original_img= Image.open('../img/img10.jpg')

# ---- obtain color themes
def main() :
    for n_colors in range(1,21):
         median_cut(original_img, n_colors)


if __name__ == "__main__":
    main()
# end timer
end = datetime.datetime.now()
print (end-start)

