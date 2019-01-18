"""
image quality assessment (IQA) of the quantized images and the original image in L*a*b* color space
----- method: PSNR

"""
import numpy as np
import csv
import math
from sklearn.cluster import KMeans
import scipy.misc
from skimage import color,data,img_as_uint


# ---- convert the original image from rgb to L*a*b* color space
rgb_raster = scipy.misc.imread('../../../../img/sky.jpg')
lab_raster = color.rgb2lab(rgb_raster)

# ---- define the quantization function
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

# ---- define PSNR method
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    # ---- 16 bits per pixel in lab color space
    PIXEL_MAX = 1
    return 10 * math.log10((PIXEL_MAX)**2 / mse)


# ---- obtain quantized images in L*a*b* color space
n_colors_list = range(1,21)
testimg_list = []
for i in n_colors_list:
    result = quantize(lab_raster, i)
    testimg_list.append(result)

# ---- rescale original raster
rescale_ori= (lab_raster + [0, 128, 128]) / [100, 255, 255]

# ---- compute PSNR in L*a*b* color space arrays
score_list = []
for i in testimg_list:
    score = psnr(rescale_ori, i)
    score_list.append(score)
print(score_list)

# ---- save PSNR score to csv file
csvfile = "sky_psnr_in_lab.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])









