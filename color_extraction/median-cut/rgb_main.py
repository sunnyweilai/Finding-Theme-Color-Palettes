# -*- coding: UTF-8 -*-
from PIL import Image
from rgb_cube import Cube
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors



# implement median-cut
def median_cut(img, num):
    ori_arr = np.array(img)
    rows, cols, channel = ori_arr.shape
    colors = []
    for count, color in img.getcolors(img.width * img.height):
        colors += [color]
    print(colors)
    cubes = [Cube(colors)]
    # print((cubes))
    while len(cubes) < num:
        cubes.sort()
        cubes += cubes.pop().split()

    LUT = {}
    for c in cubes:
        print(type(c))
        average = c.average()
        for color in c.colors:
            LUT[color] = average
    quant_arr = ori_arr
    for i in range(rows):
        for j in range(cols):
            index = (quant_arr[i, j, 0], quant_arr[i, j, 1], quant_arr[i, j, 2])
            new_color = LUT[index]
            quant_arr[i, j] = new_color
    image = Image.fromarray(quant_arr.astype(np.uint8))
    image.save("img/sky/rgb_cs/quantized_img/img_quantized%02d.png" % num)

    # extract palette using pandas
    LUT_df = pd.DataFrame.from_dict(LUT, orient = 'index',columns = ['R','G','B'])
    palette = LUT_df.drop_duplicates(subset=['R','G','B']).values
    print(palette)
    # visualize color them palette
    rgb_palette = palette / 255.0
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    # plt.show()
    plt.savefig('img/sky/rgb_cs/quantized_palette_v2/img_palette%02d.png' % num)



# open the reference image
original_img= Image.open('../img/sky.jpg')

# obtain color themes
def main() :
    for n_colors in [5]:
         median_cut(original_img, n_colors)

if __name__ == "__main__":
    main()



# ---------------------
# 作者：perry0528
# 来源：CSDN
# 原文：https://blog.csdn.net/perry0528/article/details/83048388
# 版权声明：本文为博主原创文章，转载请附上博文链接！