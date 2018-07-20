import numpy as np
import scipy.misc
from PIL import Image
import glob
import csv
import math


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



temp_img = np.array(Image.open('../../../img/sky.jpg'),'f')
quantized_img_path_list = []
quantized_img_path_list = glob.glob(r'../../img/sky/quantized_img/*.png')
quantized_img_path_list.sort()

score_list = []
for i in quantized_img_path_list:
    quantized_img = np.array(Image.open(i),'f')
    score = psnr(temp_img, quantized_img)
    score_list.append(score)
print(score_list)

# save psnr score to csv file
csvfile = "sky_psnr.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in score_list:
        writer.writerow([val])
