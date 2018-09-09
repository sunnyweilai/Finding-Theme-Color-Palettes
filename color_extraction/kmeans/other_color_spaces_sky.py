"""
change RGB color space into other color spaces in order to improve the quantized image quality
"""

import numpy as np
import cv2
import colorsys
import skimage
from skimage import io
from sklearn.cluster import KMeans
from sklearn.datasets import load_sample_image
from sklearn import metrics
import scipy.misc
import matplotlib.pyplot as plt
import  matplotlib.colors as mcolors
from PIL import Image

#  image into rgb color space
image = io.imread('../img/universe.jpg')
rgb_cs = image
width, height, depth = original_shape = tuple(image.shape)
assert depth == 3

# other color spaces (hsv, ciexyz, cielab)
# lab_cs = cv2.cvtColor(rgb_cs,cv2.COLOR_BGR2HSV)
# hsv_array = np.reshape(lab_cs,(width * height,depth))

# ciexyz_cs = cv2.cvtColor(rgb_cs,cv2.COLOR_BGR2XYZ)
# ciexyz_cs_array = np.reshape(ciexyz_cs,(width * height,depth))
#
cielab_cs = cv2.cvtColor(rgb_cs,cv2.COLOR_BGR2LAB)
cielab_cs_array = np.reshape(cielab_cs,(width * height,depth))

# create kmeans models for each color space

def quantize(cs_arrary, n_colors):

    # create kmeans model
    model = KMeans(n_clusters = n_colors, random_state = 1)
    labels = model.fit_predict(cs_arrary)
    palette = model.cluster_centers_

    # reshape the picture based on the color theme (n colors)
    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1])
    )

    # save quantized_img and colortheme_palette
    quantized_image = Image.fromarray(quantized_raster.astype(np.uint8))
    quantized_image.save("img/sky/hsv_colorspace/img_quantized%s.png" % n_colors)

    # visualize color theme palette
    # rgb_palette = palette / 255.0
    # img_palette = mcolors.ListedColormap(rgb_palette)
    # plt.figure(figsize=(n_colors, 0.5))
    # plt.title('color theme')
    # plt.pcolormesh(np.arange(img_palette.N).reshape(1, -1), cmap=img_palette)
    # plt.gca().yaxis.set_visible(False)
    # plt.gca().set_xlim(0, img_palette.N)
    # # plt.show()
    # plt.savefig('img/sky/hsv_colorspace/img_palette%s.png' % n_colors)

    return quantized_image

hsv5 = quantize(cielab_cs_array,5)

