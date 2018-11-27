from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from color import Color
from quantizer import OctreeQuantizer


#  insert all colors of image into octree
def add_color(path,num):
    image = Image.open(path)
    pixels = image.load()
    width, height = image.size

    octree = OctreeQuantizer()

    # add colors to octree
    for j in xrange(height):
        for i in xrange(width):
            octree.add_color(Color(*pixels[i, j]))

    # 256 colors for "num" bits per pixel output image
    palette_object= octree.make_palette(num)
    # save output image
    # out_image = Image.new('RGB', (width, height))
    # out_pixels = out_image.load()
    # for j in xrange(height):
    #     for i in xrange(width):
    #         index = octree.get_palette_index(Color(*pixels[i, j]))
    #         color = palette_object[index]
    #         out_pixels[i, j] = (color.red, color.green, color.blue)
    # out_image.save('img/sky/rgb_cs/quantized_img/img%02d.png' % num)

    # get the RGB color palette array
    rgb_palette = []
    for color in palette_object:
        R = color.red / 255.0
        G = color.green / 255.0
        B = color.blue / 255.0
        rgb = [R,G,B]
        rgb_palette.append(rgb)
    # print(rgb_palette)

    # make palette for 256 colors and save it to files
    # palette_image = Image.new('RGB', (16, 16))
    # palette_pixels = palette_image.load()
    # for i, color in enumerate(palette):
    #     palette_pixels[i % 16, i / 16] = (color.red, color.green, color.blue)
    # palette_image.save('universe_palette.png')

    # visualize color them palette

    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(num, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    # plt.show()
    plt.savefig('img/sky/rgb_cs/quantized_palette/img_palette%02d.png' % num)


def main():
    for i in range(10,21):
        add_color('../img/sky.jpg',i)

if __name__ == '__main__':
    main()