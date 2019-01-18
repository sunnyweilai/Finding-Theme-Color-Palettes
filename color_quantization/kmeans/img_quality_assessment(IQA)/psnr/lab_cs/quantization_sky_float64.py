import numpy as np
import csv
import cv2
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data


# ---- convert to lab color space to do kmeans
rgb_raster = scipy.misc.imread('../../../../img/sky.jpg')
lab_raster = color.rgb2lab(rgb_raster)


# ---- extract dominant color in the image
def quantize(raster, n_colors):
    width, height,depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    # ---- rescale float to [0,1]
    rescale_quant = (quantized_raster + [0, 128, 128]) / [100, 255, 255]
    return rescale_quant

# ---- PSNR method
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    # 16 bits per pixel in lab color space
    PIXEL_MAX = 1
    return 10 * math.log10((PIXEL_MAX)**2 / mse)

# ---- color themes with from 1-20 colors
n_colors_list = range(1,21)
testimg_list = []
for i in n_colors_list:
    result = quantize(lab_raster, i)
    testimg_list.append(result)

# ---- rescale original raster to [0,1]
rescale_ori= (lab_raster + [0, 128, 128]) / [100, 255, 255]








