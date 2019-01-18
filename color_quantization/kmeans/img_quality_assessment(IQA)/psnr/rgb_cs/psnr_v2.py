"""
image quality assessment (IQA) of the quantized images and the original image in RGB color space
----- method: PSNR
----- version 2.0 (create PSNR function)
"""


import numpy as np
from PIL import Image
import glob
import csv
import math


# ---- define PSNR function based on its definition
# ---- reference: https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
def psnr(temp_img, quantized_img):
    R = temp_img[:,:,0] - quantized_img[:,:,0]
    G = temp_img[:,:,1] - quantized_img[:,:,1]
    B = temp_img[:,:,2] - quantized_img[:,:,2]

    mser = R * R
    mseg = G * G
    mseb = B * B
    temp_width = temp_img.shape[0]
    temp_height = temp_img.shape[1]
    SUM = np.sum(mser) +np.sum(mseg) + np.sum(mseb)

    MSE = SUM / (temp_width * temp_height * 3)
    PSNR = 10 * math.log((255.0 * 255.0 / (MSE)), 10)
    return PSNR


# ---- obtain the original and quantized images
temp_img = np.array(Image.open('../../../../img/sky.jpg'))
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../../img/sky/rgb_cs/quantized_img/*.png')
quantized_img_path_list.sort()

# ---- compute PSNR
score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    score = psnr(temp_img, quantized_img)
    score_list.append(score)
print(score_list)

# ---- save psnr score to csv file
csvfile = "sky_psnr_v2.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])
