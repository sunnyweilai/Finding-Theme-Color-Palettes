import numpy as np
import csv
import cv2
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data,img_as_uint


# convert to lab color space to do kmeans
rgb_raster = scipy.misc.imread('../../../../img/sky.jpg')
lab_raster = color.rgb2lab(rgb_raster)

# extract dominant color in the image
def quantize(raster, n_colors):
    width, height,depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    model = KMeans(n_clusters=n_colors,random_state = 1)
    labels = model.fit_predict(reshaped_raster)
    palette = model.cluster_centers_

    quantized_raster = np.reshape(
        palette[labels], (width, height, palette.shape[1]))

    # convert float64 to uint16, !may cause precision loss
    uint16_res = quantized_raster.astype('uint16')

    # # rescale float to [0,1]
    # rescale_quant = (quantized_raster + [0, 128, 128]) / [100, 255, 255]
    # uint16_res = img_as_uint(rescale_quant)
    return uint16_res

# PSNR method
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    # 16 bits per pixel in lab color space
    PIXEL_MAX = 65535.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

# color themes with from 1-20 colors
n_colors_list = range(1,20)
testimg_list = []
for i in n_colors_list:
    result = quantize(lab_raster, i)
    testimg_list.append(result)

# rescale original raster
uint16_ori = lab_raster.astype('uint16')

# compare PSNR
score_list = []
for i in testimg_list:
    score = psnr(uint16_ori, i)
    score_list.append(score)
print(score_list)

# save PSNR score to csv file
csvfile = "psnr_lab_v1.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])









