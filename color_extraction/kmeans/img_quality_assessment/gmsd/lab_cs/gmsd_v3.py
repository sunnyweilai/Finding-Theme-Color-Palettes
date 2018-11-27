import numpy as np
import csv
import cv2
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data
import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math
import sporco.metric
from skimage import color



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

    # rescale float to [0,1]
    rescale_quant = (quantized_raster + [0, 128, 128]) / [100, 255, 255]
    return rescale_quant


# color themes with from 1-20 colors
n_colors_list = range(1,21)
testimg_list = []
for i in n_colors_list:
    result = quantize(lab_raster, i)
    testimg_list.append(result)


#resize original image array to 2d
lab_temp_img = (lab_raster + [0, 128, 128]) / [100, 255, 255]
lab_temp_width = lab_temp_img.shape[0]
lab_temp_height = lab_temp_img.shape[1]*lab_temp_img.shape[2]
lab_temp_img.resize((lab_temp_width,lab_temp_height))

# compute GMSD
score_list = []
for i in testimg_list:
    lab_quantized_width = i.shape[0]
    lab_quantized_height = i.shape[1]*i.shape[2]
    i.resize((lab_quantized_width,lab_quantized_height))
    score = sporco.metric.gmsd(lab_temp_img, i)
    score_list.append(score)


# save gmsd score to csv file
csvfile = "lab_sky_gmsd_v2.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])