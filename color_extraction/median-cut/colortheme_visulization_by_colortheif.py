from PIL import Image
from colorthief import ColorThief
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
import numpy as np




# build a color palette
# for n_colors in range(1,21):
def theme_visualiztion(color_thief,n_colors):
    # get the dominant color
    # dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count= n_colors)
    palette_arr = np.asarray(palette)
    for RGB in palette_arr:
        np.asarray(RGB)

    # visualize color them palette
    rgb_palette = palette_arr / 255.0
    img_palette = mcolors.ListedColormap(rgb_palette)
    plt.figure(figsize=(n_colors, 0.5))
    plt.title('color theme')
    plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    plt.gca().yaxis.set_visible(False)
    plt.gca().set_xlim(0, img_palette.N)
    plt.axis('off')
    # plt.show()
    plt.savefig('img/sky/rgb_cs/quantized_palette_by_colorthief/img_palette%02d.png' % n_colors)

# use colorthief (median-cut algorithm) to extract
color_thief = ColorThief('../img/sky.jpg')
n_colors = 2
while n_colors < 21:
    theme_visualiztion(color_thief, n_colors)
    n_colors +=1

# for n_colors in range(1,21):
# theme_visualiztion(color_thief,5)